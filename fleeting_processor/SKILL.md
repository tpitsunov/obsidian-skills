---
name: Fleeting Note Processor
description: Scans an Inbox folder, processes small/quick notes, suggests titles, adds tags, and suggests moving them.
---

# Fleeting Note Processor Workflow

When the user uses the slash command `/fleeting` or asks you to process, clean up, or organize fleeting notes (usually found in an "Inbox" or "Drafts" folder), follow these steps:

1. **Locate Notes**: Find all markdown files in the specified folder (e.g., `Inbox`). If no folder is specified, ask the user.
2. **Read & Analyze**: Evaluate the contents of each small note. What is the main idea? Is it a task, a random thought, a link, or a draft of a larger idea?
3. **Generate Titles**: If the note is unnamed (e.g., `Untitled`, `Note 1`), suggest a descriptive, concise title based on its content (3-5 words).
4. **Determine Tags**: Assign 1-3 appropriate tags based on the vault's existing tag structure and the note's topic.
5. **Suggest Meaningful Connections**: Search the vault for existing files related to the fleeting note's subject. Formulate `[[wikilinks]]` to tie this note into the user's broader knowledge base.
6. **Suggest Location/Folder**: Recommend an appropriate final destination folder for the note (e.g., `Projects`, `Journal`, `Zettelkasten`, `Resources`).
7. **Execution/Action Phase**: Ask the user for confirmation to apply the changes (Renaming the file, injecting tags into the YAML frontmatter, adding bottom links, and moving the file). Once confirmed, execute all file operations.
8. **Summary**: Provide a clear summary of what was renamed, tagged, linked, and moved.
