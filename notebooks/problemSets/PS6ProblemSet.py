# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.23.16"
__preliminary__ = False
__description__ = "Problem Set 6 with worked solutions beneath each question."
app = marimo.App(
    app_title="Problem Set 6: Control Variables and Regression Tables",
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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Problem Set 6</a></h1>'
                '</div>'
            ),
            mo.md(
                r"""
                **Control Variables and Regression Tables**

                - [Problem 0. Prepare before attempting the problems](#prob0)
                - [Problem 1. Measures of fit](#prob1)
                - [Problem 2. The least squares assumptions with several independent variables](#prob2)
                - [Problem 3. Control variables and bad controls](#prob3)
                - [Problem 4. The variance of a coefficient when independent variables are correlated](#prob4)
                - [Problem 5. Reading a regression table](#prob5)
                - [Problem 6. Prepare for the midterm](#prob6)
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
    # Problem Set 6: Control Variables and Regression Tables

    Due at the beginning of class on Tuesday, October 20.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob0"></a>
    ## Problem 0. Prepare before attempting the problems

    Before attempting the problems below, spend around 3 hours reviewing Section 8.4 of the Lecture 8 notebook, the Lecture 9 notebook, and the Lecture 10 notebook on the course website, together with your class notes. Work through the interactive figures as you read, and keep a list of anything you find difficult. Discuss the items on that list with your classmates, bring them to the peer mentors, or come to office hours. The problems below will go much more smoothly after this review.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob1"></a>
    ## Problem 1. Measures of fit

    A researcher regresses hourly wages on years of education and years of experience using a sample of $n = 53$ workers, so $k = 2$. The regression has a sum of squared residuals of $\text{SSR} = 2{,}000$ and a total sum of squares of $\text{TSS} = 4{,}000$.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Use the formulas in Section 8.4 of the Lecture 8 notebook to compute the standard error of the regression, the $R^2$, and the adjusted $R^2$. In a sentence, say what the standard error of the regression tells the researcher in this setting.
        """,
        r"""
        The standard error of the regression is

        $$
        \text{SER} = \sqrt{\frac{\text{SSR}}{n - k - 1}} = \sqrt{\frac{2{,}000}{50}} = \sqrt{40} \approx 6.32,
        $$

        so a typical residual is about &#36;6.32 per hour, which is how far actual wages tend to sit from the regression's predictions. The $R^2$ is $1 - 2{,}000 / 4{,}000 = 0.50$, so the two variables explain half of the variation in wages. The adjusted $R^2$ is

        $$
        \bar{R}^2 = 1 - \frac{n - 1}{n - k - 1}\cdot\frac{\text{SSR}}{\text{TSS}} = 1 - \frac{52}{50}\times 0.50 = 1 - 0.52 = 0.48.
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** The researcher adds a third independent variable, the worker's shoe size, and the sum of squared residuals falls to $1{,}980$. Recompute the $R^2$ and the adjusted $R^2$. Which measure rose and which fell? What does the comparison suggest about whether shoe size belongs in the regression?
        """,
        r"""
        With $k = 3$, the $R^2$ is $1 - 1{,}980 / 4{,}000 = 0.505$, up slightly from $0.50$. The adjusted $R^2$ is

        $$
        \bar{R}^2 = 1 - \frac{52}{49}\times\frac{1{,}980}{4{,}000} = 1 - 1.061 \times 0.495 \approx 0.475,
        $$

        down from $0.48$. The $R^2$ rose and the adjusted $R^2$ fell. Shoe size lowered the sum of squared residuals by only $20$, which is less than the penalty for using up another piece of information from the sample, so the adjusted $R^2$ says the small improvement in fit does not justify the extra independent variable. This is what we would expect from a variable with no real connection to wages.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Explain why the $R^2$ can never fall when an independent variable is added to a regression, no matter how useless that variable is. Your explanation should rely on how OLS chooses the coefficients (*hint*: OLS can always choose to set the coefficient estimates to zero!).
        """,
        r"""
        OLS chooses every coefficient, including the new one, to make the sum of squared residuals as small as possible. One option always available to it is to set the new coefficient to zero, which reproduces the old regression exactly and gives the old sum of squared residuals. OLS can only do as well or better than that option, so the sum of squared residuals cannot rise when an independent variable is added. Since $R^2 = 1 - \text{SSR}/\text{TSS}$ and the total sum of squares does not depend on the independent variables, the $R^2$ cannot fall.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Open Section 8.4 of the Lecture 8 notebook on the course website and find the slider labelled "Number of pure-noise independent variables added." Record the $R^2$, the adjusted $R^2$, and the standard error of the regression reported in the caption with the slider at $0$, $10$, $20$, and $30$. A classmate proposes choosing among the four regressions by picking the one with the highest $R^2$. Explain what is wrong with this rule, and which of the measures you recorded give a more honest picture of whether the noise variables improve the regression.
        """,
        r"""
        The caption reports roughly the following values.

        | Noise variables | $R^2$ | Adjusted $R^2$ | SER |
        |:---:|:---:|:---:|:---:|
        | 0 | 0.427 | 0.418 | 6.47 |
        | 10 | 0.455 | 0.401 | 6.57 |
        | 20 | 0.487 | 0.385 | 6.65 |
        | 30 | 0.507 | 0.349 | 6.84 |

        The classmate's rule would pick the regression with 30 noise variables, which is the worst of the four, because the $R^2$ rewards every added variable regardless of whether it means anything. Each noise variable fits a little of the sample's randomness by chance, so the $R^2$ creeps up even though the variables carry no information about wages. The adjusted $R^2$ and the standard error of the regression both account for the information used up by the extra coefficients, and both move in the direction of a worse regression as noise is added. They give the honest picture.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** Section 8.4 notes that adding parental income cut the education slope by about a quarter but raised the $R^2$ only from $0.398$ to $0.427$. Would a very high $R^2$ in a regression of wages on education tell you that the first least squares assumption holds, so that the slope can be read as a causal effect? Explain in two or three sentences.
        """,
        r"""
        No. The $R^2$ measures how tightly the points cluster around the fitted line, while the first least squares assumption is about whether the omitted factors in the error term are related to education. These are different questions. A regression can fit tightly and still be badly biased, as when ability both raises wages and rises with education, so that the fitted line passes neatly through points whose slope mixes the two effects. Conversely, parental income barely improved the fit yet removed a sizeable bias. Whether the slope is causal must be argued from how the data were generated, not read off the $R^2$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob2"></a>
    ## Problem 2. The least squares assumptions with several independent variables

    Consider the population regression model

    $$
    \text{wage}_i = \beta_0 + \beta_1\,\text{education}_i + \beta_2\,\text{experience}_i + u_i,
    $$

    where the wage is in dollars per hour and education and experience are both measured in years.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Write down the four least squares assumptions from Section 9.1 of the Lecture 9 notebook for this model, using the notation of this model rather than the general $X_1, \ldots, X_k$ notation. Then say which of the four is new relative to the single-variable regression of Lecture 6, and which one is needed to read $\beta_1$ and $\beta_2$ as the causal effects of education and experience, respectively.
        """,
        r"""
        The four assumptions are, first, that the conditional expectation of the error given both independent variables is zero, $\mathbb{E}[u \mid \text{education}, \text{experience}] = 0$; second, that the observations $(\text{wage}_i, \text{education}_i, \text{experience}_i)$ for $i = 1, \ldots, n$ are independently and identically distributed; third, that large outliers in the wage, education, or experience are unlikely; and fourth, that there is no perfect multicollinearity, so that neither education nor experience is an exact linear function of the other. The fourth assumption is new. Only the first assumption gives $\beta_1$ and $\beta_2$ a causal interpretation. The second and third make the sample estimates reliable and support the standard errors but do not make the relationship causal.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Explain in words what the first assumption requires for you to interpret the education coefficient in this particular model causally. Then give one unobserved factor that would likely violate the assumption for education, and explain in a sentence why.
        """,
        r"""
        The assumption compares workers who have the same years of experience but different years of education, and it requires that these workers have, on average, the same values of the remaining determinants of wages in $u$, such as ability, health, family background, and luck. Put differently, once experience is held fixed, the omitted factors must not be systematically higher or lower for more educated workers. Ability likely violates the assumption. More able people tend to stay in school longer and also earn more at any level of education, so among workers with the same experience, the more educated ones would have higher average ability, and the average error would rise with education.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** A researcher adds a third independent variable, experience measured in months, alongside experience measured in years. Explain why OLS cannot estimate this regression, and name the assumption that fails.
        """,
        r"""
        Experience in months is exactly twelve times experience in years for every worker, so one independent variable is an exact linear function of another. This is perfect multicollinearity, and it violates the fourth assumption. The regression cannot tell apart the effect of a year of experience from the effect of twelve months of experience, because the two can never move separately in the data.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Another researcher wants to study the wage gap between women and men. They add two indicator variables to the model, one equal to 1 for women and 0 for men, and one equal to 1 for men and 0 for women, so the model has both indicators. Explain why this regression suffers from perfect multicollinearity, and say what the researcher should do instead.
        """,
        r"""
        For every worker the two indicators add up to exactly 1, since each worker is either a woman or a man. The intercept is a variable that equals 1 for every observation, so the male indicator equals 1 minus the female indicator, an exact linear function of the intercept and the other indicator. The fourth assumption fails. The researcher should drop one of the two indicators, for example keeping only the female indicator. Its coefficient then measures the wage difference between women and men who have the same education and experience, with the intercept describing men.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob3"></a>
    ## Problem 3. Control variables and bad controls

    Return to the wage regression from Lecture 8, where the researcher wants to estimate the causal effect of education on wages and includes parental income as a second independent variable,

    $$
    \text{wage}_i = \beta_0 + \beta_1\,\text{education}_i + \beta_2\,\text{parental income}_i + u_i.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** In this regression, which variable is the variable of interest and which is a control variable? Using Section 9.2 of the Lecture 9 notebook, write down the modified first OLS assumption with control variables for this regression. Then explain in your own words what the assumption requires us to believe, and why it is easier to satisfy than the first least squares assumption from Section 9.1.
        """,
        r"""
        Education is the variable of interest, because its causal effect is what the researcher wants to estimate. Parental income is a control variable, included so that the regression compares workers from similar family backgrounds. The assumption is

        $$
        \mathbb{E}[u \mid \text{education}, \text{parental income}] = \mathbb{E}[u \mid \text{parental income}].
        $$

        It requires that, among workers with the same parental income, the average value of the omitted factors in $u$ does not vary with education. It allows the average error to vary with parental income. For example, workers from richer families may have higher average ability or better health, and that is permitted. The assumption from Section 9.1 would instead require the average error to be zero at every combination of education and parental income, which also rules out any relationship between the error and parental income.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Suppose parental income is strongly related to unobserved factors that remain in the error term, such as the quality of the schools a worker attended. Does this threaten the causal interpretation of the education coefficient $\beta_1$? Does it threaten the causal interpretation of the parental income coefficient $\beta_2$? Explain each answer in a sentence or two.
        """,
        r"""
        It does not threaten the interpretation of $\beta_1$. The conditional mean independence assumption permits the error to be related to the control variable. What matters for education is only that, once parental income is held fixed, education is unrelated to the remaining omitted factors. It does threaten the interpretation of $\beta_2$. Reading $\beta_2$ as the causal effect of parental income would require the error to be unrelated to parental income once education is held fixed, and school quality in the error term violates that. The coefficient on parental income mixes the effect of family income with the effect of school quality and anything else that travels with it, which is why we treat it as a control and do not interpret it causally.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** For each variable below, say whether it would be a good control or a bad control in the regression of wages on education, and explain in a sentence why, using the rule at the end of Section 9.3 of the Lecture 9 notebook.

        - (a) The number of siblings the worker has
        - (b) The industry the worker is currently employed in
        - (c) The region of the country where the worker grew up
        - (d) Whether the worker currently holds a managerial position
        """,
        r"""
        - (a) A good control. The number of siblings is determined before the worker's schooling and may affect both schooling and wages through family resources, so holding it fixed removes a source of bias without blocking any effect of education.
        - (b) A bad control. Education affects which industry a worker ends up in, and industry affects wages, so industry lies on the causal path from education to wages. Holding it fixed blocks the part of education's effect that works through moving people into better-paid industries.
        - (c) A good control. Where a worker grew up is fixed before schooling, and it may affect both the amount of schooling available and local wages, so it is a confounder to hold fixed rather than a pathway.
        - (d) A bad control. Education raises the chance of reaching a managerial position, and managers earn more, so this variable is a mediator. Holding it fixed removes the part of the return to education that comes from promotion into management.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Pick one of the bad controls from part 3 and draw a diagram like the one in Section 9.3 of the Lecture 9 notebook, with boxes for education, the bad control, and the wage, and arrows showing the causal paths. Then explain in two sentences what part of the effect of education is blocked when this control is included, and how you think this control would effect the estimate of education on wages, $\hat{\beta}_1$.
        """,
        r"""
        The diagram should have an arrow from education directly to the wage, an arrow from education to the bad control, say industry, and an arrow from industry to the wage. Including industry as a control holds it fixed, so the coefficient on education captures only the direct arrow and leaves out the path that runs from education through industry to the wage. Since that path is part of how education raises wages, the coefficient understates the total effect of education on wages.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob4"></a>
    ## Problem 4. The variance of a coefficient when independent variables are correlated

    Section 9.4 of the Lecture 9 notebook gives the variance of the coefficient on $X_1$ in a regression with two independent variables and homoskedastic errors,

    $$
    \sigma^2_{\hat{\beta}_1} = \frac{1}{n}\cdot\frac{1}{1 - \rho^2_{X_1 X_2}}\cdot\frac{\sigma_u^2}{\sigma_{X_1}^2},
    $$

    where $\rho_{X_1 X_2}$ is the correlation between the two independent variables.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Suppose $n = 100$, $\sigma_u = 3$, and $\sigma_{X_1} = 1.5$. Compute the standard error of $\hat{\beta}_1$ when the two independent variables are uncorrelated, when their correlation is $0.6$, and when their correlation is $0.9$. Then work out roughly how large the sample would have to be at a correlation of $0.9$ to bring the standard error back down to its value when $X_1$ and $X_2$ are not correlated.
        """,
        r"""
        With no correlation the variance is $\frac{1}{100}\cdot 1 \cdot \frac{9}{2.25} = 0.04$, so the standard error is $\sqrt{0.04} = 0.20$. At a correlation of $0.6$ the variance-inflation factor is $1/(1 - 0.36) = 1.5625$, so the variance is $0.04 \times 1.5625 = 0.0625$ and the standard error is $0.25$. At a correlation of $0.9$ the factor is $1/(1 - 0.81) \approx 5.26$, so the variance is about $0.21$ and the standard error is about $0.46$. To undo an inflation factor of $5.26$ the sample must grow by the same factor, to roughly $526$ observations, because $n$ enters the formula as $1/n$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Open Section 9.4 of the Lecture 9 notebook on the course website and find the plot with the slider labelled "Correlation between the two independent variables." The caption beneath the plot reports the standard error of $\hat{\beta}_1$. Record the standard error with the slider at $0$, $0.5$, $0.8$, and $0.95$. Then explain, using what the scatter plot on the left shows at $0.95$, why OLS pins down the slope on $X_1$ less precisely even though every observation still has its own distinct values of $X_1$ and $X_2$.
        """,
        r"""
        The caption reports standard errors of about $0.163$ at $0$, $0.189$ at $0.5$, $0.272$ at $0.8$, and $0.523$ at $0.95$. At $0.95$ the scatter plot collapses toward a thin diagonal band, so observations with similar values of $X_2$ have nearly identical values of $X_1$. OLS estimates the slope on $X_1$ by comparing observations that differ in $X_1$ while holding $X_2$ fixed, and inside the band there is very little such variation left to use. The estimate therefore depends on a small amount of information and swings widely from sample to sample, which is the wide sampling distribution on the right.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** A researcher regresses wages on education and parental income and finds that the two independent variables are highly correlated, so the standard error on education is large. A colleague suggests dropping parental income to shrink the standard error. Explain what would be gained and what would be lost by following this advice, using the omitted variable bias formula from Section 8.1 of the Lecture 8 notebook and the variance formula above.
        """,
        r"""
        Dropping parental income would remove the variance inflation, since the regression would no longer need to separate the two variables, so the standard error on education would fall. But parental income would move back into the error term, and because it is strongly correlated with education and affects wages, the education coefficient would pick up omitted variable bias of the kind described by the formula in Section 8.1. The researcher would trade a less precise but centered estimate for a more precise estimate that is centered on the wrong number. High correlation between the independent variables raises the variance of the estimate but does not bias it, so the usual remedy is a larger sample, not dropping the control.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob5"></a>
    ## Problem 5. Reading a regression table

    A researcher collects data on $n = 800$ apartments in a city and estimates four regressions of the monthly rent in dollars on the apartment's distance from downtown in miles, its size in hundreds of square feet, the age of the building in years, and an indicator equal to 1 if the apartment comes with a parking space. The table follows the format of Section 10.1 of the Lecture 10 notebook, with standard errors in parentheses. The asterisks have been left off so that you can work them out yourself in part 6.

    | Dependent variable: monthly rent (dollars) | (1) | (2) | (3) | (4) |
    |:---|:---:|:---:|:---:|:---:|
    | Distance from downtown (miles) | $-61.4$ | $-94.8$ | $-92.1$ | $-89.6$ |
    | | (8.3) | (7.1) | (7.0) | (6.9) |
    | Size (hundreds of sq. ft.) | | 181.3 | 176.6 | 172.4 |
    | | | (12.4) | (12.1) | (11.8) |
    | Building age (years) | | | $-4.7$ | $-4.5$ |
    | | | | (2.6) | (2.5) |
    | Parking space | | | | 110.2 |
    | | | | | (45.1) |
    | Constant | 1,652.7 | 1,118.5 | 1,206.9 | 1,163.8 |
    | | (24.9) | (41.2) | (47.3) | (49.6) |
    | Observations | 800 | 800 | 800 | 800 |
    | $R^2$ | 0.068 | 0.312 | 0.318 | 0.326 |
    | Adjusted $R^2$ | 0.067 | 0.310 | 0.315 | 0.323 |
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Interpret the coefficient on distance from downtown in column (1) and then in column (4). State the units of each number, and be explicit about what is held fixed in each case.
        """,
        r"""
        In column (1), apartments one mile farther from downtown rent for about 61 dollars less per month on average, with nothing else held fixed, so the comparison mixes apartments of all sizes, ages, and amenities. In column (4), among apartments with the same size, the same building age, and the same parking status, each additional mile from downtown is associated with a rent that is about 90 dollars per month lower (the estimate is $-89.6$). Both coefficients are in dollars per month per mile.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Interpret the coefficient on size and the coefficient on the parking space indicator in column (4). State the units of each number and what is held fixed.
        """,
        r"""
        Among apartments with the same distance from downtown, the same building age, and the same parking status, each additional hundred square feet of size is associated with a monthly rent that is about 172 dollars higher (the estimate is $172.4$). The units are dollars per month per hundred square feet. Among apartments with the same distance, size, and age, an apartment with a parking space is predicted to rent for about 110 dollars more per month than one without (the estimate is $110.2$), so the units are dollars per month, and the number is the predicted gap between the two groups rather than the effect of a one-unit change in a continuous variable.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Interpret the constant in column (4). Does it describe an apartment we could actually observe? Explain in a sentence or two.
        """,
        r"""
        The constant of $1{,}163.8$ is the predicted monthly rent for an apartment with every independent variable equal to zero, that is, an apartment located downtown, with zero square feet, in a building that is zero years old, and without parking. No such apartment exists, since size cannot be zero, so the constant anchors the regression surface rather than describing any real apartment. It is an extrapolation in the sense of Lecture 5.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** The distance coefficient falls from $-61.4$ to $-94.8$ when size is added in column (2). Explain this change using the omitted variable bias formula from Section 8.1 of the Lecture 8 notebook. Say how size is likely related to distance in this sample, how size affects rent, what this implies about the sign of the correlation between distance and the error in column (1), and therefore whether column (1) overstates or understates the rent penalty for distance.
        """,
        r"""
        In column (1) size sits in the error term. Apartments farther from downtown tend to be larger, so size is positively correlated with distance, and larger apartments rent for more. The error in column (1) is therefore high when distance is high, so the correlation between distance and the error is positive and the coefficient is biased upward, toward zero here since the true coefficient is negative. Column (1) understates the rent penalty for distance, because the higher rents of the larger apartments found farther out partly cancel the distance effect. Holding size fixed in column (2) compares apartments of the same size at different distances, and the penalty appears at its fuller value of about 95 dollars per mile.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** The distance coefficient barely moves when building age is added in column (3), even though age itself is associated with rent. What does this tell you about the relationship between distance and building age in this sample? Explain using the two conditions for an omitted variable to cause bias.
        """,
        r"""
        An omitted variable biases a coefficient only if it affects the outcome and is correlated with the independent variable. Age does affect rent, since older buildings rent for less, so the first condition holds. The coefficient on distance is nearly unchanged, so the second condition must fail. Building age must be close to uncorrelated with distance from downtown in this sample. Older and newer buildings are spread across the city in a way that does not line up with distance, so leaving age out of column (2) caused little or no bias in the distance coefficient.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **6.** Work out the statistical significance of the building age coefficient and of the parking space coefficient in column (4). For each coefficient, follow these steps. First, write down the null hypothesis that the population coefficient is zero. Second, compute the t-statistic by dividing the estimated coefficient by its standard error. Third, look up $\Phi(-|t|)$ in the standard normal table in the appendix of the Lecture 4 notebook and double it to get the two-sided p-value. Fourth, compare the p-value with $0.10$, $0.05$, and $0.01$, state at which of those three significance levels the coefficient is statistically significant, and assign the asterisks it would receive under the convention in Section 10.3 of the Lecture 10 notebook.
        """,
        r"""
        For building age the null hypothesis is $H_0: \beta_{\text{age}} = 0$, and

        $$
        t = \frac{-4.5 - 0}{2.5} = -1.8, \qquad p = 2\,\Phi(-1.8) \approx 2 \times 0.0359 = 0.072.
        $$

        The p-value is below $0.10$ but above $0.05$, so building age is statistically significant at the 10 percent level only and receives one asterisk. For the parking space indicator the null hypothesis is $H_0: \beta_{\text{parking}} = 0$, and

        $$
        t = \frac{110.2 - 0}{45.1} \approx 2.44, \qquad p = 2\,\Phi(-2.44) \approx 2 \times 0.0073 = 0.015.
        $$

        The p-value is below $0.05$ but above $0.01$, so parking is significant at the 10 and 5 percent levels but not at the 1 percent level, and it receives two asterisks. For comparison, distance and size have t-statistics of about $-13.0$ and $14.6$, so both are significant at the 1 percent level and would receive three asterisks.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **7.** Construct the 95 percent confidence interval for the parking space coefficient in column (4). Does it contain zero? Explain in a sentence why your answer had to agree with the asterisks you assigned in part 6.
        """,
        r"""
        $$
        110.2 \pm 1.96 \times 45.1 = 110.2 \pm 88.4, \qquad \text{so } [21.8,\ 198.6].
        $$

        The interval does not contain zero. A 95 percent confidence interval collects the null values that a test at the 5 percent level does not reject, so zero lies outside the interval exactly when the coefficient is significant at the 5 percent level, which is what the two asterisks say.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **8.** A newspaper article reports that "distance from downtown and apartment size are both highly statistically significant, so both matter about equally for rent." Use the column (4) estimates to evaluate this claim. Compare the predicted rent change from one extra mile of distance with the change from one extra hundred square feet, and explain what statistical significance does and does not tell us.
        """,
        r"""
        Statistical significance says only that we can reject a zero coefficient with confidence. It reflects the size of the estimate relative to its standard error, not the size of the effect itself. One extra mile from downtown changes predicted rent by about $-89.6$ dollars, while one extra hundred square feet changes it by about $+172.4$ dollars, so the two are not equally important per unit, and whether either is "large" depends on how much distance and size actually vary across apartments. Both coefficients are precisely estimated, which is why both are significant at the 1 percent level, but precision and importance are different things.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **9.** Interpret the $R^2$ of $0.326$ in column (4) in a sentence. Then compare the rise in the $R^2$ when size is added in column (2) with the rise when building age is added in column (3), and say what the comparison tells you about the two variables. Does the large jump in column (2) tell you that the size coefficient is a causal effect? Explain briefly.
        """,
        r"""
        The four independent variables in column (4) together explain about 33 percent of the variation in monthly rents across the 800 apartments, leaving about 67 percent to the residuals. Adding size raises the $R^2$ from $0.068$ to $0.312$, while adding building age raises it only from $0.312$ to $0.318$, so size explains far more of the variation in rents than age does once distance is in the regression. The jump says nothing about causality. The $R^2$ measures how tightly rents cluster around the fitted surface, while a causal interpretation of the size coefficient depends on whether the omitted determinants of rent are unrelated to size once the other variables are held fixed. A variable can explain a lot of variation and still have a biased coefficient, and the reverse is also possible.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **10.** The total sum of squares of monthly rent in this sample is $\text{TSS} = 160{,}000{,}000$ dollars squared. Use the $R^2$ of column (4) to compute the sum of squared residuals, then compute the standard error of the regression for column (4) using the formula in Section 8.4 of the Lecture 8 notebook. Interpret the standard error of the regression in a sentence, stating its units.
        """,
        r"""
        Since $R^2 = 1 - \text{SSR}/\text{TSS}$, the sum of squared residuals is

        $$
        \text{SSR} = (1 - 0.326) \times 160{,}000{,}000 = 107{,}840{,}000.
        $$

        With $n = 800$ and $k = 4$,

        $$
        \text{SER} = \sqrt{\frac{\text{SSR}}{n - k - 1}} = \sqrt{\frac{107{,}840{,}000}{795}} \approx \sqrt{135{,}648} \approx 368.
        $$

        The standard error of the regression is measured in dollars per month, the units of the dependent variable. It says that a typical apartment's actual rent sits about 368 dollars away from the rent the column (4) regression predicts for it.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **11.** Two apartments have the same size, the same building age, and the same parking status, but one is two miles farther from downtown. Using column (4), what is the predicted difference in their monthly rents? Then suppose the researcher treats distance as the variable of interest and the other three variables as controls. Write down the conditional mean independence assumption for this regression, and name one factor still in the error term that could violate it.
        """,
        r"""
        The predicted difference is $2 \times (-89.6) = -179.2$ dollars per month, so the farther apartment is predicted to rent for about 179 dollars less. The assumption is

        $$
        \mathbb{E}[u \mid \text{distance}, \text{size}, \text{age}, \text{parking}] = \mathbb{E}[u \mid \text{size}, \text{age}, \text{parking}],
        $$

        so that among apartments with the same size, age, and parking status, the omitted determinants of rent do not vary systematically with distance. Neighborhood amenities such as restaurants, transit access, or school quality could violate it, since they affect rent and are likely better closer to downtown. If so, part of the estimated penalty reflects amenities rather than distance itself.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob6"></a>
    ## Problem 6. Prepare for the midterm

    Review your problem set answers, your class notes, and the lecture notebooks on the course website. There is no quiz on Tuesday. The midterm on Thursday, October 22, will draw on the material covered by this problem set and the earlier ones, and it will include a long problem very much like the regression-table problem above.
    """)
    return


if __name__ == "__main__":
    app.run()
