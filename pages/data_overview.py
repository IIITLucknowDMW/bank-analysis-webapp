import pandas as pd
import numpy as np
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
import os
import traceback
from components.techniques_info import create_techniques_info_card

# Perform Outlier Detection using Isolation Forest
def detect_outliers(dataframe, contamination=0.05):
    """
    Detect outliers using Isolation Forest algorithm
    contamination: expected proportion of outliers (0.05 = 5%)
    """
    try:
        # Select numerical features
        numerical_cols = dataframe.select_dtypes(include=[np.number]).columns
        numerical_data = dataframe[numerical_cols].copy()
        
        # Fit Isolation Forest with n_jobs=-1 for parallel processing
        iso_forest = IsolationForest(contamination=contamination, random_state=42, n_jobs=-1)
        outlier_predictions = iso_forest.fit_predict(numerical_data)
        
        # -1 = outlier, 1 = normal
        dataframe['IsOutlier'] = outlier_predictions
        
        # Compute anomaly scores (use offset_tree for faster computation)
        dataframe['OutlierScore'] = iso_forest.offset_ - iso_forest.score_samples(numerical_data)
        
        return dataframe
    except Exception as e:
        print(f"Error in detect_outliers: {str(e)}")
        traceback.print_exc()
        # Return without scores if there's an error
        dataframe['IsOutlier'] = 1  # Mark all as normal if error
        dataframe['OutlierScore'] = 0.0
        return dataframe

# Load data and perform outlier detection
try:
    DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/processed-data/bank-data-processed.csv')
    df = pd.read_csv(DATA_PATH)
    df_with_outliers = detect_outliers(df.copy(), contamination=0.05)
    
    # Calculate statistics
    total_records = len(df_with_outliers)
    outlier_count = (df_with_outliers['IsOutlier'] == -1).sum()
    outlier_percentage = (outlier_count / total_records) * 100
    
    # Get top outliers
    top_outliers = df_with_outliers.nsmallest(10, 'OutlierScore')[['Age', 'Balance', 'CreditScore', 'Tenure', 'OutlierScore']]
    
    # Prepare data for anomaly score distribution
    outlier_scores = df_with_outliers['OutlierScore'].values
    
    data_loaded = True
except Exception as e:
    print(f"Error loading data: {str(e)}")
    traceback.print_exc()
    # Fallback values
    total_records = 0
    outlier_count = 0
    outlier_percentage = 0
    top_outliers = pd.DataFrame()
    outlier_scores = np.array([])
    data_loaded = False

