from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/'
                 'master/gapminder_unfiltered.csv')


def init_dashboard():
    dash_app = Dash(
        requests_pathname_prefix="/dashboards1/",
        external_stylesheets=[
                '/static/css/style.css',
            ])

    dash_app.layout = html.Div([
        html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
        dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
        dcc.Graph(id='graph-content')
    ])

    init_callbacks(dash_app)
    return dash_app


def init_callbacks(dash_app):
    @dash_app.callback(
        Output('graph-content', 'figure'),
        Input('dropdown-selection', 'value')
    )
    def update_graph(value):
        dff = df[df.country == value]
        return px.line(dff, x='year', y='pop')
