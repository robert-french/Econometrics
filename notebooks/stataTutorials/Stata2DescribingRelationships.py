# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(
    app_title="Stata Tutorial 2: Describing Data and Relationships",
    css_file="../marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


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
                '</div>'
            ),
            mo.md(
                r"""
                <div style="font-weight: 700; font-size: 1.05em;">Stata Tutorials</div>

                1. <a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata1GettingStarted.html" target="_self">Getting Started with Stata</a>
                2. **[Describing Data and Relationships](#top)**
                    1. [Picking up where we left off](#sec1)
                    1. [One variable at a time](#sec2)
                    1. [Comparing groups](#sec3)
                    1. [Scatter plots](#sec4)
                    1. [Covariance and correlation](#sec5)
                3. <span class="soon">Simple Regression</span>
                4. <span class="soon">Multiple Regression and Regression Tables</span>
                5. <span class="soon">Nonlinear Specifications</span>
                6. <span class="soon">Panel Data</span>
                """
            ),
        ],
        width="350px",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata1GettingStarted.html" target="_self">← Stata Tutorial 1</a>'),
            mo.md('<span class="nav-soon">Stata Tutorial 3 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Stata Tutorial 2: Describing Data and Relationships
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contents

    2.1 [Picking up where we left off](#sec1)<br>
    2.2 [One variable at a time](#sec2)<br>
    2.3 [Comparing groups](#sec3)<br>
    2.4 [Scatter plots](#sec4)<br>
    2.5 [Covariance and correlation](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 2.1 Picking up where we left off

    This tutorial continues in the do-file you built in the first tutorial. Open Stata, open `tutorial1.do` in the Do-file Editor, and run it from the top with the Execute (do) button to make sure the dataset loads. Then add a comment line at the bottom so you can find today's work later.

    ```stata
    * Stata Tutorial 2
    ```

    Everything you add today goes below this line. Each time you add commands, rerun the whole do-file rather than the new lines alone, so that the `use` command at the top reloads a clean copy of the data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2.2 One variable at a time

    Before studying how two variables move together, let's look at each one on its own. Add these four lines to your do-file and rerun it.

    ```stata
    summarize earnings, detail
    histogram earnings, normal
    tabulate education
    tabulate sex
    ```

    **`summarize`** with the **`detail`** option reports the percentiles of `earnings` alongside its mean and standard deviation. The 50th percentile is the median, the earnings level that half of the sample falls below, and the 25th and 75th percentiles bracket the middle half of the sample. Compare the median with the mean. When the mean sits well above the median, a small number of high earners are pulling the mean upward, which is common in earnings data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot1_summarize_detail.png" alt="summarize earnings, detail output" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`histogram`** plots the sample distribution in a separate Graph window. Each bar's height shows how much of the sample falls in that range of earnings, so the histogram is the sample counterpart of the probability density function from Lecture 2. The `normal` option overlays a normal curve with the same mean and standard deviation as the data, which makes it easy to see how far the sample distribution is from a bell shape.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot2_histogram.png" alt="Histogram of earnings with a normal curve overlaid" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`tabulate`** lists each category of a variable, the number of observations in that category (`Freq.`), its share of the sample (`Percent`), and the running total of those shares (`Cum.`). The `Percent` column is the sample analogue of the probability distribution table from Lecture 2, while the `Cum.` column is the sample analogue of its cumulative distribution. `tabulate` is especially useful for discrete variables with only a few possible values. It also works with the string variable `sex` because counting categories does not require arithmetic.<sup><a id="fnref1" href="#fn1">1</a></sup>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot3_tabulate.png" alt="tabulate output for education and sex" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 2.3 Comparing groups

    The simplest way to see whether two variables are related is to split the sample into groups defined by one variable and compare the average of the other variable across the groups. Lecture 6 calls the population version of this a conditional expectation, $\mathbb{E}[Y \mid X = x]$, the average of $Y$ among observations with a given value of $X$. The `tabstat` command computes the sample version. Add these lines and rerun the do-file.

    ```stata
    tabstat earnings, by(education) statistics(mean sd n)
    tabstat earnings, by(sex) statistics(mean sd n)
    ```

    The `by()` option splits the sample into groups, and the `statistics()` option chooses which numbers to report for each group. The first table has one row per education category showing the mean, the standard deviation, and the number of people in that group, followed by a `Total` row for the whole sample. Average earnings rise from one education category to the next, which is the association that Lecture 5 summarized with a regression line. The second table works even though `sex` is a string variable, because `by()` only needs to sort people into groups.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot4_tabstat.png" alt="tabstat output for earnings by education and by sex" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 2.4 Scatter plots

    Group averages work well when the grouping variable takes only a few values. When both variables take many values, as is common with continuous variables, a scatter plot might be more appropriate because it shows the full relationship at once, with one point for each observation. Add these lines to your do-file and rerun it.

    ```stata
    twoway (scatter earnings age) (lfit earnings age)
    twoway (scatter earnings education, jitter(5)) (lfit earnings education)
    ```

    A `twoway` command combines plots, each in its own parentheses. The `scatter` plot draws one point per person, listing the vertical-axis variable first and the horizontal-axis variable second, and the `lfit` plot adds the least-squares line introduced in Lecture 5.

    In the second graph, the points would normally stack into four vertical columns, one for each education category, with many observations lying directly on top of one another. The `jitter()` option nudges each point by a small random amount so that the columns spread into visible clouds. The number inside `jitter()` controls how much nudging is applied. Compare the height of each cloud with the group means from tabstat in Section 3. They show the same relationship in two different ways.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot5_scatter_age.png" alt="Scatter plot of earnings against age with a fitted line" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot6_scatter_education.png" alt="Jittered scatter plot of earnings against education with a fitted line" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 2.5 Covariance and correlation

    Lecture 3 introduced two numbers that summarize a scatter plot. The covariance measures whether two variables move together, and the correlation rescales it to lie between $-1$ and $1$. The `correlate` command computes both the covariance and correlation for every pair of variables you list. Add these lines and rerun the do-file.

    ```stata
    correlate earnings education age
    correlate earnings education age, covariance
    ```

    The first table lists the variables along both its rows and its columns, and each entry is the sample correlation between the row variable and the column variable. You will see that the diagonal entries are all ones, since every variable is perfectly correlated with itself, and only the entries below the diagonal are printed because the correlation between `earnings` and `education` is the same as the correlation between `education` and `earnings`.

    With the `covariance` option, the diagonal entires record each variable's sample variance and the off-diagonal entries are the sample covariances. These numbers are harder to read because they are measured in the units of both of its variables. The covariance between `earnings` and `education` is measured in dollars times education categories, and the variance of `earnings` is in dollars squared. This is why we usually report correlations, which always lie between -1 and 1.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot7_correlate.png" alt="correlate output with and without the covariance option" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In Stata, we can also build sample statistics from their underlying formulas. We will now compute the sample covariance step by step and check that Stata’s built-in commands produce the same result. Along the way, we will introduce the `generate` and `egen` commands. Recall that the sample covariance formula is,

    $$
    \hat{\sigma}_{XY} = \frac{1}{n-1}\sum_{i=1}^{n}(X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y).
    $$

    Now, add these lines and rerun the do-file.

    ```stata
    egen meanEarnings = mean(earnings)
    egen meanEducation = mean(education)
    generate product = (earnings - meanEarnings) * (education - meanEducation)
    summarize product
    display r(sum) / (r(N) - 1)
    drop meanEarnings meanEducation product
    ```

    The two `egen` lines create variables holding the sample mean of `earnings` and of `education` in every row, and `generate` creates a new variable containing the product of the two deviations for each person. After `summarize` runs, Stata keeps its results in memory for the next command, with the sum of the variable stored as `r(sum)` and the number of observations as `r(N)`, so the `display` line prints the sample covariance. Compare it with the `earnings` and `education` entry in the `correlate, covariance` table and see whether they match. The final `drop` line removes the three helper variables so the dataset stays tidy.

    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot8_hand_check.png" alt="summarize product and display output reproducing the sample covariance" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Your do-file should now look something like this, with the Tutorial 1 lines at the top and today's lines below them.

    ```stata
    * Stata Tutorial 1
    * Your name, and today's date

    local dataFolder "C:/Users/yourname/Documents/ECON3300/data"
    use "`dataFolder'/econ3300_educ_income_2024.dta", clear

    describe
    summarize earnings education

    * Stata Tutorial 2

    summarize earnings, detail
    histogram earnings, normal
    tabulate education
    tabulate sex

    tabstat earnings, by(education) statistics(mean sd n)
    tabstat earnings, by(sex) statistics(mean sd n)

    twoway (scatter earnings age) (lfit earnings age)
    twoway (scatter earnings education, jitter(5)) (lfit earnings education)

    correlate earnings education age
    correlate earnings education age, covariance

    egen meanEarnings = mean(earnings)
    egen meanEducation = mean(education)
    generate product = (earnings - meanEarnings) * (education - meanEducation)
    summarize product
    display r(sum) / (r(N) - 1)
    drop meanEarnings meanEducation product
    ```

    Save your do-file. The next tutorial picks up here and turns the fitted lines you drew today into regression output.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** string variable, value label, percentile, median, "
            "`summarize, detail`, `histogram`, `tabulate`, `tabstat`, "
            "`twoway scatter`, `lfit`, `jitter()`, `correlate`, `egen`, "
            "`generate`, `drop`, stored results `r()`.\n\n"
            "**Habits:** look at each variable on its own before relating two "
            "of them; use group means for variables with a few categories and "
            "scatter plots for variables with many values; report correlations "
            "rather than covariances because they have no units."
        ),
        title="Key terms and habits",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** A *string variable* stores text rather than numbers. In this dataset `sex` holds the words `Male` and `Female`, and the Variables pane lists its storage type as `str6`. Stata can count and group the values of a string variable, but it cannot do arithmetic with them, so commands such as `summarize` and `correlate` require numeric variables like `education`, `age`, and `earnings`. <a href="#fnref1" title="Back to text">&#8617;</a></span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata1GettingStarted.html" target="_self">← Stata Tutorial 1</a>'),
            mo.md('<span class="nav-soon">Stata Tutorial 3 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
