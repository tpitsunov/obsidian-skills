import os
import sys
import json
import stat
import argparse
import getpass
from pathlib import Path

try:
    import yt_dlp
    from openai import OpenAI
except ImportError:
    print("❌ Error: Missing dependencies.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

# --- SECURITY MODULE ---
SECRET_FILE_PATH = Path.home() / '.obsidian_agent_secrets.json'
TOOL_NAME = "WHISPER_API_KEY"

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
    print(f"\n🔐 Whisper API Security Setup")
    print("=" * 60)
    print("For security reasons (Zero-LLM-Contact), you must never paste your OpenAI API tokens into the AI chat.")
    print("This script will securely store your token in your OS home directory.")
    print(f"Target file: {SECRET_FILE_PATH}\n")
    
    token = getpass.getpass("Paste your OpenAI API Key (input will be hidden): ").strip()
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
    
    SECRET_FILE_PATH.touch()
    os.chmod(SECRET_FILE_PATH, stat.S_IRUSR | stat.S_IWUSR)
    
    with open(SECRET_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f)
        
    print(f"\n✅ SUCCESS: '{TOOL_NAME}' securely saved.")

# --- TRANSCRIBE CORE ---
def transcribe_url(url: str):
    token = get_token()
    if not token:
        print('{"error": "Authentication required. Run script with \'auth\' command first."}')
        sys.exit(1)
        
    print("📥 Downloading audio... (This may take a moment depending on the video length)", file=sys.stderr)
    
    filename = "temp_ig_audio"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{filename}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"❌ Error downloading audio. Try again or check the URL: {e}")
        sys.exit(1)
        
    audio_path = f"{filename}.mp3"
    if not os.path.exists(audio_path):
        print("❌ Error: Audio file not generated.")
        print("IMPORTANT: This script requires 'ffmpeg' to be installed on your system.")
        print("Mac: brew install ffmpeg | Windows: winget install ffmpeg")
        sys.exit(1)
        
    print("🎙️ Transcribing with Whisper API...", file=sys.stderr)
    try:
        # Defaults to OpenAI, but user can override OPENAI_BASE_URL internally if they want (e.g., Groq)
        client = OpenAI(api_key=token)
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text"
            )
            
        print("\n" + "=" * 60)
        print(" 🎬 RAW TRANSCRIPT")
        print("=" * 60)
        print(transcript)
        print("\n" + "=" * 60)
        print("AI INSTRUCTION: Clean this raw transcript, fix errors, and format as Markdown.")
        
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secure Audio Fetcher & Transcriber")
    subparsers = parser.add_subparsers(dest="command")
    
    # Auth
    subparsers.add_parser("auth", help="Securely store Whisper API Key")
    
    # Transcribe
    transcribe_parser = subparsers.add_parser("fetch", help="Fetch and transcribe audio from URL")
    transcribe_parser.add_argument("url", help="Instagram/Video URL")
    
    args = parser.parse_args()
    
    if args.command == "auth":
        auth_command()
    elif args.command == "fetch":
        transcribe_url(args.url)
    else:
        parser.print_help()
