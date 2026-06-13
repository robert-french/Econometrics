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
                    "#sec4": "4. Assumption 1: the error has mean zero given X",
                    "#sec5": "5. Assumption 2: the data are i.i.d.",
                    "#sec6": "6. Assumption 3: large outliers are unlikely",
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
    mo.md(r"""
    ## Contents

    1. [Conditional expectation](#sec1)
    2. [The error term revisited](#sec2)
    3. [From prediction to causation](#sec3)
    4. [Assumption 1: the error has mean zero given X](#sec4)
    5. [Assumption 2: the data are i.i.d.](#sec5)
    6. [Assumption 3: large outliers are unlikely](#sec6)
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

    Everything in Lecture 5 was about prediction. The fitted slope of \$1.25 says that a worker with one more year of education is predicted to earn about \$1.25 more per hour. It does not say that sending a worker back to school for a year would raise that worker's wage by \$1.25. The *causal interpretation* of the slope is exactly this stronger claim, that increasing $X$ by one unit causes $Y$ to change by $\beta_1$ units.

    The difference matters for decisions. A student weighing another year of school, or a government weighing a tuition subsidy, needs to know what education does to wages, not merely that educated workers happen to earn more.

    To attribute a causal interpretation to $\hat{\beta}_1$, we make three assumptions about how the data came to be, known as the *least squares assumptions for causal inference*.

    1. The conditional distribution of $u$ given $X$ has a mean of zero. That is, $\mathbb{E}[u \mid X] = 0$.
    2. The data $(X_i, Y_i)$ for $i = 1, \ldots, n$ are independently and identically distributed.
    3. Large outliers are unlikely.

    The first assumption carries the causal content, and it is the one that fails most often in practice. The second and third concern the quality of the sample. The next three sections unpack them one at a time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Assumption 1: the error has mean zero given X

    Assumption 1 states that the conditional mean of the error term is zero at every value of $X$,

    $$
    \mathbb{E}[u \mid X] = 0.
    $$

    In the wage example, this says that average ability and family background are the same at every education level. Workers with 16 years of education may differ from workers with 12 in their schooling, but on average they must differ in nothing else that affects wages.

    That is a strong requirement, and it is easy to see how it fails. Suppose students with higher ability find school easier and stay in it longer. Then among workers with 16 years of education, average ability is higher than among workers with 12, so $\mathbb{E}[u \mid X = 16] > \mathbb{E}[u \mid X = 12]$ and Assumption 1 fails. OLS attributes to education some of the wage gains that ability would have produced anyway, and $\hat{\beta}_1$ overstates the causal effect of schooling.

    The assumption cannot be tested with the data alone. The error term is unobserved, so there is no way to compute $\mathbb{E}[u \mid X = x]$ from a sample of $X$ and $Y$. Whether the assumption is plausible has to be argued from knowledge of how the data came about, not from a calculation.

    One technical note. The causal reading really requires only that $\mathbb{E}[u \mid X = x]$ does not vary with $x$. If it equaled some constant other than zero, that constant would fold into the intercept and leave the slope untouched. The appendix shows the algebra. With an intercept in the model, ''the conditional mean of $u$ does not depend on $X$'' and ''$\mathbb{E}[u \mid X] = 0$'' are the same assumption.

    The plot below shows why no test can detect the failure. The 40 workers are the sample from Lecture 5, and the true causal effect of a year of education is fixed at \$1.20 per hour, drawn as the dashed orange line. The slider tilts average ability with education. At zero, Assumption 1 holds and the OLS line (solid navy) matches the causal line up to sampling noise. Away from zero, the OLS line rotates away from the causal line. The scatter, though, looks like an ordinary regression dataset at every slider value. Nothing in the data announces the violation.
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
def _(mo):
    bias_delta = mo.ui.slider(
        start=-1.0, stop=2.0, step=0.25, value=0.75,
        label="How strongly average ability rises with education", show_value=True,
    )
    bias_delta
    return (bias_delta,)


@app.cell(hide_code=True)
def _(alt, bias_delta, lsa_X, lsa_b0_true, lsa_b1_true, lsa_e, mo, np, pd):
    _d = float(bias_delta.value)
    _Y = lsa_b0_true + lsa_b1_true * lsa_X + _d * (lsa_X - 14.0) + lsa_e
    _b1 = float(np.cov(lsa_X, _Y, ddof=1)[0, 1] / np.var(lsa_X, ddof=1))
    _b0 = float(_Y.mean() - _b1 * lsa_X.mean())

    _xdom = [7.0, 21.0]
    _ydom = [-5.0, 55.0]
    _xline = np.array([7.0, 21.0])
    _pts = pd.DataFrame({"x": lsa_X, "y": _Y})
    _ols = pd.DataFrame({"x": _xline, "y": _b0 + _b1 * _xline})
    _causal = pd.DataFrame({"x": _xline, "y": lsa_b0_true + lsa_b1_true * _xline})

    _scatter = (
        alt.Chart(_pts)
        .mark_circle(color="#1f4e79", opacity=0.7, size=60, clip=True)
        .encode(
            x=alt.X("x:Q", title="Years of education", scale=alt.Scale(domain=_xdom, nice=False)),
            y=alt.Y("y:Q", title="Hourly wage (USD)", scale=alt.Scale(domain=_ydom, nice=False)),
        )
    )
    _causal_line = (
        alt.Chart(_causal)
        .mark_line(color="orange", strokeDash=[6, 4], size=2.5, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _ols_line = (
        alt.Chart(_ols)
        .mark_line(color="#1f4e79", size=2.5, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _chart = alt.layer(_scatter, _causal_line, _ols_line).properties(
        width=560, height=340,
        title="When ability tilts with education, OLS misses the causal effect",
    )

    if _d == 0.0:
        _body = (
            rf"The slider is at 0.00, so average ability is the same at every education level "
            rf"and Assumption 1 holds. The OLS line $\hat{{Y}} = {_b0:.2f} + {_b1:.2f}\,X$ differs "
            rf"from the causal line $Y = 8.00 + 1.20\,X$ only through sampling noise."
        )
    else:
        _body = (
            rf"With the slider at {_d:+.2f}, average ability shifts wages by {_d * 6:+.1f} dollars "
            rf"per hour among workers with 20 years of education and by {_d * -6:+.1f} among workers "
            rf"with 8 years, so $\mathbb{{E}}[u \mid X = x]$ varies with $x$. OLS estimates a slope "
            rf"of {_b1:.2f} even though the causal effect is fixed at 1.20, and the scatter offers "
            rf"no warning."
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
    ## 5. Assumption 2: the data are i.i.d.

    Assumption 2 states that the observations $(X_i, Y_i)$ for $i = 1, \ldots, n$ are independently and identically distributed. Lecture 3 defined the two halves of that phrase. All observations are drawn from the same underlying distribution, and knowing one observation tells you nothing about another. Sampling workers at random from one population delivers both halves, which is why i.i.d. is a reasonable description of survey data like the wage sample.

    Both halves can fail. Data collected sequentially are informative about each other. Today's temperature helps predict tomorrow's, so a year of daily weather recordings is not a set of independent draws. And pooling students sampled from different countries mixes different underlying populations, so those observations are not identically distributed.

    Unlike Assumption 1, the i.i.d. assumption is not strictly necessary for a causal reading of $\hat{\beta}_1$. Its main role is in constructing the standard error of the slope, $\text{se}(\hat{\beta}_1)$, using the tools from Lecture 4. Lecture 7 builds that standard error and uses it to test hypotheses about $\beta_1$. Later parts of the course, on panel data and clustered standard errors, handle data where independence fails by design.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec6"></a>
    ## 6. Assumption 3: large outliers are unlikely

    An *outlier* is an observation whose value of $X$, of $Y$, or of both sits far from the rest of the data. Assumption 3 states that large outliers are unlikely. The formal version is a condition on fourth moments,

    $$
    0 < \mathbb{E}\left[X_i^4\right] < \infty \quad \text{and} \quad 0 < \mathbb{E}\left[Y_i^4\right] < \infty,
    $$

    which rules out distributions that produce values so extreme that a handful of points can dominate the sample.

    Outliers matter to OLS because of the squaring in the least squares criterion from Lecture 5. A point far from the line contributes the square of a large residual to the sum being minimized, so the fitted line rotates toward it. One badly recorded observation, say an hourly wage typed as \$150 instead of \$15, can move the slope on its own. In practice this assumption is a reminder to plot the data and check extreme values before trusting a regression, because many outliers in economic data are entry errors rather than genuine values.

    Like Assumption 2, this assumption mainly supports the standard error of the slope rather than the causal interpretation itself.

    The plot below adds a 41st worker with 19 years of education to the Lecture 5 sample. The slider sets that worker's recorded wage. Near \$31 the new point sits on the line, and the fits with and without the worker agree almost exactly. Drag the wage up to \$150, the kind of value a misplaced decimal produces, and the single orange point pulls the fitted line upward.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    out_wage = mo.ui.slider(
        start=30.0, stop=150.0, step=5.0, value=100.0,
        label="Recorded wage of the unusual worker", show_value=True,
    )
    out_wage
    return (out_wage,)


@app.cell(hide_code=True)
def _(alt, lsa_X, lsa_b0_true, lsa_b1_true, lsa_e, mo, np, out_wage, pd):
    _w = float(out_wage.value)
    _Y = lsa_b0_true + lsa_b1_true * lsa_X + lsa_e
    _b1_base = float(np.cov(lsa_X, _Y, ddof=1)[0, 1] / np.var(lsa_X, ddof=1))
    _b0_base = float(_Y.mean() - _b1_base * lsa_X.mean())

    _Xall = np.append(lsa_X, 19.0)
    _Yall = np.append(_Y, _w)
    _b1_all = float(np.cov(_Xall, _Yall, ddof=1)[0, 1] / np.var(_Xall, ddof=1))
    _b0_all = float(_Yall.mean() - _b1_all * _Xall.mean())

    _xdom = [7.0, 21.0]
    _ydom = [0.0, max(60.0, _w + 10.0)]
    _xline = np.array([7.0, 21.0])
    _pts = pd.DataFrame({"x": lsa_X, "y": _Y})
    _out_pt = pd.DataFrame({"x": [19.0], "y": [_w]})
    _base = pd.DataFrame({"x": _xline, "y": _b0_base + _b1_base * _xline})
    _all = pd.DataFrame({"x": _xline, "y": _b0_all + _b1_all * _xline})

    _scatter = (
        alt.Chart(_pts)
        .mark_circle(color="#1f4e79", opacity=0.7, size=60, clip=True)
        .encode(
            x=alt.X("x:Q", title="Years of education", scale=alt.Scale(domain=_xdom, nice=False)),
            y=alt.Y("y:Q", title="Hourly wage (USD)", scale=alt.Scale(domain=_ydom, nice=False)),
        )
    )
    _outlier = (
        alt.Chart(_out_pt)
        .mark_circle(color="orange", opacity=0.9, size=90, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _base_line = (
        alt.Chart(_base)
        .mark_line(color="#9aa5b1", strokeDash=[4, 3], size=2, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _all_line = (
        alt.Chart(_all)
        .mark_line(color="#1f4e79", size=2.5, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _chart = alt.layer(_scatter, _outlier, _base_line, _all_line).properties(
        width=560, height=340,
        title="One unusual observation can rotate the fitted line",
    )

    _body = (
        rf"Without the unusual worker, the fitted line is "
        rf"$\hat{{Y}} = {_b0_base:.2f} + {_b1_base:.2f}\,X$ (dashed gray). Adding one worker with "
        rf"19 years of education and a recorded wage of \${_w:.0f} moves it to "
        rf"$\hat{{Y}} = {_b0_all:.2f} + {_b1_all:.2f}\,X$ (solid navy). One observation out of 41 "
        rf"moves the slope from {_b1_base:.2f} to {_b1_all:.2f}."
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
            "**Key terms covered:** conditional expectation, causal "
            "interpretation, least squares assumptions for causal inference, "
            "outlier.\n\n"
            "**Key concepts covered:** the conditional expectation as the "
            "population object a regression approximates, the error term as "
            "everything besides X that affects Y, why the mean-zero error "
            "assumption cannot be tested from data alone, how sampling can "
            "fail to be i.i.d., how a single outlier can rotate the OLS line, "
            "and the population regression line as the conditional expectation "
            "of Y given X."
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
