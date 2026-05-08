#!/usr/bin/env python3
"""
Screenshot HTML files using Playwright.
Usage: python screenshot.py <images-directory>

Scans the directory for all .html files and screenshots each one.
Screenshot dimensions are read from the HTML body's computed width/height,
so each HTML file controls its own size via CSS.

Example HTML sizing:
  body { width: 800px; height: 600px; }   /* 4:3 ratio */
  body { width: 800px; height: 800px; }   /* 1:1 square */
  body { width: 1260px; height: 540px; }  /* 21:9 cover */
"""

import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: python screenshot.py <images-directory>")
        sys.exit(1)

    images_dir = Path(sys.argv[1]).resolve()
    if not images_dir.exists():
        print(f"Directory not found: {images_dir}")
        sys.exit(1)

    html_files = sorted(images_dir.glob("*.html"))
    if not html_files:
        print("No .html files found")
        sys.exit(0)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Install with: pip install playwright && playwright install chromium")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for html_path in html_files:
            png_path = html_path.with_suffix(".png")

            page = browser.new_page()
            page.goto(f"file://{html_path}")
            page.wait_for_timeout(1500)

            # Read body dimensions from the HTML itself
            size = page.evaluate("""() => {
                const body = document.body;
                return {
                    width: body.scrollWidth,
                    height: body.scrollHeight
                };
            }""")

            page.set_viewport_size({"width": size["width"], "height": size["height"]})
            page.wait_for_timeout(200)
            page.screenshot(path=str(png_path), full_page=False)
            print(f"  {png_path.name} ({size['width']}x{size['height']})")

        browser.close()

    print("Done!")


if __name__ == "__main__":
    main()
