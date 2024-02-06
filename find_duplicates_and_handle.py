import os
import hashlib
import shutil

def file_hash(filepath, block_size=65536):
    """Generate a hash for a given file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hasher.update(block)
    return hasher.hexdigest()

def find_duplicates(root_folder):
    """Find duplicate files in a directory and its subdirectories."""
    duplicates = {}
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_size = os.path.getsize(file_path)
            if file_size > 0:
                file_signature = (filename, file_size, file_hash(file_path))
                if file_signature in duplicates:
                    duplicates[file_signature].append(file_path)
                else:
                    duplicates[file_signature] = [file_path]
    return duplicates

def main():
    root_folder = input("Enter the path to the folder to search for duplicates: ").strip()
    duplicates_folder = os.path.join(root_folder, "duplicates")

    # Create 'duplicates' folder if it doesn't exist
    if not os.path.exists(duplicates_folder):
        os.makedirs(duplicates_folder)

    # Find duplicates
    duplicates = find_duplicates(root_folder)

    # Move all duplicate files to 'duplicates' folder
    for files in duplicates.values():
        if len(files) > 1:
            for file_path in files[1:]:
                shutil.move(file_path, duplicates_folder)
                print(f"Moved {file_path} to duplicates folder")

    # Prompt for deletion confirmation
    confirm_deletion = input("Do you want to permanently delete the duplicate files? (yes/no): ").strip().lower()
    if confirm_deletion == "yes":
        for files in duplicates.values():
            if len(files) > 1:
                for file_path in files[1:]:
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
   
