# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.23.16"
__preliminary__ = False
__description__ = "Problem Set 4 with worked solutions beneath each question."
app = marimo.App(
    app_title="Problem Set 4: Least Squares Assumptions and the Slope Estimator",
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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Problem Set 4</a></h1>'
                '</div>'
            ),
            mo.md(
                r"""
                **Least Squares Assumptions and the Slope Estimator**

                - [Problem 0. Prepare before attempting the problems](#prob0)
                - [Problem 1. Conditional expectation](#prob1)
                - [Problem 2. The error term and the least squares assumptions](#prob2)
                - [Problem 3. Unbiasedness and consistency](#prob3)
                - [Problem 4. The variance of the slope estimator](#prob4)
                - [Problem 5. The sampling distribution of the slope](#prob5)
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
    # Problem Set 4: Least Squares Assumptions and the Slope Estimator

    Due at the beginning of class on Tuesday, October 6.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob0"></a>
    ## Problem 0. Prepare before attempting the problems

    Before attempting the problems below, spend around 3 hours reviewing the Lecture 6 notebook and Sections 7.1 and 7.2 of the Lecture 7 notebook on the course website, together with your class notes. Work through the interactive figures as you read, and keep a list of anything you find difficult. Discuss the items on that list with your classmates, bring them to the peer mentors, or come to office hours. The problems below will go much more smoothly after this review.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob1"></a>
    ## Problem 1. Conditional expectation

    Consider a population of workers. Let $X$ record whether a worker holds a college degree, so $X$ takes the values No and Yes. Let $Y$ be the worker's hourly wage in dollars, which to keep the arithmetic simple takes only the values 15, 25, and 35. The table below gives the joint probability distribution of $X$ and $Y$. Each cell is the probability that a randomly chosen worker has that combination of degree status and wage.

    | Hourly wage ($Y$) | College degree ($X$): No | College degree ($X$): Yes |
    |:---:|:---:|:---:|
    | 15 | 0.30 | 0.10 |
    | 25 | 0.15 | 0.20 |
    | 35 | 0.05 | 0.20 |
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Compute the marginal probability distribution of $X$, that is, the probability that a worker holds a degree and the probability that a worker does not. Then compute the marginal probability distribution of $Y$, that is, the probability of each of the three wage levels.
        """,
        r"""
        Summing each column gives the marginal distribution of $X$,

        $$
        \mathbb{P}(X = \text{No}) = 0.30 + 0.15 + 0.05 = 0.50, \qquad \mathbb{P}(X = \text{Yes}) = 0.10 + 0.20 + 0.20 = 0.50.
        $$

        Summing each row gives the marginal distribution of $Y$,

        $$
        \mathbb{P}(Y = 15) = 0.40, \qquad \mathbb{P}(Y = 25) = 0.35, \qquad \mathbb{P}(Y = 35) = 0.25.
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Compute the conditional expectation of the wage among workers without a degree, $\mathbb{E}[Y \mid X = \text{No}]$, following the two steps in Section 6.1 of the Lecture 6 notebook. First use Bayes' rule to find the conditional probability of each wage level given $X = \text{No}$. Then take the expected value of $Y$ using those conditional probabilities.
        """,
        r"""
        Dividing each entry of the No column by $\mathbb{P}(X = \text{No}) = 0.50$ gives the conditional probabilities

        $$
        \begin{aligned}
        \mathbb{P}(Y = 15 \mid \text{No}) &= \frac{0.30}{0.50} = 0.60, \qquad
        \mathbb{P}(Y = 25 \mid \text{No}) = \frac{0.15}{0.50} = 0.30, \\
        \mathbb{P}(Y = 35 \mid \text{No}) &= \frac{0.05}{0.50} = 0.10.
        \end{aligned}
        $$

        The conditional expectation weights each wage level by its conditional probability,

        $$
        \mathbb{E}[Y \mid X = \text{No}] = 15(0.60) + 25(0.30) + 35(0.10) = 9 + 7.5 + 3.5 = 20.
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Repeat the two steps to compute $\mathbb{E}[Y \mid X = \text{Yes}]$, the expected wage among workers with a degree.
        """,
        r"""
        Dividing the Yes column by $\mathbb{P}(X = \text{Yes}) = 0.50$ gives conditional probabilities of $0.20$, $0.40$, and $0.40$ for the three wage levels, so

        $$
        \mathbb{E}[Y \mid X = \text{Yes}] = 15(0.20) + 25(0.40) + 35(0.40) = 3 + 10 + 14 = 27.
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Compute the unconditional expected wage $\mathbb{E}[Y]$ in two ways. First use the marginal distribution of $Y$ from part 1. Then take a weighted average of the two conditional expectations from parts 2 and 3, using the marginal probabilities of $X$ as the weights. Explain in one sentence why the two approaches must give the same answer.
        """,
        r"""
        Using the marginal distribution of $Y$,

        $$
        \mathbb{E}[Y] = 15(0.40) + 25(0.35) + 35(0.25) = 6 + 8.75 + 8.75 = 23.5.
        $$

        Averaging the two conditional expectations with the group probabilities as weights,

        $$
        \mathbb{E}[Y] = 0.50 \times 20 + 0.50 \times 27 = 23.5.
        $$

        The two must agree because the conditional expectation is the average wage within each group, and weighting the group averages by the size of each group rebuilds the average over the whole population.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** In words, what does the difference $\mathbb{E}[Y \mid X = \text{Yes}] - \mathbb{E}[Y \mid X = \text{No}] = 7$ measure? Using Section 6.3 of the Lecture 6 notebook, explain whether this difference can be read as the causal effect of earning a degree on a worker's wage.
        """,
        r"""
        It measures how much higher the average wage is among workers with a degree than among workers without one, which is an association between degree status and wages in this population. It is not, by itself, the causal effect of a degree. Workers who earn degrees may differ from those who do not in ability, family background, and other factors that sit in the error term and also affect wages. Only if those factors are unrelated to degree status, so that the conditional expectation of the error does not vary with $X$, would the 7 dollar gap be the causal effect.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **6.** Suppose a researcher codes $X$ as 0 for No and 1 for Yes and uses OLS to estimate the regression $Y = \beta_0 + \beta_1 X + u$ in a very large random sample from this population. What values should the estimates $\hat{\beta}_0$ and $\hat{\beta}_1$ be close to? Explain using the last paragraph of Section 6.1 of the Lecture 6 notebook and what Problem Set 3 showed about regressions with a binary independent variable.
        """,
        r"""
        The regression line approximates the conditional expectation of $Y$ at each value of $X$. With a binary $X$ the line has only two fitted values, and Problem Set 3 showed that OLS places them at the two group averages. In a very large sample those averages are close to the population conditional expectations, so $\hat{\beta}_0$ should be close to $\mathbb{E}[Y \mid X = 0] = 20$ and $\hat{\beta}_1$ close to the gap between the groups, $27 - 20 = 7$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob2"></a>
    ## Problem 2. The error term and the least squares assumptions
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Consider the population model $Y = \beta_0 + \beta_1 X + u$, where $Y$ is a worker's hourly wage and $X$ is years of education. In one sentence, say what the error term $u$ represents. Then give three concrete examples of factors that belong in $u$ other than the four examples listed in Section 6.2 of the Lecture 6 notebook.
        """,
        r"""
        The error term collects every determinant of a worker's wage other than years of education, so it is the part of the wage the population line does not explain. Examples beyond ability, family background, health, and luck include years of work experience, occupation or industry, the local labor market or region, union membership, hours worked, and the quality of the schools the worker attended.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** For each pair below, list two unobserved factors that belong in $u$, meaning factors that affect $Y$ but are not included in $X$. For each factor, say whether it would likely violate the first least squares assumption, that $\mathbb{E}[u \mid X = x]$ does not vary with $x$, and explain in a few words why.

        - (a) $Y$ = exam score, $X$ = hours spent studying
        - (b) $Y$ = monthly sales, $X$ = advertising spending
        - (c) $Y$ = city crime rate, $X$ = number of police officers
        - (d) $Y$ = blood pressure, $X$ = hours of exercise per week
        """,
        r"""
        Many answers are possible. Some examples follow.

        - (a) Prior knowledge of the subject likely violates the assumption, since students who already know the material may study less, and test anxiety might violate it if anxious students study more. Both affect scores without appearing in $X$.
        - (b) Product quality likely violates the assumption, since firms with better products may also advertise more, and seasonal demand likely violates it, since firms advertise more before busy seasons that raise sales on their own.
        - (c) Local economic conditions likely violate the assumption, because poorer cities may have both more crime and different police budgets, and past crime levels likely violate it, because cities hire more officers in response to crime.
        - (d) Diet likely violates the assumption, since people who exercise more tend to eat differently, and age might violate it, since older people may exercise less and have higher blood pressure.

        In each case the factor makes $\mathbb{E}[u \mid X = x]$ change with $x$, so the OLS slope would mix the effect of $X$ with the effect of the omitted factor.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Section 6.4 of the Lecture 6 notebook says that the first least squares assumption cannot be tested with the data alone. A classmate proposes a test anyway. They say that you should compute the OLS residuals $\hat{u}_i$, group the workers by their years of education, and check whether the average residual differs across the groups. Explain why this check cannot tell us whether $\mathbb{E}[u \mid X = x]$ varies with $x$. Your work in Problem Set 3 on the sum of the residuals and the way OLS chooses its line may help.
        """,
        r"""
        The residuals are computed from the fitted line, not from the true population line, and OLS chooses that line precisely so that the residuals show no linear relationship with $X$. In Problem Set 3 we saw that the residuals sum to zero, and the same first-order conditions make them uncorrelated with $X$ in every sample. If ability rises with education, OLS tilts the line to absorb that pattern into the slope, and the residuals come out balanced across education levels anyway. A residual check therefore looks fine whether or not the assumption holds. The unobserved error $u$ is what would need to be examined, and we never observe it, so whether the assumption holds must be argued from how the data were generated.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** The second least squares assumption says the observations $(X_i, Y_i)$ are independently and identically distributed. Give one example of a sample in which independence fails and one in which identical distribution fails, using examples other than the two given in Section 6.4 of the Lecture 6 notebook. Explain in a sentence each why the failure occurs.
        """,
        r"""
        Independence fails when observations carry information about each other. For example, wages of workers who are members of the same family, or daily sales figures for the same store on consecutive days, are linked, so one observation helps predict another. Identical distribution fails when the observations are not drawn in the same way. For example, a wage sample that combines full-time workers surveyed in one country with part-time workers surveyed in another mixes two populations with different wage and education distributions. Other reasonable examples include students in the same classroom sharing a teacher (independence) or pooling data collected before and after a large minimum wage increase (identical distribution).
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** Open Section 6.4 of the Lecture 6 notebook on the course website and find the plot beneath Least Squares Assumption 1. The slider is labelled "Do higher-ability workers tend to get more education?" and the caption beneath the plot reports the pooled OLS slope. Record the pooled slope with the slider at $0$, at $0.5$, and at $1$. Then explain, using the conditional expectation of the error term $\mathbb{E}[u \mid X]$, why the pooled OLS slope moves away from the true causal effect of $1.20$ as the slider rises, and whether it overstates or understates that causal effect.
        """,
        r"""
        At $0$ the pooled slope is $1.20$, the same as the true causal effect of a year of education. At $0.5$ it is about $2.35$ and at $1$ it is about $2.20$, so at any positive setting the pooled slope sits well above $1.20$. Ability is the only factor in the error term here. When the slider is positive, the higher-ability workers hold more education, so $\mathbb{E}[u \mid X = x]$ rises with $x$ and the first least squares assumption fails. OLS credits education with the extra wages that ability produces, so the pooled slope overstates the causal effect. The slope need not keep rising as the slider increases, because separating the groups also spreads out $X$, but it stays above the true effect of $1.20$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **6.** Now find the plot beneath Least Squares Assumption 3 in the same section. Record the OLS slope with the box "Include the two mistyped wages in the fit" unticked and then ticked. Explain, using the least squares criterion from Lecture 5, why two observations out of 42 can move the slope this much.
        """,
        r"""
        With the box unticked the slope is $1.20$, and with it ticked the slope jumps to about $2.32$. OLS minimizes the sum of squared residuals, and squaring makes a residual of &#36;120 count 10,000 times as much as a residual of &#36;1.20. Leaving the two mistyped wages far above the line would add an enormous amount to that sum, so the line tilts steeply toward them even though the other 40 workers have not moved. This is why the third assumption asks that large outliers be unlikely, and why plotting the data before trusting a regression matters.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob3"></a>
    ## Problem 3. Unbiasedness and consistency

    Section 6.5 of the Lecture 6 notebook states that under the least squares assumptions the OLS slope estimator is unbiased and consistent. Recall the definitions of these two properties from Section 4.2 of the Lecture 4 notebook.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Return to the ability example from Section 6.4, where higher-ability workers get more education and ability is left in the error term, so the first least squares assumption fails. In this setting, is $\hat{\beta}_1$ an unbiased estimator of the causal effect $\beta_1$? Explain in one or two sentences.
        """,
        r"""
        No. Across repeated samples the OLS slope centers on a value above $\beta_1$, because in every sample OLS attributes to education part of the wage difference that ability produces. The bias is the gap between that center and the true effect, and it is positive here.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Would collecting a much larger sample fix the problem? That is, as $n$ grows, does $\hat{\beta}_1$ get closer and closer to the causal effect $\beta_1$? Explain in one or two sentences, and say which of the four categories from Problem 1 of Problem Set 2 (unbiased or biased, consistent or not consistent) describes $\hat{\beta}_1$ in this setting.
        """,
        r"""
        No. A larger sample makes the estimate settle down, but it settles on the wrong number, the biased slope that blends education and ability. More data only make the estimator converge to that value more tightly. In the language of Problem Set 2, $\hat{\beta}_1$ is biased and not consistent as an estimator of the causal effect $\beta_1$, even though it remains a perfectly good estimator of the association between education and wages.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob4"></a>
    ## Problem 4. The variance of the slope estimator

    Return to the five workers from Problem Set 3. There you found that the fitted line is $\hat{Y} = -3.7 + 1.55\,X$, that the sum of squared residuals is $\text{SSR} = 17.9$, and that $\sum_{i=1}^{n}(X_i - \hat{\mu}_X)^2 = 40$, where $n = 5$.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Use the formulas in Section 7.1 of the Lecture 7 notebook to compute three quantities for the five-worker regression: the estimated variance of the error term, $\widehat{\text{var}}(\hat{u})$, the estimated variance of the slope estimator, $\hat{\sigma}^2_{\hat{\beta}_1}$, and the standard error of the slope, $\text{se}(\hat{\beta}_1)$.
        """,
        r"""
        The estimated error variance divides the sum of squared residuals by $n - 2$,

        $$
        \widehat{\text{var}}(\hat{u}) = \frac{\text{SSR}}{n - 2} = \frac{17.9}{3} \approx 5.97.
        $$

        The estimated variance of the slope divides this by the variation in $X$,

        $$
        \hat{\sigma}^2_{\hat{\beta}_1} = \frac{\widehat{\text{var}}(\hat{u})}{\sum_{i=1}^{n}(X_i - \hat{\mu}_X)^2} = \frac{5.97}{40} \approx 0.149,
        $$

        and the standard error is its square root, $\text{se}(\hat{\beta}_1) = \sqrt{0.149} \approx 0.39$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** In two or three sentences, explain what the variance of the slope estimator, $\sigma^2_{\hat{\beta}_1}$, captures, and why we want to know it.
        """,
        r"""
        The slope estimate $\hat{\beta}_1$ is a random variable because it depends on which workers happen to be in the sample, so a different sample of five workers would give a different estimate. The variance of the slope estimator measures how much these estimates would spread out across repeated samples drawn from the same population. We want to know it because it tells us how much to trust a single estimate. A small variance means the estimate from our one sample is probably close to the true slope, while a large variance means it could easily be far off.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **3.** Section 7.1 shows that the variance of the slope estimator is

    $$
    \sigma^2_{\hat{\beta}_1} = \frac{\text{var}(u)}{(n-1)\,\widehat{\text{var}}(X)}.
    $$

    We say that one slope estimate is more *precise* than another when its estimator has the smaller variance, so that estimates from repeated samples would cluster more tightly around the true slope. Each part below describes a choice a researcher faces when collecting a sample of workers. In each case, say which sample gives the more precise slope estimate, and explain why in one or two sentences, referring to the part of the formula that is involved.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(a)** Surveying workers at a single firm, where nearly everyone has between 14 and 16 years of education, or surveying workers from across the whole city, where years of education range from 8 to 20.
        """,
        r"""
        The city-wide sample. Years of education vary far more across the city, so $\widehat{\text{var}}(X)$ is larger and the denominator of the formula is larger. Comparing workers with very different amounts of schooling reveals how wages change with education much more clearly than comparing workers who all have nearly the same schooling.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(b)** Surveying workers who all hold the same occupation, or surveying workers spread across many occupations, so that wage differences between occupations that have nothing to do with education end up in the error term.
        """,
        r"""
        The single-occupation sample. Pooling many occupations adds wage variation that education does not explain, which raises $\text{var}(u)$, the numerator of the formula. With less noise around the regression line, the relationship between wages and education stands out more clearly and the slope is estimated more precisely.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(c)** Surveying 50 workers or surveying 100 workers, drawn in the same way from the same population. Does doubling the sample cut the standard error in half? Explain what happens to it instead.
        """,
        r"""
        The sample of 100. Doubling $n$ roughly doubles $(n-1)$ in the denominator, so the variance of the slope estimator roughly halves. The standard error is the square root of the variance, so it falls by a factor of about $\sqrt{2} \approx 1.4$, not by half. Cutting the standard error in half requires about four times as many workers. Each extra observation adds information about the relationship, but precision improves with the square root of the sample size, so it takes a lot more data to make a big improvement.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** One researcher reports a slope estimate of $\hat{\beta}_1 = 1.55$ with $\text{se}(\hat{\beta}_1) = 0.39$ from a sample of five workers. Another reports $\hat{\beta}_1 = 1.25$ with $\text{se}(\hat{\beta}_1) = 0.05$ from a sample of 400 workers. Which estimate is more precise, that is, which comes from the estimator with the smaller variance? In one or two sentences, explain what the second researcher's standard error says about how far their estimate is likely to be from the true slope.
        """,
        r"""
        The second estimate is far more precise, with a standard error nearly eight times smaller. A standard error of $0.05$ means that, across repeated samples of 400 workers, the slope estimates would typically land within about $0.05$ of their center, so the true slope is very likely within a few tenths of a dollar of $1.25$. The first researcher's estimate of $1.55$ could easily be off by half a dollar or more in either direction, so it tells us much less about the true slope.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob5"></a>
    ## Problem 5. The sampling distribution of the slope

    Section 7.2 of the Lecture 7 notebook says that, under the least squares assumptions, the slope estimator $\hat{\beta}_1$ is approximately normally distributed across repeated samples. The distribution is centered at the true slope $\beta_1$ and has variance $\sigma^2_{\hat{\beta}_1}$. For parts 1 through 4, suppose we happen to know that the true slope in the population of workers is $\beta_1 = 1.2$, and that the standard deviation of the slope estimator for samples of five workers is $\sigma_{\hat{\beta}_1} = 0.39$.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Write down the sampling distribution of $\hat{\beta}_1$ for samples of five workers, using the notation of Section 7.2. Then explain in one or two sentences why you think the central limit theorem from Lecture 2 applies to $\hat{\beta}_1$ and gives its sampling distribution a normal shape.
        """,
        r"""
        $$
        \hat{\beta}_1 \sim \mathcal{N}\left(\beta_1,\ \sigma^2_{\hat{\beta}_1}\right) = \mathcal{N}\left(1.2,\ 0.39^2\right) \approx \mathcal{N}(1.2,\ 0.15).
        $$

        The central limit theorem applies because the slope estimator can be written as a weighted average of the sample observations, and averages of independent and identically distributed draws are approximately normal once the sample is reasonably large.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Section 2.6 of the Lecture 2 notebook states that 95 percent of the area under a normal curve lies within 1.96 standard deviations of its center. Use this fact to find the range of values that contains 95 percent of the slope estimates from samples of five workers. Is the estimate $\hat{\beta}_1 = 1.55$ from Problem Set 3 inside this range? What does your answer say about whether $1.55$ is an unusual estimate?
        """,
        r"""
        $$
        1.2 \pm 1.96 \times 0.39 = 1.2 \pm 0.76,
        $$

        so 95 percent of estimates fall between about $0.44$ and $1.96$. The estimate of $1.55$ sits comfortably inside this range, so it is not unusual. With only five workers, a slope estimate this far above $1.2$ is the kind of sampling variation we should expect.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** The estimate $1.55$ lies $0.35$ above the true slope of $1.2$. Standardize this gap as in Section 2.6 of Lecture 2, that is, express it as a number of standard deviations of the sampling distribution. Then use the standard normal table in the appendix of the Lecture 4 notebook to find the probability that a sample of five workers produces a slope estimate at least $0.35$ away from $1.2$ in either direction, that is, an estimate below $0.85$ or above $1.55$.
        """,
        r"""
        $$
        z = \frac{1.55 - 1.2}{0.39} \approx 0.90,
        $$

        so the estimate lies about $0.90$ standard deviations above the center of the sampling distribution. The table gives $\Phi(-0.90) \approx 0.184$ for the probability of an estimate at least $0.90$ standard deviations below the center, and by symmetry the probability of one at least $0.90$ standard deviations above is the same. Adding the two tails, about $2 \times 0.184 = 0.37$, or 37 percent, of samples of five workers would produce a slope estimate at least as far from $1.2$ as $1.55$ is.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Now suppose the researcher had surveyed 80 workers instead of five, so that the standard deviation of the slope estimator is much smaller, $\sigma_{\hat{\beta}_1} = 0.10$. Find the range that contains 95 percent of slope estimates for samples of this size. Comparing your answer with part 2, which property of the OLS estimator from Section 6.5 of the Lecture 6 notebook does the comparison illustrate?
        """,
        r"""
        $$
        1.2 \pm 1.96 \times 0.10 = 1.2 \pm 0.196,
        $$

        so 95 percent of estimates now fall between about $1.00$ and $1.40$, a much narrower band around the true slope. This illustrates consistency. As the sample grows, the sampling distribution stays centered on $\beta_1$ while its spread shrinks, so estimates from large samples are very likely to be close to the true slope.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** Open Section 7.2 of the Lecture 7 notebook on the course website. Play with the three sliders and the "Draw new sample" and "Reset plot" buttons until you understand what the simulation is designed to show. Pay attention to how the slope estimate and its standard error change from draw to draw, and to how the plot of collected slope estimates on the right responds to each slider. There will be a quiz question related to this simulation. In two or three sentences, describe what the simulation shows about the sampling distribution of $\hat{\beta}_1$.
        """,
        r"""
        Each press of "Draw new sample" draws a fresh sample of workers from the same population, fits an OLS line, and adds the slope estimate to the plot on the right. The estimates differ from draw to draw, but they pile up into a bell shape centered on the true slope of $1.2$, which is the sampling distribution from Section 7.2. Raising the sample size or the spread of education makes the pile narrower, and raising the error standard deviation makes it wider, exactly as the variance formula from Section 7.1 predicts. The standard error reported for each sample is roughly the width of that pile.
        """,
    )
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
