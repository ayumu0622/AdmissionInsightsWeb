from app import *
import pandas as pd
import plotly.graph_objects as go
#From here
df = pd.read_csv("/Users/ayumuueda/Desktop/UC-Transfer-Analyzer/data/berkeley_table.csv")
years = [2021, 2022, 2019]
values = ["Admit_GPA_range","Admit_rate","Enroll_GPA_range","Yield_rate","Admits","Applicants","Enrolls"]
major_list = df['Major name'].to_list()



def range_viz(majors, df, year, value):

    lower_list = []
    upper_list = []
    for maj in majors:
        try:
            if df.loc[df['Major name'] == maj,value].tolist()[0] != 'masked':
                lower = float(df.loc[df['Major name'] == maj, value].tolist()[0][0:4])
                upper = float(df.loc[df['Major name'] == maj, value].tolist()[0][7:]) 
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
    
    
    fig.show()


for year in years:
    range_viz(major_list[0:2], df[df['year'] == year], year, "Enroll GPA range")


# df = df[df['year'] == 2021]
# print(df.loc[df['Major name'] == 'Environmental economics & policy (l&S)', "Enroll GPA range"].tolist()[0] != 'masked')