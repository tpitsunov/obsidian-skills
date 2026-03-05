---
name: Instagram Transcriber (`/ig-transcribe`)
description: Download and transcribe Instagram Reels, TikToks, or similar short media directly to a clean note using Whisper API.
---

# Instagram Transcriber Workflow

When the user gives you a video link (e.g. `/ig-transcribe <url>`), follow these steps using the fully local, isolated python script.

### Zero-LLM-Contact Security Model
**CRITICAL:** Never ask the user to paste their OpenAI API key in the chat. The Python script handles authentication transparently.

### System Requirements
This script relies on `yt-dlp` which requires **FFmpeg** to be installed on the user's host machine.

### Step 1: Execute Python Command
The python wrapper will download the audio (via `yt-dlp`), send it to the Whisper API, and print the raw transcribed text.

**CRITICAL: VIRTUAL ENVIRONMENT**
This script must be run from an isolated virtual environment to avoid polluting the user's global Python installation.

If the `.venv` directory doesn't exist in the folder, create it and install requirements:
```bash
cd /absolute/path/to/Obsidian-AI-Skills/instagram_transcribe
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run the script **using the isolated python binary**:
```bash
# Setup authentication (if auth error occurs):
/absolute/path/to/Obsidian-AI-Skills/instagram_transcribe/.venv/bin/python /absolute/path/to/Obsidian-AI-Skills/instagram_transcribe/scripts/ig_fetch.py auth

# Transcribe URL:
/absolute/path/to/Obsidian-AI-Skills/instagram_transcribe/.venv/bin/python /absolute/path/to/Obsidian-AI-Skills/instagram_transcribe/scripts/ig_fetch.py fetch "URL_HERE"
```

### Step 2: Read and Format
The underlying Whisper model might lack punctuation or have spelling errors. 

Your job as an AI is to act as an expert editor on the returned raw text:
1. Fix any obvious speech-to-text recognition errors.
2. Add proper punctuation.
3. Add markdown formatting (Headers, bold text).
4. Do NOT hallucinate content not in the transcript, just clean it up.
