# source: https://medium.com/analytics-vidhya/using-sentiment-analysis-to-predict-the-stock-market-77100295d753

import plotly.graph_objects as go
# IMPORT MODULES
from app.app import app
from calculations.sleep import sleep_data
from plotly.subplots import make_subplots
from dateutil import parser
from dash import html
from dash.dependencies import Input, Output
from dash import dcc
import dash_bootstrap_components as dbc
from dateutil import parser
import plotly.express as px
from calculations.heartrate import heartrate_data
from calculations.weight import weight_data
import pandas as pd

df_weight = pd.DataFrame()

def convert_to_datetime(date):
    return parser.parse(date)



# HEARTRATE CALLBACKS

@app.callback(
    Output('graph', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),)
def update_output_heartrate_one_view(start_date_left, end_date_left,):
    list_graphs_left, list_graphs_right =[], []
    if start_date_left is not None:
        if end_date_left is not None:
            HR, df_summary_stats = heartrate_data(start_date_left, end_date_left)
            start_date = convert_to_datetime(start_date_left).date().strftime("%d-%m-%Y")
            end_date = convert_to_datetime(end_date_left).date().strftime("%d-%m-%Y")
            title = "Heartrate in a histogram from period {} to {} ".format(start_date, end_date)
            fig1 = px.histogram(HR, x="Heart Rate", nbins=26, range_x=[50, 180], title=title, )
            fig1.update_layout(bargap=0.2)
            list_graphs_left.append(
                html.Div([
                    dbc.Table.from_dataframe(df_summary_stats,
                        style = {'backgroundColor': 'white'}
                                             )
                ],
                    style={'marginLeft': 'auto', 'marginRight': 'auto', 'width': '50%', 'justify-content': 'center'}
                )
            )
            list_graphs_left.append(
                html.Div(dcc.Graph(
                id="histo",
                figure=fig1
                ))
            )
            title = "Heartrate in daily boxplots from period {} to {} ".format(start_date, end_date)
            fig2 = px.box(HR, x="day", y="Heart Rate", points="all", title=title,)
            list_graphs_left.append(
                html.Div(dcc.Graph(
                id="boxplot",
                figure=fig2
                ))
            )
    return list_graphs_left

# HEARTRATE CALLBACK DOUBLE VIEW

@app.callback(
    Output('graph-left', 'children'),
    Output('graph-right', 'children'),
    Input('my-date-picker-range-left', 'start_date'),
    Input('my-date-picker-range-left', 'end_date'),
    Input('my-date-picker-range-right', 'start_date'),
    Input('my-date-picker-range-right', 'end_date'))
