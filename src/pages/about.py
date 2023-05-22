from dash import html, dcc 

def about_page():
    return html.Div(
        html.P(
            "About Page: Write Something!",
            className="page-about--content"),
        className="page-about"
        )