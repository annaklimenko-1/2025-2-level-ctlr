"""
Pipeline for CONLL-U formatting.
"""

# pylint: disable=too-few-public-methods, unused-import, undefined-variable, too-many-nested-blocks, duplicate-code
import pathlib
import re
from typing import Optional

from core_utils.article.article import Article
from core_utils.article.io import from_raw, to_cleaned
from core_utils.pipeline import LibraryWrapper, PipelineProtocol, TreeNode

try:
    from networkx import DiGraph
    from networkx.algorithms.isomorphism import DiGraphMatcher
except ImportError:
    DiGraph = None  # type: ignore
    print("No libraries installed. Failed to import.")

try:
    from spacy.language import Language
    from spacy.tokens import Doc
except ImportError:
    Language = None  # type: ignore
    Doc = None  # type: ignore
    print("No libraries installed. Failed to import.")


class EmptyDirectoryError(Exception):
    """Raised when directory is empty."""
    pass


class InconsistentDatasetError(Exception):
    """Raised when dataset has inconsistent structure."""
    pass


class EmptyFileError(Exception):
    """Raised when file is emptyy."""
    pass


class CorpusManager:
    """
    Work with articles and store them.
    """

    def __init__(self, path_to_raw_txt_data: pathlib.Path) -> None:
        """
        Initialize an instance of the CorpusManager class.

        Args:
            path_to_raw_txt_data (pathlib.Path): Path to raw txt data
        """
        self.path_to_raw_txt_data = path_to_raw_txt_data
        self._storage: dict[int, Article] = {}
        self._validate_dataset()
        self._scan_dataset()

    def _validate_dataset(self) -> None:
        """
        Validate folder with assets.
        """
        if not self.path_to_raw_txt_data.exists():
            raise FileNotFoundError(f"Path does not exist: {self.path_to_raw_txt_data}")
        if not self.path_to_raw_txt_data.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {self.path_to_raw_txt_data}")
        
        try:
            files = list(self.path_to_raw_txt_data.iterdir())
        except OSError:
            raise EmptyDirectoryError(f"Cannot read directory: {self.path_to_raw_txt_data}")

        if not files:
            raise EmptyDirectoryError(f"Directory is empty: {self.path_to_raw_txt_data}")
        
        raw_files = []
        meta_files = []
        raw_ids = set()
        meta_ids = set()

        for file_path in files:
            if not file_path.is_file():
                continue
        
            name = file_path.name
            if name.endswith("_raw.txt"):
                id_str = name[:-8]
                if id_str.isdigit():
                    raw_id = int(id_str)
                    raw_files.append(file_path)
                    raw_ids.add(raw_id)
            elif name.endswith("_meta.json"):
                id_str = name[:-10]
                if id_str.isdigit():
                    meta_id = int(id_str)
                    meta_files.append(file_path)
                    meta_ids.add(meta_id)
        if not raw_files:
            raise EmptyDirectoryError(f"No valid raw files found in: {self.path_to_raw_txt_data}")
        
        if meta_files:
            if raw_ids != meta_ids:
                raise InconsistentDatasetError(
                    f"Raw and meta files have different IDs. "
                    f"Raw IDs: {sorted(raw_ids)}, Meta IDs: {sorted(meta_ids)}"
                )

            if raw_ids:
                expected_ids = set(range(1, max(raw_ids) + 1))
                if raw_ids != expected_ids:
                    raise InconsistentDatasetError(
                        f"Raw files have inconsistent numbering. Found IDs: {sorted(raw_ids)}. "
                        f"Expected IDs: {sorted(expected_ids)}"
                    )

        for file_path in raw_files:
            if file_path.stat().st_size == 0:
                raise InconsistentDatasetError(f"Raw file is empty: {file_path.name}")

        for file_path in meta_files:
            if file_path.stat().st_size == 0:
                raise InconsistentDatasetError(f"Meta file is empty: {file_path.name}")

    def _scan_dataset(self) -> None:
        """
        Register each dataset entry.
        """
        for file_path in self.path_to_raw_txt_data.iterdir():
            if not file_path.is_file():
                continue

            name = file_path.name

            if name.endswith("_raw.txt"):
                id_str = name[:-8]
                if id_str.isdigit():
                    article_id = int(id_str)
                    if article_id not in self._storage:
                        self._storage[article_id] = Article(url=None, article_id=article_id)

    def get_articles(self) -> dict:
        """
        Get storage params.

        Returns:
            dict: Storage params
        """
        return self._storage


