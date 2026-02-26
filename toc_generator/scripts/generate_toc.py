import argparse
import re
import sys

def generate_toc(file_path: str) -> None:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
        
    lines = content.split('\n')
    toc_lines = []
    
    in_code_block = False
    in_frontmatter = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip frontmatter
        if i == 0 and stripped == '---':
            in_frontmatter = True
            continue
        if in_frontmatter and stripped == '---':
            in_frontmatter = False
            continue
        if in_frontmatter:
            continue
            
        # Skip code blocks where # might be comments
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
            
        # Match headers H1 to H6
        header_match = re.match(r'^(#{1,6})\s+(.+)', stripped)
        if header_match:
            level = len(header_match.group(1))
            title = header_match.group(2).strip()
            
            # Obsidian internal link format for headers: [[#Header Title]]
            # Indentation: 2 spaces per level, starting at H2 (level 2) = 0 spaces
            # H1 usually isn't in ToC or is the root, but we'll include it at 0 spaces if present
            indent_spaces = max(0, (level - 2) * 2) if level >= 2 else 0
            
            # Obsidian link formatting
            link = f"[[#{title}]]"
            toc_lines.append(f"{' ' * indent_spaces}- {link}")
            
    print("=" * 45)
    print(f" 📑 TABLE OF CONTENTS FOR: {file_path}")
    print("=" * 45)
    if not toc_lines:
        print("  No headers found in this document.")
    else:
        print("## Table of Contents")
        for line in toc_lines:
            print(line)
        print("\n(Copy and paste the above snippet into your document)")
    print("=" * 45)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Obsidian ToC from headers")
    parser.add_argument("file_path", help="Absolute path to the markdown file")
    args = parser.parse_args()
    
    generate_toc(args.file_path)
