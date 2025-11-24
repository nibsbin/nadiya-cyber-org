# Research Project Documentation: Global Cybersecurity Organization Mapping

## Executive Summary

This project, `nadiya-cyber-org`, establishes an automated pipeline for mapping the global landscape of cybersecurity governance. By leveraging Large Language Models (LLMs) with search capabilities (via the `robora` library), the project systematically identifies top-level government organizations responsible for critical sectors across approximately 193 countries. Furthermore, it assesses the cybersecurity responsibilities of these identified organizations. The result is a structured dataset enabling analysis of how different nations structure their cybersecurity governance across domains like Defense, Energy, Finance, and Telecommunications.

## Background & Purpose

Understanding the institutional architecture of national cybersecurity is critical for policy analysis and international cooperation. However, this information is often scattered, unstructured, and difficult to collect manually on a global scale.

The primary objectives of this research are:
1.  **Identification**: To identify the specific top-level state organs (ministries, departments, agencies) responsible for key functional domains (e.g., Energy, Finance, Defense) in every country.
2.  **Assessment**: To evaluate the level of cybersecurity responsibility held by these identified organizations, categorizing them by their role in governance, prevention, planning, response, or enforcement.

## Solution

The project implements a Python-based automated data collection and processing system.

### Key Components
*   **Data Models**: Rigorous data structures defined using `Pydantic` to ensure consistent output.
    *   `OrganizationModel`: Captures the name of the responsible organization and a confidence score.
    *   `OrganizationCyberModel`: Captures the organization's cybersecurity responsibility level (HIGH, LOW, NONE), provides an explanation with evidence, and a confidence score.
*   **Orchestration Engine**: Uses the `robora` library to manage the workflow of generating questions, querying the AI provider, and storing results.
*   **AI Integration**: Utilizes `SonarQueryHandler` (likely powered by a search-enabled LLM like Perplexity Sonar) to perform real-time research and answer generation.
*   **Storage**: Results are persisted in a local SQLite database (`organization.db`) to ensure data integrity and allow for resuming interrupted collection runs.

## Project Deliverables

The project pipeline produces two primary datasets, generated via interactive Jupyter notebooks:

### 1. Organization Mapping (`organization_names.xlsx`)
*   **Source**: `notebooks/organization_collect.ipynb`
*   **Description**: A comprehensive mapping of top-level state organs.
*   **Process**: Iterates through ~193 countries and ~19 domains to identify the specific ministry or agency responsible for that sector.
*   **Key Columns**: `country`, `domain`, `organization_name`, `confidence`.

### 2. Cybersecurity Responsibility Assessment (`organization_cyber.xlsx`)
*   **Source**: `notebooks/organization_cyber_collect.ipynb`
*   **Description**: A detailed assessment of the cybersecurity role of the organizations identified in the first step.
*   **Process**: Ingests the `organization_names.xlsx` file and queries the AI to determine if each identified organization has a role in cybersecurity governance, prevention, or response.
*   **Key Columns**: `organization`, `country`, `responsibility_level` (HIGH/LOW/NONE), `explanation` (with evidence), `confidence`.

## Methodology

The research follows a systematic, automated workflow:

1.  **Scope Definition**:
    *   **Countries**: A comprehensive list of ~193 nations (sourced from `data/countries.csv`).
    *   **Domains**: A targeted list of ~19 critical sectors including Foreign Affairs, Education, Economy, Finance, Transportation, Defense, Energy, and Science & Technology (sourced from `data/domains.csv`).

2.  **Question Generation**:
    *   The system programmatically generates questions for every combination of Country and Domain.
    *   *Template*: "What is the top-level state Organ (i.e., ministry/department/agency) responsible for {domain} in {country}?"

3.  **Automated Data Collection**:
    *   The `robora` workflow executes these questions asynchronously (using multiple workers).
    *   The `SonarQueryHandler` processes each question, searching for current information to provide an accurate answer.

4.  **Data Structuring & Validation**:
    *   Raw text responses are parsed into structured objects (`OrganizationModel`).
    *   The system assigns a confidence level (HIGH, MEDIUM, LOW, NONE) to each data point.

5.  **Analysis & Export**:
    *   Collected data is aggregated into Pandas DataFrames.
    *   Results are exported to Excel (`organization_names.xlsx`) and CSV formats for downstream analysis and visualization.

## Barriers & Limitations

*   **Information Availability**: The accuracy of the data is strictly limited by the public availability of government information online. For nations with limited digital presence or opaque governance structures, data collection may yield low confidence results or "NONE".
*   **Language Bias**: Queries are currently conducted in English. While modern LLMs are multilingual, searching for government entities in their native language might yield better results for non-English speaking countries.
*   **AI Hallucination & Accuracy**: Despite using a search-enabled model, there is a risk of the AI misidentifying organizations or hallucinating non-existent entities. The `confidence` score is a mitigation measure but not a guarantee.
*   **Dynamic Nature of Governance**: Government structures change (ministries merge, are renamed, or dissolved). The dataset represents a snapshot in time and requires periodic updates.
*   **Standardization Challenges**: Mapping diverse political systems (e.g., federal vs. unitary states) to a standardized "top-level state Organ" model can be complex and may require manual review for edge cases.
