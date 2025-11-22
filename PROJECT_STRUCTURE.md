
## 📁 Directory Structure

```
bank-analysis-webapp/
├── app.py                      # Main Dash application
├── requirements.txt            # Python dependencies (84 packages)
├── README.md                   # Setup & usage guide
├── LICENSE                     # MIT License
│
├── assets/                     # CSS styling (8 files)
│   ├── style.css              # Global styles
│   ├── churn_analysis.css     # Churn page
│   ├── segmentation.css       # Segmentation page
│   ├── data_overview.css      # Data overview page
│   ├── insights.css           # Insights page
│   ├── prediction_model.css   # Prediction page
│   ├── risk_analysis.css      # Risk analysis page
│   └── techniques_info.css    # Techniques display
│
├── components/                 # Reusable components
│   ├── navbar.py              # Navigation bar
│   └── techniques_info.py     # Techniques display
│
├── pages/                      # Dashboard pages (3 active, 3 inactive)
│   ├── churn_analysis.py      # ✓ XGBoost classification
│   ├── data_overview.py       # ✓ Isolation Forest
│   ├── segmentation.py        # ✓ K-Means clustering
│   ├── insights_recommendations.py     # Inactive
│   ├── prediction_model.py    # Inactive
│   └── risk_analysis.py       # Inactive
│
├── data/                       # Customer datasets
│   ├── bank-data.csv          # Raw (165,034 records)
│   ├── test-data.csv          # Test data
│   └── processed-data/
│       ├── bank-data-processed.csv     # Final (165,034 × 14)
│       ├── feature_importance.csv      # Feature scores
│       └── past-data.csv               # Historical data
│
├── models/                     # ML models
│   └── xgb_model_v2.pkl       # XGBoost model
│
├── notebooks/                  # Documentation
│   ├── decision_rules.txt     # Model rules
│   └── Insights from the data.docx    # Business insights
│
└── .git/                       # Git repository
```

---

## 📋 Key Information

| Item | Details |
|------|---------|
| **Dataset** | 165,034 customers × 14 features |
| **Churn Rate** | ~20% (33,000+ customers) |
| **Outliers** | 8,252 (5% anomalies) |
| **Active Pages** | 3 (Churn, Segmentation, Data Overview) |
| **ML Techniques** | XGBoost, K-Means, Isolation Forest |
| **Primary Color** | #1e3a5f (Dark Blue) |
| **Accent Color** | #4f9fd8 (Sky Blue) |

---

