# ⚡ Quick Start Guide

## Run Your Data Quality Analyzer Now!

### Step 1: Start the App
```bash
cd /Users/adisheshiyengar/Documents/data-quality-analyzer
source venv/bin/activate
streamlit run app.py
```

### Step 2: Open Browser
Go to: **http://localhost:8501**

### Step 3: Upload Your File
1. Click "Upload Excel or CSV file"
2. Drag & drop or browse for your file
3. Select column mappings
4. Click "🚀 Run Analysis"

### Step 4: Explore Results
View in 6 interactive tabs:
- 📈 Executive Summary - Overall quality score
- ✅ Completeness - Data coverage analysis
- 📝 Description Quality - Text quality metrics
- 🔢 Code Distribution - Category analysis
- 🤖 Classifier Readiness - ML viability
- 📥 Export Report - Download results

## What Visualizations You'll See

✅ **Bar Charts**: Column completeness, code distributions  
✅ **Pie Charts**: Code coverage breakdown  
✅ **Color-coded Metrics**: Quality indicators  
✅ **Interactive Tables**: Detailed statistics  
✅ **Export Options**: JSON & CSV downloads  

## Sample Data

A sample CSV is available at: `sample_data.csv`

Try it out to see all features in action!

## Push to GitHub

1. Create repo at: https://github.com/new
2. Name it: `data-quality-analyzer`
3. Run these commands:

```bash
git remote add origin https://github.com/YOUR_USERNAME/data-quality-analyzer.git
git push -u origin main
```

## Deploy to Streamlit Cloud

1. Push to GitHub
2. Visit: https://share.streamlit.io/
3. Connect your repo
4. Deploy! (5 minutes)

Your app will be live with a public URL! 🚀

---

**Need help?** Check `GITHUB_SETUP.md` for detailed instructions.
