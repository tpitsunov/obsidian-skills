# Obsidian AI Skills Repository

A collection of AI Agent Skills (Workflows) designed to automate, clean up, and interlink your Obsidian Vault. These are built in the standard AI Skill format (`SKILL.md` with YAML frontmatter) for use with your preferred AI coding assistant or agent.

## Available Skills

- **[MOC Builder](./moc_builder)** (`/moc`) – Automatically grouped Map of Content (Index) generation based on semantics, not just alphabet.
- **[Orphan Note Connector](./orphan_connector)** (`/orphans`) – Finds disconnected notes and suggests intelligent semantic connections mapped to your existing files.
- **[Markdown Linter](./markdown_linter)** (`/lint`) – Cleans up messy markdown pasted from the web.
- **[Smart Tagger](./smart_tagger)** (`/tag`) – Reads your note's context, cross-references your vault's tags, and populates YAML frontmatter.
- **[Vault Statistics](./obsidian_stats)** (`/stats`) – Procedurally calculates vault metrics using a Python script.
- **[Table of Contents Generator](./toc_generator)** (`/toc`) – Analyzes multiple header levels in a long markdown file and generates a clickable Table of Contents.
- **Concept Extractor** (`/extract`): Reads a large note, extracts 3-5 key concepts, creates new atomic notes for each, and maps them back into the original text.
- **Zettel Atomizer** (`/atomize`): Advanced, lossless procedural text splitter that extracts cohesive thoughts into standalone Zettels.
- **Serendipity Engine** (`/spark`): Pulls completely random notes from the vault and challenges the AI to synthesize a novel, hidden connection between them.
- **Fleeting Note Processor** (`/fleeting`): Scans an Inbox folder, processes small/quick notes, suggests titles, adds tags, and suggests how to categorize them.
- **[Broken Link Healer](./broken_link_healer)** (`/heal_links`) – Finds unresolved links, uses semantic context to guess the intended existing file, and corrects the link.
- **[Glossary Builder](./glossary_builder)** (`/glossary`) – Analyzes notes to find recurring domain-specific terms and generates a Glossary file with context-inferred definitions.
- **[Smart Web Clipper](./smart_web_clipper)** (`/clip`) – (Scripted slash command) Fetches a webpage via a Python script, cleans it of ads/navigation, and converts it to a clean Markdown note using `/clip <url>`.

## How to Install

1. Drop any of these skill folders into your agent's specified `skills` or `workflows` directory (e.g., `~/.agents/skills/` or `.gemini/antigravity/brain/skills`).
2. The agent will read the `SKILL.md` file to learn how to execute your requests predictably.
3. Prompt your agent (e.g., "Run the Smart Tagger on my latest note").

## Why AI instead of Static Scripts?

While procedural plugins (like Dataview or Templater) are fantastic for fixed patterns, these Agent Skills leverage LLMs to handle **semantic chaos**:
- Finding connections when names are misspelled or conjugated.
- Grouping a Map of Content by *meaning* rather than folders.
- Deducing appropriate tags that aren't specifically mentioned in the text.

## Frameworks & Architecture

This repository also contains a `frameworks/` folder. While skills are actions, frameworks are **architectural guidelines** for your AI agent. 
If you want your agent to strictly follow a methodology (like PARA or Zettelkasten) when organizing incoming data, add the relevant framework `.md` file to your AI context. 

## The "AI Outbox" Philosophy

A core best practice for AI-assisted note-taking is the **AI Outbox**. 
Never let an agent write directly into your core, polished knowledge folders. Instead, configure your agents to save all their generated artifacts, refactored notes, and transcriptions into a dedicated `/AI_Outbox` folder in your vault.

1. Agent creates note in `/AI_Outbox`
2. You review the note for accuracy and hallucinations
3. You manually move the note to its final destination in your vault

This ensures your graph remains pristine and human-verified.
