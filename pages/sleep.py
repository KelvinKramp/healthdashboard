# source: https://medium.com/analytics-vidhya/using-sentiment-analysis-to-predict-the-stock-market-77100295d753

# IMPORT MODULES
from dash import html
from dash.dependencies import Input, Output
from dash import dcc
import plotly.graph_objects as go
import os
import json
# IMPORT MODULES
from dash import html
from dash.dependencies import Input, Output
from dash import dcc
from dash import dash_table

import dash_bootstrap_components as dbc
from datetime import date
from datetime import datetime as dt
from dateutil import parser
import plotly.express as px
from datetime import timedelta
from calculations.sleep import sleep_data
from plotly.subplots import make_subplots
from definitions import min_date, max_date

def convert_to_datetime(date):
    return parser.parse(date)


# ---------------------------------------------------------------


layout = html.Div([
    html.Br(),
    html.H1("", id='sleep', style={'textAlign': 'center'}),
    dbc.Row([
            dbc.Col(
                dbc.Row([
                    html.Div([
                        dcc.DatePickerRange(
                            id='my-date-picker-range-5',
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
                            initial_visible_month=max_date,
                            display_format='D-M-Y',
                            start_date=max_date-timedelta(8),
                            end_date=max_date-timedelta(1),
                            # end_date=dt.now().date()
                        ),
                    ], style={'text-align': 'center', 'margin': 'auto', 'width': '50%'}, className='justify-content-center'),
                    html.Br(),
                ])
            ),
            ],
            justify="center",
        ),
    html.Br(),
    html.Div(id='graph-3', children=[]),
    html.Br(),
    ])


if __name__ == '__main__':
    from app.app import app
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8081, debug=True, use_reloader=True)