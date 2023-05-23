from dash import html 
import dash_bootstrap_components as dbc 


def banner():
    """Build the banner at the top of the page 
    """
    banner_content = \
    dbc.Row(
        class_name="banner-row",
        align="center",
        children=[
            dbc.Col(
                    html.A(
                        href="/",
                        children=[
                            html.Img(
                                className="banner-row--img",
                                src="assets/img/OneUCT_Logo_NoBackground_SM.png",
                            ),
                        ],
                ),
                align="center",
                width="auto"
            ),
            dbc.Col(
                align="center",
                children=[
                    html.H2(
                        className="banner-row--title",
                        children=["MES Analytics"]),
                ],
            ),
        ]
    )
    return banner_content