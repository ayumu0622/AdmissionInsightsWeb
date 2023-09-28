import streamlit as st
from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from gcp import *
from graph import *

statistic_option = ["Admit_GPA_range","Admit_rate","Enroll_GPA_range","Yield_rate","Admits","Applicants","Enrolls"]
year_option = [2018, 2019, 2020, 2021, 2022]

class Manipulate:
    
    def __init__(self, school, year_list, major_list, statistic_list, regression_option):  
        self.school = school
        self.year = year_list
        self.major = major_list
        self.statistic = statistic_list
        self.regression = regression_option
        self.data = None
    
    def sql_method(self):
        self.data = run_query(year_list = self.year,
                              major_list = self.major,
                              school = self.school)
        self.data = self.data[self.statistic]
    
    def visualize(self):

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
option = st.sidebar.selectbox("Choose what to do", ("Check the table data", "See the trend"))

if option == "Check the table data":
   year_time = st.sidebar.radio("year", year_option, key='year')
   major_list = list(get_the_all_major(school)["Major_name"])
   viz_instance = Manipulate(school, year_time, major_list, None, False)
   viz_instance.sql_method()
#    st.write(viz_instance.data) 
#    st.divider()

elif option == 'See the trend':
    years = st.sidebar.multiselect("Choose years", year_option)
    values = st.sidebar.multiselect("Choose Statistic", statistic_option)
    major_list = list(get_the_all_major(school)["Major_list"])
    majors = st.sidebar.multiselect("Choose majors", (major_list))
    viz_instance = Manipulate(school, years, majors, statistic_option, False)
    viz_instance.sql_method()

    if st.sidebar.button('Visualize', key='visualize'):
        viz_instance.visualize()

