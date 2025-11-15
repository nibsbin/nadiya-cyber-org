# Batch Ministry Workflow

**Scalable, DRY workflow for collecting organization names and cybersecurity assessments across multiple ministry types.**

## 🎯 The Problem

You need to run the same 2-step workflow for 10+ ministry types:
1. Collect organization names (`organization_question.py`)
2. Assess cybersecurity responsibility (`organization_cyber_question.py`)

The old copy-paste approach doesn't scale.

## ✨ The Solution

**One notebook** (`notebooks/batch_ministry_collect.ipynb`) + **One script** (`scripts/batch_ministry_workflow.py`)

The script handles all the logic (DRY), the notebook provides explainability and interactivity.

## 🚀 Quick Start

### 1. Open the Notebook

```bash
jupyter notebook notebooks/batch_ministry_collect.ipynb
```

### 2. Configure Your Domains

In the notebook, edit the list:

```python
domains_to_process = [
    "Justice",
    "Defense",
    "Health",
    "Finance",
    # ... add your 10 domains
]
```

### 3. Run All Cells

The notebook will:
- Run Step 1 (organization collection) for each domain
- Run Step 2 (cybersecurity assessment) for each domain
- Show progress and results
- Save outputs to `outputs/{domain}/`

## 📁 Output Structure

```
outputs/
  justice/
    organization.db                     # Step 1 cache
    organization_cyber.db               # Step 2 cache
    organization_names_justice.csv      # Step 1 output
    organization_cyber_justice.xlsx     # Step 2 output
  defense/
    ... (same structure)
  health/
    ... (same structure)
```

## 📚 Available Domains

19 ministry types available (from `data/domains.csv`):

Foreign Affairs • Education • Economy • Finance • Commerce • Transportation • Defense • Energy • Science and Technology • Communication • Interior/Domestic Affairs • Justice • Trade • Housing • Health • Labor • Culture • Agriculture • Industry

## 💡 Key Features

### In the Notebook

- **Interactive:** See progress, results, and errors inline
- **Explainable:** Each step shows what it's doing
- **Flexible:** Process all domains or just a few
- **Resumable:** Re-run failed domains without reprocessing
- **Summary:** View statistics across all domains

### In the Script

- **DRY:** All workflow logic in one place
- **Reusable:** Import and use in other scripts
- **Tested:** Single source of truth
- **Maintainable:** Fix once, applies everywhere
- **Resilient:** Automatic retry with exponential backoff (2s, 4s, 8s, 16s)
- **Sequential:** Processes domains one at a time to avoid rate limits

## 🔍 How It Works

### Architecture

```
notebooks/batch_ministry_collect.ipynb    (User interface - explainable)
           ↓
scripts/batch_ministry_workflow.py        (Logic - DRY)
           ↓
library/organization_question.py          (Step 1)
library/organization_cyber_question.py    (Step 2)
           ↓
outputs/{domain}/                         (Results)
```

### Workflow

For each domain in your list:

1. **Step 1:** Collect Organizations
   - Query: "What is the top-level ministry for {domain} in {country}?"
   - Output: `organization_names_{domain}.csv`

2. **Step 2:** Assess Cybersecurity
   - Query: "Is {organization} responsible for cybersecurity?"
   - Output: `organization_cyber_{domain}.xlsx`

## 📖 Notebook Sections

The notebook has these sections:

1. **Setup** - Import dependencies
2. **Configuration** - Choose which domains to process
3. **Run Batch Workflow** - Process all domains automatically
4. **Run Single Domain** - Process one domain at a time
5. **View Results** - Inspect outputs for a specific domain
6. **Summary Statistics** - Overview of all processed domains

## 🎓 Examples

### Example 1: Process 3 Domains

In the notebook:

```python
domains_to_process = ["Justice", "Defense", "Health"]
results = await run_batch_workflow(domains_to_process, output_dir, workers=4)
```

Output:
```
🚀 Starting complete workflow for domain: Justice
  ✓ 193 organizations collected
  ✓ 193 assessments completed
✅ Completed workflow for Justice

🚀 Starting complete workflow for domain: Defense
  ✓ 193 organizations collected
  ✓ 193 assessments completed
✅ Completed workflow for Defense

...
```

### Example 2: Process All Domains

