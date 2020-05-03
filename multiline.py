import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

app = dash.Dash()

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/TrackConditions.csv')
df2 = pd.read_csv('../Datasets/TripleCrownRaces_2005-2019.csv')

#layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive multiline chart', style={'color': '#df1e56'}),
    html.Div('Weather Conditions and Predicted Places in First Place horse of selected races.'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a race', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-race',
        options=[
            {'label': 'Kentucky Derby', 'value': 'Kentucky Derby'},
            {'label': 'Preakness', 'value': 'Preakness'},
            {'label': 'Belmont Stakes', 'value': 'Belmont Stakes'},
        ],
        value='Kentucky Derby'
    )
])



@app.callback(Output('graph1', 'figure'),
              [Input('select-race', 'value')])
def update_figure(selected_race, df2 = df2, df1 = df1):
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

    layout = go.Layout(title='Weather Conditions and Predicted Places in First Place Kentucky Derby Horses',
                       xaxis_title="year", yaxis_title="variables")
    # Plot the figure and saving in a html file
   # fig = go.Figure(data=data, layout=layout)
    #pyo.plot(fig)

    # filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    # new_df = filtered_df.groupby(['Country'])['Confirmed'].sum().reset_index()
    # new_df = new_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)
    # data_interactive_barchart = [go.Bar(x=new_df['Country'], y=new_df['Confirmed'])]
    return {'data': data, 'layout': layout}


if __name__ == '__main__':
    app.run_server()


