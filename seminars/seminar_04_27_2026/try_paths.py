"""
Listing for practice with paths
"""

# pylint: disable=line-too-long,invalid-name,redefined-outer-name,duplicate-code

import shutil
from pathlib import Path


def main() -> None:
    """
    Entrypoint for a seminar's listing
    """
    # Step 1. Get the directory where this script is located
    base_dir = Path(__file__).parent
    print(f"Script is running from {base_dir}")

    # Step 2. Create file.txt if it doesn't exist
    file_txt = base_dir / "file.txt"
    if not file_txt.exists():
        file_txt.write_text("This is a sample file.\nCreated for path examples.")

    # Step 3. Show both absolute and relative paths to file.txt
    print(f"Absolute path to file.txt: {file_txt.absolute()}")
    print(f"Relative path to file.txt: {file_txt.relative_to(base_dir)}")

    # Step 4. Demonstrate path operations
    print(f"\nFile exists? {file_txt.exists()}")
    print(f"File size: {file_txt.stat().st_size} bytes")
    print(f"File content:\n{file_txt.read_text()}")

    # Step 5. Working with directories
    temp_dir = base_dir / "temp_example"
    temp_dir.mkdir(exist_ok=True)  # Create directory if doesn't exist

    # Step 6. Copy file.txt to temp directory
    copied_file = temp_dir / "copied_file.txt"
    shutil.copy(file_txt, copied_file)
    print(f"\nCopied file exists? {copied_file.exists()}")

    # Step 7. List files in directory
    print("\nFiles in temp directory:")
    for f in temp_dir.glob("*"):
        print(f" - {f.name}")

    # Step 8. Cleanup
    copied_file.unlink()  # Delete file
    temp_dir.rmdir()  # Delete empty directory
    print("\nAfter cleanup:")
    print(f"temp_dir exists? {temp_dir.exists()}")
    print(f"copied_file exists? {copied_file.exists()}")


if __name__ == "__main__":
    main()
