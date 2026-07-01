# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "numpy",
#     "pandas",
#     "altair",
#     "pyarrow",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.23.9"
__preliminary__ = True
app = marimo.App(
    app_title="Lecture 8: Multiple Regression",
    css_file="marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go

    return alt, go, mo, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: block; margin-bottom: 1.5em;">Course home</a>'),
            mo.md("# [Lecture 8](#top)"),
            mo.md("Multiple Regression"),
            mo.nav_menu(
                {
                    "#sec1": "1. Omitted variable bias",
                    "#sec2": "2. The multiple regression model",
                    "#sec3": "3. Estimating the model with OLS",
                    "#sec4": "4. Measures of fit",
                    "#sec5": "5. The least squares assumptions with several regressors",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec7InferenceAndOmittedVariableBias.html" target="_self">← Lecture 7</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec9ControlVariablesAndInference.html" target="_self">Lecture 9 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 8: Multiple Regression
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

    [1. Omitted variable bias](#sec1)<br>
    [2. The multiple regression model](#sec2)<br>
    [3. Estimating the model with OLS](#sec3)<br>
    [4. Measures of fit](#sec4)<br>
    [5. The least squares assumptions with several regressors](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Omitted variable bias

    Lecture 7 built standard errors, hypothesis tests, and confidence intervals for the slope of a regression with a single regressor. Every one of those tools rested on the first least squares assumption from Lecture 6, that the error has a conditional mean of zero given $X$. That assumption fails whenever a variable left out of the regression both affects $Y$ and moves together with $X$. The left-out variable is part of the error, so the error is then correlated with $X$, written $\operatorname{cov}(X,u) \neq 0$, and $\mathbb{E}[u\mid X]\neq 0$. The estimate no longer centers on the true slope. This is *omitted variable bias*.

    With such a variable left out, the slope estimate converges not to $\beta_1$ but to

    $$ \hat{\beta}_1 \overset{p}{\to} \beta_1 + \operatorname{corr}(X,u)\cdot\frac{\sigma_u}{\sigma_X} = \beta_1 + \rho_{Xu}\,\frac{\sigma_u}{\sigma_X}. $$

    The second term is the bias, and its sign is the sign of the correlation between $X$ and the omitted part of the error. Two conditions are both needed for the bias to appear. The omitted variable must be correlated with $X$, and it must affect $Y$ so that it carries real weight inside the error. If either fails, the bias term is zero and the estimate stays on target.

    Return to the wage regression from Lectures 5 through 7. Ability sits in the error, and it raises both schooling and earnings, so education and the error are positively correlated. The bias term is then positive, and the estimated return to schooling comes out too high, because schooling gets credit for part of what is really the payoff to ability.

    A second case is new housing and home prices. Let $Y$ be local home prices and $X$ the number of new units built. Developers build more when interest rates are low, and low rates also raise demand and push prices up, so the omitted interest-rate conditions are positively correlated with building. The estimated effect of new supply on prices is biased upward for the same reason.

    Omitted variable bias is why a single explanatory variable is rarely enough for a causal claim. The repair is not to abandon regression but to bring the offending variable into it, so that ability, or interest rates, is held fixed instead of left in the error. The rest of this lecture builds that repair.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. The multiple regression model

    Bringing a variable into the regression means giving it a coefficient of its own. A *multiple regression model* relates the outcome to several explanatory variables at once,

    $$
    Y_i = \beta_0 + \beta_1 X_{1i} + \beta_2 X_{2i} + \dots + \beta_k X_{ki} + u_i, \qquad i = 1, \dots, n.
    $$

    Each $X_{ji}$ is one of the $k$ regressors measured for observation $i$, and $u_i$ holds everything still left out. The population regression function is the conditional mean of $Y$ given all the regressors,

    $$
    \mathbb{E}[Y \mid X_1 = x_1, \dots, X_k = x_k] = \beta_0 + \beta_1 x_1 + \dots + \beta_k x_k.
    $$

    Each slope now carries a *ceteris paribus* meaning, which is Latin for ''other things equal''. The coefficient $\beta_j$ is the change in $Y$ for a one-unit increase in $X_j$ when every other regressor is held fixed.

    The rest of this lecture works with a simulated sample of 200 school districts. For each district we observe the average test score of its students, the class size measured in students per teacher, and the average income of the students' parents in thousands of dollars. Districts with richer parents tend to run smaller classes, so class size and parental income are negatively correlated, exactly the setup of Section 1. Regressing test scores on class size and parental income together, $\beta_1$ is the change in a district's average score for one more student per teacher among districts with the same parental income. The phrase ''among districts with the same parental income'' is what the single-variable slope could not deliver, because there income was free to move along with class size.

    Geometry gives the same idea a picture. With one regressor the fitted model is a line through a two-dimensional scatter plot. With two regressors it is a plane floating in three dimensions, one horizontal axis for each regressor and the vertical axis for the outcome. Each slope is the tilt of the plane along its own axis, so holding parental income fixed means walking across the plane parallel to the class-size axis, and the slope of that walk is $\beta_1$. The next section puts the plane on screen and lets you fit it yourself.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Estimating the model with OLS

    The estimator is the one from Lecture 5 with more dials to turn. *Ordinary least squares* picks the intercept and slopes $\hat{\beta}_0, \hat{\beta}_1, \dots, \hat{\beta}_k$ that minimize the sum of squared residuals,

    $$
    \min_{b_0, b_1, \dots, b_k} \sum_{i=1}^{n} \left( Y_i - b_0 - b_1 X_{1i} - \dots - b_k X_{ki} \right)^2.
    $$

    The *predicted value* for observation $i$ is $\hat{Y}_i = \hat{\beta}_0 + \hat{\beta}_1 X_{1i} + \dots + \hat{\beta}_k X_{ki}$, and the *residual* is the gap between the actual and the predicted outcome, $\hat{u}_i = Y_i - \hat{Y}_i$.

    With one regressor OLS turns two dials, the intercept and the slope. With two regressors it turns three. In the district data, regressing average test scores on class size alone gives

    $$
    \widehat{TestScore} = 732.9 - 2.31 \, ClassSize.
    $$

    Adding parental income, measured in thousands of dollars, gives

    $$
    \widehat{TestScore} = 699.0 - 1.10 \, ClassSize + 0.67 \, PrntInc.
    $$

    The class-size coefficient moves from $-2.31$ to $-1.10$, less than half its former size. This is the omitted variable bias of Section 1 being removed. Parental income raises test scores and is lower where classes are larger, so the single-variable slope blamed class size for part of what was really the effect of income. The income coefficient says that among districts with the same class size, each additional thousand dollars of parental income goes with 0.67 more points.

    The figure below turns the minimization into a game. The three sliders are the dials, one for each coefficient, and the gray plane moves as you set them. The bar beside the plane keeps score by measuring the sum of squared residuals your plane leaves, and the dashed marker on the bar is the smallest score any plane can reach. Try to drive the bar down to the marker, then tick the box to reveal the plane OLS picks. The flat panel underneath shows what your plane implies for a district with average parental income, drawn against the dashed single-regressor line.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    b0_slider = mo.ui.slider(
        start=640.0, stop=780.0, step=1.0, value=700.0,
        label="β₀, the intercept", show_value=True,
    )
    b1_slider = mo.ui.slider(
        start=-4.0, stop=1.0, step=0.05, value=0.0,
        label="β₁, the slope on class size", show_value=True,
    )
    b2_slider = mo.ui.slider(
        start=-0.5, stop=1.5, step=0.05, value=0.0,
        label="β₂, the slope on parental income", show_value=True,
    )
    ols_box = mo.ui.checkbox(value=False, label="Reveal the plane OLS picks")
    mo.vstack(
        [
            mo.md(
                "Move the three dials to fit the plane to the cloud. The bar "
                "keeps score, and lower is better. Drag the 3D view to rotate it."
            ),
            b0_slider,
            b1_slider,
            b2_slider,
            ols_box,
        ]
    )
    return b0_slider, b1_slider, b2_slider, ols_box


@app.cell(hide_code=True)
def _(
    alt,
    b0_slider,
    b1_slider,
    b2_slider,
    b_multi,
    b_short,
    cs,
    go,
    mo,
    np,
    ols_box,
    pd,
    prnt,
    ssr_min,
    ts,
):
    _b0 = float(b0_slider.value)
    _b1 = float(b1_slider.value)
    _b2 = float(b2_slider.value)
    _resid = ts - (_b0 + _b1 * cs + _b2 * prnt)
    _ssr = float(_resid @ _resid)
    _gap = _ssr - ssr_min
    _pm = float(prnt.mean())
    _xline = np.array([15.0, 26.0])
    _png = np.array([float(prnt.min()), float(prnt.max())])

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter3d(
            x=cs, y=prnt, z=ts, mode="markers",
            marker=dict(size=3, color="#1f4e79", opacity=0.5),
        )
    )
    _gz_user = (_b0 + _b1 * _xline[None, :]) + _b2 * _png[:, None]
    _fig.add_trace(
        go.Surface(
            x=_xline, y=_png, z=_gz_user, opacity=0.5, showscale=False,
            colorscale=[[0, "#9aa5b1"], [1, "#9aa5b1"]],
        )
    )
    if ols_box.value:
        _gz_ols = (b_multi[0] + b_multi[1] * _xline[None, :]) + b_multi[2] * _png[:, None]
        _fig.add_trace(
            go.Surface(
                x=_xline, y=_png, z=_gz_ols, opacity=0.5, showscale=False,
                colorscale=[[0, "#f59e0b"], [1, "#f59e0b"]],
            )
        )
    _fig.update_layout(
        width=460, height=420, margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False, uirevision="keep",
        scene=dict(
            xaxis=dict(title="Class size", range=[14.5, 26.5]),
            yaxis=dict(title="Parental income", range=[float(prnt.min()) - 2.0, 39.0]),
            zaxis=dict(title="Test score", range=[615, 765]),
            camera=dict(eye=dict(x=1.7, y=1.5, z=0.7)),
        ),
    )

    _cap = 120000.0
    _bar_df = pd.DataFrame(
        {"x": ["SSR"], "value": [min(_ssr, _cap)], "label": [f"{_ssr:,.0f}"]}
    )
    _bar = (
        alt.Chart(_bar_df)
        .mark_bar(size=54, color="#1f4e79", opacity=0.85)
        .encode(
            x=alt.X("x:N", title=None, axis=alt.Axis(labels=False, ticks=False)),
            y=alt.Y("value:Q", title="Sum of squared residuals",
                    scale=alt.Scale(domain=[0.0, _cap], nice=False),
                    axis=alt.Axis(format="~s")),
        )
    )
    _bar_txt = (
        alt.Chart(_bar_df)
        .mark_text(dy=14, color="white", fontSize=11)
        .encode(x="x:N", y="value:Q", text="label:N")
    )
    _rule_df = pd.DataFrame({"y": [ssr_min], "t": ["OLS minimum"]})
    _rule = (
        alt.Chart(_rule_df)
        .mark_rule(color="#f59e0b", strokeDash=[5, 4], size=2)
        .encode(y="y:Q")
    )
    _rule_txt = (
        alt.Chart(_rule_df)
        .mark_text(dy=12, color="#b45309", fontSize=10)
        .encode(y="y:Q", text="t:N")
    )
    _bar_chart = alt.layer(_bar, _bar_txt, _rule, _rule_txt).properties(
        width=90, height=400,
    )

    _pts = pd.DataFrame({"x": cs, "y": ts})
    _user_df = pd.DataFrame({"x": _xline, "y": (_b0 + _b2 * _pm) + _b1 * _xline})
    _simple_df = pd.DataFrame({"x": _xline, "y": b_short[0] + b_short[1] * _xline})
    _scatter = (
        alt.Chart(_pts)
        .mark_circle(size=42, color="#1f4e79", opacity=0.55, clip=True)
        .encode(
            x=alt.X("x:Q", title="Class size (students per teacher)", scale=alt.Scale(domain=[14.5, 26.5], nice=False)),
            y=alt.Y("y:Q", title="Test score", scale=alt.Scale(domain=[640, 732], nice=False)),
        )
    )
    _simple_line = (
        alt.Chart(_simple_df)
        .mark_line(color="#6b7280", strokeDash=[6, 4], size=2, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _user_line = (
        alt.Chart(_user_df)
        .mark_line(color="#9aa5b1", size=2.5, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _layers = [_scatter, _simple_line, _user_line]
    if ols_box.value:
        _ols_df = pd.DataFrame(
            {"x": _xline, "y": (b_multi[0] + b_multi[2] * _pm) + b_multi[1] * _xline}
        )
        _layers.append(
            alt.Chart(_ols_df)
            .mark_line(color="#f59e0b", size=2.5, clip=True)
            .encode(x="x:Q", y="y:Q")
        )
    _chart2d = alt.layer(*_layers).properties(
        width=560, height=280, title="The flat view at average parental income",
    )

    if ols_box.value:
        _body = (
            f"The orange plane is the OLS fit, {b_multi[0]:.1f} {b_multi[1]:+.2f} ClassSize "
            f"{b_multi[2]:+.2f} PrntInc, and no other plane beats its sum of squared "
            f"residuals of {ssr_min:,.0f}. Your gray plane sits {_gap:,.0f} above it. In "
            f"the flat panel the orange slice at average income runs flatter than the "
            f"dashed single-regressor line, and the paragraph below explains why the two "
            f"disagree."
        )
    elif _ssr <= ssr_min * 1.02:
        _body = (
            f"Your plane's score of {_ssr:,.0f} is within two percent of the minimum "
            f"{ssr_min:,.0f}, so you have essentially found the OLS fit. OLS settles on "
            f"{b_multi[0]:.1f}, {b_multi[1]:+.2f}, and {b_multi[2]:+.2f}. Tick the box to "
            f"overlay its plane."
        )
    else:
        _body = (
            f"Your plane leaves a sum of squared residuals of {_ssr:,.0f}, which is "
            f"{_gap:,.0f} above the smallest any plane can manage. In the flat panel the "
            f"dashed single-regressor line stays put while your gray line moves with the "
            f"dials."
        )
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 1rem;max-width:620px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _body + "</span>"
    )
    mo.vstack(
        [
            mo.hstack(
                [mo.ui.plotly(_fig), _bar_chart],
                justify="center", align="center", gap=1.0, wrap=True,
            ),
            _chart2d,
            _caption,
        ],
        align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both lines in the flat panel are least squares fits, and they still disagree. The dashed line is the single-regressor fit from the first equation above. It answers the question ''how do test scores move with class size, letting parental income drift the way it drifts in the data''. Districts with bigger classes have poorer parents on average, so the dashed line stacks part of the income effect on top of the class-size effect and comes out steeper, at $-2.31$ points per student. The plane's slice answers a different question, ''how do test scores move with class size among districts with the same parental income'', and holding income fixed flattens the slope to $-1.10$. The gap of $-1.21$ points per student is the omitted variable bias from Section 1, and the appendix computes it as the income coefficient $0.67$ times the $-1.80$ slope from regressing income on class size. Neither line is a mistake. They answer different questions, and only the plane's slope holds income fixed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Measures of fit

    Two numbers summarize how well a multiple regression fits the data. The first is the *standard error of the regression*, the typical size of a residual,

    $$
    \mathrm{SER} = \sqrt{\frac{1}{n-k-1}\sum_{i=1}^{n}\hat{u}_i^2} = \sqrt{\frac{\mathrm{SSR}}{n-k-1}},
    $$

    where $\mathrm{SSR} = \sum_{i=1}^{n}\hat{u}_i^2$ is the sum of squared residuals. We divide by $n - k - 1$ rather than $n$ because estimating the intercept and the $k$ slopes uses up $k + 1$ pieces of information from the sample. With a single regressor this is the $n - 2$ from Lecture 5.

    The second is the *$R^2$*, the share of the variation in $Y$ that the model explains,

    $$
    R^2 = 1 - \frac{\mathrm{SSR}}{\mathrm{TSS}}, \qquad \mathrm{TSS} = \sum_{i=1}^{n}(Y_i - \bar{Y})^2.
    $$

    In the district data the payoff from the second regressor is easy to read. Class size alone gives an $R^2$ of 0.151 and a SER of 13.1 points. Adding parental income lifts the $R^2$ to 0.331 and cuts the SER to 11.7. Those gains are real, because the residuals genuinely shrink when income enters.

    In multiple regression, though, the $R^2$ has a flaw. Adding a regressor can never raise the sum of squared residuals, because OLS can always set the new coefficient to zero and do no worse. So the $R^2$ never falls when a regressor is added, even one that explains nothing. Judging a model by its $R^2$ alone would reward piling in useless variables.

    The *adjusted $R^2$* fixes this by charging a penalty for each regressor,

    $$
    \bar{R}^2 = 1 - \frac{n-1}{n-k-1}\cdot\frac{\mathrm{SSR}}{\mathrm{TSS}}.
    $$

    The factor $\frac{n-1}{n-k-1}$ grows with $k$, so a regressor that barely reduces the sum of squared residuals lowers the adjusted $R^2$ rather than raising it. A falling adjusted $R^2$ is the signal that a regressor is not earning its place.

    The demonstration below makes the flaw concrete. Starting from the two-regressor model, the slider adds regressors that are pure noise, columns of random numbers drawn by the computer, one number per district, with no connection to test scores at all. Every noise column still nudges the $R^2$ upward. Watch what the adjusted $R^2$ does instead.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    junk_slider = mo.ui.slider(
        start=0, stop=30, step=1, value=0,
        label="Number of pure-noise regressors added",
        show_value=True,
    )
    mo.vstack(
        [
            mo.md(
                "Class size and parental income stay in the regression. Each added "
                "regressor is a fresh column of random numbers, one for each of the "
                "200 districts."
            ),
            junk_slider,
        ]
    )
    return (junk_slider,)


@app.cell(hide_code=True)
def _(alt, fit_path, junk_slider, mo):
    _k = int(junk_slider.value)
    _shown = fit_path[fit_path["k"] <= _k].melt(
        id_vars="k", value_vars=["r2", "adj"], var_name="measure", value_name="value"
    )
    _shown["measure"] = _shown["measure"].map({"r2": "R²", "adj": "Adjusted R²"})

    _lines = (
        alt.Chart(_shown)
        .mark_line(size=2.5)
        .encode(
            x=alt.X("k:Q", title="Noise regressors added", scale=alt.Scale(domain=[0, 30], nice=False)),
            y=alt.Y("value:Q", title=None, scale=alt.Scale(domain=[0.27, 0.42], nice=False)),
            color=alt.Color(
                "measure:N",
                scale=alt.Scale(domain=["R²", "Adjusted R²"], range=["#1f4e79", "#f59e0b"]),
                legend=alt.Legend(title=None, orient="top"),
            ),
        )
    )
    _dots = (
        alt.Chart(_shown[_shown["k"] == _k])
        .mark_point(size=85, filled=True)
        .encode(
            x="k:Q", y="value:Q",
            color=alt.Color(
                "measure:N",
                scale=alt.Scale(domain=["R²", "Adjusted R²"], range=["#1f4e79", "#f59e0b"]),
                legend=None,
            ),
        )
    )
    _chart = alt.layer(_lines, _dots).properties(
        width=560, height=320,
        title="Pure noise pushes the R² up and the adjusted R² down",
    )

    _row = fit_path.iloc[_k]
    _base = fit_path.iloc[0]
    if _k == 0:
        _body = (
            rf"With class size and parental income and nothing else, the $R^2$ is "
            rf"{_row['r2']:.3f} and the adjusted $R^2$ is {_row['adj']:.3f}. The two "
            rf"nearly agree because the penalty for two regressors is small."
        )
    else:
        _noun = "column" if _k == 1 else "columns"
        _body = (
            rf"With {_k} {_noun} of pure noise added, the $R^2$ has climbed to "
            rf"{_row['r2']:.3f} while the adjusted $R^2$ has slipped to {_row['adj']:.3f}. "
            rf"The standard error of the regression has crept from {_base['ser']:.2f} up "
            rf"to {_row['ser']:.2f} points, and the class-size slope still sits near its "
            rf"two-regressor value (currently {_row['b_cs']:.2f}). The noise explains "
            rf"nothing, and only the adjusted $R^2$ says so."
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
    <a id="sec5"></a>
    ## 5. The least squares assumptions with several regressors

    The conditions for reading the OLS slopes as causal effects carry over from Lecture 6, with one addition, so there are four.

    The first is *mean independence*, that the error has mean zero given every regressor, $\mathbb{E}[u \mid X_1, \dots, X_k] = 0$. This is the assumption the whole lecture has been working to rescue. Each variable moved from the error into the regression is one fewer source of omitted variable bias.

    The second is that the data $(Y_i, X_{1i}, \dots, X_{ki})$ are *independent and identically distributed* across observations, which holds when the sample is drawn at random, as discussed in Lecture 6.

    The third is that *large outliers are unlikely*, so that no single observation dominates the estimates.

    The fourth is new to multiple regression. It rules out *perfect multicollinearity*, which arises when one regressor is an exact linear function of the others. Age and date of birth are an example. A person's age is fixed once the date of birth and today's date are set, so the two carry the same information. Asking for the effect of age while holding date of birth fixed has no meaning, because age cannot change with date of birth held constant. When two regressors are perfectly collinear, OLS cannot separate their coefficients and the estimates do not exist. The fix is to drop one of the redundant regressors.

    Lecture 9 picks up from here, asking which regressors belong in the model, what happens when one regressor is nearly collinear with another, and how the hypothesis tests of Lecture 7 extend to several coefficients at once.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** omitted variable bias, multiple regression model, "
            "population regression function, ceteris paribus, ordinary least squares, "
            "predicted value, residual, standard error of the regression, R-squared, "
            "adjusted R-squared, mean independence, perfect multicollinearity.\n\n"
            "**Key concepts covered:** why an omitted variable that moves with a regressor "
            "biases its slope, the multiple regression model and the ceteris paribus reading "
            "of each coefficient, OLS as minimizing the sum of squared residuals over all "
            "the coefficients at once, why the R-squared never falls when a regressor is "
            "added while the adjusted R-squared can, and the four least squares assumptions "
            "including no perfect multicollinearity."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(np):
    _rng = np.random.default_rng(95)
    _n = 200
    cs = np.clip(_rng.normal(20.0, 2.3, _n), 15.0, 26.0)
    prnt = 51.3 - 1.815 * cs + _rng.normal(0.0, 9.0, _n)
    # Discarded draw (formerly spending per pupil). Removing it would shift the
    # seed-95 stream and change every estimate quoted in the prose.
    _rng.normal(0.0, 1.2, _n)
    _u = _rng.normal(0.0, 12.0, _n)
    ts = 698.9 - 1.10 * cs + 0.65 * prnt + _u
    noise = np.random.default_rng(235).normal(0.0, 1.0, (_n, 30))
    return cs, noise, prnt, ts


@app.cell(hide_code=True)
def _(cs, noise, np, pd, prnt, ts):
    _n = len(ts)
    _ones = np.ones(_n)
    b_short, *_ = np.linalg.lstsq(np.column_stack([_ones, cs]), ts, rcond=None)
    b_multi, *_ = np.linalg.lstsq(np.column_stack([_ones, cs, prnt]), ts, rcond=None)
    _resid_min = ts - np.column_stack([_ones, cs, prnt]) @ b_multi
    ssr_min = float(_resid_min @ _resid_min)

    _tss = float(np.sum((ts - ts.mean()) ** 2))
    _rows = []
    for _k in range(31):
        _X = np.column_stack([_ones, cs, prnt] + [noise[:, _j] for _j in range(_k)])
        _b, *_ = np.linalg.lstsq(_X, ts, rcond=None)
        _res = ts - _X @ _b
        _ssr = float(_res @ _res)
        _kk = 2 + _k
        _rows.append(
            {
                "k": _k,
                "r2": 1.0 - _ssr / _tss,
                "adj": 1.0 - (_n - 1) / (_n - _kk - 1) * _ssr / _tss,
                "ser": float(np.sqrt(_ssr / (_n - _kk - 1))),
                "b_cs": float(_b[1]),
            }
        )
    fit_path = pd.DataFrame(_rows)
    return b_multi, b_short, fit_path, ssr_min


@app.cell(hide_code=True)
def _(mo):
    _appendix = mo.md(r"""
    This appendix shows where the omitted variable bias formula comes from. You will not be tested on it.

    **Omitted variable bias as a product of two regressions**

    Suppose the model with both regressors is $Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + u$, but we leave out $X_2$ and regress $Y$ on $X_1$ alone. Write the auxiliary regression of the omitted regressor on the included one as $X_2 = \delta_0 + \delta_1 X_1 + v$, where $\delta_1$ measures how the two move together. Substituting for $X_2$ gives

    $$
    Y = (\beta_0 + \beta_2 \delta_0) + (\beta_1 + \beta_2 \delta_1) X_1 + (\beta_2 v + u).
    $$

    The single-variable regression of $Y$ on $X_1$ therefore estimates the combined slope $\beta_1 + \beta_2 \delta_1$, not $\beta_1$ on its own. The bias is $\beta_2 \delta_1$, the effect of the omitted variable times its relationship with the included one.

    In the district data both pieces can be estimated. The income coefficient in the two-regressor fit is $0.67$, and regressing parental income on class size gives an auxiliary slope of $\hat{\delta}_1 = -1.80$, because richer districts run smaller classes. Their product is $0.67 \times (-1.80) \approx -1.21$, which is exactly the gap between the single-variable slope $-2.31$ and the held-income slope $-1.10$.
    """)
    mo.accordion({"## Appendix": _appendix})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec7InferenceAndOmittedVariableBias.html" target="_self">← Lecture 7</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec9ControlVariablesAndInference.html" target="_self">Lecture 9 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
