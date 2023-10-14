import os


class FolderRecoveryTool:
    def __init__(self, folder_path, output_dir="./recovered"):
        self.folder_path = folder_path
        self.output_dir = output_dir

    def list_deleted_files(self):
        deleted_files = []
        for root, dirs, files in os.walk(self.folder_path):
            for file_name in files:
                full_path = os.path.join(root, file_name)
                if not os.path.exists(full_path):
                    deleted_files.append(full_path)
        return deleted_files

    def recover_file(self, file_path):
        output_path = os.path.join(self.output_dir, os.path.basename(file_path))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as out_file, open(file_path, "rb") as in_file:
            out_file.write(in_file.read())


def carve(folder_path, output_dir="./recovered"):
    recovery_tool = FolderRecoveryTool(folder_path, output_dir)
    deleted_files = recovery_tool.list_deleted_files()
    for file_path in deleted_files:
        recovery_tool.recover_file(file_path)


import os
import pytsk3


# ... [Your existing FolderRecoveryTool class and carve function] ...

def scan_disk_for_deleted_files(image_path):
    # This function should return a list of deleted files using pytsk3

    # Open the disk image
    img_info = pytsk3.Img_Info(image_path)

    # Try auto-detection for the filesystem
    try:
        fs_info = pytsk3.FS_Info(img_info)
    except Exception as e:
        raise ValueError(f"Failed to detect filesystem: {str(e)}")

    # Logic to scan and get the list of deleted files
    deleted_files = []
    root_directory = fs_info.open_dir(path="/")
    for directory_entry in root_directory:
        if directory_entry.info.meta and directory_entry.info.name:
            # Check if the file is deleted
            if directory_entry.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
                deleted_files.append(directory_entry.info.name.name.decode('utf-8'))

    return deleted_files
