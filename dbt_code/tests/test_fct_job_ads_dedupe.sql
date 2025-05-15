-- run with dbt test -s <name_of_test_file>

-- Tests for duplicates in fct_job_ads data.

-- Testing to see if deduplicates. Finding 500 rows with x2 duplicates
{#
select 
  job_details_id, COUNT(*) as cnt
from {{ ref('fct_job_ads') }}
group by job_details_id
having count (*) > 1
#}

-- Testing for which id's that are duplicated. Same amount as above
-- appears ie 500x2
select
    id, employer__workplace, vacancies,
    count(*) as count
from {{ref ('src_job_ads')}}
group by id, employer__workplace, vacancies,
having count(*) > 1 