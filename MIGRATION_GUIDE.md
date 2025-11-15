# Migration Guide: From Manual Workflow to Batch Workflow

This guide helps you transition from the old copy-paste workflow to the new automated batch workflow.

## Quick Summary

**Old Way:** Copy notebooks to `notebooks/{domain}/`, manually edit domain name, run each separately

**New Way:** Run one command: `python scripts/batch_ministry_workflow.py --domains "Domain1,Domain2,Domain3"`

## What Changed?

### Before (Manual)
```
1. Copy notebooks/justice/organization_collect.ipynb to notebooks/defense/
2. Copy notebooks/justice/organization_cyber_collect.ipynb to notebooks/defense/
3. Edit notebooks/defense/organization_collect.ipynb
   - Change domains=['Justice'] to domains=['Defense']
4. Run notebooks/defense/organization_collect.ipynb
5. Run notebooks/defense/organization_cyber_collect.ipynb
6. Repeat for each of 10+ ministry types
```

### After (Automated)
```
1. Run: python scripts/batch_ministry_workflow.py --domains "Justice,Defense,Health,Finance,..."
2. Done! All domains processed automatically.
```

## Migration Steps

### Step 1: Understand the New Structure

The new workflow uses:
- **One script**: `scripts/batch_ministry_workflow.py` (replaces all copied notebooks)
- **One notebook**: `notebooks/batch_ministry_collect.ipynb` (optional, for interactive use)
- **Organized outputs**: `outputs/{domain}/` (instead of `notebooks/{domain}/`)

### Step 2: Your Existing Data

Your existing `notebooks/justice/` directory is **compatible** with the new structure:

```
notebooks/justice/          # Old location (still works)
  organization.db
  organization_cyber.db
  organization_names_justice.csv
  organization_cyber_justice.xlsx

outputs/justice/           # New location (where new runs go)
  organization.db
  organization_cyber.db
  organization_names_justice.csv
  organization_cyber_justice.xlsx
```

**Options:**
1. **Keep both**: Old data in `notebooks/justice/`, new data in `outputs/`
2. **Move**: `mv notebooks/justice outputs/` (if you want everything in one place)
3. **Fresh start**: Let the new workflow create everything in `outputs/`

### Step 3: Test with One Domain

Before processing all domains, test with one:

```bash
# Test with Justice (which you already have)
python scripts/batch_ministry_workflow.py --domains "Justice" --output-dir outputs

# Compare results with your existing notebooks/justice/ data
# They should be identical (or nearly identical, depending on data changes)
```

### Step 4: Process Your 10 New Domains

Now process all the domains you need:

```bash
# Replace these with your actual 10 domains
python scripts/batch_ministry_workflow.py --domains "Defense,Health,Finance,Education,Energy,Transportation,Communication,Foreign Affairs,Economy,Commerce"
```

Or use the notebook `notebooks/batch_ministry_collect.ipynb`:

```python
domains_to_process = [
    "Defense",
    "Health",
    "Finance",
    "Education",
    "Energy",
    "Transportation",
    "Communication",
    "Foreign Affairs",
    "Economy",
    "Commerce",
]
```

### Step 5: Verify Outputs

Check that outputs were created:

```bash
ls -la outputs/
# Should show directories for each domain

ls -la outputs/defense/
# Should show:
# - organization.db
# - organization_cyber.db
# - organization_names_defense.csv
# - organization_cyber_defense.xlsx
```

## Comparison Example

### Old Workflow: Adding 3 Domains

**Time required:** ~30-45 minutes

1. Create `notebooks/defense/`
2. Copy `organization_collect.ipynb` to `notebooks/defense/`
3. Copy `organization_cyber_collect.ipynb` to `notebooks/defense/`
4. Edit `notebooks/defense/organization_collect.ipynb` → change `domains=['Justice']` to `domains=['Defense']`
5. Run `notebooks/defense/organization_collect.ipynb`
6. Run `notebooks/defense/organization_cyber_collect.ipynb`
7. Create `notebooks/health/`
8. Copy `organization_collect.ipynb` to `notebooks/health/`
9. Copy `organization_cyber_collect.ipynb` to `notebooks/health/`
10. Edit `notebooks/health/organization_collect.ipynb` → change `domains=['Justice']` to `domains=['Health']`
11. Run `notebooks/health/organization_collect.ipynb`
12. Run `notebooks/health/organization_cyber_collect.ipynb`
13. Create `notebooks/finance/`
14. ... (repeat steps 8-12)

