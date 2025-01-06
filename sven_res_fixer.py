import os
import glob
from pathlib import Path

def find_true_case(base_dir, relative_path):
    relative_path_lower = relative_path.lower()
    path_parts = relative_path_lower.split('/')
    
    current_dir = base_dir
    true_path_parts = []
    
    for part in path_parts:
        found = False
        try:
            for entry in os.listdir(current_dir):
                if entry.lower() == part:
                    true_path_parts.append(entry)
                    current_dir = os.path.join(current_dir, entry)
                    found = True
                    break
            
            if not found:
                return None 
                
        except OSError:
            return None  
    
    final_path = '/'.join(true_path_parts)
    if os.path.exists(os.path.join(base_dir, final_path)):
        return final_path
    return None

def process_res_files(base_path):
    if not os.path.exists(base_path):
        print(f"Error: Path {base_path} does not exist!")
        return

    addon_path = str(Path(base_path).parent)
    
    res_files = glob.glob(os.path.join(base_path, "*.res"))
    
    if not res_files:
        print("No .res files found in the specified directory!")
        return
    
    print(f"Found {len(res_files)} .res files")
    
    for res_file in res_files:
        print(f"\nProcessing {res_file}...")
        
        with open(res_file, 'r') as f:
            lines = f.readlines()
        
        modified = False
        new_lines = []
        for line in lines:
            original_line = line.strip()
            
            if not original_line or original_line.startswith('//'):
                new_lines.append(line)
                continue
            
            true_case = find_true_case(addon_path, original_line)
            
            if true_case is not None and true_case != original_line:
                print(f"Correcting case:\nFrom: {original_line}\nTo:   {true_case}")
                new_lines.append(true_case + '\n')
                modified = True
            else:
                new_lines.append(line)
        
        if modified:
            print(f"Saving changes to {res_file}")
            with open(res_file, 'w') as f:
                f.writelines(new_lines)
        else:
            print(f"No changes needed in {res_file}")

def main():
    print("This script will find the true case of file paths in .res files")
    print("It expects to run in the 'maps' directory and will look for resources")
    print("in the parent directory (svencoop_addon)")
    print("By: TreeOfSelf (Sebastian)")
    
    base_path = input("Enter the path to your .res files (e.g., ~/SvenCoop/svencoop_addon/maps): ").strip()
    
    if base_path.startswith('~'):
        base_path = os.path.expanduser(base_path)
    
    process_res_files(base_path)

if __name__ == "__main__":
    main()
