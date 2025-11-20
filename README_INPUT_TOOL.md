# Input Embedding Experiment Tool

A companion tool to the Data Quality Analyzer for optimizing input embeddings in semantic search systems.

## Overview

While the **Data Quality Analyzer** focuses on the lookup index (ensuring clean, complete, well-distributed reference data), this **Input Embedding Experiment Tool** focuses on the input side: selecting the best features and templates to represent incoming products as embeddings.

## Two-Team Model

### Your Existing Tool: Index Management Team
- **Tool:** `app.py` (Data Quality Analyzer)
- **Focus:** Lookup index quality
- **Jobs:**
  - Ensure representative coverage
  - Maintain data quality
  - Optimize index embeddings
  - Curate index contents

### This New Tool: Input Embedding Team
- **Tool:** `input_embedding_app.py` 
- **Focus:** Input embedding optimization
- **Jobs:**
  - Feature selection from 40+ columns
  - Template design and testing
  - Pipeline optimization
  - Performance analysis

## Features

### 🔬 Feature Selection
- Select text, categorical, and numerical features
- Analyze feature completeness and uniqueness
- Visualize information density
- Save feature combinations for testing

### 📝 Template Designer
- Multiple template strategies:
  - Simple Concatenation
  - Weighted Fields
  - Structured Prompt
  - Question-Answer Format
  - Custom Templates
- Live preview with sample data
- Save and compare templates

### 📊 Experiment Results
- Compare accuracy across configurations
- Track Top-1, Top-3, Top-5 accuracy
- Feature importance analysis
- Visual comparisons

### 💾 Saved Experiments
- Manage feature configurations
- Store template designs
- Track experiment history

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements_input_tool.txt
   ```

2. Run the application:
   ```bash
   streamlit run input_embedding_app.py
   ```

3. Open your browser to `http://localhost:8501`

## Usage

### Step 1: Upload Data
- **Product Catalog**: Your full catalog with all 40+ columns
- **Ground Truth**: Test products with known correct predictions

### Step 2: Configure Columns
- Select Product ID column
- Select primary Description column

### Step 3: Experiment with Features
- Go to "Feature Selection" tab
- Choose text, categorical, and numerical features
- View completeness and uniqueness analysis
- Save promising feature sets

### Step 4: Design Templates
- Go to "Template Designer" tab
- Choose a template strategy
- Select features to include
- Configure template parameters
- Preview with sample data
- Save templates

### Step 5: Run Experiments
- Go to "Experiment Results" tab
- Run experiments with your configurations
- Compare accuracy across different approaches
- Identify winning combinations

### Step 6: Review Saved Experiments
- Go to "Saved Experiments" tab
- Review all configurations
- Delete underperforming experiments
- Export results

## Data Format

### Product Catalog
Should contain all available product data:
```
product_id | description | category | brand | material | weight | color | ... (40+ columns)
P001       | Widget A    | Industrial | BrandX | Steel    | 5.2    | Gray  | ...
```

### Ground Truth
Products with known correct predictions for testing:
```
product_id | input_description      | correct_code
P001       | industrial widget      | A123
P002       | consumer gadget        | B456
```

## Integration with Data Quality Analyzer

These tools work together:

1. **Use Data Quality Analyzer** to:
   - Audit your lookup index
   - Clean and enrich data
   - Ensure balanced coverage
   - Optimize index embeddings

2. **Use Input Embedding Tool** to:
   - Find best features from clean data
   - Design optimal templates
   - Test different strategies
   - Maximize prediction accuracy

3. **Collaborate:**
   - Share insights between teams
   - Coordinate experiments
   - Track combined improvements
   - Measure overall system accuracy

## Technical Notes

### Current Implementation
This is a **prototype/demo version** with:
- Simulated embedding generation (placeholder)
- Mock accuracy calculations
- Template preview functionality
- Feature analysis on real data

### Production Implementation
To make this production-ready, you need to:

1. **Connect to your embedding model:**
   ```python
   # Replace placeholder in embedding_experimenter.py
   def generate_embedding(text):
       # Your actual embedding code
       return model.encode(text)
   ```

2. **Implement real semantic search:**
   ```python
   def find_nearest_neighbors(query_embedding, index_embeddings):
       # Your actual search code
       return search_index(query_embedding, k=5)
   ```

3. **Calculate true accuracy:**
   ```python
   def evaluate_predictions(predictions, ground_truth):
       # Your actual evaluation code
       return calculate_metrics(predictions, ground_truth)
   ```

## Workflow Example

### Week 1: Baseline
1. Use Data Quality Analyzer on index
2. Note current accuracy: 67%
3. Use Input Embedding Tool with just description
4. Confirm baseline: 67%

### Week 2: Feature Experimentation
1. Test adding category → 72% accuracy
2. Test adding brand → 74% accuracy
3. Test adding material → 75% accuracy
4. Best combination: description + category + brand + material

### Week 3: Template Optimization
1. Test simple concatenation → 75%
2. Test weighted (emphasize category) → 78%
3. Test structured prompt → 76%
4. Best: weighted template with category emphasis

### Week 4: Refinement
1. Index team improves data quality
2. Input team optimizes feature handling
3. Combined accuracy reaches 82%

## File Structure

```
input-embedding-tool/
├── input_embedding_app.py      # Main Streamlit application
├── embedding_experimenter.py   # Core experiment logic
├── config.py                    # Configuration and constants
├── requirements_input_tool.txt  # Python dependencies
└── README.md                    # This file
```

## Tips for Success

1. **Start Simple:** Begin with just description, then add features incrementally
2. **Measure Everything:** Run experiments for every change
3. **Use Real Data:** Ground truth is critical for accurate results
4. **Iterate Quickly:** Test hypotheses fast, don't overthink
5. **Document Findings:** Save successful configurations
6. **Collaborate:** Share insights with the index team

## Extending the Tool

### Add Your Own Template Strategy
Edit `input_embedding_app.py`:
```python
elif template_strategy == "Your Custom Strategy":
    # Your template logic here
    return generated_text
```

### Add Custom Metrics
Edit `embedding_experimenter.py`:
```python
def run_experiment(self, ...):
    results = {
        # ... existing metrics
        "your_custom_metric": calculate_your_metric()
    }
    return results
```

### Connect to Your Systems
```python
# Connect to your database
def load_catalog_from_db():
    return pd.read_sql("SELECT * FROM products", connection)

# Connect to your embedding service
def generate_embeddings_batch(texts):
    return embedding_service.embed(texts)
```

## Troubleshooting

**Q: No results showing in Experiment Results?**
A: You need to upload ground truth data and run at least one experiment

**Q: Preview not showing correctly?**
A: Check that selected features exist in your sample row and have non-null values

**Q: Can't save experiments?**
A: Experiments are stored in session state - they'll reset when you refresh the page. For persistence, implement database storage.

## Next Steps

1. Test with your actual data
2. Connect to your real embedding model
3. Implement true accuracy calculation
4. Deploy alongside your Data Quality Analyzer
5. Set up your two teams and start improving!

## Support

This tool complements the semantic search optimization strategy outlined in the Jobs-to-be-Done document. Use both tools together for maximum impact.
