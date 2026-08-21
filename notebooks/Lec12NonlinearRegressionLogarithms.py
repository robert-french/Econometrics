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
                10. <span class="soon">Reading Regression Tables</span>
                11. <span class="soon">Nonlinear Regression: Polynomials</span>
                12. **[Nonlinear Regression: Logarithms](#top)**
                    1. [What is a logarithm](#sec1)
                    1. [Logarithms and percent changes](#sec2)
                    1. [Three regression models with logarithms](#sec3)
                    1. [When to use logarithms](#sec4)
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
            mo.md('<span class="nav-soon">← Lecture 11 (coming soon)</span>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/pdf/Lec12NonlinearRegressionLogarithms.pdf" target="_blank">Download PDF</a>'),
            mo.md('<span class="nav-soon">Lecture 13 (coming soon)</span>'),
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

    In Lecture 11, we modeled nonlinear relationships by adding powers of an independent variable. In this lecture, we introduce another approach. A *logarithmic regression* transforms one or more variables using the logarithm function, often allowing us to interpret coefficients in terms of percent changes. To understand logarithmic regressions, we must first understand the logarithmic function. And to understand the logarithmic function, we must first understand the exponential function!

    The *exponential function* raises the constant $e \approx 2.71828$ to a power, written $y = e^X$ or $y = \exp(X)$. The *natural logarithm* is its inverse. It is the function that gives the power to which $e$ must be raised to produce $y$. We write it as $\ln(X)$, so that

    $$
    \ln(e^X)=X.
    $$

    Because $e$ raised to any power is positive, $\ln(X)$ is defined only when $X>0$.

    The natural logarithm rises quickly at first and then more slowly. Its slope at $X$ is $1/X$, so the curve is steep near zero and gradually flattens as $X$ grows. This shape allows a logarithm to turn some nonlinear relationships into linear ones. It also means that the absolute slope of a fitted curve that is linear in $\ln(X)$ approaches zero as $X$ rises. These properties will become clearer in Section 3.

    The plot below shows the exponential and logarithm functions together. Because the functions are inverses, their curves are mirror images across the dashed 45-degree line.
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
        "The exponential function is defined for every value of X but is always positive; "
        "the logarithm function is defined only for positive values of X but takes every value. "
        "Because the functions are inverses of each other, reflecting either curve across the dashed 45-degree line produces the other.</span>"
    )
    mo.vstack([_chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>

    ## 2. Logarithms and percent changes

    Logarithms appear often in economics because a change in the logarithm of a variable is approximately its proportional change, or its percent change divided by 100. For a small change $\Delta X$,

    $$
    \ln(X+\Delta X)-\ln(X)\approx\frac{\Delta X}{X}.
    $$

    For example, an increase in experience from 10 to 10.1 years is a proportional change of $0.1/10=0.01$, or 1 percent. The corresponding log change is $\ln(10.1)-\ln(10)\approx0.00995$, which is very close to $0.01$. This approximation is close for small changes but becomes less accurate for large changes.<sup><a id="fnref1" href="#fn1">1</a></sup>

    Logarithms also obey several useful rules,

    $$
    \begin{aligned}
    \ln(X^a) &=a\ln(X), \\
    \ln(1/X) &=-\ln(X), \\
    \ln(aX) &=\ln(a)+\ln(X).
    \end{aligned}
    $$

    The first rule is useful because it turns exponents into multipliers. We will use this rule in Section 4. The second and third rules explain why log changes are symmetric in a way that percent changes are not. Doubling a variable changes its logarithm by $\ln(2X)-\ln(X)=\ln(2)\approx0.693$, while reversing that change lowers its logarithm by $\ln(X)-\ln(2X)=-\ln(2)$. The two log changes therefore have equal magnitudes and opposite signs. In percent terms, however, increasing $X$ to $2X$ is a 100 percent increase, while returning from $2X$ to $X$ is a 50 percent decrease because the decrease is measured relative to $2X$. Log changes, sometimes called *log points*, therefore treat a multiplicative change and its reversal symmetrically.

    The plot below lets you see these ideas in practice. Choose a starting level of experience and a percent change. The horizontal brace marks the change in experience, while the vertical brace marks the resulting change in its logarithm. Beneath the plot, the caption compares the percent change with its log approximation and reports the difference between them. Try a small percent change to see how closely they match, then compare $+100$ with $-50$ to see that the log changes are equal in magnitude and opposite in sign.
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
            f"{_log_change:+.3f}, which is {100.0 * _log_change:+.1f}% once multiplied by 100. "
            f"The two are within "
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
    mo.vstack([_chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>

    ## 3. Three regression models with logarithms

    There are two main reasons why you might want to estimate a regression using logarithms. First, logarithms can turn some nonlinear relationships into approximately linear ones. If wages rise quickly at low levels of experience and then more slowly, for example, a regression using log experience may represent the relationship well. Second, logarithms let us express relationships in percent terms, which are often easier to compare across different scales. A $1 raise means something very different to a minimum-wage worker and a chief executive, but a 5 percent raise is more comparable across the two workers.

    How we interpret a coefficient depends on whether we take the logarithm of the independent variable, the dependent variable, or both. Nothing about the OLS regression itself changes; we simply transform the variables before estimating it. There are three main types of logarithmic regressions, which we now describe.

    ### <span style="color:#0b68cb">Linear-log</span>

    $$
    \text{Wage}=\beta_0+\beta_1\ln(\text{Exper})+u
    $$

    In linear-log regression models, only the independent variable is in logarithms. A 1 percent increase in experience is associated with a change in the wage of approximately $0.01\beta_1$ dollars. When $\beta_1>0$, the fitted curve rises quickly at low levels of experience and then flattens, so an additional year is associated with a smaller wage increase later in a career.

    ### <span style="color:#0b68cb">Log-linear</span>

    $$
    \ln(\text{Wage})=\beta_0+\beta_1\text{Exper}+u
    $$

    In log-linear regression models, only the dependent variable is in logarithms. One additional year of experience is associated with an approximate $100\cdot\beta_1$ percent change in the wage. This percent change is the same at every level of experience. Because the same percent change corresponds to more dollars at a higher wage, the fitted curve bends upward when $\beta_1>0$.

    ### <span style="color:#0b68cb">Log-log</span>

    $$
    \ln(\text{Wage})=\beta_0+\beta_1\ln(\text{Exper})+u
    $$

    In log-log regression models, both the independent and dependent variables are in logarithms. A 1 percent increase in experience is associated with an approximate $\beta_1$ percent change in the wage. The coefficient $\beta_1$ is therefore the *elasticity* of the wage with respect to experience. Because an elasticity compares one percent change with another, it does not depend on the units used to measure either variable.

    The drop-down menu below fits all three models to the same data and plots the fitted wages in their original units. Switch between the models to see how logging experience, wages, or both changes the shape of the fitted curve.
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
            f"Wage = {_b0:.1f} + {_b1:.2f}·experience. One more year of experience is associated "
            f"with a \\${_b1:.2f} higher wage at every level of experience. The resulting straight "
            f"line misses the flattening in the data."
        )

    elif _name == "Linear-log":
        _b0, _b1 = _fit(np.log(exper), wage)
        _pred = _b0 + _b1 * np.log(_grid)
        _msg = (
            f"Wage = {_b0:.1f} + {_b1:.1f}·ln(experience). A 1% increase in experience is associated "
            f"with about a \\${_b1 / 100.0:.2f} higher wage. The fitted curve rises quickly early "
            f"in a career and flattens later."
        )

    elif _name == "Log-linear":
        _b0, _b1 = _fit(exper, np.log(wage))
        _pred = np.exp(_b0 + _b1 * _grid)
        _msg = (
            f"ln(wage) = {_b0:.2f} + {_b1:.4f}·experience. One more year of experience is associated "
            f"with about a {100.0 * _b1:.1f}% higher wage. Because the same percent change "
            f"corresponds to more dollars at higher wages, the fitted curve bends upward."
        )

    else:
        _b0, _b1 = _fit(np.log(exper), np.log(wage))
        _pred = np.exp(_b0 + _b1 * np.log(_grid))
        _msg = (
            f"ln(wage) = {_b0:.2f} + {_b1:.2f}·ln(experience). The elasticity is {_b1:.2f}, so a 1% "
            f"increase in experience is associated with about a {_b1:.2f}% higher wage. The fitted "
            f"curve rises and flattens, closely following the data."
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
    mo.vstack([_chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>

    ## 4. When to use logarithms

    Sections 2 and 3 showed that logarithms let us describe relationships in percent terms and can turn some nonlinear relationships into approximately linear ones. These ideas suggest three common situations in which logarithms are useful.

    **The underlying economic model is multiplicative.** Some economic models multiply variables instead of add them together. Logarithms are useful because they turn products into sums and powers into multipliers. A Cobb-Douglas production function is a common example,

    $$
    Y=A\,X_1^{\beta_1}X_2^{\beta_2}
    \quad\Longrightarrow\quad
    \ln(Y)=\ln(A)+\beta_1\ln(X_1)+\beta_2\ln(X_2).
    $$

    The transformed equation is linear in the coefficients and so can be estimated by OLS.

    **Percent changes are the natural unit.** If percent growth is more meaningful than a change in levels, logging a variable lets us interpret its coefficient in percent terms, as in the log-linear and log-log models from Section 3.

    **The variable ranges over very different sizes.** Firm sales can range from those of a corner shop to those of a national chain. Taking logarithms emphasizes proportional differences and compresses unusually large values, reducing their influence on the regression.

    Logarithms cannot always be used, however. Because $\ln(X)$ is defined only when $X>0$, variables that can equal zero or become negative, such as profits, cannot be logged directly. Comparing models using the R-squared also requires care. A regression of $\ln(\text{Wage})$ and a regression of $\text{Wage}$ explain variation on different scales, so their R-squared values are not comparable. Always use the economics of the problem to decide whether the relationship should be expressed in levels or in percent terms, then inspect the fitted curves in their original units, as in Section 3.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** logarithmic regression, exponential function, natural "
            "logarithm, percent change, percentage point, log point, linear-log model, "
            "log-linear model, log-log model, elasticity.\n\n"
            "**Concepts:** the natural logarithm as the inverse of the "
            "exponential function, defined only for positive values and with slope 1/X, "
            "why a change in a logarithm approximates a percent change divided by 100 and "
            "where the approximation breaks down, the difference between percent and "
            "percentage points, why log changes treat a change and its reversal "
            "symmetrically while percent changes do not, the three logarithmic regression "
            "models and how each coefficient is interpreted, the log-log slope as an "
            "elasticity that does not depend on units, the situations that call for "
            "logarithms, and why the R-squared cannot be compared between regressions of a "
            "variable and of its logarithm."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** Remember from statistics that a *percent change* measures a change relative to the starting value, while the difference between two percent changes is measured in *percentage points*. An increase from 10 percent to 12 percent is an increase of 2 percentage points, not 2 percent. <a href="#fnref1" title="Back to text">&#8617;</a></span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<span class="nav-soon">← Lecture 11 (coming soon)</span>'),
            mo.md('<span class="nav-soon">Lecture 13 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