def update_output_heartrate_double_view(start_date_left, end_date_left, start_date_right, end_date_right):
    list_graphs_left, list_graphs_right =[], []
    if start_date_left is not None:
        if end_date_left is not None:
            start_date = convert_to_datetime(start_date_left).date().strftime("%d-%m-%Y")
            end_date = convert_to_datetime(end_date_left).date().strftime("%d-%m-%Y")
            # print("start date", start_date)
            # print("end date", end_date)
            HR, df_summary_stats = heartrate_data(start_date_left, end_date_left)

            list_graphs_left.append(
                dbc.Card(html.H5(children="Summary stats",
                                             className="text-center text-light bg-primary"), body=True, color="primary")
            )
            list_graphs_left.append(
                html.Div([
                    dbc.Table.from_dataframe(df_summary_stats,
                        style = {'backgroundColor': 'white'}
                                             )
                ],
                    style={'marginLeft': 'auto', 'marginRight': 'auto', 'width': '50%', 'justify-content': 'center'}
                )
            )
            title = "Histogram from period {} to {} ".format(start_date, end_date)
            list_graphs_left.append(
                dbc.Card(html.H5(children=title,
                                             className="text-center text-light bg-primary"), body=True, color="primary")
            )
            fig1 = px.histogram(HR, x="Heart Rate", nbins=26, range_x=[50, 180],)
            fig1.update_layout(bargap=0.2)
            list_graphs_left.append(
                html.Div(dcc.Graph(
                id="histo",
                figure=fig1
                ))
            )
            title = "Boxplots from period {} to {} ".format(start_date, end_date)
            list_graphs_left.append(
                dbc.Card(html.H5(children=title,
                                             className="text-center text-light bg-primary"), body=True, color="primary")
            )
            fig2 = px.box(HR, x="day", y="Heart Rate", points="all",)
            list_graphs_left.append(
                html.Div(dcc.Graph(
                id="boxplot",
                figure=fig2
                ))
            )
    if start_date_right is not None:
        if end_date_right is not None:
            start_date = convert_to_datetime(start_date_right).date().strftime("%d-%m-%Y")
            end_date = convert_to_datetime(end_date_right).date().strftime("%d-%m-%Y")
            # print("start date", start_date)
            # print("end date", end_date)
            HR, df_summary_stats = heartrate_data(start_date_right, end_date_right)

            list_graphs_right.append(
                dbc.Card(html.H5(children="Summary stats",
                                             className="text-center text-light bg-primary"), body=True, color="primary")
            )
            list_graphs_right.append(
                html.Div([
                    dbc.Table.from_dataframe(df_summary_stats,
                        style = {'backgroundColor': 'white'}
                                             )
                ],
                    style={'marginLeft': 'auto', 'marginRight': 'auto', 'width': '50%', 'justify-content': 'center'}
                )
            )
            title = "Histogram from period {} to {} ".format(start_date, end_date)
            list_graphs_right.append(
                dbc.Card(html.H5(children=title,
                                             className="text-center text-light bg-primary"), body=True, color="primary")
            )
            fig1 = px.histogram(HR, x="Heart Rate", nbins=26, range_x=[50, 180],)
            fig1.update_layout(bargap=0.2)
            list_graphs_right.append(
                html.Div(dcc.Graph(
                id="histo",
                figure=fig1
                ))
            )
            title = "Boxplots from period {} to {} ".format(start_date, end_date)
            list_graphs_right.append(
                dbc.Card(html.H5(children=title,
                                             className="text-center text-light bg-primary"), body=True, color="primary")
            )
            fig2 = px.box(HR, x="day", y="Heart Rate", points="all",)
            list_graphs_right.append(
                html.Div(dcc.Graph(
                id="boxplot",
                figure=fig2
                ))
            )
    return list_graphs_left, list_graphs_right


# WEIGHT CALLBACK
@app.callback(
    Output(component_id='graph-1', component_property='children'),
    [Input(component_id='my_dropdown', component_property='value')]
)
def update_output_weight(dropdown_value):
    global df_weight
    if df_weight.empty:
        df_weight = weight_data("_", "_")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df_weight["dateTime"], y=df_weight[dropdown_value], mode='lines+markers', name=dropdown_value,
                   connectgaps=True, ))
    list_graphs = []
    list_graphs.append(
        html.Div(dcc.Graph(
            id="weight",
            figure=fig
        ))
    )
    return list_graphs


# SLEEP CALLBACK

@app.callback(
    Output('graph-3', 'children'),
    Input('my-date-picker-range-5', 'start_date'),
    Input('my-date-picker-range-5', 'end_date'),)
def update_output_sleep(start_date, end_date):
    list_graphs = []
    start_date = convert_to_datetime(start_date).date().strftime("%d-%m-%Y")
    end_date = convert_to_datetime(end_date).date().strftime("%d-%m-%Y")
    if start_date is not None:
        if end_date is not None:
            df = sleep_data(start_date, end_date)
            date = df['date'].tolist()
            light = df['light'].tolist()
            deep = df['deep'].tolist()
            rem = df['rem'].tolist()
            awake = df['wake'].tolist()
            fig = make_subplots(specs=[[{"secondary_y": True}]]) #
            fig.add_trace(go.Bar(x=date, y=light, name='Light', marker_color="#b4cde2"))
            fig.add_trace(go.Bar(x=date, y=deep, name='Deep', marker_color='#699cc5'))
            fig.add_trace(go.Bar(x=date, y=rem, name='Rem',marker_color='#3f75a2'))
            fig.add_trace(go.Bar(x=date, y=awake, name='Awake',marker_color='#315b7e'))
            fig.add_trace(
                go.Scatter(x=date, y=df["totalMinutesAsleep"].tolist(), mode='lines+markers', name='totalMinutesAsleep', marker_color='#8A2BE2',
                           connectgaps=True),secondary_y=False, )
            fig.add_trace(
                go.Scatter(x=date, y=df["totalTimeInBed"].tolist(), mode='lines+markers', name='totalTimeInBed', marker_color='#4B0082',
                           connectgaps=True, ),secondary_y=False, )
            fig.update_layout(hovermode="x unified")

            fig.update_layout(barmode='stack')
            list_graphs.append(
                html.Div(dcc.Graph(
                    id="sleep stages",
                    figure=fig
                ))
            )
        return list_graphs
    else:
        return None
