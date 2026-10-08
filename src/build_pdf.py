from pathlib import Path
import json

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    PageBreak,
)


# ============================================================
# PATHS
# ============================================================

ROOT = Path(file).resolve().parent.parent

CHAPTERS_DIR = (
    ROOT / "data" / "chapters"
)

OUTPUT_DIR = (
    ROOT / "output"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "Concubine_Daughters_Survival_Manual.pdf"
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

AUTHOR = (
    "Yu Jing Peng Xiang"
)

TOTAL_CHAPTERS = 303


# ============================================================
# LOAD CHAPTERS
# ============================================================

def load_chapters():

    files = sorted(
        CHAPTERS_DIR.glob(
            "chapter_*.json"
        )
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
                "title": chapter["title"],
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
# DOCUMENT
# ============================================================

class NovelDocument(
    BaseDocTemplate
):

    def init(
        self,
        filename,
        **kwargs,
    ):

        super().init(
            filename,
            **kwargs,
        )

        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="normal",
        )

        template = PageTemplate(
            id="novel",
            frames=frame,
        )

        self.addPageTemplates(
            [template]
        )


# ============================================================
# BUILD PDF
# ============================================================

def build_pdf():

    print()
    print("=" * 70)
    print(
        "BUILDING CONCUBINE DAUGHTER'S "
        "SURVIVAL MANUAL PDF"
    )
    print("=" * 70)
    print()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    chapters = load_chapters()

    if len(chapters) != TOTAL_CHAPTERS:

        raise RuntimeError(
            f"Expected {TOTAL_CHAPTERS} chapters, "
            f"but found {len(chapters)}."
        )

    print(
        f"Loaded {len(chapters)} chapters."
    )

    # ========================================================
    # DOCUMENT
    # ========================================================

    doc = NovelDocument(
        str(OUTPUT_FILE),
        pagesize=A5,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=BOOK_TITLE,
        author=AUTHOR,
    )

    # ========================================================
    # STYLES
    # ========================================================

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "BookTitle",
        parent=styles["Title"],
        fontName="Times-Roman",
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        spaceAfter=18,
    )

    original_title_style = ParagraphStyle(
        "OriginalTitle",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=15,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=25,
    )

    author_style = ParagraphStyle(
        "Author",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
    )

    toc_heading_style = ParagraphStyle(
        "TOCHeading",
        parent=styles["Heading1"],
        fontName="Times-Bold",
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=15,
    )

    toc_entry_style = ParagraphStyle(
        "TOCEntry",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11,
        leftIndent=8,
        spaceAfter=2,
    )

    chapter_heading_style = ParagraphStyle(
        "ChapterHeading",
        parent=styles["Heading1"],
        fontName="Times-Bold",
        fontSize=16,
        leading=21,
        alignment=TA_CENTER,
        spaceAfter=20,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Times-Roman",
        fontSize=10.5,
        leading=16,
        alignment=TA_JUSTIFY,
        firstLineIndent=12,
        spaceAfter=7,
    )

    # ========================================================
    # STORY
    # ========================================================

    story = []

    # ========================================================
    # TITLE PAGE
    # ========================================================

    story.append(
        Spacer(
            1,
            55 * mm,
        )
    )

    story.append(
        Paragraph(
            BOOK_TITLE,
            title_style,
        )
    )

    story.append(
        Paragraph(
            ORIGINAL_TITLE,
            original_title_style,
        )
    )

    story.append(
        Paragraph(
            f"By {AUTHOR}",
            author_style,
        )
    )

    story.append(
        PageBreak()
    )

    # ========================================================
    # TABLE OF CONTENTS
    # ========================================================

    story.append(
        Paragraph(
            "Table of Contents",
            toc_heading_style,
        )
    )

    for chapter in chapters:

        story.append(
            Paragraph(
                (
                    f"{chapter['number']}. "
                    f"{chapter['title']}"
                ),
                toc_entry_style,
            )
        )

    story.append(
        PageBreak()
    )

    # ========================================================
    # CHAPTERS
    # ========================================================

    for chapter in chapters:

        number = chapter["number"]

        title = chapter["title"]

        paragraphs = chapter["paragraphs"]

        print(
            f"Adding chapter "
            f"{number:03d}: {title}"
        )

        # ----------------------------------------------------
        # Chapter heading
        # ----------------------------------------------------

        story.append(
            Paragraph(
                title,
                chapter_heading_style,
            )
        )

        # ----------------------------------------------------
        # Story paragraphs
        # ----------------------------------------------------

        for paragraph in paragraphs:

            # Escape characters that ReportLab interprets
            # as markup.

            paragraph = (
                paragraph
                .replace(
                    "&",
                    "&amp;",
                )
                .replace(
                    "<",
                    "&lt;",
                )
                .replace(
                    ">",
                    "&gt;",
                )
            )
            
            story.append(
                Paragraph(
                    paragraph,
                    body_style,
                )
            )

        # ----------------------------------------------------
        # New page for every chapter
        # ----------------------------------------------------

        story.append(
            PageBreak()
        )

    # ========================================================
    # WRITE PDF
    # ========================================================

    print()
    print(
        "Writing PDF..."
    )

    doc.build(
        story
    )

    print()
    print("=" * 70)
    print(
        "✓ PDF CREATED SUCCESSFULLY"
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

if name == "main":
    build_pdf()