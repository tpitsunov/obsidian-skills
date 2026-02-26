---
name: Broken Link Healer
description: Finds unresolved links, uses semantic context to guess the intended existing file, and corrects the link.
---

# Broken Link Healer Workflow

When the user uses the slash command `/heal_links` or asks to heal, format, or fix broken links in a specific file or folder, follow these steps:

1. **Execute Healer Script**: Run the deterministic Python script against the target file. The script parses all links, cross-references them against *every* file in the vault (regardless of folder depth), and uses fuzzy string matching to find the 3 closest actual files for any broken links.
   ```bash
   python /absolute/path/to/Obsidian-AI-Skills/broken_link_healer/scripts/heal_links.py "/absolute/path/to/vault" "/absolute/path/to/target_file.md"
   ```
2. **Review Output**: Read the script's output, which will list exact broken links and the top 3 highly probable existing file replacements.
3. **Propose Corrections To User**: Present the script's findings. If a link should be replaced dynamically to preserve the sentence structure (e.g., changing `[[apples]]` to `[[Apple|apples]]`), suggest that format.
5. **Confirm and Apply Changes**: Show the proposed replacements to the user. Upon confirmation, update the target Markdown files, replacing the broken markdown syntax with the correct links.
6. **Notify**: Advise the user if any links appear truly orphaned (no suitable matching file exists and the note might need to be created from scratch).
