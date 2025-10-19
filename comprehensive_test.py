"""
Comprehensive Test Suite for Credit Card Fraud Detection System
Tests all implemented features from Phase 1 and Phase 4
"""

import os
import sys
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add paths for imports
sys.path.append(os.path.join('phase1_data_foundation', 'src'))
sys.path.append(os.path.join('phase1_data_foundation', 'utils'))

def test_data_generation():
    """Test 1: Sample Data Generation"""
    print("🧪 TEST 1: Sample Data Generation")
    print("-" * 50)
    
    try:
        # Run data generation
        os.chdir('phase1_data_foundation')
        result = os.system('python generate_sample_data.py > ../test_output_1.txt 2>&1')
        os.chdir('..')
        
        # Check if files were created
        data_files = [
            'phase1_data_foundation/data/creditcard_small.csv',
            'phase1_data_foundation/data/creditcard_medium.csv',
            'phase1_data_foundation/data/creditcard_large.csv'
        ]
        
        all_created = True
        for file_path in data_files:
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                print(f"✅ {file_path}: {df.shape} - Fraud rate: {df['Class'].mean():.2%}")
            else:
                print(f"❌ {file_path}: Not found")
                all_created = False
        
        return all_created
        
    except Exception as e:
        print(f"❌ Error in data generation: {str(e)}")
        return False

