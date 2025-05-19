{% for model in ['src_job_ads',
                'src_job_details', 
                
                
                'src_auxiliary_attributes']%}

select 
    '{{model}}' as model_name,
    id,
    count(*) as ct 
    from {{ref(model)}}
    group by id
    having count(*) > 1

    union all

{% endfor%}

select null as model_name, null as id, null as ct
where false 