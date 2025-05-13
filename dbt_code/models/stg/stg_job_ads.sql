with staged_ads as (
    select *,
    row_number() over (
        partition by id 
        order by application_deadline desc
    ) as st 
    from {{ source('job_ads', 'stg_ads')}}
)

SELECT
    id,
    occupation__label,
    employer__workplace,
    workplace_address__municipality,
    number_of_vacancies,
    relevance,
    application_deadline,
    experience_required,
    driving_license_required,
    access_to_own_car
FROM ranked_ads
WHERE st = 1
