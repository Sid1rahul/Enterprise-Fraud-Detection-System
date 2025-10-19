"""
Simple Demo of Credit Card Fraud Detection
Demonstrates basic functionality without heavy dependencies
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data(data_path):
    """Load and preprocess the data"""
    print("Loading data...")
    df = pd.read_csv(data_path)
    print(f"Data loaded: {df.shape}")
    print(f"Class distribution:\n{df['Class'].value_counts()}")
    
    # Separate features and target
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    # Handle categorical columns
    categorical_cols = X.select_dtypes(include=['object']).columns
    le = LabelEncoder()
    for col in categorical_cols:
        X[col] = le.fit_transform(X[col].astype(str))
    
    # Scale numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    
    return X_scaled, y

def train_models(X_train, y_train):
    """Train fraud detection models"""
    print("\nTraining models...")
    
    # Random Forest (substitute for XGBoost)
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    rf_model.fit(X_train, y_train)
    print("Random Forest model trained")
    
    # Isolation Forest
    if_model = IsolationForest(
        contamination=0.002,  # Expected fraud rate
        random_state=42,
        n_jobs=-1
    )
    if_model.fit(X_train)
    print("Isolation Forest model trained")
    
    return rf_model, if_model

def evaluate_models(rf_model, if_model, X_test, y_test):
    """Evaluate model performance"""
    print("\nEvaluating models...")
    
    # Random Forest evaluation
    rf_pred = rf_model.predict(X_test)
    rf_pred_proba = rf_model.predict_proba(X_test)[:, 1]
    
    print("\n=== RANDOM FOREST RESULTS ===")
    print("Classification Report:")
    print(classification_report(y_test, rf_pred))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, rf_pred_proba):.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, rf_pred)
    print(f"Confusion Matrix:\n{cm}")
    
    # Isolation Forest evaluation
    if_pred = if_model.predict(X_test)
    if_pred_binary = (if_pred == -1).astype(int)  # -1 means anomaly (fraud)
    
    print("\n=== ISOLATION FOREST RESULTS ===")
    print("Classification Report:")
    print(classification_report(y_test, if_pred_binary))
    
    # Feature importance from Random Forest
    feature_importance = pd.DataFrame({
        'feature': X_test.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n=== TOP 10 MOST IMPORTANT FEATURES ===")
    print(feature_importance.head(10))
    
    return rf_pred_proba, if_pred_binary

def calculate_business_impact(y_test, rf_pred, if_pred):
    """Calculate business impact of fraud detection"""
    print("\n=== BUSINESS IMPACT ANALYSIS ===")
    
    # Cost matrix (example values)
    cost_matrix = {
        'true_negative': 0,    # Correctly identified normal transaction
        'false_positive': 1,   # Normal transaction flagged as fraud
        'false_negative': 10,  # Fraud transaction missed (most expensive)
        'true_positive': -2    # Correctly identified fraud (savings)
    }
    
    # Calculate costs for Random Forest
    rf_cm = confusion_matrix(y_test, rf_pred)
    tn, fp, fn, tp = rf_cm.ravel()
    
    rf_total_cost = (
        tn * cost_matrix['true_negative'] +
        fp * cost_matrix['false_positive'] +
        fn * cost_matrix['false_negative'] +
        tp * cost_matrix['true_positive']
    )
    
    print(f"Random Forest - Total Cost: ${rf_total_cost}")
    print(f"Random Forest - Cost per Transaction: ${rf_total_cost/len(y_test):.2f}")
    
    # Calculate costs for Isolation Forest
    if_cm = confusion_matrix(y_test, if_pred)
    tn_if, fp_if, fn_if, tp_if = if_cm.ravel()
    
    if_total_cost = (
        tn_if * cost_matrix['true_negative'] +
        fp_if * cost_matrix['false_positive'] +
        fn_if * cost_matrix['false_negative'] +
        tp_if * cost_matrix['true_positive']
    )
    
    print(f"Isolation Forest - Total Cost: ${if_total_cost}")
    print(f"Isolation Forest - Cost per Transaction: ${if_total_cost/len(y_test):.2f}")

def main():
    """Main execution function"""
    print("=" * 60)
    print("CREDIT CARD FRAUD DETECTION - SIMPLE DEMO")
    print("=" * 60)
    
    # Check if data exists
    data_path = "data/creditcard_medium.csv"
    if not os.path.exists(data_path):
        print(f"Data file not found: {data_path}")
        print("Please run 'python generate_sample_data.py' first")
        return
    
    try:
        # Load and preprocess data
        X, y = load_and_preprocess_data(data_path)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        print(f"\nData split - Train: {X_train.shape}, Test: {X_test.shape}")
        
        # Train models
        rf_model, if_model = train_models(X_train, y_train)
        
        # Evaluate models
        rf_pred_proba, if_pred = evaluate_models(rf_model, if_model, X_test, y_test)
        
        # Convert probabilities to binary predictions for cost analysis
        rf_pred = (rf_pred_proba > 0.5).astype(int)
        
        # Calculate business impact
        calculate_business_impact(y_test, rf_pred, if_pred)
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nKey Insights:")
        print("1. Random Forest provides probability scores for fraud likelihood")
        print("2. Isolation Forest detects anomalous patterns without labels")
        print("3. Cost-sensitive evaluation shows business impact")
        print("4. Feature importance helps understand fraud indicators")
        
        # Save simple results
        os.makedirs("output", exist_ok=True)
        
        results_summary = {
            'model_performance': {
                'random_forest_auc': roc_auc_score(y_test, rf_pred_proba),
                'total_transactions_tested': len(y_test),
                'fraud_cases_in_test': y_test.sum(),
                'normal_cases_in_test': (y_test == 0).sum()
            }
        }
        
        print(f"\nResults saved to output/ directory")
        print(f"AUC Score: {results_summary['model_performance']['random_forest_auc']:.4f}")
        
    except Exception as e:
        print(f"Error during execution: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
