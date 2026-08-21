"""
Build script for marimo notebooks.

This script uses notebooks/ as the single source of truth.

Each marimo notebook in notebooks/ is exported twice:
    1. As an editable notebook in _site/notebooks/
    2. As a read-only app in _site/apps/

The script also generates an index.html file that lists both versions.
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "jinja2==3.1.3",
#     "fire==0.7.0",
#     "loguru==0.7.0",
#     "playwright>=1.55"
# ]
# ///

import ast
import re
import shutil
import subprocess
from typing import List, Optional, Union
from pathlib import Path

import jinja2
import fire

from loguru import logger

from export_pdf import export_notebook_pdf

# Notebooks that also get a downloadable PDF at _site/pdf/<stem>.pdf. The
# notebook's "Download PDF" link points there.
PDF_EXPORT_STEMS = {"Lec1Introduction", "Lec2RandomVariables"}


# Homepage tabs are keyed off the notebook filename: LecN* files are lectures,
# PSN* files are problem set solutions, StataN* files are Stata tutorials.
_CATEGORY_PATTERNS = (
    ("problem_set", re.compile(r"^PS(\d+)")),
    ("stata", re.compile(r"^Stata(\d+)")),
    ("lecture", re.compile(r"^Lec(\d+)")),
)

# Thematic groups for the Lectures tab, keyed on lecture number. A group with
# no built notebooks is omitted from the rendered page.
LECTURE_GROUPS = (
    ("Introduction to Econometrics", 1, 1),
    ("Probability and Statistics Review", 2, 4),
    ("Simple Linear Regression", 5, 7),
    ("Multiple Regression", 8, 10),
    ("Nonlinear Regression", 11, 13),
    ("Internal and External Validity", 14, 14),
    ("Panel Data", 15, 16),
    ("Binary Dependent Variables", 17, 17),
    ("Experiments and Quasi-Experiments", 18, 19),
)


def _categorize(stem: str) -> tuple[str, Optional[int]]:
    """Return (category, number) for a notebook filename stem."""
    for category, pattern in _CATEGORY_PATTERNS:
        match = pattern.match(stem)
        if match:
            return category, int(match.group(1))
    return "lecture", None


def _index_sections(apps_data: List[dict]) -> tuple[List[dict], List[dict], List[dict]]:
    """Split the exported apps into the three homepage tabs.

    Returns (lecture_groups, problem_sets, stata_tutorials), where
    lecture_groups is a list of {"title", "range_label", "items"} dicts in
    LECTURE_GROUPS order. Lectures whose number falls outside every group
    (or is missing) land in a trailing "Other lectures" group.
    """
    lectures: List[tuple[Optional[int], dict]] = []
    problem_sets: List[dict] = []
    stata_tutorials: List[dict] = []

    for item in apps_data:
        category, number = _categorize(item["stem"])
        if category == "problem_set":
            problem_sets.append(item)
        elif category == "stata":
            stata_tutorials.append(item)
        else:
            lectures.append((number, item))

    grouped_numbers = set()
    lecture_groups: List[dict] = []
    for title, first, last in LECTURE_GROUPS:
        items = [
            item
            for number, item in lectures
            if number is not None and first <= number <= last
        ]
        if not items:
            continue
        grouped_numbers.update(range(first, last + 1))
        range_label = (
            f"Lecture {first}" if first == last else f"Lectures {first}–{last}"
        )
        lecture_groups.append(
            {"title": title, "range_label": range_label, "items": items}
        )

    leftovers = [
        item
        for number, item in lectures
        if number is None
        or not any(first <= number <= last for _, first, last in LECTURE_GROUPS)
    ]
    if leftovers:
        lecture_groups.append(
            {"title": "Other lectures", "range_label": "", "items": leftovers}
        )

    return lecture_groups, problem_sets, stata_tutorials


def _parse_notebook(notebook_path: Path) -> Optional[ast.Module]:
    try:
        return ast.parse(notebook_path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as e:
        logger.warning(f"Could not parse {notebook_path}: {e}")
        return None


def _extract_app_title(notebook_path: Path) -> Optional[str]:
    """Return the app_title from a notebook's marimo.App(...) call, if set."""
    tree = _parse_notebook(notebook_path)
    if tree is None:
        return None

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "App"):
            continue
        for kw in node.keywords:
            if (
                kw.arg == "app_title"
                and isinstance(kw.value, ast.Constant)
                and isinstance(kw.value.value, str)
            ):
                return kw.value.value
    return None


