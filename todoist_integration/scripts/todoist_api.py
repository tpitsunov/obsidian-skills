import os
import sys
import json
import stat
import urllib.request
import urllib.error
import argparse
import getpass
from pathlib import Path

# --- SECURITY MODULE ---
# The secret file is stored in the OS user's home directory.
# Not in the Obsidian folder, not in Git.
SECRET_FILE_PATH = Path.home() / '.obsidian_agent_secrets.json'
TOOL_NAME = "TODOIST_API_TOKEN"

def get_token():
    if SECRET_FILE_PATH.exists():
        try:
            with open(SECRET_FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get(TOOL_NAME)
        except json.JSONDecodeError:
            pass
    return None

def auth_command():
    print(f"\n🔐 Todoist Security Setup")
    print("=" * 60)
    print("For security reasons (Zero-LLM-Contact), you must never paste your API tokens into the AI chat.")
    print("This script will securely store your token in your OS home directory, completely isolated from Obsidian and Git.")
    print(f"Target file: {SECRET_FILE_PATH}")
    print("Permissions: 600 (Only you can read/write it. System enforces this.)\n")
    
    token = getpass.getpass("Paste your Todoist API Token (input will be hidden): ").strip()
    if not token:
        print("❌ Error: Token cannot be empty.")
        sys.exit(1)
        
    data = {}
    if SECRET_FILE_PATH.exists():
        try:
            with open(SECRET_FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            pass
            
    data[TOOL_NAME] = token
    
    # Touch and set strict mode
    SECRET_FILE_PATH.touch()
    os.chmod(SECRET_FILE_PATH, stat.S_IRUSR | stat.S_IWUSR)
    
    with open(SECRET_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f)
        
    print(f"\n✅ SUCCESS: '{TOOL_NAME}' securely saved.")
    print("Your AI Agent can now use Todoist commands without ever seeing or transmitting your raw token.")
    print("=" * 60)

# --- TODOIST API CORE ---

def api_request(method: str, endpoint: str, data: dict = None) -> dict:
    token = get_token()
    if not token:
        print('{"error": "Authentication required. Run script with \'auth\' command first."}')
        sys.exit(1)
        
    url = f"https://api.todoist.com/rest/v2/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        req_data = json.dumps(data).encode('utf-8') if data else None
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        with urllib.request.urlopen(req) as response:
            if response.status == 204:
                return {"success": True}
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(json.dumps({"error": f"HTTP Error {e.code}", "details": body}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

# --- CLI COMMANDS ---

def cmd_list(project_id: str = None, section_id: str = None, filter: str = None):
    endpoint = "tasks"
    params = []
    if project_id: params.append(f"project_id={project_id}")
    if section_id: params.append(f"section_id={section_id}")
    if filter: params.append(f"filter={urllib.parse.quote(filter)}")
    
    if params:
        endpoint += "?" + "&".join(params)
    
    tasks = api_request("GET", endpoint)
    # Simplify output for LLM context windows
    simplified = [{"id": t.get("id"), "content": t.get("content"), "due": t.get("due", {}).get("string")} for t in tasks]
    print(json.dumps(simplified, indent=2, ensure_ascii=False))

def cmd_add(content: str, due_string: str = None, priority: int = None, project_id: str = None):
    data = {"content": content}
    if due_string: data["due_string"] = due_string
    if priority: data["priority"] = priority
    if project_id: data["project_id"] = project_id
    
    task = api_request("POST", "tasks", data)
    print(json.dumps({"id": task.get("id"), "content": task.get("content"), "due": task.get("due")}, indent=2, ensure_ascii=False))

def cmd_close(task_id: str):
    res = api_request("POST", f"tasks/{task_id}/close")
    print(json.dumps(res, indent=2))

def cmd_projects():
    projects = api_request("GET", "projects")
    simplified = [{"id": p.get("id"), "name": p.get("name")} for p in projects]
    print(json.dumps(simplified, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secure Todoist CLI Wrapper for Obsidian AI Agents")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Auth
    auth_parser = subparsers.add_parser("auth", help="Securely store Todoist API Token")
    
    # List tasks
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--project", help="Project ID")
    list_parser.add_argument("--filter", help="Natural language filter (e.g. 'today')")
    
    # List projects
    subparsers.add_parser("projects", help="List all projects")
    
    # Add Task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("content", help="Task name / content")
    add_parser.add_argument("--due", help="Due string (e.g. 'tomorrow')")
    add_parser.add_argument("--priority", type=int, help="Priority (1-4, where 4 is urgent)")
    add_parser.add_argument("--project", help="Project ID")
    
    # Close Task
    close_parser = subparsers.add_parser("close", help="Close/complete a task")
    close_parser.add_argument("task_id", help="The ID of the task to close")
    
    args = parser.parse_args()
    
    if args.command == "auth":
        auth_command()
    elif args.command == "list":
        cmd_list(project_id=args.project, filter=args.filter)
    elif args.command == "projects":
        cmd_projects()
    elif args.command == "add":
        cmd_add(args.content, due_string=args.due, priority=args.priority, project_id=args.project)
    elif args.command == "close":
        cmd_close(args.task_id)
    else:
        parser.print_help()
