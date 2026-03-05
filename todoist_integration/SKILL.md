---
name: Todoist Integration (`/todoist`)
description: Manage Todoist tasks directly. Create, complete, and list tasks safely without leaking your API key to the AI context.
---

# Todoist Workflow

When the user asks you to interact with their Todoist tasks (e.g., list tasks, add a task from meeting notes, complete a task), follow these exact rules.

### Zero-LLM-Contact Security Model
**CRITICAL:** Never ask the user to paste their API key in the chat. Never attempt to read hidden credential files (like `~/.obsidian_agent_secrets.json`). The Python script handles authentication transparently in the background to ensure your context is 100% secure.

---

### Step 1: Execute Python Command(s)
Use the included python wrapper to interact with Todoist. It parses endpoints and limits payload garbage automatically.

```bash
# To setup authentication (Tell user to run this in their terminal manually if auth fails):
python /absolute/path/to/Obsidian-AI-Skills/todoist_integration/scripts/todoist_api.py auth

# To list projects (to get IDs):
python /absolute/path/to/Obsidian-AI-Skills/todoist_integration/scripts/todoist_api.py projects

# To list tasks (supports natural language filters):
python /absolute/path/to/Obsidian-AI-Skills/todoist_integration/scripts/todoist_api.py list
python /absolute/path/to/Obsidian-AI-Skills/todoist_integration/scripts/todoist_api.py list --filter "today"

# To add a task:
python /absolute/path/to/Obsidian-AI-Skills/todoist_integration/scripts/todoist_api.py add "Buy milk" --due "tomorrow" --priority 4

# To complete/close a task by its ID:
python /absolute/path/to/Obsidian-AI-Skills/todoist_integration/scripts/todoist_api.py close "12345678"
```

### Step 2: Inform the User
After the script runs successfully, briefly confirm to the user what was done (e.g., "I've added the 3 action items from your note to your Todoist Inbox for tomorrow.").

If the script returns an `Authentication required` error, tell the user gracefully to open their terminal and run:
`python /path/to/todoist_integration/scripts/todoist_api.py auth`
Explain that this securely stores their token in their OS keychain, protecting it from flying into the AI provider's servers.
