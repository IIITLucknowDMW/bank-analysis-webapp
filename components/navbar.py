from dash import html

def Navbar(page_title, page_description):
    return html.Div(className="main", children=[
        html.H1(page_title, className="page-title"),
        html.P(page_description, className="page-description")
    ])