import pickle
import pandas as pd
import numpy as np
import streamlit as st
from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go


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
        
        features = transform(data[data['year'] == 2022])
        predicted = model.predict(features)
        predicted = predicted[0]
        multiple_value.append(predicted)

        while(len(multiple_value) < len(years)):
            multiple_value.insert(0, 0.0)

        multiple_dict[maj] = multiple_value

    fig = go.Figure()
    df = pd.DataFrame(multiple_dict)
    df["year"] = [str(x) for x in years]

    fig = px.scatter(df, x="year", y=list(multiple_dict.keys()), trendline='ols')
    fig.update_traces(marker=dict(size=10,
                                line=dict(width=2,
                                            color='DarkSlateGrey')),
                    selector=dict(mode='markers'))
    
    fig.update_layout(title=' vs '.join(majors))
    
    fig.show()


df = pd.read_csv("data/berkeley_table.csv")
print(df)
df.columns = ["Major_name", "Admit_GPA_range","Admit_rate","Enroll_GPA_range","Yield_rate","Admits","Applicants","Enrolls", 'year']
plot_for_predict(df, ["Economics (l&S)", "Business administration (ugba)"], list(range(2012, 2023)), "Admit_rate", False)

