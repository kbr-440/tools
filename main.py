import os
import argparse
import pytsk3


# import magic  # For file type detection

class RecoveryTool:
    def __init__(self, folder_path, output_dir="./recovered"):
        self.folder_path = folder_path
        self.output_dir = output_dir
        self.img_info = pytsk3.Img_Info(folder_path)
        self.fs_info = None

    def detect_file_system(self):
        if self.img_info.info.ftype in (pytsk3.TSK_FS_TYPE_NTFS, pytsk3.TSK_FS_TYPE_NTFS_DETECT):
            self.fs_info = pytsk3.FS_Info(self.img_info)
        elif self.img_info.info.ftype in (pytsk3.TSK_FS_TYPE_FAT32, pytsk3.TSK_FS_TYPE_FAT32_DETECT):
            # Handle FAT32
            pass
        elif self.img_info.info.ftype in (pytsk3.TSK_FS_TYPE_EXT4, pytsk3.TSK_FS_TYPE_EXT4_DETECT):
            # Handle EXT4
            pass
        else:
            raise ValueError("Unsupported file system")

    def list_deleted_files(self):
        if self.fs_info is None:
            raise ValueError("File system not detected. Call detect_file_system() first.")

        root_directory = self.fs_info.open_dir(path="/")

        deleted_files = []
        for entry in root_directory:
            if entry.info.meta and entry.info.name:
                name = entry.info.name.name
                if entry.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
                    deleted_files.append(name)

        return deleted_files

    def recover_file(self, file_name):
        if self.fs_info is None:
            raise ValueError("File system not detected. Call detect_file_system() first.")

        file_entry = self.fs_info.open_meta(path=f"/{file_name}")
        output_path = os.path.join(self.output_dir, file_name)
        self.carve(file_entry, output_path)

    @staticmethod
    def carve(file_entry, output_path):
        buffer_size = 1024 * 1024  # 1MB
        offset = 0

        with open(output_path, 'wb') as out_file:
            while offset < file_entry.info.meta.size:
                available_to_read = min(buffer_size, file_entry.info.meta.size - offset)
                data = file_entry.read_random(offset, available_to_read)
                out_file.write(data)
                offset += len(data)


def parse_arguments():
    parser = argparse.ArgumentParser(description="File recovery tool")
    parser.add_argument("folder_path", type=str, help="Path to the folder with deleted files")
    return parser.parse_args()


def main():
    args = parse_arguments()
    folder_path = args.folder_path
    recovery_tool = RecoveryTool(folder_path)
    recovery_tool.detect_file_system()
    deleted_files = recovery_tool.list_deleted_files()
    for file_name in deleted_files:
        print(f"Deleted file: {file_name}")
        recovery_tool.recover_file(file_name)


if __name__ == "__main__":
    main()
