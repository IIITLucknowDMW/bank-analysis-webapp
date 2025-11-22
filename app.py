import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pages.churn_analysis
import pages.data_overview
import pages.segmentation

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"
    ],
    suppress_callback_exceptions=True
)

app.title = "X-Bank Dashboard"

# Add FontAwesome CSS to head
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


# Application layout

app.layout = html.Div(className="dashboard-grid", children=[
    html.Nav(id="navbar-container", className="navbar", children=[
        html.Div(className="navbar-content", children=[
            html.H1(id="navbar-title", className="navbar-title"),
            html.P(id="navbar-subtitle", className="navbar-subtitle")
        ])
    ]),
    html.Aside(className="sidebar", children=[
        html.Div(className="top", children=[
            html.Div(className="sidebar-title", children=[
                html.I(className="fa-solid fa-money-check-dollar"),
                html.Span("X-Bank")
            ]),
            html.Ul(className="sidebar-list", children=[
                html.Li([
                    html.A(
                        id="churn-analysis-link",
                        className="sidebar-link",
                        href="/",
                        children=[
                            html.I(className="fa-solid fa-magnifying-glass-chart"),
                            html.Span("Churn Analysis", className="nav-item")
                        ]
                    ),
                ]),
                html.Li([
                    html.A(
                        id="segmentation-link",
                        className="sidebar-link",
                        href="/segmentation",
                        children=[
                            html.I(className="fa-solid fa-circle-nodes"),
                            html.Span("Customer Segmentation", className="nav-item")
                        ]
                    ),
                ]),
                html.Li([
                    html.A(
                        id="data-overview-link",
                        className="sidebar-link",
                        href="/data_overview",
                        children=[
                            html.I(className="fa-solid fa-database"),
                            html.Span("Data Overview", className="nav-item")
                        ]
                    ),
                ]),
            ])
        ])
    ]),
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content", className="main")
])

# defining font-awesome and fonts -------------------------------------------------
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>

<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");
@import url('https://fonts.googleapis.com/css2?family=Zen+Dots&display=swap');
</style>
"""

server = app.server

# Callback to update Navbar dynamically
@app.callback(
    [Output("navbar-title", "children"),
     Output("navbar-subtitle", "children")],
    [Input("url", "pathname")]
)
def update_navbar(pathname):
    if pathname == "/":
        return "Churn Analysis", "Analyze customer churn trends and KPIs"
    elif pathname == "/churn_analysis":
        return "Churn Analysis", "Explore customer churn trends"
    elif pathname == "/segmentation":
        return "Customer Segmentation", "Identify customer groups and behaviors"
    elif pathname == "/data_overview":
        return "Data Overview", "Explore the dataset and detect anomalies"
    else:
        return "Page Not Found", ""

# Callback to update the active link
@app.callback(
    [
    Output("churn-analysis-link", "className"),
    Output("segmentation-link", "className"),
    Output("data-overview-link", "className"),
    ],
    [
    Input("url", "pathname")
    ]
)
def update_active_tab(pathname):
    # Default class
    default_class = "sidebar-link"
    active_class = "sidebar-link active"

    # Check the current path and assign the active class
    return (
        active_class if pathname == "/" else default_class,
        active_class if pathname == "/segmentation" else default_class,
        active_class if pathname == "/data_overview" else default_class,
    )


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return pages.churn_analysis.layout
    elif pathname == "/segmentation":
        return pages.segmentation.layout
    elif pathname == "/data_overview":
        return pages.data_overview.layout
    else:
        return pages.churn_analysis.layout

if __name__ == "__main__":
    app.run(debug=True)