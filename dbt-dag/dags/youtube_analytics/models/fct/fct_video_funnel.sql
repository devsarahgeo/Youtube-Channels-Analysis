select
    video_id,
    channel_id,
    ingested_at as snapshot_date,

    view_count,
    like_count,
    comment_count,

    -- Funnel metrics
    case 
        when view_count > 0 then like_count / view_count::float
        else 0
    end as like_rate,

    case 
        when view_count > 0 then comment_count / view_count::float
        else 0
    end as comment_rate,

    case 
        when view_count > 0 
            then (like_count + comment_count) / view_count::float
        else 0
    end as engagement_rate

from {{ ref('stg_youtube_videos') }}
