# streamlit_app.py
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
credentials = service_account.Credentials.from_service_account_info( st.secrets["gcp_service_account"])
client = bigquery.Client(credentials=credentials)

def run_query(year_list, major_list, school):
    # year_list = [int(i) for i in year_list]
    job_config = bigquery.QueryJobConfig(
    query_parameters=[ 
        bigquery.ArrayQueryParameter("major", "STRING", major_list),
        bigquery.ArrayQueryParameter("year", "INT64", year_list),
        ]
        )
            
    if school == "UC Berkeley":
        query = f"""
                SELECT *
                FROM `tidal-beacon-349306.ucstatistic.berkeley_2012_2022` 
                WHERE Major_name IN UNNEST(@major)
                AND year IN UNNEST(@year)
                """
    query_job = client.query(query, job_config=job_config)
    return query_job.to_dataframe()


def get_the_all_major(school):
    
    if school == "UC Berkeley":
        query_text = f"""
                SELECT Major_name
                FROM `tidal-beacon-349306.ucstatistic.berkeley_2012_2022` 
                WHERE year = 2022
            """
    query_job = client.query(query_text)
    return query_job.to_dataframe()