# nr: add a TOC to PDFs

Lightweight helper that builds an outline/bookmarks for PDFs missing a table of contents. Designed around *Numerical Recipes in C* but easy to tweak for other books by adjusting the printed→PDF page offset and the content parsing rules.

## What’s here
- `add_toc.py` — reads a PDF, parses its printed contents pages, and writes a new PDF with an outline.
- `.gitignore` — keeps large PDFs out of the repo.

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
   The script writes `NumericalRecipesinC_with_toc.pdf` by default.

## Tweaking for other PDFs
- **Printed → PDF page offset:**  
  Front matter often uses roman numerals and starts before PDF page 1. In the script:
  - `pdf_index = printed_page + 23` handles the main-text offset (printed page 1 → PDF page 24). Change `23` if your PDF page numbering differs.
  - Roman numeral pages use `roman_to_int` and subtract 3 to map printed xi → PDF 9. Adjust if your front matter is longer/shorter.
- **Contents parsing:**  
  `CONTENTS_PAGES = range(2, 8)` tells the script which pages contain the printed TOC. Update this range for your book.  
  If your contents lines wrap differently, tweak `clean_contents_lines` (the merge step) or expand the filters that drop watermark/legal boilerplate.
- **Outline levels:**  
  `parse_entries` assigns outline depth from numeric prefixes:
  - `1`, `2`, … → chapter level
  - `1.0`, `2.3`, … → section level 1
  - `1.2.3`, … → section level 2  
  Adjust the regex logic to match your book’s numbering scheme.

## Publishing as `nr`
This directory is ready to initialize as a git repo and push:
```bash
git init
git add README.md add_toc.py .gitignore
git commit -m \"Add TOC helper script\"
git remote add origin git@github.com:<your-username>/nr.git
git push -u origin main
```
Note: do **not** commit copyrighted PDFs. Keep them local and out of version control.
