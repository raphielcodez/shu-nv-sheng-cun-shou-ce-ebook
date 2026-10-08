# Concubine Daughter's Survival Manual — Web Scraping & EPUB Generation

A Python-based web scraping and ebook-generation project for **Concubine Daughter's Survival Manual (庶女生存手册 / Shu Nv Sheng Cun Shou Ce)** by **Yu Jing Peng Xiang**.

The project demonstrates how to discover chapter URLs from a novel series page, extract and clean chapter content, validate the resulting dataset, and transform the structured chapter data into a properly formatted EPUB and PDF ebook with a table of contents.

> **Important:** This repository is intended primarily as a technical/data portfolio project. The novel's text is copyrighted. The repository should not contain or redistribute the full scraped novel text or generated ebook unless you have the necessary rights or permission.

---

## Project Overview

This project was created to demonstrate a complete data-processing pipeline:

```text
Public Web Page
      │
      ▼
Chapter Discovery
      │
      ▼
Chapter URL Dataset
      │
      ▼
Web Scraping
      │
      ▼
HTML Cleaning & Text Extraction
      │
      ▼
Individual Chapter JSON Files
      │
      ▼
Data Validation
      │
      ├───────────────┐
      ▼               ▼
    EPUB             PDF
      │               │
      ▼               ▼
Formatted Ebook   Formatted Ebook
```

The scraper is designed to keep every chapter separate rather than combining the entire novel into one large text file.

---

## Novel Information

| Field | Details |
| --- | --- |
| English Title | Concubine Daughter's Survival Manual |
| Original Title | 庶女生存手册 |
| Romanized Title | Shu Nv Sheng Cun Shou Ce |
| Author | Yu Jing Peng Xiang |
| Chapters | 303 |
| Source Website | MyDramaNovel |
| Programming Language | Python |
| Output Formats | EPUB, PDF |
| Data Format | JSON |

The source series page currently contains 303 chapters.

---

## Features

### Chapter Discovery

Automatically identifies chapter links from the novel's series page and creates a structured chapter index.

Example:

```json
[
    {
        "number": 1,
        "title": "Chapter 1: The Visit",
        "url": "..."
    },
    {
        "number": 2,
        "title": "Chapter 2: The Main Courtyard",
        "url": "..."
    }
]
```

### Web Scraping

The scraper downloads individual chapter pages and extracts the actual chapter content.

It attempts to remove unnecessary website elements such as:

- Navigation menus
- Previous/next chapter links
- Comment sections
- Social sharing elements
- Advertisements
- Related posts
- Subscription prompts
- Images
- Embedded media
- Website footer content
- Sidebar content
- Scripts and styles

The scraper prioritizes paragraph-level extraction so that the novel's prose remains separated into readable paragraphs.

### Individual Chapter Storage

Each chapter is stored separately:

```text
data/
└── chapters/
    ├── chapter_001.json
    ├── chapter_002.json
    ├── chapter_003.json
    ├── ...
    └── chapter_303.json
```

Example structure:

```json
{
    "number": 1,
    "title": "Chapter 1: The Visit",
    "paragraphs": [
        "Chapter paragraph one...",
        "Chapter paragraph two...",
        "Chapter paragraph three..."
    ]
}
```

This makes the dataset easier to validate, process, analyze, and convert into different formats.

---

## Data Validation

Before creating the ebook, the project validates the scraped dataset.

The validation process checks for:

- Missing chapters
- Empty chapter files
- Invalid JSON
- Chapters with insufficient content
- Incorrect chapter numbering

The expected result is:

```text
Expected chapters: 303
Missing:           0
Empty:             0
Invalid JSON:      0
Too short:         0

======================================================================
✓ ALL 303 CHAPTER FILES ARE VALID
======================================================================
```

---

## EPUB Generation

The EPUB builder converts the structured JSON dataset into a properly formatted ebook.

The generated EPUB includes:

- Title page
- Author information
- Original title
- Table of contents
- Separate XHTML document for every chapter
- Chapter headings
- Paragraph formatting
- Page navigation
- EPUB navigation metadata
- CSS styling

