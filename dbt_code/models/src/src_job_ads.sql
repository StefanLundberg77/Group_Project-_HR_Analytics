--adding deduping logic to all src?
-- as API likely duplicates all ids


with stg_job_ads as (select *

 --   ,row_number() over (
 --       partition by id
 --       order by application_deadline desc
 --   ) as rn 

from {{ source('job_ads', 'stg_ads') }}
)

select
    occupation__label,
    id,
    employer__workplace,
    workplace_address__municipality,
    number_of_vacancies as vacancies,
    relevance,
    application_deadline
from stg_job_ads
--where rn = 1