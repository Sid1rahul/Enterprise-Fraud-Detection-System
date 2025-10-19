"""
Helper utilities for Credit Card Fraud Detection
Common utility functions and helper classes
"""

import pandas as pd
import numpy as np
import os
import pickle
import joblib
from typing import Any, Dict, List, Tuple, Optional, Union
from datetime import datetime, timedelta
import hashlib
import json
import warnings
warnings.filterwarnings('ignore')

def create_directory(directory_path: str, exist_ok: bool = True) -> str:
    """
    Create directory if it doesn't exist
    
    Args:
        directory_path: Path to directory
        exist_ok: Whether to ignore if directory already exists
        
    Returns:
        Created directory path
    """
    os.makedirs(directory_path, exist_ok=exist_ok)
    return directory_path

def save_object(obj: Any, filepath: str, method: str = 'joblib') -> None:
    """
    Save object to file using specified method
    
    Args:
        obj: Object to save
        filepath: Path to save file
        method: Saving method ('joblib', 'pickle')
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if method == 'joblib':
        joblib.dump(obj, filepath)
    elif method == 'pickle':
        with open(filepath, 'wb') as f:
            pickle.dump(obj, f)
    else:
        raise ValueError(f"Unknown saving method: {method}")

def load_object(filepath: str, method: str = 'auto') -> Any:
    """
    Load object from file
    
    Args:
        filepath: Path to file
        method: Loading method ('auto', 'joblib', 'pickle')
        
    Returns:
        Loaded object
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    if method == 'auto':
        # Auto-detect based on file extension
        if filepath.endswith('.pkl'):
            method = 'pickle'
        else:
            method = 'joblib'
    
    if method == 'joblib':
        return joblib.load(filepath)
    elif method == 'pickle':
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    else:
        raise ValueError(f"Unknown loading method: {method}")

def generate_timestamp(format_str: str = "%Y%m%d_%H%M%S") -> str:
    """
    Generate timestamp string
    
    Args:
        format_str: Timestamp format
        
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime(format_str)

def generate_hash(data: Union[str, bytes, Dict, List], algorithm: str = 'md5') -> str:
    """
    Generate hash for data
    
    Args:
        data: Data to hash
        algorithm: Hash algorithm ('md5', 'sha1', 'sha256')
        
    Returns:
        Hash string
    """
    if isinstance(data, (dict, list)):
        data = json.dumps(data, sort_keys=True)
    
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    hash_func = getattr(hashlib, algorithm)()
    hash_func.update(data)
    return hash_func.hexdigest()

def memory_usage_mb() -> float:
    """Get current memory usage in MB"""
    import psutil
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def format_bytes(bytes_value: int) -> str:
    """Format bytes into human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

class Timer:
    """Context manager for timing operations"""
    
    def __init__(self, operation_name: str = "Operation"):
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        print(f"{self.operation_name} completed in {format_duration(duration)}")
    
    @property
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds"""
        if self.start_time is None:
            return 0.0
        end_time = self.end_time or datetime.now()
        return (end_time - self.start_time).total_seconds()

def validate_dataframe(df: pd.DataFrame, required_columns: List[str] = None,
                      min_rows: int = 1) -> bool:
    """
    Validate DataFrame structure and content
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        min_rows: Minimum number of rows required
        
    Returns:
        True if valid, raises ValueError if not
    """
    if df is None or df.empty:
        raise ValueError("DataFrame is None or empty")
    
    if len(df) < min_rows:
        raise ValueError(f"DataFrame has {len(df)} rows, minimum required: {min_rows}")
    
    if required_columns:
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    return True

def detect_data_types(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Detect and categorize data types in DataFrame
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with categorized column names
    """
    categorized_columns = {
        'numerical': [],
        'categorical': [],
        'datetime': [],
        'boolean': [],
        'text': []
    }
    
    for col in df.columns:
        dtype = df[col].dtype
        
        if pd.api.types.is_numeric_dtype(dtype):
            categorized_columns['numerical'].append(col)
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            categorized_columns['datetime'].append(col)
        elif pd.api.types.is_bool_dtype(dtype):
            categorized_columns['boolean'].append(col)
        elif pd.api.types.is_categorical_dtype(dtype) or dtype == 'object':
            # Check if it's actually numerical stored as object
            try:
                pd.to_numeric(df[col].dropna().iloc[:100])
                categorized_columns['numerical'].append(col)
            except (ValueError, TypeError):
                # Check if it's categorical (limited unique values)
                unique_ratio = df[col].nunique() / len(df)
                if unique_ratio < 0.05 or df[col].nunique() < 20:
                    categorized_columns['categorical'].append(col)
                else:
                    categorized_columns['text'].append(col)
    
    return categorized_columns

