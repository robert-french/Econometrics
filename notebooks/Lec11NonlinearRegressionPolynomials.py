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
    app_title="Lecture 11: Nonlinear Regression, Polynomials",
    css_file="marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt

    return alt, mo, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: block; margin-bottom: 1.5em;">Course home</a>'),
            mo.md("# [Lecture 11](#top)"),
            mo.md("Nonlinear Regression: Polynomials"),
            mo.nav_menu(
                {
                    "#sec1": "1. Modeling a nonlinear relationship",
                    "#sec2": "2. Estimating and reading the quadratic model",
                    "#sec3": "3. The effect of experience depends on its level",
                    "#sec4": "4. Testing whether the relationship is nonlinear",
                    "#sec5": "5. Higher-order polynomials and overfitting",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec10ReadingRegressionTables.html" target="_self">← Lecture 10</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec12NonlinearRegressionLogarithms.html" target="_self">Lecture 12 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 11: Nonlinear Regression, Polynomials
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

    [1. Modeling a nonlinear relationship](#sec1)<br>
    [2. Estimating and reading the quadratic model](#sec2)<br>
    [3. The effect of experience depends on its level](#sec3)<br>
    [4. Testing whether the relationship is nonlinear](#sec4)<br>
    [5. Higher-order polynomials and overfitting](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Modeling a nonlinear relationship

    Wages do not rise with work experience at a steady rate. A worker gains a lot in the first years on the job, and the gains taper off later, so the relationship between the wage and experience bends. A straight line adds the same amount to the predicted wage for every extra year, so it cannot follow that bend. It is forced to compromise, running above the data at the ends and below it in the middle.

    We can still fit a curve with OLS by building a second independent variable from the first. Alongside experience we include experience squared, and estimate

    $$
    \text{Wage} = \beta_0 + \beta_1\,\text{Exper} + \beta_2\,\text{Exper}^2 + u.
    $$

    This is a *quadratic regression*, a regression whose fitted line is a parabola rather than a straight line. It is still linear in the coefficients $\beta_0$, $\beta_1$, and $\beta_2$, so OLS estimates it exactly like the multiple regressions of Lectures 8 and 9, treating experience and experience squared as two separate independent variables. The slider below fits a *polynomial* of the degree you choose, a sum of powers of experience up to that degree, and reports how well it fits. Degree one is the straight line, and degree two is the quadratic above.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # Hourly wage and years of work experience for 100 workers. The wage rises
    # with experience but with diminishing returns, peaking near 31 years, so a
    # quadratic (not a line) describes it. The sample is deliberately modest so
    # the degrees-of-freedom penalty in the adjusted R-squared bites as the
    # polynomial degree climbs. Fixed seed for reproducibility.
    _rng = np.random.default_rng(116)
    n_workers = 100
    exper = _rng.uniform(1.0, 40.0, n_workers)
    wage = 8.0 + 1.10 * exper - 0.017 * exper**2 + _rng.normal(0.0, 3.0, n_workers)
    return exper, n_workers, wage


@app.cell(hide_code=True)
def _(mo):
    poly_degree = mo.ui.slider(
        start=1, stop=20, step=1, value=1,
        label="Polynomial degree", show_value=True, full_width=False,
    )
    mo.vstack(
        [
            mo.md("Set the degree of the polynomial fitted to the wage data and watch the fit and the two fit measures change."),
            poly_degree,
        ]
    )
    return (poly_degree,)


@app.cell(hide_code=True)
def _(alt, exper, mo, n_workers, np, pd, poly_degree, wage):
    _deg = int(poly_degree.value)

    # Fit in the Chebyshev basis, which stays well conditioned all the way to
    # degree 20 where raw powers of experience would not. A polynomial of a
    # given degree spans the same functions in either basis, so the fitted
    # values, and with them the R-squared, are unchanged.
    _series = np.polynomial.Chebyshev.fit(exper, wage, _deg)

    _grid = np.linspace(1.0, 40.0, 250)
    _fit = _series(_grid)
    _pred = _series(exper)
    _ssr = float(((wage - _pred) ** 2).sum())
    _tss = float(((wage - wage.mean()) ** 2).sum())
    _r2 = 1.0 - _ssr / _tss
    _ar2 = 1.0 - (_ssr / (n_workers - _deg - 1)) / (_tss / (n_workers - 1))

    _xsc = alt.Scale(domain=[0.0, 42.0], nice=False)
    _ysc = alt.Scale(domain=[0.0, 36.0], nice=False)
    _pts = (
        alt.Chart(pd.DataFrame({"exper": exper, "wage": wage}))
        .mark_circle(size=28, opacity=0.35, color="#1f4e79", clip=True)
        .encode(
            x=alt.X("exper:Q", scale=_xsc, title="Work experience (years)"),
            y=alt.Y("wage:Q", scale=_ysc, title="Hourly wage (dollars)"),
        )
    )
    _line = (
        alt.Chart(pd.DataFrame({"exper": _grid, "wage": _fit}))
        .mark_line(color="orange", size=3, clip=True)
        .encode(x=alt.X("exper:Q", scale=_xsc), y=alt.Y("wage:Q", scale=_ysc))
    )
    _chart = (_pts + _line).properties(width=560, height=340)

    # The estimated specification, rebuilt each time the slider moves. Degrees
    # above four are abbreviated with a middle ellipsis so the line stays short.
    _terms = [r"\beta_0"]
    if _deg <= 4:
        for _j in range(1, _deg + 1):
            _pow = "" if _j == 1 else f"^{_j}"
            _terms.append(rf"\beta_{{{_j}}}\text{{Exper}}{_pow}")
    else:
        _terms.append(r"\beta_1\text{Exper}")
        _terms.append(r"\beta_2\text{Exper}^2")
        _terms.append(r"\cdots")
        _terms.append(rf"\beta_{{{_deg}}}\text{{Exper}}^{{{_deg}}}")
    _equation = mo.md(
        r"$$\text{Wage} = " + " + ".join(_terms) + r" + u$$"
    )

    if _deg == 1:
        _msg = (
            f"A straight line misses the bend, running above the data at the ends and "
            f"below it in the middle. Its R-squared is {_r2:.3f} and its adjusted "
            f"R-squared is {_ar2:.3f}. Raise the degree to 2 to let the fit curve."
        )
    elif _deg == 2:
        _msg = (
            f"The quadratic follows the rise and the flattening, with R-squared {_r2:.3f} "
            f"and adjusted R-squared {_ar2:.3f}, both well above the straight line. Raise "
            f"the degree further to see what more flexibility does."
        )
    else:
        _msg = (
            f"At degree {_deg} the curve wiggles to chase individual points. The R-squared "
            f"has crept up to {_r2:.3f}, because another term can never worsen the fit, but "
            f"the adjusted R-squared has fallen to {_ar2:.3f}. The extra terms are fitting "
            f"noise, not signal."
        )
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_equation, _chart, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Estimating and reading the quadratic model

    The degree-two fit gives $\hat{\beta}_0 = 7.7$, $\hat{\beta}_1 = 1.18$, and $\hat{\beta}_2 = -0.019$, with experience in years and the wage in dollars per hour. The negative coefficient on experience squared is what bends the fitted line back down as experience grows. Its R-squared is 0.76, up from 0.59 for the straight line, so the curve tracks the data more closely.

    The three coefficients no longer have separate simple meanings. In a straight-line regression $\hat{\beta}_1$ is the slope, the change in the predicted wage for one more year of experience. That is no longer true here, because experience appears in two terms at once. A one-year rise in experience changes both $\text{Exper}$ and $\text{Exper}^2$, so $\hat{\beta}_1$ and $\hat{\beta}_2$ move the prediction together. To read the effect of experience we have to work from the fitted curve, which is what Section 3 does.

    Bending the fitted line changes its shape, not what is required to read it causally. A quadratic is still a multiple regression, so the least squares assumptions from Lectures 6 and 9 carry over word for word. The first of them is the one that does the work, requiring that the error have mean zero at every combination of the independent variables,

    $$
    \mathbb{E}[u \mid \text{Exper}, \text{Exper}^2] = 0.
    $$

    Since both independent variables are built from experience, this amounts to requiring that nothing left in the error term vary systematically with experience or with any power of it. Suppose workers who stay in the labour force longest are also the more able ones, and that ability raises the wage at any level of experience. Ability then sits in the error and moves with experience, the assumption fails, and the fitted curve is biased in exactly the way Lecture 8 described for a straight line. A more flexible functional form buys a better description of the shape of the relationship. It does nothing about omitted variable bias.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. The effect of experience depends on its level

    To find the effect of experience at a given level, compare the predicted wage before and after the change. For a rise from $\text{Exper}$ to $\text{Exper} + \Delta$, the predicted change is

    $$
    \Delta\hat{\text{Wage}} = \left(\hat{\beta}_1(\text{Exper}+\Delta) + \hat{\beta}_2(\text{Exper}+\Delta)^2\right) - \left(\hat{\beta}_1\text{Exper} + \hat{\beta}_2\text{Exper}^2\right).
    $$

    Dividing by $\Delta$ gives the average slope of the curve over that stretch, the extra wage per extra year. Unlike a straight line, this slope depends on where you start. The explorer below lets you set both the starting level of experience and the size of $\Delta$. Early in a career a given rise adds a large amount to the wage. Near the top of the curve it adds almost nothing, and past the peak the predicted wage falls. Widening $\Delta$ averages the slope over a longer stretch, so a span that crosses the peak mixes the rising and falling parts together.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Ranges are chosen so the end of the span, start + delta, never exceeds the
    # 40 years covered by the data, which keeps the two sliders independent.
    secant_start = mo.ui.slider(
        start=1, stop=30, step=1, value=8,
        label="Starting experience (years)", show_value=True, full_width=False,
    )
    secant_delta = mo.ui.slider(
        start=1, stop=10, step=1, value=5,
        label="Size of the increase, Δ (years)", show_value=True, full_width=False,
    )
    mo.vstack(
        [
            mo.md("Set where the increase in experience starts and how large it is, then read the slope of the curve over that stretch."),
            secant_start,
            secant_delta,
        ]
    )
    return secant_delta, secant_start


@app.cell(hide_code=True)
def _(alt, exper, mo, np, pd, secant_delta, secant_start, wage):
    _quad = np.polyfit(exper, wage, 2)  # [b2, b1, b0], highest power first
    _peak = -_quad[1] / (2.0 * _quad[0])

    def _yhat(_x):
        return float(np.polyval(_quad, _x))

    _x0 = float(secant_start.value)
    _delta = float(secant_delta.value)
    _x1 = _x0 + _delta
    _y0, _y1 = _yhat(_x0), _yhat(_x1)
    _slope = (_y1 - _y0) / _delta

    _grid = np.linspace(1.0, 40.0, 250)
    _xsc = alt.Scale(domain=[0.0, 42.0], nice=False)
    _ysc = alt.Scale(domain=[0.0, 36.0], nice=False)
    _curve = (
        alt.Chart(pd.DataFrame({"exper": _grid, "wage": np.polyval(_quad, _grid)}))
        .mark_line(color="orange", size=3, clip=True)
        .encode(x=alt.X("exper:Q", scale=_xsc, title="Work experience (years)"),
                y=alt.Y("wage:Q", scale=_ysc, title="Hourly wage (dollars)"))
    )
    _cloud = (
        alt.Chart(pd.DataFrame({"exper": exper, "wage": wage}))
        .mark_circle(size=22, opacity=0.18, color="#1f4e79", clip=True)
        .encode(x="exper:Q", y="wage:Q")
    )
    _secant = (
        alt.Chart(pd.DataFrame({"exper": [_x0, _x1], "wage": [_y0, _y1]}))
        .mark_line(color="#1f4e79", size=2.5, clip=True)
        .encode(x="exper:Q", y="wage:Q")
    )
    _ends = (
        alt.Chart(pd.DataFrame({"exper": [_x0, _x1], "wage": [_y0, _y1]}))
        .mark_point(color="#1f4e79", size=90, filled=True, clip=True)
        .encode(x="exper:Q", y="wage:Q")
    )
    _peak_rule = (
        alt.Chart(pd.DataFrame({"v": [_peak]}))
        .mark_rule(color="#9aa5b1", strokeDash=[4, 3], size=1.5)
        .encode(x="v:Q")
    )
    _chart = (_cloud + _peak_rule + _curve + _secant + _ends).properties(width=560, height=340)

    if _slope > 0.35:
        _tail = "a large raise, because the curve is steep early in a career."
    elif _slope > 0.05:
        _tail = "a smaller raise, because the curve is flattening."
    elif _slope >= -0.05:
        _tail = "almost nothing, because this stretch straddles the peak of the curve near 31 years."
    else:
        _tail = "a pay cut, because past the peak the predicted wage falls."
    _msg = (
        f"Going from {_x0:.0f} to {_x1:.0f} years of experience, a rise of {_delta:.0f} "
        f"year{'' if _delta == 1 else 's'}, changes the predicted wage by "
        f"\\${_y1 - _y0:.2f}, a slope of \\${_slope:.2f} per year. That is {_tail}"
    )
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + " The grey dashed line marks the peak.</span>"
    )
    mo.vstack([_chart, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Testing whether the relationship is nonlinear

    If $\beta_2 = 0$, the squared term drops out and the model is a straight line. So the question of whether the relationship curves is the hypothesis test $H_0: \beta_2 = 0$ against $H_1: \beta_2 \neq 0$, run exactly as in Lectures 4 and 9. Divide the estimate by its standard error to form the t-statistic, then compare the p-value with the significance level.

    In the wage data, $\hat{\beta}_2 = -0.019$ with a standard error of about $0.0023$, so the t-statistic is near $-8$ and the p-value is far below 0.01. We reject the straight line and conclude that experience enters the wage nonlinearly. The adjusted R-squared points the same way, rising from 0.590 for the line to 0.757 for the quadratic.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Higher-order polynomials and overfitting

    The same idea extends to a *polynomial of degree $r$*, which adds experience cubed, to the fourth power, and so on up to the $r$-th power,

    $$
    \text{Wage} = \beta_0 + \beta_1\text{Exper} + \beta_2\text{Exper}^2 + \dots + \beta_r\text{Exper}^r + u.
    $$

    A higher degree makes the curve more flexible, so it can bend in more places. Flexibility has a cost. Raise the degree on the slider in Section 1 above two and the curve begins to wiggle, chasing individual points instead of the overall shape. This is *overfitting*, fitting the noise in one sample rather than the pattern that would repeat in new data. The two fit measures split apart as it happens. The R-squared keeps inching up, from 0.762 at the quadratic to 0.779 at degree twenty, because adding a term can never worsen the in-sample fit. The *adjusted R-squared*, which charges for each added term, peaks at the quadratic at 0.757 and falls away to 0.724 by degree twenty. The extra nineteen terms buy a better fit to this sample and a worse description of the pattern behind it.

    A few rules of thumb help choose the degree. One is to add terms until the highest one is no longer statistically significant. Another is to watch the adjusted R-squared and stop when it stops rising. A third is to let the economics of the problem set the degree. For the wage profile, the quadratic is enough.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** quadratic regression, polynomial, polynomial of "
            "degree r, overfitting, adjusted R-squared.\n\n"
            "**Key concepts covered:** modeling a nonlinear relationship by adding powers "
            "of an independent variable and estimating with OLS, why the coefficients of a "
            "quadratic no longer read as a single slope, computing the effect of a change "
            "in X as a difference in predicted values so the slope depends on the level of "
            "X, why a flexible functional form still needs the least squares assumptions "
            "and does not cure omitted variable bias, testing for nonlinearity with the "
            "hypothesis that the squared term is zero, and how higher-degree polynomials "
            "overfit while the adjusted R-squared, not the R-squared, signals when to stop."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec10ReadingRegressionTables.html" target="_self">← Lecture 10</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec12NonlinearRegressionLogarithms.html" target="_self">Lecture 12 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
