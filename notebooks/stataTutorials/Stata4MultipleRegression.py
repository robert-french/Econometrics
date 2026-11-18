# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(
    app_title="Stata Tutorial 4: Multiple Regression",
    css_file="../marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md(
                '<div>'
                '<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: flex; align-items: center; gap: 0.5em; margin: 0;">'
                '<img src="https://robert-french.github.io/Econometrics/LMU_SquareOrig.png" alt="" style="height: 1.6em; width: auto; display: block;">'
                '<span>ECON 3300 Course home</span>'
                '</a>'
                '</div>'
            ),
            mo.md(
                r"""
                <div style="font-weight: 700; font-size: 1.05em;">Stata Tutorials</div>

                1. <a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata1GettingStarted.html" target="_self">Getting Started with Stata</a>
                2. <a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata2DescribingRelationships.html" target="_self">Describing Data and Relationships</a>
                3. <a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata3SimpleRegression.html" target="_self">Simple Regression</a>
                4. **[Multiple Regression](#top)**
                    1. [Picking up where we left off](#sec1)
                    1. [Adding a second independent variable](#sec2)
                    1. [Why did the coefficients change?](#sec3)
                    1. [Education as a categorical variable](#sec4)
                5. <span class="soon">Nonlinear Specifications</span>
                6. <span class="soon">Panel Data</span>
                """
            ),
        ],
        width="350px",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata3SimpleRegression.html" target="_self">← Stata Tutorial 3</a>'),
            mo.md('<span class="nav-soon">Stata Tutorial 5 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Stata Tutorial 4: Multiple Regression
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contents

    4.1 [Picking up where we left off](#sec1)<br>
    4.2 [Adding a second independent variable](#sec2)<br>
    4.3 [Why did the coefficients change?](#sec3)<br>
    4.4 [Education as a categorical variable](#sec4)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 4.1 Picking up where we left off

    In the third tutorial you estimated three single-variable regressions of `earnings`, one on `education`, one on `age`, and one on `female`. This tutorial puts more than one independent variable into the same regression, as in Lecture 8.

    Open Stata, open `tutorial3.do`—the do-file you saved at the end of Tutorial 3—in the Do-file Editor, and run it from the top with the Execute (do) button so that the dataset loads and the `female` variable from Tutorial 3 is created. Then add a comment line at the bottom to mark the start of this tutorial's code.

    ```stata
    * Stata Tutorial 4
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 4.2 Adding a second independent variable

    To estimate a regression with several independent variables, list them one after another following the dependent variable. Add this line to your do-file and rerun it.

    ```stata
    regress earnings education age, vce(robust)
    ```

    The coefficient table now has one row for each independent variable, plus the `_cons` row for the intercept. It represents the fitted regression

    $$
    \widehat{\text{earnings}} = 21{,}747 + 11{,}531 \times \text{education} + 376 \times \text{age}.
    $$

    As Section 8.2 of the Lecture 8 notebook explains, each coefficient now describes a comparison that holds the other independent variable fixed. Comparing two people of the same age, the person who is one education category higher earns about \$11,531 more per year on average. Comparing two people in the same education category, the person who is one year older earns about \$376 more per year on average.

    The $R^2$ rises from 0.68 in the regression on `education` alone to 0.73, because education and age together account for more of the variation in earnings than education does by itself.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata4tutorial/stata4_shot1_regress_education_age.png" alt="regress earnings education age output with robust standard errors" style="display:block;margin:0.5rem auto 1rem;width:597px;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 4.3 Why did the coefficients change?

    The table below collects the regression you just ran with the single-variable regressions from Tutorial 3, in the format of Lecture 10. Columns (1) and (2) are the regressions of `earnings` on `education` alone and on `age` alone, and column (3) is the regression from Section 4.2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Regression table for Section 4.3. All five regressions use vce(robust);
    # the numbers are copied from the Stata output for the course dataset.
    _cols = [
        {"education": ("11,281", "565"), "_cons": ("37,903", "1,471"), "r2": "0.680"},
        {"age": ("270", "120"), "_cons": ("54,281", "4,966"), "r2": "0.028"},
        {"education": ("11,531", "503"), "age": ("376", "65"),
         "_cons": ("21,747", "2,985"), "r2": "0.734"},
        {"female": ("−4,143", "2,207"), "_cons": ("67,377", "1,566"), "r2": "0.017"},
        {"female": ("−448", "1,312"), "education": ("11,254", "584"),
         "_cons": ("38,182", "1,755"), "r2": "0.680"},
    ]
    _pad = "padding:3px 15px;text-align:center;"
    _left = "padding:3px 15px;text-align:left;"

    def _cell(_c, _key):
        if _key not in _c:
            return f"<td style='{_pad}'></td>"
        _b, _se = _c[_key]
        return (
            f"<td style='{_pad}'>{_b}"
            f"<br><span style='color:#6b7280;'>({_se})</span></td>"
        )

    _rows = []
    for _key, _label in [("education", "education"), ("age", "age"),
                         ("female", "female"), ("_cons", "Constant")]:
        _name = _label if _key == "_cons" else f"<code>{_label}</code>"
        _rows.append(
            f"<tr><td style='{_left}'>{_name}</td>"
            + "".join(_cell(_c, _key) for _c in _cols) + "</tr>"
        )
    _top = "border-top:1px solid rgba(120,120,120,0.6);"
    _rows.append(
        f"<tr><td style='{_left}{_top}'>Observations</td>"
        + "".join(f"<td style='{_pad}{_top}'>200</td>" for _c in _cols) + "</tr>"
    )
    _rows.append(
        f"<tr><td style='{_left}'>R²</td>"
        + "".join(f"<td style='{_pad}'>{_c['r2']}</td>" for _c in _cols) + "</tr>"
    )
    _rule = "2px solid rgba(120,120,120,0.9)"
    _hdr = "".join(
        f"<th style='{_pad}font-weight:600;'>({_i})</th>" for _i in range(1, 6)
    )
    _table = (
        "<div style='overflow-x:auto;text-align:center;'>"
        f"<table style='display:inline-table;width:auto;border-collapse:collapse;"
        f"margin:1rem auto;font-size:0.9rem;line-height:1.25;text-align:left;"
        f"border-top:{_rule};border-bottom:{_rule};'>"
        "<thead>"
        "<tr><td></td><td colspan='5' style='text-align:center;"
        "padding:5px 0 3px;font-weight:600;'>Dependent variable: annual "
        "earnings ($)</td></tr>"
        "<tr><td style='border-bottom:1px solid rgba(120,120,120,0.6);'></td>"
        "<td colspan='5' style='border-bottom:1px solid rgba(120,120,120,0.6);'></td></tr>"
        f"<tr><td></td>{_hdr}</tr>"
        "</thead>"
        f"<tbody>{''.join(_rows)}</tbody>"
        "</table></div>"
    )
    _note = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:620px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        "Heteroskedasticity-robust standard errors are in parentheses. Every "
        "column is estimated with the <code>vce(robust)</code> option."
        "</span>"
    )
    mo.vstack([mo.md(_table), _note])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Start with columns (1) to (3). The coefficient on `education` rises from 11,281 in column (1) to 11,531 in column (3), and the coefficient on `age` rises from 270 in column (2) to 376 in column (3). Both coefficients are larger once the other variable is included. In other words, each single-variable estimate was *biased downward*, because the other variable was left in the error term.

    The sign table in Section 8.1 of the Lecture 8 notebook tells us what this implies. Take column (1), where `age` is an omitted factor. Column (3) shows that age raises earnings. An omitted factor that raises $Y$ creates a negative bias only if it is *lower* when $X$ is higher. So the downward bias tells us that the more educated people in this sample must be somewhat younger on average. The same reasoning applies to column (2), where `education` is the omitted factor.

    We can confirm this directly. Add this line to your do-file and rerun it.

    ```stata
    correlate education age
    ```

    The correlation between `education` and `age` is $-0.08$. It is negative, as we predicted. It is also small, which helps explain why the coefficient on `education` moved only a little.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata4tutorial/stata4_shot2_correlate_education_age.png" alt="correlate education age output" style="display:block;margin:0.5rem auto 1rem;width:251px;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Something similar happens when we build on the regression of `earnings` on `female` from Section 3.4 of Tutorial 3, shown in column (4). Add these lines to your do-file and rerun it.

    ```stata
    regress earnings female education, vce(robust)
    correlate female education
    ```

    The first line gives column (5). Once we hold education fixed, the coefficient on `female` moves from $-4{,}143$ to $-448$, and it is no longer statistically distinguishable from zero. The estimate in column (4) was therefore biased downward by a large amount. Since education raises earnings, the sign table from Lecture 8 says that education must be lower when `female` is higher, meaning that the women in this sample have less education than the men on average. The `correlate` output confirms this; the correlation between `female` and `education` is $-0.14$, almost twice as large in magnitude as the correlation between `education` and `age`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4.4 Education as a categorical variable

    So far, we have treated the `education` variable as continuous, even though it only takes the values 1 through 4, which represent groups of education levels. This forces each step up in education, from high school to some college, from some college to a bachelor's degree, and from a bachelor's degree to a graduate degree, to have the same association with earnings. We can relax this by instead treating `education` as a categorical variable, including a separate indicator variable for each education category. Stata creates the indicators for us when we put `i.` in front of a variable's name. Add this line to your do-file and rerun it.

    ```stata
    regress earnings i.education age, vce(robust)
    ```

    The screenshot at the end of this section shows the output. Under the `education` heading, the coefficient table now has a row for some college, a row for a bachelor's degree, and a row for a graduate degree, but no row for high school. Stata leaves out one category, called the *base category*, because the four indicators add up to 1 for every person. Including all four indicator variables together with the intercept would violate the no perfect multicollinearity assumption from Section 9.1 of the Lecture 9 notebook.

    Each coefficient in these three rows compares one category with the base category, holding age fixed. For example, the bachelor's degree row in the screenshot says that a person with a bachelor's degree earns about \$20,526 more per year on average than a person of the same age whose highest level of education is high school.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata4tutorial/stata4_shot3_regress_i_education.png" alt="regress earnings i.education age output with robust standard errors" style="display:block;margin:0.5rem auto 1rem;width:622px;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The lines you added in this tutorial should look something like this, below the Tutorial 1, 2, and 3 lines already in your do-file.

    ```stata
    * Stata Tutorial 4

    regress earnings education age, vce(robust)
    correlate education age

    regress earnings female education, vce(robust)
    correlate female education

    regress earnings i.education age, vce(robust)
    ```

    Save your do-file under a new name, `tutorial4.do`, using **File > Save As** in the Do-file Editor.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** regression with several independent variables, "
            "holding the other independent variables fixed, omitted variable "
            "bias, downward bias, regression table, correlation between "
            "independent variables with `correlate`, categorical variable, "
            "the `i.` prefix for indicator variables, base category.\n\n"
            "**Habits:** compare each coefficient with its value before a "
            "variable was added; use the direction of the change to predict "
            "how the independent variables are related; confirm the "
            "prediction with `correlate`; read each `i.` coefficient as a "
            "comparison with the base category."
        ),
        title="Key terms and habits",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata3SimpleRegression.html" target="_self">← Stata Tutorial 3</a>'),
            mo.md('<span class="nav-soon">Stata Tutorial 5 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
