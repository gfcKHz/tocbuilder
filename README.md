Lightweight helper that builds an outline/bookmarks for PDFs missing a table of contents. Configure the printed→PDF page offset and contents-page range to match your book.

## What’s here
- `add_toc.py` — reads a PDF, parses printed contents pages, and writes a new PDF with an outline.
- `.gitignore` — keeps PDFs and Python cache files out of the repo.

## Usage (Nix-friendly)
1. Enter a shell with `pypdf` (example using nix-shell):
   ```bash
   nix-shell -p 'python3.withPackages (ps: [ ps.pypdf ])'
   ```
   or any Python env where `pypdf` is installed.
2. Place your source PDF next to the script and set `SOURCE`/`OUTPUT` at the top of `add_toc.py`.
3. Run:
   ```bash
   python add_toc.py
   ```
   The script writes `book_with_toc.pdf` by default.

## Tweaking
- **Printed → PDF page offsets:**  
  Figure out how many PDF pages precede printed page 1 (e.g., title, copyright, roman-numeral pages). Edit `parse_entries`:
  - For main text, change the `printed_page + 23` value so printed page 1 points to the correct PDF page (0-based).
  - For roman numerals, change the `printed_page - 3` value so printed xi points to the correct PDF page. Both offsets are independent.
- **Contents pages:**  
  Set `CONTENTS_PAGES` to the 0-based PDF pages that contain the printed TOC. If the TOC spans multiple pages, use a range.
  If lines wrap oddly, adjust `clean_contents_lines` to merge them differently or relax/tighten the filters that drop boilerplate text.
- **Outline levels:**  
  `parse_entries` maps numbering to levels:
  - `1`, `2`, … → chapter
  - `1.0`, `2.3`, … → section
  - `1.2.3`, … → subsection  
  Change the regex checks if your book uses a different numbering style.
