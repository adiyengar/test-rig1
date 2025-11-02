"""Description quality analysis for semantic classification."""

import pandas as pd
import numpy as np
from collections import Counter
import re

def analyze_description_quality(df, description_col, min_length=20):
    """
    Analyze quality of product descriptions.
    
    Returns:
        dict: Description quality metrics and scores
    """
    descriptions = df[description_col].dropna().astype(str)
    
    # Length statistics
    lengths = descriptions.str.len()
    
    # Vocabulary analysis
    all_words = ' '.join(descriptions).lower().split()
    unique_words = len(set(all_words))
    total_words = len(all_words)
    
    # Find duplicates
    duplicate_descriptions = descriptions.value_counts()
    duplicates = duplicate_descriptions[duplicate_descriptions > 1]
    
    # Quality checks
    too_short = (lengths < min_length).sum()
    mostly_numeric = descriptions.str.replace(r'[^0-9]', '', regex=True).str.len() / lengths > 0.5
    high_special_chars = descriptions.str.replace(r'[a-zA-Z0-9\s]', '', regex=True).str.len() / lengths > 0.3
    
    results = {
        "length_stats": {
            "mean": round(lengths.mean(), 2),
            "median": round(lengths.median(), 2),
            "min": int(lengths.min()),
            "max": int(lengths.max()),
            "std": round(lengths.std(), 2)
        },
        "vocabulary": {
            "unique_words": unique_words,
            "total_words": total_words,
            "vocabulary_richness": round(unique_words / total_words, 4) if total_words > 0 else 0
        },
        "quality_flags": {
            "too_short": int(too_short),
            "too_short_pct": round((too_short / len(descriptions)) * 100, 2),
            "mostly_numeric": int(mostly_numeric.sum()),
            "high_special_chars": int(high_special_chars.sum())
        },
        "duplicates": {
            "duplicate_count": len(duplicates),
            "total_duplicate_rows": int(duplicates.sum() - len(duplicates)),
            "top_duplicates": duplicates.head(10).to_dict()
        },
        "overall_score": 0
    }
    
    # Calculate quality score
    score = 100
    score -= min((too_short / len(descriptions)) * 100, 30)  # Max 30 point penalty
    score -= min(len(duplicates) / len(descriptions) * 100, 20)  # Max 20 point penalty
    score -= min((mostly_numeric.sum() / len(descriptions)) * 100, 20)  # Max 20 point penalty
    
    results["overall_score"] = round(max(score, 0), 2)
    
    return results
