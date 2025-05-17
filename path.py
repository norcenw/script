import os

def generate_tree(directory, prefix=""):
    tree_structure = ""
    entries = sorted(os.listdir(directory))
    for i, entry in enumerate(entries):
        entry_path = os.path.join(directory, entry)
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "│── "
        tree_structure += prefix + connector + entry + "\n"
        
        if os.path.isdir(entry_path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree_structure += generate_tree(entry_path, new_prefix)
    
    return tree_structure

def save_tree_to_file(src_folder, output_file):
    if not os.path.exists(src_folder):
        print(f"Errore: La cartella '{src_folder}' non esiste.")
        return
    
    tree_structure = "/mio-progetto-electron\n" + generate_tree(src_folder)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(tree_structure)
    
    print(f"Struttura salvata in '{output_file}'")

if __name__ == "__main__":
    src_folder = "src"  # Cartella di partenza
    output_file = "dist/project_structure.txt"  # File di output
    save_tree_to_file(src_folder, output_file)
