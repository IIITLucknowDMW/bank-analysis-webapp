from dash import html

layout = html.Div([
    html.H1("Risk Analysis"),
    html.P("🚧 Work in Progress 🚧"),
]),


html.Div(className="page-content", children=[
    html.Link(rel="stylesheet", href="/assets/risk_analysis.css"),
    html.Div(className="grid-container risk", children=[
        
        # Customer at Risk
        html.Div(className="card customer-at-risk", children=[html.P("KPI 1")]),

        # Balance at Risk
        html.Div(className="card balance-at-risk", children=[html.P("KPI 1")]),

        # Churn Probability per Segment
        html.Div(className="card customer-percentage", children=[html.P("KPI 1")]),

        # Churn Probability per Segment
        html.Div(className="card churn-probability", children=[html.P("KPI 1")]),

        # Key Risk Factors
        html.Div(className="card risk-factors", children=[html.P("KPI 1")]),

        # Segment Profile Radar Chart Container
        html.Div(className="card segment-radar", children=[html.P("KPI 1")]),

        # Segment Profiles
        html.Div(className="card segment-profile", children=[html.P("KPI 1")]),

    ])
])