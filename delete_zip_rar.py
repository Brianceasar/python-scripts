import os

def delete_zip_rar_files(root_folder):
    """Delete .zip and .rar files in a directory and its subdirectories."""
    try:
        for dirpath, _, filenames in os.walk(root_folder):
            for filename in filenames:
                if filename.endswith('.zip') or filename.endswith('.rar'):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        os.remove(file_path)
                        print(f"Deleted {file_path}")
                    except OSError as e:
                        print(f"Error deleting {file_path}: {e}")
        print("Deletion completed.")
    except Exception as e:
        print(f"An error occurred during deletion: {e}")

