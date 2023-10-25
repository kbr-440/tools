import os
import pytsk3
from recoverytool import errors


class DiskRecoveryTool:

    def __init__(self, image_path, output_dir="./recovered"):
        self.image_path = image_path
        self.output_dir = output_dir
        self.img_info = pytsk3.Img_Info(self.image_path)
        self.fs_info = None  # Initialize fs_info to None

        try:
            self.fs_info = pytsk3.FS_Info(self.img_info)
        except Exception as e:
            print(f"Warning: Failed to detect filesystem: {str(e)}")

    def scan_files(self, recover_all=False):
        """Return a list of file entries using pytsk3, filtered based on user's choice."""
        if not self.fs_info:
            raise errors.FilesystemNotFoundError("Filesystem information is not available.")
        files = []
        try:
            root_directory = self.fs_info.open_dir(path="/")
            for directory_entry in root_directory:
                if directory_entry.info.meta and directory_entry.info.name:
                    if recover_all or (directory_entry.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC):
                        files.append(directory_entry)
        except Exception as e:
            raise errors.FileRecoveryError(f"Error scanning for files: {str(e)}") from e
        return files

    def recover_file(self, directory_entry):
        try:
            file_name = directory_entry.info.name.name.decode('utf-8')

            # Skip special files
            if file_name.startswith("$"):
                print(f"Skipping special file: {file_name}")
                return

            file_content = directory_entry.read_random(0, directory_entry.info.meta.size)
            output_path = os.path.join(self.output_dir, file_name)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as out_file:
                out_file.write(file_content)
        except Exception as e:
            print(f"Warning: Error recovering file {file_name}: {str(e)}")

    def carve_deleted_files(self):
        deleted_entries = self.scan_files()
        for entry in deleted_entries:
            self.recover_file(entry)
        return {}


def scan_disk_for_deleted_files(image_path):
    print("Scanning disk...")
    tool = DiskRecoveryTool(image_path)
    deleted_entries = tool.scan_files()
    if "error" in deleted_entries:
        print("Error in scanning:", deleted_entries["error"])
        return deleted_entries
    return [entry.info.name.name.decode('utf-8') for entry in deleted_entries]

def carve_files_from_disk(image_path, output_dir="./recovered"):
    print("Carving files...")
    tool = DiskRecoveryTool(image_path, output_dir)
    result = tool.carve_deleted_files()
    if result and "error" in result:
        print("Error in carving:", result["error"])
        return result
    print("Carving completed!")
    return {}

