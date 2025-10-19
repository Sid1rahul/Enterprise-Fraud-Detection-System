"""
Configuration Management for Credit Card Fraud Detection
Centralized configuration handling and parameter management
"""

import yaml
import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import logging

@dataclass
class DataProcessingConfig:
    """Data processing configuration"""
    missing_strategy: str = 'auto'
    handle_outliers: bool = True
    outlier_method: str = 'iqr'
    outlier_strategy: str = 'remove'
    encoding_method: str = 'label'
    normalize: bool = True
    normalization_method: str = 'standard'
    test_size: float = 0.2
    random_state: int = 42
    stratify: bool = True

@dataclass
class FeatureEngineeringConfig:
    """Feature engineering configuration"""
    create_temporal_features: bool = True
    create_amount_features: bool = True
    create_behavioral_features: bool = True
    create_statistical_features: bool = True
    create_pca_features: bool = True
    pca_components: int = 5
    feature_selection_method: str = 'importance'
    n_features_to_select: int = 30

@dataclass
class XGBoostConfig:
    """XGBoost model configuration"""
    objective: str = 'binary:logistic'
    eval_metric: str = 'auc'
    max_depth: int = 6
    learning_rate: float = 0.1
    n_estimators: int = 100
    subsample: float = 0.8
    colsample_bytree: float = 0.8
    random_state: int = 42
    n_jobs: int = -1
    optimization_method: str = 'optuna'
    n_trials: int = 100

@dataclass
class IsolationForestConfig:
    """Isolation Forest configuration"""
    n_estimators: int = 100
    max_samples: str = 'auto'
    contamination: float = 0.01
    max_features: float = 1.0
    bootstrap: bool = False
    random_state: int = 42
    n_jobs: int = -1

@dataclass
class OversamplingConfig:
    """Oversampling configuration"""
    method: str = 'adasyn'
    sampling_strategy: str = 'auto'
    n_neighbors: int = 5
    random_state: int = 42
    auto_optimize: bool = True

@dataclass
class ExplainabilityConfig:
    """Explainability configuration"""
    shap_explainer_type: str = 'auto'
    max_evals: int = 1000
    use_lime: bool = True
    calculate_permutation_importance: bool = True
    n_repeats: int = 10

@dataclass
class EvaluationConfig:
    """Evaluation configuration"""
    cv_folds: int = 5
    cost_matrix: Dict[str, float] = None
    perform_threshold_analysis: bool = True
    threshold_range: tuple = (0.1, 1.0)
    threshold_step: float = 0.05

@dataclass
class ProjectConfig:
    """Main project configuration"""
    project_name: str = "Credit Card Fraud Detection"
    data_path: str = ""
    output_dir: str = "output"
    model_dir: str = "models"
    log_level: str = "INFO"
    
    # Sub-configurations
    data_processing: DataProcessingConfig = None
    feature_engineering: FeatureEngineeringConfig = None
    xgboost: XGBoostConfig = None
    isolation_forest: IsolationForestConfig = None
    oversampling: OversamplingConfig = None
    explainability: ExplainabilityConfig = None
    evaluation: EvaluationConfig = None
    
    def __post_init__(self):
        """Initialize sub-configurations if not provided"""
        if self.data_processing is None:
            self.data_processing = DataProcessingConfig()
        if self.feature_engineering is None:
            self.feature_engineering = FeatureEngineeringConfig()
        if self.xgboost is None:
            self.xgboost = XGBoostConfig()
        if self.isolation_forest is None:
            self.isolation_forest = IsolationForestConfig()
        if self.oversampling is None:
            self.oversampling = OversamplingConfig()
        if self.explainability is None:
            self.explainability = ExplainabilityConfig()
        if self.evaluation is None:
            self.evaluation = EvaluationConfig()
            # Set default cost matrix
            self.evaluation.cost_matrix = {
                'tn': 0, 'fp': 1, 'fn': 10, 'tp': -2
            }

class ConfigManager:
    """Configuration manager for loading and saving configurations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_config(self, config_path: str) -> ProjectConfig:
        """
        Load configuration from file
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            ProjectConfig object
        """
        if not os.path.exists(config_path):
            self.logger.warning(f"Config file not found: {config_path}. Using default configuration.")
            return ProjectConfig()
        
        try:
            with open(config_path, 'r') as f:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    config_dict = yaml.safe_load(f)
                elif config_path.endswith('.json'):
                    config_dict = json.load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {config_path}")
            
            return self._dict_to_config(config_dict)
            
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return ProjectConfig()
    
    def save_config(self, config: ProjectConfig, config_path: str):
        """
        Save configuration to file
        
        Args:
            config: ProjectConfig object
            config_path: Path to save configuration
        """
        try:
            config_dict = asdict(config)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            with open(config_path, 'w') as f:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    yaml.dump(config_dict, f, default_flow_style=False, indent=2)
                elif config_path.endswith('.json'):
                    json.dump(config_dict, f, indent=2)
                else:
                    raise ValueError(f"Unsupported config file format: {config_path}")
            
            self.logger.info(f"Configuration saved to {config_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving config: {str(e)}")
    
    def _dict_to_config(self, config_dict: Dict[str, Any]) -> ProjectConfig:
        """Convert dictionary to ProjectConfig object"""
        # Extract sub-configurations
        data_processing = DataProcessingConfig(**config_dict.get('data_processing', {}))
        feature_engineering = FeatureEngineeringConfig(**config_dict.get('feature_engineering', {}))
        xgboost = XGBoostConfig(**config_dict.get('xgboost', {}))
        isolation_forest = IsolationForestConfig(**config_dict.get('isolation_forest', {}))
        oversampling = OversamplingConfig(**config_dict.get('oversampling', {}))
        explainability = ExplainabilityConfig(**config_dict.get('explainability', {}))
        evaluation = EvaluationConfig(**config_dict.get('evaluation', {}))
        
        # Create main config
        main_config_dict = {k: v for k, v in config_dict.items() 
                           if k not in ['data_processing', 'feature_engineering', 'xgboost', 
                                       'isolation_forest', 'oversampling', 'explainability', 'evaluation']}
        
        return ProjectConfig(
            **main_config_dict,
            data_processing=data_processing,
            feature_engineering=feature_engineering,
            xgboost=xgboost,
            isolation_forest=isolation_forest,
            oversampling=oversampling,
            explainability=explainability,
            evaluation=evaluation
        )
    
    def create_default_config_file(self, config_path: str):
        """Create a default configuration file"""
        default_config = ProjectConfig()
        self.save_config(default_config, config_path)
        self.logger.info(f"Default configuration file created: {config_path}")

# Global configuration instance
config_manager = ConfigManager()

def load_config(config_path: str = None) -> ProjectConfig:
    """Load configuration from file or return default"""
    if config_path is None:
        return ProjectConfig()
    return config_manager.load_config(config_path)

def save_config(config: ProjectConfig, config_path: str):
    """Save configuration to file"""
    config_manager.save_config(config, config_path)

if __name__ == "__main__":
    # Example usage
    config = ProjectConfig()
    print("Default configuration created successfully!")
    
    # Save default config
    config_manager.create_default_config_file("config/default_config.yaml")
