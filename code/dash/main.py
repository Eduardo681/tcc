from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


df: pd.DataFrame = pd.read_csv("../csvs/analise.csv")

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='IFood Marketing Dash'),

    html.Div(children='''

    '''),

    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(df),

    html.Div(children=[
        html.Label('Dropdown'),
        dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),

        html.Br(),
        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
                     ['Montréal', 'San Francisco'],
                     multi=True),

        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
    ], style={'padding': 10, 'flex': 1}),
])

if __name__ == '__main__':
    app.run_server(debug=True)
