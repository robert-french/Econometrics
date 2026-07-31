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
                    "#sec2": "2. Logarithms and percent changes",
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
    mo.md(r"""
    Lecture 11 modeled a curved relationship by adding powers of an independent variable. This lecture introduces a second type of nonlinear regression, the *logarithmic regression*, which instead transforms variables with the logarithm function and reads its coefficients as percent changes. We begin with the logarithm function itself, then turn to the regressions that use it.
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
    [2. Logarithms and percent changes](#sec2)<br>
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

    The plot below draws the two functions together. Because they are inverses, each is the mirror image of the other across the dashed 45-degree line.
    """)
    return


@app.cell(hide_code=True)
def _(alt, mo, np, pd):
    # Static picture of exp and ln with the 45-degree line. The chart is square
    # with identical axis domains so the mirror symmetry of the two inverse
    # functions is not distorted.
    _gx = np.linspace(-4.0, 1.9, 300)
    _gl = np.linspace(0.02, 6.0, 300)
    _dom = alt.Scale(domain=[-4.0, 6.0], nice=False)
    _exp = (
        alt.Chart(pd.DataFrame({"x": _gx, "y": np.exp(_gx)}))
        .mark_line(color="#1f4e79", size=3, clip=True)
        .encode(x=alt.X("x:Q", scale=_dom, title="X"),
                y=alt.Y("y:Q", scale=_dom, title=None))
    )
    _ln = (
        alt.Chart(pd.DataFrame({"x": _gl, "y": np.log(_gl)}))
        .mark_line(color="orange", size=3, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _diag = (
        alt.Chart(pd.DataFrame({"x": [-4.0, 6.0], "y": [-4.0, 6.0]}))
        .mark_line(color="#9aa5b1", strokeDash=[4, 3], size=1.5, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _labels = (
        alt.Chart(pd.DataFrame({
            "x": [0.35, 5.0], "y": [4.4, 2.15],
            "t": ["exp(X)", "ln(X)"],
            "c": ["#1f4e79", "orange"],
        }))
        .mark_text(fontSize=14, fontWeight="bold", align="left")
        .encode(x="x:Q", y="y:Q", text="t:N", color=alt.Color("c:N", scale=None))
    )
    _chart = (_diag + _exp + _ln + _labels).properties(width=400, height=400)
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:520px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        "The exponential function (blue) and the natural logarithm (orange). "
        "The exponential is defined for every value of X but is always positive; "
        "the logarithm is defined only for positive X but takes every value. "
        "Reflecting either curve across the dashed 45-degree line produces the other.</span>"
    )
    mo.vstack([_chart, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Logarithms and percent changes

    Logarithms appear so often in economics because a change in the logarithm of a variable is approximately its percent change divided by 100. For a small change $\Delta X$,

    $$
    \ln(X + \Delta X) - \ln(X) \approx \frac{\Delta X}{X},
    $$

    the fractional change in $X$. A rise from 10 to 10.1 years of experience is a change of $0.1 / 10 = 0.01$, or one percent, and the change in $\ln(\text{experience})$ is almost exactly $0.01$. The approximation is close for small changes and drifts apart for large ones, as the plot below shows.

    When comparing percent changes, keep the units straight. A *percent* change is a relative change, while a difference between two percent changes is measured in *percentage points*. Going from a 10 percent rise to a 12 percent rise is an increase of 2 percentage points, not 2 percent. The caption below uses percentage points to report how far the change in the logarithm is from the percent change it approximates.

    A few properties follow from the definition and are worth keeping at hand. $\ln(1/X) = -\ln(X)$, $\ln(aX) = \ln(a) + \ln(X)$, and $\ln(X^a) = a\ln(X)$. The last of these is what makes an elasticity fall out of a log-log regression later in the lecture.

    In the plot, the brace along the horizontal axis marks the change in experience, and the brace along the vertical axis marks the resulting change in its logarithm.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Starting experience runs from 4 (lower starts crowd the plot annotations
    # into the steep corner of the log curve) to 20, so the end point, at most
    # double the start, stays inside the 40 years drawn on the chart.
    base_exper = mo.ui.slider(
        start=4, stop=20, step=1, value=10,
        label="Starting experience (years)", show_value=True, full_width=False,
    )
    pct_change = mo.ui.slider(
        start=-50, stop=100, step=1, value=10,
        label="Percent change in experience", show_value=True, full_width=False,
    )
    mo.vstack(
        [
            mo.md("Choose where experience starts and the percent change applied to it, then compare the resulting change in the logarithm with the percent change itself."),
            base_exper,
            pct_change,
        ]
    )
    return base_exper, pct_change


@app.cell(hide_code=True)
def _(alt, base_exper, mo, np, pct_change, pd):
    _p = float(pct_change.value) / 100.0
    _x0 = float(base_exper.value)
    _x1 = _x0 * (1.0 + _p)
    _y0, _y1 = float(np.log(_x0)), float(np.log(_x1))
    _log_change = _y1 - _y0  # = ln(1 + p)

    _grid = np.linspace(1.0, 40.0, 250)
    _xsc = alt.Scale(domain=[0.0, 42.0], nice=False)
    _ysc = alt.Scale(domain=[0.0, 3.9], nice=False)
    _curve = (
        alt.Chart(pd.DataFrame({"x": _grid, "lnx": np.log(_grid)}))
        .mark_line(color="orange", size=3, clip=True)
        .encode(x=alt.X("x:Q", scale=_xsc, title="Experience (years)"),
                y=alt.Y("lnx:Q", scale=_ysc, title="ln(experience)"))
    )
    _secant = (
        alt.Chart(pd.DataFrame({"x": [_x0, _x1], "lnx": [_y0, _y1]}))
        .mark_line(color="#1f4e79", size=2.5, clip=True)
        .encode(x="x:Q", y="lnx:Q")
    )
    _ends = (
        alt.Chart(pd.DataFrame({"x": [_x0, _x1], "lnx": [_y0, _y1]}))
        .mark_point(color="#1f4e79", size=90, filled=True, clip=True)
        .encode(x="x:Q", y="lnx:Q")
    )

    # Dashed guides from the end points across to the vertical axis and down to
    # the horizontal axis, stopping at the braces.
    _guides = (
        alt.Chart(pd.DataFrame({
            "x": [_x0, 0.85, _x1, 0.85, _x0, _x0, _x1, _x1],
            "lnx": [_y0, _y0, _y1, _y1, _y0, 0.14, _y1, 0.14],
            "seg": ["h0", "h0", "h1", "h1", "v0", "v0", "v1", "v1"],
        }))
        .mark_line(color="#9aa5b1", strokeDash=[3, 3], size=1, clip=True)
        .encode(x="x:Q", y="lnx:Q", detail="seg:N")
    )

    def _brace_df(_a, _b, _base, _depth, _vertical):
        # Curly brace spanning [_a, _b] as a polyline: back edge at _base on
        # the other axis, cusp reaching _depth further out at the midpoint.
        _lo, _hi = min(_a, _b), max(_a, _b)
        _s = np.linspace(_lo, _hi, 120)
        _half = _s[:60]
        _sharp = 300.0 / (_hi - _lo)
        _ph = (1.0 / (1.0 + np.exp(-_sharp * (_half - _half[0])))
               + 1.0 / (1.0 + np.exp(-_sharp * (_half - _half[-1]))))
        _prof = np.concatenate([_ph, _ph[::-1]])
        _prof = (_prof - _prof.min()) / (_prof.max() - _prof.min())
        _off = _base + _depth * _prof
        _ordr = np.arange(_s.size)
        if _vertical:
            return pd.DataFrame({"x": _off, "lnx": _s, "o": _ordr})
        return pd.DataFrame({"x": _s, "lnx": _off, "o": _ordr})

    _xlab = (
        alt.Chart(pd.DataFrame({
            "x": [(_x0 + _x1) / 2.0], "lnx": [0.31],
            "t": [f"{pct_change.value:+.0f}%"],
        }))
        .mark_text(color="#b45309", fontSize=13, baseline="bottom")
        .encode(x="x:Q", y="lnx:Q", text="t:N")
    )
    # The label sits above the upper guide line rather than inside the braced
    # span, which is too short to hold it when the change is small.
    _ylab = (
        alt.Chart(pd.DataFrame({
            "x": [1.0], "lnx": [max(_y0, _y1) + 0.09],
            "t": [f"Δln ≈ {_log_change:+.3f}"],
        }))
        .mark_text(color="#1f4e79", fontSize=13, align="left", baseline="bottom")
        .encode(x="x:Q", y="lnx:Q", text="t:N")
    )

    # Either brace degenerates when its span shrinks below about ten pixels (a
    # 0% change collapses both to nothing, which _brace_df cannot even build),
    # so each brace is built only when its span is wide enough; the labels stay
    # legible at any spacing and always show. The order channel is essential:
    # without it Altair sorts line vertices by x, which scrambles the vertical
    # brace into a zigzag.
    _layers = [_guides, _xlab, _curve, _secant, _ends, _ylab]
    if abs(_x1 - _x0) >= 0.8:
        _layers.append(
            alt.Chart(_brace_df(_x0, _x1, 0.14, 0.12, False))
            .mark_line(color="#b45309", size=1.5, clip=True)
            .encode(x="x:Q", y="lnx:Q", order=alt.Order("o:Q"))
        )
    if abs(_y1 - _y0) >= 0.05:
        _layers.append(
            alt.Chart(_brace_df(_y0, _y1, 0.85, 0.7, True))
            .mark_line(color="#1f4e79", size=1.5, clip=True)
            .encode(x="x:Q", y="lnx:Q", order=alt.Order("o:Q"))
        )
    _chart = alt.layer(*_layers).properties(width=520, height=320)

    _gap = float(pct_change.value) - 100.0 * _log_change
    if pct_change.value == 0:
        _msg = (
            "With no change in experience, the logarithm does not change either. "
            "Move the percent change away from zero to compare the two measures."
        )
    else:
        _msg = (
            f"{'Raising' if _p > 0 else 'Lowering'} experience by {abs(pct_change.value):.0f}% "
            f"takes it from {_x0:.0f} to {_x1:.1f} years. The natural log changes by "
            f"{_log_change:+.3f}, which is {100.0 * _log_change:+.1f}% once multiplied by 100, "
            f"next to the actual {pct_change.value:+.0f}% change. The two are within "
            f"{abs(_gap):.1f} percentage points here"
        )
        _msg += (
            ", almost identical for a small change." if abs(pct_change.value) <= 10
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

    Why run a regression on logarithms at all? Two reasons come up again and again. First, many economic relationships are curved in exactly the way the logarithm is: earnings, firm sales, and country GDP all tend to grow quickly from a low base and then more slowly, so a regression on logged variables can fit them with a straight line in the transformed units. Second, effects stated in percent terms often travel better than effects stated in units. A \$1 raise means something very different to a minimum-wage worker and a chief executive, but a 5 percent raise is comparable across the two. Because a change in a logarithm is approximately a percent change divided by 100, putting a variable in logarithms lets its coefficient be read in percent terms.

    Putting a variable in logarithms changes how its coefficient is read. Three combinations come up, depending on whether the logarithm is applied to the independent variable, the dependent variable, or both. Each is estimated by OLS exactly as before, on the transformed variable. We fit all three to the same wage and experience data, and the switcher below draws each fitted relationship back in the original units so the shapes can be compared.

    ### <span style="color:#0b68cb">Linear-log</span>

    $$
    \text{Wage} = \beta_0 + \beta_1\ln(\text{Exper}) + u
    $$

    Only the independent variable is in logarithms. A 1 percent rise in experience is associated with a change in the wage of $0.01\,\beta_1$ dollars. The fitted curve rises quickly at low experience and flattens, because the logarithm does. This form suits a dependent variable measured in natural units whose response to the independent variable shows diminishing returns.

    ### <span style="color:#0b68cb">Log-linear</span>

    $$
    \ln(\text{Wage}) = \beta_0 + \beta_1\text{Exper} + u
    $$

    Only the dependent variable is in logarithms. A one-year rise in experience is associated with a $100\,\beta_1$ percent change in the wage. Because that percent change is the same at every level of experience, the wage in dollars bends upward as experience grows, the way a bank balance does under a fixed interest rate.

    ### <span style="color:#0b68cb">Log-log</span>

    $$
    \ln(\text{Wage}) = \beta_0 + \beta_1\ln(\text{Exper}) + u
    $$

    Both variables are in logarithms. A 1 percent rise in experience is associated with a $\beta_1$ percent change in the wage. This $\beta_1$ is the *elasticity* of the wage with respect to experience, the percent change in one variable associated with a one percent change in the other. Elasticities are free of units on both sides, which is why economists report so many results in this form.
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

    Logarithms fit three situations.

    **The economic model is multiplicative.** A Cobb-Douglas relationship $Y = A\,X_1^{\beta_1} X_2^{\beta_2}$ becomes $\ln(Y) = \ln(A) + \beta_1\ln(X_1) + \beta_2\ln(X_2)$ after taking logarithms of both sides, using the property $\ln(X^a) = a\ln(X)$ from Section 2. The transformed equation is linear in the coefficients and ready for OLS, and each slope is an elasticity.

    **Percent changes are the natural unit.** Growth rates of GDP or wages are discussed in percent terms, so a percent change carries more meaning than a change in levels. A log-linear regression of $\ln(\text{GDP})$ on time, for example, has a slope that reads directly as an annual growth rate.

    **The variable ranges over very different sizes.** Firm sales run from a corner shop to a national chain. A one percent change is comparable across that whole range, but a one-dollar change is not: it is enormous for the shop and negligible for the chain. Taking logarithms puts the two on the same footing, and it also pulls in the extreme values so that a handful of giant observations does not dominate the regression.

    Two cautions apply. First, $\ln(X)$ is defined only for $X > 0$, so a variable that can be zero or negative, such as profits, cannot be put in logarithms directly. Second, the R-squared can only be compared between models that share the same dependent variable. A regression of $\ln(\text{Wage})$ measures how much of the variation in $\ln(\text{Wage})$ it explains, not the variation in $\text{Wage}$, so its R-squared cannot be compared with that of a regression of $\text{Wage}$ itself. To choose among the specifications, ask which shape the economics of the problem suggests, and inspect the fitted curves as in Section 3.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** exponential function, natural logarithm, percent, "
            "percentage point, linear-log model, log-linear model, log-log model, "
            "elasticity.\n\n"
            "**Key concepts covered:** the natural logarithm as the inverse of the "
            "exponential, defined only for positive values and with slope 1/X, why a change "
            "in a logarithm approximates a percent change divided by 100 and where the "
            "approximation breaks down, the difference between percent and percentage "
            "points, the three log specifications and how each coefficient is interpreted, "
            "the log-log slope as an elasticity, the situations that call for logarithms, "
            "and why the R-squared cannot be compared across different dependent variables."
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
