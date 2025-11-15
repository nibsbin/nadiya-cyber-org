"""
Batch workflow for collecting organization names and cybersecurity responsibility
across multiple ministry types and countries.

This script automates the two-step process:
1. Collect organization names for each ministry type across all countries
2. Assess cybersecurity responsibility for each organization

Usage:
    python scripts/batch_ministry_workflow.py --domains "Justice,Defense,Health"
    python scripts/batch_ministry_workflow.py --all-domains
"""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import List
import pandas as pd

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from robora import Workflow, SQLiteStorageProvider
from robora.sonar_query import SonarQueryHandler
from library.organization_question import OrganizationModel, get_question_set as get_org_questions
from library.organization_cyber_question import OrganizationCyberModel, get_question_set as get_cyber_questions
from data import COUNTRIES, DOMAINS


class MinistryWorkflow:
    """Handles the complete workflow for a single ministry domain."""

    def __init__(self, domain: str, output_dir: Path, workers: int = 4):
        self.domain = domain.strip().title()
        self.output_dir = output_dir / domain.lower().replace(" ", "_").replace("/", "_")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.workers = workers

    async def step1_collect_organizations(self) -> pd.DataFrame:
        """Step 1: Collect organization names for this domain across all countries."""
        print(f"\n{'='*60}")
        print(f"STEP 1: Collecting organizations for {self.domain}")
        print(f"{'='*60}")

        # Setup storage and workflow
        db_path = self.output_dir / "organization.db"
        storage = SQLiteStorageProvider(str(db_path))
        workflow = Workflow(
            SonarQueryHandler(OrganizationModel),
            storage,
            workers=self.workers,
        )

        # Create question set
        question_set = get_org_questions(
            domains=[self.domain],
            countries=COUNTRIES,
        )
        question_set.max_questions = 0  # No limit

        # Ask questions
        await workflow.ask_multiple(question_set, return_results=False)

        # Dump and flatten answers
        answers = []
        async for answer in workflow.dump_answers():
            answers.append(answer)

        flattened = pd.concat([ans.flattened for ans in answers]).reset_index(drop=True)
        flattened.drop(columns=["enriched_citations"], inplace=True, errors='ignore')

        # Save to CSV
        csv_path = self.output_dir / f"organization_names_{self.domain.lower().replace(' ', '_')}.csv"
        flattened.to_csv(csv_path, index=False)
        print(f"✓ Saved {len(flattened)} organizations to {csv_path}")

        return flattened

    async def step2_assess_cybersecurity(self, organizations_df: pd.DataFrame) -> pd.DataFrame:
        """Step 2: Assess cybersecurity responsibility for each organization."""
        print(f"\n{'='*60}")
        print(f"STEP 2: Assessing cybersecurity responsibility for {self.domain}")
        print(f"{'='*60}")

        # Setup storage and workflow
        db_path = self.output_dir / "organization_cyber.db"
        storage = SQLiteStorageProvider(str(db_path))
        workflow = Workflow(
            SonarQueryHandler(OrganizationCyberModel),
            storage,
            workers=self.workers,
        )

        # Extract organizations and countries from step 1
        organizations = organizations_df["organization_name"].tolist()
        countries = organizations_df["country"].tolist()

        # Create question set
        question_set = get_cyber_questions(
            organizations=organizations,
            countries=countries,
        )
        question_set.max_questions = 0  # No limit

        # Ask questions
        await workflow.ask_multiple(question_set, return_results=False)

        # Dump and flatten answers
        answers = []
        async for answer in workflow.dump_answers():
            answers.append(answer)

        flattened = pd.concat([ans.flattened for ans in answers]).reset_index(drop=True)

        # Save to Excel
        xlsx_path = self.output_dir / f"organization_cyber_{self.domain.lower().replace(' ', '_')}.xlsx"
        flattened.to_excel(xlsx_path, index=False)
        print(f"✓ Saved {len(flattened)} assessments to {xlsx_path}")

        return flattened

    async def run_complete_workflow(self):
        """Run both steps of the workflow."""
        print(f"\n🚀 Starting complete workflow for domain: {self.domain}")

        # Step 1: Collect organizations
        organizations_df = await self.step1_collect_organizations()

        # Step 2: Assess cybersecurity
        cyber_df = await self.step2_assess_cybersecurity(organizations_df)

        print(f"\n✅ Completed workflow for {self.domain}")
        print(f"   Organizations collected: {len(organizations_df)}")
        print(f"   Cybersecurity assessments: {len(cyber_df)}")

        return organizations_df, cyber_df


async def run_batch_workflow(domains: List[str], output_dir: Path, workers: int = 4):
    """Run the workflow for multiple domains."""
    print(f"\n{'#'*60}")
    print(f"# BATCH MINISTRY WORKFLOW")
    print(f"# Processing {len(domains)} domains")
    print(f"# Output directory: {output_dir}")
    print(f"{'#'*60}")

    results = {}

    for i, domain in enumerate(domains, 1):
        print(f"\n[{i}/{len(domains)}] Processing domain: {domain}")

        workflow = MinistryWorkflow(domain, output_dir, workers=workers)
        try:
            org_df, cyber_df = await workflow.run_complete_workflow()
            results[domain] = {
                'status': 'success',
                'organizations': len(org_df),
                'assessments': len(cyber_df),
            }
        except Exception as e:
            print(f"❌ Error processing {domain}: {e}")
            results[domain] = {
                'status': 'error',
                'error': str(e),
            }

    # Print summary
    print(f"\n{'#'*60}")
    print(f"# BATCH WORKFLOW SUMMARY")
    print(f"{'#'*60}")
    for domain, result in results.items():
        if result['status'] == 'success':
            print(f"✓ {domain}: {result['organizations']} orgs, {result['assessments']} assessments")
        else:
            print(f"✗ {domain}: {result['error']}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Batch workflow for collecting ministry organizations and cybersecurity assessments"
    )
    parser.add_argument(
        "--domains",
        type=str,
        help="Comma-separated list of domains (e.g., 'Justice,Defense,Health')"
    )
    parser.add_argument(
        "--all-domains",
        action="store_true",
        help="Process all available domains"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Output directory (default: outputs)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)"
    )

    args = parser.parse_args()

    # Determine which domains to process
    if args.all_domains:
        domains_to_process = DOMAINS
    elif args.domains:
        domains_to_process = [d.strip() for d in args.domains.split(",")]
    else:
        parser.error("Must specify either --domains or --all-domains")

    # Validate domains
    invalid_domains = [d for d in domains_to_process if d not in DOMAINS]
    if invalid_domains:
        print(f"Warning: Unknown domains will be processed anyway: {invalid_domains}")
        print(f"Available domains: {', '.join(DOMAINS)}")

    output_dir = Path(args.output_dir)

    # Run the batch workflow
    asyncio.run(run_batch_workflow(domains_to_process, output_dir, args.workers))


if __name__ == "__main__":
    main()