Each chapter is treated as an independent ebook document rather than being appended into one large page.

---

## PDF Generation

The project also includes a PDF generation pipeline.

The PDF contains:

- Title page
- Book information
- Table of contents
- Separate chapter sections
- Chapter headings
- Proper paragraph spacing
- Page breaks between chapters
- A5 book-style page dimensions

---

# Project Structure

```text
shu-nv-sheng-cun-shou-ce-ebook/
│
├── data/
│   ├── chapters.json
│   │
│   └── chapters/
│       ├── chapter_001.json
│       ├── chapter_002.json
│       ├── chapter_003.json
│       └── ...
│
├── output/
│   ├── Concubine_Daughters_Survival_Manual.epub
│   └── Concubine_Daughters_Survival_Manual.pdf
│
├── src/
│   ├── discover_chapters.py
│   ├── scrape_chapters.py
│   ├── validate_chapters.py
│   ├── build_epub.py
│   └── build_pdf.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

For a public GitHub repository, the recommended version is slightly different:

```text
shu-nv-sheng-cun-shou-ce-ebook/
│
├── data/
│   └── sample/
│
├── src/
│   ├── discover_chapters.py
│   ├── scrape_chapters.py
│   ├── validate_chapters.py
│   ├── build_epub.py
│   └── build_pdf.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

The full scraped novel dataset and generated ebook files should normally remain outside the public repository unless you have permission to redistribute them.

---

# Technologies Used

- **Python** — project programming language
- **Requests** — HTTP requests
- **BeautifulSoup** — HTML parsing and content extraction
- **lxml** — HTML/XML processing
- **EbookLib** — EPUB generation
- **ReportLab** — PDF generation

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/shu-nv-sheng-cun-shou-ce-ebook.git
```

Move into the project:

```bash
cd shu-nv-sheng-cun-shou-ce-ebook
```

## 2. Create a virtual environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

# Requirements

```text
requests
beautifulsoup4
lxml
ebooklib
reportlab
```

---

# Running the Project

The recommended workflow is:

```text
1. Discover chapters
        ↓
2. Test scraping on one chapter
        ↓
3. Scrape all chapters
        ↓
4. Validate the dataset
        ↓
5. Build EPUB
        ↓
6. Build PDF
```

## Step 1 — Discover Chapters

Run:

```powershell
python src\discover_chapters.py
```

The script creates:

```text
data/chapters.json
```

Expected output:

```text
Expected chapters: 303
Found chapters:    303
Missing chapters:  0

✓ All 303 chapters were discovered.
```

## Step 2 — Test the Scraper

The scraper is initially configured to process only the first chapter.

Run:

```powershell
python src\scrape_chapters.py
```

Then inspect:

```text
data/chapters/chapter_001.json
```

This step is important because it allows the HTML extraction rules to be verified before downloading all 303 chapters.

## Step 3 — Scrape All Chapters

Once Chapter 1 has been verified and the extracted content is clean, change the test setting in:

```text
src/scrape_chapters.py
```

from:

```python
chapters = chapters[:1]
```

to:

```python
chapters = chapters
```

Then run:

```powershell
python src\scrape_chapters.py
```

The resulting files will be:

```text
data/chapters/
├── chapter_001.json
├── chapter_002.json
├── ...
└── chapter_303.json
```

## Step 4 — Validate the Dataset

Run:

```powershell
python src\validate_chapters.py
```

The validator should report:

```text
Expected chapters: 303
Missing:           0
Empty:             0
Invalid JSON:      0
Too short:         0
```

Only proceed to ebook generation after validation succeeds.

## Step 5 — Build the EPUB

Run:

```powershell
python src\build_epub.py
```

The resulting file will be:

```text
output/Concubine_Daughters_Survival_Manual.epub
```

The EPUB contains separate chapter files and a table of contents.

## Step 6 — Build the PDF

Run:

```powershell
python src\build_pdf.py
```

The resulting PDF will be:

```text
output/Concubine_Daughters_Survival_Manual.pdf
```

---

# Data Pipeline

```text
MyDramaNovel Series Page
          │
          ▼
