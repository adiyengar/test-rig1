"""Configuration constants for the data quality analyzer."""

# Column name expectations
PRODUCT_ID_COLUMN = "product_id"
DESCRIPTION_COLUMN = "description"
CODE_COLUMNS = ["code_1", "code_2", "code_3", "code_4", "code_5", "code_6", "code_7"]

# Quality thresholds
MIN_DESCRIPTION_LENGTH = 20
MIN_TRAINING_SAMPLES = 50
RARE_CODE_THRESHOLD = 0.005  # 0.5% of total rows
OUTLIER_STD_DEV = 3

# Scoring weights (must sum to 1.0)
WEIGHTS = {
    "completeness": 0.30,
    "description_quality": 0.30,
    "code_distribution": 0.20,
    "classifier_readiness": 0.20
}

# Visual styling
QUALITY_COLORS = {
    "excellent": "#28a745",  # Green
    "good": "#7cb342",       # Light green
    "fair": "#ffc107",       # Yellow
    "poor": "#ff9800",       # Orange
    "critical": "#dc3545"    # Red
}

def get_quality_level(score):
    """Convert numeric score to quality level."""
    if score >= 90:
        return "excellent"
    elif score >= 75:
        return "good"
    elif score >= 60:
        return "fair"
    elif score >= 40:
        return "poor"
    else:
        return "critical"
