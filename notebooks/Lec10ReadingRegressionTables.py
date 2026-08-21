# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "numpy",
#     "pandas",
#     "altair",
#     "scipy",
#     "pyarrow",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(
    app_title="Lecture 10: Reading Regression Tables",
    css_file="marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt
    from scipy import stats

    return mo, np


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
                1. <a href="https://robert-french.github.io/Econometrics/apps/Lec1Introduction.html" target="_self">Introduction</a>
                2. <a href="https://robert-french.github.io/Econometrics/apps/Lec2RandomVariables.html" target="_self">Random Variables</a>
                3. <a href="https://robert-french.github.io/Econometrics/apps/Lec3WorkingWithMultipleRandomVariables.html" target="_self">Multiple Random Variables</a>
                4. <a href="https://robert-french.github.io/Econometrics/apps/Lec4EstimationHypothesisTestingAndConfidenceIntervals.html" target="_self">Estimation and Hypothesis Testing</a>
                5. <span class="soon">Simple Linear Regression</span>
                6. <span class="soon">OLS Assumptions for Causal Inference</span>
                7. <span class="soon">Inference and Omitted Variable Bias</span>
                8. <span class="soon">Multiple Regression</span>
                9. <span class="soon">Control Variables and Inference</span>
                10. **[Reading Regression Tables](#top)**
                    1. [Regression tables](#sec1)
                    1. [Why coefficients change across columns](#sec2)
                    1. [Statistical significance](#sec3)
                11. <span class="soon">Nonlinear Regression: Polynomials</span>
                12. <span class="soon">Nonlinear Regression: Logarithms</span>
                13. <span class="soon">Nonlinear Regression: Interaction Terms</span>
                14. <span class="soon">Internal and External Validity</span>
                15. <span class="soon">Panel Data I</span>
                16. <span class="soon">Panel Data II</span>
                17. <span class="soon">Binary Dependent Variable Regressions</span>
                18. <span class="soon">Experiments</span>
                19. <span class="soon">Quasi-Experiments</span>
                """
            ),
        ],
        width="300px",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<span class="nav-soon">← Lecture 9 (coming soon)</span>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/pdf/Lec10ReadingRegressionTables.pdf" target="_blank">Download PDF</a>'),
            mo.md('<span class="nav-soon">Lecture 11 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 10: Reading Regression Tables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Same-page (#fragment) links must stay plain markdown links with no inline
    # style and no styled wrapper. marimo re-renders fragment links as React
    # navigation components, and any inline style string on the link (or on a
    # span/div around it) is passed to React as the `style` prop, which must be
    # an object, not a string -> "Minified React error #62".
    mo.md(r"""
    ## Contents

    [1. Regression tables](#sec1)<br>
    [2. Why coefficients change across columns](#sec2)<br>
    [3. Statistical significance](#sec3)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Regression tables

    A *regression table* reports several regressions side by side, making it easy to compare their results. Each column presents one regression with the same dependent variable but a different set of independent variables. Each row corresponds to one independent variable. Reading down a column describes a single regression, while reading across a row shows how the coefficient on a variable changes as other variables are added.

    The table below reports four regressions estimated using the same sample of 1,200 workers. The dependent variable is hourly wage in dollars. The independent variables are years of education, years of work experience, parental income measured in standard deviations from its mean, and an indicator equal to one if the worker is a woman. Column (1) regresses hourly wage on education alone. Each subsequent column adds one independent variable, so column (4) includes all four.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # Wage data for 1,200 workers used to build the regression table. Education
    # is correlated with parental income, which is the source of the omitted
    # variable bias discussed in Section 2.
    _rng = np.random.default_rng(42)
    _n = 1200
    _pinc = _rng.normal(0.0, 1.0, _n)
    _educ = 13.0 + 1.2 * _pinc + _rng.normal(0.0, 1.5, _n)
    _exper = _rng.normal(20.0, 8.0, _n)
    _female = _rng.integers(0, 2, _n).astype(float)
    _wage = (
        5.0 + 1.2 * _educ + 0.15 * _exper - 2.0 * _female + 2.5 * _pinc
        + _rng.normal(0.0, 4.0, _n)
    )

    _data = {
        "Education (years)": _educ,
        "Experience (years)": _exper,
        "Parental income (SD)": _pinc,
        "Female": _female,
    }
    var_order = [
        "Education (years)",
        "Experience (years)",
        "Parental income (SD)",
        "Female",
    ]
    _specs = [
        ["Education (years)"],
        ["Education (years)", "Experience (years)"],
        ["Education (years)", "Experience (years)", "Parental income (SD)"],
        ["Education (years)", "Experience (years)", "Parental income (SD)", "Female"],
    ]

    def _fit(_names):
        _X = np.column_stack([np.ones(_n)] + [_data[_c] for _c in _names])
        _k = _X.shape[1] - 1
        _beta, *_ = np.linalg.lstsq(_X, _wage, rcond=None)
        _resid = _wage - _X @ _beta
        _ssr = float(_resid @ _resid)
        _tss = float(((_wage - _wage.mean()) ** 2).sum())
        _s2 = _ssr / (_n - _k - 1)
        _se = np.sqrt(np.diag(_s2 * np.linalg.inv(_X.T @ _X)))
        _r2 = 1.0 - _ssr / _tss
        _ar2 = 1.0 - (_ssr / (_n - _k - 1)) / (_tss / (_n - 1))
        return {"names": _names, "b": _beta, "se": _se, "r2": _r2, "ar2": _ar2, "n": _n}

    fits = [_fit(_s) for _s in _specs]
    return fits, var_order


@app.cell(hide_code=True)
def _(fits, mo, var_order):
    # Each row carries a `title` attribute, so hovering it shows a native
    # tooltip with the definition of that coefficient or statistic.
    _tips = {
        "Education (years)": "Estimated change in the hourly wage for workers with one more year of education, holding the other independent variables in the column fixed.",
        "Experience (years)": "Estimated change in the hourly wage for workers with one more year of work experience, holding the other independent variables in the column fixed.",
        "Parental income (SD)": "Estimated change in the hourly wage for workers with a one standard deviation rise in parental income, holding the other independent variables in the column fixed.",
        "Female": "Estimated wage gap for women relative to men with the same values of the other independent variables in the column.",
        "Constant": "The predicted hourly wage when every independent variable in the column equals zero.",
        "Observations": "The number of workers used to estimate the regression.",
        "R²": "The share of the variation in wages the independent variables explain. The R² ranges from 0 to 1.",
        "Adjusted R²": "The R-squared with a penalty for each independent variable, so a variable that does not help explain the variation in wages lowers it.",
    }

    def _stars(_t):
        _a = abs(_t)
        return "***" if _a > 2.576 else "**" if _a > 1.96 else "*" if _a > 1.645 else ""

    def _lookup(_fit):
        _m = {"Constant": (_fit["b"][0], _fit["se"][0])}
        for _j, _nm in enumerate(_fit["names"]):
            _m[_nm] = (_fit["b"][_j + 1], _fit["se"][_j + 1])
        return _m

    _maps = [_lookup(_f) for _f in fits]
    _ncols = len(fits)
    _pad = "padding:3px 15px;text-align:center;"

    def _coef_cell(_m, _name):
        if _name not in _m:
            return f"<td style='{_pad}'></td>"
        _b, _se = _m[_name]
        _inner = (
            f"{_b:.3f}{_stars(_b / _se)}"
            f"<br><span style='color:#6b7280;'>({_se:.3f})</span>"
        )
        return f"<td style='{_pad}'>{_inner}</td>"

    def _row(_label, _cells_html, _border=""):
        _lab = f"<td style='padding:3px 15px;text-align:left;{_border}'>{_label}</td>"
        return (
            f"<tr title='{_tips.get(_label, '')}' style='cursor:help;'>"
            f"{_lab}{_cells_html}</tr>"
        )

    _rows = []
    for _name in var_order + ["Constant"]:
        _cells = "".join(_coef_cell(_m, _name) for _m in _maps)
        _rows.append(_row(_name, _cells))

    _top = "border-top:1px solid rgba(120,120,120,0.6);"

    def _stat_cells(_values, _border=""):
        return "".join(f"<td style='{_pad}{_border}'>{_v}</td>" for _v in _values)

    _rows.append(
        _row("Observations", _stat_cells([f"{_f['n']:,}" for _f in fits], _top), _border=_top)
    )
    _rows.append(_row("R²", _stat_cells([f"{_f['r2']:.3f}" for _f in fits])))
    _rows.append(_row("Adjusted R²", _stat_cells([f"{_f['ar2']:.3f}" for _f in fits])))

    _rule = "2px solid rgba(120,120,120,0.9)"
    _colhdr = "".join(
        f"<th style='{_pad}font-weight:600;'>({_i})</th>"
        for _i in range(1, _ncols + 1)
    )
    # display:inline-table + width:auto shrinks the table to its content, and
    # text-align:center on the wrapper centers it, so the top and bottom rules
    # span only the table rather than the whole page.
    _table = (
        "<div style='overflow-x:auto;text-align:center;'>"
        f"<table style='display:inline-table;width:auto;border-collapse:collapse;"
        f"margin:1rem auto;font-size:0.9rem;line-height:1.25;text-align:left;"
        f"border-top:{_rule};border-bottom:{_rule};'>"
        "<thead>"
        f"<tr><td></td><td colspan='{_ncols}' style='text-align:center;"
        "padding:5px 0 3px;font-weight:600;'>Dependent variable: hourly wage (dollars)</td></tr>"
        f"<tr><td style='border-bottom:1px solid rgba(120,120,120,0.6);'></td>"
        f"<td colspan='{_ncols}' style='border-bottom:1px solid rgba(120,120,120,0.6);'></td></tr>"
        f"<tr><td></td>{_colhdr}</tr>"
        "</thead>"
        f"<tbody>{''.join(_rows)}</tbody>"
        "</table></div>"
    )

    _note = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        "Standard errors in parentheses. "
        "One star marks statistical significance at the 10% level, two at the 5% level, "
        "and three at the 1% level. Hover your mouse over a row for its definition."
        "</span>"
    )
    mo.vstack([mo.md(_table), _note])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each coefficient cell contains two numbers. The top number is the estimated coefficient for that independent variable, $\hat\beta_j$. It gives the change in predicted hourly wage associated with a one-unit increase in that variable, holding the other independent variables included in the column fixed. The number in parentheses below it is the standard error. Recall that the standard error is the square root of the estimated sample variance of $\hat\beta_j$ and measures how much $\hat\beta_j$ would typically vary across random samples from the same population. The asterisks indicate *statistical significance*, which we discuss in Section 3. The final three rows report the number of observations, the R-squared, and the adjusted R-squared for each regression.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Why coefficients change across columns

    Let's begin by reading across the education row. In column (1), each additional year of education is associated with a roughly $2.00 increase in hourly wages.

    Column (2) adds work experience to the regression. The education coefficient remains roughly $2.00, which tells us that controlling for experience does not meaningfully change the estimated relationship between education and wages. Because experience is associated with wages, this suggests that experience is uncorrelated with education in the sample. Omitting experience therefore produces little or no omitted variable bias in the education coefficient. Experience nevertheless matters for wages; holding education fixed, each additional year of experience is associated with a $0.16 increase in hourly wages.

    Column (3) adds parental income, and the education coefficient falls from $2.00 to $1.14. This change reflects *omitted variable bias*, which we studied in Lecture 8. Before parental income was included in the regression, it was part of the error term. Parental income is likely positively correlated with education in this sample because children from higher-income families tend to complete more schooling. Parental income may also affect wages independently of education through factors such as access to internships and financial support during job searches. Columns (1) and (2) therefore attribute some of the wage differences associated with parental income to education, creating upward bias in the education coefficient. Holding parental income fixed in column (3) compares workers from similar family backgrounds and removes this particular source of bias, although other omitted factors may remain in the error term.

    Column (4) adds an indicator for female workers. The education coefficient changes only slightly, from $1.14 to $1.16, indicating that sex is nearly uncorrelated with education in this sample. Holding education, experience, and parental income fixed, women are estimated to earn $1.94 less per hour than men. Adding the indicator variable reveals this wage difference but has little effect on the estimated return to education.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Statistical significance

    The asterisks beside each coefficient indicate its *statistical significance*. Recall that we test the null hypothesis that the corresponding population coefficient equals zero using the t-statistic

    $$
    t = \frac{\hat{\beta}_j - 0}{\hat{\sigma}_{\hat{\beta}_j}}.
    $$

    We choose a significance level, denoted by $\alpha$, before conducting the test. The significance level is the probability of rejecting the null hypothesis when it is actually true. Thus, setting $\alpha=0.05$ means accepting a 5% probability of such an error across repeated samples from the same population.

    A coefficient is statistically significant at the 10% level when its p-value is below 0.10, at the 5% level when its p-value is below 0.05, and at the 1% level when its p-value is below 0.01. Smaller significance levels require stronger evidence against the null hypothesis. A coefficient significant at the 1% level is therefore also significant at the 5% and 10% levels. Regression tables commonly summarize these results with one asterisk for the 10% level, two for the 5% level, and three for the 1% level of statistical significance.

    For example, the education coefficient in column (4) is $1.16 with a standard error of $0.08. Its t-statistic is about 15, so its p-value is well below 0.01 and it receives three asterisks. We therefore reject the null hypothesis that the population education coefficient is zero at the 1% significance level. Indeed, every coefficient estimate in this table is statistically significant at the 1% level.

    Statistical significance does not tell us whether an effect is large or important. The experience coefficient is precisely estimated and highly statistically significant, but an additional year of experience is associated with only a $0.16 increase in hourly wages, compared with $1.16 for an additional year of education. You must therefore be careful to inspect a regression table  for both the size and the statistical significance of each coefficient.

    The final rows report the number of observations, the $R^2$, and the adjusted $R^2$. Both the $R^2$ and the adjusted $R^2$ rise as variables are added, indicating that the later regressions explain more of the variation in wages. Remember, however, that a better fit does not make a coefficient causal. A causal interpretation still depends on whether relevant unobserved variables remain in the error term.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** regression table, statistical "
            "significance, significance level, t-statistic, "
            "omitted variable bias, R-squared, "
            "adjusted R-squared.\n\n"
            "**Concepts:** reading a regression table column by column and "
            "row by row, a coefficient changes when an added variable is correlated "
            "with it and also explains the outcome, "
            "statistical significance versus "
            "economic importance, and a high R-squared does not make a "
            "coefficient causal."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<span class="nav-soon">← Lecture 9 (coming soon)</span>'),
            mo.md('<span class="nav-soon">Lecture 11 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
