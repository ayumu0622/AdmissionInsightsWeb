import streamlit as st
from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go


@st.cache_data(persist=True)
def load_data():
    df_2022 = pd.read_csv('/Users/ayumuueda/Desktop/tbm/2022berkeley.csv')
    df_2021 = pd.read_csv('/Users/ayumuueda/Desktop/tbm/2021berkeley.csv')
    df_2020 = pd.read_csv('/Users/ayumuueda/Desktop/tbm/2020berkeley.csv')
    df_2019 = pd.read_csv('/Users/ayumuueda/Desktop/tbm/2019berkeley.csv')
    df_2018 = pd.read_csv('/Users/ayumuueda/Desktop/tbm/2018berkeley.csv')
    return df_2022, df_2021, df_2020,df_2019, df_2018

@st.cache_data(persist=True)
def load_data_la():
    df_2022 = pd.read_csv('/Users/ayumuueda/Desktop/tbm/2022ucla.csv')
    df_2021 = pd.read_csv('/Users/ayumuueda/Desktop/tbm/2021ucla.csv')
    df_2020 = pd.read_csv('/Users/ayumuueda/Desktop/tbm/2020ucla.csv')
    df_2019 = pd.read_csv('/Users/ayumuueda/Desktop/tbm/2019ucla.csv')
    df_2018 = pd.read_csv('/Users/ayumuueda/Desktop/tbm/2018ucla.csv')
    return df_2022, df_2021, df_2020,df_2019, df_2018

def one_year_graph(majors, df, years, value):

   value_list = []
   
   for maj in majors:
      try:
        value_list.append(df.loc[df['Major name'] == maj, value].tolist()[0])
      except:
        value_list.append(0)
        st.title('Invalid value detected!!')

   fig = px.bar(x = majors, y = value_list, width=500, height=600)
   fig.update_layout(title = ' vs '.join(majors), yaxis_title=value)
   st.subheader(str(years)+' '+value)
   st.write(fig)

def range_viz(majors, df, year, value):

    lower_list = []
    upper_list = []

    for maj in majors:

        try:
            if df.loc[df['Major name'] == maj,value].tolist()[0] != 'masked':
                lower = float(df.loc[df['Major name'] == maj,value].tolist()[0][0:4])
                upper = float(df.loc[df['Major name'] == maj,value].tolist()[0][7:]) 
                lower_list.append(lower)
                upper_list.append(upper)
            else:
                lower = 0
                upper = 0
                lower_list.append(lower)
                upper_list.append(upper)
        except:
            lower = 0
            upper = 0
            lower_list.append(lower)
            upper_list.append(upper)
            st.title('Invalid Value!!')
    
    df = pd.DataFrame({'major': majors,
                   '25': lower_list,
                   '75': upper_list })
    
    w_lbl = list(map(lambda x: str(x), df['25']))
    m_lbl = list(map(lambda x: str(x), df['75']))

    fig = go.Figure()

    for i in range(0, len(df)):

        fig.add_trace(go.Scatter(x = np.linspace(df['25'][i], df['75'][i], 1000),
                                y = 1000*[df['major'][i]],
                                mode = 'markers',
                                marker = {'color': np.linspace(df['25'][i], df['75'][i], 1000),
                                        'colorscale': ['#E1A980', '#8DAEA6'],
                                        'size': 8}))

    fig.add_trace(go.Scatter(x = df['25'],
                            y = df['major'],
                            marker = dict(color = '#CC5600', size = 14),
                            mode = 'markers+text',
                            text = w_lbl,
                            textposition = 'middle left',
                            textfont = {'color': '#CC5600'},
                            name = '25 percentile'))

    fig.add_trace(go.Scatter(x = df['75'],
                            y = df['major'],
                            marker = dict(color = '#237266', size = 14),
                            mode = 'markers+text',
                            text = m_lbl,
                            textposition = 'middle right',
                            textfont = {'color': '#237266'},
                            name = '25 percentile'))

    fig.update_layout(title = ' vs '.join(majors),
                    showlegend = False)
    
    st.subheader(str(year)+' '+value)
    st.write(fig)

