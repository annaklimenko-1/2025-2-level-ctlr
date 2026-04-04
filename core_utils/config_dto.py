# pylint: disable=too-few-public-methods, disable=too-many-arguments, disable=too-many-positional-arguments
"""
ConfigDTO class implementation: stores the configuration information.
"""


class ConfigDTO:
    """
    Type annotations for configurations.
    """

    #: List of seed urls
    seed_urls: list[str]

    #: Number of total articles
    total_articles: int

    #: Headers
    headers: dict[str, str]

    #: Encoding
    encoding: str

    #: Number of seconds to wait for response
    timeout: int

    #: Should verify certificate or not
    should_verify_certificate: bool

    #: Require headless mode or not
    headless_mode: bool

    def __init__(
        self,
        seed_urls: list[str],
        total_articles_to_find_and_parse: int,
        headers: dict[str, str],
        encoding: str,
        timeout: int,
        should_verify_certificate: bool,
        headless_mode: bool,
    ) -> None:
        """
        Initializes an instance of the ConfigDTO class.

        Args:
            seed_urls (list[str]): Seed urls
            total_articles_to_find_and_parse (int): Number of total articles
            headers (dict[str, str]): Headers
            encoding (str): Encoding
            timeout (int): Number of seconds to wait for response
            should_verify_certificate (bool): Should verify certificate or not
            headless_mode (bool): Require headless mode or not
        """
        self.seed_urls = seed_urls
        self.total_articles = total_articles_to_find_and_parse
        self.headers = headers
        self.encoding = encoding
        self.timeout = timeout
        self.should_verify_certificate = should_verify_certificate
        self.headless_mode = headless_mode
