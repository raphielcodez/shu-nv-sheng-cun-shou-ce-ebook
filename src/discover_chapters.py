from pathlib import Path
import json
import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


# ============================================================
# PROJECT SETTINGS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

OUTPUT_FILE = ROOT / "data" / "chapters.json"

SERIES_URL = (
    "https://mydramanovel.com/"
    "shu-nv-sheng-cun-shou-ce/"
)

EXPECTED_CHAPTERS = 303

BASE_HOST = "mydramanovel.com"

BASE_PATH = "/shu-nv-sheng-cun-shou-ce/"


# ============================================================
# REQUEST SETTINGS
# ============================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    )
}

DELAY_SECONDS = 1.0


session = requests.Session()
session.headers.update(HEADERS)


# ============================================================
# URL VALIDATION
# ============================================================

def is_chapter_url(url):
    """
    Determine whether a URL belongs to this novel and
    contains a chapter number.
    """

    parsed = urlparse(url)

    host = parsed.netloc.lower()

    if host not in {
        BASE_HOST,
        f"www.{BASE_HOST}",
    }:
        return False

    path = parsed.path.lower()

    if not path.startswith(BASE_PATH):
        return False

    # We expect URLs containing chapter-N.
    match = re.search(
        r"/chapter-(\d+)",
        path,
        re.IGNORECASE,
    )

    return match is not None


# ============================================================
# EXTRACT CHAPTER NUMBER
# ============================================================

def get_chapter_number(url):
    """
    Extract the numeric chapter number from a URL.
    """

    match = re.search(
        r"/chapter-(\d+)",
        url,
        re.IGNORECASE,
    )

    if not match:
        return None

    return int(match.group(1))


# ============================================================
# NORMALIZE URL
# ============================================================

def normalize_url(url):
    return urljoin(
        SERIES_URL,
        url,
    )


# ============================================================
# CLEAN TITLE
# ============================================================

def get_title_from_link(link, chapter_number):
    """
    Get a useful chapter title from a chapter link.
    """

    text = link.get_text(
        " ",
        strip=True,
    )

    if text:
        return text

    return f"Chapter {chapter_number}"


# ============================================================
# DISCOVER CHAPTER LINKS
# ============================================================

def discover_chapters():

    print()
    print("=" * 70)
    print("DISCOVERING CONCUBINE DAUGHTER'S SURVIVAL MANUAL")
    print("=" * 70)
    print()

    print(
        f"Series page:\n{SERIES_URL}"
    )

    print()

    response = session.get(
        SERIES_URL,
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "lxml",
    )

    chapters = {}

    # ========================================================
    # Find every link on the series page
    # ========================================================

    for link in soup.find_all(
        "a",
        href=True,
    ):

        href = link.get("href")

        if not href:
            continue

        url = normalize_url(
            href
        )

        if not is_chapter_url(url):
            continue

        number = get_chapter_number(
            url
        )

        if number is None:
            continue

        if number < 1:
            continue

        if number > EXPECTED_CHAPTERS:
            continue

        title = get_title_from_link(
            link,
            number,
        )

        if number not in chapters:

            chapters[number] = {
                "number": number,
                "title": title,
                "url": url,
            }

    # ========================================================
    # Sort
    # ========================================================

    chapters_list = sorted(
        chapters.values(),
        key=lambda item: item["number"],
    )

    # ========================================================
    # Save
    # ========================================================

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            chapters_list,
            f,
            ensure_ascii=False,
            indent=2,
        )

    # ========================================================
    # Validate chapter numbers
    # ========================================================

    found_numbers = {
        chapter["number"]
        for chapter in chapters_list
    }

    expected_numbers = set(
        range(
            1,
            EXPECTED_CHAPTERS + 1,
        )
    )

    missing = sorted(
        expected_numbers
        - found_numbers
    )

    print()
    print("=" * 70)
    print("DISCOVERY COMPLETE")
    print("=" * 70)
    print()

    print(
        f"Expected chapters: {EXPECTED_CHAPTERS}"
    )

    print(
        f"Found chapters:    {len(chapters_list)}"
    )

    print(
        f"Missing chapters:  {len(missing)}"
    )

    if missing:

        print()
        print(
            "Missing chapter numbers:"
        )

        print(missing)

    else:

        print()
        print(
            "✓ All 303 chapters were discovered."
        )

    print()
    print(
        f"Saved to:\n{OUTPUT_FILE}"
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    discover_chapters()