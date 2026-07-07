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
    [5. The least squares assumptions with several regressors](#sec5)<br>
    &emsp;&emsp;[Least Squares Assumption 1: the conditional mean of u given the regressors is zero](#sec5a)<br>
    &emsp;&emsp;[Least Squares Assumption 2: the data are i.i.d.](#sec5b)<br>
    &emsp;&emsp;[Least Squares Assumption 3: large outliers are unlikely](#sec5c)<br>
    &emsp;&emsp;[Least Squares Assumption 4: no perfect multicollinearity](#sec5d)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>

    ## 1. Omitted variable bias

    Recall the first least squares assumption from Lecture 6. It says that the conditional mean of the error term is zero at every value of $X$,

    $$
    \mathbb{E}[u \mid X] = 0.
    $$

    This means that the omitted determinants of $Y$ do not vary systematically with $X$. If the assumption holds, then we can interpret the single-variable regression slope, $\hat{\beta}_1$, causally. If omitted determinants of $Y$ are systematically related to $X$, then the error term is correlated with $X$, the assumption fails, and the OLS slope estimator does not isolate the causal effect of $X$ on $Y$.

    Consider the regression of hourly wages on years of education. If education is the only independent variable, then the error contains all other determinants of wages, such as ability, ambition, family resources, health, school quality, and luck. For the first least squares assumption to hold, these omitted determinants must not vary systematically with education. That is hard to believe, however. More able students may find school easier and stay in school longer. Children from richer families may get more schooling and may also inherit networks that help them in the labor market. If these factors are omitted, the error term is likely to be correlated with education.

    When the error is correlated with $X$, the slope estimate does not converge to $\beta_1$. Instead,

    $$
    \hat{\beta}_1 \overset{p}{\to} \beta_1 + \underbrace{\operatorname{corr}(X,u)\cdot\frac{\sigma_u}{\sigma_X}}_{\text{bias}}.
    $$

    The second term is the *omitted variable bias*. Its sign is determined by the sign of the correlation between $X$ and the error term, $u$. Its size grows as that correlation becomes stronger, the variance of $u$ becomes larger, or the variance of $X$ becomes smaller.

    Not every omitted variable creates omitted variable bias. An omitted variable matters only if it affects $Y$ and varies systematically with $X$. In the wage example, ability and family resources likely satisfy both conditions. They affect wages, so they belong in the error term if omitted. They are also likely to be positively related to education. As a result, education is positively correlated with the error term, so $\rho_{Xu} > 0$. The estimated return to schooling is therefore *biased upward* because education receives credit for part of the wage difference that is really due to ability and family background. If the error were negatively correlated with education instead, so that $\rho_{Xu} < 0$, the estimated return to schooling would be *biased downward*.

    When omitted determinants of $Y$ vary systematically with $X$, we do not need to abandon regression analysis. Instead, we can make the first least squares assumption more plausible by including those determinants in the regression whenever possible. By adding ability, family resources, or other relevant factors as additional independent variables, we remove them from the error term. This is why we often consider multiple-variable regression instead of single-variable regression.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>

    ## 2. The multiple regression model

    A single-variable regression relates an outcome to one independent variable. A multiple-variable regression model relates the outcome to several independent variables at the same time,

    $$
    Y_i = \beta_0 + \beta_1 X_{1i} + \beta_2 X_{2i} + \dots + \beta_k X_{ki} + u_i,
    \qquad i = 1, \dots, n.
    $$

    Each $X_{ji}$ is one of the $k$ independent variables measured for observation $i$. The error term $u_i$ contains the determinants of $Y_i$ that are still left out after those variables have been included.

    The interpretation of the population parameters follows a similar logic to the single-variable model from Lectures 5 and 6. The parameter $\beta_j$ describes how $Y$ changes when $X_j$ increases by one unit, holding the other explanatory variables and the error fixed. For example, in the model

    $$
    Y_i = \beta_0 + \beta_1 X_{1i} + \beta_2 X_{2i} + u_i,
    $$

    $\beta_1$ is the change in $Y$ caused by a one-unit increase in $X_1$, holding $X_2$ and $u$ fixed. The parameter $\beta_2$ has the same interpretation for $X_2$, holding $X_1$ and $u$ fixed.

    When we estimate a regression, however, we cannot literally hold $u_i$ fixed because we do not observe it. We can only hold fixed the variables that are included in the regression. This is why adding independent variables can help with omitted variable bias. A variable that is included in the regression is no longer part of the error. Instead, it is held fixed when estimating the coefficients on the other included variables.

    ### <span style="color:#0b68cb">Earnings and education example</span>

    Return to the single-variable model of earnings and education in Lectures 5 and 6,

    $$
    \text{wage}_i = \beta_0 + \beta_1 \text{education}_i + u_i.
    $$

    In that model, all other determinants of wages are left in the error. Some of those determinants, such as ability and parental income, are likely to be related to both education and wages inducing omitted variable bias.

    Ability is usually difficult to measure, so we cannot simply add it to the regression. Parental income, however, can often be measured. Suppose we include both education and parental income as independent variables,

    $$
    \text{wage}_i
    = \beta_0 + \beta_1 \text{education}_i+\beta_2 \text{parental income}_i+u_i.
    $$

    When we estimate the model with OLS, we cannot hold fixed the determinants that remain in $u_i$, such as ability. But because parental income is now included in the regression, we can hold parental income fixed. The education coefficient is therefore estimated by comparing wages across workers with the same parental income. As a result, the OLS estimate $\hat{\beta}_1$ no longer attributes the effect of parental income to education.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>

    ## 3. Estimating the model with OLS

    The multiple regression model contains more unknown parameters than the single-variable model. Instead of estimating only an intercept and one slope, we now estimate an intercept and one slope for each independent variable,

    $$
    Y_i = \beta_0 + \beta_1 X_{1i} + \dots + \beta_k X_{ki} + u_i.
    $$

    If we knew the values of $\beta_0, \beta_1, \dots, \beta_k$, we would know the population regression function, and thus the causal impact of each $X_{j}$ on $Y$. In practice, we only have a sample. We therefore use the sample to estimate these unknown parameters.

    The basic idea is the same as in the single-variable case. Ordinary least squares chooses the coefficients that make the model's predictions come as close as possible to the observed outcomes. The only difference is that the predicted value now depends on several independent variables instead of one. For any candidate values $b_0, b_1, \dots, b_k$, the predicted value of $Y$ for observation $i$ is $b_0 + b_1 X_{1i} + \dots + b_k X_{ki}$, so the residual is

    $$
    Y_i - b_0 - b_1 X_{1i} - \dots - b_k X_{ki}.
    $$

    A set of coefficients fits the sample well when these residuals are small. As before, some residuals are positive and some are negative, so we square them before adding them up. Ordinary least squares chooses the intercept and slopes $\hat{\beta}_0, \hat{\beta}_1, \dots, \hat{\beta}_k$ that minimize the sum of squared residuals,

    $$
    \min_{b_0, b_1, \dots, b_k} \sum_{i=1}^{n} \left( Y_i - b_0 - b_1 X_{1i} - \dots - b_k X_{ki} \right)^2.
    $$

    Once OLS has chosen these coefficients, the fitted value for observation $i$ is

    $$
    \hat{Y}_i = \hat{\beta}_0 + \hat{\beta}*1 X*{1i} + \dots + \hat{\beta}*k X*{ki},
    $$

    and the OLS residual is the gap between the actual and fitted outcome,

    $$
    \hat{u}_i = Y_i - \hat{Y}_i.
    $$

    ### <span style="color:#0b68cb">Earnings and education example continued</span>

    We can see what changes when we add another independent variable by returning to the wage example. As is shown in the plots following this discussion, regressing hourly wages on years of education alone in our example data gives

    $$
    \widehat{\text{Wage}} = 7.2 + 1.63 \cdot \text{Education}.
    $$

    Adding parental income, measured in thousands of dollars, gives

    $$
    \widehat{\text{Wage}} = 5.2 + 1.22 \cdot \text{Education} + 0.10 \cdot \text{Parental income}.
    $$

    The education coefficient falls from $1.63$ to $1.22$, reducing the estimated return by about one quarter. This is what we would expect if parental income was one source of omitted variable bias in the single-variable regression. Parental income raises wages and is higher, on average, for workers with more schooling. When parental income was omitted, the single-variable slope attributed to education part of the wage difference that was really associated with family resources.

    The parental income coefficient says that, among workers with the same education, each additional thousand dollars of parental income is associated with 10 cents more in hourly wages on average. Equivalently, an additional ten thousand dollars of parental income is associated with one dollar more per hour on average.

    Just like in the single-variable regression, there is an important distinction between interpreting the population coefficient and interpreting the OLS estimate. In the population model, $\beta_1$ describes the causal effect of education only under the thought experiment of changing education while holding fixed the other determinants of wages in $u_i$. In an OLS regression, however, we do not observe or hold fixed the remaining determinants in $u_i$, such as ability, ambition, health, school quality, or luck. What we can hold fixed are the variables included in the regression. After adding parental income, the education coefficient is estimated by comparing workers with the same parental income. This removes parental income from the error term, but any remaining omitted determinants in $u_i$ could still create omitted variable bias if they vary systematically with education.

    The figure below illustrates the OLS minimization problem. The three sliders let you choose the intercept, the education slope, and the parental-income slope. As you move them, the flat surface in the three-dimensional plot moves too. This flat surface is the multiple regression version of a fitted line. For each worker, it gives the wage predicted by that worker’s education and parental income. The goal is to choose the coefficients that make the vertical gaps between the points and the surface as small as possible. The bar beside the plot measures the sum of squared residuals, and the dashed marker shows the smallest value OLS can achieve. Move the sliders to see how different coefficient choices affect the sum of squared residuals, then tick the box to show the coefficients OLS chooses.

    The two-dimensional plot directly underneath shows the education-wage relationship implied by the multiple regression model when parental income is held fixed at its average value. This line differs from the single-variable OLS line because the multiple regression coefficient on education is estimated after accounting for parental income. Notice that the single-variable OLS line is steeper than the coefficient on education in the multiple-variable regression model. Can you explain why the slopes differ using the omitted variable bias formula from Section 1?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    get_coefs, set_coefs = mo.state((10.0, 0.0, 0.0))
    get_ols_box, set_ols_box = mo.state(False)
    return get_coefs, get_ols_box, set_coefs, set_ols_box


@app.cell(hide_code=True)
def _(get_coefs, get_ols_box, mo, set_coefs, set_ols_box):
    # The dials and the checkbox are tied through mo.state: ticking the box
    # jumps the dials to the OLS values, and moving a dial unticks the box.
    # marimo does not re-run the cell whose own element triggered a state
    # change, so the sliders and the checkbox must live in separate cells.
    _b0v, _b1v, _b2v = get_coefs()

    def _move(_i):
        def _handler(_v):
            _c = list(get_coefs())
            _c[_i] = float(_v)
            set_coefs(tuple(_c))
            if get_ols_box():
                set_ols_box(False)
        return _handler

    b0_slider = mo.ui.slider(
        start=0.0, stop=20.0, step=0.1, value=_b0v,
        label="β₀, the intercept", show_value=True, on_change=_move(0),
    )
    b1_slider = mo.ui.slider(
        start=-1.0, stop=4.0, step=0.01, value=_b1v,
        label="β₁, the slope on years of education", show_value=True,
        on_change=_move(1),
    )
    b2_slider = mo.ui.slider(
        start=-0.1, stop=0.3, step=0.01, value=_b2v,
        label="β₂, the slope on parental income", show_value=True,
        on_change=_move(2),
    )
    return b0_slider, b1_slider, b2_slider


@app.cell(hide_code=True)
def _(get_ols_box, mo, ols_dials, set_coefs, set_ols_box):
    def _toggle(_v):
        set_ols_box(bool(_v))
        if _v:
            set_coefs(ols_dials)

    ols_box = mo.ui.checkbox(
        value=get_ols_box(),
        label="Show the OLS surface instead of yours",
        on_change=_toggle,
    )
    return (ols_box,)


@app.cell(hide_code=True)
def _(b0_slider, b1_slider, b2_slider, mo, ols_box):
    mo.vstack(
        [
            b0_slider,
            b1_slider,
            b2_slider,
            ols_box,
        ]
    )
    return


@app.cell(hide_code=True)
def _(
    alt,
    b_multi,
    b_short,
    educ,
    get_coefs,
    get_ols_box,
    go,
    mo,
    np,
    pd,
    prnt,
    ssr_min,
    wage,
):
    _b0, _b1, _b2 = get_coefs()
    _box = get_ols_box()
    _resid = wage - (_b0 + _b1 * educ + _b2 * prnt)
    _ssr = float(_resid @ _resid)
    _gap = _ssr - ssr_min
    _pm = float(prnt.mean())
    _xline = np.array([0.0, 21.0])
    _png = np.array([0.0, 130.0])

    # The checkbox swaps the displayed plane rather than overlaying a second
    # one, so the bar and the flat view always describe the plane on screen.
    if _box:
        _gz = (b_multi[0] + b_multi[1] * _xline[None, :]) + b_multi[2] * _png[:, None]
        _line_y = (b_multi[0] + b_multi[2] * _pm) + b_multi[1] * _xline
        _shown_ssr = ssr_min
    else:
        _gz = (_b0 + _b1 * _xline[None, :]) + _b2 * _png[:, None]
        _line_y = (_b0 + _b2 * _pm) + _b1 * _xline
        _shown_ssr = _ssr

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter3d(
            x=educ, y=prnt, z=wage, mode="markers",
            marker=dict(size=3, color="#1f4e79", opacity=0.5),
        )
    )
    _fig.add_trace(
        go.Surface(
            x=_xline, y=_png, z=_gz, opacity=0.5, showscale=False,
            colorscale=[[0, "#f59e0b"], [1, "#f59e0b"]],
        )
    )
    _fig.update_layout(
        width=580, height=470, margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False, uirevision="keep",
        scene=dict(
            xaxis=dict(title="Years of education", range=[0.0, 21.0]),
            yaxis=dict(title="Parental income", range=[0.0, 130.0]),
            zaxis=dict(title="Hourly wage", range=[0.0, 60.0]),
            camera=dict(eye=dict(x=1.7, y=1.5, z=0.7)),
        ),
    )

    _cap = 100000.0
    _bar_df = pd.DataFrame(
        {"x": ["SSR"], "value": [min(_shown_ssr, _cap)], "label": [f"{_shown_ssr:,.0f}"]}
    )
    _bar = (
        alt.Chart(_bar_df)
        .mark_bar(size=38, color="#1f4e79", opacity=0.85)
        .encode(
            x=alt.X("x:N", title=None, axis=alt.Axis(labels=False, ticks=False)),
            y=alt.Y("value:Q", title="SSR",
                    scale=alt.Scale(domain=[0.0, _cap], nice=False),
                    axis=alt.Axis(format="~s")),
        )
    )
    _bar_txt = (
        alt.Chart(_bar_df)
        .mark_text(dy=-6, color="#1f4e79", fontSize=11)
        .encode(x="x:N", y="value:Q", text="label:N")
    )
    _rule_df = pd.DataFrame({"y": [ssr_min], "t": ["OLS min"]})
    _rule = (
        alt.Chart(_rule_df)
        .mark_rule(color="#f59e0b", strokeDash=[5, 4], size=2)
        .encode(y="y:Q")
    )
    _rule_txt = (
        alt.Chart(_rule_df)
        .mark_text(dy=12, color="#b45309", fontSize=9)
        .encode(y="y:Q", text="t:N")
    )
    _bar_chart = alt.layer(_bar, _bar_txt, _rule, _rule_txt).properties(
        width=60, height=430,
    )

    _pts = pd.DataFrame({"x": educ, "y": wage})
    _line_df = pd.DataFrame({"x": _xline, "y": _line_y})
    _simple_df = pd.DataFrame({"x": _xline, "y": b_short[0] + b_short[1] * _xline})
    _scatter = (
        alt.Chart(_pts)
        .mark_circle(size=42, color="#1f4e79", opacity=0.55, clip=True)
        .encode(
            x=alt.X("x:Q", title="Years of education", scale=alt.Scale(domain=[0.0, 21.0], nice=False)),
            y=alt.Y("y:Q", title="Hourly wage (USD)", scale=alt.Scale(domain=[0.0, 60.0], nice=False)),
        )
    )
    _simple_line = (
        alt.Chart(_simple_df)
        .mark_line(color="#6b7280", strokeDash=[6, 4], size=2, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _plane_line = (
        alt.Chart(_line_df)
        .mark_line(color="#f59e0b", size=2.5, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _chart2d = alt.layer(_scatter, _simple_line, _plane_line).properties(
        width=560, height=280, title="Education-Wage Relationship Holding Parental Income Fixed",
    )

    if _box:
        _body = (
            f"The flat surface on screen is now the OLS fit, {b_multi[0]:.1f} "
            f"{b_multi[1]:+.2f} Education {b_multi[2]:+.2f} Parental income. No other "
            f"flat surface has a lower sum of squared residuals than {ssr_min:,.0f}, so "
            f"the bar sits exactly on the dashed marker. In the two-dimensional plot below, "
            f"the education-wage line holding parental income fixed at its average value is "
            f"flatter than the dashed single-regressor line.  "
            f"The sliders have jumped to the OLS values. Moving "
            f"any slider lets you choose the coefficients again."
        )
    elif _ssr <= ssr_min * 1.02:
        _body = (
            f"The current sum of squared residuals is {_ssr:,.0f}, which is within two "
            f"percent of the minimum value, {ssr_min:,.0f}. You have therefore come very "
            f"close to the OLS fit. OLS chooses coefficients of {b_multi[0]:.1f}, "
            f"{b_multi[1]:+.2f}, and {b_multi[2]:+.2f}. Tick the box to move the sliders "
            f"to those OLS values."
        )
    else:
        _body = (
            f"The current sum of squared residuals is {_ssr:,.0f}, which is "
            f"{_gap:,.0f} above the smallest value OLS can achieve. In the "
            f"two-dimensional plot below, the dashed single-regressor line stays fixed, "
            f"while the education-wage line from the multiple regression model moves as "
            f"you change the coefficient sliders."
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
                justify="center", align="center", gap=0.5,
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

    In the worker data, education alone gives an $R^2$ of 0.441 and a SER of \$6.30 an hour. Adding parental income lifts the $R^2$ to 0.471 and trims the SER to \$6.14. Notice how modest that is. The fit improves only a little even though the education slope fell by a quarter when income entered. A regressor can matter enormously for the causal story while adding little to the fit, because bias and fit are different problems.

    In multiple regression, though, the $R^2$ has a flaw. Adding a regressor can never raise the sum of squared residuals, because OLS can always set the new coefficient to zero and do no worse. So the $R^2$ never falls when a regressor is added, even one that explains nothing. Judging a model by its $R^2$ alone would reward piling in useless variables.

    The *adjusted $R^2$* fixes this by charging a penalty for each regressor,

    $$
    \bar{R}^2 = 1 - \frac{n-1}{n-k-1}\cdot\frac{\mathrm{SSR}}{\mathrm{TSS}}.
    $$

    The factor $\frac{n-1}{n-k-1}$ grows with $k$, so a regressor that barely reduces the sum of squared residuals lowers the adjusted $R^2$ rather than raising it. A falling adjusted $R^2$ is the signal that a regressor is not earning its place.

    The demonstration below makes the flaw concrete. Starting from the two-regressor model, the slider adds regressors that are pure noise, columns of random numbers drawn by the computer, one number per worker, with no connection to wages at all. The specification above the figure grows with each added column, and every noise column still nudges the $R^2$ upward. Watch what the adjusted $R^2$ does instead.
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
                "Education and parental income stay in the regression. Each added "
                "regressor is a fresh column of random numbers, one for each of the "
                "200 workers."
            ),
            junk_slider,
        ]
    )
    return (junk_slider,)


@app.cell(hide_code=True)
def _(alt, fit_path, junk_slider, mo):
    _k = int(junk_slider.value)

    if _k == 0:
        _spec = r"Wage = \beta_0 + \beta_1\,Education + \beta_2\,PrntInc + u"
    elif _k <= 3:
        _noise_terms = " + ".join(
            rf"\gamma_{{{_j}}}\,Noise_{{{_j}}}" for _j in range(1, _k + 1)
        )
        _spec = (
            rf"Wage = \beta_0 + \beta_1\,Education + \beta_2\,PrntInc "
            rf"+ {_noise_terms} + u"
        )
    else:
        _spec = (
            rf"Wage = \beta_0 + \beta_1\,Education + \beta_2\,PrntInc "
            rf"+ \gamma_1\,Noise_1 + \cdots + \gamma_{{{_k}}}\,Noise_{{{_k}}} + u"
        )
    _spec_md = mo.md(rf"$$ {_spec} $$")

    _shown = fit_path[fit_path["k"] <= _k].melt(
        id_vars="k", value_vars=["r2", "adj"], var_name="measure", value_name="value"
    )
    _shown["measure"] = _shown["measure"].map({"r2": "R²", "adj": "Adjusted R²"})

    _lines = (
        alt.Chart(_shown)
        .mark_line(size=2.5)
        .encode(
            x=alt.X("k:Q", title="Noise regressors added", scale=alt.Scale(domain=[0, 30], nice=False)),
            y=alt.Y("value:Q", title=None, scale=alt.Scale(domain=[0.41, 0.55], nice=False)),
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
            rf"With education and parental income and nothing else, the $R^2$ is "
            rf"{_row['r2']:.3f} and the adjusted $R^2$ is {_row['adj']:.3f}. The two "
            rf"nearly agree because the penalty for two regressors is small."
        )
    else:
        _noun = "column" if _k == 1 else "columns"
        _body = (
            rf"With {_k} {_noun} of pure noise added, the $R^2$ has climbed to "
            rf"{_row['r2']:.3f} while the adjusted $R^2$ has slipped to {_row['adj']:.3f}. "
            rf"The standard error of the regression has crept from {_base['ser']:.2f} up "
            rf"to {_row['ser']:.2f} dollars, and the education slope still sits near its "
            rf"two-regressor value (currently {_row['b_educ']:.2f}). The noise explains "
            rf"nothing, and only the adjusted $R^2$ says so."
        )
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 1rem;max-width:560px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _body + "</span>"
    )
    mo.vstack([_spec_md, _chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. The least squares assumptions with several regressors

    The conditions for reading the OLS slopes as causal effects carry over from Lecture 6, with one addition, so there are four. The first three are the single-regressor assumptions restated for several regressors, and the fourth is new.

    <a id="sec5a"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 1: the conditional mean of $u$ given the regressors is zero</span>

    The error must satisfy $\mathbb{E}[u \mid X_1, \dots, X_k] = 0$, the several-regressor version of *mean independence*. This is the assumption the whole lecture has been working to rescue. Each variable moved from the error into the regression is one fewer source of omitted variable bias, and Section 1's formula describes what happens to the slope when a relevant variable stays behind.

    <a id="sec5b"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 2: the data are i.i.d.</span>

    The observations $(Y_i, X_{1i}, \dots, X_{ki})$ must be *independent and identically distributed* across $i$, which holds when the sample is drawn at random, as discussed in Lecture 6.

    <a id="sec5c"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 3: large outliers are unlikely</span>

    No single observation should be able to dominate the estimates. As in Lecture 6, the practical advice is to plot the data and check extreme values before trusting a regression.

    <a id="sec5d"></a>
    ### <span style="color:#0b68cb">Least Squares Assumption 4: no perfect multicollinearity</span>

    The new assumption rules out *perfect multicollinearity*, which arises when one regressor is an exact linear function of the others. Age and date of birth are an example. A person's age is fixed once the date of birth and today's date are set, so the two carry the same information. Asking for the effect of age while holding date of birth fixed has no meaning, because age cannot change with date of birth held constant. When two regressors are perfectly collinear, OLS cannot separate their coefficients and the estimates do not exist. The fix is to drop one of the redundant regressors.

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
    _rng = np.random.default_rng(111)
    _n = 200
    educ = np.clip(_rng.normal(12.5, 3.5, _n), 2.0, 20.0)
    prnt = np.clip(20.0 + 4.0 * educ + _rng.normal(0.0, 15.0, _n), 0.0, None)
    wage = 5.0 + 1.20 * educ + 0.10 * prnt + _rng.normal(0.0, 6.0, _n)
    noise = np.random.default_rng(546).normal(0.0, 1.0, (_n, 30))
    return educ, noise, prnt, wage


@app.cell(hide_code=True)
def _(educ, noise, np, pd, prnt, wage):
    _n = len(wage)
    _ones = np.ones(_n)
    b_short, *_ = np.linalg.lstsq(np.column_stack([_ones, educ]), wage, rcond=None)
    b_multi, *_ = np.linalg.lstsq(np.column_stack([_ones, educ, prnt]), wage, rcond=None)
    _resid_min = wage - np.column_stack([_ones, educ, prnt]) @ b_multi
    ssr_min = float(_resid_min @ _resid_min)
    # The dial values the checkbox jumps to: the OLS estimates rounded onto
    # the slider step grids (0.1 for the intercept, 0.01 for the slopes).
    ols_dials = (
        round(float(b_multi[0]), 1),
        round(float(b_multi[1]), 2),
        round(float(b_multi[2]), 2),
    )

    _tss = float(np.sum((wage - wage.mean()) ** 2))
    _rows = []
    for _k in range(31):
        _X = np.column_stack([_ones, educ, prnt] + [noise[:, _j] for _j in range(_k)])
        _b, *_ = np.linalg.lstsq(_X, wage, rcond=None)
        _res = wage - _X @ _b
        _ssr = float(_res @ _res)
        _kk = 2 + _k
        _rows.append(
            {
                "k": _k,
                "r2": 1.0 - _ssr / _tss,
                "adj": 1.0 - (_n - 1) / (_n - _kk - 1) * _ssr / _tss,
                "ser": float(np.sqrt(_ssr / (_n - _kk - 1))),
                "b_educ": float(_b[1]),
            }
        )
    fit_path = pd.DataFrame(_rows)
    return b_multi, b_short, fit_path, ols_dials, ssr_min


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

    In the worker data both pieces can be estimated. The income coefficient in the two-regressor fit is $0.10$, and regressing parental income on years of education gives an auxiliary slope of $\hat{\delta}_1 = 4.1$, because more educated workers come from richer families. Their product is $0.10 \times 4.1 \approx 0.41$, which is exactly the gap between the single-variable slope $1.63$ and the held-income slope $1.22$.
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
