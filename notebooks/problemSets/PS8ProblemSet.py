# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = [
#     "marimo>=0.23.3,<0.25",
# ]
# ///

import marimo

__generated_with = "0.24.0"
__preliminary__ = False
__description__ = "Problem Set 8 with worked solutions beneath each question."
app = marimo.App(
    app_title="Problem Set 8: Polynomials and Logarithms",
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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Problem Set 8</a></h1>'
                '</div>'
            ),
            mo.md(
                r"""
                **Polynomials and Logarithms**

                - [Problem 0. Prepare before attempting the problems](#prob0)
                - [Problem 1. Interpreting a quadratic regression](#prob1)
                - [Problem 2. Wages and experience in the Lecture 11 notebook](#prob2)
                - [Problem 3. Logarithms and percent changes](#prob3)
                - [Problem 4. Three regression models with logarithms](#prob4)
                - [Problem 5. Multiplicative models](#prob5)
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
    # Problem Set 8: Polynomials and Logarithms

    Due at the beginning of class on Tuesday, November 3.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob0"></a>
    ## Problem 0. Prepare before attempting the problems

    Before attempting the problems below, spend around 3 hours reviewing the Lecture 11 notebook and the Lecture 12 notebook on the course website, together with your class notes. Work through the interactive figures as you read, and keep a list of anything you find difficult. Discuss the items on that list with your classmates, bring them to the peer mentors, or come to office hours. The problems below will go much more smoothly after this review.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob1"></a>
    ## Problem 1. Interpreting a quadratic regression

    A city's utility wants to understand how daily electricity use depends on the weather. Using $n = 1{,}460$ days of data, it regresses daily electricity use, $\text{Use}$, measured in millions of kilowatt-hours, on the day's high temperature, $\text{Temp}$, measured in degrees Fahrenheit, and on the square of the day's high temperature. The fitted regression is

    $$
    \widehat{\text{Use}} = 60 - 1.5\,\text{Temp} + 0.015\,\text{Temp}^2.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** A classmate reads the coefficient on $\text{Temp}$ and concludes that a day whose high temperature is one degree warmer uses 1.5 million fewer kilowatt-hours of electricity. Use the fitted regression to compute the change in predicted electricity use when the high temperature rises from 30 to 31 degrees, and again when it rises from 80 to 81 degrees. Then explain what is wrong with your classmate's claim.
        """,
        r"""
        From 30 to 31 degrees, the predicted change is

        $$
        -1.5\,(31 - 30) + 0.015\,(31^2 - 30^2) = -1.5 + 0.015 \times 61 = -1.5 + 0.915 = -0.585,
        $$

        so predicted use falls by about $0.59$ million kilowatt-hours. From 80 to 81 degrees, the predicted change is

        $$
        -1.5 + 0.015\,(81^2 - 80^2) = -1.5 + 0.015 \times 161 = -1.5 + 2.415 = +0.915,
        $$

        so predicted use rises by about $0.92$ million kilowatt-hours. The classmate treats $\hat{\beta}_1 = -1.5$ as the slope of a straight line, but in a quadratic regression a one-degree warmer day changes both $\text{Temp}$ and $\text{Temp}^2$. The change in predicted use depends on $\hat{\beta}_1$, $\hat{\beta}_2$, and the starting temperature. Here it is negative on cool days and positive on hot days, so no single number describes the effect of one more degree.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Compute the predicted change in electricity use when the high temperature rises from 40 to 60 degrees, and the average slope of the fitted curve over that interval. Then do the same for a rise from 60 to 90 degrees. Section 11.3 of the Lecture 11 notebook explains how to compute these quantities. Explain in a sentence why the two average slopes differ so much.
        """,
        r"""
        Predicted use at the three temperatures is

        $$
        \begin{aligned}
        \widehat{\text{Use}}(40) &= 60 - 60 + 24 = 24, \\
        \widehat{\text{Use}}(60) &= 60 - 90 + 54 = 24, \\
        \widehat{\text{Use}}(90) &= 60 - 135 + 121.5 = 46.5.
        \end{aligned}
        $$

        From 40 to 60 degrees the predicted change is $24 - 24 = 0$, so the average slope is $0 / 20 = 0$ million kilowatt-hours per degree. From 60 to 90 degrees the predicted change is $46.5 - 24 = 22.5$, so the average slope is $22.5 / 30 = 0.75$ million kilowatt-hours per degree. The slopes differ because the fitted curve is U-shaped. Between 40 and 60 degrees the curve falls and then rises by the same amount, so the two movements cancel. Between 60 and 90 degrees the curve rises throughout, and more steeply the hotter it gets, so the average slope is large and positive.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Compute predicted electricity use at high temperatures of 30, 50, and 70 degrees. At roughly what temperature does the fitted curve reach its lowest point? Give an economic reason why a U-shaped relationship between temperature and electricity use makes sense.
        """,
        r"""
        Predicted use is $60 - 45 + 13.5 = 28.5$ at 30 degrees, $60 - 75 + 37.5 = 22.5$ at 50 degrees, and $60 - 105 + 73.5 = 28.5$ at 70 degrees. The curve is symmetric around 50 degrees, where predicted use is lowest. (Together with part 2, predicted use is $24$ at both 40 and 60 degrees and $22.5$ at 50 degrees.) The U shape makes sense because people heat their homes on cold days and run air conditioning on hot days. Both activities use electricity, so use is high at either extreme and lowest on mild days when neither is needed.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** The standard error of $\hat{\beta}_2$ is $0.004$. Test the null hypothesis that the population relationship between temperature and electricity use is linear against the alternative that it is nonlinear, at the 1 percent significance level. State the null and alternative hypotheses, compute the $t$-statistic, and state your conclusion.
        """,
        r"""
        If the population relationship is linear, the coefficient on $\text{Temp}^2$ is zero, so we test $H_0\!: \beta_2 = 0$ against $H_1\!: \beta_2 \neq 0$. The $t$-statistic is

        $$
        t = \frac{\hat{\beta}_2 - 0}{\operatorname{SE}(\hat{\beta}_2)} = \frac{0.015}{0.004} = 3.75.
        $$

        A $t$-statistic of $3.75$ lies beyond the largest entry in the normal table, so the two-sided $p$-value is below $0.001$, well under $0.01$, and we reject the null hypothesis at the 1 percent level. There is strong evidence that the relationship is nonlinear. The positive estimate means that the curve bends upward, which matches the U shape found in part 3.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** Does including $\text{Temp}^2$ change the assumption needed to interpret the fitted curve as the causal effect of temperature on electricity use? Write down the first least squares assumption for this regression, explain why it is really an assumption about temperature alone, and give an example of an omitted factor that could violate it.
        """,
        r"""
        No. The quadratic regression is estimated as a multiple regression with two independent variables, so the usual least squares assumptions apply. The first assumption is

        $$
        \mathbb{E}[u \mid \text{Temp}, \text{Temp}^2] = 0.
        $$

        Because $\text{Temp}^2$ is determined entirely by $\text{Temp}$, knowing the temperature tells us the squared temperature as well, so conditioning on both is the same as conditioning on temperature alone. The assumption says that the omitted determinants of electricity use do not vary systematically with the day's high temperature. One factor that could violate it is hours of daylight. Hot days tend to fall in summer, when days are long and less electricity is needed for lighting, so the error would be systematically lower on hot days. Holidays and weekends, when offices close, are other examples if they are related to temperature.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob2"></a>
    ## Problem 2. Wages and experience in the Lecture 11 notebook

    The interactive figures in the Lecture 11 notebook fit polynomial regressions of hourly wages on years of work experience for a sample of 100 workers.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Open the interactive plot in Section 11.3 of the Lecture 11 notebook. Set the "Size of the increase, $\Delta$" slider to 5 and the "Starting experience, Exper" slider to 5, 15, 25, and 30 in turn. For each setting, record the change in the predicted wage and the slope per year reported in the caption below the plot. Describe how the slope changes as the starting level of experience rises, and explain what feature of the fitted quadratic curve produces this pattern.
        """,
        r"""
        With $\Delta = 5$ the caption reports the following values, in dollars.

        | Starting experience | Change in predicted wage | Slope per year |
        |:---:|:---:|:---:|
        | 5 | $+4.46$ | $+0.89$ |
        | 15 | $+2.54$ | $+0.51$ |
        | 25 | $+0.61$ | $+0.12$ |
        | 30 | $-0.35$ | $-0.07$ |

        The slope falls steadily as the starting level of experience rises, from almost 90 cents per year early in a career to slightly negative past 30 years. The fitted curve is a quadratic with a negative coefficient on experience squared, so it is steep at low experience, flattens as experience rises, and reaches a peak near 31 years, after which it turns downward. The same five-year increase therefore buys a smaller raise the later in a career it occurs.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Keep the starting experience at 30 and record the change in the predicted wage and the slope per year for $\Delta = 1$, $\Delta = 5$, and $\Delta = 10$. Why does the slope become more negative as $\Delta$ grows, even though the starting point is the same?
        """,
        r"""
        Starting from 30 years, the caption reports a change of $+0.01$ dollars and a slope of $+0.01$ dollars per year for $\Delta = 1$, a change of $-0.35$ dollars and a slope of $-0.07$ dollars per year for $\Delta = 5$, and a change of $-1.67$ dollars and a slope of $-0.17$ dollars per year for $\Delta = 10$. The slope is the average change per year over the whole interval. Starting at 30 years, the interval begins just before the peak of the curve, where the slope is about zero. A longer interval reaches further past the peak, where the curve falls more and more steeply, so the average over the interval becomes more negative as $\Delta$ grows. In a straight-line regression the slope would not depend on $\Delta$ at all.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Open the interactive plot in Section 11.1 of the Lecture 11 notebook. Set the "Polynomial degree" slider to 1, 2, 3, 5, 10, and 20 in turn, and record the R-squared and the adjusted R-squared reported in the caption for each degree. Describe the pattern in each measure as the degree rises.
        """,
        r"""
        | Degree | R-squared | Adjusted R-squared |
        |:---:|:---:|:---:|
        | 1 | 0.594 | 0.590 |
        | 2 | 0.762 | 0.757 |
        | 3 | 0.762 | 0.754 |
        | 5 | 0.762 | 0.749 |
        | 10 | 0.774 | 0.748 |
        | 20 | 0.779 | 0.724 |

        The R-squared jumps when the degree rises from 1 to 2, then never falls, creeping up from 0.762 to 0.779 by degree 20. The adjusted R-squared also jumps from degree 1 to 2, but then falls steadily with every additional term, from 0.757 at degree 2 to 0.724 at degree 20. The two measures move in opposite directions above degree 2.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Between degrees 2 and 3, the R-squared is unchanged to three decimal places, yet the adjusted R-squared falls. Use the formula for the adjusted R-squared from Section 8.4 of the Lecture 8 notebook,

        $$
        \bar{R}^2 = 1 - \frac{n - 1}{n - k - 1}\cdot\frac{\text{SSR}}{\text{TSS}},
        $$

        to explain why the adjusted R-squared can fall when the sum of squared residuals barely changes. Then explain which polynomial you would expect to predict the wages of a new sample of 100 workers more accurately, the degree-2 or the degree-20 polynomial.
        """,
        r"""
        Adding the cubic term raises $k$ from 2 to 3. The sum of squared residuals barely changes, so $\text{SSR}/\text{TSS}$ is essentially the same, but the factor $(n-1)/(n-k-1)$ rises from $99/97$ to $99/96$. The adjusted R-squared therefore subtracts a slightly larger number from 1 and falls. The formula penalizes each added term, and the penalty wins whenever the added term does not reduce the SSR by enough to offset it. The degree-2 polynomial should predict the new sample more accurately. The degree-20 polynomial achieves its higher in-sample R-squared by bending toward individual observations, which is overfitting. Those wiggles reflect randomness in this particular sample, which will not reappear in a new sample, so they add error rather than information when predicting new wages. The quadratic captures the pattern that is likely to repeat, rapid wage growth early in a career followed by a flattening, without that noise.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob3"></a>
    ## Problem 3. Logarithms and percent changes

    Section 12.2 of the Lecture 12 notebook explains that a change in the logarithm of a variable is approximately its proportional change, and lists three rules that logarithms obey. This problem asks you to work with both ideas.
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** A worker's experience rises from 20 to 21 years. Compute the proportional change in experience and the change in its natural logarithm, and compare the two. Then repeat the comparison for a rise from 20 to 30 years. What do the two comparisons tell you about when the approximation is reliable?
        """,
        r"""
        From 20 to 21 years, the proportional change is $1/20 = 0.05$ and the log change is $\ln(21) - \ln(20) \approx 3.0445 - 2.9957 = 0.0488$, so the two differ by only about $0.001$. From 20 to 30 years, the proportional change is $10/20 = 0.50$ while the log change is $\ln(30) - \ln(20) = \ln(1.5) \approx 0.405$, a gap of almost $0.10$. The approximation is reliable for small changes of a few percent and becomes increasingly inaccurate as the change grows.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** A restaurant's annual revenue rises from &#36;200,000 one year to &#36;300,000 the next, and then falls back to &#36;200,000 the year after. Compute the percent change in revenue in each of the two years, and the change in the natural logarithm of revenue in each of the two years. Explain why the two log changes are equal in magnitude while the two percent changes are not.
        """,
        r"""
        In the first year revenue rises by $100{,}000 / 200{,}000 = 50$ percent. In the second year it falls by $100{,}000 / 300{,}000 \approx 33.3$ percent, because the decrease is measured relative to the higher starting value. The log changes are $\ln(300{,}000) - \ln(200{,}000) = \ln(1.5) \approx +0.405$ in the first year and $\ln(200{,}000) - \ln(300{,}000) = \ln(2/3) \approx -0.405$ in the second. The two log changes are equal in magnitude because $\ln(2/3) = \ln(1/1.5) = -\ln(1.5)$. A log change depends only on the ratio of the new value to the old value, and reversing a change inverts that ratio, which flips the sign of the logarithm without changing its size. A percent change instead depends on which value is in the denominator, so a 50 percent rise is undone by a 33 percent fall.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Open the interactive plot in Section 12.2 of the Lecture 12 notebook. Leave the "Starting experience (years)" slider at 10 and set the "Percent change in experience" slider to $1$, $10$, $25$, $50$, and $100$ in turn. For each setting, record the log change multiplied by 100 and the gap in percentage points reported in the caption. Then set the percent change to $-50$ and record the same two numbers. Describe the pattern in the gap, and explain why the entries for $+100$ and $-50$ are related.
        """,
        r"""
        | Percent change | $100 \times$ log change | Gap (percentage points) |
        |:---:|:---:|:---:|
        | $+1$ | $+1.0$ | $0.0$ |
        | $+10$ | $+9.5$ | $0.5$ |
        | $+25$ | $+22.3$ | $2.7$ |
        | $+50$ | $+40.5$ | $9.5$ |
        | $+100$ | $+69.3$ | $30.7$ |
        | $-50$ | $-69.3$ | $19.3$ |

        The gap is essentially zero for a 1 percent change and grows faster and faster as the change grows, reaching more than 30 percentage points for a doubling. The entries for $+100$ and $-50$ have log changes of the same size and opposite signs, $+0.693$ and $-0.693$. Raising experience by 100 percent doubles it, from 10 to 20 years, and lowering it by 50 percent halves it, from 10 to 5 years. One change is the reverse of the other, so by the rule from part 2 their log changes are $\ln(2)$ and $-\ln(2)$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Now set the percent change to $+25$ and move the "Starting experience (years)" slider from 4 to 20. Does the log change reported in the caption depend on the starting level of experience? Use the rule $\ln(aX) = \ln(a) + \ln(X)$ to explain why or why not.
        """,
        r"""
        No. The log change stays at $+0.223$ for every starting level. A 25 percent increase takes experience from $X$ to $1.25X$, so the log change is $\ln(1.25X) - \ln(X) = \ln(1.25) + \ln(X) - \ln(X) = \ln(1.25) \approx 0.223$. The starting value cancels, so the log change depends only on the proportional change and not on where it starts. This is exactly why logarithms are so useful for describing percent changes.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob4"></a>
    ## Problem 4. Three regression models with logarithms
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Open the interactive plot in Section 12.3 of the Lecture 12 notebook and use the "Specification" drop-down menu to select each of the four options in turn. For each option, record the fitted equation reported in the caption below the plot. Then use the four fitted equations to compute the predicted hourly wage of a worker with 5 years of experience and a worker with 35 years of experience. For the two models in which the dependent variable is $\ln(\text{Wage})$, remember to convert the predicted logarithm back to dollars using the exponential function.
        """,
        r"""
        The captions report

        $$
        \begin{aligned}
        \text{Linear:} \quad & \widehat{\text{Wage}} = 10.8 + 0.78\,\text{Exper}, \\
        \text{Linear-log:} \quad & \widehat{\text{Wage}} = -3.3 + 10.8\,\ln(\text{Exper}), \\
        \text{Log-linear:} \quad & \widehat{\ln(\text{Wage})} = 2.50 + 0.0337\,\text{Exper}, \\
        \text{Log-log:} \quad & \widehat{\ln(\text{Wage})} = 1.78 + 0.51\,\ln(\text{Exper}).
        \end{aligned}
        $$

        Using $\ln(5) \approx 1.609$ and $\ln(35) \approx 3.555$, the predicted wages in dollars are

        | Model | 5 years | 35 years |
        |:---|:---:|:---:|
        | Linear | $10.8 + 0.78 \times 5 = 14.70$ | $10.8 + 0.78 \times 35 = 38.10$ |
        | Linear-log | $-3.3 + 10.8 \times 1.609 = 14.08$ | $-3.3 + 10.8 \times 3.555 = 35.10$ |
        | Log-linear | $e^{2.50 + 0.0337 \times 5} = e^{2.669} = 14.42$ | $e^{2.50 + 0.0337 \times 35} = e^{3.680} = 39.63$ |
        | Log-log | $e^{1.78 + 0.51 \times 1.609} = e^{2.601} = 13.47$ | $e^{1.78 + 0.51 \times 3.555} = e^{3.593} = 36.35$ |

        Small differences from these values are fine, since the captions round the coefficients. The log-linear model predicts the highest wage at 35 years because its fitted curve bends upward, while the linear-log and log-log curves flatten late in a career.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A researcher studies how households' annual spending on food depends on their income. $\text{Food}$ is annual food spending in dollars and $\text{Income}$ is annual household income in thousands of dollars, so a household earning &#36;50,000 has $\text{Income} = 50$. The researcher estimates three regressions,

    $$
    \begin{aligned}
    \widehat{\text{Food}} &= 2{,}400 + 620\,\ln(\text{Income}), \\
    \widehat{\ln(\text{Food})} &= 7.9 + 0.012\,\text{Income}, \\
    \widehat{\ln(\text{Food})} &= 6.8 + 0.35\,\ln(\text{Income}).
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Name each of the three models and interpret its slope coefficient in a sentence, following the pattern in Section 12.3 of the Lecture 12 notebook. Be careful about the units of income.
        """,
        r"""
        The first is a linear-log model. A 1 percent increase in income is associated with about $0.01 \times 620 = 6.20$ dollars more annual food spending. The second is a log-linear model. An increase in income of one unit, which is &#36;1,000, is associated with about $100 \times 0.012 = 1.2$ percent more food spending. The third is a log-log model. A 1 percent increase in income is associated with about a $0.35$ percent increase in food spending, so the elasticity of food spending with respect to income is $0.35$.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Economists have long observed that the share of income spent on food falls as households become richer. Is the log-log estimate consistent with this observation? Explain your answer.
        """,
        r"""
        Yes. The elasticity of $0.35$ is less than 1, so when income rises by 1 percent, food spending rises by only about $0.35$ percent. Spending grows more slowly than income, so the ratio of food spending to income falls as income rises. An elasticity greater than 1 would instead mean the share rises with income.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Use the log-log model to compute predicted food spending for a household with an income of &#36;50,000 and for a household with an income of &#36;100,000. By what percent is the second prediction larger than the first? A classmate argues that doubling income is a 100 percent increase, so the log-log model must predict $0.35 \times 100 = 35$ percent more spending. Explain why the classmate's number is off.
        """,
        r"""
        At $\text{Income} = 50$, $\ln(50) \approx 3.912$, so $\widehat{\ln(\text{Food})} = 6.8 + 0.35 \times 3.912 \approx 8.169$ and predicted spending is $e^{8.169} \approx 3{,}530$ dollars. At $\text{Income} = 100$, $\ln(100) \approx 4.605$, so $\widehat{\ln(\text{Food})} \approx 8.412$ and predicted spending is $e^{8.412} \approx 4{,}500$ dollars. The second prediction is $4{,}500 / 3{,}530 \approx 1.275$ times the first, which is about $27.5$ percent larger. The classmate applies the approximation from Section 12.2 to a very large change. Doubling income raises $\ln(\text{Income})$ by $\ln(2) \approx 0.693$, not by $1$, so $\ln(\text{Food})$ rises by $0.35 \times 0.693 \approx 0.243$ and spending is multiplied by $e^{0.243} \approx 1.275$. The approximation that a log change equals a percent change divided by 100 works for small changes, and a 100 percent change is not small.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **5.** The linear-log regression has an R-squared of $0.41$ and the log-log regression has an R-squared of $0.47$. A classmate concludes that the log-log model fits the data better. Explain what is wrong with this comparison. Which two of the three regressions could be compared using the R-squared?
        """,
        r"""
        The R-squared measures the share of the variation in the dependent variable explained by the regression, and the two regressions have different dependent variables. The linear-log regression explains variation in food spending measured in dollars, while the log-log regression explains variation in the logarithm of food spending. The two R-squared values describe fit on different scales and cannot be ranked against each other. The log-linear and log-log regressions both have $\ln(\text{Food})$ as the dependent variable, so their R-squared values can be compared.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **6.** Suppose the researcher had instead measured income in dollars, so that the new variable equals $1{,}000 \times \text{Income}$. Using the rule $\ln(aX) = \ln(a) + \ln(X)$, explain what happens to the slope coefficient and the intercept of the log-log regression. Then explain what happens to the slope coefficient of the log-linear regression. Which of the two slopes is easier to compare across studies that measure income in different units?
        """,
        r"""
        Write the new variable as $\text{Income}^{*} = 1{,}000 \times \text{Income}$. Then $\ln(\text{Income}) = \ln(\text{Income}^{*}) - \ln(1{,}000)$, so the log-log regression becomes

        $$
        \widehat{\ln(\text{Food})} = 6.8 - 0.35 \ln(1{,}000) + 0.35 \ln(\text{Income}^{*}) \approx 4.38 + 0.35 \ln(\text{Income}^{*}).
        $$

        The slope is unchanged at $0.35$ and only the intercept moves, because rescaling income shifts its logarithm by a constant that the intercept absorbs. In the log-linear regression, a one-dollar increase in income is one thousandth of a &#36;1,000 increase, so the slope becomes $0.012 / 1{,}000 = 0.000012$, while the intercept is unchanged. The log-log slope is easier to compare across studies because it is an elasticity, which compares one percent change with another and does not depend on the units of either variable.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="prob5"></a>
    ## Problem 5. Multiplicative models

    You have collected data for many counties in the US. Let $Y$ be a county's employment rate, measured as the share of residents aged 25 to 65 who are employed, let $X_1$ be the county's minimum wage in dollars, and let $X_2$ be an index of the county's cost of living that ranges from 0 to 1. Consider the economic model

    $$
    Y = \exp\!\left(\beta_0 + \beta_1 X_1 + \beta_2 X_2 + u\right).
    $$
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **1.** Transform this model into an equation that can be estimated by OLS, and name the type of logarithmic regression you obtain.
        """,
        r"""
        Taking the natural logarithm of both sides gives

        $$
        \ln(Y) = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + u,
        $$

        which is linear in the coefficients and can be estimated by OLS. Only the dependent variable is logged, so this is a log-linear regression.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **2.** Suppose you estimate $\hat{\beta}_1 = 0.012$. Interpret this estimate in a sentence. Then explain why this estimate is unlikely to be the causal effect of the minimum wage on employment, naming one omitted factor and the direction in which it would push the estimate.
        """,
        r"""
        A one-dollar increase in the minimum wage is associated with approximately a $100 \times 0.012 = 1.2$ percent higher employment rate, holding the cost of living fixed. A causal interpretation requires that the omitted determinants of employment do not vary systematically with the minimum wage once the cost of living is held fixed. That is unlikely. Counties with strong local economies may both raise their minimum wages, because employers can afford them, and have high employment for reasons unrelated to the minimum wage. This factor raises $Y$ and is higher when $X_1$ is higher, so it pushes $\hat{\beta}_1$ upward and the minimum wage gets credit for employment that is really due to the strong economy.
        """,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now suppose instead that the economic model is

    $$
    Y = \exp(\beta_0 + u)\, X_1^{\beta_1} X_2^{\beta_2}.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **3.** Transform this model into an equation that can be estimated by OLS, showing which rules of logarithms you use. Suppose you estimate $\hat{\beta}_2 = -0.3$. Interpret this estimate in a sentence.
        """,
        r"""
        Taking logarithms turns the product into a sum, using $\ln(aX) = \ln(a) + \ln(X)$, and the powers into multipliers, using $\ln(X^a) = a\ln(X)$,

        $$
        \ln(Y) = \beta_0 + u + \beta_1 \ln(X_1) + \beta_2 \ln(X_2) = \beta_0 + \beta_1 \ln(X_1) + \beta_2 \ln(X_2) + u.
        $$

        This is a log-log regression. The estimate $\hat{\beta}_2 = -0.3$ is an elasticity. A 1 percent increase in the cost of living index is associated with approximately a $0.3$ percent lower employment rate, holding the minimum wage fixed.
        """,
    )
    return


@app.cell(hide_code=True)
def _(qa):
    qa(
        r"""
        **4.** Before estimating the model in part 3, you notice that a few counties have a cost of living index of exactly 0. Explain why this is a problem for the regression in part 3 but not for the regression in part 1.
        """,
        r"""
        The regression in part 3 uses $\ln(X_2)$ as an independent variable, and the logarithm is defined only for positive values, so counties with $X_2 = 0$ have no value for this variable and would drop out of the regression. The regression in part 1 uses $X_2$ itself, without a logarithm, so a value of 0 causes no difficulty. Only the dependent variable is logged there, and employment rates are positive.
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
