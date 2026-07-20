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

__generated_with = "0.23.9"
__preliminary__ = True
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

    return alt, mo, np, pd, stats


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: block; margin-bottom: 1.5em;">Course home</a>'),
            mo.md("# [Lecture 10](#top)"),
            mo.md("Reading Regression Tables"),
            mo.nav_menu(
                {
                    "#sec1": "1. The anatomy of a regression table",
                    "#sec2": "2. Why the coefficients change across columns",
                    "#sec3": "3. Reading fit and significance",
                },
                orientation="vertical",
            ),
        ],
        width="260px",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec9ControlVariablesAndInference.html" target="_self">← Lecture 9</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec11NonlinearRegressionPolynomials.html" target="_self">Lecture 11 →</a>'),
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

    [1. The anatomy of a regression table](#sec1)<br>
    [2. Why the coefficients change across columns](#sec2)<br>
    [3. Reading fit and significance](#sec3)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. The anatomy of a regression table

    A *regression table* reports several regressions side by side so their results can be compared in one place. Each column is one regression with its own set of independent variables, and each row is one variable. Reading down a column describes a single regression. Reading across a row shows how the coefficient on that variable changes as other variables are added.

    The table below reports four regressions estimated on the same 1,200 workers. The dependent variable is the hourly wage in dollars, and the independent variables are years of education, years of work experience, parental income measured in standard deviations from its mean, and an indicator equal to one for women. Column (1) regresses the wage on education alone, and each later column adds one more independent variable, until column (4) includes all four. Hovering over any row shows what that coefficient or statistic means.
    """)
    return


@app.cell(hide_code=True)
def _(mo, np):
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
        "Education (years)": "Estimated change in the hourly wage for one more year of education, holding the other variables in the column fixed.",
        "Experience (years)": "Estimated change in the hourly wage for one more year of work experience, holding the other variables fixed.",
        "Parental income (SD)": "Estimated change in the hourly wage for a one standard deviation rise in parental income, holding the other variables fixed.",
        "Female": "Estimated wage gap for women relative to men with the same values of the other variables.",
        "Constant": "The predicted hourly wage when every independent variable in the column equals zero.",
        "Observations": "The number of workers used to estimate the regression.",
        "R²": "The share of the variation in wages the regression explains, from 0 to 1.",
        "Adjusted R²": "The R-squared with a penalty for each independent variable, so a variable that does not help lowers it.",
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
        "One star marks significance at the 10% level, two at the 5% level, "
        "and three at the 1% level. Hover over a row for its definition."
        "</span>"
    )
    mo.vstack([mo.md(_table), _note])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each coefficient cell holds two numbers. The top number is the estimated coefficient, the change in the predicted wage for a one-unit increase in that variable, holding the other variables in that column fixed. The number in parentheses below it is the *standard error*, which measures how much the coefficient would move from one random sample to the next. The asterisks flag *statistical significance*, covered in Section 3. The last three rows report the number of observations, the *R-squared*, and the *adjusted R-squared*, three summaries of the regression as a whole that Section 3 also explains.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Why the coefficients change across columns

    Read across the education row. The coefficient is \$2.00 per hour for each additional year in column (1), and when parental income enters in column (3) it drops to \$1.14. That change is *omitted variable bias*, the effect from Lecture 8. With education the only independent variable, parental income sits in the error term, and it is correlated with education, since higher-income families tend to have children with more schooling, while it also raises wages on its own. Lecture 8 showed that omitting such a variable pulls the slope estimate away from the effect it is meant to measure,

    $$
    \hat{\beta}_1 \overset{p}{\to} \beta_1 + \underbrace{\rho_{Xu}\cdot\frac{\sigma_u}{\sigma_X}}_{\text{bias}},
    $$

    where $\rho_{Xu}$ is the correlation between education and the error term, $\sigma_u$ is the standard deviation of the error, and $\sigma_X$ is the standard deviation of education. Here the omitted parental income raises wages and moves in the same direction as education, so $\rho_{Xu}$ is positive, the bias is positive, and column (1) overstates the return to education.

    Column (2) adds experience, and the education coefficient does not move, holding at \$2.00. Experience is uncorrelated with education, so it was never part of education's bias term, and adding it changes nothing for education. A variable shifts another coefficient only when the two variables are correlated.

    Column (3) adds parental income itself, and the education coefficient falls to \$1.14. Holding parental income fixed compares workers with similar family backgrounds, which removes the bias term from the education slope. Parental income is a *confounder*, a variable correlated with a regressor of interest that also affects the outcome, and controlling for it is the reason to prefer multiple regression over a simple regression.

    Column (4) adds an indicator for female workers, and the education coefficient barely moves, from \$1.14 to \$1.16, because sex is close to uncorrelated with education here. Women are estimated to earn \$1.94 per hour less than men with the same education, experience, and family background, a large gap that still leaves the education coefficient alone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Reading fit and significance

    The standard error below each coefficient measures its sampling uncertainty, and two summaries from Lecture 4 come straight from it. The *t-statistic* is the coefficient divided by its standard error, and a coefficient more than about 1.96 standard errors from zero is *statistically significant* at the 5% level. A 95% *confidence interval* is the coefficient plus or minus about 1.96 standard errors, the range of values the data leave plausible, and a coefficient is significant at the 5% level exactly when its interval excludes zero. The stars report significance directly, one for the 10% level, two for the 5% level, and three for the 1% level, and every coefficient in the table carries three. The education coefficient in column (4), for instance, is \$1.16 with a standard error of \$0.08, so its t-statistic is near 15 and its 95% interval runs from about \$1.01 to \$1.31, nowhere near zero.

    The confidence interval also shows how much the controls matter. For education it runs from about \$1.86 to \$2.14 in column (1) and from about \$1.01 to \$1.31 in column (4), two ranges that do not overlap, so the controls move the estimate well beyond sampling noise. Significance is still not the same as importance. The experience coefficient of \$0.16 per year is highly significant, yet a year of experience adds far less to the wage than a year of education, so a table must be read for the size of an effect as well as its significance.

    The standard errors themselves shift across columns. The education standard error falls from 0.072 in column (1) to 0.070 in column (2), because experience explains more of the variation in wages and tightens every coefficient. From column (2) to column (3) it rises to 0.078, because parental income is correlated with education, so the data hold less independent variation in education once it is included. This is *multicollinearity*, the loss of precision from including variables that move together, covered in Lecture 9.

    The last two rows summarize fit. The *R-squared*, introduced in Lecture 5, is the share of the variation in wages the regression explains, and it rises in every column, from 0.392 to 0.581, because adding a variable can never lower the explained share. That makes it useless for deciding whether a variable belongs. The *adjusted R-squared* from Lecture 8 charges a penalty for each variable added. It also rises here, from 0.391 to 0.580, so every variable earned its place. Had we instead added a variable unrelated to wages, the R-squared would still have edged up while the adjusted R-squared fell.

    A high R-squared does not make a coefficient causal. Column (1) explains 39% of the variation in wages, yet its education coefficient is biased upward by the omission of parental income, while column (3) explains more and controls for that confounder. Fit measures how closely the regression tracks the data. Whether a coefficient recovers a causal effect depends on the omitted variable bias from Section 2, not on the R-squared.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** regression table, standard error, statistical "
            "significance, significance level, t-statistic, confidence interval, "
            "omitted variable bias, confounder, multicollinearity, R-squared, "
            "adjusted R-squared.\n\n"
            "**Key concepts covered:** reading a regression table column by column and "
            "row by row, a coefficient changes when an added variable is correlated "
            "with it and also explains the outcome (omitted variable bias from a "
            "confounder), adding a correlated variable inflates a coefficient's "
            "standard error through multicollinearity, statistical significance versus "
            "economic importance, a coefficient is significant when its confidence "
            "interval excludes zero, R-squared always rises with more variables while "
            "adjusted R-squared penalizes them, and a high R-squared does not make a "
            "coefficient causal."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec9ControlVariablesAndInference.html" target="_self">← Lecture 9</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec11NonlinearRegressionPolynomials.html" target="_self">Lecture 11 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
