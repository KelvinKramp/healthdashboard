# source: https://medium.com/analytics-vidhya/using-sentiment-analysis-to-predict-the-stock-market-77100295d753

# IMPORT MODULES
from dash import html
from dash.dependencies import Input, Output, State
from dash import dcc
from app.app import app
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import timedelta
# from definitions import min_date, max_date
# print(df.columns)
# print(df)
from calculations.create_dataframe import get_df
import dash
from datetime import datetime as dt

# get dataframe
global df
df = get_df()


time_period_options = [
    {'label': 'Day', 'value': 'D'},
    {'label': 'Week', 'value': '7D'},
    {'label': 'Two weeks', 'value': '14D'},
    {'label': 'Month', 'value': 'M'},
    {'label': 'Season', 'value': '3M'},
    {'label': 'Year', 'value': '12M'},
    ]


viz_style_options = [
    {'label': 'TIR', 'value': 'TIR'},
    {'label': 'Percentile', 'value': 'percentile'},
    {'label': 'Average', 'value': 'average'},
    {'label': 'Median', 'value': 'median'},
    # {'label': 'Pie chart', 'value': 'Pie chart}'},
    ]


TIR = {
    "Within":"Within range",
    "Hypo": "Hypo",
    "Hyper": "Hyper",
}


glucose_values_slider = {
                    2: {'label': '2', 'style': {'color': '#FFA500', 'font-weight': 'bold'}},
                    4: '4',
                    6: '6',
                    8: '8',
                    10: '10',
                    12: {'label': '12', 'style': {'color': '#f50', 'font-weight': 'bold'}},
                    14: {'label': '14', 'style': {'color': '#f50', 'font-weight': 'bold'}},
                }

percentiles = {
    10:"10th percentile",
    25:"25th percentile",
    50:"median",
    75:"75th percentile",
    90:"90th percentile",
}





layout = html.Div([
    html.Br(),
    html.H1("Glucose", id='glucose', style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.DatePickerRange(
                    id='date-picker-glucose',
                    min_date_allowed=None,
                    max_date_allowed=None,
                    initial_visible_month=dt.now().date(),
                    display_format='D-M-Y',
                    start_date=None,
                    end_date=None,
                    style={"border": "0px"},
                    # end_date=dt.now().date()
                ),
            ], style={'text-align': 'center', 'margin': 'auto', "margin-top": "10px",'width': '100%'}, className='justify-content-center'),
        ]),
        dbc.Col([
            html.Div([
                dcc.Dropdown(id='time-period-glucose',
                             options=time_period_options,
                             optionHeight=35,  # height/space between dropdown options
                             value='M',  # dropdown value selected automatically when page loads
                             disabled=False,  # disable dropdown value selection
                             multi=False,  # allow multiple dropdown values to be selected
                             searchable=True,  # allow user-searching of dropdown values
                             search_value='',  # remembers the value searched in dropdown
                             placeholder='Please select...',  # gray, default text shown when no option is selected
                             clearable=True,  # allow user to removes the selected value
                             ),  # 'memory': browser tab is refreshed
            ], style={'text-align': 'center', 'margin': 'auto', 'width': '80%',"margin-top": "10px", "vertical-align": "baseline"}, className='justify-content-center'),
        ]),
        dbc.Col([
            html.Div([
                dcc.Dropdown(id='viz-style-glucose',
                             options=viz_style_options,
                             optionHeight=35,  # height/space between dropdown options
                             value='percentile',  # dropdown value selected automatically when page loads
                             disabled=False,  # disable dropdown value selection
                             multi=False,  # allow multiple dropdown values to be selected
                             searchable=True,  # allow user-searching of dropdown values
                             search_value='',  # remembers the value searched in dropdown
                             placeholder='Please select...',  # gray, default text shown when no option is selected
                             clearable=True,  # allow user to removes the selected value
                             ),  # 'memory': browser tab is refreshed
            ], style={'text-align': 'center', 'margin': 'auto', 'width': '80%',"margin-top": "10px", "vertical-align": "baseline"}, className='justify-content-center'),
        ]),
        dbc.Col([
            html.Div([
                dbc.Button("Show", id="show", style={"margin": "10px"}),
                dbc.Button("Download", id="download"),
                dcc.Download(id="download-text")
            ], style={'text-align': 'top',  'width': '80%', "vertical-align": "top"}, ),
        ],style={'text-align': 'top', 'width': '80%', "vertical-align": "top"},
        ),
    ],style={'text-align': 'center', 'margin': 'auto', 'width': '80%'},
    ),
    dbc.Row([
        html.Div([
            html.Div("Normal Range", style={"text-align":"center"}),
            dcc.RangeSlider(
                id='my-range-slider',  # any name you'd like to give it
                marks=glucose_values_slider,
                step=0.5,  # number of steps between values
                min=1,
                max=15,
                value=[4, 11],  # default value initially chosen
                dots=True,  # True, False - insert dots, only when step>1
                allowCross=False,  # True,False - Manage handle crossover
                disabled=False,  # True,False - disable handle
                pushable=2,  # any number, or True with multiple handles
                updatemode='mouseup',  # 'mouseup', 'drag' - update value method
                included=True,  # True, False - highlight handle
                vertical=False,  # True, False - vertical, horizontal slider
                verticalHeight=900,  # hight of slider (pixels) when vertical=True
                className='None',
                tooltip={'always_visible': False,  # show current slider values
                         'placement': 'bottom'},
            ),
        ], className='justify-content-center'),
    ],style={'text-align': 'center', 'margin': 'auto', "margin-top": "20px",'width': '80%'},
    ),
    html.Br(),
    html.Div(id='graph-1', ),
    html.Br(),
    ])


