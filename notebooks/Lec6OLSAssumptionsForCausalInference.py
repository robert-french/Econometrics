# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "numpy",
#     "pandas",
#     "altair",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(
    app_title="Lecture 6: OLS Assumptions for Causal Inference",
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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Lecture 6</a></h1>'
                '</div>'
            ),
            mo.md("**OLS Assumptions for Causal Inference**"),
            mo.nav_menu(
                {
                    "#sec1": "1. Conditional expectation",
                    "#sec2": "2. The error term revisited",
                    "#sec3": "3. From prediction to causation",
                    "#sec4": "4. The least squares assumptions",
                    "#sec5": "5. Unbiasedness and consistency",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec5SimpleLinearRegression.html" target="_self">← Lecture 5</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec7InferenceAndOmittedVariableBias.html" target="_self">Lecture 7 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 6: OLS Assumptions for Causal Inference
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Same-page (#fragment) links must stay plain markdown links with no inline
    # style and no styled wrapper. marimo re-renders fragment links as React
    # navigation components, and any inline style string on the link (or on a
    # span/div around it) is passed to React as the `style` prop, which must be
    # an object, not a string -> "Minified React error #62". Full-URL links
    # (the sidebar and prev/next nav) stay raw HTML, which is why they tolerate
    # inline styles. The links are already the course blue (marimo's default
    # --link is #0b68cb); subsections are indented with em-space entities, and
    # the matching body headings get their blue from the inline span the Lec2
    # and Lec4 subsection headings also use.
    mo.md(r"""
    ## Contents

    [1. Conditional expectation](#sec1)<br>
    [2. The error term revisited](#sec2)<br>
    [3. From prediction to causation](#sec3)<br>
    [4. The least squares assumptions](#sec4)<br>
    &emsp;&emsp;[Least Squares Assumption 1: the conditional mean of u given X is zero](#sec4a)<br>
    &emsp;&emsp;[Least Squares Assumption 2: the data are i.i.d.](#sec4b)<br>
    &emsp;&emsp;[Least Squares Assumption 3: large outliers are unlikely](#sec4c)<br>
    [5. Unbiasedness and consistency](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Conditional expectation

    Lecture 5 fit a line through sample data on wages and years of education, and interpreted the slope as describing an association. But what is the line trying to summarize? At each level of education, it estimates the average wage among people with that level of education. Before asking when the slope of that line has a causal interpretation, we therefore need to define the population average that regression is trying to approximate.

    The *conditional expectation* of $Y$ given $X$ is the average value of $Y$ among observations with a given value of $X$ which we denote with a lower-case $x$. We write it as

    $$
    \mathbb{E}[Y \mid X = x].
    $$

    Like the expected value $\mathbb{E}[Y]$ from Lecture 2, the conditional expectation is a population object, not a sample statistic. The difference is that $\mathbb{E}[Y]$ averages over the whole population, while $\mathbb{E}[Y \mid X = x]$ averages only over the subpopulation with $X = x$.

    For discrete random variables, the joint probability tables from Lecture 3 contain everything needed to compute a conditional expectation. Suppose $X$ is a student's class standing, Freshman or Senior, and $Y$ is the student's GPA, rounded to 2.0, 3.0, or 4.0. The table below lists the probability of each combination.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Rendered through mo.center (not inside mo.md) so the table keeps its
    # natural size and is centered, matching the joint tables in Lecture 3.
    _joint = """
    <table style="border-collapse:collapse;text-align:center;">
    <tr style="background:var(--lime-2,#f8faf3);"><th style="padding:6px 18px;border-bottom:1px solid #cbd2d9;" colspan="3">Joint Probability of Class Standing and GPA</th></tr>
    <tr style="background:var(--card,#fff);"><td style="padding:6px 18px;"></td><td style="padding:6px 18px;">Freshman</td><td style="padding:6px 18px;">Senior</td></tr>
    <tr style="background:var(--lime-2,#f8faf3);"><td style="padding:6px 18px;">GPA 2.0</td><td style="padding:6px 18px;">0.15</td><td style="padding:6px 18px;">0.05</td></tr>
    <tr style="background:var(--card,#fff);"><td style="padding:6px 18px;">GPA 3.0</td><td style="padding:6px 18px;">0.25</td><td style="padding:6px 18px;">0.20</td></tr>
    <tr style="background:var(--lime-2,#f8faf3);"><td style="padding:6px 18px;">GPA 4.0</td><td style="padding:6px 18px;">0.10</td><td style="padding:6px 18px;">0.25</td></tr>
    </table>
    """
    mo.center(mo.Html(_joint))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The six cells sum to one. Summing each column gives the marginal probability of each class standing,

    $$
    \mathbb{P}(X = \text{Freshman}) = 0.15 + 0.25 + 0.10 = 0.50, \qquad \mathbb{P}(X = \text{Senior}) = 0.50.
    $$

    Bayes' rule from Lecture 3 turns the joint probabilities into conditional ones. Among freshmen, the probability of each GPA is

    $$
    \mathbb{P}(Y = 2.0 \mid \text{Freshman}) = \frac{0.15}{0.50} = 0.30, \quad \mathbb{P}(Y = 3.0 \mid \text{Freshman}) = 0.50, \quad \mathbb{P}(Y = 4.0 \mid \text{Freshman}) = 0.20.
    $$

    The conditional expectation of GPA given class standing is the expected value computed with these conditional probabilities. Each value of $X$ produces one number,

    $$
    \mathbb{E}[Y \mid X = \text{Freshman}] = 2.0(0.30) + 3.0(0.50) + 4.0(0.20) = 2.9,
    $$

    $$
    \mathbb{E}[Y \mid X = \text{Senior}] = 2.0(0.10) + 3.0(0.40) + 4.0(0.50) = 3.4.
    $$

    The expected GPA is 2.9 among freshmen and 3.4 among seniors. Every value of $X$ gets its own average of $Y$, and this collection of averages, viewed as a function of $x$, is the relationship a regression line tries to approximate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. The error term revisited

    Lecture 5 modeled the population relationship between hourly wages and years of education as

    $$
    Y = \beta_0 + \beta_1 X + u,
    $$

    where $Y$ is a worker's hourly wage, $X$ is the worker's years of education, and $u$ is the error term. The error term represents everything besides education that is related to wages. Ability, family background, health, and luck all affect what a worker earns, and none of them appear in the model directly, so all of them sit inside $u$.

    The error term is not the residual from Lecture 5. The residual $\hat{u}_i = Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i$ is the gap between an observed wage and the line we fit through one sample. The error $u$ is the gap between a wage and the true population line. Because the population intercept $\beta_0$ and slope $\beta_1$ are never observed, the error term is never observed either.

    The conditional expectation from Section 1 gives us a precise way to talk about these unobserved factors. The quantity $\mathbb{E}[u \mid X = x]$ is the average value of the error term among workers with $x$ years of education. In the wage example, $\mathbb{E}[u \mid X = 16]$ is the average contribution of all unobserved factors including ability and family background to the wages of workers with 16 years of education. If you assume that this unobserved average does not vary with years of education, then you can interpret $\beta_1$ causally. We will state this condition more precisely in the following two sections.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. From prediction to causation

    Lecture 5 was about prediction. The fitted slope of $\hat{\beta}_1 =$ $1.25 says that a worker with one more year of education is predicted to earn about $1.25 more per hour. It does not say that sending the same worker back to school for one more year would raise that worker's wage by $1.25. The *causal interpretation* of the slope is this stronger claim. It says that increasing $X$ by one unit causes $Y$ to change by $\beta_1$ units. A student deciding whether to stay in school for another year, or a government deciding how much to spend on tuition subsidies, needs to know the causal effect of education on earnings, not just the fact that more educated workers tend to earn more.

    In the population model

    $$
    Y = \beta_0 + \beta_1 X + u,
    $$

    the slope $\beta_1$ describes how $Y$ changes when $X$ changes and $u$ is held fixed. In the wage example, $u$ contains every other determinant of wages in the model, such as ability, family background, health, and luck. If education increases by one year while those other determinants stay fixed, then wages change by exactly $\beta_1$.

    The main difficulty in interpreting an estimate of $\beta_1$ causally is that we never observe $u$. OLS fits the line that best predicts $Y$ from $X$ alone. The slope of that line equals the causal $\beta_1$ only when the part of wages hidden in $u$ is not systematically related to education. If workers with more education also tend to have higher ability, stronger family support, or other wage advantages, then the fitted slope blends the effect of education with the effects of those omitted factors.

    The condition that rules out this problem, together with two additional conditions that make estimation and inference reliable, gives us the three *least squares assumptions*.

    1. The conditional distribution of $u$ given $X$ has mean zero, $\mathbb{E}[u \mid X] = 0$.
    2. The data $(X_i, Y_i)$ for $i = 1, \ldots, n$ are independently and identically distributed.
    3. Large outliers are unlikely.

    Only the first assumption carries causal content, and it is the one that fails most often in practice. The second and third assumptions do not make the slope causal. They explain when sample data can recover the population slope and when we can attach a useful margin of error to the estimate. We now go over each assumption one at a time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. The least squares assumptions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4a"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 1: the conditional mean of $u$ given $X$ is zero</span>

    The first least squares assumption says that the conditional mean of the error term is zero at every value of $X$,

    $$
    \mathbb{E}[u \mid X] = 0.
    $$

    In the wage example, this means that workers with different levels of education do not systematically differ in the other determinants of wages contained in $u$. Workers with 16 years of education may differ from workers with 12 years of education in their schooling, but on average they must not differ in ability, family background, health, luck, or anything else in the error term that affects wages.

    This is a strong requirement, and it is easy to see how it can fail. Suppose students with higher ability find school easier and therefore stay in school longer. Then workers with 16 years of education will have higher average ability than workers with 12 years of education. In that case, $\mathbb{E}[u \mid X = 16] > \mathbb{E}[u \mid X = 12],$ and the assumption fails. OLS then attributes to education some of the wage gains that ability would have produced anyway, so $\hat{\beta}_1$ overstates the causal effect of schooling. When the assumption does hold, by contrast, this first assumption is exactly what makes the OLS slope estimator unbiased, so that across repeated samples its average equals the true causal effect $\beta_1$. Section 5 develops this property and its companion, consistency.

    This assumption cannot be tested with the data alone. The error term is unobserved, so we cannot compute $\mathbb{E}[u \mid X = x]$ from a sample of $X$ and $Y$. Whether the assumption holds must be argued from what we know about how the data were generated, not read from a calculation.

    An equivalent way of stating the assumption is that the average value of the error term does not vary with $X$. For the slope to have a causal interpretation, the key requirement is that $\mathbb{E}[u \mid X = x]$ be the same at every value of $x$. If that common value were some constant other than zero, it would be absorbed into the intercept and the slope would be unchanged. With an intercept in the model, we can therefore write the condition as $\mathbb{E}[u \mid X] = 0$. The appendix shows why this is true mathematically.

    The plot below shows the same idea visually. It splits 40 workers into two groups, lower ability in light gray and higher ability in navy. In this example, ability is the only factor in the error term. Within each ability group, the true causal effect of one more year of education is the same $1.20 per hour, shown by the two parallel dashed orange lines. The higher-ability group earns more at every education level, so its line sits above the lower-ability line.

    The slider controls how strongly ability and education are related. When the slider equals zero, both ability groups have the same distribution of education. The condition $\mathbb{E}[u \mid X] = 0$ holds, and the pooled OLS line through all 40 workers has the same slope as the two within-group lines. As the slider rises, higher-ability workers shift toward more education and lower-ability workers shift toward less education. The two groups pull apart, and the pooled OLS line becomes steeper than $1.20 as it blends the effect of education with the effect of ability, even though the true causal effect of education within each ability group has not changed.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    _rng = np.random.default_rng(6)
    lsa_X = _rng.uniform(8.0, 20.0, 40)
    lsa_e = 3.0 * _rng.normal(0.0, 1.0, 40)
    lsa_b0_true = 8.0
    lsa_b1_true = 1.2
    return lsa_X, lsa_b0_true, lsa_b1_true, lsa_e


@app.cell(hide_code=True)
def _(np):
    # Fixed data for the Assumption 1 plot: 40 workers in two ability groups.
    # Both groups are given the SAME 20 education values, so at slider 0 the group
    # (ability) is unrelated to education and the pooled fit is unbiased. The wage
    # noise is residualized against education and group so that only the slider's
    # selection drives the bias. Nothing is re-drawn as the slider moves.
    _rng = np.random.default_rng(11)
    _u = _rng.uniform(11.0, 17.0, 20)
    grp_baseX = np.concatenate([_u, _u])
    grp_D = np.concatenate([np.zeros(20), np.ones(20)])  # 0 = lower ability, 1 = higher
    _e = _rng.normal(0.0, 2.5, 40)
    _Z = np.column_stack([np.ones(40), grp_baseX, grp_D])
    grp_e = _e - _Z @ np.linalg.lstsq(_Z, _e, rcond=None)[0]
    grp_b0, grp_b1, grp_gamma, grp_spread = 8.0, 1.20, 8.0, 3.0
    return grp_D, grp_b0, grp_b1, grp_baseX, grp_e, grp_gamma, grp_spread


@app.cell(hide_code=True)
def _(mo):
    sel_strength = mo.ui.slider(
        start=0.0, stop=1.0, step=0.1, value=0.0,
        label="Do higher-ability workers tend to get more education? (0 = No, 1 = Yes, strongly)",
        show_value=True,
    )
    sel_strength
    return (sel_strength,)


@app.cell(hide_code=True)
def _(
    alt,
    grp_D,
    grp_b0,
    grp_b1,
    grp_baseX,
    grp_e,
    grp_gamma,
    grp_spread,
    mo,
    np,
    pd,
    sel_strength,
):
    _sel = float(sel_strength.value)
    _X = grp_baseX + _sel * grp_spread * (2.0 * grp_D - 1.0)
    _Y = grp_b0 + grp_b1 * _X + grp_gamma * grp_D + grp_e
    _b1 = float(np.cov(_X, _Y, ddof=1)[0, 1] / np.var(_X, ddof=1))
    _b0 = float(_Y.mean() - _b1 * _X.mean())

    _xdom = [7.0, 21.0]
    _ydom = [5.0, 50.0]
    _xline = np.array([8.0, 20.0])
    _group = np.where(grp_D > 0.5, "Higher ability", "Lower ability")
    _pts = pd.DataFrame({"x": _X, "y": _Y, "group": _group})
    _ols = pd.DataFrame({"x": _xline, "y": _b0 + _b1 * _xline})
    _true_low = pd.DataFrame({"x": _xline, "y": grp_b0 + grp_b1 * _xline})
    _true_high = pd.DataFrame({"x": _xline, "y": grp_b0 + grp_gamma + grp_b1 * _xline})

    _scatter = (
        alt.Chart(_pts)
        .mark_circle(size=95, clip=True)
        .encode(
            x=alt.X("x:Q", title="Years of education", scale=alt.Scale(domain=_xdom, nice=False)),
            y=alt.Y("y:Q", title="Hourly wage (USD)", scale=alt.Scale(domain=_ydom, nice=False)),
            color=alt.Color(
                "group:N",
                scale=alt.Scale(domain=["Lower ability", "Higher ability"], range=["#b6c2cf", "#1f4e79"]),
                legend=alt.Legend(title=None, orient="top"),
            ),
        )
    )
    _true_low_line = (
        alt.Chart(_true_low)
        .mark_line(color="orange", strokeDash=[6, 4], size=2, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _true_high_line = (
        alt.Chart(_true_high)
        .mark_line(color="orange", strokeDash=[6, 4], size=2, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _ols_line = (
        alt.Chart(_ols)
        .mark_line(color="#1f4e79", size=2.5, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _chart = alt.layer(_scatter, _true_low_line, _true_high_line, _ols_line).properties(
        width=560, height=340,
        title="Within each ability group the true effect of a year's education is 1.20; pooling them tilts OLS steeper",
    )

    if _sel == 0.0:
        _body = (
            rf"The two groups have the same spread of educational attainment, so $\mathbb{{E}}[u \mid X] = 0$ "
            rf"holds. The pooled OLS line $\hat{{Y}} = {_b0:.2f} + {_b1:.2f}\,X$ (solid navy) matches "
            rf"the within-group return of 1.20 drawn by the two parallel dashed orange lines."
        )
    else:
        _body = (
            rf"With the slider at {_sel:.1f}, higher-ability workers (navy) hold more education and "
            rf"lower-ability workers (gray) hold less. Pooling the two groups, OLS reports a slope of "
            rf"{_b1:.2f}, steeper than the 1.20 return that still holds inside each group, because it "
            rf"credits education with earnings that come from ability."
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
    mo.md(r"""
    <a id="sec4b"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 2: the data are i.i.d.</span>

    The second least squares assumption says that the observations $(X_i, Y_i)$ for $i = 1, \ldots, n$ are independently and identically distributed (i.i.d). Recall from Lecture 3 that this means we assume the sample is comprised of random draws from the same population. The “Identically distributed” part means that each observation is drawn in the same way. The “Independent” part means that knowing one observation does not provide information about another.

    Both parts of i.i.d. can fail. Independence fails when observations are linked to each other. For example, workers from the same firm may have wages that move together because they share the same pay policies, local labor market, or manager. Identical distribution fails when observations are not all drawn in the same way. For example, if one part of a wage sample comes from workers interviewed before a recession and another part comes from workers interviewed after, the observations may come from different wage-education distributions.

    i.i.d. sampling helps connect the sample to the population. Because observations are random draws from the same distribution, the law of large numbers makes sample averages converge to population averages as the sample grows. Together with the other least squares assumptions, this helps make $\hat{\beta}_1$ a consistent and unbiased estimator of $\beta_1$, two concepts we defined in Lecture 4.  I.i.d. sampling also supports the construction of the standard error, $\text{se}(\hat{\beta}_1)$, which Lecture 7 uses to test hypotheses about $\beta_1$. Later parts of the course handle data where independence fails by design, such as with panel data and clustered data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4c"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 3: large outliers are unlikely</span>

    An *outlier* is an observation whose value of $X$, of $Y$, or of both sits far from the rest of the data. The third assumption states that large outliers are unlikely. It rules out distributions that produce values so extreme that a handful of points can dominate the sample. The mathematical definition of an outlier is in the appendix.

    Outliers matter to OLS because of the squaring in the least squares criterion from Lecture 5. A point far from the line contributes the square of a large residual to the sum being minimized, so the fitted line swings toward it. One badly recorded observation, an hourly wage typed as \$150 instead of \$15, can move the slope on its own. In practice this assumption is a reminder to plot the data and check extreme values before trusting a regression estimate, because many outliers in economic data are entry errors rather than real values.

    Like the i.i.d. assumption, this one supports the standard error of the slope rather than the causal interpretation of $\hat{\beta}_1$.

    Consider the example below. The two faint orange points are wages recorded with a misplaced decimal, sitting far above the rest of the workers. The check box decides whether they are included in the OLS regression. Leave it unticked and the navy line is fit to the 40 properly recorded workers, resting on top of the dashed gray line. Tick it and the two outliers are included in the OLS regression line.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    include_outliers = mo.ui.checkbox(label="Include the two mistyped wages in the fit")
    include_outliers
    return (include_outliers,)


@app.cell(hide_code=True)
def _(
    alt,
    include_outliers,
    lsa_X,
    lsa_b0_true,
    lsa_b1_true,
    lsa_e,
    mo,
    np,
    pd,
):
    _inc = bool(include_outliers.value)
    _Y = lsa_b0_true + lsa_b1_true * lsa_X + lsa_e
    _ox = np.array([15.0, 18.0])
    _oy = np.array([135.0, 150.0])

    _b1_base = float(np.cov(lsa_X, _Y, ddof=1)[0, 1] / np.var(lsa_X, ddof=1))
    _b0_base = float(_Y.mean() - _b1_base * lsa_X.mean())
    _Xall = np.append(lsa_X, _ox)
    _Yall = np.append(_Y, _oy)
    _b1_all = float(np.cov(_Xall, _Yall, ddof=1)[0, 1] / np.var(_Xall, ddof=1))
    _b0_all = float(_Yall.mean() - _b1_all * _Xall.mean())

    _xdom = [7.0, 21.0]
    _ydom = [0.0, 160.0]
    _xline = np.array([7.0, 21.0])
    _pts = pd.DataFrame({"x": lsa_X, "y": _Y})
    _out = pd.DataFrame({"x": _ox, "y": _oy})
    _base = pd.DataFrame({"x": _xline, "y": _b0_base + _b1_base * _xline})
    _fit_y = (_b0_all + _b1_all * _xline) if _inc else (_b0_base + _b1_base * _xline)
    _fit = pd.DataFrame({"x": _xline, "y": _fit_y})

    _scatter = (
        alt.Chart(_pts)
        .mark_circle(color="#1f4e79", opacity=0.7, size=55, clip=True)
        .encode(
            x=alt.X("x:Q", title="Years of education", scale=alt.Scale(domain=_xdom, nice=False)),
            y=alt.Y("y:Q", title="Hourly wage (USD)", scale=alt.Scale(domain=_ydom, nice=False)),
        )
    )
    _outliers = (
        alt.Chart(_out)
        .mark_circle(color="orange", size=130, clip=True, opacity=(0.95 if _inc else 0.18))
        .encode(x="x:Q", y="y:Q")
    )
    _base_line = (
        alt.Chart(_base)
        .mark_line(color="#9aa5b1", strokeDash=[5, 4], size=2, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _fit_line = (
        alt.Chart(_fit)
        .mark_line(color="#1f4e79", size=2.5, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _chart = alt.layer(_scatter, _outliers, _base_line, _fit_line).properties(
        width=560, height=360,
        title="Two mistyped wages, left out of the fit or included",
    )

    if _inc:
        _body = (
            rf"With the two mistyped wages included, the OLS slope swings from {_b1_base:.2f} to "
            rf"{_b1_all:.2f}. Two points out of 42 pull the navy line away from the dashed gray line "
            rf"fit to the clean data, even though the other 40 workers have not moved."
        )
    else:
        _body = (
            rf"The two faint orange points are wages entered with a misplaced decimal, \$135 and "
            rf"\$150 in place of \$13.50 and \$15.00. They are not in the fit yet, so the OLS slope "
            rf"on the 40 ordinary workers is {_b1_base:.2f}. Tick the box to add them and watch it move."
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
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Unbiasedness and consistency

    The least squares assumptions do more than justify a causal interpretation of the slope. They also inform us of how the OLS estimator $\hat{\beta}_1$ behaves across repeated samples.

    First, $\hat{\beta}_1$ is *unbiased* if its average value across all possible samples equals the true slope,

    $$
    \mathbb{E}[\hat{\beta}_1] = \beta_1.
    $$

    Unbiasedness follows from the first least squares assumption, which says that the conditional mean of the error given $X$ is zero. The appendix proves why this is true with algebra. The point is not that any one estimate must equal $\beta_1$. It is that the estimator is right on average, rather than systematically too high or too low.

    Second, $\hat{\beta}_1$ is *consistent* if it converges to the true slope as the sample grows,

    $$
    \hat{\beta}_1 \overset{p}{\to} \beta_1.
    $$

    Consistency implies that estimates from large samples are more likely to be closer to $\beta_1$. As $n$ rises, the spread of $\hat{\beta}_1$ across repeated samples shrinks, so the estimates cluster closer and closer to the true value. Lecture 7 derives the variance for $\hat{\beta}_1$, and shows how it falls with the sample size.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** conditional expectation, causal "
            "interpretation, least squares assumptions, outlier, unbiasedness, "
            "consistency.\n\n"
            "**Concepts:** the conditional expectation as the "
            "population object a regression approximates, the error term as "
            "everything besides X that affects Y, why only the mean-zero error "
            "assumption carries causal content, why that assumption cannot be "
            "tested from data alone, what the i.i.d. and no-outlier assumptions "
            "add for estimating the slope and its standard error, how a "
            "single outlier can swing the OLS line, the population "
            "regression line as the conditional expectation of Y given X, and "
            "why the first assumption makes the slope estimator unbiased while "
            "the assumptions together make it consistent."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "## Appendix": mo.md(r"""
        This is bonus material. You will not be tested on the content of the appendix.

        **The population regression line is a conditional expectation.**

        Section 1 claimed that a regression approximates the conditional expectation of $Y$ given $X$. Assumption 1 makes that exact. Take the population model and condition on $X = x$,

        $$ \mathbb{E}[Y \mid X = x] = \mathbb{E}[\beta_0 + \beta_1 X + u \mid X = x] = \beta_0 + \beta_1 x + \mathbb{E}[u \mid X = x]. $$

        The first two terms pass through the conditional expectation unchanged because once we condition on $X = x$, the quantity $\beta_0 + \beta_1 x$ is a fixed number, and the expected value of a fixed number is the number itself. Under Assumption 1 the last term is zero, so

        $$ \mathbb{E}[Y \mid X = x] = \beta_0 + \beta_1 x. $$

        The population regression line passes through the average value of $Y$ at every value of $X$. The OLS line from Lecture 5 is the sample estimate of exactly this function.

        **A constant conditional mean folds into the intercept.**

        Section 4 stated that only variation of $\mathbb{E}[u \mid X = x]$ with $x$ threatens the slope. To see why, suppose the conditional mean is some constant $c$ other than zero, $\mathbb{E}[u \mid X = x] = c$ for every $x$. Define a new error $\tilde{u} = u - c$ and a new intercept $\tilde{\beta}_0 = \beta_0 + c$. Then

        $$ Y = \beta_0 + \beta_1 X + u = (\beta_0 + c) + \beta_1 X + (u - c) = \tilde{\beta}_0 + \beta_1 X + \tilde{u}, $$

        and the new error satisfies $\mathbb{E}[\tilde{u} \mid X = x] = c - c = 0$. The rewritten model satisfies Assumption 1, and the slope $\beta_1$ is the same in both versions. A constant level of ability across all education groups changes where the line sits, not how steep it is.

        **The no-large-outliers condition in symbols.**

        Least Squares Assumption 3 says large outliers are unlikely. The formal version is a condition on the fourth moments of $X$ and $Y$,

        $$ 0 < \mathbb{E}\left[X_i^4\right] < \infty \quad \text{and} \quad 0 < \mathbb{E}\left[Y_i^4\right] < \infty. $$

        A finite fourth moment rules out distributions whose tails are heavy enough that a single draw can be enormous, the kind that would dominate the sum of squares OLS minimizes. With finite fourth moments the sampling distribution of $\hat{\beta}_1$ settles to the normal shape the standard error in Lecture 7 relies on.

        **Unbiasedness of $\hat{\beta}_1$.**

        Write $S_{XX} = \sum_{i=1}^{n}(X_i - \hat{\mu}_X)^2$. The OLS slope from Lecture 5 can be written

        $$ \hat{\beta}_1 = \frac{\sum_{i=1}^{n}(X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y)}{S_{XX}}. $$

        Substituting the model $Y_i = \beta_0 + \beta_1 X_i + u_i$ and subtracting sample means gives $Y_i - \hat{\mu}_Y = \beta_1 (X_i - \hat{\mu}_X) + (u_i - \bar{u})$, so

        $$ \hat{\beta}_1 - \beta_1 = \frac{1}{S_{XX}}\sum_{i=1}^{n}(X_i - \hat{\mu}_X)\,u_i. $$

        Take the expectation conditional on the values of $X$. Assumption 1, $\mathbb{E}[u_i \mid X] = 0$, makes every term on the right have conditional mean zero, so $\mathbb{E}[\hat{\beta}_1 \mid X] = \beta_1$. Averaging over $X$ by the law of iterated expectations gives $\mathbb{E}[\hat{\beta}_1] = \beta_1$, which is what unbiasedness means.
        """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec5SimpleLinearRegression.html" target="_self">← Lecture 5</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec7InferenceAndOmittedVariableBias.html" target="_self">Lecture 7 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
