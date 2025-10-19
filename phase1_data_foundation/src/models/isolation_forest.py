"""
Isolation Forest Implementation for Credit Card Fraud Detection
Unsupervised anomaly detection for fraud identification
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional, List
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler
import joblib
import logging
import warnings
warnings.filterwarnings('ignore')

class IsolationForestFraudDetector:
    """
    Advanced Isolation Forest implementation for unsupervised fraud detection
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Isolation Forest fraud detector
        
        Args:
            config: Configuration dictionary with model parameters
        """
        self.config = config or {}
        self.model = None
        self.scaler = StandardScaler()
        self.best_params = None
        self.feature_importance = None
        self.anomaly_scores = None
        self.threshold = None
        
        # Default Isolation Forest parameters optimized for fraud detection
        self.default_params = {
            'n_estimators': 100,
            'max_samples': 'auto',
            'contamination': 0.1,  # Expected proportion of anomalies
            'max_features': 1.0,
            'bootstrap': False,
            'random_state': 42,
            'n_jobs': -1
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def estimate_contamination(self, y: pd.Series = None, method: str = 'auto') -> float:
        """
        Estimate contamination rate (proportion of anomalies)
        
        Args:
            y: Target variable (if available for supervised estimation)
            method: Method for estimation ('auto', 'supervised', 'percentile')
            
        Returns:
            Estimated contamination rate
        """
        if method == 'supervised' and y is not None:
            # Use actual fraud rate from labeled data
            contamination = y.sum() / len(y)
            self.logger.info(f"Supervised contamination estimation: {contamination:.4f}")
            
        elif method == 'percentile':
            # Use a conservative estimate (typical fraud rates are 0.1-2%)
            contamination = 0.002  # 0.2%
            self.logger.info(f"Percentile-based contamination estimation: {contamination:.4f}")
            
        else:  # auto
            if y is not None:
                contamination = min(0.1, max(0.001, y.sum() / len(y)))
            else:
                contamination = 0.01  # Default 1%
            self.logger.info(f"Auto contamination estimation: {contamination:.4f}")
        
        return contamination
    
    def preprocess_data(self, X: pd.DataFrame, fit_scaler: bool = True) -> pd.DataFrame:
        """
        Preprocess data for Isolation Forest
        
        Args:
            X: Input features
            fit_scaler: Whether to fit the scaler (True for training, False for inference)
            
        Returns:
            Preprocessed features
        """
        X_processed = X.copy()
        
        # Handle missing values
        X_processed = X_processed.fillna(X_processed.median())
        
        # Scale features for better performance
        if fit_scaler:
            X_scaled = self.scaler.fit_transform(X_processed)
        else:
            X_scaled = self.scaler.transform(X_processed)
        
        # Convert back to DataFrame
        X_scaled_df = pd.DataFrame(X_scaled, columns=X_processed.columns, index=X_processed.index)
        
        self.logger.info(f"Preprocessed data shape: {X_scaled_df.shape}")
        return X_scaled_df
    
    def train_basic_model(self, X_train: pd.DataFrame, y_train: pd.Series = None,
                         params: Dict[str, Any] = None) -> IsolationForest:
        """
        Train basic Isolation Forest model
        
        Args:
            X_train: Training features
            y_train: Training target (optional, used for contamination estimation)
            params: Model parameters
            
        Returns:
            Trained Isolation Forest model
        """
        # Use provided parameters or defaults
        model_params = params or self.default_params.copy()
        
        # Estimate contamination if not provided
        if 'contamination' not in model_params or model_params['contamination'] == 'auto':
            model_params['contamination'] = self.estimate_contamination(y_train)
        
        # Preprocess data
        X_processed = self.preprocess_data(X_train, fit_scaler=True)
        
        # Initialize and train model
        self.model = IsolationForest(**model_params)
        
        self.logger.info("Training Isolation Forest model...")
        self.model.fit(X_processed)
        
        # Calculate anomaly scores
        self.anomaly_scores = self.model.decision_function(X_processed)
        
        # Determine threshold for anomaly detection
        self.threshold = np.percentile(self.anomaly_scores, 
                                     (1 - model_params['contamination']) * 100)
        
        self.logger.info(f"Model training completed. Anomaly threshold: {self.threshold:.4f}")
        return self.model
    
    def hyperparameter_optimization(self, X_train: pd.DataFrame, y_train: pd.Series = None,
                                   cv_folds: int = 5) -> Dict[str, Any]:
        """
        Perform hyperparameter optimization for Isolation Forest
        
        Args:
            X_train: Training features
            y_train: Training target (for contamination estimation)
            cv_folds: Number of cross-validation folds
            
        Returns:
            Best parameters found
        """
        # Estimate contamination
        contamination_rate = self.estimate_contamination(y_train)
        
        # Define parameter grid
        param_grid = {
            'n_estimators': [50, 100, 200, 300],
            'max_samples': ['auto', 0.5, 0.7, 0.9],
            'contamination': [contamination_rate * 0.5, contamination_rate, 
                            contamination_rate * 1.5, contamination_rate * 2],
            'max_features': [0.5, 0.7, 0.9, 1.0],
            'bootstrap': [True, False]
        }
        
        # Preprocess data
        X_processed = self.preprocess_data(X_train, fit_scaler=True)
        
        # Custom scoring function for unsupervised learning
        def isolation_forest_scorer(estimator, X, y=None):
            # Use silhouette score or reconstruction error as proxy
            anomaly_scores = estimator.decision_function(X)
            # Return negative mean anomaly score (higher is better for GridSearchCV)
            return -np.mean(anomaly_scores)
        
        # Grid search
        self.logger.info("Starting hyperparameter optimization...")
        base_model = IsolationForest(random_state=42, n_jobs=-1)
        
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid,
            scoring=isolation_forest_scorer,
            cv=cv_folds,
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_processed)
        
        self.best_params = grid_search.best_params_
        self.best_params['random_state'] = 42
        self.best_params['n_jobs'] = -1
        
        self.logger.info(f"Hyperparameter optimization completed.")
        self.logger.info(f"Best parameters: {self.best_params}")
        
        return self.best_params
    
    def train_optimized_model(self, X_train: pd.DataFrame, y_train: pd.Series = None) -> IsolationForest:
        """
        Train model with optimized hyperparameters
        
        Args:
            X_train: Training features
            y_train: Training target
            
        Returns:
            Trained optimized Isolation Forest model
        """
        # Perform hyperparameter optimization
        self.hyperparameter_optimization(X_train, y_train)
        
        # Train model with best parameters
        self.model = self.train_basic_model(X_train, y_train, self.best_params)
        
        return self.model
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make anomaly predictions
        
        Args:
            X: Features for prediction
            
        Returns:
            Binary predictions (1 for normal, -1 for anomaly)
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_basic_model or train_optimized_model first.")
        
        # Preprocess data
        X_processed = self.preprocess_data(X, fit_scaler=False)
        
        return self.model.predict(X_processed)
    
    def predict_anomaly_scores(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get anomaly scores
        
        Args:
            X: Features for prediction
            
        Returns:
            Anomaly scores (lower scores indicate higher anomaly likelihood)
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_basic_model or train_optimized_model first.")
        
        # Preprocess data
        X_processed = self.preprocess_data(X, fit_scaler=False)
        
        return self.model.decision_function(X_processed)
    
    def predict_binary(self, X: pd.DataFrame, threshold: float = None) -> np.ndarray:
        """
        Make binary fraud predictions using custom threshold
        
        Args:
            X: Features for prediction
            threshold: Custom threshold for anomaly detection
            
        Returns:
            Binary predictions (1 for fraud, 0 for normal)
        """
        # Get anomaly scores
        scores = self.predict_anomaly_scores(X)
        
        # Use provided threshold or learned threshold
        thresh = threshold if threshold is not None else self.threshold
        
        # Convert to binary predictions (1 for fraud, 0 for normal)
        predictions = (scores < thresh).astype(int)
        
        return predictions
    
    def evaluate_model(self, X_test: pd.DataFrame, y_test: pd.Series = None,
                      threshold: float = None) -> Dict[str, Any]:
        """
        Comprehensive model evaluation
        
        Args:
            X_test: Test features
            y_test: Test target (if available)
            threshold: Custom threshold for evaluation
            
        Returns:
            Dictionary containing evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_basic_model or train_optimized_model first.")
        
        # Get predictions and scores
        anomaly_scores = self.predict_anomaly_scores(X_test)
        binary_predictions = self.predict_binary(X_test, threshold)
        
        evaluation_results = {
            'anomaly_scores': anomaly_scores,
            'binary_predictions': binary_predictions,
            'threshold_used': threshold if threshold is not None else self.threshold
        }
        
        # If ground truth is available, calculate supervised metrics
        if y_test is not None:
            auc_score = roc_auc_score(y_test, -anomaly_scores)  # Negative because lower scores = higher anomaly
            
            # Classification report
            class_report = classification_report(y_test, binary_predictions, output_dict=True)
            
            # Confusion matrix
            conf_matrix = confusion_matrix(y_test, binary_predictions)
            
            evaluation_results.update({
                'auc_score': auc_score,
                'classification_report': class_report,
                'confusion_matrix': conf_matrix.tolist(),
                'accuracy': class_report['accuracy'],
                'precision': class_report.get('1', {}).get('precision', 0),
                'recall': class_report.get('1', {}).get('recall', 0),
                'f1_score': class_report.get('1', {}).get('f1-score', 0)
            })
            
            self.logger.info(f"Model Evaluation Results:")
            self.logger.info(f"AUC Score: {auc_score:.4f}")
            self.logger.info(f"Accuracy: {evaluation_results['accuracy']:.4f}")
            self.logger.info(f"Precision: {evaluation_results['precision']:.4f}")
            self.logger.info(f"Recall: {evaluation_results['recall']:.4f}")
            self.logger.info(f"F1-Score: {evaluation_results['f1_score']:.4f}")
        
        else:
            # Unsupervised evaluation metrics
            anomaly_rate = (binary_predictions == 1).mean()
            mean_anomaly_score = anomaly_scores.mean()
            std_anomaly_score = anomaly_scores.std()
            
            evaluation_results.update({
                'anomaly_rate': anomaly_rate,
                'mean_anomaly_score': mean_anomaly_score,
                'std_anomaly_score': std_anomaly_score
            })
            
            self.logger.info(f"Unsupervised Evaluation Results:")
            self.logger.info(f"Anomaly Rate: {anomaly_rate:.4f}")
            self.logger.info(f"Mean Anomaly Score: {mean_anomaly_score:.4f}")
            self.logger.info(f"Std Anomaly Score: {std_anomaly_score:.4f}")
        
        return evaluation_results
    
    def optimize_threshold(self, X_val: pd.DataFrame, y_val: pd.Series, 
                          metric: str = 'f1') -> float:
        """
        Optimize detection threshold based on validation data
        
        Args:
            X_val: Validation features
            y_val: Validation target
            metric: Metric to optimize ('f1', 'precision', 'recall', 'accuracy')
            
        Returns:
            Optimal threshold
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_basic_model or train_optimized_model first.")
        
        # Get anomaly scores
        scores = self.predict_anomaly_scores(X_val)
        
        # Test different thresholds
        thresholds = np.percentile(scores, np.arange(1, 100, 1))
        best_threshold = None
        best_score = -np.inf
        
        for threshold in thresholds:
            predictions = (scores < threshold).astype(int)
            
            if metric == 'f1':
                from sklearn.metrics import f1_score
                score = f1_score(y_val, predictions)
            elif metric == 'precision':
                from sklearn.metrics import precision_score
                score = precision_score(y_val, predictions, zero_division=0)
            elif metric == 'recall':
                from sklearn.metrics import recall_score
                score = recall_score(y_val, predictions, zero_division=0)
            elif metric == 'accuracy':
                from sklearn.metrics import accuracy_score
                score = accuracy_score(y_val, predictions)
            else:
                raise ValueError(f"Unsupported metric: {metric}")
            
            if score > best_score:
                best_score = score
                best_threshold = threshold
        
        self.threshold = best_threshold
        self.logger.info(f"Optimized threshold: {best_threshold:.4f} (best {metric}: {best_score:.4f})")
        
        return best_threshold
    
    def get_anomaly_explanation(self, X: pd.DataFrame, top_n: int = 10) -> Dict[str, Any]:
        """
        Get explanation for anomaly detection (feature contributions)
        
        Args:
            X: Features to explain
            top_n: Number of top contributing features
            
        Returns:
            Dictionary with anomaly explanations
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_basic_model or train_optimized_model first.")
        
        # Preprocess data
        X_processed = self.preprocess_data(X, fit_scaler=False)
        
        # Get anomaly scores
        scores = self.predict_anomaly_scores(X_processed)
        
        # Calculate feature contributions (simplified approach)
        # This is an approximation - true feature importance for IF is complex
        feature_contributions = {}
        
        for idx, row in X_processed.iterrows():
            # Calculate deviation from median for each feature
            deviations = np.abs(row - X_processed.median())
            
            # Normalize deviations
            normalized_deviations = deviations / (X_processed.std() + 1e-8)
            
            feature_contributions[idx] = dict(
                zip(X_processed.columns, normalized_deviations)
            )
        
        # Get top contributing features for each sample
        explanations = {}
        for idx in feature_contributions:
            sorted_features = sorted(
                feature_contributions[idx].items(),
                key=lambda x: x[1], reverse=True
            )
            explanations[idx] = {
                'anomaly_score': scores[X_processed.index.get_loc(idx)],
                'top_features': dict(sorted_features[:top_n])
            }
        
        return explanations
    
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
            'scaler': self.scaler,
            'best_params': self.best_params,
            'threshold': self.threshold,
            'anomaly_scores': self.anomaly_scores
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
        self.scaler = model_data['scaler']
        self.best_params = model_data.get('best_params')
        self.threshold = model_data.get('threshold')
        self.anomaly_scores = model_data.get('anomaly_scores')
        
        self.logger.info(f"Model loaded from {filepath}")
    
    def plot_anomaly_scores(self, scores: np.ndarray = None, y_true: np.ndarray = None):
        """
        Plot distribution of anomaly scores
        
        Args:
            scores: Anomaly scores to plot
            y_true: True labels (if available)
        """
        if scores is None:
            scores = self.anomaly_scores
        
        if scores is None:
            self.logger.warning("No anomaly scores available.")
            return
        
        try:
            import matplotlib.pyplot as plt
            
            fig, axes = plt.subplots(1, 2, figsize=(15, 5))
            
            # Plot score distribution
            axes[0].hist(scores, bins=50, alpha=0.7, edgecolor='black')
            if self.threshold is not None:
                axes[0].axvline(self.threshold, color='red', linestyle='--', 
                              label=f'Threshold: {self.threshold:.3f}')
            axes[0].set_title('Anomaly Score Distribution')
            axes[0].set_xlabel('Anomaly Score')
            axes[0].set_ylabel('Frequency')
            axes[0].legend()
            axes[0].grid(True, alpha=0.3)
            
            # Plot scores by class (if labels available)
            if y_true is not None:
                normal_scores = scores[y_true == 0]
                fraud_scores = scores[y_true == 1]
                
                axes[1].hist(normal_scores, bins=30, alpha=0.7, label='Normal', color='blue')
                axes[1].hist(fraud_scores, bins=30, alpha=0.7, label='Fraud', color='red')
                if self.threshold is not None:
                    axes[1].axvline(self.threshold, color='black', linestyle='--', 
                                  label=f'Threshold: {self.threshold:.3f}')
                axes[1].set_title('Anomaly Scores by Class')
                axes[1].set_xlabel('Anomaly Score')
                axes[1].set_ylabel('Frequency')
                axes[1].legend()
                axes[1].grid(True, alpha=0.3)
            else:
                axes[1].text(0.5, 0.5, 'No labels available\nfor class comparison', 
                           ha='center', va='center', transform=axes[1].transAxes)
                axes[1].set_title('Class Comparison Not Available')
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            self.logger.warning("Matplotlib not available. Cannot plot anomaly scores.")


if __name__ == "__main__":
    # Example usage
    detector = IsolationForestFraudDetector()
    
    # For testing with sample data
    # detector.train_basic_model(X_train, y_train)
    # evaluation_results = detector.evaluate_model(X_test, y_test)
    print("IsolationForestFraudDetector module created successfully!")
