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

__generated_with = "0.23.6"
app = marimo.App(
    app_title="Lecture 3: Working With Multiple Random Variables",
    css_file="marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt
    from scipy import stats

    return alt, mo, np, pd, stats


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: block; margin-bottom: 1.5em;">Course home</a>'),
            mo.md("# [Lecture 3](#top)"),
            mo.md("Working With Multiple Random Variables"),
            mo.nav_menu(
                {
                    "#sec1": "1. Joint, marginal, and conditional distributions",
                    "#sec2": "2. Covariance and correlation",
                    "#sec3": "3. Independence",
                    "#sec4": "4. Independent and identically distributed",
                    "#sec5": "5. Means and variances of sums",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec2RandomVariables.html" target="_self">← Lecture 2</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec4EstimationHypothesisTestingAndConfidenceIntervals.html" target="_self">Lecture 4 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 3: Working With Multiple Random Variables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contents

    1. [Joint, marginal, and conditional distributions](#sec1)
    2. [Covariance and correlation](#sec2)
    3. [Independence](#sec3)
    4. [Independent and identically distributed](#sec4)
    5. [Means and variances of sums](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Joint, marginal, and conditional distributions

    In Lecture 2 we focused on one random variable at a time. We described its distribution, its expected value, and its spread. Most questions in econometrics, however, ask about two variables together. Does a person's earnings depend on their level of education? Does the unemployment rate depend on the inflation rate? To answer these questions we need to extend the tools from one random variable to two.

    A *joint probability distribution* describes how likely each combination of values is for two random variables. When $X$ takes possible values $x_1, x_2, \ldots, x_k$ and $Y$ takes possible values $y_1, y_2, \ldots, y_l$, the joint probability distribution lists $\mathbb{P}(X = x_i, Y = y_j)$ for every pair $(x_i, y_j)$. The table below shows one example.

    |  | $x_1$ | $x_2$ | $x_3$ |
    |---|---|---|---|
    | $y_1$ | 0.10 | 0.15 | 0.20 |
    | $y_2$ | 0.20 | 0.10 | 0.25 |

    The six cells must sum to one because together they cover every possible outcome.

    A *marginal probability distribution* gives the distribution of a single variable, ignoring the other. We compute it by summing the joint probabilities over the values of the other variable. The marginal probability that $X = x_1$ is

    $$ \mathbb{P}(X = x_1) = \mathbb{P}(X = x_1, Y = y_1) + \mathbb{P}(X = x_1, Y = y_2) = 0.10 + 0.20 = 0.30. $$

    In general, $\mathbb{P}(X = x_i) = \sum_j \mathbb{P}(X = x_i, Y = y_j)$, summing across the row or column for $x_i$.

    A *conditional probability distribution* gives the distribution of one variable, given the value of the other. The conditional probability that $Y = y_j$ given $X = x_i$ is

    $$ \mathbb{P}(Y = y_j \mid X = x_i) = \frac{\mathbb{P}(X = x_i, Y = y_j)}{\mathbb{P}(X = x_i)}. $$

    This formula is also known as *Bayes' rule*. It rewrites the question ''how likely is $Y = y_j$, knowing that $X = x_i$ has occurred?'' in terms of probabilities we can read off the table. For our example, the conditional probability that $Y = y_1$ given $X = x_1$ is

    $$ \mathbb{P}(Y = y_1 \mid X = x_1) = \frac{0.10}{0.30} = \frac{1}{3}. $$

    Bayes' rule turns up in many places, from medical testing to legal evidence. For this course, it is the bridge between the joint distribution and the conditional distribution.

    Pick a value of $X$ and a value of $Y$ in the panel below. The chart highlights the cell, and the formulas beneath the chart show how the joint, marginal, and conditional probabilities are computed from the table above.
    """)
    return


@app.cell(hide_code=True)
def _(pd):
    joint_table = pd.DataFrame({
        "X": ["x1", "x2", "x3"] * 2,
        "Y": ["y1", "y1", "y1", "y2", "y2", "y2"],
        "p": [0.10, 0.15, 0.20, 0.20, 0.10, 0.25],
    })
    return (joint_table,)


@app.cell(hide_code=True)
def _(mo):
    jt_x = mo.ui.dropdown(
        options=["x1", "x2", "x3"], value="x1", label="Pick X",
    )
    jt_y = mo.ui.dropdown(
        options=["y1", "y2"], value="y1", label="Pick Y",
    )
    mo.hstack([jt_x, jt_y], justify="start")
    return jt_x, jt_y


@app.cell(hide_code=True)
def _(alt, joint_table, jt_x, jt_y, mo, pd):
    _selected = pd.DataFrame({"X": [jt_x.value], "Y": [jt_y.value]})

    _heatmap = (
        alt.Chart(joint_table)
        .mark_rect()
        .encode(
            x=alt.X("X:N", title=None, axis=alt.Axis(labelExpr="'x_' + substring(datum.value, 1)")),
            y=alt.Y("Y:N", title=None, sort=["y2", "y1"], axis=alt.Axis(labelExpr="'y_' + substring(datum.value, 1)")),
            color=alt.Color("p:Q", scale=alt.Scale(scheme="blues"), legend=None),
        )
    )
    _labels = (
        alt.Chart(joint_table)
        .mark_text(color="white", fontSize=16, fontWeight="bold")
        .encode(
            x="X:N",
            y=alt.Y("Y:N", sort=["y2", "y1"]),
            text=alt.Text("p:Q", format=".2f"),
        )
    )
    _highlight = (
        alt.Chart(_selected)
        .mark_rect(fill=None, stroke="orange", strokeWidth=4)
        .encode(
            x="X:N",
            y=alt.Y("Y:N", sort=["y2", "y1"]),
        )
    )
    _chart = (_heatmap + _labels + _highlight).properties(
        width=360, height=180, title="Joint probability table",
    )

    _xv = jt_x.value
    _yv = jt_y.value
    _xs = "x_" + _xv[1:]
    _ys = "y_" + _yv[1:]
    _joint = float(joint_table[(joint_table.X == _xv) & (joint_table.Y == _yv)]["p"].iloc[0])
    _marg_x = float(joint_table[joint_table.X == _xv]["p"].sum())
    _marg_y = float(joint_table[joint_table.Y == _yv]["p"].sum())
    _cond = _joint / _marg_x if _marg_x > 0 else 0.0

    _formulas = mo.md(
        rf"""
- Joint: $\mathbb{{P}}(X = {_xs},\ Y = {_ys}) = {_joint:.2f}$
- Marginal of $X$: $\mathbb{{P}}(X = {_xs}) = {_marg_x:.2f}$
- Marginal of $Y$: $\mathbb{{P}}(Y = {_ys}) = {_marg_y:.2f}$
- Conditional (Bayes' rule): $\mathbb{{P}}(Y = {_ys} \mid X = {_xs}) = \dfrac{{\mathbb{{P}}(X = {_xs},\ Y = {_ys})}}{{\mathbb{{P}}(X = {_xs})}} = \dfrac{{{_joint:.2f}}}{{{_marg_x:.2f}}} = {_cond:.2f}$
"""
    )

    mo.vstack([_chart, _formulas])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Covariance and correlation

    The joint distribution describes how two random variables behave together, but it does not summarize their relationship in one number. The *covariance* of $X$ and $Y$ summarizes whether they tend to move in the same direction or in opposite directions. It is defined as

    $$ \text{cov}(X, Y) \equiv \sigma_{XY} = \mathbb{E}\big[(X - \mu_X)(Y - \mu_Y)\big] = \sum_i \sum_j (x_j - \mu_X)(y_i - \mu_Y) \cdot \mathbb{P}(X = x_j, Y = y_i). $$

    The sign of the covariance is what carries most of the meaning. A positive $\sigma_{XY}$ means that when $X$ is above its mean, $Y$ tends to be above its mean too, and the two tend to move together. A negative $\sigma_{XY}$ means one tends to be above its mean when the other is below it, so the two tend to move in opposite directions. A zero covariance means $X$ and $Y$ do not move together on average.

    The size of the covariance is harder to interpret because it depends on the units of $X$ and $Y$. The covariance between years of education and weekly earnings would be in (years $\times$ dollars), while the covariance between height and weight would be in (inches $\times$ pounds). The numbers are not comparable.

    To get a unit-free summary we divide by the standard deviations of $X$ and $Y$. The *correlation coefficient*, also written *correlation*, is

    $$ \text{corr}(X, Y) \equiv \rho_{XY} = \frac{\sigma_{XY}}{\sigma_X \sigma_Y}. $$

    The correlation always sits between $-1$ and $1$. A correlation of $+1$ means $Y$ is an exactly increasing linear function of $X$. A correlation of $-1$ means $Y$ is an exactly decreasing linear function of $X$. A correlation of $0$ means $X$ and $Y$ have no linear relationship on average.

    With data we do not observe $\sigma_{XY}$, $\sigma_X$, $\sigma_Y$ directly. We estimate them from a sample of $n$ paired observations $(X_1, Y_1), (X_2, Y_2), \ldots, (X_n, Y_n)$. The *sample covariance* is

    $$ \hat{\sigma}_{XY} = \frac{1}{n - 1} \sum_{i=1}^{n} (X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y), $$

    and the *sample correlation* is

    $$ \widehat{\text{corr}}(X, Y) = \frac{\hat{\sigma}_{XY}}{\hat{\sigma}_X \hat{\sigma}_Y}. $$

    The \$594 weekly-earnings gap between high school graduates and bachelor's-degree holders from the BLS table in Lecture 1 is one way to summarize the relationship between education and earnings. The correlation between years of education and weekly earnings is another. The correlation uses every level of education at once, instead of just two, and reports the relationship as a single number between $-1$ and $1$.

    The scatter plot below starts with a small sample of synthetic education-and-earnings pairs. Drag the mouse across a region of the chart to make a brush rectangle, then click ''Spray'' to add a cluster of new points centered on that rectangle. The four sample statistics under the chart update each time you add points. Use ''Clear'' to reset the scatter to its starting cloud.
    """)
    return


@app.cell(hide_code=True)
def _(mo, np):
    _rng = np.random.default_rng(42)
    _starter_n = 20
    _starter_edu = _rng.uniform(10.0, 20.0, _starter_n)
    _starter_earn = 90.0 * _starter_edu + _rng.normal(0.0, 200.0, _starter_n) + 100.0
    starter_points = list(zip(_starter_edu.tolist(), _starter_earn.tolist()))

    get_spray_points, set_spray_points = mo.state(starter_points)
    return get_spray_points, set_spray_points, starter_points


@app.cell(hide_code=True)
def _(alt, get_spray_points, mo, pd):
    _pts = get_spray_points()
    if len(_pts) > 0:
        _df = pd.DataFrame(_pts, columns=["education", "earnings"])
    else:
        _df = pd.DataFrame({"education": [0.0], "earnings": [0.0]}).iloc[0:0]

    _brush = alt.selection_interval()
    _scatter = (
        alt.Chart(_df)
        .mark_circle(color="#1f4e79", size=70, opacity=0.7)
        .encode(
            x=alt.X(
                "education:Q",
                scale=alt.Scale(domain=[0, 25]),
                title="Years of education",
            ),
            y=alt.Y(
                "earnings:Q",
                scale=alt.Scale(domain=[0, 3000]),
                title="Weekly earnings (USD)",
            ),
        )
        .add_params(_brush)
        .properties(width=560, height=340)
    )
    spray_chart = mo.ui.altair_chart(
        _scatter, chart_selection=False, legend_selection=False,
    )
    return (spray_chart,)


@app.cell(hide_code=True)
def _(mo):
    spray_n_slider = mo.ui.slider(
        start=1, stop=50, step=1, value=10,
        label="Points per spray", show_value=True,
    )
    return (spray_n_slider,)


@app.cell(hide_code=True)
def _(
    get_spray_points,
    mo,
    np,
    set_spray_points,
    spray_chart,
    spray_n_slider,
    starter_points,
):
    def _on_spray(value):
        brush_data = spray_chart.value
        if brush_data is not None and len(brush_data) > 0:
            cx = float(brush_data["education"].mean())
            cy = float(brush_data["earnings"].mean())
            n = int(spray_n_slider.value)
            # Seed depends on current state and centroid so consecutive
            # sprays at the same spot still produce different patterns.
            current = get_spray_points()
            seed = abs(hash((len(current), round(cx * 1000), round(cy * 1000)))) % (2**32)
            rng = np.random.default_rng(seed)
            new_x = rng.normal(cx, 1.0, n)
            new_y = rng.normal(cy, 120.0, n)
            new_pts = list(zip(new_x.tolist(), new_y.tolist()))
            set_spray_points(current + new_pts)
        return value + 1

    def _on_clear(value):
        set_spray_points(list(starter_points))
        return value + 1

    spray_button = mo.ui.button(
        label="Spray", value=0, on_click=_on_spray,
    )
    clear_button = mo.ui.button(
        label="Clear", value=0, on_click=_on_clear,
    )
    return clear_button, spray_button


@app.cell(hide_code=True)
def _(clear_button, mo, spray_button, spray_chart, spray_n_slider):
    mo.vstack([
        spray_chart,
        mo.hstack(
            [spray_n_slider, spray_button, clear_button],
            justify="start", align="center",
        ),
    ])
    return


@app.cell(hide_code=True)
def _(get_spray_points, mo, np):
    _pts = get_spray_points()
    _n = len(_pts)
    if _n < 2:
        _body = "Add at least two points to compute the sample statistics."
    else:
        _x = np.array([p[0] for p in _pts])
        _y = np.array([p[1] for p in _pts])
        _var_x = float(np.var(_x, ddof=1))
        _var_y = float(np.var(_y, ddof=1))
        _cov = float(np.cov(_x, _y, ddof=1)[0, 1])
        if _var_x > 0 and _var_y > 0:
            _corr = _cov / float(np.sqrt(_var_x) * np.sqrt(_var_y))
        else:
            _corr = 0.0
        _body = (
            rf"Based on $n = {_n}$ points: "
            rf"$\hat{{\sigma}}_X^2 = {_var_x:.2f}$, "
            rf"$\hat{{\sigma}}_Y^2 = {_var_y:,.0f}$, "
            rf"$\hat{{\sigma}}_{{XY}} = {_cov:,.1f}$, "
            rf"$\widehat{{\text{{corr}}}}(X, Y) = {_corr:.3f}$."
        )

    mo.md(
        '<span style="display:block;margin:0.2rem auto 1.2rem;'
        'max-width:560px;font-size:0.9rem;line-height:1.5;'
        'color:#6b7280;text-align:center;">'
        + _body
        + "</span>"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Independence

    Two random variables are *independent* when knowing the value of one tells us nothing about the value of the other. In probability, that informal statement comes from three equivalent conditions. If $X$ and $Y$ are independent, then

    1. The conditional distribution of $Y$ does not depend on $X$, that is $\mathbb{P}(Y = y \mid X = x) = \mathbb{P}(Y = y)$ for every $x$ and $y$.
    2. The joint distribution factors into the product of the marginals, $\mathbb{P}(X = x, Y = y) = \mathbb{P}(X = x) \cdot \mathbb{P}(Y = y)$.
    3. The correlation and the covariance are both zero, $\text{corr}(X, Y) = \sigma_{XY} = 0$.

    Any one of these conditions can serve as the definition; the other two follow.

    A coin flip and an unrelated die roll are independent. Knowing that the coin landed heads tells us nothing about which face of the die is showing, so the conditional distribution of the die given the coin is the same as the unconditional distribution. The result of the first die in a pair, however, is not independent of the sum of the two dice. If we know the sum is $11$, then the first die is very likely a $5$ or a $6$, and definitely not a $1$, so the conditional distribution of the first die given the sum is different from the unconditional distribution.

    Independence is symmetric. If $X$ is independent of $Y$, then $Y$ is independent of $X$. The three conditions above are unchanged when $X$ and $Y$ are swapped.

    The third condition only goes one way. If $X$ and $Y$ are independent, then their correlation is zero. The converse, however, is not true. Two random variables can have zero correlation and still be dependent on each other, because correlation only captures the linear part of a relationship. We show an example of this in the appendix.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Independent and identically distributed

    A sequence of random variables $X_1, X_2, \ldots, X_n$ is *independently and identically distributed* (i.i.d.) when two conditions hold. First, every $X_i$ has the same distribution. Second, every pair of $X_i$ and $X_j$ with $i \ne j$ is independent. We write $X_i \stackrel{\text{i.i.d.}}{\sim} F$ for a sequence drawn i.i.d. from a distribution $F$.

    The sixty thousand households the Census Bureau surveys each month for the Bureau of Labor Statistics are treated as an i.i.d. sample from the population of U.S. households. Each household is drawn at random, so any one household's wage tells us nothing about the wages of the others (independence), and each draw comes from the same underlying population distribution of wages (identically distributed). This i.i.d. assumption is what lets us use the law of large numbers and the central limit theorem from the previous lecture on real survey data.

    Both parts of i.i.d. can fail in practice. Heights measured within the same family are not independent because tall parents tend to have tall children, so a parent's height is informative about a child's height. Heights are also not identically distributed across people of different ages, because children's heights are systematically smaller than adults'. Sampling a hundred members of one family would violate both conditions.

    The i.i.d. assumption is the starting point for the estimator properties we study in the next lecture. When it is in doubt, the methods of this course must be adjusted, and parts of the course later on (panel data, time series) deal with exactly those settings.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Means and variances of sums

    We often want to know the expected value and variance of a sum or weighted sum of random variables. Two short rules, both proved in the appendix, take care of most cases.

    The first rule is the *linearity of the expected value*. For any constants $a$ and $b$,

    $$ \mathbb{E}[a + b X] = a + b \mu_X. $$

    Linearity extends to a sum of several random variables. The expected value of a sum is the sum of the expected values, whether or not the variables are independent,

    $$ \mathbb{E}[X_1 + X_2 + \cdots + X_n] = \mathbb{E}[X_1] + \mathbb{E}[X_2] + \cdots + \mathbb{E}[X_n]. $$

    Variance has a similar but more restrictive rule. For constants $a$ and $b$,

    $$ \text{var}(a + b X) = b^2 \sigma_X^2. $$

    Covariance is symmetric and linear in each argument,

    $$ \text{cov}(X, Y) = \text{cov}(Y, X), \qquad \text{cov}(X, Y + Z) = \text{cov}(X, Y) + \text{cov}(X, Z). $$

    The variance of a sum, however, depends on whether the variables move together. When $X_1, X_2, \ldots, X_n$ are i.i.d. with variance $\sigma_X^2$, the cross covariances are zero, so the variance of the sum is simply $n$ times the variance of one,

    $$ \text{var}(X_1 + X_2 + \cdots + X_n) = n \sigma_X^2. $$

    When the variables are correlated, the cross covariances do not vanish, and the variance of the sum is larger or smaller depending on the sign of the correlations.

    The variance of the sample mean from Lecture 2 is a direct corollary. If $\hat{\mu}_X = \frac{1}{n}\sum_{i=1}^{n} X_i$ and the $X_i$ are i.i.d. with variance $\sigma_X^2$, then $\text{var}(\hat{\mu}_X) = n \sigma_X^2 / n^2 = \sigma_X^2 / n$, so $\sigma_{\hat{\mu}_X} = \sigma_X / \sqrt{n}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** joint probability distribution, marginal "
            "probability distribution, conditional probability distribution, "
            "Bayes' rule, covariance, correlation, correlation coefficient, "
            "sample covariance, sample correlation, independence, "
            "independently and identically distributed (i.i.d.).\n\n"
            "**Key concepts covered:** linearity of the expected value, "
            "variance of a sum of i.i.d. random variables, zero correlation "
            "does not imply independence."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="appendix"></a>
    ## Appendix
    """)
    return


@app.cell(hide_code=True)
def _(alt, mo, np, pd):
    _xg = np.linspace(-1.0, 1.0, 41)
    _yg = _xg ** 2 - 1.0 / 3.0
    _df = pd.DataFrame({"x": _xg, "y": _yg})

    _scatter = (
        alt.Chart(_df)
        .mark_circle(color="#1f4e79", size=70, opacity=0.85)
        .encode(
            x=alt.X("x:Q", title="X"),
            y=alt.Y("y:Q", title="Y"),
        )
        .properties(width=520, height=260)
    )

    _corr_val = float(np.corrcoef(_xg, _yg)[0, 1])
    _caption = mo.md(
        '<span style="display:block;margin:0.2rem auto 0.6rem;'
        'max-width:520px;font-size:0.85rem;line-height:1.45;'
        'color:#6b7280;text-align:center;">'
        rf"Forty-one points on the curve $Y = X^2 - 1/3$ with $X$ evenly "
        rf"spaced on $[-1, 1]$. The sample correlation is "
        rf"$\widehat{{\text{{corr}}}}(X, Y) = {_corr_val:.2f}$, yet $Y$ is "
        rf"completely determined by $X$."
        "</span>"
    )

    _text = mo.md(r"""
        This is bonus material. You will not be tested on the content of the appendix.

        **Zero correlation does not imply independence.**

        Independence is a stronger condition than zero correlation. Correlation only captures the linear part of a relationship between two random variables. If the relationship is nonlinear, the correlation can be zero even though the two are fully dependent. The figure below illustrates this with the deterministic relationship $Y = X^2 - 1/3$, where $X$ is uniform on $[-1, 1]$. Knowing $X$ tells us $Y$ exactly, so $X$ and $Y$ are not independent. But the sample correlation is essentially zero, because the parabolic relationship has no linear component on this symmetric domain.

        This is the reason we cannot replace independence with zero correlation in the assumptions for econometric estimators. We need the stronger condition to rule out hidden nonlinear dependence.

        **Proof of the linearity of the expected value.**

        We show that $\mathbb{E}[a + b X] = a + b \mathbb{E}[X]$ when $X$ is a discrete random variable taking values $x_1, x_2, \ldots, x_K$ with probabilities $p_1, p_2, \ldots, p_K$.

        Define $Y = a + b X$. The random variable $Y$ takes the value $a + b x_i$ with probability $p_i$. Its expected value is

        $$ \mathbb{E}[Y] = \sum_{i=1}^{K} (a + b x_i) \, p_i. $$

        Distribute the multiplication and split the sum into two parts,

        $$ \mathbb{E}[Y] = \sum_{i=1}^{K} a \, p_i + \sum_{i=1}^{K} b \, x_i \, p_i = a \sum_{i=1}^{K} p_i + b \sum_{i=1}^{K} x_i \, p_i. $$

        The first sum is $a$ times the total probability, which equals $1$ because the $p_i$ cover all outcomes. The second sum is $b$ times the expected value of $X$. So

        $$ \mathbb{E}[a + b X] = a \cdot 1 + b \cdot \mathbb{E}[X] = a + b \mathbb{E}[X]. $$

        The same argument extends to a sum of several random variables, giving linearity of the expected value in full generality.
        """)

    mo.accordion({
        "Bonus material (not on assessments)": mo.vstack([
            _text, _scatter, _caption,
        ]),
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec2RandomVariables.html" target="_self">← Lecture 2</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec4EstimationHypothesisTestingAndConfidenceIntervals.html" target="_self">Lecture 4 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
