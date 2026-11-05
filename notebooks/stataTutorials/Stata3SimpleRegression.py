# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.25.2"
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

    In the second tutorial you drew least-squares lines through scatter plots with `lfit`. This tutorial estimates those lines with the `regress` command, which records the intercept and slope from Lecture 5 together with the standard errors, t-statistics, p-values, and confidence intervals from Lecture 7.

    Open Stata, open `tutorial1.do` in the Do-file Editor, and run it from the top with the Execute (do) button so that the dataset loads. Then add a comment line at the bottom to mark the start of this tutorial's code.

    ```stata
    * Stata Tutorial 3
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 3.2 Your first regression

    The `regress` command estimates a regression by ordinary least squares. You list the dependent variable first and the independent variable second. Add this line to your do-file and rerun it.

    ```stata
    regress earnings education
    ```

    Running this line of code will produce a *coefficient table*. Each row in the table reports one coefficient estimate and its corresponding measures of uncertainty. The `education` row reports the slope estimate $\hat{\beta}_1$, and the `_cons` row reports the intercept estimate $\hat{\beta}_0$, which Stata calls the constant. The coefficient table represents the following fitted line

    $$
    \widehat{\text{earnings}} = 37{,}903 + 11{,}281 \times \text{education}.
    $$

    Recall from the second Stata tutorial that `education` takes the values 1 through 4 for the four education categories. The slope estimate therefore says that moving up one education category is associated with annual earnings that are about \$11,281 higher on average. The intercept is the predicted earnings for a person with `education` equal to 0. Note that no such category exists, so the intercept only positions the line and is therefore not economically informative on its own. The same rows also report each coefficient's standard error, t-statistic, p-value, and 95% confidence interval.

    The `R-squared` in the top-right block is the $R^2$ from the regression. It says that education accounts for about 68 percent of the variation in earnings in this sample. `Root MSE` is Stata's name for the standard error of the regression, the typical size of a residual, which is about \$8,932 in this sample. The block at the top left reports the sums of squares behind the $R^2$; `Model` records the ESS, `Residual` records the SSR, and `Total` records the TSS.
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

    After `regress` runs, Stata keeps the estimates from the regression in its recent memory. The `predict` command uses them to compute a fitted value or a residual for every observation in the dataset. Add these lines to your do-file and rerun it.

    ```stata
    predict earningsHat
    predict residual, residuals
    summarize earningsHat residual
    ```

    The first `predict` line creates a new variable called `earningsHat`, which holds each person's fitted value $\hat{Y}_i = \hat{\beta}_0 + \hat{\beta}_1 X_i$. Stata notes that it assumed the `xb` option, which is the option for recording the fitted value. The second line, with the `residuals` option, creates a variable holding each person's OLS residual $\hat{u}_i = Y_i - \hat{Y}_i$. In the `summarize` output, the mean of `earningsHat` equals the mean of `earnings`. The mean of `residual` is zero up to rounding, because OLS residuals always average to zero.<sup><a id="fnref1" href="#fn1">1</a></sup>
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
    Let's now plot both of these predicted values. To do so, add the following lines to your do-file and rerun it.

    ```stata
    twoway (scatter earnings education, jitter(5)) (line earningsHat education, sort)
    twoway (scatter residual education, jitter(5)), yline(0)
    drop earningsHat residual
    ```

    The first graph redraws the scatter plot from Tutorial 2 with the fitted values drawn as a line, which reproduces what `lfit` did automatically. The second graph plots the residuals against the `education` variable, with a horizontal line at zero. The `sort` option on the `line` plot tells Stata to connect the fitted values in order of `education`, so that the line runs from left to right instead of zigzagging through the points in the order they appear in the dataset. In the residual plot, the points scatter above and below zero in every education category as expected. The `jitter` option in both plots adds a small amount of horizontal noise to the data so we can see each data point in the plots.
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

    Section 5.3 of the Lecture 5 notebook shows that when $X$ is binary, the intercept is the mean of $Y$ for the group with $X=0$, and the slope is the difference in means between the two groups. Let's verify this using the `sex` variable.

    As noted in Tutorial 2, `sex` is a string variable, so we first need to create a numeric indicator variable. Add the following lines to your do-file and rerun it.

    ```stata
    generate female = (sex == "Female")
    tabulate sex female
    regress earnings female
    tabstat earnings, by(sex) statistics(mean n)
    ```

    The first line creates the variable `female`, which equals 1 for women and 0 for men. In Stata, `==` tests whether variables are equal to a value, while `=` assigns a value to that variable. The tabulate command lets us check that the indicator was constructed correctly.

    Now compare the regression results with the tabstat table. Recall that our regression is $\widehat{earnings}=\hat{\beta}_0+\hat{\beta}_1 female$. For men, `female` equals 0, so predicted earnings are simply $\hat{\beta}_0$, the intercept (`_cons`). For women, `female` equals 1, so predicted earnings are $\hat{\beta}_0+\hat{\beta}_1$. The coefficient on `female` therefore measures the difference in predicted earnings between women and men. In a regression with a single binary explanatory variable, these predictions equal the respective group means. You can confirm this in the `tabstat` table: the intercept equals mean earnings for men, and the coefficient on female equals mean earnings for women minus mean earnings for men. In this sample, women earn about \$4,143 less per year on average.
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

    Examine again the coefficient table from our last regression and consider the columns to the right of `Coefficient`.

    - `Std. err.` reports the standard error of each coefficient estimate. In our regression of earnings on `female`, the estimated coefficient is -$4,143, with a standard error of approximately $2,216.

    - `t` reports the t-statistic for testing whether the coefficient equals zero. Recall that we calculate this by dividing the coefficient by its standard error. For `female`, this gives \(-4143/2216 \approx -1.87\). Stata tests the null hypothesis that the coefficient equals zero by default.

    - `P>|t|` reports the two-sided p-value associated with the t-statistic. For `female`, the p-value is 0.063. We therefore cannot reject the null hypothesis that men and women have equal mean earnings at the 5% significance level, although we can reject it at the 10% level. Note that Stata sometimes reports p-values as `0.000`, as in our earlier regression of earnings on education. This simply means the p-value is very small, not that it is exactly zero.

    - `[95% conf. interval]` reports the 95% confidence interval, calculated as the coefficient estimate plus or minus approximately two standard errors. For `female`, the interval runs from about -$8,514 to $227. Since the interval includes zero, we cannot reject the null hypothesis at the 5% significance level, consistent with our interpretation of the p-value.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec6"></a>
    ## 3.6 Robust standard errors

    The standard errors reported so far assume *homoskedasticity*, meaning that the variance of the error term is constant across values of $X$. As discussed in Section 7.3 of the Lecture 7 notebook, when this assumption fails, our standard errors may be too large or too small. We can account for this using *heteroskedasticity-robust standard errors*. In Stata, we do this by adding the option `vce(robust)` to our regression command. Add the following line to your do-file and rerun it.

    ```stata
    regress earnings education, vce(robust)
    ```

    Compare the results with our earlier regression of earnings on education. Notice that the coefficient estimates, $R^2$, and `Root MSE` are unchanged. This is because `vce(robust)` changes how the standard errors are calculated, but not the OLS estimates themselves. The standard error on `education` increases slightly, from about $550 to $565. The t-statistic, p-value, and confidence interval also change accordingly.

    Robust standard errors are valid whether or not the errors are homoskedastic, whereas conventional standard errors require homoskedasticity. You should therefore always include `vce(robust)` in each regression you run.
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _appendix = mo.md(r"""
    This appendix is optional. Let's check that we can reproduce the numbers in the `regress` output using the formulas from Lecture 5.

    Recall from Section 5.2 of the Lecture 5 notebook that the OLS estimates are

    $$
    \hat{\beta}_1 = \frac{\widehat{\text{cov}}(X, Y)}{\widehat{\text{var}}(X)} = \frac{\sum_{i=1}^{n}(X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y)}{\sum_{i=1}^{n}(X_i - \hat{\mu}_X)^2}, \qquad \hat{\beta}_0 = \hat{\mu}_Y - \hat{\beta}_1 \hat{\mu}_X.
    $$

    Add the following lines to your do-file and rerun it.

    ```stata
    egen meanEarnings = mean(earnings)
    egen meanEducation = mean(education)
    egen numerator = total((education - meanEducation) * (earnings - meanEarnings))
    egen denominator = total((education - meanEducation)^2)
    display numerator / denominator
    display meanEarnings - (numerator / denominator) * meanEducation
    drop meanEarnings meanEducation numerator denominator
    ```

    The first two lines compute the sample means, as in Tutorial 2. The `total` function adds up an expression across all observations in the sample, so the next two lines compute the two sums in the slope formula. The two `display` lines then print the slope and the intercept. Compare them with the `Coefficient` column in Section 3.2 and see whether they match.

    We can check the standard error of the regression in the same way. Recall from Section 5.5 of the Lecture 5 notebook that

    $$
    \text{SER} = \sqrt{\frac{\text{SSR}}{n - 2}}.
    $$

    Our sample has 200 observations, so $n - 2 = 198$. Add the following lines to your do-file and rerun it.

    ```stata
    regress earnings education
    predict residual, residuals
    egen ssr = total(residual^2)
    display sqrt(ssr / 198)
    drop residual ssr
    ```

    The number printed should match the `Root MSE` in the regression output.
    """)
    mo.accordion({"## Appendix": _appendix})
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
