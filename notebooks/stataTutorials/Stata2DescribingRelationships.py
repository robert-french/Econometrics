# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
# ]
# ///

import marimo

__generated_with = "0.24.0"
__preliminary__ = True
__description__ = "Distributions, group averages, scatter plots, and correlation in Stata."
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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Stata Tutorial 2</a></h1>'
                '</div>'
            ),
            mo.md(
                r"""
                **Describing Data and Relationships**

                1. [Picking up where we left off](#sec1)
                1. [One variable at a time](#sec2)
                1. [Comparing groups](#sec3)
                1. [Scatter plots](#sec4)
                1. [Covariance and correlation](#sec5)
                """
            ),
        ],
        width="300px",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    <a href="https://robert-french.github.io/Econometrics/" target="_self">← Course home</a>
    """)
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

    1 [Picking up where we left off](#sec1)<br>
    2 [One variable at a time](#sec2)<br>
    3 [Comparing groups](#sec3)<br>
    4 [Scatter plots](#sec4)<br>
    5 [Covariance and correlation](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1 Picking up where we left off

    This tutorial continues in the do-file you built in the first tutorial. Open Stata, open `tutorial1.do` in the Do-file Editor, and run it from the top with the Execute (do) button to make sure the dataset loads. Then add a comment line at the bottom so you can find today's work later.

    ```stata
    * Stata Tutorial 2
    ```

    Everything you add today goes below this line. Each time you add commands, rerun the whole do-file rather than the new lines alone, so that the `use` command at the top reloads a clean copy of the data.

    One detail about the variables matters today. Hover over `sex` in the Variables pane and you will see that it is stored as text (a *string* variable) with the values `Male` and `Female`. The variable `education` is stored as the numbers 1 to 4, but each number carries a *value label*, so Stata prints `High school`, `Some college`, `Bachelor's`, or `Graduate degree` in its place. Commands that do arithmetic, such as `summarize` and `correlate`, work on numeric variables like `education`, `age`, and `earnings`, but not on a string variable like `sex`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2 One variable at a time

    Before studying how two variables move together, look at each one on its own. Add these four lines to your do-file and rerun it.

    ```stata
    summarize earnings, detail
    histogram earnings, normal
    tabulate education
    tabulate sex
    ```

    **`summarize` with the `detail` option** reports the percentiles of `earnings` alongside the mean and standard deviation. The 50th percentile is the median, the earnings level that half of the sample falls below, and the 25th and 75th percentiles bracket the middle half of the sample. Compare the median with the mean. When the mean sits well above the median, a small number of high earners are pulling the mean upward, which is the usual shape of earnings data.

    **`histogram`** draws the sample distribution in a separate Graph window. Each bar's height shows how much of the sample falls in that range of earnings, so the histogram is the sample counterpart of the probability density function from Lecture 2. The `normal` option overlays a normal curve with the same mean and standard deviation as the data, which makes it easy to see how far the sample distribution is from a bell shape.

    **`tabulate`** is the right tool for variables that take only a few values. Each table lists the categories, the number of people in each one (`Freq.`), the share of the sample in each one (`Percent`), and the running total of those shares (`Cum.`). The `Percent` column is the sample version of the probability distribution table from Lecture 2, and the `Cum.` column is the sample version of its cumulative row. Note that `tabulate` works on the string variable `sex`, because counting does not require arithmetic.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot1_summarize_detail.png" alt="summarize earnings, detail output" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot2_histogram.png" alt="Histogram of earnings with a normal curve overlaid" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot3_tabulate.png" alt="tabulate output for education and sex" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3 Comparing groups

    The simplest way to see whether two variables are related is to split the sample into groups defined by one variable and compare the average of the other variable across the groups. Lecture 6 calls the population version of this a conditional expectation, $\mathbb{E}[Y \mid X = x]$, the average of $Y$ among observations with a given value of $X$. The `tabstat` command computes the sample version. Add these lines and rerun the do-file.

    ```stata
    tabstat earnings, by(education) statistics(mean sd n)
    tabstat earnings, by(sex) statistics(mean sd n)
    ```

    The `by()` option splits the sample into groups, and the `statistics()` option chooses which numbers to report for each group. The first table has one row per education category showing the mean, the standard deviation, and the number of people in that group, followed by a `Total` row for the whole sample. Average earnings rise from one education category to the next, which is the association that Lecture 5 summarized with a regression line. The second table works even though `sex` is a string variable, because `by()` only needs to sort people into groups. The difference between its two means is the comparison that a regression on a binary variable reports, as described in Section 5.3 of the Lecture 5 notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot4_tabstat.png" alt="tabstat output for earnings by education and by sex" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4 Scatter plots

    Group averages work well when the grouping variable takes only a few values. When both variables take many values, a scatter plot shows the whole relationship at once, with one point per person. Add these lines and rerun the do-file.

    ```stata
    twoway (scatter earnings age) (lfit earnings age)
    twoway (scatter earnings education, jitter(5)) (lfit earnings education)
    ```

    A `twoway` command combines plots, each in its own parentheses. The `scatter` plot draws one point per person, listing the vertical-axis variable first and the horizontal-axis variable second, and the `lfit` plot adds the least-squares line from Lecture 5.

    The first graph is the same picture as the interactive scatter plot in Section 3.2 of the Lecture 3 notebook, so ask the questions from that section. Does the cloud tilt upward or downward? How tightly do the points hug the line? Here the tilt is gently upward and the cloud is wide, so age and earnings are positively but weakly related.

    In the second graph the points would stack into four vertical columns, one per education category, with many points hiding exactly on top of each other. The `jitter()` option nudges each point by a small random amount so the columns spread into clouds, and the number sets how much nudging to apply. Compare the height of each cloud with the group means from `tabstat` in Section 3. They tell the same story in two different ways.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot5_scatter_age.png" alt="Scatter plot of earnings against age with a fitted line" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot6_scatter_education.png" alt="Jittered scatter plot of earnings against education with a fitted line" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5 Covariance and correlation

    Lecture 3 introduced two numbers that summarize a scatter plot. The covariance measures whether two variables move together, and the correlation rescales it to lie between $-1$ and $1$. The `correlate` command computes both for every pair of variables you list. Add these lines and rerun the do-file.

    ```stata
    correlate earnings education age
    correlate earnings education age, covariance
    ```

    The first table lists the variables along both its rows and its columns, and each entry is the sample correlation between the row variable and the column variable. The diagonal is all ones, since every variable is perfectly correlated with itself, and only the entries below the diagonal are printed because the correlation between `earnings` and `education` is the same as the correlation between `education` and `earnings`. Read the entries the way Section 3.3 of the Lecture 3 notebook describes. The correlation between `earnings` and `education` is high, the correlation between `earnings` and `age` is small and positive, and the correlation between `education` and `age` is close to zero, all of which match the plots from Section 4.

    With the `covariance` option, the diagonal holds each variable's sample variance and the off-diagonal entries are the sample covariances. These numbers are harder to read because each carries the units of both of its variables. The covariance between `earnings` and `education` is in dollars times education categories, and the variance of `earnings` is in dollars squared. This is why we usually report correlations, which have no units, and why Lecture 5 divides the covariance by the variance of $X$ to get a slope in the units of $Y$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot7_correlate.png" alt="correlate output with and without the covariance option" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You computed sample covariances by hand in the problem sets, and it is worth checking once that Stata does the same arithmetic,

    $$
    \hat{\sigma}_{XY} = \frac{1}{n-1}\sum_{i=1}^{n}(X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y).
    $$

    Add these lines and rerun the do-file.

    ```stata
    egen meanEarnings = mean(earnings)
    egen meanEducation = mean(education)
    generate product = (earnings - meanEarnings) * (education - meanEducation)
    summarize product
    display r(sum) / (r(N) - 1)
    drop meanEarnings meanEducation product
    ```

    The two `egen` lines create variables holding the sample mean of `earnings` and of `education` in every row, and `generate` builds the product of the two deviations for each person, the numbers you wrote in the last column of your table when you computed a covariance by hand. After `summarize` runs, Stata keeps its results in memory for the next command, with the sum stored as `r(sum)` and the number of observations as `r(N)`, so the `display` line prints the sample covariance. Compare it with the `earnings` and `education` entry in the `correlate, covariance` table. They match. The final `drop` line removes the three helper variables so the dataset stays tidy.

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
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot8_hand_check.png" alt="summarize product and display output reproducing the sample covariance" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
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


if __name__ == "__main__":
    app.run()
