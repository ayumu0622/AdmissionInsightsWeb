import streamlit as st
from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from get_data_gcp import run_query
import pickle

def first_q(col):
    return float(col[0:4])

def third_q(col):
    return float(col[7:])

def transform(df):
    
    df["25th admit"] = df["Admit_GPA_range"].apply(first_q)
    df["25th enroll"] = df["Enroll_GPA_range"].apply(first_q)
    df["75th admit"] = df["Admit_GPA_range"].apply(third_q)
    df["75th enroll"] = df["Enroll_GPA_range"].apply(third_q)
    df["approx median admit"] = (df["25th admit"] + df["75th admit"]) / 2
    df["approx median Enroll"] = (df["25th enroll"] + df["75th enroll"]) / 2

    df = df.drop(["25th admit","25th enroll", "75th admit", "75th enroll", "approx median admit", "Enrolls"], axis=1)
    df = df.drop(["Admit_GPA_range","Enroll_GPA_range"], axis = 1)

    df = df[['Admit_rate', 'Yield_rate', 'Admits', 'Applicants', 'approx median Enroll']]
    return df

def one_year_graph(majors, df, years, value):

   value_list = []
   
   for maj in majors:
      try:
        value_list.append(df.loc[df['Major_name'] == maj, value].tolist()[0])
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
            if df.loc[df['Major_name'] == maj,value].tolist()[0] != 'masked':
                lower = float(df.loc[df['Major_name'] == maj,value].tolist()[0][0:4])
                upper = float(df.loc[df['Major_name'] == maj,value].tolist()[0][7:]) 
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

def line_plot_for_multiple(mapping, majors, years, value, trendline): 
    years = sorted(years)
    multiple_dict = {}
    for maj in majors:
        multiple_value = []
        for t in years:
            frame = mapping[mapping['year'] == t]
            try:
                multiple_value.append(frame.loc[frame['Major_name'] == maj,value].to_list()[0])
            except:
                multiple_value.append(0)
        multiple_dict[maj] = multiple_value
    #multiple_dict is like {"data science", [2, 3, 4]}

    fig = go.Figure()
    df = pd.DataFrame(multiple_dict)
    df["year"] = [str(x) for x in years]

    if trendline == True:
        fig = px.scatter(df, x="year", y=list(multiple_dict.keys()), trendline='ols')
    else:
        fig = px.scatter(df, x="year", y=list(multiple_dict.keys()))

    fig.update_traces(marker=dict(size=10,
                                line=dict(width=2,
                                            color='DarkSlateGrey')),
                    selector=dict(mode='markers'))
    
    fig.update_layout(title=' vs '.join(majors))
    
    st.subheader(str(np.min(years)) + ' - ' +str(np.max(years)) +' '+value)

    st.write(fig)
    st.divider()

def plot_for_predict(data, majors, years, stat, trendline):

    with open('models/ridge_berk_pkl' , 'rb') as f:
        model = pickle.load(f)
    
    years = sorted(years)
    multiple_dict = {}
    
    for maj in majors:
        multiple_value = []
        df = data[data['year'] != 2022]
        df = df[df['Major_name'] == maj]
        df = df.sort_values(by=['year'])
        try:
            multiple_value.extend(df["Admit_rate"].to_list())
        except:
            multiple_value.extend([0.0] * len(years))
        
        x_test = data[data['year'] == 2022]
        x_test = x_test[x_test["Major_name"] == maj]
        features = transform(x_test)
        predicted = model.predict(features)
        predicted = predicted[0]
        multiple_value.append(predicted)

        while(len(multiple_value) < len(years)):
            multiple_value.insert(0, 0.0)

        multiple_dict[maj] = multiple_value

    fig = go.Figure()
    df = pd.DataFrame(multiple_dict)
    df["year"] = [str(x) for x in years]

    # fig = px.scatter(df, x="year", y=list(multiple_dict.keys()))
    fig = px.line(df, x='year', y=list(multiple_dict.keys()), markers=True)
    fig.update_traces(marker=dict(size=10,
                                line=dict(width=2,
                                            color='DarkSlateGrey')),
                    selector=dict(mode='markers'))
    for key, item in multiple_dict.items():
        fig.add_annotation(x=2022, y=item[10],
            text="prediction",
            showarrow=False,
            yshift=10)
    fig.update_layout(title=' vs '.join(majors))
    
    st.subheader(str(np.min(years)) + ' - ' +str(np.max(years)) +' '+ "Admit rate")
    st.write(fig)
    st.divider()