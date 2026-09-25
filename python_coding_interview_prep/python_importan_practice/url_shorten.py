import hashlib
import time

# URL Shortener — similar to bit.ly, TinyURL
# Approach: MD5 hash of (url + timestamp) → take first 6 chars as short code
# Storage: two dicts for O(1) encode/decode
# Collision: regenerate with incremented salt until unique

BASE_URL = "https://short.ly/"


class URLShortener:
    def __init__(self):
        self._url_to_code: dict[str, str] = {}  # original → short code
        self._code_to_url: dict[str, str] = {}  # short code → original

    def _generate_code(self, url: str, salt: int = 0) -> str:
        """Generate a 6-char alphanumeric code from MD5 hash."""
        raw = f"{url}{time.time()}{salt}".encode()
        return hashlib.md5(raw).hexdigest()[:6]

    def encode(self, long_url: str) -> str:
        """Shorten a URL. Returns same short URL if already encoded."""
        if long_url in self._url_to_code:
            return BASE_URL + self._url_to_code[long_url]

        # Handle collision by incrementing salt
        salt, code = 0, self._generate_code(long_url)
        while code in self._code_to_url:
            salt += 1
            code = self._generate_code(long_url, salt)

        self._url_to_code[long_url] = code
        self._code_to_url[code] = long_url
        return BASE_URL + code

    def decode(self, short_url: str) -> str:
        """Retrieve original URL from short URL. Raises KeyError if not found."""
        code = short_url.removeprefix(BASE_URL)
        if code not in self._code_to_url:
            raise KeyError(f"Short URL not found: {short_url}")
        return self._code_to_url[code]

    def __len__(self):
        return len(self._url_to_code)


if __name__ == "__main__":
    shortener = URLShortener()

    urls = [
        "https://www.example.com/some/very/long/path?query=123&page=1",
        "https://www.google.com/search?q=dijkstra+algorithm",
        "https://www.example.com/some/very/long/path?query=123&page=1",  # duplicate
    ]

    print("--- Encoding ---")
    short_urls = [shortener.encode(url) for url in urls]
    for original, short in zip(urls, short_urls):
        print(f"{original}\n  → {short}")

    print(f"\nTotal unique URLs stored: {len(shortener)}")

    print("\n--- Decoding ---")
    for short in set(short_urls):
        print(f"{short}\n  → {shortener.decode(short)}")
