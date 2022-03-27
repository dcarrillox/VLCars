from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import glob




app = Dash(__name__)
server = app.server


# -----------------
# parse tsv database
tsv_database_file = glob.glob("2022-*.tsv")[0]
tsv_database_df = pd.read_csv(tsv_database_file, sep="\t", header=0)
# -----------------


fig = px.scatter(tsv_database_df, x="km", y="price", color="brand") # , barmode="group"

app.layout = html.Div(children=[
    html.H1(children='VLCars'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


if __name__ == "__main__":
    app.run_server(debug=True)