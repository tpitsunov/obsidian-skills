import os
import argparse
import re

def parse_yaml_frontmatter(content: str):
    tags = []
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            for line in frontmatter.split('\n'):
                line = line.strip()
                if line.startswith('- ') and not ':' in line:  # Basic array item
                    tags.append(line[2:].strip())
                elif line.startswith('tags:'): 
                    # inline tags: [a, b] handling could go here, keeping simple for now
                    pass
    return tags

def extract_meaningful_content(content: str) -> str:
    """
    Extracts the first H1 header OR the first meaningful paragraph text
    if no headers exist in the file.
    """
    lines = content.split('\n')
    
    # 1. Look for the first H1
    for line in lines:
        if line.startswith('# '):
            return f"Header: {line.strip()}"
            
    # 2. If no headers, skip frontmatter and grab the first non-empty paragraph
    in_frontmatter = False
    for line in lines:
        stripped = line.strip()
        if stripped == '---':
            in_frontmatter = not in_frontmatter
            continue
        
        if not in_frontmatter and stripped and not stripped.startswith('#'):
            # Return first ~100 characters of the first paragraph
            return f"Excerpt: {stripped[:100]}..."
            
    return "No meaningful content found."

def gather_moc_data(vault_path: str, target_folder: str = "") -> None:
    search_path = os.path.join(vault_path, target_folder) if target_folder else vault_path
    
    print("=" * 60)
    print(f" 🗺️ MOC METADATA GATHERING: {target_folder or 'Full Vault'}")
    print("=" * 60)
    
    count = 0
    for root, dirs, files in os.walk(search_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file_name in files:
            if file_name.endswith(".md"):
                filepath = os.path.join(root, file_name)
                rel_base = file_name[:-3]  # Strip .md
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        tags = parse_yaml_frontmatter(content)
                        # Quick regex grab for inline #tags
                        inline_tags = re.findall(r'(?<!\w)(#[A-Za-z0-9_/-]+)', content)
                        all_tags = set(tags + [t.replace('#', '') for t in inline_tags])
                        
                        summary = extract_meaningful_content(content)
                        
                        print(f"📄 [[{rel_base}]]")
                        print(f"   Tags: {', '.join(all_tags) if all_tags else 'None'}")
                        print(f"   {summary}")
                        print("-" * 60)
                        count += 1
                except Exception:
                    pass
    print(f"Total files condensed: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vault_path", help="Absolute root path of the vault")
    parser.add_argument("--folder", help="Specific folder to scan (relative to vault root)", default="")
    args = parser.parse_args()
    
    gather_moc_data(args.vault_path, args.folder)
