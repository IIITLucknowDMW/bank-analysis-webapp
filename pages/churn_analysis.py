from dash import html
import pandas as pd
import numpy as np
from dash import html, dcc, Input, Output, callback, State
import plotly.express as px
from components.techniques_info import create_techniques_info_card

df = pd.read_csv(r"data/processed-data/bank-data-processed.csv")


# Create Age Groups
bins = [18, 25, 35, 45, 55, 65, 75, 90]  
labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]  
df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)


churned_customers = df[df["Exited"] == 1].shape[0]
active_customers = df[df["IsActiveMember"] == True].shape[0]
total_customers = df.shape[0]
churn_rate = (churned_customers / total_customers) * 100
retain_rate = 100 - churn_rate

churn_rate_str = f"{churn_rate:.2f}%"
active_customers_str = f"{active_customers:,}"
churned_customers_str = f"{churned_customers:,}"
total_customers_str = f"{total_customers:,}"
retain_rate_str = f"{retain_rate:.2f}%"

layout = html.Div(className="page-content", children=[
    html.Link(rel="stylesheet", href="/assets/churn_analysis.css"),
    html.Link(rel="stylesheet", href="/assets/techniques_info.css"),
    
    # Techniques Info Card
    create_techniques_info_card(),
    
    # Developer Credit Header
    html.Div(style={
        "textAlign": "center",
        "padding": "10px",
        "marginBottom": "10px",
        "color": "#1e3a5f",
        "fontSize": "11px",
        "fontWeight": "500",
        "borderBottom": "1px solid #e0e7ff"
    }, children=[
        html.P("Made by Neeraj, Gaurav and Hardik", style={"margin": "0"})
    ]),
    
    html.Div(className="grid-container churn-analysis", children=[
        
        # KPI Container
        html.Div(className="card-group churn-kpi-container", children=[
            html.H3("Customer Churn Key Metrics", className="group-title"),

                html.Div(className="card", children=[
                    html.Div(className="card-title", children=[
                        html.I(className="fa-solid fa-chart-line"),
                        html.Span("Churn Rate", className="card-header")
                    ]),
                    html.Div(churn_rate_str, className="kpi-value")
                ]),

                html.Div(className="card", children=[
                    html.Div(className="card-title", children=[
                        html.I(className="fa-solid fa-user-times"),
                        html.Span("No. of Churned Customers", className="card-header")
                    ]),
                    html.Div(churned_customers_str, className="kpi-value")
                ]),
                        
                html.Div(className="card", children=[
                    html.Div(className="card-title", children=[
                        html.I(className="fa-solid fa-user-check"),
                        html.Span("Active Customers", className="card-header")
                    ]),
                    html.Div(active_customers_str, className="kpi-value")
                ]),

                html.Div(className="card", children=[
                    html.Div(className="card-title", children=[
                        html.I(className="fa-solid fa-user-check"),
                        html.Span("Retain Rate", className="card-header")
                    ]),
                    html.Div(retain_rate_str, className="kpi-value")
                ]),

                html.Div(className="card", children=[
                    html.Div(className="card-title", children=[
                        html.I(className="fa-solid fa-user-times"),
                        html.Span("Total Customers", className="card-header")
                    ]),
                    html.Div(total_customers_str, className="kpi-value")
                ]),
        ]),

        # First Graph Container
        html.Div(className="card-group churn-graph-container1", children=[
            html.H3("Churn Rate by Demographics", className="group-title"),

                html.Div(className="card", children=[
                    html.P("by Geography"),
                    html.Div(   
                        dcc.Graph(id="churn-rate-by-geography", config={"displayModeBar": False,}, style={"width": "100%", "height": "100%"})
                    )]),

                html.Div(className="card", children=[
                    html.P("by Age Group"),
                    html.Div(
                        dcc.Graph(id="churn-rate-by-age", config={"displayModeBar": False}, style={"width": "100%", "height": "100%"})
                    )]),

                html.Div(className="card", children=[
                    html.P("by Gender"),
                    html.Div(
                        dcc.Graph(id="churn-rate-by-gender", config={"displayModeBar": False}, style={"width": "100%", "height": "100%"})
                    )]),
        ]),

        # Second Graph Container
        html.Div(className="card-group churn-graph-container2", children=[
            html.H3("Churn Rate by Product Usage", className="group-title"),

                html.Div(className="card", children=[
                    html.P("by Activity"),
                    html.Div(
                        dcc.Graph(id="churn-rate-by-activity", config={"displayModeBar": False}, style={"width": "100%", "height": "100%"})
                    )]),

                html.Div(className="card", children=[
                    html.P("by Product Number"),
                    html.Div(
                        dcc.Graph(id="churn-rate-by-product", config={"displayModeBar": False}, style={"width": "100%", "height": "100%"})
                    )]),
        #     ])
        ]),

        # Behavior Analysis
        html.Div(className="card-group behaviour-container", children=[
            html.H3("Behavior Analysis", className="group-title"),
                    html.Div(className="card", children=[
                    html.P("Important Factors for Customer Churn"),
                    html.Div(
                        dcc.Graph(id="feature-importances", config={"displayModeBar": False}, style={"width": "100%", "height": "100%"})
                    )]),
        ]),

        # Insights Part 1
        html.Div(className="card-group insight-container1", children=[
            html.H3("Insights", className="group-title"),
            html.Div(className="card insight", children=[
        
        # Insight 1: Age Matters
        html.Div([
            html.P("1. Age Matters", style={'color': '#3498db'}),
            html.P("- Younger customers (below 40) are more likely to leave, especially if they have a low balance or are inactive."),
            html.P("- Older customers (above 40) are more loyal, especially if they are active members or have a higher balance."),
        ], style={"marginBottom": "2px"}),
        
        # Insight 2: Active Members Stay Longer
        html.Div([
            html.P("2. Active Members Stay Longer", style={'color': '#3498db'}),
            html.P("- Customers who are active members are much less likely to leave the bank."),
        ], style={"marginBottom": "2px"}),
        
        # Insight 3: Balance and Credit Score
        html.Div([
            html.P("3. Balance and Credit Score", style={'color': '#3498db'}),
            html.P("- Customers with low balances (below 60,000) or lower credit scores (below 550) are more likely to leave, especially if they are younger."),
        ], style={'marginBottom': "2px"}),
        
        # Insight 4: Geography Plays a Role
        html.Div([
            html.P("4. Geography Plays a Role", style={'color': '#3498db'}),
            html.P("- Customers from Germany are more likely to leave compared to those from Spain."),
            html.P("- Customers from Spain are more loyal, especially if they are active members or have a higher balance."),
        ], style={'marginBottom': '2px'}),
    ]),
        ]),

        # Insights Part 2
        html.Div(className="card-group insight-container2", children=[
            html.Div(className="card insight", children=[
        # Insight 5: Multiple Products Increase Loyalty
        html.Div([
            html.P("5. Multiple Products Increase Loyalty", style={'color': '#3498db'}),
            html.P("- Customers with more than one product (e.g., checking account and credit card) are less likely to leave."),
            html.P("- Customers with three or more products are even more loyal."),
        ], style={'marginBottom': '2px'}),
        
        # Insight 6: Long-Term Customers Are Loyal
        html.Div([
            html.P("6. Long-Term Customers Are Loyal", style={'color': '#3498db'}),
            html.P("- Customers who have been with the bank for longer periods (e.g., more than 5 years) are less likely to leave."),
        ], style={'marginBottom': '2px'}),
        
        # Insight 7: Credit Card Ownership Helps
        html.Div([
            html.P("7. Credit Card Ownership Helps", style={'color': '#3498db'}),
            html.P("- Customers without a credit card are more likely to leave, especially if they are younger or have a low balance."),
            html.P("- Customers with a credit card are more likely to stay, especially if they are active members."),
        ], style={'marginBottom': '2px'}),

    ]),
        ]),
    ]),
]),

