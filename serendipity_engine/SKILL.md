---
name: Serendipity Engine (`/spark`)
description: Break through writer's block by forcing accidental connections between completely random notes in your Zettelkasten.
---

# Serendipity Engine Workflow

When the user uses the slash command `/spark [folder] [count]` or asks to "generate ideas", "find connections", or "ignite a spark", follow these precise steps:

### Step 1: Ignite the Engine
Run the included Python script to physically draw a random sample of notes from the vault (or a specific folder, ideally a Zettelkasten or Resources folder).
```bash
python /absolute/path/to/Obsidian-AI-Skills/serendipity_engine/scripts/spark.py "/absolute/path/to/vault" --folder "Optional/Folder/Path" --count 3
```

### Step 2: Read and Synthesize
The python script will output the content of the random notes directly into your context. 

Your task is to read these deeply disconnected ideas and act as a creative synthesizer:
1. **Find the Hidden Thread**: Brainstorm a novel philosophical, logical, thematic, or metaphorical connection that ties *all* of these random concepts together.
2. **Draft a Synthesis Note**: Write a short, compelling paragraph that articulates this new insight.

### Step 3: Present the Spark
Present your synthesis to the user in a highly readable format:
- List the `[[Random Notes]]` that triggered the idea.
- Present the **Synthesis** paragraph.
- Ask the user: *"Would you like me to save this new insight as its own Zettel note?"* 

### Step 4: Save (Optional)
If the user agrees, create a new Markdown file in their vault documenting this synthesized connection, making sure to include links back to the original source notes that sparked it.
