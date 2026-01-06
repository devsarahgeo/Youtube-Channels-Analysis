with source as (
    select
        channel_id,
        ingested_at,
        source_file,
        subscriber_count,
        raw_payload
    from {{ source('raw', 'youtube_videos_raw') }}
),

flattened as (
    select
        channel_id,
        ingested_at,
        source_file,
        subscriber_count,
        video.value:contentDetails.videoId::string        as video_id,
        video.value:duration::string                      as duration,
        video.value:statistics.viewCount::number          as view_count,
        video.value:statistics.likeCount::number          as like_count,
        video.value:statistics.dislikeCount::number       as dislikeCount,
        video.value:statistics.commentCount::number       as comment_count,
        video.value:snippet.title::string                 as title,
        video.value:snippet.description::string           as description,
        video.value:snippet.publishedAt::timestamp_ntz    as video_published_at,
        video.value:snippet.channelTitle::string          as channel_title,
        video.value:snippet.position::int                 as playlist_position,
        video.value:snippet.thumbnails.high.url::string   as thumbnail_url
    from source,
    lateral flatten(input => raw_payload:videos) video
),

ranked as (
    select
        *,
        row_number() over (partition by video_id order by ingested_at desc) as rn
    from flattened
)

select *
from ranked
where rn = 1
