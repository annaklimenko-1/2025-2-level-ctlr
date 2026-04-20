"""
Dataset validation.
"""

# pylint: disable=assignment-from-no-return,redundant-unittest-assert
import json
import re
import shutil
import unittest

import pytest

from admin_utils.test_params import TEST_PATH
from core_utils.constants import CRAWLER_CONFIG_PATH
from lab_5_scraper.scraper import Config, make_request
from lab_5_scraper.tests.utils import scraper_setup


class RawBasicDataValidator(unittest.TestCase):
    """
    Ensure collected data includes basic information.
    """

    def setUp(self) -> None:
        """
        Define start instructions for RawBasicDataValidator class.
        """
        scraper_setup(articles_number=2)

        # open and prepare texts
        self.texts = []
        for file_name in TEST_PATH.iterdir():
            if file_name.name.endswith("_raw.txt"):
                with file_name.open(encoding="utf-8") as file:
                    file = file.read()
                    print(file_name)
                    self.texts.append((int(file_name.name.split("_")[0]), file))
        self.texts = tuple(self.texts)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_validate_sort_raw(self) -> None:
        """
        Ensure raw files numeration is homogeneous.
        """
        list_ids = [pair[0] for pair in self.texts]
        for i in range(1, len(list_ids) + 1):
            self.assertTrue(
                i in list_ids,
                msg="Articles ids are not homogeneous. " "E.g. numbers are not from 1 to N",
            )

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_texts_are_not_empty(self) -> None:
        """
        Ensure text files are not empty.
        """
        msg = (
            "Text with ID: %s seems to be empty (less than 50 characters). "
            "Check if you collected article correctly"
        )
        for file_name in self.texts:
            if len(file_name[1]) > 5:
                self.assertTrue(True)
            else:
                with (TEST_PATH / f"{file_name[0]}_meta.json").open("r", encoding="utf-8") as f:
                    content = f.read()
                print(content)
                self.assertTrue(False, msg=msg % file_name[0])

            TEST_PATH.iterdir()

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    @pytest.mark.lab_5_scraper
    def test_folder_is_filled_with_no_duplicates(self) -> None:
        """
        Ensure the collected article texts are unique.
        """
        self.assertEqual(len(self.texts), len(set(self.texts)))

    def tearDown(self) -> None:
        """
        Define final instructions for RawBasicDataValidator class.
        """
        shutil.rmtree(TEST_PATH)


def check_title_in_html(title: str, html: str) -> bool:
    """
    Check that all words from title are present in article's text.

    Args:
        title (str): Article's title
        html (str): HTML given

    Returns:
        bool: Whether all words from title are present in article's text
    """
    split_markers = (
        r"&nbsp;|&#160;|&#32;|&#9248;|&#9248;|&#xA0;|&#x20;|&#x2420;|&#x2423;|&#9251;|\s"
    )
    title = " ".join(re.split(split_markers, title)).strip()
    html = " ".join(re.split(split_markers, html))
    if "&quot;" in html:
        html = re.sub(r"&quot;", '"', html)
        title = re.sub(r"&quot;", '"', title)
    elif "\\" in html:
        html = re.sub(r"\\", "", html)
        title = re.sub(r"\\", "", title)
    return title in html


