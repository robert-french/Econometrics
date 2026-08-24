"""
Regenerate every lecture notebook's sidebar and prev/next nav rows from the
course outline in course_outline.py.

Run after changing POSTED_THROUGH (the weekly release), adding a lecture to
LECTURES, or renaming sections in a notebook:

    uv run .github/scripts/update_sidebars.py            # all lectures
    uv run .github/scripts/update_sidebars.py Lec1Introduction   # one stem

For each notebook the script rewrites three cells in place, so it is safe to
rerun any number of times:

  * the mo.sidebar cell: course-home link, then a single tight outline of
    all lectures. Posted lectures link to their app pages; the current
    lecture is bold, links to #top, and nests its own section links
    (scraped from the notebook's Contents cell, so they never drift);
    unposted lectures render as grey <span class="soon"> placeholders.
  * the two prev/next nav rows (top row also carries the Download PDF
    link). Links pointing past POSTED_THROUGH become grey
    <span class="nav-soon"> text.

Styling constraint (React error #62): same-page #fragment links must stay
plain markdown with no inline style and no styled wrapper. All visual
treatment lives in notebooks/marimo-overrides.css, scoped to
marimo-sidebar / the soon classes.
"""

# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from course_outline import BASE_URL, LECTURES, POSTED_THROUGH

NOTEBOOKS_DIR = Path(__file__).resolve().parents[2] / "notebooks"

# Section links appear in two Contents-cell styles across the notebooks:
# "1. [Title](#sec1)" (Lec1-5) and "[1. Title](#sec1)<br>" (Lec6-16); the
# generated sidebar itself also contains "[Title](#secN)" lines. Matching
# every "[...](#secN)" and keeping the first occurrence per anchor (with any
# leading "N. " stripped from the label) handles all three, which is what
# makes reruns idempotent.
_SECTION_LINK = re.compile(r"\[([^\]]+)\]\(#(sec\d+)\)")


def _scrape_sections(text: str) -> list[tuple[str, str]]:
    sections: dict[str, str] = {}
    for title, anchor in _SECTION_LINK.findall(text):
        if anchor not in sections:
            sections[anchor] = re.sub(r"^\d+(?:\.\d+)?\.?\s*", "", title).strip()
    return [(title, anchor) for anchor, title in sections.items()]


# A Contents-cell section link in any of its three historical shapes:
# "1. [Title](#sec1)" (markdown list), "[1. Title](#sec1)<br>" (br lines),
# or the generated "2.1 [Title](#sec1)<br>". Sub-entries with lettered
# anchors (#sec4a) deliberately do not match and are left untouched.
_TOC_LINK = re.compile(
    r"^(\s*)(?:\d+(?:\.\d+)?\.?\s+)?\[(?:\d+(?:\.\d+)?\.?\s*)?([^\]]+)\]"
    r"\(#sec(\d+)\)(?:<br>)?\s*$"
)


def _renumber_contents(text: str, lecture_n: int) -> tuple[str, int]:
    """Rewrite the Contents cell's section links as 'L.N [Title](#secN)<br>'.

    Operates line by line inside the Contents cell only, so comments,
    lettered sub-entries, and any other structure survive. The last section
    link keeps no trailing <br>, matching the established style. Returns
    (new_text, number_of_links_rewritten).
    """
    start = text.find("## Contents")
    if start == -1:
        return text, 0
    end = text.find('"""', start)
    if end == -1:
        return text, 0

    region = text[start:end]
    lines = region.split("\n")
    hits = [i for i, line in enumerate(lines) if _TOC_LINK.match(line)]
    for i in hits:
        m = _TOC_LINK.match(lines[i])
        indent, title, sec = m.group(1), m.group(2).strip(), m.group(3)
        br = "" if i == hits[-1] else "<br>"
        lines[i] = f"{indent}{lecture_n}.{sec} [{title}](#sec{sec}){br}"
    return text[:start] + "\n".join(lines) + text[end:], len(hits)


def _renumber_headings(text: str, lecture_n: int) -> tuple[str, int]:
    """Rewrite '## N. Title' section headings as '## L.N Title'.

    Keyed to the '<a id="secN"></a>' anchor immediately above each heading,
    so reruns renumber idempotently and lettered anchors are untouched.
    """
    pattern = re.compile(
        r'(<a id="sec(\d+)"></a>\s*\n\s*)## +\d+(?:\.\d+)?\.? +'
    )
    return pattern.subn(
        lambda m: f"{m.group(1)}## {lecture_n}.{m.group(2)} ", text
    )

_SIDEBAR_CELL = re.compile(
    r"@app\.cell\(hide_code=True\)\ndef _\(mo\):\n    mo\.sidebar\(.*?\n    return\n",
    re.S,
)

# The nav rows are the only hstack cells whose first child is an inline
# mo.md HTML literal and that use this exact justify/align signature; chart
# layout hstacks pass chart variables instead.
_NAV_CELL = re.compile(
    r"@app\.cell\(hide_code=True\)\ndef _\(mo\):\n    mo\.hstack\(\n        \[\n            mo\.md\('<.*?"
    r"justify=\"space-between\", align=\"center\",\n    \)\n    return\n",
    re.S,
)


