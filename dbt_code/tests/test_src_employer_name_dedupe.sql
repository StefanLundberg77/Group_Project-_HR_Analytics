-- does not run? test again later

select
    employer__name,
    workplace_address__municipality,
    workplace_address__country,
    
    count(*) as ct 

    FROM {{ ref('src_employer_name') }}
    group by
    employer__workplace,
    employer__name,
    workplace_address__municipality,
    workplace_address__country,
   
having count(*) > 1