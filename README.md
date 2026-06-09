# Top Agents & Models Registry

This repository contains the registries and automation for the **Top 10 Agents** and **Top 10 AI Models** feeds displayed on `aiagent.org`.

## Contents

### 1. Top 10 Agents
* **`top_10_agents.md`**: The dynamically parsed markdown file listing the top 10 agents, companies, and descriptions.
* **`ai_agents_agent.py`**: A Python script utilizing the Gemini API to compile, research, and format the top AI agents.
* **`.github/workflows/generate_agents.yml`**: Scheduled and manual GitHub Actions workflow for the agents registry (runs weekly on Wednesdays at 10:00 AM UTC).

### 2. Top 10 Models
* **`top_10_models.json`**: The JSON file containing specs, contexts, benchmark scores, and API pricing for the top 10 AI models.
* **`ai_models_agent.py`**: A Python script utilizing the Gemini API to compile details for the top AI models.
* **`.github/workflows/generate_models.yml`**: Scheduled and manual GitHub Actions workflow for the models registry (runs weekly on Wednesdays at 12:00 PM UTC).

## Automation & Integration

Both registries are updated autonomously by their respective scheduled GitHub Actions workflows running weekly.

The main page at `aiagent.org` fetches these files directly from the raw content CDN of this repository and parses/renders them dynamically on page load.
