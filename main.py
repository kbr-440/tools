import pytsk3

img_info = pytsk3.Img_Info("/path/to/disk_or_image")


fs_info = None

if img_info.info.ftype in (pytsk3.TSK_FS_TYPE_NTFS, pytsk3.TSK_FS_TYPE_NTFS_DETECT):
    fs_info = pytsk3.FS_Info(img_info)
elif img_info.info.ftype in (pytsk3.TSK_FS_TYPE_FAT32, pytsk3.TSK_FS_TYPE_FAT32_DETECT):
    # Handle FAT32
    pass
elif img_info.info.ftype in (pytsk3.TSK_FS_TYPE_EXT4, pytsk3.TSK_FS_TYPE_EXT4_DETECT):
    # Handle EXT4
    pass
else:
    raise ValueError("Unsupported file system")


root_directory = fs_info.open_dir(path="/")

for entry in root_directory:
    if entry.info.meta and entry.info.name:
        name = entry.info.name.name
        if entry.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
            print(f"Deleted file: {name}")


def carve(file_entry, output_path):
    buffer_size = 1024 * 1024  # 1MB
    offset = 0
    
    with open(output_path, 'wb') as out_file:
        while offset < file_entry.info.meta.size:
            available_to_read = min(buffer_size, file_entry.info.meta.size - offset)
            data = file_entry.read_random(offset, available_to_read)
            out_file.write(data)
            offset += len(data)

for entry in root_directory:
    if entry.info.meta and entry.info.name:
        name = entry.info.name.name
        if entry.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
            output_path = f"./recovered/{name}"
            carve(entry, output_path)
