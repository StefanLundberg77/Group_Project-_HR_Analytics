-- Test if duplicates in dim_employer_name.sql
-- result clean = no duplicates

select
    employer_location_id,
    count (*) as count
from {{ ref('dim_employer_name')}}
group by employer_location_id,
having count(*) > 1