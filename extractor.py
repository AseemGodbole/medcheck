import sys
import re
import pdfplumber
from pathlib import Path

# Usage: python extractor.py <path_to_pdf>


def extract_text_from_pdf(pdf_path):
    page_texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Use tolerances that generally improve table-like clinical reports.
            page_text = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
            page_texts.append(page_text)
    return "\n".join(page_texts)


def _is_noise_line(line):
    stripped = line.strip()
    if not stripped:
        return True

    # Remove common PDF artifact rows (long hex-like sequences).
    if re.fullmatch(r"[A-F0-9]{16,}", stripped):
        return True

    # Remove repeated barcode-like patterns dominated by A-F0-9 symbols.
    alnum = re.sub(r"[^A-Za-z0-9]", "", stripped)
    if len(alnum) >= 24 and re.fullmatch(r"[A-F0-9]+", alnum):
        return True

    # Lines that are mostly hex-like tokens are usually PDF drawing artifacts.
    tokens = stripped.split()
    if tokens:
        hex_like = sum(1 for t in tokens if re.fullmatch(r"[A-F0-9]{12,}", t))
        if hex_like / len(tokens) >= 0.5:
            return True

    return False


def _normalize_repeated_chars(line):
    # Fix OCR-ish repeated letters: TTTTeeeesssstttt -> Test (3+ repeats only)
    # Keeps legitimate double letters like "oo", "ll", "ff" and digits intact.
    line = re.sub(r"([A-Za-z])\1{2,}", r"\1", line)
    # Also collapse patterns like e e e e caused by extraction artifacts.
    line = re.sub(r"(?:\b([A-Za-z])\b\s+){2,}\b([A-Za-z])\b", r"\1\2", line)
    return line


def clean_extracted_text(text):
    cleaned_lines = []
    previous = None

    for raw_line in text.splitlines():
        line = raw_line.replace("\u00a0", " ").strip()

        # Remove long embedded hex artifacts even if mixed with real text.
        line = re.sub(r"\b[A-F0-9]{12,}\b", " ", line)

        line = _normalize_repeated_chars(line)
        line = re.sub(r"([:;,.()\-/#])\1{2,}", r"\1", line)
        line = re.sub(r"\s+", " ", line).strip()

        if _is_noise_line(line):
            continue

        # Skip immediate duplicate lines (very common in these reports).
        if previous and line.lower() == previous.lower():
            continue

        cleaned_lines.append(line)
        previous = line

    return "\n".join(cleaned_lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <path_to_pdf>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    if not Path(pdf_path).exists():
        print(f"File not found: {pdf_path}")
        sys.exit(1)
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_extracted_text(raw_text)

    if cleaned_text.strip():
        print("--- Cleaned Extracted Text ---\n")
        print(cleaned_text)

        base = Path(pdf_path).stem
        raw_out = Path(f"{base}_raw.txt")
        clean_out = Path(f"{base}_cleaned.txt")
        raw_out.write_text(raw_text, encoding="utf-8")
        clean_out.write_text(cleaned_text, encoding="utf-8")
        print(f"\nSaved raw text to: {raw_out}")
        print(f"Saved cleaned text to: {clean_out}")
    else:
        print("No usable text extracted after cleaning. PDF may be scanned/image-based; use OCR fallback.")


if __name__ == "__main__":
    main()
