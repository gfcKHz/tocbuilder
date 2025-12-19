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
Need different offsets or parsing rules? Open the project in Codex and adjust `add_toc.py` to match your book’s TOC pages and numbering.
