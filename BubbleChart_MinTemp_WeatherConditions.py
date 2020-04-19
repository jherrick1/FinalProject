import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('TrackConditions.csv')


# Creating sum of number of cases group by Country Column
new_df = df.groupby(['year', 'race']).agg(
    {'low_temp': 'sum', 'track_condition': 'sum', 'weather': 'sum'}).reset_index()

# Preparing data
data = [
    go.Scatter(x=new_df['year'],
               y=new_df['track_condition'],
               text=new_df['race'],
               mode='markers',
               marker=dict(size=new_df['year']/100, color=new_df['low_temp'], showscale=True))
]

# Preparing layout
layout = go.Layout(title='Low Temperatures and Track Conditions', xaxis_title="Year",
                   yaxis_title="Track Conditions", hovermode='closest')

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='bubblechart.html')