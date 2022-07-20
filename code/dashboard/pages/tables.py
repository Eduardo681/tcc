import pandas as pd
from dash import html, get_asset_url

from dashboard.pages_plugin import register_page

import dash_bootstrap_components as dbc

from dash import dash_table

register_page(
    __name__,
    path='/tables',
    title='Analytics App'
)

df_frequencia = pd.read_csv('../csvs/frequencias.csv')
df = pd.read_csv('../csvs/final.csv')
df.columns = ['id', 'tweet_id', 'Usuário', 'Publicação', 'Data', 'Compartilhamentos', 'Comentários', 'Likes',
              'Citações', 'Sentimento']
df_frequencia.columns = ["id", "Palavra", "Frequência", "Likes", "Compartilhamentos", "Comentários", "Citações"]
df.set_index('id', inplace=True, drop=False)
df.Data = pd.DatetimeIndex(df.Data).strftime("%Y-%m-%d")
remove_col = ['id', 'tweet_id']


def generate_table(df):
    return html.Div([
        dash_table.DataTable(
            style_data={
                'whiteSpace': 'normal',
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
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
                {'name': i, 'id': i, 'deletable': True} for i in df.columns if i not in remove_col
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


tabs = dbc.Col(
    dbc.Card(
        dbc.Tabs(
            [
                dbc.Tab(generate_table(df_frequencia), label="Frequência", activeTabClassName="fw-bold fst-italic",
                        label_style={"color": "#6930C3", "background": "transparent", "border": "none"}, ),
                dbc.Tab(generate_table(df), label="Dados brutos", activeTabClassName="fw-bold fst-italic",
                        label_style={"color": "#6930C3", "background": "transparent", "border": "none"}),
            ],
        )), style={"margin-left": "20px", "justify-content": "center"})

layout = html.Div(
    [
        dbc.Container(
            children=[
                html.Div(
                    children=[
                        tabs
                    ],

                    style={"display": "flex", "justify-content": "center", "height": "100vh", "align-items": "center"}
                ),
            ]
        )], style={"background": "#F5F5F5", "height": "100vh"})