class RawMediumDataValidator(unittest.TestCase):
    """
    Ensure collected data includes extended information.
    """

    def setUp(self) -> None:
        """
        Define start instructions for RawMediumDataValidator class.
        """
        scraper_setup(articles_number=2)

        # open and prepare metadata
        self.metadata = []
        for file_name in TEST_PATH.iterdir():
            if file_name.name.endswith("_meta.json"):
                with file_name.open(encoding="utf-8") as file:
                    article_meta = json.load(file)
                    self.metadata.append((article_meta["id"], article_meta))
        self.metadata = tuple(self.metadata)
        self.config = Config(CRAWLER_CONFIG_PATH)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    @pytest.mark.lab_5_scraper
    def test_validate_sort_metadata(self) -> None:
        """
        Ensure meta files numeration is homogeneous.
        """
        list_ids = [pair[0] for pair in self.metadata]
        for i in range(1, len(list_ids) + 1):
            self.assertTrue(
                i in list_ids,
                msg="Meta file ids are not homogeneous. " "E.g. numbers are not from 1 to N",
            )

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    @pytest.mark.lab_5_scraper
    def test_validate_metadata_medium(self) -> None:
        """
        Ensure collected metadata is valid.
        """
        # can i open this URL?
        for metadata in self.metadata:
            msg = "Can not open URL: %s. Check how you collect URLs"

            response = make_request(metadata[1]["url"], self.config)
            self.assertTrue(response, msg=msg % metadata[1]["url"])

            html_source = response.text
            msg = (
                "Title is not found by specified in metadata "
                "URL %s. Check how you collect titles"
            )
            self.assertTrue(
                check_title_in_html(metadata[1]["title"], html_source), msg=msg % metadata[1]["url"]
            )

            # author is presented? NOT FOUND otherwise?
            error_message = (
                f"Author field {metadata[1]['author']} has " f"incorrect type. List is expected."
            )
            self.assertIsInstance(metadata[1]["author"], list, msg=error_message)
            try:
                self.assertTrue(all(author in html_source for author in metadata[1]["author"]))
            except AssertionError:
                message = (
                    f"Author field {metadata[1]['author']} "
                    f"(url <{metadata[1]['url']}>) is incorrect. "
                    "Collect author from the page or specify it "
                    "with special keyword <NOT FOUND> "
                    "if it is not presented at the page."
                )
                self.assertEqual(metadata[1]["author"], ["NOT FOUND"], msg=message)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    @pytest.mark.lab_5_scraper
    def test_folder_is_filled_with_no_duplicated_meta(self) -> None:
        """
        Ensure the collected meta files are unique.
        """
        for i, (meta_id, meta) in enumerate(self.metadata[:-1:]):
            for compare_id, compare_meta in self.metadata[i + 1 : :]:
                self.assertNotEqual(
                    meta_id, compare_id, "Meta IDs of different articles are the same."
                )
                self.assertNotEqual(
                    meta["url"],
                    compare_meta["url"],
                    "Meta urls of different articles are the same.",
                )

    def tearDown(self) -> None:
        """
        Define final instructions for RawMediumDataValidator class.
        """
        shutil.rmtree(TEST_PATH)


class RawAdvancedDataValidator(unittest.TestCase):
    """
    Ensure collected data includes all the required information.
    """

    def setUp(self) -> None:
        """
        Define start instructions for RawAdvancedDataValidator class.
        """
        scraper_setup()

        # datetime pattern
        self.data_pattern = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"

        # open and prepare metadata
        self.metadata = []
        for file_name in TEST_PATH.iterdir():
            if file_name.name.endswith("_meta.json"):
                with file_name.open(encoding="utf-8") as file:
                    article_meta = json.load(file)
                    self.metadata.append((article_meta["id"], article_meta))
        self.metadata = tuple(self.metadata)
        self.config = Config(CRAWLER_CONFIG_PATH)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    @pytest.mark.lab_5_scraper
    def test_validate_metadata_advanced(self) -> None:
        """
        Ensure that collected data includes correct date and topics.
        """
        for metadata in self.metadata:
            html_source = make_request(metadata[1]["url"], self.config).text

            message = (
                f"Date <{metadata[1]['date']}> do not match given "
                f"format <{self.data_pattern}> "
                f"(url <{metadata[1]['url']}>). "
                f"Check how you write dates."
            )
            self.assertTrue(re.search(self.data_pattern, metadata[1]["date"]), msg=message)

            topics = metadata[1]["topics"]
            if topics:
                for topic in topics:
                    message = (
                        f"Topics <{metadata[1]['topics']}> "
                        f"(topic <{topic}>) for url "
                        f"<{metadata[1]['url']}> are not found. "
                        f"Check how you create topics."
                    )
                    self.assertTrue(topic in html_source, msg=message)

    def tearDown(self) -> None:
        """
        Define start instructions for RawAdvancedDataValidator class.
        """
        shutil.rmtree(TEST_PATH)
