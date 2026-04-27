"""
Listing for practice with dates
"""

# pylint: disable=line-too-long,invalid-name,redefined-outer-name,duplicate-code
from datetime import datetime
from pathlib import Path


def main() -> None:
    """
    Entrypoint for a seminar's listing
    """
    # Step 0. Setup: Create sample file
    base_dir = Path(__file__).parent
    file_txt = base_dir / "file.txt"
    if not file_txt.exists():
        file_txt.write_text("This is a sample file.\nCreated for path examples.")

    # Step 1. Get file modification time (cross-platform)
    mod_time = datetime.fromtimestamp(file_txt.stat().st_mtime)
    print(f"file.txt was last modified: {mod_time}")

    # Step 2. Formatting the modification time
    # Docs: https://python.readthedocs.io/fr/stable/library/datetime.html#strftime-and-strptime-behavior
    print(f"Formatted modification time: {mod_time.strftime('%Y.%m.%d %H:%M:%S')}")

    # Step 3. Date arithmetic with file dates
    time_since_mod = datetime.now() - mod_time
    print(f"Hours since modification: {time_since_mod.total_seconds() / 3600:.1f}")

    # Step 4. Parsing dates from strings (common in filenames)
    date_str = "report_2023-11-15.txt"
    try:
        parsed_date = datetime.strptime(date_str, "report_%Y-%m-%d.txt")
        print(f"\nExtracted date from filename: {parsed_date.date()}")
    except ValueError:
        print("\nCould not parse date from filename")


if __name__ == "__main__":
    main()
