"""Initializie Dash app."""
from dash import Dash, html, dcc, Output, Input
import pandas as pd
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
from datetime import date
import datetime
import plotly.graph_objects as go

app = Dash(__name__,
           external_stylesheets=["https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cerulean/bootstrap.min.css"])


card_height = '48rem'
card_height_s = '18rem'


engine = create_engine('postgresql://postgres:123123@localhost:5432/hackathon')


# Загрузка всех данных по письмам
df = pd.read_sql("human_data", engine)
df["date"] = pd.to_datetime(df["date"])
df.sort_values("date")

# Загрузка рейтинга сложности
rating = pd.read_sql("dep_rating", engine)
rating_access = pd.read_sql("dep_access_rating", engine)
# Данные всех работников
workers = pd.read_sql("workers", engine)

# Фильтр для выбора промежутка дат
date_filter = dbc.Row([
    dbc.Label("Период", html_for="date-filter"),
    dcc.DatePickerRange(
        id="date-filter",
        start_date=date(2022, 1, 1),
        end_date=date(2022, 10, 20),
        display_format='D MMM YYYY',
        style={
            'color': "#e5e5e5 !important",
        }
    )]
)

# Фильтр для выбора работника
worker_filter = dbc.Row([
    dbc.Label("Работник", html_for="worker-filter"),
    dcc.Dropdown(df.worker.unique(),
                 id="worker-filter",
                 value="Шамара Лапунов",
                 style={
                     'color': "#e5e5e5 !important",
                 }
                 )]
)

worker_indicators = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(
                                    "Общая информация о работнике",
                                    style={
                                        'font-size': 24,
                                        'text-align': 'left',
                                    },
                                ),
                                html.Br(),
                                html.Label(
                                    "Все ключевые показатели работника за выбранный период",
                                    style={
                                        'font-size': 14,
                                        'text-align': 'left',
                                        'color': '#808080',
                                        'font-family': 'sans-serif',
                                    },
                                    ),
                                html.Br()
                            ]),
                        dbc.Col([
                            dcc.Graph(id='main_procent',
                                      style={
                                          'height': '100%',
                                          'width': '100%',
                                          'float': 'left',
                                          # 'margin-right': '8px',
                                          'font-family': 'sans-serif',
                                      })
                        ])
                    ]),
                dcc.Graph(id='all_messages_period',
                          style={
                              'height': '75%',
                              'width': '16%',
                              'float': 'left',
                              'margin-right': '8px',
                              'font-family': 'sans-serif',
                          }),
                dcc.Graph(id='all_messages_output_period',
                          style={
                              'height': '75%',
                              'width': '16%',
                              'float': 'left',
                              'margin-right': '8px',
                              'font-family': 'sans-serif',
                          }),
                dcc.Graph(id='all_messages_read_delay',
                          style={
                              'height': '75%',
                              'width': '16%',
                              'float': 'left',
                              'margin-right': '8px',
                              'font-family': 'sans-serif',
                          }),
                dcc.Graph(id='all_messages_read_delay_days',
                          style={
                              'height': '75%',
                              'width': '16%',
                              'float': 'left',
                              'margin-right': '8px',
                              'font-family': 'sans-serif',
                          }),
                dcc.Graph(id='all_input_message_not_answer',
                          style={
                              'height': '75%',
                              'width': '16%',
                              'float': 'left',
                              'margin-right': '8px',
                              'font-family': 'sans-serif',
                          }),
                dcc.Graph(id='all_input_message_answer',
                          style={
                              'height': '75%',
                              'width': '16%',
                              'float': 'left',
                          }),
            ],
            style={
                'height': card_height_s,
            },
        ),
    ],
)

engagement_filter_for_line = dbc.Row(
    [
        dcc.Dropdown(
            id="engagement_dropdown_for_line",
            value="engagement",
            options=[{'label': 'Вовлечонность', 'value': 'engagement'},
                     {'label': 'Продуктивность', 'value': 'productivity'}],
        ),
    ], style={'max-width': '100%'},
)

