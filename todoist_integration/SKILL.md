---
name: todoist
description: Manage Todoist tasks — list, create, complete, delete, and filter tasks or projects. Use when the user asks about their tasks, todos, or wants to add/complete something in Todoist.
---

You have access to the Todoist API v1 via curl. The API token is in the environment variable `TODOIST_API_TOKEN`. Always use `-4` flag (IPv4 only) with curl to avoid IPv6 connection issues.

## Base URL
`https://api.todoist.com/api/v1`

## Auth header
`Authorization: Bearer $TODOIST_API_TOKEN`

## Common operations

**List all projects:**
```bash
curl -s -4 -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  https://api.todoist.com/api/v1/projects | jq '[.results[] | {id, name}]'
```

**List all active tasks:**
```bash
curl -s -4 -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  https://api.todoist.com/api/v1/tasks | jq '[.results[] | {id, content, due, priority, project_id}]'
```

**List tasks in a project:**
```bash
curl -s -4 -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/api/v1/tasks?project_id=PROJECT_ID" | jq '[.results[] | {id, content, due, priority}]'
```

**Create a task:**
```bash
curl -s -4 -X POST -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Task name", "due_string": "tomorrow", "priority": 4}' \
  https://api.todoist.com/api/v1/tasks | jq '{id, content, due}'
```

**Complete (close) a task:**
```bash
curl -s -4 -X POST -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  https://api.todoist.com/api/v1/tasks/TASK_ID/close
```

**Delete a task:**
```bash
curl -s -4 -X DELETE -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  https://api.todoist.com/api/v1/tasks/TASK_ID
```

**Update a task:**
```bash
curl -s -4 -X POST -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "New name", "due_string": "next monday"}' \
  https://api.todoist.com/api/v1/tasks/TASK_ID | jq '{id, content, due}'
```

**Filter tasks (e.g. today or overdue):**
```bash
curl -s -4 -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/api/v1/tasks?filter=today" | jq '[.results[] | {id, content, due, priority}]'
```

## Priority levels
- 1 = normal (default)
- 2 = medium
- 3 = high
- 4 = urgent

## Notes
- `due_string` accepts natural language: "today", "tomorrow", "next monday", "every day"
- Responses are paginated under `.results[]`
- Task IDs come from listing tasks — always list first if you don't know the ID
- Always use `jq` to format responses for readability
