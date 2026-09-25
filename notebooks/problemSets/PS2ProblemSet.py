# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.23.16"
__preliminary__ = False
__description__ = "Problem Set 2 with worked solutions beneath each question."
app = marimo.App(
    app_title="Problem Set 2: Estimators, Hypothesis Tests, and Confidence Intervals",
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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Problem Set 2</a></h1>'
                '</div>'
            ),
            mo.md(
                r"""
                **Estimators, Hypothesis Tests, and Confidence Intervals**

                - [Problem 0. Prepare before attempting the problems](#prob0)
                - [Problem 1. Estimators](#prob1)
                - [Problem 2. Hypothesis tests and p-values](#prob2)
                - [Problem 3. Confidence intervals in repeated samples](#prob3)
                - [Problem 4. Prepare for the Tuesday quiz](#prob4)
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
    # Problem Set 2: Estimators, Hypothesis Tests, and Confidence Intervals

    Due at the beginning of class on Tuesday, September 22.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob0"></a>
    ## Problem 0. Prepare before attempting the problems

    Before attempting the problems below, spend around 3 hours reviewing the Lecture 4 notebook on the course website, together with your class notes. Work through the interactive figures as you read, and keep a list of anything you find difficult. Discuss the items on that list with your classmates, bring them to the peer mentors, or come to office hours. The problems below will go much more smoothly after this review.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob1"></a>
    ## Problem 1. Estimators
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** In one or two sentences, describe the difference between an estimator and an estimate.
        """,
        r"""
        An estimator is a rule that turns a random sample into a guess about a population quantity, so it is itself a random variable. An estimate is the particular number that rule produces from one specific sample. The estimator is the rule, and the estimate is the realized number.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** In one or two sentences, describe the difference between the bias and the consistency of an estimator.
        """,
        r"""
        Bias describes where an estimator is centered in samples of a given size. It is the difference between the estimator's expected value and the true parameter, $\text{Bias}(\hat{\theta}) = \mathbb{E}[\hat{\theta}] - \theta$, and an unbiased estimator has bias zero. Consistency describes what happens as the sample size grows. A consistent estimator gets closer and closer to the true parameter as $n$ increases, $\hat{\theta} \xrightarrow{p} \theta$. An estimator can have either property without the other.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **3.** Consider the expected value of a fair six-sided die roll, $\mu_X = 3.5$, as the population parameter we want to estimate, and suppose we observe $n$ rolls $X_1, X_2, \ldots, X_n$. For each of the following estimators, state whether it is biased or unbiased, and whether it is consistent or not consistent. Briefly justify each answer.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(a)** The sample mean of the $n$ rolls, $\hat{\mu}_{X}$.
        """,
        r"""
        Unbiased and consistent. From Lecture 2, $\mathbb{E}[\hat{\mu}_X] = \mu_X$, so the bias is zero, and the law of large numbers gives $\hat{\mu}_X \xrightarrow{p} \mu_X$ as $n$ grows.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(b)** The sample mean minus $\frac{2}{n}$, that is, $\hat{\mu}_{X} - \frac{2}{n}$.
        """,
        r"""
        Biased but consistent. Its expected value is $\mathbb{E}[\hat{\mu}_X - \tfrac{2}{n}] = \mu_X - \tfrac{2}{n}$, so the bias is $-\tfrac{2}{n} \neq 0$ in any finite sample. It is consistent because $\hat{\mu}_X \xrightarrow{p} \mu_X$ and the offset $\tfrac{2}{n}$ shrinks to zero as $n$ grows.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(c)** The average of the first two rolls, $\frac{X_1 + X_2}{2}$.
        """,
        r"""
        Unbiased but not consistent. Its expected value is $\tfrac{1}{2}\mu_X + \tfrac{1}{2}\mu_X = \mu_X$, so the bias is zero. It is not consistent because it ignores every roll after the second. Collecting more data does not change the estimator, so it does not get closer to $\mu_X$ as $n$ grows.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(d)** The sample mean multiplied by $\frac{1}{n}$, that is, $\hat{\mu}_{X} \cdot \frac{1}{n}$.
        """,
        r"""
        Biased and not consistent. Its expected value is $\tfrac{\mu_X}{n} \neq \mu_X$, so it is biased. As $n$ grows, the estimator converges to $0$ rather than to $\mu_X$, so it is not consistent.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(e)** The average of the first roll and the sample mean, $\frac{X_1}{2} + \frac{\hat{\mu}_{X}}{2}$.
        """,
        r"""
        Unbiased but not consistent. Its expected value is $\tfrac{1}{2}\mu_X + \tfrac{1}{2}\mu_X = \mu_X$, so the bias is zero. As $n$ grows, $\hat{\mu}_X$ converges to $\mu_X$, but $X_1$ stays random, so the estimator converges to $\tfrac{X_1}{2} + \tfrac{\mu_X}{2}$, which is random and generally different from $\mu_X$. It is therefore not consistent.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(f)** The sample mean of every fifth roll, $\frac{X_1 + X_5 + X_{10} + \cdots}{n/5}$.
        """,
        r"""
        Unbiased and consistent. Every roll it uses has expected value $\mu_X$, so its expected value is $\mu_X$ and the bias is zero. It is a sample mean computed from $n/5$ i.i.d. rolls, and $n/5$ grows without bound as $n$ grows, so by the law of large numbers it converges to $\mu_X$. It simply wastes four fifths of the data along the way.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Which is a more efficient estimator of $\mu_X$ when $n > 2$, the average of the first two rolls, $\frac{X_1 + X_2}{2}$, or the sample mean of all $n$ rolls, $\hat{\mu}_{X}$? Explain your answer using the definition of efficiency in Section 4.3 of the Lecture 4 notebook.
        """,
        r"""
        Both estimators are unbiased, so we compare them by their variances. The average of the first two rolls has variance $\tfrac{\sigma_X^2}{2}$, while the sample mean of all $n$ rolls has variance $\tfrac{\sigma_X^2}{n}$. For $n > 2$ we have $\tfrac{\sigma_X^2}{n} < \tfrac{\sigma_X^2}{2}$, so the sample mean has the smaller variance and is therefore the more efficient estimator.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** Consider again the estimator $\hat{\mu}_{X} - \frac{2}{n}$ from part 3(b). Use the mean squared error decomposition in Section 4.3 of the Lecture 4 notebook to write its mean squared error in terms of $\sigma_X^2$ and $n$. You may find referring to Section 3.5 of Lecture 3 helpful.
        """,
        r"""
        The decomposition says $\text{MSE}(\hat{\theta}) = \text{var}(\hat{\theta}) + \text{Bias}(\hat{\theta})^2$. Subtracting the constant $\tfrac{2}{n}$ does not change the variance, so the variance term is $\text{var}(\hat{\mu}_X) = \tfrac{\sigma_X^2}{n}$. From part 3(b), the bias is $-\tfrac{2}{n}$, so the squared bias term is $\tfrac{4}{n^2}$. Therefore

        $$
        \text{MSE}\left(\hat{\mu}_X - \tfrac{2}{n}\right) = \frac{\sigma_X^2}{n} + \frac{4}{n^2}.
        $$

        Both terms shrink as $n$ grows, which matches the estimator being consistent.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob2"></a>
    ## Problem 2. Hypothesis tests and p-values

    The standard normal table in the appendix of the Lecture 4 notebook will help you approximate the p-values in this problem. You may check your work with the lookup tool beneath the table, but practice reading the table by hand, because you will use the table, not software, during quizzes and exams.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **1.** A sample of workers has an average weekly income of $\hat{\mu}_X^{\text{est}} = 950$ with a standard error of $\text{se}(\hat{\mu}_X) = 25$. Consider the null hypothesis $H_0: \mu_X = 1000$ against the two-sided alternative $H_1: \mu_X \neq 1000$ at the $\alpha = 0.05$ significance level.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(a)** Compute the t-statistic.
        """,
        r"""
        $$
        t^{\text{est}} = \frac{\hat{\mu}_X^{\text{est}} - \mu_{X,0}}{\text{se}(\hat{\mu}_X)} = \frac{950 - 1000}{25} = -2.00.
        $$
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(b)** Approximate the two-sided p-value.
        """,
        r"""
        The table gives $\Phi(-|t^{\text{est}}|) = \Phi(-2.00) \approx 0.0228$, so

        $$
        p = 2\,\Phi(-|t^{\text{est}}|) = 2 \times 0.0228 = 0.0456.
        $$
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(c)** Do you reject $H_0$? State your conclusion in plain English.
        """,
        r"""
        Yes. Since $p \approx 0.046 < \alpha = 0.05$, we reject the null hypothesis that mean weekly income equals &#36;1,000. The sample provides statistically significant evidence at the 5% level that mean weekly income differs from &#36;1,000, and the estimate of &#36;950 suggests it is lower.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **2.** A recent report claims the mean hourly wage for college graduates is &#36;20. You collect a sample of graduates and find $\hat{\mu}_X^{\text{est}} = 21$ with $\text{se}(\hat{\mu}_X) = 0.7$.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(a)** Compute the t-statistic for testing $H_0: \mu_X = 20$ against the two-sided alternative.
        """,
        r"""
        $$
        t^{\text{est}} = \frac{21 - 20}{0.7} \approx 1.43.
        $$
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(b)** Approximate the two-sided p-value.
        """,
        r"""
        The table gives $\Phi(-1.43) \approx 0.0764$, so

        $$
        p = 2 \times 0.0764 = 0.1528.
        $$
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(c)** If $\alpha = 0.10$, do you reject or fail to reject the null hypothesis? What does your decision mean in plain English about average wages?
        """,
        r"""
        Since $p \approx 0.153 > \alpha = 0.10$, we fail to reject $H_0$. The sample does not provide strong enough evidence, at our chosen significance level, that the mean hourly wage of college graduates differs from &#36;20.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(d)** Construct a 90% confidence interval for $\mu_X$. The critical values listed in Section 4.6 of the Lecture 4 notebook will help.
        """,
        r"""
        The critical value for a 90% interval is $c = 1.64$, so

        $$
        \hat{\mu}_X^{\text{est}} \pm c \cdot \text{se}(\hat{\mu}_X) = 21 \pm 1.64 \times 0.7 = 21 \pm 1.148,
        $$

        which gives the interval $(19.85,\ 22.15)$, rounded to two decimals.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(e)** Does $\mu_X = 20$ fall inside your interval? How does this relate to your answer in part (c)?
        """,
        r"""
        Yes, 20 lies inside the 90% confidence interval. That is consistent with part (c). Failing to reject $H_0: \mu_X = 20$ at $\alpha = 0.10$ and finding 20 inside the 90% confidence interval are two ways of expressing the same conclusion, since the confidence interval collects the null values that would not be rejected.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** In words, what does a small p-value imply about your estimate in relation to the null hypothesis?
        """,
        r"""
        A small p-value means that, if the null hypothesis were true, an estimate at least as far from the null value as the one we observed would be very unlikely. Because our estimate would be so surprising under the null, a small p-value counts as evidence against the null hypothesis.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **4.** Suppose you compute a p-value of $0.03$.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(a)** If your chosen significance level is $\alpha = 0.05$, would you reject or fail to reject $H_0$?
        """,
        r"""
        Reject $H_0$, since $0.03 < 0.05$.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(b)** If instead you had chosen $\alpha = 0.01$, how would your decision change?
        """,
        r"""
        Fail to reject $H_0$, since $0.03 > 0.01$.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(c)** Explain in your own words what this example shows about how the choice of $\alpha$ affects hypothesis testing, and why the same p-value can lead to different conclusions.
        """,
        r"""
        The p-value measures the strength of the evidence against the null, while $\alpha$ is the standard of evidence we choose before running the test. We reject when the p-value falls below $\alpha$, so a stricter standard (a smaller $\alpha$) requires stronger evidence. The same $p = 0.03$ clears the $\alpha = 0.05$ bar but not the $\alpha = 0.01$ bar, which is why the identical data can lead to different decisions under different significance levels.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **5.** Open Section 4.5 of the Lecture 4 notebook on the course website. The interactive plot tests the null hypothesis $H_0: \mu_X = 20$, and its readout beneath the chart reports whether the test rejects this null hypothesis. Interact with the plot until you understand how it works and what it shows. Then, set $\hat{\mu}_X^{\text{est}} = 22$, $\text{se}(\hat{\mu}_X) = 1$, and $\alpha = 0.05$, and note the shaded area and the test decision. Now raise the standard error to $2$ and leave everything else unchanged.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(a)** Write down the t-statistic and the two-sided p-value for both settings (i.e., when $\text{se}(\hat{\mu}_X) = 1$ and when $\text{se}(\hat{\mu}_X) = 2$). These values are shown beneath the interactive plot, but take a minute to check your answers using the standard normal table in the appendix.
        """,
        r"""
        With $\text{se}(\hat{\mu}_X) = 1$, the t-statistic is $t^{\text{est}} = \tfrac{22 - 20}{1} = 2.00$, and the table gives $p = 2\,\Phi(-2.00) = 2 \times 0.0228 = 0.0456$. With $\text{se}(\hat{\mu}_X) = 2$, the t-statistic is $t^{\text{est}} = \tfrac{22 - 20}{2} = 1.00$, and the table gives $p = 2\,\Phi(-1.00) = 2 \times 0.1587 = 0.3174$.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **(b)** The estimate sits exactly &#36;2 above the null value in both settings, yet the test rejects the null hypothesis in one setting but not the other. Explain intuitively why this happens in one or two sentences.
        """,
        r"""
        The t-statistic measures the gap between the estimate and the null value in standard-error units. Doubling the standard error halves the t-statistic, so the same &#36;2 gap counts as only one standard error of evidence instead of two. A gap that is large relative to sampling uncertainty is convincing, while the same gap is unconvincing when the estimate is imprecise.
        """,
        indent=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob3"></a>
    ## Problem 3. Confidence intervals in repeated samples

    Open Section 4.6 of the Lecture 4 notebook on the course website. The interactive plot draws one hundred samples from a population with a true mean of &#36;20, builds a confidence interval from each sample, and highlights in yellow the intervals that do not include the true mean.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Keep the confidence level at 95% and the sample size at $n = 30$. Click "Draw new samples" five times, and each time write down how many of the one hundred intervals are yellow.
        """,
        r"""
        Exact counts vary from click to click, which is the point of recording them. A typical list looks like 4, 6, 5, 3, 7. Around five intervals out of one hundred miss the true mean on a typical draw, though any one draw can produce a few more or a few less.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Now switch the confidence level to 90% and record five counts in the same way. Compare your two lists, and explain the difference using what a confidence level means.
        """,
        r"""
        The counts roughly double, with a typical list looking like 9, 11, 8, 12, 10. A 95% confidence level means the interval-building procedure captures the true mean in about 95% of repeated samples, so about 5 in 100 intervals exclude the true mean. A 90% level uses a smaller critical value, which produces narrower intervals that miss more often, about 10 in 100. The confidence level describes the long-run success rate of the procedure, not any single interval.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob4"></a>
    ## Problem 4. Prepare for the Tuesday quiz

    Review your problem set answers, your class notes, and the lecture notebooks on the course website. The quiz on Tuesday will draw on the material covered by this problem set and the corresponding lecture notebooks.
    """)
    return


if __name__ == "__main__":
    app.run()
