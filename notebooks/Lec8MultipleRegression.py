# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "numpy",
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
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go

    return go, mo, np


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

    Every property in Lecture 7 rested on the first least squares assumption, that the conditional mean of the error given $X$ is zero. That assumption fails whenever a variable left out of the regression both belongs in the error and moves with education. When the omitted variable is correlated with $X$, the error is correlated with $X$, written $\operatorname{cov}(X,u) \neq 0$, and then $\mathbb{E}[u\mid X]\neq 0$. The estimate no longer centers on the true slope. This is *omitted variable bias*.

    With such a variable left out, the slope estimate converges not to $\beta_1$ but to

    $$ \hat{\beta}_1 \overset{p}{\to} \beta_1 + \operatorname{corr}(X,u)\cdot\frac{\sigma_u}{\sigma_X} = \beta_1 + \rho_{Xu}\,\frac{\sigma_u}{\sigma_X}. $$

    The second term is the bias, and its sign is the sign of the correlation between $X$ and the omitted part of the error. Two conditions are both needed for the bias to appear. The omitted variable must be correlated with $X$, and it must affect $Y$ so that it carries real weight inside the error. If either fails, the bias term is zero and the estimate stays on target.

    Return to the wage regression. Ability is left out of the error, and it raises both schooling and earnings, so education and the error are positively correlated. The bias term is then positive, and the estimated return to schooling comes out too high, because we credit schooling with part of what is really the payoff to ability.

    A second case is new housing and rents. Let $Y$ be local home prices and $X$ the number of new units built. Developers build more when interest rates are low, and low rates also raise demand and push prices up, so the omitted interest-rate conditions are positively correlated with building. The estimated effect of new supply on prices is biased upward for the same reason.

    Omitted variable bias is why a single explanatory variable is rarely enough for a causal claim. Adding more variables to the regression lets a factor like ability be held constant instead of left in the error. That is the idea behind multiple regression, and the rest of this lecture builds it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. The multiple regression model

    The way to stop a variable from biasing the slope is to bring it into the regression. A *multiple regression model* relates the outcome to several explanatory variables at once,

    $$
    Y_i = \beta_0 + \beta_1 X_{1i} + \beta_2 X_{2i} + \dots + \beta_k X_{ki} + u_i, \qquad i = 1, \dots, n.
    $$

    Each $X_{ji}$ is one of the $k$ regressors measured for observation $i$, and $u_i$ holds everything still left out. The population regression function is the conditional mean of $Y$ given all the regressors,

    $$
    \mathbb{E}[Y \mid X_1 = x_1, \dots, X_k = x_k] = \beta_0 + \beta_1 x_1 + \dots + \beta_k x_k.
    $$

    Each slope now carries a *ceteris paribus* meaning, which is Latin for ''other things equal''. The coefficient $\beta_j$ is the change in $Y$ for a one-unit increase in $X_j$ when every other regressor is held fixed. Take the test-score example with two regressors, class size and parental income. Here $\beta_1$ is the change in a district's average test score for one more student per teacher among districts with the same parental income. The phrase ''among districts with the same parental income'' is what the single-variable slope could not deliver, because there income was free to move along with class size.

    With one regressor the fitted model is a line. With two regressors it is a plane, and each slope is the tilt of that plane along one axis. The plot below shows the test-score data in three dimensions. Drag to rotate it, then add parental income as a second regressor and watch the fitted line open into a plane.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    plane_box = mo.ui.checkbox(value=False, label="Include parental income")
    mo.vstack(
        [
            mo.md("Drag the figure to rotate it. Toggle parental income to turn the fitted line into a plane."),
            plane_box,
        ]
    )
    return (plane_box,)


