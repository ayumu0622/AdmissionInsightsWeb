import streamlit as st
from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from get_data_gcp import *
from plot import *

statistic_option = ["Admit_GPA_range", "Admit_rate", "Enroll_GPA_range", "Yield_rate","Admits","Applicants","Enrolls"]
year_option = list(range(2012, 2023))
cache = {}

class Manipulate:
    
    def __init__(self, school: str, year_list: list, major_list: list, statistic_list: list, trendline: bool):  
        self.school = school
        self.year = year_list
        self.major = major_list
        self.statistic = statistic_list
        self.trendline = trendline
        self.data = None
    
    def sql_method(self):
        self.data = run_query(year_list = self.year, major_list = self.major, school = self.school)
    
    def visualize(self):
        for astat in self.statistic:
            if ('Enroll_GPA_range' != astat) and ('Admit_GPA_range' != astat) and (len(self.year)==1):
                one_year_graph(self.major, self.select_year(self.year), self.year[0], astat)

            elif (('Enroll_GPA_range' == astat) or ('Admit_GPA_range' == astat)) and (len(self.year)==1):
                range_viz(self.major, self.select_year(self.year), self.year[0], astat)

            elif ('Enroll_GPA_range' != astat) and ('Admit_GPA_range' != astat) and (len(self.year)>1):
                line_plot_for_multiple(self.data, self.major, self.year, astat, self.trendline)

            elif (('Enroll_GPA_range' == astat) or ('Admit_GPA_range' == astat)) and (len(self.year)>1):
                for year in self.year:
                    range_viz(self.major, self.select_year([year]), year, astat)
    
    def predict(self):
        plot_for_predict(self.data, self.major, self.year, self.statistic[0], self.trendline)

    def get_data(self):
        return self.data
    
    def get_majors(self):
        return self.major
    
    def select_year(self, yr: list):
        return self.data[self.data["year"].isin(yr)]

st.set_page_config(page_title="University of California Transfer Statistics Visualization")
st.header("TransferInsight UC")
st.caption("Welcome to my UC Transfer Insights web app! Discover transfer data and visualizations for UC majors sourced from the official Transfer by Major information provided by the University of California. Explore key findings, interactive tables, charts, and graphs. Easily compare transfer rates across majors. Gain insights and make informed decisions. Data sourced from the University of California. Visit https://www.universityofcalifornia.edu/about-us/information-center/transfers-major for more details.")
st.divider()

st.sidebar.header("TransferInsight UC")
school = st.sidebar.selectbox("School", ("UC Berkeley", "UCLA"))
option = st.sidebar.selectbox("choose what to do", ("check the table data", "visualize the data", "predict future acceptance rate"))

if option == "check the table data":
   year_time = st.sidebar.radio("year", year_option, key='year')

   if school in cache.keys():
       major_list = cache[school]
   else:
       major_list = list(get_the_all_major(school)["Major_name"])
       cache[school] = major_list

   viz_instance = Manipulate(school, [year_time], major_list, statistic_option, False)
   viz_instance.sql_method()
   st.write(viz_instance.data) 
   st.divider()

#From here
elif option == 'visualize the data':
    years = st.sidebar.multiselect("Choose years", year_option)
    stats = st.sidebar.multiselect("Choose Statistic", statistic_option)
    
    if school in cache.keys():
       major_list = cache[school]
    else:
       major_list = list(get_the_all_major(school)["Major_name"])
       cache[school] = major_list

    majors = st.sidebar.multiselect("Choose majors", (major_list))
    trendline = st.sidebar.checkbox('trendline')

    viz_instance = Manipulate(school, years, majors, stats, trendline)
    viz_instance.sql_method()

    if st.sidebar.button('visualize', key='visualize'):
        viz_instance.visualize()

elif option == 'predict future acceptance rate':

    if school in cache.keys():
       major_list = cache[school]
    else:
       major_list = list(get_the_all_major(school)["Major_name"])
       cache[school] = major_list
    
    majors = st.sidebar.multiselect("Choose majors", (major_list))
    
    viz_instance = Manipulate(school, year_option, majors, ["Admit_rate"], False)
    viz_instance.sql_method()

    if st.sidebar.button('predict', key='predict'):
        viz_instance.predict()
        