worker_analytics = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col([
                            html.Label("Динамика вовлеченности сотрудника",
                                       style={'font-size': 24,
                                              'text-align': 'left',},
                                       ),
                            html.Br(),
                            html.Label(
                                "Динамика вовлеченности сотрудника за выбранный период.",
                                style={'font-size': 14,
                                       'text-align': 'left',
                                       'color': '#808080',
                                       },
                            ),
                        ], width=8),
                        dbc.Col(
                            engagement_filter_for_line,
                            width=4,
                        )
                    ]),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(id="engagement_draw", style={'height': '36rem'}),
                    )
                )
            ], style={
                'height': card_height,
            }
        )
    ]
)


def init_dashboard():
    dash_app = Dash(
        requests_pathname_prefix="/dashboards1/",
        external_stylesheets=[dbc.themes.SKETCHY])

    dash_app.layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col([
                        html.Label("Эффективность Работника", style={"text-align": "left", "font-size": 24}),
                        html.Br(),
                        html.Label("Дашборд позволяет посмотреть, эффективность работника",
                                   style={"text-align": "left", 'font-size': 16, "color": "#808080"})
                    ], width=4, style={'margin-top': '8px'}),
                    dbc.Col([
                        date_filter,
                    ], width=3),
                    dbc.Col([
                        worker_filter,
                    ], width=4)

                ]
            ),
            dbc.Row([
                dbc.Col([
                    worker_indicators,
                ]),
            ], style={'margin-bottom': '16px'}),
            dbc.Row([
                dbc.Col([
                    worker_analytics,
                ]),
            ], style={'margin-bottom': '16px'})

        ]
    )

    init_callbacks(dash_app)
    return dash_app


def init_callbacks(dash_app):
    @dash_app.callback(
        Output('main_procent', 'figure'),
        [
            Input('date-filter', 'start_date'),
            Input('date-filter', 'end_date'),
            Input('worker-filter', 'value'),

        ]
    )
    def update_profit_indicator(start_date, end_date, value):
        return get_static_message_engagement(df, start_date, end_date, value, "procent")

    # Входящие
    @dash_app.callback(
        Output('all_messages_period', 'figure'),
        [
            Input('date-filter', 'start_date'),
            Input('date-filter', 'end_date'),
            Input('worker-filter', 'value'),

        ]
    )
    def update_profit_indicator(start_date, end_date, value):
        return get_static_message(df, start_date, end_date, value, "input")

    # Исходящие
    @dash_app.callback(
        Output('all_messages_output_period', 'figure'),
        [
            Input('date-filter', 'start_date'),
            Input('date-filter', 'end_date'),
            Input('worker-filter', 'value'),

        ]
    )
    def update_profit_indicator(start_date, end_date, value):
        return get_static_message(df, start_date, end_date, value, "output")

    # Задержка
    @dash_app.callback(
        Output('all_messages_read_delay', 'figure'),
        [
            Input('date-filter', 'start_date'),
            Input('date-filter', 'end_date'),
            Input('worker-filter', 'value'),

        ]
    )
    def update_profit_indicator(start_date, end_date, value):
        return get_static_message(df, start_date, end_date, value, "days")

    @dash_app.callback(
        Output('all_messages_read_delay_days', 'figure'),
        [
            Input('date-filter', 'start_date'),
            Input('date-filter', 'end_date'),
            Input('worker-filter', 'value'),

        ]
    )
    def update_profit_indicator(start_date, end_date, value):
        return get_static_message(df, start_date, end_date, value, "delay")

    # вопросы без ответа
    @dash_app.callback(
        Output('all_input_message_answer', 'figure'),
        [
            Input('date-filter', 'start_date'),
            Input('date-filter', 'end_date'),
            Input('worker-filter', 'value'),

        ]
    )
    def update_profit_indicator(start_date, end_date, value):
        return get_static_message(df, start_date, end_date, value, "answers")

    @dash_app.callback(
        Output('all_input_message_not_answer', 'figure'),
        [
            Input('date-filter', 'start_date'),
            Input('date-filter', 'end_date'),
            Input('worker-filter', 'value'),

        ]
    )
    def update_profit_indicator(start_date, end_date, value):
        return get_static_message(df, start_date, end_date, value, "ans_q")

    @dash_app.callback(
        Output('engagement_draw', 'figure'),
        [
            Input('date-filter', 'start_date'),
            Input('date-filter', 'end_date'),
            Input('worker-filter', 'value'),
            Input('engagement_dropdown_for_line', 'value'),

        ]
    )
    def update_profit_indicator(start_date, end_date, value, value_type):
        if value_type == "productivity":
            return get_static_message_productivity(df, start_date, end_date, value)
        elif value_type == "engagement":
            return get_static_message_engagement(df, start_date, end_date, value)


