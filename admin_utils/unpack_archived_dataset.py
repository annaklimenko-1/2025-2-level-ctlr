"""
Unpack dataset.
"""

import argparse
import shutil
import sys

from quality_control.collect_coverage.run_coverage import get_target_score
from quality_control.console_logging import get_child_logger

from admin_utils.test_params import PROJECT_ROOT
from core_utils.constants import ASSETS_PATH

logger = get_child_logger(__file__)


def main(lab_name: str) -> None:  # pylint: disable=too-many-branches
    """
    Unpack dataset.

    Args:
        lab_name (str): Laboratory name
    """
    logger.info("Check files processing on student dataset")
    target_score = get_target_score(PROJECT_ROOT / lab_name)

    if target_score == 0:
        sys.exit(0)
    if target_score not in (4, 6, 8, 10):
        sys.exit("Incorrect mark!")

    ASSETS_PATH.mkdir(parents=True, exist_ok=True)
    for raw_file in PROJECT_ROOT.glob("*_raw.txt"):
        shutil.move(raw_file, ASSETS_PATH)

    if target_score != 4:
        for meta_file in PROJECT_ROOT.glob("*_meta.json"):
            shutil.move(meta_file, ASSETS_PATH)

    if lab_name == "lab_6_pipeline":
        cleaned_files = list(PROJECT_ROOT.glob("*_cleaned.txt"))
        if len(cleaned_files) != 0:
            for cleaned_file in cleaned_files:
                shutil.move(cleaned_file, ASSETS_PATH)
        else:
            logger.info("no files to move")

        if target_score > 4:
            for meta_file in PROJECT_ROOT.glob("*_meta.json"):
                shutil.move(meta_file, ASSETS_PATH)
            pos_files = list(PROJECT_ROOT.glob("*_pos.conllu"))
            if len(pos_files) != 0:
                for pos_file in pos_files:
                    shutil.move(pos_file, ASSETS_PATH)
            else:
                logger.info("no files to move")

        if target_score > 6:
            morphological_files = list(PROJECT_ROOT.glob("*_morphological.conllu"))
            if len(morphological_files) != 0:
                for morphological_file in morphological_files:
                    shutil.move(morphological_file, ASSETS_PATH)
            else:
                logger.info("no files to move")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lab_name", type=str, help="Lab name")
    args = parser.parse_args()
    main(args.lab_name)
