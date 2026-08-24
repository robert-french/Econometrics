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
    app_title="Lecture 7: Inference in Simple Regression",
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
                5. <a href="https://robert-french.github.io/Econometrics/apps/Lec5SimpleLinearRegression.html" target="_self">Simple Linear Regression</a>
                6. <a href="https://robert-french.github.io/Econometrics/apps/Lec6OLSAssumptionsForCausalInference.html" target="_self">OLS Assumptions for Causal Inference</a>
                7. **[Inference and Omitted Variable Bias](#top)**
                    1. [The variance of the slope estimator](#sec1)
                    1. [The sampling distribution of the slope](#sec2)
                    1. [Heteroskedasticity](#sec3)
                    1. [Hypothesis tests for the slope](#sec4)
                    1. [Confidence intervals for the slope](#sec5)
                8. <a href="https://robert-french.github.io/Econometrics/apps/Lec8MultipleRegression.html" target="_self">Multiple Regression</a>
                9. <a href="https://robert-french.github.io/Econometrics/apps/Lec9ControlVariablesAndInference.html" target="_self">Control Variables and Inference</a>
                10. <a href="https://robert-french.github.io/Econometrics/apps/Lec10ReadingRegressionTables.html" target="_self">Reading Regression Tables</a>
                11. <a href="https://robert-french.github.io/Econometrics/apps/Lec11NonlinearRegressionPolynomials.html" target="_self">Nonlinear Regression: Polynomials</a>
                12. <a href="https://robert-french.github.io/Econometrics/apps/Lec12NonlinearRegressionLogarithms.html" target="_self">Nonlinear Regression: Logarithms</a>
                13. <a href="https://robert-french.github.io/Econometrics/apps/Lec13NonlinearRegressionInteractionTerms.html" target="_self">Nonlinear Regression: Interaction Terms</a>
                14. <a href="https://robert-french.github.io/Econometrics/apps/Lec14InternalAndExternalValidity.html" target="_self">Internal and External Validity</a>
                15. <a href="https://robert-french.github.io/Econometrics/apps/Lec15PanelDataI.html" target="_self">Panel Data I</a>
                16. <a href="https://robert-french.github.io/Econometrics/apps/Lec16PanelDataII.html" target="_self">Panel Data II</a>
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec6OLSAssumptionsForCausalInference.html" target="_self">← Lecture 6</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/pdf/Lec7InferenceAndOmittedVariableBias.pdf" target="_blank">Download PDF</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec8MultipleRegression.html" target="_self">Lecture 8 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 7: Inference in Simple Regression
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Same-page (#fragment) links must stay plain markdown links with no inline
    # style and no styled wrapper. marimo re-renders fragment links as React
    # navigation components, and any inline style string on the link (or on a
    # span/div around it) is passed to React as the `style` prop, which must be
    # an object, not a string -> "Minified React error #62". Subsection body
    # headings get their blue from the inline span used below, not from styling
    # the links.
    mo.md(r"""
    ## Contents

    [1. The variance of the slope estimator](#sec1)<br>
    [2. The sampling distribution of the slope](#sec2)<br>
    [3. Heteroskedasticity](#sec3)<br>
    [4. Hypothesis tests for the slope](#sec4)<br>
    [5. Confidence intervals for the slope](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. The variance of the slope estimator

    In Lecture 6, we wrote the regression model as $Y_i = \beta_0 + \beta_1 X_i + u_i$. Let's again suppose $Y_i$ is a worker’s wage and $X_i$ is the worker’s years of education. In this example, $u_i$ includes everything other than education that affects the worker’s wage.

    When we estimate the model using one sample, we get one estimate of the slope, $\hat{\beta}_1$. In our wage and education example, we might estimate with a single sample that each additional year of education is associated with a $1.20 increase in hourly wages. But another sample would usually give us a different slope estimate, because the estimate depends on the particular observations included in the sample.

    To understand how reliable $\hat{\beta}_1$ is, we need to know how much it would vary across repeated samples. This is the variance of the slope estimator. When the errors have the same dispersion at every value of $X$, the variance of $\hat{\beta}_1$ is

    $$
    \sigma^2_{\hat{\beta}_1} = \frac{\operatorname{var}(u)}{(n-1)\cdot \widehat{\operatorname{var}}(X)}.
    $$

    This formula shows that the slope estimate is more precise when the errors are less spread out, when the sample is larger, and when there is more variation in $X$. Section 3 considers the case where the dispersion of the errors differs across values of $X$. In practice, we do not observe $\operatorname{var}(u)$, so we estimate it using the residuals, $\widehat{\operatorname{var}}(\hat{u}) = \frac{1}{n-2}\sum_{i=1}^{n}\hat{u}_i^2$. This is the sum of squared residuals divided by $n-2$. We divide by $n-2$ rather than $n$ because estimating the intercept, $\hat{\beta}_0$, and the slope, $\hat{\beta}_1$, uses up two pieces of information from the sample.

    Using this estimate of the error variance gives the estimated variance of the slope estimator:

    $$
    \hat{\sigma}^2_{\hat{\beta}*1} = \frac{\widehat{\operatorname{var}}(\hat{u})}{\sum_{i=1}^{n}(X_i - \hat{\mu}_X)^2}.
    $$

    The square root of this quantity is the standard error of $\hat{\beta}_1$, written $\operatorname{se}(\hat{\beta}_1)$. The standard error tells us the typical size of the sampling error in the slope estimate. It is measured in the same units as the slope.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1a"></a>
    The formula shows why some slope estimates are more precise than others. Three things matter. First, the denominator contains the variation in $X$. In the wage and education example, a sample with workers who have very different levels of education gives us clearer comparisons between high-education and low-education workers. Those comparisons make it easier to see how wages change when education changes. Second, the numerator contains $\operatorname{var}(u)$. When wages are less spread out around the regression line for reasons not captured by education, there is less noise hiding the relationship between wages and education. That makes the slope easier to estimate precisely. Third, the sample size $n$ matters. Each additional observation adds information about the relationship between $Y$ and $X$, so the estimate depends less on any one unusual worker. As the sample gets larger, the slope estimate varies less from one sample to the next.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. The sampling distribution of the slope

    Knowing the variance of $\hat{\beta}_1$ is useful because it tells us how spread out the slope estimates are across repeated samples. To use that variance for confidence intervals and hypothesis tests, we also need to know the shape of the sampling distribution.

    Under the three least squares assumptions from Lecture 6, $\hat{\beta}_1$ is approximately normally distributed when the sample is reasonably large:

    $$
    \hat{\beta}_1 \sim \mathcal{N}\:\left(\beta_1,\ \sigma^2_{\hat{\beta}_1}\right).
    $$

    This means that repeated estimates of $\hat{\beta}_1$ would be centered around the true slope, $\beta_1$ (the estimator is unbiased, as shown in Lecture 6), with variance given by $\sigma^2_{\hat{\beta}_1}$, defined in Section 1.

    This normal approximation comes from the central limit theorem from Lecture 2 because the slope estimate can be written as a weighted mean of sample observations. When the observations are independent and identically distributed as the second least squares assumption states, averages like this are close to normally distributed in large samples. The third least squares assumption that large outliers are unlikely helps ensure that no single observation dominates the estimate.

    The plot below helps you see these ideas in practice. Use the sliders to set the underlying population and choose how many observations are drawn in each sample, then press the ''Draw new sample''. Each draw creates one sample, fits the corresponding OLS line, and reports its standard error. The orange dashed lines plot the OLS slope estimate multiplied by both plus and minus 1.96 times its standard error. These lines represent the range of a 95% confidence interval, which we consider again in Section 5. Each draw also adds its slope estimate to the adjacent density plot, so repeated draws build the sampling distribution one estimate at a time. Press ''Reset plots'' to start over. You should reset the plots after moving a slider so that all the collected slope estimates come from the same settings.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <span style="color:#0b68cb">What determines the variance of the sampling distribution?</span>
    """)
    return


@app.cell(hide_code=True)
def _(np):
    def draw_sample(n, xsd, esd, seed):
        rng = np.random.default_rng(seed)
        X = 14.0 + xsd * rng.standard_normal(n)
        Y = 8.0 + 1.2 * X + esd * rng.standard_normal(n)
        b1h = float(np.cov(X, Y, ddof=1)[0, 1] / np.var(X, ddof=1))
        b0h = float(Y.mean() - b1h * X.mean())
        resid = Y - (b0h + b1h * X)
        sxx = float(np.sum((X - X.mean()) ** 2))
        se = float(np.sqrt(np.sum(resid ** 2) / max(n - 2, 1) / sxx))
        return {
            "X": X.tolist(), "Y": Y.tolist(),
            "b0h": b0h, "b1h": b1h, "se": se,
            "xbar": float(X.mean()), "ybar": float(Y.mean()),
        }

    return (draw_sample,)


@app.cell(hide_code=True)
def _(draw_sample, mo):
    _init = draw_sample(80, 3.5, 3.0, 50)
    get_acc, set_acc = mo.state({"betas": [], "sample": _init})
    return get_acc, set_acc


@app.cell(hide_code=True)
def _(draw_sample, get_acc, mo, set_acc):
    sd_n = mo.ui.slider(
        start=20, stop=400, step=20, value=80,
        label="Sample size (n)", show_value=True,
    )
    sd_xspread = mo.ui.slider(
        start=1.0, stop=6.0, step=0.5, value=3.5,
        label="Spread of education (standard deviation of X)", show_value=True,
    )
    sd_errsd = mo.ui.slider(
        start=1.0, stop=8.0, step=0.5, value=3.0,
        label="Error standard deviation", show_value=True,
    )

    def _on_draw(_v):
        _st = get_acc()
        _k = len(_st["betas"])
        _s = draw_sample(
            int(sd_n.value), float(sd_xspread.value), float(sd_errsd.value), 50 + _k
        )
        set_acc({"betas": _st["betas"] + [_s["b1h"]], "sample": _s})

    def _on_reset(_v):
        set_acc({"betas": [], "sample": get_acc()["sample"]})

    draw_button = mo.ui.button(label="Draw new sample", on_change=_on_draw)
    reset_button = mo.ui.button(label="Reset plot", on_change=_on_reset)

    mo.vstack([
        sd_n, sd_xspread, sd_errsd,
        mo.hstack([draw_button, reset_button], justify="start"),
    ])
    return sd_errsd, sd_n, sd_xspread


@app.cell(hide_code=True)
def _(alt, get_acc, mo, np, pd, sd_errsd, sd_n, sd_xspread, stats):
    _s = get_acc()["sample"]
    _X = np.array(_s["X"])
    _Y = np.array(_s["Y"])
    _b1h = _s["b1h"]
    _se = _s["se"]
    _xb = _s["xbar"]
    _yb = _s["ybar"]
    _n = len(_X)

    _xline = np.array([2.0, 26.0])
    _pts = pd.DataFrame({"x": _X, "y": _Y})
    _fit = pd.DataFrame({"x": _xline, "y": _yb + _b1h * (_xline - _xb)})
    _band = pd.DataFrame({
        "x": np.concatenate([_xline, _xline]),
        "y": np.concatenate([
            _yb + (_b1h - 1.96 * _se) * (_xline - _xb),
            _yb + (_b1h + 1.96 * _se) * (_xline - _xb),
        ]),
        "edge": ["lo", "lo", "hi", "hi"],
    })

    _xdom = [2.0, 26.0]
    _ydom = [0.0, 55.0]
    _scatter = (
        alt.Chart(_pts)
        .mark_circle(color="#1f4e79", opacity=0.55, size=45, clip=True)
        .encode(
            x=alt.X("x:Q", title="Years of education", scale=alt.Scale(domain=_xdom, nice=False)),
            y=alt.Y("y:Q", title="Hourly wage (USD)", scale=alt.Scale(domain=_ydom, nice=False)),
        )
    )
    _edges = (
        alt.Chart(_band)
        .mark_line(color="orange", strokeDash=[5, 4], size=2, clip=True)
        .encode(x="x:Q", y="y:Q", detail="edge:N")
    )
    _ols = (
        alt.Chart(_fit)
        .mark_line(color="#111827", size=2.5, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _chart = (_scatter + _edges + _ols).properties(
        width=370, height=300,
        title="One sample and its OLS line",
    )

    _lo = _b1h - 1.96 * _se
    _hi = _b1h + 1.96 * _se
    _body = (
        rf"This sample of {_n} workers gives $\hat{{\beta}}_1 = {_b1h:.2f}$ with "
        rf"$\operatorname{{se}}(\hat{{\beta}}_1) = {_se:.3f}$, so its 95% confidence "
        rf"interval for the slope runs from {_lo:.2f} to {_hi:.2f}."
    )
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 0.5rem;max-width:370px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _body + "</span>"
    )
    _left = mo.vstack([_chart, _caption])

    _betas = get_acc()["betas"]
    _b1 = 1.2
    _base_lo, _base_hi = 0.4, 2.0
    _cap_lo, _cap_hi = -1.8, 4.2

    if len(_betas) > 0:
        _arr = np.clip(np.asarray(_betas, dtype=float), _cap_lo, _cap_hi)
        _dlo = min(_base_lo, float(_arr.min()))
        _dhi = max(_base_hi, float(_arr.max()))
    else:
        _arr = np.asarray([], dtype=float)
        _dlo, _dhi = _base_lo, _base_hi

    _xscale = alt.Scale(domain=[_dlo, _dhi], nice=False)
    _has_kde = len(_arr) >= 2 and float(np.std(_arr)) > 1e-9

    _grid = np.linspace(_dlo, _dhi, 200)
    if _has_kde:
        _dens = stats.gaussian_kde(_arr)(_grid)
        _ymax = float(_dens.max()) * 1.15
    else:
        _dens = np.zeros_like(_grid)
        _ymax = 1.0

    _show_normal = len(_arr) >= 50
    if _show_normal:
        _se_th = float(sd_errsd.value) / (float(sd_xspread.value) * (int(sd_n.value) ** 0.5))
        _norm = stats.norm.pdf(_grid, _b1, _se_th)
        _ymax = max(_ymax, float(_norm.max()) * 1.15)

    _yscale = alt.Scale(domain=[0.0, _ymax], nice=False)

    _layers = []
    if _has_kde:
        _layers.append(
            alt.Chart(pd.DataFrame({"b": _grid, "density": _dens}))
            .mark_area(color="#1f4e79", opacity=0.25, line={"color": "#1f4e79"})
            .encode(
                x=alt.X("b:Q", scale=_xscale, title="Collected slope estimates"),
                y=alt.Y("density:Q", scale=_yscale, title="Density"),
            )
        )
    if _show_normal:
        _layers.append(
            alt.Chart(pd.DataFrame({"b": _grid, "density": _norm}))
            .mark_line(color="#9aa5b1", strokeDash=[4, 3], size=2)
            .encode(x=alt.X("b:Q", scale=_xscale), y=alt.Y("density:Q", scale=_yscale))
        )
    if len(_arr) > 0:
        _layers.append(
            alt.Chart(pd.DataFrame({"b": _arr, "density": np.zeros_like(_arr)}))
            .mark_tick(color="#1f4e79", opacity=0.5, thickness=1, size=10)
            .encode(x=alt.X("b:Q", scale=_xscale), y=alt.Y("density:Q", scale=_yscale))
        )
    _layers.append(
        alt.Chart(pd.DataFrame({"b": [_b1]}))
        .mark_rule(color="orange", size=2.5)
        .encode(x=alt.X("b:Q", scale=_xscale, title="Collected slope estimates"))
    )

    _chart = alt.layer(*_layers).properties(
        width=370, height=300, title="Sampling distribution built from your draws"
    )

    _c = len(_betas)
    _plural = "" if _c == 1 else "s"
    _body = (
        f"You have collected {_c} slope estimate{_plural}, each drawn as a tick on "
        f"the axis. The shaded curve is an empirical density plot. "
        f"The orange line marks the true slope of 1.2. Keep "
        f"drawing and the density should pile up into a bell-shaped curve centered there."
    )
    if _show_normal:
        _body += " The grey dashed curve is the true normal density your sample draws should approximate."
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 0.5rem;max-width:370px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _body + "</span>"
    )
    _right = mo.vstack([_chart, _caption])

    mo.hstack([_left, _right], justify="center", align="start")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Heteroskedasticity

    The variance formula in Section 1 assumes that the error term has the same dispersion at every value of $X$. In that case, we say the error term is *homoskedastic*. By contrast, the error is *heteroskedastic* when its dispersion changes with $X$.

    The error term in the wage and education example may be heteroskedastic. Among workers with little education, hourly wages may be clustered in a relatively narrow range. Among workers with a college degree, some workers may earn close to the group average, while others may earn much more or much less. As a result, wages may be more dispersed at higher levels of education.

    Remember that we never observe $u_i$ itself. We instead estimate the residual $\hat{u}_i = Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i$. In a scatter plot, heteroskedasticity appears as a change in the vertical dispersion of the points, or size of the residuals, around the fitted line.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3a"></a>
    ### <span style="color:#0b68cb">Heteroskedasticity-robust standard errors</span>

    When the error is heteroskedastic, the formula in Section 1 no longer gives the right variance for $\hat{\beta}_1$. A standard error based on that formula can therefore be too small or too large.

    When the error is heteroskedastic, we instead estimate the variance of $\hat{\beta}_1$ with a formula that weights each observation’s squared residual differently, rather than assuming the error has the same dispersion everywhere.

    $$
    \hat{\sigma}^2_{\hat{\beta}_1} = \frac{1}{n} \cdot \frac{\frac{1}{n-2}\sum_{i=1}^{n}(X_i-\hat{\mu}_X)^2\hat{u}_i^2}{\left[\frac{1}{n}\sum_{i=1}^{n}(X_i-\hat{\mu}_X)^2\right]^2}.
    $$

    This is the *heteroskedasticity-robust* estimate of the variance of $\hat{\beta}_1$. Its square root is the heteroskedasticity-robust standard error. The formula allows the residuals to be more spread out at some values of $X$ than at others. It gives more weight to a large residual when the corresponding observation is far from the average value of $X$, because points far along the horizontal axis have more influence on the OLS slope estimate.

    The plot below compares the variance formula that assumes homoskedastic errors with the heteroskedasticity-robust variance formula. The five sliders set the spread of the error in five parts of the education range, from the least educated workers on the left to the most educated workers on the right. When all five sliders are equal, the error is homoskedastic. When some sliders are higher than others, the error is heteroskedastic. Beneath the plot, the homoskedastic variance estimate appears next to the robust variance estimate. When the sliders are level, the two estimates are similar. As the spread changes across the education range, the two estimates move apart, and the homoskedastic estimate is the one that becomes unreliable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _opts = dict(start=1.0, stop=10.0, step=0.5, value=2.5, show_value=True, full_width=True)
    het_s1 = mo.ui.slider(label="8-10 years", **_opts)
    het_s2 = mo.ui.slider(label="10-12 years", **_opts)
    het_s3 = mo.ui.slider(label="12-14 years", **_opts)
    het_s4 = mo.ui.slider(label="14-16 years", **_opts)
    het_s5 = mo.ui.slider(label="16-18 years", **_opts)
    # The negative left margin slides the whole slider row left so each thin
    # slider sits closer to its slice; tune the inch value to nudge it.
    _row = mo.hstack(
        [mo.Html("<div></div>"), het_s1, het_s2, het_s3, het_s4, het_s5],
        widths=[0.1, 1, 1, 1, 1, 1],
        gap=0.4,
    ).style({"margin-left": "-0.75in"})
    mo.vstack([
        mo.md("Choose the dispersion of the error term in each slice of the education range and see how it impacts the variance estimates."),
        _row,
    ])
    return het_s1, het_s2, het_s3, het_s4, het_s5


@app.cell(hide_code=True)
def _(alt, het_s1, het_s2, het_s3, het_s4, het_s5, mo, np, pd):
    _sds = [
        float(het_s1.value), float(het_s2.value), float(het_s3.value),
        float(het_s4.value), float(het_s5.value),
    ]

    _rng = np.random.default_rng(3)
    _n = 250
    _X = _rng.uniform(8.0, 18.0, _n)
    _panel = np.clip(((_X - 8.0) // 2.0).astype(int), 0, 4)
    _Z = _rng.standard_normal(_n)
    _sd_i = np.array(_sds)[_panel]
    _Y = 8.0 + 1.2 * _X + _sd_i * _Z

    _b1h = float(np.cov(_X, _Y, ddof=1)[0, 1] / np.var(_X, ddof=1))
    _b0h = float(_Y.mean() - _b1h * _X.mean())
    _resid = _Y - (_b0h + _b1h * _X)
    _dev2 = (_X - _X.mean()) ** 2
    _sxx = float(np.sum(_dev2))
    _varhat_u = float(np.sum(_resid ** 2) / (_n - 2))
    _var_homo = _varhat_u / _sxx
    _num = float(np.sum(_dev2 * _resid ** 2) / (_n - 2))
    _den = float((np.sum(_dev2) / _n) ** 2)
    _var_robust = (1.0 / _n) * _num / _den

    _pts = pd.DataFrame({"x": _X, "y": _Y})
    _xline = np.array([8.0, 18.0])
    _fitdf = pd.DataFrame({"x": _xline, "y": _b0h + _b1h * _xline})

    _xsc = alt.Scale(domain=[8.0, 18.0], nice=False)
    _ysc = alt.Scale(domain=[0.0, 60.0], nice=False)

    _line = (
        alt.Chart(_fitdf)
        .mark_line(color="#111827", size=2.5, clip=True)
        .encode(x=alt.X("x:Q", scale=_xsc), y=alt.Y("y:Q", scale=_ysc))
    )
    _points = (
        alt.Chart(_pts)
        .mark_circle(size=40, opacity=0.55, color="#1f4e79", clip=True)
        .encode(
            x=alt.X("x:Q", scale=_xsc, title="Years of education"),
            y=alt.Y("y:Q", scale=_ysc, title="Hourly wage (USD)"),
        )
    )
    _chart = (_points + _line).properties(
        width=560, height=320, title="Wages and education"
    )

    _homo_str = f"{_var_homo:.5f}"
    _rob_str = f"{_var_robust:.5f}"
    _homo_group = mo.vstack(
        [
            mo.md("**Assuming homoskedasticity**"),
            mo.md(
                r"$$\hat{\sigma}^2_{\hat{\beta}_1} = \frac{\widehat{\operatorname{var}}(\hat{u})}{\sum_i (X_i-\hat{\mu}_X)^2} = "
                + _homo_str
                + r"$$"
            ),
        ],
        align="center",
    )
    _rob_group = mo.vstack(
        [
            mo.md("**Heteroskedasticity-robust**"),
            mo.md(
                r"$$\hat{\sigma}^2_{\hat{\beta}_1} = \frac{\frac{1}{n}\cdot\frac{1}{n-2}\sum_i (X_i-\hat{\mu}_X)^2\,\hat{u}_i^2}{\left[\frac{1}{n}\sum_i (X_i-\hat{\mu}_X)^2\right]^2} = "
                + _rob_str
                + r"$$"
            ),
        ],
        align="center",
    )
    _formulas = mo.hstack(
        [_homo_group, _rob_group], justify="center", align="start", gap=2.0
    )

    _homosked = len(set(_sds)) == 1
    if _homosked:
        _msg = (
            "The error dispersion is currently the same in every slice, so the error is homoskedastic and "
            "the two estimates of the variance of the slope nearly match."
        )
    else:
        _msg = (
            "The spread differs with years of education, so the error is heteroskedastic. The two "
            "variance estimates have pulled apart, and the estimate assuming homoskedasticity no longer reports "
            "the correct variance."
        )
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 1rem;max-width:560px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _msg + "</span>"
    )
    mo.vstack([_chart, _formulas, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Hypothesis tests in the regression model

    Lecture 4 introduced hypothesis tests, p-values, and t-statistics. Here we use the same ideas to test claims about the OLS estimates $\hat{\beta}_0$ and $\hat{\beta}_1$. For example, a common question in econometrics is whether education affects wages. In the population regression model, this is the claim that the slope parameter $\beta_1$ equals zero. Hypothesis tests formalize these claims.

    A *hypothesis test* for the regression slope uses the sample estimate $\hat{\beta}_1$ to assess a null hypothesis about the parameter $\beta_1$. We denote the null value as $\beta_{1,H_0}$. The null hypothesis is the claim that $\beta_1 = \beta_{1,H_0}$. In our example, setting $\beta_{1,H_0} = 0$ represents the null hypothesis that education, $X$, has no effect on wages, $Y$.

    Hypothesis tests for a single coefficient like the OLS slope estimator are based on the *t-statistic*,

    $$
    t = \frac{\hat{\beta}_1 - \beta_{1,H_0}}{\operatorname{se}(\hat{\beta}_1)}.
    $$

    The numerator is the gap between the estimated slope and the null value. The denominator is the standard error of the slope estimator. The t-statistic therefore measures the gap in standard-error units. For a two-sided test, the *p-value* is the probability of seeing a t-statistic at least this far from zero when the null is true,

    $$
    p = 2\cdot\Phi(-|t|),
    $$

    where $\Phi$ is the standard normal cumulative distribution. A small p-value means that the estimated slope would be surprising if the null hypothesis were true, so it counts as evidence against the null hypothesis.

    Suppose a sample gives $\hat{\beta}_1 = 1.20$ with $\operatorname{se}(\hat{\beta}_1) = 0.30$, and we test the null hypothesis of no effect. Then

    $$
    t = \frac{1.20 - 0}{0.30} = 4.0,
    $$

    and the p-value is $2\cdot\Phi(-4.0) \approx 0.00006$. An estimated slope four standard errors away from zero is very unlikely to arise from sampling error when the population slope parameter is zero, so we reject the null hypothesis of no effect.

    Note that the hypothesis itself is about the causal effect of education on wages, represented by $\beta_1$, but the test uses the estimate $\hat{\beta}_1$ to evaluate that hypothesis. When the first OLS assumption from Lecture 6 holds, $\hat{\beta}_1$ is centered on the true causal slope (i.e., $\hat{\beta}_1$ is an unbiased estimator of $\beta_1$). In that case, rejecting the null hypothesis gives evidence that the causal effect of education on wages is not zero. When the first OLS assumption fails, the hypothesis test no longer gives clear evidence about the causal effect of education on wages, but on the strength of their association.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Confidence intervals for the slope

    A hypothesis test asks whether the data are consistent with one particular guess about $\beta_1$. Often, though, we want more than a yes-or-no answer for a single guess. We want to know which values of $\beta_1$ remain plausible after looking at the data. A *confidence interval* gives us that range.

    Recall from Lecture 4 that to build a confidence interval, we start from the estimate $\hat{\beta}_1$. We then collect the null values that the test in Section 4 would not reject at a chosen *significance level* $\alpha$. The significance level is the chance of rejecting a true null that the researcher is willing to accept. A common choice is $\alpha = 0.05$.

    For large $n$, where the $t$-statistic is standard normal, that range is the estimate plus or minus a multiple of its standard error,

    $$
    \begin{aligned}
    \text{90\% interval} &= \hat{\beta}_1 \pm 1.64 \cdot \operatorname{se}(\hat{\beta}_1),\\
    \text{95\% interval} &= \hat{\beta}_1 \pm 1.96 \cdot \operatorname{se}(\hat{\beta}_1),\\
    \text{99\% interval} &= \hat{\beta}_1 \pm 2.58 \cdot \operatorname{se}(\hat{\beta}_1).
    \end{aligned}
    $$

    A 95% confidence interval is built so that, across many samples, it contains the true $\beta_1$ in 95 out of every 100 samples. With $\hat{\beta}_1 = 1.20$ and $\operatorname{se}(\hat{\beta}_1) = 0.30$, the 95% interval runs from $1.20 - 1.96(0.30) = 0.61$ to $1.20 + 1.96(0.30) = 1.79$. The whole interval lies above zero, so the data reject the null of no effect at the 5% level.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** homoskedasticity, standard error, sampling "
            "distribution, heteroskedasticity, heteroskedasticity-robust standard "
            "error, hypothesis test, null hypothesis, t-statistic, p-value, "
            "confidence interval, significance level.\n\n"
            "**Concepts:** the variance of the slope estimator and "
            "what drives it, the normal sampling distribution from the central "
            "limit theorem, testing whether a slope is zero, and a confidence "
            "interval as the set of guesses the data do not reject."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _appendix = mo.md(r"""
    This appendix derives the variance of $\hat{\beta}_1$ used in the main text. You will not be tested on it.

    **The variance of $\hat{\beta}_1$ under homoskedasticity**

    Write $S_{XX} = \sum_{i=1}^{n}(X_i - \hat{\mu}_X)^2$, so the slope estimator is

    $$
    \hat{\beta}_1 = \frac{\sum_{i=1}^{n}(X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y)}{S_{XX}}.
    $$

    Subtracting sample means in the model $Y_i = \beta_0 + \beta_1 X_i + u_i$ gives $Y_i - \hat{\mu}_Y = \beta_1 (X_i - \hat{\mu}_X) + (u_i - \bar{u})$. Substituting that into the numerator leaves

    $$
    \hat{\beta}_1 - \beta_1 = \frac{1}{S_{XX}}\sum_{i=1}^{n}(X_i - \hat{\mu}_X)\,u_i.
    $$

    Under homoskedasticity every error has the same variance $\sigma_u^2$ and the draws are independent, so the sum has variance $\sigma_u^2 \, S_{XX}$, and

    $$
    \operatorname{var}(\hat{\beta}_1) = \frac{\sigma_u^2 \, S_{XX}}{S_{XX}^2} = \frac{\sigma_u^2}{S_{XX}}.
    $$

    Replacing $\sigma_u^2$ with the residual estimate $\hat{\sigma}_u^2 = \frac{1}{n-2}\sum_{i=1}^{n}\hat{u}_i^2$ gives the standard error $\operatorname{se}(\hat{\beta}_1) = \sqrt{\hat{\sigma}_u^2 / S_{XX}}$.
    """)
    mo.accordion({"## Appendix": _appendix})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec6OLSAssumptionsForCausalInference.html" target="_self">← Lecture 6</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec8MultipleRegression.html" target="_self">Lecture 8 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
