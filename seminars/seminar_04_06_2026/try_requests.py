"""
Listing for practice with requests library
"""

# pylint: disable=missing-timeout,line-too-long,invalid-name


try:
    import requests
except ImportError:
    print("No libraries installed. Failed to import.")

if __name__ == "__main__":
    # Step 1. GET request
    url = "https://lit.lib.ru/"
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    print(f"First 500 chars:\n{response.text[:500]}...")



    # Step 3. Adding headers (simulate browser request, some sites may respond better)
    # View my headers at: https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending/
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 YaBrowser/26.3.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "ru,en;q=0.9",
    }
    response = requests.get(url, headers=headers)
    print(f"With headers status: {response.status_code}")

    # Step 4. Using timeout (seconds) to avoid hanging requests
    try:
        response = requests.get(url, headers=headers, timeout=3)
        print("Request successful with timeout")
    except requests.exceptions.Timeout:
        print("Timeout: Server didn't respond in 3s")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    # Step 5. Response handling
    if response.ok:
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Page saved successfully")
    else:
        print(f"Error: HTTP {response.status_code}")
