import sys
import argparse
import re

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("❌ Error: youtube-transcript-api is not installed.")
    print("Please run: pip install youtube-transcript-api")
    sys.exit(1)

def extract_video_id(url_or_id: str) -> str:
    # Handle pure IDs, long URLs, and short youtu.be URLs
    if len(url_or_id) == 11 and not "http" in url_or_id:
        return url_or_id
        
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', 
        r'youtu\.be\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
            
    print(f"❌ Error: Could not extract an 11-character YouTube ID from '{url_or_id}'")
    sys.exit(1)

def fetch_transcript(video_url: str):
    video_id = extract_video_id(video_url)
    
    try:
        # Instantiate the API client and list transcripts
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        try:
            transcript = transcript_list.find_transcript(['ru', 'en'])
        except Exception:
            transcript = transcript_list.find_generated_transcript(['ru', 'en'])
            
        transcript_data = transcript.fetch()
        
        # Drop timestamps to save LLM context tokens.
        # Join into a pure text block.
        full_text = " ".join([segment.text for segment in transcript_data])
        
        # Clean up common garbled artifacts like newlines
        full_text = full_text.replace("\n", " ").replace("  ", " ")
        
        print("=" * 60)
        print(f" 🎬 YOUTUBE RAW TRANSCRIPT (ID: {video_id})")
        print("=" * 60)
        print(full_text)
        print("\n" + "=" * 60)
        print("AI INSTRUCTION:")
        print("The above text is a raw, unformatted transcript without punctuation.")
        print("Act as an expert editor. Clean up the text, add proper punctuation,")
        print("fix any obvious speech-to-text recognition errors, and format it")
        print("into a readable markdown note with logical paragraphs and H2 headers.")
        
    except Exception as e:
        print(f"❌ Error fetching transcript: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch YouTube Transcript as plain text")
    parser.add_argument("url", help="YouTube video URL or Video ID")
    
    args = parser.parse_args()
    fetch_transcript(args.url)
