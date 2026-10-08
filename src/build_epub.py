from pathlib import Path
import json
from html import escape

from ebooklib import epub


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

CHAPTERS_DIR = (
    ROOT / "data" / "chapters"
)

OUTPUT_DIR = (
    ROOT / "output"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "Concubine Daughters Survival Manual by Yu Jing Peng Xiang.epub"
)


# ============================================================
# BOOK INFORMATION
# ============================================================

BOOK_TITLE = (
    "Concubine Daughter's Survival Manual"
)

ORIGINAL_TITLE = (
    "庶女生存手册"
)

ALTERNATE_TITLE = (
    "Shu Nv Sheng Cun Shou Ce"
)

AUTHOR = (
    "Yu Jing Peng Xiang"
)

TOTAL_CHAPTERS = 303


# ============================================================
# EPUB CSS
# ============================================================

CSS = """
body {
    font-family: Georgia, "Times New Roman", serif;
    margin: 6%;
    line-height: 1.75;
    text-align: justify;
    color: #222222;
}

h1 {
    text-align: center;
    font-size: 1.65em;
    line-height: 1.35;
    margin-top: 2em;
    margin-bottom: 2em;
}

h2 {
    text-align: center;
    font-size: 1.3em;
    margin-top: 2em;
    margin-bottom: 1.5em;
}

p {
    margin-top: 0;
    margin-bottom: 0.9em;
    text-indent: 1.5em;
}

.title-page {
    text-align: center;
    margin-top: 30%;
}

.title-page h1 {
    font-size: 2.1em;
    margin-bottom: 0.7em;
}

.title-page .original-title {
    font-size: 1.4em;
    margin-top: 1em;
}

.title-page .alternate-title {
    font-size: 1em;
    margin-top: 1em;
}

.title-page .author {
    margin-top: 3em;
    font-size: 1em;
}

.toc-page {
    margin: 5%;
}

.toc-page h1 {
    margin-bottom: 2em;
}

.toc-page ol {
    padding-left: 2em;
}

.toc-page li {
    margin-bottom: 0.45em;
    line-height: 1.4;
}

.chapter-navigation {
    text-align: center;
    margin-top: 3em;
    padding-top: 1em;
    border-top: 1px solid #cccccc;
    font-size: 0.9em;
}

.chapter-navigation a {
    text-decoration: none;
}
"""


# ============================================================
# LOAD CHAPTERS
# ============================================================

def load_chapters():

    files = sorted(
        CHAPTERS_DIR.glob(
            "chapter_*.json"
        )
    )

    if not files:

        raise FileNotFoundError(
            "No chapter JSON files were found."
        )

    chapters = []

    for file in files:

        with open(
            file,
            "r",
            encoding="utf-8",
        ) as f:

            chapter = json.load(f)

        chapters.append(
            {
                "number": int(
                    chapter["number"]
                ),
                "title": chapter.get(
                    "title",
                    f"Chapter {chapter['number']}",
                ),
                "paragraphs": chapter.get(
                    "paragraphs",
                    [],
                ),
            }
        )

    chapters.sort(
        key=lambda x: x["number"]
    )

    return chapters


# ============================================================
# TITLE PAGE
# ============================================================

def create_title_page(book):

    page = epub.EpubHtml(
        title="Title Page",
        file_name="title.xhtml",
        lang="en",
    )

    page.content = f"""
    <html xmlns="http://www.w3.org/1999/xhtml">

    <head>
        <title>
            {escape(BOOK_TITLE)}
        </title>
    </head>

    <body>

        <div class="title-page">

            <h1>
                {escape(BOOK_TITLE)}
            </h1>

            <div class="original-title">
                {escape(ORIGINAL_TITLE)}
            </div>

            <div class="alternate-title">
                {escape(ALTERNATE_TITLE)}
            </div>

            <div class="author">
                By {escape(AUTHOR)}
            </div>

        </div>

    </body>

    </html>
    """

    book.add_item(page)

    return page


# ============================================================
# TABLE OF CONTENTS
# ============================================================

def create_toc_page(
    book,
    chapters,
):

    page = epub.EpubHtml(
        title="Table of Contents",
        file_name="toc.xhtml",
        lang="en",
    )

    html = """
    <html xmlns="http://www.w3.org/1999/xhtml">

    <head>
        <title>Table of Contents</title>
    </head>

    <body>

        <div class="toc-page">

            <h1>
                Table of Contents
            </h1>

            <ol>
    """

    for chapter in chapters:

        filename = (
            f"chapter_"
            f"{chapter['number']:03d}.xhtml"
        )

        html += f"""
                <li>
                    <a href="{filename}">
                        {escape(chapter['title'])}
                    </a>
                </li>
        """

    html += """
            </ol>

        </div>

    </body>

    </html>
    """

    page.content = html

    book.add_item(page)

    return page


# ============================================================
# CHAPTER PAGE
# ============================================================

