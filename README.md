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
- **Printed → PDF page offset:**  
  Front matter often uses roman numerals; main text starts later in the PDF. In the script:
  - `pdf_index = printed_page + 23` handles the main-text offset (printed page 1 → PDF page 24). Change `23` to match your PDF.
  - Roman numeral pages use `roman_to_int` and subtract 3 to map printed xi → PDF 9. Adjust both offsets if your front matter is longer/shorter.
- **Contents parsing:**  
  `CONTENTS_PAGES = range(2, 8)` tells the script which pages contain the printed TOC. Update this range for your book.  
  If your contents lines wrap differently, tweak `clean_contents_lines` (merge logic) or expand the filters that drop watermark/legal boilerplate.
- **Outline levels:**  
  `parse_entries` assigns outline depth from numeric prefixes:
  - `1`, `2`, … → chapter level
  - `1.0`, `2.3`, … → section level 1
  - `1.2.3`, … → section level 2  
  Adjust the regex logic to match your book’s numbering scheme.
