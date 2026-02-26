---
name: Table of Contents Generator
description: Analyzes multiple header levels in a long markdown file and generates or updates a clickable Table of Contents at the top of the file.
---

# Table of Contents Generator Workflow

When the user uses the slash command `/toc` or asks you to generate, build, or update a Table of Contents (ToC) for a specific note, follow these steps:

1. **Generate ToC via Script**: Use the included Python script to instantly parse the document structure, ignore code blocks/YAML, and generate the perfect indent-level Table of Contents snippet.
   ```bash
   python /absolute/path/to/Obsidian-AI-Skills/toc_generator/scripts/generate_toc.py "/absolute/path/to/target_file.md"
   ```
2. **Review Output**: Read the standard output from the script, which contains the exact Markdown block for the ToC.
3. **Insert the ToC**: Ask the user where they want the ToC placed, or edit the file directly to insert the generated snippet right below the first `H1` header.
4. **Apply Changes**: Update the file content with the new or modified Table of Contents layout.
5. **Notify User**: Inform the user that the Table of Contents has been successfully generated or updated.
