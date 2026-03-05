#!/usr/bin/env bash
# Auto-bootstrapping wrapper for Yandex Cloud transcriber
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -d "$DIR/.venv" ]; then
    echo "⚙️  Первый запуск: создаю виртуальное окружение и устанавливаю зависимости..."
    python3 -m venv "$DIR/.venv"
    "$DIR/.venv/bin/pip" install -r "$DIR/requirements.txt" > /dev/null 2>&1
    echo "✅ Установка завершена."
fi

"$DIR/.venv/bin/python" "$DIR/scripts/yc_transcribe.py" "$@"
