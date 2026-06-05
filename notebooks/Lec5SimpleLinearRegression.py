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

__generated_with = "0.23.6"
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: block; margin-bottom: 1.5em;">Course home</a>'),
            mo.md("# [Lecture 5](#top)"),
            mo.md("Simple Linear Regression: Estimation, Interpretation, and Fit"),
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

    The previous lectures studied one variable at a time, and then pairs of variables through covariance and correlation. We now ask a sharper question. Given two variables that move together, what single straight line best summarizes how one depends on the other?

    Take hourly wages and years of education. Lecture 1 showed that workers with more education tend to earn more, and Lecture 3 measured that kind of co-movement with covariance. A *linear regression* goes one step further and draws a line through the cloud of points, so we can read off a predicted wage for any level of education.

    We write the model for the population as

    $$ Y_i = \beta_0 + \beta_1 X_i + u_i, \qquad i = 1, \ldots, n. $$

    Here $Y_i$ is the *dependent variable*, the outcome we want to explain, which is the hourly wage of worker $i$. $X_i$ is the *independent variable*, the input we use to explain it, which is worker $i$'s years of education. The straight line $\beta_0 + \beta_1 X_i$ is the *population regression line*. Its *intercept* $\beta_0$ is the value of $Y$ the line predicts when $X = 0$, and its *slope* $\beta_1$ is the change in predicted $Y$ for a one-unit increase in $X$. The *error term* $u_i = Y_i - (\beta_0 + \beta_1 X_i)$ is the gap between worker $i$'s actual wage and the line, and it collects everything other than education that moves the wage.

    The intercept and slope are population parameters we cannot see, in the same way the population mean $\mu_X$ was hidden in Lecture 2. The next section estimates them from a sample.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Ordinary least squares

    To draw the line we need values for the intercept and slope. A natural idea is to pick the line that comes closest to the points. For a candidate line with intercept $b_0$ and slope $b_1$, the predicted wage for worker $i$ is $b_0 + b_1 X_i$, and the *residual* is the leftover gap between the actual wage and that prediction,

    $$ \hat{u}_i = Y_i - (b_0 + b_1 X_i). $$

    A line fits well when its residuals are small. Some residuals are positive and some are negative, so adding them directly lets them cancel. Instead we square each one, which makes every gap count and penalizes large misses more heavily, and then add the squares. *Ordinary least squares* chooses the intercept and slope that make this sum of squared residuals as small as possible,

    $$ \min_{b_0,\, b_1} \sum_{i=1}^{n} \hat{u}_i^2 = \min_{b_0,\, b_1} \sum_{i=1}^{n} \left(Y_i - b_0 - b_1 X_i\right)^2. $$

    The minimizing values have a closed form. The slope estimate is the sample covariance of $X$ and $Y$ divided by the sample variance of $X$, and the intercept estimate then forces the line through the point of averages,

    $$ \hat{\beta}_1 = \frac{\widehat{\text{cov}}(X, Y)}{\widehat{\text{var}}(X)}, \qquad \hat{\beta}_0 = \hat{\mu}_Y - \hat{\beta}_1 \hat{\mu}_X. $$

    The appendix derives both formulas. The slope should look familiar from Lecture 3, since covariance measures how $X$ and $Y$ move together while variance measures how much $X$ moves on its own. A positive covariance gives an upward-sloping line, a negative covariance a downward-sloping one.

    In the tool below, the points are a sample of 40 workers. Move the two sliders to set the intercept and slope of your own line, and watch the gray segments, which are the residuals, and the running sum of squared residuals. Make that sum as small as you can, then tick the box to reveal the least-squares line, the one ordinary least squares would choose.
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
def _(alt, mo, np, pd, reg_X, reg_Y, reg_b0_hat, reg_b1_hat, slr_b0, slr_b1, slr_show):
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

    Once we have the fitted line $\hat{Y}_i = \hat{\beta}_0 + \hat{\beta}_1 X_i$, the slope and intercept carry the meaning.

    When $X$ is continuous, the slope is the predicted change in $Y$ for a one-unit increase in $X$, measured in the units of $Y$. In our wage data the least-squares line is about $\hat{Y} = 7.30 + 1.25\,X$, so each additional year of schooling is associated with about \$1.25 more per hour. The intercept is the predicted wage at $X = 0$, about \$7.30 per hour, though zero years of schooling sits far outside the data, so that figure is an extrapolation rather than a description of anyone we observed.

    When $X$ is binary, taking only the values 0 and 1, the slope reads even more simply. The intercept $\hat{\beta}_0$ is the predicted $Y$ for the group with $X = 0$, and $\hat{\beta}_0 + \hat{\beta}_1$ is the predicted $Y$ for the group with $X = 1$, so the slope $\hat{\beta}_1$ is just the difference in average $Y$ between the two groups. Suppose $X$ equals 1 for female workers and 0 otherwise, and a regression of hourly wages on that indicator gives $\hat{\beta}_0 = 26$ and $\hat{\beta}_1 = -4$, both in dollars per hour. Workers with $X = 0$ are then predicted to earn \$26 per hour, and workers with $X = 1$ to earn $\hat{\beta}_0 + \hat{\beta}_1 = 22$, or \$22 per hour. The slope is the gap between the two group means, here \$4 per hour.

    One caution, which the course returns to later. These statements are about prediction and association, not cause. A positive slope on education does not by itself show that schooling raises wages, because workers with more education may differ in other ways that also affect pay. Notebook 6 makes the conditions for a causal reading precise.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Prediction

    The fitted line turns any level of education into a predicted wage. Plugging a value of $X$ into $\hat{Y} = \hat{\beta}_0 + \hat{\beta}_1 X$ gives the *fitted value*, the height of the line at that point. With our line $\hat{Y} \approx 7.30 + 1.25\,X$, three quick examples:

    $$
    \begin{aligned}
    X = 12 \text{ years} &\;\Rightarrow\; \hat{Y} = 7.30 + 1.25 \cdot 12 = \$22.30 \text{ per hour}, \\
    X = 16 \text{ years} &\;\Rightarrow\; \hat{Y} = 7.30 + 1.25 \cdot 16 = \$27.30 \text{ per hour}, \\
    X = 25 \text{ years} &\;\Rightarrow\; \hat{Y} = 7.30 + 1.25 \cdot 25 = \$38.55 \text{ per hour}.
    \end{aligned}
    $$

    Predictions come in two kinds. An *in-sample* prediction uses a value of $X$ inside the range of the data the line was built from, here roughly 8 to 20 years of schooling. The first two examples above are in-sample. An *out-of-sample* prediction uses a value of $X$ outside that range, which is called *extrapolation*. The third example, $X = 25$ years, sits well outside the data. Extrapolation is riskier, because nothing in the data tells us the straight-line pattern continues past the values we observed. The line will happily report a wage for 30 years of schooling or for 2, but we have no evidence the relationship stays linear that far out.

    The diagram below sketches the line: the solid middle is the part backed by data, and the dashed tails are extrapolation.
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
    ## 5. Measuring fit

    A line can be the best of all straight lines and still predict poorly, if the points scatter far from it. Two measures summarize how well the fitted line explains the data.

    The first splits the variation in $Y$ into a part the line explains and a part it does not. Write $\hat{\mu}_Y$ for the sample mean of $Y$. The *total sum of squares* adds up how far each $Y_i$ falls from that mean, the *explained sum of squares* adds up how far each fitted value falls from it, and the *sum of squared residuals* adds up the leftover gaps,

    $$ \text{TSS} = \sum_{i=1}^{n}(Y_i - \hat{\mu}_Y)^2, \qquad \text{ESS} = \sum_{i=1}^{n}(\hat{Y}_i - \hat{\mu}_Y)^2, \qquad \text{SSR} = \sum_{i=1}^{n}\hat{u}_i^2. $$

    These three satisfy $\text{TSS} = \text{ESS} + \text{SSR}$. The *R-squared* is the share of the total variation the line explains,

    $$ R^2 = \frac{\text{ESS}}{\text{TSS}} = 1 - \frac{\text{SSR}}{\text{TSS}}. $$

    It runs from 0 to 1. An $R^2$ of 0 means $X$ explains none of the variation in $Y$ and the fitted line is flat at $\hat{\mu}_Y$. An $R^2$ of 1 means every point lies exactly on the line. In our wage data $R^2$ is about $0.72$, so education explains roughly seventy percent of the variation in wages across these workers.

    The second measure reports the typical size of a residual in the units of $Y$. The *standard error of the regression* is

    $$ \text{SER} = \sqrt{\frac{\text{SSR}}{n - 2}}, $$

    the square root of the average squared residual, dividing by $n - 2$ rather than $n$ because estimating the intercept and slope used up two pieces of information. For our wage line the SER is about \$2.94, so a typical worker's wage lands within about three dollars of the line. A larger $R^2$ and a smaller SER both signal a tighter fit.

    Move the slider below to change how far the points scatter around a fixed true line. As the scatter shrinks the points hug the line, $R^2$ climbs toward 1, and the SER falls toward 0. As the scatter grows the reverse happens.
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
    _tss = float(np.sum((_Y - _ybar) ** 2))
    _ssr = float(np.sum((_Y - _yhat) ** 2))
    _ess = _tss - _ssr
    _r2 = 1.0 - _ssr / _tss
    _ser = float(np.sqrt(_ssr / (_n - 2)))

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

    _body = (
        rf"With this much scatter, $R^2 = {_r2:.2f}$ and the SER is \${_ser:.2f}. "
        rf"The line explains {100 * _r2:.0f}% of the variation in wages "
        rf"($\text{{ESS}} = {_ess:.0f}$, $\text{{TSS}} = {_tss:.0f}$, $\text{{SSR}} = {_ssr:.0f}$). "
        rf"Tighten the scatter and $R^2$ rises toward 1 while the SER falls toward 0."
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
            "**Key terms covered:** linear regression, dependent variable, "
            "independent variable, population regression line, intercept, slope, "
            "error term, ordinary least squares, residual, fitted value, "
            "in-sample prediction, out-of-sample prediction, extrapolation, "
            "R-squared, total sum of squares, explained sum of squares, sum of "
            "squared residuals, standard error of the regression.\n\n"
            "**Key concepts covered:** the least-squares criterion, the OLS slope "
            "as covariance over variance, interpreting the slope for continuous "
            "and binary X, the difference between prediction and causation, and "
            "splitting the variation in Y into explained and unexplained parts."
        ),
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
