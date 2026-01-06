SELECT
    channel_id,
    COUNT(video_id) AS total_videos,
    AVG(view_count) AS avg_views,
    STDDEV(view_count) AS volatility,
    avg(like_rate) as avg_like_rate,
    avg(comment_rate) as avg_comment_rate,
    PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY view_count) AS viral_threshold
FROM {{ ref('fct_video_funnel') }}  
GROUP BY channel_id
