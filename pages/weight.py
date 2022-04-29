# source: https://medium.com/analytics-vidhya/using-sentiment-analysis-to-predict-the-stock-market-77100295d753

# IMPORT MODULES
from dash import html
from dash.dependencies import Input, Output
from dash import dcc
from app.app import app
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json

import pandas as pd

# print(df.columns)
# print(df)

list_variables_smartscale = ['bone', 'fat', 'muscle','visceralFat',  'water', 'weight']

# ---------------------------------------------------------------
list_smartscale = [
            {'label': 'Weight', 'value': 'weight'},
            {'label': 'Fat', 'value': 'fat'},
            {'label': 'Visceral Fat', 'value': 'visceralFat'},
            {'label': 'Water', 'value': 'water'},
            {'label': 'Muscle', 'value': 'muscle'},
            {'label': 'Bone', 'value': 'bone'}
        ]

layout = html.Div([
    html.Br(),
    html.H1("", id='weight', style={'textAlign': 'center'}),
    html.Div([
        dcc.Dropdown(id='my_dropdown',
                     options=list_smartscale,
                     optionHeight=35,  # height/space between dropdown options
                     value='weight',  # dropdown value selected automatically when page loads
                     disabled=False,  # disable dropdown value selection
                     multi=False,  # allow multiple dropdown values to be selected
                     searchable=True,  # allow user-searching of dropdown values
                     search_value='',  # remembers the value searched in dropdown
                     placeholder='Please select...',  # gray, default text shown when no option is selected
                     clearable=True,  # allow user to removes the selected value
                     ),  # 'memory': browser tab is refreshed
    ], style={'text-align':'center', 'margin':'auto','width':'50%'}, className='justify-content-center'),
    html.Br(),
    html.Div(id='graph-1', ),
    html.Br(),
    ])



if __name__ == '__main__':
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)