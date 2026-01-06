with stg as (
    select distinct
        video_id,
        channel_id,
        title,
        description,
        LENGTH(title) AS title_length,
        DATEDIFF('day', video_published_at, CURRENT_DATE) AS video_age_days
    from {{ ref('stg_youtube_videos') }}
)

select *
from stg
