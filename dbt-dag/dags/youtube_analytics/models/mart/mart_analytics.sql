SELECT
    c.channel_id,
    c.channel_title,
    SUM(f.view_count) AS total_views,
    AVG(f.like_count) AS avg_likes,
    COUNT(f.video_id) AS video_count
FROM {{ ref('fct_video_perf') }} f
JOIN {{ ref('dim_videos') }} v ON f.video_id = v.video_id
JOIN {{ ref('dim_channels') }} c ON f.channel_id = c.channel_id
GROUP BY c.channel_id, c.channel_title
ORDER BY total_views DESC
