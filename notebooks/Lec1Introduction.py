# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "pandas",
#     "altair",
# ]
# ///

import marimo

__generated_with = "0.23.6"
app = marimo.App(
    app_title="Lecture 1: Introduction to Econometrics",
    css_file="marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt

    return alt, mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md(
                '<div>'
                '<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: flex; align-items: center; gap: 0.5em; margin: 0;">'
                '<img src="https://robert-french.github.io/Econometrics/LMU_SquareOrig.png" alt="" style="height: 1.6em; width: auto; display: block;">'
                '<span>ECON 3300 Course home</span>'
                '</a>'
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Lecture 1</a></h1>'
                '</div>'
            ),
            mo.md("**Introduction to Econometrics**"),
            mo.nav_menu(
                {
                    "#sec1": "1. What is econometrics?",
                    "#sec2": "2. Descriptive and causal questions",
                    "#sec3": "3. Education and earnings",
                    "#sec4": "4. Why causal questions are hard",
                    "#sec5": "5. Populations and samples",
                    "#sec6": "6. Types of data",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/pdf/Lec1Introduction.pdf" target="_blank">Download PDF</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec2RandomVariables.html" target="_self">Lecture 2 →</a>'),
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
    2. [Descriptive and causal questions](#sec2)
    3. [Education and earnings](#sec3)
    4. [Why causal questions are hard](#sec4)
    5. [Populations and samples](#sec5)
    6. [Types of data](#sec6)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. What is econometrics?

    Econometrics is the use of statistical methods to measure economic
    relationships in data.

    Economic theory gives us a way to think about how different things are related. It tells us, for example, that when the price of a good rises, people usually buy less of it. Statistics gives us general tools for learning from data, including ways to summarize data points, estimate relationships between different things we observe, and measure how much an estimate might change if we collected new data. Econometrics applies those tools to economic questions by asking whether the relationships predicted by theory appear in real data, how large they are, and how confident we should be in the results. For example, econometrics uses data to estimate how much less people actually buy when the price of a good rises.

    Econometrics helps economists move from ideas to evidence. Economists use econometrics to test whether a prediction from theory appears in real data, like whether the quantity people buy really falls as price rises. They use econometrics to forecast future values, such as next quarter's GDP or next month's unemployment rate. They also use econometrics to estimate how much one thing changes another so that policies can be judged, for example how many jobs are gained or lost when the minimum wage rises by one dollar. In each case, econometrics gives economists a disciplined way to turn data into evidence about economic relationships.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Descriptive and causal questions

    Econometrics typically begins by turning broad economic ideas into questions that can be answered with data.

    A *descriptive question* asks how two things are related in the data we already have. ''Do people with more education earn more, on average?'' is a descriptive question. We can answer it by computing average earnings at each education level and comparing those averages. The answer describes a pattern in the data, but it does not tell us why the pattern exists.

    A *causal question* asks how an outcome would change if we changed one thing while holding everything else fixed. ''If this person stayed in school one more year, how much would their earnings rise?'' is a causal question. We cannot answer it just by comparing a college graduate to a high school graduate, because they are different people who may differ in family background, ability, motivation, and many other ways. A clean answer would compare the same person with and without the additional schooling, but we never observe both outcomes for the same person.

    This course is mostly about causal questions. Still, descriptive questions matter in their own right because many economic questions begin with knowing what patterns exist in the data. They also matter because causal arguments usually build from those patterns. If we measure or summarize the pattern badly, we will have a weak starting point for deciding what caused it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Education and earnings example

    The link between education and earnings shows the gap between a descriptive
    answer and a causal one in concrete numbers.

    The U.S. Bureau of Labor Statistics (BLS) reports the median weekly earnings of
    full-time workers aged 25 and over by the highest degree they have completed.
    The 2023 figures are shown below.
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
    mo.vstack([
        mo.md("Median weekly earnings by education, U.S. workers age 25 and over"),
        bls_chart,
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Median weekly earnings climb from \$708 for workers without a high school
    diploma to \$899 with a diploma, \$1,493 with a bachelor's degree, and \$2,109
    with a doctorate. The descriptive answer is that each step up in education (aside
    from doctoral degrees) is associated with higher pay.

    That \$594 difference between a high school diploma and a bachelor's degree is
    not yet the causal effect of the degree. The workers in the bachelor's bar are
    not the high school workers with four years of school added on; they are
    different people who, on average, also grew up in higher-income families and
    had more opportunities, and many of them would have out-earned the high school
    group even without the degree. Some of the \$594 reflects those prior
    differences between the two groups, and only the remainder is caused by the
    education itself. Section 4 explains why separating the two is hard, and the
    later lectures will help us build the tools to do exactly this.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Why causal questions are hard to answer

    Causal questions are hard to answer for two main reasons: omitted variables and reverse causality.

    A *variable* is something we can measure that differs across observations, such as a person's schooling, earnings, age, or family income. An *omitted variable* is a factor that affects both the variable we are focused on and the outcome, but that we cannot measure or did not hold constant in the comparison. Family income is an omitted variable in the education-and-earnings comparison. Children from higher-income families complete more schooling on average, and they also tend to earn more as adults for reasons that do not come directly from schooling, such as family wealth and connections. Because the high school group and the bachelor's group differ in average family income, part of the $594 gap reflects the effect of family income rather than the effect of education alone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _svg = r'''<svg viewBox="0 0 520 220" width="100%" style="max-width:520px;height:auto;font-family:inherit" role="img" aria-label="Family income raises both education and earnings; education also raises earnings"><defs><marker id="ahb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#1f4e79"/></marker><marker id="ahg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#8a93a2"/></marker></defs><line x1="232" y1="64" x2="146" y2="148" stroke="#8a93a2" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#ahg)"/><line x1="288" y1="64" x2="374" y2="148" stroke="#8a93a2" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#ahg)"/><line x1="177" y1="172" x2="343" y2="172" stroke="#1f4e79" stroke-width="2" marker-end="url(#ahb)"/><rect x="200" y="20" width="120" height="44" rx="8" fill="#f1f3f5" stroke="#8a93a2" stroke-width="2" stroke-dasharray="5,4"/><text x="260" y="47" text-anchor="middle" font-size="15" fill="#6b7280">Family income</text><rect x="55" y="150" width="120" height="44" rx="8" fill="#eef3f8" stroke="#1f4e79" stroke-width="2"/><text x="115" y="177" text-anchor="middle" font-size="15" fill="#1f4e79">Education</text><rect x="345" y="150" width="120" height="44" rx="8" fill="#eef3f8" stroke="#1f4e79" stroke-width="2"/><text x="405" y="177" text-anchor="middle" font-size="15" fill="#1f4e79">Earnings</text></svg>'''
    _caption = "Each arrow runs from a cause to what it changes. Family income typically raises both education and earnings, so leaving it out overstates the effect of education on earnings."
    mo.Html(
        '<figure style="max-width:560px;margin:2rem auto;text-align:center;">'
        + _svg
        + '<figcaption style="margin:0.7rem auto 0;max-width:560px;font-size:0.85rem;line-height:1.45;color:#6b7280;">'
        + _caption
        + "</figcaption></figure>"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Reverse causality* is the case where the outcome also changes the variable we
    are studying, so causality runs in both directions. Consider the relationship between police presence and crime rates. Adding police to a neighborhood may lower its crime, but city
    governments also assign more police to the neighborhoods where crime is already
    highest. A comparison of police numbers and crime numbers across neighborhoods
    therefore contains both "more police lower crime" and "more crime brings more
    police," and the raw comparison cannot separate these two effects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _svg = r'''<svg viewBox="0 0 520 180" width="100%" style="max-width:520px;height:auto;font-family:inherit" role="img" aria-label="Police lowers crime and crime raises police at the same time"><defs><marker id="ahr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#1f4e79"/></marker></defs><path d="M192,80 Q260,26 326,80" fill="none" stroke="#1f4e79" stroke-width="2" marker-end="url(#ahr)"/><path d="M328,100 Q260,154 194,100" fill="none" stroke="#1f4e79" stroke-width="2" marker-end="url(#ahr)"/><text x="260" y="18" text-anchor="middle" font-size="13" fill="#6b7280">more police may reduce crime</text><text x="260" y="172" text-anchor="middle" font-size="13" fill="#6b7280">more crime may bring more police</text><rect x="70" y="68" width="120" height="44" rx="8" fill="#eef3f8" stroke="#1f4e79" stroke-width="2"/><text x="130" y="95" text-anchor="middle" font-size="15" fill="#1f4e79">Police</text><rect x="330" y="68" width="120" height="44" rx="8" fill="#eef3f8" stroke="#1f4e79" stroke-width="2"/><text x="390" y="95" text-anchor="middle" font-size="15" fill="#1f4e79">Crime</text></svg>'''
    _caption = "Both arrows reflect causal relationships occurring at the same time. Police may affect crime and crime may affect police presence, so the simple comparison measures neither on its own."
    mo.Html(
        '<figure style="max-width:560px;margin:2rem auto;text-align:center;">'
        + _svg
        + '<figcaption style="margin:0.7rem auto 0;max-width:560px;font-size:0.85rem;line-height:1.45;color:#6b7280;">'
        + _caption
        + "</figcaption></figure>"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Omitted variable bias and reverse causality are common because we usually observe relationships as they occur in the real world. The variables we study often differ across people, firms, or places for many reasons at once, and some of those reasons may also affect the outcome we want to explain. This makes it difficult to separate the relationship of interest from other differences in the data. The direction of causality can also be unclear, since the outcome may affect our variable of interest rather than only the other way around. Later lectures introduce methods that help hold other factors constant and better isolate causal relationships.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Populations and samples

    Every estimate in this course is computed from a limited set of data, but it is usually meant to tell us something about a larger setting that we never observe in full.

    In econometrics, the *population* is what we want to learn about. Sometimes the population is a concrete group, such as all U.S. workers. More generally, it is the broader setting that our data come from, including the relationships among the things we observe. For example, if we study earnings, education, and age using data on a group of workers, we usually want to learn how these things are related beyond the particular workers in our dataset.

    A *sample* is the finite set of observations we actually have, such as the weekly earnings of the roughly sixty thousand households the Census Bureau contacts each month on behalf of the BLS. Because we usually observe only a sample, any claim about the population must be inferred from limited data. A different sample collected in the same way would usually produce somewhat different numbers. *Statistical inference* gives us methods for using one sample to draw conclusions about the population while also describing how far our estimates might be from the truth. The rest of the course introduces the econometric tools used to conduct statistical inference for economic relationships.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec6"></a>
    ## 6. Types of data

    How a dataset is organized decides which questions it can answer.

    - **Cross-sectional data** measure many different units once, at about the same
      time, such as the earnings and education of 60,000 different workers surveyed
      in 2023. They show how earnings differ across people but cannot show how one
      person's earnings change as that person gets more schooling.
    - **Time-series data** measure one unit repeatedly over time, such as the U.S.
      unemployment rate every month from 1948 to today. They show how that unit's
      value moves over time but cannot compare different units, for example two
      countries' unemployment rates in the same month.
    - **Panel data** measure the same many units repeatedly over time, such as the
      same 5,000 workers interviewed every year for ten years. Because each worker
      is seen more than once, traits of a worker that never change, such as where
      they grew up, can be held constant, which removes them as omitted variables.

    We will encounter each of these data types during the course.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** variable, omitted variable, population, "
            "sample, cross-sectional data, time-series data, panel data.\n\n"
            "**Concepts:** descriptive question, causal question, "
            "reverse causality, statistical inference."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self">← Course home</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec2RandomVariables.html" target="_self">Lecture 2 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
