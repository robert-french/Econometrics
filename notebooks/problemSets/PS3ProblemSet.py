# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.23.16"
__preliminary__ = False
__description__ = "Problem Set 3 with worked solutions beneath each question."
app = marimo.App(
    app_title="Problem Set 3: Simple Linear Regression",
    css_file="../marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    def qa(question, solution, indent=False):
        # Native <details> instead of mo.accordion: the shared name attribute
        # makes the browser close every other solution when one is opened.
        # Styling (bold header, chevron, blue body) lives in marimo-overrides.css
        # under details.ps-solution.
        panel = mo.Html(
            '<details class="ps-solution" name="ps-solution">'
            "<summary>Solution</summary>"
            f'<div class="ps-solution-body">{mo.md(solution).text}</div>'
            "</details>"
        )
        block = mo.vstack([mo.md(question), panel], gap=0.5)
        if indent:
            return block.style({"margin-left": "1.75em"})
        return block

    return (qa,)


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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Problem Set 3</a></h1>'
                '</div>'
            ),
            mo.md(
                r"""
                **Simple Linear Regression**

                - [Problem 0. Prepare before attempting the problems](#prob0)
                - [Problem 1. From sample statistics to a regression line](#prob1)
                - [Problem 2. Fitted values, residuals, and prediction](#prob2)
                - [Problem 3. Measuring fit](#prob3)
                - [Problem 4. A binary independent variable](#prob4)
                - [Problem 5. Prepare for the Tuesday quiz](#prob5)
                """
            ),
        ],
        width="300px",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self">← Course home</a>')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Problem Set 3: Simple Linear Regression

    Due at the beginning of class on Tuesday, September 29.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob0"></a>
    ## Problem 0. Prepare before attempting the problems

    Before attempting the problems below, spend around 3 hours reviewing the Lecture 5 notebook on the course website, together with your class notes. Work through the interactive figures as you read, and keep a list of anything you find difficult. Discuss the items on that list with your classmates, bring them to the peer mentors, or come to office hours. The problems below will go much more smoothly after this review.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob1"></a>
    ## Problem 1. From sample statistics to a regression line

    A researcher wants to study how hourly wages relate to years of education, as in the example running through the Lecture 5 notebook. She starts with a tiny sample of five workers.

    | Worker | Years of education ($X$) | Hourly wage in dollars ($Y$) |
    |:---:|:---:|:---:|
    | 1 | 10 | 12 |
    | 2 | 12 | 17 |
    | 3 | 14 | 15 |
    | 4 | 16 | 20 |
    | 5 | 18 | 26 |
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Write down the population regression model for this setting, as in Section 5.1 of the Lecture 5 notebook. Which variable is the dependent variable, which is the independent variable, and what does the error term $u_i$ represent here?
        """,
        r"""
        The population regression model is

        $$
        Y_i = \beta_0 + \beta_1 X_i + u_i, \qquad i = 1, \ldots, n,
        $$

        where $Y_i$ is worker $i$'s hourly wage and $X_i$ is worker $i$'s years of education. The hourly wage is the dependent variable, the outcome we want to explain, and years of education is the independent variable, the variable we use to explain it. The error term $u_i$ collects all the other factors besides education that affect worker $i$'s wage, such as experience, occupation, or luck.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Compute the sample means $\hat{\mu}_X$ and $\hat{\mu}_Y$.
        """,
        r"""
        $$
        \hat{\mu}_X = \frac{10 + 12 + 14 + 16 + 18}{5} = 14, \qquad
        \hat{\mu}_Y = \frac{12 + 17 + 15 + 20 + 26}{5} = 18.
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Compute the sample variance of $X$ and the sample covariance of $X$ and $Y$.
        """,
        r"""
        The deviations from the sample means are $X_i - \hat{\mu}_X = -4, -2, 0, 2, 4$ and $Y_i - \hat{\mu}_Y = -6, -1, -3, 2, 8$. The sample variance of $X$ is

        $$
        \hat{\sigma}_X^2 = \frac{1}{n-1}\sum_{i=1}^{n}(X_i - \hat{\mu}_X)^2 = \frac{16 + 4 + 0 + 4 + 16}{4} = \frac{40}{4} = 10.
        $$

        The sample covariance is

        $$
        \hat{\sigma}_{XY} = \frac{1}{n-1}\sum_{i=1}^{n}(X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y) = \frac{24 + 2 + 0 + 4 + 32}{4} = \frac{62}{4} = 15.5.
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Use the formulas in Section 5.2 of the Lecture 5 notebook to compute the OLS estimates $\hat{\beta}_1$ and $\hat{\beta}_0$, and write down the fitted regression line.
        """,
        r"""
        The slope estimate is the sample covariance divided by the sample variance of $X$,

        $$
        \hat{\beta}_1 = \frac{\widehat{\text{cov}}(X, Y)}{\widehat{\text{var}}(X)} = \frac{15.5}{10} = 1.55,
        $$

        and the intercept estimate makes the fitted line pass through the point of sample averages,

        $$
        \hat{\beta}_0 = \hat{\mu}_Y - \hat{\beta}_1 \hat{\mu}_X = 18 - 1.55 \times 14 = -3.7.
        $$

        The fitted regression line is $\hat{Y} = -3.7 + 1.55\,X$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** Are the two numbers you just computed parameters, estimators, or estimates? How do they relate to $\beta_0$ and $\beta_1$ from part 1?
        """,
        r"""
        They are estimates, the realized numbers that the OLS estimator produced from this particular sample of five workers. The OLS formulas themselves are estimators, rules that turn any sample into a guess. The parameters $\beta_0$ and $\beta_1$ are fixed, unobserved features of the population. With a different sample of five workers, the same estimator would produce different estimates of the same parameters.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **6.** Compute the sample correlation between $X$ and $Y$. Must the sample correlation always have the same sign as $\hat{\beta}_1$? Explain briefly.
        """,
        r"""
        The sample variance of $Y$ is

        $$
        \hat{\sigma}_Y^2 = \frac{36 + 1 + 9 + 4 + 64}{4} = \frac{114}{4} = 28.5,
        $$

        so the sample correlation is

        $$
        \widehat{\text{corr}}(X, Y) = \frac{\hat{\sigma}_{XY}}{\hat{\sigma}_X \hat{\sigma}_Y} = \frac{15.5}{\sqrt{10}\sqrt{28.5}} \approx \frac{15.5}{16.88} \approx 0.92.
        $$

        Yes, the signs must always agree. The correlation and the slope estimate share the same numerator, the sample covariance, and each is divided by a quantity that cannot be negative. When the covariance is positive both are positive, and when it is negative both are negative.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **7.** To see the least squares idea behind the formulas you used, open Section 5.2 of the Lecture 5 notebook and try the interactive plot. Move the intercept and slope sliders to make the sum of squared residuals beneath the plot as small as you can, then tick "Show the least-squares line" to compare your line with the line OLS chooses. Nothing to hand in for this part.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob2"></a>
    ## Problem 2. Fitted values, residuals, and prediction

    This problem continues with the five workers and the fitted line $\hat{Y} = -3.7 + 1.55\,X$ from Problem 1.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Interpret $\hat{\beta}_1 = 1.55$ and $\hat{\beta}_0 = -3.7$ in words, as in Section 5.3 of the Lecture 5 notebook. Be careful to state the units of each number. Does the intercept describe any worker we could actually observe?
        """,
        r"""
        The slope says that each additional year of education is associated with an hourly wage that is about &#36;1.55 higher on average. Its units are the units of $Y$, dollars per hour. The intercept is the predicted hourly wage for a worker with zero years of education, $-$&#36;3.70 per hour. A negative wage is impossible, which is a reminder that the intercept is an extrapolation. Zero years of education lies far outside the observed range of 10 to 18 years, so the intercept anchors the line rather than describing any worker we could actually observe.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Compute the fitted value $\hat{Y}_i$ and the OLS residual $\hat{u}_i$ for each of the five workers, and record them in a table. In one sentence each, explain what a fitted value and a residual describe. Then, in one more sentence, explain how the residual $\hat{u}_i$ differs from the error term $u_i$ in the population model.
        """,
        r"""
        Using $\hat{Y}_i = -3.7 + 1.55\,X_i$ and $\hat{u}_i = Y_i - \hat{Y}_i$,

        | Worker | $X_i$ | $Y_i$ | $\hat{Y}_i$ | $\hat{u}_i$ |
        |:---:|:---:|:---:|:---:|:---:|
        | 1 | 10 | 12 | 11.8 | 0.2 |
        | 2 | 12 | 17 | 14.9 | 2.1 |
        | 3 | 14 | 15 | 18.0 | $-3.0$ |
        | 4 | 16 | 20 | 21.1 | $-1.1$ |
        | 5 | 18 | 26 | 24.2 | 1.8 |

        The fitted value is the wage the fitted line predicts for a worker with that many years of education. The residual is the gap between the worker's actual wage and the wage the fitted line predicts, so it is the part of the wage the line leaves unexplained. The error term $u_i$ is defined relative to the true population regression line, which we never observe, while the residual $\hat{u}_i$ is defined relative to the line we drew through this particular sample.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Add up the five residuals from part 2. What do you notice, and why does this happen?
        """,
        r"""
        The residuals sum to $0.2 + 2.1 - 3.0 - 1.1 + 1.8 = 0$. The positive and negative residuals cancel exactly. This is not a coincidence. The intercept formula $\hat{\beta}_0 = \hat{\mu}_Y - \hat{\beta}_1\hat{\mu}_X$ forces the fitted line through the point of sample averages, so the fitted values average out to $\hat{\mu}_Y$ and the residuals average out to zero for any data set.

        *Optional derivation.* Writing each residual as $\hat{u}_i = Y_i - \hat{\beta}_0 - \hat{\beta}_1 X_i$ and summing over the $n$ observations,

        $$
        \begin{aligned}
        \sum_{i=1}^{n}\hat{u}_i &= \sum_{i=1}^{n} Y_i - n\hat{\beta}_0 - \hat{\beta}_1 \sum_{i=1}^{n} X_i \\
        &= n\hat{\mu}_Y - n\hat{\beta}_0 - n\hat{\beta}_1\hat{\mu}_X && \text{since } \textstyle\sum Y_i = n\hat{\mu}_Y \text{ and } \sum X_i = n\hat{\mu}_X \\
        &= n\left(\hat{\mu}_Y - \hat{\beta}_1\hat{\mu}_X - \hat{\beta}_0\right) \\
        &= n\left(\hat{\beta}_0 - \hat{\beta}_0\right) = 0 && \text{since } \hat{\beta}_0 = \hat{\mu}_Y - \hat{\beta}_1\hat{\mu}_X.
        \end{aligned}
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Use the fitted line to predict the hourly wage of a worker with 13 years of education and of a worker with 4 years of education. Which prediction is an in-sample prediction and which is an out-of-sample prediction? What does the second prediction suggest about extrapolation?
        """,
        r"""
        For 13 years, $\hat{Y} = -3.7 + 1.55 \times 13 = 16.45$ dollars per hour. For 4 years, $\hat{Y} = -3.7 + 1.55 \times 4 = 2.50$ dollars per hour. The first is an in-sample prediction, because 13 lies inside the observed range of 10 to 18 years of education. The second is an out-of-sample prediction, or extrapolation, because 4 lies well outside that range. A predicted wage of &#36;2.50 per hour is below any wage we would expect to see, which shows that the straight line fitted to workers with 10 to 18 years of education need not describe workers far outside that range.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** Open Section 5.2 of the Lecture 5 notebook on the course website. Set the "Slope $b_1$" slider to exactly $0$, so that your line is flat, and move the "Intercept $b_0$" slider until the sum of squared residuals beneath the plot is as small as you can make it. Write down the intercept you find and the sum of squared residuals at that intercept. What sample statistic does your intercept approximate?
        """,
        r"""
        The sum of squared residuals is smallest at an intercept of about $24.5$, where it equals roughly $1{,}182$. This intercept approximates the sample mean of the forty wages, $\hat{\mu}_Y$. A flat line predicts the same wage for every worker, and the best single prediction is the sample mean. This flat line is the one Section 5.5 describes as having an $R^2$ of $0$, and its sum of squared residuals is the total sum of squares.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob3"></a>
    ## Problem 3. Measuring fit

    This problem uses the fitted values and residuals for the five workers that you computed in Problem 2. The formulas you need are in Section 5.5 of the Lecture 5 notebook.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Compute the total sum of squares (TSS), the explained sum of squares (ESS), and the sum of squared residuals (SSR). Check that $\text{TSS} = \text{ESS} + \text{SSR}$.
        """,
        r"""
        With $\hat{\mu}_Y = 18$, the deviations $Y_i - \hat{\mu}_Y$ are $-6, -1, -3, 2, 8$, so

        $$
        \text{TSS} = 36 + 1 + 9 + 4 + 64 = 114.
        $$

        The fitted values minus the sample mean, $\hat{Y}_i - \hat{\mu}_Y$, are $-6.2, -3.1, 0, 3.1, 6.2$, so

        $$
        \text{ESS} = 38.44 + 9.61 + 0 + 9.61 + 38.44 = 96.1.
        $$

        The squared residuals are $0.04, 4.41, 9.00, 1.21, 3.24$, so

        $$
        \text{SSR} = 17.9.
        $$

        The identity checks out, since $\text{ESS} + \text{SSR} = 96.1 + 17.9 = 114 = \text{TSS}$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Compute the $R^2$ of the regression in two ways, once as $\text{ESS}/\text{TSS}$ and once as $1 - \text{SSR}/\text{TSS}$. Interpret the number in one sentence.
        """,
        r"""
        $$
        R^2 = \frac{\text{ESS}}{\text{TSS}} = \frac{96.1}{114} \approx 0.84, \qquad
        R^2 = 1 - \frac{\text{SSR}}{\text{TSS}} = 1 - \frac{17.9}{114} \approx 0.84.
        $$

        Years of education account for about 84 percent of the variation in hourly wages across these five workers, and the remaining 16 percent is left in the residuals.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Compute the standard error of the regression (SER). Explain in one or two sentences what the number means, and be careful to state its units.
        """,
        r"""
        $$
        \text{SER} = \sqrt{\frac{\text{SSR}}{n - 2}} = \sqrt{\frac{17.9}{3}} \approx \sqrt{5.97} \approx 2.44.
        $$

        The SER is measured in the units of $Y$, dollars per hour. It says that a typical worker's wage sits about &#36;2.44 per hour away from the fitted line. We divide by $n - 2 = 3$ rather than by $n = 5$ because estimating the intercept and the slope used up two pieces of information.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Open Section 5.5 of the Lecture 5 notebook on the course website. The interactive plot fits a line to forty workers, and the "Spread of points around the line" slider controls how far the points scatter around a fixed true line. The caption beneath the plot reports $R^2$ and the SER. Set the slider to $0.5$, then $3.0$, then $9.0$, and at each setting write down $R^2$ and the SER. Describe the pattern in your two lists. Then explain, using the formulas in Section 5.5, why $R^2$ can never leave the interval from $0$ to $1$ while the SER has no upper limit.
        """,
        r"""
        At a spread of $0.5$ the caption reports $R^2 \approx 0.99$ and $\text{SER} \approx$ &#36;0.49. At $3.0$ it reports $R^2 \approx 0.72$ and $\text{SER} \approx$ &#36;2.94. At $9.0$ it reports $R^2 \approx 0.25$ and $\text{SER} \approx$ &#36;8.82. As the scatter grows, $R^2$ falls toward $0$ and the SER rises, so both measures report a worse fit, but in different ways. $R^2 = \text{ESS}/\text{TSS}$ is a share. Because $\text{TSS} = \text{ESS} + \text{SSR}$ and neither piece can be negative, ESS can never exceed TSS, so the ratio is trapped between $0$ and $1$. The SER is $\sqrt{\text{SSR}/(n-2)}$, and SSR is a sum of squared residuals in dollars, so it simply keeps growing as the points scatter further from the line.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** Suppose the researcher had recorded wages in cents rather than dollars, so that every value of $Y$ is 100 times larger. Without recomputing anything, state what happens to $\hat{\beta}_1$, to the SER, and to $R^2$. Explain briefly.
        """,
        r"""
        The slope and the SER are both measured in the units of $Y$, so both are multiplied by 100. The slope becomes 155 cents per year of education and the SER becomes about 244 cents. The $R^2$ does not change. It is a ratio of two sums of squares that are both measured in squared units of $Y$, so the factor of $100^2$ cancels from the numerator and the denominator. Changing units changes how we describe the fit in words, but not how good the fit is.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob4"></a>
    ## Problem 4. A binary independent variable

    Section 5.3 of the Lecture 5 notebook explains how to interpret the intercept and slope when the independent variable is binary. This problem checks that explanation against the OLS formulas. A second researcher records the hourly wages of six workers along with whether each worker holds a college degree.

    | Worker | College degree ($X$, 1 if yes, 0 if no) | Hourly wage in dollars ($Y$) |
    |:---:|:---:|:---:|
    | 1 | 0 | 14 |
    | 2 | 0 | 18 |
    | 3 | 0 | 22 |
    | 4 | 1 | 24 |
    | 5 | 1 | 30 |
    | 6 | 1 | 33 |
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Compute the average wage of the workers without a degree and the average wage of the workers with a degree. Then compute the difference between the two averages.
        """,
        r"""
        Without a degree, the average wage is $(14 + 18 + 22)/3 = 18$ dollars per hour. With a degree, it is $(24 + 30 + 33)/3 = 29$ dollars per hour. The difference is $29 - 18 = 11$ dollars per hour.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Now compute $\hat{\beta}_1$ and $\hat{\beta}_0$ from the OLS formulas in Section 5.2 of the Lecture 5 notebook, treating $X$ like any other independent variable. Show your work, starting from the sample means $\hat{\mu}_X$ and $\hat{\mu}_Y$.
        """,
        r"""
        The sample means are $\hat{\mu}_X = 3/6 = 0.5$ and $\hat{\mu}_Y = 141/6 = 23.5$. The deviations $X_i - \hat{\mu}_X$ are $-0.5$ for the first three workers and $0.5$ for the last three, and the deviations $Y_i - \hat{\mu}_Y$ are $-9.5, -5.5, -1.5, 0.5, 6.5, 9.5$. The sum of products and the sum of squared $X$ deviations are

        $$
        \begin{aligned}
        \sum_{i=1}^{n}(X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y) &= 4.75 + 2.75 + 0.75 + 0.25 + 3.25 + 4.75 = 16.5, \\
        \sum_{i=1}^{n}(X_i - \hat{\mu}_X)^2 &= 6 \times 0.25 = 1.5.
        \end{aligned}
        $$

        Dividing each by $n - 1 = 5$ gives the sample covariance $3.3$ and the sample variance of $X$ $0.3$, so

        $$
        \hat{\beta}_1 = \frac{3.3}{0.3} = 11, \qquad \hat{\beta}_0 = \hat{\mu}_Y - \hat{\beta}_1\hat{\mu}_X = 23.5 - 11 \times 0.5 = 18.
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Compare your answers to parts 1 and 2. In one or two sentences, explain why the OLS estimates line up with the group averages in the way that they do.
        """,
        r"""
        The intercept $\hat{\beta}_0 = 18$ equals the average wage of the workers without a degree, and the slope $\hat{\beta}_1 = 11$ equals the difference between the two group averages. When $X$ only takes the values $0$ and $1$, the fitted line has only two fitted values, $\hat{\beta}_0$ at $X = 0$ and $\hat{\beta}_0 + \hat{\beta}_1$ at $X = 1$. The line minimizes the sum of squared residuals by placing each of those two values at the average wage of the corresponding group, so the slope is the gap between the group averages.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** A news article summarizes this regression by writing that "earning a college degree raises hourly wages by &#36;11." Explain in two or three sentences what is wrong with this summary.
        """,
        r"""
        The regression shows that workers with a degree earn &#36;11 more per hour on average than workers without one in this sample. That is a statement about prediction and association. It does not show that the degree itself raises wages, because the two groups of workers may differ in other ways that also affect pay, such as ability, family background, or the kinds of jobs they take. The conditions needed to read a slope as a causal effect are the subject of Lecture 6.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob5"></a>
    ## Problem 5. Prepare for the Tuesday quiz

    Review your problem set answers, your class notes, and the lecture notebooks on the course website. The quiz on Tuesday will draw on the material covered by this problem set and the corresponding lecture notebooks.
    """)
    return


if __name__ == "__main__":
    app.run()
