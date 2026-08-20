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

__generated_with = "0.23.16"
app = marimo.App(
    app_title="Lecture 14: Internal and External Validity",
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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Lecture 14</a></h1>'
                '</div>'
            ),
            mo.md("**Internal and External Validity**"),
            mo.nav_menu(
                {
                    "#sec1": "1. What makes a study valid",
                    "#sec2": "2. Threats to internal validity",
                    "#sec3": "3. External validity",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec13NonlinearRegressionInteractionTerms.html" target="_self">← Lecture 13</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec15PanelDataI.html" target="_self">Lecture 15 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 14: Internal and External Validity
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

    [1. What makes a study valid](#sec1)<br>
    [2. Threats to internal validity](#sec2)<br>
    [3. External validity](#sec3)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. What makes a study valid

    Remember that regression models are designed to answer questions. Sometimes we want to estimate a causal effect, such as how an extra year of work experience affects wages. Other times we want to describe an economic relationship or make a prediction. Once we have estimated a regression, we therefore need to ask how well it answers the question we care about. This is the idea of *validity*.

    There are two types of validity. *Internal validity* asks whether the regression gives us the correct answer for the population we studied. For a causal question, this means asking whether $\hat{\beta}_1$ is an unbiased and consistent estimator of the true causal effect $\beta_1$. *External validity* asks whether the result from our sample applies to the population and setting we want to draw conclusions about.

    For instance, continuing our running example from Lectures 11 through 13, *internal validity* asks whether the estimated return to experience captures the causal effect of an extra year of experience for the workers in our sample. *External validity* asks whether that result also applies to the workers we ultimately care about, who may work in a different industry, country, or decade.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Threats to internal validity

    We focus first on internal validity for causal questions. Most problems that prevent a regression from answering a causal question correctly fall into five recurring categories, which we call *threats to internal validity*:

    1. Omitted variable bias
    2. Misspecification of the functional form
    3. Measurement error
    4. Sample selection
    5. Simultaneous causality

    All five threats matter when the question is causal, but not all matter when the question is descriptive. Functional-form misspecification, measurement error, and sample selection can also lead a regression to answer descriptive questions poorly. Omitted variable bias and simultaneous causality matter primarily when we are asking a causal question. We now consider each of the five threats in turn.

    ### <span style="color:#0b68cb">Threat 1: Omitted variable bias</span>

    We first saw *omitted variable bias* in Lecture 8. It occurs when we leave out a variable that affects $Y$ and is correlated with $X$. The omitted variable becomes part of the error term, making $X$ and $u$ correlated. Suppose we regress wages on experience but leave out schooling. Schooling affects wages, so it becomes part of $u$. If experience and schooling are correlated, then $\text{cov}(X,u) \neq 0$, which means $\mathbb{E}[u \mid X] \neq 0$. The first OLS assumption therefore fails, and

    $$
    \hat{\beta}_1 \overset{p}{\to} \underbrace{\beta_1}_{\text{True causal effect}}
    +
    \underbrace{\rho_{Xu}\frac{\sigma_u}{\sigma_X}}_{\text{Bias}}.
    $$

    The sign of the bias depends on $\rho_{Xu}$, so we can often work out whether $\hat{\beta}_1$ is biased upward or downward even if we cannot calculate the bias exactly. Its size also grows with the variation in the error term relative to the variation in $X$.

    **Solutions.** The most direct solution is to control for the omitted variables, as in Lecture 9. If the needed variables are not available, we should acknowledge the likely direction of the bias and explain what it means for our conclusions. Lecture 19 will introduce more advanced ways to address omitted variable bias.

    ### <span style="color:#0b68cb">Threat 2: Misspecification of the functional form</span>

    *Functional form* describes the shape we assume for the relationship between variables. Functional-form *misspecification* occurs when we assume the wrong shape. A common example is assuming a linear relationship when the true relationship curves.

    Suppose the true relationship between $X$ and $Y$ is quadratic,

    $$
    Y = \alpha_0 + \alpha_1 X + \alpha_2 X^2 + \varepsilon
    \qquad\text{with}\qquad
    \mathbb{E}[\varepsilon \mid X] = 0,
    $$

    but we instead estimate the linear regression

    $$
    Y = \beta_0 + \beta_1 X + u.
    $$

    A straight line cannot capture the quadratic relationship at every value of $X$. The part of the relationship that the linear model misses ends up in the error term, so the error varies systematically with $X$. As a result, $\mathbb{E}[u \mid X] \neq 0$. The first OLS assumption therefore fails. In this sense, functional-form misspecification is similar to omitted variable bias. We saw this threat in Lecture 11. When the relationship between wages and experience was curved, a straight line predicted wages that were too high at low and high levels of experience and too low in the middle.

    **Solutions.** Choose a functional form flexible enough to capture the relationship. Polynomials, logarithms, and interaction terms are common ways to do so.

    ### <span style="color:#0b68cb">Threat 3: Bias due to measurement error</span>

    *Measurement error in $X$* occurs when we observe $X$ imprecisely. Data may be entered incorrectly, and self-reports of income, hours worked, or years of experience are often inaccurate. We typically denote the measured value of $X$ by $\widetilde{X}$.

    Suppose the true regression is $Y = \beta_0 + \beta_1 X + u$, but we observe $\widetilde{X}$ rather than the true $X$. Write the measurement error as $\nu$, so that $\widetilde{X} = X + \nu$. Since $X = \widetilde{X} - \nu$, we can rewrite the true regression as $Y = \beta_0 + \beta_1\widetilde{X} + (u-\beta_1\nu)$. Notice that the measurement error has now become part of the regression's error term. If $\widetilde{X}$ is related to this new error term, the first OLS assumption fails and $\hat{\beta}_1$ is inconsistent.<sup><a id="fnref1" href="#fn1">1</a></sup>

    An important special case of measurement error is *classical measurement error*. Here, $\nu$ is purely random and unrelated to both the true $X$ and the original error term $u$. For example, workers might simply misremember their years of experience, with some reporting too much and others too little. Even this purely random error biases $\hat{\beta}_1$. In a simple regression,

    $$
    \hat{\beta}_1 \overset{p}{\to}
    \beta_1
    \frac{\text{var}(X)}
    {\text{var}(X)+\text{var}(\nu)}.
    $$

    Because $\text{var}(X)/[\text{var}(X)+\text{var}(\nu)]$ is less than one, the estimated slope is pulled toward zero. This is called *attenuation bias*, and more measurement error produces more attenuation. The key point is that random measurement error in $X$ does not wash out with more observations. It systematically flattens the estimated relationship, as the appendix proves algebraically.

    The chart below illustrates attenuation bias using a simulated survey of 100 workers whose wages are modeled as $\text{Wage} = 12 + 0.30\cdot\text{Exper} + u$. The navy points show each worker's true experience. The slider adds random reporting error, as if workers misremember how long they have worked, and the orange points show their reported experience, $\widetilde{X}=X+\nu$. As the reporting error grows the estimated regression slope flattens.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # Simulated survey for the attenuation-bias demo: 100 workers, wages linear
    # in true experience with slope 0.30. Wages and true experience are fixed;
    # the reporting error is drawn fresh in the chart cell, seeded by the
    # slider value, so every slider move redraws the noise while the same
    # position always renders the same picture. Fixed seed.
    _rng = np.random.default_rng(117)
    me_n = 100
    me_exper = _rng.uniform(1.0, 40.0, me_n)
    me_wage = 12.0 + 0.30 * me_exper + _rng.normal(0.0, 2.0, me_n)
    return me_exper, me_wage


@app.cell(hide_code=True)
def _(mo):
    me_noise = mo.ui.slider(
        start=0, stop=12, step=1, value=0,
        label="Standard deviation of the reporting error for experience",
        show_value=False,
    )
    mo.vstack(
        [
            me_noise,
        ]
    )
    return (me_noise,)


@app.cell(hide_code=True)
def _(alt, me_exper, me_noise, me_wage, mo, np, pd):
    _sig = float(me_noise.value)
    # A fresh reporting-error draw at each slider position, seeded by the
    # slider value: moving the slider redraws the noise, and returning to a
    # position reproduces its draw. The wages never change.
    _nu_rng = np.random.default_rng(1700 + int(me_noise.value))
    _xt = me_exper + _sig * _nu_rng.standard_normal(len(me_exper))

    # Clean fit on true experience, and the fit the researcher actually gets
    # when only reported experience is available.
    _b1c, _b0c = np.polyfit(me_exper, me_wage, 1)
    _b1n, _b0n = np.polyfit(_xt, me_wage, 1)
    _varx = float(me_exper.var())
    _factor = _varx / (_varx + _sig**2)

    # Fixed axes: the frame must not rescale as the slider moves, or the
    # flattening of the orange line would be visually confounded with the
    # rescaling. The x-domain leaves room for the noisy points to spread.
    _xsc = alt.Scale(domain=[-24.0, 64.0], nice=False)
    _ysc = alt.Scale(domain=[8.0, 28.0], nice=False)

    _layers = []
    if _sig > 0:
        _pts = pd.DataFrame({
            "exper": np.concatenate([me_exper, _xt]),
            "wage": np.concatenate([me_wage, me_wage]),
            "sample": (["Experience measured exactly"] * len(me_exper)
                       + ["Experience reported with error"] * len(_xt)),
        })
    else:
        _pts = pd.DataFrame({
            "exper": me_exper,
            "wage": me_wage,
            "sample": ["Experience measured exactly"] * len(me_exper),
        })
    _layers.append(
        alt.Chart(_pts)
        .mark_circle(size=26, opacity=0.4, clip=True)
        .encode(
            x=alt.X("exper:Q", scale=_xsc, title="Work experience (years)"),
            y=alt.Y("wage:Q", scale=_ysc, title="Hourly wage (dollars)"),
            color=alt.Color(
                "sample:N",
                scale=alt.Scale(
                    domain=["Experience measured exactly",
                            "Experience reported with error"],
                    range=["#1f4e79", "orange"],
                ),
                legend=alt.Legend(title=None, orient="top"),
            ),
        )
    )
    _gx_c = np.linspace(float(me_exper.min()), float(me_exper.max()), 2)
    _layers.append(
        alt.Chart(pd.DataFrame({"exper": _gx_c, "wage": _b0c + _b1c * _gx_c}))
        .mark_line(color="#1f4e79", size=3, clip=True)
        .encode(x=alt.X("exper:Q", scale=_xsc), y=alt.Y("wage:Q", scale=_ysc))
    )
    if _sig > 0:
        _gx_n = np.linspace(float(_xt.min()), float(_xt.max()), 2)
        _layers.append(
            alt.Chart(pd.DataFrame({"exper": _gx_n, "wage": _b0n + _b1n * _gx_n}))
            .mark_line(color="orange", size=3, clip=True)
            .encode(x=alt.X("exper:Q", scale=_xsc), y=alt.Y("wage:Q", scale=_ysc))
        )
    _chart = alt.layer(*_layers).properties(width=560, height=340)

    if _sig == 0:
        _msg = (
            rf"With no reporting error, reported and true experience coincide, and the "
            rf"fitted line on true experience has slope \${_b1c:.2f} per year of "
            rf"experience, close to the true \$0.30. Drag the slider to the right to add "
            rf"random reporting error."
        )
    else:
        _msg = (
            rf"As you move the slider, workers keep the same wages but report their experience with more error. "
            rf"The orange points therefore spread horizontally, flattening the fitted line. "
            rf"The slope falls from \${_b1c:.2f} using true experience to \${_b1n:.2f} using reported experience. "
            rf"The attenuation formula predicts this change: "
            rf"{_varx:.0f}/({_varx:.0f} + {_sig**2:.0f}) = {_factor:.2f}, "
            rf"so {_factor:.2f} × \${_b1c:.2f} = \${_factor * _b1c:.2f}."
        )
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Solutions.** Obtain more accurate data when possible. If that is not possible, acknowledge the likely bias and explain what it means for the study. Measurement error in $Y$ rather than $X$ is much less of an issue for internal validity, as we explain in the appendix.

    ### <span style="color:#0b68cb">Threat 4: Bias due to sample selection</span>

    *Sample selection* occurs when some types of observations are more likely to end up in our sample than others. Whether this biases $\hat{\beta}_1$ depends on what types of observations are missing. There are three main cases of sample selection:

    * **Selection unrelated to $X$ or $Y$.** Suppose some worker surveys are randomly lost in the mail. The workers who remain are no different from those who are missing, so $\hat{\beta}_1$ remains unbiased. We simply have less data, which increases the estimate's standard error.

    * **Selection based on $X$.** Suppose workers with more experience are less likely to answer the survey. We observe fewer highly experienced workers in the sample, but within each level of experience, the workers who respond are no different from those who do not. $\hat{\beta}_1$ therefore remains unbiased, although having less data and less variation in $X$ will generally increase its standard error.

    * **Selection based on $Y$.** Now suppose high-wage workers are more likely to answer the survey. At a given level of experience, the workers who respond are no longer representative of all workers. For example, low-experience workers who make it into the sample will tend to have unusually high wages, and therefore high values of $u$, while high-experience workers need not have high values of $u$. This makes $X$ and $u$ negatively related in the sample, violating $\mathbb{E}[u \mid X] = 0$ and biasing $\hat{\beta}_1$ downward. This is called *sample selection bias*.

    The chart below illustrates these cases using a simulated survey of 400 workers whose wages follow $\text{Wage} = 12 + 0.30\cdot\text{Exper} + u$. Choose a rule for which workers are missing from the sample. The excluded workers fade to gray, while the full-sample line remains for comparison and a new line and confidence band are fit to the workers who remain in the sample.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # Simulated survey for the sample-selection demo: 400 workers, wages linear
    # in experience with slope 0.30. The uniform draw sel_mar is fixed at data
    # time so the "missing at random" rule always drops the same workers.
    # Fixed seed for reproducibility.
    _rng = np.random.default_rng(118)
    sel_n = 400
    sel_exper = _rng.uniform(1.0, 40.0, sel_n)
    sel_wage = 12.0 + 0.30 * sel_exper + _rng.normal(0.0, 3.0, sel_n)
    sel_mar = _rng.random(sel_n)
    return sel_exper, sel_mar, sel_n, sel_wage


@app.cell(hide_code=True)
def _(mo):
    sel_rule = mo.ui.radio(
        options=[
            "Keep the full sample",
            "Data missing at random",
            "Data missing based on X",
            "Data missing based on Y",
        ],
        value="Keep the full sample",
        label="Which data go missing?",
        inline=True,
    )
    sel_rule
    return (sel_rule,)


@app.cell(hide_code=True)
def _(alt, mo, np, pd, sel_exper, sel_mar, sel_n, sel_rule, sel_wage):
    _rule = sel_rule.value

    # The three missing-data rules, each dropping about half the sample. The
    # X rule drops long-career workers; the Y rule drops the high-wage half.
    if _rule == "Data missing at random":
        _keep = sel_mar < 0.5
    elif _rule == "Data missing based on X":
        _keep = sel_exper <= 20.5
    elif _rule == "Data missing based on Y":
        _keep = sel_wage <= np.median(sel_wage)
    else:
        _keep = np.ones(sel_n, dtype=bool)

    def _fit(_x, _y):
        # OLS slope and intercept with the slope's standard error, the R
        # squared, and the pieces needed for the confidence band of the line.
        _b1, _b0 = np.polyfit(_x, _y, 1)
        _res = _y - (_b0 + _b1 * _x)
        _m = len(_x)
        _sig2 = float((_res**2).sum() / (_m - 2))
        _sxx = float(((_x - _x.mean()) ** 2).sum())
        _se1 = float(np.sqrt(_sig2 / _sxx))
        _r2 = 1.0 - float((_res**2).sum()) / float(((_y - _y.mean()) ** 2).sum())
        return float(_b0), float(_b1), _se1, _r2, _sig2, _sxx, float(_x.mean()), _m

    _f = _fit(sel_exper, sel_wage)
    _k = _fit(sel_exper[_keep], sel_wage[_keep])

    def _band_df(_b0, _b1, _sig2, _sxx, _xbar, _m):
        # Pointwise 95 percent confidence band for the regression line.
        _g = np.linspace(1.0, 40.0, 120)
        _se = np.sqrt(_sig2 * (1.0 / _m + (_g - _xbar) ** 2 / _sxx))
        _yhat = _b0 + _b1 * _g
        return pd.DataFrame({
            "exper": _g,
            "lo": _yhat - 1.96 * _se,
            "hi": _yhat + 1.96 * _se,
            "wage": _yhat,
        })

    _xsc = alt.Scale(domain=[0.0, 42.0], nice=False)
    _ysc = alt.Scale(domain=[4.0, 34.0], nice=False)
    _active = _band_df(_k[0], _k[1], _k[4], _k[5], _k[6], _k[7])

    _status = np.where(_keep, "Included in the regression",
                       "Excluded by the missing-data rule")
    _layers = [
        alt.Chart(pd.DataFrame({
            "exper": sel_exper, "wage": sel_wage, "status": _status,
        }))
        .mark_circle(size=18, opacity=0.4, clip=True)
        .encode(
            x=alt.X("exper:Q", scale=_xsc, title="Work experience (years)"),
            y=alt.Y("wage:Q", scale=_ysc, title="Hourly wage (dollars)"),
            color=alt.Color(
                "status:N",
                scale=alt.Scale(
                    domain=["Included in the regression",
                            "Excluded by the missing-data rule"],
                    range=["#1f4e79", "#c3ccd6"],
                ),
                legend=alt.Legend(title=None, orient="top"),
            ),
        )
    ]
    _layers.append(
        alt.Chart(_active)
        .mark_area(color="#1f4e79", opacity=0.18, clip=True)
        .encode(x=alt.X("exper:Q", scale=_xsc),
                y=alt.Y("lo:Q", scale=_ysc), y2="hi:Q")
    )
    if _rule != "Keep the full sample":
        # The full-sample line stays behind, fainter, for comparison.
        _gx = np.linspace(1.0, 40.0, 2)
        _layers.append(
            alt.Chart(pd.DataFrame({"exper": _gx, "wage": _f[0] + _f[1] * _gx}))
            .mark_line(color="#9aa5b1", size=2, strokeDash=[6, 4], clip=True)
            .encode(x=alt.X("exper:Q", scale=_xsc), y=alt.Y("wage:Q", scale=_ysc))
        )
    _layers.append(
        alt.Chart(_active)
        .mark_line(color="#1f4e79", size=3, clip=True)
        .encode(x=alt.X("exper:Q", scale=_xsc), y=alt.Y("wage:Q", scale=_ysc))
    )
    _chart = alt.layer(*_layers).properties(width=560, height=340)

    if _rule == "Keep the full sample":
        _msg = (
            rf"All 400 workers are in the sample. The fitted line has a slope of "
            rf"\${_f[1]:.2f} per year of experience, close to the true \$0.30, "
            rf"with a standard error of {_f[2]:.3f}. Choose a missing-data rule "
            rf"above to drop about half the sample."
        )
    elif _rule == "Data missing at random":
        _msg = (
            rf"About half the surveys are lost for reasons unrelated to the workers, "
            rf"leaving {_k[7]} of 400. The slope barely moves, from \${_f[1]:.2f} to "
            rf"\${_k[1]:.2f}, but its standard error rises from {_f[2]:.3f} to "
            rf"{_k[2]:.3f} and the confidence band widens. Randomly losing observations "
            rf"does not bias the slope; it simply leaves us with less information."
        )
    elif _rule == "Data missing based on X":
        _msg = (
            rf"Workers with more than about 20 years of experience stop answering the "
            rf"survey, leaving {_k[7]} of 400. The slope remains close to the full-sample "
            rf"estimate, at \${_k[1]:.2f} compared with \${_f[1]:.2f}. Its standard "
            rf"error rises from {_f[2]:.3f} to {_k[2]:.3f}, however, because we now "
            rf"have fewer workers and less variation in experience. Selection based "
            rf"only on X does not bias the slope."
        )
    else:
        _msg = (
            rf"The highest-earning half of workers decline to report their wages, "
            rf"leaving {_k[7]} of 400. The slope falls from \${_f[1]:.2f} to "
            rf"\${_k[1]:.2f}. High-experience workers now make it into the sample only "
            rf"when their wages are unusually low for their experience, creating a "
            rf"negative relationship between experience and the error term. The fitted "
            rf"line therefore becomes flatter. This is sample selection bias."
        )
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Solutions.** Improve data collection so that inclusion in the sample no longer depends on the outcome.

    ### <span style="color:#0b68cb">Threat 5: Simultaneous causality bias</span>

    *Simultaneous causality* occurs when $X$ affects $Y$, but $Y$ also affects $X$. The causal relationship therefore runs in both directions:

    $$
    X \longrightarrow Y
    \qquad \text{and} \qquad
    Y \longrightarrow X.
    $$

    Consider a researcher studying the effect of the minimum wage on unemployment. A higher minimum wage may affect unemployment, but unemployment may also influence the minimum wage that states choose. Changes in unemployment that would otherwise be part of the error term can therefore cause changes in $X$, making $X$ and $u$ related. In this case, the first OLS assumption fails, and $\hat{\beta}_1$ is biased.<sup><a id="fnref2" href="#fn2">2</a></sup>

    **Solutions.** Focus on settings where causality runs in only one direction, or use methods that isolate changes in $X$ that are not caused by $Y$. Lectures 18 and 19 will introduce methods to do exactly this.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. External validity

    Suppose a regression is internally valid, so it answers the question we are asking correctly for the *population studied*. External validity asks whether that answer also applies to our *population of interest*, the population we ultimately care about. What this requires depends on whether the question is causal or predictive.

    ### <span style="color:#0b68cb">External validity in causal inference</span>

    For a causal question, external validity comes down to two questions:

    * Who is the population of interest?
    * Should we expect the same causal effect in the population of interest as in the population studied?

    Suppose a study estimates the causal return to experience among manufacturing workers. If we want to know the return to experience among service workers, the estimate applies only if experience affects wages similarly in both populations.

    There are two main ways to assess whether a causal effect applies to our population of interest.

    1. **Introspection.** Compare the population studied with the population of interest. Ask yourself, are the mechanisms generating the causal effect likely to operate similarly in both populations?
    2. **Replication.** Study the same causal question in different populations and compare the estimated effects. If similar studies find similar effects across different populations, we have more reason to believe the causal effect carries over beyond any one of them. For example, one study of the minimum wage in one state tells us little about whether its effect applies elsewhere. Similar estimates across many states and decades provide much stronger evidence that it does.

    Unlike internal validity, external validity cannot usually be established from the study alone. We need to ask how the population of interest differs from the population studied and whether those differences are likely to change the causal effect.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <span style="color:#0b68cb">External validity in prediction</span>

    When we use a regression to predict outcomes from observed $X$s rather than to estimate a causal effect, external validity asks how well those predictions carry over to new observations from the population of interest. This is the idea of out-of-sample prediction from Lecture 5. A model may fit the original sample closely because it captures genuine patterns in the population, but it may also fit randomness that will not appear again in a new sample. If the regression fits too much of this randomness, it will predict new observations poorly.

    We can assess how well the model makes predictions using the same measures of fit introduced in Lecture 5. Recall that the standard error of the regression,

    $$
    \text{SER} = \sqrt{\frac{\text{SSR}}{n-2}}, \quad \text{where } \text{SSR} = \sum_{i=1}^{n} \hat{u}_i^2,
    $$

    measures the typical prediction error in the units of $Y$, while the R-squared,

    $$
    R^2 = \frac{\text{ESS}}{\text{TSS}}
    = \frac{\sum_{i=1}^{n}(\hat{Y}_i-\hat{\mu}_Y)^2}{\sum_{i=1}^{n}(Y_i-\hat{\mu}_Y)^2},
    $$

    measures how much of the variation in $Y$ the predictions explain. To learn about external validity, however, we want to know how these predictions perform on observations that were not used to estimate the model.

    Ideally, we would estimate the model using our sample and then evaluate its predictions using a new sample from the population we care about. When a new sample is not available, we can approximate this exercise by randomly dividing our sample into two groups. We use one group to estimate the model and set the other group aside. We then use the estimated model to predict the outcomes of the observations in the second group. Because those observations were not used to estimate the model, the resulting prediction errors give us a better indication of how well the model will predict new observations from the same population. We call the first group the *training data* and the second group the *hold-out sample*, or *testing data*.

    To evaluate how well a model predicts new observations using a single sample, we can follow these four steps:

    1. Randomly divide the sample into *training data* and a *hold-out sample*, or *testing data*.
    2. Estimate the model using only the training data.
    3. Use the estimated model to predict $Y$ for the observations in the hold-out sample.
    4. Calculate the SER or $R^2$ in the hold-out sample and compare model specifications based on these measures.

    Note, however, that this procedure uses how well the model predicts new observations from the same population as the original sample. It does not tell us whether the model will predict well in a different population, time period, or setting. Answering that broader question requires data from those other settings.

    The chart below applies this procedure to the same 100 workers from Lecture 11, whose wages have a curved relationship with experience. The workers are randomly divided into training data (navy) and a hold-out sample (orange). The degree slider selects the degree of the polynomial regression estimated on the training data, the share slider changes the size of the training sample, and the button creates a new random split between training data and the hold-out sample. The bars report prediction error for the training and hold-out samples separately. In Lecture 11, you compared these polynomial regressions using the adjusted R-squared. Here, we instead compare how well they predict the hold-out sample. A more flexible polynomial may fit the training data better but predict new observations worse.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # The same 100 workers as Lecture 11: identical seed and draw order, so the
    # scatter is literally the same data the polynomial-degree slider fit there.
    # Which workers land in the training set is decided in the chart cell,
    # seeded by the resample button. Fixed seed for reproducibility.
    _rng = np.random.default_rng(116)
    ho_n = 100
    ho_exper = _rng.uniform(1.0, 40.0, ho_n)
    ho_wage = 8.0 + 1.10 * ho_exper - 0.017 * ho_exper**2 + _rng.normal(0.0, 3.0, ho_n)
    return ho_exper, ho_n, ho_wage


@app.cell(hide_code=True)
def _(mo):
    ho_degree = mo.ui.slider(
        start=1, stop=30, step=1, value=1,
        label="Polynomial degree (fitted to training data only)",
        show_value=True,
    )
    ho_share = mo.ui.slider(
        start=10, stop=90, step=5, value=70,
        label="Training share of the sample (%)",
        show_value=True,
    )
    ho_resample = mo.ui.button(
        label="New random split", value=0, on_click=lambda c: c + 1,
    )
    mo.vstack(
        [
            mo.md("Raise the degree and compare the fit on the training workers with the fit on the hold-out workers."),
            mo.hstack([ho_degree, ho_share], justify="start", gap=2),
            ho_resample,
        ]
    )
    return ho_degree, ho_resample, ho_share


@app.cell(hide_code=True)
def _(
    alt,
    ho_degree,
    ho_exper,
    ho_n,
    ho_resample,
    ho_share,
    ho_wage,
    mo,
    np,
    pd,
):
    # Random train/hold-out split, seeded by the resample button so dragging
    # the sliders never reshuffles which workers land in each group.
    _perm = np.random.default_rng(2024 + ho_resample.value).permutation(ho_n)
    _n_tr = int(round(ho_share.value / 100 * ho_n))
    _tr, _te = _perm[:_n_tr], _perm[_n_tr:]
    _xtr, _ytr = ho_exper[_tr], ho_wage[_tr]
    _xte, _yte = ho_exper[_te], ho_wage[_te]

    # A degree-d polynomial needs more than d training points, so the degree
    # is clamped when the training share is small.
    _deg_req = int(ho_degree.value)
    _deg = min(_deg_req, _n_tr - 2)

    # Fit on the training data only, in the Chebyshev basis, which stays well
    # conditioned at high degree where raw powers of experience would not.
    _series = np.polynomial.Chebyshev.fit(_xtr, _ytr, _deg)

    def _ser(_y, _x, _s):
        return float(np.sqrt(((_y - _s(_x)) ** 2).sum() / max(len(_y) - 2, 1)))

    _ser_tr = _ser(_ytr, _xtr, _series)
    _ser_te = _ser(_yte, _xte, _series)
    # Degree-2 benchmark on the same split, for the caption's comparison.
    _ser2_te = _ser(_yte, _xte, np.polynomial.Chebyshev.fit(_xtr, _ytr, 2))

    def _fmt(_v):
        if _v < 100.0:
            return f"${_v:.2f}"
        if _v < 10000.0:
            return f"${_v:,.0f}"
        return "> $10,000"

    _grid = np.linspace(1.0, 40.0, 250)
    _xsc = alt.Scale(domain=[0.0, 42.0], nice=False)
    _ysc = alt.Scale(domain=[0.0, 36.0], nice=False)
    _set = np.empty(ho_n, dtype=object)
    _set[_tr] = "Training (used to fit)"
    _set[_te] = "Hold-out (not used to fit)"
    _pts = pd.DataFrame({"exper": ho_exper, "wage": ho_wage, "set": _set})
    _scatter = (
        alt.Chart(_pts)
        .mark_circle(size=30, opacity=0.5, clip=True)
        .encode(
            x=alt.X("exper:Q", scale=_xsc, title="Work experience (years)"),
            y=alt.Y("wage:Q", scale=_ysc, title="Hourly wage (dollars)"),
            color=alt.Color(
                "set:N",
                scale=alt.Scale(
                    domain=["Training (used to fit)", "Hold-out (not used to fit)"],
                    range=["#1f4e79", "orange"],
                ),
                legend=alt.Legend(title=None, orient="top"),
            ),
        )
    )
    _line = (
        alt.Chart(pd.DataFrame({"exper": _grid, "wage": _series(_grid)}))
        .mark_line(color="#374151", size=3, clip=True)
        .encode(x=alt.X("exper:Q", scale=_xsc), y=alt.Y("wage:Q", scale=_ysc))
    )
    _main = (_scatter + _line).properties(width=460, height=340)

    # SER bars beside the chart. The bar heights are capped so the frame stays
    # fixed when the hold-out SER explodes at high degree; the text labels
    # always report the actual value.
    _cap = 12.0
    _bars_df = pd.DataFrame({
        "group": ["Training", "Hold-out"],
        "ser": [min(_ser_tr, _cap), min(_ser_te, _cap)],
        "label": [_fmt(_ser_tr), _fmt(_ser_te)],
    })
    _bar_x = alt.X(
        "group:N", title=None, sort=["Training", "Hold-out"],
        axis=alt.Axis(labelAngle=-25),
    )
    _bar_y = alt.Y(
        "ser:Q", scale=alt.Scale(domain=[0.0, _cap], nice=False),
        title="SER (dollars)",
    )
    _bars = (
        alt.Chart(_bars_df)
        .mark_bar(clip=True)
        .encode(
            x=_bar_x, y=_bar_y,
            color=alt.Color(
                "group:N",
                scale=alt.Scale(domain=["Training", "Hold-out"],
                                range=["#1f4e79", "orange"]),
                legend=None,
            ),
        )
    )
    _bar_labels = (
        alt.Chart(_bars_df)
        .mark_text(dy=-7, fontSize=11, color="#374151")
        .encode(x=_bar_x, y=_bar_y, text="label:N")
    )
    _chart = alt.hconcat(
        _main, (_bars + _bar_labels).properties(width=110, height=340)
    ).resolve_scale(color="independent")

    # The estimated specification, abbreviated above degree four so the
    # equation line stays short.
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
    _equation = mo.md(r"$$\text{Wage} = " + " + ".join(_terms) + r" + u$$")

    _note = ""
    if _deg < _deg_req:
        _note = (
            f"With only {_n_tr} training workers, the highest degree that can be "
            f"fit is {_n_tr - 2}, so the chart shows degree {_deg}. "
        )
    if _deg == 1:
        _msg = _note + (
            rf"The straight line misses the curvature for both groups: the training SER "
            rf"is {_fmt(_ser_tr)} and the hold-out SER is {_fmt(_ser_te)}. A model this "
            rf"rigid predicts badly everywhere. Raise the degree to 2."
        )
    elif _deg == 2:
        _msg = _note + (
            rf"The quadratic captures the rise and later flattening of wages: the "
            rf"training SER falls to {_fmt(_ser_tr)} and the hold-out SER to "
            rf"{_fmt(_ser_te)}. Press the button a few times: the numbers move with "
            rf"each new split, but the quadratic stays hard to beat out of sample."
        )
    elif _ser_te <= _ser2_te:
        _msg = _note + (
            rf"On this split, degree {_deg} happens to predict the hold-out workers "
            rf"slightly better than the quadratic ({_fmt(_ser_te)} against "
            rf"{_fmt(_ser2_te)}). Press the button a few times: the advantage rarely "
            rf"survives a new split, which is why single-split verdicts should be "
            rf"averaged (see the appendix)."
        )
    else:
        _msg = _note + (
            rf"At degree {_deg}, the training SER has fallen to {_fmt(_ser_tr)}, "
            rf"because adding flexibility can only improve the in-sample fit. The "
            rf"hold-out SER is {_fmt(_ser_te)}, against {_fmt(_ser2_te)} for the "
            rf"quadratic on the same split. The gap between the two bars is "
            rf"overfitting: the model is memorizing noise in the training data, and "
            rf"the noise does not repeat in the hold-out sample."
        )
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_equation, _chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** validity, internal validity, external validity, "
            "functional form, misspecification, measurement error in X, classical "
            "measurement error, attenuation bias, sample selection, sample selection "
            "bias, simultaneous causality, introspection, replication, training data, "
            "hold-out sample, testing data, k-fold cross-validation.\n\n"

            "**Concepts:** the five threats to internal validity and how each can make "
            "X correlated with the error term, the direction of omitted variable bias, "
            "how functional form misspecification, measurement error, sample selection, "
            "and simultaneous causality bias regression estimates, assessing external "
            "validity through introspection and replication, evaluating predictions on "
            "a hold-out sample, and using k-fold cross-validation to compare models "
            "while limiting overfitting."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** The direction of the bias depends on how $X$ is mismeasured. For example, if more experienced workers exaggerate their experience more in a survey, measured experience will rise faster than true experience. A regression of wages on measured experience will then understate how much wages increase with true experience. <a href="#fnref1" title="Back to text">&#8617;</a></span>

    <span id="fn2" style="display:block;font-size:0.9rem;">**2.** The direction of the bias depends on the reverse effect. If higher unemployment leads states to lower their minimum wage, the reverse channel works against the effect of the minimum wage on unemployment and will tend to bias $\hat{\beta}_1$ downward. If higher unemployment instead leads states to raise their minimum wage, the reverse channel works in the same direction and will tend to bias $\hat{\beta}_1$ upward. <a href="#fnref2" title="Back to text">&#8617;</a></span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "## Appendix": mo.md(r"""
        This is bonus material. You will not be tested on the content of the appendix.

        **The algebra of classical measurement error in $X$.** Section 2 stated that classical measurement error shrinks the estimated slope by the factor $\text{var}(X) / (\text{var}(X) + \text{var}(\nu))$. When we use $\widetilde{X}$ in place of $X$, the true population regression $Y = \beta_0 + \beta_1 X + u$ becomes

        $$
        \begin{aligned}
        Y &= \beta_0 + \beta_1 X + u \\
          &= \beta_0 + \beta_1 \widetilde{X} + \beta_1(X - \widetilde{X}) + u \\
          &= \beta_0 + \beta_1 \widetilde{X} + w,
        \end{aligned}
        $$

        where $w = \beta_1(X - \widetilde{X}) + u$. The regression we can actually run uses $\widetilde{X}$, so its error term is $w$, and $w$ contains the measurement gap $X - \widetilde{X}$. If $\text{cov}(\widetilde{X}, w) \neq 0$, then $\mathbb{E}[w \mid \widetilde{X}] \neq 0$ and $\hat{\beta}_1$ is inconsistent.

        Under classical measurement error, $\widetilde{X} = X + \nu$ with $\mathbb{E}[\nu \mid X, u] = 0$. And in large samples,

        $$
        \hat{\beta}_1 \overset{p}{\to} \frac{\text{cov}(\widetilde{X}, Y)}{\text{var}(\widetilde{X})} = \frac{\text{cov}(X + \nu,\ \beta_1 X + u)}{\text{var}(X + \nu)} = \frac{\text{cov}(X, Y)}{\text{var}(X) + \text{var}(\nu)}.
        $$

        The numerator is unchanged, because purely random noise does not covary with $Y$. By contrast, the denominator grows by $\text{var}(\nu)$. And because

        $$
        \left| \frac{\text{cov}(X, Y)}{\text{var}(X) + \text{var}(\nu)} \right| \leq \left| \frac{\text{cov}(X, Y)}{\text{var}(X)} \right|,
        $$

        we must have $|\hat{\beta}_1| < |\beta_1|$, which is the attenuation result the slider in Section 2 demonstrates.

        **Measurement error in $Y$.** Section 2 showed that classical measurement error in $X$ produces attenuation bias. Classical measurement error in $Y$ is less of an issue for estimation. Suppose the true model is $Y = \beta_0 + \beta_1 X + u$, but we observe $\widetilde{Y} = Y + v$ with $\mathbb{E}[v \mid X, u] = 0$. In large samples,

        $$
        \hat{\beta}_1 \overset{p}{\to} \frac{\text{cov}(X, \widetilde{Y})}{\text{var}(X)} = \frac{\text{cov}(X,\ \beta_1 X + u + v)}{\text{var}(X)} = \frac{\text{cov}(X, Y)}{\text{var}(X)} = \beta_1,
        $$

        where the second-to-last equality follows from $\mathbb{E}[v \mid X, u] = 0$; that is, the noise in $Y$ is unrelated to $X$, so it contributes nothing to the covariance in the numerator. The slope estimator is therefore still consistent.

        However, because $\text{var}(\widetilde{Y}) > \text{var}(Y)$, there is more unexplained variation around the fitted line, so the coefficients' standard errors increase and the $R^2$ falls. While the slope is unbiased when there is measurement error in $Y$, the model is less informative.

        **$k$-fold cross-validation.** Section 3 evaluated each polynomial using a single random split between training data and a hold-out sample. But the results can depend on which observations happen to fall into each group. A different split can therefore make the same model look better or worse. $k$-fold cross-validation reduces this problem by evaluating the model on several different parts of the sample.

        The procedure works as follows.

        1. Divide the sample into $k$ groups, called *folds*, of roughly equal size. Common choices are $k = 5$ and $k = 10$.
        2. Set the first fold aside, estimate the model using the other $k-1$ folds, and measure how well it predicts the observations in the first fold using the SER.
        3. Repeat this process until each fold has been set aside once. Each observation is therefore used for estimation in $k-1$ rounds and for testing in one round.
        4. Average the $k$ test SERs. This gives the model's *cross-validated SER*.
        5. Repeat the procedure for each candidate specification, such as each polynomial degree, and choose the specification with the lowest cross-validated SER. Then estimate that specification on the full sample to obtain the final coefficients.

        The advantage over a single training and hold-out split is that the result no longer depends on one particular group of observations being set aside. Every observation gets one turn being predicted by a model that was estimated without it, and the cross-validated SER summarizes prediction error across the full sample.
        """),
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec13NonlinearRegressionInteractionTerms.html" target="_self">← Lecture 13</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec15PanelDataI.html" target="_self">Lecture 15 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
