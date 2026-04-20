"""
Listing for practice with beautifulsoup4 library
"""

# pylint: disable=missing-timeout

from urllib.parse import urlparse, urlunparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("No libraries installed. Failed to import.")


def main() -> None:
    """
    Entrypoint for a seminar's listing
    """
    article_url = "https://bold-vest.ru/articles/1888-maiak-dlia-mnogix-pokolenii"
    response = requests.get(article_url)

    # 1. Creating instance of soup
    # install 'lxml' first or remove it from arguments below
    soup = BeautifulSoup(response.text, features="lxml")

    # 2. Getting tags by dot notation
    if soup.title:
        print(f"Title tag: {soup.title}")
        print(f"Title type: {type(soup.title)}")
        print(f"Title text: {soup.title.text}")

    # 3. Finding tags by their name
    all_spans = soup.find_all("span")
    print(f"Number of spans: {len(all_spans)}")

    # 4. Finding elements by their class
    header = soup.find_all(class_="header")
    if header:
        print(f"Found a header: {header[0].text}")

    # 5. You can mix them all if you need
    article_title = soup.find_all("h1", class_="head")
    if article_title:
        print(f"Found article_title: {article_title[0].text}")

    # 6. Get all texts
    all_body = soup.find_all("p")

    texts = []
    for p in all_body:
        texts.append(p.text)

    print("All text from a page:")
    print(" ".join(texts))

    # 7. Find any link by tag and get its attributes
    seed_url = "https://bold-vest.ru/articles/rubric/obrazovanie"
    response = requests.get(seed_url)
    soup = BeautifulSoup(response.text, features="lxml")

    all_links = soup.find_all("a")
    for link in all_links:
        try:
            address = link["href"]
        except KeyError:
            continue
        parsed_address = urlparse(str(address))
        print(
            f"Parsing the URL: {address}. "
            f"Protocol: {parsed_address.scheme}. "
            f"Netloc: {parsed_address.netloc}."
        )
        print(f"\tPath: {parsed_address.path}. Params: {parsed_address.params}.")

        if not parsed_address.netloc:
            print("This is a relative path. Let us construct the full path.")
            full_url = urlunparse(
                (
                    urlparse(seed_url).scheme,
                    urlparse(seed_url).netloc,
                    parsed_address.path,
                    None,
                    None,
                    None,
                )
            )
            print(f"And it is: {full_url}")

        # skipping all other links - remove break if you want all links to be processed
        break


if __name__ == "__main__":
    main()
