#!/usr/bin/env bash
# Auto-bootstrapping wrapper for Todoist Integration
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -d "$DIR/.venv" ]; then
    echo "⚙️  First run: creating virtual environment and installing dependencies..."
    python3 -m venv "$DIR/.venv"
    "$DIR/.venv/bin/pip" install -r "$DIR/requirements.txt" > /dev/null 2>&1
    echo "✅ Setup complete."
fi

"$DIR/.venv/bin/python" "$DIR/scripts/todoist_api.py" "$@"
