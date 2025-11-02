
# Data Quality Analyzer

A comprehensive web application for analyzing product catalog data quality and assessing readiness for semantic classification.

## Features

- **Completeness Analysis**: Track missing values and data coverage across all columns
- **Description Quality**: Evaluate text quality for semantic classification
- **Code Distribution**: Analyze categorization code patterns and balance
- **Classifier Readiness**: Assess if data is ready for machine learning training
- **Interactive Dashboard**: Beautiful Streamlit interface with visualizations
- **Export Reports**: Download analysis results in JSON or CSV format

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```
2. Open your browser to `http://localhost:8501`
3. Upload your Excel or CSV file
4. Map columns (Product ID, Description, Code columns)
5. Click "Run Analysis"
6. Explore results in interactive tabs

## Data Format

Your file should contain:
- **Product ID**: Unique identifier for each product
- **Description**: Text description for semantic classification
- **Code Columns**: 1-20 categorization code columns (alphanumeric)

Example:
| product_id | description | code_1 | code_2 | ... |
|------------|-------------|--------|--------|-----|
| P001 | Widget A | A123 | X01 | ... |

## Metrics Explained

### Completeness (30% weight)
- Missing value analysis per column
- Row-level code coverage
- Overall data coverage score

### Description Quality (30% weight)
- Length statistics
- Vocabulary richness
- Duplicate descriptions
- Quality flags (too short, mostly numeric, special characters)

### Code Distribution (20% weight)
- Unique code counts
- Rare code detection
- Distribution entropy (balance)
