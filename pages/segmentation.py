from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.techniques_info import create_techniques_info_card

df = pd.read_csv("data/processed-data/past-data.csv")

# Calculate segment statistics
segment_counts = df['GMM_Cluster'].value_counts().reset_index()
segment_counts.columns = ['Cluster', 'Count']

layout = html.Div(className="page-content", children=[
    html.Link(rel="stylesheet", href="/assets/segmentation.css"),
    html.Link(rel="stylesheet", href="/assets/techniques_info.css"),
    
    # Techniques Info Card
    create_techniques_info_card(),
    
    html.Div(className="grid-container segmentation", children=[
        
        # Churn Rate by Segment
        html.Div(className="card churn-rate", children=[
            html.P("Churn Rate by Segment (K-Means Clustering)"),
            dcc.Graph(id="churn-rate-segment", config={"displayModeBar": False})
        ]),

        # Segment Distribution
        html.Div(className="card segment-distribution", children=[
            html.P("Customer Distribution by Segment"),
            dcc.Graph(id="segment-distribution-graph", config={"displayModeBar": False})
        ]),

        # Segment Summary
        html.Div(className="card-group segment-descriptions", children=[
            html.H3("Segment Characteristics", className="group-title"),
            dcc.Graph(id="segment-summary-graph", config={"displayModeBar": False})
        ]),

    ])
])


# Callback for Churn Rate by Segment
@callback(
    Output("churn-rate-segment", "figure"),
    Input("churn-rate-segment", 'id')
)
def update_churn_rate(_):
    gmm_churn_rate = df.groupby('GMM_Cluster')['Churn_Probability'].mean().reset_index()
    gmm_churn_rate.columns = ['Cluster', 'Churn_Rate']
    gmm_churn_rate = gmm_churn_rate.sort_values('Churn_Rate', ascending=False)
    
    fig = px.bar(gmm_churn_rate, x='Cluster', y='Churn_Rate', 
                 title="Average Churn Rate by K-Means Segment",
                 color='Churn_Rate',
                 color_continuous_scale='RdYlGn_r')
    fig.update_layout(
        margin=dict(t=30, b=10, l=40, r=10),
        xaxis_title="Segment",
        yaxis_title="Churn Rate",
        template="plotly_white",
        hovermode='x unified',
        plot_bgcolor='#f8f9fb',
        paper_bgcolor='white'
    )
    return fig


# Callback for Segment Distribution Pie Chart
@callback(
    Output("segment-distribution-graph", "figure"),
    Input("segment-distribution-graph", 'id')
)
def update_segment_distribution(_):
    fig = px.pie(segment_counts, values='Count', names='Cluster',
                 title="Customer Distribution by K-Means Segment",
                 color_discrete_sequence=['#1e3a5f', '#4f9fd8', '#27ae60', '#f39c12', '#e74c3c', '#9b59b6'])
    fig.update_layout(
        margin=dict(t=30, b=10, l=10, r=10),
        template="plotly_white",
        font=dict(color='#1e3a5f'),
        paper_bgcolor='white'
    )
    return fig


# Callback for Segment Summary
@callback(
    Output("segment-summary-graph", "figure"),
    Input("segment-summary-graph", 'id')
)
def update_segment_summary(_):
    summary_data = df.groupby('GMM_Cluster').agg({
        'Age': 'mean',
        'Churn_Probability': 'mean',
        'Tenure': 'mean'
    }).reset_index()
    summary_data.columns = ['Cluster', 'Avg_Age', 'Churn_Prob', 'Avg_Tenure']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=summary_data['Cluster'], y=summary_data['Avg_Age'],
                         name='Avg Age', marker_color='#4f9fd8'))
    fig.add_trace(go.Bar(x=summary_data['Cluster'], y=summary_data['Churn_Prob'],
                         name='Churn Probability', marker_color='#e74c3c'))
    fig.add_trace(go.Bar(x=summary_data['Cluster'], y=summary_data['Avg_Tenure'],
                         name='Avg Tenure', marker_color='#27ae60'))
    
    fig.update_layout(
        title="K-Means Segment Characteristics",
        margin=dict(t=30, b=10, l=40, r=10),
        xaxis_title="Segment",
        yaxis_title="Value",
        template="plotly_white",
        hovermode='x unified',
        plot_bgcolor='#f8f9fb',
        paper_bgcolor='white',
        barmode='group'
    )
    return fig