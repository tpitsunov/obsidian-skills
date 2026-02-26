import urllib.request
import urllib.parse
import re
import argparse
import sys

def fetch_and_clean(url):
    """
    Fetches raw HTML from a URL and removes heavy/useless tags (scripts, styles, navs, footers)
    to output a minimized HTML structure. This prevents LLM token limits from being exceeded
    while retaining semantic HTML tags (h1, p, a, b) for the LLM to convert into Markdown.
    """
    if not url.startswith('http'):
        url = 'https://' + url

    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )

    try:
        response = urllib.request.urlopen(req, timeout=10)
        html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)

    # 1. Strip out bulky non-content tags entirely
    tags_to_remove = ['script', 'style', 'noscript', 'svg', 'iframe', 'canvas']
    for tag in tags_to_remove:
        html = re.sub(f'<{tag}.*?>.*?</{tag}>', '', html, flags=re.IGNORECASE | re.DOTALL)
    
    # 2. Strip out common layout/semantic tags that rarely contain the main article
    layout_tags = ['nav', 'footer', 'aside', 'header']
    for tag in layout_tags:
        html = re.sub(f'<{tag}.*?>.*?</{tag}>', '', html, flags=re.IGNORECASE | re.DOTALL)

    # 3. Strip out common ad or menu classes/ids (rudimentary heuristic)
    html = re.sub(r'<[^>]+(?:id|class)=["\'][^"\']*(?:ad-|banner|menu|sidebar|popup|cookie|social)[^"\']*["\'][^>]*>.*?</[^>]+>', '', html, flags=re.IGNORECASE | re.DOTALL)

    # 4. Collapse massive whitespace blocks into a single space/newline to reduce tokens
    html = re.sub(r'[ \t]+', ' ', html)
    html = re.sub(r'\n\s*\n', '\n', html)

    # Print a summary indicating it's the raw minimized HTML
    print(f"--- MINIMIZED HTML DUMP FROM {url} ---")
    
    # Restrict output to ~40,000 characters to ensure it fits well within most LLM context windows
    MAX_CHARS = 40000 
    if len(html) > MAX_CHARS:
        print(html[:MAX_CHARS] + "\n...[CONTENT TRUNCATED]...")
    else:
        print(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and minimize webpage HTML for AI LLM parsing.")
    parser.add_argument("url", help="The URL of the webpage to fetch.")
    args = parser.parse_args()
    
    fetch_and_clean(args.url)
