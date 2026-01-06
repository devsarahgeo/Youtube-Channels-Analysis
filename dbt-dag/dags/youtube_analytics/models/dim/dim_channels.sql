with stg as (
    select distinct
        channel_id,
        channel_title,
        CASE 
            WHEN subscriber_count < 50000 THEN '10k–50k' 
            WHEN subscriber_count < 250000 THEN '50k–250k' 
            ELSE '250k–1M' 
        END AS subscriber_count_bucket
    from {{ ref('stg_youtube_videos') }}
)

select *
from stg
