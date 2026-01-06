-- models/fact/fct_video_perf.sql
SELECT
    video_id,
    channel_id,
    ingested_at AS snapshot_date,
    view_count::INT     AS view_count,
    like_count::INT     AS like_count,
    comment_count::INT  AS comment_count
FROM {{ ref('stg_youtube_videos') }}
