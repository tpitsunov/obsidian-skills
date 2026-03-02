import os
import sys
import json
import argparse
import datetime

from typing import List

def read_blocks(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Split by double newline to get structural blocks (paragraphs, lists, etc.)
    return content.split('\n\n')

def prepare(file_path: str):
    """
    Reads a markdown file and prints enumerated blocks to stdout.
    This is what the LLM reads to save context and pinpoint extraction targets.
    """
    blocks = read_blocks(file_path)
    print("=" * 60)
    print(f" ⚛️ ZETTEL ATOMIZER (PREPARE): {os.path.basename(file_path)}")
    print("=" * 60)
    
    in_yaml = False
    for i, block in enumerate(blocks):
        stripped = block.strip()
        
        # Determine if we are inside a YAML block (very simplistic check)
        if stripped.startswith('---') and i == 0:
            print(f"[{i}] [YAML FRONTMATTER - SKIPPED FOR EXTRACTION]")
            continue
            
        # Print the block with its index
        # Truncate for display if it's crazy long, but usually we want the LLM to read it
        print(f"[{i}]\n{block}\n")
    print("=" * 60)
    print("Provide a JSON array of extractions, for example:")
    print('[{"title": "My Concept", "tags": ["tag1"], "blocks": [3, 4]}]')

def split_blocks(file_path: str, instruction_file: str, out_dir: str):
    """
    Reads the original file and the JSON instructions.
    Creates Zettels and replaces the original text with wiki-links losslessly.
    """
    blocks = read_blocks(file_path)
    
    with open(instruction_file, 'r', encoding='utf-8') as f:
        instructions = json.load(f)
        
    extracted_counts = 0
    
    for concept in instructions:
        title = concept.get("title", f"Zettel-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
        tags = concept.get("tags", [])
        target_blocks = concept.get("blocks", [])
        
        if not target_blocks:
            continue
            
        # Gather text losslessly
        extracted_text = "\n\n".join([blocks[i] for i in target_blocks if i < len(blocks) and blocks[i] != ""])
        
        # Build new Zettel content
        new_content = ""
        if tags:
            new_content += "---\ntags:\n"
            for t in tags:
                new_content += f"  - {t}\n"
            new_content += "---\n"
            
        new_content += f"# {title}\n\n{extracted_text}\n"
        
        # Save new Zettel
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        new_file_path = os.path.join(out_dir, f"{safe_title}.md")
        
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"✅ Created Zettel: {new_file_path}")
        extracted_counts += 1
        
        # Mutate the blocks array: replace the FIRST block with the link, nullify the rest
        first_idx = target_blocks[0]
        blocks[first_idx] = f"[[{safe_title}]]"
        for idx in target_blocks[1:]:
            if idx < len(blocks):
                blocks[idx] = ""
                
    # Reconstruct the original file
    new_original_content = "\n\n".join([b for b in blocks if b != ""])
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_original_content)
        
    print(f"🔗 Updated original file with {extracted_counts} links.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zettel Atomizer: Extract atomic notes from a long document")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Prepare command
    prep_parser = subparsers.add_parser("prepare", help="Enumerate blocks for LLM reading")
    prep_parser.add_argument("file_path", help="Path to markdown file")
    
    # Split command
    split_parser = subparsers.add_parser("split", help="Apply JSON extraction instructions")
    split_parser.add_argument("file_path", help="Path to original markdown file")
    split_parser.add_argument("json_file", help="Path to JSON instruction file")
    split_parser.add_argument("out_dir", help="Directory to save the new Zettels")
    
    args = parser.parse_args()
    
    if args.command == "prepare":
        prepare(args.file_path)
    elif args.command == "split":
        split_blocks(args.file_path, args.json_file, args.out_dir)
    else:
        parser.print_help()
