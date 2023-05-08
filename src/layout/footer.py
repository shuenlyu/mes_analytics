from dash import html 
import dash_bootstrap_components as dbc 


def footer():
    return  dbc.Row(
                    id="footer",
                    align="center", 
                    # justify="center", 
                    children = [
                         html.H6(["©2023, Developed By UCT Digital Transformation Team"])
                    ]
                    )