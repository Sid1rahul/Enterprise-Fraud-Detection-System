"""
Advanced Oversampling Module for Credit Card Fraud Detection
ADASYN, SMOTE, and other oversampling techniques for handling class imbalance
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional, List
from imblearn.over_sampling import ADASYN, SMOTE, BorderlineSMOTE, SVMSMOTE
from imblearn.under_sampling import EditedNearestNeighbours, TomekLinks
from imblearn.combine import SMOTETomek, SMOTEENN
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import logging
import warnings
warnings.filterwarnings('ignore')

class AdvancedOversampler:
    """
    Advanced oversampling techniques for handling class imbalance in fraud detection
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Advanced Oversampler
        
        Args:
            config: Configuration dictionary with oversampling parameters
        """
        self.config = config or {}
        self.oversampler = None
        self.oversampling_method = None
        self.original_distribution = None
        self.resampled_distribution = None
        self.sampling_strategy = 'auto'
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def analyze_class_imbalance(self, y: pd.Series) -> Dict[str, Any]:
        """
        Analyze class imbalance in the dataset
        
        Args:
            y: Target variable
            
        Returns:
            Dictionary containing imbalance analysis
        """
        class_counts = y.value_counts().sort_index()
        total_samples = len(y)
        
        imbalance_analysis = {
            'class_counts': class_counts.to_dict(),
            'class_proportions': (class_counts / total_samples).to_dict(),
            'total_samples': total_samples,
            'minority_class': class_counts.idxmin(),
            'majority_class': class_counts.idxmax(),
            'imbalance_ratio': class_counts.max() / class_counts.min(),
            'minority_percentage': (class_counts.min() / total_samples) * 100
        }
        
        self.original_distribution = imbalance_analysis
        
        self.logger.info(f"Class Imbalance Analysis:")
        self.logger.info(f"Total samples: {total_samples}")
        self.logger.info(f"Class distribution: {imbalance_analysis['class_counts']}")
        self.logger.info(f"Imbalance ratio: {imbalance_analysis['imbalance_ratio']:.2f}")
        self.logger.info(f"Minority class percentage: {imbalance_analysis['minority_percentage']:.2f}%")
        
        return imbalance_analysis
    
    def adasyn_oversampling(self, X: pd.DataFrame, y: pd.Series, 
                           sampling_strategy: str = 'auto', 
                           n_neighbors: int = 5, 
                           random_state: int = 42) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Apply ADASYN (Adaptive Synthetic Sampling) oversampling
        
        Args:
            X: Feature matrix
            y: Target variable
            sampling_strategy: Sampling strategy
            n_neighbors: Number of nearest neighbors
            random_state: Random state for reproducibility
            
        Returns:
            Tuple of (resampled_X, resampled_y)
        """
        self.logger.info("Applying ADASYN oversampling...")
        
        # Initialize ADASYN
        adasyn = ADASYN(
            sampling_strategy=sampling_strategy,
            n_neighbors=n_neighbors,
            random_state=random_state
        )
        
        # Apply oversampling
        X_resampled, y_resampled = adasyn.fit_resample(X, y)
        
        # Convert back to pandas
        X_resampled_df = pd.DataFrame(X_resampled, columns=X.columns)
        y_resampled_series = pd.Series(y_resampled, name=y.name)
        
        self.oversampler = adasyn
        self.oversampling_method = 'ADASYN'
        self.sampling_strategy = sampling_strategy
        
        # Analyze new distribution
        self.resampled_distribution = self.analyze_resampled_distribution(y_resampled_series)
        
        self.logger.info(f"ADASYN completed. New shape: {X_resampled_df.shape}")
        return X_resampled_df, y_resampled_series
    
    def smote_oversampling(self, X: pd.DataFrame, y: pd.Series,
                          variant: str = 'standard',
                          sampling_strategy: str = 'auto',
                          k_neighbors: int = 5,
                          random_state: int = 42) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Apply SMOTE (Synthetic Minority Oversampling Technique) variants
        
        Args:
            X: Feature matrix
            y: Target variable
            variant: SMOTE variant ('standard', 'borderline', 'svm')
            sampling_strategy: Sampling strategy
            k_neighbors: Number of nearest neighbors
            random_state: Random state for reproducibility
            
        Returns:
            Tuple of (resampled_X, resampled_y)
        """
        self.logger.info(f"Applying {variant} SMOTE oversampling...")
        
        # Select SMOTE variant
        if variant == 'standard':
            smote = SMOTE(
                sampling_strategy=sampling_strategy,
                k_neighbors=k_neighbors,
                random_state=random_state
            )
        elif variant == 'borderline':
            smote = BorderlineSMOTE(
                sampling_strategy=sampling_strategy,
                k_neighbors=k_neighbors,
                random_state=random_state
            )
        elif variant == 'svm':
            smote = SVMSMOTE(
                sampling_strategy=sampling_strategy,
                k_neighbors=k_neighbors,
                random_state=random_state
            )
        else:
            raise ValueError(f"Unknown SMOTE variant: {variant}")
        
        # Apply oversampling
        X_resampled, y_resampled = smote.fit_resample(X, y)
        
        # Convert back to pandas
        X_resampled_df = pd.DataFrame(X_resampled, columns=X.columns)
        y_resampled_series = pd.Series(y_resampled, name=y.name)
        
        self.oversampler = smote
        self.oversampling_method = f'{variant.upper()}_SMOTE'
        self.sampling_strategy = sampling_strategy
        
        # Analyze new distribution
        self.resampled_distribution = self.analyze_resampled_distribution(y_resampled_series)
        
        self.logger.info(f"{variant} SMOTE completed. New shape: {X_resampled_df.shape}")
        return X_resampled_df, y_resampled_series
    
    def hybrid_oversampling(self, X: pd.DataFrame, y: pd.Series,
                           method: str = 'smote_tomek',
                           sampling_strategy: str = 'auto',
                           random_state: int = 42) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Apply hybrid oversampling + undersampling techniques
        
        Args:
            X: Feature matrix
            y: Target variable
            method: Hybrid method ('smote_tomek', 'smote_enn')
            sampling_strategy: Sampling strategy
            random_state: Random state for reproducibility
            
        Returns:
            Tuple of (resampled_X, resampled_y)
        """
        self.logger.info(f"Applying {method} hybrid sampling...")
        
        # Select hybrid method
        if method == 'smote_tomek':
            hybrid_sampler = SMOTETomek(
                sampling_strategy=sampling_strategy,
                random_state=random_state
            )
        elif method == 'smote_enn':
            hybrid_sampler = SMOTEENN(
                sampling_strategy=sampling_strategy,
                random_state=random_state
            )
        else:
            raise ValueError(f"Unknown hybrid method: {method}")
        
        # Apply hybrid sampling
        X_resampled, y_resampled = hybrid_sampler.fit_resample(X, y)
        
        # Convert back to pandas
        X_resampled_df = pd.DataFrame(X_resampled, columns=X.columns)
        y_resampled_series = pd.Series(y_resampled, name=y.name)
        
        self.oversampler = hybrid_sampler
        self.oversampling_method = method.upper()
        self.sampling_strategy = sampling_strategy
        
        # Analyze new distribution
        self.resampled_distribution = self.analyze_resampled_distribution(y_resampled_series)
        
        self.logger.info(f"{method} completed. New shape: {X_resampled_df.shape}")
        return X_resampled_df, y_resampled_series
    
    def analyze_resampled_distribution(self, y_resampled: pd.Series) -> Dict[str, Any]:
        """
        Analyze the distribution after resampling
        
        Args:
            y_resampled: Resampled target variable
            
        Returns:
            Dictionary containing resampled distribution analysis
        """
        class_counts = y_resampled.value_counts().sort_index()
        total_samples = len(y_resampled)
        
        resampled_analysis = {
            'class_counts': class_counts.to_dict(),
            'class_proportions': (class_counts / total_samples).to_dict(),
            'total_samples': total_samples,
            'balance_achieved': abs(class_counts.max() - class_counts.min()) / class_counts.max() < 0.1
        }
        
        self.logger.info(f"Resampled Distribution:")
        self.logger.info(f"New class distribution: {resampled_analysis['class_counts']}")
        self.logger.info(f"Balance achieved: {resampled_analysis['balance_achieved']}")
        
        return resampled_analysis
    
    def compare_sampling_methods(self, X: pd.DataFrame, y: pd.Series,
                                methods: List[str] = None,
                                cv_folds: int = 5,
                                random_state: int = 42) -> Dict[str, Dict[str, float]]:
        """
        Compare different sampling methods using cross-validation
        
        Args:
            X: Feature matrix
            y: Target variable
            methods: List of methods to compare
            cv_folds: Number of cross-validation folds
            random_state: Random state for reproducibility
            
        Returns:
            Dictionary containing comparison results
        """
        if methods is None:
            methods = ['adasyn', 'smote', 'borderline_smote', 'smote_tomek']
        
        self.logger.info(f"Comparing {len(methods)} sampling methods...")
        
        # Base classifier for evaluation
        base_classifier = RandomForestClassifier(n_estimators=100, random_state=random_state)
        
        comparison_results = {}
        
        # Evaluate original data (no sampling)
        original_scores = cross_val_score(base_classifier, X, y, cv=cv_folds, scoring='f1')
        comparison_results['original'] = {
            'f1_mean': original_scores.mean(),
            'f1_std': original_scores.std(),
            'method': 'No Sampling'
        }
        
        # Evaluate each sampling method
        for method in methods:
            try:
                if method == 'adasyn':
                    X_resampled, y_resampled = self.adasyn_oversampling(X, y, random_state=random_state)
                elif method == 'smote':
                    X_resampled, y_resampled = self.smote_oversampling(X, y, variant='standard', random_state=random_state)
                elif method == 'borderline_smote':
                    X_resampled, y_resampled = self.smote_oversampling(X, y, variant='borderline', random_state=random_state)
                elif method == 'svm_smote':
                    X_resampled, y_resampled = self.smote_oversampling(X, y, variant='svm', random_state=random_state)
                elif method == 'smote_tomek':
                    X_resampled, y_resampled = self.hybrid_oversampling(X, y, method='smote_tomek', random_state=random_state)
                elif method == 'smote_enn':
                    X_resampled, y_resampled = self.hybrid_oversampling(X, y, method='smote_enn', random_state=random_state)
                else:
                    self.logger.warning(f"Unknown method: {method}. Skipping.")
                    continue
                
                # Evaluate resampled data
                scores = cross_val_score(base_classifier, X_resampled, y_resampled, cv=cv_folds, scoring='f1')
                comparison_results[method] = {
                    'f1_mean': scores.mean(),
                    'f1_std': scores.std(),
                    'method': method.upper().replace('_', ' ')
                }
                
            except Exception as e:
                self.logger.error(f"Error with method {method}: {str(e)}")
                comparison_results[method] = {
                    'f1_mean': 0.0,
                    'f1_std': 0.0,
                    'method': method.upper().replace('_', ' '),
                    'error': str(e)
                }
        
        # Find best method
        best_method = max(comparison_results.keys(), 
                         key=lambda x: comparison_results[x]['f1_mean'])
        
        self.logger.info(f"Method comparison completed. Best method: {best_method}")
        self.logger.info(f"Best F1 score: {comparison_results[best_method]['f1_mean']:.4f}")
        
        return comparison_results
    
    def optimize_sampling_parameters(self, X: pd.DataFrame, y: pd.Series,
                                   method: str = 'adasyn',
                                   cv_folds: int = 5) -> Dict[str, Any]:
        """
        Optimize parameters for the selected sampling method
        
        Args:
            X: Feature matrix
            y: Target variable
            method: Sampling method to optimize
            cv_folds: Number of cross-validation folds
            
        Returns:
            Dictionary containing optimal parameters
        """
        self.logger.info(f"Optimizing parameters for {method}...")
        
        base_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        best_score = 0
        best_params = {}
        
        if method == 'adasyn':
            # Parameter grid for ADASYN
            param_combinations = [
                {'n_neighbors': n, 'sampling_strategy': s}
                for n in [3, 5, 7, 10]
                for s in ['auto', 0.5, 0.8, 1.0]
            ]
            
            for params in param_combinations:
                try:
                    X_resampled, y_resampled = self.adasyn_oversampling(
                        X, y, 
                        sampling_strategy=params['sampling_strategy'],
                        n_neighbors=params['n_neighbors']
                    )
                    
                    scores = cross_val_score(base_classifier, X_resampled, y_resampled, 
                                           cv=cv_folds, scoring='f1')
                    mean_score = scores.mean()
                    
                    if mean_score > best_score:
                        best_score = mean_score
                        best_params = params
                        
                except Exception as e:
                    self.logger.warning(f"Error with params {params}: {str(e)}")
                    continue
        
        elif method == 'smote':
            # Parameter grid for SMOTE
            param_combinations = [
                {'k_neighbors': k, 'sampling_strategy': s}
                for k in [3, 5, 7, 10]
                for s in ['auto', 0.5, 0.8, 1.0]
            ]
            
            for params in param_combinations:
                try:
                    X_resampled, y_resampled = self.smote_oversampling(
                        X, y,
                        variant='standard',
                        sampling_strategy=params['sampling_strategy'],
                        k_neighbors=params['k_neighbors']
                    )
                    
                    scores = cross_val_score(base_classifier, X_resampled, y_resampled,
                                           cv=cv_folds, scoring='f1')
                    mean_score = scores.mean()
                    
                    if mean_score > best_score:
                        best_score = mean_score
                        best_params = params
                        
                except Exception as e:
                    self.logger.warning(f"Error with params {params}: {str(e)}")
                    continue
        
        best_params['best_f1_score'] = best_score
        self.logger.info(f"Parameter optimization completed. Best score: {best_score:.4f}")
        self.logger.info(f"Best parameters: {best_params}")
        
        return best_params
    
    def apply_best_sampling(self, X: pd.DataFrame, y: pd.Series,
                           auto_optimize: bool = True) -> Tuple[pd.DataFrame, pd.Series, Dict[str, Any]]:
        """
        Apply the best sampling method automatically
        
        Args:
            X: Feature matrix
            y: Target variable
            auto_optimize: Whether to automatically find the best method
            
        Returns:
            Tuple of (resampled_X, resampled_y, sampling_report)
        """
        self.logger.info("Applying best sampling method...")
        
        # Analyze original imbalance
        imbalance_analysis = self.analyze_class_imbalance(y)
        
        sampling_report = {
            'original_analysis': imbalance_analysis,
            'method_used': None,
            'parameters_used': None,
            'performance_improvement': None
        }
        
        if auto_optimize:
            # Compare methods and select best
            comparison_results = self.compare_sampling_methods(X, y)
            
            # Find best method (excluding original)
            methods_only = {k: v for k, v in comparison_results.items() if k != 'original'}
            best_method = max(methods_only.keys(), key=lambda x: methods_only[x]['f1_mean'])
            
            sampling_report['comparison_results'] = comparison_results
            sampling_report['method_used'] = best_method
            
            # Optimize parameters for best method
            if best_method in ['adasyn', 'smote']:
                best_params = self.optimize_sampling_parameters(X, y, method=best_method)
                sampling_report['parameters_used'] = best_params
            
            # Apply best method with optimal parameters
            if best_method == 'adasyn':
                params = sampling_report.get('parameters_used', {})
                X_resampled, y_resampled = self.adasyn_oversampling(
                    X, y,
                    sampling_strategy=params.get('sampling_strategy', 'auto'),
                    n_neighbors=params.get('n_neighbors', 5)
                )
            elif best_method == 'smote':
                params = sampling_report.get('parameters_used', {})
                X_resampled, y_resampled = self.smote_oversampling(
                    X, y,
                    variant='standard',
                    sampling_strategy=params.get('sampling_strategy', 'auto'),
                    k_neighbors=params.get('k_neighbors', 5)
                )
            elif best_method == 'borderline_smote':
                X_resampled, y_resampled = self.smote_oversampling(X, y, variant='borderline')
            elif best_method == 'smote_tomek':
                X_resampled, y_resampled = self.hybrid_oversampling(X, y, method='smote_tomek')
            else:
                # Fallback to ADASYN
                X_resampled, y_resampled = self.adasyn_oversampling(X, y)
            
            # Calculate performance improvement
            original_f1 = comparison_results['original']['f1_mean']
            best_f1 = comparison_results[best_method]['f1_mean']
            improvement = ((best_f1 - original_f1) / original_f1) * 100
            sampling_report['performance_improvement'] = improvement
            
        else:
            # Use ADASYN as default
            X_resampled, y_resampled = self.adasyn_oversampling(X, y)
            sampling_report['method_used'] = 'adasyn'
        
        sampling_report['final_distribution'] = self.resampled_distribution
        
        self.logger.info(f"Best sampling completed using {sampling_report['method_used']}")
        return X_resampled, y_resampled, sampling_report
    
    def get_sampling_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive sampling report
        
        Returns:
            Dictionary containing sampling information
        """
        report = {
            'oversampling_method': self.oversampling_method,
            'sampling_strategy': self.sampling_strategy,
            'original_distribution': self.original_distribution,
            'resampled_distribution': self.resampled_distribution,
            'oversampler_params': getattr(self.oversampler, 'get_params', lambda: {})()
        }
        
        return report
    
    def visualize_class_distribution(self, y_original: pd.Series, y_resampled: pd.Series = None):
        """
        Visualize class distribution before and after sampling
        
        Args:
            y_original: Original target variable
            y_resampled: Resampled target variable
        """
        try:
            import matplotlib.pyplot as plt
            
            if y_resampled is not None:
                fig, axes = plt.subplots(1, 2, figsize=(15, 5))
                
                # Original distribution
                y_original.value_counts().plot(kind='bar', ax=axes[0], color=['blue', 'red'])
                axes[0].set_title('Original Class Distribution')
                axes[0].set_xlabel('Class')
                axes[0].set_ylabel('Count')
                axes[0].tick_params(axis='x', rotation=0)
                
                # Resampled distribution
                y_resampled.value_counts().plot(kind='bar', ax=axes[1], color=['blue', 'red'])
                axes[1].set_title(f'After {self.oversampling_method} Sampling')
                axes[1].set_xlabel('Class')
                axes[1].set_ylabel('Count')
                axes[1].tick_params(axis='x', rotation=0)
                
            else:
                fig, ax = plt.subplots(1, 1, figsize=(8, 5))
                y_original.value_counts().plot(kind='bar', ax=ax, color=['blue', 'red'])
                ax.set_title('Class Distribution')
                ax.set_xlabel('Class')
                ax.set_ylabel('Count')
                ax.tick_params(axis='x', rotation=0)
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            self.logger.warning("Matplotlib not available. Cannot visualize class distribution.")


if __name__ == "__main__":
    # Example usage
    oversampler = AdvancedOversampler()
    
    # For testing with sample data
    # X_resampled, y_resampled, report = oversampler.apply_best_sampling(X_train, y_train)
    print("AdvancedOversampler module created successfully!")
