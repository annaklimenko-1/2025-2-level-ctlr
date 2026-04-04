"""
Changer of num_article param with random number in range(2, 7).
"""

import argparse
import json
import random


def parser() -> argparse.ArgumentParser:
    """
    Change parameters.

    Returns:
        argparse.ArgumentParser: Parser object
    """
    parser_ = argparse.ArgumentParser(description=" ")
    parser_.add_argument(
        "--config_path", type=str, required=True, help="Full path to the scraper config file"
    )
    return parser_


def change_volume(config: str) -> None:
    """
    Change article volume.

    Args:
        config (str): Config
    """
    with open(config, encoding="utf-8") as file:
        reference = json.load(file)

    num_articles = random.randint(2, 7)
    reference["total_articles_to_find_and_parse"] = num_articles

    with open(config, "w", encoding="utf-8") as file:
        json.dump(reference, file)


if __name__ == "__main__":
    args = parser().parse_args()
    change_volume(args.config_path)
