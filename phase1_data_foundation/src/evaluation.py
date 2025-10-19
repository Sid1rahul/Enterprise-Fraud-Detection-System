"""
Comprehensive Model Evaluation Framework for Credit Card Fraud Detection
Advanced metrics, visualization, and performance analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional, Union
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    average_precision_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve, matthews_corrcoef, cohen_kappa_score
)
from sklearn.model_selection import cross_val_score, learning_curve, validation_curve
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import warnings
warnings.filterwarnings('ignore')

class ModelEvaluator:
    """
    Comprehensive model evaluation framework for fraud detection models
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Model Evaluator
        
        Args:
            config: Configuration dictionary with evaluation parameters
        """
        self.config = config or {}
        self.evaluation_results = {}
        self.cost_matrix = None
        self.threshold_analysis = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def set_cost_matrix(self, cost_matrix: Dict[str, float] = None):
        """
        Set cost matrix for cost-sensitive evaluation
        
        Args:
            cost_matrix: Dictionary with cost values
                        {'tn': true_negative_cost, 'fp': false_positive_cost,
                         'fn': false_negative_cost, 'tp': true_positive_cost}
        """
        if cost_matrix is None:
            # Default costs for fraud detection (FN is most expensive)
            self.cost_matrix = {
                'tn': 0,    # True Negative (correctly identified normal transaction)
                'fp': 1,    # False Positive (normal transaction flagged as fraud)
                'fn': 10,   # False Negative (fraud transaction missed)
                'tp': -2    # True Positive (correctly identified fraud, negative = savings)
            }
        else:
            self.cost_matrix = cost_matrix
        
        self.logger.info(f"Cost matrix set: {self.cost_matrix}")
    
    def calculate_basic_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, 
                               y_pred_proba: np.ndarray = None) -> Dict[str, float]:
        """
        Calculate basic classification metrics
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_pred_proba: Predicted probabilities
            
        Returns:
            Dictionary containing basic metrics
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, zero_division=0),
            'specificity': self._calculate_specificity(y_true, y_pred),
            'matthews_corrcoef': matthews_corrcoef(y_true, y_pred),
            'cohen_kappa': cohen_kappa_score(y_true, y_pred)
        }
        
        # Add probability-based metrics if available
        if y_pred_proba is not None:
            metrics.update({
                'roc_auc': roc_auc_score(y_true, y_pred_proba),
                'average_precision': average_precision_score(y_true, y_pred_proba)
            })
        
        return metrics
    
    def _calculate_specificity(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate specificity (True Negative Rate)"""
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return tn / (tn + fp) if (tn + fp) > 0 else 0.0
    
    def calculate_confusion_matrix_metrics(self, y_true: np.ndarray, 
                                         y_pred: np.ndarray) -> Dict[str, Any]:
        """
        Calculate detailed confusion matrix metrics
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            
        Returns:
            Dictionary containing confusion matrix and derived metrics
        """
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        total = tn + fp + fn + tp
        
        metrics = {
            'confusion_matrix': cm.tolist(),
            'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp),
            'total_samples': int(total),
            'true_negative_rate': tn / (tn + fp) if (tn + fp) > 0 else 0,
            'false_positive_rate': fp / (tn + fp) if (tn + fp) > 0 else 0,
            'true_positive_rate': tp / (tp + fn) if (tp + fn) > 0 else 0,
            'false_negative_rate': fn / (tp + fn) if (tp + fn) > 0 else 0,
            'positive_predictive_value': tp / (tp + fp) if (tp + fp) > 0 else 0,
            'negative_predictive_value': tn / (tn + fn) if (tn + fn) > 0 else 0
        }
        
        return metrics
    
    def calculate_cost_sensitive_metrics(self, y_true: np.ndarray, 
                                       y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate cost-sensitive metrics
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            
        Returns:
            Dictionary containing cost-sensitive metrics
        """
        if self.cost_matrix is None:
            self.set_cost_matrix()
        
        cm_metrics = self.calculate_confusion_matrix_metrics(y_true, y_pred)
        
        # Calculate total cost
        total_cost = (
            cm_metrics['tn'] * self.cost_matrix['tn'] +
            cm_metrics['fp'] * self.cost_matrix['fp'] +
            cm_metrics['fn'] * self.cost_matrix['fn'] +
            cm_metrics['tp'] * self.cost_matrix['tp']
        )
        
        # Calculate cost per prediction
        cost_per_prediction = total_cost / cm_metrics['total_samples']
        
        # Calculate savings (negative cost is savings)
        total_savings = -min(0, total_cost)
        
        cost_metrics = {
            'total_cost': total_cost,
            'cost_per_prediction': cost_per_prediction,
            'total_savings': total_savings,
            'cost_reduction_percentage': (total_savings / abs(total_cost)) * 100 if total_cost != 0 else 0
        }
        
        return cost_metrics
    
    def threshold_analysis(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                          thresholds: np.ndarray = None) -> Dict[str, Any]:
        """
        Perform threshold analysis to find optimal decision threshold
        
        Args:
            y_true: True labels
            y_pred_proba: Predicted probabilities
            thresholds: Array of thresholds to test
            
        Returns:
            Dictionary containing threshold analysis results
        """
        if thresholds is None:
            thresholds = np.arange(0.1, 1.0, 0.05)
        
        self.logger.info(f"Performing threshold analysis with {len(thresholds)} thresholds...")
        
        threshold_results = []
        
        for threshold in thresholds:
            y_pred = (y_pred_proba >= threshold).astype(int)
            
            # Calculate metrics for this threshold
            basic_metrics = self.calculate_basic_metrics(y_true, y_pred, y_pred_proba)
            cm_metrics = self.calculate_confusion_matrix_metrics(y_true, y_pred)
            cost_metrics = self.calculate_cost_sensitive_metrics(y_true, y_pred)
            
            result = {
                'threshold': threshold,
                **basic_metrics,
                **cm_metrics,
                **cost_metrics
            }
            
            threshold_results.append(result)
        
        # Convert to DataFrame for easier analysis
        threshold_df = pd.DataFrame(threshold_results)
        
        # Find optimal thresholds based on different criteria
        optimal_thresholds = {
            'f1_score': threshold_df.loc[threshold_df['f1_score'].idxmax(), 'threshold'],
            'precision': threshold_df.loc[threshold_df['precision'].idxmax(), 'threshold'],
            'recall': threshold_df.loc[threshold_df['recall'].idxmax(), 'threshold'],
            'roc_auc': threshold_df.loc[threshold_df['roc_auc'].idxmax(), 'threshold'],
            'cost_minimization': threshold_df.loc[threshold_df['total_cost'].idxmin(), 'threshold'],
            'matthews_corrcoef': threshold_df.loc[threshold_df['matthews_corrcoef'].idxmax(), 'threshold']
        }
        
        self.threshold_analysis = {
            'threshold_results': threshold_df,
            'optimal_thresholds': optimal_thresholds,
            'best_threshold_f1': optimal_thresholds['f1_score'],
            'best_metrics_f1': threshold_df[threshold_df['threshold'] == optimal_thresholds['f1_score']].iloc[0].to_dict()
        }
        
        self.logger.info(f"Threshold analysis completed. Best F1 threshold: {optimal_thresholds['f1_score']:.3f}")
        
        return self.threshold_analysis
    
    def cross_validation_evaluation(self, model: Any, X: pd.DataFrame, y: pd.Series,
                                   cv_folds: int = 5, scoring: List[str] = None) -> Dict[str, Any]:
        """
        Perform cross-validation evaluation
        
        Args:
            model: Model to evaluate
            X: Feature data
            y: Target data
            cv_folds: Number of cross-validation folds
            scoring: List of scoring metrics
            
        Returns:
            Dictionary containing cross-validation results
        """
        if scoring is None:
            scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        
        self.logger.info(f"Performing {cv_folds}-fold cross-validation...")
        
        cv_results = {}
        
        for metric in scoring:
            try:
                scores = cross_val_score(model, X, y, cv=cv_folds, scoring=metric)
                cv_results[metric] = {
                    'scores': scores.tolist(),
                    'mean': scores.mean(),
                    'std': scores.std(),
                    'min': scores.min(),
                    'max': scores.max()
                }
            except Exception as e:
                self.logger.warning(f"Could not calculate {metric}: {str(e)}")
                cv_results[metric] = None
        
        self.logger.info("Cross-validation completed")
        return cv_results
    
    def learning_curve_analysis(self, model: Any, X: pd.DataFrame, y: pd.Series,
                               train_sizes: np.ndarray = None, cv_folds: int = 5) -> Dict[str, Any]:
        """
        Perform learning curve analysis
        
        Args:
            model: Model to analyze
            X: Feature data
            y: Target data
            train_sizes: Training set sizes to use
            cv_folds: Number of cross-validation folds
            
        Returns:
            Dictionary containing learning curve data
        """
        if train_sizes is None:
            train_sizes = np.linspace(0.1, 1.0, 10)
        
        self.logger.info("Performing learning curve analysis...")
        
        train_sizes_abs, train_scores, val_scores = learning_curve(
            model, X, y, train_sizes=train_sizes, cv=cv_folds, 
            scoring='f1', n_jobs=-1
        )
        
        learning_curve_data = {
            'train_sizes': train_sizes_abs.tolist(),
            'train_scores_mean': train_scores.mean(axis=1).tolist(),
            'train_scores_std': train_scores.std(axis=1).tolist(),
            'val_scores_mean': val_scores.mean(axis=1).tolist(),
            'val_scores_std': val_scores.std(axis=1).tolist()
        }
        
        self.logger.info("Learning curve analysis completed")
        return learning_curve_data
    
    def comprehensive_evaluation(self, model: Any, X_test: pd.DataFrame, y_test: pd.Series,
                                X_train: pd.DataFrame = None, y_train: pd.Series = None,
                                perform_cv: bool = True) -> Dict[str, Any]:
        """
        Perform comprehensive model evaluation
        
        Args:
            model: Trained model to evaluate
            X_test: Test features
            y_test: Test target
            X_train: Training features (for cross-validation)
            y_train: Training target (for cross-validation)
            perform_cv: Whether to perform cross-validation
            
        Returns:
            Dictionary containing comprehensive evaluation results
        """
        self.logger.info("Starting comprehensive model evaluation...")
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        evaluation_results = {
            'model_type': type(model).__name__,
            'test_set_size': len(X_test),
            'class_distribution': y_test.value_counts().to_dict()
        }
        
        # Basic metrics
        evaluation_results['basic_metrics'] = self.calculate_basic_metrics(y_test, y_pred, y_pred_proba)
        
        # Confusion matrix metrics
        evaluation_results['confusion_matrix_metrics'] = self.calculate_confusion_matrix_metrics(y_test, y_pred)
        
        # Cost-sensitive metrics
        evaluation_results['cost_sensitive_metrics'] = self.calculate_cost_sensitive_metrics(y_test, y_pred)
        
        # Threshold analysis
        if y_pred_proba is not None:
            evaluation_results['threshold_analysis'] = self.threshold_analysis(y_test, y_pred_proba)
        
        # Cross-validation (if training data provided)
        if perform_cv and X_train is not None and y_train is not None:
            evaluation_results['cross_validation'] = self.cross_validation_evaluation(model, X_train, y_train)
            evaluation_results['learning_curve'] = self.learning_curve_analysis(model, X_train, y_train)
        
        # Classification report
        evaluation_results['classification_report'] = classification_report(y_test, y_pred, output_dict=True)
        
        self.evaluation_results = evaluation_results
        self.logger.info("Comprehensive evaluation completed")
        
        return evaluation_results
    
    def compare_models(self, models: Dict[str, Any], X_test: pd.DataFrame, y_test: pd.Series,
                      X_train: pd.DataFrame = None, y_train: pd.Series = None) -> Dict[str, Any]:
        """
        Compare multiple models
        
        Args:
            models: Dictionary of model name -> model object
            X_test: Test features
            y_test: Test target
            X_train: Training features
            y_train: Training target
            
        Returns:
            Dictionary containing model comparison results
        """
        self.logger.info(f"Comparing {len(models)} models...")
        
        comparison_results = {}
        
        for model_name, model in models.items():
            self.logger.info(f"Evaluating {model_name}...")
            
            try:
                model_results = self.comprehensive_evaluation(
                    model, X_test, y_test, X_train, y_train, perform_cv=False
                )
                comparison_results[model_name] = model_results
                
            except Exception as e:
                self.logger.error(f"Error evaluating {model_name}: {str(e)}")
                comparison_results[model_name] = {'error': str(e)}
        
        # Create comparison summary
        comparison_summary = self._create_comparison_summary(comparison_results)
        
        return {
            'individual_results': comparison_results,
            'comparison_summary': comparison_summary
        }
    
    def _create_comparison_summary(self, comparison_results: Dict[str, Any]) -> pd.DataFrame:
        """Create summary comparison table"""
        summary_data = []
        
        for model_name, results in comparison_results.items():
            if 'error' not in results:
                basic_metrics = results.get('basic_metrics', {})
                cost_metrics = results.get('cost_sensitive_metrics', {})
                
                summary_data.append({
                    'Model': model_name,
                    'Accuracy': basic_metrics.get('accuracy', 0),
                    'Precision': basic_metrics.get('precision', 0),
                    'Recall': basic_metrics.get('recall', 0),
                    'F1-Score': basic_metrics.get('f1_score', 0),
                    'ROC-AUC': basic_metrics.get('roc_auc', 0),
                    'Total Cost': cost_metrics.get('total_cost', 0),
                    'Cost per Prediction': cost_metrics.get('cost_per_prediction', 0)
                })
        
        return pd.DataFrame(summary_data)
    
    def plot_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray, 
                             model_name: str = "Model"):
        """Plot confusion matrix heatmap"""
        try:
            cm = confusion_matrix(y_true, y_pred)
            
            plt.figure(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                       xticklabels=['Normal', 'Fraud'], 
                       yticklabels=['Normal', 'Fraud'])
            plt.title(f'Confusion Matrix - {model_name}')
            plt.xlabel('Predicted')
            plt.ylabel('Actual')
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error plotting confusion matrix: {str(e)}")
    
    def plot_roc_curve(self, y_true: np.ndarray, y_pred_proba: np.ndarray, 
                      model_name: str = "Model"):
        """Plot ROC curve"""
        try:
            fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
            auc_score = roc_auc_score(y_true, y_pred_proba)
            
            plt.figure(figsize=(8, 6))
            plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc_score:.3f})')
            plt.plot([0, 1], [0, 1], 'k--', label='Random')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC Curve')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error plotting ROC curve: {str(e)}")
    
    def plot_precision_recall_curve(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                                   model_name: str = "Model"):
        """Plot Precision-Recall curve"""
        try:
            precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
            avg_precision = average_precision_score(y_true, y_pred_proba)
            
            plt.figure(figsize=(8, 6))
            plt.plot(recall, precision, label=f'{model_name} (AP = {avg_precision:.3f})')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title('Precision-Recall Curve')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error plotting Precision-Recall curve: {str(e)}")
    
    def plot_threshold_analysis(self):
        """Plot threshold analysis results"""
        if not self.threshold_analysis:
            self.logger.warning("No threshold analysis data available")
            return
        
        try:
            df = self.threshold_analysis['threshold_results']
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            # Precision, Recall, F1 vs Threshold
            axes[0, 0].plot(df['threshold'], df['precision'], label='Precision')
            axes[0, 0].plot(df['threshold'], df['recall'], label='Recall')
            axes[0, 0].plot(df['threshold'], df['f1_score'], label='F1-Score')
            axes[0, 0].set_xlabel('Threshold')
            axes[0, 0].set_ylabel('Score')
            axes[0, 0].set_title('Precision, Recall, F1 vs Threshold')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)
            
            # ROC-AUC vs Threshold
            axes[0, 1].plot(df['threshold'], df['roc_auc'], color='purple')
            axes[0, 1].set_xlabel('Threshold')
            axes[0, 1].set_ylabel('ROC-AUC')
            axes[0, 1].set_title('ROC-AUC vs Threshold')
            axes[0, 1].grid(True, alpha=0.3)
            
            # Cost vs Threshold
            axes[1, 0].plot(df['threshold'], df['total_cost'], color='red')
            axes[1, 0].set_xlabel('Threshold')
            axes[1, 0].set_ylabel('Total Cost')
            axes[1, 0].set_title('Total Cost vs Threshold')
            axes[1, 0].grid(True, alpha=0.3)
            
            # True/False Positive Rate vs Threshold
            axes[1, 1].plot(df['threshold'], df['true_positive_rate'], label='TPR (Recall)')
            axes[1, 1].plot(df['threshold'], df['false_positive_rate'], label='FPR')
            axes[1, 1].set_xlabel('Threshold')
            axes[1, 1].set_ylabel('Rate')
            axes[1, 1].set_title('TPR and FPR vs Threshold')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error plotting threshold analysis: {str(e)}")
    
    def generate_evaluation_report(self) -> str:
        """Generate text-based evaluation report"""
        if not self.evaluation_results:
            return "No evaluation results available. Run comprehensive_evaluation first."
        
        report = []
        report.append("=" * 60)
        report.append("FRAUD DETECTION MODEL EVALUATION REPORT")
        report.append("=" * 60)
        
        # Basic info
        report.append(f"Model Type: {self.evaluation_results['model_type']}")
        report.append(f"Test Set Size: {self.evaluation_results['test_set_size']}")
        report.append(f"Class Distribution: {self.evaluation_results['class_distribution']}")
        report.append("")
        
        # Basic metrics
        basic_metrics = self.evaluation_results['basic_metrics']
        report.append("BASIC METRICS:")
        report.append("-" * 20)
        for metric, value in basic_metrics.items():
            report.append(f"{metric.replace('_', ' ').title()}: {value:.4f}")
        report.append("")
        
        # Confusion matrix
        cm_metrics = self.evaluation_results['confusion_matrix_metrics']
        report.append("CONFUSION MATRIX:")
        report.append("-" * 20)
        report.append(f"True Negatives: {cm_metrics['tn']}")
        report.append(f"False Positives: {cm_metrics['fp']}")
        report.append(f"False Negatives: {cm_metrics['fn']}")
        report.append(f"True Positives: {cm_metrics['tp']}")
        report.append("")
        
        # Cost analysis
        cost_metrics = self.evaluation_results['cost_sensitive_metrics']
        report.append("COST ANALYSIS:")
        report.append("-" * 20)
        report.append(f"Total Cost: ${cost_metrics['total_cost']:.2f}")
        report.append(f"Cost per Prediction: ${cost_metrics['cost_per_prediction']:.2f}")
        report.append(f"Total Savings: ${cost_metrics['total_savings']:.2f}")
        report.append("")
        
        return "\n".join(report)
    
    def save_evaluation_results(self, filepath: str):
        """Save evaluation results to file"""
        import json
        
        # Convert numpy arrays to lists for JSON serialization
        save_data = {}
        for key, value in self.evaluation_results.items():
            if isinstance(value, dict):
                save_data[key] = {k: v.tolist() if isinstance(v, np.ndarray) else v 
                                for k, v in value.items()}
            else:
                save_data[key] = value.tolist() if isinstance(value, np.ndarray) else value
        
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2, default=str)
        
        self.logger.info(f"Evaluation results saved to {filepath}")


if __name__ == "__main__":
    # Example usage
    evaluator = ModelEvaluator()
    
    # For testing with sample data
    # results = evaluator.comprehensive_evaluation(model, X_test, y_test, X_train, y_train)
    # print(evaluator.generate_evaluation_report())
    print("ModelEvaluator module created successfully!")
