from dash import html, get_asset_url


def navbar():
    layout = html.Div(
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
        ])

    return layout
