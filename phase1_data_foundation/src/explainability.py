"""
SHAP Explainability Module for Credit Card Fraud Detection
Advanced model interpretability and explanation generation
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional, Union
import shap
import lime
from lime import lime_tabular
from sklearn.inspection import permutation_importance, partial_dependence
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import warnings
warnings.filterwarnings('ignore')

class ModelExplainer:
    """
    Comprehensive model explainability using SHAP, LIME, and other XAI techniques
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Model Explainer
        
        Args:
            config: Configuration dictionary with explainability parameters
        """
        self.config = config or {}
        self.model = None
        self.explainer = None
        self.shap_values = None
        self.feature_names = None
        self.lime_explainer = None
        self.background_data = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def initialize_shap_explainer(self, model: Any, X_background: pd.DataFrame, 
                                 explainer_type: str = 'auto') -> shap.Explainer:
        """
        Initialize SHAP explainer based on model type
        
        Args:
            model: Trained model to explain
            X_background: Background data for SHAP explainer
            explainer_type: Type of SHAP explainer ('auto', 'tree', 'linear', 'kernel', 'deep')
            
        Returns:
            Initialized SHAP explainer
        """
        self.model = model
        self.background_data = X_background
        self.feature_names = X_background.columns.tolist()
        
        if explainer_type == 'auto':
            # Auto-detect explainer type based on model
            model_name = type(model).__name__.lower()
            
            if any(tree_model in model_name for tree_model in ['xgb', 'lgb', 'catboost', 'randomforest', 'extratrees']):
                explainer_type = 'tree'
            elif any(linear_model in model_name for linear_model in ['linear', 'logistic', 'ridge', 'lasso']):
                explainer_type = 'linear'
            else:
                explainer_type = 'kernel'
        
        self.logger.info(f"Initializing {explainer_type} SHAP explainer...")
        
        if explainer_type == 'tree':
            self.explainer = shap.TreeExplainer(model)
        elif explainer_type == 'linear':
            self.explainer = shap.LinearExplainer(model, X_background)
        elif explainer_type == 'kernel':
            self.explainer = shap.KernelExplainer(model.predict_proba, X_background.sample(min(100, len(X_background))))
        elif explainer_type == 'deep':
            self.explainer = shap.DeepExplainer(model, X_background.values)
        else:
            raise ValueError(f"Unknown explainer type: {explainer_type}")
        
        self.logger.info("SHAP explainer initialized successfully")
        return self.explainer
    
    def calculate_shap_values(self, X: pd.DataFrame, max_evals: int = 1000) -> np.ndarray:
        """
        Calculate SHAP values for given data
        
        Args:
            X: Data to explain
            max_evals: Maximum number of evaluations for kernel explainer
            
        Returns:
            SHAP values array
        """
        if self.explainer is None:
            raise ValueError("SHAP explainer not initialized. Call initialize_shap_explainer first.")
        
        self.logger.info(f"Calculating SHAP values for {len(X)} samples...")
        
        # Handle different explainer types
        if isinstance(self.explainer, shap.KernelExplainer):
            self.shap_values = self.explainer.shap_values(X, nsamples=max_evals)
            # For binary classification, take positive class SHAP values
            if isinstance(self.shap_values, list):
                self.shap_values = self.shap_values[1]
        else:
            self.shap_values = self.explainer.shap_values(X)
            # For binary classification, take positive class SHAP values
            if isinstance(self.shap_values, list):
                self.shap_values = self.shap_values[1]
        
        self.logger.info("SHAP values calculated successfully")
        return self.shap_values
    
    def get_global_feature_importance(self, shap_values: np.ndarray = None) -> Dict[str, float]:
        """
        Get global feature importance from SHAP values
        
        Args:
            shap_values: SHAP values array
            
        Returns:
            Dictionary of feature importance scores
        """
        if shap_values is None:
            shap_values = self.shap_values
        
        if shap_values is None:
            raise ValueError("SHAP values not available. Call calculate_shap_values first.")
        
        # Calculate mean absolute SHAP values
        importance_scores = np.abs(shap_values).mean(axis=0)
        
        # Create feature importance dictionary
        feature_importance = dict(zip(self.feature_names, importance_scores))
        
        # Sort by importance
        feature_importance = dict(sorted(feature_importance.items(), 
                                       key=lambda x: x[1], reverse=True))
        
        self.logger.info(f"Global feature importance calculated for {len(feature_importance)} features")
        return feature_importance
    
    def get_local_explanation(self, X_instance: pd.DataFrame, 
                            instance_idx: int = 0) -> Dict[str, Any]:
        """
        Get local explanation for a specific instance
        
        Args:
            X_instance: Instance data
            instance_idx: Index of instance to explain
            
        Returns:
            Dictionary containing local explanation
        """
        if self.shap_values is None:
            self.calculate_shap_values(X_instance)
        
        instance_shap_values = self.shap_values[instance_idx]
        instance_features = X_instance.iloc[instance_idx]
        
        # Create explanation dictionary
        local_explanation = {
            'feature_values': instance_features.to_dict(),
            'shap_values': dict(zip(self.feature_names, instance_shap_values)),
            'base_value': self.explainer.expected_value if hasattr(self.explainer, 'expected_value') else 0,
            'prediction': self.model.predict_proba([instance_features])[0][1] if hasattr(self.model, 'predict_proba') else None
        }
        
        # Sort features by absolute SHAP value
        sorted_features = sorted(local_explanation['shap_values'].items(), 
                               key=lambda x: abs(x[1]), reverse=True)
        local_explanation['top_features'] = dict(sorted_features[:10])
        
        return local_explanation
    
    def initialize_lime_explainer(self, X_train: pd.DataFrame, mode: str = 'classification'):
        """
        Initialize LIME explainer
        
        Args:
            X_train: Training data for LIME
            mode: LIME mode ('classification' or 'regression')
        """
        self.lime_explainer = lime_tabular.LimeTabularExplainer(
            X_train.values,
            feature_names=X_train.columns,
            class_names=['Normal', 'Fraud'] if mode == 'classification' else None,
            mode=mode,
            discretize_continuous=True
        )
        
        self.logger.info("LIME explainer initialized successfully")
    
    def get_lime_explanation(self, X_instance: pd.DataFrame, 
                           instance_idx: int = 0, 
                           num_features: int = 10) -> Dict[str, Any]:
        """
        Get LIME explanation for a specific instance
        
        Args:
            X_instance: Instance data
            instance_idx: Index of instance to explain
            num_features: Number of features to include in explanation
            
        Returns:
            Dictionary containing LIME explanation
        """
        if self.lime_explainer is None:
            raise ValueError("LIME explainer not initialized. Call initialize_lime_explainer first.")
        
        instance = X_instance.iloc[instance_idx].values
        
        # Generate LIME explanation
        explanation = self.lime_explainer.explain_instance(
            instance, 
            self.model.predict_proba,
            num_features=num_features
        )
        
        # Extract explanation data
        lime_explanation = {
            'feature_importance': dict(explanation.as_list()),
            'intercept': explanation.intercept[1] if hasattr(explanation, 'intercept') else 0,
            'prediction_proba': explanation.predict_proba[1] if hasattr(explanation, 'predict_proba') else None,
            'score': explanation.score if hasattr(explanation, 'score') else None
        }
        
        return lime_explanation
    
    def calculate_permutation_importance(self, X: pd.DataFrame, y: pd.Series, 
                                       n_repeats: int = 10, 
                                       random_state: int = 42) -> Dict[str, float]:
        """
        Calculate permutation feature importance
        
        Args:
            X: Feature data
            y: Target data
            n_repeats: Number of permutation repeats
            random_state: Random state for reproducibility
            
        Returns:
            Dictionary of permutation importance scores
        """
        self.logger.info("Calculating permutation importance...")
        
        perm_importance = permutation_importance(
            self.model, X, y, 
            n_repeats=n_repeats, 
            random_state=random_state,
            scoring='roc_auc'
        )
        
        # Create importance dictionary
        importance_dict = dict(zip(X.columns, perm_importance.importances_mean))
        importance_dict = dict(sorted(importance_dict.items(), 
                                    key=lambda x: x[1], reverse=True))
        
        self.logger.info("Permutation importance calculated successfully")
        return importance_dict
    
    def generate_partial_dependence_plots(self, X: pd.DataFrame, 
                                        features: List[str] = None,
                                        n_cols: int = 3) -> Dict[str, Any]:
        """
        Generate partial dependence plots for selected features
        
        Args:
            X: Feature data
            features: List of features to plot (if None, use top features)
            n_cols: Number of columns in plot grid
            
        Returns:
            Dictionary containing PDP data
        """
        if features is None:
            # Use top 6 features from SHAP importance
            if self.shap_values is not None:
                feature_importance = self.get_global_feature_importance()
                features = list(feature_importance.keys())[:6]
            else:
                features = X.columns[:6].tolist()
        
        self.logger.info(f"Generating partial dependence plots for {len(features)} features...")
        
        pdp_data = {}
        
        try:
            # Calculate partial dependence
            for feature in features:
                if feature in X.columns:
                    pd_result = partial_dependence(
                        self.model, X, features=[feature], 
                        kind='average'
                    )
                    
                    pdp_data[feature] = {
                        'values': pd_result['values'][0],
                        'average': pd_result['average'][0]
                    }
            
            self.logger.info("Partial dependence plots data generated successfully")
            
        except Exception as e:
            self.logger.error(f"Error generating partial dependence plots: {str(e)}")
        
        return pdp_data
    
    def create_shap_summary_plot(self, X: pd.DataFrame = None, 
                               shap_values: np.ndarray = None,
                               max_display: int = 20,
                               plot_type: str = 'dot'):
        """
        Create SHAP summary plot
        
        Args:
            X: Feature data
            shap_values: SHAP values
            max_display: Maximum number of features to display
            plot_type: Type of plot ('dot', 'bar', 'violin')
        """
        if shap_values is None:
            shap_values = self.shap_values
        
        if X is None:
            X = self.background_data
        
        if shap_values is None or X is None:
            self.logger.warning("SHAP values or data not available for plotting")
            return
        
        try:
            plt.figure(figsize=(10, 8))
            
            if plot_type == 'dot':
                shap.summary_plot(shap_values, X, max_display=max_display, show=False)
            elif plot_type == 'bar':
                shap.summary_plot(shap_values, X, plot_type="bar", 
                                max_display=max_display, show=False)
            elif plot_type == 'violin':
                shap.summary_plot(shap_values, X, plot_type="violin", 
                                max_display=max_display, show=False)
            
            plt.title(f'SHAP Summary Plot ({plot_type.title()})')
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error creating SHAP summary plot: {str(e)}")
    
    def create_shap_waterfall_plot(self, X_instance: pd.DataFrame, 
                                  instance_idx: int = 0):
        """
        Create SHAP waterfall plot for a specific instance
        
        Args:
            X_instance: Instance data
            instance_idx: Index of instance to explain
        """
        if self.shap_values is None:
            self.calculate_shap_values(X_instance)
        
        try:
            # Create explanation object for waterfall plot
            explanation = shap.Explanation(
                values=self.shap_values[instance_idx],
                base_values=self.explainer.expected_value if hasattr(self.explainer, 'expected_value') else 0,
                data=X_instance.iloc[instance_idx].values,
                feature_names=self.feature_names
            )
            
            plt.figure(figsize=(10, 8))
            shap.waterfall_plot(explanation, show=False)
            plt.title(f'SHAP Waterfall Plot - Instance {instance_idx}')
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error creating SHAP waterfall plot: {str(e)}")
    
    def create_feature_importance_comparison(self, X: pd.DataFrame, y: pd.Series,
                                           methods: List[str] = None) -> Dict[str, Dict[str, float]]:
        """
        Compare feature importance across different methods
        
        Args:
            X: Feature data
            y: Target data
            methods: List of methods to compare
            
        Returns:
            Dictionary containing importance scores from different methods
        """
        if methods is None:
            methods = ['shap', 'permutation']
        
        importance_comparison = {}
        
        # SHAP importance
        if 'shap' in methods and self.shap_values is not None:
            importance_comparison['shap'] = self.get_global_feature_importance()
        
        # Permutation importance
        if 'permutation' in methods:
            importance_comparison['permutation'] = self.calculate_permutation_importance(X, y)
        
        # Tree-based importance (if applicable)
        if 'tree' in methods and hasattr(self.model, 'feature_importances_'):
            tree_importance = dict(zip(X.columns, self.model.feature_importances_))
            importance_comparison['tree'] = dict(sorted(tree_importance.items(), 
                                                      key=lambda x: x[1], reverse=True))
        
        return importance_comparison
    
    def generate_explanation_report(self, X: pd.DataFrame, y: pd.Series = None,
                                  sample_instances: List[int] = None) -> Dict[str, Any]:
        """
        Generate comprehensive explanation report
        
        Args:
            X: Feature data
            y: Target data (optional)
            sample_instances: List of instance indices to explain in detail
            
        Returns:
            Dictionary containing comprehensive explanation report
        """
        self.logger.info("Generating comprehensive explanation report...")
        
        report = {
            'model_type': type(self.model).__name__,
            'num_features': len(self.feature_names),
            'num_instances': len(X)
        }
        
        # Calculate SHAP values if not already done
        if self.shap_values is None:
            self.calculate_shap_values(X)
        
        # Global feature importance
        report['global_feature_importance'] = self.get_global_feature_importance()
        
        # Feature importance comparison
        if y is not None:
            report['importance_comparison'] = self.create_feature_importance_comparison(X, y)
        
        # Local explanations for sample instances
        if sample_instances is None:
            sample_instances = [0, len(X)//2, len(X)-1] if len(X) > 2 else [0]
        
        report['local_explanations'] = {}
        for idx in sample_instances:
            if idx < len(X):
                report['local_explanations'][f'instance_{idx}'] = self.get_local_explanation(X, idx)
        
        # Summary statistics
        report['shap_statistics'] = {
            'mean_abs_shap': np.abs(self.shap_values).mean(),
            'std_abs_shap': np.abs(self.shap_values).std(),
            'max_abs_shap': np.abs(self.shap_values).max(),
            'min_abs_shap': np.abs(self.shap_values).min()
        }
        
        self.logger.info("Explanation report generated successfully")
        return report
    
    def save_explanations(self, filepath: str, explanation_data: Dict[str, Any]):
        """
        Save explanation data to file
        
        Args:
            filepath: Path to save explanations
            explanation_data: Explanation data to save
        """
        import json
        import joblib
        
        # Prepare data for saving (convert numpy arrays to lists)
        save_data = {}
        for key, value in explanation_data.items():
            if isinstance(value, np.ndarray):
                save_data[key] = value.tolist()
            elif isinstance(value, dict):
                save_data[key] = {k: v.tolist() if isinstance(v, np.ndarray) else v 
                                for k, v in value.items()}
            else:
                save_data[key] = value
        
        # Save as JSON
        if filepath.endswith('.json'):
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2, default=str)
        else:
            # Save as pickle
            joblib.dump(save_data, filepath)
        
        self.logger.info(f"Explanations saved to {filepath}")


if __name__ == "__main__":
    # Example usage
    explainer = ModelExplainer()
    
    # For testing with sample data
    # explainer.initialize_shap_explainer(model, X_background)
    # shap_values = explainer.calculate_shap_values(X_test)
    # report = explainer.generate_explanation_report(X_test, y_test)
    print("ModelExplainer module created successfully!")
