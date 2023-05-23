from dash import html, dcc 

def error_page():
    return html.Div(
        [
            html.P(
                "404 Error - Page Not Found",
                className="page-error--content"
            ),
            html.A(
                html.P(
                    "Home Page",
                    className="page-error--href"
                ), 
                href="/"
            )
        ],
        className="page-error"
        )