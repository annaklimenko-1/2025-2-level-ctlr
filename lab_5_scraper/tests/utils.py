"""
Utils for lab_5_scraper tests.
"""

# pylint: disable=no-member,assignment-from-no-return

import random

from admin_utils.test_params import TEST_PATH
from core_utils.article import article
from core_utils.article.io import to_meta, to_raw
from core_utils.constants import ASSETS_PATH, CRAWLER_CONFIG_PATH
from core_utils.tests.utils import copy_student_data
from lab_5_scraper.scraper import Config, Crawler, HTMLParser


def scraper_setup(articles_number: int = 1) -> None:
    """
    Set up TEST_PATH for scraper tests.

    Args:
        articles_number (int, optional): number of articles
            to collect for tests. Defaults to 1.
    """
    if ASSETS_PATH.exists() and any(ASSETS_PATH.iterdir()):
        copy_student_data()
    else:
        config = Config(CRAWLER_CONFIG_PATH)

        TEST_PATH.mkdir(exist_ok=True)
        article.ASSETS_PATH = TEST_PATH

        crawler = Crawler(config)
        crawler.find_articles()
        for article_id in range(1, articles_number + 1):
            random_url = random.choice(crawler.urls)
            parser = HTMLParser(random_url, article_id, config)
            return_value = parser.parse()
            to_raw(return_value)
            to_meta(return_value)
            crawler.urls.remove(random_url)