# Callback for Churn Rate by Geography
@callback(
    Output("churn-rate-by-geography", "figure"),
    Input("churn-rate-by-geography", 'id')
)
def update_geography(_):
    geo_churn = df.groupby("Geography", as_index=False, observed=True)["Exited"].mean()
    fig = px.bar(geo_churn, 
                 x="Geography", 
                 y="Exited", 
                 title=None,
                 labels={"Geography": "Country", "Exited": "Churn Rate"})
    fig.update_layout(yaxis_tickformat=".0%",
                      margin=dict(t=10, b=10, l=10, r=10),
                      xaxis_title=None,
                      yaxis_title=None,
                      title=None,
                      dragmode=False,
                      yaxis=dict(
                          showgrid=True,
                          zeroline=False,
                          showline=False,
                          showticklabels=True,
                          showticksuffix="none",
                        ),
                      template="plotly_white",
                      hoverlabel=dict(
                          bgcolor="white",  
                          font_size=12,     
                          font_color="black",
                          font_family="Poppins",  
                          bordercolor="white"  
                        ),
                      )
    return fig

# Callback for Churn Rate by Age Group
@callback(
    Output("churn-rate-by-age", "figure"),
    Input("churn-rate-by-age", 'id')
)
def update_age_group(_):
    age_churn = df.groupby("AgeGroup", as_index=False, observed=True)["Exited"].mean()
    fig = px.bar(age_churn, x="AgeGroup", y="Exited", title="Churn Rate by Age Group")
    fig.update_layout(yaxis_tickformat=".0%",
                      margin=dict(t=10, b=10, l=10, r=10),
                      xaxis_title=None,
                      yaxis_title=None,
                      dragmode=False,
                      title=None,
                      yaxis=dict(
                          showgrid=True,
                          zeroline=False,
                          showline=False,
                          showticklabels=True,
                          showticksuffix="none",
                        ),
                      template="plotly_white",
                      hoverlabel=dict(
                          bgcolor="white",  
                          font_size=12,     
                          font_color="black",
                          font_family="Poppins",  
                          bordercolor="white"  
                        ),
                      )
    return fig

