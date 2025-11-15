# Batch Ministry Workflow Guide

This guide explains how to use the new scalable workflow for collecting organization names and cybersecurity assessments across multiple ministry types.

## Table of Contents
- [Overview](#overview)
- [Migration from Old Workflow](#migration-from-old-workflow)
- [Quick Start](#quick-start)
- [Usage Methods](#usage-methods)
- [Output Structure](#output-structure)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

### What This Solves
The old workflow required manually copying notebooks for each ministry type, editing domain names, and running them individually. This didn't scale well for 10+ ministry types.

The new workflow:
- ✅ Processes any number of ministry types with a single command
- ✅ DRY (Don't Repeat Yourself) - no code duplication
- ✅ Automatic organization of outputs
- ✅ Progress tracking and error handling
- ✅ Can run all domains or specific subsets
- ✅ Resume failed runs without re-processing completed domains

### The Two-Step Process
For each ministry type (domain), the workflow:

1. **Step 1: Organization Collection**
   - Runs `organization_question.py` for the domain across all countries
   - Outputs: `organization_names_{domain}.csv`

2. **Step 2: Cybersecurity Assessment**
   - Runs `organization_cyber_question.py` for each organization from Step 1
   - Outputs: `organization_cyber_{domain}.xlsx`

## Migration from Old Workflow

### Old Way (Copy-Paste)
```
notebooks/
  justice/
    organization_collect.ipynb          # Manually copied & edited
    organization_cyber_collect.ipynb    # Manually copied & edited
    organization.db
    organization_cyber.db
    organization_names_justice.csv
    organization_cyber_justice.xlsx

  # Repeat for each ministry type...
  defense/
    organization_collect.ipynb          # Manually copied & edited
    organization_cyber_collect.ipynb    # Manually copied & edited
    ...
```

### New Way (Automated)
```
scripts/
  batch_ministry_workflow.py            # Single reusable script

notebooks/
  batch_ministry_collect.ipynb          # Single notebook for all domains

outputs/                                # Auto-organized outputs
  justice/
    organization.db
    organization_cyber.db
    organization_names_justice.csv
    organization_cyber_justice.xlsx
  defense/
    organization.db
    organization_cyber.db
    organization_names_defense.csv
    organization_cyber_defense.xlsx
  # ... automatically created for each domain
```

## Quick Start

### Method 1: Command Line (Recommended for batch processing)

Process specific domains:
```bash
python scripts/batch_ministry_workflow.py --domains "Defense,Health,Finance"
```

Process all available domains:
```bash
python scripts/batch_ministry_workflow.py --all-domains
```

### Method 2: Jupyter Notebook (Recommended for interactive work)

1. Open `notebooks/batch_ministry_collect.ipynb`
2. Edit the `domains_to_process` list
3. Run all cells

## Usage Methods

### Command Line Script

The script `scripts/batch_ministry_workflow.py` provides maximum flexibility:

```bash
# Basic usage - specific domains
python scripts/batch_ministry_workflow.py --domains "Justice,Defense,Health"

# Process all available domains
python scripts/batch_ministry_workflow.py --all-domains

# Custom output directory
python scripts/batch_ministry_workflow.py --domains "Justice" --output-dir my_results

# Adjust number of parallel workers
python scripts/batch_ministry_workflow.py --domains "Justice" --workers 8

# Show help
python scripts/batch_ministry_workflow.py --help
```

**Available Options:**
- `--domains`: Comma-separated list of domains to process
- `--all-domains`: Process all 19 available domains
- `--output-dir`: Output directory (default: `outputs`)
- `--workers`: Number of parallel workers (default: 4)

### Jupyter Notebook

The notebook `notebooks/batch_ministry_collect.ipynb` provides an interactive interface:

**Features:**
- Visual progress tracking
- Easy configuration via Python lists
- Ability to view results inline
- Summary statistics
- Re-run individual domains if needed

**Usage:**
1. Edit the `domains_to_process` list in the configuration cell
2. Run the "Run Batch Workflow" cell to process all domains
3. Or use the "Run Single Domain" cell to process one domain at a time
4. Use the "View Results" cell to inspect outputs

### Programmatic Usage

You can also import and use the workflow in your own scripts:

```python
from pathlib import Path
from scripts.batch_ministry_workflow import run_batch_workflow, MinistryWorkflow

# Batch processing
domains = ["Justice", "Defense", "Health"]
output_dir = Path("outputs")
results = await run_batch_workflow(domains, output_dir, workers=4)

# Single domain processing
workflow = MinistryWorkflow("Justice", output_dir)
org_df, cyber_df = await workflow.run_complete_workflow()
```

## Output Structure

Outputs are organized by domain:

```
outputs/
  {domain}/
    organization.db                      # SQLite database for step 1
    organization_cyber.db                # SQLite database for step 2
    organization_names_{domain}.csv      # Organization names (step 1 output)
    organization_cyber_{domain}.xlsx     # Cybersecurity assessments (step 2 output)
```

**Example:**
```
outputs/
  justice/
    organization.db
    organization_cyber.db
    organization_names_justice.csv
    organization_cyber_justice.xlsx
  defense/
    organization.db
    organization_cyber.db
    organization_names_defense.csv
    organization_cyber_defense.xlsx
```

### File Descriptions

- **`organization.db`**: Stores cached results from organization name queries (step 1)
- **`organization_cyber.db`**: Stores cached results from cybersecurity assessment queries (step 2)
- **`organization_names_{domain}.csv`**: Final output of step 1 with organization names
- **`organization_cyber_{domain}.xlsx`**: Final output of step 2 with cybersecurity assessments

## Examples

### Example 1: Process 3 Specific Domains

```bash
python scripts/batch_ministry_workflow.py --domains "Justice,Defense,Health"
```

Output:
```
############################################################
# BATCH MINISTRY WORKFLOW
# Processing 3 domains
# Output directory: outputs
############################################################

[1/3] Processing domain: Justice
============================================================
STEP 1: Collecting organizations for Justice
============================================================
Processing 193 questions...
✓ Saved 193 organizations to outputs/justice/organization_names_justice.csv

============================================================
STEP 2: Assessing cybersecurity responsibility for Justice
============================================================
Processing 193 questions...
✓ Saved 193 assessments to outputs/justice/organization_cyber_justice.xlsx

✅ Completed workflow for Justice
   Organizations collected: 193
   Cybersecurity assessments: 193

[2/3] Processing domain: Defense
...
```

### Example 2: Process All Available Domains

```bash
python scripts/batch_ministry_workflow.py --all-domains
```

This will process all 19 domains from `data/domains.csv`:
- Foreign Affairs
- Education
- Economy
- Finance
- Commerce
- Transportation
- Defense
- Energy
- Science and Technology (and/or Innovation)
- Communication
- Interior/Domestic Affairs
- Justice
- Trade
- Housing
- Health
- Labor
- Culture
- Agriculture
- Industry

### Example 3: Using the Notebook

1. Open `notebooks/batch_ministry_collect.ipynb`

2. Configure domains:
```python
domains_to_process = [
    "Defense",
    "Health",
    "Finance",
]
```

3. Run the batch workflow cell:
```python
results = await run_batch_workflow(domains_to_process, output_dir, workers=4)
```

4. View summary:
```python
# Summary DataFrame shows status of all domains
display(summary_df)
```

### Example 4: Re-run a Single Failed Domain

If one domain fails, you can re-run just that domain:

```bash
python scripts/batch_ministry_workflow.py --domains "Defense"
```

Or in the notebook, use the "Run Single Domain" cell:
```python
single_domain = "Defense"
workflow = MinistryWorkflow(single_domain, output_dir, workers=workers)
org_df, cyber_df = await workflow.run_complete_workflow()
```

## Available Domains

You can process any of these 19 ministry types:

1. Foreign Affairs
2. Education
3. Economy
4. Finance
5. Commerce
6. Transportation
7. Defense
8. Energy
9. Science and Technology (and/or Innovation)
10. Communication
11. Interior/Domestic Affairs
12. Justice
13. Trade
14. Housing
15. Health
16. Labor
17. Culture
18. Agriculture
19. Industry

## Advanced Usage

### Adjusting Parallelism

The `--workers` parameter controls how many questions are processed in parallel:

```bash
# More workers = faster, but more API calls
python scripts/batch_ministry_workflow.py --domains "Justice" --workers 8

# Fewer workers = slower, but more conservative
python scripts/batch_ministry_workflow.py --domains "Justice" --workers 2
```

### Custom Output Directory

```bash
python scripts/batch_ministry_workflow.py --domains "Justice,Defense" --output-dir research_results
```

This creates:
```
research_results/
  justice/
    ...
  defense/
    ...
```

### Processing Subsets

You can process domains in batches:

```bash
# Batch 1: Core ministries
python scripts/batch_ministry_workflow.py --domains "Justice,Defense,Interior/Domestic Affairs"

# Batch 2: Economic ministries
python scripts/batch_ministry_workflow.py --domains "Finance,Economy,Commerce,Trade"

# Batch 3: Social ministries
python scripts/batch_ministry_workflow.py --domains "Health,Education,Labor,Housing"
```

## Troubleshooting

### Issue: "Module not found" error

**Solution:** Make sure you're running from the project root:
```bash
cd /path/to/nadiya-cyber-org
python scripts/batch_ministry_workflow.py --domains "Justice"
```

### Issue: Domain not found warning

**Solution:** Check the domain name matches exactly (case-insensitive, but spaces matter):
```bash
# ✓ Correct
python scripts/batch_ministry_workflow.py --domains "Science and Technology (and/or Innovation)"

# ✗ Wrong
python scripts/batch_ministry_workflow.py --domains "Science and Technology"
```

### Issue: Workflow fails partway through

**Solution:** The databases cache results, so you can safely re-run:
```bash
# This will skip already-processed questions
python scripts/batch_ministry_workflow.py --domains "Justice"
```

### Issue: Want to start fresh

**Solution:** Delete the domain's output directory:
```bash
rm -rf outputs/justice
python scripts/batch_ministry_workflow.py --domains "Justice"
```

### Issue: Notebook kernel dies

**Solution:** Reduce the number of workers or process fewer domains at once:
```python
workers = 2  # Instead of 4
domains_to_process = ["Justice"]  # Start with one
```

## Performance Tips

1. **Start Small**: Test with 1-2 domains before running all 19
2. **Monitor Resources**: Each worker makes API calls; adjust based on rate limits
3. **Use Caching**: The SQLite databases cache results; re-running is fast
4. **Batch Wisely**: Process related domains together for logical organization

## Comparison: Old vs New Workflow

| Aspect | Old Workflow | New Workflow |
|--------|-------------|--------------|
| Setup for 10 domains | Copy 20 files, edit 10 times | Edit 1 list |
| Code duplication | High (10 copies) | None (DRY) |
| Consistency | Manual, error-prone | Automated, consistent |
| Progress tracking | Manual checking | Automatic summary |
| Error recovery | Re-run everything | Re-run failed domains only |
| Adding new domain | Copy & edit 2 files | Add to list |
| Time to setup | ~30 min for 10 domains | ~30 seconds |

## Next Steps

1. **Test**: Start with 1-2 domains to verify everything works
2. **Scale**: Process all 10+ domains you need
3. **Automate**: Consider scheduling regular runs
4. **Extend**: The `MinistryWorkflow` class can be extended for custom workflows

## Need Help?

- Check `scripts/batch_ministry_workflow.py --help` for command-line options
- Review the examples in `notebooks/batch_ministry_collect.ipynb`
- Look at the existing `notebooks/justice/` directory for reference data
