from dash import html 
import dash_bootstrap_components as dbc 


def footer():
     footer_content =\
     dbc.Row(
          id="footer",
          class_name="footer-row",
          children = [
               html.H6(
                    ["©2023, Developed By UCT Digital Transformation Team"],
                    className="footer-row--content")
          ],
          align='end',
     )
     return footer_content
              