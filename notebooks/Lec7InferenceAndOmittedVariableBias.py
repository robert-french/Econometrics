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
    app_title="Lecture 7: Inference and Omitted Variable Bias in Simple Regression",
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
            mo.md("# [Lecture 7](#top)"),
            mo.md("Inference and Omitted Variable Bias in Simple Regression"),
            mo.nav_menu(
                {
                    "#sec1": "1. The variance of the slope estimator",
                    "#sec2": "2. The sampling distribution of the slope",
                    "#sec3": "3. Heteroskedasticity",
                    "#sec4": "4. Hypothesis tests for the slope",
                    "#sec5": "5. Confidence intervals for the slope",
                    "#sec6": "6. Unbiasedness and consistency",
                    "#sec7": "7. Omitted variable bias",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec6OLSAssumptionsForCausalInference.html" target="_self">← Lecture 6</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec8MultipleRegression.html" target="_self">Lecture 8 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 7: Inference and Omitted Variable Bias in Simple Regression
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
    [5. Confidence intervals for the slope](#sec5)<br>
    [6. Unbiasedness and consistency](#sec6)<br>
    [7. Omitted variable bias](#sec7)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. The variance of the slope estimator

    Lecture 6 wrote the regression model as $Y_i = \beta_0 + \beta_1 X_i + u_i$, where the error $u_i$ collects everything other than education that moves a worker's wage. Fitting it to one sample of workers gives a single slope estimate $\hat{\beta}_1$, say a rise of \$1.20 in hourly wage for each extra year of education. That one number says nothing on its own about how firmly it is pinned down. A different sample of workers would hand us a different estimate, since the slope is computed from whichever workers happened to be drawn, and a slope built from a few dozen people can land well away from the truth. Before leaning on the estimate, we need to know how widely $\hat{\beta}_1$ would swing from one sample to the next. That swing is its variance across samples. When the spread of the error around the line is the same at every level of education, a case called *homoskedasticity*, that variance is

    $$
    \sigma^2_{\hat{\beta}_1} = \frac{\operatorname{var}(u)}{(n-1)\cdot \widehat{\operatorname{var}}(X)}.
    $$

    Section 3 takes up the opposite case, where the spread changes with education.

    We never observe $\operatorname{var}(u)$, so we estimate it from the residuals as $\widehat{\operatorname{var}}(\hat{u}) = \frac{1}{n-2}\sum_{i=1}^{n}\hat{u}_i^2$, the sum of squared residuals divided by $n-2$. The divisor is $n-2$ rather than $n$ because estimating $\hat{\beta}_0$ and $\hat{\beta}_1$ uses up two pieces of information from the sample. Putting this estimate into the formula gives the sample version,

    $$
    \hat{\sigma}^2_{\hat{\beta}_1} = \frac{\widehat{\operatorname{var}}(\hat{u})}{\sum_{i=1}^{n}(X_i - \hat{\mu}_X)^2}.
    $$

    The square root of this quantity is the *standard error* of $\hat{\beta}_1$, written $\operatorname{se}(\hat{\beta}_1)$. It is the typical distance between the estimate and the true slope, measured in the same units as the slope.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1a"></a>
    ### <span style="color:#0b68cb">What drives the variance</span>

    Three quantities in the formula set the size of $\sigma^2_{\hat{\beta}_1}$. The variance of $X$ sits in the denominator, so a wider spread of education across workers makes the slope easier to pin down and shrinks the variance. The variance of $u$ sits in the numerator, so noisier wages around the line make the slope harder to pin down and raise the variance. The sample size $n$ enters through the $(n-1)$ factor and the sum over all $n$ observations, so collecting more workers shrinks the variance. The interactive plot in Section 2 lets you change all three and watch the standard error respond.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. The sampling distribution of the slope

    Knowing the variance of $\hat{\beta}_1$ is only useful once we also know the shape of its distribution across samples. Under the three least squares assumptions from Lecture 6, that the conditional mean of the error is zero, that the data are independent and identically distributed, and that large outliers are unlikely, the estimate follows a normal distribution,

    $$
    \hat{\beta}_1 \sim \mathcal{N}\!\left(\beta_1,\ \sigma^2_{\hat{\beta}_1}\right).
    $$

    The result comes from the central limit theorem of Lecture 2. The slope estimate can be written as a kind of sample average over the $n$ workers, and a sample average of independent draws is close to normal once $n$ is reasonably large. The center of the distribution is the true slope $\beta_1$, and its spread is the standard error from Section 1.

    The plot below makes this concrete. Set the sliders, then press Draw new sample. Each draw shows one sample of workers, fits the OLS line, and reports its standard error. The orange dashed lines are the slopes 1.96 standard errors to each side, the reach of a 95% confidence interval. Each draw also drops its slope estimate into the histogram beneath, so repeated draws build up the sampling distribution by hand. Press Reset histogram to empty it, and reset after moving a slider so the collected slopes all come from the same settings.
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
    reset_button = mo.ui.button(label="Reset histogram", on_change=_on_reset)

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
        f"the axis. The shaded curve is their kernel density, scaled so the area "
        f"under it is one. The orange line marks the true slope of 1.2. Keep "
        f"drawing and the density piles up into a bell centered there."
    )
    if _show_normal:
        _body += " The grey dashed curve is the normal density the theory predicts."
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

    The variance formula in Section 1 assumed the error spread is the same at every level of education. The error is *heteroskedastic* when that spread changes with $X$. Wages fit this case. Among workers with little education, hourly wages sit in a narrow band near the bottom. Among workers with a college degree, some earn close to the average for their group while others earn far more, so the band of wages is much wider.

    We never see $u$ itself, but the residuals $\hat{u}_i = Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i$ estimate it, and their spread is what a scatter plot shows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3a"></a>
    ### <span style="color:#0b68cb">Heteroskedasticity-robust standard errors</span>

    The equal-spread formula gives the wrong variance once the error is heteroskedastic, so a standard error built from it can be too small or too large. The fix keeps the same idea but weights each observation by how far its education sits from the average,

    $$
    \hat{\sigma}^2_{\hat{\beta}_1} = \frac{1}{n} \cdot \frac{\frac{1}{n-2}\sum_{i=1}^{n}(X_i-\hat{\mu}_X)^2\,\hat{u}_i^2}{\left[\frac{1}{n}\sum_{i=1}^{n}(X_i-\hat{\mu}_X)^2\right]^2}.
    $$

    This is the *heteroskedasticity-robust standard error*. It lets the spread of the error change with $X$, and it counts a large residual more heavily when that residual sits far from the average education, since a point far out on the horizontal axis has more pull on the slope. Robust standard errors are correct whether or not the error is homoskedastic, so regression software reports them by default and this course uses them throughout.

    The plot below puts the two estimates side by side. The five sliders set the error spread in five slices of the education range, from the least educated on the left to the most educated on the right. When all five are equal the spread is the same everywhere; raising some above the others concentrates the variance. Beneath the plot, the equal-spread estimate of the variance of $\hat{\beta}_1$ sits next to the robust estimate. With the sliders level the two nearly match. As the spread varies across the range, they pull apart, and the equal-spread estimate is the one that goes wrong.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _opts = dict(start=1.0, stop=10.0, step=0.5, value=2.5, show_value=True, full_width=True)
    het_s1 = mo.ui.slider(label="8-10", **_opts)
    het_s2 = mo.ui.slider(label="10-12", **_opts)
    het_s3 = mo.ui.slider(label="12-14", **_opts)
    het_s4 = mo.ui.slider(label="14-16", **_opts)
    het_s5 = mo.ui.slider(label="16-18", **_opts)
    # The negative left margin slides the whole slider row left so each thin
    # slider sits closer to its slice; tune the inch value to nudge it.
    _row = mo.hstack(
        [mo.Html("<div></div>"), het_s1, het_s2, het_s3, het_s4, het_s5],
        widths=[0.1, 1, 1, 1, 1, 1],
        gap=0.4,
    ).style({"margin-left": "-0.5in"})
    mo.vstack([
        mo.md("Error spread (standard deviation) in each slice of the education range"),
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
            mo.md("**Equal-spread (homoskedastic)**"),
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
            "The spread is the same in every slice, so the error is homoskedastic and "
            "the two estimates of the variance of the slope nearly match."
        )
    else:
        _msg = (
            "The spread differs across slices, so the error is heteroskedastic. The two "
            "estimates have pulled apart, and the equal-spread estimate no longer reports "
            "the right variance."
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
    ## 4. Hypothesis tests for the slope

    A common question is whether education affects wages at all, which is the claim that the true slope is zero. A *hypothesis test* compares a specific guess about $\beta_1$, the null hypothesis $H_0:\ \beta_1 = \beta_{1,H_0}$, against the estimate. The guess we test is usually $\beta_{1,H_0} = 0$, since that is the case of no effect.

    The test rests on the *t-statistic*,

    $$
    t = \frac{\hat{\beta}_1 - \beta_{1,H_0}}{\operatorname{se}(\hat{\beta}_1)},
    $$

    which counts how many standard errors separate the estimate from the guess. When the null hypothesis is true, $t$ follows the standard normal distribution from Lecture 2, so values far from zero are unlikely. The *p-value* is the probability of seeing a $t$-statistic at least this far from zero when the null is true, $p = 2\,\Phi(-|t|)$, where $\Phi$ is the standard normal cumulative distribution. A small p-value means the estimate would be surprising if the slope really were $\beta_{1,H_0}$, which counts as evidence against the null.

    Suppose a sample gives $\hat{\beta}_1 = 1.20$ with $\operatorname{se}(\hat{\beta}_1) = 0.30$, testing the null of no effect. Then $t = 1.20 / 0.30 = 4.0$, and the p-value is $2\,\Phi(-4.0) \approx 0.00006$. An estimate four standard errors away from zero is so unlikely when the slope is really zero that we reject the null.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Confidence intervals for the slope

    A hypothesis test checks one guess about $\beta_1$ at a time. A *confidence interval* reports the whole range of guesses the data do not reject. Start from the estimate $\hat{\beta}_1$ and collect every null value the test in Section 4 would not reject at a chosen *significance level* $\alpha$, the chance of rejecting a true null that the researcher is willing to accept, commonly $\alpha = 0.05$.

    For large $n$, where the $t$-statistic is standard normal, that range is the estimate plus or minus a multiple of its standard error,

    $$
    \begin{aligned}
    \text{90\% interval} &= \hat{\beta}_1 \pm 1.64 \cdot \operatorname{se}(\hat{\beta}_1),\\
    \text{95\% interval} &= \hat{\beta}_1 \pm 1.96 \cdot \operatorname{se}(\hat{\beta}_1),\\
    \text{99\% interval} &= \hat{\beta}_1 \pm 2.58 \cdot \operatorname{se}(\hat{\beta}_1).
    \end{aligned}
    $$

    A 95% confidence interval is built so that, across many samples, the interval holds the true $\beta_1$ in 95 of every 100. With $\hat{\beta}_1 = 1.20$ and $\operatorname{se}(\hat{\beta}_1) = 0.30$, the 95% interval runs from $1.20 - 1.96(0.30) = 0.61$ to $1.20 + 1.96(0.30) = 1.79$. That interval lies entirely above zero, so the data reject the null of no effect at the 5% level, which matches the small p-value from Section 4.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec6"></a>
    ## 6. Unbiasedness and consistency

    The normal sampling distribution in Section 2 is centered on the true slope, and two properties explain why. The estimator $\hat{\beta}_1$ is *unbiased* when its average across all possible samples equals the true value,

    $$
    \mathbb{E}[\hat{\beta}_1] = \beta_1.
    $$

    Unbiasedness holds as long as the first least squares assumption holds, that the conditional mean of the error given $X$ is zero. The appendix shows the few lines of algebra. Unbiasedness does not say a single estimate equals $\beta_1$, only that estimates are right on average rather than systematically too high or too low.

    The estimator is also *consistent*, meaning it converges to the true value as the sample grows,

    $$
    \hat{\beta}_1 \overset{p}{\to} \beta_1.
    $$

    Consistency follows from the variance in Section 1 shrinking toward zero as $n$ grows, which pulls the whole sampling distribution in around $\beta_1$. The histogram in Section 2 shows this directly, with a larger sample size squeezing the collected slopes against the line at the true value.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec7"></a>
    ## 7. Omitted variable bias

    Every property in this lecture rested on the first least squares assumption, that the conditional mean of the error given $X$ is zero. That assumption fails whenever a variable left out of the regression both belongs in the error and moves with education. When the omitted variable is correlated with $X$, the error is correlated with $X$, written $\operatorname{cov}(X,u) \neq 0$, and then $\mathbb{E}[u\mid X]\neq 0$. The estimate no longer centers on the true slope. This is *omitted variable bias*.

    With such a variable left out, the slope estimate converges not to $\beta_1$ but to

    $$
    \hat{\beta}_1 \overset{p}{\to} \beta_1 + \operatorname{corr}(X,u)\cdot\frac{\sigma_u}{\sigma_X} = \beta_1 + \rho_{Xu}\,\frac{\sigma_u}{\sigma_X}.
    $$

    The second term is the bias, and its sign is the sign of the correlation between $X$ and the omitted part of the error. Two conditions are both needed for the bias to appear. The omitted variable must be correlated with $X$, and it must affect $Y$ so that it carries real weight inside the error. If either fails, the bias term is zero and the estimate stays on target.

    Return to the wage regression. Ability is left out of the error, and it raises both schooling and earnings, so education and the error are positively correlated. The bias term is then positive, and the estimated return to schooling comes out too high, because we credit schooling with part of what is really the payoff to ability.

    A second case is new housing and rents. Let $Y$ be local home prices and $X$ the number of new units built. Developers build more when interest rates are low, and low rates also raise demand and push prices up, so the omitted interest-rate conditions are positively correlated with building. The estimated effect of new supply on prices is biased upward for the same reason.

    Omitted variable bias is why a single explanatory variable is rarely enough for a causal claim. The next notebook adds more variables to the regression so that a factor like ability can be held constant instead of left in the error.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** homoskedasticity, standard error, sampling "
            "distribution, heteroskedasticity, heteroskedasticity-robust standard "
            "error, hypothesis test, null hypothesis, t-statistic, p-value, "
            "confidence interval, significance level, unbiasedness, consistency, "
            "omitted variable bias.\n\n"
            "**Key concepts covered:** the variance of the slope estimator and "
            "what drives it, the normal sampling distribution from the central "
            "limit theorem, testing whether a slope is zero, a confidence "
            "interval as the set of guesses the data do not reject, the bias "
            "formula and its two conditions."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _appendix = mo.md(r"""
    This appendix derives the two results used in the main text. You will not be tested on it.

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

    **Unbiasedness of $\hat{\beta}_1$**

    Start from the same identity. Take the expectation conditional on the values of $X$. The first least squares assumption $\mathbb{E}[u_i \mid X] = 0$ makes every term in the sum have conditional mean zero, so

    $$
    \mathbb{E}[\hat{\beta}_1 - \beta_1 \mid X] = \frac{1}{S_{XX}}\sum_{i=1}^{n}(X_i - \hat{\mu}_X)\,\mathbb{E}[u_i \mid X] = 0.
    $$

    So $\mathbb{E}[\hat{\beta}_1 \mid X] = \beta_1$, and averaging over $X$ by the law of iterated expectations gives $\mathbb{E}[\hat{\beta}_1] = \beta_1$.
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
