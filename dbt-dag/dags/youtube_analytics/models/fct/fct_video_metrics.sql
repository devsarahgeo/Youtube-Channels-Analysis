with stg as (
    select
        video_id,
        channel_id,
        video_published_at as published_at
        -- length(description) as description_length
    from {{ ref('stg_youtube_videos') }}
)

select *
from stg

