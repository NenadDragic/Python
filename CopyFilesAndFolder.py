import os
import shutil
import hashlib
from tqdm import tqdm

def sanitize_path(path):
    """Sanitize file paths to remove invalid characters."""
    return path.replace(":", "_").replace("\\", "_").replace("/", "_")

def calculate_checksum(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def copy_files_with_extension(source_folder, destination_folder, extension_filter):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    files_to_copy = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith(extension_filter):
                files_to_copy.append((root, file))

    with tqdm(total=len(files_to_copy), desc="Copying files", unit="file") as pbar:
        for root, file in files_to_copy:
            try:
                source_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, source_folder)
                destination_subfolder = os.path.join(destination_folder, relative_path)

                # Sanitize paths
                file = sanitize_path(file)
                destination_subfolder = sanitize_path(destination_subfolder)

                # Debug: Log file paths
                print(f"Processing file: {file}")
                print(f"Source path: {source_file_path}")
                print(f"Destination folder: {destination_subfolder}")

                if not os.path.exists(destination_subfolder):
                    os.makedirs(destination_subfolder)

                destination_file_path = os.path.join(destination_subfolder, file)

                # Debug: Check if source file exists
                if not os.path.exists(source_file_path):
                    print(f"Source file does not exist: {source_file_path}")
                    continue

                # Debug: Check file size
                source_size = os.path.getsize(source_file_path)
                print(f"Source file size: {source_size} bytes")

                shutil.copy2(source_file_path, destination_file_path)

                # Debug: Check if destination file exists
                if not os.path.exists(destination_file_path):
                    print(f"Destination file was not created: {destination_file_path}")
                    continue

                # Validate the copied file
                source_checksum = calculate_checksum(source_file_path)
                destination_checksum = calculate_checksum(destination_file_path)
                if source_checksum == destination_checksum:
                    print(f"Copied and validated: {source_file_path} -> {destination_file_path}")
                else:
                    print(f"Validation failed: {source_file_path} -> {destination_file_path}")

                pbar.update(1)
            except Exception as e:
                print(f"Error copying file: {file}")
                print(f"Source path: {source_file_path}")
                print(f"Destination path: {destination_file_path}")
                print(f"Error: {e}")

# Example usage
source_folder = "/run/user/1000/gvfs/smb-share:server=192.168.1.50,share=dragic/Daily"
destination_folder = "/home/nenad/Downloads/Temp"
extension_filter = ".zipx"

copy_files_with_extension(source_folder, destination_folder, extension_filter)