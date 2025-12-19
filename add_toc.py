import re
from typing import List, Tuple

from pypdf import PdfReader, PdfWriter

# Input/output filenames (adjust as needed).
SOURCE = "book.pdf"
OUTPUT = "book_with_toc.pdf"
# Pages (0-based) that contain the printed table of contents.
CONTENTS_PAGES = range(2, 8)


def roman_to_int(s: str) -> int:
    values = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}
    total = 0
    prev = 0
    for ch in reversed(s.lower()):
        val = values[ch]
        if val < prev:
            total -= val
        else:
            total += val
            prev = val
    return total


def clean_contents_lines(reader: PdfReader) -> List[str]:
    raw = "\n".join(reader.pages[i].extract_text() or "" for i in CONTENTS_PAGES)
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        lower = line.lower()
        if lower.startswith("sample page from") or lower.startswith("copyright"):
            continue
        if lower.startswith("permission is granted") or lower.startswith("http://"):
            continue
        if "further reproduction" in lower or "readable files" in lower:
            continue
        if lower.startswith("nr.com") or "nr.com" in lower:
            continue
        if lower.endswith("allowed") or "prohibited" in lower:
            continue
        if line in {"Contents", "v", "vi Contents", "Contents vii", "Contents ix", "x Contents"}:
            continue
        lines.append(line)
    merged: List[str] = []
    buffer = ""
    page_re = re.compile(r"\b([0-9]+|[ivxlcdmIVXLCDM]+)$")
    for line in lines:
        if buffer:
            buffer += " " + line
        else:
            buffer = line
        if page_re.search(buffer):
            merged.append(buffer)
            buffer = ""
    if buffer:
        merged.append(buffer)
    return merged


def parse_entries(lines: List[str]) -> List[Tuple[str, int, int, bool]]:
    entries: List[Tuple[str, int, int, bool]] = []
    for line in lines:
        m = re.match(r"(.+?)\s+([0-9ivxlcdmIVXLCDM]+)$", line)
        if not m:
            continue
        title = m.group(1).strip()
        page_str = m.group(2)
        is_roman = page_str.isalpha()
        if is_roman:
            printed_page = roman_to_int(page_str)
            pdf_index = printed_page - 3  # printed xi (11) -> pdf 9 (0-based)
        else:
            printed_page = int(page_str)
            pdf_index = printed_page + 23  # printed 1 -> pdf 24 (0-based)
        # Determine outline level from numeric prefix.
        level = 0
        prefix = title.split()[0]
        if re.match(r"^\d+\.\d+$", prefix):
            level = 1
        elif re.match(r"^\d+\.\d+\.\d+$", prefix):
            level = 2
        elif re.match(r"^\d+$", prefix):
            level = 0
        else:
            level = 0
        entries.append((title, pdf_index, level, is_roman))
    return entries


def build_outline():
    reader = PdfReader(SOURCE)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)

    lines = clean_contents_lines(reader)
    entries = parse_entries(lines)

    parents = {}
    for title, pdf_index, level, _ in entries:
        if pdf_index < 0 or pdf_index >= len(writer.pages):
            continue
        parent = parents.get(level - 1) if level > 0 else None
        item = writer.add_outline_item(title, pdf_index, parent=parent)
        parents[level] = item
        for k in list(parents.keys()):
            if k > level:
                parents.pop(k, None)

    with open(OUTPUT, "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    build_outline()
