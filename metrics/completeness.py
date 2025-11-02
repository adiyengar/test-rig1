"""Completeness analysis for data quality."""

import pandas as pd
import numpy as np

def analyze_completeness(df, product_id_col, description_col, code_cols):
    """
    Analyze data completeness across all columns.
    
    Returns:
        dict: Completeness metrics and scores
    """
    total_rows = len(df)
    results = {
        "total_rows": total_rows,
        "column_completeness": {},
        "row_completeness": {},
        "overall_score": 0
    }
    
    # Completeness per column
    for col in [product_id_col, description_col] + code_cols:
        non_null = df[col].notna().sum()
        non_empty = df[col].astype(str).str.strip().ne('').sum()
        completeness_pct = (non_empty / total_rows) * 100
        
        results["column_completeness"][col] = {
            "non_null_count": int(non_null),
            "non_empty_count": int(non_empty),
            "completeness_pct": round(completeness_pct, 2),
            "missing_count": int(total_rows - non_empty)
        }
    
    # Row-level completeness for codes
    code_data = df[code_cols]
    code_completeness = code_data.notna().sum(axis=1)
    
    results["row_completeness"] = {
        "all_codes_present": int((code_completeness == len(code_cols)).sum()),
        "no_codes_present": int((code_completeness == 0).sum()),
        "partial_codes": int(((code_completeness > 0) & (code_completeness < len(code_cols))).sum()),
        "avg_codes_per_row": round(code_completeness.mean(), 2)
    }
    
    # Calculate overall completeness score
    all_completeness = [v["completeness_pct"] for v in results["column_completeness"].values()]
    results["overall_score"] = round(np.mean(all_completeness), 2)
    
    return results
