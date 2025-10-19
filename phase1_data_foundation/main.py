"""
Main execution script for Phase 1: Data Foundation & Basic ML Pipeline
Credit Card Fraud Detection System
"""

import os
import sys
import argparse
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Import modules
from data_processor import DataProcessor
from feature_engineer import FeatureEngineer
from models.xgboost_model import XGBoostFraudDetector
from models.isolation_forest import IsolationForestFraudDetector
from oversampling import AdvancedOversampler
from explainability import ModelExplainer
from evaluation import ModelEvaluator
from config import load_config, ProjectConfig
from logger import setup_logger, Timer
from helpers import create_directory, save_object, generate_timestamp

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Credit Card Fraud Detection - Phase 1')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--data', type=str, required=True, help='Path to dataset')
    parser.add_argument('--output', type=str, default='output', help='Output directory')
    parser.add_argument('--log-level', type=str, default='INFO', help='Logging level')
    parser.add_argument('--skip-optimization', action='store_true', help='Skip hyperparameter optimization')
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        config = load_config(args.config)
    else:
        config = ProjectConfig()
        config.data_path = args.data
        config.output_dir = args.output
    
    # Setup logging
    timestamp = generate_timestamp()
    log_dir = os.path.join(args.output, 'logs')
    logger = setup_logger('fraud_detection_phase1', args.log_level, log_dir)
    
    logger.info("=" * 60)
    logger.info("CREDIT CARD FRAUD DETECTION - PHASE 1")
    logger.info("Data Foundation & Basic ML Pipeline")
    logger.info("=" * 60)
    logger.info(f"Timestamp: {timestamp}")
    logger.info(f"Data path: {args.data}")
    logger.info(f"Output directory: {args.output}")
    logger.info(f"Configuration: {args.config or 'Default'}")
    
    # Create output directories
    output_dirs = {
        'models': os.path.join(args.output, 'models'),
        'data': os.path.join(args.output, 'processed_data'),
        'results': os.path.join(args.output, 'results'),
        'explanations': os.path.join(args.output, 'explanations'),
        'plots': os.path.join(args.output, 'plots')
    }
    
    for dir_path in output_dirs.values():
        create_directory(dir_path)
    
    try:
        # Phase 1: Data Processing
        logger.info("Phase 1.1: Starting Data Processing...")
        with Timer("Data Processing"):
            processor = DataProcessor(config.data_processing.__dict__)
            X_train, X_test, y_train, y_test = processor.process_pipeline(
                args.data,
                **config.data_processing.__dict__
            )
            
            # Save processed data
            processor.save_processed_data(X_train, X_test, y_train, y_test, output_dirs['data'])
            logger.info(f"Processed data saved to {output_dirs['data']}")
        
        # Phase 1.2: Feature Engineering
        logger.info("Phase 1.2: Starting Feature Engineering...")
        with Timer("Feature Engineering"):
            engineer = FeatureEngineer(config.feature_engineering.__dict__)
            
            # Combine train and test for feature engineering
            X_combined = pd.concat([X_train, X_test], ignore_index=True)
            y_combined = pd.concat([y_train, y_test], ignore_index=True)
            combined_df = pd.concat([X_combined, y_combined], axis=1)
            
            # Apply feature engineering
            df_engineered, selected_features = engineer.feature_engineering_pipeline(
                combined_df,
                target_col='Class',
                feature_selection_method=config.feature_engineering.feature_selection_method,
                n_features=config.feature_engineering.n_features_to_select
            )
            
            # Split back to train/test
            train_size = len(X_train)
            X_train_eng = df_engineered.iloc[:train_size].drop('Class', axis=1)
            X_test_eng = df_engineered.iloc[train_size:].drop('Class', axis=1)
            y_train_eng = df_engineered.iloc[:train_size]['Class']
            y_test_eng = df_engineered.iloc[train_size:]['Class']
            
            # Save feature engineering artifacts
            engineer.save_feature_engineering_artifacts(output_dirs['results'])
            logger.info(f"Feature engineering completed. Selected {len(selected_features)} features")
        
        # Phase 1.3: Class Imbalance Handling
        logger.info("Phase 1.3: Handling Class Imbalance with ADASYN...")
        with Timer("ADASYN Oversampling"):
            oversampler = AdvancedOversampler(config.oversampling.__dict__)
            
            if config.oversampling.auto_optimize:
                X_train_balanced, y_train_balanced, sampling_report = oversampler.apply_best_sampling(
                    X_train_eng, y_train_eng, auto_optimize=True
                )
            else:
                X_train_balanced, y_train_balanced = oversampler.adasyn_oversampling(
                    X_train_eng, y_train_eng,
                    sampling_strategy=config.oversampling.sampling_strategy,
                    n_neighbors=config.oversampling.n_neighbors,
                    random_state=config.oversampling.random_state
                )
                sampling_report = oversampler.get_sampling_report()
            
            # Save sampling report
            save_object(sampling_report, os.path.join(output_dirs['results'], 'sampling_report.pkl'))
            logger.info("Class imbalance handling completed")
        
        # Phase 1.4: Model Training - XGBoost
        logger.info("Phase 1.4: Training XGBoost Model...")
        with Timer("XGBoost Training"):
            xgb_detector = XGBoostFraudDetector(config.xgboost.__dict__)
            
            if not args.skip_optimization:
                xgb_model = xgb_detector.train_optimized_model(
                    X_train_balanced, y_train_balanced,
                    X_test_eng, y_test_eng,
                    optimization_method=config.xgboost.optimization_method
                )
            else:
                xgb_model = xgb_detector.train_basic_model(
                    X_train_balanced, y_train_balanced,
                    X_test_eng, y_test_eng
                )
            
            # Save XGBoost model
            xgb_detector.save_model(os.path.join(output_dirs['models'], 'xgboost_model.pkl'))
            logger.info("XGBoost model training completed")
        
        # Phase 1.5: Model Training - Isolation Forest
        logger.info("Phase 1.5: Training Isolation Forest Model...")
        with Timer("Isolation Forest Training"):
            if_detector = IsolationForestFraudDetector(config.isolation_forest.__dict__)
            
            if not args.skip_optimization:
                if_model = if_detector.train_optimized_model(X_train_eng, y_train_eng)
            else:
                if_model = if_detector.train_basic_model(X_train_eng, y_train_eng)
            
            # Save Isolation Forest model
            if_detector.save_model(os.path.join(output_dirs['models'], 'isolation_forest_model.pkl'))
            logger.info("Isolation Forest model training completed")
        
        # Phase 1.6: Model Evaluation
        logger.info("Phase 1.6: Evaluating Models...")
        with Timer("Model Evaluation"):
            evaluator = ModelEvaluator(config.evaluation.__dict__)
            evaluator.set_cost_matrix(config.evaluation.cost_matrix)
            
            # Evaluate XGBoost
            xgb_results = evaluator.comprehensive_evaluation(
                xgb_model, X_test_eng, y_test_eng,
                X_train_balanced, y_train_balanced,
                perform_cv=True
            )
            
            # Evaluate Isolation Forest
            if_results = evaluator.comprehensive_evaluation(
                if_model, X_test_eng, y_test_eng,
                X_train_eng, y_train_eng,
                perform_cv=True
            )
            
            # Compare models
            models = {
                'XGBoost': xgb_model,
                'Isolation_Forest': if_model
            }
            
            comparison_results = evaluator.compare_models(
                models, X_test_eng, y_test_eng,
                X_train_balanced, y_train_balanced
            )
            
            # Save evaluation results
            save_object(xgb_results, os.path.join(output_dirs['results'], 'xgboost_evaluation.pkl'))
            save_object(if_results, os.path.join(output_dirs['results'], 'isolation_forest_evaluation.pkl'))
            save_object(comparison_results, os.path.join(output_dirs['results'], 'model_comparison.pkl'))
            
            logger.info("Model evaluation completed")
        
        # Phase 1.7: Model Explainability
        logger.info("Phase 1.7: Generating Model Explanations...")
        with Timer("Model Explainability"):
            explainer = ModelExplainer(config.explainability.__dict__)
            
            # SHAP explanations for XGBoost
            explainer.initialize_shap_explainer(
                xgb_model, X_train_balanced.sample(min(1000, len(X_train_balanced))),
                explainer_type=config.explainability.shap_explainer_type
            )
            
            shap_values = explainer.calculate_shap_values(
                X_test_eng.head(100),  # Limit for performance
                max_evals=config.explainability.max_evals
            )
            
            # Generate comprehensive explanation report
            explanation_report = explainer.generate_explanation_report(
                X_test_eng.head(100), y_test_eng.head(100),
                sample_instances=[0, 25, 50, 75, 99]
            )
            
            # Save explanations
            explainer.save_explanations(
                os.path.join(output_dirs['explanations'], 'xgboost_explanations.pkl'),
                explanation_report
            )
            
            logger.info("Model explainability analysis completed")
        
        # Generate Final Report
        logger.info("Generating Final Report...")
        final_report = {
            'timestamp': timestamp,
            'configuration': config.__dict__,
            'data_info': {
                'original_shape': (len(X_train) + len(X_test), len(X_train.columns)),
                'processed_shape': (len(X_train_eng), len(X_train_eng.columns)),
                'balanced_shape': (len(X_train_balanced), len(X_train_balanced.columns)),
                'selected_features': selected_features
            },
            'model_performance': {
                'xgboost': {
                    'accuracy': xgb_results['basic_metrics']['accuracy'],
                    'precision': xgb_results['basic_metrics']['precision'],
                    'recall': xgb_results['basic_metrics']['recall'],
                    'f1_score': xgb_results['basic_metrics']['f1_score'],
                    'roc_auc': xgb_results['basic_metrics']['roc_auc']
                },
                'isolation_forest': {
                    'accuracy': if_results['basic_metrics']['accuracy'],
                    'precision': if_results['basic_metrics']['precision'],
                    'recall': if_results['basic_metrics']['recall'],
                    'f1_score': if_results['basic_metrics']['f1_score'],
                    'roc_auc': if_results['basic_metrics'].get('roc_auc', 'N/A')
                }
            },
            'cost_analysis': {
                'xgboost_total_cost': xgb_results['cost_sensitive_metrics']['total_cost'],
                'isolation_forest_total_cost': if_results['cost_sensitive_metrics']['total_cost']
            }
        }
        
        # Save final report
        save_object(final_report, os.path.join(output_dirs['results'], 'phase1_final_report.pkl'))
        
        # Print summary
        logger.info("=" * 60)
        logger.info("PHASE 1 COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        logger.info(f"XGBoost Performance - F1: {final_report['model_performance']['xgboost']['f1_score']:.4f}, "
                   f"AUC: {final_report['model_performance']['xgboost']['roc_auc']:.4f}")
        logger.info(f"Isolation Forest Performance - F1: {final_report['model_performance']['isolation_forest']['f1_score']:.4f}")
        logger.info(f"Total Cost - XGBoost: ${final_report['cost_analysis']['xgboost_total_cost']:.2f}, "
                   f"Isolation Forest: ${final_report['cost_analysis']['isolation_forest_total_cost']:.2f}")
        logger.info(f"Results saved to: {args.output}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error in Phase 1 execution: {str(e)}")
        raise

if __name__ == "__main__":
    # Import pandas here to avoid circular imports
    import pandas as pd
    main()
