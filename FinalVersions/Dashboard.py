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
html.Hr(style={'color': '#7FDBFF'}),
html.H4(children='The Triple Crown Races is comprised of the Kentucky Derby, Preakness Stakes (or just Preakness), and the Belmont Stakes.',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Br(),
    html.Div('Terms to Know:', style={'textAlign': 'center'}),
    html.Div('WIN: To get this money, you have to bet that horse wins the race.', style={'textAlign': 'center'}),
    html.Div('PLACE: To get this money, you have to bet that horse finishes in the top 2.', style={'textAlign': 'center'}),
    html.Div('SHOW: To get this money, you have to bet that horse finishes in the top 3', style={'textAlign': 'center'}),
    html.Div('NOTE:', style={'textAlign': 'center'}),
    html.Div('Horses that don\'t finish in the top 3 have no win/place/show amount.', style={'textAlign': 'center'}),
html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Top Trainers', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the placement amounts of the top 10 trainers in each of the races.'),
    html.Div('(Use the drop down menu under the chart to change which race and placement type you are looking at.)'),
    dcc.Graph(id='graph1'),
    html.Div('Select a Race:', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='bar-race',
        options=[
            {'label': 'Kentucky Derby', 'value': 'Kentucky Derby'},
            {'label': 'Preakness', 'value': 'Preakness'},
            {'label': 'Belmont Stakes', 'value': 'Belmont Stakes'}
        ],
        value='Kentucky Derby'
    ),
    html.Br(),
html.Div('Select a Placement Type:', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='bar-amount',
        options=[
            {'label': 'Win', 'value': 'Win'},
            {'label': 'Place', 'value': 'Place'},
            {'label': 'Show', 'value': 'Show'}
        ],
        value='Win'
    ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Placement Averages', style={'color': '#df1e56'}),
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
    html.H3('Weather\'s Impact on Horses', style={'color': '#df1e56'}),
    html.Div(
        'This multiline chart represents the weather and predicted placement of the first place horses.'),
    html.Br(),
    html.Div('Weather: Lower the number = Worse Conditions'),
    html.Div('Predicted Place: Lower the number = Higher place (1st/2nd/3rd/etc.)'),
    html.Div('Odds: Lower the number = Less money you can win'),
    html.Div('(Use the drop down menu under the chart to change which race you are looking at.)'),
    dcc.Graph(id='graph4'),
html.Div('Select a Race', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-race',
        options=[
            {'label': 'Kentucky Derby', 'value': 'Kentucky Derby'},
            {'label': 'Preakness', 'value': 'Preakness'},
            {'label': 'Belmont Stakes', 'value': 'Belmont Stakes'}
        ],
        value='Kentucky Derby'
    ),
    html.Br(),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Track Conditions', style={'color': '#df1e56'}),
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
    html.H3('Temperatures', style={'color': '#df1e56'}),
    html.Div('These heat maps represent the high and low temperatures each year at Triple Crown Races'),
    html.Div('(Use the drop down menu under the chart to change which temperatures (low or high) you are looking at.)'),
    html.Br(),
    dcc.Graph(id='graph7'),
    html.Br(),
    html.Div('Select a Race:', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='temp-type-combo',
        options=[
            {'label': 'High Temperatures', 'value': 'high_temp'},
            {'label': 'Low Temperatures', 'value': 'low_temp'},
        ],
        value='high_temp'
    ),
    html.Br()
])


@app.callback(Output('graph1', 'figure'),
              [Input('bar-race', 'value'), Input('bar-amount', 'value')])
def update_bar(bar_race, bar_amount):
    bar_df = df2[df2['race'] == bar_race]

    bar_df = bar_df.groupby(['Trainer'])[bar_amount].sum().reset_index()
    bar_df = bar_df.sort_values(by=[bar_amount], ascending=[False]).head(10).reset_index()
    data_interactive_barchart = [go.Bar(x=bar_df['Trainer'], y=bar_df[bar_amount])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title=bar_amount+' Amount of Top 10 Trainers in '+bar_race,
                                                                   xaxis={'title': 'Trainers'},
                                                                   yaxis={'title': 'Money Back/per $2'})}


@app.callback(Output('graph4', 'figure'),
              [Input('select-race', 'value')])
def update_multi(selected_race, df2 = df2, df1 = df1):
    df1_temp = df1[df1['race'] == selected_race]
    df2_temp = df2[df2['race'] == selected_race]
    df2_temp = df2_temp[df2_temp["final_place"] == 1]

    trackNum = []
    for i in range(len(df1_temp)):
        if df1.at[i, 'track_condition'] == "Fast":
            trackNum.append(20)
        elif df1.at[i, 'track_condition'] == "Sloppy":
            trackNum.append(10)
        else:
            trackNum.append(1)

    df1_temp['trackNum'] = trackNum

    trace1 = go.Scatter(x=df2_temp['year'], y=df2_temp['Odds'], mode='lines', name='odds')
    trace2 = go.Scatter(x=df2_temp['year'], y=df2_temp['PP'], mode='lines', name='predicted place')
    trace3 = go.Scatter(x=df1_temp['year'], y=df1_temp['trackNum'], mode='lines', name='track conditions')
    data = [trace1, trace2, trace3]

    layout = go.Layout(title='Weather Conditions and Predicted Places in First Place '+selected_race+' Horses',
                       xaxis_title="year", yaxis_title="variables")
    return {'data': data, 'layout': layout}


@app.callback(Output('graph7', 'figure'),
              [Input('temp-type-combo', 'value')])
def update_heatcombo(temp_type):
    heat_df = [go.Heatmap(x=df1['year'],
                y=df1['race'],
                z=df1[temp_type].values.tolist(),
                colorscale='Jet')]

    temp_type_str = ''

    if(temp_type == 'low_temp'):
        temp_type_str = 'Low'
    elif(temp_type == 'high_temp'):
        temp_type_str ='High'

    return {'data': heat_df, 'layout': go.Layout(title=temp_type_str+' Temperatures Each Year at the Triple Crown Races',
                                                                   xaxis={'title': 'Year'},
                                                                   yaxis={'title': 'Race'})}


if __name__ == '__main__':
    app.run_server()