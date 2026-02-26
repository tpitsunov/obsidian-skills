---
name: Markdown Linter
description: Clean up and format a messy Markdown note to a standard Obsidian style.
---

# Markdown Linter & Formatter Workflow

When the user uses the slash command `/lint` or asks to clean up, format, or lint a note, follow these steps:

1. **Read the Note**: Read the contents of the target note.
2. **Analyze Formatting Issues**: Scan the text for common Markdown mistakes:
   - Multiple consecutive blank lines.
   - Double or trailing spaces.
   - Broken list structures (wrong indentation, inconsistent bullet characters).
   - Poorly structured links (e.g., raw URLs instead of `[Title](Link)`).
   - Incorrect header levels (e.g., jumping from `#` to `###` without a `##`, or lacking spaces after `#`).
3. **Generate Cleaned Version**: Reformat the text to strict, clean Markdown while preserving all the content and logic. Ensure proper spacing, consistent lists, and correct headers.
4. **Apply Corrections**: Update the note with the cleaned Markdown.
5. **Report Changes**: Provide a concise summary to the user outlining the formatting rules that were applied.
