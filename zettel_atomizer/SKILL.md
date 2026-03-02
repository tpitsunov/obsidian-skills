---
name: Zettel Atomizer (`/atomize`)
description: Break down long, rambling essays into atomic Zettelkasten notes without hallucinating or losing text.
---

# Zettel Atomizer Workflow

When the user uses the slash command `/atomize` or asks you to "extract concepts", "split this essay", or "atomize this note", follow these precise steps. **Do not read the file manually using text tools.** This process guarantees lossless text extraction while saving your context tokens.

### Step 1: Prepare the Text
Run the Python script to chop the file into numbered paragraphs. This allows you to reference blocks by number.
```bash
python /absolute/path/to/Obsidian-AI-Skills/zettel_atomizer/scripts/atomizer.py prepare "/absolute/path/to/target/file.md"
```

### Step 2: Analyze and Index
Read the output of the script. Identify 1 to 4 independent, atomic concepts buried in the text.
Create a strict JSON configuration block describing how the text should be split. 

- `title`: The title of the new Zettel (will be used as filename and H1).
- `tags`: An array of semantic Zettelkasten tags.
- `blocks`: The integer IDs of the paragraphs (from Step 1) that should be removed from the main article and placed into this Zettel. They do *not* strictly need to be contiguous.

**Example JSON Response formatting:**
```json
[
  {
    "title": "Capitalism and Biological Limits",
    "tags": ["capitalism", "ecology", "philosophy"],
    "blocks": [2, 3, 4]
  },
  {
    "title": "The Growth Imperative",
    "tags": ["economics", "growth"],
    "blocks": [7, 8]
  }
]
```

Write this raw JSON to a temporary file in the workspace, e.g., `/Users/casi/projects/obsidian-skills/tmp_instructions.json`.

### Step 3: Apply the Split
Execute the Python script again, feeding it the JSON instructions you just generated. The script will physically create the new notes and safely replace the extracted text in the original document with `[[Wikilinks]]`.
```bash
python /absolute/path/to/Obsidian-AI-Skills/zettel_atomizer/scripts/atomizer.py split "/absolute/path/to/target/file.md" "/absolute/path/to/tmp_instructions.json" "/absolute/path/to/target_directory_for_zettels"
```

### Step 4: Cleanup & Notify
Delete your temporary JSON file. Present the user with a summary of the Zettels that were created and successfully linked into the parent article.