@app.cell(hide_code=True)
def _(cs, go, mo, np, plane_box, prnt, ts):
    _Xs = np.column_stack([np.ones(len(ts)), cs])
    _bs, *_ = np.linalg.lstsq(_Xs, ts, rcond=None)
    _Xm = np.column_stack([np.ones(len(ts)), cs, prnt])
    _bm, *_ = np.linalg.lstsq(_Xm, ts, rcond=None)

    _csg = np.array([float(cs.min()), float(cs.max())])
    _png = np.array([float(prnt.min()), float(prnt.max())])

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter3d(
            x=cs, y=prnt, z=ts, mode="markers",
            marker=dict(size=3, color="#1f4e79", opacity=0.7),
        )
    )
    if plane_box.value:
        _gz = _bm[0] + _bm[1] * _csg[None, :] + _bm[2] * _png[:, None]
        _fig.add_trace(
            go.Surface(
                x=_csg, y=_png, z=_gz, opacity=0.6, showscale=False,
                colorscale=[[0, "#f59e0b"], [1, "#f59e0b"]],
            )
        )
    else:
        _ym = float(prnt.mean())
        _zl = _bs[0] + _bs[1] * _csg
        _fig.add_trace(
            go.Scatter3d(
                x=_csg, y=[_ym, _ym], z=_zl, mode="lines",
                line=dict(color="#f59e0b", width=7),
            )
        )
    _fig.update_layout(
        width=620, height=480, margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        scene=dict(
            xaxis_title="Class size", yaxis_title="Parental income",
            zaxis_title="Test score",
            camera=dict(eye=dict(x=1.7, y=1.5, z=0.7)),
        ),
    )

    if plane_box.value:
        _body = (
            f"Adding parental income turns the fit into a plane. Holding income fixed, the "
            f"class-size slope flattens to about {_bm[1]:.1f} points per student, and the plane "
            f"tilts upward with parental income. Each slope is the tilt of the plane along one "
            f"axis, which is the ceteris paribus effect of that variable."
        )
    else:
        _body = (
            f"With class size as the only regressor, the fit is a line with a slope of about "
            f"{_bs[1]:.1f} points per student. The line ignores parental income, so it holds at "
            f"one height across the whole income axis."
        )
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 1rem;max-width:560px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _body + "</span>"
    )
    mo.vstack([mo.ui.plotly(_fig), _caption])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Estimating the model with OLS

    We estimate the coefficients the same way as with one regressor, by choosing the values that make the fitted model miss the data by as little as possible. *Ordinary least squares* picks the intercept and slopes $\hat{\beta}_0, \hat{\beta}_1, \dots, \hat{\beta}_k$ that minimize the sum of squared residuals,

    $$
    \min_{b_0, b_1, \dots, b_k} \sum_{i=1}^{n} \left( Y_i - b_0 - b_1 X_{1i} - \dots - b_k X_{ki} \right)^2.
    $$

    The *predicted value* for observation $i$ is $\hat{Y}_i = \hat{\beta}_0 + \hat{\beta}_1 X_{1i} + \dots + \hat{\beta}_k X_{ki}$, and the *residual* is the gap between the actual and the predicted outcome, $\hat{u}_i = Y_i - \hat{Y}_i$.

    The test-score example shows what changes when a second regressor enters. Regressing a district's average test score on its class size alone gives

    $$
    \widehat{TestScore} = 698.9 - 2.28 \, ClassSize.
    $$

    Adding the parental income of the district's students, measured in thousands of dollars, gives

    $$
    \widehat{TestScore} = 698.9 - 1.10 \, ClassSize + 0.65 \, PrntInc.
    $$

    The class-size coefficient falls from $-2.28$ to $-1.10$. This is the omitted variable bias from Section 1 being removed. Parental income raises test scores and tends to be lower in districts with larger classes, so the single-variable slope blamed class size for part of what was really the effect of income. Once income is held fixed, the estimated effect of one more student per teacher is smaller. The income coefficient says that among districts of the same class size, each additional thousand dollars of parental income goes with 0.65 more points.
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

    In multiple regression the $R^2$ has a flaw. Adding a regressor can never raise the sum of squared residuals, because OLS can always leave the new coefficient at zero and do no worse. So the $R^2$ never falls when a regressor is added, even one that explains nothing. Judging a model by the $R^2$ alone would reward piling in useless variables.

    The *adjusted $R^2$* fixes this by charging a penalty for each regressor,

    $$
    \bar{R}^2 = 1 - \frac{n-1}{n-k-1}\cdot\frac{\mathrm{SSR}}{\mathrm{TSS}}.
    $$

    The factor $\frac{n-1}{n-k-1}$ grows with $k$, so a regressor that barely reduces the sum of squared residuals lowers the adjusted $R^2$ rather than raising it. A falling adjusted $R^2$ is the signal that a regressor is not earning its place.

    The table below fits the test-score model for whichever regressors you include. Start with class size alone, then add parental income and a measure of district spending per pupil, and watch both the coefficients and the fit measures respond.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    inc_box = mo.ui.checkbox(value=False, label="Add parental income")
    expn_box = mo.ui.checkbox(value=False, label="Add expenditure per pupil")
    mo.vstack(
        [
            mo.md("Class size is always included. Toggle the other regressors to see the coefficients and the fit measures change."),
            mo.hstack([inc_box, expn_box], justify="start", gap=1.5),
        ]
    )
    return expn_box, inc_box


