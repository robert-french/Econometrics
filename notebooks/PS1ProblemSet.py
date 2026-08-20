# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
# ]
# ///

import marimo

__generated_with = "0.23.16"
__preliminary__ = True
__description__ = "Worked solutions for Problem Set 1."
app = marimo.App(
    app_title="Problem Set 1: Probability and Random Variables",
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
            mo.md("# [Problem Set 1](#top)"),
            mo.md("Probability and Random Variables"),
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
    # Problem Set 1: Probability and Random Variables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md("**Solutions are not posted yet.** Worked solutions will appear here after the problem set is due."),
        kind="warn",
    )
    return


if __name__ == "__main__":
    app.run()
