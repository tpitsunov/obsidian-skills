import os
import re
import argparse
from typing import Set, Dict, List

def find_orphans(vault_path: str) -> List[str]:
    """
    Scans an Obsidian vault to find true orphan notes:
    Notes that have NO outgoing links AND NO incoming links from anywhere else.
    """
    all_files: Set[str] = set()
    all_links: Set[str] = set()
    outgoing_links_count: Dict[str, int] = {}
    
    # Regex to match [[WikiLinks]] or [[WikiLink|Alias]]
    link_pattern = re.compile(r'\[\[(.*?)(?:\|.*?)?\]\]')
    
    # First pass: collect all files and all outgoing links
    for root, dirs, files in os.walk(vault_path):
        # Ignore common hidden/system directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith(".md"):
                # Store the base filename without extension to match Obsidian links
                base_name = file[:-3]
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, vault_path)
                
                all_files.add(base_name)
                outgoing_links_count[base_name] = 0
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        links_in_file = link_pattern.findall(content)
                        
                        for link in links_in_file:
                            # Obsidian links often refer to the base filename
                            # We normalize it by removing any #headers
                            clean_link = link.split('#')[0].strip()
                            if clean_link:
                                all_links.add(clean_link)
                                outgoing_links_count[base_name] += 1
                except Exception:
                    # Skip unreadable files
                    pass

    orphans = []
    for file_base in all_files:
        # A file is an orphan if:
        # 1. Nobody links to it (not in all_links)
        # 2. It doesn't link to anything else (outgoing = 0)
        # Note: If you want to find files that *only* have NO incoming links, 
        # remove the `outgoing == 0` check. For strict orphans, keep it.
        if file_base not in all_links and outgoing_links_count[file_base] == 0:
            # Reconstruct the likely relative path or just return the name
            orphans.append(file_base)
            
    return sorted(orphans)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find Orphan Notes in Obsidian Vault")
    parser.add_argument("vault_path", help="Absolute path to the root of the Obsidian vault")
    args = parser.parse_args()
    
    if not os.path.exists(args.vault_path):
        print(f"Error: Directory '{args.vault_path}' does not exist.")
        exit(1)
        
    orphans = find_orphans(args.vault_path)
    
    print("=" * 45)
    print(" 🪁 ORPHAN NOTES DETECTED")
    print("=" * 45)
    if not orphans:
        print("  Good job! No strict orphans found.")
    else:
        print(f"  Found {len(orphans)} completely isolated notes:")
        for orphan in orphans:
            print(f"  - [[{orphan}]]")
    print("=" * 45)
