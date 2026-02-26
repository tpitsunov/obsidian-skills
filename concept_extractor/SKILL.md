---
name: Concept Extractor
description: Reads a large note, extracts 3-5 key concepts, creates new atomic notes for each, and maps them back into the original text.
---

# Concept Extractor (Zettelkasten Atomizer) Workflow

When the user uses the slash command `/extract` or asks you to extract concepts, atomize, or break down a large target note, follow these steps:

1. **Read & Analyze**: Read the full content of the target note. Understand the core topics and distinct ideas being discussed.
2. **Extract Key Concepts**: Identify 3-5 distinct, independent ideas, theories, or concepts that can stand alone as separate "atomic" notes (Zettelkasten principle).
3. **Create Atomic Notes**: 
   - For each extracted concept, formulate a clear, descriptive title.
   - Create a **new markdown file** for each concept in the vault. 
   - In each new file, write a concise summary (1-3 paragraphs) explaining the concept based ONLY on the original text. Add a `Source: [[Original Note Name]]` link at the bottom connecting it back to the original text.
   - Apply general tags if appropriate.
4. **Update Original Note**: 
   - Go back to the original note. 
   - Find the exact words or paragraphs where the concept was discussed.
   - Replace the inline mentions of the concept with links to the newly created notes (e.g., replacing "the theory of relativity" with "[[Theory of Relativity]]").
   - *Alternatively*, if inline replacement is too destructive to the original text formatting, you can append an "Extracted Concepts" section at the bottom of the original note containing links to the new atomic notes. Ask the user for their preference if unsure.
5. **Notify User**: Show the user a summary of the atomic notes that were created and successfully linked.
