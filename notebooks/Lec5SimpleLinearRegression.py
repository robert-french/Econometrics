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
    app_title="Lecture 5: Simple Linear Regression",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: flex; align-items: center; gap: 0.5em; margin-bottom: 0.5em;"><img src="https://robert-french.github.io/Econometrics/LMU_SquareOrig.png" alt="" style="height: 1.6em; width: auto; display: block;"><span>ECON 3300 Course home</span></a>'),
            mo.md("# [Lecture 5](#top)"),
            mo.md("**Simple Linear Regression: Estimation, Interpretation, and Fit**"),
            mo.nav_menu(
                {
                    "#sec1": "1. The regression model",
                    "#sec2": "2. Ordinary least squares",
                    "#sec3": "3. Interpreting the slope",
                    "#sec4": "4. Prediction",
                    "#sec5": "5. Measuring fit",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec4EstimationHypothesisTestingAndConfidenceIntervals.html" target="_self">← Lecture 4</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec6OLSAssumptionsForCausalInference.html" target="_self">Lecture 6 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 5: Simple Linear Regression
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contents

    1. [The regression model](#sec1)
    2. [Ordinary least squares](#sec2)
    3. [Interpreting the slope](#sec3)
    4. [Prediction](#sec4)
    5. [Measuring fit](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. The regression model

    In Lecture 2, we introduced covariance and correlation as ways to describe how two random variables move together. In this lecture, we use those ideas to ask a new question. Given two variables that move together, what single straight line best summarizes their relationship?

    Consider hourly wages and years of education. In Lecture 1, we saw that workers with more education tend to earn more. In Lecture 3, we used covariance to measure that kind of co-movement. A *linear regression* goes one step further. It represents the relationship between wages and education with a single straight line that allows us to predict a worker's wage from their years of education.

    We write the population regression model as

    $$
    Y_i = \beta_0 + \beta_1 X_i + u_i, \qquad i = 1, \ldots, n.
    $$

    Here $Y_i$ is the *dependent variable*, or the outcome we want to explain. In this example, $Y_i$ is worker $i$'s hourly wage. The variable $X_i$ is the *independent variable*, or the variable we use to explain the outcome. Here, $X_i$ is worker $i$'s years of education. $i$ is simply an index that refers to a single worker among $1, \ldots, n$ possible workers.

    The expression $\beta_0 + \beta_1 X$ is the *population regression line*. The *intercept* $\beta_0$ is the value of the population regression line when $X = 0$. The *slope* $\beta_1$ describes how $Y$ changes when $X$ increases by one unit, holding the error term fixed. In the wage and education example, $\beta_1$ is the change in hourly wages from one more year of education, holding fixed the other determinants of wages in $u_i$.

    The term $u_i$ is the *error term*. It represents the part of worker $i$'s wage that is not explained by education in the population regression model. In other words, it includes all the other factors, besides education, that affect wages.

    The intercept $\beta_0$ and slope $\beta_1$ are population parameters. We cannot observe them directly, just as we could not directly observe the population mean $\mu_X$ in Lecture 2. Moreover, because $\beta_0$ and $\beta_1$ are population parameters, we cannot use them to compute the true error term $u_i$. The next section shows how to estimate the population parameters $\beta_0$ and $\beta_1$ using a sample.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Ordinary least squares

    The population regression model contains two unknown parameters, the intercept $\beta_0$ and the slope $\beta_1$. If we knew these values, we would know the population regression line. But in practice, we only have a sample of observations on wages and education. We therefore use the sample to estimate the population line.

    The basic idea is simple. We draw a line through the sample data and use that line as our estimate of the population regression line. The intercept and slope of the sample line are our estimates of $\beta_0$ and $\beta_1$. To draw this line, we need a rule for choosing among all possible lines. A natural rule is to choose the line that comes closest to the data points. For a candidate line with intercept $b_0$ and slope $b_1$, the predicted value of $Y$ for observation $i$ is $b_0 + b_1 X_i$. The *residual* is the gap between the actual value of $Y_i$ and the value predicted by this candidate line for observation $i$, $Y_i - (b_0 + b_1 X_i)$.<sup><a id="fnref1" href="#fn1">1</a></sup>

    A line fits the sample well when its residuals are small. Some residuals are positive and some are negative, so adding them directly would allow them to cancel out. Instead, we square each residual and then add the squared residuals across all observations. Squaring makes every residual count as positive and gives extra weight to large residuals.

    *Ordinary least squares*, or OLS, chooses the intercept and slope that make the *sum of squared residuals* as small as possible,

    $$
    \min_{b_0,, b_1} \sum_{i=1}^{n} \left(Y_i - b_0 - b_1 X_i\right)^2.
    $$

    The values of $b_0$ and $b_1$ that solve this problem are called the OLS estimates. We write them as $\hat{\beta}_0$ and $\hat{\beta}_1$. These estimates define the fitted regression line. The predicted value from this fitted line is called the *fitted value*,

    $$
    \hat{Y}_i = \hat{\beta}_0 + \hat{\beta}_1 X_i.
    $$

    The residuals from the fitted regression line are called the *OLS residuals*. For observation $i$, the OLS residual is the actual value of $Y_i$ minus the fitted value $\hat{Y}_i$,

    $$
    \hat{u}_i = Y_i - \hat{Y}_i = Y_i - (\hat{\beta}_0 + \hat{\beta}_1 X_i).
    $$

    The OLS estimates have convenient solutions. The slope estimate is the sample covariance of $X$ and $Y$ divided by the sample variance of $X$,

    $$
    \hat{\beta}_1 = \frac{\widehat{\text{cov}}(X, Y)}{\widehat{\text{var}}(X)}.
    $$

    The intercept estimate then makes the fitted line pass through the point of sample averages,

    $$
    \hat{\beta}_0 = \hat{\mu}_Y - \hat{\beta}_1 \hat{\mu}_X.
    $$

    The formula for the slope should look familiar from Lecture 3. Recall that the covariance measures how $X$ and $Y$ move together, while the variance measures how much $X$ moves on its own. When the covariance between $X$ and $Y$ is positive, the fitted line slopes upward. When the covariance is negative, the fitted line slopes downward. The appendix derives both of these formulas.

    In the interactive plot below, the data points represent a sample of 40 workers from our example relating wages and years of education. Move the two sliders to set the intercept and slope of your own line. Watch the gray segments, which show the residuals from your line. Also notice the sum of squared residuals computed beneath the plot. Try to make that sum as small as possible. Then tick the box to reveal the least-squares line, which is the line ordinary least squares chooses.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    _rng = np.random.default_rng(5)
    reg_n = 40
    reg_X = _rng.uniform(8.0, 20.0, reg_n)
    reg_noise = _rng.normal(0.0, 1.0, reg_n)
    reg_b0_true = 8.0
    reg_b1_true = 1.2
    reg_Y = reg_b0_true + reg_b1_true * reg_X + 3.0 * reg_noise
    reg_b1_hat = float(np.cov(reg_X, reg_Y, ddof=1)[0, 1] / np.var(reg_X, ddof=1))
    reg_b0_hat = float(reg_Y.mean() - reg_b1_hat * reg_X.mean())
    return (
        reg_X,
        reg_Y,
        reg_b0_hat,
        reg_b0_true,
        reg_b1_hat,
        reg_b1_true,
        reg_noise,
    )


@app.cell(hide_code=True)
def _(mo):
    slr_b1 = mo.ui.slider(
        start=-1.0, stop=4.0, step=0.1, value=0.5,
        label=r"Slope $b_1$", show_value=True,
    )
    slr_b0 = mo.ui.slider(
        start=-5.0, stop=25.0, step=0.5, value=15.0,
        label=r"Intercept $b_0$", show_value=True,
    )
    slr_show = mo.ui.checkbox(value=False, label="Show the least-squares line")
    mo.vstack([slr_b0, slr_b1, slr_show])
    return slr_b0, slr_b1, slr_show


@app.cell(hide_code=True)
def _(
    alt,
    mo,
    np,
    pd,
    reg_X,
    reg_Y,
    reg_b0_hat,
    reg_b1_hat,
    slr_b0,
    slr_b1,
    slr_show,
):
    _b0 = float(slr_b0.value)
    _b1 = float(slr_b1.value)
    _xdom = [7.0, 21.0]
    _ydom = [0.0, 45.0]
    _xline = np.array([7.0, 21.0])

    _pts = pd.DataFrame({"x": reg_X, "y": reg_Y, "fit": _b0 + _b1 * reg_X})
    _user = pd.DataFrame({"x": _xline, "y": _b0 + _b1 * _xline})

    _resid = (
        alt.Chart(_pts)
        .mark_rule(color="#9aa5b1", opacity=0.7, size=1, clip=True)
        .encode(
            x=alt.X("x:Q", title="Years of education", scale=alt.Scale(domain=_xdom, nice=False)),
            y=alt.Y("y:Q", title="Hourly wage (USD)", scale=alt.Scale(domain=_ydom, nice=False)),
            y2="fit:Q",
        )
    )
    _scatter = (
        alt.Chart(_pts)
        .mark_circle(color="#1f4e79", opacity=0.7, size=60, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _line = (
        alt.Chart(_user)
        .mark_line(color="#111827", size=2, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _layers = [_resid, _scatter, _line]

    _ssr_user = float(np.sum((reg_Y - (_b0 + _b1 * reg_X)) ** 2))
    _ssr_ols = float(np.sum((reg_Y - (reg_b0_hat + reg_b1_hat * reg_X)) ** 2))

    if slr_show.value:
        _ols = pd.DataFrame({"x": _xline, "y": reg_b0_hat + reg_b1_hat * _xline})
        _layers.append(
            alt.Chart(_ols)
            .mark_line(color="orange", size=2.5, clip=True)
            .encode(x="x:Q", y="y:Q")
        )

    _chart = alt.layer(*_layers).properties(
        width=560, height=340, title="Fit a line by setting the slope and intercept"
    )

    _body = (
        rf"Your line is $\hat{{Y}} = {_b0:.1f} + {_b1:.2f}\,X$, with a sum of squared "
        rf"residuals of {_ssr_user:.0f}. "
    )
    if slr_show.value:
        _body += (
            rf"The least-squares line is $\hat{{Y}} = {reg_b0_hat:.2f} + {reg_b1_hat:.2f}\,X$, "
            rf"with a sum of squared residuals of {_ssr_ols:.0f}, the smallest any line can reach."
        )
    else:
        _body += "Tick the box to reveal the least-squares line and its sum of squared residuals."
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
    <a id="sec3"></a>
    ## 3. Interpreting the slope

    Let's now consider how to interpret the fitted line, $\hat{Y}_i = \hat{\beta}_0 + \hat{\beta}_1 X_i$.

    ### <span style="color:#0b68cb">When X is continuous</span>

    When $X$ is continuous, the slope $\hat{\beta}_1$ is the expected, or average, change in $Y$ associated with a one-unit increase in $X$. The units of the slope are the same as the units of $Y$. For example, if $Y$ were measured in dollars, then we should interpret $\hat{\beta}_1$ in dollar terms. In our wage and education example, the least-squares line is approximately

    $$
    \hat{Y} = 7.30 + 1.25X.
    $$

    This means that each additional year of schooling is associated with a wage that is about $1.25 higher per hour on average. The intercept is the predicted wage when $X = 0$. Here, that value is about $7.30 per hour. Since zero years of schooling lies far outside the range of the data, this intercept is an extrapolation rather than a description of workers we actually observe.

    ### <span style="color:#0b68cb">When X is binary</span>

    When $X$ is binary, meaning it only takes the values 0 and 1, the slope has an especially simple interpretation. The intercept $\hat{\beta}_0$ is the predicted value of $Y$ for observations with $X = 0$. The value $\hat{\beta}_0 + \hat{\beta}_1$ is the predicted value of $Y$ for observations with $X = 1$. And the estimate of $\hat{\beta}_1$ is therefore the difference in average $Y$ between the two groups.

    For example, suppose $X$ equals 1 for female workers and 0 otherwise, and a regression of hourly wages on this indicator variable gives $\hat{\beta}_0 = 26$ and $\hat{\beta}_1 = -4$, both measured in dollars per hour. Workers with $X = 0$ are predicted to earn $26 per hour. Workers with $X = 1$ are predicted to earn

    $$
    \hat{\beta}_0 + \hat{\beta}_1 = 26 - 4 = 22,
    $$

    or $22 per hour. The group with $X = 1$ therefore has an average wage that is $4 per hour lower than the group with $X = 0$.

    Importantly, note that these interpretations describe prediction and association, not causation. A positive slope on education does not by itself show that schooling raises wages, because workers with more education may differ in other ways that also affect pay. Notebook 6 explains the conditions needed to interpret a regression slope causally.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    <a id="sec4"></a>

    ## 4. Prediction

    Once we estimate a regression line, we can use it to make predictions. The fitted line turns a value of $X$ into a predicted value of $Y$. For an observation in the sample, this predicted value is the fitted value,

    $$
    \hat{Y}_i = \hat{\beta}_0 + \hat{\beta}_1 X_i.
    $$

    We can also use the same line to predict $Y$ at other values of $X$. In the wage and education example, the fitted line is approximately

    $$
    \hat{Y} = 7.30 + 1.25X.
    $$

    Plugging in different values of $X$ gives different predicted wages,

    $$
    \begin{aligned}
    X = 12 \text{ years} &;\Rightarrow; \hat{Y} = 7.30 + 1.25 \cdot 12 = \text{\$}22.30 \text{ per hour}, \\
    X = 16 \text{ years} &;\Rightarrow; \hat{Y} = 7.30 + 1.25 \cdot 16 = \text{\$}27.30 \text{ per hour}, \\
    X = 25 \text{ years} &;\Rightarrow; \hat{Y} = 7.30 + 1.25 \cdot 25 = \text{\$}38.55 \text{ per hour}.
    \end{aligned}
    $$

    Predictions are more reliable when they use values of $X$ similar to those observed in the sample. An *in-sample prediction* uses a value of $X$ inside the range of the data used to estimate the line. In this example, the observed values of schooling run from roughly 8 to 20 years, so the predictions for $X = 12$ and $X = 16$ are in-sample predictions.

    An *out-of-sample prediction* uses a value of $X$ outside the range of the data. This is called *extrapolation*. The prediction for $X = 25$ years is an extrapolation because it lies well outside the observed range of schooling. Extrapolation is risky because the sample does not tell us whether the straight-line relationship continues beyond the values we observed. The regression line can produce a predicted wage for 25, 30, or even 2 years of schooling, but those predictions rely on extending the line beyond the support of the data.

    The diagram below illustrates this distinction. The solid part of the line shows predictions supported by the observed data, while the dashed tails show extrapolations beyond the observed range.
    """)
    return


@app.cell(hide_code=True)
def _(alt, pd, reg_b0_hat, reg_b1_hat):
    def _yfn(x):
        return reg_b0_hat + reg_b1_hat * x

    _xdom = [0.0, 26.0]
    _ydom = [0.0, 45.0]
    _xscale = alt.Scale(domain=_xdom, nice=False)
    _yscale = alt.Scale(domain=_ydom, nice=False)

    _left = pd.DataFrame({"x": [0.0, 8.0], "y": [_yfn(0.0), _yfn(8.0)]})
    _mid = pd.DataFrame({"x": [8.0, 20.0], "y": [_yfn(8.0), _yfn(20.0)]})
    _right = pd.DataFrame({"x": [20.0, 26.0], "y": [_yfn(20.0), _yfn(26.0)]})

    _left_dash = (
        alt.Chart(_left)
        .mark_line(color="#1f4e79", strokeDash=[4, 3], size=2)
        .encode(
            x=alt.X("x:Q", title="Years of education", scale=_xscale),
            y=alt.Y("y:Q", title=None, scale=_yscale, axis=None),
        )
    )
    _solid = (
        alt.Chart(_mid)
        .mark_line(color="#1f4e79", size=2.5)
        .encode(x="x:Q", y="y:Q")
    )
    _right_dash = (
        alt.Chart(_right)
        .mark_line(color="#1f4e79", strokeDash=[4, 3], size=2)
        .encode(x="x:Q", y="y:Q")
    )

    _labels = pd.DataFrame({
        "x": [4.0, 14.0, 23.0],
        "y": [44.0, 44.0, 44.0],
        "label": ["extrapolation", "observed range", "extrapolation"],
    })
    _text = (
        alt.Chart(_labels)
        .mark_text(color="#6b7280", fontSize=11, baseline="top")
        .encode(x="x:Q", y="y:Q", text="label:N")
    )

    alt.layer(_left_dash, _solid, _right_dash, _text).properties(
        width=560, height=120
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    <a id="sec5"></a>

    ## 5. Measuring fit

    OLS gives us the best-fitting straight line, but that does not mean the line predicts the data well. If the points are scattered far from the line, even the best straight line may leave large prediction errors. We therefore need measures of how closely the fitted line matches the data.

    The first measure is the *R-squared* ($R^2$). It is based on splitting the variation in $Y$ into two parts. One part is accounted for by the fitted line, and the other part is left in the residuals. Let $\hat{\mu}_Y$ be the sample mean of $Y$. The *total sum of squares* (TSS) measures how far the observed values of $Y$ are from their sample mean. The *explained sum of squares* (ESS) measures how far the fitted values are from that same mean. And the *sum of squared residuals* (SSR) measures the variation left over after fitting the line,


    $$
    \text{TSS} = \sum_{i=1}^{n}(Y_i - \hat{\mu}_Y)^2, \quad \text{ESS} = \sum_{i=1}^{n}(\hat{Y}_i - \hat{\mu}_Y)^2, \quad  \text{SSR} = \sum_{i=1}^{n}\hat{u}_i^2.
    $$

    These three quantities satisfy $\text{TSS} = \text{ESS} + \text{SSR}$. The $R^2$ is the share of the total variation in $Y$ accounted for by the fitted line,

    $$
    R^2 = \frac{\text{ESS}}{\text{TSS}} = 1 - \frac{\text{SSR}}{\text{TSS}}.
    $$

    The value of $R^2$ runs from 0 to 1. An $R^2$ of 0 means that $X$ accounts for none of the variation in $Y$, so the fitted line is flat at $\hat{\mu}_Y$. An $R^2$ of 1 means that every point lies exactly on the fitted line. In the wage and education example, $R^2$ is about $0.72$, so education accounts for roughly seventy percent of the variation in wages in this sample.

    The second measure is the *standard error of the regression* (SER). While $R^2$ is a share, the standard error of the regression is measured in the units of $Y$. It reports the typical size of a residual,

    $$
    \text{SER} = \sqrt{\frac{\text{SSR}}{n - 2}}.
    $$

    This formula takes the square root of the average squared residual. We divide by $n - 2$ rather than $n$ because estimating the intercept and slope uses up two pieces of information. In the wage and education example, the SER is about $2.94. Since wages are measured in dollars per hour, this means that a typical wage is about three dollars per hour away from the fitted line.

    A larger $R^2$ and a smaller SER both indicate a tighter fit. Move the slider below to change how far the points scatter around a fixed true line. As the scatter shrinks, the points move closer to the line, $R^2$ rises toward 1, and the SER falls toward 0. As the scatter grows, the reverse happens.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    fit_noise = mo.ui.slider(
        start=0.5, stop=9.0, step=0.5, value=3.0,
        label="Spread of points around the line", show_value=True,
    )
    fit_noise
    return (fit_noise,)


@app.cell(hide_code=True)
def _(alt, fit_noise, mo, np, pd, reg_X, reg_b0_true, reg_b1_true, reg_noise):
    _Y = reg_b0_true + reg_b1_true * reg_X + float(fit_noise.value) * reg_noise
    _b1 = float(np.cov(reg_X, _Y, ddof=1)[0, 1] / np.var(reg_X, ddof=1))
    _b0 = float(_Y.mean() - _b1 * reg_X.mean())
    _yhat = _b0 + _b1 * reg_X
    _ybar = float(_Y.mean())
    _n = len(reg_X)
    _dof = _n - 2
    _tss = float(np.sum((_Y - _ybar) ** 2))
    _ssr = float(np.sum((_Y - _yhat) ** 2))
    _ess = _tss - _ssr
    _r2 = 1.0 - _ssr / _tss
    _ser = float(np.sqrt(_ssr / _dof))

    _xdom = [7.0, 21.0]
    _ydom = [-5.0, 55.0]
    _xline = np.array([7.0, 21.0])
    _pts = pd.DataFrame({"x": reg_X, "y": _Y})
    _fit = pd.DataFrame({"x": _xline, "y": _b0 + _b1 * _xline})
    _meanline = pd.DataFrame({"y": [_ybar]})

    _scatter = (
        alt.Chart(_pts)
        .mark_circle(color="#1f4e79", opacity=0.6, size=55)
        .encode(
            x=alt.X("x:Q", title="Years of education", scale=alt.Scale(domain=_xdom)),
            y=alt.Y("y:Q", title="Hourly wage (USD)", scale=alt.Scale(domain=_ydom)),
        )
    )
    _mean = (
        alt.Chart(_meanline)
        .mark_rule(color="#9aa5b1", strokeDash=[4, 3], size=1.5)
        .encode(y="y:Q")
    )
    _line = (
        alt.Chart(_fit)
        .mark_line(color="#1f4e79", size=2.5, clip=True)
        .encode(x="x:Q", y="y:Q")
    )
    _chart = alt.layer(_scatter, _mean, _line).properties(
        width=560, height=340, title="How scatter around the line drives R-squared and the SER"
    )

    _text_body = (
        rf"With this much scatter, "
        rf"$R^2 = \text{{ESS}}/\text{{TSS}} = {_ess:.0f}/{_tss:.0f} = {_r2:.2f}$, "
        rf"equivalently $R^2 = 1 - \text{{SSR}}/\text{{TSS}} = 1 - {_ssr:.0f}/{_tss:.0f} = {_r2:.2f}$. "
        rf"The standard error of the regression is "
        rf"$\text{{SER}} = \sqrt{{\text{{SSR}}/(n-2)}} = \sqrt{{{_ssr:.0f}/{_dof}}} = \${_ser:.2f}$. "
        rf"Tighten the scatter and $R^2$ rises toward 1 while the SER falls toward 0."
    )
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 1rem;max-width:560px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _text_body
        + "</span>"
    )

    mo.vstack([_chart, _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** linear regression, dependent variable, "
            "independent variable, population regression line, intercept, slope, "
            "error term, ordinary least squares, residual, fitted value, "
            "in-sample prediction, out-of-sample prediction, extrapolation, "
            "R-squared, total sum of squares, explained sum of squares, sum of "
            "squared residuals, standard error of the regression.\n\n"
            "**Concepts:** the least-squares criterion, the OLS slope "
            "as covariance over variance, interpreting the slope for continuous "
            "and binary X, the difference between prediction and causation, and "
            "splitting the variation in Y into explained and unexplained parts."
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

        **Deriving the OLS estimators.**

        Ordinary least squares chooses $\hat{\beta}_0$ and $\hat{\beta}_1$ to minimize the sum of squared residuals,

        $$ \text{SSR}(\hat{\beta}_0, \hat{\beta}_1) = \sum_{i=1}^{n}\left(Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i\right)^2. $$

        At the minimum the two partial derivatives are zero,

        $$ \frac{\partial \text{SSR}}{\partial \hat{\beta}_0} = -2\sum_{i=1}^{n}\left(Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i\right) = 0, \qquad \frac{\partial \text{SSR}}{\partial \hat{\beta}_1} = -2\sum_{i=1}^{n} X_i\left(Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i\right) = 0. $$

        Dividing each condition by $-2$ gives two equations the OLS residuals must satisfy, where $\hat{u}_i = Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i$,

        $$ \text{(i)} \quad \sum_{i=1}^{n} \hat{u}_i = 0, \qquad \text{(ii)} \quad \sum_{i=1}^{n} X_i\, \hat{u}_i = 0. $$

        Expanding equation (i) gives $\sum Y_i - n\hat{\beta}_0 - \hat{\beta}_1 \sum X_i = 0$. Dividing by $n$ and using the definitions $\hat{\mu}_X = \tfrac{1}{n}\sum X_i$ and $\hat{\mu}_Y = \tfrac{1}{n}\sum Y_i$,

        $$ \hat{\beta}_0 = \hat{\mu}_Y - \hat{\beta}_1 \hat{\mu}_X. $$

        The fitted line therefore passes through the point of averages $(\hat{\mu}_X, \hat{\mu}_Y)$. Substituting this expression for $\hat{\beta}_0$ into equation (ii),

        $$ \sum_{i=1}^{n} X_i \left( Y_i - \hat{\mu}_Y + \hat{\beta}_1 \hat{\mu}_X - \hat{\beta}_1 X_i \right) = 0, $$

        and grouping the slope terms on one side gives

        $$ \sum_{i=1}^{n} X_i (Y_i - \hat{\mu}_Y) = \hat{\beta}_1 \sum_{i=1}^{n} X_i (X_i - \hat{\mu}_X). $$

        Both sums simplify into symmetric form. Because $\sum (X_i - \hat{\mu}_X) = 0$, we can subtract $\hat{\mu}_X \sum (X_i - \hat{\mu}_X) = 0$ on each side without changing anything:

        $$ \sum X_i (Y_i - \hat{\mu}_Y) = \sum (X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y), \qquad \sum X_i (X_i - \hat{\mu}_X) = \sum (X_i - \hat{\mu}_X)^2. $$

        Solving for the slope,

        $$ \hat{\beta}_1 = \frac{\sum_{i=1}^{n}(X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y)}{\sum_{i=1}^{n}(X_i - \hat{\mu}_X)^2} = \frac{\widehat{\text{cov}}(X, Y)}{\widehat{\text{var}}(X)}. $$

        Both estimators are exactly the formulas used in Section 2.

        **The variance decomposition: $\text{TSS} = \text{ESS} + \text{SSR}$.**

        Section 5 used this identity but did not prove it. Write each deviation of $Y_i$ from its mean as the sum of a residual and the line's deviation from the mean,

        $$ Y_i - \hat{\mu}_Y = \hat{u}_i + \left(\hat{Y}_i - \hat{\mu}_Y\right). $$

        Squaring and summing,

        $$ \text{TSS} = \sum_{i=1}^{n}\hat{u}_i^2 + 2\sum_{i=1}^{n}\hat{u}_i\left(\hat{Y}_i - \hat{\mu}_Y\right) + \sum_{i=1}^{n}\left(\hat{Y}_i - \hat{\mu}_Y\right)^2 = \text{SSR} + 2\,C + \text{ESS}, $$

        where the cross term is $C = \sum \hat{u}_i \hat{Y}_i - \hat{\mu}_Y \sum \hat{u}_i$. The OLS first-order conditions above already gave $\sum \hat{u}_i = 0$ from (i) and $\sum X_i \hat{u}_i = 0$ from (ii). Substituting $\hat{Y}_i = \hat{\beta}_0 + \hat{\beta}_1 X_i$,

        $$ \sum_{i=1}^{n} \hat{u}_i \hat{Y}_i = \hat{\beta}_0 \sum_{i=1}^{n} \hat{u}_i + \hat{\beta}_1 \sum_{i=1}^{n} X_i \hat{u}_i = 0. $$

        Both pieces of $C$ vanish, so $C = 0$ and

        $$ \text{TSS} = \text{ESS} + \text{SSR}. $$

        This is the algebraic identity behind $R^2 = \text{ESS}/\text{TSS} = 1 - \text{SSR}/\text{TSS}$.
        """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** These residuals differ from the error terms in the population model. The error term $u_i$ is defined using the true population regression line, while a residual is defined using a line drawn through the sample data. <a href="#fnref1" title="Back to text">&#8617;</a></span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec4EstimationHypothesisTestingAndConfidenceIntervals.html" target="_self">← Lecture 4</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec6OLSAssumptionsForCausalInference.html" target="_self">Lecture 6 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
