with fct as (
    select *
    from {{ ref('fct_video_metrics') }}
)

select
    c.channel_id,
    c.channel_title,
    count(f.video_id) as total_videos,
    avg(f.description_length) as avg_desc_length,
    min(f.published_at) as first_video,
    max(f.published_at) as last_video
from {{ ref('dim_channels') }} c
left join fct_video_metrics f
on c.channel_id = f.channel_id
group by 1,2