```python
from data import DOMAINS
domains_to_process = DOMAINS  # All 19 domains
results = await run_batch_workflow(domains_to_process, output_dir)
```

### Example 3: Re-run a Failed Domain

```python
single_domain = "Defense"
workflow = MinistryWorkflow(single_domain, output_dir)
org_df, cyber_df = await workflow.run_complete_workflow()
```

## 🛠️ Advanced: Programmatic Usage

You can also use the script directly from Python:

```python
from pathlib import Path
from scripts.batch_ministry_workflow import run_batch_workflow, MinistryWorkflow

# Batch processing
domains = ["Justice", "Defense", "Health"]
results = await run_batch_workflow(domains, Path("outputs"))

# Single domain
workflow = MinistryWorkflow("Justice", Path("outputs"))
org_df, cyber_df = await workflow.run_complete_workflow()
```

Or from command line:

```bash
python scripts/batch_ministry_workflow.py --domains "Justice,Defense,Health"
python scripts/batch_ministry_workflow.py --all-domains
```

## 📂 File Organization

### Core Files

```
notebooks/
  batch_ministry_collect.ipynb          # ⭐ Main interface (start here!)
  justice/                              # Legacy - reference only
    organization_collect.ipynb
    organization_cyber_collect.ipynb

scripts/
  batch_ministry_workflow.py            # ⭐ DRY logic (abstracted)

library/
  organization_question.py              # Step 1 logic
  organization_cyber_question.py        # Step 2 logic

data/
  countries.csv                         # List of countries
  domains.csv                           # List of ministry types
```

### Documentation

```
README_BATCH_WORKFLOW.md                # This file - Quick start
MIGRATION_GUIDE.md                      # Transition guide
docs/
  BATCH_WORKFLOW_GUIDE.md               # Complete reference
```

### Outputs

```
outputs/                                # Auto-created
  {domain}/                             # One per domain
    organization.db
    organization_cyber.db
    organization_names_{domain}.csv
    organization_cyber_{domain}.xlsx
```

## 🧹 Cleanup Recommendations

You can safely delete or archive:

- **`notebooks/justice/`** - Keep as reference or delete (new outputs go to `outputs/justice/`)
- **Any other `notebooks/{domain}/`** - Replaced by batch workflow

Keep:
- **`notebooks/batch_ministry_collect.ipynb`** - Your main interface
- **`scripts/batch_ministry_workflow.py`** - DRY abstraction
- **`library/`** - Core logic
- **`data/`** - Source data

## 🚦 Getting Started

1. **Open the notebook:**
   ```bash
   jupyter notebook notebooks/batch_ministry_collect.ipynb
   ```

2. **Choose your domains:**
   ```python
   domains_to_process = ["Justice", "Defense", "Health", ...]
   ```

3. **Run the batch workflow cell**

4. **Check `outputs/` directory for results**

## 📊 Comparison: Old vs New

| Aspect | Old (Copy-Paste) | New (Batch) |
|--------|------------------|-------------|
| Setup for 10 domains | Copy 20 files, edit 10× | Edit 1 list |
| Explainability | Each notebook separate | One notebook, all steps visible |
| Code duplication | High (10 copies) | None (DRY in script) |
| Progress tracking | Manual per notebook | Automatic in notebook |
| Error recovery | Re-run entire notebook | Re-run failed domains only |
| Maintenance | Update 10+ notebooks | Update 1 script |

## 🎯 Why This Approach?

### Notebook First (Explainability)

- Interactive, visual, step-by-step
- See what's happening at each stage
- Inspect results inline
- Perfect for research and exploration

### Script Behind (DRY)

- All logic in one place
- Reusable across notebooks
- Testable and maintainable
- Single source of truth

**Best of both worlds!**

## 📖 Full Documentation

- **[Migration Guide](MIGRATION_GUIDE.md)** - Transition from old workflow
- **[Complete Guide](docs/BATCH_WORKFLOW_GUIDE.md)** - All features and options

## 💬 Next Steps

1. Open `notebooks/batch_ministry_collect.ipynb`
2. Run through it with 1-2 test domains
3. Scale up to your 10+ target domains
4. Check `outputs/` for results

🎉 **Enjoy the scalable, explainable workflow!**
