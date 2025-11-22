"""
Component for displaying Data Mining Techniques/Topics
Used across all pages of the dashboard
"""

from dash import html

def create_techniques_info_card():
    """
    Creates an info card showing the 3 data mining techniques used
    Returns a Dash HTML component
    """
    return html.Div(className="techniques-info-container", children=[
        html.Div(className="techniques-header", children=[
            html.H3("📊 Data Mining Techniques Used", className="techniques-title"),
        ]),
        
        html.Div(className="techniques-grid", children=[
            # Classification - XGBoost
            html.Div(className="technique-card classification", children=[
                html.Div(className="technique-badge", children="1️⃣ CLASSIFICATION"),
                html.H4("XGBoost", className="technique-name"),
                html.P("Binary Classification Algorithm", className="technique-description"),
                html.Div(className="technique-details", children=[
                    html.P(["Location: ", html.Span("pages/churn_analysis.py", className="code")]),
                    html.P(["Purpose: ", "Predict whether customers will churn"]),
                    html.P(["Output: ", html.Span("Churn probability scores (0-1)", className="code")]),
                ]),
            ]),
            
            # Clustering - K-Means
            html.Div(className="technique-card clustering", children=[
                html.Div(className="technique-badge", children="2️⃣ CLUSTERING"),
                html.H4("K-Means", className="technique-name"),
                html.P("Unsupervised Learning Algorithm", className="technique-description"),
                html.Div(className="technique-details", children=[
                    html.P(["Location: ", html.Span("pages/segmentation.py", className="code")]),
                    html.P(["Purpose: ", "Group customers into segments by behavior"]),
                    html.P(["Output: ", html.Span("Customer segments & groups", className="code")]),
                ]),
            ]),
            
            # Outlier Detection - Isolation Forest
            html.Div(className="technique-card outlier-detection", children=[
                html.Div(className="technique-badge", children="3️⃣ OUTLIER DETECTION"),
                html.H4("Isolation Forest", className="technique-name"),
                html.P("Anomaly Detection Algorithm", className="technique-description"),
                html.Div(className="technique-details", children=[
                    html.P(["Location: ", html.Span("pages/data_overview.py", className="code")]),
                    html.P(["Purpose: ", "Identify anomalous customer records"]),
                    html.P(["Output: ", html.Span("Anomaly scores & outlier flags", className="code")]),
                ]),
            ]),
        ]),
    ])