def test_data_processing():
    """Test 2: Data Processing Module"""
    print("\n🧪 TEST 2: Data Processing Module")
    print("-" * 50)
    
    try:
        from data_processor import DataProcessor
        
        # Initialize processor
        processor = DataProcessor()
        print("✅ DataProcessor initialized")
        
        # Load test data
        data_path = 'phase1_data_foundation/data/creditcard_small.csv'
        if not os.path.exists(data_path):
            print(f"❌ Test data not found: {data_path}")
            return False
        
        df = processor.load_data(data_path)
        print(f"✅ Data loaded: {df.shape}")
        
        # Test data exploration
        exploration = processor.explore_data(df)
        print(f"✅ Data exploration completed - {len(exploration)} metrics")
        
        # Test missing value handling
        df_clean = processor.handle_missing_values(df)
        print(f"✅ Missing values handled: {df_clean.shape}")
        
        # Test outlier detection
        outliers = processor.detect_outliers(df_clean)
        print(f"✅ Outliers detected in {len(outliers)} columns")
        
        # Test categorical encoding
        df_encoded = processor.encode_categorical_features(df_clean)
        print(f"✅ Categorical encoding completed: {df_encoded.shape}")
        
        # Test data splitting
        X_train, X_test, y_train, y_test = processor.split_data(df_encoded)
        print(f"✅ Data split - Train: {X_train.shape}, Test: {X_test.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in data processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_feature_engineering():
    """Test 3: Feature Engineering Pipeline"""
    print("\n🧪 TEST 3: Feature Engineering Pipeline")
    print("-" * 50)
    
    try:
        from feature_engineer import FeatureEngineer
        
        # Initialize feature engineer
        engineer = FeatureEngineer()
        print("✅ FeatureEngineer initialized")
        
        # Load test data
        data_path = 'phase1_data_foundation/data/creditcard_small.csv'
        df = pd.read_csv(data_path)
        
        # Test temporal features
        df_temporal = engineer.create_temporal_features(df)
        print(f"✅ Temporal features created: {df_temporal.shape}")
        
        # Test amount features
        df_amount = engineer.create_amount_features(df_temporal)
        print(f"✅ Amount features created: {df_amount.shape}")
        
        # Test behavioral features
        df_behavioral = engineer.create_behavioral_features(df_amount)
        print(f"✅ Behavioral features created: {df_behavioral.shape}")
        
        # Test statistical features
        df_statistical = engineer.create_statistical_features(df_behavioral)
        print(f"✅ Statistical features created: {df_statistical.shape}")
        
        # Test feature importance
        if len(df_statistical) > 100:  # Only if enough data
            X = df_statistical.drop('Class', axis=1)
            y = df_statistical['Class']
            importance = engineer.select_features_importance(X, y, n_features=10)
            print(f"✅ Feature importance calculated: {importance.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in feature engineering: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_oversampling():
    """Test 4: ADASYN Oversampling"""
    print("\n🧪 TEST 4: ADASYN Oversampling")
    print("-" * 50)
    
    try:
        from oversampling import AdvancedOversampler
        
        # Initialize oversampler
        oversampler = AdvancedOversampler()
        print("✅ AdvancedOversampler initialized")
        
        # Load and prepare test data
        data_path = 'phase1_data_foundation/data/creditcard_small.csv'
        df = pd.read_csv(data_path)
        
        # Prepare features (simplified)
        X = df.drop('Class', axis=1).select_dtypes(include=[np.number])
        y = df['Class']
        
        print(f"Original distribution: {y.value_counts().to_dict()}")
        
        # Test class imbalance analysis
        analysis = oversampler.analyze_class_imbalance(y)
        print(f"✅ Class imbalance analyzed - Ratio: {analysis['imbalance_ratio']:.2f}")
        
        # Test ADASYN oversampling
        X_resampled, y_resampled = oversampler.adasyn_oversampling(X, y)
        print(f"✅ ADASYN completed: {X_resampled.shape}")
        print(f"New distribution: {y_resampled.value_counts().to_dict()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in oversampling: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_models():
    """Test 5: ML Models (Simplified)"""
    print("\n🧪 TEST 5: ML Models")
    print("-" * 50)
    
    try:
        from sklearn.ensemble import RandomForestClassifier, IsolationForest
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import classification_report, roc_auc_score
        
        # Load test data
        data_path = 'phase1_data_foundation/data/creditcard_small.csv'
        df = pd.read_csv(data_path)
        
        # Prepare data
        X = df.drop('Class', axis=1).select_dtypes(include=[np.number])
        y = df['Class']
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Test Random Forest (substitute for XGBoost)
        rf_model = RandomForestClassifier(n_estimators=50, random_state=42, class_weight='balanced')
        rf_model.fit(X_train, y_train)
        rf_pred = rf_model.predict(X_test)
        rf_proba = rf_model.predict_proba(X_test)[:, 1]
        
        print(f"✅ Random Forest trained and tested")
        print(f"   AUC Score: {roc_auc_score(y_test, rf_proba):.4f}")
        
        # Test Isolation Forest
        if_model = IsolationForest(contamination=0.1, random_state=42)
        if_model.fit(X_train)
        if_pred = if_model.predict(X_test)
        if_pred_binary = (if_pred == -1).astype(int)
        
        print(f"✅ Isolation Forest trained and tested")
        print(f"   Anomalies detected: {if_pred_binary.sum()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in model testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_evaluation():
    """Test 6: Model Evaluation Framework"""
    print("\n🧪 TEST 6: Model Evaluation Framework")
    print("-" * 50)
    
    try:
        from evaluation import ModelEvaluator
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        
        # Initialize evaluator
        evaluator = ModelEvaluator()
        print("✅ ModelEvaluator initialized")
        
        # Prepare test data and model
        data_path = 'phase1_data_foundation/data/creditcard_small.csv'
        df = pd.read_csv(data_path)
        X = df.drop('Class', axis=1).select_dtypes(include=[np.number])
        y = df['Class']
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train a simple model
        model = RandomForestClassifier(n_estimators=50, random_state=42, class_weight='balanced')
        model.fit(X_train, y_train)
        
        # Test basic metrics
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        basic_metrics = evaluator.calculate_basic_metrics(y_test, y_pred, y_pred_proba)
        print(f"✅ Basic metrics calculated: {len(basic_metrics)} metrics")
        
        # Test confusion matrix metrics
        cm_metrics = evaluator.calculate_confusion_matrix_metrics(y_test, y_pred)
        print(f"✅ Confusion matrix metrics calculated")
        
        # Test cost-sensitive metrics
        evaluator.set_cost_matrix()
        cost_metrics = evaluator.calculate_cost_sensitive_metrics(y_test, y_pred)
        print(f"✅ Cost-sensitive metrics calculated - Total cost: ${cost_metrics['total_cost']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in evaluation testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_explainability():
    """Test 7: Model Explainability (Simplified)"""
    print("\n🧪 TEST 7: Model Explainability")
    print("-" * 50)
    
    try:
        from explainability import ModelExplainer
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        
        # Initialize explainer
        explainer = ModelExplainer()
        print("✅ ModelExplainer initialized")
        
        # Prepare test data and model
        data_path = 'phase1_data_foundation/data/creditcard_small.csv'
        df = pd.read_csv(data_path)
        X = df.drop('Class', axis=1).select_dtypes(include=[np.number])
        y = df['Class']
        
        scaler = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train a simple model
        model = RandomForestClassifier(n_estimators=50, random_state=42, class_weight='balanced')
        model.fit(X_train, y_train)
        
        # Test permutation importance
        perm_importance = explainer.calculate_permutation_importance(X_test, y_test)
        print(f"✅ Permutation importance calculated for {len(perm_importance)} features")
        
        # Test feature importance comparison
        importance_comparison = explainer.create_feature_importance_comparison(X_test, y_test, methods=['permutation'])
        print(f"✅ Feature importance comparison completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in explainability testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """Test 8: Configuration Management"""
    print("\n🧪 TEST 8: Configuration Management")
    print("-" * 50)
    
    try:
        from config import ProjectConfig, ConfigManager
        
        # Test default configuration
        config = ProjectConfig()
        print("✅ Default configuration created")
        print(f"   Project name: {config.project_name}")
        print(f"   Log level: {config.log_level}")
        
        # Test configuration manager
        config_manager = ConfigManager()
        print("✅ ConfigManager initialized")
        
        # Test saving configuration
        test_config_path = "test_config.yaml"
        config_manager.save_config(config, test_config_path)
        print("✅ Configuration saved")
        
        # Test loading configuration
        loaded_config = config_manager.load_config(test_config_path)
        print("✅ Configuration loaded")
        
        # Cleanup
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in configuration testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_logging():
    """Test 9: Logging System"""
    print("\n🧪 TEST 9: Logging System")
    print("-" * 50)
    
    try:
        from logger import setup_logger, ProgressLogger, Timer
        
        # Test basic logger setup
        logger = setup_logger("test_logger", log_level="INFO", log_dir="test_logs")
        print("✅ Logger setup completed")
        
        # Test logging messages
        logger.info("Test info message")
        logger.warning("Test warning message")
        print("✅ Log messages sent")
        
        # Test progress logger
        progress = ProgressLogger(100, "Test Operation", log_interval=25)
        for i in range(100):
            progress.update()
        progress.complete()
        print("✅ Progress logger tested")
        
        # Test timer
        with Timer("Test Timer"):
            time.sleep(0.1)
        print("✅ Timer tested")
        
        # Cleanup
        import shutil
        if os.path.exists("test_logs"):
            shutil.rmtree("test_logs")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in logging testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_structure():
    """Test 10: API Structure (Phase 4)"""
    print("\n🧪 TEST 10: API Structure (Phase 4)")
    print("-" * 50)
    
    try:
        # Check if API files exist
        api_files = [
            'phase4_rpa_integration/api_integration/fraud_detection_api.py',
            'phase4_rpa_integration/uipath_workflows/workflow_specifications.md',
            'phase4_rpa_integration/README.md'
        ]
        
        all_exist = True
        for file_path in api_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path}: Exists")
            else:
                print(f"❌ {file_path}: Not found")
                all_exist = False
        
        # Test API imports (without running server)
        try:
            sys.path.append('phase4_rpa_integration/api_integration')
            # Just test if the file can be parsed
            with open('phase4_rpa_integration/api_integration/fraud_detection_api.py', 'r') as f:
                content = f.read()
                if 'FastAPI' in content and 'FraudDetectionAPI' in content:
                    print("✅ API structure is valid")
                else:
                    print("❌ API structure incomplete")
                    all_exist = False
        except Exception as e:
            print(f"❌ API structure test failed: {str(e)}")
            all_exist = False
        
        return all_exist
        
    except Exception as e:
        print(f"❌ Error in API structure testing: {str(e)}")
        return False

def test_end_to_end():
    """Test 11: End-to-End Integration"""
    print("\n🧪 TEST 11: End-to-End Integration")
    print("-" * 50)
    
    try:
        # Run the simple demo
        os.chdir('phase1_data_foundation')
        result = os.system('python simple_demo.py > ../test_output_e2e.txt 2>&1')
        os.chdir('..')
        
        if result == 0:
            print("✅ End-to-end demo completed successfully")
            
            # Check output file
            if os.path.exists('test_output_e2e.txt'):
                with open('test_output_e2e.txt', 'r') as f:
                    output = f.read()
                    if 'DEMO COMPLETED SUCCESSFULLY' in output:
                        print("✅ Demo output verification passed")
                        return True
                    else:
                        print("❌ Demo output verification failed")
                        return False
            else:
                print("❌ Demo output file not found")
                return False
        else:
            print("❌ End-to-end demo failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in end-to-end testing: {str(e)}")
        return False

def main():
    """Run comprehensive test suite"""
    print("🚀 COMPREHENSIVE TEST SUITE")
    print("Credit Card Fraud Detection System")
    print("=" * 60)
    
    # List of all tests
    tests = [
        ("Data Generation", test_data_generation),
        ("Data Processing", test_data_processing),
        ("Feature Engineering", test_feature_engineering),
        ("ADASYN Oversampling", test_oversampling),
        ("ML Models", test_models),
        ("Model Evaluation", test_evaluation),
        ("Model Explainability", test_explainability),
        ("Configuration Management", test_configuration),
        ("Logging System", test_logging),
        ("API Structure (Phase 4)", test_api_structure),
        ("End-to-End Integration", test_end_to_end)
    ]
    
    # Run all tests
    results = {}
    start_time = time.time()
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name}: Critical error - {str(e)}")
            results[test_name] = False
    
    # Summary
    total_time = time.time() - start_time
    passed = sum(results.values())
    total = len(results)
    
    print("\n" + "=" * 60)
    print("🏁 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"Total execution time: {total_time:.2f} seconds")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is working correctly.")
    else:
        print(f"\n⚠️  {total-passed} tests failed. Check the output above for details.")
    
    # Save results
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': total,
        'passed_tests': passed,
        'failed_tests': total - passed,
        'success_rate': passed/total*100,
        'execution_time_seconds': total_time,
        'individual_results': results
    }
    
    with open('test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\nDetailed results saved to: test_results.json")
    
    # Cleanup temporary files
    temp_files = ['test_output_1.txt', 'test_output_e2e.txt']
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    main()
