import pickle

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html, get_asset_url, callback
from dash.dependencies import Input, Output
from sklearn.feature_extraction.text import CountVectorizer

with open(get_asset_url('classifier.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(get_asset_url('vector.pkl'), 'rb') as f:
    vectorizer = pickle.load(f)


df = pd.read_csv('../csvs/final.csv')
df.columns = ['id', 'tweet_id', 'Usuário', 'Publicação', 'Data', 'Compartilhamentos', 'Comentários', 'Likes',
              'Citações', 'Sentimento']
df.set_index('id', inplace=True, drop=False)

totalLikes = df['Likes'].sum().item()
totalCompartilhamentos = df['Compartilhamentos'].sum().item()
totalComentarios = df['Comentários'].sum().item()
totalCitacoes = df['Citações'].sum().item()
totalPostagens = len(df)
df_positive: pd.DataFrame = df[df['Sentimento'] == 'pos']
df_negative: pd.DataFrame = df[df['Sentimento'] == 'neg']
countPositive = df_positive.shape[0]
countNegative = df_negative.shape[0]
percPositiva = countPositive / totalPostagens
percNegativa = countNegative / totalPostagens


def generate_card(title, total, totalAbsoluto, icone):
    return dbc.Card(
        dbc.CardBody(
            [
                html.A(
                    children=[html.I(className=icone)],
                    href="/",
                    className="icon"
                ),
                html.H4(title, className="card-title"),
                html.H5(f"{total} em {totalAbsoluto} postagens"
                        , className="card-subtitle"),
            ]
        ),
        class_name="box",
    )


def generate_img(source):
    return html.Div(html.Img(
        src=get_asset_url(source + '.png'),
        width=400,
        height=400
    ), className="img")


cardPositivos = dbc.Card(
    dbc.CardBody(
        [
            html.H1(f"{percPositiva * 100:.2f} % positivos", className="card-title"),
            html.H5(f"{countPositive} de {totalPostagens} com avaliação positiva.", className="card-subtitle"),
        ]
    ),
    style={"background": "#1BBD8C"}, class_name="card-perc",
)

cardNegativos = dbc.Card(
    dbc.CardBody(
        [
            html.H1(f"{percNegativa * 100:.2f} % negativos", className="card-title"),
            html.H5(f"{countNegative} de {totalPostagens} com avaliação negativa.", className="card-subtitle"),
        ]
    ),
    color="danger",
    style={"background": "#EC3B50"}, class_name="card-perc",
)

cardsSentimentos = html.Div(
    children=[cardPositivos, cardNegativos],
    style={"display": "flex", "justify-content": "space-between"}
)

classifier = dbc.Card([
    html.Div(
        [
            dcc.Input(
                id="input",
                type='text',
                placeholder="Digite frase a ser classificada",
                className="form__field"
            ),
            html.Label(children=[
                "Texto a ser classificado"
            ], className="form__label", htmlFor="input")],
        className="form__group"
    ),
    html.Div(id="output")],
    class_name="card-input"
)

cardsTotais = dbc.Row(
    children=[
        generate_card("Likes", totalLikes, totalPostagens, "fa-solid fa-heart"),
        generate_card("Compartilhamentos", totalCompartilhamentos, totalPostagens, "fa-solid fa-retweet"),
        generate_card("Comentários", totalComentarios, totalPostagens, "fa-solid fa-comments"),
        generate_card("Citações", totalCitacoes, totalPostagens, "fa-solid fa-reply")
    ], style={"justify-content": "space-between", "background": "transparent", "margin-top": "30px"}
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
        ), style={"height": "500px"}), style={"margin-left": "20px", "justify-content": "center"})


@callback(
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
    return html.Div(
        html.Span(
            return_sentiment
        ), style={"margin-top": "20px", "font-size": "22pt"})


layout = html.Div(
    [
        dbc.Container(
            children=[
                html.Div(
                    children=[
                        column, tabs
                    ], style={"display": "flex"}
                ),
                cardsTotais,
            ]
        )], style={"background": "#f5f5f5", "display": "flex", "height": "100vh", "justify-content": "center",
                   "align-items": "center"})