# WEIGHT CALLBACK
@app.callback(
    Output(component_id='graph-1', component_property='children'),
    Output("download-text", "data"),
    Output("date-picker-glucose", "start_date"),
    Output("date-picker-glucose", "end_date"),
    [Input(component_id='show', component_property='n_clicks'),
    Input(component_id='download', component_property='n_clicks'),
    Input('my-range-slider','value'),
     ],
    State(component_id='date-picker-glucose', component_property='start_date'),
    State(component_id='date-picker-glucose', component_property='end_date'),
    State(component_id='time-period-glucose', component_property='value'),
    State(component_id='viz-style-glucose', component_property='value'),
    # prevent_initial_call=True,
)
def update_output_glucose(click_show, click_download, slider, date_picker_glucose_start, date_picker_glucose_end, time_period_glucose, viz_style_glucose):
    ctx = dash.callback_context
    interaction_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # get dataframe
    df = get_df()

    # # set min and max date based on df start and end
    # print(df.columns)
    min_date = df.iloc[[-1]]["dateString"].squeeze().date()
    max_date = df.iloc[[0]]["dateString"].squeeze().date()
    print(repr(min_date))
    print(type(min_date))
    print(repr(max_date))
    print(type(max_date))
    print(len(df))

    # slice to specified time
    df = df.set_index("dateString")
    df = df[date_picker_glucose_start:date_picker_glucose_end]
    df = df.reset_index()

    # get normal range and convert to mg/dl
    lower_limit = slider[0]/0.0555
    upper_limit = slider[1]/0.0555

    # create empty graph object
    fig = go.Figure()

    # viz style
    print(viz_style_glucose)

    # TIR
    if viz_style_glucose == "TIR":
        df["within_range"] = df['sgv'].apply(lambda x: 1 if (x <= upper_limit) & (x > lower_limit) else 0)
        df["hypo"] = df['sgv'].apply(lambda x: 1 if (x <= lower_limit) else 0)
        df["hyper"] = df['sgv'].apply(lambda x: 1 if (x > upper_limit) else 0)
        df = df.resample(time_period_glucose, on='dateString').mean().reset_index()
        fig.add_trace(
            go.Scatter(x=df["dateString"], y=df["within_range"].apply(lambda x: x*100), mode='lines', name=TIR['Within'],
                       connectgaps=True, ))
        fig.add_trace(
            go.Scatter(x=df["dateString"], y=df["hypo"].apply(lambda x: x*100), mode='lines', name=TIR['Hypo'],
                       connectgaps=True, ))
        fig.add_trace(
            go.Scatter(x=df["dateString"], y=df["hyper"].apply(lambda x: x*100), mode='lines', name=TIR['Hyper'],
                       connectgaps=True, ))
        fig.update_yaxes(
            title_text="Percentage",
            # title_standoff=25
        )

    # percentile chart
    if viz_style_glucose == "percentile":
        df = df[['dateString', 'sgv']]
        df = df.set_index("dateString")
        df3 = pd.DataFrame()
        # object = df.resample(time_period_glucose, on='dateString')
        # df = object.quantile(1)[['sgv']]
        percentile_values = [10, 25, 50, 75, 90]
        for i in percentile_values:
            # df[str(i)] = object.quantile((i/100))[['sgv']]
            df2 = df.groupby(pd.Grouper(freq=time_period_glucose)).quantile(i / 100)[['sgv']]
            df3[str(i)] = df2["sgv"]
        df = df3
        fig.add_trace(
            go.Scatter(x=df.index.to_list() + df.index.to_list()[::-1], y=df["10"].apply(lambda x: x * 0.0555).to_list()+df["25"].apply(lambda x: x * 0.0555).to_list()[::-1],
                       fill='toself',
                       fillcolor='#dfdfec',
                       line=dict(color='#8080b3', width=1),
                       showlegend=False
                       ))
        fig.add_trace(
            go.Scatter(x=df.index.to_list() + df.index.to_list()[::-1], y=df["25"].apply(lambda x: x * 0.0555).to_list()+df["50"].apply(lambda x: x * 0.0555).to_list()[::-1],
                       fill='toself',
                       fillcolor='#9999ff',
                       line=dict(color='#8080b3', width=1),
                       showlegend=False
                       ))
        fig.add_trace(
            go.Scatter(x=df.index.to_list() + df.index.to_list()[::-1], y=df["50"].apply(lambda x: x * 0.0555).to_list()+df["75"].apply(lambda x: x * 0.0555).to_list()[::-1],
                       fill='toself',
                       fillcolor='#9999ff',
                       line=dict(color='black', width=2),
                       showlegend=False
                       ))
        fig.add_trace(
            go.Scatter(x=df.index.to_list() + df.index.to_list()[::-1], y=df["75"].apply(lambda x: x * 0.0555).to_list()+df["90"].apply(lambda x: x * 0.0555).to_list()[::-1],
                       fill='toself',
                       fillcolor='#dfdfec',
                       line=dict(color='#8080b3', width=1),
                       showlegend=False
                       ))


        fig.add_trace(
            go.Scatter(x=df.index, y=df["10"].apply(lambda x: x * 0.0555),
                       line=dict(color='#8080b3', width=1),
                       showlegend=True,
                       name=percentiles[10]
                       ))
        fig.add_trace(
            go.Scatter(x=df.index, y=df["25"].apply(lambda x: x * 0.0555),
                       line=dict(color='#8080b3', width=3),
                       showlegend=True,
                       name=percentiles[25]
                       ))
        fig.add_trace(
            go.Scatter(x=df.index, y=df["50"].apply(lambda x: x * 0.0555),
                       line=dict(color='black', width=3),
                       showlegend=True,
                       name=percentiles[50]
                       ))
        fig.add_trace(
            go.Scatter(x=df.index, y=df["75"].apply(lambda x: x * 0.0555),
                       line=dict(color='#8080b3', width=1),
                       showlegend=True,
                       name=percentiles[75]
                       ))
        fig.add_trace(
            go.Scatter(x=df.index, y=df["90"].apply(lambda x: x * 0.0555),
                       line=dict(color='#8080b3', width=1),
                       showlegend=True,
                       name=percentiles[90]
                       ))

        fig.update_yaxes(
            title_text="Percentiles",
            # title_standoff=25
        )


    # average
    elif viz_style_glucose == "average":
        df = df.resample(time_period_glucose, on='dateString').mean().reset_index()
        fig.add_trace(
            go.Scatter(x=df["dateString"], y=df["sgv"].apply(lambda x: x * 0.0555), mode='lines', name=viz_style_glucose,
                       connectgaps=True, ))
        fig.update_yaxes(
            title_text="Average",
            # title_standoff=25
        )
    # median
    elif viz_style_glucose == "median":
        df = df.resample(time_period_glucose, on='dateString').median().reset_index()
        fig.add_trace(
            go.Scatter(x=df["dateString"], y=df["sgv"].apply(lambda x: x * 0.0555), mode='lines', name=viz_style_glucose,
                       connectgaps=True, ))
        fig.update_yaxes(
            title_text="Median",
            # title_standoff=25
        )


    list_graphs = []
    list_graphs.append(
        html.Div(dcc.Graph(
            id="weight",
            figure=fig
        ))
    )

    if interaction_id == "download":
        return list_graphs, dict(content=df.to_string(), filename="data.txt"), min_date, max_date
    return list_graphs, None, min_date, max_date


if __name__ == '__main__':
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)