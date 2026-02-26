---
name: Table of Contents Generator
description: Analyzes multiple header levels in a long markdown file and generates or updates a clickable Table of Contents at the top of the file.
---

# Table of Contents Generator Workflow

When the user uses the slash command `/toc` or asks you to generate, build, or update a Table of Contents (ToC) for a specific note, follow these steps:

1. **Analyze File Structure**: Read the target markdown file. Scan the document for all Markdown headers (H1 to H6, e.g., `# Header`, `## Subheader`).
   - *Note:* Ignore headers that are contained within code blocks (\`\`\`).
2. **Build the ToC**: Construct a Markdown list that represents the hierarchy of the headers.
   - Use indentation to represent header levels (e.g., H2 indented under H1, H3 indented under H2).
   - Create standard Markdown links pointing to the headers. In standard Obsidian markdown, a link to a header within the same file is formatted as `[[#Header Name]]`. If the user has a different preference for internal header links (e.g., standard markdown anchors like `[Header Name](#header-name)`), adapt accordingly. Usually, `[[#Header Name]]` is best for Obsidian.
3. **Locate or Create ToC Section**:
   - Check if there is already a `## Table of Contents` or `## ToC` header near the top of the file (usually right below the frontmatter or main title H1).
   - If it exists, replace the content below it with your newly generated ToC.
   - If it does not exist, insert it below the YAML frontmatter (if any) and the main H1 title. Add a `## Table of Contents` header followed by the generated list.
4. **Apply Changes**: Update the file content with the new or modified Table of Contents layout.
5. **Notify User**: Inform the user that the Table of Contents has been successfully generated or updated.
