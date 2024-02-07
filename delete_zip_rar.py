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

def main():
    root_folder = input("Enter the path to the folder to search for .zip and .rar files: ").strip()

    # Confirm with the user before proceeding with deletion
    confirm_deletion = input(f"WARNING: This action is irreversible and may result in permanent loss of files.\nAre you sure you want to delete .zip and .rar files in {root_folder}? (yes/no): ").strip().lower()
    if confirm_deletion == "yes":
        delete_zip_rar_files(root_folder)
    else:
        print("Deletion aborted.")

if __name__ == "__main__":
    main()
