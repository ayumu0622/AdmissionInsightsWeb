import streamlit as st
from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from gcp import *
from graph import *

# @st.cache_data(persist=True)
# def load_data():
#     df_2022 = pd.read_csv('2022berkeley.csv')
#     df_2021 = pd.read_csv('2021berkeley.csv')
#     df_2020 = pd.read_csv('2020berkeley.csv')
#     df_2019 = pd.read_csv('2019berkeley.csv')
#     df_2018 = pd.read_csv('2018berkeley.csv')
#     return df_2022, df_2021, df_2020,df_2019, df_2018

# @st.cache_data(persist=True)
# def load_data_la():
#     df_2022 = pd.read_csv('2022ucla.csv')
#     df_2021 = pd.read_csv('2021ucla.csv')
#     df_2020 = pd.read_csv('2020ucla.csv')
#     df_2019 = pd.read_csv('2019ucla.csv')
#     df_2018 = pd.read_csv('2018ucla.csv')
#     return df_2022, df_2021, df_2020,df_2019, df_2018

# df_2022, df_2021, df_2020,df_2019, df_2018 = load_data()
# df_2022_la, df_2021_la, df_2020_la, df_2019_la, df_2018_la = load_data_la()

statistic_option = ["Admit_GPA_range","Admit_rate","Enroll_GPA_range","Yield_rate","Admits","Applicants","Enrolls"]
year_option = ["2018", "2019", "2020", "2021", "2022"]
# year_df_mapping_la = {
#     2022: df_2022_la,
#     2021: df_2021_la,
#     2020: df_2020_la,
#     2019: df_2019_la,
#     2018: df_2018_la
# }

# year_df_mapping = {
#     2022: df_2022,
#     2021: df_2021,
#     2020: df_2020,
#     2019: df_2019,
#     2018: df_2018
# }


# def main(mapping):

#     for value in values:

#         if ('Enroll GPA range' != value) and ('Admit GPA range' != value) and (len(years)==1):
#            df = mapping.get(years[0], None)
#            one_year_graph(majors, df, years[0], value)

#         elif (('Enroll GPA range' == value) or ('Admit GPA range' == value)) and (len(years)==1):
#            df = mapping.get(years[0], None)
#            range_viz(majors, df, years[0], value)

#         elif ('Enroll GPA range' != value) and ('Admit GPA range' != value) and (len(years)>1):
#             line_plot_for_multiple(mapping, majors, years, value)

#         elif (('Enroll GPA range' == value) or ('Admit GPA range' == value)) and (len(years)>1):
#             for year in years:
#                 df = mapping.get(year, None)
#                 range_viz(majors, df, year, value)

class Manipulate:
    
    def __init__(self, school, year_list, major_list, statistic_list, regression_option):  
        self.school = school
        self.year = year_list
        self.major = major_list
        self.statistic = statistic_list
        self.regression = regression_option
        self.data = None
    
    def sql_method(self):
        self.statistic
        self.data = run_query(year_list = self.year,
                              major_list = self.major,
                              school = self.school)
        self.data = self.data[self.statistic]
    
    def visualize(self, value):

        if ('Enroll GPA range' != self.statistic) and ('Admit GPA range' != self.statistic) and (len(self.year)==1):
           one_year_graph(self.major, self.data, self.year, self.statistic)

        elif (('Enroll GPA range' == self.statistic) or ('Admit GPA range' == self.statistic)) and (len(self.year)==1):
           range_viz(self.major, self.data, self.year, self.statistic)

        elif ('Enroll GPA range' != self.statistic) and ('Admit GPA range' != self.statistic) and (len(self.year)>1):
            line_plot_for_multiple(self.data, self.major, self.year, self.statistic)

        elif (('Enroll GPA range' == self.statistic) or ('Admit GPA range' == self.statistic)) and (len(self.year)>1):
            for year in self.year:
                range_viz(self.major, self.data, year, self.statistic)


st.set_page_config(page_title="University of California Transfer Statistics Visualization")
st.header("UC Transfer Analyzer")
st.caption("Welcome to our UC Transfer Insights web app! Discover transfer data and visualizations for UC majors sourced from the official Transfer by Major information provided by the University of California. Explore key findings, interactive tables, charts, and graphs. Easily compare transfer rates across majors. Gain insights and make informed decisions. Data sourced from the University of California. Visit https://www.universityofcalifornia.edu/about-us/information-center/transfers-major for more details.")
st.divider()

st.sidebar.header("UC Transfer Analyzer")
school = st.sidebar.selectbox("School", ("UC Berkeley", "UCLA", "UC San Diego", "UC Irvine", "UC Davis", "UC SantaBarbara"))
options = st.sidebar.selectbox("Choose what to do", ("Check the table data", "See the trend"))

if options == "Check the table data":
   year_time = st.sidebar.radio("year", year_option, key='year')
   viz_instance = Manipulate(school, year_time, None, None, False)
   viz_instance.sql_method()
   st.write(viz_instance.data) 
   st.divider()

elif options == 'See the trend':
    years = st.sidebar.multiselect("Choose years", year_option)
    values = st.sidebar.multiselect("Choose Statistic", statistic_option)
    major_list = list(get_the_all_major(school)["Major_list"])
    majors = st.sidebar.multiselect("Choose majors", (major_list))
    viz_instance = Manipulate(school, years, majors, statistic_option, False)
    viz_instance.sql_method()

    if st.sidebar.button('Visualize', key='visualize'):
        viz_instance.visualize()


        # if school == 'UCLA':
        #     main(year_df_mapping_la)
        # elif school == 'UC Berkeley':
        #     main(year_df_mapping)
    
    # if school == 'UC Berkeley':
    #     years = st.sidebar.multiselect("Choose years", year_option)
    #     majors = st.sidebar.multiselect("Choose majors", (df_2022['Major name'].tolist()))
    #     values = st.sidebar.multiselect("Choose Statistic", statistic_option)


    # elif school == 'UCLA':
    #     years = st.sidebar.multiselect("Choose years", year_df_mapping_la.keys())
    #     majors = st.sidebar.multiselect("Choose majors", (df_2022_la['Major name'].tolist()))
    #     values = st.sidebar.multiselect("Choose Statistic", year_option)

    # if st.sidebar.button('Visualize', key='visualize'):
    #     if school == 'UCLA':
    #         main(year_df_mapping_la)
    #     elif school == 'UC Berkeley':
    #         main(year_df_mapping)