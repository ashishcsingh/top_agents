# Top 10 Agents Registry

This repository contains the registry and automation for the **Top 10 Agents & Frameworks** feed displayed on `aiagent.org`.

## Contents

* **`top_10_agents.md`**: The dynamically parsed markdown file listing the top 10 agents, companies, and descriptions.
* **`ai_agents_agent.py`**: A Python script utilizing the Gemini API to compile, research, and format the top AI agents.
* **`requirements.txt`**: Project dependency list.
* **`.github/workflows/generate_agents.yml`**: Scheduled and manual GitHub Actions workflow.

## Automation & Integration

This registry is updated autonomously by a scheduled GitHub Actions workflow running weekly. 

The main page at `aiagent.org` fetches `top_10_agents.md` directly from the raw content CDN of this repository and parses the headings to dynamically render the dashboard cards.
