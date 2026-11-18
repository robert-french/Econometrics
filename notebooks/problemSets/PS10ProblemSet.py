# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.24.0"
__preliminary__ = False
__description__ = "Problem Set 10 with worked solutions beneath each question."
app = marimo.App(
    app_title="Problem Set 10: External Validity and Describing Data in Stata",
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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Problem Set 10</a></h1>'
                '</div>'
            ),
            mo.md(
                r"""
                **External Validity and Describing Data in Stata**

                - [Problem 0. Prepare before attempting the problems](#prob0)
                - [Problem 1. External validity](#prob1)
                - [Problem 2. Loading and describing the data in Stata](#prob2)
                - [Problem 3. Comparing groups in Stata](#prob3)
                - [Problem 4. Relationships between variables in Stata](#prob4)
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
    # Problem Set 10: External Validity and Describing Data in Stata

    Due at the beginning of class on Tuesday, November 17.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob0"></a>
    ## Problem 0. Prepare before attempting the problems

    Before attempting the problems below, spend around 3 hours reviewing Section 14.3 of the Lecture 14 notebook and the three Stata tutorials on the course website, together with your class notes. Work through the interactive figures as you read, and keep a list of anything you find difficult. Discuss the items on that list with your classmates, bring them to the peer mentors, or come to office hours. The problems below will go much more smoothly after this review.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob1"></a>
    ## Problem 1. External validity

    A study uses a random sample of public elementary schools in California in 1999 to estimate the causal effect of class size on students' test scores. Suppose the study is internally valid, so that its estimate is the true causal effect for the schools it studied. A school board in Texas is deciding in 2026 whether to reduce class sizes in its high schools, and it wants to use the study's estimate.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** In two or three sentences, explain the difference between internal validity and external validity in your own words.
        """,
        r"""
        Internal validity asks whether a study gives the right answer for the population it actually studied, meaning that its estimate is unbiased and consistent for the causal effect there. External validity asks whether that answer carries over to the population we care about, which may differ in place, time, or type of person. A study can therefore be internally valid and still tell us little about the population of interest.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Identify the population studied and the population of interest in the school board's case. Then give one specific reason the causal effect of class size might differ between the two populations.
        """,
        r"""
        The population studied is California public elementary schools in 1999, while the population of interest is Texas public high schools in 2026. One reason the effect might differ is that small classes may matter more for young children, who need individual attention to learn to read, than for high school students, who work more independently. Other reasons, such as changes in teaching methods and technology since 1999, are equally acceptable.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Section 14.3 of the Lecture 14 notebook describes replication as a way to assess external validity. In one or two sentences, say what pattern of results across other studies would make the board more confident in using the estimate to inform its decision to reduce class sizes.
        """,
        r"""
        The board should be more confident if studies of the same question in other populations, such as high schools, other states, and more recent years, find effects of similar size. Consistent results across settings are much stronger grounds for applying the estimate to Texas high schools today than any single study.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Now consider a regression used for prediction rather than for a causal effect. Why might a regression model that fits the original sample well perform poorly when predicting outcomes for new observations? Explain how can we assess its ability to predict new observations using the methods introduced in Section 14.3 of the Lecture 14 notebook.
        """,
        r"""
        A flexible model can fit the randomness in the original sample as well as the underlying relationship, which is called overfitting. That randomness is not repeated in new observations, so the model can predict them poorly even though it fits the original sample well. To assess this, we can set aside a hold-out sample, estimate the model on the remaining training sample, and measure its prediction errors on the hold-out sample. Cross-validation repeats this across $k$ folds and averages the results, so that the measure does not depend on any single split.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** Open the interactive chart in Section 14.3 of the Lecture 14 notebook. Leave the "Training share of the sample (%)" slider at 70 and do not press the "New random split" button. Set the "Polynomial degree (fitted to training data only)" slider to 2 and then to 20, and record the training SER and the hold-out SER shown above the two bars for each degree. Explain in a sentence or two why the hold-out SER, rather than the training SER, is the better guide to how well each model will predict new workers.
        """,
        r"""
        At degree 2, the training SER is about &#36;2.80 and the hold-out SER is about &#36;3.38. At degree 20, the training SER falls to about &#36;2.48 while the hold-out SER jumps to about &#36;66.24. The training SER always improves as the model becomes more flexible, because the model is judged on the same observations it was fitted to. The hold-out workers were not used to estimate the model, so their prediction errors show how it performs on new observations, which is what we want to know.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob2"></a>
    ## Problem 2. Loading and describing the data in Stata

    The remaining problems use the course dataset you downloaded in Stata Tutorial 1. Open the do-file you built in the tutorials, make sure the `use` line loads the dataset, and add a comment line (using as asterisk) marking the start of this problem set. For each question below, add the command to your do-file, run the file, and copy the numbers you need from the Results window.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Run the command `describe`. How many observations are in the dataset, and what does each observation represent? List the variables in the dataset.
        """,
        r"""
        The dataset has 200 observations, each representing one person. It contains five variables: `id`, `age` (age in years), `sex`, `education` (highest level of education, with four categories), and `earnings` (annual earnings in dollars).
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Run the command `summarize age earnings`. Report the mean, standard deviation, minimum, and maximum of each variable.
        """,
        r"""
        Age has a mean of $41.3$ years, a standard deviation of $9.7$ years, a minimum of $25$, and a maximum of $57$. Annual earnings have a mean of &#36;65,430, a standard deviation of &#36;15,741, a minimum of &#36;26,000, and a maximum of &#36;109,000.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Run `summarize earnings, detail`. Report the median and the 25th and 75th percentiles of earnings. Is the median above or below the mean you reported in part 2? What does this tell you about the shape of the earnings distribution?
        """,
        r"""
        The median is &#36;64,000, with a 25th percentile of &#36;52,000 and a 75th percentile of &#36;77,000. Because the median is below the mean of &#36;65,430, the distribution is skewed to the right, with a few high earners pulling the mean above the typical person's earnings. The gap is only about &#36;1,400, however, so the skew is mild.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob3"></a>
    ## Problem 3. Comparing groups in Stata
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Run `tabulate education` and `tabulate sex`. Report the share of the sample in each education category and the share that is female.
        """,
        r"""
        By education, $29.5$ percent of the sample has a high school diploma ($59$ people), $21.0$ percent has some college ($42$), $25.5$ percent has a bachelor's degree ($51$), and $24.0$ percent has a graduate degree ($48$). Women make up $94$ of the $200$ people, or $47.0$ percent of the sample.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Run the command

        ```stata
        tabstat earnings, by(education) statistics(mean sd n)
        ```

        and report the mean earnings in each education category. By how much do mean earnings differ between people with a bachelor's degree and people with only a high school diploma?
        """,
        r"""
        Mean annual earnings are &#36;50,254 for high school, &#36;58,929 for some college, &#36;70,569 for a bachelor's degree, and &#36;84,313 for a graduate degree. People with a bachelor's degree therefore earn $70{,}569 - 50{,}254 =$ &#36;20,315 more on average than people with only a high school diploma. Small differences from rounding are fine.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Run the command

        ```stata
        tabstat earnings, by(sex) statistics(mean sd n)
        ```

        and report the mean earnings of women and of men and the difference between them.
        """,
        r"""
        Women earn &#36;63,234 on average and men earn &#36;67,377, so men earn about &#36;4,143 more per year on average in this sample.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Stata can restrict a command to part of the sample with an `if` qualifier placed before the comma. For example,

        ```stata
        tabstat earnings if age < 40, by(sex) statistics(mean n)
        ```

        reports the means for people under 40 only. Run this command, and then run it again with `if age >= 40` in place of `if age < 40`. Report the mean earnings of women and men in each age group, and compute the difference between men and women in each group. Is the difference larger among younger or older workers?
        """,
        r"""
        Among people under $40$, women earn &#36;61,523 on average ($44$ people) and men earn &#36;63,646 ($48$), a difference of &#36;2,123. Among people $40$ and older, women earn &#36;64,740 ($50$) and men earn &#36;70,466 ($58$), a difference of &#36;5,726. The difference between men and women is therefore larger among older workers.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob4"></a>
    ## Problem 4. Relationships between variables in Stata
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Run `correlate earnings education age`. Report the correlation between earnings and education and the correlation between earnings and age. Which variable has the stronger relationship with earnings?
        """,
        r"""
        The correlation between earnings and education is $0.82$, while the correlation between earnings and age is only $0.17$, so education has the much stronger relationship with earnings.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Run the command

        ```stata
        regress earnings education, vce(robust)
        ```

        and write down the fitted line. Interpret the slope coefficient in a sentence, recalling that `education` takes the values 1 through 4 for the four education categories. Re-run the same command without the option `vce(robust)`. Do your standard errors change? Type in the command window `help robust` to see what the option does.
        """,
        r"""
        The fitted line is $\widehat{\text{earnings}} = 37{,}903 + 11{,}281 \times \text{education}$. Moving up one education category, for example from a high school diploma to some college, is associated with annual earnings that are about &#36;11,281 higher on average. Without `vce(robust)`, the coefficients are unchanged but the standard error on `education` falls slightly, from about $565$ to about $550$, because the option replaces the conventional standard errors with heteroskedasticity-robust ones.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** From the same output, report the R-squared and the `Root MSE`. Note that Stata's `Root MSE` is the same thing as the standard error of the regression (SER) from the lecture notebooks. Interpret each in a sentence.
        """,
        r"""
        The R-squared is $0.68$, so differences in education account for about $68$ percent of the variation in earnings in the sample. The `Root MSE`, which is the SER, is $8{,}932$, so a typical person's actual earnings are about &#36;8,932 away from the earnings the fitted line predicts for their education category.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Use the fitted line to predict the earnings of a person with a graduate degree, for whom `education` equals 4. Compare your prediction with the mean earnings of people with a graduate degree from Problem 3, part 2. Why are the two numbers not identical?
        """,
        r"""
        The prediction is $37{,}903 + 11{,}281 \times 4 =$ &#36;83,027, compared with a mean of &#36;84,313 for people with a graduate degree. The two differ because the regression forces the four predicted values to lie on a straight line, with the same step of &#36;11,281 between neighboring categories, whereas the four group means do not rise in exactly equal steps. The line is the best straight-line approximation to the four means, not a perfect match to each one.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** Run the command

        ```stata
        regress earnings age, vce(robust)
        ```

        and report the slope coefficient, its standard error, its t-statistic, and its p-value. Is the slope statistically significant at the 5 percent level? Report the R-squared and compare it with the R-squared from part 3.
        """,
        r"""
        The slope on age is about &#36;270 per year of age, with a robust standard error of about &#36;120, a t-statistic of $2.26$, and a p-value of $0.025$. Since the p-value is below $0.05$, the slope is statistically significant at the 5 percent level. The R-squared is only $0.03$, however, compared with $0.68$ for education. Age is therefore related to earnings, but it explains far less of the variation in earnings than education does.
        """,
    )
    return


if __name__ == "__main__":
    app.run()
