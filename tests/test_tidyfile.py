import unittest
import tempfile
import os
from datetime import datetime, timedelta
from unittest.mock import patch
import argparse
from pathlib import Path

# Import the functions you want to test from tidyfile.py
from tidyfile import parse_arguments, setup_archive_folder, should_move, main

class TestTidyFile(unittest.TestCase):

    # Test parse_arguments function
    def test_parse_arguments(self):
        args = parse_arguments(["--days", "2", "--desktop", "/path/to/desktop", "--verbose"])
        self.assertEqual(args.days, 2)
        self.assertEqual(args.desktop, "/path/to/desktop")
        self.assertTrue(args.verbose)
        self.assertEqual(args.archive_folder, Path("~/Desktop Archive"))

    # Test setup_archive_folder function
    def test_setup_archive_folder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_folder = setup_archive_folder(temp_dir)
            self.assertTrue(archive_folder.is_dir())

    # Test should_move function
    def test_should_move(self):
        now = datetime.now()
        two_days_ago = now - timedelta(days=2)
        three_days_ago = now - timedelta(days=3)

        # Create a temporary file with a mtime of two days ago
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = Path(temp_file.name)
            os.utime(temp_file_path, (two_days_ago.timestamp(), two_days_ago.timestamp()))

            config = {"days_threshold": 1}
            self.assertFalse(should_move(temp_file_path, config))

            config = {"days_threshold": 3}
            self.assertTrue(should_move(temp_file_path, config))

        os.remove(temp_file_path)

    # Test main function (requires more extensive mocking)
    @patch("tidyfile.setup_logging")
    @patch("tidyfile.setup_archive_folder")
    @patch("tidyfile.move_files")
    @patch("tidyfile.print")
    def test_main(self, mock_print, mock_move_files, mock_setup_archive_folder, mock_setup_logging):
        mock_setup_archive_folder.return_value = Path("/tmp/archive")
        mock_args = mock_setup_logging.return_value = argparse.Namespace(days=1, desktop=None, downloads=None, archive_folder="/tmp/archive", verbose=False)
        mock_config = {
            "days_threshold": 1,
            "directories": {
                "desktop": Path("~/Desktop"),
                "downloads": Path("~/Downloads"),
            },
            "archive_folder": Path("/tmp/archive"),
        }

        main()

        mock_setup_archive_folder.assert_called_once_with("/tmp/archive")
        mock_setup_logging.assert_called_once_with(False)
        mock_move_files.assert_any_call("desktop", Path("~/Desktop"), mock_config)
        mock_move_files.assert_any_call("downloads", Path("~/Downloads"), mock_config)
        mock_print.assert_called_with("Script execution completed successfully")

if __name__ == "__main__":
    unittest.main()
