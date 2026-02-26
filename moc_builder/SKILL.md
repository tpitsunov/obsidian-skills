---
name: MOC Builder
description: Create a Map of Content (MOC) index note for a specific folder or tag.
---

# Map of Content (MOC) Builder Workflow

When the user uses the slash command `/moc [folder/tag]` or asks to build a Map of Content (MOC) or an index for a specific folder or tag, follow these steps:

1. **Identify the Scope**: Determine which folder or tag the user wants to map.
2. **Gather Notes**: 
   - If a folder: Use file listing tools (`list_dir`, `find_by_name`) to get all `.md` files in that folder.
   - If a tag: Use text search tools (`grep_search`) to find all files containing that tag.
3. **Analyze Content**: Read the first 100-200 lines of each note to understand its main topic, entities, and purpose. If there are too many notes, ask the user if they want to process them in batches.
4. **Group by Semantic Similarity**: Group the gathered notes into logical categories or sub-topics based on your understanding of their content.
5. **Generate the MOC Content**:
   - Create a title `# MOC: [Folder/Tag Name]`.
   - Write a short introduction explaining what this topic covers.
   - Create sections for each semantic category (`## Category Name`).
   - For each note, create a wiki-link `[[NoteFileName]]` followed by a concise 1-sentence annotation detailing its contents.
6. **Save the MOC**: Create or over-write `_MOC_[Name].md` (or index name specified by user) in the target directory.
7. **Review**: Present the MOC to the user for review and ask if they want any changes to the categorization.
