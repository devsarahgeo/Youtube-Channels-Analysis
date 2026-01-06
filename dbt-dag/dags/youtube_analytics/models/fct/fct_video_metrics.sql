with stg as (
    select
        video_id,
        channel_id,
        video_published_at as published_at,
        LPAD(COALESCE(TO_NUMBER(REGEXP_SUBSTR(duration, '(\d+)S')),0),2,'0') AS readable_duration,
        length(description) as description_length
    from {{ ref('stg_youtube_videos') }}
)

select *
from stg

