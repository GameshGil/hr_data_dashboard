"""Initializie Dash app."""
from flask import url_for
from dash import Dash, html, dcc, Output, Input, dash_table
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
        html.Header(children=html.Div(
            children=html.A(
                children=[
                    html.Img(
                        className='logo_img',
                        # src=f"{url_for('static', filename='img/logo.png')}"
                        src="my_dash/static/img/logo.png"
                    ),
                    html.H1(
                        children='HR Dash', className='logo_title'
                    ),
                ], href="/", className='logo_ref'
                # ], href=f"{url_for('loading_data')}", className='logo_ref'
            ), className='container header_cont',
        ), className='header'),
        html.Div(
            children=html.A(
                children="Разослать отчеты",
                href="/post_reports",
                className="send_reports_btn ref_btn"
            ), className='send_reports_cont'
        ),
        dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
        # Отрисовка графика, определяемого через ф-ию коллбэка.
        # Сама функция создана ниже.
        dcc.Graph(id='graph-content'),
        # Отрисовка обычной таблицы с данными
        dash_table.DataTable(data=df.to_dict('records'), page_size=10),
        # Отрисовка гистограммы
        dcc.Graph(
            figure=px.histogram(
                df,
                x='continent',
                y='lifeExp',
                histfunc='avg'
            )
        ),
        # Отрисовка круговой диаграммы
        dcc.Graph(
            figure=px.pie(
                df,
                values='pop',
                names='continent',
                title='Population of European continent',
                height=500
            ),
        ),
    ], style={'backgound-color': '#fff'})

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
