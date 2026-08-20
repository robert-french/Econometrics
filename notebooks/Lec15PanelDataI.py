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
app = marimo.App(
    app_title="Lecture 15: Panel Data I",
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
            mo.md("Panel Data I"),
            mo.nav_menu(
                {
                    "#sec1": "1. A puzzling regression",
                    "#sec2": "2. Panel data",
                    "#sec3": "3. Difference regression",
                    "#sec4": "4. Fixed effect regression",
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
    # Lecture 15: Panel Data I
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
    [3. Difference regression](#sec3)<br>
    [4. Fixed effect regression](#sec4)<br>
    [5. What fixed effects cannot fix](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. A puzzling regression

    As we have frequently discussed in this course, many causal questions are difficult to answer because the entities we compare differ in ways that are hard to observe. Workers differ in ability, firms differ in management, and neighborhoods differ in amenities. When these unobserved differences are related to both our outcome and independent variables of interest, they create omitted variable bias.

    In this lecture, we study another economic relationship involving the effect of nitrogen fertilizer on corn yields. Nitrogen is widely understood to increase corn yields, yet a simple regression of corn yields on nitrogen use can suggest exactly the opposite. We will use data on 150 corn farms over six years that record each farm's yield, measured in bushels per acre,<sup><a id="fnref1" href="#fn1">1</a></sup> and nitrogen fertilizer use, measured in pounds per acre. Using data from only the 2014 growing season, when we estimate

    $$
    \text{Yield}_i = \beta_0 + \beta_1 \, \text{Fertilizer}_i + u_i
    $$

    we obtain $\hat{\beta}_1 = -0.19$. According to the regression, each additional pound of nitrogen is associated with about one-fifth of a bushel less corn per acre. Use the dropdown to change seasons, and the same negative relationship appears every year.
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
    return fm_fert, fm_six, fm_years, fm_yield


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
    The likely explanation for these negative coefficient estimates is an omitted variable. Farms with better soil tend to produce higher yields with less fertilizer, while farms with poorer soil tend to apply more nitrogen to compensate for their poor soil. Soil quality therefore sits in the error term and is negatively correlated with fertilizer use, biasing $\hat{\beta}_1$ downward enough to reverse its sign. Controlling directly for soil quality would be difficult because the survey does not measure it, and no single variable fully captures differences in drainage, nutrients, slope, and land-use history.

    The important feature of these data is that the survey follows the same 150 farms every season from 2014 to 2019. This allows us to compare each farm with itself over time rather than relying only on comparisons across farms. In this lecture, we will see how repeated observations of the same entity can be used to account for persistent unobserved differences across entities and thereby address an important source of omitted variable bias.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Panel data

    So far in the course, our datasets have observed each worker, district, or other entity only once. Recall from Lecture 1 that data in which each entity is observed at a single point in time are called *cross-sectional data*. By contrast, *panel data* follow the same entities repeatedly over time. These might be individuals, firms, farms, states, or any other entities that can be observed across multiple periods. Panel data are also sometimes called *longitudinal data*.

    When working with panel data, we use the following notation:

    * $i$ indexes the entity, such as a farm, individual, or firm,
    * $t$ indexes the time period, such as a season, year, or month,
    * $Y_{it}$ is the value of $Y$ for entity $i$ in period $t$.

    A panel is *balanced* if every entity is observed in every time period. It is *unbalanced* if some entities are missing in one or more periods. Our farm data form a balanced panel because all 150 farms are observed in every season. If some farms had stopped responding or left the survey before 2019, the panel would instead be unbalanced.

    Our panel follows $n = 150$ farms over $T = 6$ growing seasons from 2014 to 2019, giving us $150 \times 6 = 900$ observations. The first few rows of the dataset look like this:
    """)
    return


@app.cell(hide_code=True)
def _(fm_fert, fm_years, fm_yield, mo):
    _lines = []

    for _t in range(6):
        _lines.append(
            f"| Farm 1 | {fm_years[_t]} | {fm_yield[0, _t]:.0f} "
            f"| {fm_fert[0, _t]:.0f} |"
        )

    for _t in range(3):
        _lines.append(
            f"| Farm 2 | {fm_years[_t]} | {fm_yield[1, _t]:.0f} "
            f"| {fm_fert[1, _t]:.0f} |"
        )

    _table = (
        "| Farm ($i$) | Season ($t$) | Yield (bu/acre) | Nitrogen (lbs/acre) |\n"
        "|---|---|---|---|\n"
        + "\n".join(_lines)
        + "\n| ⋮ | ⋮ | ⋮ | ⋮ |"
    )

    mo.md(_table)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>

    ## 3. Difference regression

    To see how we can use panel data to help deal with omitted variable bias, let's split the error term into two parts,

    $$
    u_{it} = Z_i + \varepsilon_{it},
    $$

    where $Z_i$ represents the unobserved factors that differ across farms but do not change over time, such as soil type, slope, or drainage. $\varepsilon_{it}$ collects the unobserved factors that vary over time within a farm, such as rainfall, temperature, or pest pressure in a particular season. The absence of a $t$ subscript on $Z_i$ is important; soil type, slope, or drainage changes very little over six seasons, so we can treat it as part of $Z_i$.

    We can now compare each farm in the first and last seasons of the survey by subtracting its 2014 observation from its 2019 observation. This gives the *difference regression*,

    $$
    \text{Yield}_{i2019} - \text{Yield}_{i2014} =
    \beta_1
    \left(
    \text{Fertilizer}_{i2019} - \text{Fertilizer}_{i2014}
    \right)
    +
    \underbrace{(Z_i - Z_i)}_{= 0}
    +
    \left(\varepsilon_{i2019} - \varepsilon_{i2014}\right).
    $$

    Any farm characteristic that remained unchanged between 2014 and 2019 and hence in $Z_i$ cancels out, whether or not we can observe it. The intercept $\beta_0$ cancels for the same reason. Instead of comparing farms with different types of soil, we are now asking whether farms whose fertilizer use increased more between 2014 and 2019 also experienced larger increases in crop yield.

    The key is that soil type may affect the *level* of a farm's yield, but if soil type does not change over time, it cannot explain changes in yield between 2014 and 2019. Differencing therefore removes soil type, along with every other time-invariant farm characteristic, from the regression. Unobserved factors that do change over time are not removed. If changes in weather, pests, irrigation, or other conditions are related to changes in fertilizer use, they remain in $\varepsilon_{i2019} - \varepsilon_{i2014}$ and can still bias $\hat{\beta}_1$. We return to this issue in Section 5.

    The chart below estimates this difference regression across our 150 farms.
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
    The same farms that told us fertilizer is associated with lower corn yields in regressions using cross-sectional data now tell us a pound of nitrogen yields about a third of an additional bushel. Nothing about the data changed. We simply compared each farm *with itself*, so the differences in soil that drove the cross-sectional slope never entered the comparison.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>

    ## 4. Fixed effect regression

    The before-and-after comparison in Section 3 used only two years of our panel. *Fixed effects regressions* extend the same idea to all years in a dataset by allowing each entity, each farm in our case, to have its own intercept in the regression. In practice, we can do this by including a separate binary indicator for each farm. This allows us to estimate the relationship between nitrogen use and crop yield from changes within the same farm over time rather than from differences across farms.

    Consider again the model from Section 3,

    $$
    Y_{it} = \beta_0 + \beta_1 X_{it} + Z_i + \varepsilon_{it},
    $$

    where $Y_{it}$ is farm $i$'s yield in season $t$, $X_{it}$ is its nitrogen use, and $Z_i$ contains the characteristics of the farm that remain constant over time. We cannot observe $Z_i$ directly, but we can account for these persistent differences by allowing each farm to have its own intercept. To do so, we include binary indicators for Farms 1 through 149 in the regression,

    $$
    Y_{it} = \beta_0 + \beta_1 X_{it} + \gamma_1 \text{F1}_i + \gamma_2 \text{F2}_i + \cdots +  \gamma_{149} \text{F149}_i + \varepsilon_{it},
    $$
    where $\text{F1}_i$ equals 1 when farm $i$ is Farm 1 and 0 otherwise, $\text{F2}_i$ equals 1 when farm $i$ is Farm 2 and 0 otherwise, and so on.<sup><a id="fnref2" href="#fn2">2</a></sup> These binary indicators are what we call *mutually exclusive*; if one of the binary indicators equals 1, then all the other binary indicators must equal 0. With this setup, $\beta_0 + \gamma_1$ is Farm 1's expected corn yield when it uses no nitrogen fertilizer, $\beta_0 + \gamma_2$ is Farm 2's expected corn yield when it uses no nitrogen fertilizer, and so on. For Farm 150, whose indicator is omitted, the corresponding expected yield is simply $\beta_0$. Rather than writing out all 149 farm indicators each time, we can collect them into a single term,

    $$\alpha_i = \gamma_1 \text{F1}_i + \gamma_2 \text{F2}_i +\cdots + \gamma_{149} \text{F149}_i.$$

    We can then write the regression more compactly as,
    $$
    Y_{it} =
    \beta_0
    +
    \beta_1 X_{it}
    +
    \alpha_i
    +
    \varepsilon_{it}.
    $$
    The term $\alpha_i$ is called an *entity fixed effect*. It allows the average level of corn yield to differ across farms because of any farm characteristic that remains constant over time, whether we observe it or not. In our example, this includes persistent differences in soil quality, slope, drainage, and other characteristics of the land. By accounting for these time-invariant differences, the regression estimates $\beta_1$ from changes *within* farms over time. It compares a farm's yield in seasons when it uses more fertilizer with its own yield in seasons when it uses less, rather than comparing different farms with one another. The regression still estimates a single $\beta_1$ shared by all farms, so farms can have different intercepts but the model assumes that the average effect of an additional pound of nitrogen on corn yield is the same across farms. When there are only two periods, the fixed effects estimate of $\beta_1$ is the same as the before-and-after difference estimate from Section 3.

    The chart below shows six of the 150 farms. Switch between the pooled regression and the fixed effects regression to see how the fitted relationship changes when each farm is allowed to have its own intercept.
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
        label="How should we fit the regression line(s)?",
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

    # The regression the current selection fits, shown between the buttons and
    # the chart. The pooled version keeps Z_i visible inside the error term,
    # since leaving it there is exactly what biases the pooled line.
    _eqs = {
        "One pooled line":
            r"$$Y_{it} = \beta_0 + \beta_1 X_{it} + \underbrace{Z_i + \varepsilon_{it}}_{u_{it}}$$",
        "One intercept per farm (fixed effects)":
            r"$$Y_{it} = \beta_0 + \beta_1 X_{it} + \alpha_i + \varepsilon_{it}$$",
    }
    _eq = mo.md(_eqs[fe_view.value])

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
            f"One line through all six farms has a slope of {_b1p:+.2f}. "
            f"The line is biased downward "
            f"because the farms applying the most nitrogen tend to have the "
            f"worst quality soil."
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
            rf"With one intercept per farm, the common slope is {_b1f:+.2f}. "
            rf"For the same farm, an extra pound of nitrogen yields an additional third of "
            rf"a bushel of corn. Using all 150 farms, $\hat{{\beta}}_1$ is 0.30. "
            rf"Each farm's intercept "
            rf"absorbs its soil quality, so only differences within a farm over time "
            rf"determine the slope."
        )
    _chart = alt.layer(*_layers).properties(width=560, height=360)
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_eq, _chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>

    ## 5. What fixed effects cannot fix

    Entity fixed effects remove factors that remain constant over time within a farm, but they do not remove factors that change from one season to another. These time-varying factors remain in $\varepsilon_{it}$ and can still bias $\hat{\beta}_1$ if they are related to fertilizer use. For example, rainfall, pest damage, or irrigation may change across seasons and affect both a farm's fertilizer use and its corn yield. Fixed effects do not solve this source of omitted variable bias simply because we observe the same farm over time.

    As in a regular multiple regression, one solution is to control directly for time-varying factors that we observe. A fixed effects regression can include additional independent variables of interest, $X_{1it}, X_{2it}, \dots, X_{kit}$, as well as time-varying controls, $W_{1it}, W_{2it}, \dots, W_{rit}$. In our farm example, we might control for rainfall or pest damage in each farm and season if we could observe them. Doing so holds fixed these observed time-varying factors when estimating the effect of nitrogen fertilizer on yield.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** cross-sectional data, panel data, longitudinal data, "
            "balanced panel, unbalanced panel, difference regression, mutually "
            "exclusive, fixed effects regression, entity fixed effect, base "
            "farm.\n\n"

            "**Concepts:** how an unmeasured, time-invariant confounder can "
            "flip the sign of a cross-sectional slope, panel notation and "
            "structure, differencing two periods to remove time-invariant "
            "confounders, a fixed effect as one intercept per entity absorbing "
            "everything constant about that entity, why only within-entity "
            "movements identify the slope, why one indicator must be left out "
            "of the regression and why the choice of base farm changes no "
            "estimates of interest, and the limits of entity fixed effects "
            "when confounders vary over time."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** A bushel is a unit of volume traditionally used for grain in the United States, equal to about 35 liters. <a href="#fnref1" title="Back to text">&#8617;</a></span>

    <span id="fn2" style="display:block;font-size:0.9rem;">**2.** We leave out the indicator for Farm 150 because the regression already contains the intercept $\beta_0$. If we included all 150 farm indicators, they would add up to 1 for every observation and would therefore be an exact linear function of the intercept. The regression would thus exhibit perfect multicollinearity, violating the fourth OLS assumption discussed in Lecture 9 that no independent variable is an exact linear function of the others. <a href="#fnref2" title="Back to text">&#8617;</a></span>
    """)
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
def _(np):
    # Appendix demo: six students in a single semester, eight courses each.
    # Ability (in grade points) is the time-invariant confounder: the ablest
    # students study the fewest weekly hours yet earn the highest grades, so
    # the pooled slope turns negative while the within-student slope is +2.
    # Fixed seed; draw order matters.
    _rng = np.random.default_rng(1978)
    _ability = _rng.normal(0.0, 12.0, 6)
    _hbar = np.clip(7.0 - 0.21 * _ability + _rng.normal(0.0, 1.5, 6), 2.5, 11.0)
    ap_hours = np.clip(_hbar[:, None] + _rng.normal(0.0, 2.0, (6, 8)), 1.0, 12.0)
    ap_grades = (
        58.0 + 2.0 * ap_hours + _ability[:, None]
        + _rng.normal(0.0, 4.0, (6, 8))
    )
    ap_students = ["Ana", "Ben", "Cara", "Dan", "Eva", "Finn"]
    return ap_grades, ap_hours, ap_students


@app.cell(hide_code=True)
def _(mo):
    ap_view = mo.ui.radio(
        options=[
            "One pooled line",
            "One intercept per student (fixed effects)",
        ],
        value="One pooled line",
        label="How should the line(s) be fit?",
        inline=True,
    )
    return (ap_view,)


@app.cell(hide_code=True)
def _(
    alt,
    ap_grades,
    ap_hours,
    ap_students,
    ap_view,
    bs_farm,
    fm_fert,
    fm_six,
    fm_yield,
    mo,
    np,
    pd,
):
    _names = [f"Farm {_i + 1}" for _i in fm_six]
    _t6 = fm_fert[fm_six]
    _f6 = fm_yield[fm_six]
    _base = _names.index(bs_farm.value)

    # Part 1 - the base-farm table: the dummy regression with an intercept,
    # fertilizer, and an indicator for every farm except the chosen base farm.
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
            f"| $\\hat{{\\gamma}}$: {_lab} (relative to {bs_farm.value}) "
            f"| {_beta[2 + _k]:+.1f} |"
        )
    _table = mo.md(
        "| Coefficient | Estimate |\n|---|---|\n" + "\n".join(_rows)
    )

    # One paragraph per vstack item: paragraphs inside a single mo.md pick up
    # the large prose <p> margins while separate items only get the flex gap,
    # which made the appendix spacing uneven. With one paragraph per item the
    # vstack gap alone controls the rhythm.
    _bonus = mo.md(r"""This is bonus material. You will not be tested on the content of the appendix.""")

    _base_text = mo.md(r"""**Choosing the base farm.** In Section 4, we left out the indicator for Farm 150. As a result, $\beta_0$ gives Farm 150's intercept, while each $\gamma$ measures the difference between another farm's intercept and Farm 150's. The omitted farm is called the *base farm*, but which farm we choose as the base is simply a matter of labelling. You can verify this below using the six farms from Section 4. The regression includes an intercept, fertilizer use, and an indicator for every farm except the base farm you select. Changing the base farm changes the constant and every $\hat{\gamma}$ because these coefficients are now expressed relative to a different farm. But $\hat{\beta}_1$, the fitted values, and the residuals do not change. Choosing a different base farm simply changes how the intercepts are represented, not the fitted regression.""")
    # Part 2 - fixed effects without a time dimension: the student-grades
    # demo. Fits mirror the Section 4 chart: pooled line vs one intercept per
    # student, the latter computed by demeaning within student, which yields
    # the identical slope to the dummy regression.
    _b1p, _b0p = np.polyfit(ap_hours.ravel(), ap_grades.ravel(), 1)
    _hd = ap_hours - ap_hours.mean(axis=1, keepdims=True)
    _gd = ap_grades - ap_grades.mean(axis=1, keepdims=True)
    _b1w = float((_hd * _gd).sum() / (_hd * _hd).sum())

    _fe2 = mo.md(r"""**Fixed effects without a time dimension.** Nothing in the fixed effects logic requires observing entities over time. It requires only multiple observations on the same entity, and those observations can all come from a single point in time. Suppose we observe six students during one semester and have data on their course grades and weekly study hours for each of the eight courses on their schedules. Suppose we want to use regression analysis to understand the causal effect of hours studied on course grades. If we pooled all these observations and regressed the $6 \times 8 = 48$ course grades on study hours, we would mix two different statistical relationships: study hours vary across courses within a student's schedule, but students also differ in how much they tend to study overall. Student ability now plays the role that soil quality played in the lecture. It is hard to measure, raises grades directly, and in our data the ablest students tend to study less, so the pooled regression suggests that studying lowers grades. Including a student-level fixed effect, so that we have one intercept per student exactly as in Section 4, removes student ability and every other stable student trait from the error term. Then $\beta_1$ is estimated by comparing the courses a student studies hardest for with the other courses in that same student's schedule.""")

    _xsc = alt.Scale(domain=[0.0, 13.0], nice=False)
    _ysc = alt.Scale(domain=[48.0, 102.0], nice=False)
    _colors = ["#1f4e79", "#e69138", "#2a9d8f", "#7d5ba6", "#c05b5b", "#5b8bc0"]
    _pts = pd.DataFrame({
        "hours": ap_hours.ravel(),
        "grade": ap_grades.ravel(),
        "student": np.repeat(ap_students, 8),
    })
    _layers = [
        alt.Chart(_pts)
        .mark_circle(size=42, opacity=0.6, clip=True)
        .encode(
            x=alt.X("hours:Q", scale=_xsc,
                    title="Weekly study hours for the course"),
            y=alt.Y("grade:Q", scale=_ysc, title="Course grade (out of 100)"),
            color=alt.Color(
                "student:N",
                scale=alt.Scale(domain=ap_students, range=_colors),
                legend=alt.Legend(title=None, orient="top"),
            ),
        )
    ]
    if ap_view.value == "One pooled line":
        _gx = np.array([float(ap_hours.min()) - 0.4,
                        float(ap_hours.max()) + 0.4])
        _layers.append(
            alt.Chart(pd.DataFrame({"hours": _gx, "grade": _b0p + _b1p * _gx}))
            .mark_line(color="#111827", size=4, clip=True)
            .encode(x=alt.X("hours:Q", scale=_xsc),
                    y=alt.Y("grade:Q", scale=_ysc))
        )
        _msg = (
            f"One line through all six students has a slope of {_b1p:+.2f}; "
            f"studying appears to cost grade points. The line is biased "
            f"because the strongest students both study the least and earn "
            f"the highest grades."
        )
    else:
        for _j in range(6):
            _a = float(ap_grades[_j].mean() - _b1w * ap_hours[_j].mean())
            _gx = np.array([float(ap_hours[_j].min()) - 0.5,
                            float(ap_hours[_j].max()) + 0.5])
            _layers.append(
                alt.Chart(pd.DataFrame({"hours": _gx,
                                        "grade": _a + _b1w * _gx}))
                .mark_line(color=_colors[_j], size=2.5, clip=True)
                .encode(x=alt.X("hours:Q", scale=_xsc),
                        y=alt.Y("grade:Q", scale=_ysc))
            )
        _msg = (
            f"With one intercept per student, the common slope is "
            f"{_b1w:+.2f}. An extra weekly hour spent on a course raises its "
            f"grade by about two points. Each student's intercept absorbs "
            f"their ability, and the slope comes only from comparisons "
            f"within each student's own schedule."
        )
    _chart = alt.layer(*_layers).properties(width=560, height=340)
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 0.4rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    _grades_demo = mo.vstack([_chart, _caption], align="center")

    mo.accordion({
        "## Appendix": mo.vstack(
            [_bonus, _base_text, bs_farm, _table, _fe2, ap_view, _grades_demo],
            gap=1,
        ),
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
