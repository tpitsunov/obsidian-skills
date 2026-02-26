---
name: Smart Tagger
description: Automatically analyze a note and add appropriate tags to its YAML frontmatter based on existing vault tags.
---

# Smart Tagger & Cataloger Workflow

When the user uses the slash command `/tag` or asks to analyze and tag a note, follow these steps:

1. **Understand Note Context**: Read the target note and extract its core topics, entities, and context.
2. **Identify Existing Vault Tags**: 
   - If you don't already know the user's tag taxonomy, search the vault targeting `tags:` or `#` to see what tags the user typically uses. *Do not hallucinate tags if possible; prioritize existing ones.*
3. **Determine Best Tags**: Select 3-5 fitting tags based on the note's content. Include broader category tags and specific thematic tags.
4. **Determine Target Path**: Check the note to see if it already has YAML frontmatter at the very top.
   - If NO frontmatter exists: Prepend standard frontmatter indicating the new tags.
     ```yaml
     ---
     tags:
       - tag1
       - tag2
     ---
     ```
   - If frontmatter exists but NO tags: Insert the `tags:` field.
   - If `tags:` already exists: Append only the new, unique tags to the existing list.
5. **Apply Frontmatter**: Update the file content to inject or update the YAML frontmatter of the note.
6. **Optional Categorization**: If the note seems out of place, suggest moving it to a more appropriate folder based on its new tags.
7. **Notify User**: Show the user the tags that were added.
