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

__generated_with = "0.23.6"
app = marimo.App(
    app_title="Lecture 4: Estimation, Hypothesis Testing, and Confidence Intervals",
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
                4. **[Estimation and Hypothesis Testing](#top)**
                    1. [Estimators and estimates](#sec1)
                    1. [Bias and consistency](#sec2)
                    1. [Mean squared error and efficiency](#sec3)
                    1. [Hypothesis tests](#sec4)
                    1. [P-values and the t-statistic](#sec5)
                    1. [Confidence intervals](#sec6)
                5. <a href="https://robert-french.github.io/Econometrics/apps/Lec5SimpleLinearRegression.html" target="_self">Simple Linear Regression</a>
                6. <a href="https://robert-french.github.io/Econometrics/apps/Lec6OLSAssumptionsForCausalInference.html" target="_self">OLS Assumptions for Causal Inference</a>
                7. <a href="https://robert-french.github.io/Econometrics/apps/Lec7InferenceAndOmittedVariableBias.html" target="_self">Inference and Omitted Variable Bias</a>
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec3WorkingWithMultipleRandomVariables.html" target="_self">← Lecture 3</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/pdf/Lec4EstimationHypothesisTestingAndConfidenceIntervals.pdf" target="_blank">Download PDF</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec5SimpleLinearRegression.html" target="_self">Lecture 5 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 4: Estimation, Hypothesis Testing, and Confidence Intervals
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contents

    4.1 [Estimators and estimates](#sec1)<br>
    4.2 [Bias and consistency](#sec2)<br>
    4.3 [Mean squared error and efficiency](#sec3)<br>
    4.4 [Hypothesis tests](#sec4)<br>
    4.5 [P-values and the t-statistic](#sec5)<br>
    4.6 [Confidence intervals](#sec6)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 4.1 Estimators and estimates

    The previous two lectures introduced random variables and their distributions. We now turn to the central task of statistical inference, which is using a sample of data to learn about a population we cannot fully observe.

    An *estimator* is a rule that turns a random sample into a guess about a population quantity, often called a *parameter*. The sample mean $\hat{\mu}_X = \frac{1}{n}\sum_{i=1}^{n} X_i$ is an estimator of the population mean $\mu_X$, a parameter. Because the sample is drawn at random, the estimator is itself a random variable, with a distribution, an expected value, and a variance, exactly like the random variables from Lecture 2. The particular number an estimator produces from one specific sample is called an *estimate*. The estimator is the rule, and the estimate is the realized number, in the same way that a random variable is a rule and its realization is a single observed data point.

    A population quantity, or parameter, can be estimated in more than one way. To see this, suppose we want to estimate the expected value of a fair die roll, which we know is equal to $\left(\frac{1}{6} + \frac{2}{6} + \frac{3}{6} + \frac{4}{6} + \frac{5}{6} + \frac{6}{6} \right) = 3.5$. We could use the sample mean of $n$ rolls, or only the first value of $n$ rolls, or the lowest value among $n$ rolls. Each of these is a valid estimator, and each produces a different guess. Some estimators are clearly better than others, so we need a way to compare them. The next two sections give three properties that help us evaluate the quality of an estimator.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 4.2 Bias and consistency

    The first property concerns where an estimator is centered across repeated samples of the same size. The *bias* of an estimator $\hat{\theta}$ of a population quantity $\theta$ is the difference between the estimator’s expected value and the population quantity,

    $$
    \text{Bias}(\hat{\theta}) = \mathbb{E}[\hat{\theta}] - \theta.
    $$

    An estimator is *unbiased* when this difference is zero, so that $\mathbb{E}[\hat{\theta}] = \theta$. This does not mean that every estimate equals the true parameter. A single sample can still produce an estimate that is too high or too low. Unbiasedness means that if we could draw many independent samples of the same size and recompute the estimate from each one, those estimates would be centered around the true parameter.

    The sample mean is unbiased because $\mathbb{E}[\hat{\mu}_X] = \mu_X$, a fact we saw in Lecture 2. A single die roll is also unbiased for the value $3.5$, because the expected outcome of one roll is $3.5$. The lowest of $n$ rolls, by contrast, is biased downward, since the smallest of several rolls tends to be below $3.5$.

    The second property concerns what happens as the sample size, $n$, grows large. An estimator is *consistent* when it gets closer and closer to the parameter as the sample size increases. We write this as

    $$
    \hat{\theta} \xrightarrow{p} \theta,
    $$

    which reads as ''$\hat{\theta}$ converges in probability to $\theta$''. It means that, with enough data, the probability that the estimate sits far from the true parameter shrinks toward zero.

    The sample mean is consistent by the law of large numbers from Lecture 2, since $\hat{\mu}_X \xrightarrow{p} \mu_X$ as $n$ grows. A single die roll is not consistent because it does not use the additional data. Even if we collect more rolls, an estimator based only on the first roll does not become more reliable.

    Bias and consistency are separate ideas. A single die roll is unbiased for $3.5$ but not consistent. Going the other way, the sample mean plus $1/n$ is biased in any finite sample, since $\mathbb{E}[\hat{\mu}_X + 1/n] = \mu_X + 1/n > \mu_X$, yet it is consistent because the $1/n$ term becomes vanishingly small as $n$ grows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 4.3 Mean squared error and efficiency

    Bias and consistency each capture one aspect of a good estimator, but we often want a single number that measures how close an estimator lands to the true parameter value. The *mean squared error* averages the squared distance between the estimator and the true parameter value,

    $$ \text{MSE}(\hat{\theta}) = \mathbb{E}\big[(\hat{\theta} - \theta)^2\big]. $$

    An estimator with a smaller mean squared error is generally preferable because it tends to produce estimates closer to the true parameter. The mean squared error splits cleanly into two parts, the variance of the estimator and its squared bias,

    $$ \text{MSE}(\hat{\theta}) = \text{var}(\hat{\theta}) + \text{Bias}(\hat{\theta})^2. $$

    The appendix proves this. The split shows the two ways an estimator can miss. It can be off-center, which is captured by the bias term, or it can be noisy from one sample to the next, which is captured in the variance term. A good estimator keeps both small.

    When we compare two unbiased estimators, the bias term is zero for both, so the one with the smaller variance has the smaller mean squared error. We say that an unbiased estimator $\hat{\theta}_1$ is more *efficient* than another unbiased estimator $\hat{\theta}_2$ when it has a smaller variance, $\text{var}(\hat{\theta}_1) < \text{var}(\hat{\theta}_2)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4.4 Hypothesis tests

    Estimation gives us a best guess about a population quantity. A *hypothesis test* asks whether the data provide enough evidence against a specific claim about that quantity.

    The claim being tested is called the *null hypothesis* and is written as $H_0$. The competing claim is called the *alternative hypothesis* and is written as $H_1$. A hypothesis test uses a sample to decide whether to reject $H_0$ in favor of $H_1$, or whether the evidence is not strong enough to reject $H_0$.

    For example, suppose we want to test whether the mean hourly earnings of recent college graduates is \$20. Let $\mu_X$ be the population mean hourly earnings of recent college graduates. The null hypothesis is

    $$
    H_0: \mu_X = 20.
    $$

    The alternative hypothesis depends on the question we want to ask. A *two-sided alternative* allows the mean to be either above or below \$20,

    $$
    H_1: \mu_X \neq 20.
    $$

    A *one-sided alternative* allows only one direction. For example, if we want to know whether mean hourly earnings are below \$20, we would write

    $$
    H_1: \mu_X < 20.
    $$

    Throughout this course, however, we will focus on two-sided alternative hypotheses. The next section explains how we measure the strength of the evidence against $H_0$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 4.5 P-values and the t-statistic

    Suppose the null hypothesis says that the population mean is $\mu_{X,0}$, and our estimator is the sample mean, $\hat{\mu}_X$. In any particular sample, the estimate may come out above or below the null value, $\mu_{X,0}$. If the estimate is far from $\mu_{X,0}$, there are two possible explanations. The null may be false, meaning the true population mean differs from $\mu_{X,0}$, or the null may be true and our sample happened to produce an estimate far from the null value by chance.

    A *p-value* measures how surprising our estimate would be if the null hypothesis were true. For a two-sided test, it is the probability, computed assuming the null hypothesis is true, of obtaining an estimate at least as far from $\mu_{X,0}$ as the estimate we actually observed,

    $$
    p\text{-value}
    =
    \mathbb{P}_{H_0}
    \left(
    \left| \hat{\mu}_X - \mu_{X,0} \right|
    \geq
    \left| \hat{\mu}_X^{\text{est}} - \mu_{X,0} \right|
    \right).
    $$

    In the expression above, $\hat{\mu}_X^{\text{est}}$ is the estimate computed from the actual sample.<sup><a id="fnref1" href="#fn1">1</a></sup> A small p-value means that estimates this far from the null value would be unlikely if the null were true, so small p-values count as evidence against the null. To compute the p-value, we first convert the gap between the estimate and the null value into a *test statistic*, a number that measures how far the data are from what the null predicts. The *t-statistic* is one such test statistic. It divides the gap between the estimate and the null value by the estimator's standard error, so the gap is measured in standard-error units:


    $$
    t
    =
    \frac{\hat{\mu}_X - \mu_{X,0}}{\text{se}(\hat{\mu}_X)}.
    $$

    The standard error measures how much the estimator $\hat{\mu}_X$ varies across repeated samples. Recall from Lecture 2 that the estimated standard error of the sample mean is $\text{se}(\hat{\mu}_X) = \hat{\sigma}_X / \sqrt{n}$. When the null hypothesis is true and $n$ is large, the central limit theorem tells us that the t-statistic is approximately standard normal, $t \sim \mathcal{N}(0,1)$.


    The two-sided p-value is therefore the probability that a standard normal random variable lands at least $|t^{\text{est}}|$ distance away from zero in either direction,

    $$
    p = 2\Phi(-|t^{\text{est}}|),
    $$

    where $\Phi$ is the cumulative distribution function of the standard normal distribution and $t^{\text{est}}$ is the t-statistic evaluated at the estimate $\hat{\mu}_X^{\text{est}}$.

    We reject the null hypothesis when the p-value falls below a chosen *significance level* $\alpha$. The significance level is the cutoff we choose before conducting the test for how much evidence is enough to reject the null. The most common choice is $\alpha = 0.05$, so we reject $H_0$ when the p-value is less than $0.05$.

    ### <span style="color:#0b68cb">Hypothesis testing example</span>

    Recall the earnings example and suppose a large sample gives an estimate for the mean wage of $\hat{\mu}_X^{\text{est}} = 22$, with a standard error of $1$. Let the null hypothesis be $H_0: \mu_X = 20$, so the t-statistic is $t^{\text{est}} = \frac{22 - 20}{1} = 2.0.$ The corresponding two-sided p-value is then $p = 2\Phi(-2.0) \approx 0.046.$ We therefore reject the null hypothesis that mean hourly earnings equal \$20 when $\alpha = 0.05$ because $0.046 < 0.05$.

    Now explore hypothesis testing interactively. The plot below shows how the two-sided p-value for this example changes with the estimate, $\hat{\mu}_X^{\text{est}}$, standard error, $\text{se}(\hat{\mu}_X)$, and chosen significance level, $\alpha$, when testing the null that the mean wage equals \$20.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pv_est = mo.ui.number(
        value=22.0, start=0.0, stop=100.0, step=0.5,
        label=r"$\hat{\mu}_X^{\text{est}}$",
    )
    pv_se = mo.ui.number(
        value=1.0, start=-10.0, stop=50.0, step=0.25,
        label=r"$\text{se}(\hat{\mu}_X)$",
    )
    pv_alpha = mo.ui.dropdown(
        options={"0.10": 0.10, "0.05": 0.05, "0.01": 0.01},
        value="0.05", label=r"$\alpha$",
    )
    mo.vstack([
        mo.md(r"Null hypothesis $H_0:\ \mu_X = 20$."),
        mo.hstack([pv_est, pv_se, pv_alpha], justify="start", gap=2),
    ])
    return pv_alpha, pv_est, pv_se


@app.cell(hide_code=True)
def _(alt, mo, np, pd, pv_alpha, pv_est, pv_se, stats):
    _MU0 = 20.0
    _est = float(pv_est.value)
    _se = float(pv_se.value)
    _alpha = float(pv_alpha.value)
    _zcrit = float(stats.norm.ppf(1.0 - _alpha / 2.0))

    _x = np.linspace(-4.0, 4.0, 401)
    _frame = pd.DataFrame({"x": _x, "pdf": stats.norm.pdf(_x)})

    _valid = _se > 0.0
    if _valid:
        _t = (_est - _MU0) / _se
        _p = 2.0 * float(stats.norm.cdf(-abs(_t)))
        _reject = _p < _alpha
        _visible = abs(_t) < 4.0
        _edge = min(abs(_t), 4.0)
        _tcolor = "orange" if _reject else "#1f4e79"

    # The curve, drawn as a line only (no full-area fill), so the shaded
    # region equals the p-value and nothing else.
    _line = (
        alt.Chart(_frame)
        .mark_line(color="#1f4e79", size=1.5)
        .encode(
            x=alt.X(
                "x:Q",
                title="t-statistic assuming the null is true (standard normal distribution)",
                scale=alt.Scale(domain=[-4.0, 4.0]),
            ),
            y=alt.Y(
                "pdf:Q", title="Density", scale=alt.Scale(domain=[0.0, 0.42])
            ),
        )
    )
    # Faint dashed cutoffs at the critical values for the chosen alpha.
    _cutoffs = (
        alt.Chart(pd.DataFrame({"x": [_zcrit, -_zcrit]}))
        .mark_rule(color="#9ca3af", strokeDash=[4, 3], size=1.5)
        .encode(x="x:Q")
    )
    # The null value sits at t = 0.
    _nullrule = (
        alt.Chart(pd.DataFrame({"x": [0.0]}))
        .mark_rule(color="#d1d5db", size=1)
        .encode(x="x:Q")
    )

    _layers = []
    if _valid:
        _ltail = pd.DataFrame({"x": np.linspace(-4.0, -_edge, 120)})
        _ltail["pdf"] = stats.norm.pdf(_ltail["x"])
        _rtail = pd.DataFrame({"x": np.linspace(_edge, 4.0, 120)})
        _rtail["pdf"] = stats.norm.pdf(_rtail["x"])
        _shade_l = (
            alt.Chart(_ltail)
            .mark_area(color=_tcolor, opacity=0.5)
            .encode(x="x:Q", y="pdf:Q")
        )
        _shade_r = (
            alt.Chart(_rtail)
            .mark_area(color=_tcolor, opacity=0.5)
            .encode(x="x:Q", y="pdf:Q")
        )
        _estrules = (
            alt.Chart(pd.DataFrame({"x": [_edge, -_edge]}))
            .mark_rule(color=_tcolor, size=2)
            .encode(x="x:Q")
        )
        _layers = [_shade_l, _shade_r, _line, _nullrule, _cutoffs, _estrules]
    else:
        _layers = [_line, _nullrule, _cutoffs]

    _chart = alt.layer(*_layers).properties(
        width=560, height=300, title="The p-value is the shaded tail area"
    )

    # Stateful caption: warning, full computation, or "too small to see".
    if not _valid:
        _color = "#b91c1c"
        _body = (
            "The standard error must be positive. Enter a value greater than "
            "0 to compute the t-statistic."
        )
    else:
        if _p < 0.001:
            _mant, _exp = f"{_p:.1e}".split("e")
            _pstr = rf"{_mant}\times10^{{{int(_exp)}}}"
        else:
            _pstr = f"{_p:.3f}"
        _formula = (
            rf"$t = \dfrac{{\hat{{\mu}}_X^{{\text{{est}}}} - \mu_{{X,0}}}}{{\text{{se}}(\hat{{\mu}}_X)}} "
            rf"= \dfrac{{{_est:g} - {_MU0:g}}}{{{_se:g}}} = {_t:.2f}$"
        )
        _color = "#6b7280"
        if _visible:
            _dec = "rejects" if _reject else "does not reject"
            _cmp = "<" if _reject else r"\geq"
            _body = (
                _formula
                + rf", so $p = 2\Phi(-|{_t:.2f}|) = {_pstr}$. "
                + rf"At $\alpha = {_alpha:g}$, since $p {_cmp} \alpha$, this "
                + rf"test {_dec} the null hypothesis $H_0: \mu_X = 20$."
            )
        else:
            _body = (
                _formula
                + rf", giving $p \approx {_pstr}$. This t-statistic is too "
                + r"far into the tail to show on the plot. Increase the "
                + r"standard error or choose an estimate closer to the null "
                + r"(\$20) to see the shaded area."
            )
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 1rem;max-width:560px;'
        f"font-size:0.85rem;line-height:1.45;color:{_color};text-align:center;\">"
        + _body
        + "</span>"
    )
    mo.vstack([_chart, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec6"></a>
    ## 4.6 Confidence intervals

    A hypothesis test starts with a claim and asks whether the data provide enough evidence to reject it. A *confidence interval* starts with the estimate and asks which values of the population mean remain plausible given uncertainty in it.

    Suppose our estimator is the sample mean, $\hat{\mu}_X$. The estimate from one sample will usually not equal the true mean exactly. A confidence interval builds a range around $\hat{\mu}_X$ that accounts for this sampling uncertainty. For a large sample,

    $$
    \text{CI for } \mu_X = \hat{\mu}_X \pm c \cdot \text{se}(\hat{\mu}_X).
    $$

    The standard error measures how much $\hat{\mu}_X$ varies across repeated samples. A larger standard error makes the interval wider, while a larger sample usually makes it narrower. The *critical value* $c$ determines how many standard errors we add on each side. Common choices for the critical value are $1.64$ for a 90% interval, $1.96$ for a 95% interval, and $2.58$ for a 99% interval.

    A 95% confidence interval does not mean there is a 95% probability that a particular interval contains the true mean. It means that if we repeatedly drew samples and built an interval the same way each time, about 95% of those intervals would contain the true mean.

    The plot below illustrates this repeated-samples idea. It draws one hundred samples from a population with true mean \$20, builds a confidence interval from each sample, and marks the true mean with a dashed line. Intervals that miss the true mean are highlighted.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ci_level = mo.ui.dropdown(
        options=["90%", "95%", "99%"], value="95%", label="Confidence level",
    )
    ci_n = mo.ui.slider(
        start=5, stop=200, step=5, value=30,
        label="Sample size n", show_value=True,
    )
    ci_button = mo.ui.button(
        label="Draw new samples", value=0, on_click=lambda c: c + 1,
    )
    mo.vstack([ci_level, ci_n, ci_button])
    return ci_button, ci_level, ci_n


@app.cell(hide_code=True)
def _(alt, ci_button, ci_level, ci_n, mo, np, pd):
    _K = 100
    _NMAX = 200
    _mu = 20.0
    _sigma = 6.0
    _zmap = {"90%": 1.645, "95%": 1.960, "99%": 2.576}
    _z = _zmap[ci_level.value]
    _n = int(ci_n.value)

    # Hold the x-axis fixed at the n = 5 scale (the widest the intervals ever
    # get) so that raising the sample size visibly shrinks the intervals
    # instead of the axis rescaling to fit them.
    _se5 = _sigma / np.sqrt(5)
    _xhalf = (3.5 + _z) * _se5
    _xdom = [_mu - _xhalf, _mu + _xhalf]

    _rng = np.random.default_rng(7 + ci_button.value)
    _pool = _rng.normal(_mu, _sigma, (_K, _NMAX))
    _means = _pool[:, :_n].mean(axis=1)
    _se = _sigma / np.sqrt(_n)
    _half = _z * _se
    _lo = _means - _half
    _hi = _means + _half
    _contains = (_lo <= _mu) & (_hi >= _mu)
    _frame = pd.DataFrame({
        "idx": np.arange(_K),
        "lo": _lo,
        "hi": _hi,
        "mean": _means,
        "status": np.where(_contains, "contains the true mean", "misses the true mean"),
    })

    _intervals = (
        alt.Chart(_frame)
        .mark_rule(size=1.5, clip=True)
        .encode(
            x=alt.X("lo:Q", title="Hourly earnings (USD)", scale=alt.Scale(domain=_xdom, nice=False)),
            x2="hi:Q",
            y=alt.Y("idx:Q", axis=None, title=None),
            color=alt.Color(
                "status:N",
                scale=alt.Scale(
                    domain=["contains the true mean", "misses the true mean"],
                    range=["#1f4e79", "orange"],
                ),
                legend=alt.Legend(title=None, orient="top"),
            ),
        )
    )
    _truth = (
        alt.Chart(pd.DataFrame({"mu": [_mu]}))
        .mark_rule(color="#6b7280", strokeDash=[4, 3], size=2)
        .encode(x="mu:Q")
    )
    _chart = (_intervals + _truth).properties(
        width=560, height=360, title=f"{_K} sample confidence intervals",
    )

    _k = int(_contains.sum())
    _body = (
        rf"{_k} of {_K} intervals contain the true mean of \$20, which is "
        rf"{100 * _k / _K:.0f}% coverage, close to the {ci_level.value} "
        rf"confidence level. Press Draw new samples to see a fresh set."
    )
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 1rem;max-width:560px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _body
        + "</span>"
    )
    mo.vstack([_chart, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** estimator, estimate, parameter, bias, unbiased, "
            "consistency, mean squared error, efficiency, hypothesis test, "
            "null hypothesis, alternative hypothesis, two-sided alternative, "
            "one-sided alternative, p-value, test statistic, t-statistic, "
            "standard error, significance level, confidence interval, critical "
            "value.\n\n"
            "**Concepts:** an estimator is a random variable, the "
            "bias-variance decomposition, the t-statistic is approximately "
            "standard normal under the null by the central limit theorem, the "
            "interpretation of a confidence interval."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    tbl_t = mo.ui.number(
        start=-5.0, stop=5.0, step=0.01, value=2.01, label="t value",
    )
    return (tbl_t,)


@app.cell(hide_code=True)
def _(mo, stats, tbl_t):
    _t = float(tbl_t.value)
    _phi = float(stats.norm.cdf(-abs(_t)))
    _p = 2.0 * _phi
    _readout = mo.md(
        rf"For $t = {_t:.2f}$, the table gives $\Phi(-|t|) = {_phi:.4f}$, so "
        rf"the two-sided p-value is $p = 2 \times {_phi:.4f} = {_p:.4f}$."
    )

    _text_lookup = mo.md(r"""
        **Looking up a p-value in a standard normal table.**

        Before statistical software was common, p-values were read from a printed table of the standard normal cumulative distribution function $\Phi$. The table gives $\Phi(z)$, the probability that a standard normal random variable falls below $z$. To find a two-sided p-value from a t-statistic, compute $p = 2\,\Phi(-|t^{\text{est}}|)$, which needs the single table value $\Phi(-|t^{\text{est}}|)$.

        For example, take $t^{\text{est}} = 2.01$. Find the row for $-2.0$ and the column for the second decimal $0.01$, which gives $\Phi(-2.01) \approx 0.0222$. The two-sided p-value is $p = 2 \times 0.0222 = 0.0444$. The tool below does this lookup for any t value. You may use it to check your work, but you are expected to read p-values from the table by hand, because you will use the table, not software, during tests and exams.
        """)

    _text_biasvar = mo.md(r"""
        **The bias-variance decomposition.**

        This derivation is bonus material. You will not be tested on it.

        Section 4.3 split the mean squared error into a variance term and a squared bias term. Here is why. Start from the definition and add and subtract the expected value of the estimator inside the square,

        $$ \text{MSE}(\hat{\theta}) = \mathbb{E}\big[(\hat{\theta} - \theta)^2\big] = \mathbb{E}\big[(\hat{\theta} - \mathbb{E}[\hat{\theta}] + \mathbb{E}[\hat{\theta}] - \theta)^2\big]. $$

        Expanding the square gives three terms,

        $$ \mathbb{E}\big[(\hat{\theta} - \mathbb{E}[\hat{\theta}])^2\big] + 2\big(\mathbb{E}[\hat{\theta}] - \theta\big)\,\mathbb{E}\big[\hat{\theta} - \mathbb{E}[\hat{\theta}]\big] + \big(\mathbb{E}[\hat{\theta}] - \theta\big)^2. $$

        The middle term is zero, because $\mathbb{E}\big[\hat{\theta} - \mathbb{E}[\hat{\theta}]\big] = \mathbb{E}[\hat{\theta}] - \mathbb{E}[\hat{\theta}] = 0$. The first term is the variance of $\hat{\theta}$ and the last term is its squared bias, which leaves

        $$ \text{MSE}(\hat{\theta}) = \text{var}(\hat{\theta}) + \text{Bias}(\hat{\theta})^2. $$
        """)

    mo.accordion({
        "## Appendix": mo.vstack([_text_lookup, tbl_t, _readout, _text_biasvar]),
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** Recall from algebra that the vertical bars denote *absolute value*, which measures distance from zero. For example, $|3|=3$ and $|-3|=3$. Here, $\left| \hat{\mu}_X^{\text{est}} - \mu_{X,0} \right|$ is the distance between the estimate and the null value, ignoring whether the estimate is above or below the null. A two-sided test uses absolute values because evidence against the null can come from either direction. <a href="#fnref1" title="Back to text">&#8617;</a></span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec3WorkingWithMultipleRandomVariables.html" target="_self">← Lecture 3</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec5SimpleLinearRegression.html" target="_self">Lecture 5 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
