#!/usr/bin/env python3

import logging
import argparse
from datetime import datetime, timedelta
from unittest.mock import patch
from pathlib import Path

def main():
    args = parse_arguments()

    try:
        setup_logging(args.verbose)
        archive_folder = setup_archive_folder(args.archive_folder)

        if args.desktop and args.downloads:
            print("Error: You cannot specify both Desktop and Downloads paths.")
            return

        desktop_path = Path(args.desktop) if args.desktop else Path("~/Desktop")
        downloads_path = Path(args.downloads) if args.downloads else Path("~/Downloads")

        config = {
            "days_threshold": args.days,
            "directories": {
                "desktop": desktop_path,
                "downloads": downloads_path,
            },
            "archive_folder": archive_folder,
        }

        for directory_name, directory_path in config["directories"].items():
            move_files(directory_name, directory_path, config)

        print("Script execution completed successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Archive files older than a certain number of days.")
    parser.add_argument("--days", type=int, default=1, help="Number of days threshold")
    parser.add_argument("--desktop", help="Path to Desktop folder")
    parser.add_argument("--downloads", help="Path to Downloads folder")
    parser.add_argument("--archive-folder", help="Path to Archive folder", default=Path("~/Desktop Archive"))
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args()

def setup_logging(verbose):
    level = logging.INFO if not verbose else logging.DEBUG
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def setup_archive_folder(archive_folder_path):
    archive_folder = Path(archive_folder_path).expanduser()
    archive_folder.mkdir(parents=True, exist_ok=True)
    return archive_folder

def move_files(directory_name, from_folder, config):
    for file_path in from_folder.iterdir():
        if should_move(file_path, config):
            try:
                archive_path = config["archive_folder"] / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                archive_path.mkdir(parents=True, exist_ok=True)
                new_file_path = archive_path / file_path.name
                file_path.rename(new_file_path)
                logging.info(f"Moved '{file_path.name}' to '{new_file_path}'")
            except Exception as e:
                logging.warning(f"Failed to move '{file_path.name}': {e}")

def should_move(file_path, config):
    days_threshold = config["days_threshold"]
    return (
        file_path.is_file()
        and (datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)) > timedelta(days=days_threshold)
        and not file_path.name.startswith(".")
    )

if __name__ == "__main__":
    main()