def _extract_description(notebook_path: Path) -> Optional[str]:
    """Return the value of a module-level `__description__ = "..."` assignment."""
    tree = _parse_notebook(notebook_path)
    if tree is None:
        return None

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if (
                isinstance(target, ast.Name)
                and target.id == "__description__"
                and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)
            ):
                return node.value.value
    return None


def _extract_preliminary(notebook_path: Path) -> bool:
    """Return True if the notebook sets a module-level `__preliminary__ = True`.

    Used to flag a lecture as a work in progress so the homepage card can show
    a "Preliminary" badge. Absent or falsy assignment means not preliminary.
    """
    tree = _parse_notebook(notebook_path)
    if tree is None:
        return False

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if (
                isinstance(target, ast.Name)
                and target.id == "__preliminary__"
                and isinstance(node.value, ast.Constant)
            ):
                return bool(node.value.value)
    return False


# Labels that open the two halves of a notebook's summary callout. The
# "**Terms:**"/"**Concepts:**" pair is current; the "Key ... covered:" pair is
# the original wording, kept so an older notebook still yields a teaser.
_KEY_TERM_LABELS = (
    "**Terms:**",
    "**Concepts:**",
    "Key terms covered:",
    "Key concepts covered:",
)


def _extract_key_terms(notebook_path: Path) -> Optional[str]:
    """Return the notebook's summary-callout terms and concepts as one
    comma-separated string, for use as a teaser on the index cards. Returns
    None if the summary callout is absent.

    The summary callout is written as adjacent string literals, which Python
    concatenates into a single string constant, so the whole block lives in one
    ast.Constant node we can read directly.
    """
    tree = _parse_notebook(notebook_path)
    if tree is None:
        return None

    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        text = node.value
        if not any(label in text for label in _KEY_TERM_LABELS):
            continue
        # Strip the labels before the bold markers, so a label carrying its own
        # asterisks ("**Terms:**") is matched while it is still intact.
        cleaned = text
        for label in _KEY_TERM_LABELS:
            cleaned = cleaned.replace(label, "")
        cleaned = cleaned.replace("**", "")
        parts = [
            seg.strip().strip(".").strip()
            for seg in cleaned.split("\n")
            if seg.strip()
        ]
        joined = ", ".join(p for p in parts if p)
        return joined or None
    return None


def _export_html_wasm(
    notebook_path: Path,
    output_file: Path,
    as_app: bool = False,
) -> bool:
    """Export a single marimo notebook to HTML/WebAssembly format."""

    # --execute pre-runs every cell at build time so the deployed page renders
    # immediately with the default-state outputs (charts, captions, computed
    # numbers) while Pyodide boots in the background. Combined with marimo's
    # session-snapshot rendering, this kills the "blank page until Pyodide
    # finishes" wait. See https://marimo.io/blog/newsletter-25 (PR #9437).
    cmd: List[str] = ["uvx", "marimo", "export", "html-wasm", "--sandbox", "--execute"]

    if as_app:
        logger.info(f"Exporting {notebook_path} to {output_file} as app")
        cmd.extend(["--mode", "run", "--no-show-code"])
    else:
        logger.info(f"Exporting {notebook_path} to {output_file} as editable notebook")
        cmd.extend(["--mode", "edit"])

    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Run from the notebook's directory so marimo resolves `css_file=`
        # (and any other notebook-relative paths) against that folder. We pass
        # absolute paths for the notebook and the output to keep the rest of
        # the build's path semantics intact.
        notebook_abs = notebook_path.resolve()
        output_abs = output_file.resolve()
        cmd.extend([str(notebook_abs), "-o", str(output_abs)])

        logger.debug(f"Running command: {cmd} (cwd={notebook_abs.parent})")
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd=notebook_abs.parent,
        )

        logger.info(f"Successfully exported {notebook_path}")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Error exporting {notebook_path}:")
        logger.error(f"Command output: {e.stderr}")
        return False

    except Exception as e:
        logger.error(f"Unexpected error exporting {notebook_path}: {e}")
        return False