@app.cell(hide_code=True)
def _(cs, expn, expn_box, inc_box, mo, np, prnt, ts):
    def _fit(cols):
        _Xm = np.column_stack([np.ones(len(ts))] + cols)
        _beta, *_ = np.linalg.lstsq(_Xm, ts, rcond=None)
        _resid = ts - _Xm @ _beta
        _nn = len(ts)
        _kk = len(cols)
        _ssr = float(np.sum(_resid ** 2))
        _tss = float(np.sum((ts - ts.mean()) ** 2))
        _r2 = 1.0 - _ssr / _tss
        _adj = 1.0 - (_nn - 1) / (_nn - _kk - 1) * _ssr / _tss
        _ser = float(np.sqrt(_ssr / (_nn - _kk - 1)))
        return _beta, _r2, _adj, _ser

    _cols = [cs]
    _names = ["Class size"]
    if inc_box.value:
        _cols.append(prnt)
        _names.append("Parental income")
    if expn_box.value:
        _cols.append(expn)
        _names.append("Expenditure per pupil")

    _beta, _r2, _adj, _ser = _fit(_cols)
    _base, _, _, _ = _fit([cs])
    _cs_only = float(_base[1])

    _rows = "\n".join(
        f"| {_nm} | {_beta[_j + 1]:+.2f} |" for _j, _nm in enumerate(_names)
    )
    _table = (
        "| Regressor | Coefficient |\n|:--|--:|\n" + _rows
    )
    _stats = (
        f"Standard error of the regression $= {_ser:.2f}$ &nbsp;&nbsp; "
        f"$R^2 = {_r2:.3f}$ &nbsp;&nbsp; adjusted $R^2 = {_adj:.3f}$"
    )

    if not inc_box.value and not expn_box.value:
        _msg = (
            f"With class size alone, its coefficient is about {_cs_only:.2f} points per "
            f"student. Parental income and spending are still in the error."
        )
    elif inc_box.value:
        _msg = (
            f"Adding parental income flattens the class-size coefficient from about "
            f"{_cs_only:.2f} to about {_beta[1]:.2f}, the omitted variable bias from Section 1 "
            f"being removed."
        )
        if expn_box.value:
            _msg += (
                " Spending per pupil adds almost nothing. The $R^2$ ticks up, but the adjusted "
                "$R^2$ falls, the penalty showing the variable does not earn its place."
            )
    else:
        _msg = (
            "Spending per pupil adds almost nothing on its own. The $R^2$ barely moves, and the "
            "adjusted $R^2$ falls once the penalty for the extra regressor is applied."
        )

    _caption = mo.md(
        '<span style="display:block;margin:0.4rem auto 1rem;max-width:520px;'
        'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
        + _msg + "</span>"
    )
    mo.vstack(
        [
            mo.md(_table),
            mo.md(
                '<span style="display:block;text-align:center;margin:0.6rem 0;">'
                + _stats + "</span>"
            ),
            _caption,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. The least squares assumptions with several regressors

    The conditions for reading the OLS slopes as causal effects carry over from Lecture 6, with one addition, so there are four.

    The first is *mean independence*, that the error has mean zero given every regressor, $\mathbb{E}[u \mid X_1, \dots, X_k] = 0$. This is the assumption that adding controls is meant to rescue. Each variable moved from the error into the regression is one fewer source of omitted variable bias.

    The second is that the data $(Y_i, X_{1i}, \dots, X_{ki})$ are *independent and identically distributed* across observations, which holds when the sample is drawn at random.

    The third is that *large outliers are unlikely*, so that no single observation dominates the estimates.

    The fourth is new to multiple regression. It rules out *perfect multicollinearity*, which arises when one regressor is an exact linear function of the others. Age and date of birth are an example. A person's age is fixed once the date of birth and today's date are set, so the two carry the same information. Asking for the effect of age while holding date of birth fixed has no meaning, because age cannot change with date of birth held constant. When two regressors are perfectly collinear, OLS cannot separate their coefficients and the estimates do not exist. The fix is to drop one of the redundant regressors.
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
            "of each coefficient, estimating several coefficients by least squares, why the "
            "R-squared never falls while the adjusted R-squared can, and the four least squares "
            "assumptions including no perfect multicollinearity."
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
    expn = 8.0 - 0.10 * cs + _rng.normal(0.0, 1.2, _n)
    _u = _rng.normal(0.0, 12.0, _n)
    ts = 698.9 - 1.10 * cs + 0.65 * prnt + _u
    return cs, expn, prnt, ts


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

    In the test-score example $\beta_2$ is positive, because income raises scores, and $\delta_1$ is negative, because richer districts run smaller classes. Their product is negative, which is why the single-variable slope $-2.28$ lies below the held-income slope $-1.10$.
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
