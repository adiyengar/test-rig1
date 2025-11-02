"""Machine learning classifier readiness analysis."""

import pandas as pd
import numpy as np

def analyze_classifier_readiness(df, description_col, code_cols, min_samples=50):
    """
    Analyze if data is ready for training a semantic classifier.
    
    Returns:
        dict: Classifier readiness metrics
    """
    results = {
        "per_code_column": {},
        "training_viability": {},
        "data_quality_issues": [],
        "overall_score": 0
    }
    
    # Analyze each code column as a potential classification target
    for col in code_cols:
        # Remove rows with missing codes or descriptions
        valid_data = df[[description_col, col]].dropna()
        
        if len(valid_data) == 0:
            results["per_code_column"][col] = {
                "status": "insufficient_data",
                "unique_classes": 0,
                "ready_for_training": False
            }
            continue
        
        # Class distribution
        class_counts = valid_data[col].value_counts()
        classes_with_min_samples = (class_counts >= min_samples).sum()
        
        # Description uniqueness per code
        desc_per_code = valid_data.groupby(col)[description_col].agg(['count', 'nunique'])
        avg_unique_desc_ratio = (desc_per_code['nunique'] / desc_per_code['count']).mean()
        
        # Check for ambiguous descriptions (same description, different codes)
        ambiguous = valid_data.groupby(description_col)[col].nunique()
        ambiguous_descriptions = (ambiguous > 1).sum()
        
        results["per_code_column"][col] = {
            "total_samples": len(valid_data),
            "unique_classes": len(class_counts),
            "classes_with_sufficient_data": int(classes_with_min_samples),
            "classes_needing_more_data": int(len(class_counts) - classes_with_min_samples),
            "min_class_size": int(class_counts.min()),
            "max_class_size": int(class_counts.max()),
            "median_class_size": int(class_counts.median()),
            "class_imbalance_ratio": round(class_counts.max() / class_counts.min(), 2) if class_counts.min() > 0 else float('inf'),
            "avg_description_uniqueness": round(avg_unique_desc_ratio, 4),
            "ambiguous_descriptions": int(ambiguous_descriptions),
            "ready_for_training": classes_with_min_samples >= max(2, len(class_counts) * 0.7),
            "recommended_train_test_split": calculate_split_recommendation(class_counts, min_samples)
        }
    
    # Overall training viability
    ready_columns = sum(1 for v in results["per_code_column"].values() if v.get("ready_for_training", False))
    results["training_viability"] = {
        "columns_ready": ready_columns,
        "columns_not_ready": len(code_cols) - ready_columns,
        "readiness_pct": round((ready_columns / len(code_cols)) * 100, 2)
    }
    
    # Identify critical issues
    for col, metrics in results["per_code_column"].items():
        if metrics.get("ambiguous_descriptions", 0) > 10:
            results["data_quality_issues"].append(
                f"{col}: {metrics['ambiguous_descriptions']} ambiguous descriptions (same text, different codes)"
            )
        if metrics.get("class_imbalance_ratio", 0) > 100:
            results["data_quality_issues"].append(
                f"{col}: Severe class imbalance (ratio: {metrics['class_imbalance_ratio']:.1f})"
            )
    
    # Calculate overall readiness score
    results["overall_score"] = round(results["training_viability"]["readiness_pct"], 2)
    
    return results

def calculate_split_recommendation(class_counts, min_samples):
    """Recommend train/test split based on smallest class size."""
    smallest_class = class_counts.min()
    
    if smallest_class < min_samples:
        return "Insufficient data - collect more samples"
    elif smallest_class < min_samples * 2:
        return "90/10 split (limited data)"
    elif smallest_class < min_samples * 3:
        return "80/20 split (recommended)"
    else:
        return "70/30 or 80/20 split"
