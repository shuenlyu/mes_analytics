from dash import html 
import dash_bootstrap_components as dbc 


def banner():
    """Build the banner at the top of the page 
    """
    return html.Div(
        id="banner",
        children=[
            dbc.Row(
                align="start",
                children=[
                    dbc.Col(
                            html.A(
                                href="/",
                                children=[
                                    html.Img(
                                        src="assets/img/OneUCT_Logo_NoBackground_SM.png",
                                        # style={"height": "50%", "width":"50%"}
                                        style={'height': '30px','width': 'auto','margin-bottom': '0px'}
                                    ),
                                ],
                        ),
                        align="center",
                        width="auto"
                    ),
                    dbc.Col(
                        align="center",
                        children=[
                            html.H1(id="banner-title", children=["MES Analytics"]),
                            # html.H5(id="banner-subtitle", children=["Select Tab"])
                        ],
                    ),
                ]
            )
        ]
    )