# Quick Start Guide: Two-Team Semantic Search Optimization

## What You Have Now

You have a complete demo suite for optimizing your semantic search system using a two-team approach:

### 📊 Index Management Team Tool (Your Existing)
- **File:** `app.py` (Your Data Quality Analyzer)
- **Purpose:** Manage lookup index quality
- **URL:** https://test-rig1-n5fnqef5pxnjvayjhljumm.streamlit.app/

### 🧪 Input Embedding Team Tool (New)
- **Files:** 
  - `input_embedding_app.py` (Main app)
  - `embedding_experimenter.py` (Core logic)
  - `config.py` (Configuration)
  - `requirements_input_tool.txt` (Dependencies)
- **Purpose:** Optimize input embedding strategy

## How to Demo This

### Option 1: Show Them Separately (Recommended for First Demo)

**Part 1: Index Side (3-5 minutes)**
1. Open your existing tool: https://test-rig1-n5fnqef5pxnjvayjhljumm.streamlit.app/
2. Upload sample product catalog
3. Show data quality metrics
4. Point out: "This is what the Index Management Team uses"
5. Highlight: coverage gaps, data quality issues, distribution problems

**Part 2: Input Side (3-5 minutes)**
1. Run the new tool locally:
   ```bash
   cd /path/to/files
   pip install -r requirements_input_tool.txt
   streamlit run input_embedding_app.py
   ```
2. Upload same product catalog + ground truth
3. Show feature selection analysis
4. Demo template designer with live preview
5. Point out: "This is what the Input Embedding Team uses"

**Part 3: The Story (2 minutes)**
- "These two teams work on the same goal: high prediction accuracy"
- "Index team ensures we have the right things to find"
- "Input team ensures we're asking in the right way"
- "Together they drive accuracy from 67% to 85%+"

### Option 2: Deploy Both and Show Side-by-Side

Deploy the input embedding tool to Streamlit Cloud:
1. Create a new GitHub repo for the input tool
2. Push these files:
   - `input_embedding_app.py`
   - `embedding_experimenter.py`
   - `config.py`
   - `requirements_input_tool.txt`
3. Deploy on Streamlit Cloud
4. Demo both URLs side-by-side in different browser tabs

### Option 3: Build a Unified Demo App

Create a single app with navigation:
```python
# combined_app.py
import streamlit as st

page = st.sidebar.radio("Select Tool", ["Index Quality", "Input Optimization"])

if page == "Index Quality":
    # Your existing app code
    pass
elif page == "Input Optimization":
    # New app code
    pass
```

## Demo Script

### Introduction (1 minute)
"We have a semantic search engine that predicts product codes. Currently 67% accurate. We want to get to 85%+. The key insight is that this is actually TWO optimization problems, requiring TWO teams."

### Problem Statement (2 minutes)
Show the system diagram:
```
INPUT SIDE                 LOOKUP SIDE
────────────               ───────────
New Product                Index Database
     ↓                            ↓
Features +                  Clean Data +
Template                    Good Coverage
     ↓                            ↓
INPUT EMBEDDING            INDEX EMBEDDINGS
     ↓                            ↓
     └────→ SEMANTIC SEARCH ←─────┘
                  ↓
              PREDICTION
```

"If the index is messy → bad matches, no matter how good the input is"
"If the input is poor → bad matches, no matter how clean the index is"
"We need both sides optimized"

### Index Side Demo (3 minutes)
1. Open data quality analyzer
2. Upload sample data
3. Show: "See these coverage gaps? Missing categories?"
4. Show: "See this data quality? Only 60% complete?"
5. "This is why predictions fail. The Index Team fixes this."

### Input Side Demo (3 minutes)
1. Open input embedding tool
2. Show feature selection: "Currently only using description"
3. Add category, brand, material
4. Show completeness analysis
5. Design a template with preview
6. "The Input Team finds the best feature combinations"

### Results (2 minutes)
Show the comparison:
- Baseline (description only): 67%
- After index cleanup: 72%
- After input optimization: 78%
- After both: 85%+

### Call to Action (1 minute)
"This demo shows the foundation. To implement:
1. Set up two teams with clear responsibilities
2. Give them these tools
3. Track metrics weekly
4. Watch accuracy improve over 3 months"

