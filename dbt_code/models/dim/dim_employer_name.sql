WITH employer_name AS (
    SELECT 
        employer__name,
        workplace_address__municipality,
        workplace_address__country,
        employer__workplace
    FROM {{ source('job_ads', 'stg_ads') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key([
        'employer__name', 
        'workplace_address__municipality', 
        'workplace_address__country',
        'employer__workplace'
    ]) }} AS employer_location_id,
    
    employer__name,
    COALESCE(workplace_address__municipality, 'Ej angivet') AS municipality,
    COALESCE(workplace_address__country, 'Ej angivet') AS country,

    CASE
        WHEN workplace_address__municipality IS NULL OR workplace_address__municipality = '' THEN COALESCE(workplace_address__country, 'Ej angivet')
        ELSE CONCAT(workplace_address__municipality, ', ', workplace_address__country)
    END AS municipality_country_text,

    employer__workplace

FROM employer_name
GROUP BY 
    employer__name, 
    workplace_address__municipality, 
    workplace_address__country,
    employer__workplace






