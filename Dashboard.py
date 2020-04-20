import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/TrackConditions.csv')
df2 = pd.read_csv('../Datasets/TripleCrownRaces_2005-2019.csv')

app = dash.Dash()

# Bar chart data
barchart_df = df2
barchart_df = barchart_df.groupby(['Trainer'])['Win'].sum().reset_index()
barchart_df = barchart_df.sort_values(by=['Win'], ascending=[False]).head(20).reset_index()
data_barchart = [go.Bar(x=barchart_df['Trainer'], y=barchart_df['Win'])]

# Stack bar chart data
stackbarchart_df = df2.groupby(['Trainer']).agg({'Win': 'sum', 'Place': 'sum', 'Show': 'sum'}).reset_index()
stackbarchart_df = df2.sort_values(by=['Win'], ascending=[False]).head(20).reset_index()
trace1_stackbarchart = go.Bar(x=stackbarchart_df['Trainer'], y=stackbarchart_df['Show'], name='Show', marker={'color': '#CD7F32'})
trace2_stackbarchart = go.Bar(x=stackbarchart_df['Trainer'], y=stackbarchart_df['Place'], name='Place', marker={'color': '#9EA0A1'})
trace3_stackbarchart = go.Bar(x=stackbarchart_df['Trainer'], y=stackbarchart_df['Win'], name='Win', marker={'color': '#FFD700'})
data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# Bubble charts
max_bubble_df = df1.groupby(['weather']).agg({'high_temp': 'mean', 'low_temp': 'mean'}).reset_index()
data_bubblechart = [
    go.Scatter(x=max_bubble_df['weather'],
               y=max_bubble_df['high_temp'],
               mode='markers',
               marker=dict(size=max_bubble_df['high_temp'],
                           color=max_bubble_df['high_temp'],
                           showscale=True))
]

new_df = df1.groupby(['year', 'race']).agg({'low_temp': 'sum', 'track_condition': 'sum', 'weather': 'sum'}).reset_index()
data_bubble_min = [
    go.Scatter(x=new_df['year'],
               y=new_df['track_condition'],
               text=new_df['race'],
               mode='markers',
               marker=dict(size=new_df['year']/100,
                           color=new_df['low_temp'],
                           showscale=True))
]

# Heat Maps
data_heatmap_low = [go.Heatmap(x=df1['year'],
                    y=df1['race'],
                    z=df1['low_temp'].values.tolist(),
                    colorscale='Jet')]

data_heatmap_high = [go.Heatmap(x=df1['year'],
                     y=df1['race'],
                     z=df1['high_temp'].values.tolist(),
                     colorscale='Jet')]

# Multiline
df1 = df1[df1['race'] == "Kentucky Derby"]
df2 = df2[df2['race'] == "Kentucky Derby"]

df2 = df2[df2["final_place"] == 1]
trackNum = []
for i in range(len(df1)):
    if df1.at[i, 'track_condition'] == "Fast":
        trackNum.append(20)
    elif df1.at[i, 'track_condition'] == "Sloppy":
        trackNum.append(10)
    else:
        trackNum.append(0)

df1['trackNum'] = trackNum

# Preparing data
trace1 = go.Scatter(x=df2['year'], y=df2['Odds'], mode='lines', name='odds')
trace2 = go.Scatter(x=df2['year'], y=df2['PP'], mode='lines', name='predicted place')
trace3 = go.Scatter(x=df1['year'], y=df1['trackNum'], mode='lines', name='track conditions')
data_multiline = [trace1, trace2, trace3]


# Layout
app.layout = html.Div(children=[
html.H1(children='Even the Playing Field',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Triple Crown Races Data', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
html.Hr(style={'color': '#7FDBFF'}),
    html.Div('Terms to Know:', style={'textAlign': 'center'}),
    html.Div('WIN: To get this money, you have to bet that horse wins the race.', style={'textAlign': 'center'}),
    html.Div('PLACE: To get this money, you have to bet that horse finishes in the top 2.', style={'textAlign': 'center'}),
    html.Div('SHOW: To get this money, you have to bet that horse finishes in the top 3', style={'textAlign': 'center'}),
    html.Div('NOTE:', style={'textAlign': 'center'}),
    html.Div('Horses that don\'t finish in the top 3 have no win/place/show amount.', style={'textAlign': 'center'}),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar Chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the Win amounts of the top 20 trainers of the 1st place horses.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Win Amounts of the Top 20 Trainers',
                                      xaxis={'title': 'Trainer'}, yaxis={'title': 'Win Amount'})
              }
              ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack Bar Chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represents the placement (Win, Place, Show) amounts of the top 20 trainers.'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Placement Amounts for the Top 20 Trainers',
                                      xaxis={'title': 'Trainer'}, yaxis={'title': 'Placement Amounts'},
                                      barmode='stack')
              }
              ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multiline Chart', style={'color': '#df1e56'}),
    html.Div(
        'This multiline chart represents the weather and predicted placement of the first place horses.'),
    html.Br(),
    html.Div('Weather: Lower the number = Worse Conditions'),
    html.Div('Predicted Place: Lower the number = Higher place (1st/2nd/3rd/etc.)'),
    html.Div('Odds: Lower the number = Less money you can win'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(title='Weather Conditions, Odds, and Predicted Places of First Place Kentucky Derby Horses',
                                      xaxis={'title': 'Year'}, yaxis={'title': 'Variables'})
              }
              ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble Charts', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represents the max temperatures for the Triple Crown Races during different weather conditions.'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='Average Temperatures of the Triple Crown Races',
                                      xaxis={'title': 'Weather Condition'},
                                      yaxis={'title': 'Max Temperature'},
                                      hovermode='closest')
              }
              ),
    html.Br(),
    html.Br(),
    html.Div(
        'This bubble chart represents the track conditions for the Triple Crown Races during the min temperatures.'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bubble_min,
                  'layout': go.Layout(title='Low Temperatures and Track Conditions',
                                      xaxis={'title': 'Year'},
                                      yaxis={'title': 'Track Conditions'},
                                      hovermode='closest')
              }
              ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat Maps', style={'color': '#df1e56'}),
    html.Div(
        'These heat maps represent the high and low temperatures each year at Triple Crown Races'),
    html.Br(),
    html.Div('High Temperatures:'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_heatmap_high,
                  'layout': go.Layout(title='High Temperatures Each Year at the Triple Crown Races',
                                      xaxis={'title': 'Year'}, yaxis={'title': 'Race'})
              }
              ),
    html.Br(),
    html.Div('Low Temperatures:'),
    dcc.Graph(id='graph8',
              figure={
                  'data': data_heatmap_low,
                  'layout': go.Layout(title='Low Temperatures Each Year at the Triple Crown Races',
                                      xaxis={'title': 'Year'}, yaxis={'title': 'Race'})
              }
              )
])


if __name__ == '__main__':
    app.run_server()