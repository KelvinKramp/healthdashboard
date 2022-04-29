# IMPORT MODULES
from dash import html
from dash import dcc
from app.app import app
import dash_bootstrap_components as dbc
from datetime import date
from datetime import datetime as dt
from dateutil import parser
from datetime import timedelta
from definitions import min_date, max_date
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
                            id='my-date-picker-range',
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
                    dbc.Row([
                        html.Br(),
                        html.Div(""),
                    ]),
                    html.Div(id='graph', ),
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