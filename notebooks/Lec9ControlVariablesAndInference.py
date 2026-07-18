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
                    "#sec1": "1. The least squares assumptions with multiple independent variables",
                    "#sec2": "2. Control variables",
                    "#sec3": "3. Bad controls",
                    "#sec4": "4. The variance of a coefficient with multiple independent variables",
                    "#sec5": "5. Hypothesis testing a single coefficient",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec10ReadingRegressionTables.html" target="_self">Lecture 10 →</a>'),
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

    [1. The least squares assumptions with multiple independent variables](#sec1)<br>
    [2. Control variables](#sec2)<br>
    [3. Bad controls](#sec3)<br>
    [4. The variance of a coefficient with multiple independent variables](#sec4)<br>
    [5. Hypothesis testing a single coefficient](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>

    ## 1. The least squares assumptions with multiple independent variables

    In Lecture 8, we estimated regressions with multiple independent variables. As in the single-variable case, we can interpret the OLS estimates as causal effects only under certain assumptions. We adapt the three assumptions from the single-variable case to the multiple-variable case and add a fourth assumption.

    <a id="sec1a"></a>

    ### <span style="color:#0b68cb">Least Squares Assumption 1: the conditional mean of $u$ given the independent variables is zero</span>

    The first least squares assumption is

    $$
    \mathbb{E}[u \mid X_1, \dots, X_k] = 0,
    $$

    the multiple-variable version of conditional *mean independence*. This means that the average value of the error term must be zero at every combination of the independent variables. Once we hold all the independent variables fixed, the remaining determinants of $Y$ contained in $u$ cannot be systematically higher or lower for particular values of any independent variable.

    Consider our wage regression that includes education and parental income as independent variables. The assumption requires workers with different levels of education but the same parental income to have, on average, the same ability, health, luck, and other determinants of wages contained in $u$. It also requires workers with different levels of parental income but the same education to have, on average, the same remaining determinants of wages. More generally, the variables left in the error term cannot vary systematically with either independent variable after we hold the other fixed.

    Adding relevant independent variables can make this first OLS assumption more plausible than in the single-variable case because we move potential sources of omitted variable bias out of the error term and into the regression. However, the assumption must now hold for every independent variable we include. We can interpret the coefficient on a particular independent variable causally only if the remaining error term does not vary systematically with that variable after we hold the other independent variables fixed.

    <a id="sec1b"></a>

    ### <span style="color:#0b68cb">Least Squares Assumption 2: the data are i.i.d.</span>

    The second least squares assumption requires the observations

    $$
    (Y_i, X_{1i}, \dots, X_{ki}), \qquad i=1,\dots,n,
    $$

    to be *independent and identically distributed*. In practice, this means that we treat the sample as a collection of random draws from the same population. The “identically distributed” part means that we draw each observation in the same way from the same population. The “independent” part means that knowing one observation does not provide information about another.

    The multiple-variable case does not require the independent variables within an observation to be independent of one another. Education and parental income, for example, may be related. Instead, the assumption requires the observations to be independent across individuals. Knowing one worker’s wage, education, and parental income should not provide information about another worker’s wage, education, or parental income.

    <a id="sec1c"></a>

    ### <span style="color:#0b68cb">Least Squares Assumption 3: large outliers are unlikely</span>

    An outlier is an observation whose value of $Y$, one or more of the independent variables, or both lies far from the rest of the data. The third assumption states that large outliers are unlikely. It rules out distributions that produce values so extreme that a handful of observations can dominate the sample and the OLS estimates.

    As in the single-variable case, we should plot the data and inspect extreme values before trusting the regression results. With multiple independent variables, we may need to examine each variable separately.

    <a id="sec1d"></a>

    ### <span style="color:#0b68cb">Least Squares Assumption 4: no perfect multicollinearity</span>

    The fourth assumption rules out *perfect multicollinearity*, which occurs when one independent variable is an exact linear function of the others. A linear function represents one independent variable using fixed multiples of the others and a constant term. For example, perfect multicollinearity exists if

    $$
    X_3 = a + b_1X_1 + b_2X_2
    $$

    for every observation. In this case, knowing $X_1$ and $X_2$ tells us the exact value of $X_3$, so $X_3$ contains no separate information.

    Age and date of birth is a simple example. Once we fix today’s date, knowing a person’s date of birth tells us the person’s age. We therefore cannot ask how age affects an outcome while holding date of birth fixed. OLS cannot estimate separate coefficients on perfectly collinear independent variables, so we must drop one of the redundant variables.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Control variables

    In many multiple-variable regressions, we care about interpreting some coefficients causally but not others. We can therefore divide the independent variables into *variables of interest*, whose causal effects we want to estimate, and *control variables*, whose causal effects we are not interested in.

    Let $X_1, \dots, X_k$ denote the variables of interest and $W_1, \dots, W_r$ the control variables,

    $$
    Y_i = \beta_0 + \beta_1 X_{1i} + \dots + \beta_k X_{ki} + \beta_{k+1} W_{1i} + \dots + \beta_{k+r} W_{ri} + u_i.
    $$

    In this regression model, the coefficients $\beta_1, \dots, \beta_k$ are the causal effects we want to estimate. The control variables allow us to compare observations with the same values of $W_1, \dots, W_r$ but different values of $X_1, \dots, X_k$. We include $W_1, \dots, W_r$ to hold these factors fixed when trying to estimate the causal effects $\beta_1, \dots, \beta_k$.

    In our wage example from Lecture 8, we can treat education as the variable of interest and parental income as a control variable. We include parental income so that we compare workers with different levels of education but similar family backgrounds. We do not want to use the regression to estimate the causal effect of parental income on wages, however.

    Because we seek a causal interpretation only for the variables of interest, we can relax the first least squares assumption from Section 1. Rather than requiring the average value of the error term to equal zero at every combination of the variables of interest and control variables, we instead require

    $$
    \mathbb{E}[u \mid X_1, \dots, X_k, W_1, \dots, W_r] = \mathbb{E}[u \mid W_1, \dots, W_r].
    $$

    This amended assumption is also called conditional mean independence. It says that once we hold the control variables fixed, the average value of the error term cannot vary systematically with the variables of interest. The error may still vary with the controls, making this condition easier to satisfy than the first least squares assumption from Section 1.

    In the wage example, workers from different family backgrounds may differ in ability, health, luck, and other determinants of wages contained in $u$. The assumption allows these factors to differ across levels of parental income. It requires only that workers with different levels of education but the same parental income have, on average, the same remaining determinants of wages.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Bad controls

    Adding a control variable does not always make the estimated coefficient on the variable of interest a better estimate of its causal effect. A *bad control* is an independent variable that lies on the causal path from the variable of interest to the outcome. The variable of interest affects this control, which then affects the outcome. Because the control mediates part of the causal effect, holding it fixed blocks part of the causal effect we want to estimate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <div style="max-width:560px;margin:1.25rem auto;">
    <svg viewBox="0 0 560 240" width="100%" font-family="system-ui, sans-serif" role="img" aria-label="Schooling raises wages directly and through occupation, which is a bad control">
      <defs>
        <marker id="bcarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" fill="#64748b"></path>
        </marker>
      </defs>
      <rect x="210" y="20" width="140" height="52" rx="9" fill="#fbe9e7" stroke="#c0392b" stroke-width="2"></rect>
      <text x="280" y="50" text-anchor="middle" font-size="15" font-weight="600" fill="#c0392b">Occupation</text>
      <text x="280" y="92" text-anchor="middle" font-size="12.5" font-style="italic" fill="#c0392b">bad control</text>
      <rect x="20" y="150" width="140" height="52" rx="9" fill="#e8f0f9" stroke="#1f4e79" stroke-width="2"></rect>
      <text x="90" y="182" text-anchor="middle" font-size="15" font-weight="600" fill="#1f4e79">Schooling</text>
      <rect x="400" y="150" width="140" height="52" rx="9" fill="#e8f0f9" stroke="#1f4e79" stroke-width="2"></rect>
      <text x="470" y="182" text-anchor="middle" font-size="15" font-weight="600" fill="#1f4e79">Wage</text>
      <line x1="150" y1="150" x2="214" y2="70" stroke="#64748b" stroke-width="2" marker-end="url(#bcarrow)"></line>
      <line x1="346" y1="70" x2="410" y2="150" stroke="#64748b" stroke-width="2" marker-end="url(#bcarrow)"></line>
      <line x1="160" y1="176" x2="398" y2="176" stroke="#64748b" stroke-width="2" marker-end="url(#bcarrow)"></line>
      <text x="280" y="196" text-anchor="middle" font-size="12.5" fill="#64748b">direct effect</text>
    </svg>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The diagram illustrates the return to schooling, where $Y$ is a worker's wage and $X$ is years of schooling. More schooling can move workers into higher-paying occupations, which in turn raise their wages. Occupation therefore lies on the causal path from schooling to wages. Controlling for occupation holds it fixed and excludes this pathway from the estimated effect, so the coefficient on schooling captures only the part of schooling's effect that does not operate through occupation. The resulting coefficient on schooling therefore understates the total effect of schooling on wages.

    Hours worked, a score on a test taken after schooling is measured, and where a person settles as an adult may be bad controls for the same reason. Schooling may affect each of these variables, which may then affect wages.

    A good control instead captures a factor determined before the variable of interest is measured. Family background affects how much schooling a person receives but is not impacted by schooling itself. Holding family background fixed can therefore remove a source of bias without blocking part of schooling's effect. As a general rule, we should control for relevant factors determined before the variable of interest is measured and avoid controlling for variables it may affect.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. The variance of a coefficient with several independent variables

    In Lecture 7, we showed that the variance of an OLS coefficient estimate in a single-variable regression depends on the sample size, the variation in the independent variable, and the variation in the error term. These same factors matter in a multiple-variable regression, but the variance of a coefficient estimate now also depends on how closely the independent variables are related to one another.

    Across repeated random samples, each OLS coefficient has its own sampling distribution. Under the assumptions from Section 1, every $\hat{\beta}_j$ is approximately normally distributed in large samples and centered on the population coefficient $\beta_j$,

    $$
    \hat{\beta}j \sim \mathcal{N}\left(\beta_j,\ \sigma^2_{\hat{\beta}_j}\right).
    $$

    The t-tests and confidence intervals from Lecture 7 therefore carry over to each coefficient. A smaller variance produces a smaller standard error and a more precise estimate.

    The general formula for the variance of a coefficient in a multiple-variable regression $\sigma^2_{\hat{\beta}_j}$ is complicated. An illuminating special case is a regression with two independent variables, $X_1$ and $X_2$, and homoskedastic errors. In this case,

    $$
    \sigma^2_{\hat{\beta}_1} = \frac{1}{n}\cdot\frac{1}{1 - \rho^2_{X_1 X_2}}\cdot\frac{\sigma_u^2}{\sigma_{X_1}^2},
    $$

    where $\rho_{X_1X_2}$ is the correlation between $X_1$ and $X_2$. As in the single-variable case, a larger sample and greater variation in $X_1$ reduce the variance, while greater variation in the error term increases it. The middle factor is new, however. It captures the *variance inflation* caused by how much the independent variables move together.

    When $X_1$ and $X_2$ are uncorrelated, $\rho_{X_1X_2}=0$ and the variance-inflation factor equals one. As their correlation approaches either one or negative one, $\rho^2_{X_1X_2}$ approaches one and the variance increases. To understand why, remember that OLS estimates the effect of $X_1$ while holding $X_2$ fixed. When the two variables move closely together, the sample will therefore contain little variation in $X_1$ among observations with similar values of $X_2$, making it difficult to distinguish their separate effects. This situation is called *imperfect multicollinearity*. It increases the variance of the coefficient estimates but does not prevent OLS from estimating them.<sup><a id="fnref1" href="#fn1">1</a></sup>

    The plot below shows the correlation between two independent variables alongside the sampling distribution of $\hat{\beta}_1$. As the correlation increases in magnitude, the sampling distribution becomes more dispersed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mc_rho = mo.ui.slider(
        start=0.0, stop=0.95, step=0.05, value=0.0,
        label="Correlation between the two independent variables", show_value=True, full_width=False,
    )
    mo.vstack(
        [
            mo.md("Set how strongly the two independent variables move together and see the effect on the spread of the slope estimate."),
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
        .properties(width=290, height=290, title="The two independent variables")
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
            f"The independent variables are uncorrelated, so the variance-inflation factor "
            f"$1/(1-\\rho^2)$ is 1.00 and there is no inflation. The standard error of "
            f"$\\hat{{\\beta}}_1$ is at its smallest, {_se:.3f}, and the orange line marks the "
            f"true slope of 1.2. Raise the correlation to watch the estimates spread out."
        )
    else:
        _body = (
            f"At a correlation of {_rho:.2f}, the variance-inflation factor is "
            f"$1/(1-\\rho^2) = {_vif:.2f}$, so the standard error of $\\hat{{\\beta}}_1$ is {_se:.3f}, "
            f"up from {_se0:.3f} when the independent variables are uncorrelated (the grey dashed bell). The "
            f"orange line marks the true slope of 1.2. As the independent variables line up, the estimates "
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

    which is distributed as a standard normal when the null hypothesis is true in large samples. The two-sided p-value is $2\Phi(-|t|)$, and we reject when it falls below our chosen significance level, often 0.05. The most common null hypothesis is that the coefficient is zero, meaning the independent variable being tested has no effect once the others are held fixed.

    Take the education coefficient from Lecture 8, which was $1.22$ when we controlled for parental income. Suppose its standard error is $0.48$. The t-statistic for the null hypothesis of no effect is $t = 1.22 / 0.48 = 2.54$, and the p-value is $2\Phi(-2.54) \approx 0.01$, so we reject the null hypothesis at the 5% level and conclude that education matters for wages once parental income is held fixed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ell_rho = mo.ui.slider(
        start=-0.9, stop=0.9, step=0.1, value=-0.8,
        label="Correlation between the two coefficient estimates", show_value=True, full_width=False,
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
            "several independent variables including no perfect multicollinearity, a control variable "
            "holds confounders fixed and need only satisfy conditional mean independence, a "
            "bad control is a mediator that blocks part of the causal effect, how correlation "
            "between independent variables inflates a coefficient's variance, and testing one coefficient "
            "with a t-test."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(alt, ell_rho, mo, np, pd, stats):
    _ftest_md = mo.md(r"""
    This appendix explains how to test hypotheses involving several coefficients at once. You will not be tested on this material.

    **Testing several coefficients at once**

    Sometimes we want to test a hypothesis involving several coefficients, such as whether two independent variables both have no effect,

    $$
    H_0:\beta_1=0 \quad \text{and} \quad \beta_2=0.
    $$

    Separate t-tests do not test this joint hypothesis. Each tests one restriction at a time, whereas a joint test must determine whether the restrictions hold simultaneously and account for the correlation between the coefficient estimates.

    We use an *F-statistic* to test a joint hypothesis. For the null hypothesis above,
    $$
    F = \frac{1}{2}\left(\frac{t_1^2 + t_2^2 - 2\hat{\rho}_{t_1 t_2}\, t_1 t_2}{1 - \hat{\rho}^2_{t_1 t_2}}\right),
    $$

    where $t_1$ and $t_2$ are the individual t-statistics and $\hat{\rho}_{t_1t_2}$ is the estimated correlation between them. The statistic combines the evidence against both restrictions while accounting for the relationship between the two estimates.

    In large samples, the F-statistic follows an $F_{q,\infty}$ distribution under the null hypothesis, where $q$ is the number of restrictions (we introduced the $F$ distribution in the Appendix of Lecture 2). Here, $q=2$. We reject the null hypothesis when the F-statistic exceeds the relevant critical value, which is approximately $3.00$ at the 5 percent level for two restrictions.

    With a single restriction, the F-statistic equals the square of the corresponding t-statistic, $F = t^2$, so the F-test and t-test produce the same conclusion. The same principle gives us the overall regression F-statistic, which tests the joint null hypothesis that all slope coefficients equal zero.

    The plot below illustrates why a joint test can produce a different conclusion from separate t-tests. Both coefficient estimates equal 1.5 and have standard errors of 1.0, so both t-statistics equal 1.5. Change the correlation between the estimates and compare the resulting joint confidence region with the two individual confidence intervals. The joint confidence region contains the combinations of values for $\beta_1$ and $\beta_2$ for which the corresponding joint null hypothesis is not rejected at the chosen significance level.
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

    mo.accordion(
        {"## Appendix": mo.vstack([_ftest_md, ell_rho, _chart, _caption])}
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** Perfect multicollinearity occurs when $\rho^2_{X_1 X_2}=1$. The denominator then equals zero, and OLS cannot estimate separate coefficients on the two independent variables. This is why the fourth least squares assumption rules it out. <a href="#fnref1" title="Back to text">&#8617;</a></span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec8MultipleRegression.html" target="_self">← Lecture 8</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec10ReadingRegressionTables.html" target="_self">Lecture 10 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
