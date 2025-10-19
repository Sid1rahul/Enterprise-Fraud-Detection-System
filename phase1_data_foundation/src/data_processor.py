"""
Data Processing Module for Credit Card Fraud Detection
Handles data ingestion, cleaning, preprocessing, and validation
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, Optional
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import logging
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    """
    Comprehensive data processing pipeline for credit card fraud detection
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize DataProcessor with configuration
        
        Args:
            config: Configuration dictionary with processing parameters
        """
        self.config = config or {}
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.target_column = 'Class'  # Default fraud indicator column
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def load_data(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Load data from various file formats
        
        Args:
            file_path: Path to the data file
            **kwargs: Additional parameters for pandas read functions
            
        Returns:
            Loaded DataFrame
        """
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, **kwargs)
            elif file_path.endswith('.parquet'):
                df = pd.read_parquet(file_path, **kwargs)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path, **kwargs)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
                
            self.logger.info(f"Loaded data with shape: {df.shape}")
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise
    
    def explore_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive data exploration report
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary containing exploration results
        """
        exploration_report = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
            'duplicates': df.duplicated().sum(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
        }
        
        # Numerical columns statistics
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            exploration_report['numerical_stats'] = df[numerical_cols].describe().to_dict()
        
        # Categorical columns statistics
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            exploration_report['categorical_stats'] = {}
            for col in categorical_cols:
                exploration_report['categorical_stats'][col] = {
                    'unique_values': df[col].nunique(),
                    'top_values': df[col].value_counts().head().to_dict()
                }
        
        # Class distribution (if target column exists)
        if self.target_column in df.columns:
            exploration_report['class_distribution'] = df[self.target_column].value_counts().to_dict()
            exploration_report['class_imbalance_ratio'] = df[self.target_column].value_counts().min() / df[self.target_column].value_counts().max()
        
        self.logger.info("Data exploration completed")
        return exploration_report
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'auto') -> pd.DataFrame:
        """
        Handle missing values using various strategies
        
        Args:
            df: Input DataFrame
            strategy: Strategy for handling missing values ('auto', 'drop', 'mean', 'median', 'mode')
            
        Returns:
            DataFrame with missing values handled
        """
        df_processed = df.copy()
        
        if strategy == 'auto':
            # Automatic strategy based on data type and missing percentage
            for col in df_processed.columns:
                missing_pct = df_processed[col].isnull().sum() / len(df_processed)
                
                if missing_pct > 0.5:  # Drop columns with >50% missing
                    df_processed.drop(col, axis=1, inplace=True)
                    self.logger.info(f"Dropped column {col} due to high missing percentage: {missing_pct:.2%}")
                    
                elif missing_pct > 0:
                    if df_processed[col].dtype in ['object', 'category']:
                        # Fill categorical with mode
                        mode_value = df_processed[col].mode().iloc[0] if not df_processed[col].mode().empty else 'Unknown'
                        df_processed[col].fillna(mode_value, inplace=True)
                    else:
                        # Fill numerical with median
                        median_value = df_processed[col].median()
                        df_processed[col].fillna(median_value, inplace=True)
                    
                    self.logger.info(f"Filled missing values in {col}: {missing_pct:.2%}")
        
        elif strategy == 'drop':
            initial_shape = df_processed.shape
            df_processed.dropna(inplace=True)
            self.logger.info(f"Dropped rows with missing values: {initial_shape[0]} -> {df_processed.shape[0]}")
        
        elif strategy in ['mean', 'median']:
            numerical_cols = df_processed.select_dtypes(include=[np.number]).columns
            if strategy == 'mean':
                df_processed[numerical_cols] = df_processed[numerical_cols].fillna(df_processed[numerical_cols].mean())
            else:
                df_processed[numerical_cols] = df_processed[numerical_cols].fillna(df_processed[numerical_cols].median())
        
        elif strategy == 'mode':
            for col in df_processed.columns:
                if df_processed[col].isnull().sum() > 0:
                    mode_value = df_processed[col].mode().iloc[0] if not df_processed[col].mode().empty else 'Unknown'
                    df_processed[col].fillna(mode_value, inplace=True)
        
        return df_processed
    
    def detect_outliers(self, df: pd.DataFrame, method: str = 'iqr', threshold: float = 1.5) -> Dict[str, np.ndarray]:
        """
        Detect outliers using various methods
        
        Args:
            df: Input DataFrame
            method: Outlier detection method ('iqr', 'zscore', 'isolation_forest')
            threshold: Threshold for outlier detection
            
        Returns:
            Dictionary with outlier indices for each numerical column
        """
        outliers = {}
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                outliers[col] = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.values
                
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers[col] = df[z_scores > threshold].index.values
        
        # Log outlier statistics
        total_outliers = sum(len(indices) for indices in outliers.values())
        self.logger.info(f"Detected {total_outliers} outliers using {method} method")
        
        return outliers
    
    def remove_outliers(self, df: pd.DataFrame, outlier_indices: Dict[str, np.ndarray], 
                       strategy: str = 'remove') -> pd.DataFrame:
        """
        Remove or cap outliers
        
        Args:
            df: Input DataFrame
            outlier_indices: Dictionary with outlier indices for each column
            strategy: Strategy for handling outliers ('remove', 'cap')
            
        Returns:
            DataFrame with outliers handled
        """
        df_processed = df.copy()
        
        if strategy == 'remove':
            # Get unique outlier indices across all columns
            all_outlier_indices = set()
            for indices in outlier_indices.values():
                all_outlier_indices.update(indices)
            
            initial_shape = df_processed.shape
            df_processed = df_processed.drop(list(all_outlier_indices))
            self.logger.info(f"Removed outliers: {initial_shape[0]} -> {df_processed.shape[0]} rows")
            
        elif strategy == 'cap':
            for col, indices in outlier_indices.items():
                if len(indices) > 0:
                    Q1 = df_processed[col].quantile(0.25)
                    Q3 = df_processed[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    df_processed[col] = df_processed[col].clip(lower=lower_bound, upper=upper_bound)
                    self.logger.info(f"Capped outliers in {col}")
        
        return df_processed
    
    def encode_categorical_features(self, df: pd.DataFrame, encoding_method: str = 'label') -> pd.DataFrame:
        """
        Encode categorical features
        
        Args:
            df: Input DataFrame
            encoding_method: Encoding method ('label', 'onehot', 'target')
            
        Returns:
            DataFrame with encoded categorical features
        """
        df_processed = df.copy()
        categorical_cols = df_processed.select_dtypes(include=['object', 'category']).columns
        
        if encoding_method == 'label':
            for col in categorical_cols:
                if col != self.target_column:  # Don't encode target column
                    le = LabelEncoder()
                    df_processed[col] = le.fit_transform(df_processed[col].astype(str))
                    self.label_encoders[col] = le
                    self.logger.info(f"Label encoded column: {col}")
        
        elif encoding_method == 'onehot':
            # One-hot encoding for categorical columns
            df_processed = pd.get_dummies(df_processed, columns=categorical_cols, drop_first=True)
            self.logger.info(f"One-hot encoded {len(categorical_cols)} categorical columns")
        
        return df_processed
    
    def normalize_features(self, df: pd.DataFrame, method: str = 'standard') -> pd.DataFrame:
        """
        Normalize numerical features
        
        Args:
            df: Input DataFrame
            method: Normalization method ('standard', 'minmax', 'robust')
            
        Returns:
            DataFrame with normalized features
        """
        df_processed = df.copy()
        numerical_cols = df_processed.select_dtypes(include=[np.number]).columns
        
        # Exclude target column from normalization
        if self.target_column in numerical_cols:
            numerical_cols = numerical_cols.drop(self.target_column)
        
        if method == 'standard':
            df_processed[numerical_cols] = self.scaler.fit_transform(df_processed[numerical_cols])
            self.logger.info("Applied standard scaling to numerical features")
        
        return df_processed
    
    def split_data(self, df: pd.DataFrame, test_size: float = 0.2, 
                   random_state: int = 42, stratify: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Split data into training and testing sets
        
        Args:
            df: Input DataFrame
            test_size: Proportion of test set
            random_state: Random state for reproducibility
            stratify: Whether to stratify split based on target column
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        # Separate features and target
        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in DataFrame")
        
        X = df.drop(self.target_column, axis=1)
        y = df[self.target_column]
        
        self.feature_columns = X.columns.tolist()
        
        # Stratified split if requested and target is categorical
        stratify_param = y if stratify and len(y.unique()) > 1 else None
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, 
            stratify=stratify_param
        )
        
        self.logger.info(f"Data split - Train: {X_train.shape}, Test: {X_test.shape}")
        self.logger.info(f"Class distribution - Train: {y_train.value_counts().to_dict()}")
        self.logger.info(f"Class distribution - Test: {y_test.value_counts().to_dict()}")
        
        return X_train, X_test, y_train, y_test
    
    def process_pipeline(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Complete data processing pipeline
        
        Args:
            file_path: Path to the data file
            **kwargs: Additional processing parameters
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        self.logger.info("Starting data processing pipeline")
        
        # Load data
        df = self.load_data(file_path)
        
        # Explore data
        exploration_report = self.explore_data(df)
        
        # Handle missing values
        df = self.handle_missing_values(df, strategy=kwargs.get('missing_strategy', 'auto'))
        
        # Detect and handle outliers
        if kwargs.get('handle_outliers', True):
            outliers = self.detect_outliers(df, method=kwargs.get('outlier_method', 'iqr'))
            df = self.remove_outliers(df, outliers, strategy=kwargs.get('outlier_strategy', 'remove'))
        
        # Encode categorical features
        df = self.encode_categorical_features(df, encoding_method=kwargs.get('encoding_method', 'label'))
        
        # Normalize features
        if kwargs.get('normalize', True):
            df = self.normalize_features(df, method=kwargs.get('normalization_method', 'standard'))
        
        # Split data
        X_train, X_test, y_train, y_test = self.split_data(
            df, 
            test_size=kwargs.get('test_size', 0.2),
            random_state=kwargs.get('random_state', 42),
            stratify=kwargs.get('stratify', True)
        )
        
        self.logger.info("Data processing pipeline completed successfully")
        return X_train, X_test, y_train, y_test
    
    def save_processed_data(self, X_train: pd.DataFrame, X_test: pd.DataFrame, 
                           y_train: pd.Series, y_test: pd.Series, output_dir: str):
        """
        Save processed data to files
        
        Args:
            X_train, X_test, y_train, y_test: Processed data splits
            output_dir: Directory to save processed data
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        X_train.to_csv(os.path.join(output_dir, 'X_train.csv'), index=False)
        X_test.to_csv(os.path.join(output_dir, 'X_test.csv'), index=False)
        y_train.to_csv(os.path.join(output_dir, 'y_train.csv'), index=False)
        y_test.to_csv(os.path.join(output_dir, 'y_test.csv'), index=False)
        
        self.logger.info(f"Processed data saved to {output_dir}")


if __name__ == "__main__":
    # Example usage
    processor = DataProcessor()
    
    # For testing with sample data
    # X_train, X_test, y_train, y_test = processor.process_pipeline('path/to/creditcard.csv')
    print("DataProcessor module created successfully!")
