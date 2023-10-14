import argparse
from recoverytool.core import FolderRecoveryTool


def parse_arguments():
    parser = argparse.ArgumentParser(description="File recovery tool")
    parser.add_argument("folder_path", type=str, help="Path to the folder with deleted files")
    return parser.parse_args()


def main():
    args = parse_arguments()
    folder_path = args.folder_path
    recovery_tool = FolderRecoveryTool(folder_path)
    deleted_files = recovery_tool.list_deleted_files()
    for file_path in deleted_files:
        recovery_tool.recover_file(file_path)


if __name__ == "__main__":
    main()
