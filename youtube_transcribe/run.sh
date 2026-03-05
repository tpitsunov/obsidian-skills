#!/usr/bin/env bash
# Resolves the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check for virtual environment and create if missing
if [ ! -d "$DIR/.venv" ]; then
    echo "⚙️  First-time setup: Creating virtual environment and installing dependencies..."
    python3 -m venv "$DIR/.venv"
    "$DIR/.venv/bin/pip" install -r "$DIR/requirements.txt" > /dev/null 2>&1
    echo "✅ Setup complete."
fi

# Execute the python script inside the isolated environment, passing all arguments
"$DIR/.venv/bin/python" "$DIR/scripts/yt_fetch.py" "$@"
