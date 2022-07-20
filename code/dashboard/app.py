import dash_bootstrap_components as dbc
from dash import Dash, html, get_asset_url

import pages_plugin

app = Dash(__name__, plugins=[pages_plugin], external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

app.layout = html.Div(
    children=[
        html.Div(
            className="aside",
            children=[
                html.A(
                    href="/",
                    className="nav-page",
                    children=[
                        html.Img(
                            className="icon",
                            src=get_asset_url("logo.png"),
                            width=100,
                            height=100,
                            style={"border-radius": "100%"}
                        )
                    ], style={"position": "absolute", "top": "100px"}
                ),
                html.A(
                    href="/",
                    className="nav-page",
                    children=[
                        html.Img(
                            className="icon",
                            src=get_asset_url("bi.svg"),
                            width=60,
                            height=60
                        )
                    ]
                ),
                html.A(
                    href="/tables",
                    className="nav-page",
                    children=[
                        html.Img(
                            className="icon",
                            src=get_asset_url("table.svg"),
                            width=60,
                            height=60
                        )
                    ],
                    style={"margin-top": "20px"}
                ),
            ]
        ), pages_plugin.page_container
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
