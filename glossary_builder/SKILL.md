---
name: Glossary / Terminology Builder
description: Analyzes notes to find recurring domain-specific terms and generates a Glossary file with context-inferred definitions.
---

# Glossary Builder Workflow

When the user uses the slash command `/glossary [folder]` or asks you to build, create, or update a Glossary or Terminology index based on a specific folder, project, or domain, follow these steps:

1. **Scan Target Directory**: Read all Markdown files within the scope provided by the user (e.g., all files in `/Biology Class` or a specific set of project notes).
2. **Extract Terminology**: 
   - Look for domain-specific terminology, acronyms, jargon, or heavily repeated key phrases that might require definition.
   - Ignore common words or general concepts. Focus on highly specific nouns and phrases.
3. **Infer Definitions**: For each extracted term, read its surrounding context across the analyzed notes. Synthesize a concise (1-2 sentence) definition based purely on how the user has used it in their notes. Do not hallucinate external definitions unless instructed.
4. **Identify Primary Sources**: Keep track of the file(s) where the term was most prominently defined or heavily used.
5. **Generate Glossary Note**:
   - Create a new file (or append to an existing one) named `Glossary.md` or as requested by the user.
   - Structure the file alphabetically.
   - For each term, format it as:
     `**Term**`: The synthesized definition. (Source: `[[File Location]]`)
   - Alternatively, use a Markdown table format if preferred or instructed.
6. **Update Links (Optional)**: If requested by the user, you can go back to the source documents and turn the first mention of each term into a backlink pointing to the new `[[Glossary#Term]]` header. Focus on maintaining a clean vault structure.
7. **Notify User**: Display a sample of the definitions created and indicate where the new Glossary file was saved.
