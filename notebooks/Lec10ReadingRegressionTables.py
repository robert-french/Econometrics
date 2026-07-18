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

    The table below is built from simulated data on 1,200 workers, generated so that the true effects are known and the estimates can be checked against them. The dependent variable is the hourly wage in dollars. We built the data so that one more year of education raises the wage by \$1.20 per hour, one more year of experience by \$0.15, and each standard deviation of parental income by \$2.50, and so that women earn \$2.00 per hour less than men with the same characteristics. Column (1) regresses the wage on education alone, and each later column adds one more independent variable, until column (4) includes all four.
    """)
    return


@app.cell(hide_code=True)
def _(mo, np):
    # Simulated wage data for 1,200 workers. The coefficients are known by
    # construction (true return to a year of education is $1.20/hour), so the
    # estimates in the table can be compared against the truth. Education is
    # correlated with parental income, which is the source of the omitted
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

    def _coef_cell(_m, _name, _border=""):
        if _name not in _m:
            return f"<td style='{_pad}{_border}'></td>"
        _b, _se = _m[_name]
        _inner = (
            f"{_b:.3f}{_stars(_b / _se)}"
            f"<br><span style='color:#6b7280;'>({_se:.3f})</span>"
        )
        return f"<td style='{_pad}{_border}'>{_inner}</td>"

    _rows = []
    for _name in var_order + ["Constant"]:
        _label = f"<td style='padding:3px 15px;text-align:left;'>{_name}</td>"
        _cells = "".join(_coef_cell(_m, _name) for _m in _maps)
        _rows.append(f"<tr>{_label}{_cells}</tr>")

    _top = "border-top:1px solid rgba(120,120,120,0.6);"

    def _stat_row(_label, _values, _border=""):
        _lab = f"<td style='padding:3px 15px;text-align:left;{_border}'>{_label}</td>"
        _cells = "".join(
            f"<td style='{_pad}{_border}'>{_v}</td>" for _v in _values
        )
        return f"<tr>{_lab}{_cells}</tr>"

    _rows.append(
        _stat_row("Observations", [f"{_f['n']:,}" for _f in fits], _border=_top)
    )
    _rows.append(_stat_row("R²", [f"{_f['r2']:.3f}" for _f in fits]))
    _rows.append(
        _stat_row("Adjusted R²", [f"{_f['ar2']:.3f}" for _f in fits])
    )

    _rule = "2px solid rgba(120,120,120,0.9)"
    _colhdr = "".join(
        f"<th style='{_pad}font-weight:600;'>({_i})</th>"
        for _i in range(1, _ncols + 1)
    )
    _table = (
        "<div style='overflow-x:auto;'>"
        f"<table style='border-collapse:collapse;margin:1rem auto;font-size:0.9rem;"
        f"line-height:1.25;border-top:{_rule};border-bottom:{_rule};min-width:560px;'>"
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
        "and three at the 1% level."
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

    Read across the education row. In column (1) the coefficient on education is \$2.00 per hour for each additional year, but we built the data so the true return is \$1.20. The estimate is too large by \$0.80 because education is the only variable in the regression. Parental income is left in the error term, and it is correlated with education, since higher-income families tend to have children with more schooling, while it also raises wages on its own. This is *omitted variable bias* from Lecture 8. The bias is positive because parental income moves in the same direction with both education and the wage, so the education coefficient absorbs part of parental income's effect and overstates the return.

    Column (2) adds experience, and the education coefficient does not move, holding at \$2.00. Experience is uncorrelated with education, so leaving it out never biased the education coefficient, and adding it changes nothing for education. A variable shifts another coefficient only when the two variables are correlated.

    Column (3) adds parental income, and the education coefficient falls to \$1.14, close to the true \$1.20. Holding parental income fixed compares workers with similar family backgrounds, which strips out the bias. Parental income is a *confounder*, a variable correlated with a regressor of interest that also affects the outcome, and controlling for it is the reason to prefer multiple regression over a simple regression when the confounder is available.

    Column (4) adds an indicator for female workers. The education coefficient barely moves, from \$1.14 to \$1.16, because sex is roughly uncorrelated with education in these data. Women are estimated to earn \$1.94 per hour less than men with the same education, experience, and family background, a large and precisely estimated gap that still leaves the education coefficient alone.

    The plot below tracks the education coefficient across the four columns, with the vertical bars showing a 95% confidence interval and the orange line marking the true return of \$1.20.
    """)
    return


