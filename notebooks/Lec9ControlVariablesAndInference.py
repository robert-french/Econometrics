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
    app_title="Lecture 9: Control Variables and Inference",
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
            mo.md("# [Lecture 9](#top)"),
            mo.md("Control Variables and Inference"),
            mo.nav_menu(
                {
                    "#sec1": "1. The least squares assumptions with several regressors",
                    "#sec2": "2. Control variables",
                    "#sec3": "3. Bad controls",
                    "#sec4": "4. The variance of a coefficient with several regressors",
                    "#sec5": "5. Testing a single coefficient",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec8MultipleRegression.html" target="_self">← Lecture 8</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec10NonlinearRegressionPolynomials.html" target="_self">Lecture 10 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 9: Control Variables and Inference
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

    [1. The least squares assumptions with several regressors](#sec1)<br>
    [2. Control variables](#sec2)<br>
    [3. Bad controls](#sec3)<br>
    [4. The variance of a coefficient with several regressors](#sec4)<br>
    [5. Testing a single coefficient](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. The least squares assumptions with several regressors

    Lecture 8 estimated regressions with several regressors but left a question open. Under what conditions can the estimated slopes be read as causal effects? The conditions carry over from Lecture 6, with one addition, so there are four. The first three are the single-regressor assumptions restated for several regressors, and the fourth is new.

    <a id="sec1a"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 1: the conditional mean of $u$ given the regressors is zero</span>

    The error must satisfy $\mathbb{E}[u \mid X_1, \dots, X_k] = 0$, the several-regressor version of *mean independence*. This is the assumption Lecture 8 worked to rescue. Each variable moved from the error into the regression is one fewer source of omitted variable bias, and Lecture 8's omitted variable bias formula describes what happens to the slope when a relevant variable stays behind.

    <a id="sec1b"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 2: the data are i.i.d.</span>

    The observations $(Y_i, X_{1i}, \dots, X_{ki})$ must be *independent and identically distributed* across $i$, which holds when the sample is drawn at random, as discussed in Lecture 6.

    <a id="sec1c"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 3: large outliers are unlikely</span>

    No single observation should be able to dominate the estimates. As in Lecture 6, the practical advice is to plot the data and check extreme values before trusting a regression.

    <a id="sec1d"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 4: no perfect multicollinearity</span>

    The new assumption rules out *perfect multicollinearity*, which arises when one regressor is an exact linear function of the others. Age and date of birth are an example. A person's age is fixed once the date of birth and today's date are set, so the two carry the same information. Asking for the effect of age while holding date of birth fixed has no meaning, because age cannot change with date of birth held constant. When two regressors are perfectly collinear, OLS cannot separate their coefficients and the estimates do not exist. The fix is to drop one of the redundant regressors.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Control variables

    Lecture 8 added regressors to clear the error of factors that would otherwise bias the slope. Often only one of those regressors is the effect we care about. We split the model into *variables of interest* $X_1, \dots, X_k$, whose causal effects we want, and *control variables* $W_1, \dots, W_r$, which we include only to hold other factors fixed,

    $$
    Y_i = \beta_0 + \beta_1 X_{1i} + \dots + \beta_k X_{ki} + \beta_{k+1} W_{1i} + \dots + \beta_{k+r} W_{ri} + u_i.
    $$

    A *control variable* is a regressor we add not for its own coefficient but to absorb something that would otherwise sit in the error and bias a variable of interest. In the wage example from Lecture 8, education is the variable of interest and parental income is a control. We have no causal question about income. It is there so that education is compared across workers with similar family backgrounds.

    Because we do not read the controls causally, they face a weaker requirement than the variables of interest. The first least squares assumption from Section 1 becomes *conditional mean independence*,

    $$
    \mathbb{E}[u \mid X_1, \dots, X_k, W_1, \dots, W_r] = \mathbb{E}[u \mid W_1, \dots, W_r].
    $$

    Once the controls are held fixed, the error has nothing more to do with the variables of interest, though it may still move with the controls. So a control can be correlated with the error and need not have a causal meaning of its own. It only has to soak up the part of the error that would otherwise be linked to $X$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Bad controls

    Adding a control does not always help. A *bad control* is a regressor that sits on the causal path from the variable of interest to the outcome, a variable that the variable of interest affects and that in turn affects the outcome. Such a variable is called a *mediator*, because the effect passes through it. Holding a mediator fixed blocks part of the very effect we are trying to measure.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    <div style="max-width:560px;margin:1.25rem auto;">
    <svg viewBox="0 0 560 240" width="100%" font-family="system-ui, sans-serif" role="img" aria-label="Schooling raises wages directly and through occupation, which is a bad control">
      <defs>
        <marker id="bcarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" fill="#64748b"></path>
        </marker>
      </defs>
      <rect x="210" y="20" width="140" height="52" rx="9" fill="#fbe9e7" stroke="#c0392b" stroke-width="2"></rect>
      <text x="280" y="50" text-anchor="middle" font-size="15" font-weight="600" fill="#c0392b">Occupation</text>
      <text x="280" y="92" text-anchor="middle" font-size="12.5" font-style="italic" fill="#c0392b">bad control (mediator)</text>
      <rect x="20" y="150" width="140" height="52" rx="9" fill="#e8f0f9" stroke="#1f4e79" stroke-width="2"></rect>
      <text x="90" y="182" text-anchor="middle" font-size="15" font-weight="600" fill="#1f4e79">Schooling</text>
      <rect x="400" y="150" width="140" height="52" rx="9" fill="#e8f0f9" stroke="#1f4e79" stroke-width="2"></rect>
      <text x="470" y="182" text-anchor="middle" font-size="15" font-weight="600" fill="#1f4e79">Wage</text>
      <line x1="150" y1="150" x2="214" y2="70" stroke="#64748b" stroke-width="2" marker-end="url(#bcarrow)"></line>
      <line x1="346" y1="70" x2="410" y2="150" stroke="#64748b" stroke-width="2" marker-end="url(#bcarrow)"></line>
      <text x="280" y="128" text-anchor="middle" font-size="12.5" fill="#64748b">mediated effect</text>
      <line x1="160" y1="176" x2="398" y2="176" stroke="#64748b" stroke-width="2" marker-end="url(#bcarrow)"></line>
      <text x="280" y="196" text-anchor="middle" font-size="12.5" fill="#64748b">direct effect</text>
    </svg>
    </div>
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The diagram traces the return to schooling, with $Y$ a worker's wage and $X$ years of schooling. Occupation is the mediator. More schooling moves people into higher-paying occupations, and those occupations pay more, so part of schooling's effect on wages runs through occupation. Holding occupation fixed strips out that channel and leaves only the direct effect, the part of the return that does not run through the job a person holds, which understates schooling's total effect. Hours worked, a test taken after leaving school, and where a person settles as an adult are bad controls for the same reason, because schooling shapes each of them.

    A good control does the opposite. It comes before the variable of interest rather than after it. Family background shapes how much schooling a person gets and does not result from that schooling, so holding it fixed removes a source of bias without blocking any of schooling's effect. The rule is to control for what comes before the variable of interest and to leave out what comes after.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. The variance of a coefficient with several regressors

    Each OLS coefficient is a random variable with its own sampling distribution. Under the assumptions from Section 1, every $\hat{\beta}_j$ is approximately normal in large samples, centered on $\beta_j$,

    $$
    \hat{\beta}_j \sim \mathcal{N}\left(\beta_j,\ \sigma^2_{\hat{\beta}_j}\right),
    $$

    so the t-tests and confidence intervals from Lecture 7 carry over to each coefficient. What is new is how the other regressors affect the variance. With two regressors $X_1$ and $X_2$ and homoskedastic errors,

    $$
    \sigma^2_{\hat{\beta}_1} = \frac{1}{n}\cdot\frac{1}{1 - \rho^2_{X_1 X_2}}\cdot\frac{\sigma_u^2}{\sigma_{X_1}^2},
    $$

    where $\rho_{X_1 X_2}$ is the correlation between the two regressors. The first and last factors are familiar from Lecture 7, since a larger sample and more spread in $X_1$ both shrink the variance. The middle factor is new. It is the *variance inflation* from *multicollinearity*, the degree to which the regressors move together.

    When the regressors are uncorrelated, $\rho_{X_1 X_2} = 0$ and the middle factor is one. As they line up, $\rho^2_{X_1 X_2}$ approaches one and the factor grows without bound, so the variance explodes. The reason is that when $X_1$ and $X_2$ move together, the data hold little information about the effect of one while the other is held fixed, because the two are rarely seen apart. This is *imperfect multicollinearity*. The perfect multicollinearity ruled out in Section 1 is the limit $\rho^2_{X_1 X_2} = 1$, where the variance is infinite and the coefficients cannot be estimated at all.

    The plot below shows the correlation between two regressors next to the sampling distribution of $\hat{\beta}_1$. Raise the correlation and watch the estimates spread out.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mc_rho = mo.ui.slider(
        start=0.0, stop=0.95, step=0.05, value=0.0,
        label="Correlation between the two regressors", show_value=True, full_width=True,
    )
    mo.vstack(
        [
            mo.md("Set how strongly the two regressors move together and see the effect on the spread of the slope estimate."),
            mc_rho,
        ]
    )
    return (mc_rho,)


@app.cell(hide_code=True)
def _(alt, mc_rho, mo, np, pd, stats):
    _rho = float(mc_rho.value)

    _rng = np.random.default_rng(7)
    _m = 160
    _x1 = _rng.standard_normal(_m)
    _z = _rng.standard_normal(_m)
    _x2 = _rho * _x1 + np.sqrt(1.0 - _rho ** 2) * _z
    _pts = pd.DataFrame({"x1": _x1, "x2": _x2})
    _scatter = (
        alt.Chart(_pts)
        .mark_circle(size=35, opacity=0.5, color="#1f4e79", clip=True)
        .encode(
            x=alt.X("x1:Q", title="X1", scale=alt.Scale(domain=[-3.2, 3.2], nice=False)),
            y=alt.Y("x2:Q", title="X2", scale=alt.Scale(domain=[-3.2, 3.2], nice=False)),
        )
        .properties(width=290, height=290, title="The two regressors")
    )

    _n = 150
    _sigu = 2.0
    _sigx1 = 1.0
    _b1 = 1.2
    _vif = 1.0 / (1.0 - _rho ** 2)
    _se = float(np.sqrt((1.0 / _n) * _vif * (_sigu ** 2) / (_sigx1 ** 2)))
    _se0 = float(np.sqrt((1.0 / _n) * (_sigu ** 2) / (_sigx1 ** 2)))

    _grid = np.linspace(_b1 - 2.2, _b1 + 2.2, 240)
    _dens = stats.norm.pdf(_grid, _b1, _se)
    _dens0 = stats.norm.pdf(_grid, _b1, _se0)
    _ymax = float(_dens0.max()) * 1.1

    _xsc = alt.Scale(domain=[_b1 - 2.2, _b1 + 2.2], nice=False)
    _ysc = alt.Scale(domain=[0.0, _ymax], nice=False)
    _area = (
        alt.Chart(pd.DataFrame({"b": _grid, "d": _dens}))
        .mark_area(color="#1f4e79", opacity=0.3, line={"color": "#1f4e79"})
        .encode(
            x=alt.X("b:Q", scale=_xsc, title="Estimates of the slope on X1"),
            y=alt.Y("d:Q", scale=_ysc, title="Density"),
        )
    )
    _base = (
        alt.Chart(pd.DataFrame({"b": _grid, "d": _dens0}))
        .mark_line(color="#9aa5b1", strokeDash=[4, 3], size=1.5)
        .encode(x=alt.X("b:Q", scale=_xsc), y=alt.Y("d:Q", scale=_ysc))
    )
    _truth = (
        alt.Chart(pd.DataFrame({"v": [_b1]}))
        .mark_rule(color="orange", size=2)
        .encode(x=alt.X("v:Q", scale=_xsc))
    )
    _density = (_area + _base + _truth).properties(
        width=290, height=290, title="Sampling distribution of the slope on X1"
    )

    if _rho == 0.0:
        _body = (
            f"The regressors are uncorrelated, so the variance-inflation factor "
            f"$1/(1-\\rho^2)$ is 1.00 and there is no inflation. The standard error of "
            f"$\\hat{{\\beta}}_1$ is at its smallest, {_se:.3f}, and the orange line marks the "
            f"true slope of 1.2. Raise the correlation to watch the estimates spread out."
        )
    else:
        _body = (
            f"At a correlation of {_rho:.2f}, the variance-inflation factor is "
            f"$1/(1-\\rho^2) = {_vif:.2f}$, so the standard error of $\\hat{{\\beta}}_1$ is {_se:.3f}, "
            f"up from {_se0:.3f} when the regressors are uncorrelated (the grey dashed bell). The "
            f"orange line marks the true slope of 1.2. As the regressors line up, the estimates "
            f"spread out and the slope is pinned down less precisely."
        )
    _caption = mo.md(
        '<span style="display:block;margin:0.4rem auto 1rem;max-width:600px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _body + "</span>"
    )
    mo.vstack(
        [mo.hstack([_scatter, _density], justify="center", align="center"), _caption]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Testing a single coefficient

    Because each $\hat{\beta}_j$ is approximately normal, testing one coefficient works exactly as in Lecture 7. To test the null hypothesis that $\beta_j$ equals some value $\beta_{j, H_0}$, we form the *t-statistic*

    $$
    t = \frac{\hat{\beta}_j - \beta_{j, H_0}}{\hat{\sigma}_{\hat{\beta}_j}},
    $$

    which is standard normal under the null in large samples. The two-sided p-value is $2\Phi(-|t|)$, and we reject when it falls below the significance level. The most common null is that the coefficient is zero, meaning the regressor has no effect once the others are held fixed.

    Take the education coefficient from Lecture 8, which was $1.22$ with parental income controlled. Suppose its standard error is $0.48$. The t-statistic for the null of no effect is $t = 1.22 / 0.48 = 2.54$, and the p-value is $2\Phi(-2.54) \approx 0.01$. The estimate is about two and a half standard errors above zero, so we reject the null at the 5% level and conclude that education matters for wages once parental income is held fixed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ell_rho = mo.ui.slider(
        start=-0.9, stop=0.9, step=0.1, value=-0.8,
        label="Correlation between the two coefficient estimates", show_value=True, full_width=True,
    )
    return (ell_rho,)


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** mean independence, perfect multicollinearity, control "
            "variable, variable of interest, conditional mean independence, bad control, "
            "mediator, multicollinearity, variance inflation, imperfect multicollinearity, "
            "t-statistic.\n\n"
            "**Key concepts covered:** the four least squares assumptions for regression with "
            "several regressors including no perfect multicollinearity, a control variable "
            "holds confounders fixed and need only satisfy conditional mean independence, a "
            "bad control is a mediator that blocks part of the causal effect, how correlation "
            "between regressors inflates a coefficient's variance, and testing one coefficient "
            "with a t-test."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(alt, ell_rho, mo, np, pd, stats):
    _ftest_md = mo.md(r"""
    This appendix covers testing several coefficients at once and the origin of the variance-inflation factor from Section 4. You will not be tested on either.

    **Testing several coefficients at once**

    Sometimes we want to test a claim about several coefficients together, such as whether two regressors both have zero effect. Running a separate t-test on each is not the same test, because each t-test ignores the other coefficient and the correlation between the two estimates. A *joint hypothesis* needs a single statistic that accounts for both at once.

    That statistic is the *F-statistic*. For the null that two coefficients are both zero, it is

    $$
    F = \frac{1}{2}\left(\frac{t_1^2 + t_2^2 - 2\hat{\rho}_{t_1 t_2}\, t_1 t_2}{1 - \hat{\rho}^2_{t_1 t_2}}\right),
    $$

    where $t_1$ and $t_2$ are the individual t-statistics and $\hat{\rho}_{t_1 t_2}$ is the correlation between the two coefficient estimates. Under the null the F-statistic follows an $F_{q, \infty}$ distribution, where $q$ is the number of restrictions being tested, here two. We reject when $F$ is larger than the critical value, about $3.00$ for two restrictions at the 5% level. For a single restriction the F-statistic is just the square of the t-statistic, $F = t^2$, so the two tests agree. The same idea extends to the *overall regression F-statistic*, which tests that all the slope coefficients are zero at once.

    The plot below shows why the joint test can differ from two separate ones. Both estimates are 1.5 with a standard error of 1.0, so each t-statistic is 1.5. Change how the estimates are correlated and compare the joint confidence region with the two single-coefficient intervals.
    """)

    _r = float(ell_rho.value)
    _b1 = _b2 = 1.5
    _se1 = _se2 = 1.0
    _t1 = _b1 / _se1
    _t2 = _b2 / _se2
    _chi = float(stats.chi2.ppf(0.95, 2))
    _fcrit = float(stats.f.ppf(0.95, 2, 1_000_000))
    _F = 0.5 * (_t1 ** 2 + _t2 ** 2 - 2.0 * _r * _t1 * _t2) / (1.0 - _r ** 2)

    _Sig = np.array([[_se1 ** 2, _r * _se1 * _se2], [_r * _se1 * _se2, _se2 ** 2]])
    _L = np.linalg.cholesky(_Sig)
    _th = np.linspace(0.0, 2.0 * np.pi, 220)
    _circ = np.vstack([np.cos(_th), np.sin(_th)]) * np.sqrt(_chi)
    _ell = np.array([_b1, _b2])[:, None] + _L @ _circ
    _elldf = pd.DataFrame({"b1": _ell[0], "b2": _ell[1], "i": np.arange(_th.size)})

    _lo1, _hi1 = _b1 - 1.96 * _se1, _b1 + 1.96 * _se1
    _lo2, _hi2 = _b2 - 1.96 * _se2, _b2 + 1.96 * _se2
    _rectdf = pd.DataFrame(
        {
            "b1": [_lo1, _hi1, _hi1, _lo1, _lo1],
            "b2": [_lo2, _lo2, _hi2, _hi2, _lo2],
            "i": [0, 1, 2, 3, 4],
        }
    )

    _dom = [-1.6, 4.1]
    _xsc = alt.Scale(domain=_dom, nice=False)
    _ysc = alt.Scale(domain=_dom, nice=False)
    _ellipse = (
        alt.Chart(_elldf)
        .mark_line(color="#1f4e79", size=2.5)
        .encode(
            x=alt.X("b1:Q", scale=_xsc, title="Coefficient on X1"),
            y=alt.Y("b2:Q", scale=_ysc, title="Coefficient on X2"),
            order="i:Q",
        )
    )
    _rect = (
        alt.Chart(_rectdf)
        .mark_line(color="#9aa5b1", strokeDash=[5, 4], size=1.5)
        .encode(x=alt.X("b1:Q", scale=_xsc), y=alt.Y("b2:Q", scale=_ysc), order="i:Q")
    )
    _est = (
        alt.Chart(pd.DataFrame({"b1": [_b1], "b2": [_b2]}))
        .mark_point(color="#1f4e79", size=80, filled=True)
        .encode(x="b1:Q", y="b2:Q")
    )
    _origin = (
        alt.Chart(pd.DataFrame({"b1": [0.0], "b2": [0.0]}))
        .mark_point(color="orange", size=120, shape="cross", filled=True, strokeWidth=3)
        .encode(x="b1:Q", y="b2:Q")
    )
    _chart = (_rect + _ellipse + _est + _origin).properties(
        width=360, height=360,
        title="Joint 95% region (navy) vs the two t-intervals (grey box)",
    )

    _rejects = _F > _fcrit
    _verdict = (
        "the origin falls outside the navy ellipse, so the joint F-test rejects the null that both coefficients are zero, even though neither t-test does"
        if _rejects
        else "the origin sits inside both the ellipse and the box, so the joint test and the two t-tests agree"
    )
    _body = (
        f"Each t-statistic is 1.5, below 1.96, so neither single test rejects zero, which is "
        f"why the orange cross at the origin sits inside the grey box of the two t-intervals. "
        f"With the estimates correlated at {_r:.1f}, the joint F-statistic is {_F:.2f} against a "
        f"critical value of about {_fcrit:.2f}. Here {_verdict}."
    )
    _caption = mo.md(
        '<span style="display:block;margin:0.4rem auto 1rem;max-width:520px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _body + "</span>"
    )

    _vif_md = mo.md(r"""
    ---

    **The variance of $\hat{\beta}_1$ with two regressors**

    Regress $X_1$ on $X_2$ and write the residual as $\tilde{X}_1 = X_1 - \hat{\gamma}_0 - \hat{\gamma}_1 X_2$, the part of $X_1$ that the other regressor does not explain. The OLS coefficient on $X_1$ in the two-regressor model equals the slope from regressing $Y$ on this residual alone, so

    $$
    \operatorname{var}(\hat{\beta}_1) = \frac{\sigma_u^2}{\sum_{i=1}^{n}\tilde{X}_{1i}^2}.
    $$

    The denominator is the leftover variation in $X_1$ after removing what $X_2$ explains. The regression of $X_1$ on $X_2$ has an $R^2$ equal to $\rho^2_{X_1 X_2}$, so the leftover variation is the fraction $1 - \rho^2_{X_1 X_2}$ of the total, $\sum_{i=1}^{n}\tilde{X}_{1i}^2 = (1 - \rho^2_{X_1 X_2})\sum_{i=1}^{n}(X_{1i} - \hat{\mu}_{X_1})^2$. Substituting gives

    $$
    \operatorname{var}(\hat{\beta}_1) = \frac{1}{1 - \rho^2_{X_1 X_2}}\cdot\frac{\sigma_u^2}{\sum_{i=1}^{n}(X_{1i} - \hat{\mu}_{X_1})^2},
    $$

    which is the formula in Section 4. The factor $1/(1 - \rho^2_{X_1 X_2})$ is the price of the two regressors sharing information.
    """)
    mo.accordion(
        {"## Appendix": mo.vstack([_ftest_md, ell_rho, _chart, _caption, _vif_md])}
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec8MultipleRegression.html" target="_self">← Lecture 8</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec10NonlinearRegressionPolynomials.html" target="_self">Lecture 10 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
