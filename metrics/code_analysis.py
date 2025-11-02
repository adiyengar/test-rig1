"""Code distribution and pattern analysis."""

import pandas as pd
import numpy as np
from itertools import combinations

def analyze_code_distribution(df, code_cols, rare_threshold=0.005):
    """
    Analyze distribution and patterns in categorization codes.
    
    Returns:
        dict: Code distribution metrics
    """
    total_rows = len(df)
    results = {
        "code_columns": {},
        "co_occurrence": {},
        "overall_score": 0
    }
    
    # Analyze each code column
    for col in code_cols:
        code_values = df[col].dropna()
        value_counts = code_values.value_counts()
        
        # Identify rare codes
        rare_codes = value_counts[value_counts < (total_rows * rare_threshold)]
        
        results["code_columns"][col] = {
            "unique_codes": len(value_counts),
            "most_common": value_counts.head(10).to_dict(),
            "rare_codes_count": len(rare_codes),
            "rare_codes": rare_codes.to_dict() if len(rare_codes) <= 20 else dict(list(rare_codes.items())[:20]),
            "distribution_entropy": round(calculate_entropy(value_counts), 4),
            "top_code_concentration": round((value_counts.iloc[0] / total_rows) * 100, 2) if len(value_counts) > 0 else 0
        }
    
    # Code co-occurrence analysis (for first 3 code pairs to avoid explosion)
    for col1, col2 in list(combinations(code_cols[:3], 2)):
        pair_counts = df.groupby([col1, col2]).size().sort_values(ascending=False)
        key = f"{col1}_x_{col2}"
        results["co_occurrence"][key] = {
            "unique_combinations": len(pair_counts),
            "top_combinations": pair_counts.head(10).to_dict()
        }
    
    # Calculate distribution quality score
    entropies = [v["distribution_entropy"] for v in results["code_columns"].values()]
    avg_entropy = np.mean(entropies) if entropies else 0
    
    # Higher entropy (more balanced distribution) is better, max entropy for codes is typically 4-6
    results["overall_score"] = round(min((avg_entropy / 5) * 100, 100), 2)
    
    return results

def calculate_entropy(value_counts):
    """Calculate Shannon entropy for distribution."""
    probabilities = value_counts / value_counts.sum()
    return -np.sum(probabilities * np.log2(probabilities + 1e-10))
