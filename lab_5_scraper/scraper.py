"""
Crawler implementation.
"""

# pylint: disable=too-many-arguments, too-many-instance-attributes, unused-import, undefined-variable, unused-argument

import datetime
import json
import re
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Tag

from core_utils.article.article import Article
from core_utils.article.io import to_meta, to_raw
from core_utils.config_dto import ConfigDTO
from core_utils.constants import ASSETS_PATH, CRAWLER_CONFIG_PATH


class IncorrectSeedURLError(Exception):
    """
    Raised when seed URL does not match standard pattern.
    """


class NumberOfArticlesOutOfRangeError(Exception):
    """
    Raised when total number of articles is out of range 1-150.
    """


class IncorrectNumberOfArticlesError(Exception):
    """
    Raised when total number of articles is not integer or less than 0.
    """


class IncorrectHeadersError(Exception):
    """
    Raised when headers are not in a form of dictionary.
    """


class IncorrectEncodingError(Exception):
    """
    Raised when encoding is not specified as a string.
    """


class IncorrectTimeoutError(Exception):
    """
    Raised when timeout value is not a positive integer less than 60.
    """


class IncorrectVerifyError(Exception):
    """
    Verify certificate value must either be True or False.
    """


class Config:
    """
    Class for unpacking and validating configurations.
    """

    def __init__(self, path_to_config: Path) -> None:
        """
        Initialize an instance of the Config class.

        Args:
            path_to_config (pathlib.Path): Path to configuration.
        """
        self.path_to_config = path_to_config

        self._seed_urls: list[str] = []
        self._num_articles: int = 0
        self._headers: dict[str, str] = {}
        self._encoding: str = ""
        self._timeout: int = 0
        self._should_verify_certificate: bool = False
        self._headless_mode: bool = False

        self._validate_config_content()

        config_values = self._extract_config_content()

        self._seed_urls = config_values.seed_urls
        self._num_articles = config_values.total_articles
        self._headers = config_values.headers
        self._encoding = config_values.encoding
        self._timeout = config_values.timeout
        self._should_verify_certificate = config_values.should_verify_certificate
        self._headless_mode = config_values.headless_mode

    def _extract_config_content(self) -> ConfigDTO:
        """
        Get config values.

        Returns:
            ConfigDTO: Config values
        """
        with open(self.path_to_config, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
    
        return ConfigDTO(
            seed_urls=config_data.get('seed_urls', []),
            total_articles_to_find_and_parse=config_data.get('total_articles_to_find_and_parse', 0),
            headers=config_data.get('headers', {}),
            encoding=config_data.get('encoding', 'utf-8'),
            timeout=config_data.get('timeout', 30),
            should_verify_certificate=config_data.get('should_verify_certificate', True),
            headless_mode=config_data.get('headless_mode', False)
        )

    def _validate_config_content(self) -> None:
        """
        Ensure configuration parameters are not corrupt.
        """
        config_dto = self._extract_config_content()

        if not isinstance(config_dto.seed_urls, list):
            raise IncorrectSeedURLError("Seed URLs must be a list")

        if not config_dto.seed_urls:
            raise IncorrectSeedURLError("Seed URLs cannot be empty")

        url_pattern = re.compile(r'^https?://(www\.)?')
        for url in config_dto.seed_urls:
            if not isinstance(url, str):
                raise IncorrectSeedURLError(f"Seed URL must be a string: {url}")
            if not url_pattern.match(url):
                raise IncorrectSeedURLError(f"Invalid seed URL format: {url}")

        total = config_dto.total_articles
        if isinstance(total, bool):
            raise IncorrectNumberOfArticlesError("Total articles must be an integer, not a boolean")

        if not isinstance(total, int):
            raise IncorrectNumberOfArticlesError("Total articles must be an integer")

        if total < 0:
            raise IncorrectNumberOfArticlesError("Total articles cannot be negative")

        if total < 1 or total > 150:
            raise NumberOfArticlesOutOfRangeError("Total articles must be between 1 and 150")

        if not isinstance(config_dto.headers, dict):
            raise IncorrectHeadersError("Headers must be a dictionary")

        if not isinstance(config_dto.encoding, str):
            raise IncorrectEncodingError("Encoding must be a string")

        timeout = config_dto.timeout
        if isinstance(timeout, bool):
            raise IncorrectTimeoutError("Timeout must be an integer, not a boolean")
            
        if not isinstance(timeout, int):
            raise IncorrectTimeoutError("Timeout must be an integer")

        if timeout <= 0 or timeout > 60:
            raise IncorrectTimeoutError("Timeout must be between 1 and 60 seconds")

        if not isinstance(config_dto.should_verify_certificate, bool):
            raise IncorrectVerifyError("Verify certificate must be a boolean")

        if not isinstance(config_dto.headless_mode, bool):
            raise IncorrectVerifyError("Headless mode must be a boolean")

    def get_seed_urls(self) -> list[str]:
        """
        Retrieve seed urls.

        Returns:
            list[str]: Seed urls
        """
        return self._seed_urls

    def get_num_articles(self) -> int:
        """
        Retrieve total number of articles to scrape.

        Returns:
            int: Total number of articles to scrape
        """
        return self._num_articles

    def get_headers(self) -> dict[str, str]:
        """
        Retrieve headers to use during requesting.

        Returns:
            dict[str, str]: Headers
        """
        return self._headers

    def get_encoding(self) -> str:
        """
        Retrieve encoding to use during parsing.

        Returns:
            str: Encoding
        """
        return self._encoding

    def get_timeout(self) -> int:
        """
        Retrieve number of seconds to wait for response.

        Returns:
            int: Number of seconds to wait for response
        """
        return self._timeout
        

    def get_verify_certificate(self) -> bool:
        """
        Retrieve whether to verify certificate.

        Returns:
            bool: Whether to verify certificate or not
        """
        return self._should_verify_certificate

    def get_headless_mode(self) -> bool:
        """
        Retrieve whether to use headless mode.

        Returns:
            bool: Whether to use headless mode or not
        """
        return self._headless_mode


def make_request(url: str, config: Config) -> requests.models.Response:
    """
    Deliver a response from a request with given configuration.

    Args:
        url (str): Site url
        config (Config): Configuration

    Returns:
        requests.models.Response: A response from a request
    """
    response = requests.get(
        url,
        headers=config.get_headers(),
        timeout=config.get_timeout(),
        verify=config.get_verify_certificate(),
    )
    response.encoding = config.get_encoding()
    return response


class Crawler:
    """
    Crawler implementation.
    """

    #: Url pattern
    url_pattern: re.Pattern | str

    def __init__(self, config: Config) -> None:
        """
        Initialize an instance of the Crawler class.

        Args:
            config (Config): Configuration
        """
        self.config = config
        self.urls: list[str] = []
        self.base_url: str = ""
        self.url_pattern = re.compile(r'/[a-z]/[a-z_]+/text_\d+\.shtml')

    def _extract_url(self, article_bs: Tag) -> str:
        """
        Find and retrieve url from HTML.

        Args:
            article_bs (bs4.Tag): Tag instance

        Returns:
            str: Url from HTML
        """
        for link in article_bs.find_all('a', href=True):
            href = link.get('href', '')
            if '.shtml' in href or 'text_' in href:
                if href.startswith('/') or href.startswith('http'):
                    return href
        return ""

    def find_articles(self) -> None:
        """
        Find articles.
        """
        required_count = self.config.get_num_articles()
        queue = list(self.config.get_seed_urls())
        visited = set()

        while queue and len(self.urls) < required_count:
            current_url = queue.pop(0)

            if current_url in visited:
                continue

            visited.add(current_url)

            match = re.match(r'(https?://[^/]+)', current_url)
            if match:
                self.base_url = match.group(1)
            else:
                continue

            try:
                response = make_request(current_url, self.config)
            except requests.RequestException:
                continue

            if not response.ok:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link.get('href', '')

                if href.startswith('/'):
                    full_url = self.base_url + href
                elif href.startswith('http'):
                    full_url = href
                else:
                    continue

                if self.url_pattern.search(full_url):
                    if full_url not in self.urls and len(self.urls) < required_count:
                        self.urls.append(full_url)
                elif '/a/' in full_url or '/b/' in full_url or '/c/' in full_url:
                    if full_url not in visited and full_url not in queue:
                        queue.append(full_url)

    def get_search_urls(self) -> list:
        """
        Get seed_urls param.

        Returns:
            list: seed_urls param
        """
        return self.config.get_seed_urls()


# 10


class CrawlerRecursive(Crawler):
    """
    Recursive implementation.

    Get one URL of the title page and find requested number of articles recursively.
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize an instance of the CrawlerRecursive class.

        Args:
            config (Config): Configuration
        """

    def find_articles(self) -> None:
        """
        Find number of article urls requested.
        """


# 4, 6, 8, 10


class HTMLParser:
    """
    HTMLParser implementation.
    """

    def __init__(self, full_url: str, article_id: int, config: Config) -> None:
        """
        Initialize an instance of the HTMLParser class.

        Args:
            full_url (str): Site url
            article_id (int): Article id
            config (Config): Configuration
        """
        self.full_url = full_url
        self.article_id = article_id
        self.config = config
        self.article = Article(full_url, article_id)

    def _fill_article_with_text(self, article_soup: BeautifulSoup) -> None:
        """
        Find text of article.

        Args:
            article_soup (bs4.BeautifulSoup): BeautifulSoup instance
        """
        paragraphs = article_soup.find_all('p')
        text_parts = []
        for p in paragraphs:
            text_parts.append(p.get_text(strip=True))

        if not text_parts:
            content_div = article_soup.find('div', class_='content')
            if content_div:
                text_parts.append(content_div.get_text(strip=True))

        if not text_parts:
            body = article_soup.find('body')
            if body:
                text_parts.append(body.get_text(strip=True))
        
        self.article.text = ' '.join(text_parts)

    def _fill_article_with_meta_information(self, article_soup: BeautifulSoup) -> None:
        """
        Find meta information of article.

        Args:
            article_soup (bs4.BeautifulSoup): BeautifulSoup instance
        """
        title_tag = article_soup.find('title')
        if title_tag:
            self.article.title = title_tag.get_text(strip=True)
        
        author_tag = article_soup.find('meta', {'name': 'author'})
        if author_tag and author_tag.get('content'):
            self.article.author = [author_tag['content']]
        else:
            author_link = article_soup.find('a', href=re.compile(r'indexdate\.shtml|/a/|/b/|/w/'))
            if author_link:
                self.article.author = [author_link.get_text(strip=True)]
            else:
                self.article.author = ["NOT FOUND"]
        date_str = None

        date_tag = article_soup.find('time')
        if date_tag:
            date_str = date_tag.get('datetime') or date_tag.get_text(strip=True)
        if not date_str:
            meta_date = article_soup.find('meta', {'name': 'article:published_time'})
            if meta_date:
                date_str = meta_date.get('content')
        if not date_str:
            date_pattern = re.compile(r'\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}|\d{4}[/.-]\d{1,2}[/.-]\d{1,2}')
            text = article_soup.get_text()
            match = date_pattern.search(text)
            if match:
                date_str = match.group(0)

        if date_str:
            self.article.date = self.unify_date_format(date_str)

        topics = []
        keywords_tag = article_soup.find('meta', {'name': 'keywords'})
        if keywords_tag and keywords_tag.get('content'):
            topics = [k.strip() for k in keywords_tag['content'].split(',')]

        if not topics:
            genre_keywords = ['проза', 'поэзия', 'рассказ', 'роман', 'повесть', 'стихотворение']
            text_lower = article_soup.get_text().lower()
            for genre in genre_keywords:
                if genre in text_lower:
                    topics.append(genre)

        self.article.topics = topics
        
        

    def unify_date_format(self, date_str: str) -> datetime.datetime:
        """
        Unify date format.

        Args:
            date_str (str): Date in text format

        Returns:
            datetime.datetime: Datetime object
        """
        months_ru = {
        'января': 'January', 'февраля': 'February', 'марта': 'March',
        'апреля': 'April', 'мая': 'May', 'июня': 'June',
        'июля': 'July', 'августа': 'August', 'сентября': 'September',
        'октября': 'October', 'ноября': 'November', 'декабря': 'December'
        }
    
        for ru, en in months_ru.items():
            if ru in date_str:
                date_str = date_str.replace(ru, en)
                break
    
        formats = [
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
            '%d.%m.%Y',
            '%d/%m/%Y',
            '%Y-%m-%d',
            '%d %B %Y, %H:%M',
            '%d %B %Y',
        ]
    
        for fmt in formats:
            try:
                return datetime.datetime.strptime(date_str, fmt)
            except (ValueError, TypeError):
                continue
    
        return datetime.datetime.now()



    def parse(self) -> Article | bool:
        """
        Parse each article.

        Returns:
            Article | bool: Article instance, False in case of request error
        """
        response = make_request(self.full_url, self.config)

        if response.ok:
            article_bs = BeautifulSoup(response.text, 'html.parser')

            self._fill_article_with_text(article_bs)

            self._fill_article_with_meta_information(article_bs)

        return self.article


def prepare_environment(base_path: Path | str) -> None:
    """
    Create ASSETS_PATH folder if no created and remove existing folder.

    Args:
        base_path (pathlib.Path | str): Path where articles stores
    """
    if base_path.exists():
        shutil.rmtree(base_path)
    base_path.mkdir(parents=True, exist_ok=True)


def main() -> None:
    """
    Entrypoint for scraper module.
    """
    prepare_environment(ASSETS_PATH)

    config = Config(CRAWLER_CONFIG_PATH)

    crawler = Crawler(config)
    crawler.find_articles()
    article_urls = crawler.urls

    for idx, url in enumerate(article_urls[:config.get_num_articles()], start=1):
        parser = HTMLParser(url, idx, config)
        article = parser.parse()
        
        to_raw(article)
        to_meta(article) 


if __name__ == "__main__":
    main()
    