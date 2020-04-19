import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/TrackConditions.csv')
df2 = pd.read_csv('../Datasets/TripleCrownRaces_2005-2019.csv')

#df1['year'] = pd.to_datetime(df1['year'])
df1 = df1[df1['race'] == "Kentucky Derby"]
df2 = df2[df2['race'] == "Kentucky Derby"]
'''
df2['PP'] = df2['PP'].str.replace(r'\D', '').astype(int)
df2['diff'] = df2["PP"].subtract(df2['final_place'])
print(df2['diff'])
'''

df2 = df2[df2["final_place"] == 1]
trackNum = []
for i in range(len(df1)):
    if df1.at[i, 'track_condition'] == "Fast":
        trackNum.append(20)
    elif df1.at[i, 'track_condition'] == "Sloppy":
        trackNum.append(10)
    else:
        trackNum.append(1)

df1['trackNum'] = trackNum

# Preparing data
#trace4 = go.Scatter(x=df2['year'], y=df2['diff'], mode='lines', name='difference')
trace1 = go.Scatter(x=df2['year'], y=df2['final_place'], mode='lines', name='final place')
trace2 = go.Scatter(x=df2['year'], y=df2['PP'], mode='lines', name='predicted place')
trace3 = go.Scatter(x=df1['year'], y=df1['trackNum'], mode='lines', name='track conditions')
data = [trace1,trace2,trace3]
# Preparing layout
layout = go.Layout(title='Weather Conditions and Predicted Places in First Place Kentucky Derby Horses', xaxis_title="year",yaxis_title="variables")
# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='multilinechart.html')