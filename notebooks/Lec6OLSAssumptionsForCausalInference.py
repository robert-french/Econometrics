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
# Flags this notebook as a work in progress. build.py reads this module-level
# constant and the homepage template renders a "Preliminary" badge on the card.
__preliminary__ = True
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: block; margin-bottom: 1.5em;">Course home</a>'),
            mo.md("# [Lecture 6](#top)"),
            mo.md("OLS Assumptions for Causal Inference"),
            mo.nav_menu(
                {
                    "#sec1": "1. Conditional expectation",
                    "#sec2": "2. The error term revisited",
                    "#sec3": "3. From prediction to causation",
                    "#sec4": "4. The least squares assumptions",
                    "#sec4a": "4.1 Least Squares Assumption 1",
                    "#sec4b": "4.2 Least Squares Assumption 2",
                    "#sec4c": "4.3 Least Squares Assumption 3",
                    "#sec5": "5. What the assumptions give us",
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
    [5. What the assumptions give us](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Conditional expectation

    Lecture 5 fit a line through a sample of wages and education and was careful to interpret the slope as a description of association. This lecture states the conditions under which that slope can instead be read as a causal effect. The conditions are claims about averages within groups, so the first step is a tool for talking about such averages.

    The *conditional expectation* of $Y$ given $X$ is the average of $Y$ among observations that share the same value of $X$. We write it as

    $$
    \mathbb{E}[Y \mid X = x].
    $$

    Like the expected value $\mathbb{E}[Y]$ from Lecture 2, the conditional expectation describes the population, not a sample. It is also the object a regression approximates. The fitted line from Lecture 5 is a straight-line estimate of the average value of $Y$ at each value of $X$, which is exactly what $\mathbb{E}[Y \mid X = x]$ records.

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

    The expected GPA is 2.9 among freshmen and 3.4 among seniors. Every value of $X$ gets its own average of $Y$, and this collection of averages, viewed as a function of $x$, is the relationship a regression line tries to trace out.
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

    where $Y$ is a worker's hourly wage, $X$ is the worker's years of education, and $u$ is the error term. The error term holds everything besides education that is related to wages. Ability, family background, health, and luck all affect what a worker earns, and none of them appear in the model, so all of them sit inside $u$.

    The error term is not the residual from Lecture 5. The residual $\hat{u}_i = Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i$ is the gap between an observed wage and the line we fit through one sample. The error $u$ is the gap between a wage and the true population line. Because the population intercept $\beta_0$ and slope $\beta_1$ are never observed, the error term is never observed either.

    The conditional expectation from Section 1 gives us a precise way to talk about these unobserved factors. The quantity $\mathbb{E}[u \mid X = x]$ is the average effect of everything in the error term among workers with $x$ years of education. In the wage example, $\mathbb{E}[u \mid X = 16]$ is the average contribution of ability and family background to the wages of workers with 16 years of education. Whether that average is allowed to change with education turns out to be the dividing line between prediction and causation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. From prediction to causation

    Everything in Lecture 5 was about prediction. The fitted slope of \$1.25 says that a worker with one more year of education is predicted to earn about \$1.25 more per hour. It does not say that sending the same worker back to school for a year would raise that worker's wage by \$1.25. The *causal interpretation* of the slope is this stronger claim, that raising $X$ by one unit causes $Y$ to change by $\beta_1$ units. A student deciding whether to stay in school another year, or a government pricing a tuition subsidy, needs the causal claim, not the fact that educated workers happen to earn more.

    In the population model $Y = \beta_0 + \beta_1 X + u$, the slope $\beta_1$ already is the causal effect by construction. The error $u$ holds every other influence on wages, so raising $X$ by one unit while $u$ stays fixed changes $Y$ by exactly $\beta_1$. The difficulty is that OLS never sees $u$. It fits the line that best predicts $Y$ from $X$ alone, and the slope of that line equals the causal $\beta_1$ only when the part of wages hidden in $u$ does not move with education. When that hidden part does move with education, the fitted slope blends the effect of schooling with the effect of whatever in $u$ travels alongside it.

    The condition that rules this out, together with two more that make the estimate and its precision trustworthy, are the three *least squares assumptions*.

    1. The conditional distribution of $u$ given $X$ has a mean of zero, $\mathbb{E}[u \mid X] = 0$.
    2. The data $(X_i, Y_i)$ for $i = 1, \ldots, n$ are independently and identically distributed.
    3. Large outliers are unlikely.

    Only the first assumption carries causal content, and it is the one that fails most often in practice. The second and third say nothing about causation. They are what let us estimate $\beta_1$ from a sample and attach a margin of error to the estimate. The next three sections take the assumptions one at a time, and Section 5 collects what each one buys.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. The least squares assumptions

    Each of the three assumptions does a different job. The first decides whether the slope can be read as a causal effect. The second and third decide whether a finite sample can estimate that slope and how precisely.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4a"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 1: the conditional mean of $u$ given $X$ is zero</span>

    The first assumption states that the conditional mean of the error term is zero at every value of $X$,

    $$
    \mathbb{E}[u \mid X] = 0.
    $$

    In the wage example, this says that the average of everything in the error term is the same at every education level. Workers with 16 years of education may differ from workers with 12 in their schooling, but on average they must differ in nothing else that affects wages, not in ability, not in family background.

    That is a strong requirement, and it is easy to see how it fails. Suppose students with higher ability find school easier and stay in it longer. Then among workers with 16 years of education, average ability is higher than among workers with 12, so $\mathbb{E}[u \mid X = 16] > \mathbb{E}[u \mid X = 12]$ and the assumption fails. OLS attributes to education some of the wage gains that ability would have produced anyway, and $\hat{\beta}_1$ overstates the causal effect of schooling.

    The assumption cannot be tested with the data alone. The error term is unobserved, so there is no way to compute $\mathbb{E}[u \mid X = x]$ from a sample of $X$ and $Y$. Whether the assumption holds has to be argued from knowledge of how the data came about, not read off a calculation.

    One technical note. The causal reading requires only that $\mathbb{E}[u \mid X = x]$ not vary with $x$. If it equaled some constant other than zero, that constant would fold into the intercept and leave the slope untouched. The appendix shows the algebra. With an intercept in the model, ''the conditional mean of $u$ does not depend on $X$'' and ''$\mathbb{E}[u \mid X] = 0$'' are the same assumption.

    The plot below splits the 40 workers into two groups, lower ability in light gray and higher ability in navy, and for this example ability is the only thing in the error term. Within each group the true causal effect of a year of education is the same \$1.20 per hour, drawn as the two parallel dashed orange lines. The higher-ability group earns more at every education level, which is why its line sits above the other. The slider controls how strongly the two groups differ in schooling. At zero, both groups have the same spread of education, $\mathbb{E}[u \mid X] = 0$ holds, and the pooled OLS line (solid navy) through all 40 workers matches the within-group slope of 1.20. As the slider rises, the higher-ability workers shift to more education and the lower-ability workers to less, the two clouds pull apart, and the pooled OLS line tilts steeper than 1.20 even though nothing changed the true effect inside either group.
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
        start=0.0, stop=1.0, step=0.1, value=0.5,
        label="How strongly higher-ability workers get more education (0 = no link, 1 = strong)",
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
        title="Within each group the true return is 1.20; pooling them tilts OLS steeper",
    )

    if _sel == 0.0:
        _body = (
            rf"The two groups have the same spread of education, so $\mathbb{{E}}[u \mid X] = 0$ "
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

    The second assumption states that the observations $(X_i, Y_i)$ for $i = 1, \ldots, n$ are independently and identically distributed. Lecture 3 defined the two halves of that phrase. All observations are drawn from the same underlying distribution, and knowing one observation tells you nothing about another. Sampling workers at random from one population delivers both halves, which is why i.i.d. is a reasonable description of survey data like the wage sample.

    Both halves can fail. Data collected in sequence carry information about each other. Today's temperature helps predict tomorrow's, so a year of daily weather recordings is not a set of independent draws. Pooling students sampled from several countries mixes different underlying populations, so those observations are not identically distributed.

    This assumption carries no causal content. A causal reading of $\beta_1$ rests entirely on Assumption 1, with or without i.i.d. sampling. What i.i.d. sampling buys is the estimate. It makes $\hat{\beta}_1$ an unbiased and consistent estimate of $\beta_1$, and it underpins the standard error of the slope, $\text{se}(\hat{\beta}_1)$, built from the tools in Lecture 4. Lecture 7 constructs that standard error and uses it to test hypotheses about $\beta_1$. Later parts of the course, on panel data and clustered standard errors, handle data where independence fails by design.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4c"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 3: large outliers are unlikely</span>

    An *outlier* is an observation whose value of $X$, of $Y$, or of both sits far from the rest of the data. The third assumption states that large outliers are unlikely. The formal version is a condition on fourth moments,

    $$
    0 < \mathbb{E}\left[X_i^4\right] < \infty \quad \text{and} \quad 0 < \mathbb{E}\left[Y_i^4\right] < \infty,
    $$

    which rules out distributions that produce values so extreme that a handful of points can dominate the sample.

    Outliers matter to OLS because of the squaring in the least squares criterion from Lecture 5. A point far from the line contributes the square of a large residual to the sum being minimized, so the fitted line swings toward it. One badly recorded observation, an hourly wage typed as \$150 instead of \$15, can move the slope on its own. In practice this assumption is a reminder to plot the data and check extreme values before trusting a regression, because many outliers in economic data are entry errors rather than real values.

    Like the i.i.d. assumption, this one supports the standard error of the slope rather than the causal reading. It is a regularity condition that keeps the estimator and its variance well behaved.

    Try it below. The two faint orange points are wages recorded with a misplaced decimal, sitting far above the rest of the workers. The check box decides whether they count. Leave it unticked and the navy line is fit to the 40 ordinary workers, resting on top of the dashed gray line. Tick it and the two outliers join the fit, and the navy line swings up and away from the gray line, which stays where the clean data put it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    include_outliers = mo.ui.checkbox(label="Include the two mistyped wages in the fit")
    include_outliers
    return (include_outliers,)


@app.cell(hide_code=True)
def _(alt, include_outliers, lsa_X, lsa_b0_true, lsa_b1_true, lsa_e, mo, np, pd):
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
    ## 5. What the assumptions give us

    The three assumptions are not interchangeable, and it helps to see what each one adds. Assumption 1 is the only one about causation. On its own it makes the population slope $\beta_1$ equal to the causal effect of education on wages rather than a summary of how the two move together. Whether you hold a sample at all is beside the point, since this is a claim about the population.

    The other two are about getting from the population to a sample and back. With Assumption 1 holding, adding the i.i.d. assumption makes $\hat{\beta}_1$ an unbiased and consistent estimate of $\beta_1$, so a large enough random sample lands near the true causal effect. Adding the no-large-outliers assumption keeps the sampling distribution of $\hat{\beta}_1$ well behaved enough to attach a standard error, and from that standard error come the hypothesis tests and confidence intervals built in Lecture 7.

    | Assumptions in force | What you can claim |
    | --- | --- |
    | Assumption 1 | The population slope is the causal effect, not just an association. |
    | Assumptions 1 and 2 | The estimated slope is unbiased and consistent for that causal effect. |
    | Assumptions 1, 2, and 3 | The estimate comes with a valid standard error, so tests and confidence intervals are trustworthy. |

    Causation enters at the top row and stays. The lower rows add no causal content; they turn that single causal number into something you can estimate and place error bars around. A failure of Assumption 1 is therefore fatal to a causal claim, while a failure of Assumption 2 or 3 damages the standard error, a problem the panel-data and robust-standard-error tools later in the course are built to repair.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** conditional expectation, causal "
            "interpretation, least squares assumptions, outlier.\n\n"
            "**Key concepts covered:** the conditional expectation as the "
            "population object a regression approximates, the error term as "
            "everything besides X that affects Y, why only the mean-zero error "
            "assumption carries causal content, why that assumption cannot be "
            "tested from data alone, what the i.i.d. and no-outlier assumptions "
            "add for estimating the slope and judging its precision, how a "
            "single outlier can swing the OLS line, and the population "
            "regression line as the conditional expectation of Y given X."
        ),
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
