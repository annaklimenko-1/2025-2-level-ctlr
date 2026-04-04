"""
Tests for Article.
"""

import datetime
import json
import shutil
import unittest
from pathlib import Path

import pytest

from admin_utils.test_params import TEST_PATH
from core_utils.article import article
from core_utils.article.article import (
    Article,
    ArtifactType,
    date_from_meta,
    get_article_id_from_filepath,
)
from core_utils.article.io import from_meta, from_raw, to_cleaned, to_meta, to_raw
from core_utils.tests.utils import universal_setup


class ArticleSupplementalTest(unittest.TestCase):
    """
    Class for testing supplemental functions in article.py.
    """

    def setUp(self) -> None:
        """
        Define start instructions for ArticleSupplementalTest class.
        """
        article.ASSETS_PATH = TEST_PATH
        universal_setup()
        self.text = (
            "Мама красиво мыла раму. Мама красиво мыла раму... "
            "Мама красиво мыла раму! Мама красиво мыла раму!!! "
            "Мама красиво мыла раму? Мама красиво мыла раму?! "
            'Мама мыла раму... красиво. Мама сказала: "Помой раму!"'
        )

    @pytest.mark.core_utils
    def test_date_from_meta_ideal(self) -> None:
        """
        Ideal date_from_meta scenario.
        """
        date_time = "2022-11-06 16:30:00"
        expected = datetime.datetime(2022, 11, 6, 16, 30)
        actual = date_from_meta(date_time)
        self.assertEqual(expected, actual)

    @pytest.mark.core_utils
    def test_get_article_id_return_int(self) -> None:
        """
        Ensure that get_article_id_from_filepath() function returns article id.
        """
        for file in TEST_PATH.iterdir():
            self.assertIsInstance(get_article_id_from_filepath(file), int)

    def tearDown(self) -> None:
        """
        Define final instructions for ArticleSupplementalTest class.
        """
        shutil.rmtree(TEST_PATH)


