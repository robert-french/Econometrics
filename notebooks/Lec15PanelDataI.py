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
                    "#sec1": "1. A puzzling regression",
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

    [1. A puzzling regression](#sec1)<br>
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
    ## 1. A puzzling regression

    Does nitrogen fertilizer raise corn yields? Every agronomy textbook says yes, and every farmer who buys fertilizer is betting on it. Let us check with a regression.

    Our data is a survey of 150 corn farms. For each farm we observe the season's yield, measured in bushels of corn per acre, and the amount of nitrogen fertilizer the farm applied, in pounds per acre. Using the 2014 growing season, we estimate

    $$
    \text{Yield}_i = \beta_0 + \beta_1 \, \text{Fertilizer}_i + u_i
    $$

    and obtain $\hat{\beta}_1 = -0.19$: each additional pound of nitrogen is associated with about a fifth of a bushel *less* corn. Taken at face value, fertilizer poisons corn. Use the dropdown to try the other seasons in the survey; the slope is negative every single year.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # The farm panel used throughout the lecture: 150 corn farms observed over
    # the six growing seasons 2014-2019. Soil quality (fm_z, in bushels per
    # acre) is the time-invariant confounder: farms with poor soil apply more
    # nitrogen to compensate, which is what turns the cross-sectional slope
    # negative. Fertilizer is a level that wobbles year to year around each
    # farm's typical rate, with no trend. Errors are persistent within a farm
    # (AR(1) with coefficient 0.7). True fertilizer effect: +0.30 bushels per
    # acre per pound of nitrogen. Fixed seed; draw order matters.
    fm_years = np.arange(2014, 2020)
    _n, _T = 150, 6
    _rng = np.random.default_rng(411)
    fm_z = _rng.normal(0.0, 25.0, _n)
    _typical = 150.0 - 0.6 * fm_z + _rng.normal(0.0, 20.0, _n)
    fm_fert = _typical[:, None] + _rng.normal(0.0, 12.0, (_n, _T))
    _innov = _rng.normal(0.0, 1.0, (_n, _T))
    _eps = np.empty((_n, _T))
    _eps[:, 0] = _innov[:, 0]
    for _t in range(1, _T):
        _eps[:, _t] = 0.7 * _eps[:, _t - 1] + np.sqrt(1 - 0.7**2) * _innov[:, _t]
    _eps *= 8.0
    fm_yield = 125.0 + 0.30 * fm_fert + fm_z[:, None] + _eps
    # Six farms with a spread of typical nitrogen rates, used by the Section 4
    # chart and the appendix. Deterministic given the seed.
    fm_six = [7, 47, 65, 110, 114, 115]
    return fm_fert, fm_six, fm_years, fm_yield, fm_z


@app.cell(hide_code=True)
def _(fm_years, mo):
    cs_year = mo.ui.dropdown(
        options=[str(_y) for _y in fm_years],
        value="2014",
        label="Growing season",
    )
    cs_year
    return (cs_year,)


@app.cell(hide_code=True)
def _(alt, cs_year, fm_fert, fm_years, fm_yield, mo, np, pd):
    _t = int(cs_year.value) - int(fm_years[0])
    _x, _y = fm_fert[:, _t], fm_yield[:, _t]
    _b1, _b0 = np.polyfit(_x, _y, 1)

    _xsc = alt.Scale(domain=[60.0, 250.0], nice=False)
    _ysc = alt.Scale(domain=[95.0, 245.0], nice=False)
    _pts = (
        alt.Chart(pd.DataFrame({"fert": _x, "yield": _y}))
        .mark_circle(size=34, opacity=0.5, color="#1f4e79", clip=True)
        .encode(
            x=alt.X("fert:Q", scale=_xsc,
                    title=f"Nitrogen applied in {cs_year.value} (pounds per acre)"),
            y=alt.Y("yield:Q", scale=_ysc,
                    title=f"Corn yield in {cs_year.value} (bushels per acre)"),
        )
    )
    _gx = np.array([float(_x.min()), float(_x.max())])
    _line = (
        alt.Chart(pd.DataFrame({"fert": _gx, "yield": _b0 + _b1 * _gx}))
        .mark_line(color="orange", size=3, clip=True)
        .encode(x=alt.X("fert:Q", scale=_xsc), y=alt.Y("yield:Q", scale=_ysc))
    )
    _chart = (_pts + _line).properties(width=560, height=340)

    _msg = (
        f"Each point is one of the 150 farms in the {cs_year.value} season. "
        f"The fitted slope is {_b1:+.2f} bushels per pound of nitrogen. "
        f"Whichever season you pick, the heaviest fertilizer users harvest "
        f"the least corn."
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
    Lecture 14 taught us what to suspect: an omitted variable. Farms differ in *soil quality*, which we cannot measure. Good soil raises yields on its own. And it is precisely the farms with poor soil that apply the most nitrogen, trying to compensate for what their land lacks. Soil quality therefore sits in the error term and is negatively correlated with fertilizer use, which biases $\hat{\beta}_1$ downward, so far downward that its sign flips.

    The usual remedy from Lecture 9 would be to control for soil quality. But no one in the survey measured it, and "soil quality" bundles drainage, nutrients, slope, and history into something no single number captures. We seem stuck.

    We are not stuck, because this survey has a structure we have not exploited yet: it went back to the *same 150 farms* every season from 2014 to 2019.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Panel data

    So far in the course, each dataset observed every worker, district, or farm exactly once. In *panel data*, the same entities are observed over multiple time periods. The entities can be farms, individuals, firms, states, or any other category that is repeatedly observed. Panel data is also called *longitudinal data*. We use the following notation:

    * $i$ indexes the entity (a farm, an individual, a firm),
    * $t$ indexes the time period (a season, a year, a month),
    * $Y_{i,t}$ is the value of the variable $Y$ for entity $i$ in period $t$.

    A panel is a *balanced panel* if it contains data on every entity in every time period. If data on some entities are missing in at least one period, the panel is an *unbalanced panel*. Ours is balanced because every farm reported in every season; a real survey in which some farms sold up or stopped responding would be unbalanced.

    Our panel follows $n = 150$ farms over the $T = 6$ seasons from 2014 to 2019, giving $150 \times 6 = 900$ observations. The first rows look like this:
    """)
    return


@app.cell(hide_code=True)
def _(fm_fert, fm_years, fm_yield, mo):
    _lines = []
    for _i, _t in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]:
        _lines.append(
            f"| Farm {_i + 1} | {fm_years[_t]} | {fm_yield[_i, _t]:.0f} "
            f"| {fm_fert[_i, _t]:.0f} |"
        )
    _table = (
        "| Farm ($i$) | Season ($t$) | Yield (bu/acre) | Nitrogen (lbs/acre) |\n"
        "|---|---|---|---|\n" + "\n".join(_lines) + "\n| ⋮ | ⋮ | ⋮ | ⋮ |"
    )
    mo.md(_table)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each farm contributes one row per season. Reading down Farm 1's rows shows how its yield and nitrogen use evolve over time; jumping to Farm 2's rows switches to a different entity. The repetition is the resource: whatever is stable about a farm, soil quality included, appears in all six of its rows. The next two sections turn that repetition into a way of removing soil quality from the regression without ever measuring it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Before-and-after comparisons

    Split the error term into two parts,

    $$
    u_{i,t} = Z_i + \varepsilon_{i,t},
    $$

    where $Z_i$ collects the unobserved factors that differ across farms but do not change over time (note that $Z_i$ has no $t$ subscript), and $\varepsilon_{i,t}$ collects the unobserved factors that vary over time within a farm. Soil quality changes very little over six seasons, so it lives in $Z_i$.

    Now take the survey's first and last seasons and subtract, farm by farm. The result is the *difference regression*:

    $$
    \text{Yield}_{i,2019} - \text{Yield}_{i,2014}
    = \beta_1\left(\text{Fertilizer}_{i,2019} - \text{Fertilizer}_{i,2014}\right)
    + \underbrace{Z_i - Z_i}_{0}
    + \left(\varepsilon_{i,2019} - \varepsilon_{i,2014}\right).
    $$

    Every time-invariant farm factor subtracts away, whether we can measure it or not. The intercept $\beta_0$ cancels for the same reason, since it too is the same in both seasons. What remains relates the *change* in yield to the *change* in fertilizer. The logic:

    * Soil quality influences the *level* of a farm's yield.
    * If soil quality did not change between 2014 and 2019, it did not cause *changes* in yield.
    * Any change in a farm's yield must therefore come from other sources, such as its change in fertilizer use.
    * The caveat: factors that *did* change over the period, and did so in step with fertilizer use, remain in $\varepsilon_{i,2019} - \varepsilon_{i,2014}$ and can still bias $\hat{\beta}_1$. Section 5 returns to this.

    The chart below runs the difference regression on our 150 farms.
    """)
    return


@app.cell(hide_code=True)
def _(alt, fm_fert, fm_yield, mo, np, pd):
    _dx = fm_fert[:, 5] - fm_fert[:, 0]
    _dy = fm_yield[:, 5] - fm_yield[:, 0]
    _b1, _b0 = np.polyfit(_dx, _dy, 1)

    _xsc = alt.Scale(domain=[-50.0, 50.0], nice=False)
    _ysc = alt.Scale(domain=[-36.0, 42.0], nice=False)
    _pts = (
        alt.Chart(pd.DataFrame({"dfert": _dx, "dyield": _dy}))
        .mark_circle(size=34, opacity=0.5, color="#1f4e79", clip=True)
        .encode(
            x=alt.X("dfert:Q", scale=_xsc,
                    title="Change in nitrogen, 2019 minus 2014 (pounds per acre)"),
            y=alt.Y("dyield:Q", scale=_ysc,
                    title="Change in yield (bushels per acre)"),
        )
    )
    _zero = (
        alt.Chart(pd.DataFrame({"dyield": [0.0]}))
        .mark_rule(color="#9aa5b1", strokeDash=[4, 3])
        .encode(y=alt.Y("dyield:Q", scale=_ysc))
    )
    _gx = np.array([float(_dx.min()), float(_dx.max())])
    _line = (
        alt.Chart(pd.DataFrame({"dfert": _gx, "dyield": _b0 + _b1 * _gx}))
        .mark_line(color="orange", size=3, clip=True)
        .encode(x=alt.X("dfert:Q", scale=_xsc), y=alt.Y("dyield:Q", scale=_ysc))
    )
    _chart = (_pts + _zero + _line).properties(width=560, height=340)

    _msg = (
        f"Each point is now one farm's change from 2014 to 2019, so soil "
        f"quality has subtracted out. The slope flips sign to {_b1:+.2f}: "
        f"farms that raised their nitrogen the most saw yields rise the most, "
        f"close to the true effect of +0.30 built into the simulation. The "
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
    The same farms that told us fertilizer poisons corn now tell us a pound of nitrogen buys about a third of a bushel. Nothing about the data changed. We simply compared each farm *with itself*, so the differences in soil that drove the cross-sectional slope never entered the comparison.

    One thing should nag at you: this used only two of our six seasons. The next section uses all 900 observations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Entity fixed effects

    The tool that generalizes before-and-after differencing is a regression whose independent variables are a set of binary variables,

    $$
    Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_K X_K + u,
    $$

    where each of $X_1, \dots, X_K$ equals either 0 or 1. The binary variables are *mutually exclusive* if only one of them can equal 1 for each observation. For example, $X_k$ might equal 1 if the observation comes from farm $k$: every observation belongs to exactly one farm, so one indicator equals 1 and the other 149 equal 0.

    Interpreting the coefficients works the same way as for the single binary regressor in Lecture 5:

    * $\hat{\beta}_0$ is the predicted value of $Y$ for observations with all $X_k = 0$.
    * $\hat{\beta}_0 + \hat{\beta}_k$ is the predicted value of $Y$ for observations with $X_k = 1$.

    Because the binary variables are mutually exclusive, we can write the regression more compactly as

    $$
    Y = \beta_0 + \alpha_k + u,
    \qquad \text{where} \qquad
    \alpha_k = \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_K X_K.
    $$

    The term $\alpha_k$ is called a *fixed effect*: a fixed effect gives each group its own intercept.

    Now apply this to the panel. Start from the pooled model with the error split as in Section 3,

    $$
    Y_{i,t} = \beta_0 + \beta_1 X_{i,t} + \underbrace{Z_i + \varepsilon_{i,t}}_{u_{i,t}},
    $$

    where $Y_{i,t}$ is farm $i$'s yield in season $t$, $X_{i,t}$ is its nitrogen use, and $Z_i$ is its unobserved soil quality. We cannot control for $Z_i$ directly. But we can include a mutually exclusive binary variable for each farm,

    $$
    Y_{i,t} = \beta_0 + \beta_1 X_{i,t} + \gamma_2\text{F2}_i + \gamma_3\text{F3}_i + \dots + \gamma_{150}\text{F150}_i + \varepsilon_{i,t},
    $$

    where, for example, $\text{F2}_i$ is a binary variable equal to 1 when $i$ is Farm 2 and 0 otherwise, and then collapse the indicators exactly as above:

    $$
    Y_{i,t} = \beta_0 + \beta_1 X_{i,t} + \alpha_i + \varepsilon_{i,t},
    \qquad \text{where} \qquad
    \alpha_i = \gamma_2\text{F2}_i + \gamma_3\text{F3}_i + \dots + \gamma_{150}\text{F150}_i.
    $$

    This is the *fixed effects regression model* for panel data, and the $\alpha_i$ are called *entity fixed effects*. The regression estimates one intercept per farm plus a single slope $\beta_1$ shared by all farms. The fixed effect $\alpha_i$ controls for *all* factors of farm $i$ that are constant over time, observed and unobserved alike: soil quality, drainage, the farmer's skill, distance to market. Only movements *within* each farm, this season's nitrogen against the same farm's other seasons, identify $\beta_1$. The before-and-after comparison of Section 3 is exactly this model in the special case $T = 2$.

    The chart below shows six of the 150 farms. Switch between fitting one pooled line and fitting one intercept per farm.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    fe_view = mo.ui.radio(
        options=[
            "One pooled line",
            "One intercept per farm (fixed effects)",
        ],
        value="One pooled line",
        label="How should the line(s) be fit?",
        inline=True,
    )
    fe_view
    return (fe_view,)


@app.cell(hide_code=True)
def _(alt, fe_view, fm_fert, fm_six, fm_yield, mo, np, pd):
    _t6 = fm_fert[fm_six]
    _f6 = fm_yield[fm_six]
    _names = [f"Farm {_i + 1}" for _i in fm_six]
    _colors = ["#1f4e79", "#e69138", "#2a9d8f", "#7d5ba6", "#c05b5b", "#5b8bc0"]

    # Pooled fit on the 36 shown observations, and the fixed-effects fit with
    # one indicator per farm (the dummy regression; computed by demeaning
    # within farm, which yields the identical slope).
    _b1p, _b0p = np.polyfit(_t6.ravel(), _f6.ravel(), 1)
    _td = _t6 - _t6.mean(axis=1, keepdims=True)
    _fd = _f6 - _f6.mean(axis=1, keepdims=True)
    _b1f = float((_td * _fd).sum() / (_td * _td).sum())

    _xsc = alt.Scale(domain=[95.0, 235.0], nice=False)
    _ysc = alt.Scale(domain=[95.0, 235.0], nice=False)

    _pts = pd.DataFrame({
        "fert": _t6.ravel(),
        "yield": _f6.ravel(),
        "farm": np.repeat(_names, 6),
    })
    _layers = [
        alt.Chart(_pts)
        .mark_circle(size=42, opacity=0.6, clip=True)
        .encode(
            x=alt.X("fert:Q", scale=_xsc, title="Nitrogen applied (pounds per acre)"),
            y=alt.Y("yield:Q", scale=_ysc, title="Corn yield (bushels per acre)"),
            color=alt.Color(
                "farm:N",
                scale=alt.Scale(domain=_names, range=_colors),
                legend=alt.Legend(title=None, orient="top"),
            ),
        )
    ]
    if fe_view.value == "One pooled line":
        _gx = np.array([float(_t6.min()) - 3.0, float(_t6.max()) + 3.0])
        _layers.append(
            alt.Chart(pd.DataFrame({"fert": _gx, "yield": _b0p + _b1p * _gx}))
            .mark_line(color="#111827", size=4, clip=True)
            .encode(x=alt.X("fert:Q", scale=_xsc), y=alt.Y("yield:Q", scale=_ysc))
        )
        _msg = (
            f"One line through all six farms has a slope of {_b1p:+.2f}: the "
            f"cross-sectional puzzle again. The line is dragged downward "
            f"because the farms applying the most nitrogen (their own low "
            f"intercepts, poor soil) sit at the bottom right."
        )
    else:
        for _j in range(6):
            _a = float(_f6[_j].mean() - _b1f * _t6[_j].mean())
            _gx = np.array([float(_t6[_j].min()) - 4.0, float(_t6[_j].max()) + 4.0])
            _layers.append(
                alt.Chart(pd.DataFrame({"fert": _gx, "yield": _a + _b1f * _gx}))
                .mark_line(color=_colors[_j], size=2.5, clip=True)
                .encode(x=alt.X("fert:Q", scale=_xsc), y=alt.Y("yield:Q", scale=_ysc))
            )
        _msg = (
            f"With one intercept per farm, the common slope is {_b1f:+.2f}: "
            f"within a farm, an extra pound of nitrogen adds about a third of "
            f"a bushel. Using all 150 farms, the estimate is +0.30, matching "
            f"the true effect built into the simulation. Each farm's intercept "
            f"absorbs its soil quality, so only within-farm movements "
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

    One detail needs care. We cannot include all 150 farm fixed effects *and* the intercept $\beta_0$. The 150 farm indicators sum to 1 for every observation, which makes them perfectly collinear with the constant, the *dummy variable trap* from Lecture 8's discussion of perfect multicollinearity. There are two equivalent ways out:

    * Omit one farm, as the equation above does by starting at $\gamma_2$. The omitted farm is the *base farm*, its intercept is $\beta_0$, and each $\alpha_i$ is the mean difference in $Y$ between farm $i$ and the base farm, holding fertilizer fixed.
    * Or drop $\beta_0$ and include all 150 fixed effects, so each farm's intercept is estimated directly.

    Which farm is omitted changes how the intercepts are labelled but changes nothing of substance: $\hat{\beta}_1$, the fitted values, and the residuals are identical either way. The appendix lets you verify this.

    Finally, the fixed-effects regression is not limited to one regressor. Like in regular multiple regression, we can add further time-varying variables $X_{1,i,t}, X_{2,i,t}, \dots, X_{k,i,t}$, such as each farm's rainfall or pest damage in each season, and their coefficients keep their usual holding-fixed interpretation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. What fixed effects cannot fix

    Entity fixed effects remove every confounder that is constant over time within a farm. They remove nothing else. Factors that change over the sample period stay in $\varepsilon_{i,t}$, and if they move together with fertilizer use they still bias $\hat{\beta}_1$, exactly the caveat from Section 3.

    The dangerous confounders are now the ones that change over time for *all* farms at once. A drought season lowers every farm's yield regardless of fertilizer. Fertilizer prices rise and fall for everyone together, shifting how much nitrogen every farm applies in the same year. Seed varieties improve for all farms over time. None of these is constant over time, so no farm fixed effect absorbs them. If they trend in step with fertilizer use, our estimate of $\beta_1$ still mixes the fertilizer effect with a shared shock.

    The fix mirrors what we did in this lecture: give each *time period* its own intercept. That is the subject of Lecture 16.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** panel data, longitudinal data, balanced panel, "
            "unbalanced panel, difference regression, mutually exclusive, "
            "fixed effect, fixed effects regression model, entity fixed "
            "effects, dummy variable trap, base farm.\n\n"

            "**Concepts:** how an unmeasured, time-invariant confounder can "
            "flip the sign of a cross-sectional slope, panel notation and "
            "structure, differencing two periods to remove time-invariant "
            "confounders, a fixed effect as one intercept per group absorbing "
            "everything stable about that group, the entity fixed-effects "
            "regression with many periods and why only within-entity movements "
            "identify the slope, the dummy variable trap and the base-category "
            "interpretation, and the limits of entity fixed effects when "
            "confounders vary over time."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(fm_six, mo):
    bs_farm = mo.ui.dropdown(
        options=[f"Farm {_i + 1}" for _i in fm_six],
        value=f"Farm {fm_six[0] + 1}",
        label="Base (omitted) farm",
    )
    return (bs_farm,)


@app.cell(hide_code=True)
def _(bs_farm, fm_fert, fm_six, fm_yield, mo, np):
    _names = [f"Farm {_i + 1}" for _i in fm_six]
    _t6 = fm_fert[fm_six]
    _f6 = fm_yield[fm_six]
    _base = _names.index(bs_farm.value)

    # The dummy regression itself: intercept, fertilizer, and an indicator for
    # every farm except the chosen base farm.
    _y = _f6.ravel()
    _x = _t6.ravel()
    _fid = np.repeat(np.arange(6), 6)
    _cols = [np.ones(36), _x]
    _labels = []
    for _j in range(6):
        if _j != _base:
            _cols.append((_fid == _j).astype(float))
            _labels.append(_names[_j])
    _X = np.column_stack(_cols)
    _beta, *_rest = np.linalg.lstsq(_X, _y, rcond=None)

    _rows = [
        f"| Fertilizer, $\\hat{{\\beta}}_1$ | {_beta[1]:+.3f} |",
        f"| Constant, $\\hat{{\\beta}}_0$ (intercept of {bs_farm.value}) | {_beta[0]:+.1f} |",
    ]
    for _k, _lab in enumerate(_labels):
        _rows.append(
            f"| $\\hat{{\\alpha}}$: {_lab} (relative to {bs_farm.value}) "
            f"| {_beta[2 + _k]:+.1f} |"
        )
    _table = (
        "| Coefficient | Estimate |\n|---|---|\n" + "\n".join(_rows)
    )

    _text = mo.md(r"""
    This is bonus material. You will not be tested on the content of the appendix.

    **Choosing the base farm.** Section 4 said that which farm we omit from the fixed-effects regression is a labelling choice with no substance. Verify it here. The regression below uses the six farms from Section 4's chart, an intercept, fertilizer, and an indicator for every farm except the base farm you choose.

    Change the base farm and watch the table. The constant becomes the chosen farm's intercept, and every $\hat{\alpha}$ re-expresses the other farms' intercepts relative to that new base, so all of these numbers move. The fertilizer coefficient $\hat{\beta}_1$ never moves. Neither do the fitted values or residuals: adding a constant to every intercept while relabelling differences leaves every fitted line exactly where it was.
    """)

    mo.accordion({
        "## Appendix": mo.vstack([_text, bs_farm, mo.md(_table)]),
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
