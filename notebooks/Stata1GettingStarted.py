# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
# ]
# ///

import marimo

__generated_with = "0.23.16"
__preliminary__ = True
__description__ = "Open Stata, load a dataset, and run your first commands."
app = marimo.App(
    app_title="Stata Tutorial 1: Getting Started with Stata",
    css_file="marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: block; margin-bottom: 1.5em;">Course home</a>'),
            mo.md("# [Stata Tutorial 1](#top)"),
            mo.md("Getting Started with Stata"),
        ],
        width="260px",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self">← Course home</a>')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Stata Tutorial 1: Getting Started with Stata
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md("**This tutorial is under construction.** A full walkthrough of installing Stata, loading data, and running your first regressions is coming soon."),
        kind="warn",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tutorial series walks you through the Stata skills you need for ECON 3300,
    one short guide at a time. The code blocks show Stata commands to type into
    Stata's command window — they do not run in the browser.

    As a preview, here is what a first Stata session looks like. The `sysuse`
    command loads one of Stata's built-in practice datasets, `summarize` reports
    descriptive statistics, and `regress` fits a regression by OLS:

    ```stata
    sysuse auto, clear
    summarize price mpg
    regress price mpg
    ```

    Each tutorial will pair commands like these with screenshots of the output and
    an explanation of how to read it.
    """)
    return


if __name__ == "__main__":
    app.run()
