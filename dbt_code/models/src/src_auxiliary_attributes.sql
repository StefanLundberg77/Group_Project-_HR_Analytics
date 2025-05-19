with deduped_aux as (
    select*,
    row_number() over (
        partition by id 
        order by experience_required desc
    ) as rn 
    from {{source('job_ads', 'stg_ads')}}
    )

-- with stg_job_ads as (select * from {{ source('job_ads', 'stg_ads') }})

select
    id,
    experience_required,
    driving_license_required,
    access_to_own_car
from deduped_aux
where rn = 1
