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

    In the first tutorial you built a do-file that loads the course dataset and runs `describe` and `summarize`. This tutorial continues in that same do-file. Open Stata, open `tutorial1.do` in the Do-file Editor, and run it from the top with the Execute (do) button to make sure the dataset loads. Then add a comment line at the bottom so you can find today's work later.

    ```stata
    * Stata Tutorial 2
    ```

    Everything you add today goes below this line. Each time you add a command, rerun the whole do-file rather than the single line. The `use` command at the top reloads the data, so the do-file always starts from the same clean dataset.

    Recall the five variables in the dataset: `id`, `age`, `sex`, `education`, and `earnings`. One detail from the Variables pane matters today. Hover over `sex` and you will see that it is stored as text (Stata calls this a *string* variable), with the values `Male` and `Female`. The variable `education` is stored as the numbers 1 to 4, but each number carries a *value label*, so Stata prints `High school`, `Some college`, `Bachelor's`, or `Graduate degree` in place of the number. Commands that do arithmetic, such as `summarize` and `correlate`, work on numeric variables like `education`, `age`, and `earnings`, but not on string variables like `sex`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2 One variable at a time

    Before studying how two variables move together, look at each one on its own. Lecture 2 described a random variable by its distribution, and the commands below show the sample version of that distribution.

    **`summarize` with the `detail` option** reports much more than the mean and standard deviation. Add this line to your do-file and rerun it.

    ```stata
    summarize earnings, detail
    ```

    The output now includes the percentiles of `earnings`. The 50th percentile is the median, the earnings level that half of the sample falls below, and the 25th and 75th percentiles bracket the middle half of the sample. Compare the median with the mean. When the two are close, the distribution is roughly symmetric. When the mean sits well above the median, a small number of high earners are pulling the mean upward, which is the usual shape of earnings data.
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
    **`histogram`** draws the sample distribution. Add the line below and rerun the do-file. Stata opens the graph in a separate Graph window.

    ```stata
    histogram earnings
    ```

    Each bar's height shows how much of the sample falls in that range of earnings, so the histogram is the sample counterpart of the probability density function from Lecture 2. Notice where the bars pile up and how far the right tail stretches. Those features are exactly what the percentiles in the `summarize, detail` output describe with numbers.

    Adding the `normal` option overlays a normal curve with the same mean and standard deviation as the data, which makes it easy to see how far the sample distribution is from a bell shape.

    ```stata
    histogram earnings, normal
    ```
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
    **`tabulate`** is the right tool for variables that take only a few values. A histogram of `education` would be four bars, so instead ask Stata to count how many people fall into each category. Add these two lines and rerun the do-file.

    ```stata
    tabulate education
    tabulate sex
    ```

    Each table lists the categories, the number of people in each one (`Freq.`), the share of the sample in each one (`Percent`), and the running total of those shares (`Cum.`). The `Percent` column is the sample version of the probability distribution table from Lecture 2, and the `Cum.` column is the sample version of its cumulative row. Note that `tabulate` works on the string variable `sex` without complaint, because counting does not require arithmetic.

    The `education` table prints the value labels rather than the numbers underneath them. To see the numbers instead, add the `nolabel` option.

    ```stata
    tabulate education, nolabel
    ```
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

    The simplest way to see whether two variables are related is to split the sample into groups defined by one variable and compare the average of the other variable across the groups. Lecture 6 calls the population version of this a conditional expectation, $\mathbb{E}[Y \mid X = x]$, the average of $Y$ among observations with a given value of $X$. The `tabstat` command computes the sample version. Add this line and rerun the do-file.

    ```stata
    tabstat earnings, by(education) statistics(mean sd n)
    ```

    The `by(education)` option splits the sample by education level, and the `statistics()` option chooses which numbers to report for each group. The output has one row per education category showing the mean, the standard deviation, and the number of people in that group, followed by a `Total` row for the whole sample. Read down the `Mean` column. Average earnings rise from one education category to the next, which is the association between education and earnings that Lecture 5 summarized with a regression line.

    The same command works with the string variable `sex` as the grouping variable, because `by()` only needs to sort people into groups.

    ```stata
    tabstat earnings, by(sex) statistics(mean sd n)
    ```

    The difference between the two means in this table is the kind of comparison that a regression on a binary variable reports, as described in Section 5.3 of the Lecture 5 notebook.
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
    A bar chart shows the same group means as a picture. Add this line and rerun the do-file.

    ```stata
    graph bar (mean) earnings, over(education)
    ```

    The `(mean)` part tells Stata which statistic each bar should represent, and `over(education)` gives one bar per education category. A chart like this is often the clearest way to present a comparison of group averages in a report.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot5_bar_chart.png" alt="Bar chart of mean earnings by education" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4 Scatter plots

    Group averages work well when the variable that defines the groups takes only a few values. When both variables take many values, a scatter plot shows the whole relationship at once, with one point per person. The `twoway scatter` command draws it, listing the vertical-axis variable first and the horizontal-axis variable second. Add this line and rerun the do-file.

    ```stata
    twoway scatter earnings age
    ```

    Each point is one person, positioned by their age and their earnings. This is the same picture as the interactive scatter plot in Section 3.2 of the Lecture 3 notebook. Ask yourself the questions from that section. Does the cloud tilt upward or downward? How tightly do the points hug a line? In this sample the tilt is gently upward and the cloud is wide, so age and earnings are positively but weakly related.

    To add the line that ordinary least squares would fit through these points, combine two plots inside one `twoway` command, with each plot in its own parentheses. The `lfit` plot draws the least-squares line from Lecture 5.

    ```stata
    twoway (scatter earnings age) (lfit earnings age)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot6_scatter_age.png" alt="Scatter plot of earnings against age with a fitted line" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now try the same plot with `education` on the horizontal axis.

    ```stata
    twoway scatter earnings education
    ```

    The points stack into four vertical columns, one per education category, because `education` only takes the values 1 to 4. Many points sit exactly on top of each other, so the plot hides how many people are in each column. The `jitter()` option nudges each point by a small random amount so that overlapping points spread out. The number sets how much nudging to apply.

    ```stata
    twoway (scatter earnings education, jitter(5)) (lfit earnings education)
    ```

    The columns now read as four clouds, and the fitted line passes close to the middle of each one. Compare the height of each cloud with the group means you computed with `tabstat` in Section 3. They tell the same story in two different ways.

    Graphs appear in the Graph window, and each new graph replaces the previous one. To keep a graph, save it as a picture file right after the command that draws it, reusing the `dataFolder` local from the top of your do-file.

    ```stata
    graph export "`dataFolder'/scatter_education.png", replace
    ```

    The `replace` option lets Stata overwrite the file the next time you run the do-file.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot7_scatter_education.png" alt="Jittered scatter plot of earnings against education with a fitted line" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5 Covariance and correlation

    A scatter plot shows a relationship, and Lecture 3 introduced two numbers that summarize it. The covariance measures whether two variables move together, and the correlation rescales the covariance to lie between $-1$ and $1$. The `correlate` command computes the sample correlation for every pair of variables you list. Add this line and rerun the do-file.

    ```stata
    correlate earnings education age
    ```

    The output is a table with the listed variables along both the rows and the columns. Each entry is the sample correlation between the row variable and the column variable, so the diagonal is all ones, since every variable is perfectly correlated with itself. Only the entries below the diagonal are printed, because the correlation between `earnings` and `education` is the same as the correlation between `education` and `earnings`. Read the entries the way Section 3.3 of the Lecture 3 notebook describes. A value near $1$ means a tight, upward-sloping cloud, a value near $0$ means little linear relationship, and a negative value means the cloud tilts downward. The correlation between `earnings` and `education` is high, the correlation between `earnings` and `age` is small and positive, and the correlation between `education` and `age` is close to zero, all of which match the plots you drew in Section 4.

    Adding the `covariance` option reports the sample covariances instead.

    ```stata
    correlate earnings education age, covariance
    ```

    Now the diagonal holds each variable's sample variance, and the off-diagonal entries are the sample covariances. The numbers are much harder to read than the correlations, because each one carries the units of both of its variables. The covariance between `earnings` and `education` is in dollars times education categories, and the variance of `earnings` is in dollars squared. This is why we usually report correlations, which have no units, and why Lecture 5 divides the covariance by the variance of $X$ to get a slope in the units of $Y$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot8_correlate.png" alt="correlate output with and without the covariance option" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You computed sample covariances by hand in the problem sets, and it is worth checking once that Stata does exactly the same arithmetic. The formula from Section 2.3 of the Lecture 2 notebook, applied to two variables as in Lecture 3, is

    $$
    \hat{\sigma}_{XY} = \frac{1}{n-1}\sum_{i=1}^{n}(X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y).
    $$

    The lines below build it one step at a time. Add them to your do-file and rerun it.

    ```stata
    egen meanEarnings = mean(earnings)
    egen meanEducation = mean(education)
    generate product = (earnings - meanEarnings) * (education - meanEducation)
    summarize product
    display r(sum) / (r(N) - 1)
    ```

    The `egen` command with the `mean()` function creates a new variable that holds the sample mean of `earnings` in every row, and the second line does the same for `education`. The `generate` command then creates the product of the two deviations for each person. These are the numbers you wrote in the third column of your table when you computed a covariance by hand.

    The last two lines add up the products and divide by $n - 1$. After `summarize` runs, Stata keeps its results in memory for the next command to use. The sum of the summarized variable is stored as `r(sum)` and the number of observations as `r(N)`, so the `display` line prints the sample covariance. Compare it with the `earnings` and `education` entry in the `correlate, covariance` table. They match.

    The three new variables now sit in the Variables pane. They served their purpose, so remove them with `drop` to keep the dataset tidy.

    ```stata
    drop meanEarnings meanEducation product
    ```

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
    graph bar (mean) earnings, over(education)

    twoway (scatter earnings age) (lfit earnings age)
    twoway (scatter earnings education, jitter(5)) (lfit earnings education)
    graph export "`dataFolder'/scatter_education.png", replace

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
    <img src="https://robert-french.github.io/Econometrics/stata2tutorial/stata2_shot9_hand_check.png" alt="summarize product and display output reproducing the sample covariance" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** string variable, value label, percentile, median, "
            "`summarize, detail`, `histogram`, `tabulate`, `tabstat`, "
            "`graph bar`, `twoway scatter`, `lfit`, `jitter()`, `graph export`, "
            "`correlate`, `egen`, `generate`, `drop`, stored results `r()`.\n\n"
            "**Habits:** look at each variable on its own before relating two "
            "of them; use group means for variables with a few categories and "
            "scatter plots for variables with many values; report correlations "
            "rather than covariances because they have no units; check once by "
            "hand that the software computes the formula from lecture."
        ),
        title="Key terms and habits",
        kind="info",
    )
    return


if __name__ == "__main__":
    app.run()