@app.cell(hide_code=True)
def _(alt, fits, mo, pd):
    _labels = [f"({_i})" for _i in range(1, len(fits) + 1)]
    _b = [float(_f["b"][1]) for _f in fits]
    _se = [float(_f["se"][1]) for _f in fits]
    _df = pd.DataFrame(
        {
            "spec": _labels,
            "b": _b,
            "lo": [_bi - 1.96 * _si for _bi, _si in zip(_b, _se)],
            "hi": [_bi + 1.96 * _si for _bi, _si in zip(_b, _se)],
        }
    )

    _xsc = alt.X("spec:N", title="Column", sort=_labels)
    _ysc = alt.Scale(domain=[0.6, 2.4], nice=False)
    _bars = (
        alt.Chart(_df)
        .mark_rule(color="#1f4e79", size=2)
        .encode(x=_xsc, y=alt.Y("lo:Q", scale=_ysc, title="Coefficient on education (dollars per year)"), y2="hi:Q")
    )
    _pts = (
        alt.Chart(_df)
        .mark_point(color="#1f4e79", size=90, filled=True)
        .encode(x=_xsc, y=alt.Y("b:Q", scale=_ysc))
    )
    _truth = (
        alt.Chart(pd.DataFrame({"v": [1.20]}))
        .mark_rule(color="orange", strokeDash=[6, 4], size=2)
        .encode(y="v:Q")
    )
    _chart = (_truth + _bars + _pts).properties(width=460, height=300)

    _caption = mo.md(
        "<span style='display:block;margin:0.4rem auto 1rem;max-width:520px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        "In columns (1) and (2) the confidence interval sits well above the true "
        "\\$1.20, because parental income is omitted and the estimate is biased "
        "upward. Once parental income enters in columns (3) and (4), the interval "
        "drops and now covers the truth.</span>"
    )
    mo.vstack([mo.hstack([_chart], justify="center"), _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Reading fit and significance

    The standard error below each coefficient measures its sampling uncertainty. Dividing a coefficient by its standard error gives the *t-statistic*, and a coefficient more than about 1.96 standard errors from zero is *statistically significant* at the 5% level, meaning a true value of zero would rarely produce an estimate this far from zero. The asterisks encode this, with one star for significance at the 10% level, two at the 5% level, and three at the 1% level. Every coefficient in the table carries three stars, so each is far from zero relative to its standard error. The education coefficient in column (4), for instance, has a t-statistic of about \$1.16 / \$0.08, or roughly 15.

    Statistical significance is not the same as importance. A coefficient can be statistically significant but too small to matter in practice, or economically large but estimated too imprecisely to be sure of. The experience coefficient of \$0.16 per year is highly significant, yet a year of experience adds far less to the wage than a year of education. Reading a table means checking both whether a coefficient is distinguishable from zero and whether its size matters in the units of the problem.

    The standard errors themselves shift across columns. The standard error on education is 0.072 in column (1) and 0.070 in column (2). Adding experience explains more of the variation in wages, which shrinks the estimated spread of the error term and tightens every coefficient a little. From column (2) to column (3) the education standard error rises to 0.078, because parental income is correlated with education, so once it is included the data hold less independent variation in education and its coefficient is pinned down less precisely. This is *multicollinearity*, the price of including variables that move together.

    The last two rows summarize how well the regression fits. The *R-squared* is the share of the variation in wages the regression explains, and it rises in every column, from 0.392 to 0.581, because adding a variable can never lower the explained share. That makes R-squared useless for deciding whether a variable belongs, since it rewards adding variables whether or not they matter. The *adjusted R-squared* corrects for this by charging a penalty for each variable added. It also rises here, from 0.391 to 0.580, which says every variable added enough explanatory power to outweigh its penalty. Had we instead added a variable unrelated to wages, the R-squared would still have ticked up while the adjusted R-squared fell.

    A high R-squared does not mean the coefficients can be read as causal. Column (1) explains 39% of the variation in wages yet reports an education effect nearly double the truth, while column (3) explains more and reports a credible one. Fit measures how closely the regression tracks the data. Whether a coefficient recovers a causal effect depends on the omitted variable bias from Section 2, not on the R-squared.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** regression table, standard error, statistical "
            "significance, significance level, t-statistic, omitted variable bias, "
            "confounder, multicollinearity, R-squared, adjusted R-squared.\n\n"
            "**Key concepts covered:** reading a regression table column by column and "
            "row by row, a coefficient changes when an added variable is correlated "
            "with it and also explains the outcome (omitted variable bias from a "
            "confounder), adding a correlated variable inflates a coefficient's "
            "standard error through multicollinearity, statistical significance versus "
            "economic importance, R-squared always rises with more variables while "
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
