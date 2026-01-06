select
    channel_id,
    date_trunc('week', snapshot_date) as week,

    avg(view_count) as avg_views,
    avg(engagement_rate) as avg_engagement_rate,
    avg(like_rate) as avg_like_rate,
    avg(comment_rate) as avg_comment_rate

from {{ ref('fct_video_funnel') }}
group by 1, 2
