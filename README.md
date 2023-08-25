# tidyfile

An automatic archiving tool for your desktop and downloads folders

## Description

Tidyfile is a command-line utility designed to help you efficiently manage cluttered desktops and download folders. It automatically archives files older than a specified threshold, ensuring that your essential workspaces stay organized and uncluttered.

## Features

- Archive files based on their age, keeping your Desktop and Downloads folders clean.
- Customizable days threshold to decide when a file is considered for archiving.
- Supports user-defined archive folders for easy file retrieval.

## Example

```
$ python tidyfile.py --days 7 --desktop ~/Desktop --downloads ~/Downloads --archive-folder ~/Archive
Script execution completed successfully
```

This command runs tidyfile with a 7-day threshold, archiving older files from both the Desktop and Downloads folders to the specified Archive folder.

## Business Use Case

In a busy workplace, maintaining an organized digital environment is crucial for productivity. Tidyfile offers a seamless solution to reduce clutter and locate important files quickly. By automating the archival process, tidyfile frees up valuable time.

**Best Practices**

- Run tidyfile periodically using scheduled tasks or cron jobs to maintain organization effortlessly.
- Adjust the days threshold based on your usage patterns to strike a balance between tidiness and accessibility.

## Usage

```bash
python3 tidyfile.py [options]
```

### Options

- `--days`: Number of days threshold for archiving files (default is 1).
- `--desktop`: Path to the Desktop folder.
- `--downloads`: Path to the Downloads folder.
- `--archive-folder`: Path to the Archive folder (default is `~/Desktop Archive`).
- `--verbose`: Enable verbose logging.

## How to Schedule a Cronjob

Configure your cron job to run the script at specific intervals:

1. Open your terminal.

2. Edit the cron jobs using the `crontab` command. If you've never set up cron jobs before, you can start by typing:

   ```bash
   crontab -e
   ```

3. In the text editor that opens, add a new line to specify when and how often you want the script to run. For example, to run the script every day at 2:00 AM, you would add:

   ```bash
   0 2 * * * /usr/bin/env python3 /path/to/tidyfile.py --days 7 --desktop /path/to/desktop --downloads /path/to/downloads --archive-folder /path/to/archive
   ```

   Replace `/path/to/tidyfile.py`, `/path/to/desktop`, `/path/to/downloads`, and `/path/to/archive` with the actual paths on your system.

   The fields in the cron schedule are as follows:

   - `0`: Minutes (0-59)
   - `2`: Hours (0-23)
   - `*`: Day of the month (1-31)
   - `*`: Month (1-12)
   - `*`: Day of the week (0-6, where 0 is Sunday)
   - The command to run the script.

4. Save and exit the text editor.

The script will now run as a cron job according to the schedule you've specified. Make sure to adjust the schedule and paths as needed for your use case.

## Call Graph

```txt
main()
|-- parse_arguments()
|-- setup_logging()
|-- setup_archive_folder()
|-- move_files()
| |-- should_move()
```

## Data Flow

1. User provides input arguments including days threshold, folder paths, and archive folder.
2. `tidyfile.py` processes the user input and configures logging.
3. The script interacts with the file system to identify and move eligible files to the archive folder.
4. Logging records the script's actions and any issues encountered.

## Quality Assurance

Tidyfile is a script designed to help you organize and archive files based on their age. To ensure its reliability and performance, several quality assurance measures have been implemented.

### Limitations

- You cannot specify both Desktop and Downloads paths simultaneously. Choose either one when using the script.

### Error Handling

The script is designed to handle various error scenarios gracefully. If an error occurs during execution, it will be caught, and an informative error message will be displayed.

### Logging

The script uses logging to provide detailed information about its execution. Logging helps in troubleshooting and understanding the script's behavior. By default, the script logs at the INFO level. To enable more detailed logging, use the `--verbose` argument.

### Testing

The script has been thoroughly tested using unit tests to ensure its functionality and reliability. The unit tests cover different aspects of the script's logic, including argument parsing, file manipulation, and decision-making processes.

To run the unit tests, navigate to the `tests` directory and execute the following command:

```bash
python3 -m unittest test_tidyfile.py
```

## License

This project is licensed under the [MIT License](LICENSE).
