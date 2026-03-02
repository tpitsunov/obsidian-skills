import os
import random
import argparse
from typing import List

def get_random_notes(vault_path: str, target_folder: str, num_notes: int = 3) -> List[str]:
    search_path = os.path.join(vault_path, target_folder) if target_folder else vault_path
    
    all_md_files = []
    for root, dirs, files in os.walk(search_path):
        # Ignore hidden folders
        for d in list(dirs):
            if d.startswith('.'):
                dirs.remove(d)
        for file in files:
            if file.endswith(".md"):
                all_md_files.append(os.path.join(root, file))
                
    if not all_md_files:
        return []
        
    num_to_pick = min(num_notes, len(all_md_files))
    return random.sample(all_md_files, num_to_pick)

def output_notes(file_paths: List[str]):
    print("=" * 60)
    print(f" 🔮 SERENDIPITY ENGINE: Igniting {len(file_paths)} random ideas")
    print("=" * 60)
    
    for path in file_paths:
        base_name = os.path.basename(path)
        if base_name.endswith(".md"):
            base_name = base_name[:-3]
            
        print(f"\n📄 [[{base_name}]]")
        print("-" * 40)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # If the note is massive, truncate to first 1000 chars to save tokens
                if len(content) > 1000:
                    print(content[0:1000] + "\n...[TRUNCATED]")
                else:
                    print(content)
        except Exception as e:
            print(f"Error reading file: {e}")
            
    print("\n" + "=" * 60)
    print("AI INSTRUCTION:")
    print("Read the above notes. They were selected purely at random.")
    print("Your task is to find a hidden philosophical, logical, or thematic connection between them.")
    print("Synthesize them into a single, novel insight.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serendipity Engine: Pick random notes for synthesis")
    parser.add_argument("vault_path", help="Absolute root path of the vault")
    parser.add_argument("--folder", help="Specific folder to draw from (relative to vault root)", default="")
    parser.add_argument("--count", help="Number of random notes to pick", type=int, default=3)
    args = parser.parse_args()
    
    picked_files = get_random_notes(args.vault_path, args.folder, args.count)
    if not picked_files:
        print(f"No markdown files found in {os.path.join(args.vault_path, args.folder)}")
    else:
        output_notes(picked_files)
