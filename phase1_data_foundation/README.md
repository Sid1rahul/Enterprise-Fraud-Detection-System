# Phase 1: Data Foundation & Basic ML Pipeline

## Overview
This phase implements the core data processing and machine learning pipeline for credit card fraud detection.

## ✅ Completed Tasks
1. **Data Processing Module** - Data ingestion, cleaning, and preprocessing
2. **Feature Engineering Pipeline** - Advanced feature creation and selection
3. **XGBoost Classifier** - Primary supervised learning model
4. **Isolation Forest** - Unsupervised anomaly detection
5. **ADASYN Integration** - Advanced oversampling for class imbalance
6. **SHAP Explainability** - Model interpretability and feature importance
7. **Evaluation Framework** - Comprehensive model assessment

## Directory Structure
```
phase1_data_foundation/
├── src/
│   ├── data_processor.py       # Data processing and cleaning
│   ├── feature_engineer.py     # Feature engineering pipeline
│   ├── models/
│   │   ├── xgboost_model.py   # XGBoost implementation
│   │   └── isolation_forest.py # Isolation Forest implementation
│   ├── oversampling.py        # ADASYN and other oversampling techniques
│   ├── explainability.py      # SHAP and other XAI methods
│   └── evaluation.py          # Model evaluation metrics
├── utils/
│   ├── config.py              # Configuration management
│   ├── logger.py              # Logging utilities
│   └── helpers.py             # Helper functions
├── config/
│   └── default_config.yaml    # Default configuration file
├── data/                      # Sample datasets (generated)
├── main.py                    # Main execution script
└── generate_sample_data.py    # Sample data generator
```

## Quick Start

### 1. Generate Sample Data
```bash
python generate_sample_data.py
```

### 2. Run the Complete Pipeline
```bash
# With default configuration
python main.py --data data/creditcard_medium.csv --output output

# With custom configuration
python main.py --data data/creditcard_medium.csv --config config/default_config.yaml --output output

# Skip hyperparameter optimization for faster execution
python main.py --data data/creditcard_medium.csv --output output --skip-optimization
```

### 3. View Results
Results will be saved in the `output/` directory:
- `models/` - Trained models
- `processed_data/` - Processed datasets
- `results/` - Evaluation results and reports
- `explanations/` - SHAP explanations
- `logs/` - Execution logs

## Key Features

### Advanced Data Processing
- Automatic missing value handling
- Outlier detection and removal
- Feature scaling and normalization
- Categorical encoding

### Sophisticated Feature Engineering
- Temporal features (hour, day, weekend indicators)
- Amount-based features (log, percentiles, categories)
- Behavioral features (rolling statistics, frequency)
- Statistical features (interactions, polynomials)
- PCA features for dimensionality reduction

### Class Imbalance Handling
- ADASYN (Adaptive Synthetic Sampling)
- Multiple SMOTE variants
- Hybrid oversampling techniques
- Automatic method selection and optimization

### Model Training
- **XGBoost**: Gradient boosting with hyperparameter optimization
- **Isolation Forest**: Unsupervised anomaly detection
- Optuna-based hyperparameter tuning
- Cross-validation and early stopping

### Explainable AI
- SHAP (SHapley Additive exPlanations)
- LIME (Local Interpretable Model-agnostic Explanations)
- Permutation feature importance
- Partial dependence plots

### Comprehensive Evaluation
- Standard metrics (accuracy, precision, recall, F1, AUC)
- Cost-sensitive evaluation
- Threshold optimization
- Confusion matrix analysis
- Cross-validation results

## Configuration

The system uses YAML configuration files. Key parameters:

```yaml
# Data Processing
data_processing:
  missing_strategy: "auto"
  handle_outliers: true
  test_size: 0.2

# Feature Engineering
feature_engineering:
  feature_selection_method: "importance"
  n_features_to_select: 30

# XGBoost
xgboost:
  optimization_method: "optuna"
  n_trials: 100

# Evaluation
evaluation:
  cost_matrix:
    tn: 0    # True Negative cost
    fp: 1    # False Positive cost
    fn: 10   # False Negative cost (most expensive)
    tp: -2   # True Positive savings
```

## Output Structure

After running the pipeline, you'll get:

```
output/
├── models/
│   ├── xgboost_model.pkl
│   └── isolation_forest_model.pkl
├── processed_data/
│   ├── X_train.csv
│   ├── X_test.csv
│   ├── y_train.csv
│   └── y_test.csv
├── results/
│   ├── xgboost_evaluation.pkl
│   ├── isolation_forest_evaluation.pkl
│   ├── model_comparison.pkl
│   ├── sampling_report.pkl
│   └── phase1_final_report.pkl
├── explanations/
│   └── xgboost_explanations.pkl
└── logs/
    ├── fraud_detection_phase1.log
    └── fraud_detection_phase1_error.log
```

## Performance Expectations

With the default configuration on a medium dataset (10,000 samples):
- **Processing Time**: 5-15 minutes (depending on optimization)
- **Expected AUC**: 0.85-0.95
- **Expected F1-Score**: 0.70-0.85
- **Memory Usage**: < 2GB

## Next Steps

Phase 1 provides the foundation for:
- **Phase 4**: UiPath RPA & Chatbot Integration
- **Phase 5**: Production Portal & Advanced Features

The trained models and processed data from Phase 1 will be used in subsequent phases.
