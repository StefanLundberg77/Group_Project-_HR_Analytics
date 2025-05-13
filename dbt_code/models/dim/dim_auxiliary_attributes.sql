-- create table auxiliary_attributes

with auxiliary_attributes as (select * from {{ ref('src_auxiliary_attributes') }})

select
    {{ dbt_utils.generate_surrogate_key(['id']) }} as auxiliary_attributes_id,
    -- checking boolean
    -- https://www.w3schools.com/sql/sql_where.asp 
    coalesce(experience_required, false) as experience_required, 
    coalesce(driving_license_required, false) as driver_license,
    coalesce(access_to_own_car, false) as access_to_own_car,

    -- text added to boolean response for dashboard
    -- https://www.w3schools.com/sql/sql_case.asp
    case when experience_required then 'Ja' else 'Nej' end as experience_required_text, 
    case when driver_license then 'Ja' else 'Nej' end as driver_license_text,
    case when access_to_own_car then 'Ja' else 'Nej' end as access_to_own_car_text
from auxiliary_attributes
-- need to check null? max or distinct? surrogate? scrs job ads eller stgn?