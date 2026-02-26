---
name: MOC Builder
description: Create a Map of Content (MOC) index note for a specific folder or tag.
---

# Map of Content (MOC) Builder Workflow

When the user uses the slash command `/moc [folder/tag]` or asks to build a Map of Content (MOC) or an index for a specific folder or tag, follow these steps:

1. **Identify the Scope**: Determine which folder or tag the user wants to map.
2. **Gather Condensed Data**: **Do not read the raw files yourself.** To save context tokens and ensure accuracy, run the Python script to extract metadata (tags, H1s, or first-paragraph excerpts) from the target directory:
   ```bash
   python /absolute/path/to/Obsidian-AI-Skills/moc_builder/scripts/gather_data.py "/absolute/path/to/vault" --folder "Folder/Path/If/Requested"
   ```
3. **Analyze Condensed Output**: Read the condensed summary list provided by the script. (If filtering by tag, just ignore files in the script output that don't possess the requested tag).
4. **Group by Semantic Similarity**: Group the gathered notes into logical categories or sub-topics based on your understanding of their titles and excerpts.
5. **Generate the MOC Content**:
   - Create a title `# MOC: [Folder/Tag Name]`.
   - Write a short introduction explaining what this topic covers.
   - Create sections for each semantic category (`## Category Name`).
   - For each note, create a wiki-link `[[NoteFileName]]` followed by a concise 1-sentence annotation detailing its contents.
6. **Save the MOC**: Create or over-write `_MOC_[Name].md` (or index name specified by user) in the target directory.
7. **Review**: Present the MOC to the user for review and ask if they want any changes to the categorization.
