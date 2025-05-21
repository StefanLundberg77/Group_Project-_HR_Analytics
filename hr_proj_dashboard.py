import streamlit as st
import duckdb
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model= genai.GenerativeModel("gemini-2.0-flash")
con= duckdb.connect("ads_data_warehouse.duckdb")


# Main Dashboard Title
st.markdown("# HR Dashboard")
st.markdown("### Job Ads Skills")

# Dropdown to pick job field
occupation_fields = con.execute("""
                               SELECT DISTINCT occupation_field
                               FROM refined.dim_occupation
                               WHERE occupation_field IS NOT NULL
                               ORDER BY occupation_field
                               """).fetchdf()["occupation_field"].tolist()

selected_field = st.selectbox(label="",
                              options=occupation_fields,
                              index=None,
                              placeholder="Choose an occupational field below: ")

if selected_field:
    raw_data = con.execute(f"""
            SELECT j.headline, j.description, o.occupation, o.occupation_field
            FROM refined.dim_job_details j 
            JOIN refined.dim_occupation o 
            ON j.id = o.id 
            WHERE o.occupation_field = '{selected_field}'
            LIMIT 100
           """).fetchdf()
    
    st.markdown("### Sample Job Ads")
    st.dataframe(raw_data)


st.markdown("### Soft Skills Generator")

# dropdown for selecting 'occupation'
occupations = con.execute("""
                        SELECT DISTINCT occupation
                        FROM refined.dim_occupation
                        WHERE occupation IS NOT NULL
                        ORDER BY occupation                      
                          """).fetchdf()["occupation"].tolist()

selected_occ = st.selectbox(label="", 
                            options= occupations,
                            index=None,
                            placeholder= "Choose an occupation below: ")

if selected_occ:
    job_desc = con.execute(f"""
                           SELECT j.description
                           FROM refined.dim_job_details j 
                           JOIN refined.dim_occupation o ON j.id = o.id
                           WHERE o.occupation = '{selected_occ}'
                           AND j.description IS NOT NULL
                           LIMIT 100
                    """).fetchdf()
    
    text_blob = " ".join(job_desc["description"].tolist())
    prompt = f"""
    Analyze the following job ad descriptions for '{selected_occ}'.
    Return the top 5 most desired candidate characteristics or skills as a JSON list with score estimates (0-10). 

    {text_blob}
    """

    response = model.generate_content(prompt)
    json_skills = response.text

    



