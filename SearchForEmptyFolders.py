import os
import sys

def find_empty_folders(root_folder):
    """
    Finds and prints the paths of all empty folders and subfolders
    within a specified root directory.

    Args:
        root_folder (str): The path to the root directory to search.
    """
    if not os.path.isdir(root_folder):
        print(f"Error: The provided path '{root_folder}' is not a valid directory.")
        return

    empty_folders = []
    
    # os.walk traverses the directory tree
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # A directory is considered empty if it contains no files and no subdirectories
        if not dirnames and not filenames:
            empty_folders.append(dirpath)
    
    if empty_folders:
        print("Found empty folders:")
        for folder in empty_folders:
            print(folder)
    else:
        print("No empty folders found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python SearchForEmptyFolders.py <path_to_directory>")
        sys.exit(1)
    
    search_path = sys.argv[1]
    find_empty_folders(search_path)