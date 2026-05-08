# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.5",
#     "numpy",
#     "pandas",
#     "altair",
# ]
# ///
import marimo

__generated_with = "0.23.3"
__description__ = "What econometrics is, descriptive vs causal questions, identification problems, and types of data."
app = marimo.App(
    width="compact",
    css_file="marimo-overrides.css",
    app_title="Lecture 1: Introduction to Econometrics",
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
            mo.md("# [Lecture 1](#top)"),
            mo.md("**Introduction to Econometrics**"),
            mo.nav_menu(
                {
                    "#sec1": "1. What is econometrics?",
                    "#sec2": "2. Descriptive vs causal",
                    "#sec3": "3. Education & earnings",
                    "#sec4": "4. Why isolating effects is hard",
                    "#sec5": "5. Sample and population",
                    "#sec6": "6. Types of data",
                    "#sec7": "7. Reading associations carefully",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self">Lecture 2 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 1: Introduction to Econometrics
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contents

    1. [What is econometrics?](#sec1)
    2. [It always begins with a question: descriptive vs causal](#sec2)
    3. [A causal question: education and earnings](#sec3)
    4. [Why isolating an effect is hard](#sec4)
    5. [From data to inference: sample and population](#sec5)
    6. [Types of data](#sec6)
    7. [Reading associations carefully](#sec7)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1) What is econometrics?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Econometrics is what you get when you use **structured thinking from economic theory** together with **statistical methods** to answer interesting questions about the economy. Stock and Watson put it succinctly: it is

    > "the science and art of using economic theory and statistical techniques to analyze economic data."

    Where does econometrics sit relative to neighbouring fields? Pure **economic theory** asks what *should* happen if agents and markets behave a certain way; pure **statistics** asks what patterns are present in some data without taking a strong stand on what generated them. Econometrics combines the two: theory disciplines what we look for, and statistics tells us how confident we can be about what we see.

    A few ways economists use the toolkit:

    - **Test economic theories.** Does the law of supply and demand hold for a particular good? Do consumers really equate marginal utility per dollar across goods?
    - **Forecast** future values of economic outcomes — GDP next year, unemployment next month, the price of electricity tomorrow.
    - **Apply mathematical models to real data.** How do interest-rate increases pass through to the stock market or to mortgage demand?
    - **Make quantitative policy recommendations.** How much would poverty change if the federal minimum wage rose to \$15? How many fewer cars would be sold under a carbon tax?

    For this class, the running theme is the third and fourth bullets: **using data to understand economic relationships in a complex world**, with a particular focus on quantifying how one variable changes another.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2) It always begins with a question: descriptive vs causal
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every econometric project starts with a question, and almost every such question falls into one of two camps.

    **Descriptive questions** ask: *what is the association between $X$ and $Y$?*

    - Do educated individuals earn more, on average?
    - Do students in smaller classes score higher on standardized tests?

    A descriptive analysis summarizes a pattern in the data. It does **not** claim that one variable causes the other. The pattern might be driven by something else entirely.

    **Causal questions** ask: *how does $X$ affect $Y$?*

    - How does an extra year of education affect earnings?
    - How does cutting class size by five students affect test scores?

    The phrasing is similar but the bar is much higher. A causal analysis tries to estimate how a change in $X$ would change $Y$ *holding all other factors constant*. That italicised phrase is doing a lot of work. It says: imagine intervening on a single individual or unit, changing only their value of $X$, and watching $Y$ respond — leaving everything else exactly as it was. Most of the difficulties in econometrics come from the fact that we almost never observe such a clean intervention; we only observe data where many things vary at once.

    This class focuses primarily on causal questions, but we'll spend real time on descriptive analysis too — partly because clear description is a prerequisite for honest causal claims.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3) A causal question: how does education affect earnings?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Consider one of the most studied questions in labor economics: *how does educational attainment affect earnings?* The U.S. Bureau of Labor Statistics publishes median weekly earnings by the highest degree completed. The 2023 figures look like this:
    """)
    return


@app.cell(hide_code=True)
def _(alt, mo, pd):
    bls = pd.DataFrame({
        "education": [
            "Less than high school", "High school diploma", "Some college, no degree",
            "Associate's", "Bachelor's", "Master's", "Professional", "Doctoral",
        ],
        "median_weekly_earnings": [708, 899, 992, 1058, 1493, 1737, 2206, 2109],
    })
    bls_chart = (
        alt.Chart(bls)
        .mark_bar(color="#1f4e79")
        .encode(
            x=alt.X("median_weekly_earnings:Q", title="Median weekly earnings (USD, 2023)"),
            y=alt.Y("education:N", sort=list(bls["education"]), title=None),
            tooltip=["education", "median_weekly_earnings"],
        )
        .properties(width=520, height=240, title="BLS, 2023")
    )
    mo.vstack([mo.md("**Median weekly earnings by education, U.S. workers age 25+**"), bls_chart])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The pattern is clear: people with more education earn more. So is the answer to "does education raise earnings?" simply *yes, by a lot*?

    Not so fast. The chart shows an **association** between education and earnings, not a **causal effect**. The people in the "Bachelor's" bar are not the same people as those in the "High school diploma" bar with four extra years of school added on. They differ in many other ways — family background, ability, occupation, where they live — and any of those differences could be doing some of the work that we're crediting to education. The next section is about exactly this problem.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4) Why isolating an effect is hard
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two recurring threats stand between an interesting association and a credible causal effect.

    **Omitted variable bias.** Some unobserved third variable, $Z$, drives both $X$ and $Y$. If we ignore $Z$, the simple relationship between $X$ and $Y$ mixes up the true effect of $X$ on $Y$ with the effect of $Z$. Family income is a classic suspect for the education–earnings question: children from higher-income families tend to get more education *and* tend to earn more later in life for reasons unrelated to their schooling.

    **Reverse causality.** Sometimes $Y$ also affects $X$, not just the other way around. Police presence and crime is the textbook example: more police likely reduce crime, but high-crime areas attract more police. With observational data alone we cannot easily separate the two arrows.

    Both problems share the same root: in observational data, $X$ varies for many reasons, and only some of those reasons reflect a genuine causal channel from $X$ to $Y$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A small numerical illustration of omitted variable bias

    To make this concrete, let's simulate a world in which we know the true causal effect — and then watch a naive analysis get the wrong answer.

    Suppose family income causes both education and earnings, while education *also* causes earnings:

    - $\text{income} \sim \mathcal{N}(50, 15^2)$ (in thousands of dollars)
    - $\text{education} = 12 + 0.05 \cdot \text{income} + \varepsilon_e$, with $\varepsilon_e \sim \mathcal{N}(0, 1.5^2)$
    - $\text{earnings} = 5 + 2 \cdot \text{education} + 0.4 \cdot \text{income} + \varepsilon_y$, with $\varepsilon_y \sim \mathcal{N}(0, 5^2)$

    The **true causal effect** of one extra year of education on earnings is `2`. Family income is the omitted variable. Let's see what a naive simple regression of earnings on education recovers.
    """)
    return


@app.cell
def _(np, pd):
    rng = np.random.default_rng(0)
    n = 5_000
    income = rng.normal(50, 15, n)
    education = 12 + 0.05 * income + rng.normal(0, 1.5, n)
    earnings = 5 + 2.0 * education + 0.4 * income + rng.normal(0, 5, n)
    sim = pd.DataFrame({"income": income, "education": education, "earnings": earnings})

    naive_slope = np.polyfit(sim["education"], sim["earnings"], 1)[0]

    X = np.column_stack([np.ones(n), sim["education"], sim["income"]])
    beta_full, *_ = np.linalg.lstsq(X, sim["earnings"], rcond=None)
    controlled_slope = beta_full[1]
    return controlled_slope, naive_slope, sim


@app.cell(hide_code=True)
def _(controlled_slope, mo, naive_slope):
    mo.md(rf"""
    | Estimator | Slope on `education` |
    |---|---|
    | Naive (earnings on education only) | **{naive_slope:.2f}** |
    | Controlling for income (earnings on education *and* income) | **{controlled_slope:.2f}** |
    | True causal effect | **2.00** |

    The naive slope is biased upward because family income lurks behind both education and earnings: students with richer parents end up with more education *and* more earnings, so a regression that ignores income gives education credit for some of income's effect. Adding income as a control roughly recovers the true effect.

    The plot below shows the same intuition visually. The orange line is the naive fit; the cloud of points is colour-coded by income tertile. Within any single tertile, the slope is much closer to the true effect — pointing at exactly the bias that omitted variables introduce.
    """)
    return


@app.cell(hide_code=True)
def _(alt, mo, pd, sim):
    sim_plot = sim.assign(
        income_tertile=pd.qcut(sim["income"], 3, labels=["Low income", "Mid income", "High income"]).astype(str)
    ).sample(800, random_state=0)
    points = (
        alt.Chart(sim_plot)
        .mark_circle(opacity=0.5, size=20)
        .encode(
            x=alt.X("education:Q", title="Years of education"),
            y=alt.Y("earnings:Q", title="Earnings ($000s)"),
            color=alt.Color("income_tertile:N", title="Family income"),
        )
    )
    naive_line = (
        alt.Chart(sim_plot)
        .transform_regression("education", "earnings")
        .mark_line(color="orange", size=3)
        .encode(x="education:Q", y="earnings:Q")
    )
    mo.vstack([
        mo.md("**Education vs earnings, simulated data with income as an omitted variable**"),
        (points + naive_line).properties(width=560, height=320),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Reverse causality is harder to demonstrate cleanly with one regression and we won't simulate it here, but the intuition is symmetric: if higher earnings let people afford more schooling — perhaps by funding graduate degrees — then a simple regression of earnings on education is again recovering a mixture of two arrows, not the single arrow we wanted.

    Most of this class is about the tools economists use to defend against omitted variable bias and reverse causality: control variables, panel data, instrumental variables, randomised experiments, and quasi-experiments.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5) From data to inference: sample and population
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A research question is almost always about a **population of interest** — the full group we want to learn about. "How does education affect earnings?" might really mean *all U.S. workers age 25 and over*, or *low-income Americans*, or *first-generation college students in California*. The population is conceptual; we usually cannot observe all of it.

    What we *can* observe is a **sample**: a finite subset of the population that ends up in our dataset. Everything we know about the population comes through the sample. **Statistical inference** is the discipline of using the sample to make calibrated statements about the population — point estimates, confidence intervals, hypothesis tests — while honestly accounting for the fact that a different sample would have given somewhat different answers.

    A small simulation makes the relationship between population and sample concrete. Suppose the population's true mean weekly earnings is \$1,170 (the BLS overall figure). Imagine drawing 200 independent samples of 50 workers each from that population and computing the sample mean of each one.
    """)
    return


@app.cell
def _(np, pd):
    rng_pop = np.random.default_rng(7)
    pop_mean = 1170
    pop_sd = 600
    n_samples = 200
    sample_size = 50

    sample_means = pd.DataFrame({
        "draw": np.arange(n_samples),
        "sample_mean": [
            rng_pop.normal(pop_mean, pop_sd, sample_size).mean()
            for _ in range(n_samples)
        ],
    })
    return pop_mean, sample_means, sample_size


@app.cell(hide_code=True)
def _(alt, mo, pop_mean, sample_means, sample_size):
    hist = (
        alt.Chart(sample_means)
        .mark_bar(color="#1f4e79", opacity=0.85)
        .encode(
            x=alt.X("sample_mean:Q", bin=alt.Bin(maxbins=25), title="Sample mean of weekly earnings (USD)"),
            y=alt.Y("count()", title="Number of samples"),
        )
    )
    pop_rule = (
        alt.Chart(alt.InlineData(values=[{"x": pop_mean}]))
        .mark_rule(color="orange", size=3)
        .encode(x="x:Q")
    )
    n_draws = len(sample_means)
    mo.vstack([
        mo.md(f"**Sampling distribution: {n_draws} samples of {sample_size} workers each**"),
        (hist + pop_rule).properties(width=560, height=260),
        mo.md(
            f"The orange line is the true population mean (\\${pop_mean:,}). "
            f"The bars show the spread of sample means across the {n_draws} repeated draws. "
            "Each individual sample is wrong by some amount; the *distribution* of those errors is what statistical inference describes — and what lets us turn one sample into a calibrated claim about the population."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec6"></a>
    ## 6) Types of data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Econometricians work with two broad kinds of data, distinguished by how they were generated.

    **Primary data** are collected by the researcher — typically through experiments, surveys, or interviews designed for the question at hand. Lab and field experiments are the cleanest setting for causal inference because the researcher controls who receives the treatment.

    **Observational data** (sometimes called *secondary* data) record behaviour from real-world, non-experimental settings. Most data economists touch falls in this bucket. Observational datasets come in three shapes, and the shape determines what kinds of questions are answerable.
    """)
    return


@app.cell(hide_code=True)
def _(mo, pd):
    cross_section = pd.DataFrame({
        "person_id": [1, 2, 3, 4],
        "year": [2023, 2023, 2023, 2023],
        "education": [12, 16, 14, 18],
        "earnings": [42_000, 71_000, 58_000, 95_000],
    })
    mo.vstack([
        mo.md("**Cross-sectional data** — many entities, single point in time. Example: the Demographic and Health Survey of Mexico (1987)."),
        cross_section,
    ])
    return


@app.cell(hide_code=True)
def _(mo, pd):
    time_series = pd.DataFrame({
        "country": ["USA"] * 4,
        "year": [2020, 2021, 2022, 2023],
        "unemployment_rate": [8.1, 5.4, 3.6, 3.7],
    })
    mo.vstack([
        mo.md("**Time-series data** — one entity tracked over many time periods. Example: BLS monthly unemployment rate."),
        time_series,
    ])
    return


@app.cell(hide_code=True)
def _(mo, pd):
    panel = pd.DataFrame({
        "person_id": [1, 1, 2, 2, 3, 3],
        "year": [2022, 2023, 2022, 2023, 2022, 2023],
        "education": [12, 13, 16, 16, 14, 15],
        "earnings": [40_000, 44_000, 70_000, 73_000, 56_000, 60_000],
    })
    mo.vstack([
        mo.md("**Panel (longitudinal) data** — many entities, each observed over many time periods. Examples: the PSID, the National Longitudinal Surveys."),
        panel,
        mo.md(
            "Panel data are especially valuable for causal inference because we can see the *same* person change over time, "
            "letting us strip out fixed characteristics of that person that would otherwise act as omitted variables."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec7"></a>
    ## 7) Reading associations carefully
    """)
    return


@app.cell(hide_code=True)
def _(mo, pd):
    interpret = pd.DataFrame({
        "Relationship": [
            "Housing prices vs house size",
            "Crime vs police presence",
            "Sales vs advertising",
            "Firm performance vs CEO pay",
            "Innovation vs R&D spending",
        ],
        "What we see in the data": [
            "Bigger homes sell for more.",
            "More police stationed in higher-crime areas.",
            "Periods with more ads coincide with higher sales.",
            "Higher-paid CEOs run stronger firms, on average.",
            "Firms that spend more on R&D file more patents.",
        ],
        "Why simple causal reading is risky": [
            "Bigger homes also sit in 'better' neighbourhoods — location is an omitted variable.",
            "Reverse causality: police likely reduce crime, but crime also draws police.",
            "Seasonality affects both ads and sales — an omitted variable inflates the link.",
            "Reverse causality: strong performance permits higher pay, not just the other way around.",
            "Reverse causality: success in innovation can fund still more R&D.",
        ],
    })
    mo.vstack([
        mo.md(
            "Each row below describes a tempting causal story and the threat that complicates it. "
            "These are the kinds of subtleties we'll learn to handle later when we study regression, panel methods, and instrumental variables."
        ),
        interpret,
        mo.md(
            "**Takeaway.** The same regression coefficient can mean very different things depending on what you've been able to control for and what you can plausibly assume about the data-generating process. "
            "Most of the rest of this course is about making those assumptions explicit and disciplined."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self">← Course home</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self">Lecture 2 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
