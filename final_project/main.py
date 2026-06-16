"""
Final project implementation.
"""

# pylint: disable=unused-import
from pathlib import Path


def main(corpus_path: Path, dist_path: Path) -> None:
    """
    Generate conllu file for provided corpus of texts.

    Args:
        corpus_path (Path): Path to folder containing text files.
        dist_path (Path): Path to folder for saving auto_annotated.conllu.
    """
    result = None
    assert result, "Result is None"


if __name__ == "__main__":
    main(Path(__file__).parent / "assets" / "articles", Path(__file__).parent / "dist")
