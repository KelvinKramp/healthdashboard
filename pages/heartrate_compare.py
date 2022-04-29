# IMPORT MODULES
from dash import html
from dash.dependencies import Input, Output
from dash import dcc
from dash import dash_table
from app.app import app
import dash_bootstrap_components as dbc
from datetime import date
from datetime import datetime as dt
from calculations.heartrate import heartrate_data
from dateutil import parser
import plotly.express as px
from definitions import min_date, max_date
from datetime import timedelta
# ---------------------------------------------------------------
# FUNCTIONS

def convert_to_datetime(date):
    return parser.parse(date)

# ---------------------------------------------------------------
# LAYOUT
layout = html.Div([
    html.Br(),
    html.H1("", id='histograms-overview', style={'textAlign': 'center'}),
    dbc.Row([
            dbc.Col(
                dbc.Row([
                    html.Div([
                        dcc.DatePickerRange(
                            id='my-date-picker-range-left',
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
                            initial_visible_month=max_date,
                            display_format='D-M-Y',
                            start_date=max_date-timedelta(8),
                            end_date=max_date-timedelta(1),
                            # end_date=dt.now().date()
                        ),
                    ], style={'text-align': 'center', 'margin': 'auto', 'width': '50%'}, className='justify-content-center'),
                    dbc.Row([
                        html.Br(),
                        html.Div(""),
                    ]),
                    html.Div(id='graph-left', ),
                    html.Br(),
                ])
            ),
            dbc.Col(
                dbc.Row([
                    html.Div([
                        dcc.DatePickerRange(
                            id='my-date-picker-range-right',
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
                            initial_visible_month=max_date,
                            display_format='D-M-Y',
                            start_date=max_date-timedelta(8),
                            end_date=max_date-timedelta(1),
                            # end_date=dt.now().date()
                        ),
                    ], style={'text-align': 'center', 'margin': 'auto', 'width': '50%'}, className='justify-content-center'),
                    dbc.Row([
                        html.Br(),
                        html.Div(""),
                    ]),
                    html.Div(id='graph-right', ),
                    html.Br(),
                ])
            ),
            ],
            justify="center",
        ),

    ])

if __name__ == '__main__':
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)