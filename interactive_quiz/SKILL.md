---
name: Interactive Quiz (`/quiz`)
description: Challenges the user to a scenario-based interview or exam on a specific note. The AI generates challenging questions one by one and grades responses.
---

# Interactive Quiz Workflow

When the user gives the slash command `/quiz` (or asks to be "tested", "interviewed", or "quizzed" on a note), you must transform from an assistant into a rigorous interviewer.

### Step 1: Read and Synthesize
1. Identify the target note the user wants to be tested on.
2. Read the entire note to understand the core facts, trade-offs, and architectural decisions.
3. Formulate **3 to 5** challenging, scenario-based questions.
   - **Bad Question**: "What is the definition of Inertia?"
   - **Good Question**: "Given a spaceship in zero-gravity moving at a constant velocity, what happens to the cargo inside if the engine suddenly fires a retro-burn? Explain using the concept of Inertia."

### Step 2: The Interview Loop (STOP HERE)
**Do not list all questions at once.** You must engage in a back-and-forth loop:
1. Pose **Question 1** only.
2. **Stop and Wait** for the user's response in the chat.
3. Once the user responds:
   - Provide feedback/grading on their answer.
   - Pose **Question 2**.
   - Repeat until all questions are answered.

### Step 3: Final Score
After the final question is answered, provide a summary:
1. **Overall Grade**: (e.g., A, B, C or Pass/Fail).
2. **Key Strengths**: What did the user understand well?
3. **Knowledge Gaps**: What areas/sections in the note should they re-read?

---
*Ready to begin? Pitch Question 1 to the user now.*