discover_chapters.py
          │
          ▼
data/chapters.json
          │
          ▼
scrape_chapters.py
          │
          ▼
Individual Chapter JSON
          │
          ▼
validate_chapters.py
          │
          ├───────────────┐
          ▼               ▼
 build_epub.py       build_pdf.py
          │               │
          ▼               ▼
       EPUB             PDF
```

---

# Why Store Chapters as JSON?

JSON provides a structured intermediate format between the website and the final ebook.

Instead of:

```text
Entire Novel → EPUB
```

the project uses:

```text
Website
   ↓
HTML
   ↓
Clean structured data
   ↓
JSON
   ↓
EPUB/PDF
```

This makes it possible to:

- Validate the data
- Detect missing chapters
- Rebuild the ebook without scraping again
- Analyze chapter lengths
- Search chapter metadata
- Modify formatting independently
- Generate multiple output formats
- Reuse the structured data for legitimate analytical purposes

---

# Possible Data Analysis Extensions

Because every chapter is stored as structured data, the project can be extended into a larger data-analysis portfolio project.

Potential analyses include:

- Characters per chapter
- Words per chapter
- Paragraphs per chapter
- Average chapter length
- Longest chapter
- Shortest chapter
- Total word count
- Median words per chapter
- Average paragraph length
- Chapter length distribution

A future dashboard could visualize chapter length across all 303 chapters.

---

# Example Portfolio Questions

This project can demonstrate answers to questions such as:

- How can Python automatically discover URLs from a website?
- How can HTML be converted into structured data?
- How can unwanted website elements be removed?
- How can scraped data be validated?
- How can a large text collection be stored as JSON?
- How can structured data be transformed into an EPUB?
- How can an automated data pipeline be designed?
- How can scraping errors be detected before downstream processing?

---

# Error Handling

Potential scraping problems include:

- Missing chapters
- Changed website HTML
- Empty pages
- Duplicate paragraphs
- Navigation text appearing in chapter content
- Website redesigns
- Network failures
- Invalid JSON output

If the website changes its HTML structure, the CSS selectors in:

```text
src/scrape_chapters.py
```

may need to be updated.

---

# Responsible Use

This project is designed as a technical demonstration of:

- Web scraping
- Data cleaning
- Data validation
- JSON data processing
- Document generation
- Automation
- Python programming

The source website and novel remain the property of their respective owners.

Do not use this project to:

- Circumvent paywalls
- Bypass authentication
- Defeat CAPTCHAs
- Circumvent technical access controls
- Republish copyrighted material without permission
- Sell or redistribute copyrighted content without authorization

Use scraping responsibly and respect website terms, copyright law, and reasonable request rates.

---

# Future Improvements

- [ ] Automatic retry handling
- [ ] Request logging
- [ ] Scraping progress bar
- [ ] Configurable request delays
- [ ] Better chapter URL detection
- [ ] Automatic detection of changed HTML structure
- [ ] Word-count analysis
- [ ] Chapter-length visualization
- [ ] Automated data-quality report
- [ ] Clickable PDF table of contents
- [ ] EPUB metadata improvements
- [ ] Cover image generation
- [ ] Automated tests
- [ ] GitHub Actions pipeline
- [ ] Docker support
- [ ] Streamlit dashboard for chapter statistics

---

# Author

**Raphiel**

This project was created as part of a Python/data portfolio demonstrating practical skills in:

- Web scraping
- Data cleaning
- Data validation
- JSON
- Automation
- Document generation
- Python development
- Git
- GitHub

---

# License

The source code for this project can be released under the MIT License if desired.

The MIT License applies to the **original code written for this project**, not to the copyrighted novel content obtained from external sources.

Novel text, translations, characters, and other copyrighted material remain subject to their respective rights holders.

---

## Disclaimer

This project is provided for educational and portfolio purposes.

The scraper is intended for publicly accessible web content and should be used responsibly. Users are responsible for complying with applicable laws, website terms of service, and copyright requirements.
