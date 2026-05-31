"""
Pipeline for CONLL-U formatting.
"""

# pylint: disable=too-few-public-methods, unused-import, undefined-variable, too-many-nested-blocks, duplicate-code
import pathlib
import re
import json
from typing import Optional

import spacy_udpipe
from spacy_conll.parser import ConllParser

from core_utils.article.article import Article, ArtifactType
from core_utils.article.io import from_meta, from_raw, to_cleaned, to_meta
from core_utils.constants import ASSETS_PATH, PROJECT_ROOT
from core_utils.pipeline import LibraryWrapper, PipelineProtocol, TreeNode
from core_utils.visualizer import visualize

try:
    from networkx import DiGraph
    from networkx.algorithms.isomorphism import DiGraphMatcher
except ImportError:
    DiGraph = None
    DiGraphMatcher = None

try:
    from spacy.language import Language
    from spacy.tokens import Doc
except ImportError:
    Language = None
    Doc = None


class EmptyDirectoryError(Exception):
    """Raised when directory is empty."""


class InconsistentDatasetError(Exception):
    """Raised when dataset has inconsistent structure."""


class EmptyFileError(Exception):
    """Raised when file is empty."""


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
        except OSError as exc:
            raise EmptyDirectoryError(
                f"Cannot read directory: {self.path_to_raw_txt_data}"
            ) from exc

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
            raise EmptyDirectoryError(
                f"No valid raw files found in: {self.path_to_raw_txt_data}"
            )

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

        if len(raw_ids) != len(meta_ids):
            raise InconsistentDatasetError(
                f"Number of raw files ({len(raw_ids)}) "
                f"does not match number of meta files ({len(meta_ids)})"
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
        for file_path in self.path_to_raw_txt_data.glob("*_raw.txt"):
            article_id = int(file_path.stem.split("_")[0])
            article = Article(url=None, article_id=article_id)
            from_raw(file_path, article)
            self._storage[article_id] = article

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
        self, corpus_manager: CorpusManager, analyzer: Optional[LibraryWrapper] = None
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

        for article_obj in articles.values():
            raw_file_path = article_obj.get_raw_text_path()
            article_with_text = from_raw(raw_file_path)
            raw_text = article_with_text.text

            # Очистка для *_cleaned.txt (оценка 4)
            text_lower = raw_text.lower()
            cleaned_text = re.sub(r'[^\w\s\n]', ' ', text_lower)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            cleaned_text = cleaned_text.strip()

            article_obj.cleaned_text = cleaned_text
            to_cleaned(article_obj)

            # UDPipe использует оригинальный текст
            if self._analyzer is not None:
                conllu_results = self._analyzer.analyze([raw_text])
                if conllu_results:
                    article_obj.set_conllu_info(conllu_results[0])
                    self._analyzer.to_conllu(article_obj)


class UDPipeAnalyzer(LibraryWrapper):
    """
    Wrapper for udpipe library.
    """

    _analyzer: Optional[Language] = None
    _parser: Optional[ConllParser] = None

    def __init__(self) -> None:
        """
        Initialize an instance of the UDPipeAnalyzer class.
        """
        self._analyzer = self._bootstrap()
        if ConllParser is not None and self._analyzer is not None:
            self._parser = ConllParser(self._analyzer)

    def _bootstrap(self) -> Optional[Language]:
        """
        Load and set up the UDPipe model.

        Returns:
            Language: Analyzer instance
        """
        if spacy_udpipe is None:
            raise ImportError("spacy_udpipe is not installed")

        from core_utils.constants import PROJECT_ROOT

        model_path = (
            PROJECT_ROOT / 'lab_6_pipeline' / 'assets' / 'model'
            / 'russian-syntagrus-ud-2.0-170801.udpipe'
        )

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")

        nlp = spacy_udpipe.load_from_path(lang='ru', path=str(model_path))

        if "conll_formatter" not in nlp.pipe_names:
            nlp.add_pipe(
                "conll_formatter",
                last=True,
                config={
                    "conversion_maps": {"XPOS": {"": "_"}},
                    "include_headers": True,
                    "field_names": {
                        "ID": "ID",
                        "FORM": "FORM",
                        "LEMMA": "LEMMA",
                        "UPOS": "UPOS",
                        "XPOS": "XPOS",
                        "FEATS": "FEATS",
                        "HEAD": "HEAD",
                        "DEPREL": "DEPREL",
                        "DEPS": "DEPS",
                        "MISC": "MISC",
                    },
                },
            )

        nlp.max_length = 2000000

        return nlp

    def analyze(self, texts: list[str]) -> list[str]:
        """
        Process texts into CoNLL-U formatted markup.

        Args:
            texts (list[str]): Collection of texts

        Returns:
            list[str]: List of documents
        """
        if self._analyzer is None:
            return []

        results = []
        for text in texts:
            doc = self._analyzer(text)
            conllu = doc._.conll_str
            results.append(conllu)

        return results

    def to_conllu(self, article: Article) -> None:
        """
        Save content to ConLLU format.

        Args:
            article (Article): Article containing information to save
        """
        conllu_info = article.get_conllu_info()
        if conllu_info:
            conllu_path = article.get_file_path(ArtifactType.UDPIPE_CONLLU)
            conllu_path.write_text(conllu_info + '\n', encoding='utf-8')

    def from_conllu(self, article: Article) -> Doc:
        """
        Load ConLLU content from article stored on disk.

        Args:
            article (Article): Article to load

        Returns:
            Doc: Document ready for parsing
        """
        if self._parser is None:
            raise ImportError("ConllParser is not available")

        conllu_path = article.get_file_path(ArtifactType.UDPIPE_CONLLU)

        if not conllu_path.exists():
            raise FileNotFoundError(f"CoNLL-U file not found: {conllu_path}")

        conllu_content = conllu_path.read_text(encoding='utf-8')

        if len(conllu_content.strip()) == 0:
            raise EmptyFileError(f"CoNLL-U file is empty: {conllu_path}")

        doc = self._parser.parse_conll_text_as_spacy(conllu_content.rstrip('\n'))
        return doc


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
        self._corpus = corpus_manager
        self._analyzer = analyzer

    def _count_frequencies(self, article: Article) -> dict[str, int]:
        """
        Count POS frequency in Article.

        Args:
            article (Article): Article instance

        Returns:
            dict[str, int]: POS frequencies
        """
        doc = self._analyzer.from_conllu(article)
        pos_counter: dict[str, int] = {}

        for token in doc:
            pos = token.pos_
            if pos in pos_counter:
                pos_counter[pos] += 1
            else:
                pos_counter[pos] = 1

        return pos_counter

    def run(self) -> None:
        """
        Visualize the frequencies of each part of speech.
        """
        from core_utils.constants import ASSETS_PATH

        for article in self._corpus.get_articles().values():
            frequencies = self._count_frequencies(article)
            if frequencies:
                article.set_pos_info(frequencies)
                to_meta(article)
                visualize(
                    article=article,
                    path_to_save=ASSETS_PATH / f'{article.article_id}.image.png'
                )

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
        self._corpus = corpus_manager
        self._analyzer = analyzer
        self._node_labels = pos

    def _make_graphs(self, doc: Doc) -> list[DiGraph]:
        """
        Make graphs for a document.

        Args:
            doc (Doc): Document for patterns searching

        Returns:
            list[DiGraph]: Graphs for the sentences in the document
        """
        return []

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
        return {}

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

    if spacy_udpipe is not None:
        analyzer = UDPipeAnalyzer()
        pipeline = TextProcessingPipeline(corpus_manager, analyzer)
        pipeline.run()

        pos_pipeline = POSFrequencyPipeline(corpus_manager, analyzer)
        pos_pipeline.run()
    else:
        print("spacy_udpipe not installed. Running basic preprocessing only (score 4).")
        pipeline = TextProcessingPipeline(corpus_manager)
        pipeline.run()


if __name__ == "__main__":
    main()
