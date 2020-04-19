import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd

# Load CSV file from folder
df = pd.read_csv('TrackConditions.csv')

# Preparing data
data = [go.Heatmap(x=df['year'],
                   y=df['race'],
                   z=df['low_temp'].values.tolist(),
                   colorscale='Jet')]

# Preparing layout
layout = go.Layout(title='Low Temperature', xaxis_title="Year",
                   yaxis_title="Race")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='heatmap.html')
