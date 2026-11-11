# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.24.0"
__preliminary__ = False
__description__ = "Problem Set 9 with worked solutions beneath each question."
app = marimo.App(
    app_title="Problem Set 9: Interactions and Threats to Internal Validity",
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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Problem Set 9</a></h1>'
                '</div>'
            ),
            mo.md(
                r"""
                **Interactions and Threats to Internal Validity**

                - [Problem 0. Prepare before attempting the problems](#prob0)
                - [Problem 1. Interacting two binary variables](#prob1)
                - [Problem 2. Interacting a binary and a continuous variable](#prob2)
                - [Problem 3. Interacting two continuous variables](#prob3)
                - [Problem 4. Threats to internal validity](#prob4)
                - [Problem 5. Identifying the threat](#prob5)
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
    # Problem Set 9: Interactions and Threats to Internal Validity

    Due at the beginning of class on Tuesday, November 10.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob0"></a>
    ## Problem 0. Prepare before attempting the problems

    Before attempting the problems below, spend around 3 hours reviewing the Lecture 13 notebook and Sections 14.1 and 14.2 of the Lecture 14 notebook on the course website, together with your class notes. Work through the interactive figures as you read, and keep a list of anything you find difficult. Discuss the items on that list with your classmates, bring them to the peer mentors, or come to office hours. The problems below will go much more smoothly after this review.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob1"></a>
    ## Problem 1. Interacting two binary variables

    A researcher studies the annual earnings of accountants, measured in thousands of dollars. Let $X_1 = 1$ if the accountant holds a professional certification and $0$ otherwise, and let $X_2 = 1$ if the accountant works at a large firm and $0$ otherwise. The researcher estimates

    $$
    \widehat{\text{Earnings}} = 42 + 6\,X_1 + 9\,X_2 + 4\,(X_1 \times X_2).
    $$
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Compute the predicted earnings for each of the four groups of accountants: uncertified at a small firm, certified at a small firm, uncertified at a large firm, and certified at a large firm. Present your answers in a table like the one in Section 13.1 of the Lecture 13 notebook.
        """,
        r"""
        In thousands of dollars per year,

        | | Small firm ($X_2 = 0$) | Large firm ($X_2 = 1$) |
        |:---|:---:|:---:|
        | Uncertified ($X_1 = 0$) | $42$ | $42 + 9 = 51$ |
        | Certified ($X_1 = 1$) | $42 + 6 = 48$ | $42 + 6 + 9 + 4 = 61$ |
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Using your table, compute the predicted earnings premium for a certification at small firms and at large firms. Which coefficient equals the difference between the two premiums? In a sentence, say whether the certification is associated with a larger earnings premium at small firms or at large firms, and by how much.
        """,
        r"""
        The premium is $48 - 42 = 6$ at small firms and $61 - 51 = 10$ at large firms. The difference, $10 - 6 = 4$, is the interaction coefficient $\hat{\beta}_3$. The certification is associated with a larger premium at large firms, by 4 thousand dollars a year.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** A classmate drops the interaction term and instead estimates $\text{Earnings} = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + u$. Using this regression, write the predicted earnings for each of the four groups of accountants in terms of $\hat{\beta}_0$, $\hat{\beta}_1$, and $\hat{\beta}_2$, and then write the certification premium at small firms and at large firms. What does this regression force to be true about the two premiums?
        """,
        r"""
        The four predicted values are $\hat{\beta}_0$, $\hat{\beta}_0 + \hat{\beta}_1$, $\hat{\beta}_0 + \hat{\beta}_2$, and $\hat{\beta}_0 + \hat{\beta}_1 + \hat{\beta}_2$. The certification premium is $\hat{\beta}_1$ at small firms and also $\hat{\beta}_1$ at large firms, so the regression forces the two premiums to be equal.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** A second classmate reads $\hat{\beta}_1 = 6$ as the causal effect of earning the certification for accountants at small firms. Write down the first least squares assumption for this regression and explain in words what it requires of certified and uncertified accountants at small firms. Then give one reason the assumption might fail.
        """,
        r"""
        The assumption is $\mathbb{E}[u \mid X_1, X_2] = 0$. Among accountants at small firms, those with and without the certification must not differ systematically in the omitted determinants of earnings. It could fail if more able accountants are more likely to earn the certification and would earn more without it, which would bias $\hat{\beta}_1$ upward.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob2"></a>
    ## Problem 2. Interacting a binary and a continuous variable

    Section 13.2 of the Lecture 13 notebook regresses hourly wages on years of experience for the survey of 300 workers, with $D = 1$ for workers in STEM jobs. The interactive chart has two checkboxes, "Include the STEM indicator as a main effect in the regression" and "Interact the STEM indicator with Experience in the regression."
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Check both boxes so that the chart estimates specification (c). Record the fitted line for non-STEM workers and the fitted line for STEM workers from the caption below the chart. Then use the two lines to compute the predicted wage difference between a STEM and a non-STEM worker at 0, 20, and 40 years of experience.
        """,
        r"""
        The non-STEM line is $\widehat{\text{Wage}} = 12.98 + 0.24\,\text{Experience}$ and the STEM line is $\widehat{\text{Wage}} = 17.12 + 0.37\,\text{Experience}$. Their difference is $4.14 + 0.13 \times \text{Experience}$, which is &#36;4.14 at 0 years, &#36;6.74 at 20 years, and &#36;9.34 at 40 years. The caption reports &#36;9.24 at 40 years because it uses the unrounded slope difference.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Now uncheck the interaction box and leave the main-effect box checked, which estimates specification (a). Record the two fitted lines. The STEM line now sits a fixed amount above the non-STEM line. Explain why this fixed amount is larger than the intercept difference you found in specification (c).
        """,
        r"""
        The lines are $12.13 + 0.29\,\text{Experience}$ for non-STEM workers and $18.86 + 0.29\,\text{Experience}$ for STEM workers, so the gap is &#36;6.73 at every level of experience. In specification (c) the gap grows from &#36;4.14 at 0 years to about &#36;9.24 at 40 years. Specification (a) forces a single gap, so OLS picks the value that fits best on average, which lies between the small gap for inexperienced workers and the large gap for experienced workers.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Now check only the interaction box, which estimates specification (b). Record the common intercept and the two slopes. Use them to compute the predicted STEM wage difference at 10 and at 40 years of experience, and compare each with the corresponding difference from specification (c). At which experience levels does specification (b) understate the difference, and at which does it overstate it?
        """,
        r"""
        Both lines start at &#36;14.32, with slopes of $0.19$ for non-STEM workers and $0.48$ for STEM workers, so the difference is $0.29 \times \text{Experience}$, which is &#36;2.90 at 10 years and &#36;11.60 at 40 years. Specification (c) gives &#36;5.44 and about &#36;9.24. Specification (b) understates the gap for inexperienced workers, because it forces the gap to be zero at zero experience, and overstates it for experienced workers, because the whole gap must come through a steeper STEM slope.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** In specification (c), suppose the interaction coefficient is $\hat{\beta}_3 = 0.13$ with a standard error of $0.03$. Test $H_0\!: \beta_3 = 0$ against $H_1\!: \beta_3 \neq 0$ at the 1 percent significance level. If you reject the null hypothesis, do the STEM and non-STEM lines have different slopes, different intercepts, or both? Explain your answer.
        """,
        r"""
        $t = 0.13 / 0.03 \approx 4.3$, so the two-sided $p$-value is below $0.001$ and we reject $H_0$ at the 1 percent level. Since $\beta_3$ is the difference between the two slopes, the lines have different slopes. The test says nothing about the intercepts, which are compared by testing $\beta_2$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob3"></a>
    ## Problem 3. Interacting two continuous variables

    A researcher studies the annual sales of retail stores, measured in thousands of dollars. Let $A$ be a store's annual advertising spending in thousands of dollars and let $S$ be its floor space in hundreds of square feet. The researcher estimates

    $$
    \widehat{\text{Sales}} = 120 + 3.0\,A + 2.0\,S + 0.25\,(A \times S).
    $$
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Compute the change in predicted sales associated with one additional thousand dollars of advertising for a store with 10 hundred square feet of floor space, and for a store with 30 hundred square feet. Explain why the two answers differ.
        """,
        r"""
        Holding floor space fixed, one more unit of $A$ changes predicted sales by $3.0 + 0.25\,S$, which is $5.5$ thousand dollars at $S = 10$ and $10.5$ at $S = 30$. The answers differ because the interaction term makes the advertising slope depend on floor space.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Section 13.3 of the Lecture 13 notebook explains that an interaction coefficient can be read from the point of view of either variable. In part 1 you found that, holding floor space fixed, one more thousand dollars of advertising changes predicted sales by $3.0 + 0.25\,S$. From this point of view, $0.25$ is the amount by which the advertising slope rises with each additional hundred square feet of floor space. Now take the point of view of floor space. Write the change in predicted sales associated with one more hundred square feet of floor space, holding advertising fixed. Use it to give the second interpretation of $0.25$, and then say in a sentence what the positive sign of $0.25$ means for how advertising and floor space are related to sales.
        """,
        r"""
        Holding advertising fixed, one more hundred square feet changes predicted sales by $2.0 + 0.25\,A$ thousand dollars, so each additional thousand dollars of advertising raises the floor-space slope by $0.25$. The positive sign means that each variable's association with sales is larger when the other variable is larger.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Compute predicted sales for a store with $A = 10$ and $S = 20$, and for a store with $A = 20$ and $S = 20$.
        """,
        r"""
        For $A = 10$ and $S = 20$, predicted sales are $120 + 30 + 40 + 50 = 240$ thousand dollars. For $A = 20$ and $S = 20$, they are $120 + 60 + 40 + 100 = 320$ thousand dollars.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** A classmate says that $\hat{\beta}_1 = 3.0$ is "the effect of advertising on sales." Explain precisely what $3.0$ measures in this regression and why it is not a useful summary of the association between advertising and sales for the stores in the sample.
        """,
        r"""
        Since the advertising slope is $3.0 + 0.25\,S$, the coefficient $3.0$ is the slope for a store with $S = 0$, which no real store has. For stores in the sample the slope is larger, for example $8.0$ at $S = 20$, so $3.0$ understates the association. The classmate should report the slope at a typical floor space.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob4"></a>
    ## Problem 4. Threats to internal validity

    A researcher wants to estimate the causal effect of irrigation on crop yields. She surveys farms in a region, asking each farmer how many inches of irrigation water they applied over the growing season ($X$), and later records each farm's yield in bushels per acre ($Y$). She estimates $Y = \beta_0 + \beta_1 X + u$.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Name one factor in the error term that is likely to cause omitted variable bias. Say whether it is higher or lower when $X$ is higher, whether it raises or lowers $Y$, and therefore whether it biases $\hat{\beta}_1$ upward or downward.
        """,
        r"""
        Many answers work. For example, rainfall. Farms with more rain irrigate less, so rainfall is lower when $X$ is higher, and rainfall raises $Y$. A factor that is lower when $X$ is higher and raises $Y$ biases $\hat{\beta}_1$ downward.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Suppose the true relationship between irrigation and yields is hump-shaped: yields rise with water up to a point and then fall for farms that apply so much water that their fields become waterlogged. Explain why fitting a straight line violates the first least squares assumption, and say what type of regression from Lecture 11 the researcher should estimate instead.
        """,
        r"""
        A straight line predicts yields that are too low near the peak and too high at very low and very high irrigation, so the error is positive at moderate values of $X$ and negative at the extremes. The average error therefore depends on $X$, violating $\mathbb{E}[u \mid X] = 0$. The researcher should add irrigation squared, a quadratic regression.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Farmers report their water use from memory, so suppose reported irrigation equals true irrigation plus a purely random error. Suppose the true effect is $\beta_1 = 5$ bushels per acre for each additional inch of water, the variance of true irrigation across farms is $16$, and the variance of the reporting error is $4$. Use the attenuation formula in Section 14.2 of the Lecture 14 notebook to compute the value that $\hat{\beta}_1$ converges to. Explain in a sentence why random reporting error pulls the estimate in this direction.
        """,
        r"""
        The attenuation formula gives

        $$
        \hat{\beta}_1 \overset{p}{\to} \beta_1 \frac{\text{var}(X)}{\text{var}(X) + \text{var}(\nu)} = 5 \times \frac{16}{16 + 4} = 4
        $$

        bushels per acre per inch. Random reporting error spreads reported irrigation out horizontally without changing yields, which flattens the fitted line and pulls the estimate toward zero.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Open the interactive chart in Section 14.2 of the Lecture 14 notebook that follows the discussion of measurement error. Set the slider labelled "Standard deviation of the reporting error for experience" to 4, 8, and 12 in turn. For each setting, record the slope using reported experience and the attenuation bias factor reported in the caption. Explain, with reference to the attenuation bias formula, why the estimated slope becomes flatter as the measurement error increases.
        """,
        r"""
        The caption reports $\text{var}(X) = 141$ for true experience.

        | Slider | Slope with reported experience | Attenuation bias factor |
        |:---:|:---:|:---:|
        | 4 | $0.27$ | $0.90$ |
        | 8 | $0.22$ | $0.69$ |
        | 12 | $0.14$ | $0.49$ |

        The slope converges to $\beta_1 \times \text{var}(X) / (\text{var}(X) + \text{var}(\nu))$. Since $\text{var}(X) = 141$ is fixed, a larger reporting error raises $\text{var}(\nu)$ in the denominator and shrinks the factor, from $141/(141+16) = 0.90$ to $141/(141+144) = 0.49$. The estimated slope is the true slope times this factor, so it moves toward zero.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** Open the next interactive chart in Section 14.2, which asks "Which data go missing?" Select each of the four options in turn and record the number of workers in the sample, the slope, and the standard error of the slope from the caption. Explain why the standard error rises most under "Data missing based on X," and why only "Data missing based on Y" changes the slope by much.
        """,
        r"""
        | Option | Workers | Slope | Standard error |
        |:---|:---:|:---:|:---:|
        | Keep the full sample | 400 | $0.30$ | $0.014$ |
        | Data missing at random | 195 | $0.32$ | $0.021$ |
        | Data missing based on X | 175 | $0.32$ | $0.036$ |
        | Data missing based on Y | 200 | $0.14$ | $0.018$ |

        The standard error falls with the spread of $X$ as well as with the number of workers. Dropping workers with more than 20 years of experience removes all the high values of experience, so the line is pinned down less tightly than when a similar number of surveys is lost at random. Only selection based on $Y$ changes the slope. Dropping high earners leaves experienced workers in the sample only when their wages are unusually low, which creates a negative relationship between $X$ and $u$ and flattens the line.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **6.** Return to the irrigation study. In each scenario below, say whether $\hat{\beta}_1$ is biased and explain why. First, the survey is mailed to every farm, but about a third of the forms are lost in the mail at random. Second, the survey is handed out only at an awards dinner for the farms whose yields were in the top half of the region.
        """,
        r"""
        In the first scenario $\hat{\beta}_1$ is not biased. The lost forms are unrelated to irrigation or yields, so the remaining farms are typical, although the standard error is larger. In the second scenario the sample is selected based on $Y$. Farms that irrigated little appear only if their yields were unusually high, so the error is positive at low $X$, $X$ and $u$ are negatively related, and $\hat{\beta}_1$ is biased downward.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **7.** Suppose that farmers whose crops are struggling for reasons unrelated to water, such as pests or disease, respond by irrigating more heavily. Explain why this is a case of simultaneous causality, and whether this biases $\hat{\beta}_1$ upward or downward.
        """,
        r"""
        Irrigation affects yields, and the condition of the crop affects irrigation, so causality runs in both directions. A farm with pests has a low value of $u$ and irrigates more, so $X$ is high when $u$ is low. $X$ and $u$ are negatively related and $\hat{\beta}_1$ is biased downward.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob5"></a>
    ## Problem 5. Identifying the threat

    For each study below, name the threat to internal validity that it illustrates, say whether $\hat{\beta}_1$ is likely to be biased and in which direction if you can tell, and suggest one way to address the problem.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** A researcher regresses a city's crime rate on the number of police officers it employs, using a cross-section of cities and no control variables.
        """,
        r"""
        Simultaneous causality. Cities with more crime hire more police, so $X$ and $u$ are positively related and $\hat{\beta}_1$ is biased upward. One fix is to use changes in police numbers that are not responses to crime, as in Lectures 18 and 19, or to control for the city characteristics that drive both.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** A researcher fits a straight line to data on wages and experience, even though the Lecture 11 notebook showed that wages rise quickly early in a career and flatten later on.
        """,
        r"""
        Misspecification of the functional form. The straight line misses the curvature, so the error is related to experience and $\mathbb{E}[u \mid X] \neq 0$. The fix is a more flexible form, such as adding experience squared or using the logarithm of experience.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** A researcher regresses firms' patent counts on their research spending, where spending is taken from a survey in which managers answer from memory and make random errors in their responses.
        """,
        r"""
        Classical measurement error in $X$. Random reporting error makes reported spending more spread out than true spending, so $\hat{\beta}_1$ is biased toward zero. The fix is better data, for example spending from audited financial statements.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** A researcher regresses annual earnings on years of education using a survey from which about a quarter of the questionnaires were lost in the mail at random.
        """,
        r"""
        Sample selection unrelated to $X$ or $Y$. The lost questionnaires are no different from the rest, so $\hat{\beta}_1$ is not biased. The only cost is a larger standard error, which more data would reduce.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** A researcher estimates the effect of years of education on annual earnings using a dataset that includes only people who earn more than &#36;50,000 a year.
        """,
        r"""
        Sample selection based on $Y$. People with little education appear only if their earnings are unusually high, so $X$ and $u$ are negatively related and $\hat{\beta}_1$ is biased downward. The fix is a sample whose inclusion does not depend on earnings, such as a random sample of all adults.
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