def sample_dataframe(df: pd.DataFrame, n_samples: int = None, 
                    fraction: float = None, stratify_column: str = None,
                    random_state: int = 42) -> pd.DataFrame:
    """
    Sample DataFrame with optional stratification
    
    Args:
        df: Input DataFrame
        n_samples: Number of samples to take
        fraction: Fraction of data to sample
        stratify_column: Column to use for stratified sampling
        random_state: Random state for reproducibility
        
    Returns:
        Sampled DataFrame
    """
    if n_samples is None and fraction is None:
        return df
    
    if stratify_column and stratify_column in df.columns:
        # Stratified sampling
        if fraction is not None:
            return df.groupby(stratify_column, group_keys=False).apply(
                lambda x: x.sample(frac=fraction, random_state=random_state)
            )
        else:
            # Calculate samples per group
            group_sizes = df[stratify_column].value_counts()
            samples_per_group = (group_sizes * n_samples / len(df)).round().astype(int)
            
            sampled_dfs = []
            for group, n_group_samples in samples_per_group.items():
                group_df = df[df[stratify_column] == group]
                if len(group_df) >= n_group_samples:
                    sampled_dfs.append(group_df.sample(n=n_group_samples, random_state=random_state))
                else:
                    sampled_dfs.append(group_df)
            
            return pd.concat(sampled_dfs, ignore_index=True)
    
    else:
        # Simple random sampling
        if fraction is not None:
            return df.sample(frac=fraction, random_state=random_state)
        else:
            return df.sample(n=min(n_samples, len(df)), random_state=random_state)

def calculate_correlation_matrix(df: pd.DataFrame, method: str = 'pearson',
                                min_periods: int = 30) -> pd.DataFrame:
    """
    Calculate correlation matrix for numerical columns
    
    Args:
        df: Input DataFrame
        method: Correlation method ('pearson', 'spearman', 'kendall')
        min_periods: Minimum number of observations for correlation
        
    Returns:
        Correlation matrix DataFrame
    """
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) < 2:
        return pd.DataFrame()
    
    return df[numerical_cols].corr(method=method, min_periods=min_periods)

def find_highly_correlated_features(correlation_matrix: pd.DataFrame, 
                                   threshold: float = 0.95) -> List[Tuple[str, str, float]]:
    """
    Find highly correlated feature pairs
    
    Args:
        correlation_matrix: Correlation matrix
        threshold: Correlation threshold
        
    Returns:
        List of highly correlated feature pairs
    """
    highly_correlated = []
    
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_value = abs(correlation_matrix.iloc[i, j])
            if corr_value >= threshold:
                highly_correlated.append((
                    correlation_matrix.columns[i],
                    correlation_matrix.columns[j],
                    corr_value
                ))
    
    return sorted(highly_correlated, key=lambda x: x[2], reverse=True)

