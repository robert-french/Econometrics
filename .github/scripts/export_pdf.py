"""
Export a marimo notebook to a static PDF.

Trial implementation backing the "Download PDF" button (currently Lecture 1
only; see PDF_EXPORT_STEMS in build.py). Two steps:

    1. `marimo export html` runs the notebook natively and writes a static
       HTML snapshot with every output embedded, code hidden to match the
       deployed app view.
    2. A headless Chromium browser prints that snapshot to PDF. GitHub's
       ubuntu runners ship Google Chrome; Windows ships Edge, so no extra
       dependency is needed on either.

The snapshot pulls marimo's JS bundle and renders the Vega charts at print
time, so the browser needs network access and a rendering budget
(--virtual-time-budget) before the PDF is captured.

Three hard-won details (found by trial on Windows/Edge):
  * The marimo app scrolls inside a fixed-height container, so a plain print
    captures only the first viewport. _PRINT_CSS is injected into the
    snapshot to let the content flow across pages.
  * Old-style `--headless` printed before the JS rendered (blank one-page
    PDF); `--headless=new` with a throwaway --user-data-dir waits correctly.
  * On Windows, the initial msedge.exe is a launcher that detaches and exits
    in ~0.1s while the real browser keeps rendering, so waiting on the
    spawned process is not enough (the PDF would be missing or blank). After
    the launcher exits we poll until no process is running with our unique
    --user-data-dir on its command line. Chrome on the Linux CI runners does
    not detach, so the poll returns immediately there.
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "loguru==0.7.0",
#     "psutil==7.0.0"
# ]
# ///

import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import List, Optional

import psutil
from loguru import logger

# Checked in order: names resolved on PATH first, then well-known install
# locations (Chrome on the CI runners, Edge on a default Windows install).
_BROWSER_CANDIDATES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium-browser",
    "chromium",
    "msedge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
)


# The app body lives in a fixed-height scrolling container; without these
# rules the print captures a single cut-off page. Buttons (the sidebar
# hamburger, chart menus) are chrome, not content, so they are hidden.
_PRINT_CSS = """
<style media="print">
  html, body, #root { height: auto !important; overflow: visible !important; }
  #root > * { height: auto !important; overflow: visible !important; }
  * { overflow: visible !important; }
  button { display: none !important; }
</style>
"""


def _find_browser() -> Optional[str]:
    """Return the path of an installed Chromium-based browser, if any."""
    for candidate in _BROWSER_CANDIDATES:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
        if Path(candidate).is_file():
            return candidate
    return None


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


def _wait_for_profile_processes(profile_token: str, timeout: float) -> bool:
    """Block until no process has profile_token on its command line.

    The token is this run's unique --user-data-dir path, so this waits out a
    browser that detached from the process we spawned. Returns False on
    timeout.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        alive = False
        for proc in psutil.process_iter(["cmdline"]):
            cmdline = proc.info.get("cmdline") or []
            if any(profile_token in arg for arg in cmdline):
                alive = True
                break
        if not alive:
            return True
        time.sleep(0.5)
    return False


def _print_to_pdf(
    html_file: Path, output_pdf: Path, browser: str, profile_dir: Path
) -> bool:
    """Print a local HTML file to PDF with a headless Chromium browser."""
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        f"--user-data-dir={profile_dir}",
        "--no-pdf-header-footer",
        # Fast-forward timers so the marimo bundle and Vega charts finish
        # rendering before capture; real (network) time is unaffected.
        "--virtual-time-budget=30000",
        f"--print-to-pdf={output_pdf.resolve()}",
        html_file.resolve().as_uri(),
    ]
    logger.info(f"Printing {html_file.name} to {output_pdf}")
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=180)
    except subprocess.CalledProcessError as e:
        logger.error(f"Headless print failed for {html_file}:")
        logger.error(f"Command output: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        logger.error(f"Headless print timed out for {html_file}")
        return False

    # Wait out a detached browser (see module docstring) before declaring
    # success; until it exits the PDF may be missing or half-written.
    if not _wait_for_profile_processes(str(profile_dir), timeout=180):
        logger.error(f"Detached browser did not finish for {html_file}")
        return False
    return output_pdf.is_file()


def export_notebook_pdf(notebook_path: Path, output_pdf: Path) -> bool:
    """Export one marimo notebook to a PDF at output_pdf."""
    browser = _find_browser()
    if browser is None:
        logger.error(
            "No Chromium-based browser found for PDF export; skipping "
            f"{notebook_path.name}"
        )
        return False

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        html_file = Path(tmp) / f"{notebook_path.stem}.html"
        if not _export_static_html(notebook_path, html_file):
            return False
        html = html_file.read_text(encoding="utf-8")
        html_file.write_text(
            html.replace("</head>", f"{_PRINT_CSS}</head>", 1), encoding="utf-8"
        )
        if not _print_to_pdf(
            html_file, output_pdf, browser, profile_dir=Path(tmp) / "profile"
        ):
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
