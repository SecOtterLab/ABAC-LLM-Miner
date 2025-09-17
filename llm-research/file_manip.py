import os
import shutil
from helper_functions import write_text_to_file

def move_and_rename_all(src_dir, dest_dir, name_prefix, timestamp):
 
    # one consistent timestamp for everything

    # Rename the parent folder itself
    folder_name = os.path.basename(src_dir.rstrip(os.sep))
    new_folder_name = f"{name_prefix}_{timestamp}_{folder_name}"
    new_folder_path = os.path.join(dest_dir, new_folder_name)

    # Copy the whole directory first
    shutil.copytree(src_dir, new_folder_path)

    # Walk through everything we just copied and rename items
    for root, dirs, files in os.walk(new_folder_path, topdown=False):
        # Rename files
        for fname in files:
            old_path = os.path.join(root, fname)
            new_name = f"{name_prefix}_{timestamp}_{fname}"
            new_path = os.path.join(root, new_name)
            os.rename(old_path, new_path)

        # Rename directories
        for dname in dirs:
            old_path = os.path.join(root, dname)
            new_name = f"{name_prefix}_{timestamp}_{dname}"
            new_path = os.path.join(root, new_name)
            os.rename(old_path, new_path)

    return new_folder_path



def main():

 
    return

if __name__ == "__main__":
    main()