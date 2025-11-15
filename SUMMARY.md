# Batch Ministry Workflow - Summary

## What Was Created

### Primary Interface (Notebook-First)
- **`notebooks/batch_ministry_collect.ipynb`** - Single notebook for all ministry types
  - Interactive, explainable workflow
  - Process any number of domains with one notebook
  - Includes: configuration, batch processing, single domain runs, results viewing, summary stats

### DRY Abstraction (Script)
- **`scripts/batch_ministry_workflow.py`** - All workflow logic in one place
  - `MinistryWorkflow` class for single domain processing
  - `run_batch_workflow()` function for batch processing
  - Reusable, testable, maintainable
  - Command-line interface available

### Documentation
- **`README_BATCH_WORKFLOW.md`** - Quick start guide
- **`MIGRATION_GUIDE.md`** - Transition from old copy-paste workflow
- **`docs/BATCH_WORKFLOW_GUIDE.md`** - Complete reference documentation

## How It Works

```
User edits list in notebook:
  domains_to_process = ["Justice", "Defense", "Health"]

Notebook calls script:
  run_batch_workflow(domains_to_process, ...)

Script processes each domain:
  Step 1: organization_question.py → organization_names_{domain}.csv
  Step 2: organization_cyber_question.py → organization_cyber_{domain}.xlsx

Results saved to:
  outputs/{domain}/
```

## Usage

### Quick Start
1. Open `notebooks/batch_ministry_collect.ipynb`
2. Edit `domains_to_process` list
3. Run all cells
4. Check `outputs/` directory

### Command Line (Alternative)
```bash
python scripts/batch_ministry_workflow.py --domains "Justice,Defense,Health"
python scripts/batch_ministry_workflow.py --all-domains
```

## Benefits

| Old Approach | New Approach |
|--------------|--------------|
| Copy 2 notebooks per domain | Edit 1 list in 1 notebook |
| Manually edit domain names 10+ times | Change list once |
| Run 20+ notebooks separately | Run 1 notebook |
| High code duplication | Zero duplication (DRY) |
| Hard to maintain | Single source of truth |
| ~30 min setup for 10 domains | ~30 sec setup |

## File Organization

### Keep & Use
```
notebooks/batch_ministry_collect.ipynb    ⭐ Start here
scripts/batch_ministry_workflow.py        ⭐ DRY logic
library/organization_question.py
library/organization_cyber_question.py
data/countries.csv
data/domains.csv
```

### Reference (Optional)
```
notebooks/justice/                        Original example (reference only)
```

### Auto-Generated
```
outputs/{domain}/                         Results for each domain
  organization.db
  organization_cyber.db
  organization_names_{domain}.csv
  organization_cyber_{domain}.xlsx
```

## Next Steps

1. Review `README_BATCH_WORKFLOW.md` for quick start
2. Open `notebooks/batch_ministry_collect.ipynb`
3. Test with 1-2 domains
4. Scale to all 10+ target domains

## Architecture Principles

✅ **Notebook-first** - Explainability and interactivity
✅ **Script-backed** - DRY, reusable, testable
✅ **Scalable** - Handles 1 or 100 domains
✅ **Organized** - Clear file structure
✅ **Documented** - Comprehensive guides

---

**Ready to process 10+ ministry types?** Open `notebooks/batch_ministry_collect.ipynb` and get started!
