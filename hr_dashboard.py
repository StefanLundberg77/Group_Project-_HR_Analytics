# Streamlit dashboard for visualising and analysing HR metrics

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

con = duckdb.connect("ads_data_warehouse.duckdb")

df = con.execute("SELECT * FROM staging.job_ads").fetchdf()

st.markdown("## HiRe Analytics Dashboard")

st.markdown(" ### Raw Data Preview")
st.dataframe(df.head(20))

if "occupation_field" in df.columns:
    group = st.selectbox("Filter by Occupation", df["occupation_field"].dropna().unique())
    st.write(df[df["occupation_field"] == group])

# create pie charts to see which locations have the most vacancies for the 
# 3 different occ_fields

query = """
SELECT
    occupation_field__label AS occupation_field,
    workplace_address__municipality AS municipality,
    SUM(number_of_vacancies) AS total_vacancies
FROM staging.job_ads
WHERE occupation_field__label IS NOT NULL AND municipality IS NOT NULL
GROUP BY occupation_field__label, municipality
"""

df = con.execute(query).fetchdf()

st.markdown("### Vacancies by Location")
selected_field = st.selectbox("Choose occupation field:", df["occupation_field"].unique())

# Pie chart showing ALL vacancies for 3 fields. Too crowded
#filtered = df[df["occupation_field"] == selected_field]
#fig = px.pie(filtered, values="total_vacancies", names="municipality", title="Vacancies by Location")
#st.plotly_chart(fig)

# 2 pie charts showing 10 locations each with most / least vacancies
# Top 10
filtered = df[df["occupation_field"] == selected_field]
top_10 = filtered.sort_values("total_vacancies", ascending = False).head(10)
fig_top_10 = px.pie(
    top_10, values="total_vacancies", 
    names="municipality", 
    title="Top 10 Municipality with Highest Recruitment Need")
fig_top_10.update_traces(textinfo="label+value") # show numerical vacancies instead of default %
st.plotly_chart(fig_top_10)

# Bottom 10
bottom_10 = filtered.sort_values("total_vacancies", ascending = True).head(10)
fig_bottom_10 = px.pie(
    bottom_10, values="total_vacancies", 
    names="municipality", 
    title="Bottom 10 Municipalities by Number of Vacancies")
fig_bottom_10.update_traces(textinfo="label+value") # show numerical vacancies instead of default %
st.plotly_chart(fig_bottom_10)

# Listing all municipalities with low numerical demand (= 1 vacancy)
low_vacancy = df[df["total_vacancies"]==1]
field_choice = st.selectbox(
    "Single-Vacancy Municipality by Field", 
    low_vacancy["occupation_field"].unique()
    )
filtered_low = low_vacancy[low_vacancy["occupation_field"]== field_choice]

with st.expander("Show All Municipalities with Only 1 Vacancy"):
    st.dataframe(filtered_low.sort_values("municipality"))