def create_chapter_page(
    book,
    chapter,
    previous_chapter,
    next_chapter,
):

    number = chapter["number"]

    title = chapter["title"]

    paragraphs = chapter["paragraphs"]

    filename = (
        f"chapter_{number:03d}.xhtml"
    )

    page = epub.EpubHtml(
        title=title,
        file_name=filename,
        lang="en",
    )

    html = f"""
    <html xmlns="http://www.w3.org/1999/xhtml">

    <head>
        <title>
            {escape(title)}
        </title>
    </head>

    <body>

        <h1>
            {escape(title)}
        </h1>
    """

    # ========================================================
    # STORY PROSE
    # ========================================================

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        html += (
            "<p>"
            + escape(paragraph)
            + "</p>"
        )

    # ========================================================
    # CHAPTER NAVIGATION
    # ========================================================

    html += """
        <div class="chapter-navigation">
    """

    if previous_chapter:

        previous_filename = (
            f"chapter_"
            f"{previous_chapter['number']:03d}.xhtml"
        )

        html += f"""
            <a href="{previous_filename}">
                ← Previous Chapter
            </a>

            &nbsp;&nbsp;|&nbsp;&nbsp;
        """

    html += """
            <a href="toc.xhtml">
                Table of Contents
            </a>
    """

    if next_chapter:

        next_filename = (
            f"chapter_"
            f"{next_chapter['number']:03d}.xhtml"
        )

        html += f"""
            &nbsp;&nbsp;|&nbsp;&nbsp;

            <a href="{next_filename}">
                Next Chapter →
            </a>
        """

    html += """
        </div>

    </body>

    </html>
    """

    page.content = html

    book.add_item(page)

    return page


# ============================================================
# BUILD EPUB
# ============================================================

def build_epub():

    print()
    print("=" * 70)
    print(
        "BUILDING CONCUBINE DAUGHTER'S "
        "SURVIVAL MANUAL EPUB"
    )
    print("=" * 70)
    print()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    chapters = load_chapters()

    print(
        f"Loaded {len(chapters)} chapters."
    )

    if len(chapters) != TOTAL_CHAPTERS:

        raise RuntimeError(
            f"Expected {TOTAL_CHAPTERS} chapters, "
            f"but found {len(chapters)}."
        )

    # ========================================================
    # CREATE BOOK
    # ========================================================

    book = epub.EpubBook()

    book.set_identifier(
        "concubine-daughters-survival-manual"
    )

    book.set_title(
        BOOK_TITLE
    )

    book.set_language(
        "en"
    )

    book.add_author(
        AUTHOR
    )

    # ========================================================
    # CSS
    # ========================================================

    style = epub.EpubItem(
        uid="style",
        file_name="style/style.css",
        media_type="text/css",
        content=CSS.encode(
            "utf-8"
        ),
    )

    book.add_item(style)

    # ========================================================
    # TITLE PAGE
    # ========================================================

    title_page = create_title_page(
        book
    )

    title_page.add_link(
        href="style/style.css",
        rel="stylesheet",
        type="text/css",
    )

    # ========================================================
    # TOC PAGE
    # ========================================================

    toc_page = create_toc_page(
        book,
        chapters,
    )

    toc_page.add_link(
        href="style/style.css",
        rel="stylesheet",
        type="text/css",
    )

    # ========================================================
    # CHAPTERS
    # ========================================================

    epub_chapters = []

    for index, chapter in enumerate(
        chapters
    ):

        previous_chapter = (
            chapters[index - 1]
            if index > 0
            else None
        )

        next_chapter = (
            chapters[index + 1]
            if index < len(chapters) - 1
            else None
        )

        page = create_chapter_page(
            book=book,
            chapter=chapter,
            previous_chapter=previous_chapter,
            next_chapter=next_chapter,
        )

        page.add_link(
            href="style/style.css",
            rel="stylesheet",
            type="text/css",
        )

        epub_chapters.append(
            page
        )

        print(
            f"Added chapter "
            f"{chapter['number']:03d}: "
            f"{chapter['title']}"
        )

    # ========================================================
    # EPUB TOC
    # ========================================================

    book.toc = tuple(
        epub_chapters
    )

    # ========================================================
    # NAVIGATION
    # ========================================================

    book.add_item(
        epub.EpubNcx()
    )

    book.add_item(
        epub.EpubNav()
    )

    # ========================================================
    # READING ORDER
    # ========================================================

    book.spine = [
        "nav",
        title_page,
        toc_page,
        *epub_chapters,
    ]

    # ========================================================
    # WRITE EPUB
    # ========================================================

    print()
    print(
        "Writing EPUB..."
    )

    epub.write_epub(
        str(OUTPUT_FILE),
        book,
    )

    print()
    print("=" * 70)
    print(
        "✓ EPUB CREATED SUCCESSFULLY"
    )
    print("=" * 70)
    print()

    print(
        f"Output:\n{OUTPUT_FILE}"
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    build_epub()