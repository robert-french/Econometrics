# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(
    app_title="Stata Tutorial 5: Nonlinear Regression",
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
                3. <a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata3SimpleRegression.html" target="_self">Simple Regression</a>
                4. <a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata4MultipleRegression.html" target="_self">Multiple Regression</a>
                5. **[Nonlinear Regression](#top)**
                    1. [Picking up where we left off](#sec1)
                    1. [Merging a second dataset](#sec2)
                    1. [A quadratic in experience](#sec3)
                    1. [Logarithms](#sec4)
                    1. [Interaction terms](#sec5)
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata4MultipleRegression.html" target="_self">← Stata Tutorial 4</a>'),
            mo.md('<span class="nav-soon">Stata Tutorial 6 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Stata Tutorial 5: Nonlinear Regression
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contents

    5.1 [Picking up where we left off](#sec1)<br>
    5.2 [Merging a second dataset](#sec2)<br>
    5.3 [A quadratic in experience](#sec3)<br>
    5.4 [Logarithms](#sec4)<br>
    5.5 [Interaction terms](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 5.1 Picking up where we left off

    In the fourth tutorial you estimated regressions with several independent variables. This tutorial estimates the nonlinear regressions from Lectures 11, 12, and 13. To do so, we first add some new variables to our data by combining two datasets.

    Open Stata, open `tutorial4.do`—the do-file you saved at the end of Tutorial 4—in the Do-file Editor, and run it from the top with the Execute (do) button so that the dataset loads. Then add a comment line at the bottom to mark the start of this tutorial's code.

    ```stata
    * Stata Tutorial 5
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 5.2 Merging a second dataset

    Researchers often need variables that are stored in different files. Suppose the people in our dataset were surveyed a second time in the same year, 2024, and this follow-up survey recorded each person's work experience, hourly wage, and whether they work in a STEM job. Click the link below to download the follow-up dataset, and move it from your Downloads folder into the same `data` folder as the original dataset.

    <a href="https://robert-french.github.io/Econometrics/econ3300_followup_2024.dta" download><strong>Download the dataset: econ3300_followup_2024.dta</strong></a>

    Before combining the two files, let's see what the new one contains. The `describe using` command describes a dataset stored on your computer without loading it. Add this line to your do-file and rerun it.

    ```stata
    describe using "`dataFolder'/econ3300_followup_2024.dta"
    ```

    The follow-up dataset has 198 observations and five variables: `id`, `year` (the survey year), `experience` (years of work experience), `stem` (equal to 1 if the person works in a STEM job and 0 otherwise), and `wage` (hourly wage in dollars). The `id` variable also appears in our original dataset, and a person has the same `id` in both files. This is what allows Stata to match each person's row in one file with the same person's row in the other.

    The `merge` command combines the two files. Add this line to your do-file and rerun it.

    ```stata
    merge 1:1 id using "`dataFolder'/econ3300_followup_2024.dta"
    ```

    There are three parts to this command.

    - `1:1` tells Stata that this is a one-to-one merge, meaning each `id` appears only once in each file. `1:m` would instead tell Stata that each `id` appears once in the master dataset but can appear many times in the using dataset, and `m:1` would tell Stata the reverse.
    - `id` is the variable Stata uses to match observations across the two files.
    - `using` names the file to merge in. Stata calls the dataset already in memory the *master* dataset and the file named after `using` the *using* dataset.

    After merging, Stata prints a report on how the observations matched.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata5tutorial/stata5_shot1_merge.png" alt="The report Stata prints after the merge command" style="display:block;margin:0.5rem auto 1rem;width:472px;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The report shows that 192 people were matched, meaning they appear in both files. The remaining 14 people were not matched. Eight of them are `from master`. These are people in our original dataset who did not answer the follow-up survey. Six of them are `from using`. These are people who answered the follow-up survey but were not in our original dataset.

    Stata records this information in a new variable called `_merge`, which equals 1 for observations found only in the master dataset, 2 for observations found only in the using dataset, and 3 for matched observations. Unmatched people are still in the dataset, but they have missing values for the variables from the file they were not in. For example, the eight people `from master` have no `wage`.

    For the rest of this tutorial we keep only the people who appear in both files. Add these lines to your do-file and rerun it.

    ```stata
    tabulate _merge
    keep if _merge == 3
    drop _merge
    summarize experience stem wage
    ```

    The `keep if` command keeps the observations that satisfy a condition and deletes the rest, so our dataset now has 192 observations. We then drop `_merge` because we no longer need it. The `summarize` output confirms that the three new variables are in the dataset. Experience ranges from 1 to 41 years, about 33 percent of the sample works in a STEM job, and the average hourly wage is about \$22.97.

    Deleting observations may seem risky, but it only changes the copy of the data in Stata's memory. The files in your `data` folder are untouched, and the `use` command at the top of your do-file reloads the original dataset every time you run it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 5.3 A quadratic in experience

    Let's start by looking at the relationship between hourly wages and experience. Add this line to your do-file and rerun it.

    ```stata
    twoway (scatter wage experience) (qfit wage experience)
    ```

    This is the scatter plot command from Tutorial 2, with `qfit` in place of `lfit`. While `lfit` draws the fitted straight line, `qfit` draws the fitted *quadratic* curve.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata5tutorial/stata5_shot2_qfit.png" alt="Scatter plot of hourly wage against experience with a fitted quadratic curve" style="display:block;margin:0.5rem auto 1rem;width:560px;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The fitted curve rises quickly at low levels of experience and then flattens out, just like the wage and experience relationship in Lecture 11. To estimate the curve with `regress`, we need to include the square of experience as a second independent variable. We could create it with `generate`, but Stata can also construct it inside the `regress` command. Add this line to your do-file and rerun it.

    ```stata
    regress wage c.experience##c.experience, vce(robust)
    ```

    There are two new things to notice in this command.

    - The `#` operator multiplies two variables together, so `c.experience#c.experience` is experience squared. The `c.` prefix tells Stata to treat `experience` as a continuous variable, in the same way that the `i.` prefix from Tutorial 4 tells Stata to treat a variable as categorical.
    - The `##` operator is a shortcut that includes each variable on its own as well as their product. Writing `c.experience##c.experience` is therefore the same as writing `experience c.experience#c.experience`.

    In the coefficient table, the row labelled `experience` reports the coefficient on experience, and the row labelled `c.experience#c.experience` reports the coefficient on experience squared. The table represents the fitted quadratic regression

    $$
    \widehat{\text{wage}} = 14.44 + 0.641 \times \text{experience} - 0.0087 \times \text{experience}^2.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata5tutorial/stata5_shot3_regress_quadratic.png" alt="regress wage c.experience##c.experience output with robust standard errors" style="display:block;margin:0.5rem auto 1rem;width:699px;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As Section 11.2 of the Lecture 11 notebook explains, we cannot interpret the two coefficients separately, because experience cannot change while its square stays fixed. Instead, following Section 11.3, we compute the change in the predicted wage between two levels of experience. Add these lines to your do-file and rerun it.

    ```stata
    display _b[experience] * (6 - 5) + _b[c.experience#c.experience] * (6^2 - 5^2)
    display _b[experience] * (26 - 25) + _b[c.experience#c.experience] * (26^2 - 25^2)
    ```

    After a regression, Stata stores each coefficient estimate under the name `_b[ ]`, with the name of its row in the coefficient table inside the brackets. Using the stored estimates saves us from retyping them and avoids rounding errors. The first line computes the change in the predicted wage when experience rises from 5 to 6 years, which is about \$0.55 per hour. The second line computes the same change when experience rises from 25 to 26 years, which is only about \$0.20 per hour. An additional year of experience is associated with a much larger wage increase early in a career than later on.

    Finally, Section 11.4 of the Lecture 11 notebook shows that we can test whether the relationship is nonlinear with a t-test on the coefficient of the squared term. In the coefficient table, the t-statistic on `c.experience#c.experience` is $-2.71$ and its p-value is 0.007. We therefore reject the null hypothesis that the relationship between wages and experience is linear at the 1% significance level.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 5.4 Logarithms

    Lecture 12 introduced a second way to model a nonlinear relationship, which is to take the logarithm of the dependent variable, the independent variable, or both. Stata's `ln()` function computes the natural logarithm. Add these lines to your do-file and rerun it.

    ```stata
    generate lnWage = ln(wage)
    regress lnWage experience education, vce(robust)
    ```

    This is the *log-linear* model from Section 12.3 of the Lecture 12 notebook, in which the dependent variable is in logarithms and the independent variables are not. In this model, we multiply a coefficient by 100 to read it as a percent change in the dependent variable. The coefficient on `experience` is 0.0154, so an additional year of experience is associated with a wage that is about 1.5 percent higher on average, holding education fixed. The coefficient on `education` is 0.067, so moving up one education category is associated with a wage that is about 6.7 percent higher on average, holding experience fixed.

    We can also take the logarithm of experience. Add these lines to your do-file and rerun it.

    ```stata
    generate lnExperience = ln(experience)
    regress lnWage lnExperience education, vce(robust)
    ```

    With both wages and experience in logarithms, this is the *log-log* model, and the coefficient on `lnExperience` is an elasticity. It equals 0.20, so a 1 percent increase in experience is associated with a wage that is about 0.20 percent higher on average, holding education fixed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5.5 Interaction terms

    Lecture 13 showed how an interaction term allows the relationship between $Y$ and one independent variable to depend on the value of another. Let's ask whether wages rise with experience at a different rate for workers in STEM jobs. As in Section 13.2 of the Lecture 13 notebook, we interact the binary variable `stem` with the continuous variable `experience`. We can again use the `##` operator from Section 5.3. Add this line to your do-file and rerun it.

    ```stata
    regress wage i.stem##c.experience, vce(robust)
    ```

    Here `i.stem##c.experience` includes the indicator `stem`, the continuous variable `experience`, and their product. The product is the interaction term. It equals the person's experience for STEM workers and 0 for everyone else. In the coefficient table, the row labelled `1.stem` reports the coefficient on `stem`, and the row labelled `stem#c.experience` reports the coefficient on the interaction term. The table represents the fitted regression

    $$
    \widehat{\text{wage}} = 16.72 + 3.19 \times \text{stem} + 0.204 \times \text{experience} + 0.143 \times (\text{stem} \times \text{experience}).
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata5tutorial/stata5_shot4_regress_interaction.png" alt="regress wage i.stem##c.experience output with robust standard errors" style="display:block;margin:0.5rem auto 1rem;width:639px;max-width:100%;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This single regression describes two fitted lines, one for each group of workers.

    - For non-STEM workers, `stem` equals 0, so the fitted line is $\widehat{\text{wage}} = 16.72 + 0.204 \times \text{experience}$.
    - For STEM workers, `stem` equals 1, so the intercept is $16.72 + 3.19 = 19.91$ and the slope is $0.204 + 0.143 = 0.347$. The fitted line is $\widehat{\text{wage}} = 19.91 + 0.347 \times \text{experience}$.

    The coefficient on `1.stem` is the difference between the two intercepts, and the coefficient on the interaction term is the difference between the two slopes. An additional year of experience is associated with a wage that is about \$0.20 higher for non-STEM workers and about \$0.35 higher for STEM workers. The t-statistic on the interaction term is 2.70 and its p-value is 0.007, so we reject the null hypothesis that the two groups have the same slope at the 1% significance level.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The lines you added in this tutorial should look something like this, below the lines from the earlier tutorials already in your do-file.

    ```stata
    * Stata Tutorial 5

    describe using "`dataFolder'/econ3300_followup_2024.dta"
    merge 1:1 id using "`dataFolder'/econ3300_followup_2024.dta"
    tabulate _merge
    keep if _merge == 3
    drop _merge
    summarize experience stem wage

    twoway (scatter wage experience) (qfit wage experience)
    regress wage c.experience##c.experience, vce(robust)
    display _b[experience] * (6 - 5) + _b[c.experience#c.experience] * (6^2 - 5^2)
    display _b[experience] * (26 - 25) + _b[c.experience#c.experience] * (26^2 - 25^2)

    generate lnWage = ln(wage)
    regress lnWage experience education, vce(robust)
    generate lnExperience = ln(experience)
    regress lnWage lnExperience education, vce(robust)

    regress wage i.stem##c.experience, vce(robust)
    ```

    Save your do-file under a new name, `tutorial5.do`, using **File > Save As** in the Do-file Editor.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** combining two datasets with `merge 1:1`, master and "
            "using datasets, the `_merge` variable, describing a file on disk "
            "with `describe using`, keeping observations with `keep if`, "
            "fitted quadratic curves with `qfit`, stored coefficient "
            "estimates `_b[ ]`, natural logarithms with `ln()`, log-linear "
            "and log-log regressions, squared and interaction terms with the "
            "`#` and `##` operators, the `c.` prefix for continuous "
            "variables.\n\n"
            "**Habits:** read the merge report before using the merged data; "
            "compute the effect in a quadratic regression as the difference "
            "between two predicted values; multiply a log-linear coefficient "
            "by 100 to read it as a percent change; write out the fitted "
            "line for each group after a regression with an interaction "
            "term."
        ),
        title="Key terms and habits",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/stataTutorials/Stata4MultipleRegression.html" target="_self">← Stata Tutorial 4</a>'),
            mo.md('<span class="nav-soon">Stata Tutorial 6 (coming soon)</span>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
