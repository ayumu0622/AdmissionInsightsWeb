import streamlit as st
from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from gcp import run_query

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