def _entry(number):
    for n, title, stem in LECTURES:
        if n == number:
            return title, stem
    return None, None


def _sidebar_cell(current_n: int, sections: list[tuple[str, str]]) -> str:
    lines = []
    for n, title, stem in LECTURES:
        if n == current_n:
            lines.append(f"                {n}. **[{title}](#top)**")
            for sec_title, anchor in sections:
                lines.append(f"                    1. [{sec_title}](#{anchor})")
        elif stem is not None and n <= POSTED_THROUGH:
            lines.append(
                f'                {n}. <a href="{BASE_URL}/apps/{stem}.html" '
                f'target="_self">{title}</a>'
            )
        else:
            lines.append(f'                {n}. <span class="soon">{title}</span>')
    outline = "\n".join(lines)
    return f'''@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md(
                '<div>'
                '<a href="{BASE_URL}/" target="_self" style="display: flex; align-items: center; gap: 0.5em; margin: 0;">'
                '<img src="{BASE_URL}/LMU_SquareOrig.png" alt="" style="height: 1.6em; width: auto; display: block;">'
                '<span>ECON 3300 Course home</span>'
                '</a>'
                '</div>'
            ),
            mo.md(
                r"""
                <div style="font-weight: 700; font-size: 1.05em;">Course Outline</div>

{outline}
                """
            ),
        ],
        width="350px",
    )
    return
'''.replace("{BASE_URL}", BASE_URL).replace("{outline}", outline)


def _left_item(current_n: int) -> str:
    if current_n == 1:
        return f'<a href="{BASE_URL}/" target="_self">← Course home</a>'
    title, stem = _entry(current_n - 1)
    if stem is not None and current_n - 1 <= POSTED_THROUGH:
        return (
            f'<a href="{BASE_URL}/apps/{stem}.html" target="_self">'
            f"← Lecture {current_n - 1}</a>"
        )
    return f'<span class="nav-soon">← Lecture {current_n - 1} (coming soon)</span>'


def _right_item(current_n: int) -> str:
    title, stem = _entry(current_n + 1)
    if title is None:
        return f'<a href="{BASE_URL}/" target="_self">Course home →</a>'
    if stem is not None and current_n + 1 <= POSTED_THROUGH:
        return (
            f'<a href="{BASE_URL}/apps/{stem}.html" target="_self">'
            f"Lecture {current_n + 1} →</a>"
        )
    return f'<span class="nav-soon">Lecture {current_n + 1} (coming soon)</span>'


def _nav_cell(current_n: int, stem: str, with_pdf: bool) -> str:
    items = [f"            mo.md('{_left_item(current_n)}'),"]
    if with_pdf:
        items.append(
            f"            mo.md('<a href=\"{BASE_URL}/pdf/{stem}.pdf\" "
            f"target=\"_blank\">Download PDF</a>'),"
        )
    items.append(f"            mo.md('{_right_item(current_n)}'),")
    body = "\n".join(items)
    return f'''@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
{body}
        ],
        justify="space-between", align="center",
    )
    return
'''


def update_notebook(number: int, stem: str) -> bool:
    path = NOTEBOOKS_DIR / f"{stem}.py"
    if not path.is_file():
        print(f"SKIP {stem}: file not found")
        return False
    text = path.read_text(encoding="utf-8")

    sections = _scrape_sections(text)
    if not sections:
        print(f"SKIP {stem}: no Contents links found")
        return False

    new_text, n_side = _SIDEBAR_CELL.subn(
        lambda m: _sidebar_cell(number, sections), text, count=1
    )
    if n_side != 1:
        print(f"SKIP {stem}: sidebar cell not found")
        return False

    new_text, n_toc = _renumber_contents(new_text, number)
    new_text, n_head = _renumber_headings(new_text, number)
    if n_toc != len(sections) or n_head != len(sections):
        print(
            f"WARN {stem}: {len(sections)} sections but renumbered "
            f"{n_toc} Contents links and {n_head} headings"
        )

    nav_cells = _NAV_CELL.findall(new_text)
    if len(nav_cells) != 2:
        print(f"SKIP {stem}: expected 2 nav cells, found {len(nav_cells)}")
        return False
    new_text = _NAV_CELL.sub(
        lambda m, it=iter([True, False]): _nav_cell(number, stem, next(it)),
        new_text,
        count=2,
    )

    path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"updated {stem} ({len(sections)} sections)")
    return True


def update_all(only=None) -> int:
    """Regenerate the given stems (or all lectures); returns failure count."""
    only = set(only or [])
    failures = 0
    for number, title, stem in LECTURES:
        if stem is None:
            continue
        if only and stem not in only:
            continue
        if not update_notebook(number, stem):
            failures += 1
    return failures


def main() -> int:
    return 1 if update_all(sys.argv[1:]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
