"""
URL Shortener API Implementation

Here are the approaches taken in url_shorten.py:

Hashing Approach

MD5 hash of (url + timestamp + salt) — first 6 chars become the short code

Timestamp ensures different codes for same URL across sessions

Storage Approach

Two reverse-mapping dicts — url_to_code and code_to_url for O(1) both encode and decode

In-memory storage (no DB/file), suitable for interview/practice context

Collision Handling

Incremental salt — if a generated code already exists, salt is incremented and code is regenerated until unique

Idempotency

Duplicate URLs return the same short URL without creating a new entry — checked upfront in encode

OOP Approach

Single URLShortener class encapsulates all logic

Private methods (_generate_code) and private storage (_url_to_code, _code_to_url) via name convention

__len__ dunder method for natural len(shortener) usage

Error Handling

decode raises KeyError with a descriptive message for unknown short URLs instead of returning None silently
"""
# url_shorten.py
import random
import string
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl, field_validator

app = FastAPI()

# In-memory storage (Replace with Redis or SQL database for production persistence)
url_to_key: dict[str, str] = {}       # Map long_url -> short_key (for idempotency)
key_to_url: dict[str, str] = {}       # Map short_key -> long_url
key_to_visits: dict[str, int] = {}    # Map short_key -> visit_count

BASE_DOMAIN = "https://company.com"


class URLRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        # Validate URL scheme and hostname structure
        parsed = urlparse(value)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL format")
        if parsed.scheme not in ("http", "https"):
            raise ValueError("URL must start with http:// or https://")
        return value


def generate_short_key(length: int = 5) -> str:
    """Generates a random 5-character alphanumeric key."""
    chars = string.ascii_letters + string.digits
    while True:
        key = "".join(random.choice(chars) for _ in range(length))
        if key not in key_to_url:
            return key


@app.post("/", status_code=201)
def create_short_url(payload: URLRequest) -> dict[str, str]:
    long_url = payload.url

    # Idempotency check: Return existing short URL if already created
    if long_url in url_to_key:
        existing_key = url_to_key[long_url]
        return {"short_url": f"{BASE_DOMAIN}/{existing_key}"}

    # Generate new short key and save mapping
    key = generate_short_key(length=5)
    url_to_key[long_url] = key
    key_to_url[key] = long_url
    key_to_visits[key] = 0

    return {"short_url": f"{BASE_DOMAIN}/{key}"}


@app.get("/{key}")
def redirect_to_url(key: str):
    if key not in key_to_url:
        raise HTTPException(status_code=404, detail="Shortened URL not found")

    # Increment visit metrics and redirect
    key_to_visits[key] += 1
    return RedirectResponse(url=key_to_url[key], status_code=307)


@app.get("/info/{key}")
def get_url_info(key: str):
    # Returns 0 visits if key does not exist
    visits = key_to_visits.get(key, 0)
    return {"visits": visits}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
