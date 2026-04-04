"""
Tests for ConfigDTO.
"""

import unittest

import pytest

from core_utils.config_dto import ConfigDTO


class ConfigDTOTest(unittest.TestCase):
    """
    Class for testing ConfigDTO implementation.
    """

    @pytest.mark.core_utils
    def test_config_dto_initialization(self) -> None:
        """
        Assert correct initialization.
        """
        seed_urls = ["https://github.com"]
        total_articles_to_find_and_parse = 2
        headers = {}
        encoding = "utf-8"
        timeout = 0
        should_verify_certificate = False
        headless_mode = False

        configuration = ConfigDTO(
            seed_urls=seed_urls,
            total_articles_to_find_and_parse=total_articles_to_find_and_parse,
            headers=headers,
            encoding=encoding,
            timeout=timeout,
            should_verify_certificate=should_verify_certificate,
            headless_mode=headless_mode,
        )
        for attribute in (
            "seed_urls",
            "total_articles",
            "headers",
            "encoding",
            "timeout",
            "should_verify_certificate",
            "headless_mode",
        ):
            self.assertTrue(hasattr(configuration, attribute))
