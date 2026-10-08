from pathlib import Path
import json
import re
import time
import html

import requests
from bs4 import BeautifulSoup


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

CHAPTER_INDEX_FILE = (
    ROOT / "data" / "chapters.json"
)

OUTPUT_DIR = (
    ROOT / "data" / "chapters"
)


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
# UNWANTED TEXT
# ============================================================

UNWANTED_EXACT = {
    "previous chapter",
    "next chapter",
    "previous",
    "next",
    "comments",
    "comment",
    "leave a comment",
    "post a comment",
    "submit comment",
    "share",
    "share this",
    "share this post",
    "related posts",
    "related post",
    "read more",
    "subscribe",
}


UNWANTED_SUBSTRINGS = [
    "previous chapter",
    "next chapter",
    "leave a comment",
    "post a comment",
    "submit comment",
    "subscribe to",
    "follow us",
    "share this post",
    "share this",
    "related posts",
    "related post",
    "you may also like",
    "read more",
]


# ============================================================
# POSSIBLE CONTENT CONTAINERS
# ============================================================

CONTENT_SELECTORS = [
    "article .entry-content",
    "article .post-content",
    "article .entry-content-wrap",
    ".entry-content",
    ".post-content",
    ".entry-content-wrap",
    "article",
]


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):
    """
    Normalize text and remove obvious website/navigation
    fragments.
    """

    if not text:
        return ""

    text = html.unescape(
        text
    )

    text = text.replace(
        "\xa0",
        " ",
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    text = text.strip()

    if not text:
        return ""

    lower = text.lower()

    if lower in UNWANTED_EXACT:
        return ""

    for phrase in UNWANTED_SUBSTRINGS:

        if phrase in lower:
            return ""

    return text


# ============================================================
# REMOVE WEBSITE ELEMENTS
# ============================================================

def remove_unwanted_elements(
    container
):
    """
    Remove site navigation, comments, ads, sharing widgets,
    images, sidebars, etc.
    """

    selectors = [

        # Scripts
        "script",
        "style",
        "noscript",

        # Embedded media
        "iframe",
        "video",
        "audio",

        # Forms
        "form",

        # Navigation
        "nav",
        ".navigation",
        ".nav-links",
        ".post-navigation",
        ".pagination",

        # Comments
        "#comments",
        ".comments",
        ".comment-list",
        ".comment-respond",
        ".comments-area",

        # Social sharing
        ".sharedaddy",
        ".social-sharing",
        ".share-buttons",
        ".social-buttons",
        ".sharing",

        # Advertisements
        ".ads",
        ".advertisement",
        ".advert",
        ".ad-container",
        ".google-auto-placed",

        # Related content
        ".related-posts",
        ".related",
        ".you-may-also-like",

        # Widgets/sidebar
        ".widget",
        ".sidebar",

        # Footer
        ".footer",
        ".site-footer",

        # Media
        "img",
        "figure",
    ]

    for selector in selectors:

        for element in container.select(
            selector
        ):

            element.decompose()


# ============================================================
# FIND CONTENT CONTAINER
# ============================================================

def find_content_container(
    soup
):
    """
    Locate the container most likely to contain the actual
    chapter prose.
    """

    # --------------------------------------------------------
    # Preferred selectors
    # --------------------------------------------------------

    for selector in CONTENT_SELECTORS:

        container = soup.select_one(
            selector
        )

        if container:

            paragraph_count = len(
                container.find_all("p")
            )

            if paragraph_count >= 2:

                return container

    # --------------------------------------------------------
    # Fallback: choose the container with the most paragraphs.
    # --------------------------------------------------------

    candidates = []

    for selector in [
        "article",
        "main",
        "section",
        "div",
    ]:

        for container in soup.select(
            selector
        ):

            paragraph_count = len(
                container.find_all("p")
            )

            if paragraph_count > 0:

                candidates.append(
                    (
                        paragraph_count,
                        container,
                    )
                )

    if candidates:

        candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return candidates[0][1]

    return None


# ============================================================
# EXTRACT PARAGRAPHS
# ============================================================

def extract_paragraphs(
    container
):
    """
    Extract actual paragraph elements.

    This is deliberately NOT:
        container.get_text()

    because get_text() would flatten the entire website
    section into one giant block.
    """

    paragraphs = []

    # --------------------------------------------------------
    # Primary extraction: paragraph tags
    # --------------------------------------------------------

    p_tags = container.find_all(
        "p"
    )

    for p in p_tags:

        text = p.get_text(
            " ",
            strip=True,
        )

        text = clean_text(
            text
        )

        if not text:
            continue

        paragraphs.append(
            text
        )

    # --------------------------------------------------------
    # Fallback for pages that don't use <p>
    # --------------------------------------------------------

    if not paragraphs:

        for element in container.find_all(
            ["div", "br"]
        ):

            text = element.get_text(
                " ",
                strip=True,
            )

            text = clean_text(
                text
            )

            if text:

                paragraphs.append(
                    text
                )

    # --------------------------------------------------------
    # Remove consecutive duplicates.
    # --------------------------------------------------------

    cleaned = []

    for paragraph in paragraphs:

        if (
            cleaned
            and paragraph == cleaned[-1]
        ):
            continue

        cleaned.append(
            paragraph
        )

    return cleaned


# ============================================================
# SCRAPE ONE CHAPTER
# ============================================================

def scrape_chapter(
    chapter
):

    number = chapter["number"]

    title = chapter["title"]

    url = chapter["url"]

    print()
    print(
        f"Scraping Chapter {number}: "
        f"{title}"
    )

    print(url)

    response = session.get(
        url,
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "lxml",
    )

    container = find_content_container(
        soup
    )

    if container is None:

        raise RuntimeError(
            f"Could not find the chapter "
            f"content container for Chapter "
            f"{number}."
        )

    remove_unwanted_elements(
        container
    )

    paragraphs = extract_paragraphs(
        container
    )

    if not paragraphs:

        raise RuntimeError(
            f"No chapter prose was found "
            f"for Chapter {number}."
        )

    return {
        "number": number,
        "title": title,
        "paragraphs": paragraphs,
    }


# ============================================================
# MAIN SCRAPER
# ============================================================

def scrape_chapters():

    print()
    print("=" * 70)
    print(
        "SCRAPING CONCUBINE DAUGHTER'S "
        "SURVIVAL MANUAL"
    )
    print("=" * 70)
    print()

    if not CHAPTER_INDEX_FILE.exists():

        raise FileNotFoundError(
            "data/chapters.json was not found.\n"
            "Run discover_chapters.py first."
        )

    with open(
        CHAPTER_INDEX_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        chapters = json.load(f)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ========================================================
    # TEST MODE
    # ========================================================
    #
    # FIRST RUN:
    #
    #     chapters = chapters[:1]
    #
    # This scrapes ONLY Chapter 1 so you can inspect it.
    #
    # AFTER Chapter 1 is confirmed clean, change it to:
    #
    #     chapters = chapters
    #
    # ========================================================

    chapters = chapters

    print(
        f"Chapters selected for this run: "
        f"{len(chapters)}"
    )

    # ========================================================
    # SCRAPE
    # ========================================================

    successful = 0
    failed = 0

    for chapter in chapters:

        number = chapter["number"]

        output_file = (
            OUTPUT_DIR
            / f"chapter_{number:03d}.json"
        )

        try:

            cleaned = scrape_chapter(
                chapter
            )

            with open(
                output_file,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    cleaned,
                    f,
                    ensure_ascii=False,
                    indent=2,
                )

            print(
                f"✓ Saved "
                f"{output_file.name}"
            )

            print(
                f"  Paragraphs: "
                f"{len(cleaned['paragraphs'])}"
            )

            successful += 1

        except Exception as exc:

            print()
            print(
                f"✗ ERROR Chapter {number}"
            )

            print(
                str(exc)
            )

            failed += 1

        time.sleep(
            DELAY_SECONDS
        )

    print()
    print("=" * 70)
    print("SCRAPING RUN COMPLETE")
    print("=" * 70)
    print()

    print(
        f"Successful: {successful}"
    )

    print(
        f"Failed:     {failed}"
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    scrape_chapters()