### New Workflow: Adding 3 Domains

**Time required:** ~30 seconds

```bash
python scripts/batch_ministry_workflow.py --domains "Defense,Health,Finance"
```

Or in the notebook:
```python
domains_to_process = ["Defense", "Health", "Finance"]
results = await run_batch_workflow(domains_to_process, output_dir)
```

## What Stays the Same?

- The underlying Python code (`library/organization_question.py` and `library/organization_cyber_question.py`)
- The data sources (`data/countries.csv`, `data/domains.csv`)
- The output formats (CSV for step 1, XLSX for step 2)
- The database caching (SQLite databases still cache results)

## What's Better?

| Feature | Old | New |
|---------|-----|-----|
| **Add a new domain** | Copy & edit 2 files | Add to a list |
| **Process 10 domains** | 20 file copies, 10 edits | 1 command |
| **Fix a bug in workflow** | Update 20+ notebook copies | Update 1 script |
| **See progress** | Check each directory manually | Automatic summary |
| **Re-run failed domain** | Open notebook, re-run | Re-run command |
| **Code maintenance** | High (many copies) | Low (DRY) |

## Troubleshooting Migration

### Q: Can I keep using my old notebooks?

**A:** Yes! The old notebooks in `notebooks/justice/` still work. The new workflow is an alternative, not a replacement.

### Q: What if I want to keep my old directory structure?

**A:** You can specify the output directory:

```bash
python scripts/batch_ministry_workflow.py --domains "Defense" --output-dir notebooks
```

This creates `notebooks/defense/` just like before.

### Q: Do I need to delete my old notebooks?

**A:** No. You can keep them as reference or backup. The new workflow uses `outputs/` by default, so there's no conflict.

### Q: What if the results are different?

**A:** The underlying queries might fetch slightly different data over time (as websites update). The workflow logic is the same, so any differences should be due to data changes, not workflow changes.

### Q: Can I use both workflows?

**A:** Yes, but be careful about which directories you're using. Recommend using:
- Old notebooks: Keep in `notebooks/{domain}/` for reference
- New workflow: Use `outputs/{domain}/` for new runs

### Q: How do I migrate my existing Justice data?

**A:** You have options:

1. **Leave it**: Keep `notebooks/justice/` as-is, new runs go to `outputs/justice/`
2. **Move it**: `mv notebooks/justice outputs/`
3. **Copy it**: `cp -r notebooks/justice outputs/`

## Next Steps After Migration

1. **Archive old notebooks** (optional):
   ```bash
   mkdir notebooks/archive
   mv notebooks/justice notebooks/archive/
   ```

2. **Process all your domains**:
   ```bash
   python scripts/batch_ministry_workflow.py --all-domains
   # or
   python scripts/batch_ministry_workflow.py --domains "Domain1,Domain2,..."
   ```

3. **Set up automation** (optional):
   - Add to cron for periodic updates
   - Create custom scripts for your specific domain subsets
   - Extend `MinistryWorkflow` class for custom workflows

## Getting Help

- See `docs/BATCH_WORKFLOW_GUIDE.md` for detailed usage
- Run `python scripts/batch_ministry_workflow.py --help`
- Check `notebooks/batch_ministry_collect.ipynb` for examples

## Summary

The new workflow gives you:
- ✅ **10x faster** setup for multiple domains
- ✅ **DRY** - no code duplication
- ✅ **Maintainable** - fix once, apply everywhere
- ✅ **Scalable** - easily handle 10, 20, or 100 domains
- ✅ **Consistent** - same logic for all domains
- ✅ **Automated** - batch processing with progress tracking

Welcome to the new workflow! 🎉
