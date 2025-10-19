"""
Feature Engineering Pipeline for Credit Card Fraud Detection
Advanced feature creation, selection, and transformation
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import PolynomialFeatures
from datetime import datetime, timedelta
import logging
import warnings
warnings.filterwarnings('ignore')

class FeatureEngineer:
    """
    Advanced feature engineering pipeline for credit card fraud detection
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize FeatureEngineer with configuration
        
        Args:
            config: Configuration dictionary with feature engineering parameters
        """
        self.config = config or {}
        self.feature_selectors = {}
        self.created_features = []
        self.feature_importance = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def create_temporal_features(self, df: pd.DataFrame, timestamp_col: str = 'Time') -> pd.DataFrame:
        """
        Create temporal features from timestamp column
        
        Args:
            df: Input DataFrame
            timestamp_col: Name of timestamp column
            
        Returns:
            DataFrame with temporal features added
        """
        df_processed = df.copy()
        
        if timestamp_col not in df_processed.columns:
            self.logger.warning(f"Timestamp column '{timestamp_col}' not found. Skipping temporal features.")
            return df_processed
        
        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(df_processed[timestamp_col]):
            # Assume Time column contains seconds since first transaction
            df_processed[timestamp_col] = pd.to_datetime(df_processed[timestamp_col], unit='s')
        
        # Extract temporal features
        df_processed['hour'] = df_processed[timestamp_col].dt.hour
        df_processed['day_of_week'] = df_processed[timestamp_col].dt.dayofweek
        df_processed['day_of_month'] = df_processed[timestamp_col].dt.day
        df_processed['month'] = df_processed[timestamp_col].dt.month
        df_processed['quarter'] = df_processed[timestamp_col].dt.quarter
        df_processed['is_weekend'] = (df_processed['day_of_week'] >= 5).astype(int)
        
        # Business hours indicator (9 AM to 5 PM)
        df_processed['is_business_hours'] = ((df_processed['hour'] >= 9) & (df_processed['hour'] <= 17)).astype(int)
        
        # Night time indicator (10 PM to 6 AM)
        df_processed['is_night_time'] = ((df_processed['hour'] >= 22) | (df_processed['hour'] <= 6)).astype(int)
        
        temporal_features = ['hour', 'day_of_week', 'day_of_month', 'month', 'quarter', 
                           'is_weekend', 'is_business_hours', 'is_night_time']
        self.created_features.extend(temporal_features)
        
        self.logger.info(f"Created {len(temporal_features)} temporal features")
        return df_processed
    
    def create_amount_features(self, df: pd.DataFrame, amount_col: str = 'Amount') -> pd.DataFrame:
        """
        Create amount-based features
        
        Args:
            df: Input DataFrame
            amount_col: Name of amount column
            
        Returns:
            DataFrame with amount features added
        """
        df_processed = df.copy()
        
        if amount_col not in df_processed.columns:
            self.logger.warning(f"Amount column '{amount_col}' not found. Skipping amount features.")
            return df_processed
        
        # Log transformation (handle zero values)
        df_processed['amount_log'] = np.log1p(df_processed[amount_col])
        
        # Square root transformation
        df_processed['amount_sqrt'] = np.sqrt(df_processed[amount_col])
        
        # Amount categories
        amount_percentiles = df_processed[amount_col].quantile([0.25, 0.5, 0.75, 0.9, 0.95])
        df_processed['amount_category'] = pd.cut(
            df_processed[amount_col], 
            bins=[-np.inf, amount_percentiles[0.25], amount_percentiles[0.5], 
                  amount_percentiles[0.75], amount_percentiles[0.9], 
                  amount_percentiles[0.95], np.inf],
            labels=['very_low', 'low', 'medium', 'high', 'very_high', 'extreme']
        )
        
        # Convert category to numerical
        df_processed['amount_category_num'] = df_processed['amount_category'].cat.codes
        
        # Amount deviation from mean
        mean_amount = df_processed[amount_col].mean()
        std_amount = df_processed[amount_col].std()
        df_processed['amount_deviation'] = (df_processed[amount_col] - mean_amount) / std_amount
        
        # Amount percentile rank
        df_processed['amount_percentile'] = df_processed[amount_col].rank(pct=True)
        
        amount_features = ['amount_log', 'amount_sqrt', 'amount_category_num', 
                          'amount_deviation', 'amount_percentile']
        self.created_features.extend(amount_features)
        
        self.logger.info(f"Created {len(amount_features)} amount-based features")
        return df_processed
    
    def create_behavioral_features(self, df: pd.DataFrame, customer_col: str = None) -> pd.DataFrame:
        """
        Create behavioral features based on customer transaction patterns
        
        Args:
            df: Input DataFrame
            customer_col: Name of customer identifier column
            
        Returns:
            DataFrame with behavioral features added
        """
        df_processed = df.copy()
        
        if customer_col and customer_col in df_processed.columns:
            # Customer-based features
            customer_stats = df_processed.groupby(customer_col).agg({
                'Amount': ['count', 'mean', 'std', 'min', 'max', 'sum'],
                'Time': ['min', 'max']
            }).reset_index()
            
            # Flatten column names
            customer_stats.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] 
                                    for col in customer_stats.columns]
            
            # Merge back to original dataframe
            df_processed = df_processed.merge(customer_stats, on=customer_col, how='left')
            
            self.logger.info("Created customer-based behavioral features")
        
        # Global behavioral features (without customer ID)
        # Transaction frequency by hour
        hourly_freq = df_processed.groupby('hour').size() if 'hour' in df_processed.columns else None
        if hourly_freq is not None:
            df_processed['hourly_transaction_freq'] = df_processed['hour'].map(hourly_freq)
        
        # Rolling statistics (if data is sorted by time)
        if 'Time' in df_processed.columns:
            df_processed = df_processed.sort_values('Time')
            
            # Rolling mean and std for amount (window of 10 transactions)
            df_processed['amount_rolling_mean_10'] = df_processed['Amount'].rolling(window=10, min_periods=1).mean()
            df_processed['amount_rolling_std_10'] = df_processed['Amount'].rolling(window=10, min_periods=1).std()
            
            # Rolling mean and std for amount (window of 50 transactions)
            df_processed['amount_rolling_mean_50'] = df_processed['Amount'].rolling(window=50, min_periods=1).mean()
            df_processed['amount_rolling_std_50'] = df_processed['Amount'].rolling(window=50, min_periods=1).std()
            
            # Time since last transaction
            df_processed['time_since_last'] = df_processed['Time'].diff()
            df_processed['time_since_last'].fillna(0, inplace=True)
            
            behavioral_features = ['hourly_transaction_freq', 'amount_rolling_mean_10', 
                                 'amount_rolling_std_10', 'amount_rolling_mean_50', 
                                 'amount_rolling_std_50', 'time_since_last']
            self.created_features.extend(behavioral_features)
            
            self.logger.info(f"Created {len(behavioral_features)} behavioral features")
        
        return df_processed
    
    def create_statistical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create statistical features from existing numerical columns
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with statistical features added
        """
        df_processed = df.copy()
        numerical_cols = df_processed.select_dtypes(include=[np.number]).columns
        
        # Remove target column if present
        if 'Class' in numerical_cols:
            numerical_cols = numerical_cols.drop('Class')
        
        # Create interaction features for top correlated pairs
        if len(numerical_cols) >= 2:
            # Calculate correlations
            corr_matrix = df_processed[numerical_cols].corr().abs()
            
            # Find top correlated pairs
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_pairs.append((
                        corr_matrix.columns[i], 
                        corr_matrix.columns[j], 
                        corr_matrix.iloc[i, j]
                    ))
            
            # Sort by correlation and take top 5 pairs
            corr_pairs.sort(key=lambda x: x[2], reverse=True)
            top_pairs = corr_pairs[:5]
            
            # Create interaction features
            interaction_features = []
            for col1, col2, corr_val in top_pairs:
                if corr_val > 0.1:  # Only create if correlation is meaningful
                    # Multiplication
                    feature_name = f"{col1}_x_{col2}"
                    df_processed[feature_name] = df_processed[col1] * df_processed[col2]
                    interaction_features.append(feature_name)
                    
                    # Division (avoid division by zero)
                    if (df_processed[col2] != 0).all():
                        feature_name = f"{col1}_div_{col2}"
                        df_processed[feature_name] = df_processed[col1] / df_processed[col2]
                        interaction_features.append(feature_name)
            
            self.created_features.extend(interaction_features)
            self.logger.info(f"Created {len(interaction_features)} interaction features")
        
        # Create polynomial features for selected columns (degree 2)
        if 'Amount' in df_processed.columns:
            df_processed['Amount_squared'] = df_processed['Amount'] ** 2
            df_processed['Amount_cubed'] = df_processed['Amount'] ** 3
            
            polynomial_features = ['Amount_squared', 'Amount_cubed']
            self.created_features.extend(polynomial_features)
            self.logger.info(f"Created {len(polynomial_features)} polynomial features")
        
        return df_processed
    
    def create_pca_features(self, df: pd.DataFrame, n_components: int = 5) -> pd.DataFrame:
        """
        Create PCA features from V columns (if present)
        
        Args:
            df: Input DataFrame
            n_components: Number of PCA components to create
            
        Returns:
            DataFrame with PCA features added
        """
        df_processed = df.copy()
        
        # Find V columns (common in credit card datasets)
        v_columns = [col for col in df_processed.columns if col.startswith('V')]
        
        if len(v_columns) >= n_components:
            from sklearn.decomposition import PCA
            
            pca = PCA(n_components=n_components)
            pca_features = pca.fit_transform(df_processed[v_columns])
            
            # Add PCA features to dataframe
            pca_feature_names = [f'PCA_{i+1}' for i in range(n_components)]
            for i, feature_name in enumerate(pca_feature_names):
                df_processed[feature_name] = pca_features[:, i]
            
            self.created_features.extend(pca_feature_names)
            
            # Store explained variance ratio
            self.feature_importance['pca_explained_variance'] = pca.explained_variance_ratio_
            
            self.logger.info(f"Created {n_components} PCA features explaining "
                           f"{pca.explained_variance_ratio_.sum():.2%} of variance")
        
        return df_processed
    
    def select_features_univariate(self, X: pd.DataFrame, y: pd.Series, 
                                  k: int = 20, score_func=f_classif) -> pd.DataFrame:
        """
        Select features using univariate statistical tests
        
        Args:
            X: Feature matrix
            y: Target vector
            k: Number of features to select
            score_func: Scoring function
            
        Returns:
            DataFrame with selected features
        """
        selector = SelectKBest(score_func=score_func, k=k)
        X_selected = selector.fit_transform(X, y)
        
        # Get selected feature names
        selected_features = X.columns[selector.get_support()].tolist()
        
        # Store feature scores
        self.feature_importance['univariate_scores'] = dict(
            zip(X.columns, selector.scores_)
        )
        
        self.feature_selectors['univariate'] = selector
        
        self.logger.info(f"Selected {len(selected_features)} features using univariate selection")
        
        return pd.DataFrame(X_selected, columns=selected_features, index=X.index)
    
    def select_features_rfe(self, X: pd.DataFrame, y: pd.Series, 
                           n_features: int = 20, estimator=None) -> pd.DataFrame:
        """
        Select features using Recursive Feature Elimination
        
        Args:
            X: Feature matrix
            y: Target vector
            n_features: Number of features to select
            estimator: Base estimator for RFE
            
        Returns:
            DataFrame with selected features
        """
        if estimator is None:
            estimator = RandomForestClassifier(n_estimators=100, random_state=42)
        
        selector = RFE(estimator=estimator, n_features_to_select=n_features)
        X_selected = selector.fit_transform(X, y)
        
        # Get selected feature names
        selected_features = X.columns[selector.get_support()].tolist()
        
        # Store feature rankings
        self.feature_importance['rfe_rankings'] = dict(
            zip(X.columns, selector.ranking_)
        )
        
        self.feature_selectors['rfe'] = selector
        
        self.logger.info(f"Selected {len(selected_features)} features using RFE")
        
        return pd.DataFrame(X_selected, columns=selected_features, index=X.index)
    
    def select_features_importance(self, X: pd.DataFrame, y: pd.Series, 
                                  n_features: int = 20, estimator=None) -> pd.DataFrame:
        """
        Select features based on feature importance from tree-based models
        
        Args:
            X: Feature matrix
            y: Target vector
            n_features: Number of features to select
            estimator: Tree-based estimator
            
        Returns:
            DataFrame with selected features
        """
        if estimator is None:
            estimator = RandomForestClassifier(n_estimators=100, random_state=42)
        
        estimator.fit(X, y)
        
        # Get feature importances
        importances = estimator.feature_importances_
        
        # Sort features by importance
        feature_importance_pairs = list(zip(X.columns, importances))
        feature_importance_pairs.sort(key=lambda x: x[1], reverse=True)
        
        # Select top features
        selected_features = [pair[0] for pair in feature_importance_pairs[:n_features]]
        
        # Store feature importances
        self.feature_importance['tree_importance'] = dict(feature_importance_pairs)
        
        self.logger.info(f"Selected {len(selected_features)} features using importance-based selection")
        
        return X[selected_features]
    
    def feature_engineering_pipeline(self, df: pd.DataFrame, 
                                   target_col: str = 'Class',
                                   feature_selection_method: str = 'importance',
                                   n_features: int = 30) -> Tuple[pd.DataFrame, List[str]]:
        """
        Complete feature engineering pipeline
        
        Args:
            df: Input DataFrame
            target_col: Name of target column
            feature_selection_method: Method for feature selection
            n_features: Number of features to select
            
        Returns:
            Tuple of (processed_dataframe, selected_feature_names)
        """
        self.logger.info("Starting feature engineering pipeline")
        
        df_processed = df.copy()
        
        # Create temporal features
        df_processed = self.create_temporal_features(df_processed)
        
        # Create amount-based features
        df_processed = self.create_amount_features(df_processed)
        
        # Create behavioral features
        df_processed = self.create_behavioral_features(df_processed)
        
        # Create statistical features
        df_processed = self.create_statistical_features(df_processed)
        
        # Create PCA features
        df_processed = self.create_pca_features(df_processed)
        
        self.logger.info(f"Total features created: {len(self.created_features)}")
        self.logger.info(f"DataFrame shape after feature engineering: {df_processed.shape}")
        
        # Feature selection
        if target_col in df_processed.columns:
            X = df_processed.drop(target_col, axis=1)
            y = df_processed[target_col]
            
            if feature_selection_method == 'univariate':
                X_selected = self.select_features_univariate(X, y, k=n_features)
            elif feature_selection_method == 'rfe':
                X_selected = self.select_features_rfe(X, y, n_features=n_features)
            elif feature_selection_method == 'importance':
                X_selected = self.select_features_importance(X, y, n_features=n_features)
            else:
                X_selected = X
                self.logger.info("No feature selection applied")
            
            # Combine selected features with target
            df_final = pd.concat([X_selected, y], axis=1)
            selected_features = X_selected.columns.tolist()
            
        else:
            df_final = df_processed
            selected_features = df_processed.columns.tolist()
        
        self.logger.info(f"Feature engineering pipeline completed. Final shape: {df_final.shape}")
        
        return df_final, selected_features
    
    def get_feature_importance_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive feature importance report
        
        Returns:
            Dictionary containing feature importance information
        """
        report = {
            'created_features': self.created_features,
            'total_features_created': len(self.created_features),
            'feature_importance_scores': self.feature_importance,
            'feature_selectors': list(self.feature_selectors.keys())
        }
        
        return report
    
    def save_feature_engineering_artifacts(self, output_dir: str):
        """
        Save feature engineering artifacts
        
        Args:
            output_dir: Directory to save artifacts
        """
        import os
        import joblib
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save feature selectors
        for name, selector in self.feature_selectors.items():
            joblib.dump(selector, os.path.join(output_dir, f'{name}_selector.pkl'))
        
        # Save feature importance report
        import json
        with open(os.path.join(output_dir, 'feature_importance_report.json'), 'w') as f:
            json.dump(self.get_feature_importance_report(), f, indent=2, default=str)
        
        self.logger.info(f"Feature engineering artifacts saved to {output_dir}")


if __name__ == "__main__":
    # Example usage
    engineer = FeatureEngineer()
    
    # For testing with sample data
    # df_engineered, selected_features = engineer.feature_engineering_pipeline(df)
    print("FeatureEngineer module created successfully!")
