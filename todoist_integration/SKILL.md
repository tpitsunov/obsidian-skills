---
name: Todoist Integration (`/todoist`)
description: Manage Todoist tasks directly. Create, complete, and list tasks safely without leaking your API key to the AI context.
---

# Todoist Workflow

When the user asks you to interact with their Todoist tasks (e.g., list tasks, add a task from meeting notes, complete a task), follow these exact rules.

### Zero-LLM-Contact Security Model
**CRITICAL:** Never ask the user to paste their API key in the chat. The script stores credentials in the OS Keychain and handles authentication transparently.

---

### Step 1: Execute Command(s)
Use the provided `run.sh` wrapper. It auto-creates a virtual environment on first run.

```bash
# To setup authentication (Tell user to run this in their terminal manually if auth fails):
/absolute/path/to/Obsidian-AI-Skills/todoist_integration/run.sh auth

# To list projects (to get IDs):
/absolute/path/to/Obsidian-AI-Skills/todoist_integration/run.sh projects

# To list tasks (supports natural language filters):
/absolute/path/to/Obsidian-AI-Skills/todoist_integration/run.sh list
/absolute/path/to/Obsidian-AI-Skills/todoist_integration/run.sh list --filter "today"

# To add a task:
/absolute/path/to/Obsidian-AI-Skills/todoist_integration/run.sh add "Buy milk" --due "tomorrow" --priority 4

# To complete/close a task by its ID:
/absolute/path/to/Obsidian-AI-Skills/todoist_integration/run.sh close "12345678"
```

### Step 2: Inform the User
After the script runs successfully, briefly confirm to the user what was done.

If the script returns an `Authentication required` error, tell the user to open their terminal and run:
`/path/to/todoist_integration/run.sh auth`
This stores the token in the OS Keychain, completely isolated from the AI context.
