#!/usr/bin/env python3
"""
Yandex Cloud Instagram Transcriber
===================================
All-in-one script: downloads audio via yt-dlp, uploads to Yandex Object Storage,
transcribes via Yandex SpeechKit async API, polls for result, and prints text.

Credentials are stored securely in ~/.obsidian_agent_secrets.json (Zero-LLM-Contact).

Required system tools: ffmpeg
Required pip packages: yt-dlp, boto3
"""
import os
import sys
import json
import stat
import time
import argparse
import getpass
import tempfile
from pathlib import Path

# --- Lazy imports (checked at runtime) ---
def check_deps():
    try:
        import yt_dlp
        import boto3
        return True
    except ImportError:
        print("❌ Missing dependencies. Run: pip install yt-dlp boto3")
        sys.exit(1)

# ============================================================
# SECURITY MODULE — ~/.obsidian_agent_secrets.json
# ============================================================
SECRET_FILE = Path.home() / '.obsidian_agent_secrets.json'

REQUIRED_KEYS = {
    'YANDEX_API_KEY':  'API-ключ сервисного аккаунта (для SpeechKit)',
    'YANDEX_KEY_ID':   'Статический ключ доступа (идентификатор, для Object Storage)',
    'YANDEX_SECRET':   'Секретный ключ (для Object Storage)',
    'YANDEX_BUCKET':   'Имя бакета в Object Storage',
}

def _load_secrets() -> dict:
    if SECRET_FILE.exists():
        try:
            return json.loads(SECRET_FILE.read_text('utf-8'))
        except json.JSONDecodeError:
            pass
    return {}

def _save_secrets(data: dict):
    SECRET_FILE.touch()
    os.chmod(SECRET_FILE, stat.S_IRUSR | stat.S_IWUSR)  # 600
    SECRET_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), 'utf-8')

def get_yandex_creds() -> dict | None:
    """Return dict with all 4 keys, or None if any is missing."""
    data = _load_secrets()
    creds = {k: data.get(k) for k in REQUIRED_KEYS}
    if all(creds.values()):
        return creds
    return None

def auth_command():
    """Interactive setup — prompts user for each Yandex Cloud credential."""
    print("\n🔐 Yandex Cloud — Безопасная настройка")
    print("=" * 60)
    print("Все токены будут сохранены ЛОКАЛЬНО в вашей домашней директории.")
    print(f"Файл:  {SECRET_FILE}")
    print(f"Права: 600 (только вы)\n")

    data = _load_secrets()

    for key, description in REQUIRED_KEYS.items():
        current = data.get(key)
        hint = f" (текущий: ...{current[-6:]})" if current else ""
        value = getpass.getpass(f"  {description}{hint}\n  [{key}]: ").strip()
        if value:
            data[key] = value
        elif not current:
            print(f"  ⚠ Пропущено — {key} останется пустым.")

    _save_secrets(data)
    print(f"\n✅ Сохранено в {SECRET_FILE}")


# ============================================================
# CORE PIPELINE
# ============================================================
def transcribe(url: str, lang: str = 'ru-RU'):
    check_deps()
    import yt_dlp
    import boto3
    import urllib.request

    creds = get_yandex_creds()
    if not creds:
        print('{"error": "Нет Yandex Cloud токенов. Запустите: run.sh auth"}')
        sys.exit(1)

    # --- 1. Download audio ---
    print("📥 Скачиваю аудио...", file=sys.stderr)
    tmpdir = tempfile.mkdtemp()
    audio_path = os.path.join(tmpdir, 'audio.mp3')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(tmpdir, 'audio.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }],
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        sys.exit(1)

    if not os.path.exists(audio_path):
        print("❌ ffmpeg не смог извлечь аудио. Убедитесь, что ffmpeg установлен.")
        sys.exit(1)

    # --- 2. Upload to Yandex Object Storage ---
    print("☁️  Загружаю в Object Storage...", file=sys.stderr)
    filename = f"transcribe-{int(time.time())}.mp3"

    s3 = boto3.client(
        's3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=creds['YANDEX_KEY_ID'],
        aws_secret_access_key=creds['YANDEX_SECRET'],
    )
    s3.upload_file(audio_path, creds['YANDEX_BUCKET'], filename)

    # --- 3. Send async recognition request ---
    print("🎙️  Отправляю на распознавание (SpeechKit)...", file=sys.stderr)
    request_body = json.dumps({
        "config": {
            "specification": {
                "languageCode": lang,
                "model": "general",
                "audioEncoding": "MP3",
                "literature_text": True,
            }
        },
        "audio": {
            "uri": f"https://storage.yandexcloud.net/{creds['YANDEX_BUCKET']}/{filename}"
        }
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize',
        data=request_body,
        headers={
            'Authorization': f"Api-Key {creds['YANDEX_API_KEY']}",
            'Content-Type': 'application/json',
        },
    )
    with urllib.request.urlopen(req) as resp:
        operation = json.loads(resp.read())
    operation_id = operation['id']

    # --- 4. Poll for result ---
    print(f"⏳ Жду результат (operation: {operation_id})...", file=sys.stderr)
    while True:
        time.sleep(5)
        poll_req = urllib.request.Request(
            f'https://operation.api.cloud.yandex.net/operations/{operation_id}',
            headers={'Authorization': f"Api-Key {creds['YANDEX_API_KEY']}"},
        )
        with urllib.request.urlopen(poll_req) as resp:
            result = json.loads(resp.read())
        if result.get('done'):
            break
        print("  ...ещё не готово, жду 5 сек...", file=sys.stderr)

    # --- 5. Extract text ---
    chunks = result.get('response', {}).get('chunks', [])
    text = ' '.join(
        alt['text']
        for chunk in chunks
        for alt in chunk.get('alternatives', [])[:1]
    )

    print("\n" + "=" * 60)
    print(" 🎬 ТРАНСКРИПТ (Yandex SpeechKit)")
    print("=" * 60)
    print(text)
    print("\n" + "=" * 60)
    print("AI INSTRUCTION:")
    print("Очисти этот сырой транскрипт: расставь знаки пунктуации,")
    print("исправь очевидные ошибки распознавания и оформи как Markdown заметку.")

    # --- 6. Cleanup ---
    try:
        os.remove(audio_path)
        os.rmdir(tmpdir)
    except OSError:
        pass


# ============================================================
# CLI
# ============================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Yandex Cloud Instagram/Video Transcriber'
    )
    sub = parser.add_subparsers(dest='command')

    sub.add_parser('auth', help='Сохранить токены Yandex Cloud')

    fetch_p = sub.add_parser('fetch', help='Скачать и распознать аудио')
    fetch_p.add_argument('url', help='URL видео (Instagram, YouTube, и др.)')
    fetch_p.add_argument('--lang', default='ru-RU',
                         help='Язык распознавания (по умолчанию ru-RU)')

    args = parser.parse_args()
    if args.command == 'auth':
        auth_command()
    elif args.command == 'fetch':
        transcribe(args.url, args.lang)
    else:
        parser.print_help()
