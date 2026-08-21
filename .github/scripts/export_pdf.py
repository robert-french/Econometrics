"""
Export a marimo notebook to a static PDF.

Trial implementation backing the "Download PDF" button (currently Lecture 1
only; see PDF_EXPORT_STEMS in build.py). Two steps:

    1. `marimo export html` runs the notebook natively and writes a static
       HTML snapshot with every output embedded, code hidden to match the
       deployed app view.
    2. Playwright drives an already-installed Chromium-based browser (Chrome
       on the CI runners, Edge on a default Windows install; no browser
       download needed), waits for the page to actually render, and prints
       it to PDF.

The snapshot pulls marimo's JS bundle from a CDN and renders the Vega charts
at load time, so the browser needs network access. Playwright replaced a
plain `--headless --print-to-pdf` invocation, which raced the render and
intermittently produced a blank one-page PDF; waiting on network idle plus a
rendered heading makes the capture deterministic.

One more hard-won detail: the marimo app scrolls inside a fixed-height
container, so an unmodified print captures only the first viewport.
_PRINT_CSS is injected into the snapshot to let the content flow across
pages; it also hides UI chrome (buttons, site-navigation links) and sets the
page margins.
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "loguru==0.7.0",
#     "playwright>=1.55"
# ]
# ///

import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional

from loguru import logger
from playwright.sync_api import sync_playwright

# Playwright "channels" name browsers already installed on the machine,
# tried in order. The empty string falls back to a Playwright-managed
# chromium, present only if `playwright install chromium` was run.
_BROWSER_CHANNELS = ("chrome", "msedge", "")

_PRINT_ATTEMPTS = 3

# The app body lives in a fixed-height scrolling container; without the
# height/overflow rules the print captures a single cut-off page. Buttons
# (the sidebar hamburger, chart menus) are chrome, not content, so they are
# hidden, as are the site-navigation rows (Course home / next lecture /
# Download PDF): those links all point at the deployed site, while in-page
# Contents links are #fragments, so the href prefix selects exactly the nav
# links. The :has() variant removes the whole nav row so no empty gap is
# left behind.
_PRINT_CSS = """
<style media="print">
  /* Vertical margins enlarged; horizontal kept near Chromium's ~10mm
     default because the fixed-width charts clip against anything
     narrower. */
  @page { margin: 25mm 10mm; }
  html, body, #root { height: auto !important; overflow: visible !important; }
  #root > * { height: auto !important; overflow: visible !important; }
  * { overflow: visible !important; }
  button { display: none !important; }
  a[href^="https://robert-french.github.io/Econometrics"] { display: none !important; }
  div:has(> a[href^="https://robert-french.github.io/Econometrics"]) { display: none !important; }
  span.nav-soon { display: none !important; }
</style>
"""


def _export_static_html(notebook_path: Path, html_file: Path) -> bool:
    """Run the notebook natively and write a static HTML snapshot."""
    cmd: List[str] = [
        "uvx",
        "marimo",
        "export",
        "html",
        "--sandbox",
        "--no-include-code",
        str(notebook_path.resolve()),
        "-o",
        str(html_file.resolve()),
    ]
    logger.info(f"Exporting {notebook_path} to static HTML for PDF capture")
    try:
        # cwd matters for the same reason as in build.py: marimo resolves
        # `css_file=` against the notebook's directory.
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd=notebook_path.resolve().parent,
        )
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"marimo export html failed for {notebook_path}:")
        logger.error(f"Command output: {e.stderr}")
        return False


def _print_to_pdf(html_file: Path, output_pdf: Path) -> bool:
    """Render a local HTML file in a headless browser and print it to PDF."""
    logger.info(f"Printing {html_file.name} to {output_pdf}")
    with sync_playwright() as p:
        browser = None
        for channel in _BROWSER_CHANNELS:
            try:
                browser = p.chromium.launch(channel=channel or None)
                break
            except Exception:
                continue
        if browser is None:
            logger.error(
                "No Chromium-based browser found for PDF export (tried "
                f"channels {_BROWSER_CHANNELS})"
            )
            return False
        try:
            page = browser.new_page()
            page.goto(
                html_file.resolve().as_uri(),
                wait_until="networkidle",
                timeout=120_000,
            )
            # networkidle alone can fire before marimo has painted; wait for
            # real content, then give the Vega charts a moment to finish.
            page.wait_for_selector("h1", timeout=60_000)
            page.wait_for_timeout(2_000)
            page.pdf(path=str(output_pdf.resolve()), print_background=True)
        except Exception as e:
            logger.error(f"Headless print failed for {html_file}: {e}")
            return False
        finally:
            browser.close()
    return output_pdf.is_file()


def export_notebook_pdf(notebook_path: Path, output_pdf: Path) -> bool:
    """Export one marimo notebook to a PDF at output_pdf."""
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        html_file = Path(tmp) / f"{notebook_path.stem}.html"
        if not _export_static_html(notebook_path, html_file):
            return False
        html = html_file.read_text(encoding="utf-8")
        html_file.write_text(
            html.replace("</head>", f"{_PRINT_CSS}</head>", 1), encoding="utf-8"
        )
        # A cold browser launch with an empty cache can occasionally lose the
        # race against the CDN and time out before the page renders; a fresh
        # attempt almost always succeeds.
        for attempt in range(1, _PRINT_ATTEMPTS + 1):
            if _print_to_pdf(html_file, output_pdf):
                break
            logger.warning(
                f"Print attempt {attempt}/{_PRINT_ATTEMPTS} failed for "
                f"{notebook_path.name}"
            )
        else:
            logger.error(f"All print attempts failed for {notebook_path.name}")
            return False

    logger.info(f"Successfully exported {output_pdf}")
    return True


if __name__ == "__main__":
    # Standalone use: uv run .github/scripts/export_pdf.py <notebook.py> <out.pdf>
    import sys

    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: export_pdf.py <notebook.py> <output.pdf>"
        )
    ok = export_notebook_pdf(Path(sys.argv[1]), Path(sys.argv[2]))
    raise SystemExit(0 if ok else 1)

