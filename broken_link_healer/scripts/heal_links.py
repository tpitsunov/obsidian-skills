import os
import re
import difflib
import argparse
from typing import Dict, List, Set, Tuple

def get_all_vault_files(vault_path: str) -> Dict[str, str]:
    """
    Returns a dictionary mapping 'BaseName' -> 'Relative/Full/Path/BaseName.md'
    Obsidian links usually use just the BaseName, regardless of the folder it is in.
    """
    files_map = {}
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith(".md"):
                base_name = file[:-3]
                # Store the relative path just in case we need it, but the key is the BaseName
                rel_path = os.path.relpath(os.path.join(root, file), vault_path)
                # If there are duplicate filenames in different folders, we store a list or just the first one.
                # Standard Obsidian warns about duplicate base names, but we'll just keep the first encountered for simplicity.
                if base_name not in files_map:
                    files_map[base_name] = rel_path
    return files_map

def find_broken_links_and_suggestions(file_path: str, vault_path: str) -> List[Tuple[str, List[str]]]:
    """
    Finds broken links in a file and uses difflib to suggest the 3 closest matches
    from the actual files existing anywhere in the vault.
    """
    vault_files = get_all_vault_files(vault_path)
    available_bases = list(vault_files.keys())
    
    link_pattern = re.compile(r'\[\[(.*?)(?:\|.*?)?\]\]')
    broken_links = set()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        links = link_pattern.findall(content)
        for link in links:
            # Clean header links like [[Note Name#Header]]
            clean_link = link.split('#')[0].strip()
            if clean_link and clean_link not in vault_files:
                broken_links.add(clean_link)
                
    results = []
    for broken in broken_links:
        # get_close_matches uses Gestalt pattern matching (SequenceMatcher)
        suggestions = difflib.get_close_matches(broken, available_bases, n=3, cutoff=0.4)
        results.append((broken, suggestions))
        
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find broken links and suggest fixes")
    parser.add_argument("vault_path", help="Absolute root path of the vault")
    parser.add_argument("file_path", help="Absolute path to the specific file to heal")
    args = parser.parse_args()
    
    results = find_broken_links_and_suggestions(args.file_path, args.vault_path)
    
    print("=" * 45)
    print(f" 💔 BROKEN LINKS IN: {os.path.basename(args.file_path)}")
    print("=" * 45)
    if not results:
        print("  No broken links found!")
    else:
        for broken, suggestions in results:
            print(f"  ❌ Broken Link: [[{broken}]]")
            if suggestions:
                print("  💡 Did you mean one of these existing files?")
                for sug in suggestions:
                    print(f"      - [[{sug}]]")
            else:
                print("  ⚠️ No similar files found across the entire vault.")
            print("-" * 45)
