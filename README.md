# Google Photos Takeout Cleanup Script

A Python script to organize and clean up files from Google Photos Takeout exports by moving media files into a structured directory while excluding metadata and system files.

## Overview

When you download your Google Photos archive via Google Takeout, you often end up with a complex directory structure containing:
- Your photos and videos
- `.json` metadata files for each media file
- System files like `.DS_Store`
- Multiple nested subdirectories

This script helps you organize these files by moving all media files (photos, videos, etc.) into a clean, organized structure under a single `gphoto` directory, while excluding the metadata and system files you don't need.

## What It Does

The script performs the following operations:

1. **Scans Recursively**: Walks through all subdirectories in your source folder
2. **Filters Files**: Processes only media files (excludes `.json` and hidden files starting with `.`)
3. **Organizes Structure**: Creates folders based on the original source folder names
4. **Moves Files**: Relocates files to the new organized structure
5. **Handles Conflicts**: Automatically renames duplicate files to avoid overwrites
6. **Provides Feedback**: Shows real-time progress and final statistics

## Directory Structure

### Before Running

```
/Users/dmitri/Downloads/zips/takeouts/
├── Album1/
│   ├── photo1.jpg
│   ├── photo1.jpg.json
│   ├── photo2.jpg
│   └── photo2.jpg.json
├── Album2/
│   ├── video1.mp4
│   ├── video1.mp4.json
│   └── .DS_Store
└── Vacation/
    ├── img001.png
    └── img001.png.json
```

### After Running

```
/Users/dmitri/Downloads/zips/takeouts/
├── gphoto/
│   ├── Album1/
│   │   ├── photo1.jpg
│   │   └── photo2.jpg
│   ├── Album2/
│   │   └── video1.mp4
│   └── Vacation/
│       └── img001.png
├── Album1/
│   ├── photo1.jpg.json
│   └── photo2.jpg.json
├── Album2/
│   ├── video1.mp4.json
│   └── .DS_Store
└── Vacation/
    └── img001.png.json
```

## Features

### File Filtering

- ✅ **Moves**: All photos, videos, and other media files
- ❌ **Skips**: `.json` metadata files
- ❌ **Skips**: Hidden files starting with `.` (like `.DS_Store`, `.localized`, etc.)

### Smart Organization

- **Folder Creation**: Automatically creates destination folders based on source folder names
- **Duplicate Handling**: If a file with the same name exists, appends `_1`, `_2`, etc.
- **Preserve Names**: Keeps original filenames intact

### Safety Features

- **Confirmation Prompt**: Asks for confirmation before starting the operation
- **Non-Destructive**: Uses `shutil.move()` which is atomic on most systems
- **Error Handling**: Catches and reports errors without stopping the entire process
- **Skip gphoto**: Automatically skips files already in the `gphoto` directory to prevent loops

## Requirements

- Python 3.6 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Standard library only (no external dependencies)

## Installation

This project uses `uv` for project management:

```bash
# Initialize the project (if not already done)
uv init

# The script should be saved as main.py
```

## Usage

### Basic Usage

1. **Edit the paths** in the script if needed (defaults are already set):
   ```python
   SOURCE_DIR = "/Users/dmitri/Downloads/zips/takeouts"
   TARGET_DIR = "/Users/dmitri/Downloads/zips/takeouts/gphoto"
   ```

2. **Run the script with uv**:
   ```bash
   uv run main.py
   ```

3. **Confirm the operation** when prompted:
   ```
   Proceed? (yes/no): yes
   ```

### Command Line Output

The script provides detailed feedback:

```
Google Photos Cleanup Script
==================================================
Source: /Users/dmitri/Downloads/zips/takeouts
Target: /Users/dmitri/Downloads/zips/takeouts/gphoto

This will move all non-JSON files to the gphoto directory.
==================================================

Proceed? (yes/no): yes

Scanning: /Users/dmitri/Downloads/zips/takeouts
Target: /Users/dmitri/Downloads/zips/takeouts/gphoto

Moved: photo1.jpg -> Album1/
Moved: photo2.jpg -> Album1/
Moved: video1.mp4 -> Album2/
Moved: img001.png -> Vacation/

==================================================
Cleanup complete!
Files moved: 4
JSON files skipped: 4
==================================================
```

## Customization

### Change Source/Target Directories

Edit these variables in the script:

```python
SOURCE_DIR = "/your/custom/source/path"
TARGET_DIR = "/your/custom/target/path"
```

### Skip Additional File Types

To skip more file types, modify the filter condition:

```python
if file.lower().endswith('.json') or file.startswith('.') or file.lower().endswith('.txt'):
    skipped_count += 1
    continue
```

### Change Folder Organization

To use the full relative path instead of just the folder name:

```python
# Replace this line:
folder_name = root_path.name if root_path != source_path else "root"

# With this:
folder_name = str(relative_path) if relative_path != Path('.') else "root"
```

## Safety Considerations

### Before Running

1. **Backup Your Data**: Always have a backup before running file operations
2. **Check Paths**: Verify the source and target directories are correct
3. **Test First**: Consider testing on a small subset of files first

### Dry Run Mode

To add a dry run mode (preview without moving), add this flag:

```python
DRY_RUN = True  # Set to False to actually move files

# Then in the move section:
if not DRY_RUN:
    shutil.move(str(source_file), str(target_file))
else:
    print(f"[DRY RUN] Would move: {source_file.name} -> {folder_name}/")
```

## Troubleshooting

### Permission Errors

If you get permission errors:
```bash
# Run with sudo (use cautiously)
sudo uv run main.py
```

### Files Not Moving

- Check that the source directory path is correct
- Ensure you have write permissions
- Verify files aren't locked by another application

### Duplicate Files

The script automatically handles duplicates by appending numbers. If you see `photo_1.jpg`, `photo_2.jpg`, etc., these were files with the same name from different folders.

## What Gets Skipped

- **JSON files**: All files ending with `.json`
- **Hidden files**: All files starting with `.` (e.g., `.DS_Store`, `.localized`, `.git`, etc.)
- **Files already in gphoto**: Prevents moving files that are already organized

## Performance

- **Speed**: Processes thousands of files in seconds
- **Memory**: Low memory footprint (processes files one at a time)
- **Disk I/O**: Uses move operation (fast, doesn't copy then delete)

## License

This script is provided as-is for personal use. Feel free to modify and adapt it to your needs.

## Support

If you encounter issues:

1. Check the error message in the output
2. Verify your Python version: `python --version`
3. Ensure you have necessary permissions
4. Review the paths in the script

## Version History

- **v1.0**: Initial release with basic move functionality

