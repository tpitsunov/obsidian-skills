---
name: Orphan Note Connector
description: Find unlinked notes and suggest relevant semantic connections to other notes in the vault.
---

# Orphan Note Connector Workflow

When the user uses the slash command `/orphans` or asks to connect an orphan note or find connections for a specific note, follow these steps:

1. **Identify the Target**: Understand which note the user wants to process. If they want you to find an orphan note, search for notes with few/no connections (no `[[` or `]]`).
2. **Read the Note**: Read the target note thoroughly to understand its context.
3. **Extract Entities & Themes**: Identify the main keywords, named entities (characters, locations, organizations, concepts), and overarching themes in the text.
4. **Search the Vault**: Search the workspace for the extracted keywords and entities to find other notes that mention them but are not currently linked.
5. **Determine Connections**: Select the 3-5 most conceptually relevant notes from the search results.
6. **Propose Links**: Inform the user about the suggested connections. Explain *why* these notes should be linked and show a snippet of how the text could be changed to include a wiki-link `[[Target Note]]`.
7. **Apply Changes**: Upon user confirmation, edit the file to insert the wiki-links directly into the text. You can either turn existing words into links or add a 'Related:' section at the bottom.
