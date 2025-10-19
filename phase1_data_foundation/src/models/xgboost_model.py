"""
XGBoost Classifier Implementation for Credit Card Fraud Detection
Advanced gradient boosting with hyperparameter optimization
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional, List
import xgboost as xgb
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import optuna
import joblib
import logging
import warnings
warnings.filterwarnings('ignore')

class XGBoostFraudDetector:
    """
    Advanced XGBoost implementation for fraud detection with hyperparameter optimization
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize XGBoost fraud detector
        
        Args:
            config: Configuration dictionary with model parameters
        """
        self.config = config or {}
        self.model = None
        self.best_params = None
        self.feature_importance = None
        self.training_history = {}
        
        # Default XGBoost parameters optimized for fraud detection
        self.default_params = {
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
            'max_depth': 6,
            'learning_rate': 0.1,
            'n_estimators': 100,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
            'n_jobs': -1,
            'scale_pos_weight': 1  # Will be adjusted based on class imbalance
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def calculate_scale_pos_weight(self, y: pd.Series) -> float:
        """
        Calculate scale_pos_weight for handling class imbalance
        
        Args:
            y: Target variable
            
        Returns:
            Calculated scale_pos_weight value
        """
        negative_count = (y == 0).sum()
        positive_count = (y == 1).sum()
        scale_pos_weight = negative_count / positive_count
        
        self.logger.info(f"Class distribution - Negative: {negative_count}, Positive: {positive_count}")
        self.logger.info(f"Calculated scale_pos_weight: {scale_pos_weight:.2f}")
        
        return scale_pos_weight
    
    def prepare_data(self, X_train: pd.DataFrame, y_train: pd.Series, 
                    X_val: pd.DataFrame = None, y_val: pd.Series = None) -> Tuple[xgb.DMatrix, xgb.DMatrix]:
        """
        Prepare data for XGBoost training
        
        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            
        Returns:
            Tuple of (train_dmatrix, val_dmatrix)
        """
        # Create DMatrix for training
        dtrain = xgb.DMatrix(X_train, label=y_train)
        
        # Create DMatrix for validation if provided
        dval = None
        if X_val is not None and y_val is not None:
            dval = xgb.DMatrix(X_val, label=y_val)
        
        self.logger.info(f"Prepared training data: {X_train.shape}")
        if dval is not None:
            self.logger.info(f"Prepared validation data: {X_val.shape}")
        
        return dtrain, dval
    
    def train_basic_model(self, X_train: pd.DataFrame, y_train: pd.Series, 
                         X_val: pd.DataFrame = None, y_val: pd.Series = None,
                         params: Dict[str, Any] = None) -> xgb.XGBClassifier:
        """
        Train basic XGBoost model with default or provided parameters
        
        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            params: Model parameters
            
        Returns:
            Trained XGBoost model
        """
        # Use provided parameters or defaults
        model_params = params or self.default_params.copy()
        
        # Calculate and set scale_pos_weight for class imbalance
        model_params['scale_pos_weight'] = self.calculate_scale_pos_weight(y_train)
        
        # Initialize model
        self.model = xgb.XGBClassifier(**model_params)
        
        # Prepare evaluation set for early stopping
        eval_set = []
        if X_val is not None and y_val is not None:
            eval_set = [(X_train, y_train), (X_val, y_val)]
        else:
            eval_set = [(X_train, y_train)]
        
        # Train model
        self.logger.info("Training XGBoost model...")
        self.model.fit(
            X_train, y_train,
            eval_set=eval_set,
            eval_metric=['auc', 'logloss'],
            early_stopping_rounds=10,
            verbose=False
        )
        
        # Store training history
        self.training_history = {
            'train_auc': self.model.evals_result()['validation_0']['auc'],
            'train_logloss': self.model.evals_result()['validation_0']['logloss']
        }
        
        if len(eval_set) > 1:
            self.training_history.update({
                'val_auc': self.model.evals_result()['validation_1']['auc'],
                'val_logloss': self.model.evals_result()['validation_1']['logloss']
            })
        
        # Store feature importance
        self.feature_importance = dict(zip(X_train.columns, self.model.feature_importances_))
        
        self.logger.info(f"Model training completed. Best iteration: {self.model.best_iteration}")
        return self.model
    
    def hyperparameter_optimization_grid(self, X_train: pd.DataFrame, y_train: pd.Series,
                                        cv_folds: int = 5) -> Dict[str, Any]:
        """
        Perform hyperparameter optimization using GridSearchCV
        
        Args:
            X_train: Training features
            y_train: Training target
            cv_folds: Number of cross-validation folds
            
        Returns:
            Best parameters found
        """
        # Define parameter grid
        param_grid = {
            'max_depth': [3, 4, 5, 6, 7],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'n_estimators': [100, 200, 300],
            'subsample': [0.7, 0.8, 0.9],
            'colsample_bytree': [0.7, 0.8, 0.9],
            'reg_alpha': [0, 0.1, 0.5],
            'reg_lambda': [1, 1.5, 2]
        }
        
        # Base model with class imbalance handling
        base_params = self.default_params.copy()
        base_params['scale_pos_weight'] = self.calculate_scale_pos_weight(y_train)
        
        base_model = xgb.XGBClassifier(**base_params)
        
        # Grid search with cross-validation
        self.logger.info("Starting Grid Search hyperparameter optimization...")
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid,
            scoring='roc_auc',
            cv=cv_folds,
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        self.best_params = grid_search.best_params_
        self.best_params.update(base_params)  # Include base parameters
        
        self.logger.info(f"Grid Search completed. Best score: {grid_search.best_score_:.4f}")
        self.logger.info(f"Best parameters: {self.best_params}")
        
        return self.best_params
    
    def hyperparameter_optimization_optuna(self, X_train: pd.DataFrame, y_train: pd.Series,
                                          n_trials: int = 100, cv_folds: int = 5) -> Dict[str, Any]:
        """
        Perform hyperparameter optimization using Optuna
        
        Args:
            X_train: Training features
            y_train: Training target
            n_trials: Number of optimization trials
            cv_folds: Number of cross-validation folds
            
        Returns:
            Best parameters found
        """
        def objective(trial):
            # Define hyperparameter search space
            params = {
                'objective': 'binary:logistic',
                'eval_metric': 'auc',
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
                'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
                'reg_alpha': trial.suggest_float('reg_alpha', 0, 2),
                'reg_lambda': trial.suggest_float('reg_lambda', 0, 2),
                'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
                'gamma': trial.suggest_float('gamma', 0, 2),
                'scale_pos_weight': self.calculate_scale_pos_weight(y_train),
                'random_state': 42,
                'n_jobs': -1
            }
            
            # Create and evaluate model
            model = xgb.XGBClassifier(**params)
            scores = cross_val_score(model, X_train, y_train, cv=cv_folds, 
                                   scoring='roc_auc', n_jobs=-1)
            
            return scores.mean()
        
        # Create study and optimize
        self.logger.info(f"Starting Optuna hyperparameter optimization with {n_trials} trials...")
        study = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler())
        study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
        
        # Get best parameters
        self.best_params = study.best_params
        self.best_params.update({
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
            'scale_pos_weight': self.calculate_scale_pos_weight(y_train),
            'random_state': 42,
            'n_jobs': -1
        })
        
        self.logger.info(f"Optuna optimization completed. Best score: {study.best_value:.4f}")
        self.logger.info(f"Best parameters: {self.best_params}")
        
        return self.best_params
    
    def train_optimized_model(self, X_train: pd.DataFrame, y_train: pd.Series,
                             X_val: pd.DataFrame = None, y_val: pd.Series = None,
                             optimization_method: str = 'optuna') -> xgb.XGBClassifier:
        """
        Train model with optimized hyperparameters
        
        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            optimization_method: Method for hyperparameter optimization ('grid', 'optuna')
            
        Returns:
            Trained optimized XGBoost model
        """
        # Perform hyperparameter optimization
        if optimization_method == 'grid':
            self.hyperparameter_optimization_grid(X_train, y_train)
        elif optimization_method == 'optuna':
            self.hyperparameter_optimization_optuna(X_train, y_train)
        else:
            self.logger.warning(f"Unknown optimization method: {optimization_method}. Using default parameters.")
            self.best_params = self.default_params.copy()
            self.best_params['scale_pos_weight'] = self.calculate_scale_pos_weight(y_train)
        
        # Train model with best parameters
        self.model = self.train_basic_model(X_train, y_train, X_val, y_val, self.best_params)
        
        return self.model
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions using trained model
        
        Args:
            X: Features for prediction
            
        Returns:
            Binary predictions
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_basic_model or train_optimized_model first.")
        
        return self.model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get prediction probabilities
        
        Args:
            X: Features for prediction
            
        Returns:
            Prediction probabilities
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_basic_model or train_optimized_model first.")
        
        return self.model.predict_proba(X)
    
    def evaluate_model(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Any]:
        """
        Comprehensive model evaluation
        
        Args:
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dictionary containing evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_basic_model or train_optimized_model first.")
        
        # Make predictions
        y_pred = self.predict(X_test)
        y_pred_proba = self.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        # Classification report
        class_report = classification_report(y_test, y_pred, output_dict=True)
        
        # Confusion matrix
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        evaluation_results = {
            'auc_score': auc_score,
            'classification_report': class_report,
            'confusion_matrix': conf_matrix.tolist(),
            'accuracy': class_report['accuracy'],
            'precision': class_report['1']['precision'],
            'recall': class_report['1']['recall'],
            'f1_score': class_report['1']['f1-score'],
            'support': class_report['1']['support']
        }
        
        self.logger.info(f"Model Evaluation Results:")
        self.logger.info(f"AUC Score: {auc_score:.4f}")
        self.logger.info(f"Accuracy: {evaluation_results['accuracy']:.4f}")
        self.logger.info(f"Precision: {evaluation_results['precision']:.4f}")
        self.logger.info(f"Recall: {evaluation_results['recall']:.4f}")
        self.logger.info(f"F1-Score: {evaluation_results['f1_score']:.4f}")
        
        return evaluation_results
    
    def get_feature_importance(self, top_n: int = 20) -> Dict[str, float]:
        """
        Get top N most important features
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            Dictionary of feature names and importance scores
        """
        if self.feature_importance is None:
            raise ValueError("Feature importance not available. Train model first.")
        
        # Sort features by importance
        sorted_features = sorted(self.feature_importance.items(), 
                               key=lambda x: x[1], reverse=True)
        
        return dict(sorted_features[:top_n])
    
    def save_model(self, filepath: str):
        """
        Save trained model to file
        
        Args:
            filepath: Path to save the model
        """
        if self.model is None:
            raise ValueError("No model to save. Train model first.")
        
        model_data = {
            'model': self.model,
            'best_params': self.best_params,
            'feature_importance': self.feature_importance,
            'training_history': self.training_history
        }
        
        joblib.dump(model_data, filepath)
        self.logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """
        Load trained model from file
        
        Args:
            filepath: Path to load the model from
        """
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.best_params = model_data.get('best_params')
        self.feature_importance = model_data.get('feature_importance')
        self.training_history = model_data.get('training_history', {})
        
        self.logger.info(f"Model loaded from {filepath}")
    
    def plot_training_history(self):
        """
        Plot training history if available
        """
        if not self.training_history:
            self.logger.warning("No training history available.")
            return
        
        try:
            import matplotlib.pyplot as plt
            
            fig, axes = plt.subplots(1, 2, figsize=(15, 5))
            
            # Plot AUC
            if 'train_auc' in self.training_history:
                axes[0].plot(self.training_history['train_auc'], label='Train AUC')
                if 'val_auc' in self.training_history:
                    axes[0].plot(self.training_history['val_auc'], label='Validation AUC')
                axes[0].set_title('AUC Score')
                axes[0].set_xlabel('Iteration')
                axes[0].set_ylabel('AUC')
                axes[0].legend()
                axes[0].grid(True)
            
            # Plot Log Loss
            if 'train_logloss' in self.training_history:
                axes[1].plot(self.training_history['train_logloss'], label='Train Log Loss')
                if 'val_logloss' in self.training_history:
                    axes[1].plot(self.training_history['val_logloss'], label='Validation Log Loss')
                axes[1].set_title('Log Loss')
                axes[1].set_xlabel('Iteration')
                axes[1].set_ylabel('Log Loss')
                axes[1].legend()
                axes[1].grid(True)
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            self.logger.warning("Matplotlib not available. Cannot plot training history.")


if __name__ == "__main__":
    # Example usage
    detector = XGBoostFraudDetector()
    
    # For testing with sample data
    # detector.train_basic_model(X_train, y_train, X_val, y_val)
    # evaluation_results = detector.evaluate_model(X_test, y_test)
    print("XGBoostFraudDetector module created successfully!")
