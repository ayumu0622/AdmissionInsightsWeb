# streamlit_app.py
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
year_list = list(range(2018, 2023))
# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# @st.cache_data(ttl=600)

def run_query(query, job_config):
    query_job = client.query(query, job_config=job_config)
    return query_job.to_dataframe()

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ArrayQueryParameter("year", "INT64", year_list), 
        bigquery.ArrayQueryParameter("major", "STRING", ["English"])
    ]
)

data = run_query(f"""
            SELECT *
            FROM `tidal-beacon-349306.ucstatistic.with_column_berkekey`
            WHERE year in UNNEST(@year)
            AND Major_name in UNNEST(@major)
        """, job_config)

print(data)

# WHERE year in UNNEST(@year)
# # Print results.
# st.write(data)



# from google.cloud import bigquery


# query = """
#     SELECT name, sum(number) as count
#     FROM `bigquery-public-data.usa_names.usa_1910_2013`
#     WHERE gender = @gender
#     AND state IN UNNEST(@states)
#     GROUP BY name
#     ORDER BY count DESC
#     LIMIT 10;
# """
# job_config = bigquery.QueryJobConfig(
#     query_parameters=[
#         bigquery.ScalarQueryParameter("gender", "STRING", "M"),
#         bigquery.ArrayQueryParameter("states", "STRING", ["WA", "WI", "WV", "WY"]),
#     ]
# )
# query_job = client.query(query, job_config=job_config)  # Make an API request.

# for row in query_job:
#     print("{}: \t{}".format(row.name, row.count))