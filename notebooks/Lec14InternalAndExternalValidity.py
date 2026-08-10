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

__generated_with = "0.23.14"
__preliminary__ = True
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
            "**Terms:** validity, internal validity, external validity, "
            mo.md("# [Lecture 14](#top)"),
            mo.md("Internal and External Validity"),
            mo.nav_menu(
                {
                    "#sec1": "1. What makes a study valid",
            "**Concepts:** the five threats to internal validity and why "
                    "#sec3": "3. External validity in causal inference",
                    "#sec4": "4. External validity in prediction",
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
    [3. External validity in causal inference](#sec3)<br>
    [4. External validity in prediction](#sec4)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. What makes a study valid

    We say a study is *valid* if it is useful for answering the question it set out to answer. Validity has two parts, and they can fail independently. *Internal validity* asks whether the study correctly estimates the causal effect of $X$ on $Y$ within the population studied: in the language of Lecture 6, whether $\hat{\beta}_1$ is an unbiased and consistent estimator of the true causal value $\beta_1$. *External validity* asks whether the findings generalize to other populations and settings. It is about how far the estimate travels rather than about bias, and a study can be useful for prediction even when its $\hat{\beta}_1$ is not an unbiased estimate of a causal effect.

    Our survey of workers from Lectures 11 through 13 makes the distinction concrete. Internal validity asks whether the estimated return to experience measures what an additional year of experience causes wages to be among workers like those surveyed. External validity asks whether that estimate tells us anything about workers in a different industry, country, or decade. Section 2 works through the five ways internal validity fails; Sections 3 and 4 turn to external validity, first for causal questions and then for prediction.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Threats to internal validity

    Five threats account for most internal-validity failures in regression studies:

    1. Omitted variable bias
    2. Misspecification of the functional form
    3. Bias due to measurement error
    4. Bias due to sample selection
    5. Simultaneous causality bias

    Each threat, in its own way, breaks the first causal-inference assumption from Lecture 6, $\mathbb{E}[u \mid X_1, \dots, X_k] = 0$ (or, with control variables, its conditional mean independence version from Lecture 9), so $\hat{\beta}_1$ no longer centers on the causal effect. We take the five threats one at a time.

    ### <span style="color:#0b68cb">Threat 1: Omitted variable bias</span>

    Lecture 8 introduced omitted variable bias: a variable that affects $Y$ and is correlated with $X$ is left out of the regression, so its influence ends up inside the error term. Suppose we regress wages on experience but leave out schooling. Workers with more schooling earn higher wages at every level of experience, so schooling sits inside $u$, and if experience and schooling are correlated, then $\text{cov}(X, u) \neq 0$. Whenever $\text{cov}(X, u) \neq 0$, we also have $\mathbb{E}[u \mid X] \neq 0$, so the first causal-inference assumption fails and

    $$
    \hat{\beta}_1 \overset{p}{\to} \underbrace{\beta_1}_{\text{True causal effect}} + \underbrace{\rho_{Xu} \cdot \frac{\sigma_u}{\sigma_X}}_{\text{Bias term}}.
    $$

    The bias term is worth reading closely. Its sign comes from $\rho_{Xu}$, the correlation between the independent variable and the error term, so you can often reason out the direction of the bias even without data. Its size grows with the standard deviation of the error relative to the standard deviation of $X$.

    **Solutions.** Include the variables that would otherwise generate the bias as controls, as in Lecture 9. When the needed control is not available in the data, the honest fallback is to acknowledge the likely direction of the bias and discuss what it means for the study's conclusion.

    ### <span style="color:#0b68cb">Threat 2: Misspecification of the functional form</span>

    *Functional form* is the shape you assume for the relationship between variables. Functional-form *misspecification* arises when you assume the wrong shape. A common example is assuming a linear relationship when the true relationship curves.

    Suppose the true relationship is quadratic,

    $$
    Y = \alpha_0 + \alpha_1 X + \alpha_2 X^2 + \varepsilon,
    \qquad
    \mathbb{E}[\varepsilon \mid X] = 0,
    $$

    but you instead specify the linear regression

    $$
    Y = \beta_0 + \beta_1 X + u.
    $$

    A straight line cannot capture the quadratic relationship at every value of $X$. The error term therefore varies systematically with $X$, so

    $$
    \mathbb{E}[u \mid X] \neq 0.
    $$

    Functional-form misspecification therefore violates the zero-conditional-mean assumption. It is similar to omitted-variable bias because the linear model leaves out the relevant term $X^2$.

    We saw this failure in Lecture 11. A straight line fit to the curved relationship between wages and experience predicted wages that were too high at low and high levels of experience and too low in the middle.

    **Solution.** Choose a specification flexible enough to capture the relationship. Polynomials, logarithms, and interaction terms provide common ways to do so.

    ### <span style="color:#0b68cb">Threat 3: Bias due to measurement error</span>

    *Measurement error in $X$* occurs when the true value of $X$ is measured imprecisely. Data can be entered incorrectly into a database, and self-reports of income, hours worked, or years of experience are often inaccurate. We denote the imprecisely measured value of $X$ as $\widetilde{X}$.

    When we use $\widetilde{X}$ in place of $X$, the gap between the true value and the reported value becomes part of the regression's error term. If that gap is related to $\widetilde{X}$, the first causal-inference assumption fails and $\hat{\beta}_1$ is inconsistent.

    The most important special case has a name. *Classical measurement error* means $\widetilde{X}$ equals $X$ plus a purely random component $\nu$, so $\widetilde{X} = X + \nu$. The reporting error is unrelated to the truth, like a worker misremembering their years of experience with no particular tilt up or down. Even this best case biases the slope. The noise adds variation to the regressor without adding any relationship with $Y$, and in large samples the estimated slope shrinks by the factor $\text{var}(X) / (\text{var}(X) + \text{var}(\nu))$, so that $|\hat{\beta}_1| < |\beta_1|$: the estimated slope is always dragged toward zero. This is called *attenuation bias*, and it is a common problem in observational studies. Note what it rules out: random noise in $X$ does not average away. It systematically flattens the estimated relationship. The appendix works through the algebra behind the shrinkage factor.

    The chart below re-creates this result with a simulated survey of 100 workers whose wages follow the true relationship $\text{Wage} = 12 + 0.30 \cdot \text{Exper} + u$. The navy points plot each worker at their true experience. The slider adds random reporting error to experience, as if the workers misremember how long they have worked, and the orange points plot the same workers at their reported experience $\widetilde{X} = X + \nu$. Watch what the noise does to the orange fitted line.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # Simulated survey for the attenuation-bias demo: 100 workers, wages linear
    # in true experience with slope 0.30. The reporting error is a fixed
    # standard-normal draw scaled by the slider, so dragging the slider never
    # resamples; it only stretches the same noise realization. Fixed seed.
    _rng = np.random.default_rng(117)
    me_n = 100
    me_exper = _rng.uniform(1.0, 40.0, me_n)
    me_wage = 12.0 + 0.30 * me_exper + _rng.normal(0.0, 2.0, me_n)
    me_base = _rng.standard_normal(me_n)
    return me_base, me_exper, me_n, me_wage


@app.cell(hide_code=True)
def _(mo):
    me_noise = mo.ui.slider(
        start=0, stop=12, step=1, value=0,
        label="Standard deviation of the reporting error (years)",
        show_value=True,
    )
    mo.vstack(
        [
            mo.md("Increase the size of the reporting error and watch the fitted slope on reported experience."),
            me_noise,
        ]
    )
    return (me_noise,)


@app.cell(hide_code=True)
def _(alt, me_base, me_exper, me_noise, me_wage, mo, np, pd):
    _sig = float(me_noise.value)
    _xt = me_exper + _sig * me_base

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
            rf"reporting error."
        )
    else:
        _msg = (
            rf"The same workers, the same wages. Only the recorded experience values have "
            rf"changed: the orange points are the navy points pushed sideways by the "
            rf"reporting error. The fit on true experience still has slope \${_b1c:.2f}, "
            rf"but the fit on reported experience has slope \${_b1n:.2f}. The shrinkage "
            rf"factor predicts this: var(X)/(var(X) + var(ν)) = "
            rf"{_varx:.0f}/({_varx:.0f} + {_sig**2:.0f}) = {_factor:.2f}, and "
            rf"{_factor:.2f} × \${_b1c:.2f} = \${_factor * _b1c:.2f}. The noise spreads "
            rf"the points horizontally without changing their wages, so the cloud gets "
            rf"wider but no steeper, and the fitted line tilts toward flat."
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
    **Solutions.** Obtain more accurate data when possible. When it is not, acknowledge the likely attenuation and discuss what it means for the study, or turn to more advanced econometric methods designed for mismeasured regressors. Measurement error in $Y$ rather than in $X$ turns out to be far less damaging; the appendix works through why.

    ### <span style="color:#0b68cb">Threat 4: Bias due to sample selection</span>

    *Sample selection* occurs when the sampling procedure influences which observations end up in the data. Whether selection biases $\hat{\beta}_1$ depends entirely on what the availability of data is related to.

    - **Data missing at random.** Some surveys are lost in transit, unrelated to anything about the workers. $\hat{\beta}_1$ is not biased; the only cost is a smaller sample, so the standard error $\sigma_{\hat{\beta}_1}$ increases.
    - **Data missing based on $X$.** Suppose workers with long careers rarely answer the survey. $\hat{\beta}_1$ is still not biased, but the standard error increases and the $R^2$ falls: with less variation in $X$ in the sample, the regression can explain less of the variation in $Y$.
    - **Data missing based on $Y$.** This is the damaging case, called *sample selection bias*: $\hat{\beta}_1$ becomes biased. Consider collecting national election data from only urban areas. Which observations are available now depends on the outcome being studied, and the fitted relationship inside the sample no longer matches the relationship in the population.

    If the missing data depend on both $X$ and $Y$, the bias can go in either direction.

    The chart below lets you watch each rule act on the same data. It shows a large simulated survey of 400 workers whose wages follow the true relationship $\text{Wage} = 12 + 0.30 \cdot \text{Exper} + u$, together with the fitted OLS line and its 95 percent confidence band. Choose a rule for which data go missing: the excluded workers fade to gray, the full-sample line stays behind for comparison, and a new line and band are fit to the workers who remain.
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
            rf"All 400 workers are in the sample. The fitted line has slope "
            rf"\${_f[1]:.2f} per year of experience (standard error {_f[2]:.3f}), close "
            rf"to the true \$0.30, with an R-squared of {_f[3]:.2f}. Choose a "
            rf"missing-data rule above to drop about half the sample."
        )
    elif _rule == "Data missing at random":
        _msg = (
            rf"About half the surveys are lost for reasons unrelated to the workers, "
            rf"leaving {_k[7]} of 400. The slope barely moves, from \${_f[1]:.2f} to "
            rf"\${_k[1]:.2f}, but its standard error rises from {_f[2]:.3f} to "
            rf"{_k[2]:.3f} and the confidence band widens. The estimate is still "
            rf"unbiased; it is just measured less precisely."
        )
    elif _rule == "Data missing based on X":
        _msg = (
            rf"Long-career workers stop answering the survey: everyone with more than "
            rf"about 20 years of experience is missing, leaving {_k[7]} of 400. The "
            rf"slope is still \${_k[1]:.2f}, against \${_f[1]:.2f} in the full sample, "
            rf"but the standard error jumps from {_f[2]:.3f} to {_k[2]:.3f} and the "
            rf"R-squared falls from {_f[3]:.2f} to {_k[3]:.2f}. With less variation in "
            rf"experience, the regression explains less variation in wages, and the "
            rf"band fans out over the empty half of the chart."
        )
    else:
        _msg = (
            rf"The highest-earning half of the workers decline to report their wages, "
            rf"leaving {_k[7]} of 400. Now the availability of data depends on the "
            rf"outcome itself, and the slope collapses from \${_f[1]:.2f} to "
            rf"\${_k[1]:.2f}: at every experience level, the workers who remain are the "
            rf"ones who happened to earn little, so the line tilts toward flat. This is "
            rf"sample selection bias, and no amount of extra data of the same kind "
            rf"fixes it."
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
    **Solutions.** Improve the data collection so availability no longer depends on the outcome, or control for the selection criteria directly, for example by including an indicator for rural versus urban counties.

    ### <span style="color:#0b68cb">Threat 5: Simultaneous causality bias</span>

    *Simultaneous causality* occurs when $X$ affects $Y$ and $Y$ also affects $X$, so the causal arrow runs in both directions at once:

    $$
    X \longrightarrow Y \qquad \text{and} \qquad Y \longrightarrow X.
    $$

    Consider a researcher examining the effect of the minimum wage on unemployment. A higher minimum wage may increase unemployment. But states with higher unemployment may respond by lowering their minimum wage. The regression of unemployment on the minimum wage cannot tell these channels apart, so $\hat{\beta}_1$ picks up the causal effects from both directions. If the two channels counteract each other, $\hat{\beta}_1$ is likely an underestimate of the effect of the minimum wage; if they reinforce each other, it is likely an overestimate.

    **Solutions.** Focus on settings where the relationship runs in only one direction, or use more advanced econometric methods built for two-way causation. The experiments and quasi-experiments of Lectures 18 and 19 are designed to shut down the reverse channel by construction.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. External validity in causal inference

    Suppose a study clears every threat in Section 2, so its $\hat{\beta}_1$ is a credible estimate of the causal effect in the population studied. External validity asks a different question: does that estimate apply beyond the study?

    For a causal question, this comes down to two things:

    - Who is the intended population of interest?
    - Should we expect the same causal relationship in the population of interest as in the population studied?

    Suppose our survey estimates the causal return to experience among manufacturing workers. If the population of interest is service workers, the estimate travels only if experience builds wages the same way in both settings, which is far from guaranteed.

    Two tools help evaluate external validity for causal questions.

    1. *Introspection*: think carefully about the similarities and differences between the population studied and the population of interest. Do the mechanisms that generate the causal effect operate the same way in both?
    2. *Replication*: when multiple studies ask the same causal question in different populations, external validity improves if they find similar results. One study of the minimum wage in one state is suggestive; twenty studies across different states and decades that agree are far more persuasive.

    Neither tool is a formula. External validity for causal questions is ultimately an argument, and the argument has to be made case by case.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. External validity in prediction

    When the goal is prediction or forecasting rather than causal inference, external validity has a sharper meaning: how well does the fitted model predict variation in other samples from the population of interest? This is the out-of-sample prediction idea from Lecture 5, now promoted to the main criterion of success.

    The two measures of fit from Lecture 5 do the assessing. The standard error of the regression,

    $$
    \text{SER} = \sqrt{\frac{\text{SSR}}{n-2}}, \quad \text{where } \text{SSR} = \sum_{i=1}^{n} \hat{u}_i^2,
    $$

    reports the typical prediction miss in the units of $Y$, and the R-squared,

    $$
    R^2 = \frac{\text{ESS}}{\text{TSS}} = \frac{\sum_{i=1}^{n}(\hat{Y}_i - \hat{\mu}_Y)^2}{\sum_{i=1}^{n}(Y_i - \hat{\mu}_Y)^2},
    $$

    reports the share of the variation in $Y$ the predictions account for. The key move is where they are computed: on a sample from the population of interest, using the $\hat{\beta}$s estimated from the population studied. A model that fits its own sample well but predicts a new sample badly has low external validity for prediction, however good its in-sample fit looks.

    You do not need to wait for a second dataset to run this check. Your current sample can play both roles:

    1. Estimate the model on a sub-sample of your data, called the *training data*.
    2. Predict $Y$ given the $X$s on the *hold-out sample*, also called the *testing data*: the part of the sample the model was not trained on.
    3. Measure how well the predictions do on the hold-out sample, using the SER or the $R^2$.
    4. Repeat with new model specifications until the hold-out SER is as small as you can make it.

    The chart below runs this procedure on the same 100 workers from Lecture 11, whose wages follow a curved relationship with experience. The workers are split at random into training data (navy) and a hold-out sample (orange). The degree slider sets the polynomial fitted to the training data only, the share slider sets how much of the sample is used for training, and the button re-draws the random split. The two bars beside the chart report the SER separately for the training and the hold-out workers. In Lecture 11 you judged these polynomials by the adjusted R-squared; now the hold-out sample delivers the verdict directly.
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
def _(alt, ho_degree, ho_exper, ho_n, ho_resample, ho_share, ho_wage, mo, np, pd):
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
    mo.md(r"""
    A single split is the simplest version of this check, and it leaves the verdict partly to luck: press the resample button above and the two SER bars shift with every new split. *Model evaluation algorithms* refine the idea by averaging the check over many splits. The most common one, *$k$-fold cross-validation*, is described in detail in the appendix.

    This closes the validity checklist. Internal validity asks whether a study's estimate means what it claims within the population studied, and Section 2's five threats are the ways it can fail. External validity asks how far the estimate travels, by argument and replication for causal questions, and by out-of-sample performance for prediction. Lecture 15 turns to panel data, the first of several tools that remove an internal-validity threat rather than just naming it: following the same entities over time makes it possible to cancel out omitted variables that stay fixed within each entity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** validity, internal validity, external validity, "
            "functional form, misspecification, measurement error in X, classical "
            "measurement error, attenuation bias, sample selection, sample selection "
            "bias, simultaneous causality, introspection, replication, training data, "
            "hold-out sample, testing data, model evaluation algorithm, k-fold "
            "cross-validation.\n\n"
            "**Concepts:** the five threats to internal validity and why "
            "every one of them violates the first causal-inference assumption, reading "
            "the sign and size of the omitted variable bias term, how fitting the wrong "
            "shape puts the leftover curvature into the error term, why purely random "
            "noise in X does not average away but drags the estimated slope toward zero, "
            "why bias from missing data depends on whether availability is related to Y "
            "rather than to X, how two-way causation mixes both causal directions into "
            "one estimated slope, evaluating external validity for causal questions by "
            "introspection and replication, judging predictive models by out-of-sample "
            "fit on a hold-out sample, and overfitting as the gap between training and "
            "hold-out performance that k-fold cross-validation is built to detect."
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

        **The algebra of classical measurement error in $X$.** Section 2 stated that classical measurement error shrinks the estimated slope by the factor $\text{var}(X) / (\text{var}(X) + \text{var}(\nu))$. Here is the derivation. When we use $\widetilde{X}$ in place of $X$, the true population regression $Y = \beta_0 + \beta_1 X + u$ becomes

        $$
        \begin{aligned}
        Y &= \beta_0 + \beta_1 X + u \\
          &= \beta_0 + \beta_1 \widetilde{X} + \beta_1(X - \widetilde{X}) + u \\
          &= \beta_0 + \beta_1 \widetilde{X} + w,
        \end{aligned}
        $$

        where $w = \beta_1(X - \widetilde{X}) + u$. The regression we can actually run uses $\widetilde{X}$, so its error term is $w$, and $w$ contains the measurement gap $X - \widetilde{X}$. If $\text{cov}(\widetilde{X}, w) \neq 0$, then $\mathbb{E}[w \mid \widetilde{X}] \neq 0$ and $\hat{\beta}_1$ is inconsistent.

        Under classical measurement error, $\widetilde{X} = X + \nu$ with $\mathbb{E}[\nu \mid X, u] = 0$, and we can compute exactly where the slope estimator settles. In large samples,

        $$
        \hat{\beta}_1 \overset{p}{\to} \frac{\text{cov}(\widetilde{X}, Y)}{\text{var}(\widetilde{X})} = \frac{\text{cov}(X + \nu,\ \beta_1 X + u)}{\text{var}(X + \nu)} = \frac{\text{cov}(X, Y)}{\text{var}(X) + \text{var}(\nu)}.
        $$

        The numerator is unchanged, because purely random noise does not covary with $Y$. The denominator grows by $\text{var}(\nu)$. Because

        $$
        \left| \frac{\text{cov}(X, Y)}{\text{var}(X) + \text{var}(\nu)} \right| \leq \left| \frac{\text{cov}(X, Y)}{\text{var}(X)} \right|,
        $$

        we must have $|\hat{\beta}_1| < |\beta_1|$, which is the attenuation result the slider in Section 2 demonstrates.

        **Measurement error in $Y$.** Section 2 showed that classical measurement error in $X$ produces attenuation bias. Classical measurement error in $Y$ is far more forgiving. Suppose the true model is $Y = \beta_0 + \beta_1 X + u$, but we observe $\widetilde{Y} = Y + v$ with $\mathbb{E}[v \mid X, u] = 0$. In large samples,

        $$
        \hat{\beta}_1 \overset{p}{\to} \frac{\text{cov}(X, \widetilde{Y})}{\text{var}(X)} = \frac{\text{cov}(X,\ \beta_1 X + u + v)}{\text{var}(X)} = \frac{\text{cov}(X, Y)}{\text{var}(X)} = \beta_1,
        $$

        where the second-to-last equality follows from $\mathbb{E}[v \mid X, u] = 0$: the noise in $Y$ is unrelated to $X$, so it contributes nothing to the covariance in the numerator. The slope estimator is therefore still consistent.

        The noise is not free, however. Because $\text{var}(\widetilde{Y}) > \text{var}(Y)$, there is more unexplained variation around the fitted line, so the standard errors increase and the $R^2$ falls. Noise in the outcome costs precision; noise in the regressor costs consistency. That asymmetry is why Section 2's checklist worries about measurement error in $X$.

        **$k$-fold cross-validation.** Section 4 judged each polynomial by a single split into training and hold-out data, and the resample button showed the weakness of that verdict: it depends on the split. An unlucky hold-out sample can make a good model look bad, and a lucky one can excuse an overfit model. $k$-fold cross-validation replaces the single split with an average over many. The procedure:

        1. Split the sample into $k$ folds (sub-samples) of roughly equal size. Common choices are $k = 5$ and $k = 10$.
        2. Set fold 1 aside as the test data, estimate the model on the other $k - 1$ folds combined, and record the SER (or the $R^2$) of its predictions on fold 1.
        3. Repeat until each fold has taken exactly one turn as the test data. Every observation is used for estimation in $k - 1$ rounds and for testing in one round, and never for both at once.
        4. Average the $k$ test SERs. This average, the cross-validated SER, is the model's score.
        5. Compute the score for every candidate specification, for example each polynomial degree, and pick the specification with the lowest score. Then re-estimate that specification on the full sample to get the final coefficients.

        The averaging is what the single split lacks. Each observation gets one turn at being predicted by a model that never saw it, so the score reflects the whole sample rather than one arbitrary cut, and the verdict stops bouncing around the way the SER bars in Section 4 do. The overfitting logic is unchanged: the in-sample SER always falls as the model grows more flexible, while the cross-validated SER falls and then rises, and its minimum marks where flexibility stops paying for itself. Taking $k$ all the way to $n$ gives leave-one-out cross-validation, in which each single observation takes a turn as the test set. That is the most thorough version, at the cost of estimating the model $n$ times.
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
