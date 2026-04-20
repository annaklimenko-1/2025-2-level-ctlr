# pylint: disable=no-member, protected-access
"""
Crawler instantiation validation.
"""

import shutil
import unittest

import pytest

from admin_utils.test_params import TEST_PATH
from core_utils.constants import CRAWLER_CONFIG_PATH
from lab_5_scraper.scraper import Config, Crawler, make_request, prepare_environment


class CrawlerTest(unittest.TestCase):
    """
    Class for testing Crawler functionality.
    """

    def setUp(self) -> None:
        """
        Define start instructions for CrawlerTest class.
        """
        self.config = Config(CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_2_crawler_check
    @pytest.mark.lab_5_scraper
    def test_newly_created_crawler_instance_empty(self) -> None:
        """
        Ensure that field 'urls' is not filled initially.
        """
        crawler = Crawler(config=self.config)
        error_msg = 'Check Crawler constructor: field "urls" is supposed to initially be empty'
        self.assertFalse(crawler.urls, error_msg)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_2_crawler_check
    @pytest.mark.lab_5_scraper
    def test_crawler_instance_is_filled_from_find_articles(self) -> None:
        """
        Ensure find_articles() fills 'urls' field.
        """
        crawler = Crawler(self.config)
        crawler.find_articles()
        error_msg = (
            'Method find_articles() must fill field "urls" '
            "with links found with the help of seed URLs"
        )
        self.assertTrue(crawler.urls, error_msg)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_2_crawler_check
    @pytest.mark.lab_5_scraper
    def test_crawler_instance_stores_full_urls(self) -> None:
        """
        Ensure URLs from 'urls' field are valid.
        """
        crawler = Crawler(self.config)
        crawler.find_articles()
        error_msg = (
            "Method find_articles() must fill field "
            '"urls" with ready-to-use, valid full links. Current url: {}'
        )
        for url in crawler.urls:
            status_code = make_request(url, self.config).status_code
            self.assertTrue(status_code == 200, error_msg.format(url))

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_2_crawler_check
    @pytest.mark.lab_5_scraper
    def test_crawler_finds_required_number_of_articles(self) -> None:
        """
        Ensure Crawler is capable to collect required number of articles.
        """
        crawler = Crawler(self.config)
        crawler.find_articles()
        error_msg = (
            'Method find_articles() must fill field "urls" '
            "with not less articles than specified in config file."
            f"{len(crawler.urls)} != {self.config.get_num_articles()}"
        )
        self.assertTrue(len(crawler.urls) >= self.config.get_num_articles(), error_msg)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_2_crawler_check
    @pytest.mark.lab_5_scraper
    def test_crawler_stores_unique_urls(self) -> None:
        """
        Ensure find_articles() fills 'urls' with unique urls.
        """
        crawler = Crawler(self.config)
        crawler.find_articles()
        error_msg = (
            'Method find_articles() must fill field "urls" '
            "with unique urls. Found "
            f"{len(crawler.urls) - len(set(crawler.urls))} "
            "duplicated urls."
        )
        self.assertEqual(len(crawler.urls), len(set(crawler.urls)), error_msg)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_2_crawler_check
    @pytest.mark.lab_5_scraper
    def test_crawler_get_search_urls(self) -> None:
        """
        Ensure get_search_urls retrieves seed urls.
        """
        crawler = Crawler(self.config)
        crawler.find_articles()
        error_msg = "Method get_search_urls() must retrieve seed urls"
        self.assertEqual(crawler.get_search_urls(), self.config.get_seed_urls(), error_msg)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_2_crawler_check
    @pytest.mark.lab_5_scraper
    def test_crawler_handles_unavailable_websites(self) -> None:
        """
        Ensure does not fail given unavailable webpage.
        """
        self.config = Config(CRAWLER_CONFIG_PATH)
        self.config._seed_urls = self.config._seed_urls + ["https://github.com/non-existent-page"]
        crawler = Crawler(self.config)
        crawler.find_articles()
        error_msg = "Crawler does not fail given unavailable webpage"
        self.assertTrue(crawler.urls, msg=error_msg)


class PrepareEnvironmentTest(unittest.TestCase):
    """
    Class for testing prepare environment function.
    """

    def setUp(self) -> None:
        """
        Define start instructions for PrepareEnvironmentTest class.
        """
        TEST_PATH.mkdir(parents=True, exist_ok=True)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_2_crawler_check
    @pytest.mark.lab_5_scraper
    def test_prepare_environment_function_creates_directory(self) -> None:
        """
        Ensure get_search_urls retrieves seed urls.
        """
        prepare_environment(TEST_PATH)
        self.assertTrue(TEST_PATH.exists())
        self.assertFalse(any(TEST_PATH.iterdir()))

    def tearDown(self) -> None:
        """
        Define final instructions for PrepareEnvironmentTest class.
        """
        if TEST_PATH.exists():
            shutil.rmtree(TEST_PATH)
