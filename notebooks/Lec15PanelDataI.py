# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "numpy",
#     "pandas",
#     "altair",
#     "scipy",
#     "pyarrow",
# ]
# ///

import marimo

__generated_with = "0.23.16"
__preliminary__ = True
app = marimo.App(
    app_title="Lecture 15: Panel Data I: Entity Fixed Effects and Before/After Comparisons",
    css_file="marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt

    return alt, mo, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: block; margin-bottom: 1.5em;">Course home</a>'),
            mo.md("# [Lecture 15](#top)"),
            mo.md("Panel Data I: Entity Fixed Effects and Before/After Comparisons"),
            mo.nav_menu(
                {
                    "#sec1": "1. What a fixed effect is",
                    "#sec2": "2. Panel data",
                    "#sec3": "3. Before-and-after comparisons",
                    "#sec4": "4. Entity fixed effects",
                    "#sec5": "5. What fixed effects cannot fix",
                },
                orientation="vertical",
            ),
        ],
        width="260px",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec14InternalAndExternalValidity.html" target="_self">← Lecture 14</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec16PanelDataII.html" target="_self">Lecture 16 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 15: Panel Data I: Entity Fixed Effects and Before/After Comparisons
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Same-page (#fragment) links must stay plain markdown links with no inline
    # style and no styled wrapper; see the note in Lec14.
    mo.md(r"""
    ## Contents

    [1. What a fixed effect is](#sec1)<br>
    [2. Panel data](#sec2)<br>
    [3. Before-and-after comparisons](#sec3)<br>
    [4. Entity fixed effects](#sec4)<br>
    [5. What fixed effects cannot fix](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. What a fixed effect is

    Lecture 14 listed omitted variable bias first among the threats to internal validity, and its solutions were limited. We can control for an omitted variable if we can measure it, or acknowledge the bias if we cannot. This lecture develops a tool that removes an entire class of omitted variables without measuring any of them. The tool works whenever the observations in our data belong to groups, such as students in courses or yearly observations on states.

    We begin with a regression whose independent variables are a set of binary variables,

    $$
    Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_K X_K + u,
    $$

    where each of $X_1, \dots, X_K$ equals either 0 or 1. The binary variables are *mutually exclusive* if only one of them can equal 1 for each observation. For example, $X_k$ might equal 1 if $k$ is the individual's home state. Every individual has exactly one home state, so exactly one of the fifty state indicators equals 1 and the other forty-nine equal 0.

    Interpreting the coefficients works the same way as for the single binary regressor in Lecture 5:

    * $\hat{\beta}_0$ is the predicted value of $Y$ for observations with all $X_k = 0$.
    * $\hat{\beta}_0 + \hat{\beta}_k$ is the predicted value of $Y$ for observations with $X_k = 1$.

    Because the binary variables are mutually exclusive, we can write the regression more compactly as

    $$
    Y = \beta_0 + \alpha_k + u,
    \qquad \text{where} \qquad
    \alpha_k = \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_K X_K.
    $$

    The term $\alpha_k$ is called a *fixed effect*. For each observation, $\alpha_k$ takes the single value $\beta_k$ belonging to that observation's group: a fixed effect gives each group its own intercept.

    To see why these group intercepts matter, consider regressing students' final course grades on their weekly study hours, with a fixed effect for each course:

    $$
    \text{Grade} = \alpha_{\text{course}} + \beta \, \text{Study Hours} + u.
    $$

    The chart below shows simulated grades for 240 students across four economics courses. Within every course, studying more raises grades: each colored line has a slope of about 2 grade points per weekly hour. But the courses differ in difficulty. Econometrics students study the most and would earn the lowest grades for any fixed amount of study, while Intro students study the least and would earn the highest. The slider controls how strongly course difficulty is tied to study hours. The black line pools all 240 students into one regression with a single intercept.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # Simulated grades for the course fixed-effects demo: 60 students in each
    # of four courses, mean weekly study hours 3/6/9/11, within-course slope 2.
    # The difficulty penalty is applied in the chart cell from the slider, so
    # dragging the slider shifts intercepts of the same fixed draws and never
    # resamples. Fixed seeds for reproducibility.
    _mu = np.array([3.0, 6.0, 9.0, 11.0])
    _rng = np.random.default_rng(1233)
    _hours, _course = [], []
    for _j, _m in enumerate(_mu):
        _hours.append(np.clip(_rng.normal(_m, 0.9, 60), 0.5, 14.5))
        _course.append(np.full(60, _j))
    gr_hours = np.concatenate(_hours)
    gr_course = np.concatenate(_course)
    gr_noise = np.random.default_rng(1234).normal(0.0, 3.0, len(gr_hours))
    gr_mu = _mu
    gr_names = ["Intro Econ", "Computational Econ", "Micro", "Econometrics"]
    return gr_course, gr_hours, gr_mu, gr_names, gr_noise


@app.cell(hide_code=True)
def _(mo):
    gr_c = mo.ui.slider(
        start=0.0, stop=3.0, step=0.25, value=2.0,
        label="Strength of the course-difficulty confounder",
        show_value=True,
    )
    gr_c
    return (gr_c,)


@app.cell(hide_code=True)
def _(alt, gr_c, gr_course, gr_hours, gr_mu, gr_names, gr_noise, mo, np, pd):
    _c = float(gr_c.value)
    _mubar = float(gr_mu.mean())
    # Grades: common within-course slope of 2, minus a difficulty penalty that
    # grows with the course's average study hours. Only the intercepts move
    # with the slider; the draws are fixed.
    _grade = (
        80.0 + 2.0 * (gr_hours - _mubar)
        - _c * (gr_mu[gr_course] - _mubar) + gr_noise
    )

    _b1p, _b0p = np.polyfit(gr_hours, _grade, 1)
    # Within (fixed-effects) slope: demean hours and grades by course. This is
    # numerically identical to the regression with course indicators.
    _hd = gr_hours - np.array([gr_hours[gr_course == _j].mean() for _j in range(4)])[gr_course]
    _gd = _grade - np.array([_grade[gr_course == _j].mean() for _j in range(4)])[gr_course]
    _b1w = float((_hd * _gd).sum() / (_hd * _hd).sum())

    _xsc = alt.Scale(domain=[0.0, 15.0], nice=False)
    _ysc = alt.Scale(domain=[58.0, 103.0], nice=False)
    _colors = ["#1f4e79", "#e69138", "#2a9d8f", "#7d5ba6"]

    _pts = pd.DataFrame({
        "hours": gr_hours,
        "grade": _grade,
        "course": [gr_names[_j] for _j in gr_course],
    })
    _layers = [
        alt.Chart(_pts)
        .mark_circle(size=24, opacity=0.45, clip=True)
        .encode(
            x=alt.X("hours:Q", scale=_xsc, title="Weekly study hours"),
            y=alt.Y("grade:Q", scale=_ysc, title="Final course grade"),
            color=alt.Color(
                "course:N",
                scale=alt.Scale(domain=gr_names, range=_colors),
                legend=alt.Legend(title=None, orient="top", columns=2),
            ),
        )
    ]
    for _j in range(4):
        _hj = gr_hours[gr_course == _j]
        _gj = _grade[gr_course == _j]
        _b1j, _b0j = np.polyfit(_hj, _gj, 1)
        _gx = np.array([float(_hj.min()) - 0.4, float(_hj.max()) + 0.4])
        _layers.append(
            alt.Chart(pd.DataFrame({"hours": _gx, "grade": _b0j + _b1j * _gx}))
            .mark_line(color=_colors[_j], size=2.5, clip=True)
            .encode(x=alt.X("hours:Q", scale=_xsc), y=alt.Y("grade:Q", scale=_ysc))
        )
    _gx = np.array([0.5, 14.5])
    _layers.append(
        alt.Chart(pd.DataFrame({"hours": _gx, "grade": _b0p + _b1p * _gx}))
        .mark_line(color="#111827", size=4, clip=True)
        .encode(x=alt.X("hours:Q", scale=_xsc), y=alt.Y("grade:Q", scale=_ysc))
    )
    _chart = alt.layer(*_layers).properties(width=560, height=360)

    if _c == 0.0:
        _msg = (
            f"With the confounder switched off, all four courses share the same "
            f"difficulty, and studying is all that matters. The pooled black line "
            f"has a slope of {_b1p:.2f} grade points per hour, essentially the same "
            f"as the within-course slope of {_b1w:.2f}. Drag the slider to the "
            f"right to make the courses with more study hours harder."
        )
    elif _b1p > 0.5:
        _msg = (
            f"Courses that demand more study hours now also grade harder. The "
            f"within-course lines keep their slope of about {_b1w:.2f}, but the "
            f"pooled black line has flattened to {_b1p:.2f}: comparing students "
            f"across courses mixes the reward for studying with the penalty for "
            f"being in a harder course."
        )
    elif _b1p > -0.05:
        _msg = (
            f"The pooled black line is now nearly flat, with a slope of only "
            f"{_b1p:.2f}, even though every within-course line still has a slope "
            f"of about {_b1w:.2f}. Pooling the courses hides the benefit of "
            f"studying entirely, because the students who study the most sit in "
            f"the hardest courses."
        )
    else:
        _msg = (
            f"The difficulty penalty is now so strong that the pooled black line "
            f"slopes downward, at {_b1p:.2f}: across courses, students who study "
            f"more earn lower grades. Yet within every course the slope is still "
            f"about {_b1w:.2f}. Only the course intercepts, not the reward for "
            f"studying, have changed."
        )
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two questions about this chart are worth pausing on.

    First, why does the pooled regression find almost no effect of studying? Because course difficulty is an omitted variable. It affects grades, and it is correlated with study hours, since the harder courses are the ones that demand more study. Difficulty therefore sits in the error term and is negatively correlated with $X$, which biases the pooled slope downward, exactly the omitted variable bias of Lecture 8. Including the course fixed effects $\alpha_{\text{course}}$ moves difficulty out of the error term and into the intercepts, and the estimated slope recovers the true reward for studying. Notice what made this possible: we never measured difficulty. The fixed effect absorbs it, together with every other difference between courses that is the same for all students in the course.

    Second, if we include a fixed effect for every one of the four courses, can we still include the constant $\beta_0$? We cannot, for a reason we will meet again in Section 4: the four course indicators add up to 1 for every student, which makes them perfectly collinear with the constant.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Panel data

    So far in the course, each dataset observed every individual, worker, or state once. In *panel data*, the same entities are observed over multiple time periods. The entities can be individuals, firms, states, or any other category that is repeatedly observed. Panel data is also called *longitudinal data*. We use the following notation:

    * $i$ indexes the entity (a state, an individual, a firm),
    * $t$ indexes the time period (a year, a month, a day),
    * $Y_{i,t}$ is the value of the variable $Y$ for entity $i$ in period $t$.

    A panel is a *balanced panel* if it contains data on every entity in every time period. If data on some entities are missing in at least one period, the panel is an *unbalanced panel*.

    Our running example for this lecture and the next is a balanced panel of the $n = 50$ U.S. states over the $T = 7$ years from 1982 to 1988, giving $50 \times 7 = 350$ observations. The research question: do higher alcohol taxes lower traffic fatalities? For each state and year we observe the traffic fatality rate, measured in deaths per 10,000 residents, and the tax on a case of beer, measured in dollars. The data are simulated for this course, built to mirror a well-known panel from Stock and Watson's textbook. The first rows look like this:
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # The state fatality panel used in Sections 2 through 5 and in Lecture 16:
    # 50 states, 1982-1988. States whose drinking culture produces more
    # fatalities (pn_z) also levy higher beer taxes, which is the confounder
    # that flips the cross-sectional slope. Beer taxes drift up over the sample
    # while their cross-state spread compresses, and the errors are persistent
    # within a state (an AR(1) with coefficient 0.7, which matters for the
    # standard-error discussion in Lecture 16). True tax effect: -0.45 deaths
    # per 10,000 residents per dollar of tax. Fixed seed; draw order matters.
    pn_states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    ]
    pn_years = np.arange(1982, 1989)
    _n, _T = 50, 7
    _tau = np.arange(_T, dtype=float)
    _spread = 1.0 - 0.055 * _tau

    _rng = np.random.default_rng(3750)
    pn_z = _rng.normal(0.0, 0.30, _n)
    _base = 1.10 + 0.8333 * pn_z + _rng.normal(0.0, 0.25, _n)
    pn_tax = (
        _base.mean()
        + _spread[None, :] * (_base[:, None] - _base.mean())
        + 0.06 * _tau[None, :]
        + _rng.normal(0.0, 0.03, (_n, _T))
    )
    _innov = _rng.normal(0.0, 1.0, (_n, _T))
    _eps = np.empty((_n, _T))
    _eps[:, 0] = _innov[:, 0]
    for _t in range(1, _T):
        _eps[:, _t] = 0.7 * _eps[:, _t - 1] + np.sqrt(1 - 0.7**2) * _innov[:, _t]
    _eps *= 0.10
    pn_fat = 2.40 - 0.45 * pn_tax + pn_z[:, None] + _eps
    return pn_fat, pn_states, pn_tax, pn_years


@app.cell(hide_code=True)
def _(mo, pn_fat, pn_states, pn_tax, pn_years):
    _lines = []
    for _i, _t in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]:
        _lines.append(
            f"| {pn_states[_i]} | {pn_years[_t]} | {pn_fat[_i, _t]:.2f} "
            f"| {pn_tax[_i, _t]:.2f} |"
        )
    _table = (
        "| State ($i$) | Year ($t$) | Fatality rate (per 10,000) | Beer tax (\\$ per case) |\n"
        "|---|---|---|---|\n" + "\n".join(_lines) + "\n| ⋮ | ⋮ | ⋮ | ⋮ |"
    )
    mo.md(_table)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each state contributes one row per year. Reading down the rows for Alabama shows how its fatality rate and beer tax evolve over time; jumping to the Alaska rows switches to a different entity. This structure, many entities each observed in many periods, is what lets us apply the fixed-effects idea from Section 1: the repeated observations on a state play the role that the students in a course played there.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Before-and-after comparisons

    A first idea is to ignore the panel structure and run one cross-sectional regression per year:

    $$
    \begin{aligned}
    \text{Fatality Rate}_{i,1982} &= \beta_0 + \beta_1 \, \text{Beer Tax}_{i,1982} + u_{i,1982}, \\
    \text{Fatality Rate}_{i,1988} &= \beta_0 + \beta_1 \, \text{Beer Tax}_{i,1988} + u_{i,1988}.
    \end{aligned}
    $$

    Running these two regressions on our panel gives $\hat{\beta}_1 = 0.15$ for 1982 and $\hat{\beta}_1 = 0.44$ for 1988. Taken at face value, higher taxes on beer are associated with *more* traffic fatalities. Before concluding that alcohol taxes kill, recall Lecture 14: these estimates are likely biased by state-level omitted variables. A state's drinking culture influences both how many fatal crashes it has and how heavily it decides to tax alcohol. States with severe drunk-driving problems tax beer heavily *because* of those problems, which drags the cross-sectional slope upward.

    Panel data lets us do something about this without measuring drinking culture. Split the error term into two parts,

    $$
    u_{i,t} = Z_i + \varepsilon_{i,t},
    $$

    where $Z_i$ collects the unobserved factors that differ across states but do not change over time (note that $Z_i$ has no $t$ subscript), and $\varepsilon_{i,t}$ collects the unobserved factors that vary over time within a state. Drinking culture, if it is stable over our seven years, lives in $Z_i$.

    Now subtract the 1982 regression from the 1988 regression, state by state. The result is the *difference regression*:

    $$
    \text{Fatality Rate}_{i,1988} - \text{Fatality Rate}_{i,1982}
    = \beta_1\left(\text{Beer Tax}_{i,1988} - \text{Beer Tax}_{i,1982}\right)
    + \underbrace{Z_i - Z_i}_{0}
    + \left(\varepsilon_{i,1988} - \varepsilon_{i,1982}\right).
    $$

    Every time-invariant state factor subtracts away, whether we can measure it or not. The intercept $\beta_0$ cancels for the same reason, since it too is the same in both years. What remains relates the *change* in fatalities to the *change* in the beer tax. The logic:

    * Cultural attitudes toward drinking and driving influence the level of a state's traffic fatalities.
    * If those attitudes did not change between 1982 and 1988, they did not cause *changes* in fatalities.
    * Any change in fatalities must therefore come from other sources, such as changes in the beer tax.
    * The caveat: unobserved factors that *did* change over the period, and did so in step with beer taxes, remain in $\varepsilon_{i,1988} - \varepsilon_{i,1982}$ and can still bias $\hat{\beta}_1$. We return to this in Section 5.

    Use the buttons below to compare the two cross-sections with the difference regression on the same 50 states.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ba_view = mo.ui.radio(
        options=[
            "1982 cross-section",
            "1988 cross-section",
            "Changes, 1988 minus 1982",
        ],
        value="1982 cross-section",
        label="Which regression?",
        inline=True,
    )
    ba_view
    return (ba_view,)


@app.cell(hide_code=True)
def _(alt, ba_view, mo, np, pd, pn_fat, pn_tax):
    _view = ba_view.value

    if _view == "1982 cross-section":
        _x, _y = pn_tax[:, 0], pn_fat[:, 0]
        _xt = "Beer tax in 1982 (dollars per case)"
        _yt = "Fatality rate in 1982 (per 10,000)"
        _xsc = alt.Scale(domain=[0.4, 2.3], nice=False)
        _ysc = alt.Scale(domain=[1.0, 2.6], nice=False)
    elif _view == "1988 cross-section":
        _x, _y = pn_tax[:, 6], pn_fat[:, 6]
        _xt = "Beer tax in 1988 (dollars per case)"
        _yt = "Fatality rate in 1988 (per 10,000)"
        _xsc = alt.Scale(domain=[0.4, 2.3], nice=False)
        _ysc = alt.Scale(domain=[1.0, 2.6], nice=False)
    else:
        _x, _y = pn_tax[:, 6] - pn_tax[:, 0], pn_fat[:, 6] - pn_fat[:, 0]
        _xt = "Change in beer tax, 1988 minus 1982 (dollars per case)"
        _yt = "Change in fatality rate (per 10,000)"
        _xsc = alt.Scale(domain=[-0.05, 0.70], nice=False)
        _ysc = alt.Scale(domain=[-0.55, 0.25], nice=False)

    _b1, _b0 = np.polyfit(_x, _y, 1)
    _pts = (
        alt.Chart(pd.DataFrame({"tax": _x, "fat": _y}))
        .mark_circle(size=42, opacity=0.55, color="#1f4e79", clip=True)
        .encode(
            x=alt.X("tax:Q", scale=_xsc, title=_xt),
            y=alt.Y("fat:Q", scale=_ysc, title=_yt),
        )
    )
    _gx = np.array([float(_x.min()), float(_x.max())])
    _line = (
        alt.Chart(pd.DataFrame({"tax": _gx, "fat": _b0 + _b1 * _gx}))
        .mark_line(color="orange", size=3, clip=True)
        .encode(x=alt.X("tax:Q", scale=_xsc), y=alt.Y("fat:Q", scale=_ysc))
    )
    _layers = [_pts, _line]
    if _view == "Changes, 1988 minus 1982":
        _layers.append(
            alt.Chart(pd.DataFrame({"fat": [0.0]}))
            .mark_rule(color="#9aa5b1", strokeDash=[4, 3])
            .encode(y=alt.Y("fat:Q", scale=_ysc))
        )
    _chart = alt.layer(*_layers).properties(width=560, height=340)

    if _view == "1982 cross-section":
        _msg = (
            f"Each point is one state in 1982. The fitted slope is {_b1:+.2f}: "
            f"states with higher beer taxes have slightly higher fatality rates. "
            f"The high-tax states sit high because of their drinking culture, "
            f"not because of the tax."
        )
    elif _view == "1988 cross-section":
        _msg = (
            f"Six years later the puzzle is worse: the fitted slope is now "
            f"{_b1:+.2f}. A researcher with only cross-sectional data might "
            f"conclude that raising the beer tax by one dollar per case adds "
            f"{_b1:.2f} deaths per 10,000 residents."
        )
    else:
        _msg = (
            f"Now each point is one state's change from 1982 to 1988, so the "
            f"stable state factors Z (drinking culture among them) have "
            f"subtracted out. The slope flips sign to {_b1:+.2f}: states that "
            f"raised their beer tax the most saw fatalities fall the most. The "
            f"dashed line marks a change of zero."
        )
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Entity fixed effects

    The before-and-after comparison uses only two of our seven years. To use all 350 observations, start from the pooled model with the error split as before:

    $$
    Y_{i,t} = \beta_0 + \beta_1 X_{i,t} + \underbrace{Z_i + \varepsilon_{i,t}}_{u_{i,t}},
    $$

    where $Y_{i,t}$ is the fatality rate in state $i$ and year $t$, $X_{i,t}$ is the state's beer tax, $Z_i$ is the unobserved time-invariant state factors, and $\varepsilon_{i,t}$ is the unobserved time-varying factors. We cannot control for $Z_i$ directly, since we cannot measure drinking culture. But we can include a binary variable for each state:

    $$
    Y_{i,t} = \beta_0 + \beta_1 X_{i,t} + \gamma_2\text{CA}_i + \gamma_3\text{IL}_i + \dots + \gamma_{50}\text{NY}_i + \varepsilon_{i,t},
    $$

    where, for example, $\text{CA}_i$ is a binary variable equal to 1 when $i = \text{CA}$ and 0 otherwise. The state indicators are mutually exclusive, so exactly as in Section 1 we can collapse them into one term:

    $$
    Y_{i,t} = \beta_0 + \beta_1 X_{i,t} + \alpha_i + \varepsilon_{i,t},
    \qquad \text{where} \qquad
    \alpha_i = \gamma_2\text{CA}_i + \gamma_3\text{IL}_i + \dots + \gamma_{50}\text{NY}_i.
    $$

    This is the *fixed effects regression model* for panel data, and the $\alpha_i$ are called *entity fixed effects*. The regression estimates one intercept per state ($\alpha_2, \dots, \alpha_{50}$ are unknown coefficients, just like $\beta_1$) plus a single slope $\beta_1$ shared by all states. The fixed effect $\alpha_i$ controls for *all* factors in state $i$ that are constant over time, observed and unobserved alike. Drinking culture, geography, road quality, and anything else that does not change over the seven years is absorbed into the state's intercept, and $\beta_1$ is identified by how fatalities move *within* each state as its beer tax changes.

    The chart below shows six of the fifty states. Switch between fitting one pooled line and fitting one intercept per state.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    fe_view = mo.ui.radio(
        options=[
            "One pooled line",
            "One intercept per state (fixed effects)",
        ],
        value="One pooled line",
        label="How should the line(s) be fit?",
        inline=True,
    )
    fe_view
    return (fe_view,)


@app.cell(hide_code=True)
def _(alt, fe_view, mo, np, pd, pn_fat, pn_states, pn_tax):
    _six = ["CA", "FL", "IL", "NY", "TX", "WI"]
    _idx = [pn_states.index(_s) for _s in _six]
    _t6 = pn_tax[_idx]
    _f6 = pn_fat[_idx]
    _colors = ["#1f4e79", "#e69138", "#2a9d8f", "#7d5ba6", "#c05b5b", "#5b8bc0"]

    # Pooled fit on the 42 shown observations, and the fixed-effects fit with
    # one indicator per state (the dummy regression; computed by demeaning
    # within state, which yields the identical slope).
    _b1p, _b0p = np.polyfit(_t6.ravel(), _f6.ravel(), 1)
    _td = _t6 - _t6.mean(axis=1, keepdims=True)
    _fd = _f6 - _f6.mean(axis=1, keepdims=True)
    _b1f = float((_td * _fd).sum() / (_td * _td).sum())

    _xsc = alt.Scale(domain=[0.7, 1.9], nice=False)
    _ysc = alt.Scale(domain=[1.0, 2.5], nice=False)

    _pts = pd.DataFrame({
        "tax": _t6.ravel(),
        "fat": _f6.ravel(),
        "state": np.repeat(_six, 7),
    })
    _layers = [
        alt.Chart(_pts)
        .mark_circle(size=42, opacity=0.6, clip=True)
        .encode(
            x=alt.X("tax:Q", scale=_xsc, title="Beer tax (dollars per case)"),
            y=alt.Y("fat:Q", scale=_ysc, title="Fatality rate (per 10,000)"),
            color=alt.Color(
                "state:N",
                scale=alt.Scale(domain=_six, range=_colors),
                legend=alt.Legend(title=None, orient="top"),
            ),
        )
    ]
    if fe_view.value == "One pooled line":
        _gx = np.array([float(_t6.min()) - 0.05, float(_t6.max()) + 0.05])
        _layers.append(
            alt.Chart(pd.DataFrame({"tax": _gx, "fat": _b0p + _b1p * _gx}))
            .mark_line(color="#111827", size=4, clip=True)
            .encode(x=alt.X("tax:Q", scale=_xsc), y=alt.Y("fat:Q", scale=_ysc))
        )
        _msg = (
            f"One line through all six states has a slope of {_b1p:+.2f}: higher "
            f"beer taxes look harmless or worse. The line is dragged upward by "
            f"the same problem as in Section 3: the states with the highest "
            f"taxes (and their own high intercepts) sit at the top right."
        )
    else:
        for _j, _s in enumerate(_six):
            _a = float(_f6[_j].mean() - _b1f * _t6[_j].mean())
            _gx = np.array([float(_t6[_j].min()) - 0.06, float(_t6[_j].max()) + 0.06])
            _layers.append(
                alt.Chart(pd.DataFrame({"tax": _gx, "fat": _a + _b1f * _gx}))
                .mark_line(color=_colors[_j], size=2.5, clip=True)
                .encode(x=alt.X("tax:Q", scale=_xsc), y=alt.Y("fat:Q", scale=_ysc))
            )
        _msg = (
            f"With one intercept per state, the common slope is {_b1f:+.2f}: "
            f"within a state, raising the beer tax by one dollar per case lowers "
            f"fatalities by about {abs(_b1f):.2f} per 10,000 residents. Using all "
            f"fifty states, the estimate is -0.42, close to the true effect of "
            f"-0.45 built into the simulation. Each state's intercept absorbs "
            f"its stable characteristics, so only within-state movements "
            f"identify the slope."
        )
    _chart = alt.layer(*_layers).properties(width=560, height=360)
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <span style="color:#0b68cb">The dummy variable trap</span>

    One detail needs care. We cannot include all 50 state fixed effects *and* the intercept $\beta_0$. The 50 state indicators sum to 1 for every observation, which makes them perfectly collinear with the constant, the *dummy variable trap* from Lecture 8's discussion of perfect multicollinearity. There are two equivalent ways out:

    * Omit one state, as the equation above does by starting at $\gamma_2$. The omitted state is the *base state*, its intercept is $\beta_0$, and each $\alpha_i$ is the mean difference in $Y$ between state $i$ and the base state, holding the beer tax fixed.
    * Or drop $\beta_0$ and include all 50 fixed effects, so each state's intercept is estimated directly.

    Which state is omitted changes how the intercepts are labelled but changes nothing of substance: $\hat{\beta}_1$, the fitted values, and the residuals are identical either way. The appendix lets you verify this.

    Finally, the fixed-effects regression is not limited to one regressor. Like in regular multiple regression, we can add further time-varying variables $X_{1,i,t}, X_{2,i,t}, \dots, X_{k,i,t}$, such as each state's unemployment rate or minimum drinking age in each year, and their coefficients keep their usual holding-fixed interpretation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. What fixed effects cannot fix

    Entity fixed effects remove every confounder that is constant over time within a state. They remove nothing else. Factors that change over the sample period stay in $\varepsilon_{i,t}$, and if they move together with beer taxes they still bias $\hat{\beta}_1$, exactly the caveat from Section 3.

    The dangerous confounders are now the ones that change over time for *all* states at once. Over 1982 to 1988, federal safety regulation tightened, cars gained better safety features, and national attitudes toward drunk driving shifted. None of these is constant over time, so no state fixed effect absorbs them. If they trended in step with beer taxes, our estimate of $\beta_1$ still mixes the tax effect with a nationwide trend.

    The fix mirrors what we did in this lecture: give each *time period* its own intercept. That is the subject of Lecture 16.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** mutually exclusive, fixed effect, panel data, "
            "longitudinal data, balanced panel, unbalanced panel, difference "
            "regression, fixed effects regression model, entity fixed effects, "
            "dummy variable trap, base state.\n\n"

            "**Concepts:** a fixed effect as one intercept per group, group "
            "intercepts absorbing all time-invariant group characteristics "
            "without measuring them, why pooled regression is biased when group "
            "intercepts are correlated with the regressor, panel notation and "
            "structure, differencing two periods to remove time-invariant "
            "confounders, the entity fixed-effects regression with many periods, "
            "the dummy variable trap and the base-category interpretation, and "
            "the limits of entity fixed effects when confounders vary over time."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    bs_state = mo.ui.dropdown(
        options=["CA", "FL", "IL", "NY", "TX", "WI"],
        value="CA",
        label="Base (omitted) state",
    )
    return (bs_state,)


@app.cell(hide_code=True)
def _(bs_state, mo, np, pn_fat, pn_states, pn_tax):
    _six = ["CA", "FL", "IL", "NY", "TX", "WI"]
    _idx = [pn_states.index(_s) for _s in _six]
    _t6 = pn_tax[_idx]
    _f6 = pn_fat[_idx]
    _base = _six.index(bs_state.value)

    # The dummy regression itself: intercept, beer tax, and an indicator for
    # every state except the chosen base state.
    _y = _f6.ravel()
    _x = _t6.ravel()
    _sid = np.repeat(np.arange(6), 7)
    _cols = [np.ones(42), _x]
    _labels = []
    for _j in range(6):
        if _j != _base:
            _cols.append((_sid == _j).astype(float))
            _labels.append(_six[_j])
    _X = np.column_stack(_cols)
    _beta, *_rest = np.linalg.lstsq(_X, _y, rcond=None)

    _rows = [
        f"| Beer tax, $\\hat{{\\beta}}_1$ | {_beta[1]:+.3f} |",
        f"| Constant, $\\hat{{\\beta}}_0$ (intercept of {bs_state.value}) | {_beta[0]:+.3f} |",
    ]
    for _k, _lab in enumerate(_labels):
        _rows.append(
            f"| $\\hat{{\\alpha}}$: {_lab} (relative to {bs_state.value}) "
            f"| {_beta[2 + _k]:+.3f} |"
        )
    _table = (
        "| Coefficient | Estimate |\n|---|---|\n" + "\n".join(_rows)
    )

    _text = mo.md(r"""
    This is bonus material. You will not be tested on the content of the appendix.

    **Choosing the base state.** Section 4 said that which state we omit from the fixed-effects regression is a labelling choice with no substance. Verify it here. The regression below uses the six states from Section 4's chart, an intercept, the beer tax, and an indicator for every state except the base state you choose.

    Change the base state and watch the table. The constant becomes the chosen state's intercept, and every $\hat{\alpha}$ re-expresses the other states' intercepts relative to that new base, so all of these numbers move. The beer-tax coefficient $\hat{\beta}_1$ never moves. Neither do the fitted values or residuals: adding a constant to every intercept while relabelling differences leaves every fitted line exactly where it was.
    """)

    mo.accordion({
        "## Appendix": mo.vstack([_text, bs_state, mo.md(_table)]),
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec14InternalAndExternalValidity.html" target="_self">← Lecture 14</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec16PanelDataII.html" target="_self">Lecture 16 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
