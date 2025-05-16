import streamlit as st
import duckdb
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
con= duckdb.connect("ads_data_warehouse.duckdb")

# Main Dashboard Title
st.markdown("## HR Dashboard")
st.markdown("### Job Ads Skills")

# Dropdown to pick job field
occupation_field = con.execute("""
                               SELECT DISTINCT occupation__field
                               FROM refined.dim_occupation
                               WHERE occupation_field IS NOT NULL
                               ORDER BY occupation_field
                               """).fetchdf()["occupation_field"].tolist()


