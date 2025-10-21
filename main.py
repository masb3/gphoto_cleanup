import os
import shutil
from pathlib import Path


def cleanup_google_photos(source_dir, target_base_dir):
    """
    Move all non-JSON files from source directory to organized structure.

    Args:
        source_dir: Source directory path (/Users/dmitri/Downloads/zips/takeouts)
        target_base_dir: Target base directory (/Users/dmitri/Downloads/zips/takeouts/gphoto)
    """
    source_path = Path(source_dir)
    target_path = Path(target_base_dir)

    # Create base gphoto directory if it doesn't exist
    target_path.mkdir(parents=True, exist_ok=True)

    # Track statistics
    moved_count = 0
    skipped_count = 0

    print(f"Scanning: {source_path}")
    print(f"Target: {target_path}\n")

    # Walk through all subdirectories
    for root, dirs, files in os.walk(source_path):
        root_path = Path(root)

        # Skip if we're already in the gphoto directory
        if target_path in root_path.parents or root_path == target_path:
            continue

        # Get the relative folder name from source_dir
        try:
            relative_path = root_path.relative_to(source_path)
        except ValueError:
            continue

        # Use the immediate parent folder name for organization
        folder_name = root_path.name if root_path != source_path else "root"

        for file in files:
            # Skip .json files and hidden files (starting with '.')
            if file.lower().endswith('.json') or file.startswith('.'):
                skipped_count += 1
                continue

            source_file = root_path / file

            # Create target directory structure
            target_dir = target_path / folder_name
            target_dir.mkdir(parents=True, exist_ok=True)

            target_file = target_dir / file

            # Handle filename conflicts
            counter = 1
            original_target = target_file
            while target_file.exists():
                stem = original_target.stem
                suffix = original_target.suffix
                target_file = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            try:
                # Move the file
                shutil.move(str(source_file), str(target_file))
                moved_count += 1
                print(f"Moved: {source_file.name} -> {folder_name}/")
            except Exception as e:
                print(f"Error moving {source_file}: {e}")

    print(f"\n{'='*50}")
    print(f"Cleanup complete!")
    print(f"Files moved: {moved_count}")
    print(f"JSON files skipped: {skipped_count}")
    print(f"{'='*50}")


if __name__ == "__main__":
    # Define paths
    SOURCE_DIR = "/Users/dmitri/Downloads/zips/takeouts"
    TARGET_DIR = "/Users/dmitri/Downloads/zips/takeouts/gphoto"

    # Confirm before proceeding
    print("Google Photos Cleanup Script")
    print("=" * 50)
    print(f"Source: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")
    print("\nThis will move all non-JSON files to the gphoto directory.")
    print("=" * 50)

    response = input("\nProceed? (yes/no): ").lower().strip()

    if response == 'yes':
        cleanup_google_photos(SOURCE_DIR, TARGET_DIR)
    else:
        print("Operation cancelled.")
