"""
Interface definitions for text processing pipelines.
"""

# pylint: disable=too-few-public-methods, unused-argument
from dataclasses import dataclass
from typing import Protocol

from core_utils.article.article import Article


class PipelineProtocol(Protocol):
    """
    Interface definition for pipeline.
    """

    def run(self) -> None:
        """
        Key API method.
        """


class CoNLLUDocument(Protocol):
    """
    Utility class to mimic analyzer document class.
    """


@dataclass
class ConLLUWord:
    """
    Interface definition for word class of unified analyzer document.
    """

    id: str
    upos: str
    head: str
    deprel: str
    text: str


@dataclass
class ConLLUSentence:
    """
    Interface definition for sentence class of unified analyzer document.
    """

    words: list[ConLLUWord]


@dataclass
class UnifiedCoNLLUDocument:
    """
    Interface definition for sentence class of unified analyzer document.
    """

    sentences: list[ConLLUSentence]


class AbstractCoNLLUAnalyzer(Protocol):
    """
    Mock definition of library-specific entity.
    """

    def __call__(self, text: str) -> CoNLLUDocument:
        """
        Run analyzer as a function.

        Args:
            text (str): Raw document content.

        Returns:
            CoNLLUDocument: Output document.
        """


class LibraryWrapper(Protocol):
    """
    Interface definition for text analyzers.
    """

    _analyzer: AbstractCoNLLUAnalyzer

    def _bootstrap(self) -> AbstractCoNLLUAnalyzer:
        """
        Bootstrap analyzer with required models and settings.

        Returns:
            AbstractCoNLLUAnalyzer: Instance of analyzer.
        """

    def analyze(self, texts: list[str]) -> list[CoNLLUDocument | str]:
        """
        Analyze given texts.

        Args:
            texts (list[str]): Texts to analyze.

        Returns:
            list[CoNLLUDocument | str]: Collection of processed documents.
        """

    def to_conllu(self, article: Article) -> None:
        """
        Write ConLLU content to a file.

        Args:
            article (Article): Article to save
        """

    def from_conllu(self, article: Article) -> CoNLLUDocument:
        """
        Load ConLLU content from article stored on disk.

        Args:
            article (Article): Article to load

        Returns:
            CoNLLUDocument: Document ready for parsing
        """

    def get_document(self, doc: CoNLLUDocument) -> UnifiedCoNLLUDocument:
        """
        Present ConLLU document's sentence tokens as a unified structure.

        Args:
            doc (CoNLLUDocument): ConLLU document from analyzer.

        Returns:
            UnifiedCoNLLUDocument: Unified document of token features within document sentences
        """


@dataclass
class TreeNode:
    """
    Interface definition for node in the graph.
    """

    upos: str
    text: str
    children: list["TreeNode"]
