# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.23.16"
__preliminary__ = False
__description__ = "Problem Set 1 with worked solutions beneath each question."
app = marimo.App(
    app_title="Problem Set 1: Probability and Random Variables",
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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Problem Set 1</a></h1>'
                '</div>'
            ),
            mo.md(
                r"""
                **Probability and Random Variables**

                - [Problem 0. Prepare before attempting the problems](#prob0)
                - [Problem 1. Probability and random variables](#prob1)
                - [Problem 2. Central limit theorem](#prob2)
                - [Problem 3. Prepare for the Tuesday quiz](#prob3)
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
    # Problem Set 1: Probability and Random Variables

    Due at the beginning of class on Tuesday, September 15.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob0"></a>
    ## Problem 0. Prepare before attempting the problems

    Before attempting the problems below, spend around 3 hours reviewing the Lecture 2 and Lecture 3 notebooks on the course website, together with your class notes. Work through the interactive figures as you read, and keep a list of anything you find difficult. Discuss the items on that list with your classmates, bring them to the peer mentors, or come to office hours. The problems below will go much more smoothly after this review.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob1"></a>
    ## Problem 1. Probability and random variables
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** In two or three sentences, describe the differences between a probability density function and a cumulative distribution function.
        """,
        r"""
        A probability density function (PDF) shows how likely different values of a continuous random variable are, with the total area under the curve equal to 1. In contrast, a cumulative distribution function (CDF) gives the probability that the random variable is less than or equal to a given value, so it is always non-decreasing and ranges from 0 to 1.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Section 2.3 of the Lecture 2 notebook records the number of emails arriving in each of 24 separate hours, together with the true probability of each outcome. Compute the variance and the sample variance using that table. Are they the same? If not, when would they be the same and why?
        """,
        r"""
        Using the formulas from Section 2.3 of Lecture 2, the variance of $X$ is given by

        $$
        \begin{aligned}
        \text{var}(X) = \sigma_X^2 &= \sum_{i=1}^{K} (x_i - \mu_X)^2 \cdot p_i \\
        &= (0 - 0.35)^2 \cdot 0.80 + (1 - 0.35)^2 \cdot 0.10 + (2 - 0.35)^2 \cdot 0.06 \\
        &\quad + (3 - 0.35)^2 \cdot 0.03 + (4 - 0.35)^2 \cdot 0.01 \\
        &= 0.6475
        \end{aligned}
        $$

        and the sample variance, computed from the 24 observed hours with sample mean $\hat{\mu}_X = 0.25$, is given by

        $$
        \begin{aligned}
        \hat{\sigma}_X^2 &= \frac{1}{n-1} \sum_{i=1}^{n} \left(X_i - \hat{\mu}_X \right)^2 \\
        &= \frac{1}{23} \left[ 19 \cdot (0 - 0.25)^2 + 4 \cdot (1 - 0.25)^2 + 1 \cdot (2 - 0.25)^2 \right] \\
        &= \frac{6.5}{23} \approx 0.2826
        \end{aligned}
        $$

        The variance and sample variance are not the same. The variance is a fixed property of the true probability distribution, while the sample variance is computed from one particular sample of 24 hours. By the law of large numbers, we should expect the sample variance to get close to the true variance as the amount of data we collect grows, that is, as $n \to \infty$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Using the probability row of the emails per hour table in Section 2.2 of the Lecture 2 notebook, separately compute $\mathbb{P}(X \ge 1)$ and $\mathbb{P}(1 \le X \le 3)$. Then explain how each of your two answers could instead be obtained from the cumulative probability row of the same table.
        """,
        r"""
        The opposite of the event $X \ge 1$ is $X = 0$, so

        $$
        \mathbb{P}(X \ge 1) = 1 - \mathbb{P}(X = 0) = 1 - 0.80 = 0.20.
        $$

        Summing the probabilities of the outcomes 1, 2, and 3 gives

        $$
        \mathbb{P}(1 \le X \le 3) = 0.10 + 0.06 + 0.03 = 0.19.
        $$

        Both answers can also be read from the cumulative row. The first is one minus the cumulative probability at 0, that is, $1 - 0.80 = 0.20$, because the cumulative probability at 0 collects exactly the outcomes excluded from $X \ge 1$. The second is the cumulative probability at 3 minus the cumulative probability at 0, that is, $0.99 - 0.80 = 0.19$, because the subtraction removes exactly the outcomes at or below 0.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Open Section 2.4 of the Lecture 2 notebook on the course website. Choose the coin flip from the dropdown menu and set the number of coin flips to 10. Click "Draw new sample" five times, and each time write down the final value of the running sample mean. Then set the number of flips to 5,000 and record five final values in the same way. Compare your two lists. Around what value do the numbers in each list cluster, and which list is more spread out? Name the result from Lecture 2 that explains the difference.
        """,
        r"""
        Exact values will differ from student to student, which is the point of recording them. A typical list at 10 flips might read 0.3, 0.6, 0.4, 0.7, 0.5, while at 5,000 flips all five values land within roughly 0.02 of 0.5. Both lists cluster around 0.5, the true expected value of a fair coin flip, but the 10 flip list is far more spread out. This is the law of large numbers. The sample mean gets close to the true expected value when the sample is large, so with 5,000 flips every draw of the simulation produces a sample mean close to 0.5, while with 10 flips chance still has a large effect.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** In two or three sentences, describe the differences between joint, marginal, and conditional probability distributions.
        """,
        r"""
        A joint distribution describes how two or more variables behave together, assigning probabilities to every combination of their outcomes. A marginal distribution looks at just one variable by "summing over" the other variables, showing how likely each outcome is for that single variable regardless of the other variables' outcomes. A conditional distribution tells you how one variable behaves once you restrict attention to cases where another variable takes a specific value.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **6.** Using the joint probability distribution table in Section 3.1 of the Lecture 3 notebook, apply Bayes' rule to find the probability that $X = x_2$ if $Y = y_2$.
        """,
        r"""
        This question asks us to compute $\mathbb{P}(X = x_2 \vert Y = y_2)$. Bayes' rule gives

        $$
        \begin{aligned}
        \mathbb{P}(X = x_2 \vert Y = y_2) &= \frac{\mathbb{P}(X = x_2, Y = y_2)}{\mathbb{P}(Y = y_2)} \\
        &= \frac{0.10}{0.20 + 0.10 + 0.25} \\
        &= \frac{2}{11}
        \end{aligned}
        $$

        where the joint probability in the numerator comes straight from the table, and the marginal probability in the denominator sums the $y_2$ row of the table over the three values of $X$. You can check the denominator against the Marginal of Y table in the same section, which lists $\mathbb{P}(Y = y_2) = 0.55$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **7.** Consider rolling a fair *three-sided* die twice.<sup><a id="fnref1" href="#fn1">1</a></sup> Define $X$ as the value of the first roll and $Y$ as the value of the sum of the two rolls.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(a)** Write out the joint probability distribution table of $X$ and $Y$.
        """,
        r"""
        | | $X = 1$ | $X = 2$ | $X = 3$ |
        |:---:|:---:|:---:|:---:|
        | $Y = 2$ | $\frac{1}{9}$ | 0 | 0 |
        | $Y = 3$ | $\frac{1}{9}$ | $\frac{1}{9}$ | 0 |
        | $Y = 4$ | $\frac{1}{9}$ | $\frac{1}{9}$ | $\frac{1}{9}$ |
        | $Y = 5$ | 0 | $\frac{1}{9}$ | $\frac{1}{9}$ |
        | $Y = 6$ | 0 | 0 | $\frac{1}{9}$ |

        One way to think about writing this table is to ask, given $X = 1$, how many ways are there to make $Y = 2, 3, 4, 5$, or $6$? Write these down in the table (there is either 1 or 0 ways for each). Do this for $X = 2$ and $X = 3$. Then divide each total by the number of possible outcome combinations, which in this case is $9$.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(b)** Use the joint probability distribution table to compute the marginal probability that the sum of the two rolls is 4 (put formally, compute $\mathbb{P}(Y = 4)$).
        """,
        r"""
        To compute the marginal probability that $Y = 4$, we sum the joint probabilities over all values of $X$,

        $$
        \begin{aligned}
        \mathbb{P}(Y = 4) &= \mathbb{P}(Y = 4, X = 1) + \mathbb{P}(Y = 4, X = 2) + \mathbb{P}(Y = 4, X = 3) \\
        &= \frac{1}{9} + \frac{1}{9} + \frac{1}{9} \\
        &= \frac{1}{3}.
        \end{aligned}
        $$
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(c)** Use the joint probability distribution table to compute the probability that the sum of the two rolls is 3 conditional on the first roll being 1 (put formally, compute $\mathbb{P}(Y = 3 \vert X = 1)$).
        """,
        r"""
        To compute the conditional probability that $Y = 3$ given that $X = 1$, we apply Bayes' rule,

        $$
        \begin{aligned}
        \mathbb{P}(Y = 3 \vert X = 1) &= \frac{\mathbb{P}(Y = 3, X = 1)}{\mathbb{P}(X = 1)} \\
        &= \frac{\frac{1}{9}}{\frac{1}{9} + \frac{1}{9} + \frac{1}{9}} \\
        &= \frac{1}{3}
        \end{aligned}
        $$

        where the marginal probability $\mathbb{P}(X = 1)$ sums the $X = 1$ column of the table over the three sums that a first roll of 1 can produce. The answer also matches direct reasoning. Given a first roll of 1, the sum is 3 exactly when the second roll is 2, which happens with probability $\frac{1}{3}$.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(d)** Use the joint probability distribution table to compute the probability that the first roll is 2 conditional on the sum of the two rolls being 3 (put formally, compute $\mathbb{P}(X = 2 \vert Y = 3)$).
        """,
        r"""
        To compute the conditional probability that $X = 2$ given that $Y = 3$, we again apply Bayes' rule,

        $$
        \begin{aligned}
        \mathbb{P}(X = 2 \vert Y = 3) &= \frac{\mathbb{P}(X = 2, Y = 3)}{\mathbb{P}(Y = 3)} \\
        &= \frac{\frac{1}{9}}{\frac{1}{9} + \frac{1}{9}} \\
        &= \frac{1}{2}
        \end{aligned}
        $$
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(e)** The two rolls are independent, and each roll has expected value $2$ and variance $\frac{2}{3}$. Use Rule 4 in Section 3.5 of the Lecture 3 notebook to compute $\text{cov}(X, Y)$, and then compute $\text{corr}(X, Y)$. *Hint. Write $Y = X + X_2$, where $X_2$ is the value of the second roll.*
        """,
        r"""
        Writing $Y = X + X_2$ and applying Rule 4, the covariance splits into two pieces,

        $$
        \text{cov}(X, Y) = \text{cov}(X, X + X_2) = \text{cov}(X, X) + \text{cov}(X, X_2) = \text{var}(X) + 0 = \frac{2}{3},
        $$

        where $\text{cov}(X, X_2) = 0$ because the two rolls are independent, and the covariance of a variable with itself is its variance. For the correlation we also need the variance of $Y$. The rolls are i.i.d., so $\text{var}(Y) = \text{var}(X + X_2) = \text{var}(X) + \text{var}(X_2) = \frac{2}{3} + \frac{2}{3} = \frac{4}{3}$. Then

        $$
        \text{corr}(X, Y) = \frac{\text{cov}(X, Y)}{\sigma_X \, \sigma_Y} = \frac{\frac{2}{3}}{\sqrt{\frac{2}{3}}\sqrt{\frac{4}{3}}} = \frac{1}{\sqrt{2}} \approx 0.71.
        $$

        The first roll and the sum are strongly positively correlated, which makes sense because the first roll is one of the two ingredients of the sum.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **8.** Assume two random variables $Z$ and $W$ are independent. Three implications of independence are

        - $\mathbb{P}(W = w \vert Z = z) = \mathbb{P}(W = w)$
        - $\mathbb{P}(W = w , Z = z) = \mathbb{P}(W = w) \cdot \mathbb{P}(Z = z)$
        - $\text{corr}(Z,W) = \text{cov}(Z,W) = 0$

        Describe and explain these implications in one or two sentences each. Then spray the interactive scatter plot in Section 3.2 of the Lecture 3 notebook with a cloud of points whose sample correlation is near zero even though the two coordinates clearly depend on each other, using a shape other than the arch and trough mentioned in Section 3.3. Briefly describe your shape in words and explain why it shows dependence without correlation.
        """,
        r"""
        - $\mathbb{P}(W=w \mid Z=z)=\mathbb{P}(W=w)$. Knowing the value of $Z$ does not change the probability of $W$, so information about $Z$ is irrelevant for predicting $W$.
        - $\mathbb{P}(W=w, Z=z)=\mathbb{P}(W=w)\,\cdot\mathbb{P}(Z=z)$. The probability that both $w$ and $z$ occur equals the product of their marginal probabilities because independent variables do not influence each other.
        - $\operatorname{cov}(Z,W)=0$ and $\operatorname{corr}(Z,W)=0$. Independent variables do not systematically move together, so the average product of deviations is zero, and both the covariance and the correlation are zero. Remember from Section 3.3 of Lecture 3 that the converse need not hold, since zero correlation does not imply independence.

        For the spray plot, one shape that works is a ring of points, and an X made of two crossing diagonal strips works as well. The sample correlation reported under the plot stays near zero because the shape has no overall linear tilt. The coordinates are still dependent, since knowing a point's horizontal position narrows its height to the top or bottom of the ring, or to one of the two strips of the X.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **9.** Let $X$ be the emails per hour random variable from Lecture 2, with $\mu_X = 0.35$ and $\sigma_X^2 = 0.6475$. Suppose that handling each email takes 2 minutes and that an hourly system check adds another 3 minutes, so the minutes of email work in an hour is the random variable $Y = 3 + 2X$. Use Rules 1 and 3 in Section 3.5 of the Lecture 3 notebook to compute $\mathbb{E}[Y]$ and $\text{var}(Y)$.
        """,
        r"""
        By Rule 1, the linearity of the expected value,

        $$
        \mathbb{E}[Y] = \mathbb{E}[3 + 2X] = 3 + 2\,\mathbb{E}[X] = 3 + 2 \cdot 0.35 = 3.7 \text{ minutes.}
        $$

        By Rule 3, adding the constant 3 does not change the variance, and multiplying by 2 multiplies the variance by $2^2$,

        $$
        \text{var}(Y) = \text{var}(3 + 2X) = 2^2 \cdot \sigma_X^2 = 4 \cdot 0.6475 = 2.59.
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **10.** Using the rules in Section 3.5 of the Lecture 3 notebook, prove the following two properties of the sample mean of the random variable $X$, denoted $\hat{\mu}_X$ and defined in Section 2.3 of the Lecture 2 notebook. You should assume the draws of $X$ are independently and identically distributed.

        - The expected value of the sample mean equals the expected value of $X$ (denoted $\mu_X$).
        - The standard deviation of the sample mean (denoted $\sigma_{\hat{\mu}_X}$) equals $\frac{\sigma_{X}}{\sqrt{n}}$. Recall that $\sigma_{X}$ is the standard deviation of the random variable $X$ itself, and that $n$ is the number of draws of $X$ used to compute the sample mean.

        The second derivation appears at the end of Section 3.5. Write both proofs before checking your work against the notebook.
        """,
        r"""
        For the first result we have that

        $$
        \begin{aligned}
        \mathbb{E}[\hat{\mu}_X] &= \mathbb{E}\left[\frac{1}{n} \sum_{i=1}^{n} X_i\right] \\
        &= \frac{1}{n}\mathbb{E}\left[ \sum_{i=1}^{n} X_i \right] && \text{By Rule 1, since } \tfrac{1}{n} \text{ is a constant.} \\
        &= \frac{1}{n}\mathbb{E}\left[ X_1 + X_2 + \dots + X_n \right] && \text{Just writing out the summation fully.} \\
        &= \frac{1}{n}\left(\mathbb{E}\left[ X_1\right] + \mathbb{E}\left[X_2\right] + \dots + \mathbb{E}\left[X_n\right]\right) && \text{By Rule 2.} \\
        &= \frac{1}{n}\left(\mu_X + \mu_X + \dots + \mu_X\right) && \text{The expected value of each } X_i \text{ is } \mu_X. \\
        &= \frac{1}{n}\left(n \cdot \mu_X\right) && \text{There were } n \text{ values of } \mu_X. \\
        &= \mu_X
        \end{aligned}
        $$

        For the second result, we will start with the identity

        $$
        \sigma_{\hat{\mu}_X} = \sqrt{\text{var}(\hat{\mu}_X)}.
        $$

        We therefore first compute $\text{var}(\hat{\mu}_X)$ using Rules 3 and 5,

        $$
        \begin{aligned}
        \text{var}(\hat{\mu}_X) &= \text{var}\left(\frac{1}{n} \sum_{i=1}^{n} X_i \right) \\
        &= \frac{1}{n^2}\text{var}\left(\sum_{i=1}^{n} X_i\right) && \text{By Rule 3, since } \tfrac{1}{n} \text{ is a constant.} \\
        &= \frac{1}{n^2} \cdot n \sigma^2_X && \text{By Rule 5, since the } X_i \text{ are i.i.d.} \\
        &= \frac{\sigma^2_X}{n}
        \end{aligned}
        $$

        Taking the square root of the last result, we obtain $\sigma_{\hat{\mu}_X} = \frac{\sigma_X}{\sqrt{n}}$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob2"></a>
    ## Problem 2. Central limit theorem

    We are going to consider the random event of rolling a fair die with six sides (a fair die has $\frac{1}{6}$ probability of landing on each of its six possible outcomes).
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Assume we roll the die twice. Consider the random variable equal to the average of the two rolls. Write out the probability distribution table of this random variable.
        """,
        r"""
        I would recommend constructing this probability distribution in three steps.

        **(a)** List the sum of all possible die rolls.

        | First roll $\backslash$ Second roll | 1 | 2 | 3 | 4 | 5 | 6 |
        |:---:|:---:|:---:|:---:|:---:|:---:|:---:|
        | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
        | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
        | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
        | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
        | 6 | 7 | 8 | 9 | 10 | 11 | 12 |

        **(b)** List all possible average values by dividing the sums by two.

        | First roll $\backslash$ Second roll | 1 | 2 | 3 | 4 | 5 | 6 |
        |:---:|:---:|:---:|:---:|:---:|:---:|:---:|
        | 1 | 1 | $\frac{3}{2}$ | 2 | $\frac{5}{2}$ | 3 | $\frac{7}{2}$ |
        | 2 | $\frac{3}{2}$ | 2 | $\frac{5}{2}$ | 3 | $\frac{7}{2}$ | 4 |
        | 3 | 2 | $\frac{5}{2}$ | 3 | $\frac{7}{2}$ | 4 | $\frac{9}{2}$ |
        | 4 | $\frac{5}{2}$ | 3 | $\frac{7}{2}$ | 4 | $\frac{9}{2}$ | 5 |
        | 5 | 3 | $\frac{7}{2}$ | 4 | $\frac{9}{2}$ | 5 | $\frac{11}{2}$ |
        | 6 | $\frac{7}{2}$ | 4 | $\frac{9}{2}$ | 5 | $\frac{11}{2}$ | 6 |

        **(c)** Compute the probability each distinct average value appears, noting that there are 36 elements in the table. This yields the final probability distribution.

        | Possible outcomes ($x_i$) | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 | 5 | 5.5 | 6 |
        |:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
        | Probability of outcomes ($p_i$) | $\frac{1}{36}$ | $\frac{2}{36}$ | $\frac{3}{36}$ | $\frac{4}{36}$ | $\frac{5}{36}$ | $\frac{6}{36}$ | $\frac{5}{36}$ | $\frac{4}{36}$ | $\frac{3}{36}$ | $\frac{2}{36}$ | $\frac{1}{36}$ |
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Compute the expected value of this random variable.
        """,
        r"""
        Use the probability distribution in part 1 and the formula for expected value to obtain

        $$
        \begin{aligned}
        \mathbb{E}[\hat{\mu}_X] &= \sum_{i=1}^{K} x_i \cdot p_i \\
        &= 1 \cdot \frac{1}{36} + 1.5 \cdot \frac{2}{36} + 2 \cdot \frac{3}{36} + 2.5 \cdot \frac{4}{36} + 3 \cdot \frac{5}{36} + 3.5 \cdot \frac{6}{36} \\
        &\quad + 4 \cdot \frac{5}{36} + 4.5 \cdot \frac{4}{36} + 5 \cdot \frac{3}{36} + 5.5 \cdot \frac{2}{36} + 6 \cdot \frac{1}{36} \\
        &= 3.5
        \end{aligned}
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Compute the variance of this random variable.
        """,
        r"""
        Use the same probability distribution from part 1 and the formula for variance to obtain

        $$
        \begin{aligned}
        \text{var}(\hat{\mu}_X) &= \sum_{i=1}^{K} (x_i - \mu_X)^2 \cdot p_i \\
        &= (1 - 3.5)^2 \cdot \frac{1}{36} + (1.5 - 3.5)^2 \cdot \frac{2}{36} + (2 - 3.5)^2 \cdot \frac{3}{36} + (2.5 - 3.5)^2 \cdot \frac{4}{36} \\
        &\quad + (3 - 3.5)^2 \cdot \frac{5}{36} + (3.5 - 3.5)^2 \cdot \frac{6}{36} + (4 - 3.5)^2 \cdot \frac{5}{36} + (4.5 - 3.5)^2 \cdot \frac{4}{36} \\
        &\quad + (5 - 3.5)^2 \cdot \frac{3}{36} + (5.5 - 3.5)^2 \cdot \frac{2}{36} + (6 - 3.5)^2 \cdot \frac{1}{36} \\
        &= 1.4583
        \end{aligned}
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** How would we expect our answers to change in parts 2 and 3 (roughly speaking, no need to recompute the actual values) if we were considering the random variable equal to the average of three rolls instead of two?
        """,
        r"""
        We are computing the expected value and variance of a *sample mean*. Recall from Section 2.5 of Lecture 2 that for any sample size $n$, the expected value of the sample mean equals the expected value of a single roll,

        $$
        \mathbb{E}[\hat{\mu}_X] = \mu_X = 3.5.
        $$

        This does not depend on how many rolls are averaged, so the expected value is the same for the average of three rolls as for the average of two rolls.

        For the variance, recall that $\text{var}(\hat{\mu}_X) = \sigma_X^2 / n$. The variance of a single roll, $\sigma_X^2$, is unchanged, but increasing $n$ from $2$ to $3$ makes $\text{var}(\hat{\mu}_X)$ smaller. In words, the average of three rolls is less variable (more concentrated around $3.5$) than the average of two rolls.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **5.** Open Section 2.7 of the Lecture 2 notebook on the course website. The interactive simulation at the end of the section draws many samples from a random variable you choose, computes the sample mean of each sample, and plots the distribution of those sample means next to the distribution of the random variable itself. Choose the exponential random variable from the dropdown menu. Play with the two sliders and the "Draw new samples" button until you understand what the simulation is designed to show. Then answer the following questions.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(a)** Keep the number of sample means fixed at 1,000 and increase the sample size behind each mean. Try $n = 1$, then a handful of values up to $n = 100$. What happens to the spread and the shape of the distribution of sample means in the right chart? Explain the change in spread using the formula for $\sigma_{\hat{\mu}_X}$ from Section 2.5, noting that the exponential random variable in the simulation has $\sigma_X = 1$.
        """,
        r"""
        At $n = 1$ each "sample mean" is just a single draw, so the right chart looks like the skewed exponential distribution in the left chart. As $n$ increases, two things happen. The distribution of sample means becomes tighter around the true mean of 1, because the standard deviation of the sample mean is $\sigma_{\hat{\mu}_X} = \sigma_X / \sqrt{n} = 1/\sqrt{n}$, which falls from 1 at $n = 1$ to $0.1$ at $n = 100$. And its shape becomes more and more bell shaped, matching the normal curve drawn on top, even though the underlying random variable is strongly skewed.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(b)** Now keep the sample size fixed at $n = 30$ and change the number of sample means. Try 200, 1,000, and 3,000. Does the underlying distribution of the sample mean change? What does change in the chart?
        """,
        r"""
        Fixing $n$ fixes the true sampling distribution of the sample mean, so the underlying distribution does not change at all. What changes is how well the histogram approximates that distribution. With only 200 simulated sample means the histogram is ragged and jumps around from one click of "Draw new samples" to the next. With 3,000 simulated means it becomes smooth and stable, and it hugs the normal curve closely.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(c)** Explain why your answers to parts (a) and (b) differ. How do these differences relate to the central limit theorem?
        """,
        r"""
        Parts (a) and (b) change two different things.

        Part (a) changes the number of observations per sample, which changes the *true sampling distribution* of the sample mean. If $\hat{\mu}_X$ is the mean of $n$ i.i.d. draws from a population with mean $\mu_X$ and variance $\sigma_X^2$, then

        $$
        \mathbb{E}[\hat{\mu}_X] = \mu_X \qquad \text{and} \qquad \text{var}(\hat{\mu}_X) = \frac{\sigma_X^2}{n},
        $$

        so increasing $n$ makes the sampling distribution tighter. The central limit theorem adds that, for large $n$, the shape of the distribution of $\hat{\mu}_X$ is approximately normal even when the underlying random variable is not,

        $$
        \hat{\mu}_X \approx \mathcal{N}\!\left(\mu_X, \tfrac{\sigma_X^2}{n}\right).
        $$

        Part (b) changes the number of simulated samples, which does *not* change the sampling distribution at all. It only changes how well the simulation approximates it. With few simulated sample means the histogram is rough, and with many it settles down to the underlying distribution.

        So the central limit theorem is about what happens as the number of observations per sample grows, while increasing the number of samples just gives a better picture of whatever the sampling distribution is.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **6.** Describe what it means to "standardize" a normal random variable. In your answer, write the formula you would use to create a standardized normal variable. Section 2.6 of the Lecture 2 notebook may be a useful reference, and its interactive figure lets you see standardization in action.
        """,
        r"""
        To standardize a normal random variable means to shift it to have mean 0 and rescale it to have standard deviation 1. If $X \sim \mathcal{N}(\mu,\sigma^2)$, then the standardized variable is

        $$
        Z = \frac{X-\mu}{\sigma},
        $$

        and $Z \sim \mathcal{N}(0,1)$. Subtracting $\mu$ moves the center of the distribution to zero, and dividing by $\sigma$ stretches or shrinks it so its variance is one.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **7.** Scores on a national exam are distributed $X \sim \mathcal{N}(500, 100^2)$.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(a)** A student scores 630. Compute the student's standardized score.
        """,
        r"""
        Applying the standardization formula,

        $$
        Z = \frac{X - \mu}{\sigma} = \frac{630 - 500}{100} = 1.3,
        $$

        so the student scored 1.3 standard deviations above the mean.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(b)** What is the probability that a randomly chosen student scores between 304 and 696? *Hint. Section 2.6 of the Lecture 2 notebook states a fact about the area under the normal curve that answers this without any further computation.*
        """,
        r"""
        The interval runs from $500 - 196$ to $500 + 196$, that is, from $\mu - 1.96\sigma$ to $\mu + 1.96\sigma$. Section 2.6 of Lecture 2 states that the area under the normal curve between these two points is exactly 0.95, so the probability is 0.95.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob3"></a>
    ## Problem 3. Prepare for the Tuesday quiz

    Review your problem set answers, your class notes, and the lecture notebooks on the course website. The quiz on Tuesday will draw on the material covered by this problem set and the corresponding lecture notebooks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** A fair three-sided die has $\frac{1}{3}$ probability of landing on each of its three possible outcomes: 1, 2, and 3. <a href="#fnref1" title="Back to text">&#8617;</a></span>
    """)
    return


if __name__ == "__main__":
    app.run()
