-- models/fact/fct_upload_behaviour.sql
SELECT
    channel_id,
    DATE(video_published_at) AS upload_date,
    COUNT(video_id) AS videos_uploaded_that_day
FROM {{ ref('stg_youtube_videos') }}
GROUP BY channel_id, DATE(video_published_at)
