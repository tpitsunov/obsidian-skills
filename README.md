# Obsidian AI Skills Repository

A collection of AI Agent Skills (Workflows) designed to automate, clean up, and interlink your Obsidian Vault. These are built in the standard AI Skill format (`SKILL.md` with YAML frontmatter) for use with your preferred AI coding assistant or agent.

## Available Skills

- **[Vault Statistics](./obsidian_stats)** (`/stats`) – Procedurally calculates vault metrics using a Python script.
- **[Table of Contents Generator](./toc_generator)** (`/toc`) – Analyzes multiple header levels in a long markdown file and generates a clickable Table of Contents.
- **[Minimalist Distiller](./minimalist_distiller)** (`/distill` or `/tldr`) – Aggressively reduces verbose notes to dry bullet points, non-obvious facts, and actionable insights.
- **[Todoist Integration](./todoist_integration)** (`/todoist`) – Manage Todoist tasks directly. Create, complete, and list tasks safely using a zero-LLM-contact secret manager.
- **[Broken Link Healer](./broken_link_healer)** (`/heal_links`) – Finds unresolved links, uses semantic context to guess the intended existing file (handling typos and aliases), and corrects the link.
- **[Zettel Atomizer](./zettel_atomizer)** (`/atomize`) – Advanced, lossless procedural text splitter that extracts cohesive thoughts from a long document into standalone Zettels.
- **[Smart Web Clipper](./smart_web_clipper)** (`/clip`) – Fetches a webpage via a Python script, cleans it of ads/navigation, and converts it to a clean Markdown note.
- **[Markdown Linter](./markdown_linter)** (`/lint`) – Cleans up messy markdown pasted from the web.
- **[Instagram Transcriber](./instagram_transcribe)** (`/ig-transcribe`) – Download and transcribe Instagram Reels/TikToks directly to clean notes using a local Whisper API and private `yt-dlp` environment.
- **[YouTube Transcriber](./youtube_transcribe)** (`/yt-transcript`) – A zero-dependency script to download pure subtitles from any YouTube video and format them into readable notes.
- **[Knowledge Merger](./knowledge_merger)** (`/merge`) – Intelligently updates "master" notes by identifying net-new facts in a rough source note and mapping them to the correct sections of the master document.
- **[Serendipity Engine](./serendipity_engine)** (`/spark`) – Pulls completely random notes from the vault and challenges the AI to synthesize a novel, hidden connection between them.
- **[Orphan Note Connector](./orphan_connector)** (`/orphans`) – Finds disconnected notes and suggests intelligent semantic connections mapped to your existing files.
- **[Fleeting Note Processor](./fleeting_processor)** (`/fleeting`) – Scans an Inbox folder, processes small/quick notes, suggests titles, adds tags, and suggests how to categorize them.
- **[MOC Builder](./moc_builder)** (`/moc`) – Automatically grouped Map of Content (Index) generation based on semantics, not just alphabet.
- **[Glossary Builder](./glossary_builder)** (`/glossary`) – Analyzes notes to find recurring domain-specific terms and generates a Glossary file with context-inferred definitions.
- **[Smart Tagger](./smart_tagger)** (`/tag`) – Reads your note's context, cross-references your vault's tags, and populates YAML frontmatter.

## How to Install

1. Drop any of these skill folders into your agent's specified `skills` or `workflows` directory (e.g., `~/.agents/skills/` or `.gemini/antigravity/brain/skills`).
2. The agent will read the `SKILL.md` file to learn how to execute your requests predictably.
3. Prompt your agent (e.g., "Run the Smart Tagger on my latest note").

## Security: Zero-LLM-Contact

This repository follows a strict **Zero-LLM-Contact** security model for sensitive data (API keys, tokens). 

- **No `.env` files**: We avoid global environment files that could be accidentally committed or read by the LLM.
- **Local Secret Vault**: Secrets are stored in `~/.obsidian_agent_secrets.json` with restricted OS-level permissions (`600`).
- **Transparent Auth**: Python wrappers handle authentication locally. The LLM agent never sees, handles, or requests your API keys in the chat.
- **No Obsidian Sync Leakage**: Because secrets are stored in your home directory (outside the vault), they are never synced via Obsidian Sync or Git.

To set up a skill that requires an API key, run its `run.sh auth` command in your terminal when prompted by the agent.

## Why AI instead of Static Scripts?

While procedural plugins (like Dataview or Templater) are fantastic for fixed patterns, these Agent Skills leverage LLMs to handle **semantic chaos**:
- Finding connections when names are misspelled or conjugated.
- Grouping a Map of Content by *meaning* rather than folders.
- Deducing appropriate tags that aren't specifically mentioned in the text.


## The "AI Outbox" Philosophy

A core best practice for AI-assisted note-taking is the **AI Outbox**. 
Never let an agent write directly into your core, polished knowledge folders. Instead, configure your agents to save all their generated artifacts, refactored notes, and transcriptions into a dedicated `/AI_Outbox` folder in your vault.

1. Agent creates note in `/AI_Outbox`
2. You review the note for accuracy and hallucinations
3. You manually move the note to its final destination in your vault

This ensures your graph remains pristine and human-verified.
