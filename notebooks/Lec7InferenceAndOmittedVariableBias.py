# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "numpy",
#     "pandas",
#     "altair",
#     "scipy",
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
                    "#sec1": "1. Homoskedasticity and heteroskedasticity",
                    "#sec2": "2. The variance of the slope estimator",
                    "#sec2a": "What drives the variance",
                    "#sec2b": "Heteroskedasticity-robust standard errors",
                    "#sec3": "3. The sampling distribution of the slope",
                    "#sec4": "4. Hypothesis tests for the slope",
                    "#sec5": "5. Confidence intervals for the slope",
                    "#sec6": "6. Unbiasedness and consistency",
                    "#sec7": "7. Omitted variable bias",
                    "#appendix": "Appendix",
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

    [1. Homoskedasticity and heteroskedasticity](#sec1)<br>
    [2. The variance of the slope estimator](#sec2)<br>
    &emsp;&emsp;[What drives the variance](#sec2a)<br>
    &emsp;&emsp;[Heteroskedasticity-robust standard errors](#sec2b)<br>
    [3. The sampling distribution of the slope](#sec3)<br>
    [4. Hypothesis tests for the slope](#sec4)<br>
    [5. Confidence intervals for the slope](#sec5)<br>
    [6. Unbiasedness and consistency](#sec6)<br>
    [7. Omitted variable bias](#sec7)<br>
    [Appendix](#appendix)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Homoskedasticity and heteroskedasticity

    Lecture 6 wrote the regression model as $Y_i = \beta_0 + \beta_1 X_i + u_i$, where the error $u_i$ collects everything other than education that moves a worker's wage. That error has a spread around the line, and the size of that spread can either stay the same across education levels or change with them.

    The error is *homoskedastic* when the variance of $u$ does not depend on $X$, so the vertical spread of wages around the line is the same at eight years of education as it is at twenty. The error is *heteroskedastic* when that variance changes with $X$. Wages fit the heteroskedastic case. Among workers with little education, hourly wages sit in a narrow band near the bottom. Among workers with a college degree, some earn close to the average for their group while others earn far more, so the band of wages is much wider.

    We never see $u$ itself, but the residuals $\hat{u}_i = Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i$ estimate it, and their spread is what a scatter plot shows. The slider below grows that spread with education. At zero the band has the same width everywhere. Move it toward one and the points fan out toward the right.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    het_strength = mo.ui.slider(
        start=0.0, stop=1.0, step=0.1, value=0.0,
        label="How much does the spread grow with education?",
        show_value=True,
    )
    het_strength
    return (het_strength,)


@app.cell(hide_code=True)
def _(alt, het_strength, mo, np, pd):
    _rng = np.random.default_rng(7)
    _n = 140
    _b0, _b1 = 8.0, 1.2
    _X = _rng.uniform(8.0, 20.0, _n)
    _Z = _rng.standard_normal(_n)
    _het = float(het_strength.value)
    _scale = 1.0 + _het * (_X - 8.0) / 6.0
    _Y = _b0 + _b1 * _X + 2.5 * _scale * _Z

    _b1h = float(np.cov(_X, _Y, ddof=1)[0, 1] / np.var(_X, ddof=1))
    _b0h = float(_Y.mean() - _b1h * _X.mean())
    _xline = np.array([8.0, 20.0])
    _pts = pd.DataFrame({"x": _X, "y": _Y})
    _fit = pd.DataFrame({"x": _xline, "y": _b0h + _b1h * _xline})

    _xdom = [7.0, 21.0]
    _ydom = [0.0, 50.0]
    _scatter = (
        alt.Chart(_pts)
        .mark_circle(color="#1f4e79", opacity=0.6, size=55, clip=True)
        .encode(
            x=alt.X("x:Q", title="Years of education", scale=alt.Scale(domain=_xdom, nice=False)),
            y=alt.Y("y:Q", title="Hourly wage (USD)", scale=alt.Scale(domain=_ydom, nice=False)),
        )
    )
    _line = (
        alt.Chart(_fit)
        .mark_line(color="orange", size=2.5, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _chart = (_scatter + _line).properties(
        width=560, height=340, title="Wages and education, with the OLS line"
    )

    if _het == 0.0:
        _body = (
            "The vertical spread of wages around the line is the same at every "
            "level of education. This is the homoskedastic case."
        )
    else:
        _body = (
            "The points now fan out as education rises, so wages are more spread "
            "out among the highly educated than among the least educated. This is "
            "the heteroskedastic case. The orange line barely moves, because "
            "heteroskedasticity changes the spread around the line, not its slope."
        )
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 1rem;max-width:560px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _body + "</span>"
    )
    mo.vstack([_chart, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. The variance of the slope estimator

    The slope estimate $\hat{\beta}_1$ changes from one sample to the next, because each sample draws different workers. To judge how far a single estimate might sit from the truth, we need the variance of $\hat{\beta}_1$ across samples. When the error is homoskedastic, that variance is

    $$
    \sigma^2_{\hat{\beta}_1} = \frac{\operatorname{var}(u)}{(n-1)\cdot \widehat{\operatorname{var}}(X)}.
    $$

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
    <a id="sec2a"></a>
    ### <span style="color:#0b68cb">What drives the variance</span>

    Three quantities in the formula set the size of $\sigma^2_{\hat{\beta}_1}$. The variance of $X$ sits in the denominator, so a wider spread of education across workers makes the slope easier to pin down and shrinks the variance. The variance of $u$ sits in the numerator, so noisier wages around the line make the slope harder to pin down and raise the variance. The sample size $n$ enters through the $(n-1)$ factor and the sum over all $n$ observations, so collecting more workers shrinks the variance.

    The plot below draws a fresh sample of workers and reports $\operatorname{se}(\hat{\beta}_1)$. The black line is the OLS fit, and the orange dashed lines are the slopes 1.96 standard errors on either side, the edge of a 95% confidence interval for the slope. Raise the sample size or widen the spread of education and the orange fan tightens. Raise the error spread and it widens.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    vd_n = mo.ui.slider(
        start=20, stop=400, step=20, value=80,
        label="Sample size (n)", show_value=True,
    )
    vd_xspread = mo.ui.slider(
        start=1.0, stop=6.0, step=0.5, value=3.5,
        label="Spread of education (standard deviation of X)", show_value=True,
    )
    vd_errsd = mo.ui.slider(
        start=1.0, stop=8.0, step=0.5, value=3.0,
        label="Error standard deviation", show_value=True,
    )
    vd_button = mo.ui.button(
        label="Draw new sample", value=0, on_click=lambda c: c + 1,
    )
    mo.vstack([vd_n, vd_xspread, vd_errsd, vd_button])
    return vd_button, vd_errsd, vd_n, vd_xspread


@app.cell(hide_code=True)
def _(alt, mo, np, pd, vd_button, vd_errsd, vd_n, vd_xspread):
    _rng = np.random.default_rng(20 + vd_button.value)
    _n = int(vd_n.value)
    _xsd = float(vd_xspread.value)
    _esd = float(vd_errsd.value)
    _b0, _b1 = 8.0, 1.2
    _xbar = 14.0
    _Zx = _rng.standard_normal(_n)
    _Zu = _rng.standard_normal(_n)
    _X = _xbar + _xsd * _Zx
    _Y = _b0 + _b1 * _X + _esd * _Zu

    _b1h = float(np.cov(_X, _Y, ddof=1)[0, 1] / np.var(_X, ddof=1))
    _b0h = float(_Y.mean() - _b1h * _X.mean())
    _resid = _Y - (_b0h + _b1h * _X)
    _sxx = float(np.sum((_X - _X.mean()) ** 2))
    _varhat = float(np.sum(_resid ** 2) / max(_n - 2, 1))
    _se = float(np.sqrt(_varhat / _sxx))

    _xb = float(_X.mean())
    _yb = float(_Y.mean())
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
        width=560, height=340,
        title="A fresh sample, its OLS line, and the slope uncertainty",
    )

    _lo = _b1h - 1.96 * _se
    _hi = _b1h + 1.96 * _se
    _body = (
        rf"This sample gives $\hat{{\beta}}_1 = {_b1h:.2f}$ with "
        rf"$\operatorname{{se}}(\hat{{\beta}}_1) = {_se:.3f}$, so a 95% confidence "
        rf"interval for the slope runs from {_lo:.2f} to {_hi:.2f}. The orange "
        rf"dashed lines are the slopes 1.96 standard errors to each side. Raise "
        rf"the sample size or the spread of education and the fan tightens. Raise "
        rf"the error standard deviation and it widens."
    )
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 1rem;max-width:560px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _body + "</span>"
    )
    mo.vstack([_chart, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2b"></a>
    ### <span style="color:#0b68cb">Heteroskedasticity-robust standard errors</span>

    The formula above assumed the error is homoskedastic. When the error is heteroskedastic, that formula is wrong, and a standard error built from it can be too small or too large. The fix keeps the same idea but weights each observation by how far its education sits from the average,

    $$
    \hat{\sigma}^2_{\hat{\beta}_1} = \frac{1}{n} \cdot \frac{\frac{1}{n-2}\sum_{i=1}^{n}(X_i-\hat{\mu}_X)^2\,\hat{u}_i^2}{\left[\frac{1}{n}\sum_{i=1}^{n}(X_i-\hat{\mu}_X)^2\right]^2}.
    $$

    This is the *heteroskedasticity-robust standard error*. It lets the spread of the error change with $X$, and it counts a large residual more heavily when that residual sits far from the average education, since a point far out on the horizontal axis has more pull on the slope. Robust standard errors are correct whether or not the error is homoskedastic, so regression software reports them by default and this course uses them throughout.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. The sampling distribution of the slope

    Knowing the variance of $\hat{\beta}_1$ is only useful once we also know the shape of its distribution across samples. Under the three least squares assumptions from Lecture 6, that the conditional mean of the error is zero, that the data are independent and identically distributed, and that large outliers are unlikely, the estimate follows a normal distribution,

    $$
    \hat{\beta}_1 \sim \mathcal{N}\!\left(\beta_1,\ \sigma^2_{\hat{\beta}_1}\right).
    $$

    The result comes from the central limit theorem of Lecture 2. The slope estimate can be written as a kind of sample average over the $n$ workers, and a sample average of independent draws is close to normal once $n$ is reasonably large. The center of the distribution is the true slope $\beta_1$, and its spread is the standard error from Section 2.

    The histogram below draws many samples, computes $\hat{\beta}_1$ in each one, and stacks the estimates. The orange curve is the normal distribution the theory predicts. Raise the sample size and the histogram pulls in tightly around the true slope, marked by the orange vertical line.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    sdist_n = mo.ui.slider(
        start=20, stop=200, step=20, value=80,
        label="Sample size (n)", show_value=True,
    )
    sdist_errsd = mo.ui.slider(
        start=1.0, stop=8.0, step=0.5, value=3.0,
        label="Error standard deviation", show_value=True,
    )
    sdist_reps = mo.ui.slider(
        start=200, stop=3000, step=100, value=1500,
        label="Number of samples", show_value=True,
    )
    sdist_button = mo.ui.button(
        label="Draw new samples", value=0, on_click=lambda c: c + 1,
    )
    mo.vstack([sdist_n, sdist_errsd, sdist_reps, sdist_button])
    return sdist_button, sdist_errsd, sdist_n, sdist_reps


@app.cell(hide_code=True)
def _(np, sdist_button):
    # New samples are drawn only when the button is clicked (the seed depends
    # only on the button). The sliders below slice and rescale this pool, so
    # dragging them does not reroll the underlying draws.
    _MAX, _NMAX = 3000, 200
    _rng = np.random.default_rng(11 + sdist_button.value)
    sdist_Xpool = _rng.normal(14.0, 3.5, (_MAX, _NMAX))
    sdist_Upool = _rng.standard_normal((_MAX, _NMAX))
    return sdist_Upool, sdist_Xpool


@app.cell(hide_code=True)
def _(alt, mo, np, pd, sdist_Upool, sdist_Xpool, sdist_errsd, sdist_n, sdist_reps, stats):
    _n = int(sdist_n.value)
    _esd = float(sdist_errsd.value)
    _reps = int(sdist_reps.value)
    _b0, _b1 = 8.0, 1.2

    _Xs = sdist_Xpool[:_reps, :_n]
    _Us = sdist_Upool[:_reps, :_n] * _esd
    _Ys = _b0 + _b1 * _Xs + _Us

    _Xm = _Xs.mean(axis=1, keepdims=True)
    _Ym = _Ys.mean(axis=1, keepdims=True)
    _num = ((_Xs - _Xm) * (_Ys - _Ym)).sum(axis=1)
    _den = ((_Xs - _Xm) ** 2).sum(axis=1)
    _b1hats = _num / _den

    _hist = (
        alt.Chart(pd.DataFrame({"b": _b1hats}))
        .mark_bar(color="#1f4e79", opacity=0.85)
        .encode(
            x=alt.X("b:Q", bin=alt.Bin(maxbins=40), title="Estimated slope"),
            y=alt.Y("count()", title="Number of samples"),
        )
    )
    _rule = (
        alt.Chart(pd.DataFrame({"b": [_b1]}))
        .mark_rule(color="orange", size=2.5)
        .encode(x="b:Q")
    )

    _se_theory = _esd / (3.5 * (_n ** 0.5))
    _lo = float(_b1hats.min())
    _hi = float(_b1hats.max())
    if _hi > _lo and _se_theory > 0:
        _grid = np.linspace(_lo, _hi, 200)
        _binw = (_hi - _lo) / 40.0
        _curve = (
            alt.Chart(pd.DataFrame({
                "b": _grid,
                "count": stats.norm.pdf(_grid, _b1, _se_theory) * _reps * _binw,
            }))
            .mark_line(color="orange", size=2)
            .encode(x="b:Q", y="count:Q")
        )
        _chart = _hist + _curve + _rule
    else:
        _chart = _hist + _rule

    _chart = _chart.properties(
        width=560, height=320,
        title="Distribution of the slope estimate across many samples",
    )

    _body = (
        rf"Each of the {_reps} samples holds {_n} workers and gives its own slope "
        rf"estimate $\hat{{\beta}}_1$. The estimates pile up in a bell centered on "
        rf"the true slope $\beta_1 = {_b1:.1f}$, the orange line, with a standard "
        rf"error near {_se_theory:.3f}. Raise the sample size and the bell tightens "
        rf"against the true slope, which is what consistency means."
    )
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 1rem;max-width:560px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _body + "</span>"
    )
    mo.vstack([_chart, _caption])
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

    The normal sampling distribution in Section 3 is centered on the true slope, and two properties explain why. The estimator $\hat{\beta}_1$ is *unbiased* when its average across all possible samples equals the true value,

    $$
    \mathbb{E}[\hat{\beta}_1] = \beta_1.
    $$

    Unbiasedness holds as long as the first least squares assumption holds, that the conditional mean of the error given $X$ is zero. The appendix shows the few lines of algebra. Unbiasedness does not say a single estimate equals $\beta_1$, only that estimates are right on average rather than systematically too high or too low.

    The estimator is also *consistent*, meaning it converges to the true value as the sample grows,

    $$
    \hat{\beta}_1 \overset{p}{\to} \beta_1.
    $$

    Consistency follows from the variance in Section 2 shrinking toward zero as $n$ grows, which pulls the whole sampling distribution in around $\beta_1$. The sampling-distribution plot in Section 3 showed this directly, with a larger sample size squeezing the histogram against the line at the true slope.
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
            "**Key terms covered:** homoskedasticity, heteroskedasticity, "
            "standard error, heteroskedasticity-robust standard error, sampling "
            "distribution, hypothesis test, null hypothesis, t-statistic, "
            "p-value, confidence interval, significance level, unbiasedness, "
            "consistency, omitted variable bias.\n\n"
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
    mo.md(r"""
    <a id="appendix"></a>
    ## Appendix
    """)
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
    mo.accordion({"Bonus material (not on assessments)": _appendix})
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
