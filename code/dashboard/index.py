from dash import html, dcc
from dash.dependencies import Input, Output

from app import app

from components import navbar
from pages import home, tables

nav = navbar.navbar()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content', children=[]),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    if pathname == '/tables':
        return tables.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
