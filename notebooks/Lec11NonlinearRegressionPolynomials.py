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
                <div style="font-weight: 700; font-size: 1.05em;">Course Outline</div>

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
                11. **[Nonlinear Regression: Polynomials](#top)**
                    1. [Modeling a nonlinear relationship](#sec1)
                    1. [Interpreting the quadratic model](#sec2)
                    1. [The effect of experience depends on its level](#sec3)
                    1. [Testing whether the relationship is nonlinear](#sec4)
                    1. [Higher-order polynomials and overfitting](#sec5)
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
        width="350px",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<span class="nav-soon">← Lecture 10 (coming soon)</span>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/pdf/Lec11NonlinearRegressionPolynomials.pdf" target="_blank">Download PDF</a>'),
            mo.md('<span class="nav-soon">Lecture 12 (coming soon)</span>'),
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
    [2. Interpreting the quadratic model](#sec2)<br>
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

    The regressions we have considered so far assume that the relationship between each independent variable and the dependent variable is linear. In a linear relationship, a one-unit increase in an independent variable is always associated with the same change in the dependent variable, holding the other independent variables fixed. Many economic relationships do not follow this pattern, however. A worker's wage, for example, typically rises quickly early in their career and more slowly later on. The relationship between wages and experience is therefore curved rather than linear. A linear regression cannot capture this curvature and often predicts wages that are too high at low and high levels of experience and too low at moderate levels of experience.

    To capture relationships like this, we use a *nonlinear regression*, which allows the fitted relationship between an independent variable and the dependent variable to curve. One way to create this curvature is to include powers of an existing independent variable. For example, we can include both experience and experience squared as independent variables in a regression:

    $$
    \text{Wage} = \beta_0 + \beta_1\text{Exper} + \beta_2\text{Exper}^2 + u.
    $$

    A regression that includes powers of an independent variable is called a *polynomial regression*. The equation above is a *quadratic regression* because the highest power of experience is two; it is a special type of polynomial regression.<sup><a id="fnref1" href="#fn1">1</a></sup>

    Although the quadratic regression is nonlinear in experience, it remains linear in the coefficients $\beta_0$, $\beta_1$, and $\beta_2$. We can therefore estimate it using OLS just like the multiple regressions from Lectures 8 and 9, treating experience and experience squared as two separate independent variables.

    The slider below fits a polynomial regression of the degree you choose. A polynomial of degree one produces a straight line, a polynomial of degree two produces the quadratic relationship described above, and higher-degree polynomials produce more flexible curves. The plot also reports how well each polynomial fits the data. Lectures 12 and 13 will introduce other types of nonlinear regressions.
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
            mo.md("Adjust the degree of the polynomial regression and observe how the fitted wage curve and both $R$-squared measures change."),
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
            f"The degree-one polynomial produces a straight line. It predicts wages that "
            f"are too high at low and high levels of experience and too low at moderate "
            f"levels. Its R-squared is {_r2:.3f} and its adjusted R-squared is {_ar2:.3f}. "
            f"Raise the degree to 2 to allow the fitted relationship to curve."
        )
    elif _deg == 2:
        _msg = (
            f"The quadratic regression captures the rise and later flattening of "
            f"wages with experience. Its R-squared is {_r2:.3f} and its adjusted R-squared is {_ar2:.3f}, "
            f"both higher than the corresponding values for the straight line. Raise the "
            f"degree further to see how additional flexibility affects the fitted curve "
            f"and the two measures of fit."
        )
    else:
        _msg = (
            f"At degree {_deg}, the fitted curve begins to bend toward individual "
            f"observations. Its R-squared has risen to {_r2:.3f} because adding independent variables can "
            f"never lower the R-squared. Its adjusted R-squared, however, has fallen to "
            f"{_ar2:.3f}, indicating that the additional terms do not improve the fit "
            f"enough to justify the added complexity. This pattern suggests that the "
            f"additional terms are beginning to fit noise in the data rather than the underlying "
            f"relationship."
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
    ## 2. Interpreting the quadratic model

    The degree-two polynomial regression from Section 1 yields coefficient estimates $\hat{\beta}_0 = 7.7$, $\hat{\beta}_1 = 1.18$, and $\hat{\beta}_2 = -0.019$, with experience measured in years and wages measured in dollars per hour (set the polynomial degree slider to 2 to see the fitted curve). The negative coefficient on experience squared causes the fitted curve to flatten and eventually turn downward as experience increases. The quadratic regression has an R-squared of 0.76, compared with 0.59 for the straight-line regression, so it fits the observed data more closely.

    The intercept retains its usual interpretation, but the two coefficients on experience cannot be interpreted separately as changes in the predicted wage. In a straight-line regression, $\hat{\beta}_1$ is the regression slope and gives the change in the predicted wage associated with one additional year of experience. In a quadratic regression, a one-year increase in experience changes both $\text{Exper}$ and $\text{Exper}^2$. The change in the predicted wage therefore depends on $\hat{\beta}_1$, $\hat{\beta}_2$, and the worker’s current level of experience. Section 3 shows how to calculate and interpret changes in predicted wages from the fitted curve.

    Allowing the fitted relationship to curve does not change the assumptions required for a causal interpretation. A quadratic regression is still estimated as a multiple regression, so the least-squares assumptions from Lectures 6 and 9 continue to apply. The first OLS assumption concerns the unobserved determinants of wages collected in the error term. For the fitted relationship to have a causal interpretation, these omitted determinants cannot vary systematically with the independent variables in ways that raise or lower wages. Formally, the error must have mean zero for every possible combination of experience and experience squared,

    $$
    \mathbb{E}[u \mid \text{Exper}, \text{Exper}^2] = 0.
    $$

    Because $\text{Exper}^2$ is determined entirely by $\text{Exper}$, conditioning on both variables is equivalent to conditioning on experience alone. In our wage example, workers with different levels of experience cannot systematically differ in unobserved characteristics that also affect their wages.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. The effect of experience depends on its level

    To determine how the predicted wage changes from a given starting point, compare the fitted wage before and after an increase in experience. Suppose experience rises from $\text{Exper}$ to $\text{Exper}+\Delta$. The predicted change in wages is

    $$
    \Delta\widehat{\text{Wage}} = \left[ \hat{\beta}_1(\text{Exper}+\Delta) + \hat{\beta}_2(\text{Exper}+\Delta)^2 \right] - \left[ \hat{\beta}_1\text{Exper} + \hat{\beta}_2\text{Exper}^2 \right].
    $$

    The intercept, $\hat{\beta}_0$, does not appear because it is the same in both predictions and therefore cancels. Dividing the predicted change by $\Delta$ gives the average slope of the fitted curve over this interval, $\frac{\Delta\widehat{\text{Wage}}}{\Delta}$.

    This slope gives the average change in the predicted hourly wage associated with each additional year of experience over the interval. Unlike the constant slope of a straight-line regression, it depends on both the starting level of experience and the size of $\Delta$. The interactive plot below lets you choose both of these values. Early in a career, a small increase in experience raises the predicted wage substantially. Near the peak of the curve, the same increase in experience changes the predicted wage very little. Beyond the peak, it lowers the predicted wage. Increasing $\Delta$ averages the slope over a longer interval.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Ranges are chosen so the end of the span, start + delta, never exceeds the
    # 40 years covered by the data, which keeps the two sliders independent.
    secant_start = mo.ui.slider(
        start=1, stop=30, step=1, value=8,
        label="Starting experience, Exper", show_value=True, full_width=False,
    )
    secant_delta = mo.ui.slider(
        start=1, stop=10, step=1, value=5,
        label="Size of the increase, Δ", show_value=True, full_width=False,
    )
    mo.vstack(
        [
            mo.md("Set where the increase in experience starts and how large it is, then observe the slope of the curve over that interval."),
            secant_start,
            secant_delta,
        ]
    )
    return secant_delta, secant_start


@app.cell(hide_code=True)
def _(alt, exper, mo, np, pd, secant_delta, secant_start, wage):
    _quad = np.polyfit(exper, wage, 2)  # [b2, b1, b0], highest power first

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
    # Dashed guides from the secant endpoints across to the vertical axis and
    # down to the horizontal axis, stopping at the braces.
    _guides = (
        alt.Chart(pd.DataFrame({
            "exper": [_x0, 1.4, _x1, 1.4, _x0, _x0, _x1, _x1],
            "wage": [_y0, _y0, _y1, _y1, _y0, 1.2, _y1, 1.2],
            "seg": ["h0", "h0", "h1", "h1", "v0", "v0", "v1", "v1"],
        }))
        .mark_line(color="#9aa5b1", strokeDash=[3, 3], size=1, clip=True)
        .encode(x="exper:Q", y="wage:Q", detail="seg:N")
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
            return pd.DataFrame({"exper": _off, "wage": _s, "o": _ordr})
        return pd.DataFrame({"exper": _s, "wage": _off, "o": _ordr})

    # The order channel is essential: without it Altair sorts line vertices by
    # x, which scrambles the vertical brace into a zigzag.
    _xbrace = (
        alt.Chart(_brace_df(_x0, _x1, 1.2, 1.1, False))
        .mark_line(color="#b45309", size=1.5, clip=True)
        .encode(x="exper:Q", y="wage:Q", order=alt.Order("o:Q"))
    )
    _xlab = (
        alt.Chart(pd.DataFrame({
            "exper": [(_x0 + _x1) / 2.0], "wage": [2.7],
            "t": [f"Δ = {_delta:.0f}"],
        }))
        .mark_text(color="#b45309", fontSize=13, baseline="bottom")
        .encode(x="exper:Q", y="wage:Q", text="t:N")
    )
    _ybrace = (
        alt.Chart(_brace_df(_y0, _y1, 1.4, 0.9, True))
        .mark_line(color="#1f4e79", size=1.5, clip=True)
        .encode(x="exper:Q", y="wage:Q", order=alt.Order("o:Q"))
    )
    # The label sits above the upper guide line rather than inside the braced
    # span, which is too short to hold it when the wage change is small.
    _ylab = (
        alt.Chart(pd.DataFrame({
            "exper": [1.6], "wage": [max(_y0, _y1) + 0.8],
            "t": [f"ΔWage ≈ {'−' if _y1 < _y0 else ''}${abs(_y1 - _y0):.2f}"],
        }))
        .mark_text(color="#1f4e79", fontSize=13, align="left", baseline="bottom")
        .encode(x="exper:Q", y="wage:Q", text="t:N")
    )

    # Near the peak the two predicted wages almost coincide and the vertical
    # brace degenerates, so only the brace is omitted; the label sits above the
    # upper guide line and stays legible at any spacing, so it always shows.
    _layers = [_cloud, _guides, _xbrace, _xlab, _curve, _secant, _ends, _ylab]
    if abs(_y1 - _y0) >= 1.0:
        _layers += [_ybrace]
    _chart = alt.layer(*_layers).properties(width=560, height=340)

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
        + _msg + "</span>"
    )
    mo.vstack([_chart, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Testing whether the relationship is nonlinear

    Polynomial regressions allow us to model nonlinear relationships. Even when the population relationship is linear, however, sampling variation can produce nonzero coefficient estimates on squared and higher-order independent variables. We therefore often test whether the population coefficients on all such terms are zero.<sup><a id="fnref2" href="#fn2">2</a></sup> If they are, the terms drop out and the model becomes linear.

    The quadratic wage model contains only one higher-order independent variable, experience squared. We therefore test $H_0: \beta_2 = 0$ against $H_1: \beta_2 \neq 0$ using the same t-test as in Lectures 4 and 9. In the wage data, $\hat{\beta}_2 = -0.019$ with a standard error of about $0.0023$, so

    $$
    t
    =
    \frac{\hat{\beta}_2 - 0}{\operatorname{SE}(\hat{\beta}_2)}
    =
    \frac{-0.019 - 0}{0.0023}
    \approx -8.3.
    $$

    The corresponding p-value is far below 0.01, so we reject the null hypothesis and find strong evidence that the relationship between wages and experience is nonlinear. The negative estimate means that the curve bends downward, so wage gains diminish as experience rises. The adjusted R-squared also increases from 0.590 for the linear regression line to 0.757 for the quadratic regression, indicating that the quadratic regression fits the data substantially better.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Higher-order polynomials and overfitting

    As demonstrated in Section 1, the quadratic model we have focussed on extends naturally to a *polynomial of degree $r$*, which includes powers of experience through the $r$-th power and takes the form

    $$
    \text{Wage} = \beta_0 + \beta_1\text{Exper} + \beta_2\text{Exper}^2 + \dots + \beta_r\text{Exper}^r + u.
    $$

    Raising the degree gives the curve more flexibility by allowing it to bend in more places. That flexibility can become a problem, however. As you raise the degree above two on the slider in Section 1, the curve begins to wiggle around individual observations rather than capture the overall pattern. This is called *overfitting*, which occurs when a model captures randomness in the current sample rather than a pattern likely to reappear in new samples.

    The R-squared and adjusted R-squared illustrate this tradeoff. In the Section 1 plot, the R-squared rises from 0.762 for the quadratic regression to 0.779 for a degree-twenty polynomial regression because adding terms can never worsen the in-sample fit. The *adjusted R-squared*, which penalizes each added term, instead peaks at 0.757 for the quadratic regression model and falls to 0.724 by degree twenty. The additional eighteen terms do not appear to improve the model fit.

    A few rules of thumb can help you decide how many degrees to include in your regression model. One is to increase the degree until the highest-order term is no longer statistically significant. Another is to choose the degree with the highest adjusted R-squared. Most importantly, the degree should be consistent with the economics of the problem. For our wage example, the quadratic regression model captures rapid wage growth early in a career followed by slower wage growth later on without adding unnecessary complexity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** nonlinear regression, polynomial regression, "
            "quadratic regression, polynomial of degree r, overfitting, adjusted "
            "R-squared.\n\n"
            "**Concepts:** modeling a curved relationship by including powers "
            "of an independent variable, why a polynomial regression remains linear in its "
            "coefficients and can be estimated by OLS as a multiple regression, why the "
            "coefficients on experience and experience squared cannot be interpreted "
            "separately as changes in the predicted wage, computing the effect of an "
            "increase in experience as the difference between two predicted wages so that "
            "it depends on the starting level of experience and the size of the increase, "
            "why allowing the fitted relationship to curve does not change the assumptions "
            "required for a causal interpretation, testing whether the relationship is "
            "nonlinear with a t-test on the coefficient of the squared term, and why "
            "adding terms can never lower the R-squared while the adjusted R-squared "
            "penalizes each added term and signals overfitting."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** Quadratic regressions are therefore polynomial regressions, and polynomial regressions of degree two or higher are nonlinear regressions! Not all nonlinear regressions are polynomial regressions, however, and not all polynomial regressions are quadratic regressions. <a href="#fnref1" title="Back to text">&#8617;</a></span>

    <span id="fn2" style="display:block;font-size:0.9rem;">**2.** When a polynomial includes more than one higher-order term, we must test whether their coefficients are jointly zero (i.e., $\beta_2 = \beta_3 = \dots = \beta_r = 0$). The Appendix of Lecture 9 explains how to conduct this test using an $F$-statistic. <a href="#fnref2" title="Back to text">&#8617;</a></span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<span class="nav-soon">← Lecture 10 (coming soon)</span>'),
            mo.md('<span class="nav-soon">Lecture 12 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
