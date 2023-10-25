import unittest
import pytsk3
from unittest.mock import patch, Mock
from recoverytool.core import DiskRecoveryTool, scan_disk_for_deleted_files, carve_files_from_disk
from recoverytool import errors
import os

# Sample Image Path
SAMPLE_IMAGE_PATH = "sampleImage\doc.img"


class TestDiskRecoveryTool(unittest.TestCase):

    def setUp(self):
        self.mock_fs_info = Mock()
        self.mock_img_info = Mock()
        self.mock_fs_info.return_value = self.mock_fs_info
        self.mock_img_info.return_value = self.mock_img_info

    def test_initialization_with_default_output_dir(self):
        tool = DiskRecoveryTool(SAMPLE_IMAGE_PATH)
        self.assertEqual(tool.image_path, SAMPLE_IMAGE_PATH)
        self.assertEqual(tool.output_dir, "./recovered")

    def test_initialization_with_custom_output_dir(self):
        custom_output_dir = "./custom_output"
        tool = DiskRecoveryTool(SAMPLE_IMAGE_PATH, custom_output_dir)
        self.assertEqual(tool.image_path, SAMPLE_IMAGE_PATH)
        self.assertEqual(tool.output_dir, custom_output_dir)

    def test_scan_files_with_valid_fs_info(self):
        tool = DiskRecoveryTool(SAMPLE_IMAGE_PATH)
        tool.fs_info = self.mock_fs_info

        directory_entry = Mock()
        directory_entry.info.meta.flags = pytsk3.TSK_FS_META_FLAG_UNALLOC
        directory_entry.info.name = Mock()
        self.mock_fs_info.open_dir.return_value = [directory_entry]

        files = tool.scan_files()
        self.assertIn(directory_entry, files)

    def test_scan_files_with_missing_fs_info(self):
        tool = DiskRecoveryTool(SAMPLE_IMAGE_PATH)
        tool.fs_info = None

        with self.assertRaises(errors.FilesystemNotFoundError):
            tool.scan_files()

    def test_recover_file_with_valid_directory_entry(self):
        tool = DiskRecoveryTool(SAMPLE_IMAGE_PATH)
        directory_entry = Mock()
        directory_entry.info.name.name.decode.return_value = "test_file.txt"
        directory_entry.info.meta.size = 10
        directory_entry.read_random.return_value = b"test_content"

        with patch('builtins.open', new_callable=unittest.mock.mock_open) as mock_open:
            tool.recover_file(directory_entry)

        # Get the actual path used in the open call and normalize it
        actual_path = os.path.normpath(mock_open.call_args[0][0])

        # Get the expected path using os.path and normalize it
        expected_path = os.path.normpath(os.path.join('recovered', 'test_file.txt'))

        # Assert that the actual path matches the expected path
        self.assertEqual(expected_path, actual_path)

    def test_recover_file_with_special_filename(self):
        tool = DiskRecoveryTool(SAMPLE_IMAGE_PATH)
        directory_entry = Mock()
        directory_entry.info.name.name.decode.return_value = "$special_file.txt"

        with patch('builtins.open', new_callable=unittest.mock.mock_open) as mock_open:
            tool.recover_file(directory_entry)

        mock_open.assert_not_called()

    def test_carve_deleted_files_with_valid_fs_info(self):
        tool = DiskRecoveryTool(SAMPLE_IMAGE_PATH)
        tool.fs_info = self.mock_fs_info

        directory_entry = Mock()
        directory_entry.info.meta.flags = pytsk3.TSK_FS_META_FLAG_UNALLOC
        directory_entry.info.name = Mock()
        self.mock_fs_info.open_dir.return_value = [directory_entry]

        result = tool.carve_deleted_files()
        self.assertEqual(result, {})

    def test_carve_deleted_files_with_missing_fs_info(self):
        tool = DiskRecoveryTool(SAMPLE_IMAGE_PATH)
        tool.fs_info = None
        with self.assertRaises(errors.FilesystemNotFoundError):
            result = tool.carve_deleted_files()
            tool.carve_deleted_files()

    def test_scan_disk_for_deleted_files(self):
        with patch.object(DiskRecoveryTool, 'scan_files', return_value=[]):
            result = scan_disk_for_deleted_files(SAMPLE_IMAGE_PATH)
            self.assertEqual(result, [])

    def test_carve_files_from_disk(self):
        with patch.object(DiskRecoveryTool, 'carve_deleted_files', return_value={}):
            result = carve_files_from_disk(SAMPLE_IMAGE_PATH)
            self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
