# Ministry Cybersecurity Assessment - Batch Workflow

Automated workflow for collecting organization names and cybersecurity responsibility assessments across multiple ministry types.

## 🚀 Quick Start

1. **Open the notebook:**
   ```bash
   jupyter notebook notebooks/batch_ministry_collect.ipynb
   ```

2. **Configure domains:**
   ```python
   domains_to_process = ["Justice", "Defense", "Health", ...]
   ```

3. **Run all cells**

Results are saved to `outputs/{domain}/`

## 📚 Documentation

- **[Quick Start Guide](README_BATCH_WORKFLOW.md)** - Get started in 5 minutes
- **[Migration Guide](MIGRATION_GUIDE.md)** - Transition from old workflow
- **[Complete Reference](docs/BATCH_WORKFLOW_GUIDE.md)** - All features and options
- **[Summary](SUMMARY.md)** - Overview of the workflow

## 🎯 What This Does

For each ministry type (domain):
1. **Step 1:** Collect organization names across all countries
2. **Step 2:** Assess cybersecurity responsibility for each organization

## ✨ Features

- **Sequential Processing:** Domains processed one at a time to avoid rate limits
- **Automatic Retry:** Exponential backoff (2s, 4s, 8s, 16s) handles transient failures
- **DRY Architecture:** All logic in one script, notebook provides explainability
- **Scalable:** Handles 1 or 100 domains with the same ease
- **Resumable:** Database caching allows re-running without reprocessing

## 📁 Project Structure

```
.
├── notebooks/
│   └── batch_ministry_collect.ipynb    # Main interface
├── scripts/
│   └── batch_ministry_workflow.py      # DRY workflow logic
├── library/
│   ├── organization_question.py        # Step 1 logic
│   └── organization_cyber_question.py  # Step 2 logic
├── data/
│   ├── countries.csv                   # List of countries
│   └── domains.csv                     # List of ministry types
├── docs/
│   └── BATCH_WORKFLOW_GUIDE.md         # Complete reference
├── outputs/                            # Auto-generated results
│   └── {domain}/
│       ├── organization_names_{domain}.csv
│       └── organization_cyber_{domain}.xlsx
└── README_BATCH_WORKFLOW.md            # Quick start guide
```

## 🎓 Available Domains

19 ministry types available:

Foreign Affairs • Education • Economy • Finance • Commerce • Transportation • Defense • Energy • Science and Technology • Communication • Interior/Domestic Affairs • Justice • Trade • Housing • Health • Labor • Culture • Agriculture • Industry

## 💻 Command Line Usage (Alternative)

```bash
# Process specific domains
python scripts/batch_ministry_workflow.py --domains "Justice,Defense,Health"

# Process all domains
python scripts/batch_ministry_workflow.py --all-domains
```

## 📖 Read This First

Start with [README_BATCH_WORKFLOW.md](README_BATCH_WORKFLOW.md) for the quick start guide.

---

**Ready to process ministry data at scale?** Open `notebooks/batch_ministry_collect.ipynb` and get started!
