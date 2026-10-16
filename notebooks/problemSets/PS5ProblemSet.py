# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.23.16"
__preliminary__ = False
__description__ = "Problem Set 5 with worked solutions beneath each question."
app = marimo.App(
    app_title="Problem Set 5: Inference and Omitted Variable Bias",
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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Problem Set 5</a></h1>'
                '</div>'
            ),
            mo.md(
                r"""
                **Inference and Omitted Variable Bias**

                - [Problem 0. Prepare before attempting the problems](#prob0)
                - [Problem 1. Heteroskedasticity](#prob1)
                - [Problem 2. Hypothesis tests and confidence intervals for the slope](#prob2)
                - [Problem 3. Omitted variable bias](#prob3)
                - [Problem 4. The multiple-variable regression model](#prob4)
                - [Problem 5. Measures of fit](#prob5)
                - [Problem 6. Prepare for the Tuesday quiz](#prob6)
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
    # Problem Set 5: Inference and Omitted Variable Bias

    Due at the beginning of class on Tuesday, October 13.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob0"></a>
    ## Problem 0. Prepare before attempting the problems

    Before attempting the problems below, spend around 3 hours reviewing Sections 7.3 through 7.5 of the Lecture 7 notebook and the Lecture 8 notebook on the course website, together with your class notes. Work through the interactive figures as you read, and keep a list of anything you find difficult. Discuss the items on that list with your classmates, bring them to the peer mentors, or come to office hours. The problems below will go much more smoothly after this review.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob1"></a>
    ## Problem 1. Heteroskedasticity
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** In one or two sentences each, explain what it means for the error term in the regression $Y = \beta_0 + \beta_1 X + u$ to be homoskedastic and what it means for it to be heteroskedastic. Then give an example of a regression, other than wages on education, in which you would expect the error to be heteroskedastic, and say which values of $X$ you expect to have the more dispersed errors and why.
        """,
        r"""
        The error is homoskedastic when its dispersion is the same at every value of $X$, so the points scatter around the population line by about the same amount everywhere. It is heteroskedastic when the dispersion changes with $X$, so the points are more spread out at some values of $X$ than at others. Many examples work. In a regression of household spending on household income, low-income households all spend close to their income because they have little choice, while high-income households differ widely in how much they spend and save, so the errors are more dispersed at high values of income. In a regression of a firm's sales on its number of employees, small firms have similar sales while large firms range from struggling to booming.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Section 7.3 of the Lecture 7 notebook says that heteroskedasticity shows up in a scatter plot as a change in the vertical dispersion of the points around the fitted line. Draw two scatter plots of wages against years of education, each with a fitted line. In the first, make the errors homoskedastic. In the second, make them heteroskedastic, with wages more dispersed at higher levels of education. Label the axes. Then explain in a sentence what someone should look for in a real scatter plot to decide which case they are in.
        """,
        r"""
        The first plot should show points scattered in a band of roughly constant width around an upward-sloping line. The second should show points that hug the line closely at low education and fan out above and below the line as education rises, so the band gets wider from left to right. To judge a real scatter plot, look at whether the vertical spread of the points around the fitted line changes as you move along the horizontal axis. A band of roughly constant width suggests homoskedastic errors, while a band that widens or narrows suggests heteroskedastic errors.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Open Section 7.3 of the Lecture 7 notebook on the course website and find the plot with five sliders. Each slider sets the dispersion of the error in one slice of the education range, from "8-10 years" on the left to "16-18 years" on the right. Beneath the plot, the notebook reports the variance estimate that assumes homoskedasticity next to the heteroskedasticity-robust estimate. Record both estimates for each of the following three settings. Start with all five sliders at their starting value of $2.5$. Then set the two outer sliders, "8-10 years" and "16-18 years," to $10$ and the other three to $1$. Finally set the middle slider, "12-14 years," to $10$ and the other four to $1$.
        """,
        r"""
        With all five sliders at $2.5$, the homoskedastic estimate is about $0.0034$ and the robust estimate about $0.0032$, so the two nearly agree. With the two outer sliders at $10$ and the rest at $1$, the homoskedastic estimate is about $0.0167$ and the robust estimate about $0.0353$, so the robust estimate is roughly twice as large. With only the middle slider at $10$, the homoskedastic estimate is about $0.0111$ and the robust estimate about $0.0012$, so the homoskedastic estimate is roughly nine times too large.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** In which of your three settings is the homoskedastic estimate too small, and in which is it too large? Section 7.3 says the robust formula gives more weight to a large residual when that observation is far from the average value of $X$. Use this fact to explain why large errors at the ends of the education range raise the variance of $\hat{\beta}_1$ much more than large errors in the middle, and why the homoskedastic formula misses this.
        """,
        r"""
        With the two outer sliders at $10$ the homoskedastic estimate is too small, and with the middle slider at $10$ it is too large. The slope of a fitted line is pinned down by the points far from the average level of education, because tilting the line moves its fitted values most at the ends of the $X$ range. A large error for a worker with 8 or 18 years of education therefore swings the slope estimate a lot, while a large error for a worker near the average of about 13 years barely moves it, because the line pivots around the middle. The robust formula multiplies each squared residual by $(X_i - \hat{\mu}_X)^2$, so it counts the outer errors heavily and the middle errors lightly. The homoskedastic formula pools all the residuals into a single average dispersion, $\widehat{\text{var}}(\hat{u})$, and spreads it evenly across the range, so it understates the variance when the big errors sit at the ends and overstates it when they sit in the middle.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** A researcher does not know whether the error in their regression is homoskedastic or heteroskedastic. Based on what you recorded in part 3, which of the two variance formulas is the safer choice for computing the standard error of $\hat{\beta}_1$? Explain your answer.
        """,
        r"""
        The heteroskedasticity-robust formula is the safer choice. When the error is heteroskedastic, the homoskedastic formula can be badly wrong in either direction, while the robust formula is designed to handle changing dispersion. When the error is homoskedastic, part 3 showed that the two estimates are nearly the same, so the researcher gives up almost nothing by using the robust formula. The cost of using the robust formula when it is not needed is small, while the cost of using the homoskedastic formula when it is wrong can be large.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob2"></a>
    ## Problem 2. Hypothesis tests and confidence intervals for the slope

    A researcher draws a random sample of $n = 200$ workers and regresses hourly wages on years of education, obtaining the fitted line $\hat{Y} = 9.5 + 0.75\,X$ with $\text{se}(\hat{\beta}_1) = 0.25$. Assume the least squares assumptions hold. Use the standard normal table in the appendix of the Lecture 4 notebook for the p-values.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** The researcher wants to test whether education has any effect on wages. State the null hypothesis and the alternative hypothesis in terms of $\beta_1$. Then compute the t-statistic, find the two-sided p-value, and say whether the null hypothesis is rejected at the 5 percent significance level.
        """,
        r"""
        The null hypothesis is $H_0: \beta_1 = 0$ and the alternative is $H_1: \beta_1 \neq 0$. The t-statistic is

        $$
        t = \frac{\hat{\beta}_1 - \beta_{1,H_0}}{\text{se}(\hat{\beta}_1)} = \frac{0.75 - 0}{0.25} = 3.0,
        $$

        so the estimate sits three standard errors above zero. The table gives $\Phi(-3.0) \approx 0.00135$, so the two-sided p-value is $p = 2 \times 0.00135 \approx 0.0027$. Since $0.0027 < 0.05$, the null hypothesis of no effect is rejected at the 5 percent level.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** In one or two sentences, explain what the p-value you found in part 1 means in the context of this regression. Your explanation should make clear what is being assumed and what probability is being described.
        """,
        r"""
        If education truly had no effect on wages, so that $\beta_1 = 0$, then only about $0.27$ percent of random samples of 200 workers would produce a slope estimate at least three standard errors away from zero, in either direction. An estimate like $0.75$ would be very surprising under the null hypothesis, which is why it counts as strong evidence against it.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** An earlier study of the same population reported that each year of education raises hourly wages by &#36;1.20. Using the same estimate and standard error as in part 1, test the null hypothesis that $\beta_1 = 1.2$ against the two-sided alternative. Compute the t-statistic and the p-value, and state whether the null is rejected at the 5 percent level and at the 10 percent level.
        """,
        r"""
        The t-statistic is

        $$
        t = \frac{0.75 - 1.2}{0.25} = -1.8,
        $$

        so the estimate lies $1.8$ standard errors below the earlier study's value. The table gives $\Phi(-1.8) \approx 0.0359$, so the two-sided p-value is $p = 2 \times 0.0359 \approx 0.072$. This is above $0.05$, so the null is not rejected at the 5 percent level, but it is below $0.10$, so the null is rejected at the 10 percent level. The data are mildly, but not strongly, inconsistent with a slope of $1.2$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Construct the 95 percent and the 90 percent confidence intervals for $\beta_1$ using the multiples in Section 7.5 of the Lecture 7 notebook. Then check that each interval agrees with your test results in parts 1 and 3. That is, say whether each interval contains $0$ and whether each contains $1.2$, and explain why the intervals and the tests must agree.
        """,
        r"""
        The intervals are

        $$
        \begin{aligned}
        \text{95 percent:} \quad & 0.75 \pm 1.96 \times 0.25 = 0.75 \pm 0.49, \quad \text{so } [0.26,\ 1.24], \\
        \text{90 percent:} \quad & 0.75 \pm 1.64 \times 0.25 = 0.75 \pm 0.41, \quad \text{so } [0.34,\ 1.16].
        \end{aligned}
        $$

        Neither interval contains $0$, which matches rejecting $\beta_1 = 0$ at both the 5 and 10 percent levels in part 1. The 95 percent interval contains $1.2$ but the 90 percent interval does not, which matches part 3, where $\beta_1 = 1.2$ was not rejected at the 5 percent level but was rejected at the 10 percent level. The intervals and the tests agree because a confidence interval is built as the set of null values the test does not reject at the matching significance level. A value inside the 95 percent interval is one whose t-statistic is less than $1.96$ in absolute value, and a value outside the 90 percent interval is one whose t-statistic exceeds $1.64$ in absolute value. With $|t| = 1.8$, the value $1.2$ falls between the two cutoffs.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob3"></a>
    ## Problem 3. Omitted variable bias
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Write down the omitted variable bias formula from Section 8.1, which says what $\hat{\beta}_1$ converges to in large samples when the error is correlated with $X$. Name the three quantities that appear in the bias term, and explain in a sentence each how the sign and the size of the bias depend on them.
        """,
        r"""
        $$
        \hat{\beta}_1 \overset{p}{\to} \beta_1 + \rho_{Xu}\cdot\frac{\sigma_u}{\sigma_X}.
        $$

        The bias term involves the correlation between $X$ and the error, $\rho_{Xu}$, the standard deviation of the error, $\sigma_u$, and the standard deviation of $X$, $\sigma_X$. The sign of the bias is the sign of $\rho_{Xu}$, so a positive correlation between the regressor and the omitted factors pushes the estimate above $\beta_1$ and a negative correlation pushes it below. The size of the bias grows as the correlation gets stronger in either direction, grows as the error becomes more dispersed, since the omitted factors then account for more of the variation in $Y$, and shrinks as $X$ becomes more dispersed, since a wide range of $X$ makes the relationship between $X$ and $Y$ easier to separate from the omitted factors.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Section 8.1 says that not every omitted variable creates omitted variable bias. State the two conditions an omitted variable must satisfy to bias the slope. Then, for the regression of hourly wages on years of education, give one example of a factor that belongs in the error term but is unlikely to bias $\hat{\beta}_1$, and explain which condition it fails.
        """,
        r"""
        An omitted variable biases the slope only if it affects $Y$ and varies systematically with $X$, so that it is correlated with the regressor. A factor that affects wages but is unrelated to education fails the second condition and causes no bias. For example, plain luck in the job search, such as whether a worker happened to apply to a firm just as it was expanding, affects wages but has no reason to be related to years of education, so it sits in the error term without biasing the slope. Similar examples are the month in which the worker was surveyed or whether the worker's employer was hit by an unexpected local event. Such factors add noise to the regression, which raises the variance of $\hat{\beta}_1$, but they do not shift its center.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** For each regression below, name one omitted factor that is likely to cause bias. Say how that factor is related to $X$, how it affects $Y$, and therefore what sign $\rho_{Xu}$ has. Then conclude whether $\hat{\beta}_1$ is biased upward or downward.

        - (a) $Y$ = a farm's crop yield, $X$ = the amount of fertilizer the farm applies
        - (b) $Y$ = whether a patient survives surgery, $X$ = the hospital's quality rating
        - (c) $Y$ = a country's life expectancy, $X$ = its number of doctors per thousand people
        """,
        r"""
        Many answers work. Some examples follow.

        - (a) Soil quality. Farms with poor soil tend to apply more fertilizer to make up for it, so soil quality is negatively related to fertilizer use, and better soil raises yields on its own. The error therefore tends to be high when $X$ is low, so $\rho_{Xu} < 0$ and $\hat{\beta}_1$ is biased downward. Fertilizer looks less effective than it really is.
        - (b) The severity of the patient's illness. The sickest patients are often sent to the highest-rated hospitals, so severity is positively related to the rating, and greater severity lowers the chance of survival. The error is low when $X$ is high, so $\rho_{Xu} < 0$ and $\hat{\beta}_1$ is biased downward. Good hospitals look less effective than they are.
        - (c) National income. Richer countries have more doctors and also better nutrition, sanitation, and housing, which raise life expectancy on their own. The error is high when $X$ is high, so $\rho_{Xu} > 0$ and $\hat{\beta}_1$ is biased upward. Doctors receive credit for gains that are really due to wealth.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Suppose that in the population of workers the true causal effect of a year of education on hourly wages is $\beta_1 = 1.2$, that the correlation between education and the error is $\rho_{Xu} = 0.3$, and that the standard deviations are $\sigma_u = 6$ and $\sigma_X = 3$. What value does $\hat{\beta}_1$ converge to as the sample grows? Repeat the calculation for a second population in which education is more spread out, with $\sigma_X = 6$ and everything else the same. Finally, explain in a sentence why collecting a very large sample from the first population would not solve the problem.
        """,
        r"""
        In the first population the bias is $0.3 \times 6 / 3 = 0.6$, so $\hat{\beta}_1$ converges to $1.2 + 0.6 = 1.8$, an estimate that overstates the causal effect by half. In the second population the bias is $0.3 \times 6 / 6 = 0.3$, so $\hat{\beta}_1$ converges to $1.5$. More variation in education cuts the bias in half, although it does not remove it. A very large sample does not help in the first population because the formula describes exactly where the estimate settles as $n$ grows. More data make $\hat{\beta}_1$ converge more tightly to $1.8$, not to $1.2$, so the estimator is biased and not consistent for the causal effect, as in Problem 3 of Problem Set 4.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob4"></a>
    ## Problem 4. The multiple-variable regression model

    Section 8.2 of the Lecture 8 notebook adds parental income, measured in thousands of dollars, to the wage regression,

    $$
    \text{wage}_i = \beta_0 + \beta_1\,\text{education}_i + \beta_2\,\text{parental income}_i + u_i.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** In a sentence each, interpret the population parameters $\beta_1$ and $\beta_2$, being explicit about what is held fixed in each case. Then explain the difference between what is held fixed in that interpretation and what OLS can actually hold fixed when it estimates $\beta_1$ from a sample.
        """,
        r"""
        The parameter $\beta_1$ is the change in a worker's hourly wage caused by one more year of education, holding parental income and the error term fixed. The parameter $\beta_2$ is the change in the wage caused by one more thousand dollars of parental income, holding education and the error fixed. The interpretation holds fixed everything else that affects wages, including the unobserved determinants in $u$ such as ability and ambition. OLS can only hold fixed the variables that are included in the regression. Its estimate of $\beta_1$ compares workers with the same parental income, but it cannot compare workers with the same ability, because ability is not observed and stays in the error term.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Section 8.3 reports the fitted multiple-variable regression $\widehat{\text{wage}} = 4.6 + 1.22 \cdot \text{education} + 0.10 \cdot \text{parental income}$. Compute the predicted hourly wage for three workers: one with 12 years of education and parental income of 40 thousand dollars, one with 16 years of education and parental income of 40 thousand dollars, and one with 12 years of education and parental income of 80 thousand dollars. Then say what the gap between the first and second predictions measures, and what the gap between the first and third measures.
        """,
        r"""
        $$
        \begin{aligned}
        4.6 + 1.22(12) + 0.10(40) &= 4.6 + 14.64 + 4.0 = 23.24, \\
        4.6 + 1.22(16) + 0.10(40) &= 4.6 + 19.52 + 4.0 = 28.12, \\
        4.6 + 1.22(12) + 0.10(80) &= 4.6 + 14.64 + 8.0 = 27.24.
        \end{aligned}
        $$

        The gap between the first and second predictions, $28.12 - 23.24 = 4.88 = 4 \times 1.22$, is the predicted wage difference associated with four more years of education among workers with the same parental income. The gap between the first and third, $27.24 - 23.24 = 4.00 = 40 \times 0.10$, is the predicted wage difference associated with 40 thousand dollars more parental income among workers with the same education.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** The education coefficient is $1.63$ in the single-variable regression of Section 8.3 and $1.22$ once parental income is added. Explain this drop using the omitted variable bias formula from Section 8.1. In your answer, say how parental income is related to education in the data, how it affects wages, what this implies about the sign of $\rho_{Xu}$ in the single-variable regression, and why adding parental income removes this source of bias.
        """,
        r"""
        In the single-variable regression, parental income sits in the error term. Workers with more education tend to come from richer families, so parental income is positively related to education, and parental income raises wages. The error is therefore high when education is high, so $\rho_{Xu} > 0$ and the single-variable slope is biased upward. It attributes to education part of the wage difference that is really due to family resources, which is why $1.63$ overstates the return. Adding parental income to the regression moves it out of the error term and into the set of variables that OLS holds fixed. The education coefficient is then estimated by comparing workers with the same parental income, so parental income can no longer be credited to education, and the slope falls to $1.22$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Open Section 8.3 of the Lecture 8 notebook on the course website and find the three-dimensional plot with three sliders. Set "$\beta_0$, the intercept" to $6.5$, "$\beta_1$, the slope on years of education" to $1.63$, and "$\beta_2$, the slope on parental income" to $0$, so that the surface matches the single-variable fitted line from Section 8.3. Record the sum of squared residuals reported in the caption. Then tick the box "Show the OLS surface instead of yours" and record the sum of squared residuals of the OLS surface. Explain what the gap between the two numbers represents.
        """,
        r"""
        With the sliders at $6.5$, $1.63$, and $0$, the sum of squared residuals is about $5{,}725$. Ticking the box moves the sliders to the OLS values of $4.6$, $1.22$, and $0.10$, and the sum of squared residuals falls to about $5{,}445$. The single-variable line is one of the flat surfaces OLS could have chosen, the one with $\beta_2 = 0$, and OLS picks the surface with the smallest sum of squared residuals of all, so it does at least as well. The gap of about $280$ is the reduction in the sum of squared residuals that comes from letting the surface tilt along the parental income axis, that is, the part of the variation in wages that parental income explains once education is already in the regression.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** After adding parental income, can the coefficient of $1.22$ be interpreted as the causal effect of a year of education on wages? Name two factors that remain in the error term and explain, in a sentence or two, what would need to be true of them for $1.22$ to be the causal effect.
        """,
        r"""
        Not necessarily. Ability and ambition, for example, remain in the error term, along with health, school quality, and luck. For $1.22$ to be the causal effect, the remaining omitted factors would need to be unrelated to education among workers with the same parental income, so that the first least squares assumption holds in the multiple-variable regression. If more able students still get more education even after accounting for family resources, then $\rho_{Xu}$ is still positive and $1.22$ still overstates the causal effect, though by less than $1.63$ did.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob5"></a>
    ## Problem 5. Measures of fit

    You were asked to skip this problem. It has moved to Problem Set 6 as Problem 1, and its solutions will be posted with that set.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob6"></a>
    ## Problem 6. Prepare for the Tuesday quiz

    Review your problem set answers, your class notes, and the lecture notebooks on the course website. The quiz on Tuesday will draw on the material covered by this problem set and the corresponding lecture notebooks.
    """)
    return


if __name__ == "__main__":
    app.run()