def _generate_index(
    output_dir: Path,
    template_file: Path,
    notebooks_data: List[dict] | None = None,
    apps_data: List[dict] | None = None,
) -> None:
    """Generate an index.html file that lists all exported notebooks and apps."""

    logger.info("Generating index.html")

    index_path: Path = output_dir / "index.html"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        template_dir = template_file.parent
        template_name = template_file.name

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
        )

        lecture_groups, problem_sets, stata_tutorials = _index_sections(
            apps_data or []
        )

        template = env.get_template(template_name)
        rendered_html = template.render(
            notebooks=notebooks_data,
            apps=apps_data,
            lecture_groups=lecture_groups,
            problem_sets=problem_sets,
            stata_tutorials=stata_tutorials,
        )

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)

        logger.info(f"Successfully generated index.html at {index_path}")

    except IOError as e:
        logger.error(f"Error generating index.html: {e}")

    except jinja2.exceptions.TemplateError as e:
        logger.error(f"Error rendering template: {e}")


def _export_from_notebooks(
    source_folder: Path,
    output_dir: Path,
    as_app: bool = False,
) -> List[dict]:
    """Export all marimo notebooks from notebooks/ either as apps or editable notebooks.

    Source files always live in notebooks/.

    Editable notebooks are written to:
        _site/notebooks/<name>.html

    Apps are written to:
        _site/apps/<name>.html
    """

    if not source_folder.exists():
        logger.warning(f"Directory not found: {source_folder}")
        return []

    def _natural_key(path: Path):
        # Sort "Lec2..." before "Lec10..." by treating digit runs as integers,
        # so the index lists lectures in numeric order regardless of the
        # arbitrary order rglob returns files in.
        return [
            int(tok) if tok.isdigit() else tok.lower()
            for tok in re.split(r"(\d+)", path.stem)
        ]

    notebooks = sorted(source_folder.rglob("*.py"), key=_natural_key)
    logger.debug(f"Found {len(notebooks)} Python files in {source_folder}")

    if not notebooks:
        logger.warning(f"No notebooks found in {source_folder}!")
        return []

    notebook_data = []

    output_subfolder = "apps" if as_app else "notebooks"

    for nb in notebooks:
        relative_path = nb.relative_to(source_folder).with_suffix(".html")
        html_path = Path(output_subfolder) / relative_path
        output_file = output_dir / html_path

        success = _export_html_wasm(
            notebook_path=nb,
            output_file=output_file,
            as_app=as_app,
        )

        if success:
            display_name = _extract_app_title(nb) or nb.stem.replace("_", " ").title()
            notebook_data.append(
                {
                    "stem": nb.stem,
                    "display_name": display_name,
                    "description": _extract_description(nb),
                    "key_terms": _extract_key_terms(nb),
                    "preliminary": _extract_preliminary(nb),
                    "html_path": html_path.as_posix(),
                }
            )

    logger.info(
        f"Successfully exported {len(notebook_data)} out of {len(notebooks)} files "
        f"from {source_folder} as {'apps' if as_app else 'editable notebooks'}"
    )

    return notebook_data


def main(
    output_dir: Union[str, Path] = "_site",
    template: Union[str, Path] = "templates/tailwind.html.j2",
) -> None:
    """Main function to export marimo notebooks."""

    logger.info("Starting marimo build process")

    output_dir = Path(output_dir)
    logger.info(f"Output directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    template_file = Path(template)
    logger.info(f"Using template file: {template_file}")

    source_folder = Path("notebooks")

    # Export each source notebook once as an editable notebook.
    notebooks_data = _export_from_notebooks(
        source_folder=source_folder,
        output_dir=output_dir,
        as_app=False,
    )

    # Export each source notebook again as a clean app.
    apps_data = _export_from_notebooks(
        source_folder=source_folder,
        output_dir=output_dir,
        as_app=True,
    )

    if not notebooks_data and not apps_data:
        logger.warning("No notebooks found!")
        return

    # Generate downloadable PDFs for the allowlisted notebooks.
    for nb in sorted(source_folder.rglob("*.py")):
        if nb.stem in PDF_EXPORT_STEMS:
            export_notebook_pdf(nb, output_dir / "pdf" / f"{nb.stem}.pdf")

    _generate_index(
        output_dir=output_dir,
        notebooks_data=notebooks_data,
        apps_data=apps_data,
        template_file=template_file,
    )

    # Copy any static assets sitting next to the template (e.g. the LMU shield
    # watermark) into the site root so the rendered index.html can reference
    # them with relative paths.
    static_dir = template_file.parent / "static"
    if static_dir.exists():
        for asset in static_dir.iterdir():
            if asset.is_file():
                shutil.copy2(asset, output_dir / asset.name)
                logger.info(f"Copied static asset {asset.name} to {output_dir}")

    logger.info(f"Build completed successfully. Output directory: {output_dir}")


if __name__ == "__main__":
    fire.Fire(main)