## Next Steps After Demo

### If They Want to See It Working
1. Get their actual data (sample of 1000 products)
2. Get ground truth (50-100 test cases)
3. Run real experiments
4. Show actual accuracy improvements

### If They Want to Implement
1. Share the Jobs-to-be-Done document
2. Help them set up teams
3. Deploy both tools
4. Train teams on usage
5. Set up weekly metrics tracking

### If They Want to Customize
1. Connect to their actual embedding model
2. Integrate with their databases
3. Add their specific metrics
4. Customize for their domain

## Making It Production-Ready

The current tools are **demos** with simulated results. To make them production-ready:

### For Index Tool (Already Mostly Ready)
- Already analyzes real data
- Add: Export to database
- Add: Scheduled analysis
- Add: Alerting on quality drops

### For Input Tool (Needs Real Integration)
Replace these placeholders:

```python
# In embedding_experimenter.py

# Current (placeholder):
def run_experiment(self, ...):
    # Simulated results
    results = {"accuracy": 75.0}
    return results

# Replace with real:
def run_experiment(self, ...):
    # Generate real embeddings
    embeddings = your_model.encode(texts)
    # Do real semantic search
    predictions = your_search_engine.search(embeddings)
    # Calculate real accuracy
    accuracy = calculate_accuracy(predictions, ground_truth)
    return {"accuracy": accuracy}
```

## Tips for a Great Demo

1. **Have sample data ready:** Don't make them wait while you find files
2. **Show real problems:** Use messy data to make the point
3. **Keep it visual:** Charts and colors are more compelling than numbers
4. **Tell a story:** "Here's the problem → Here's the solution → Here's the impact"
5. **Be ready to go deeper:** Have the Jobs-to-be-Done doc ready
6. **Show quick wins:** "In week 1, you'll see these improvements"
7. **Be honest about limitations:** "This is a demo, production needs X, Y, Z"

## Sample Data You Can Use

If you don't have real data ready, create sample data:

```python
import pandas as pd
import numpy as np

# Sample catalog
products = []
for i in range(1000):
    products.append({
        "product_id": f"P{i:04d}",
        "description": f"Product {i} description...",
        "category": np.random.choice(["A", "B", "C", "D"]),
        "brand": np.random.choice(["Brand1", "Brand2", "Brand3"]),
        "material": np.random.choice(["Steel", "Plastic", "Wood"]),
        "weight": np.random.uniform(1, 100),
        "color": np.random.choice(["Red", "Blue", "Green", "Gray"]),
        # Add 40+ more columns...
    })

catalog_df = pd.DataFrame(products)
catalog_df.to_excel("sample_catalog.xlsx", index=False)

# Sample ground truth
ground_truth = catalog_df.sample(100)[["product_id", "description"]].copy()
ground_truth["input_description"] = ground_truth["description"] # Simplified
ground_truth["correct_code"] = ["A123"] * 100  # Dummy correct codes
ground_truth.to_excel("sample_ground_truth.xlsx", index=False)
```

## Files Included

1. **input_embedding_app.py** - Main Streamlit application
2. **embedding_experimenter.py** - Core experiment logic
3. **config.py** - Configuration matching your existing tool
4. **requirements_input_tool.txt** - Python dependencies
5. **README_INPUT_TOOL.md** - Detailed documentation
6. **THIS FILE** - Quick start guide

## Questions?

Common questions and answers:

**Q: Do I need to rebuild my existing data quality analyzer?**
A: No! Keep using it as-is. This new tool complements it.

**Q: Can these tools share data?**
A: Yes, they both read from the same product catalog.

**Q: How long to set up?**
A: 10 minutes to run locally, 30 minutes to deploy to cloud.

**Q: Is this production-ready?**
A: The index tool is close. The input tool needs real embedding integration.

**Q: Can I customize the UI?**
A: Yes! It's Streamlit - easy to modify colors, layouts, metrics.

## Success Criteria

You'll know the demo was successful if they:
1. Understand the two-team model
2. See the value of both tools
3. Want to try it with their data
4. Ask about implementation timeline
5. Request the Jobs-to-be-Done document

Good luck with your demo! 🚀
