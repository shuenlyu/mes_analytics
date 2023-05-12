from dash import html, dcc 

def about_page():
    return html.Div(
        children=[
           dcc.Markdown("""
                        ##### about page placeholder
                        """) 
        ])