def line_plot_for_multiple(mapping, majors, years, value): 
    
    multiple_dict = {}

    for maj in majors:
        multiple_value = []
        for tt in years:
            frame = mapping[tt]
            try:
                multiple_value.append(frame.loc[frame['Major name'] == maj,value].to_list()[0])
            except:
                multiple_value.append(0)

        multiple_dict[maj] = multiple_value
    
    str_years = [str(x) for x in sorted(years)]
    fig = go.Figure()
    for key, new_value in multiple_dict.items():
        fig.add_trace(go.Scatter(x=str_years, y=new_value,
                    mode='lines',
                    name=key))
    
    fig.update_layout(title=' vs '.join(majors))
    
    st.subheader(str(np.min(years)) + ' - ' +str(np.max(years)) +' '+value)

    st.write(fig)
    st.divider()

df_2022, df_2021, df_2020,df_2019, df_2018 = load_data()
df_2022_la, df_2021_la, df_2020_la, df_2019_la, df_2018_la = load_data_la()

column_option = list(df_2022.columns)
column_option.remove('Major name')

year_df_mapping_la = {
    2022: df_2022_la,
    2021: df_2021_la,
    2020: df_2020_la,
    2019: df_2019_la,
    2018: df_2018_la
}

year_df_mapping = {
    2022: df_2022,
    2021: df_2021,
    2020: df_2020,
    2019: df_2019,
    2018: df_2018
}


def main(mapping):

    for value in values:

        if ('Enroll GPA range' != value) and ('Admit GPA range' != value) and (len(years)==1):
           df = mapping.get(years[0], None)
           one_year_graph(majors, df, years[0], value)

        elif (('Enroll GPA range' == value) or ('Admit GPA range' == value)) and (len(years)==1):
           df = mapping.get(years[0], None)
           range_viz(majors, df, years[0], value)

        elif ('Enroll GPA range' != value) and ('Admit GPA range' != value) and (len(years)>1):
            line_plot_for_multiple(mapping, majors, years, value)

        elif (('Enroll GPA range' == value) or ('Admit GPA range' == value)) and (len(years)>1):
            for year in years:
                df = mapping.get(year, None)
                range_viz(majors, df, year, value)
           
st.header("UC Transfer Analyzer")
st.caption("Welcome to our UC Transfer Insights web app! Discover transfer data and visualizations for UC majors sourced from the official Transfer by Major information provided by the University of California. Explore key findings, interactive tables, charts, and graphs. Easily compare transfer rates across majors. Gain insights and make informed decisions. Data sourced from the University of California. Visit https://www.universityofcalifornia.edu/about-us/information-center/transfers-major for more details.")
st.divider()

st.sidebar.header("UC Transfer Analyzer")
school = st.sidebar.selectbox("School", ("UC Berkeley", "UCLA"))
options = st.sidebar.selectbox("Choose what to do", ("Check the table data", "Visualize the data"))

if options == "Check the table data":

   if school == 'UC Berkeley':
       year_time = st.sidebar.radio("year", year_df_mapping.keys(), key='year')
       show_data = year_df_mapping.get(year_time, None)
   else:
       year_time = st.sidebar.radio("year", year_df_mapping_la.keys(), key='year')
       show_data = year_df_mapping_la.get(year_time, None)

   st.write(show_data) 
   st.divider()
   
elif options == 'Visualize the data':
    
    if school == 'UC Berkeley':
        years = st.sidebar.multiselect("Choose years", year_df_mapping.keys())
        majors = st.sidebar.multiselect("Choose majors", (df_2022['Major name'].tolist()))
        values = st.sidebar.multiselect("Choose Statistic", column_option)
    elif school == 'UCLA':
        years = st.sidebar.multiselect("Choose years", year_df_mapping_la.keys())
        majors = st.sidebar.multiselect("Choose majors", (df_2022_la['Major name'].tolist()))
        values = st.sidebar.multiselect("Choose Statistic", column_option)

    if st.sidebar.button('Visualize', key='visualize'):
        if school == 'UCLA':
            main(year_df_mapping_la)
        elif school == 'UC Berkeley':
            main(year_df_mapping)
   

