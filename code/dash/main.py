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


def generate_card(title, total, totalAbsoluto):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, className="card-title"),
                html.H6(total + " em " + totalAbsoluto + " postagens", className="card-subtitle"),
            ]
        ),
        class_name="box",
    )


def generate_img(source):
    return html.Img(
        src=app.get_asset_url(source + '.png'),
        width=400,
        height=400
    )


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

cardPositivos = dbc.Card(
    dbc.CardBody(
        [
            html.H4("50% Positivos", className="card-title"),
            html.H6("4000 de 8000 com avaliação positiva", className="card-subtitle"),
        ]
    ),
    style={"width": "350px", "color": "white", "background": "#1BBD8C", "height": "230px"},
)

cardNegativos = dbc.Card(
    dbc.CardBody(
        [
            html.H4("50% Positivos", className="card-title"),
            html.H6("4000 de 8000 com avaliação positiva", className="card-subtitle"),
        ]
    ),
    color="danger",
    style={"width": "350px", "color": "white", "background": "#EC3B50", "height": "230px"},
)

cardsSentimentos = html.Div(
    children=[cardPositivos, cardNegativos],
    style={"display": "flex", "justify-content": "space-between"}
)

classifier = dbc.Card([
    dcc.Input(
        id="input",
        type='text',
        placeholder="Digite frase a ser classificada",
        className="form-control"
    ),
    html.Div(id="output")],
    style={"margin-top": "30px", "height": "250px"}
)

cardsTotais = dbc.Row(
    children=[
        generate_card("Likes", "8000", "5000"), generate_card("Compartilhamentos", "8000", "5000"),
        generate_card("Comentários", "8000", "5000"), generate_card("Citações", "8000", "5000")
    ], style={"justify-content": "space-between", "background": "transparent"}
)

column = html.Div(
    children=[cardsSentimentos, classifier],
    style={"display": "flex", "flex-direction": "column"}
)

tabs = dbc.Col(
    dbc.Card(
        dbc.Tabs(
            [
                dbc.Tab(generate_img("Likes"), label="Likes", activeTabClassName="fw-bold fst-italic",
                        label_style={"color": "#6930C3", "background": "transparent", "border": "none"}, ),
                dbc.Tab(generate_img("Comentários"), label="Comentários", activeTabClassName="fw-bold fst-italic",
                        label_style={"color": "#6930C3", "background": "transparent", "border": "none"}),
                dbc.Tab(generate_img("Compartilhamentos"), label="Compartilhamentos",
                        activeTabClassName="fw-bold fst-italic",
                        label_style={"color": "#6930C3", "background": "transparent", "border": "none"}),
                dbc.Tab(generate_img("Citações"), label="Citações", activeTabClassName="fw-bold fst-italic",
                        label_style={"color": "#6930C3", "background": "transparent", "border": "none"})
            ],
        )), style={"margin-left": "10px"})


@app.callback(
    Output("output", "children"),
    Input("input", "value"),
)
def update_output(value):
    if value is not None and len(value) > 5:
        lista = [value]
        freq_text: CountVectorizer = vectorizer.transform(lista)
        sentiments = model.predict(freq_text)
        if sentiments[0] == 'pos':
            return_sentiment = 'Frase classificada como: positiva'
        else:
            return_sentiment = 'Frase classificada como: negativa'
    else:
        return_sentiment = 'Digite mais caracteres para obter a classificação do texto'
    return html.H3(return_sentiment)


app.layout = html.Div(dbc.Container(
    children=[
        html.H1("Dashboard"),
        html.Div(
            children=[
                column, tabs
            ], style={"display": "flex"}
        ),
        html.Hr(),
        cardsTotais,
        html.Hr(),
    ]
), style={"background": "#F5F5F5"})

if __name__ == '__main__':
    app.run_server(debug=True)