def get_static_message(df, start_date, end_date, value, type_):

    if type_ == "input":
        label = "Входящие"
    elif type_ == "output":
        label = "Исходящие"
    elif type_ == "answers":
        label = "Ответы"
    elif type_ == "ans_q":
        label = "Вопросы без ответа"
    elif type_ == "delay":
        label = "Задержка дней"
    elif type_ == "days":
        label = "Задержка 4 часа"

    filtered_df = df.copy()
    if start_date is not None:
        if type(start_date) is str:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        filtered_df = filtered_df[filtered_df["date"] >= start_date]
    if end_date is not None:
        if type(end_date) is str:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        filtered_df = filtered_df[filtered_df["date"] <= end_date]
    filtered_df = filtered_df[filtered_df["worker"] == value]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered_df.groupby(pd.Grouper(key="date", freq='1W')).sum().index,
            y=filtered_df.groupby(pd.Grouper(key="date", freq='1W')).sum()[type_],
            name="",
            mode='lines',
            fill='tozerox',
            line_color='#b8d8d8',
            hoverinfo='skip',

        )
    )

    fig.add_trace(
        go.Indicator(
            mode='number',
            value=filtered_df.groupby(pd.Grouper(key="date", freq='1W')).sum()[type_].sum(),
            title={'text': label,
                   'font': {'size': 18,
                            'family': 'sans-serif',
                            },
                   },
            number={'prefix': " ",
                    'suffix': " ",
                    'font': {'size': 18,
                             'family': 'sans-serif',
                             },
                    },
            delta={'position': 'left',
                   'reference': 2,
                   'relative': True,
                   'font': {'size': 14,
                            'family': 'sans-serif',
                            },
                   },
            domain={'y': [0, 0.7], 'x': [0.25, 0.75]},
        ))
    fig.update_layout(autosize=True,
                      font={
                          'family': 'Roboto',
                      },
                      )
    fig.update_layout(
        xaxis={'showgrid': False,
               'showticklabels': False},
        yaxis={'showgrid': False,
               'showticklabels': False},
        plot_bgcolor='#eef5db',
        margin=dict(l=0, r=0, b=0, t=15),
        autosize=True,
    )
    return fig


def get_static_message_productivity(df, start_date, end_date, value):
    filtered_df = df.copy()
    if start_date is not None:
        if type(start_date) is str:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        filtered_df = filtered_df[filtered_df["date"] >= start_date]
    if end_date is not None:
        if type(end_date) is str:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        filtered_df = filtered_df[filtered_df["date"] <= end_date]
    filtered_df = filtered_df[filtered_df["worker"] == value]

    workers_dep = workers[workers["full_name"] == value]["department"].tolist()[0]

    import functools

    raiting = (rating[rating["id"] == workers_dep]).drop("id", axis=1)
    raiting = (functools.reduce(lambda a, b: a * b, (rating.values[0])))

    raiting_access = (rating_access[rating_access["id"] == workers_dep]).drop("id", axis=1)
    raiting_access = (functools.reduce(lambda a, b: a * b, (rating_access.values[0])))

    p = abs(round(
        (((filtered_df["output"] * raiting) / (filtered_df["input"] * raiting_access)) / (raiting / raiting_access)),
        2))

    filtered_df["point"] = p
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered_df.groupby(pd.Grouper(key="date", freq='1D')).min().dropna().index,
            y=filtered_df.groupby(pd.Grouper(key="date", freq='1D')).min().dropna().point * 100,

            name="",
            mode='lines',
            hoverinfo='skip',

        )
    )
    fig.add_trace(
        go.Indicator(
            mode='number',
            value=round(((filtered_df.groupby(pd.Grouper(key='date', freq='1D')).min().dropna()['point'].mean())), 2) * 100,

            title={'text': "Продуктивность",
                   'font': {'size': 18,
                            'family': 'sans-serif',
                            },
                   },
            number={'prefix': " ",
                    'suffix': "%",
                    'font': {'size': 18,
                             'family': 'sans-serif',
                             },
                    },
            delta={'position': 'left',
                   'reference': 2,
                   'relative': True,
                   'font': {'size': 14,
                            'family': 'sans-serif',
                            },
                   },
            domain={'y': [0, 0.7], 'x': [0.25, 0.75]},
        ))

    fig.update_layout(autosize=True,
                      font={
                          'family': 'Roboto',
                      },
                      yaxis={
                          'title': "Продуктивность",
                          'gridcolor': '#e5e5e5',
                          'tickmode': 'array',
                          'ticktext': list(range(1, 100))
                      }
                      )

    return fig


