---
name: YouTube Transcriber (`/yt-transcript`)
description: A zero-dependency skill to download pure subtitles from any YouTube video and format them into readable notes.
---

# YouTube Transcriber Workflow

When the user asks you to extract or transcribe a YouTube video (`/yt-transcript <url>`), follow these precise steps:

### Step 1: Execute Python Fetcher

Run the lightweight python script to securely and privately fetch the video's subtitle track. This script extracts raw text without burning your context limits on timestamps or requiring third-party API keys.

**CRITICAL: VIRTUAL ENVIRONMENT**
This script requires the `youtube-transcript-api` package. It must be run from an isolated virtual environment to avoid polluting the user's global Python installation.

If the `.venv` directory doesn't exist in the `youtube_transcribe` folder, create it and install the requirements first:
```bash
cd /absolute/path/to/Obsidian-AI-Skills/youtube_transcribe
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Once the environment is ready, run the script **using the isolated python binary**:
```bash
/absolute/path/to/Obsidian-AI-Skills/youtube_transcribe/.venv/bin/python /absolute/path/to/Obsidian-AI-Skills/youtube_transcribe/scripts/yt_fetch.py "YOUTUBE_URL_OR_ID"
```

### Step 2: Read and Clean

The script will output the raw, unformatted transcript block into your context. 

Your job as an AI is to act as an expert editor:
1. Fix any obvious speech-to-text recognition errors.
2. Add proper punctuation (commas, periods, question marks).
3. Break the massive wall of text into logical, readable paragraphs.
4. Add markdown H2 (`##`) headers denoting topic changes.

### Step 3: Present

Output the cleaned, readable markdown document to the user. Do not try to summarize the document unless the user explicitly requested it; your goal is to provide a cleaned, full transcription.
