#!/usr/bin/env python3
"""Render a poster HTML file to PNG (and optionally PDF).

Usage:
    python render_poster.py poster.html poster.png [--width 1080 --height 1350] [--pdf poster.pdf]

Backends, tried in order:
  1. Playwright + Chromium  (pip install playwright && playwright install chromium)
  2. WeasyPrint + PyMuPDF   (pip install weasyprint pymupdf)

Any browser screenshot at the poster size is equally fine; this script is a convenience.
Bengali and other Indic scripts need a real shaping engine: both backends above have one.
"""
import argparse
import sys
from pathlib import Path


def render_playwright(html: Path, png: Path, w: int, h: int, pdf: Path | None) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            page.goto(html.resolve().as_uri())
            page.wait_for_timeout(600)  # let web fonts settle
            page.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": w, "height": h})
            if pdf:
                page.pdf(path=str(pdf), width=f"{w}px", height=f"{h}px", print_background=True)
            browser.close()
        return True
    except Exception as exc:  # browser binary missing, etc.
        print(f"[render] Playwright unavailable ({exc}); trying WeasyPrint", file=sys.stderr)
        return False


def render_weasyprint(html: Path, png: Path, w: int, h: int, pdf: Path | None) -> bool:
    try:
        import weasyprint
        import pymupdf
    except ImportError:
        return False
    doc = weasyprint.HTML(filename=str(html)).render()
    pdf_bytes = doc.write_pdf()
    if pdf:
        pdf.write_bytes(pdf_bytes)
    pdf_doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    page = pdf_doc[0]
    zoom = w / page.rect.width
    page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False).save(str(png))
    if len(pdf_doc) > 1:
        print(f"[render] WARNING: content overflowed onto {len(pdf_doc)} pages; "
              "only page 1 was exported. Check sizes.", file=sys.stderr)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=Path)
    ap.add_argument("png", type=Path)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--pdf", type=Path, default=None)
    a = ap.parse_args()

    if not a.html.exists():
        print(f"[render] not found: {a.html}", file=sys.stderr)
        return 2
    a.png.parent.mkdir(parents=True, exist_ok=True)

    for fn in (render_playwright, render_weasyprint):
        if fn(a.html, a.png, a.width, a.height, a.pdf):
            print(f"[render] wrote {a.png} ({a.width}x{a.height})")
            return 0
    print("[render] No renderer found. Install one of:\n"
          "  pip install playwright && playwright install chromium\n"
          "  pip install weasyprint pymupdf\n"
          "or open the HTML in a browser and take a screenshot at the poster size.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
