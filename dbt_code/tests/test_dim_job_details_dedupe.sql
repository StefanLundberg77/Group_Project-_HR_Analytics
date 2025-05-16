select
    job_details_id,
    count(*) as ct 
    from {{ref('dim_job_details')}}
    group by job_details_id
    having count(*) > 1