class TextProcessingPipeline(PipelineProtocol):
    """
    Preprocess and morphologically annotate sentences into the CONLL-U format.
    """

    def __init__(
        self, corpus_manager: CorpusManager, analyzer: LibraryWrapper | None = None
    ) -> None:
        """
        Initialize an instance of the TextProcessingPipeline class.

        Args:
            corpus_manager (CorpusManager): CorpusManager instance
            analyzer (LibraryWrapper | None, optional): Analyzer instance. Defaults to None.
        """
        self._corpus = corpus_manager
        self._analyzer = analyzer

    def run(self) -> None:
        """
        Perform basic preprocessing and write processed text to files.
        """
        articles = self._corpus.get_articles()

        for article_id, article_obj in articles.items():
            raw_file_path = article_obj.get_raw_text_path()
            raw_text = from_raw(raw_file_path)
            text_lower = raw_text.lower()
            cleaned_text = re.sub(r'[^\w\s\n]', ' ', text_lower)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            cleaned_text = cleaned_text.strip()
            to_cleaned(article_obj, cleaned_text)


class UDPipeAnalyzer(LibraryWrapper):
    """
    Wrapper for udpipe library.
    """

    #: Analyzer
    _analyzer: Language

    def __init__(self) -> None:
        """
        Initialize an instance of the UDPipeAnalyzer class.
        """

    def _bootstrap(self) -> Language:
        """
        Load and set up the UDPipe model.

        Returns:
            Language: Analyzer instance
        """

    def analyze(self, texts: list[str]) -> list[str]:
        """
        Process texts into CoNLL-U formatted markup.

        Args:
            texts (list[str]): Collection of texts

        Returns:
            list[str]: List of documents
        """

    def to_conllu(self, article: Article) -> None:
        """
        Save content to ConLLU format.

        Args:
            article (Article): Article containing information to save
        """

    def from_conllu(self, article: Article) -> Doc:
        """
        Load ConLLU content from article stored on disk.

        Args:
            article (Article): Article to load

        Returns:
            Doc: Document ready for parsing
        """


class POSFrequencyPipeline:
    """
    Count frequencies of each POS in articles, update meta info and produce graphic report.
    """

    def __init__(self, corpus_manager: CorpusManager, analyzer: LibraryWrapper) -> None:
        """
        Initialize an instance of the POSFrequencyPipeline class.

        Args:
            corpus_manager (CorpusManager): CorpusManager instance
            analyzer (LibraryWrapper): Analyzer instance
        """

    def _count_frequencies(self, article: Article) -> dict[str, int]:
        """
        Count POS frequency in Article.

        Args:
            article (Article): Article instance

        Returns:
            dict[str, int]: POS frequencies
        """

    def run(self) -> None:
        """
        Visualize the frequencies of each part of speech.
        """


class PatternSearchPipeline(PipelineProtocol):
    """
    Search for the required syntactic pattern.
    """

    def __init__(
        self, corpus_manager: CorpusManager, analyzer: LibraryWrapper, pos: tuple[str, ...]
    ) -> None:
        """
        Initialize an instance of the PatternSearchPipeline class.

        Args:
            corpus_manager (CorpusManager): CorpusManager instance
            analyzer (LibraryWrapper): Analyzer instance
            pos (tuple[str, ...]): Root, Dependency, Child part of speech
        """

    def _make_graphs(self, doc: Doc) -> list[DiGraph]:
        """
        Make graphs for a document.

        Args:
            doc (Doc): Document for patterns searching

        Returns:
            list[DiGraph]: Graphs for the sentences in the document
        """

    def _add_children(
        self, graph: DiGraph, subgraph_to_graph: dict, node_id: int, tree_node: TreeNode
    ) -> None:
        """
        Add children to TreeNode.

        Args:
            graph (DiGraph): Sentence graph to search for a pattern
            subgraph_to_graph (dict): Matched subgraph
            node_id (int): ID of root node of the match
            tree_node (TreeNode): Root node of the match
        """

    def _find_pattern(self, doc_graphs: list) -> dict[int, list[TreeNode]]:
        """
        Search for the required pattern.

        Args:
            doc_graphs (list): A list of graphs for the document

        Returns:
            dict[int, list[TreeNode]]: A dictionary with pattern matches
        """

    def run(self) -> None:
        """
        Search for a pattern in documents and writes found information to JSON file.
        """


def main() -> None:
    """
    Entrypoint for pipeline module.
    """
    from core_utils.constants import ASSETS_PATH
    corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
    pipeline = TextProcessingPipeline(corpus_manager)
    pipeline.run()


if __name__ == "__main__":
    main()
