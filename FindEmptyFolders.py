import os

def find_empty_folders(root_folder):
    """Find and list all empty folders starting from the root folder."""
    empty_folders = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Check if the folder is empty (no files and no subfolders)
        if not dirnames and not filenames:
            empty_folders.append(dirpath)
    return empty_folders

def print_tree_structure(root_folder, prefix=""):
    """Print the folder structure as a tree."""
    if not os.path.exists(root_folder):
        print(f"The folder '{root_folder}' does not exist.")
        return

    # Print the current folder
    print(f"{prefix}{os.path.basename(root_folder)}/")

    # List all subfolders and files
    entries = sorted(os.listdir(root_folder))
    for index, entry in enumerate(entries):
        entry_path = os.path.join(root_folder, entry)
        is_last = index == len(entries) - 1
        new_prefix = f"{prefix}│   " if not is_last else f"{prefix}    "

        if os.path.isdir(entry_path):
            # Print subfolder
            print(f"{prefix}├── {entry}/")
            print_tree_structure(entry_path, new_prefix)
        else:
            # Print file
            print(f"{prefix}├── {entry}")

def main():
    # Get the root folder from the user
    root_folder = input("Enter the root folder to search for empty folders: ").strip()
    
    if not os.path.exists(root_folder):
        print(f"The folder '{root_folder}' does not exist.")
        return

    # Find empty folders
    empty_folders = find_empty_folders(root_folder)

    # Print the results
    if empty_folders:
        print(f"Empty folders found: {len(empty_folders)}")
        for folder in empty_folders:
            print(folder)
    else:
        print("No empty folders found.")

    # Print the tree structure
    print("\nFolder structure:")
    print_tree_structure(root_folder)

if __name__ == "__main__":
    main()