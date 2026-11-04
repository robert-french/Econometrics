# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(
    app_title="Stata Tutorial 3: Simple Regression",
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
                2. <a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata2DescribingRelationships.html" target="_self">Describing Data and Relationships</a>
                3. **[Simple Regression](#top)**
                    1. [Picking up where we left off](#sec1)
                    1. [Your first regression](#sec2)
                    1. [Fitted values and residuals](#sec3)
                    1. [A binary independent variable](#sec4)
                    1. [Standard errors, t-statistics, and confidence intervals](#sec5)
                    1. [Robust standard errors](#sec6)
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata2DescribingRelationships.html" target="_self">← Stata Tutorial 2</a>'),
            mo.md('<span class="nav-soon">Stata Tutorial 4 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Stata Tutorial 3: Simple Regression
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contents

    3.1 [Picking up where we left off](#sec1)<br>
    3.2 [Your first regression](#sec2)<br>
    3.3 [Fitted values and residuals](#sec3)<br>
    3.4 [A binary independent variable](#sec4)<br>
    3.5 [Standard errors, t-statistics, and confidence intervals](#sec5)<br>
    3.6 [Robust standard errors](#sec6)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 3.1 Picking up where we left off

    In the second tutorial you drew least-squares lines through scatter plots with `lfit`. This tutorial estimates those lines with the `regress` command, which prints the intercept and slope from Lecture 5 together with the standard errors, t-statistics, p-values, and confidence intervals from Lecture 7.

    Open Stata, open `tutorial1.do` in the Do-file Editor, and run it from the top with the Execute (do) button so that the dataset loads. Then add a comment line at the bottom to mark today's work.

    ```stata
    * Stata Tutorial 3
    ```

    Everything you add today goes below this line. As before, rerun the whole do-file each time you add commands, so that the `use` command at the top reloads a clean copy of the data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 3.2 Your first regression

    The `regress` command estimates a regression by ordinary least squares. You list the dependent variable first and the independent variable second, in the same order as `scatter`. Add this line to your do-file and rerun it.

    ```stata
    regress earnings education
    ```

    The most important part of the output is the **coefficient table** at the bottom. Each row is one coefficient. The `education` row reports the slope $\hat{\beta}_1$, and the `_cons` row reports the intercept $\hat{\beta}_0$, which Stata calls the constant. The `Coefficient` column holds the OLS estimates from Lecture 5, so the fitted line is

    $$
    \widehat{\text{earnings}} = 37{,}903 + 11{,}281 \times \text{education}.
    $$

    Recall from Tutorial 2 that `education` takes the values 1 through 4 for the four education categories. The slope therefore says that moving up one education category is associated with annual earnings that are about \$11,281 higher on average. The intercept is the predicted earnings for a person with `education` equal to 0. No such category exists, so the intercept only positions the line and should not be interpreted on its own. The remaining columns of the coefficient table report the standard error of each estimate and the inference built on it. Section 3.5 returns to them.

    Two numbers in the block at the **top right** are also worth reading. `R-squared` is the $R^2$ from Section 5.5 of the Lecture 5 notebook, and here it says that education accounts for about 68 percent of the variation in earnings in this sample. `Root MSE` is Stata's name for the standard error of the regression, the typical size of a residual, which is about \$8,932 here. The block at the top left reports the sums of squares behind the $R^2$, and you will rarely need it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata3tutorial/stata3_shot1_regress_education.png" alt="regress earnings education output" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3.3 Fitted values and residuals

    After `regress` runs, Stata keeps the estimates in memory. The `predict` command uses them to compute a fitted value or a residual for every person in the dataset. Add these lines and rerun the do-file.

    ```stata
    predict earningsHat
    predict residual, residuals
    summarize earningsHat residual
    ```

    The first `predict` line creates a new variable, `earningsHat`, holding each person's fitted value $\hat{Y}_i = \hat{\beta}_0 + \hat{\beta}_1 X_i$. Stata notes that it assumed the `xb` option, which is its name for the fitted value. The second line, with the `residuals` option, creates a variable holding each person's OLS residual $\hat{u}_i = Y_i - \hat{Y}_i$. In the `summarize` output, the mean of `earningsHat` equals the mean of `earnings`, because the fitted line passes through the point of sample means, and the mean of `residual` is zero up to rounding, because OLS residuals always average to zero.<sup><a id="fnref1" href="#fn1">1</a></sup>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata3tutorial/stata3_shot3_predict.png" alt="predict and summarize output for the fitted values and residuals" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now plot both. The first graph redraws the scatter plot from Tutorial 2 with the fitted values drawn as a line, which reproduces what `lfit` did automatically. The second plots the residuals against `education`, with a horizontal line at zero. Add these lines, rerun the do-file, and then remove the two new variables so the dataset stays tidy.

    ```stata
    twoway (scatter earnings education, jitter(5)) (line earningsHat education, sort)
    twoway (scatter residual education, jitter(5)), yline(0)
    drop earningsHat residual
    ```

    The `sort` option on the `line` plot tells Stata to connect the fitted values in order of `education`, so that the line runs from left to right instead of zigzagging through the points in the order they appear in the dataset. In the residual plot, the points scatter above and below zero in every education category. Look at whether the vertical spread of the residuals is similar across categories or changes with education. Section 7.3 of the Lecture 7 notebook explains that a spread that changes with $X$ is heteroskedasticity, and Section 3.6 shows what to do about it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata3tutorial/stata3_shot4_fitted_line.png" alt="Scatter plot of earnings against education with the fitted values drawn as a line" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata3tutorial/stata3_shot5_residuals.png" alt="Scatter plot of OLS residuals against education with a line at zero" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 3.4 A binary independent variable

    Section 5.3 of the Lecture 5 notebook shows that when $X$ takes only the values 0 and 1, the intercept is the average of $Y$ in the group with $X = 0$ and the slope is the difference in average $Y$ between the two groups. Let's confirm this using `sex`.

    Tutorial 2 noted that `sex` is a string variable, so `regress` cannot use it directly. The first step is to build a numeric indicator from it. Add these lines and rerun the do-file.

    ```stata
    generate female = (sex == "Female")
    tabulate sex female
    regress earnings female
    tabstat earnings, by(sex) statistics(mean n)
    ```

    The expression in parentheses after `generate` is a comparison. For each person it is true or false, and Stata stores true as 1 and false as 0, so `female` equals 1 for women and 0 for men. The double equals sign tests whether two things are equal, which is different from the single equals sign that assigns a value. The `tabulate` line cross-tabulates the string variable against the new indicator. Every woman should be in the `1` column and every man in the `0` column. Build this check into your habits, because a typo inside the quotation marks would silently produce an indicator that is 0 for everyone.

    Now compare the regression with the `tabstat` table. The intercept `_cons` equals the mean earnings of men, the group with `female` equal to 0, and the coefficient on `female` equals the mean earnings of women minus the mean earnings of men. In this sample, women earn about \$4,143 less per year than men on average. A regression on a single binary variable is a comparison of two group means, written in the language of slopes and intercepts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata3tutorial/stata3_shot6_regress_female.png" alt="regress earnings female output next to the tabstat table of group means" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 3.5 Standard errors, t-statistics, and confidence intervals

    Return to the coefficient table and read the columns to the right of `Coefficient`. They apply the tools from Sections 7.4 and 7.5 of the Lecture 7 notebook to each coefficient.

    **`Std. err.`** is the standard error of the estimate. In the `female` regression, the slope is $-4{,}143$ with a standard error of about $2{,}216$.

    **`t`** is the t-statistic for the null hypothesis that the coefficient is zero. It is the coefficient divided by its standard error, so for `female` it is $-4{,}143 / 2{,}216 \approx -1.87$. Stata always tests the null of zero. To test a different null value, compute the t-statistic yourself from the coefficient and its standard error.

    **`P>|t|`** is the two-sided p-value for that test. For `female` it is $0.063$, so we cannot reject the null that men and women have the same mean earnings at the 5 percent significance level, although we can at the 10 percent level. In the `education` regression, the p-value is printed as $0.000$, which means it is below $0.0005$, not that it is exactly zero.<sup><a id="fnref2" href="#fn2">2</a></sup>

    **`[95% conf. interval]`** reports the confidence interval from Section 7.5, the estimate plus or minus about two standard errors. For `female` it runs from about $-8{,}514$ to $227$. The interval contains zero, which is the same conclusion as the p-value above 0.05: the data do not rule out equal mean earnings at the 5 percent level.

    To see a case between these two, add this line and rerun the do-file.

    ```stata
    regress earnings age
    ```

    The slope on `age` is about \$270 per year of age with a standard error of about \$113. The t-statistic is $2.38$ and the p-value is $0.018$, so we reject the null of no association at the 5 percent level but not at the 1 percent level. Check that the 95 percent confidence interval excludes zero, as it must when the p-value is below 0.05. Note also the $R^2$ of $0.03$. Age is statistically significant in this sample, but it accounts for only a small share of the variation in earnings. Statistical significance and the strength of a relationship are different things.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata3tutorial/stata3_shot7_regress_age.png" alt="regress earnings age output" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec6"></a>
    ## 3.6 Robust standard errors

    The standard errors printed so far assume homoskedasticity, meaning that the error term has the same spread at every value of $X$. Section 7.3 of the Lecture 7 notebook explains that when the spread changes with $X$, those standard errors can be too small or too large, and that the heteroskedasticity-robust standard error fixes this. In Stata, the `vce(robust)` option asks for the robust version. Add these lines and rerun the do-file.

    ```stata
    regress earnings education, vce(robust)
    regress earnings age, vce(robust)
    ```

    Compare each table with its counterpart from earlier in the tutorial. The coefficients, the $R^2$, and the `Root MSE` are identical, because the option changes only how the standard errors are computed and not the line that OLS fits. The column is now labelled `Robust std. err.`, and the standard error on `education` rises from about $550$ to $565$, while the standard error on `age` rises from about $113$ to $120$. The t-statistics, p-values, and confidence intervals change along with them. The block of sums of squares at the top left is gone, since it is tied to the homoskedastic formulas.

    The robust standard error is valid whether or not the error is homoskedastic, while the default is valid only when it is. For the rest of this course, add `vce(robust)` to every regression you run. You will often find, as here, that the two versions are close, but you cannot know that until you have compared them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata3tutorial/stata3_shot8_robust.png" alt="regress output with the vce(robust) option" style="display:block;margin:0.5rem auto 1rem;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Your do-file should now look something like this, with the Tutorial 1 and 2 lines at the top and today's lines below them.

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

    * Stata Tutorial 3

    regress earnings education
    predict earningsHat
    predict residual, residuals
    summarize earningsHat residual
    twoway (scatter earnings education, jitter(5)) (line earningsHat education, sort)
    twoway (scatter residual education, jitter(5)), yline(0)
    drop earningsHat residual

    generate female = (sex == "Female")
    tabulate sex female
    regress earnings female
    tabstat earnings, by(sex) statistics(mean n)

    regress earnings age

    regress earnings education, vce(robust)
    regress earnings age, vce(robust)
    ```

    Save your do-file. The next tutorial adds more independent variables to these regressions and shows how to collect several regressions into a single table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** `regress`, `_cons`, `Root MSE`, `predict`, fitted value, "
            "residual, indicator variable, `==`, `Std. err.`, `t`, `P>|t|`, "
            "confidence interval, `vce(robust)`.\n\n"
            "**Habits:** list the dependent variable first; read the coefficient "
            "table before the blocks above it; cross-tabulate a new indicator "
            "against the variable it came from; plot the residuals; report "
            "heteroskedasticity-robust standard errors."
        ),
        title="Key terms and habits",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** The mean of `residual` prints as a number like `-6.62e-06`, which is scientific notation for $-0.00000662$. It is not exactly zero only because the computer rounds at the last decimal place. <a href="#fnref1" title="Back to text">&#8617;</a></span>

    <span id="fn2" style="display:block;font-size:0.9rem;">**2.** Lecture 7 computes p-values and confidence intervals from the standard normal distribution, which is the sampling distribution of the t-statistic in large samples. Stata instead uses the Student t distribution with $n - 2$ degrees of freedom, which is slightly wider in small samples. With 200 observations the two agree closely: the critical value for a 95 percent interval is $1.97$ rather than $1.96$. <a href="#fnref2" title="Back to text">&#8617;</a></span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _appendix = mo.md(r"""
    This appendix is optional. It rebuilds the numbers that `regress` prints from the formulas in the Lecture 5 notebook, in the same way that Tutorial 2 rebuilt the sample covariance. Nothing here is needed for the problem sets, but working through it shows that `regress` does nothing mysterious.

    **The slope and intercept.** Section 5.2 of the Lecture 5 notebook gives the OLS estimates in closed form. The slope is the sample covariance of $X$ and $Y$ divided by the sample variance of $X$, and the intercept makes the line pass through the point of sample means,

    $$
    \hat{\beta}_1 = \frac{\widehat{\text{cov}}(X, Y)}{\widehat{\text{var}}(X)}, \qquad \hat{\beta}_0 = \hat{\mu}_Y - \hat{\beta}_1 \hat{\mu}_X.
    $$

    In Tutorial 2 you saw that `summarize` leaves its results in memory, with the sum of a variable stored as `r(sum)` and the number of observations as `r(N)`. It also stores the mean as `r(mean)` and the sample variance as `r(Var)`. The lines below capture those results in locals before the next `summarize` overwrites them, then print the two formulas.

    ```stata
    summarize education
    local meanEducation = r(mean)
    local varEducation = r(Var)
    summarize earnings
    local meanEarnings = r(mean)
    generate product = (earnings - `meanEarnings') * (education - `meanEducation')
    summarize product
    local covariance = r(sum) / (r(N) - 1)
    display `covariance' / `varEducation'
    display `meanEarnings' - (`covariance' / `varEducation') * `meanEducation'
    drop product
    ```

    These `local` lines look slightly different from the one in Tutorial 1. There, `local dataFolder "..."` stored a piece of text. Here, the equals sign tells Stata to evaluate the expression on the right and store the resulting number. Both `display` lines should match the `Coefficient` column from Section 3.2 to the last printed digit.

    **Stored coefficients.** Instead of retyping numbers from the output, you can refer to the estimates directly. After `regress`, the slope is stored as `_b[education]` and the intercept as `_b[_cons]`. The last line below is the prediction from Section 5.4 of the Lecture 5 notebook for the bachelor's degree category, `education` equal to 3.

    ```stata
    regress earnings education
    display _b[education]
    display _b[_cons]
    display _b[_cons] + _b[education] * 3
    ```

    **The standard error of the regression.** Section 5.5 of the Lecture 5 notebook defines it as the square root of the sum of squared residuals divided by $n - 2$. The lines below rebuild it from the residuals created in Section 3.3, so run them before the `drop` line in that section. The number printed should match `Root MSE`.

    ```stata
    generate residualSq = residual^2
    summarize residualSq
    display sqrt(r(sum) / (r(N) - 2))
    drop residualSq
    ```
    """)
    mo.accordion({"## Appendix: checking the formulas by hand (optional)": _appendix})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata2DescribingRelationships.html" target="_self">← Stata Tutorial 2</a>'),
            mo.md('<span class="nav-soon">Stata Tutorial 4 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
