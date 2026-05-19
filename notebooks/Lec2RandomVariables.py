# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "numpy",
#     "pandas",
#     "altair",
#     "scipy",
# ]
# ///

import marimo

__generated_with = "0.23.6"
app = marimo.App(
    app_title="Lecture 2: Random Variables and Probability Distributions",
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
            mo.md("# [Lecture 2](#top)"),
            mo.md("Random Variables and Probability Distributions"),
            mo.nav_menu(
                {
                    "#sec1": "1. Why we need probability",
                    "#sec2": "2. Random variables",
                    "#sec3": "3. Describing a random variable",
                    "#sec4": "4. The sample mean is random",
                    "#sec5": "5. Law of large numbers",
                    "#sec6": "6. Central limit theorem",
                    "#sec7": "7. Common probability distributions",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self">← Course home</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self">Lecture 3 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 2: Random Variables and Probability Distributions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contents

    1. [Why we need probability](#sec1)
    2. [Random variables](#sec2)
    3. [Describing a random variable](#sec3)
    4. [The sample mean is random](#sec4)
    5. [Law of large numbers](#sec5)
    6. [Central limit theorem](#sec6)
    7. [Common probability distributions](#sec7)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Why we need probability

    In the last lecture we saw that we almost never observe a whole population,
    only a sample, and that a different sample would give somewhat different
    numbers.

    Probability and statistics work in opposite directions. Probability starts
    from a known true distribution for the population and works out how samples
    drawn from it behave. Statistics goes the other way, using one observed
    sample to learn an unknown population quantity, such as the population mean
    $\mu_X$, through an estimator such as the sample mean $\hat{\mu}_X$.
    Econometrics uses a sample to infer an economic relationship in the
    population, and it rests on the probability and statistics ideas built here.

    This lecture builds those ideas using one running example, the number of
    emails you receive in an hour.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Random variables

    A variable is anything we measure that can take different values, such as a
    person's wage or the number of emails in an hour. Variables come in a few
    standard types.

    | Type | What it means | Example |
    |---|---|---|
    | Continuous | Can take any real value | Monthly income |
    | Discrete | Drawn from a countable set | Shoe sizes in half steps (5, 5.5, 6, ...) |
    | Count | Nonnegative integers, no fractions | Number of children |
    | Ordinal | Ordered categories, gaps not meaningful | Likert scale (strongly agree to strongly disagree) |
    | Categorical | Unordered categories, codes have no magnitude | Names of US states |
    | Binary | Two-category categorical variable | Yes or no |

    Continuous, discrete, count, and binary variables are usually treated as
    numeric in analysis, where binary is the special two-category case.

    A random variable is a numerical summary of a random outcome, so before the
    outcome happens we cannot say which value it will take, only how likely each
    value is. We write a random variable with a capital letter such as $X$. The
    number of emails you get in an hour is a random variable, because it depends
    on who happens to write to you that hour. A person's wage is a random
    variable because, before you draw a person at random from the population, you
    do not know which wage you will get.

    A discrete random variable takes only separated values you can count, such as
    $0, 1, 2, 3, \ldots$ emails. Its probability distribution lists its possible
    outcomes $x_1, x_2, \ldots, x_K$ together with the probability of each, where
    $p_i = \Pr(X = x_i)$ is shorthand for the probability that $X$ takes the
    value $x_i$. The cumulative probability distribution, written
    $\Pr(X \le x)$, is the probability that the random variable is at or below a
    particular value. A possible distribution for the emails example is the
    following.

    | Number of emails | 0 | 1 | 2 | 3 | 4 |
    |---|---|---|---|---|---|
    | Probability | 0.80 | 0.10 | 0.06 | 0.03 | 0.01 |
    | Cumulative probability | 0.80 | 0.90 | 0.96 | 0.99 | 1.00 |

    A continuous random variable takes any value in a continuum, such as a wage
    of \$18.46 an hour or any nearby amount. We cannot list every outcome, so
    instead of a probability for each value we use a probability density
    function. The area under the density between any two points is the
    probability that the outcome falls between them, and the cumulative
    distribution gives the probability of being at or below a value. The figure
    below uses the distribution of hourly wages as an example. Drag the two
    sliders to choose a wage range. The shaded area under the density is the
    probability that a worker's wage falls in that range, and the cumulative
    distribution on the right reads off the same probability directly. The
    calculus behind the continuous case is in the appendix.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    wage_lo = mo.ui.slider(
        start=0, stop=60, step=1, value=15,
        label="Lower wage (USD per hour)", show_value=True,
    )
    wage_hi = mo.ui.slider(
        start=0, stop=60, step=1, value=30,
        label="Upper wage (USD per hour)", show_value=True,
    )
    mo.vstack([wage_lo, wage_hi])
    return wage_hi, wage_lo


@app.cell(hide_code=True)
def _(alt, mo, np, pd, stats, wage_hi, wage_lo):
    _a = float(min(wage_lo.value, wage_hi.value))
    _b = float(max(wage_lo.value, wage_hi.value))

    # Hourly wage modeled as a lognormal distribution (right-skewed).
    _dist = stats.lognorm(s=0.5, scale=20.0)
    _x = np.linspace(0.0, 80.0, 400)
    _frame = pd.DataFrame({
        "wage": _x,
        "pdf": _dist.pdf(_x),
        "cdf": _dist.cdf(_x),
    })
    _band = _frame[(_frame["wage"] >= _a) & (_frame["wage"] <= _b)]
    _prob = float(_dist.cdf(_b) - _dist.cdf(_a))

    _area = (
        alt.Chart(_band)
        .mark_area(color="#1f4e79", opacity=0.25)
        .encode(x="wage:Q", y="pdf:Q")
    )
    _pdf_line = (
        alt.Chart(_frame)
        .mark_line(color="#1f4e79")
        .encode(
            x=alt.X("wage:Q", title="Hourly wage (USD)"),
            y=alt.Y("pdf:Q", title="Density"),
        )
    )
    _left = (_area + _pdf_line).properties(
        width=250, height=240, title="Wage density"
    )

    _rule = (
        alt.Chart(pd.DataFrame({"wage": [_a, _b]}))
        .mark_rule(color="orange", strokeDash=[4, 3])
        .encode(x="wage:Q")
    )
    _cdf_line = (
        alt.Chart(_frame)
        .mark_line(color="#1f4e79")
        .encode(
            x=alt.X("wage:Q", title="Hourly wage (USD)"),
            y=alt.Y("cdf:Q", title="Cumulative probability"),
        )
    )
    _right = (_cdf_line + _rule).properties(
        width=250, height=240, title="Cumulative distribution"
    )

    mo.vstack([
        alt.hconcat(_left, _right),
        mo.md(
            f"The probability that an hourly wage falls between "
            f"\\${_a:,.0f} and \\${_b:,.0f} is {_prob:.2f}. On the left that is "
            "the shaded area under the density. On the right it is the "
            "cumulative curve's height at the upper wage minus its height at "
            "the lower wage."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Describing a random variable

    Two numbers summarize most of what we care about in a random variable. The
    expected value of $X$ is denoted $\mathbb{E}[X] \equiv \mu_X$, a weighted
    average of the possible outcomes where the weights are their probabilities.
    When $X$ takes $K$ possible values $x_1, \ldots, x_K$ with probabilities
    $p_i = \Pr(X = x_i)$,

    $$ \mathbb{E}[X] \equiv \mu_X = \sum_{i=1}^{K} x_i \cdot p_i. $$

    The variance of $X$ measures the spread of its distribution and is denoted

    $$ \text{var}(X) \equiv \sigma_X^2 = \mathbb{E}\big[(X - \mathbb{E}[X])^2\big] = \sum_{i=1}^{K} (x_i - \mu_X)^2 \cdot p_i. $$

    Because the variance is in squared units, the spread is usually reported as
    the standard deviation $\text{sd}(X) = \sigma_X = \sqrt{\sigma_X^2}$, which is
    back in the original units. These are properties of the probability
    distribution, so computing them needs the true probabilities $p_i$.

    With data we do not observe the $p_i$. We instead compute the sample mean and
    the sample variance,

    $$ \hat{\mu}_X = \frac{1}{n} \sum_{i=1}^{n} X_i, \qquad \hat{\sigma}_X^2 = \frac{1}{n-1} \sum_{i=1}^{n} (X_i - \hat{\mu}_X)^2, $$

    where the $X_i$ are the observed outcomes and
    $\hat{\sigma}_X = \sqrt{\hat{\sigma}_X^2}$. When $n$ is large these sample
    quantities approximate the population $\mu_X$ and $\sigma_X^2$, because
    outcomes show up in proportion to their underlying probabilities. That result
    is the law of large numbers, the subject of Section 5.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example with the emails data

    Suppose the true distribution is the one from Section 2, and over 24 separate
    hours you record how many emails arrived in each hour.

    | Number of emails $x_i$ | 0 | 1 | 2 | 3 | 4 |
    |---|---|---|---|---|---|
    | Probability $p_i$ (unobserved) | 0.80 | 0.10 | 0.06 | 0.03 | 0.01 |
    | Hours with $x_i$ emails (observed) | 19 | 4 | 1 | 0 | 0 |

    If we knew the probabilities, the expected number of emails in an hour would
    be

    $$ \mu_X = \sum_{i=1}^{K} x_i \cdot p_i = 0 \times 0.80 + 1 \times 0.10 + 2 \times 0.06 + 3 \times 0.03 + 4 \times 0.01 = 0.35. $$

    In practice we do not know the probabilities, so we approximate the expected
    value with the sample mean over the 24 observed hours,

    $$ \hat{\mu}_X = \frac{1}{n} \sum_{i=1}^{n} X_i = \frac{1}{24}\big(0 \times 19 + 1 \times 4 + 2 \times 1 + 3 \times 0 + 4 \times 0\big) = 0.25. $$

    The sample mean of $0.25$ is not equal to the expected value of $0.35$
    because 24 hours is a small sample. Collecting data over many more hours
    would pull the sample mean toward $0.35$, which is the law of large numbers
    in Section 5.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. The sample mean is random

    The sample mean $\hat{\mu}_X$ is itself a numerical summary of random
    outcomes, so it is itself a random variable. The sample mean number of
    emails per hour would come out differently on a different day. So the sample
    mean has its own expected value and its own standard deviation. Its expected
    value is the population expected value, and its standard deviation is

    $$ \mathbb{E}[\hat{\mu}_X] = \mu_X, \qquad \sigma_{\hat{\mu}_X} = \frac{\sigma_X}{\sqrt{n}}. $$

    The first equation is why the sample mean is a sensible estimate of $\mu_X$.
    The second says its spread shrinks as $n$ grows, so a larger sample makes us
    more confident about $\hat{\mu}_X$. Because $\sigma_X$ is an unobserved
    property of the distribution, approximating it with the sample standard
    deviation gives the standard error of the sample mean,

    $$ \text{se}(\hat{\mu}_X) = \frac{\hat{\sigma}_X}{\sqrt{n}}. $$

    The next two sections show what these formulas mean in simulations you can
    run yourself.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Law of large numbers

    The law of large numbers says that the sample mean $\hat{\mu}_X$ gets close
    to the population expected value $\mu_X$ when the sample is large, because
    over many draws the outcomes occur in proportion to their underlying
    probabilities. With a few draws the sample mean can be far off by luck. With
    thousands of draws it settles near $\mu_X$ and barely moves.

    Use the controls below. Pick a process, change the number of draws, and draw
    new samples. The wiggly line is the running sample mean as each new draw is
    added. The flat line marks the true expected value of the chosen process.
    Watch the running mean swing when the sample is small and settle onto the
    flat line as the sample grows, for every process in the list.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    lln_process = mo.ui.dropdown(
        options=[
            "Fair die (1 to 6)",
            "Coin flip (0 or 1)",
            "Emails per hour",
            "Wait time (exponential)",
        ],
        value="Fair die (1 to 6)",
        label="Process",
    )
    lln_draws = mo.ui.slider(
        start=10, stop=5000, step=10, value=200,
        label="Number of draws", show_value=True,
    )
    lln_button = mo.ui.button(
        label="Draw new sample", value=0, on_click=lambda c: c + 1,
    )
    mo.vstack([lln_process, lln_draws, lln_button])
    return lln_button, lln_draws, lln_process


@app.cell(hide_code=True)
def _(alt, lln_button, lln_draws, lln_process, mo, np, pd):
    _seed = 2024 + lln_button.value
    _rng = np.random.default_rng(_seed)
    _n = lln_draws.value
    _name = lln_process.value

    if _name == "Fair die (1 to 6)":
        _draws = _rng.integers(1, 7, _n).astype(float)
        _true = 3.5
    elif _name == "Coin flip (0 or 1)":
        _draws = _rng.integers(0, 2, _n).astype(float)
        _true = 0.5
    elif _name == "Emails per hour":
        _draws = _rng.poisson(4, _n).astype(float)
        _true = 4.0
    else:
        _draws = _rng.exponential(5, _n)
        _true = 5.0

    _running = np.cumsum(_draws) / np.arange(1, _n + 1)
    _path = pd.DataFrame({"draw": np.arange(1, _n + 1), "mean": _running})

    _line = (
        alt.Chart(_path)
        .mark_line(color="#1f4e79")
        .encode(
            x=alt.X("draw:Q", title="Number of draws"),
            y=alt.Y("mean:Q", title="Running sample mean"),
        )
    )
    _rule = (
        alt.Chart(pd.DataFrame({"y": [_true]}))
        .mark_rule(color="orange", size=2)
        .encode(y="y:Q")
    )
    _chart = (_line + _rule).properties(width=560, height=300)

    mo.vstack([
        _chart,
        mo.md(
            "The wiggly line is the sample mean after each new draw. The flat "
            "line is the true expected value of the chosen process. Small "
            "samples land anywhere; large samples settle on the flat line."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec6"></a>
    ## 6. Central limit theorem

    The central limit theorem says that the distribution of the sample mean
    $\hat{\mu}_X$ is well approximated by a normal distribution when $n$ is large.
    From the previous section the mean of $\hat{\mu}_X$ is $\mu_X$ and its
    variance is $\sigma_{\hat{\mu}_X}^2 = \sigma_X^2 / n$, so for large $n$ the
    sample mean is approximately

    $$ \hat{\mu}_X \ \sim\ \mathcal{N}\!\left(\mu_X,\ \sigma_{\hat{\mu}_X}^2\right), $$

    where $\mathcal{N}(\mu_X, \sigma_{\hat{\mu}_X}^2)$ is the normal distribution
    with mean $\mu_X$ and variance $\sigma_{\hat{\mu}_X}^2$. This holds whether or
    not $X$ itself is normally distributed, and if $X$ is normal the
    approximation is exact. This result underlies many of the hypothesis tests we
    use later in the course.

    The controls below let you pick a deliberately non-normal process, set the
    sample size behind each mean, and choose how many means to simulate. The
    left chart is the shape of the raw process. The right chart is the
    distribution of the sample means, with the matching normal curve drawn on
    top. Set the sample size to one and the means still look like the raw
    process. Raise it and the right chart becomes the bell curve, whatever the
    left chart looks like.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    clt_process = mo.ui.dropdown(
        options=[
            "Uniform (0 to 1)",
            "Exponential (mean 1)",
            "Lopsided coin (10% ones)",
            "Emails per hour",
        ],
        value="Exponential (mean 1)",
        label="Process",
    )
    clt_n = mo.ui.slider(
        start=1, stop=100, step=1, value=30,
        label="Sample size behind each mean (n)", show_value=True,
    )
    clt_reps = mo.ui.slider(
        start=200, stop=3000, step=100, value=1000,
        label="Number of sample means", show_value=True,
    )
    clt_button = mo.ui.button(
        label="Draw new samples", value=0, on_click=lambda c: c + 1,
    )
    mo.vstack([clt_process, clt_n, clt_reps, clt_button])
    return clt_button, clt_n, clt_process, clt_reps


@app.cell(hide_code=True)
def _(alt, clt_button, clt_n, clt_process, clt_reps, mo, np, pd, stats):
    # New samples are drawn only when "Draw new samples" is clicked (the seed
    # depends only on the button). The "number of sample means" slider just
    # shows more or fewer of the same pre-drawn pool, so moving it does not
    # redraw. Changing n necessarily redraws, since n is the variable of
    # interest in this demonstration.
    _MAX = 3000
    _rng = np.random.default_rng(7 + clt_button.value)
    _n = int(clt_n.value)
    _reps = int(clt_reps.value)
    _name = clt_process.value

    if _name == "Uniform (0 to 1)":
        _raw = _rng.uniform(0.0, 1.0, 2000)
        _pool = _rng.uniform(0.0, 1.0, (_MAX, _n))
        _mu, _sd = 0.5, (1.0 / 12.0) ** 0.5
    elif _name == "Exponential (mean 1)":
        _raw = _rng.exponential(1.0, 2000)
        _pool = _rng.exponential(1.0, (_MAX, _n))
        _mu, _sd = 1.0, 1.0
    elif _name == "Lopsided coin (10% ones)":
        _raw = (_rng.random(2000) < 0.1).astype(float)
        _pool = (_rng.random((_MAX, _n)) < 0.1).astype(float)
        _mu, _sd = 0.1, (0.1 * 0.9) ** 0.5
    else:
        _raw = _rng.poisson(3, 2000).astype(float)
        _pool = _rng.poisson(3, (_MAX, _n)).astype(float)
        _mu, _sd = 3.0, 3.0 ** 0.5

    _means = _pool.mean(axis=1)[:_reps]

    _parent = (
        alt.Chart(pd.DataFrame({"x": _raw}))
        .mark_bar(color="#9aa5b1")
        .encode(
            x=alt.X("x:Q", bin=alt.Bin(maxbins=30), title="Raw process"),
            y=alt.Y("count()", title="Count"),
        )
        .properties(width=250, height=260, title="The raw process")
    )

    _hist = (
        alt.Chart(pd.DataFrame({"m": _means}))
        .mark_bar(color="#1f4e79", opacity=0.85)
        .encode(
            x=alt.X("m:Q", bin=alt.Bin(maxbins=30), title="Sample means"),
            y=alt.Y("count()", title="Count"),
        )
    )

    _lo = float(_means.min())
    _hi = float(_means.max())
    _se = _sd / (_n ** 0.5)
    if _hi > _lo and _se > 0:
        _grid = np.linspace(_lo, _hi, 200)
        _binw = (_hi - _lo) / 30.0
        _curve_df = pd.DataFrame({
            "m": _grid,
            "count": stats.norm.pdf(_grid, _mu, _se) * _reps * _binw,
        })
        _curve = (
            alt.Chart(_curve_df)
            .mark_line(color="orange", size=2)
            .encode(x="m:Q", y="count:Q")
        )
        _right = (_hist + _curve)
    else:
        _right = _hist

    _right = _right.properties(
        width=250, height=260, title="Distribution of the sample means"
    )

    mo.vstack([
        alt.hconcat(_parent, _right),
        mo.md(
            "Left is the shape of the raw process. Right is the distribution of "
            "the sample means with the matching normal curve on top. Raising "
            "the sample size turns the right chart into the bell curve no "
            "matter what the left chart looks like."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec7"></a>
    ## 7. Common probability distributions

    A probability distribution is the full description of how likely each value
    of a random variable is. A few come up so often they have names, and the most
    important is the normal distribution.

    The normal distribution is a bell-shaped, symmetric distribution fully
    determined by its mean $\mu$ and variance $\sigma^2$, and it is denoted
    $\mathcal{N}(\mu, \sigma^2)$. It appears throughout statistics and
    econometrics because of the central limit theorem. The area under its curve
    between $\mu - 1.96\sigma$ and $\mu + 1.96\sigma$ is $0.95$.

    The standard normal distribution is the normal distribution with $\mu = 0$
    and $\sigma = 1$, written $\mathcal{N}(0, 1)$. Standardizing turns any normal
    variable into a standard normal one. If $X \sim \mathcal{N}(\mu, \sigma^2)$,
    then subtracting the mean and dividing by the standard deviation gives

    $$ Z = \frac{X - \mu}{\sigma} \sim \mathcal{N}(0, 1). $$

    Subtracting $\mu$ recenters the variable on zero and dividing by $\sigma$
    rescales its spread to one, so two normal variables measured on different
    scales can be compared once both are standardized. The chi-squared, t, and F
    distributions, which appear later when we test hypotheses, are defined in the
    appendix.

    The demo below shows standardization at work. Move the mean and the standard
    deviation and watch the normal on the left shift and spread, while its
    standardized version on the right stays exactly the standard normal.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    std_mu = mo.ui.slider(
        start=-3.0, stop=3.0, step=0.5, value=1.0,
        label="Mean (mu)", show_value=True,
    )
    std_sigma = mo.ui.slider(
        start=0.5, stop=3.0, step=0.5, value=1.5,
        label="Standard deviation (sigma)", show_value=True,
    )
    mo.vstack([std_mu, std_sigma])
    return std_mu, std_sigma


@app.cell(hide_code=True)
def _(alt, mo, np, pd, stats, std_mu, std_sigma):
    _mu = std_mu.value
    _sigma = std_sigma.value

    _xl = np.linspace(-9.0, 9.0, 400)
    _left = (
        alt.Chart(pd.DataFrame({"x": _xl, "density": stats.norm.pdf(_xl, _mu, _sigma)}))
        .mark_line(color="#1f4e79", size=2)
        .encode(
            x=alt.X("x:Q", scale=alt.Scale(domain=[-9, 9]), title="X"),
            y=alt.Y("density:Q", scale=alt.Scale(domain=[0, 0.85]), title="Density"),
        )
        .properties(width=250, height=240, title="X, a normal you chose")
    )

    _xr = np.linspace(-4.0, 4.0, 400)
    _right = (
        alt.Chart(pd.DataFrame({"x": _xr, "density": stats.norm.pdf(_xr, 0.0, 1.0)}))
        .mark_line(color="#1f4e79", size=2)
        .encode(
            x=alt.X("x:Q", title="Z = (X - mu) / sigma"),
            y=alt.Y("density:Q", scale=alt.Scale(domain=[0, 0.85]), title="Density"),
        )
        .properties(width=250, height=240, title="X after standardizing")
    )

    mo.vstack([
        alt.hconcat(_left, _right),
        mo.md(
            "Left is the normal you chose; moving the sliders shifts and "
            "spreads it. Right is the same variable after standardizing with "
            "Z = (X - mu) / sigma, which is always the standard normal no "
            "matter which mean and standard deviation you pick."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Appendix (bonus material, not on assessments)": mo.md(r"""
        This is bonus material. You will not need calculus on any quiz, problem
        set, or exam.

        When a random variable does not take a discrete set of values we call it
        continuous, and we cannot sum over its outcomes. The discrete formula
        $\mathbb{E}[X] = \sum_{i=1}^{K} x_i \cdot p_i$ no longer works, and the
        same is true for the variance. We use calculus instead, with the
        probability density function $f(x)$ in place of the probabilities,

        $$ \mathbb{E}[X] = \int x \cdot f(x)\,dx. $$

        The intuition is unchanged. We still add up each possible outcome $x$
        times its chance of occurring, with the integral playing the role the
        sum played in the discrete case.

        Two less common measures of spread are the skewness and the kurtosis.
        The skewness measures the tilt of a distribution and is zero when it is
        symmetric, with a positive value meaning a long right tail. The kurtosis
        measures how much mass is in the tails, that is how much of the variance
        comes from extreme values,

        $$ \text{skewness} = \frac{\mathbb{E}\big[(X - \mu_X)^3\big]}{\sigma_X^3}, \qquad \text{kurtosis} = \frac{\mathbb{E}\big[(X - \mu_X)^4\big]}{\sigma_X^4}. $$

        The expected value $\mathbb{E}[X]$ is also called the first moment of
        $X$, $\mathbb{E}[X^2]$ the second moment, and $\mathbb{E}[X^r]$ the
        $r$-th moment. The variance, skewness, and kurtosis are built from the
        second, third, and fourth moments.

        Three named distributions come up later when we test hypotheses. The
        chi-squared distribution is the distribution of a sum of $m$ squared
        independent standard normal variables, denoted $\chi^2_m$, where $m$ is
        its degrees of freedom. The other two build on it. Let $Z \sim
        \mathcal{N}(0, 1)$ and $W \sim \chi^2_m$ be independent, where $\sim$
        means "distributed as". The statistic $T = Z / \sqrt{W/m}$ has a Student
        t distribution with $m$ degrees of freedom, denoted $t_m$. It has fatter
        tails than the normal and approaches $\mathcal{N}(0, 1)$ as $m$ grows.
        Let $W \sim \chi^2_m$ and $V \sim \chi^2_n$ be independent. Then
        $F = (W/m)/(V/n)$ has an F distribution with $m$ numerator and $n$
        denominator degrees of freedom, denoted $F_{m,n}$, and it takes only
        positive values.
        """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Appendix figure (bonus): chi-square, t, and F shapes

    The t distribution approaches the standard normal as its degrees of freedom
    grow, while the chi-square and F distributions take only positive values and
    lean to the right.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    appx_dist = mo.ui.dropdown(
        options=["Chi-square", "t", "F"],
        value="t",
        label="Distribution",
    )
    appx_df = mo.ui.slider(
        start=1, stop=30, step=1, value=4,
        label="Degrees of freedom", show_value=True,
    )
    mo.vstack([appx_dist, appx_df])
    return appx_df, appx_dist


@app.cell(hide_code=True)
def _(alt, appx_df, appx_dist, mo, np, pd, stats):
    _name = appx_dist.value
    _k = int(appx_df.value)
    _x = np.linspace(-5.0, 15.0, 400)

    if _name == "Chi-square":
        _y = stats.chi2.pdf(_x, _k)
        _label = f"Chi-square (df = {_k})"
    elif _name == "t":
        _y = stats.t.pdf(_x, _k)
        _label = f"t (df = {_k})"
    else:
        _y = stats.f.pdf(_x, _k, 10)
        _label = f"F (df = {_k} and 10)"

    _faint = (
        alt.Chart(pd.DataFrame({"x": _x, "density": stats.norm.pdf(_x, 0.0, 1.0)}))
        .mark_line(color="#9aa5b1", strokeDash=[4, 3])
        .encode(x="x:Q", y="density:Q")
    )
    _main = (
        alt.Chart(pd.DataFrame({"x": _x, "density": _y}))
        .mark_line(color="#1f4e79", size=2)
        .encode(
            x=alt.X("x:Q", title="Value"),
            y=alt.Y("density:Q", title="Density"),
        )
    )
    _chart = (_faint + _main).properties(width=560, height=300, title=_label)

    mo.vstack([
        _chart,
        mo.md(
            "The solid line is the chosen distribution and the faint dashed "
            "line is the standard normal, shown for comparison. For F the "
            "slider sets the numerator degrees of freedom and the denominator "
            "is fixed at 10."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self">← Course home</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self">Lecture 3 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
