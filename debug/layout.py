from dash import dcc, html 
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


def build_tabs():
    """ build the seven different tabs """
    return html.Div(
        id = "tabs-container",
        children=[
            dcc.Tabs(
                id="tabs",
                parent_className="custom-tabs",
                value="tab-select",
                children=[
                    dcc.Tab(
                        label="Weekly Summary",
                        value="tab-select",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="mes-analytics",
                        label="MES Analytics",
                        value="mes-analytics",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        # disabled=True,
                    ),
                    dcc.Tab(
                        id="iron-gate-compliance",
                        label="Iron-Gate Compliance",
                        value="iron-gate-compliance",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        # disabled=True, 
                    ),
                    dcc.Tab(
                        id="comparison",
                        label="Comparison",
                        value="comparison", 
                        className="custom-tab--selected",
                        # disable=True,
                    ),
                    dcc.Tab(
                        id="documentation",
                        label="Documentation",
                        value="documentation", 
                        className="custom-tab--selected",
                        # disable=True,
                    ),
                ]
            )
        ]
    )
    

def footer():
    return  dbc.Row(
                    id="footer", 
                    align = "end", 
                    justify="start", 
                    children = [
                        html.H6(["©2023, Developed By UCT Digital Transformation Team"])
                    ],
                    )