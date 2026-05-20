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
                    "#appendix": "Appendix",
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

    [Appendix](#appendix)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Why we need probability

    In the last lecture we drew a line between a population and a sample. The
    population is the whole group a question is meant to cover, for example
    every adult worker in the country, on the order of a hundred and fifty
    million people. The sample is the much smaller group we actually collect
    data from, for example the sixty thousand households the Census Bureau
    contacts each month for its labor force survey.

    The numbers we compute live in the sample, not the population. If a
    different sixty thousand households had been picked, the average wage in
    the data would come out a little differently. It would still be near the
    truth, perhaps \$24.30 an hour instead of \$24.10, but not exactly the
    same. A number computed from a sample, then, does not have one fixed
    value. It varies from one possible sample to the next.

    Probability is the language for describing how a number that varies from
    sample to sample behaves. Probability starts from a known true
    distribution in the population and works out how samples drawn from it
    look on average and how much they swing around that average. Statistics
    goes the other way. We observe one sample and use it to learn an unknown
    population quantity, such as the population mean $\mu_X$, through an
    estimator such as the sample mean $\hat{\mu}_X$. Econometrics applies
    both to economic questions, using a sample to infer an economic
    relationship in the population.

    This lecture builds the probability ideas the rest of the course needs.
    The running example is the number of emails you receive in an hour.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Random variables

    A variable is something we measure that takes different values from one
    case to the next. Hourly wage is a variable because different people earn
    different amounts. The number of emails you receive in an hour is a
    variable because some hours bring zero and other hours bring five.
    Variables come in a few standard types.

    | Type | What it means | Example |
    |---|---|---|
    | Continuous | Can take any real value | Monthly income |
    | Discrete | Drawn from a countable set | Shoe sizes in half steps (5, 5.5, 6, ...) |
    | Count | Nonnegative integers, no fractions | Number of children |
    | Ordinal | Ordered categories, gaps not meaningful | Likert scale (strongly agree to strongly disagree) |
    | Categorical | Unordered categories, codes have no magnitude | Names of US states |
    | Binary | Two-category categorical variable | Yes or no |

    The first four types are numeric, so they can be added, averaged, and put
    through formulas. Ordinal and categorical variables cannot, because their
    codes are labels rather than amounts.

    A random variable is a numerical measurement of an outcome we cannot
    predict in advance. We write a random variable with a capital letter such
    as $X$. The number of emails you get in the next hour is a random
    variable, because before the hour starts we cannot say which value it
    will take, only which values are possible and roughly how likely each is.
    A person's hourly wage is a random variable when we picture drawing one
    person at random from the population, because we will not know that
    person's wage until we draw them.

    The probability distribution of a random variable describes how likely
    each of its possible values is. What this description looks like depends
    on whether the variable is discrete or continuous.

    A discrete random variable takes values that come in separate, countable
    steps, such as $0, 1, 2, 3, \ldots$ emails per hour. Its probability
    distribution lists the possible outcomes $x_1, x_2, \ldots, x_K$ together
    with the probability of each. We write $p_i = \Pr(X = x_i)$ for the
    probability that $X$ takes the particular value $x_i$. The cumulative
    probability distribution, written $\Pr(X \le x)$, is the probability that
    $X$ comes out at or below the value $x$. The table below is one possible
    distribution for the emails example. Most hours bring zero emails, a few
    bring one, and the chance of more than that drops off quickly.

    | Number of emails | 0 | 1 | 2 | 3 | 4 |
    |---|---|---|---|---|---|
    | Probability | 0.80 | 0.10 | 0.06 | 0.03 | 0.01 |
    | Cumulative probability | 0.80 | 0.90 | 0.96 | 0.99 | 1.00 |

    A continuous random variable takes values on a smooth range with no gaps,
    so it can equal \$18.46, \$18.47, \$18.461, or any nearby number. There
    are infinitely many such values, and we cannot list them, so we cannot
    give a probability to each one individually. Instead we describe the
    variable with a curve called the probability density function. The area
    under that curve between any two values is the probability that the
    variable falls between those two values. The cumulative distribution
    still gives the probability of being at or below a value, just as in the
    discrete case. The figure below uses hourly wages as the continuous
    example. The calculus version of these definitions sits in the appendix.
    """)
    return


@app.cell(hide_code=True)
def _(alt, mo, np, pd, stats):
    # Hourly wage modeled as a lognormal distribution (right-skewed).
    _dist = stats.lognorm(s=0.5, scale=20.0)
    _x = np.linspace(0.0, 80.0, 400)
    _frame = pd.DataFrame({
        "wage": _x,
        "pdf": _dist.pdf(_x),
        "cdf": _dist.cdf(_x),
    })

    _brush = alt.selection_interval(encodings=["x"], empty=False)

    _pdf_base = (
        alt.Chart(_frame)
        .mark_area(color="#1f4e79", opacity=0.18)
        .encode(
            x=alt.X("wage:Q", title="Hourly wage (USD)"),
            y=alt.Y("pdf:Q", title="Density"),
        )
    )
    _pdf_hl = (
        alt.Chart(_frame)
        .mark_area(color="#1f4e79", opacity=0.55)
        .encode(x="wage:Q", y="pdf:Q")
        .transform_filter(_brush)
    )
    _pdf_chart = (_pdf_base + _pdf_hl).properties(
        width=560, height=240,
        title="Probability density function (PDF)",
    )

    _cdf_line = (
        alt.Chart(_frame)
        .mark_line(color="#1f4e79", size=2)
        .encode(
            x=alt.X("wage:Q", title="Hourly wage (USD)"),
            y=alt.Y("cdf:Q", title="Cumulative probability"),
        )
    )

    # Aggregate both endpoints in one pass with unique output field names so
    # the upper- and lower-endpoint layers cannot collide on a shared field.
    _ep = (
        alt.Chart(_frame)
        .transform_filter(_brush)
        .transform_aggregate(
            lo_wage="min(wage)", hi_wage="max(wage)",
            lo_cdf="min(cdf)", hi_cdf="max(cdf)",
        )
        .transform_calculate(zero="0")
    )

    # Horizontal lines from the CDF curve back to the vertical axis at the two
    # selected wages, so the cumulative probabilities can be read off the axis.
    _h_lo = _ep.mark_rule(color="orange", strokeDash=[4, 3], size=2).encode(
        y="lo_cdf:Q", x="zero:Q", x2="lo_wage:Q",
    )
    _h_hi = _ep.mark_rule(color="orange", strokeDash=[4, 3], size=2).encode(
        y="hi_cdf:Q", x="zero:Q", x2="hi_wage:Q",
    )
    # Vertical lines from the x-axis up to the CDF curve at the selected wages.
    _v_lo = _ep.mark_rule(color="orange", strokeDash=[4, 3], size=2).encode(
        x="lo_wage:Q", y="zero:Q", y2="lo_cdf:Q",
    )
    _v_hi = _ep.mark_rule(color="orange", strokeDash=[4, 3], size=2).encode(
        x="hi_wage:Q", y="zero:Q", y2="hi_cdf:Q",
    )

    _cdf_chart = (_cdf_line + _h_lo + _h_hi + _v_lo + _v_hi).properties(
        width=560, height=240, title="Cumulative distribution function (CDF)",
    )

    # Declare the brush at the outermost level so both sub-views see it, then
    # wrap in mo.ui.altair_chart so the Python side can read the brushed range
    # and report the probability in the paragraph below.
    _combined = (
        alt.vconcat(_pdf_chart, _cdf_chart)
        .add_params(_brush)
    )
    wage_chart = mo.ui.altair_chart(
        _combined, chart_selection=False, legend_selection=False,
    )
    wage_dist = _dist
    wage_chart
    return wage_chart, wage_dist


@app.cell(hide_code=True)
def _(mo, wage_chart, wage_dist):
    _sel = wage_chart.value
    _intro = mo.md(
        "Drag across the top chart to pick a range of hourly wages. The dark "
        "shaded band that appears is the probability that a randomly chosen "
        "worker has a wage in that range. The lower chart updates at the "
        "same time, with dashed lines dropping from the cumulative "
        "distribution curve to the vertical axis at the two endpoints, so "
        "the cumulative probability at each end can be read off the axis."
    )
    if _sel is not None and len(_sel) > 0:
        _a = float(_sel["wage"].min())
        _b = float(_sel["wage"].max())
        _prob = float(wage_dist.cdf(_b) - wage_dist.cdf(_a))
        _caption_body = (
            f"You picked wages between &#36;{_a:,.0f} and &#36;{_b:,.0f}, "
            f"and the probability that a worker earns in that range is "
            f"{_prob:.2f}. This is also the vertical gap between the two "
            f"horizontal dashed lines on the cumulative distribution "
            f"chart, because the chance of being at or below the upper "
            f"wage minus the chance of being at or below the lower wage "
            f"is exactly the chance of falling between them."
        )
        _caption = mo.Html(
            '<div style="margin:0.2rem auto 1rem;max-width:560px;'
            'font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;">'
            + _caption_body
            + "</div>"
        )
        _output = mo.vstack([_caption, _intro])
    else:
        _output = _intro
    _output
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Describing a random variable

    Two numbers summarize most of what we care about in a random variable,
    its average and its spread. The expected value of $X$ is the long-run
    average of $X$ across many draws. We write it $\mathbb{E}[X] \equiv
    \mu_X$ and compute it as a weighted average of the possible outcomes,
    with each outcome weighted by its probability. When $X$ is discrete and
    takes $K$ possible values $x_1, \ldots, x_K$ with probabilities
    $p_i = \Pr(X = x_i)$,

    $$ \mathbb{E}[X] \equiv \mu_X = \sum_{i=1}^{K} x_i \cdot p_i. $$

    Outcomes that are more likely pull the average toward them, and outcomes
    that are unlikely barely move it.

    The variance of $X$ measures how spread out the outcomes of $X$ are
    around $\mu_X$. If most outcomes sit close to $\mu_X$, the variance is
    small. If outcomes routinely land far above and far below $\mu_X$, the
    variance is large. Formally,

    $$ \text{var}(X) \equiv \sigma_X^2 = \mathbb{E}\big[(X - \mathbb{E}[X])^2\big] = \sum_{i=1}^{K} (x_i - \mu_X)^2 \cdot p_i. $$

    The variance is in squared units, so a variance computed from wages in
    dollars comes out in dollars squared, which is hard to interpret. We
    usually report the spread instead as the standard deviation, the square
    root of the variance, $\text{sd}(X) = \sigma_X = \sqrt{\sigma_X^2}$,
    which is back in the original units of $X$.

    The expected value, the variance, and the standard deviation are
    properties of the true population distribution, so computing them
    requires the true probabilities $p_i$. With real data we never observe
    those probabilities. We instead have a sample of $n$ observed outcomes
    $X_1, X_2, \ldots, X_n$, from which we form the sample mean and the
    sample variance,

    $$ \hat{\mu}_X = \frac{1}{n} \sum_{i=1}^{n} X_i, \qquad \hat{\sigma}_X^2 = \frac{1}{n-1} \sum_{i=1}^{n} (X_i - \hat{\mu}_X)^2, $$

    with $\hat{\sigma}_X = \sqrt{\hat{\sigma}_X^2}$. The hat marks a quantity
    estimated from data, as opposed to the unobserved population value
    written without a hat. As $n$ grows the sample versions get close to the
    population versions, because outcomes show up in the sample in roughly
    the proportions given by their underlying probabilities. That result is
    the law of large numbers, which we come back to in Section 5.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <span style="color:#0b68cb">Example</span>

    Suppose the true distribution of emails per hour is the one from Section
    2, and that over 24 separate hours you record how many emails arrived in
    each one. The first row of the table lists the possible outcomes. The
    second row gives the true probabilities, which in reality we would not
    know. The third row gives the number of hours in which each outcome
    actually occurred.

    | Number of emails $x_i$ | 0 | 1 | 2 | 3 | 4 |
    |---|---|---|---|---|---|
    | Probability $p_i$ (unobserved) | 0.80 | 0.10 | 0.06 | 0.03 | 0.01 |
    | Hours with $x_i$ emails (observed) | 19 | 4 | 1 | 0 | 0 |

    If we knew the probabilities, the expected number of emails in an hour
    would be

    $$ \mu_X = \sum_{i=1}^{K} x_i \cdot p_i = 0 \times 0.80 + 1 \times 0.10 + 2 \times 0.06 + 3 \times 0.03 + 4 \times 0.01 = 0.35. $$

    In practice we do not know the probabilities, so we estimate the expected
    value with the sample mean of the 24 observed hours,

    $$ \hat{\mu}_X = \frac{1}{n} \sum_{i=1}^{n} X_i = \frac{1}{24}\big(0 \times 19 + 1 \times 4 + 2 \times 1 + 3 \times 0 + 4 \times 0\big) = 0.25. $$

    The sample mean of $0.25$ does not match the expected value of $0.35$
    because 24 hours is a small sample, and across those 24 hours the
    outcomes did not show up in exactly the proportions given by the
    underlying probabilities. With many more hours of data the counts in
    each column would line up closer to the probabilities, and the sample
    mean would land closer to $0.35$. That is the law of large numbers, in
    Section 5.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. The sample mean is random

    The sample mean is computed from random outcomes, so the sample mean is
    itself a random variable. The $0.25$ emails per hour we computed in the
    example above came from one particular set of 24 hours. If we sat at the
    desk for a different 24 hours and counted again, we would compute a
    different sample mean, perhaps $0.42$ or $0.29$. Repeat the experiment
    many times and the sample mean takes on its own distribution of values,
    with its own expected value and its own standard deviation.

    The expected value of the sample mean is the population expected value
    $\mu_X$. The standard deviation of the sample mean is the population
    standard deviation divided by $\sqrt{n}$,

    $$ \mathbb{E}[\hat{\mu}_X] = \mu_X, \qquad \sigma_{\hat{\mu}_X} = \frac{\sigma_X}{\sqrt{n}}. $$

    The first equation says that across many repeats of the experiment, the
    sample means average out to the true population mean. That is why
    $\hat{\mu}_X$ is a sensible guess for $\mu_X$ on any one run. The second
    equation says the sample mean's spread shrinks as the sample size $n$
    grows, so a larger sample produces a sample mean that lands closer to
    $\mu_X$. Because $\sigma_X$ is itself an unobserved property of the
    population, we approximate it with the sample standard deviation
    $\hat{\sigma}_X$, giving the standard error of the sample mean,

    $$ \text{se}(\hat{\mu}_X) = \frac{\hat{\sigma}_X}{\sqrt{n}}. $$

    The standard error is the spread of the sample mean as we can actually
    estimate it from one observed sample, and it is the quantity we will use
    later to build hypothesis tests and confidence intervals. Sections 5 and
    6 show the two facts above in simulations you can run yourself.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Law of large numbers

    The law of large numbers says that the sample mean $\hat{\mu}_X$ gets
    close to the true expected value $\mu_X$ when the sample is large. The
    reasoning was sketched in Section 3. Over many draws each outcome shows
    up in the sample in roughly the proportion its probability says it
    should, so the weighted average we compute from the sample, $\hat{\mu}_X$,
    lines up with the weighted average computed using the true probabilities,
    $\mu_X$.

    In a small sample the law has not had room to act. The sample mean of
    $0.25$ in the example landed below the truth of $0.35$ because random
    luck pushed the 24-hour count one way or the other. A sample of a
    hundred hours would be tighter, a sample of a thousand hours tighter
    still, and a sample of ten thousand hours would essentially land on
    $0.35$.

    Use the controls below. Pick a random process from the dropdown, set the
    number of draws, and click ''Draw new sample''. The wiggly line is the
    running sample mean, recomputed each time a new draw is added. The flat
    orange line is the true expected value of the chosen process. The
    running mean swings wildly when only a handful of draws are in, and
    settles onto the flat line as the sample grows. The same pattern holds
    for every process in the dropdown.
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
            "The wiggly line is the sample mean recomputed after each new "
            "draw. The flat orange line is the true expected value of the "
            "chosen process. With only a handful of draws the running mean "
            "lands almost anywhere. With thousands of draws it settles onto "
            "the flat line."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec6"></a>
    ## 6. Central limit theorem

    Picture running the same study many times. Each run uses a fresh sample
    of size $n$ from the same population, and each run produces one sample
    mean $\hat{\mu}_X$. The collection of those sample means, one per run, is
    itself a distribution. Section 4 already told us this distribution is
    centered on $\mu_X$ with spread $\sigma_X / \sqrt{n}$. The central limit
    theorem tells us about its shape. It says that for large enough $n$, the
    distribution of $\hat{\mu}_X$ is well approximated by a bell curve, the
    normal distribution we meet in Section 7,

    $$ \hat{\mu}_X \ \sim\ \mathcal{N}\!\left(\mu_X,\ \sigma_{\hat{\mu}_X}^2\right), $$

    where $\mathcal{N}(\mu_X, \sigma_{\hat{\mu}_X}^2)$ is the normal
    distribution with mean $\mu_X$ and variance
    $\sigma_{\hat{\mu}_X}^2 = \sigma_X^2 / n$, and $\sim$ is read as
    ''distributed as''. The remarkable part is that the approximation holds
    whether or not $X$ itself is normal. The raw outcomes can be sharply
    skewed or piled up at a single value, and as soon as $n$ is at all
    sizeable, the sample means computed from them line up on a bell curve.
    This is the result that lets us build hypothesis tests for the sample
    mean later in the course.

    Use the controls below. Pick a deliberately non-normal process, set the
    sample size $n$ behind each mean, and choose how many means to simulate.
    The left chart shows the shape of the raw process. The right chart shows
    the distribution of the simulated sample means, with the matching normal
    curve drawn on top. Set $n = 1$ and the means look just like the raw
    process, because in that case each ''mean'' is a single draw. Raise $n$
    and the right chart turns into a bell curve, no matter what shape the
    left chart has.
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
            "The left chart is the raw process you picked. The right chart "
            "is the distribution of the sample means from many fresh "
            "samples, with the matching normal curve drawn on top. Raising "
            "the sample size narrows the right chart and pulls its shape "
            "toward a bell curve, no matter what the left chart looks like."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec7"></a>
    ## 7. Common probability distributions

    A few continuous distributions come up so often in statistics and
    econometrics that they have names. The most important by a wide margin
    is the normal distribution.

    The normal distribution is a continuous, symmetric, bell-shaped
    distribution. Its shape is fixed once we choose two numbers, its mean
    $\mu$ and its variance $\sigma^2$, and we write it
    $\mathcal{N}(\mu, \sigma^2)$. The mean $\mu$ is where the peak of the
    bell sits on the horizontal axis. The variance $\sigma^2$ controls how
    wide the bell is around that peak, with larger $\sigma^2$ giving a wider
    bell. The area under the curve between $\mu - 1.96\sigma$ and
    $\mu + 1.96\sigma$ is exactly $0.95$, a fact we will use repeatedly
    later in the course. The reason the normal distribution shows up
    everywhere is the central limit theorem from the previous section.

    The standard normal distribution is the special normal with $\mu = 0$
    and $\sigma = 1$, written $\mathcal{N}(0, 1)$. It is the version
    tabulated in textbooks and built into every statistics package. Any
    normal variable can be turned into a standard normal by standardizing
    it. If $X \sim \mathcal{N}(\mu, \sigma^2)$, then

    $$ Z = \frac{X - \mu}{\sigma} \sim \mathcal{N}(0, 1). $$

    Standardizing has a plain interpretation. Subtracting $\mu$ shifts the
    variable so its center sits at zero, and dividing by $\sigma$ stretches
    or shrinks the variable so its spread is one. That is why two normal
    variables measured on different scales, for example test scores in
    points and wages in dollars, can be put on the same footing once each
    is standardized. Three further named distributions, the chi-squared,
    the $t$, and the $F$, come up later when we test hypotheses, and they
    are defined in the appendix.

    The figure below shows standardization in action. The slider $\mu$
    moves the normal on the left across the horizontal axis, the slider
    $\sigma$ widens or narrows it, and the chart on the right redraws the
    same variable after standardizing. The right chart never changes,
    because for any choice of $\mu$ and $\sigma$ the standardized version
    is always the standard normal $\mathcal{N}(0, 1)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    std_mu = mo.ui.slider(
        start=-3.0, stop=3.0, step=0.5, value=1.0,
        label=r"Mean $\mu$", show_value=True,
    )
    std_sigma = mo.ui.slider(
        start=0.5, stop=3.0, step=0.5, value=1.5,
        label=r"Standard deviation $\sigma$", show_value=True,
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
            x=alt.X("x:Q", title="Z = (X - μ) / σ"),
            y=alt.Y("density:Q", scale=alt.Scale(domain=[0, 0.85]), title="Density"),
        )
        .properties(width=250, height=240, title="X after standardizing")
    )

    mo.vstack([
        alt.hconcat(_left, _right),
        mo.md(
            r"The left chart is the normal $\mathcal{N}(\mu, \sigma^2)$ you "
            "set with the sliders. The right chart is the same variable "
            r"after standardizing with $Z = (X - \mu)/\sigma$. The right "
            "chart never moves, because the standardization always lands on "
            "the standard normal."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="appendix"></a>
    ## Appendix
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

    _text = mo.md(r"""
        This is bonus material. You will not need calculus on any quiz,
        problem set, or exam.

        When a random variable does not take a discrete set of values we call
        it continuous, and we cannot sum over its outcomes. The discrete
        formula $\mathbb{E}[X] = \sum_{i=1}^{K} x_i \cdot p_i$ no longer
        works, and the same is true for the variance. We use calculus
        instead, with the probability density function $f(x)$ in place of
        the probabilities,

        $$ \mathbb{E}[X] = \int x \cdot f(x)\,dx. $$

        The intuition is unchanged. We still add up each possible outcome
        $x$ weighted by its chance of occurring, with the integral playing
        the role the sum played in the discrete case.

        Two less common measures of spread are the skewness and the
        kurtosis. The skewness measures the tilt of a distribution and is
        zero when the distribution is symmetric, with a positive value
        meaning a long right tail. The kurtosis measures how much of the
        variance comes from extreme values far from the mean,

        $$ \text{skewness} = \frac{\mathbb{E}\big[(X - \mu_X)^3\big]}{\sigma_X^3}, \qquad \text{kurtosis} = \frac{\mathbb{E}\big[(X - \mu_X)^4\big]}{\sigma_X^4}. $$

        The expected value $\mathbb{E}[X]$ is also called the first moment
        of $X$, $\mathbb{E}[X^2]$ the second moment, and $\mathbb{E}[X^r]$
        the $r$-th moment. The variance, skewness, and kurtosis are built
        from the second, third, and fourth moments respectively.

        Three named distributions show up later when we test hypotheses. The
        chi-squared distribution is the distribution of a sum of $m$ squared
        independent standard normal variables, denoted $\chi^2_m$, where $m$
        is its degrees of freedom. The other two build on the chi-squared.
        Let $Z \sim \mathcal{N}(0, 1)$ and $W \sim \chi^2_m$ be independent,
        where $\sim$ is read as ''distributed as''. The statistic
        $T = Z / \sqrt{W/m}$ has a Student t distribution with $m$ degrees
        of freedom, denoted $t_m$. The t distribution has fatter tails than
        the standard normal and approaches $\mathcal{N}(0, 1)$ as $m$ grows.
        Now let $W \sim \chi^2_m$ and $V \sim \chi^2_n$ be independent. Then
        $F = (W/m)/(V/n)$ has an F distribution with $m$ numerator and $n$
        denominator degrees of freedom, denoted $F_{m,n}$, and it takes only
        positive values.

        The figure below shows these shapes. The t distribution approaches
        the standard normal as its degrees of freedom grow, while the
        chi-square and F distributions take only positive values and lean
        to the right.
        """)

    _caption = mo.md(
        "The solid line is the chosen distribution and the faint dashed line "
        "is the standard normal, shown for comparison. For F the slider sets "
        "the numerator degrees of freedom and the denominator is fixed at 10."
    )

    mo.accordion({
        "Bonus material (not on assessments)": mo.vstack([
            _text, appx_dist, appx_df, _chart, _caption,
        ]),
    })
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
