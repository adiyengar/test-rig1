# Quick Reference Card: Two-Team Semantic Search Demo

## 🎯 The Pitch (30 seconds)
"We optimize semantic search using TWO teams working in parallel:
- **Index Team** ensures we have the right things to find
- **Input Team** ensures we're asking in the right way
Together, they drive accuracy from 67% → 85%+ in 3 months"

---

## 🛠️ The Tools

| Tool | Team | What It Does | Status |
|------|------|--------------|--------|
| **Data Quality Analyzer** | Index | Audit index quality, coverage, distribution | ✅ Deployed |
| **Input Embedding Tool** | Input | Test features, design templates, optimize | 📦 Ready to deploy |

---

## 📊 The Demo (10 min)

### Intro (1 min)
Problem: 67% accuracy, need 85%+  
Insight: Two distinct optimization problems

### Index Tool (3 min)
- Open: https://test-rig1-n5fnqef5pxnjvayjhljumm.streamlit.app/
- Show: Coverage gaps, data quality issues
- Message: "Messy index = bad predictions"

### Input Tool (3 min)
- Open: `streamlit run input_embedding_app.py`
- Show: 40+ columns, template designer, live preview
- Message: "Poor inputs = bad predictions"

### Solution (2 min)
- Show: Jobs-to-be-Done document
- Explain: Two teams, clear roles, shared goal
- Timeline: 3 months to 85%+ accuracy

### Close (1 min)
Next steps, ROI, implementation plan

---

## 💡 Key Messages

1. **"It's Two Problems"** - Not one optimization, but two distinct challenges
2. **"Parallel Progress"** - Teams work simultaneously without blocking
3. **"Measurable Impact"** - Weekly metrics, monthly reviews, clear ROI
4. **"Reusable Investment"** - Tools and processes work for any catalog

---

## 📁 Files to Have Ready

✅ `semantic_search_teams_jtbd.md` - Team structure & jobs  
✅ `QUICK_START_DEMO_GUIDE.md` - Detailed demo script  
✅ `sample_catalog.xlsx` - Demo data (run generate_sample_data.py)  
✅ `sample_ground_truth.xlsx` - Test cases  
✅ Both tools tested and working  

---

## 🎓 Questions You'll Get

**Q: Why two teams instead of one?**  
A: Different skill sets, different problems, parallel progress

**Q: How long to see results?**  
A: Week 1 baseline, Month 1 first improvements, Month 3 target accuracy

**Q: What if we don't have ground truth data?**  
A: Start building it now - crucial for any ML optimization

**Q: Is this only for semantic search?**  
A: Core principles apply to any two-sided matching problem

**Q: What's the team size?**  
A: Start with 3-4 per team, can scale up or down

---

## 📈 Success Metrics

| Metric | Baseline | Target | Impact |
|--------|----------|--------|--------|
| Accuracy | 67% | 85%+ | +18% |
| Top-3 | 82% | 95%+ | +13% |
| Manual corrections | High | Minimal | -70% |
| Index coverage | 85% | 98%+ | +13% |
| Data completeness | 65% | 95%+ | +30% |

---

## 🚀 Next Steps

### After Successful Demo:
1. ✅ Share complete package
2. ✅ Get their actual data  
3. ✅ Run baseline experiment
4. ✅ Propose 3-month pilot
5. ✅ Define team structure

### To Deploy:
```bash
# Generate sample data
python generate_sample_data.py

# Run locally
pip install -r requirements_input_tool.txt
streamlit run input_embedding_app.py

# Or deploy to cloud
# Push to GitHub → share.streamlit.io → Deploy
```

---

## 🎬 Opening Lines

**Version 1 (Problem-first):**
"Your semantic search is at 67% accuracy. You need 85%. The reason it's stuck? You're trying to solve two problems with one team. Let me show you a better way..."

**Version 2 (Value-first):**  
"What if I told you we could get your semantic search from 67% to 85% accuracy in 3 months, with a clear path, defined roles, and measurable progress? Here's how..."

**Version 3 (Question-first):**
"Quick question: When a prediction is wrong, is it because you have bad data in your index, or because you're not describing the product correctly? Answer: Both. That's why you need two teams..."

---

## 📞 Contact & Resources

- Demo files: `/mnt/user-data/outputs/`
- Existing tool: https://test-rig1-n5fnqef5pxnjvayjhljumm.streamlit.app/
- Full docs: See COMPLETE_DEMO_SUITE_SUMMARY.md
- Ready to deploy: All files included

---

**Remember:** Show enthusiasm, be confident, connect to business value, end with clear next steps!

**Good luck! 🎉**
