# Obsidian AI Skills Repository

A collection of AI Agent Skills (Workflows) designed to automate, clean up, and interlink your Obsidian Vault. These are built in the standard AI Skill format (`SKILL.md` with YAML frontmatter) for use with your preferred AI coding assistant or agent.

## Available Skills

- **[MOC Builder](./moc_builder)** – Automatically grouped Map of Content (Index) generation based on semantics, not just alphabet.
- **[Orphan Note Connector](./orphan_connector)** – Finds disconnected notes and suggests intelligent semantic connections mapped to your existing files.
- **[Markdown Linter](./markdown_linter)** – Cleans up messy markdown pasted from the web (jumping headers, broken lists, extra lines) into pristine Obsidian-ready MD.
- **[Smart Tagger](./smart_tagger)** – Reads your note's context, cross-references your vault's existing tag structure, and automatically populates YAML frontmatter.
- **[Vault Statistics](./obsidian_stats)** – Procedurally calculates hard numbers and metrics for your vault (word count, link count, top tags, etc.) using a Python script.

## How to Install

1. Drop any of these skill folders into your agent's specified `skills` or `workflows` directory (e.g., `~/.agents/skills/` or `.gemini/antigravity/brain/skills`).
2. The agent will read the `SKILL.md` file to learn how to execute your requests predictably.
3. Prompt your agent (e.g., "Run the Smart Tagger on my latest note").

## Why AI instead of Static Scripts?

While procedural plugins (like Dataview or Templater) are fantastic for fixed patterns, these Agent Skills leverage LLMs to handle **semantic chaos**:
- Finding connections when names are misspelled or conjugated.
- Grouping a Map of Content by *meaning* rather than folders.
- Deducing appropriate tags that aren't specifically mentioned in the text.
