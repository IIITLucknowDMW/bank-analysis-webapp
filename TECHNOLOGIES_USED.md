
## How the Project Uses These Topics

### 1. **Classification** ✅ (Primary Goal: Churn Prediction)
The main objective of the project is to build a model that predicts whether a bank customer will close their account (Churn). This is a classic binary classification problem.

- **Algorithm Used:** XGBoost
- **Location:** `pages/prediction_model.py` | Model: `models/xgb_model_v2.pkl`
- **Purpose:** Predict the probability that a customer will churn
- **Output:** Binary prediction + Churn probability score (0-1)
- **Dashboard Page:** Churn Prediction Model

---

### 2. **Clustering** ✅ (Goal: Customer Segmentation)
Clustering is used to group customers into distinct segments based on their behavior or demographics. This provides valuable context for understanding churn patterns.

- **Algorithm Used:** K-Means Clustering
- **Location:** `pages/segmentation.py`
- **Purpose:** Group customers into segments by behavior and characteristics
- **Application:** These segments help identify which groups are most at-risk of churning
- **Dashboard Page:** Customer Segmentation

---

### 3. **Outlier Detection** ✅ (Goal: Data Cleaning/Preprocessing)
Data preprocessing is a mandatory step in any professional machine learning project. Outlier detection is performed during data cleaning before building classification or clustering models.

- **Status:** ✅ Fully Implemented
- **Algorithm Used:** Isolation Forest
- **Location:** `pages/data_overview.py`
- **Purpose:** Identify and handle extreme values in customer data that could skew the models
- **Dashboard Page:** Data Overview - Shows outlier statistics, anomaly score distribution, and top 10 detected outliers
- **Output:** 
  - Total outliers detected
  - Outlier percentage
  - Anomaly scores for each record
  - Top 10 most anomalous records











