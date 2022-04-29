# IMPORT MODULES
from app.app import app, server
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from pages import blank, heartrate_overview, heartrate_compare, weight, sleep
import sys
from os import path
from dash.exceptions import PreventUpdate
from dateutil import parser
import plotly.express as px
import callbacks
import os

def convert_to_datetime(date):
    return parser.parse(date)

# # START APP
# app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])
# server = app.server


navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Overview",href='/hr-overview', n_clicks=0),
                dbc.DropdownMenuItem("Compare", href='/hr-compare', n_clicks=0),
            ],
            nav=True,
            in_navbar=True,
            label="Heartrate",
        ),
        dbc.NavItem(dbc.NavLink("Weight", href='/weight')),
        dbc.NavItem(dbc.NavLink("Sleep", href="/sleep")),
    ],
    brand="Health dashboard",
    brand_href="/",
    color="primary",
    dark=True,
    sticky='top',
)

app.title = 'Health Dashboard'
app.layout = html.Div(children=[
                            navbar,
                            dcc.Location(id='url', refresh=False),
                            html.Div(id="page-content", children=[
                            ]),
                            html.Br(),
                            html.Div(id='empyt-div',children=[]),
                            html.Div(id="hidden_div_for_redirect_callback", children=[]),
        ])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'href')])
def display_page(url):
    # https://github.com/plotly/dash/issues/468
    if "hr-overview" in url:
        return heartrate_overview.layout
    elif "hr-compare" in url:
        return heartrate_compare.layout
    elif "weight" in url:
        return weight.layout
    elif "sleep" in url:
        return sleep.layout
    else:
        return blank.layout



if __name__ == '__main__':
    if os.path.exists("local"):
        app.run_server(host='0.0.0.0', port=8081, debug=True)
    else:
        app.run_server(host='0.0.0.0', port=8081, debug=False)