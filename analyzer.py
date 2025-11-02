"""Main data quality analyzer orchestrator."""

import pandas as pd
import numpy as np
from metrics.completeness import analyze_completeness
from metrics.description_quality import analyze_description_quality
from metrics.code_analysis import analyze_code_distribution
from metrics.classifier_readiness import analyze_classifier_readiness
from config import WEIGHTS, get_quality_level

class DataQualityAnalyzer:
    """Main analyzer class that coordinates all quality checks."""
    
    def __init__(self, df, product_id_col=None, description_col=None, code_cols=None):
        """
        Initialize analyzer with dataframe and column mappings.
        
        Args:
            df: pandas DataFrame
            product_id_col: name of product ID column
            description_col: name of description column
            code_cols: list of code column names
        """
        self.df = df
        self.product_id_col = product_id_col or self._detect_product_id_col()
        self.description_col = description_col or self._detect_description_col()
        self.code_cols = code_cols or self._detect_code_cols()
        
        self.results = {}
    
    def _detect_product_id_col(self):
        """Auto-detect product ID column."""
        candidates = [col for col in self.df.columns if 'id' in col.lower() or 'product' in col.lower()]
        return candidates[0] if candidates else self.df.columns[0]
    
    def _detect_description_col(self):
        """Auto-detect description column."""
        candidates = [col for col in self.df.columns if 'desc' in col.lower() or 'name' in col.lower()]
        return candidates[0] if candidates else self.df.columns[1]
    
    def _detect_code_cols(self):
        """Auto-detect code columns."""
        exclude = [self.product_id_col, self.description_col]
        return [col for col in self.df.columns if col not in exclude]
    
    def analyze_all(self):
        """Run all quality analyses."""
        print("Running completeness analysis...")
        self.results["completeness"] = analyze_completeness(
            self.df, self.product_id_col, self.description_col, self.code_cols
        )
        
        print("Running description quality analysis...")
        self.results["description_quality"] = analyze_description_quality(
            self.df, self.description_col
        )
        
        print("Running code distribution analysis...")
        self.results["code_distribution"] = analyze_code_distribution(
            self.df, self.code_cols
        )
        
        print("Running classifier readiness analysis...")
        self.results["classifier_readiness"] = analyze_classifier_readiness(
            self.df, self.description_col, self.code_cols
        )
        
        # Calculate overall quality score
        self.results["overall"] = self._calculate_overall_score()
        
        return self.results
    
    def _calculate_overall_score(self):
        """Calculate weighted overall quality score."""
        scores = {
            "completeness": self.results["completeness"]["overall_score"],
            "description_quality": self.results["description_quality"]["overall_score"],
            "code_distribution": self.results["code_distribution"]["overall_score"],
            "classifier_readiness": self.results["classifier_readiness"]["overall_score"]
        }
        
        overall = sum(scores[k] * WEIGHTS[k] for k in scores.keys())
        
        return {
            "overall_score": round(overall, 2),
            "quality_level": get_quality_level(overall),
            "component_scores": scores
        }
    
    def get_summary(self):
        """Get executive summary of quality analysis."""
        if not self.results:
            self.analyze_all()
        
        return {
            "dataset_info": {
                "total_rows": len(self.df),
                "total_columns": len(self.df.columns),
                "product_id_column": self.product_id_col,
                "description_column": self.description_col,
                "code_columns": self.code_cols
            },
            "overall_quality": self.results["overall"],
            "critical_issues": self._get_critical_issues()
        }
    
    def _get_critical_issues(self):
        """Extract critical issues from all analyses."""
        issues = []
        
        # Completeness issues
        comp = self.results["completeness"]
        for col, metrics in comp["column_completeness"].items():
            if metrics["completeness_pct"] < 80:
                issues.append(f"Low completeness in {col}: {metrics['completeness_pct']:.1f}%")
        
        # Description issues
        desc = self.results["description_quality"]
        if desc["quality_flags"]["too_short_pct"] > 10:
            issues.append(f"{desc['quality_flags']['too_short_pct']:.1f}% of descriptions are too short")
        
        # Classifier issues
        issues.extend(self.results["classifier_readiness"]["data_quality_issues"])
        
        return issues[:10]  # Return top 10 issues