layout = html.Div([
    html.Link(rel="stylesheet", href="/assets/data_overview.css"),
    html.Link(rel="stylesheet", href="/assets/techniques_info.css"),
    
    # Techniques Info Card
    create_techniques_info_card(),
    
    html.Div([
        html.H1("📊 Data Overview & Outlier Detection", style={'textAlign': 'center', 'color': '#1e3a5f', 'marginBottom': '30px'}),
    ], style={'padding': '20px'}),
    
    # KPI Cards
    html.Div([
        html.Div([
            html.H3("Total Records", style={'color': '#4f9fd8', 'fontSize': '14px'}),
            html.H2(f"{total_records:,}", style={'color': '#1e3a5f', 'fontSize': '32px', 'margin': '10px 0'})
        ], style={'backgroundColor': '#f0f7ff', 'padding': '20px', 'borderRadius': '8px', 'border': 'left 4px solid #4f9fd8'}),
        
        html.Div([
            html.H3("Outliers Detected", style={'color': '#e74c3c', 'fontSize': '14px'}),
            html.H2(f"{outlier_count}", style={'color': '#c0392b', 'fontSize': '32px', 'margin': '10px 0'})
        ], style={'backgroundColor': '#fff5f5', 'padding': '20px', 'borderRadius': '8px', 'border': 'left 4px solid #e74c3c'}),
        
        html.Div([
            html.H3("Outlier Percentage", style={'color': '#f39c12', 'fontSize': '14px'}),
            html.H2(f"{outlier_percentage:.2f}%", style={'color': '#d68910', 'fontSize': '32px', 'margin': '10px 0'})
        ], style={'backgroundColor': '#fffaf0', 'padding': '20px', 'borderRadius': '8px', 'border': 'left 4px solid #f39c12'}),
        
        html.Div([
            html.H3("Normal Records", style={'color': '#27ae60', 'fontSize': '14px'}),
            html.H2(f"{total_records - outlier_count:,}", style={'color': '#1e8449', 'fontSize': '32px', 'margin': '10px 0'})
        ], style={'backgroundColor': '#f0fdf4', 'padding': '20px', 'borderRadius': '8px', 'border': 'left 4px solid #27ae60'})
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))', 'gap': '16px', 'margin': '20px', 'marginBottom': '40px'}),
    
] + ([] if not data_loaded else [
    # Charts and tables only show if data loaded
    html.Div([
        # Anomaly Score Distribution
        html.Div([
            dcc.Graph(
                id='anomaly-distribution',
                figure={
                    'data': [
                        go.Histogram(
                            x=outlier_scores if len(outlier_scores) > 0 else [0],
                            nbinsx=50,
                            name='Anomaly Scores',
                            marker=dict(color='#4f9fd8'),
                            opacity=0.7
                        )
                    ],
                    'layout': go.Layout(
                        title='Distribution of Anomaly Scores',
                        xaxis_title='Anomaly Score (Lower = More Anomalous)',
                        yaxis_title='Frequency',
                        hovermode='x unified',
                        plot_bgcolor='#f8f9fb',
                        paper_bgcolor='white',
                        font=dict(color='#1e3a5f')
                    )
                }
            )
        ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '20px'})
    ]),
    
    # Outlier vs Normal Distribution
    html.Div([
        dcc.Graph(
            id='outlier-pie',
            figure={
                'data': [
                    go.Pie(
                        labels=['Normal', 'Outliers'],
                        values=[max(0, total_records - outlier_count), outlier_count],
                        marker=dict(colors=['#27ae60', '#e74c3c']),
                        textposition='inside',
                        textinfo='label+percent'
                    )
                ],
                'layout': go.Layout(
                    title='Data Distribution: Normal vs Outliers',
                    plot_bgcolor='#f8f9fb',
                    paper_bgcolor='white',
                    font=dict(color='#1e3a5f'),
                    height=400
                )
            }
        )
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '20px'}),
    
    # Top Outliers Table
    html.Div([
        html.H2('🔍 Top 10 Detected Outliers', style={'color': '#1e3a5f', 'marginBottom': '15px'}),
        html.Table([
            html.Thead(
                html.Tr([
                    html.Th('Age', style={'padding': '10px', 'backgroundColor': '#1e3a5f', 'color': 'white', 'textAlign': 'left'}),
                    html.Th('Balance', style={'padding': '10px', 'backgroundColor': '#1e3a5f', 'color': 'white', 'textAlign': 'left'}),
                    html.Th('Credit Score', style={'padding': '10px', 'backgroundColor': '#1e3a5f', 'color': 'white', 'textAlign': 'left'}),
                    html.Th('Tenure', style={'padding': '10px', 'backgroundColor': '#1e3a5f', 'color': 'white', 'textAlign': 'left'}),
                    html.Th('Anomaly Score', style={'padding': '10px', 'backgroundColor': '#1e3a5f', 'color': 'white', 'textAlign': 'left'})
                ])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(f"{row['Age']:.0f}", style={'padding': '10px', 'borderBottom': '1px solid #e5e7eb'}),
                    html.Td(f"${row['Balance']:,.0f}", style={'padding': '10px', 'borderBottom': '1px solid #e5e7eb'}),
                    html.Td(f"{row['CreditScore']:.0f}", style={'padding': '10px', 'borderBottom': '1px solid #e5e7eb'}),
                    html.Td(f"{row['Tenure']:.0f} yrs", style={'padding': '10px', 'borderBottom': '1px solid #e5e7eb'}),
                    html.Td(f"{row['OutlierScore']:.4f}", style={'padding': '10px', 'borderBottom': '1px solid #e5e7eb', 'color': '#e74c3c', 'fontWeight': 'bold'})
                ]) for _, row in top_outliers.iterrows()
            ])
        ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '15px'})
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '20px'}),
    
    # Algorithm Explanation
    html.Div([
        html.H2('📋 About Outlier Detection', style={'color': '#1e3a5f', 'marginBottom': '15px'}),
        html.Div([
            html.H3('Algorithm Used: Isolation Forest', style={'color': '#4f9fd8'}),
            html.P('Isolation Forest is an unsupervised learning algorithm that identifies outliers by isolating anomalies. It randomly selects a feature and then randomly selects a split value between the maximum and minimum values of the selected feature.', style={'lineHeight': '1.6', 'color': '#555'}),
            
            html.H3('How It Works:', style={'color': '#4f9fd8', 'marginTop': '20px'}),
            html.Ul([
                html.Li('Recursively partitions the data using random thresholds', style={'marginBottom': '10px'}),
                html.Li('Anomalies require fewer partitions to isolate than normal points', style={'marginBottom': '10px'}),
                html.Li('Assigns anomaly scores based on isolation path length', style={'marginBottom': '10px'}),
                html.Li('Lower scores indicate more anomalous records', style={'marginBottom': '10px'})
            ], style={'color': '#555'}),
            
            html.H3('Advantages:', style={'color': '#4f9fd8', 'marginTop': '20px'}),
            html.Ul([
                html.Li('Does not require distance metrics', style={'marginBottom': '10px'}),
                html.Li('Handles high-dimensional data well', style={'marginBottom': '10px'}),
                html.Li('Fast and scalable', style={'marginBottom': '10px'}),
                html.Li('No need for labeled data', style={'marginBottom': '10px'})
            ], style={'color': '#555'})
        ], style={'backgroundColor': '#f0f7ff', 'padding': '20px', 'borderRadius': '8px', 'borderLeft': '4px solid #4f9fd8'})
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '20px'})
]))