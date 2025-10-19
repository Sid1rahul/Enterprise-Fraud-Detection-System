"""
Sample Data Generator for Credit Card Fraud Detection
Creates synthetic credit card transaction data for testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_credit_card_data(n_samples: int = 10000, fraud_rate: float = 0.002) -> pd.DataFrame:
    """
    Generate synthetic credit card transaction data
    
    Args:
        n_samples: Number of samples to generate
        fraud_rate: Proportion of fraudulent transactions
        
    Returns:
        DataFrame with synthetic credit card data
    """
    np.random.seed(42)
    
    # Calculate number of fraud cases
    n_fraud = int(n_samples * fraud_rate)
    n_normal = n_samples - n_fraud
    
    # Generate time features (seconds since start)
    start_time = datetime(2023, 1, 1)
    time_range = 365 * 24 * 3600  # 1 year in seconds
    times = np.random.uniform(0, time_range, n_samples)
    times = np.sort(times)  # Sort to make it realistic
    
    # Generate V features (PCA-transformed features, common in credit card datasets)
    n_v_features = 28
    v_features = {}
    
    for i in range(1, n_v_features + 1):
        if i <= 14:  # First half - more discriminative
            normal_data = np.random.normal(0, 1, n_normal)
            fraud_data = np.random.normal(2, 1.5, n_fraud)  # Shifted for fraud
        else:  # Second half - less discriminative
            normal_data = np.random.normal(0, 1, n_normal)
            fraud_data = np.random.normal(0.5, 1.2, n_fraud)  # Slightly shifted
        
        v_features[f'V{i}'] = np.concatenate([normal_data, fraud_data])
    
    # Generate Amount feature
    # Normal transactions: log-normal distribution
    normal_amounts = np.random.lognormal(mean=3, sigma=1, size=n_normal)
    normal_amounts = np.clip(normal_amounts, 0.01, 25000)  # Reasonable range
    
    # Fraud transactions: different distribution (often smaller amounts)
    fraud_amounts = np.random.lognormal(mean=2, sigma=1.5, size=n_fraud)
    fraud_amounts = np.clip(fraud_amounts, 0.01, 10000)  # Smaller max for fraud
    
    amounts = np.concatenate([normal_amounts, fraud_amounts])
    
    # Create labels
    labels = np.concatenate([np.zeros(n_normal), np.ones(n_fraud)])
    
    # Shuffle all data together
    indices = np.random.permutation(n_samples)
    
    # Create DataFrame
    data = {
        'Time': times[indices],
        'Amount': amounts[indices],
        'Class': labels[indices].astype(int)
    }
    
    # Add V features
    for feature_name, feature_values in v_features.items():
        data[feature_name] = feature_values[indices]
    
    df = pd.DataFrame(data)
    
    # Add some additional realistic features
    df['Hour'] = ((df['Time'] % (24 * 3600)) / 3600).astype(int)
    df['DayOfWeek'] = ((df['Time'] / (24 * 3600)) % 7).astype(int)
    
    # Add merchant category (categorical feature)
    merchant_categories = ['grocery', 'gas', 'restaurant', 'retail', 'online', 'atm', 'other']
    df['MerchantCategory'] = np.random.choice(merchant_categories, n_samples)
    
    # Add customer age groups
    age_groups = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    df['AgeGroup'] = np.random.choice(age_groups, n_samples)
    
    # Reorder columns to match typical credit card dataset format
    column_order = ['Time'] + [f'V{i}' for i in range(1, n_v_features + 1)] + \
                   ['Amount', 'Hour', 'DayOfWeek', 'MerchantCategory', 'AgeGroup', 'Class']
    
    df = df[column_order]
    
    print(f"Generated {n_samples} samples with {n_fraud} fraud cases ({fraud_rate*100:.2f}% fraud rate)")
    print(f"Dataset shape: {df.shape}")
    print(f"Class distribution:\n{df['Class'].value_counts()}")
    
    return df

def save_sample_data(output_dir: str = "data"):
    """Generate and save sample datasets"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate different sized datasets
    datasets = {
        'small': 1000,
        'medium': 10000,
        'large': 50000
    }
    
    for name, size in datasets.items():
        print(f"\nGenerating {name} dataset ({size} samples)...")
        df = generate_sample_credit_card_data(size)
        
        # Save as CSV
        filepath = os.path.join(output_dir, f'creditcard_{name}.csv')
        df.to_csv(filepath, index=False)
        print(f"Saved to: {filepath}")

if __name__ == "__main__":
    # Generate sample data
    save_sample_data("data")
    
    print("\nSample data generation completed!")
    print("You can now run the main pipeline with:")
    print("python main.py --data data/creditcard_medium.csv --output output")
