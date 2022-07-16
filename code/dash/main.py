import os

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output

df = pd.read_csv('../csvs/final.csv')
df.columns = ['id', 'tweet_id', 'Usuário', 'Publicação', 'Data', 'Compartilhamentos', 'Comentários', 'Likes',
                  'Citações', 'Sentimento']
df.set_index('id', inplace=True, drop=False)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

table = html.Div([
    dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        css=[{
            'selector': '.dash-spreadsheet td div',
            'rule': '''
                line-height: 15px;
                max-height: 30px; min-height: 30px; height: 30px;
                display: block;
                overflow-y: hidden;
            '''
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
])

dropdown = html.Div([
    dcc.Dropdown(['Likes', 'Compartilhamentos', 'Comentários', 'Citações'], 'Likes', id='dropdown'),
    html.Div(id='dd-output-container')
])


@app.callback(
    Output('dd-output-container', 'children'),
    Input('dropdown', 'value')
)
def update_output(value):
    return html.Img(
        src=app.get_asset_url(value+'.png')
    )


app.layout = dbc.Container(
    children=[
        html.H1("Ifood Dashboard"),
        dropdown,
        table,
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
