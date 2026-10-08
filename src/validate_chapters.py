from pathlib import Path
import json


# ============================================================
# SETTINGS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

CHAPTERS_DIR = (
    ROOT / "data" / "chapters"
)

EXPECTED_CHAPTERS = 303

MINIMUM_TEXT_LENGTH = 100


# ============================================================
# VALIDATE
# ============================================================

def validate_chapters():

    print()
    print("=" * 70)
    print(
        "VALIDATING CHAPTER FILES"
    )
    print("=" * 70)
    print()

    missing = []
    empty = []
    invalid = []
    too_short = []

    # ========================================================
    # Check every expected chapter
    # ========================================================

    for number in range(
        1,
        EXPECTED_CHAPTERS + 1,
    ):

        file_path = (
            CHAPTERS_DIR
            / f"chapter_{number:03d}.json"
        )

        if not file_path.exists():

            missing.append(
                number
            )

            continue

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8",
            ) as f:

                chapter = json.load(f)

        except Exception:

            invalid.append(
                number
            )

            continue

        paragraphs = chapter.get(
            "paragraphs",
            [],
        )

        if not paragraphs:

            empty.append(
                number
            )

            continue

        text = "\n".join(
            paragraphs
        )

        if len(text) < MINIMUM_TEXT_LENGTH:

            too_short.append(
                number
            )

    # ========================================================
    # Report
    # ========================================================

    print(
        f"Expected chapters: {EXPECTED_CHAPTERS}"
    )

    print(
        f"Missing:           {len(missing)}"
    )

    print(
        f"Empty:             {len(empty)}"
    )

    print(
        f"Invalid JSON:      {len(invalid)}"
    )

    print(
        f"Too short:         {len(too_short)}"
    )

    # ========================================================
    # Details
    # ========================================================

    if missing:

        print()
        print(
            "Missing chapters:"
        )

        print(missing)

    if empty:

        print()
        print(
            "Empty chapters:"
        )

        print(empty)

    if invalid:

        print()
        print(
            "Invalid JSON:"
        )

        print(invalid)

    if too_short:

        print()
        print(
            "Very short chapters:"
        )

        print(too_short)

    # ========================================================
    # Final status
    # ========================================================

    if not (
        missing
        or empty
        or invalid
        or too_short
    ):

        print()
        print("=" * 70)
        print(
            "✓ ALL 303 CHAPTER FILES ARE VALID"
        )
        print("=" * 70)

    else:

        print()
        print("=" * 70)
        print(
            "⚠ VALIDATION FOUND PROBLEMS"
        )
        print("=" * 70)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    validate_chapters()