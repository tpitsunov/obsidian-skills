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
To ensure the user's host machine is not polluted, this skill uses an isolated virtual environment.

Run the script exclusively through the provided `run.sh` bash wrapper. The wrapper will automatically build the environment if it doesn't exist and pass your arguments to the script transparently.

```bash
# Setup authentication (if auth error occurs):
/absolute/path/to/Obsidian-AI-Skills/instagram_transcribe/run.sh auth

# Transcribe URL:
/absolute/path/to/Obsidian-AI-Skills/instagram_transcribe/run.sh fetch "URL_HERE"
```

### Step 2: Read and Format
The underlying Whisper model might lack punctuation or have spelling errors. 

Your job as an AI is to act as an expert editor on the returned raw text:
1. Fix any obvious speech-to-text recognition errors.
2. Add proper punctuation.
3. Add markdown formatting (Headers, bold text).
4. Do NOT hallucinate content not in the transcript, just clean it up.
