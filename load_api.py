import dlt
import requests
import json
from pathlib import Path
import os

db_path = Path(__file__).parent / "ads_data_warehouse.duckdb"

def _get_ads(url_for_search, params):
    headers = {"accept": "application/json"}
    response = requests.get(url_for_search, headers=headers, params=params)
    response.raise_for_status()  # check for http errors
    return json.loads(response.content.decode("utf8"))


@dlt.resource(write_disposition="append")
def jobsearch_resource(params):
    """
    params should include at least:
      - "q": your query
      - "limit": page size (e.g. 100)
    """
    url = "https://jobsearch.api.jobtechdev.se"
    url_for_search = f"{url}/search"
    limit = params.get("limit", 100)
    offset = 0

    while True:
        # build this page’s params
        page_params = dict(params, offset=offset)
        data = _get_ads(url_for_search, page_params)

        hits = data.get("hits", [])
        if not hits:
            # no more results
            break

        # yield each ad on this page
        for ad in hits:
            yield ad

        # if fewer than a full page was returned, we’re done
        if len(hits) < limit or offset > 1900:
            break

        offset += limit


def run_pipeline(query, table_name, occupation_fields):
    pipeline = dlt.pipeline(
        pipeline_name="jobads_demo",
        destination=dlt.destinations.duckdb(str(db_path)),
        dataset_name="staging",
    )

    for occupation_field in occupation_fields:
        params = {"q": query, "limit": 100, "occupation-field": occupation_field}
        load_info = pipeline.run(
            jobsearch_resource(params=params), table_name=table_name
        )
        print(f"Occupation field: {occupation_field}")
        print(load_info)


if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    query = ""
    table_name = "job_ads"

   # "Säkerhet och bevakning", "Yrken med social inriktning", "Data/IT"
    occupation_fields = ("E7hm_BLq_fqZ", "GazW_2TU_kJw", "apaJ_2ja_LuF")

    run_pipeline(query, table_name, occupation_fields)