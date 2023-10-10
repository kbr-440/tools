# recoverytool.py
import argparse
from recoverytool import core

def parse_arguments():
    parser = argparse.ArgumentParser(description="File recovery tool")
    parser.add_argument("folder_path", type=str, help="Path to the folder with deleted files")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    folder_path = args.folder_path
    core.recover_deleted_files(folder_path)  # Call your recovery function from core.py