class ArticleTest(unittest.TestCase):
    """
    Class for testing Article implementation.
    """

    def setUp(self) -> None:
        """
        Define start instructions for ArticleTest class.
        """
        article.ASSETS_PATH = TEST_PATH
        universal_setup()
        self.article = Article(url="test", article_id=1)

    @pytest.mark.core_utils
    def test_article_instantiation(self) -> None:
        """
        Ensure that Article instance is instantiated correctly.
        """
        attrs = ["url", "title", "date", "author", "topics", "pos_frequencies", "_conllu_sentences"]
        error_msg = f"Article instance must possess the following arguments: {', '.join(attrs)}"

        self.assertTrue(
            all(
                (
                    hasattr(self.article, attrs[0]),
                    hasattr(self.article, attrs[1]),
                    hasattr(self.article, attrs[2]),
                    hasattr(self.article, attrs[3]),
                    hasattr(self.article, attrs[4]),
                    hasattr(self.article, attrs[5]),
                    hasattr(self.article, attrs[6]),
                )
            ),
            error_msg,
        )

    @pytest.mark.core_utils
    def test_article_instances_type(self) -> None:
        """
        Ensure that Article constructor is filled with correct instances types.
        """
        self.article = from_meta(self.article.get_meta_file_path(), self.article)

        error_msg = 'Check Article constructor: field "url" is supposed to be a string or None'
        self.assertIsInstance(self.article.url, (str, type(None)), error_msg)

        error_msg = 'Check Article constructor: field "title" is supposed to be a string'
        self.assertIsInstance(self.article.title, str, error_msg)

        error_msg = 'Check Article constructor: field "author" is supposed to be a list'
        self.assertIsInstance(self.article.author, list, error_msg)

        error_msg = 'Check Article constructor: field "topics" is supposed to be a list'
        self.assertIsInstance(self.article.topics, list, error_msg)

        error_msg = 'Check Article constructor: field "pos_frequencies" is supposed to be a dict'
        self.assertIsInstance(self.article.pos_frequencies, dict, error_msg)

        error_msg = (
            'Check Article constructor: field "_conllu_sentences" is supposed to be a string'
        )
        self.assertIsInstance(self.article.get_conllu_info(), str, error_msg)

    @pytest.mark.core_utils
    def test_article_get_raw_text_return_str(self) -> None:
        """
        Ensure that Article.get_raw_text() method returns a string.
        """
        self.assertIsInstance(self.article.get_raw_text(), str)

    @pytest.mark.core_utils
    def test_article_get_conllu_text_return_str(self) -> None:
        """
        Ensure that Article.get_conllu_text() method returns a string.
        """
        self.assertIsInstance(self.article.get_conllu_text(include_morphological_tags=False), str)

    @pytest.mark.core_utils
    def test_article_sets_conllu_sentences(self) -> None:
        """
        Ensure that Article sets the conllu_sentences_attribute.
        """
        test_sentence = "мама красиво мыла раму"
        self.article.set_conllu_info(test_sentence)
        self.assertEqual(test_sentence, self.article.get_conllu_info())

    @pytest.mark.core_utils
    def test_article_get_cleaned_text_return_str(self) -> None:
        """
        Ensure that Article.get_cleaned_text() method returns a string.
        """
        self.assertIsInstance(self.article.get_cleaned_text(), str)

    @pytest.mark.core_utils
    def test_raw_text_file_is_not_empty(self) -> None:
        """
        Ensure that a file with raw text is not empty.
        """
        error_msg = "File for article raw text is empty"
        self.assertIsNot(self.article.get_raw_text_path().stat().st_size, 0, error_msg)

    @pytest.mark.core_utils
    def test_meta_file_is_not_empty(self) -> None:
        """
        Ensure that a metafile is not empty.
        """
        error_msg = "File for article meta info is empty"
        self.assertIsNot(self.article.get_meta_file_path().stat().st_size, 0, error_msg)

    @pytest.mark.core_utils
    def test_article_get_file_path(self) -> None:
        """
        Ensure that Article.get_file_path() method gets the correct path.
        """
        kind = ArtifactType.UDPIPE_CONLLU
        self.assertTrue(isinstance(self.article.get_file_path(kind), Path))

    @pytest.mark.core_utils
    def test_article_get_file_path_raise_error(self) -> None:
        """
        Ensure that Article.get_file_path() method raises ValueError.
        """
        kind = "some text"
        with self.assertRaises(AttributeError):
            self.article.get_file_path(kind)

    # pylint: disable=protected-access
    @pytest.mark.core_utils
    def test_article_sets_pos_info(self) -> None:
        """
        Ensure that Article adds POS information in metafile.
        """
        test_statistics = {"test": 0, "test1": 1}
        self.article.set_pos_info(test_statistics)

        self.assertEqual(test_statistics, self.article.get_pos_freq())

    @pytest.mark.core_utils
    def test_article_saves_meta_file(self) -> None:
        """
        Ensure that Article saves metafile.
        """
        self.article = from_meta(self.article.get_meta_file_path(), self.article)
        to_meta(self.article)
        self.assertTrue(self.article.get_meta_file_path().is_file())

        with open(self.article.get_meta_file_path(), encoding="utf-8") as file:
            meta_file = json.load(file)

        self.article = from_meta(self.article.get_meta_file_path(), self.article)
        self.assertEqual(meta_file, self.article.get_meta())

    def tearDown(self) -> None:
        """
        Define final instructions for ArticleTest class.
        """
        shutil.rmtree(TEST_PATH)


class IOTest(unittest.TestCase):
    """
    Class for testing I/O operations for Article.
    """

    def setUp(self) -> None:
        """
        Define start instructions for IOTest class.
        """
        article.ASSETS_PATH = TEST_PATH
        universal_setup()
        self.article = Article(url="test", article_id=1)

    @pytest.mark.core_utils
    def test_raw_text_file_is_created(self) -> None:
        """
        Ensure that a file with raw text is created.
        """
        error_msg = "File for article raw text is not created"
        to_raw(self.article)
        self.assertTrue(self.article.get_raw_text_path().is_file(), error_msg)

    @pytest.mark.core_utils
    def test_from_raw_return_article(self) -> None:
        """
        Ensure that from_raw() function returns Article object.
        """
        path = TEST_PATH / "1_raw.txt"
        self.assertIsInstance(from_raw(path), Article)

    @pytest.mark.core_utils
    def test_cleaned_file_is_created(self) -> None:
        """
        Ensure that to_cleaned() function creates a file with cleaned text.
        """
        error_msg = "File for article cleaned text is not created"
        to_cleaned(self.article)
        self.assertTrue(self.article.get_file_path(ArtifactType.CLEANED).is_file(), error_msg)

    @pytest.mark.core_utils
    def test_meta_file_is_created(self) -> None:
        """
        Ensure that metafile is created.
        """
        error_msg = "File for article meta info is not created"
        to_meta(self.article)
        self.assertTrue(self.article.get_meta_file_path().is_file(), error_msg)

    def tearDown(self) -> None:
        """
        Define final instructions for IOTest class.
        """
        shutil.rmtree(TEST_PATH)
