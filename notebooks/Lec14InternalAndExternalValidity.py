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
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: block; margin-bottom: 1.5em;">Course home</a>'),
            mo.md("# [Lecture 14](#top)"),
            mo.md("Internal and External Validity"),
            mo.nav_menu(
                {
                    "#sec1": "1. What makes a study valid",
                    "#sec2": "2. Threats to internal validity",
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

    Lectures 5 through 13 built a complete regression toolkit. We can now fit lines and curves, add control variables, and attach standard errors and hypothesis tests to any coefficient. This lecture steps back and asks when the numbers that toolkit produces should be believed, and for whom.

    We say a study is *valid* if it is useful for answering the question it set out to answer. Validity has two parts, and the two parts can fail independently.

    *Internal validity* asks whether the study correctly estimates the causal effect of $X$ on $Y$ within the population studied. It is a question about causality. In the language of Lecture 6, it asks whether $\hat{\beta}_1$ is an unbiased and consistent estimator of the true causal value $\beta_1$.

    *External validity* asks whether we can generalize the findings to other populations and settings. It is typically a question about how far the estimate travels rather than about bias, and a study can be externally useful for prediction even when its $\hat{\beta}_1$ is not an unbiased estimate of a causal effect.

    Our survey of workers from Lectures 11 through 13 makes the distinction concrete. Internal validity asks whether the estimated return to experience measures what an additional year of experience causes wages to be among workers like those surveyed. External validity asks whether that estimate tells us anything about workers in a different industry, country, or decade.

    Section 2 works through the five ways internal validity fails. Sections 3 and 4 turn to external validity, first for causal questions and then for prediction.
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

    The list is worth committing to memory. When you read an empirical study, these five items are the checklist to run through before believing a causal claim. Each threat, in its own way, breaks the first causal-inference assumption from Lecture 6,

    $$
    \mathbb{E}[u \mid X_1, \dots, X_k] = 0,
    $$

    or, when the regression includes control variables $W_1, \dots, W_r$, the conditional mean independence version from Lecture 9,

    $$
    \mathbb{E}[u \mid X_1, \dots, X_k, W_1, \dots, W_r] = \mathbb{E}[u \mid W_1, \dots, W_r].
    $$

    When either version fails, the error term contains something that moves with the independent variables, and $\hat{\beta}_1$ no longer centers on the causal effect. The rest of this section takes the five threats one at a time.

    ### <span style="color:#0b68cb">Threat 1: Omitted variable bias</span>

    Lecture 8 introduced omitted variable bias: a variable that affects $Y$ and is correlated with $X$ is left out of the regression, so its influence ends up inside the error term. Suppose we regress wages on experience but leave out schooling. Workers with more schooling earn higher wages at every level of experience, so schooling sits inside $u$, and if experience and schooling are correlated, then $\text{cov}(X, u) \neq 0$. Whenever $\text{cov}(X, u) \neq 0$, we also have $\mathbb{E}[u \mid X] \neq 0$, so the first causal-inference assumption fails and

    $$
    \hat{\beta}_1 \overset{p}{\to} \underbrace{\beta_1}_{\text{True causal effect}} + \underbrace{\rho_{Xu} \cdot \frac{\sigma_u}{\sigma_X}}_{\text{Bias term}}.
    $$

    The bias term is worth reading closely. Its sign comes from $\rho_{Xu}$, the correlation between the independent variable and the error term, so you can often reason out the direction of the bias even without data. Its size grows with the standard deviation of the error relative to the standard deviation of $X$.

    **Solutions.** Include the variables that would otherwise generate the bias as controls, as in Lecture 9. When the needed control is not available in the data, the honest fallback is to acknowledge the likely direction of the bias and discuss what it means for the study's conclusion.

    ### <span style="color:#0b68cb">Threat 2: Misspecification of the functional form</span>

    *Functional form* is the shape you assume for the relationship between variables. Functional form *misspecification* arises when you assume the wrong shape. The most common version is assuming a linear relationship between $Y$ and $X$ when the true relationship curves.

    Suppose the true relationship between $X$ and $Y$ is quadratic,

    $$
    Y = \alpha_0 + \alpha_1 X + \alpha_2 X^2 + \varepsilon, \quad \text{where } X > 0,
    $$

    but you instead estimate

    $$
    Y = \beta_0 + \beta_1 X + u.
    $$

    The error term of the estimated regression then contains everything the straight line leaves out: $u = \alpha_2 X^2 + \varepsilon$. Because $X^2$ moves with $X$, we get $\text{cov}(X, u) = \text{cov}(X, \alpha_2 X^2 + \varepsilon) \neq 0$, which implies $\mathbb{E}[u \mid X] \neq 0$. Assuming the wrong shape therefore violates the first causal-inference assumption in exactly the same way an omitted variable does. The omitted variable here is $X^2$ itself.

    We saw this failure in pictures in Lecture 11. The straight line fit to the curved wage and experience data predicted wages that were too high at low and high levels of experience and too low in the middle.

    **Solution.** Use a specification flexible enough to match the shape of the relationship. Polynomials (Lecture 11), logarithms (Lecture 12), and interaction terms (Lecture 13) are the toolkit for exactly this problem.

    ### <span style="color:#0b68cb">Threat 3: Bias due to measurement error</span>

    *Measurement error in $X$* occurs when the true value of $X$ is measured imprecisely. Data can be entered incorrectly into a database, and self-reports of income, hours worked, or years of experience are often inaccurate. We denote the imprecisely measured value of $X$ as $\widetilde{X}$.

    When we use $\widetilde{X}$ in place of $X$, the true population regression $Y = \beta_0 + \beta_1 X + u$ becomes

    $$
    \begin{aligned}
    Y &= \beta_0 + \beta_1 X + u \\
      &= \beta_0 + \beta_1 \widetilde{X} + \beta_1(X - \widetilde{X}) + u \\
      &= \beta_0 + \beta_1 \widetilde{X} + w,
    \end{aligned}
    $$

    where $w = \beta_1(X - \widetilde{X}) + u$. The regression we can actually run uses $\widetilde{X}$, so its error term is $w$, and $w$ contains the measurement gap $X - \widetilde{X}$. If $\text{cov}(\widetilde{X}, w) \neq 0$, then $\mathbb{E}[w \mid \widetilde{X}] \neq 0$ and $\hat{\beta}_1$ is inconsistent.

    The most important special case has a name. *Classical measurement error* means $\widetilde{X}$ equals $X$ plus a purely random component $\nu$, so $\widetilde{X} = X + \nu$ with $\mathbb{E}[\nu \mid X, u] = 0$. The reporting error is unrelated to the truth, like a worker misremembering their years of experience with no particular tilt up or down. Even this best case biases the slope. In large samples,

    $$
    \hat{\beta}_1 \overset{p}{\to} \frac{\text{cov}(\widetilde{X}, Y)}{\text{var}(\widetilde{X})} = \frac{\text{cov}(X + \nu,\ \beta_1 X + u)}{\text{var}(X + \nu)} = \frac{\text{cov}(X, Y)}{\text{var}(X) + \text{var}(\nu)}.
    $$

    The numerator is unchanged, because purely random noise does not covary with $Y$. The denominator grows by $\text{var}(\nu)$. Because

    $$
    \left| \frac{\text{cov}(X, Y)}{\text{var}(X) + \text{var}(\nu)} \right| \leq \left| \frac{\text{cov}(X, Y)}{\text{var}(X)} \right|,
    $$

    we must have $|\hat{\beta}_1| < |\beta_1|$: the estimated slope is always dragged toward zero. This is called *attenuation bias*, and it is a common problem in observational studies. Note what it rules out: random noise in $X$ does not average away. It systematically flattens the estimated relationship.

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
            rf"but the fit on reported experience has slope \${_b1n:.2f}. The attenuation "
            rf"formula predicts this: var(X)/(var(X) + var(ν)) = "
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

    The chart below runs this procedure on the same 100 workers from Lecture 11, whose wages follow a curved relationship with experience. The first 70 workers are the training data (navy) and the remaining 30 are the hold-out sample (gray). The slider sets the degree of a polynomial regression fitted to the training data only. In Lecture 11 you judged these polynomials by the adjusted R-squared; now the hold-out sample delivers the verdict directly.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # The same 100 workers as Lecture 11: identical seed and draw order, so the
    # scatter is literally the same data the polynomial-degree slider fit there.
    # The train/hold-out split is a fixed index cut, not a random draw, so the
    # demo never resamples. Fixed seed for reproducibility.
    _rng = np.random.default_rng(116)
    ho_n = 100
    ho_exper = _rng.uniform(1.0, 40.0, ho_n)
    ho_wage = 8.0 + 1.10 * ho_exper - 0.017 * ho_exper**2 + _rng.normal(0.0, 3.0, ho_n)
    ho_train = 70
    return ho_exper, ho_n, ho_train, ho_wage


@app.cell(hide_code=True)
def _(mo):
    ho_degree = mo.ui.slider(
        start=1, stop=12, step=1, value=1,
        label="Polynomial degree (fitted to training data only)",
        show_value=True,
    )
    mo.vstack(
        [
            mo.md("Raise the degree and compare the fit on the training workers with the fit on the hold-out workers."),
            ho_degree,
        ]
    )
    return (ho_degree,)


@app.cell(hide_code=True)
def _(alt, ho_degree, ho_exper, ho_train, ho_wage, mo, np, pd):
    _deg = int(ho_degree.value)
    _xtr, _ytr = ho_exper[:ho_train], ho_wage[:ho_train]
    _xte, _yte = ho_exper[ho_train:], ho_wage[ho_train:]

    # Fit on the training data only, in the Chebyshev basis, which stays well
    # conditioned at high degree where raw powers of experience would not.
    _series = np.polynomial.Chebyshev.fit(_xtr, _ytr, _deg)
    _ser_tr = float(np.sqrt(((_ytr - _series(_xtr)) ** 2).sum() / (len(_xtr) - 2)))
    _ser_te = float(np.sqrt(((_yte - _series(_xte)) ** 2).sum() / (len(_xte) - 2)))

    _grid = np.linspace(1.0, 40.0, 250)
    _xsc = alt.Scale(domain=[0.0, 42.0], nice=False)
    _ysc = alt.Scale(domain=[0.0, 36.0], nice=False)
    _pts = pd.DataFrame({
        "exper": ho_exper,
        "wage": ho_wage,
        "set": (["Training (used to fit)"] * ho_train
                + ["Hold-out (not used to fit)"] * (len(ho_exper) - ho_train)),
    })
    _scatter = (
        alt.Chart(_pts)
        .mark_circle(size=30, opacity=0.45, clip=True)
        .encode(
            x=alt.X("exper:Q", scale=_xsc, title="Work experience (years)"),
            y=alt.Y("wage:Q", scale=_ysc, title="Hourly wage (dollars)"),
            color=alt.Color(
                "set:N",
                scale=alt.Scale(
                    domain=["Training (used to fit)", "Hold-out (not used to fit)"],
                    range=["#1f4e79", "#6b7280"],
                ),
                legend=alt.Legend(title=None, orient="top"),
            ),
        )
    )
    _line = (
        alt.Chart(pd.DataFrame({"exper": _grid, "wage": _series(_grid)}))
        .mark_line(color="orange", size=3, clip=True)
        .encode(x=alt.X("exper:Q", scale=_xsc), y=alt.Y("wage:Q", scale=_ysc))
    )
    _chart = (_scatter + _line).properties(width=560, height=340)

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

    if _deg == 1:
        _msg = (
            rf"The straight line misses the curvature for both groups: the training SER "
            rf"is \${_ser_tr:.2f} and the hold-out SER is \${_ser_te:.2f}. A model this "
            rf"rigid predicts badly everywhere. Raise the degree to 2."
        )
    elif _deg == 2:
        _msg = (
            rf"The quadratic captures the rise and later flattening of wages. The "
            rf"training SER falls to \${_ser_tr:.2f}, and the hold-out SER falls to "
            rf"\${_ser_te:.2f}, its lowest value at any degree on this slider. By the "
            rf"out-of-sample criterion, this is the specification to keep."
        )
    elif _deg <= 5:
        _msg = (
            rf"At degree {_deg}, the training SER is \${_ser_tr:.2f}, barely below its "
            rf"value at degree 2, while the hold-out SER has edged up to \${_ser_te:.2f}. "
            rf"The extra terms bend the curve toward quirks of the training workers that "
            rf"the hold-out workers do not share."
        )
    else:
        _msg = (
            rf"At degree {_deg}, the training SER has fallen to \${_ser_tr:.2f}, because "
            rf"adding flexibility can only improve the in-sample fit. The hold-out SER "
            rf"has risen to \${_ser_te:.2f}. The gap between the two is overfitting: the "
            rf"model is memorizing noise in the training data, and the noise does not "
            rf"repeat in the hold-out sample."
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
    Steps like these underlie many *model evaluation algorithms*. The most common one is *$k$-fold cross-validation*: split the sample into $k$ folds (sub-samples), train the model on $k-1$ of them, test it on the remaining fold, and repeat so that each fold takes one turn as the test set. Averaging the test performance across folds gives a more stable measure than a single split, because no single lucky or unlucky hold-out sample decides the verdict. The logic is exactly what the chart above showed: if the model fits noise in the training folds, it performs poorly on the test fold.

    This closes the validity checklist. Internal validity asks whether a study's estimate means what it claims within the population studied, and Section 2's five threats are the ways it can fail. External validity asks how far the estimate travels, by argument and replication for causal questions, and by out-of-sample performance for prediction. Lecture 15 turns to panel data, the first of several tools that remove an internal-validity threat rather than just naming it: following the same entities over time makes it possible to cancel out omitted variables that stay fixed within each entity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** validity, internal validity, external validity, "
            "functional form, misspecification, measurement error in X, classical "
            "measurement error, attenuation bias, sample selection, sample selection "
            "bias, simultaneous causality, introspection, replication, training data, "
            "hold-out sample, testing data, model evaluation algorithm, k-fold "
            "cross-validation.\n\n"
            "**Key concepts covered:** the five threats to internal validity and why "
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
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "## Appendix": mo.md(r"""
        This is bonus material. You will not be tested on the content of the appendix.

        **Measurement error in $Y$.** Section 2 showed that classical measurement error in $X$ produces attenuation bias. Classical measurement error in $Y$ is far more forgiving. Suppose the true model is $Y = \beta_0 + \beta_1 X + u$, but we observe $\widetilde{Y} = Y + v$ with $\mathbb{E}[v \mid X, u] = 0$. In large samples,

        $$
        \hat{\beta}_1 \overset{p}{\to} \frac{\text{cov}(X, \widetilde{Y})}{\text{var}(X)} = \frac{\text{cov}(X,\ \beta_1 X + u + v)}{\text{var}(X)} = \frac{\text{cov}(X, Y)}{\text{var}(X)} = \beta_1,
        $$

        where the second-to-last equality follows from $\mathbb{E}[v \mid X, u] = 0$: the noise in $Y$ is unrelated to $X$, so it contributes nothing to the covariance in the numerator. The slope estimator is therefore still consistent.

        The noise is not free, however. Because $\text{var}(\widetilde{Y}) > \text{var}(Y)$, there is more unexplained variation around the fitted line, so the standard errors increase and the $R^2$ falls. Noise in the outcome costs precision; noise in the regressor costs consistency. That asymmetry is why Section 2's checklist worries about measurement error in $X$.
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
