"""
Tests for final project implementation.
"""

import shutil
from pathlib import Path
from typing import Generator

import pytest

import final_project.main as main_module
from admin_utils.final_project.checker import check_via_official_validator


@pytest.fixture(scope="function")
def corpus_path(tmp_path: Path) -> Path:
    """
    Create temporary corpus folder with test files.

    Args:
        tmp_path (Path): Temporary path fixture.

    Returns:
        Path: Path to corpus folder with copied test files.
    """
    assets_path = tmp_path / "assets"
    assets_path.mkdir(parents=True, exist_ok=True)

    test_files_dir = Path(__file__).parent / "test_files"
    txt_files = list(test_files_dir.glob("*.txt"))

    if not txt_files:
        pytest.skip("No test files found in specified directory")

    for txt_file in txt_files:
        shutil.copy(txt_file, assets_path / txt_file.name)

    return assets_path


@pytest.fixture(scope="function")
def dist_path(tmp_path: Path) -> Path:
    """
    Create temporary dist folder.

    Args:
        tmp_path (Path): Temporary path fixture.

    Returns:
        Path: Path to created dist folder.
    """
    dist = tmp_path / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    return dist


@pytest.fixture(scope="function")
def generated_conllu(corpus_path: Path, dist_path: Path) -> Generator[Path, None, None]:
    """
    Run main and yield path to generated conllu.

    Args:
        corpus_path (Path): Path to corpus folder with test files.
        dist_path (Path): Path to dist folder for output.

    Yields:
        Path: Path to generated auto_annotated.conllu file.
    """
    main_module.main(corpus_path=corpus_path, dist_path=dist_path)
    yield dist_path / "auto_annotated.conllu"


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.final_project
def test_main_creates_conllu_file(generated_conllu: Path) -> None:
    """
    Ensure auto_annotated.conllu is created in dist folder.

    Args:
        generated_conllu (Path): Fixture to generated conllu.
    """
    assert generated_conllu.exists(), f"auto_annotated.conllu was not created at {generated_conllu}"


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.final_project
def test_main_creates_nonempty_conllu(generated_conllu: Path) -> None:
    """
    Ensure generated conllu file is not empty.

    Args:
        generated_conllu (Path): Fixture to generated conllu.
    """
    content = generated_conllu.read_text(encoding="utf-8").strip()
    assert content, "Generated auto_annotated.conllu is empty"


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.final_project
def test_main_generates_valid_conllu(generated_conllu: Path) -> None:
    """
    Ensure generated conllu passes official UD validator.

    Args:
        generated_conllu (Path): Fixture to generated conllu.
    """
    _, _, return_code = check_via_official_validator(generated_conllu)
    assert return_code == 0, "Generated conllu file failed UD validation"


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.final_project
def test_main_correct_filename(generated_conllu: Path) -> None:
    """
    Ensure output file is named exactly auto_annotated.conllu.

    Args:
        generated_conllu (Path): Fixture to generated conllu.
    """
    assert (
        generated_conllu.name == "auto_annotated.conllu"
    ), f"Expected auto_annotated.conllu, got {generated_conllu.name}"


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.final_project
def test_main_fails_on_empty_corpus(tmp_path: Path) -> None:
    """
    Ensure an error is raised when corpus folder has no txt files.

    Args:
        tmp_path (Path): Temporary path fixture.
    """
    empty_corpus = tmp_path / "assets"
    empty_corpus.mkdir(parents=True, exist_ok=True)
    dist = tmp_path / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    with pytest.raises(ValueError):
        main_module.main(corpus_path=empty_corpus, dist_path=dist)


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.final_project
def test_main_fails_when_corpus_folder_missing(tmp_path: Path) -> None:
    """
    Ensure an error is raised when corpus folder does not exist.

    Args:
        tmp_path (Path): Temporary path fixture.
    """
    missing_corpus = tmp_path / "assets" / "nonexistent"
    dist = tmp_path / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    with pytest.raises(FileNotFoundError):
        main_module.main(corpus_path=missing_corpus, dist_path=dist)
