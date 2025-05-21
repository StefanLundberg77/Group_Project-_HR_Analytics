6. .dbt Tests & Documentation

To run tests, use the following command from the dbt_code project root: dbt test -s <name_of_test_file>
Alternatively, for custom SQL-based tests, you can run Jinja-enabled queries directly using the dbt Power User extension in VS Code. Set the file language to Jinja SQL, then use the ▶️ ("Run") button to preview query results in the terminal.

This folder contains **custom and generic dbt tests** that validate the quality of our data models in the HiRe Data Analytics project.

## Purpose

These tests help us ensure:
- Data is clean and reliable
- Keys are unique
- Relationships between tables make sense
- No duplicates are passed downstream

## Tests Implemented

### Generic YAML Tests
- **`src_job_ads.yml`**
  - `not_null` tests on required columns (e.g. `id`, `occupation__label`, `application_deadline`)
  - `unique` test on `id` to ensure ad-level uniqueness

- **`src_job_details.yml`**
  - Similar structure: `not_null`, `unique` on `id`
  - Validated key dimensions like `headline`, `description`, `working_hours_type`

- **`src_auxiliary_attributes.yml`**
  - `accepted_values` test on booleans (True/False)
  - `unique` + `not_null` test on `id`

### Custom SQL Tests
- **`test_fct_job_ads_dedupe.sql`**
  - Checks for duplicate `job_details_id` in the fact table
- **`test_dim_employer_name_duplicates.sql`**
  - Ensures `employer_location_id` is unique
- **`test_dim_nr_rows.sql`**
  - Compares number of `occupation_id`s in fact and dim tables to detect mismatch

## Learnings

- Duplicates exist in `src_job_ads` and `src_job_details`, caused by multiple rows per job ad ID
- Dimensional keys like `employer_location_id` are clean and stable
- Tests helped isolate dirty data *before* it reached dashboards
- Latest learning as of this week (May 21 2025) each new API upload
  duplicates any job ad remaining from a previous upload - so we added
  deduplication-logic to sources.yml to squash duplication at the *source

## dbt Documentation

We also generated dbt docs using:

```bash
dbt docs generate
dbt docs serve

## This lets us:

- Visualize model dependencies

- View column-level metadata

- Understand upstream/downstream flow