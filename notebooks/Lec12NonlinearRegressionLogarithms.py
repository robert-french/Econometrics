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
    app_title="Lecture 12: Nonlinear Regression, Logarithms",
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
            mo.md("# [Lecture 12](#top)"),
            mo.md("Nonlinear Regression: Logarithms"),
            mo.nav_menu(
                {
                    "#sec1": "1. What is a logarithm",
                    "#sec2": "2. Logarithms and percentage changes",
                    "#sec3": "3. Three regression models with logarithms",
                    "#sec4": "4. When to use logarithms",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec11NonlinearRegressionPolynomials.html" target="_self">← Lecture 11</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec13BinaryVariablesAndInteractionTerms.html" target="_self">Lecture 13 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 12: Nonlinear Regression, Logarithms
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

    [1. What is a logarithm](#sec1)<br>
    [2. Logarithms and percentage changes](#sec2)<br>
    [3. Three regression models with logarithms](#sec3)<br>
    [4. When to use logarithms](#sec4)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. What is a logarithm

    The *exponential function* raises the constant $e = 2.718\dots$ to a power, written $e^X$ or $\exp(X)$. The *natural logarithm* is its inverse, the power to which $e$ must be raised to produce $X$, written $\ln(X)$, so that $\ln(e^X) = X$. Because $e$ raised to any power is positive, $\ln(X)$ is defined only for $X > 0$. Experience is measured from one year upward in this lecture, so its logarithm is always defined.

    The natural logarithm rises quickly at first and then more slowly. Its slope at a point $X$ is $1/X$, so the curve is steep near zero and flattens as $X$ grows. That shape is what lets a logarithm turn a bending relationship into a straight-line one, and it is why the slope of a fitted log curve falls as $X$ rises.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Logarithms and percentage changes

    Logarithms appear so often in economics because a change in the logarithm of a variable is approximately its percentage change divided by 100. For a small change $\Delta X$,

    $$
    \ln(X + \Delta X) - \ln(X) \approx \frac{\Delta X}{X},
    $$

    the fractional change in $X$. A rise from 10 to 10.1 years of experience is a change of $0.1 / 10 = 0.01$, or one percent, and the change in $\ln(\text{experience})$ is almost exactly $0.01$. The approximation is close for small changes and drifts apart for large ones, as the demo below shows.

    A few properties follow from the definition and are worth keeping at hand. $\ln(1/X) = -\ln(X)$, $\ln(aX) = \ln(a) + \ln(X)$, and $\ln(X^a) = a\ln(X)$. The last of these is what makes an elasticity fall out of a log-log regression later in the lecture.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pct_change = mo.ui.slider(
        start=1, stop=100, step=1, value=10,
        label="Percentage rise in experience", show_value=True, full_width=False,
    )
    mo.vstack(
        [
            mo.md("Raise experience from a baseline of 10 years by the chosen percentage and compare the exact change in its logarithm with the percentage itself."),
            pct_change,
        ]
    )
    return (pct_change,)


@app.cell(hide_code=True)
def _(alt, mo, np, pct_change, pd):
    _p = float(pct_change.value) / 100.0
    _x0 = 10.0
    _x1 = _x0 * (1.0 + _p)
    _log_change = float(np.log(_x1) - np.log(_x0))  # = ln(1 + p)

    _grid = np.linspace(1.0, 30.0, 250)
    _xsc = alt.Scale(domain=[0.0, 30.0], nice=False)
    _ysc = alt.Scale(domain=[0.0, 3.6], nice=False)
    _curve = (
        alt.Chart(pd.DataFrame({"x": _grid, "lnx": np.log(_grid)}))
        .mark_line(color="orange", size=3, clip=True)
        .encode(x=alt.X("x:Q", scale=_xsc, title="Experience (years)"),
                y=alt.Y("lnx:Q", scale=_ysc, title="ln(experience)"))
    )
    _secant = (
        alt.Chart(pd.DataFrame({"x": [_x0, _x1], "lnx": [np.log(_x0), np.log(_x1)]}))
        .mark_line(color="#1f4e79", size=2.5, clip=True)
        .encode(x="x:Q", y="lnx:Q")
    )
    _ends = (
        alt.Chart(pd.DataFrame({"x": [_x0, _x1], "lnx": [np.log(_x0), np.log(_x1)]}))
        .mark_point(color="#1f4e79", size=90, filled=True, clip=True)
        .encode(x="x:Q", y="lnx:Q")
    )
    _chart = (_curve + _secant + _ends).properties(width=520, height=320)

    _gap = float(pct_change.value) - 100.0 * _log_change
    _msg = (
        f"Raising experience by {pct_change.value:.0f}% takes it from 10 to {_x1:.1f} years. "
        f"The natural log rises by {_log_change:.3f}, which is {100.0 * _log_change:.1f}% once "
        f"multiplied by 100, next to the actual {pct_change.value:.0f}% change. The two are "
        f"within {abs(_gap):.1f} percentage points here"
    )
    _msg += (
        ", almost identical for a small change." if pct_change.value <= 10
        else ", a gap that widens as the change grows."
    )
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:520px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_chart, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Three regression models with logarithms

    Putting a variable in logarithms changes how its coefficient is read. Three combinations come up, depending on whether the logarithm is applied to the independent variable, the dependent variable, or both. Each is estimated by OLS exactly as before, on the transformed variable. We fit all three to the same wage and experience data, and the switcher below draws each fitted relationship back in the original units so the shapes can be compared.

    ### <span style="color:#0b68cb">Linear-log: $\text{Wage} = \beta_0 + \beta_1\ln(\text{Exper}) + u$</span>

    A 1% rise in experience is associated with a change in the wage of $0.01\,\beta_1$ dollars. The fitted curve rises quickly at low experience and flattens, because the logarithm does.

    ### <span style="color:#0b68cb">Log-linear: $\ln(\text{Wage}) = \beta_0 + \beta_1\text{Exper} + u$</span>

    A one-year rise in experience is associated with a $100\,\beta_1$ percent change in the wage. Because that percentage is constant, the wage in dollars bends upward as experience grows.

    ### <span style="color:#0b68cb">Log-log: $\ln(\text{Wage}) = \beta_0 + \beta_1\ln(\text{Exper}) + u$</span>

    A 1% rise in experience is associated with a $\beta_1$ percent change in the wage. This $\beta_1$ is the *elasticity* of the wage with respect to experience, the percentage change in one variable for a one percent change in the other.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # Hourly wage and years of work experience for 300 workers, the same scenario
    # as Lecture 11. The data are generated from a log-log relationship, so the
    # wage rises with experience with diminishing returns (a concave, root-like
    # curve). Fixed seed for reproducibility; experience >= 1 so ln is defined.
    _rng = np.random.default_rng(1)
    n_workers = 300
    exper = _rng.uniform(1.0, 40.0, n_workers)
    _lnwage = np.log(6.0) + 0.5 * np.log(exper) + _rng.normal(0.0, 0.25, n_workers)
    wage = np.exp(_lnwage)
    return exper, wage


@app.cell(hide_code=True)
def _(mo):
    spec = mo.ui.dropdown(
        options=["Linear", "Linear-log", "Log-linear", "Log-log"],
        value="Linear",
        label="Specification",
    )
    mo.vstack(
        [
            mo.md("Choose a functional form and see the fitted relationship drawn through the wage and experience data, with the interpretation of its slope."),
            spec,
        ]
    )
    return (spec,)


@app.cell(hide_code=True)
def _(alt, exper, mo, np, pd, spec, wage):
    def _fit(_xv, _yv):
        _X = np.column_stack([np.ones(len(_xv)), _xv])
        _b, *_ = np.linalg.lstsq(_X, _yv, rcond=None)
        return float(_b[0]), float(_b[1])

    _grid = np.linspace(1.0, 40.0, 250)
    _name = spec.value
    if _name == "Linear":
        _b0, _b1 = _fit(exper, wage)
        _pred = _b0 + _b1 * _grid
        _msg = (
            f"Wage = {_b0:.1f} + {_b1:.2f}·experience. One more year adds \\${_b1:.2f} to the "
            f"predicted wage at every level. The straight line misses the curvature, sitting "
            f"above the data early and below it late."
        )
    elif _name == "Linear-log":
        _b0, _b1 = _fit(np.log(exper), wage)
        _pred = _b0 + _b1 * np.log(_grid)
        _msg = (
            f"Wage = {_b0:.1f} + {_b1:.1f}·ln(experience). A 1% rise in experience is associated "
            f"with about \\${_b1 / 100.0:.2f} more per hour. The curve is concave, flattening as "
            f"experience grows."
        )
    elif _name == "Log-linear":
        _b0, _b1 = _fit(exper, np.log(wage))
        _pred = np.exp(_b0 + _b1 * _grid)
        _msg = (
            f"ln(wage) = {_b0:.2f} + {_b1:.4f}·experience. One more year is associated with about "
            f"{100.0 * _b1:.1f}% higher wage. Back in dollars the curve bends upward, which "
            f"overshoots at high experience here."
        )
    else:
        _b0, _b1 = _fit(np.log(exper), np.log(wage))
        _pred = np.exp(_b0 + _b1 * np.log(_grid))
        _msg = (
            f"ln(wage) = {_b0:.2f} + {_b1:.2f}·ln(experience). Here {_b1:.2f} is the elasticity, so "
            f"a 1% rise in experience is associated with about {_b1:.2f}% higher wage. The curve is "
            f"concave and tracks the data."
        )

    _xsc = alt.Scale(domain=[0.0, 42.0], nice=False)
    _ysc = alt.Scale(domain=[0.0, 68.0], nice=False)
    _pts = (
        alt.Chart(pd.DataFrame({"exper": exper, "wage": wage}))
        .mark_circle(size=28, opacity=0.35, color="#1f4e79", clip=True)
        .encode(x=alt.X("exper:Q", scale=_xsc, title="Work experience (years)"),
                y=alt.Y("wage:Q", scale=_ysc, title="Hourly wage (dollars)"))
    )
    _line = (
        alt.Chart(pd.DataFrame({"exper": _grid, "wage": _pred}))
        .mark_line(color="orange", size=3, clip=True)
        .encode(x=alt.X("exper:Q", scale=_xsc), y=alt.Y("wage:Q", scale=_ysc))
    )
    _chart = (_pts + _line).properties(width=560, height=340)
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_chart, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. When to use logarithms

    Logarithms fit three situations. The first is when the economic model is multiplicative. A Cobb-Douglas relationship $Y = A\,X_1^{\beta_1} X_2^{\beta_2}$ becomes $\ln(Y) = \ln(A) + \beta_1\ln(X_1) + \beta_2\ln(X_2)$, linear in the coefficients and ready for OLS, with each slope an elasticity. The second is when percentage changes are the natural unit, as with growth rates of GDP or wages, where a percentage change carries more meaning than a change in levels. The third is when a variable ranges over very different sizes, such as firm sales from a corner shop to a national chain, where a one percent change is comparable across the range but a one-dollar change is not.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** exponential function, natural logarithm, linear-log "
            "model, log-linear model, log-log model, elasticity.\n\n"
            "**Key concepts covered:** the natural logarithm as the inverse of the "
            "exponential, defined only for positive values and with slope 1/X, why a change "
            "in a logarithm approximates a percentage change and where the approximation "
            "breaks down, the three log specifications and how each coefficient is "
            "interpreted, the log-log slope as an elasticity, and the situations that call "
            "for logarithms."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec11NonlinearRegressionPolynomials.html" target="_self">← Lecture 11</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec13BinaryVariablesAndInteractionTerms.html" target="_self">Lecture 13 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
