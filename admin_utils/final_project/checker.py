"""
Public module for checking student CoNLL-U files.
"""

import logging
import subprocess
import sys
from pathlib import Path

from quality_control.cli_unifier import _run_console_tool, choose_python_exe
from quality_control.console_logging import get_child_logger

from admin_utils.constants import PROJECT_ROOT

logger = get_child_logger(__file__)

if not logger.handlers:
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))


def check_via_official_validator(conllu_path: Path) -> tuple[str, str, int]:
    """
    Run validator checks for the project.

    URL: https://github.com/UniversalDependencies/tools/blob/master/validate.py

    Args:
        conllu_path: Path to conllu file

    Returns:
        subprocess.CompletedProcess: Program execution values
    """
    validator_args = [
        str(Path(__file__).parent / "ud_validator" / "validate.py"),
        "--lang",
        "ru",
        "--max-err",
        "0",
        "--level",
        "2",
        str(PROJECT_ROOT / conllu_path),
    ]
    return _run_console_tool(str(choose_python_exe(PROJECT_ROOT)), validator_args, debug=True)


def main() -> None:
    """
    Module entrypoint.
    """
    if len(sys.argv) < 2:
        logger.info("Provide path to the file to check.")
        sys.exit(1)
    conllu_path = Path(sys.argv[1])
    if not conllu_path.exists():
        logger.info("Total CONLLU file is not present. Analyze first.")
        sys.exit(1)
    if conllu_path.stat().st_size == 0:
        logger.info("CONLLU file is empty. Nothing to validate.")
        sys.exit(1)

    try:
        stdout, stderr, return_code = check_via_official_validator(conllu_path=conllu_path)
        logger.info(stdout)
        logger.info(stderr)
        logger.info(return_code)
        logger.info("Check passed.")
    except subprocess.CalledProcessError as e:
        logger.info(e.stdout.decode("utf-8", errors="replace"))
        logger.info(e.stderr.decode("utf-8", errors="replace"))
        logger.info("Check failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
