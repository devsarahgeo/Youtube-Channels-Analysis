import os
import time
import json
import boto3
import requests
from datetime import datetime, timedelta
from typing import List
import requests
from dotenv import load_dotenv

load_dotenv()   # loads .env file

# ---------------- CONFIG ---------------- #
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
AWS_BUCKET = os.getenv("AWS_BUCKET")
AWS_PREFIX = "myyoutube/raw"
print(AWS_BUCKET)

SEARCH_TERMS = [
    "data analyst",
    "SQL tutorial",
    "Power BI",
    "Python for data analysis",
    "Data science projects"
]

MAX_CHANNELS = 120
VIDEOS_PER_CHANNEL = 100
SUBSCRIBER_MIN = 10_000
SUBSCRIBER_MAX = 1_000_000
LOOKBACK_MONTHS = 18

RATE_LIMIT_SLEEP = 0.2 

BASE_URL = "https://www.googleapis.com/youtube/v3"

s3 = boto3.client("s3")

# ---------------- HELPERS ---------------- #

def s3_put_json(data, key):
    s3.put_object(
        Bucket=AWS_BUCKET,
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json"
    )

def yt_get(endpoint, params):
    params["key"] = YOUTUBE_API_KEY
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)

    if response.status_code == 429:
        time.sleep(5)
        return yt_get(endpoint, params)

    response.raise_for_status()
    time.sleep(RATE_LIMIT_SLEEP)
    return response.json()

# ---------------- CHANNEL SEARCH ---------------- #

def search_channels() -> List[dict]:
    channels = {}
    for term in SEARCH_TERMS:
        page_token = None

        while len(channels) < MAX_CHANNELS:
            data = yt_get(
                "search",
                {
                    "q": term,
                    "type": "channel",
                    "part": "snippet",
                    "maxResults": 50,
                    "pageToken": page_token
                }
            )

            for item in data["items"]:
                cid = item["snippet"]["channelId"]
                channels[cid] = item

            page_token = data.get("nextPageToken")
            if not page_token:
                break

    return list(channels.keys())

# ---------------- CHANNEL METADATA ---------------- #

def filter_channels(channel_ids: List[str]) -> List[str]:
    valid_channels = []

    for i in range(0, len(channel_ids), 50):
        batch = channel_ids[i:i+50]

        data = yt_get(
            "channels",
            {
                "part": "statistics,snippet",
                "id": ",".join(batch)
            }
        )

        for ch in data["items"]:
            subs = int(ch["statistics"].get("subscriberCount", 0))
            if SUBSCRIBER_MIN <= subs <= SUBSCRIBER_MAX:
                valid_channels.append({
                    "channel_id": ch["id"],
                    "subscriber_count": subs
                })
    return valid_channels

# ---------------- VIDEOS FETCH ---------------- #

def fetch_videos(channel_id):
    videos = []
    page_token = None
    cutoff_date = datetime.utcnow() - timedelta(days=30 * LOOKBACK_MONTHS)

    try:
        ch = yt_get(
            "channels",
            {"part": "contentDetails", "id": channel_id}
        )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Channel {channel_id} not found, skipping...")
            return []
        else:
            raise

    items = ch.get("items", [])
    if not items:
        return []

    uploads_playlist_id = (
        items[0]
        .get("contentDetails", {})
        .get("relatedPlaylists", {})
        .get("uploads")
    )
    if not uploads_playlist_id:
        print(f"Channel {channel_id} has no uploads playlist, skipping...")
        return []

    while True:
        try:
            data = yt_get(
                "playlistItems",
                {
                    "part": "snippet,contentDetails",
                    "playlistId": uploads_playlist_id,
                    "maxResults": 50,
                    "pageToken": page_token
                }
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Playlist not found for channel {channel_id}, skipping...")
                break
            else:
                raise

        video_ids = []
        for item in data["items"]:
            published = datetime.fromisoformat(
                item["contentDetails"]["videoPublishedAt"].replace("Z", "")
            )
            if published < cutoff_date:
                continue
            videos.append(item)
            video_ids.append(item["contentDetails"]["videoId"])

        # Fetch statistics, topic details, and duration
        if video_ids:
            stats_data = yt_get(
                "videos",
                {
                    "part": "statistics,topicDetails,contentDetails",
                    "id": ",".join(video_ids)
                }
            )
            stats_map = {v["id"]: v for v in stats_data.get("items", [])}
            for v in videos[-len(video_ids):]:
                vid = v["contentDetails"]["videoId"]
                if vid in stats_map:
                    v["statistics"] = stats_map[vid].get("statistics", {})
                    v["topicDetails"] = stats_map[vid].get("topicDetails", {})
                    v["duration"] = stats_map[vid].get("contentDetails", {}).get("duration")

        page_token = data.get("nextPageToken")
        if not page_token or len(videos) >= VIDEOS_PER_CHANNEL:
            break

    return videos[:VIDEOS_PER_CHANNEL]


# ---------------- HELPER: UPDATE VIDEO LIST ---------------- #

def update_channel_videos(existing_videos, new_videos, max_videos=VIDEOS_PER_CHANNEL):
    """
    Combine existing and new videos, keep only the most recent `max_videos` videos.
    """
    # Combine new + existing
    combined = new_videos + existing_videos
    
    # Sort descending by publish date
    combined.sort(key=lambda x: x['contentDetails']['videoPublishedAt'], reverse=True)
    
    # Keep only the top `max_videos`
    return combined[:max_videos]

def s3_get_json(key):
    """
    Fetch existing JSON from S3. Returns [] if not exists.
    """
    try:
        resp = s3.get_object(Bucket=AWS_BUCKET, Key=key)
        data = json.loads(resp['Body'].read())
        return data.get("videos", [])
    except s3.exceptions.NoSuchKey:
        return []

# ---------------- MAIN PIPELINE ---------------- #

def main():
    print("Searching channels...")
    channel_ids = search_channels()

    print("Filtering channels...")
    filtered_channels = filter_channels(channel_ids)
    print(f"Selected {len(filtered_channels)} channels")

    for ch in filtered_channels:
        channel_id = ch["channel_id"]
        subscriber_count = ch["subscriber_count"]
        
        print(f"Fetching new videos for {channel_id}")
        new_videos = fetch_videos(channel_id)  # get new videos ignoring 100 limit

        # Determine S3 key for existing videos
        existing_key = f"{AWS_PREFIX}/channel_id={channel_id}/latest.json"
        existing_videos = s3_get_json(existing_key)

        # Merge and keep latest 100
        updated_videos = update_channel_videos(existing_videos, new_videos)

        # Store updated video list back to S3
        s3_put_json(
            {
                "channel_id": channel_id,
                "subscriber_count": subscriber_count,
                "videos": updated_videos,
                "ingested_at": datetime.utcnow().isoformat()
            },
            existing_key
        )

        print(f"Channel {channel_id} updated with {len(updated_videos)} videos")

if __name__ == "__main__":
    main()

