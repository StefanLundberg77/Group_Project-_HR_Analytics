with
    fct_job_ads as (select * from {{ ref("fct_job_ads") }}),
    dim_job_details as (select * from {{ ref("dim_job_details") }}),
    dim_occupation as (select * from {{ ref("dim_occupation") }}),
    dim_employer as (select * from {{ ref("dim_employer") }}),
    dim_auxiliary_attributes as (select * from {{ ref("dim_auxiliary_attributes") }}),
    joined as (
        select
            f.job_details_id,
            f.auxiliary_attributes_id,
            f.occupation_id,
            f.employer_id,
            jd.headline,
            f.vacancies,
            f.relevance,
            e.employer_name,
            e.workplace_city,
            e.employer_workplace,
            e.workplace_country,
            e.workplace_region,
            e.workplace_municipality,
            o.occupation,
            o.occupation_group,
            o.occupation_field,
            f.application_deadline,
            jd.description,
            jd.description_html,
            jd.duration,
            jd.salary_type,
            jd.salary_description,
            jd.working_hours_type,
            row_number() over (
                partition by f.job_details_id
                order by f.application_deadline desc nulls last
            ) as rn
        from fct_job_ads f
        left join dim_job_details jd on f.job_details_id = jd.job_details_id
        left join
            dim_occupation o
            on f.occupation_id = o.occupation_id
            and o.occupation_field = 'Data/IT'
        left join dim_employer e on f.employer_id = e.employer_id
        left join
            dim_auxiliary_attributes a
            on f.auxiliary_attributes_id = a.auxiliary_attributes_id
    )

select *
from joined
where rn = 1 and occupation_field = 'Data/IT'
