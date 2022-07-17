import pickle

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
from sklearn.feature_extraction.text import CountVectorizer

with open('../classifier.pkl', 'rb') as f:
    model = pickle.load(f)

with open('../vector.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

df = pd.read_csv('../csvs/final.csv')
df.columns = ['id', 'tweet_id', 'Usuário', 'Publicação', 'Data', 'Compartilhamentos', 'Comentários', 'Likes',
              'Citações', 'Sentimento']
df.set_index('id', inplace=True, drop=False)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

table = html.Div([
    dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
            'color': 'white',
            'backgroundColor': 'rgb(14, 16, 18)'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                "background-color": "rgb(22, 26, 29)", "border-color": "rgb(63, 63, 63)", "border-style": "solid",
                "border-width": "1px"
            }
        ],
        style_header={
            'backgroundColor': '#161A1D',
            'fontWeight': 'bold'
        },
        css=[{
            'selector': '.dash-spreadsheet td div',
            'rule': '''
                line-height: 15px;
                max-height: 30px; min-height: 30px; height: 30px;
                display: block;
                overflow-y: hidden;
            ''',
        }, {
            'selector': '.dash-table-tooltip',
            'rule': 'font-family: monospace; color: black; border: thin solid rgb(63, 63, 63)'
        }],
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
        tooltip_duration=None,
        style_cell={'textAlign': 'left'},
        id='datatable-row-ids',
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in df.columns
        ],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        selected_rows=[],
        page_action='native',
        page_current=0,
        page_size=10,
    ),
    html.Div(id='datatable-row-ids-container')
], style={"margin-top": "10px"})

dropdown = html.Div([
    dcc.Dropdown(['Likes', 'Compartilhamentos', 'Comentários', 'Citações'], 'Likes', id='dropdown',
                 style={"background": "white", "color": "black", "border-radius": ".25rem"}, ),
    html.Div(id='dd-output-container', style={"margin-top": "10px"})
])

cardPositivos = dbc.Card(
    dbc.CardBody(
        [
            html.H4("50% Positivos", className="card-title"),
            html.H6("4000 de 8000 com avaliação positiva", className="card-subtitle"),
        ]
    ),
    color="success",
    style={"width": "18rem", "color": "white"},
)

cardNegativos = dbc.Card(
    dbc.CardBody(
        [
            html.H4("50% Positivos", className="card-title"),
            html.H6("4000 de 8000 com avaliação positiva", className="card-subtitle"),
        ]
    ),
    color="danger",
    style={"width": "18rem", "color": "white"},
)

cardsSentimentos = html.Div(
    children=[cardPositivos, cardNegativos],
    style={"display": "flex", "justify-content": "space-between"}
)

classifier = html.Div([
    dcc.Input(
        id="input",
        type='text',
        placeholder="Digite frase a ser classificada",
        className="form-control"
    ),
    html.Div(id="output")],
    style={"margin-top": "50px"}
)

column = html.Div(
    children=[cardsSentimentos, classifier],
    style={"display": "flex", "flex-direction": "column", "width": "60%"}
)


@app.callback(
    Output('dd-output-container', 'children'),
    Input('dropdown', 'value')
)
def update_output(value):
    return html.Img(
        src=app.get_asset_url(value + '.png'),
        width=400,
        height=400
    )


@app.callback(
    Output("output", "children"),
    Input("input", "value"),
)
def update_output(value):
    returnSentiment = None
    if value is not None and len(value) > 5:
        lista = [value]
        freq_text: CountVectorizer = vectorizer.transform(lista)
        sentiments = model.predict(freq_text)
        if sentiments[0] == 'pos':
            returnSentiment = 'Frase classificada como: positiva'
        else:
            returnSentiment = 'Frase classificada como: negativa'
    else:
        returnSentiment = 'Digite mais caracteres para obter a classificação do texto'
    return html.H3(returnSentiment)


app.layout = html.Div(dbc.Container(
    children=[
        html.H1("Dashboard"),
        html.Div(
            children=[
                column, dropdown
            ], style={"display": "flex", "justify-content": "space-between"}
        ),
        html.Hr(),
        table,
    ]
), style={"background": "#0e1012", "color": "#fff"})

if __name__ == '__main__':
    app.run_server(debug=True)
