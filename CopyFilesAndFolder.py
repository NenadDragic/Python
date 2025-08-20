import os
import shutil
import hashlib
from tqdm import tqdm  # Import tqdm for the progress bar

def calculate_checksum(file_path):
    """
    Calculates the checksum of a file using SHA256.
    
    :param file_path: Path to the file
    :return: Hexadecimal checksum string
    """
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def copy_files_with_extension(source_folder, destination_folder, extension_filter):
    """
    Copies files with a specific extension from source_folder (including subfolders)
    to destination_folder. Creates destination folders if they don't exist.
    Validates that the copied files are identical.
    Displays a progress bar for the copying process.
    
    :param source_folder: Path to the source folder
    :param destination_folder: Path to the destination folder
    :param extension_filter: File extension to filter (e.g., '.txt')
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Collect all files to copy
    files_to_copy = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith(extension_filter):
                files_to_copy.append((root, file))

    # Initialize the progress bar
    with tqdm(total=len(files_to_copy), desc="Copying files", unit="file") as pbar:
        for root, file in files_to_copy:
            source_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, source_folder)
            destination_subfolder = os.path.join(destination_folder, relative_path)

            if not os.path.exists(destination_subfolder):
                os.makedirs(destination_subfolder)

            destination_file_path = os.path.join(destination_subfolder, file)
            shutil.copy2(source_file_path, destination_file_path)

            # Validate the copied file
            source_checksum = calculate_checksum(source_file_path)
            destination_checksum = calculate_checksum(destination_file_path)
            if source_checksum == destination_checksum:
                print(f"Copied and validated: {source_file_path} -> {destination_file_path}")
            else:
                print(f"Validation failed: {source_file_path} -> {destination_file_path}")

            # Update the progress bar
            pbar.update(1)

# Example usage
source_folder = "/run/user/1000/gvfs/smb-share:server=192.168.1.50,share=dragic/Daily"
destination_folder = "/media/nenad/7283-2089"
extension_filter = ".zipx"  # Change this to the desired file extension

copy_files_with_extension(source_folder, destination_folder, extension_filter)