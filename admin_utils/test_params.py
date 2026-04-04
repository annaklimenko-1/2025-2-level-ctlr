"""
Parameters for testing.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

SCRAPER_CONFIG = "scraper_config.json"
CRAWLER_CONFIG_PATH = PROJECT_ROOT / "lab_5_scraper" / SCRAPER_CONFIG

TEST_PATH = PROJECT_ROOT / "test_tmp"

TEST_SCRAPER_CONFIG = "scraper_config_test.json"
TEST_CRAWLER_CONFIG_PATH = TEST_PATH / TEST_SCRAPER_CONFIG

PIPE_TEST_FILES_FOLDER = PROJECT_ROOT / "lab_6_pipeline" / "tests" / "test_files"
CORE_UTILS_TEST_FILES_FOLDER = PROJECT_ROOT / "core_utils" / "tests" / "test_files"