# Callback for Churn Rate by Gender
@callback(
    Output("churn-rate-by-gender", "figure"),
    Input("churn-rate-by-gender", 'id')
)
def update_gender(_):
    gender_churn = df.groupby("Gender", as_index=False, observed=True)["Exited"].mean()
    fig = px.bar(gender_churn, x="Gender", y="Exited", title="Churn Rate by Gender",
                 labels={"Gender": "Customer Gender", "Exited": "Churn Rate"})
    fig.update_layout(yaxis_tickformat=".0%",
                      margin=dict(t=10, b=10, l=10, r=10),
                      xaxis_title=None,
                      yaxis_title=None,
                      title=None,
                      dragmode=False,
                      yaxis=dict(
                          showgrid=True,
                          zeroline=False,
                          showline=False,
                          showticklabels=True,
                          showticksuffix="none",
                        ),
                      template="plotly_white",
                      hoverlabel=dict(
                          bgcolor="white",  
                          font_size=12,     
                          font_color="black",
                          font_family="Poppins",  
                          bordercolor="white"  
                        ),
                      )
    return fig

# Callback for Churn Rate by Activity Status
@callback(
    Output("churn-rate-by-activity", "figure"),
    Input("churn-rate-by-activity", 'id')
)
def update_activity(_):
    activity_churn = df.groupby("IsActiveMember", as_index=False, observed=True)["Exited"].mean()
    # Map 0/1 to Inactive/Active for display
    activity_churn["Status"] = activity_churn["IsActiveMember"].map({0.0: "Inactive", 1.0: "Active"})
    fig = px.bar(activity_churn, x="Status", y="Exited", title="Churn Rate by Gender",
                 labels={"Status": "Member Activity Status", "Exited": "Churn Rate"})
    fig.update_layout(yaxis_tickformat=".0%",
                      margin=dict(t=10, b=10, l=10, r=10),
                      xaxis_title=None,
                      yaxis_title=None,
                      title=None,
                      dragmode=False,
                      xaxis=dict(
                          tickfont=dict(
                          size=10,
                          color='rgb(82, 82, 82)',
                          ),
                          tickmode='array',
                          ),
                      yaxis=dict(
                          showgrid=True,
                          zeroline=False,
                          showline=False,
                          showticklabels=True,
                          showticksuffix="none",
                        ),
                      template="plotly_white",
                      hoverlabel=dict(
                          bgcolor="white",  
                          font_size=12,     
                          font_color="black",
                          font_family="Poppins",  
                          bordercolor="white"  
                        ),
                      )
    return fig

# Callback for Churn Rate by Product
@callback(
    Output("churn-rate-by-product", "figure"),
    Input("churn-rate-by-product", 'id')
)
def update_prodcuct(_):
    product_churn = df.groupby("NumOfProducts", as_index=False, observed=True)["Exited"].mean()
    fig = px.bar(product_churn, x="NumOfProducts", y="Exited", title="Churn Rate by Gender",
                 labels={"NumOfProducts": "Number of Products Held", "Exited": "Churn Rate"})
    fig.update_layout(yaxis_tickformat=".0%",
                      margin=dict(t=10, b=10, l=10, r=10),
                      xaxis_title=None,
                      yaxis_title=None,
                      title=None,
                      dragmode=False,
                      xaxis=dict(
                          tickfont=dict(
                          size=10,
                          color='rgb(82, 82, 82)',
                          ),
                          tickmode='array',
                          ),
                      yaxis=dict(
                          tickfont=dict(
                              size=10,
                          ),
                          showgrid=True,
                          zeroline=False,
                          showline=False,
                          showticklabels=True,
                          showticksuffix="none",
                        ),
                      template="plotly_white",
                      hoverlabel=dict(
                          bgcolor="white",  
                          font_size=12,     
                          font_color="black",
                          font_family="Poppins",  
                          bordercolor="white"  
                        ),
                      )
    return fig

# Callback for Feature Importances
@callback(
    Output("feature-importances", "figure"),
    Input("feature-importances", 'id')
)
def update_prodcuct(_):
    feature_importance = pd.read_csv(r"data/processed-data/feature_importance.csv")
    fig = px.bar(feature_importance, 
             x="Importance", 
             y="Feature", 
             orientation="h",
             title="Feature Importance",
             color="Importance")
    fig.update_layout(yaxis_tickformat=".0%",
                      margin=dict(t=10, b=10, l=150, r=50),
                      xaxis_title=None,
                      yaxis_title=None,
                      title=None,
                      dragmode=False,
                      height=450,
                      xaxis=dict(
                          tickfont=dict(
                          size=11,
                          color='rgb(82, 82, 82)',
                          ),
                          tickmode='array',
                          ),
                          autosize=True,
                      yaxis=dict(
                          autorange="reversed",
                          tickfont=dict(
                              size=12,
                              color='rgb(30, 58, 95)',
                              family="Arial"
                          ),
                          showgrid=True,
                          zeroline=False,
                          showline=False,
                          showticklabels=True,
                          showticksuffix="none",
                        ),
                      template="plotly_white",
                      hoverlabel=dict(
                          bgcolor="white",  
                          font_size=12,     
                          font_color="black",
                          font_family="Poppins",  
                          bordercolor="white"  
                        ),
                      )
    return fig

