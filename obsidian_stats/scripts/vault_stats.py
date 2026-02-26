import os
import re
import argparse
from collections import Counter
from typing import Dict, Any, List, Tuple
import time

def get_vault_stats(vault_path: str) -> Dict[str, Any]:
    stats: Dict[str, Any] = {
        "files": 0,
        "words": 0,
        "characters": 0,
        "links": 0,
        "tasks": 0,
        "completed_tasks": 0,
        "tags": Counter(),
        "new_last_7_days": 0,
        "new_last_30_days": 0,
        "modified_last_7_days": 0,
        "modified_last_30_days": 0,
        "recently_modified": []
    }
    
    # Regex patterns
    # Matches [[Link]] or [[Link|Alias]]
    link_pattern = re.compile(r'\[\[(.*?)\]\]')
    # Matches #tag, carefully avoiding markdown headers
    tag_pattern = re.compile(r'(?<!\w)(#[A-Za-z0-9_/-]+)', re.IGNORECASE)
    # Matches - [ ] or - [x]
    task_pattern = re.compile(r'^\s*-\s*\[([ xX])\]', re.MULTILINE)
    
    for root, dirs, files in os.walk(vault_path):
        # Ignore common hidden/system directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith(".md"):
                stats["files"] += 1
                filepath = os.path.join(root, file)
                
                try:
                    file_stat = os.stat(filepath)
                    ctime = file_stat.st_ctime
                    mtime = file_stat.st_mtime
                    
                    now = time.time()
                    days_7 = 7 * 24 * 3600
                    days_30 = 30 * 24 * 3600
                    
                    if now - ctime <= days_7:
                        stats["new_last_7_days"] += 1
                    if now - ctime <= days_30:
                        stats["new_last_30_days"] += 1
                        
                    if now - mtime <= days_7:
                        stats["modified_last_7_days"] += 1
                    if now - mtime <= days_30:
                        stats["modified_last_30_days"] += 1
                        
                    rel_path = os.path.relpath(filepath, vault_path)
                    stats["recently_modified"].append((mtime, rel_path))
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Word and character count
                        stats["characters"] += len(content)
                        # A simple approximation for words in markdown
                        stats["words"] += len(content.split())
                        
                        # Links
                        stats["links"] += len(link_pattern.findall(content))
                        
                        # Tags (excluding standalone `#` used for headers)
                        tags = tag_pattern.findall(content)
                        # Filter out things that are likely headers (e.g. if the regex accidentally caught one, though the regex is safe)
                        valid_tags = [t for t in tags if len(t) > 1 and not t.startswith('# ')]
                        
                        for tag in valid_tags:
                            stats["tags"][tag] += 1
                            
                        # Tasks
                        tasks = task_pattern.findall(content)
                        stats["tasks"] += len(tasks)
                        stats["completed_tasks"] += sum(1 for t in tasks if t in ['x', 'X'])
                        
                except Exception as e:
                    # Skip problematic or unreadable markdown files
                    pass
    stats["recently_modified"].sort(reverse=True, key=lambda x: x[0])
    stats["recently_modified"] = [f for _, f in stats["recently_modified"][:5]]
                    
    return stats

def main():
    parser = argparse.ArgumentParser(description="Calculate Objective Obsidian Vault Statistics")
    parser.add_argument("vault_path", help="Absolute path to the root of the Obsidian vault")
    args = parser.parse_args()
    
    if not os.path.exists(args.vault_path):
        print(f"Error: Directory '{args.vault_path}' does not exist.")
        return
        
    stats = get_vault_stats(args.vault_path)
    
    print("="*45)
    print(" 📊 VAULT STATISTICS")
    print("="*45)
    print(f" Total Notes:       {stats['files']:,}")
    print(f" Total Words:       {stats['words']:,}")
    print(f" Total Characters:  {stats['characters']:,}")
    print("-" * 45)
    print(f" Internal Links:    {stats['links']:,}  ([[]])")
    print(f" Total Tasks:       {stats['tasks']:,}")
    print(f" Completed Tasks:   {stats['completed_tasks']:,}")
    print("-" * 45)
    print(" Activity Metrics:")
    print(f" Created (last 7 days):   {stats['new_last_7_days']:,}")
    print(f" Created (last 30 days):  {stats['new_last_30_days']:,}")
    print(f" Modified (last 7 days):  {stats['modified_last_7_days']:,}")
    print(f" Modified (last 30 days): {stats['modified_last_30_days']:,}")
    print("-" * 45)
    print(" 5 Most Recently Modified:")
    for note in stats["recently_modified"]:
        print(f"   - {note}")
    print("-" * 45)
    
    print(" Top 10 Tags:")
    if not stats["tags"]:
        print("   No tags found.")
    else:
        for tag, count in stats["tags"].most_common(10):
            print(f"   {tag}: {count}")
    print("="*45)

if __name__ == "__main__":
    main()
