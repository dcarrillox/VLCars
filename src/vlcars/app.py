from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd



def run_server(df):

    app = Dash(__name__)

    fig = px.scatter(df, x="km", y="price", color="brand") # , barmode="group"

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])

    app.run_server(debug=False)


def run_server_heroku(df):

    app = Dash(__name__)
    server = app.server

    fig = px.scatter(df, x="km", y="price", color="brand") # , barmode="group"

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])

    app.run_server(debug=True)