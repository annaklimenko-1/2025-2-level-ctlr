"""
Article implementation.
"""

# pylint: disable=no-name-in-module

import datetime
import enum
import pathlib
import re
import string

from core_utils.constants import ASSETS_PATH


def date_from_meta(date_txt: str) -> datetime.datetime:
    """
    Convert text date to datetime object.

    Args:
        date_txt (str): Date in text format

    Returns:
        datetime.datetime: Datetime object
    """
    if not date_txt:
        return datetime.datetime.now()
    return datetime.datetime.strptime(date_txt, "%Y-%m-%d %H:%M:%S")


def get_article_id_from_filepath(path: pathlib.Path) -> int:
    """
    Extract the article id from its path.

    Args:
        path (pathlib.Path): Path to article

    Returns:
        int: Article id
    """
    return int(path.stem.split("_")[0])


def split_by_sentence(text: str) -> list[str]:
    """
    Splits the given text by sentence separators.

    Args:
        text (str): raw text to split

    Returns:
        list[str]: List of sentences
    """
    pattern = r"(?<!\w\.\w.)(?<![А-Я][а-я]\.)((?<=\.|\?|!)|(?<=\?\"|!\"))\s(?=[А-Я])"
    text = re.sub(r"[\n|\t]+", ". ", text)
    sentences = [
        sentence
        for sentence in re.split(pattern, text)
        if sentence.replace(" ", "") and len(sentence) > 10
    ]
    return sentences


class ArtifactType(enum.Enum):
    """
    Types of artifacts that can be created by text processing pipelines.
    """

    CLEANED = "cleaned"
    UDPIPE_CONLLU = "udpipe"


class Article:
    """
    Article class implementation.
    """

    #: A date
    date: datetime.datetime | None

    #: ConLLU information
    _conllu_info: str

    def __init__(self, url: str | None, article_id: int) -> None:
        """
        Initialize an instance of Article.

        Args:
            url (str | None): Site url
            article_id (int): Article id
        """
        self.url = url
        self.article_id = article_id

        self.title = ""
        self.date = None
        self.author = []
        self.topics = []
        self.text = ""
        self.pos_frequencies = {}
        self._conllu_sentences = []
        self.pattern_matches = {}
        self._conllu_info = ""

    def set_pos_info(self, pos_freq: dict) -> None:
        """
        Set POS frequencies attribute.

        Args:
            pos_freq (dict): POS frequencies
        """
        self.pos_frequencies = pos_freq

    def set_patterns_info(self, pattern_matches: dict) -> None:
        """
        Set patterns frequencies attribute.

        Args:
            pattern_matches (dict): Syntactic patterns
        """
        self.pattern_matches = pattern_matches

    def get_meta(self) -> dict:
        """
        Get all meta params.

        Returns:
            dict: Meta params
        """
        return {
            "id": self.article_id,
            "url": self.url,
            "title": self.title,
            "date": self._date_to_text() or None,
            "author": self.author,
            "topics": self.topics,
            "pos_frequencies": self.pos_frequencies,
            "pattern_matches": self.pattern_matches,
        }

    def get_raw_text(self) -> str:
        """
        Get raw text from the article.

        Returns:
            str: Raw text from the article
        """
        return self.text

    def get_conllu_text(self, include_morphological_tags: bool) -> str:
        """
        Get the text in the CONLL-U format.

        Args:
            include_morphological_tags (bool): Flag to include morphological information

        Returns:
            str: A text in the CONLL-U format
        """
        return "\n".join(
            [
                sentence.get_conllu_text(include_morphological_tags)
                for sentence in self._conllu_sentences
            ]
        )

    def set_conllu_info(self, info: str) -> None:
        """
        Set the conllu_sentences_attribute.

        Args:
            info (str): CONLL-U sentences
        """
        self._conllu_info = info

    def get_conllu_info(self) -> str:
        """
        Get the sentences from ConlluArticle.

        Returns:
            str: Sentences from ConlluArticle
        """
        return self._conllu_info

    def get_cleaned_text(self) -> str:
        """
        Get cleaned text.

        Returns:
            str: Cleaned text.
        """
        return self.text.lower().translate(str.maketrans("", "", string.punctuation))

    def _date_to_text(self) -> str:
        """
        Convert datetime object to text.

        Returns:
            str: Datetime object
        """
        return self.date.strftime("%Y-%m-%d %H:%M:%S") if self.date else ""

    def get_raw_text_path(self) -> pathlib.Path:
        """
        Get path for requested raw article.

        Returns:
            pathlib.Path: Path to requested raw article
        """
        article_txt_name = f"{self.article_id}_raw.txt"
        return ASSETS_PATH / article_txt_name

    def get_meta_file_path(self) -> pathlib.Path:
        """
        Get path for requested article's meta info.

        Returns:
            pathlib.Path: Path to requested article's meta info
        """
        meta_file_name = f"{self.article_id}_meta.json"
        return ASSETS_PATH / meta_file_name

    def get_file_path(self, kind: ArtifactType) -> pathlib.Path:
        """
        Get a proper filepath for an Article instance.

        Args:
            kind (ArtifactType): A variant of a file

        Returns:
            pathlib.Path: Path to Article instance
        """
        extension = ".conllu" if kind == ArtifactType.UDPIPE_CONLLU else ".txt"
        article_name = f"{self.article_id}_{kind.value}{extension}"

        return ASSETS_PATH / article_name

    def get_pos_freq(self) -> dict:
        """
        Get a pos_frequency parameter.

        Returns:
            dict: POS frequency
        """
        return self.pos_frequencies