class DataFrameInfo:
    """Class to generate comprehensive DataFrame information"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self._info = None
    
    def generate_info(self) -> Dict[str, Any]:
        """Generate comprehensive DataFrame information"""
        if self._info is not None:
            return self._info
        
        info = {
            'basic_info': {
                'shape': self.df.shape,
                'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
                'dtypes': self.df.dtypes.value_counts().to_dict()
            },
            'missing_data': {
                'total_missing': self.df.isnull().sum().sum(),
                'missing_percentage': (self.df.isnull().sum().sum() / self.df.size) * 100,
                'columns_with_missing': self.df.columns[self.df.isnull().any()].tolist(),
                'missing_by_column': self.df.isnull().sum().to_dict()
            },
            'duplicates': {
                'total_duplicates': self.df.duplicated().sum(),
                'duplicate_percentage': (self.df.duplicated().sum() / len(self.df)) * 100
            },
            'data_types': detect_data_types(self.df)
        }
        
        # Numerical statistics
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            info['numerical_stats'] = self.df[numerical_cols].describe().to_dict()
        
        # Categorical statistics
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            info['categorical_stats'] = {}
            for col in categorical_cols:
                info['categorical_stats'][col] = {
                    'unique_count': self.df[col].nunique(),
                    'top_values': self.df[col].value_counts().head().to_dict()
                }
        
        self._info = info
        return info
    
    def print_summary(self):
        """Print summary of DataFrame information"""
        info = self.generate_info()
        
        print("=" * 60)
        print("DATAFRAME SUMMARY")
        print("=" * 60)
        
        # Basic info
        print(f"Shape: {info['basic_info']['shape']}")
        print(f"Memory Usage: {info['basic_info']['memory_usage_mb']:.2f} MB")
        print(f"Data Types: {info['basic_info']['dtypes']}")
        print()
        
        # Missing data
        print("MISSING DATA:")
        print(f"Total Missing: {info['missing_data']['total_missing']}")
        print(f"Missing Percentage: {info['missing_data']['missing_percentage']:.2f}%")
        if info['missing_data']['columns_with_missing']:
            print(f"Columns with Missing: {info['missing_data']['columns_with_missing']}")
        print()
        
        # Duplicates
        print("DUPLICATES:")
        print(f"Total Duplicates: {info['duplicates']['total_duplicates']}")
        print(f"Duplicate Percentage: {info['duplicates']['duplicate_percentage']:.2f}%")
        print()
        
        # Data types
        print("COLUMN CATEGORIZATION:")
        for category, columns in info['data_types'].items():
            if columns:
                print(f"{category.title()}: {len(columns)} columns")

def export_to_multiple_formats(df: pd.DataFrame, base_filename: str, 
                              formats: List[str] = None, output_dir: str = "."):
    """
    Export DataFrame to multiple formats
    
    Args:
        df: DataFrame to export
        base_filename: Base filename (without extension)
        formats: List of formats ('csv', 'parquet', 'excel', 'json')
        output_dir: Output directory
    """
    if formats is None:
        formats = ['csv', 'parquet']
    
    create_directory(output_dir)
    
    for format_type in formats:
        filepath = os.path.join(output_dir, f"{base_filename}.{format_type}")
        
        if format_type == 'csv':
            df.to_csv(filepath, index=False)
        elif format_type == 'parquet':
            df.to_parquet(filepath, index=False)
        elif format_type == 'excel':
            df.to_excel(filepath, index=False)
        elif format_type == 'json':
            df.to_json(filepath, orient='records', indent=2)
        else:
            print(f"Warning: Unknown format '{format_type}' skipped")

if __name__ == "__main__":
    # Example usage
    print("Helper utilities module created successfully!")
    
    # Test timer
    with Timer("Test operation"):
        import time
        time.sleep(1)
    
    # Test timestamp generation
    timestamp = generate_timestamp()
    print(f"Generated timestamp: {timestamp}")
    
    # Test hash generation
    test_data = {"key": "value", "number": 123}
    hash_value = generate_hash(test_data)
    print(f"Generated hash: {hash_value}")
