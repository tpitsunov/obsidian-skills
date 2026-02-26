---
name: Vault Statistics
description: Calculate deterministic quantitative statistics and metrics for the Obsidian vault using a Python script.
---

# Vault Statistics (Dry Numbers) Workflow

When the user asks for vault statistics, objective numbers, or metrics (e.g., "Give me stats on my vault" or "How many words are in my Obsidian"), follow these steps:

1. **Locate the Script**: This skill relies on a deterministic Python script located at `scripts/vault_stats.py` within this skill's folder.
2. **Determine Vault Path**: Identify the absolute path to the root directory of the user's Obsidian Vault.
3. **Execute the Script**: Use your terminal/command execution tool (`run_command`) to run the Python script against the vault path:
   ```bash
   python /absolute/path/to/Obsidian-AI-Skills/obsidian_stats/scripts/vault_stats.py "/absolute/path/to/vault"
   ```
4. **Report the Results**: The script will output a clean, formatted block of statistics (file count, word count, total links, tasks, and top 10 tags). Present this exact output block to the user. Do not try to guess or LLM-hallucinate these numbers.