def get_static_message_engagement(df, start_date, end_date, value, type_=None):
    filtered_df = df.copy()
    if start_date is not None:
        if type(start_date) is str:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        filtered_df = filtered_df[filtered_df["date"] >= start_date]
    if end_date is not None:
        if type(end_date) is str:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        filtered_df = filtered_df[filtered_df["date"] <= end_date]
    filtered_df = filtered_df[filtered_df["worker"] == value]

    workers_dep = workers[workers["full_name"] == value]["department"].tolist()[0]

    import functools

    raiting = (rating[rating["id"] == workers_dep]).drop("id", axis=1)
    raiting = (functools.reduce(lambda a, b: a * b, (rating.values[0])))

    raiting_access = (rating_access[rating_access["id"] == workers_dep]).drop("id", axis=1)
    raiting_access = (functools.reduce(lambda a, b: a * b, (rating_access.values[0])))

    p = abs(round(
        (((filtered_df["output"] * raiting) / (filtered_df["input"] * raiting_access)) / (raiting / raiting_access)),
        2))

    filtered_df["point"] = p

    from statsmodels.tsa.seasonal import seasonal_decompose

    temporary = filtered_df.loc[:, ["date", "point"]]
    temporary["date"] = pd.to_datetime(temporary.date)
    temporary.set_index("date")
    temporary = temporary.set_index('date')
    temporary.sort_index(inplace=True)
    temporary = temporary.dropna()
    data = temporary.resample('1D').sum()
    decom = seasonal_decompose(data)
    if type_ is None:

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=decom.trend.index,
                y=decom.trend / 4,
                name="",
                mode='lines',
                hoverinfo='skip',

            )
        )
        fig.add_trace(
            go.Indicator(
                mode='number',
                value=(1 - decom.trend.min() / 4) * 100,

                title={'text': "Вовлеченность",
                       'font': {'size': 18,
                                'family': 'sans-serif',
                                },
                       },
                number={'prefix': " ",
                        'suffix': "%",
                        'font': {'size': 18,
                                 'family': 'sans-serif',
                                 },
                        },
                delta={'position': 'left',
                       'reference': 2,
                       'relative': True,
                       'font': {'size': 14,
                                'family': 'sans-serif',
                                },
                       },
                domain={'y': [0, 0.7], 'x': [0.25, 0.75]},
            ))

        fig.update_layout(autosize=True,
                          font={
                              'family': 'Roboto',
                          },
                          yaxis={
                              'title': "Вовлеченность",
                              'gridcolor': '#e5e5e5',
                              'tickmode': 'array',
                              'ticktext': list(range(1, 100))
                          }
                          )
        return fig
    else:

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=decom.trend.index,
                y=decom.trend / 4,
                name="",
                hoverinfo='skip',

            )
        )
        fig.add_trace(
            go.Indicator(
                mode='number',
                value=(100 - ((1 - decom.trend.min() / 4) * 100)),

                title={'text': "Вероятность увольнения",
                       'font': {'size': 12,
                                'family': 'sans-serif',
                                'color': '#000000',
                                },
                       },
                number={'prefix': " ",
                        'suffix': "%",
                        'font': {'size': 18,
                                 'family': 'sans-serif',
                                 },
                        },
                delta={'position': 'left',
                       'reference': 2,
                       'relative': True,
                       'font': {'size': 14,
                                'family': 'sans-serif',
                                },
                       },
                domain={'y': [0, 0.7], 'x': [0.25, 0.75]},
            ))
        fig.update_layout(
            xaxis={'showgrid': False,
                   'showticklabels': False},
            yaxis={'showgrid': False,
                   'showticklabels': False},
            plot_bgcolor='#eef5db',
            margin=dict(l=0, r=0, b=0, t=15),
            autosize=True,
        )
        return fig
