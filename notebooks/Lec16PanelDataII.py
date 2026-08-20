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
    app_title="Lecture 16: Panel Data II",
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
            mo.md("# [Lecture 16](#top)"),
            mo.md("Panel Data II"),
            mo.nav_menu(
                {
                    "#sec1": "1. Another puzzling regression",
                    "#sec2": "2. Time fixed effects",
                    "#sec3": "3. Two-way fixed effects",
                    "#sec4": "4. Standard errors in panel data",
                    "#sec5": "5. Reading a panel regression table",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec15PanelDataI.html" target="_self">← Lecture 15</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec17BinaryDependentVariables.html" target="_self">Lecture 17 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 16: Panel Data II
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Same-page (#fragment) links must stay plain markdown links with no inline
    # style and no styled wrapper; see the note in Lec14.
    mo.md(r"""
    ## Contents

    [1. Another puzzling regression](#sec1)<br>
    [2. Time fixed effects](#sec2)<br>
    [3. Two-way fixed effects](#sec3)<br>
    [4. Standard errors in panel data](#sec4)<br>
    [5. Reading a panel regression table](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Another puzzling regression

    In Lecture 15, we used a panel of 150 corn farms observed over the 2014 to 2019 growing seasons to estimate the effect of nitrogen fertilizer on corn yields. The fixed effects regression gave each farm its own intercept, holding fixed unobserved differences in soil quality that had reversed the sign of the cross-sectional relationship. The regression estimated that an extra pound of nitrogen raises yields by $\hat{\beta}_1 = 0.30$ bushels per acre.

    Suppose the survey later resumed and followed the same 150 farms for six more seasons, from 2020 through 2025. During these years, however, two things changed. Fertilizer became cheaper, so farms across the country applied more nitrogen each season. At the same time, newly developed seed varieties spread quickly and raised yields on the farms that adopted them.

    Estimating the same fixed effects regression from Lecture 15 on these new seasons,

    $$
    Y_{it} = \beta_0 + \beta_1 X_{it} + \alpha_i + \varepsilon_{it},
    $$

    now gives $\hat{\beta}_1 = 0.63$, more than twice the estimate we trusted in Lecture 15. Fertilizer did not suddenly become twice as effective, though. Something must therefore be wrong with the regression. The chart below suggests to us the issue, following the same six farms as Lecture 15 across the six new seasons:
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # The same 150 farms as Lecture 15 (identical seed and draw order for the
    # soil quality fm_z and each farm's typical nitrogen rate), now observed
    # over six new seasons, 2020-2025. Two additions relative to the Lecture 15
    # panel: a common upward drift in nitrogen use of 7 lbs per season (cheaper
    # fertilizer) and a common upward trend in yields of 3.5 bushels per season
    # (better seed varieties), which is the season-level confounder this
    # lecture removes. A farm's nitrogen deviations from its typical rate are
    # persistent (AR(1) with coefficient 0.8), as are the errors (0.7), which
    # drives the standard-error discussion in Section 4. True fertilizer
    # effect: +0.30 bushels per acre per pound of nitrogen. Fixed seeds; draw
    # order matters.
    fm_years = np.arange(2020, 2026)
    _n, _T = 150, 6
    _tau = np.arange(_T, dtype=float)
    _r = np.random.default_rng(411)
    fm_z = _r.normal(0.0, 25.0, _n)
    _typical = 150.0 - 0.6 * fm_z + _r.normal(0.0, 20.0, _n)

    _rng = np.random.default_rng(2820)
    _wi = _rng.normal(0.0, 1.0, (_n, _T))
    _wx = np.empty((_n, _T))
    _wx[:, 0] = _wi[:, 0]
    for _t in range(1, _T):
        _wx[:, _t] = 0.8 * _wx[:, _t - 1] + np.sqrt(1 - 0.8**2) * _wi[:, _t]
    fm_fert = _typical[:, None] + 7.0 * _tau[None, :] + 12.0 * _wx
    _inn = _rng.normal(0.0, 1.0, (_n, _T))
    _eps = np.empty((_n, _T))
    _eps[:, 0] = _inn[:, 0]
    for _t in range(1, _T):
        _eps[:, _t] = 0.7 * _eps[:, _t - 1] + np.sqrt(1 - 0.7**2) * _inn[:, _t]
    _eps *= 8.0
    fm_yield = (
        125.0 + 0.30 * fm_fert + fm_z[:, None] + 3.5 * _tau[None, :] + _eps
    )
    # The same six display farms as Lecture 15.
    fm_six = [7, 47, 65, 110, 114, 115]
    fm_tau = _tau
    return fm_fert, fm_six, fm_tau, fm_years, fm_yield, fm_z


@app.cell(hide_code=True)
def _(alt, fm_fert, fm_six, fm_years, fm_yield, mo, np, pd):
    # The marching cloud: the six display farms in fertilizer-yield space,
    # points colored by season, with a light path connecting each farm's six
    # seasons in time order. Every farm's path climbs up and to the right,
    # which is the common-shock problem made visible.
    _t6 = fm_fert[fm_six]
    _f6 = fm_yield[fm_six]
    _long = pd.DataFrame({
        "fert": _t6.ravel(),
        "yield": _f6.ravel(),
        "farm": np.repeat([f"Farm {_i + 1}" for _i in fm_six], 6),
        "season": np.tile(fm_years, 6),
    })
    _xsc = alt.Scale(domain=[110.0, 245.0], nice=False)
    _ysc = alt.Scale(domain=[95.0, 260.0], nice=False)
    _paths = (
        alt.Chart(_long)
        .mark_line(color="#9aa5b1", size=1.2, opacity=0.8, clip=True)
        .encode(
            x=alt.X("fert:Q", scale=_xsc,
                    title="Nitrogen applied (pounds per acre)"),
            y=alt.Y("yield:Q", scale=_ysc,
                    title="Corn yield (bushels per acre)"),
            detail="farm:N",
            order="season:O",
        )
    )
    _pts = (
        alt.Chart(_long)
        .mark_circle(size=54, opacity=0.9, clip=True)
        .encode(
            x=alt.X("fert:Q", scale=_xsc),
            y=alt.Y("yield:Q", scale=_ysc),
            color=alt.Color(
                "season:O",
                scale=alt.Scale(scheme="viridis"),
                legend=alt.Legend(title="Season", orient="right"),
            ),
        )
    )
    _chart = (_paths + _pts).properties(width=560, height=360)
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        "Each point is one of the six farms in one season, colored from 2020 "
        "(dark) to 2025 (yellow); the gray path connects each farm's seasons "
        "in order. "
        "</span>"
    )
    mo.vstack([_chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The problem with running our fixed effects regression from Lecture 15 on these latter seasons is a new omitted variable. Improved seed varieties raised corn yields during the same seasons in which all farms were also applying more nitrogen. Seed quality therefore enters the error term and is positively correlated with fertilizer use. Unlike soil quality, however, seed quality changes from season to season and affects all farms at the same time.

    A farm fixed effect cannot absorb this kind of time-varying omitted variable. The farm fixed effect $\alpha_i$ captures factors that differ across farms but remain fixed over time, not factors that change across seasons. As nitrogen use and seed quality rose together, the regression incorrectly attributed some of the gains in corn yield from improved seeds to fertilizer. This lecture shows how to handle omitted variables that change from season to season but affect all farms in a similar way.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>

    ## 2. Time fixed effects

    Farm fixed effects, $\alpha_i$, capture only omitted factors that remain constant within a farm over time. They therefore cannot account for the improved seed varieties in our example, which change from season to season in a way that's correlated with fertilizer use. However, because improved seed varieties affect all farms in a similar way, we can account for this unobserved factor using a second type of fixed effect.

    In Lecture 15, we separated out from the error term a farm-specific component $Z_i$ that differed across farms but remained fixed over time. Now suppose the error also contains a component $S_t$ that changes across seasons but is common to all farms,

    $$
    Y_{it} = \beta_0 + \beta_1 X_{it} + S_t + Z_i + \nu_{it},
    $$

    where $S_t$ captures the common component of unobserved factors that affect farms in season $t$, such as the quality of available seed varieties or a widespread weather shock. The absence of an $i$ subscript on $S_t$ is important. Within a given season, the same $S_t$ applies to every farm. The remaining error $\nu_{it}$ represents unobserved factors that vary across farms *and* over seasons, such as a pest outbreak on one farm in one particular season.

    We cannot observe $S_t$ directly, but we can account for it in much the same way that farm fixed effects accounted for $Z_i$. Specifically, we can add indicator variables for five of the six seasons to the regression,

    $$
    Y_{it} = \beta_0 + \beta_1 X_{it} + \delta_1 \text{B1}_t + \delta_2 \text{B2}_t + \cdots + \delta_5 \text{B5}_t + Z_i + \nu_{it},
    $$

    where $\text{B1}_t$ equals 1 when $t =$ 2020 and 0 otherwise, $\text{B2}_t$ equals 1 when $t =$ 2021 and 0 otherwise, and so on.<sup><a id="fnref1" href="#fn1">1</a></sup> Note that these season indicators are mutually exclusive, just like the farm indicators from Lecture 15; a single observation can belong to only one season. Rather than writing out all five indicators each time, we can collect them into a single term, $\lambda_t = \delta_1 \text{B1}_t + \delta_2 \text{B2}_t + \cdots + \delta_5 \text{B5}_t$, so that the regression can be written,

    $$
    Y_{it} = \beta_0 + \beta_1 X_{it} + \lambda_t + \underbrace{v_{it}}_{Z_i + \nu_{it}}.
    $$

    The season indicators are called *time fixed effects*, and $\lambda_t$ is a compact way to represent them. The corresponding regression is a *time fixed effects regression*. The error term $v_{it}$ contains everything not captured by the time fixed effects, including the time-invariant farm component $Z_i$ and remaining unobserved factors $\nu_{it}$ that vary across farms and seasons. Time fixed effects allow the average level of corn yields to differ from season to season because of factors that affect all farms in a similar way, whether or not we observe those factors. In our example, they account for the season-by-season yield gains associated with improved seed varieties, so those gains can no longer be misattributed to fertilizer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Two-way fixed effects

    The 2020 to 2025 panel contains two distinct sources of omitted-variable bias. Soil quality differs across farms but remains fixed over time, and it is correlated with nitrogen use. Improved seed varieties, meanwhile, change from season to season and raise corn yields across farms at the same time that nitrogen use is increasing. Farm fixed effects account for the first source of bias, while time fixed effects account for the second. Including both fixed effects gives the *two-way fixed effects regression*,

    $$
    Y_{it} = \beta_0 + \beta_1 X_{it} + \alpha_i + \lambda_t + \nu_{it}.
    $$

    Here $\alpha_i$ captures factors about farm $i$ that remain constant over seasons, while $\lambda_t$ captures factors that change across seasons but affect all farms in a similar way. What remains in the error term, $\nu_{it}$, are unobserved factors that vary across farms and over seasons, such as a pest outbreak, drainage failure, or irrigation upgrade on one farm in a particular year.

    For $\hat{\beta}_1$ to estimate the causal effect of fertilizer, nitrogen use must be unrelated to these remaining unobserved factors after accounting for the farm and time fixed effects. Formally, the first least squares assumption becomes $\mathbb{E}[\nu_{it} \mid X_{it}, \alpha_i, \lambda_t] = \mathbb{E}[\nu_{it} \mid \alpha_i, \lambda_t]$.

    The chart below compares the four regressions we have now considered using the 2020 to 2025 panel: pooled OLS, farm fixed effects, time fixed effects, and two-way fixed effects. The true effect of nitrogen used on corn yield is given by $\beta_1 = 0.30$. The left panel shows the same six farms as Lecture 15 for readability, while the regression estimates and bars use all $150 \times 6 = 900$ observations.
    """)
    return


@app.cell(hide_code=True)
def _(fm_fert, fm_yield):
    # The four estimates of beta_1 on the full 900-observation panel. Each
    # fixed effects regression is the indicator regression of Sections 2 and
    # 3; demeaning within farm and/or season gives the identical slope and is
    # what the code computes.
    def _slope(_x, _y):
        return float((_x * _y).sum() / (_x * _x).sum())

    _x0 = fm_fert - fm_fert.mean()
    _y0 = fm_yield - fm_yield.mean()
    _xe = fm_fert - fm_fert.mean(axis=1, keepdims=True)
    _ye = fm_yield - fm_yield.mean(axis=1, keepdims=True)
    _xt = fm_fert - fm_fert.mean(axis=0, keepdims=True)
    _yt = fm_yield - fm_yield.mean(axis=0, keepdims=True)
    _xw = _xe - _xe.mean(axis=0, keepdims=True)
    _yw = _ye - _ye.mean(axis=0, keepdims=True)

    est_b1 = {
        "Pooled OLS": _slope(_x0, _y0),
        "Farm (entity) fixed effects": _slope(_xe, _ye),
        "Season fixed effects": _slope(_xt, _yt),
        "Two-way fixed effects": _slope(_xw, _yw),
    }
    return (est_b1,)


@app.cell(hide_code=True)
def _(mo):
    est_pick = mo.ui.radio(
        options=[
            "Pooled OLS",
            "Farm (entity) fixed effects",
            "Season fixed effects",
            "Two-way fixed effects",
        ],
        value="Pooled OLS",
        inline=True,
    )
    # The negative top margin pulls the question up toward the preceding
    # paragraph, which otherwise sits a full cell gap away.
    mo.vstack(
        [
            mo.md(
                "<span style='display:block;margin:-0.5rem 0 0;'>"
                "Which regression should we fit?</span>"
            ),
            est_pick,
        ],
        gap=0.5,
    )
    return (est_pick,)


@app.cell(hide_code=True)
def _(alt, est_b1, est_pick, fm_fert, fm_six, fm_years, fm_yield, mo, np, pd):
    _pick = est_pick.value
    _b1 = est_b1[_pick]

    # The regression the current selection fits, shown between the buttons and
    # the chart. Each equation keeps the not-yet-absorbed confounders visible
    # in the error, with braces labeled by the lectures' error symbols:
    # u_it = Z_i + eps_it (Lecture 15), eps_it = S_t + nu_it (Section 2), and
    # v_it (Latin v, distinct from Greek nu) names the season-FE leftover
    # Z_i + nu_it. Rendered as \displaystyle inline math inside a styled block
    # so the gap to the radio above stays tight.
    _eqs = {
        "Pooled OLS":
            r"$\displaystyle Y_{it} = \beta_0 + \beta_1 X_{it} + \underbrace{Z_i + S_t + \nu_{it}}_{u_{it}}$",
        "Farm (entity) fixed effects":
            r"$\displaystyle Y_{it} = \beta_0 + \beta_1 X_{it} + \alpha_i + \underbrace{S_t + \nu_{it}}_{\varepsilon_{it}}$",
        "Season fixed effects":
            r"$\displaystyle Y_{it} = \beta_0 + \beta_1 X_{it} + \lambda_t + \underbrace{Z_i + \nu_{it}}_{v_{it}}$",
        "Two-way fixed effects":
            r"$\displaystyle Y_{it} = \beta_0 + \beta_1 X_{it} + \alpha_i + \lambda_t + \nu_{it}$",
    }
    _eq = mo.md(
        "<span style='display:block;text-align:center;margin:-0.5rem auto 0.2rem;'>"
        + _eqs[_pick] + "</span>"
    )

    _t6 = fm_fert[fm_six]
    _f6 = fm_yield[fm_six]
    _names = [f"Farm {_i + 1}" for _i in fm_six]
    _farm_colors = ["#1f4e79", "#e69138", "#2a9d8f", "#7d5ba6", "#c05b5b", "#5b8bc0"]

    _xsc = alt.Scale(domain=[110.0, 245.0], nice=False)
    _ysc = alt.Scale(domain=[95.0, 260.0], nice=False)
    _xax = alt.X("fert:Q", scale=_xsc, title="Nitrogen applied (pounds per acre)")
    _yax = alt.Y("yield:Q", scale=_ysc, title="Corn yield (bushels per acre)")

    _long = pd.DataFrame({
        "fert": _t6.ravel(),
        "yield": _f6.ravel(),
        "farm": np.repeat(_names, 6),
        "season": np.tile(fm_years, 6),
    })

    # Lines use the full-panel slope for the chosen regression; each line is
    # anchored at its own group's mean point among the six displayed farms.
    _layers = []
    if _pick == "Pooled OLS":
        _layers.append(
            alt.Chart(_long)
            .mark_circle(size=40, opacity=0.5, color="#6b7280", clip=True)
            .encode(x=_xax, y=_yax)
        )
        _a = float(_f6.mean() - _b1 * _t6.mean())
        _gx = np.array([float(_t6.min()) - 3.0, float(_t6.max()) + 3.0])
        _layers.append(
            alt.Chart(pd.DataFrame({"fert": _gx, "yield": _a + _b1 * _gx}))
            .mark_line(color="#111827", size=4, clip=True)
            .encode(x=_xax, y=_yax)
        )
    elif _pick == "Season fixed effects":
        _layers.append(
            alt.Chart(_long)
            .mark_circle(size=40, opacity=0.6, clip=True)
            .encode(
                x=_xax, y=_yax,
                color=alt.Color(
                    "season:O",
                    scale=alt.Scale(scheme="viridis"),
                    legend=alt.Legend(title="Season", orient="right"),
                ),
            )
        )
        for _t in range(6):
            _a = float(_f6[:, _t].mean() - _b1 * _t6[:, _t].mean())
            _gx = np.array([float(_t6[:, _t].min()) - 4.0,
                            float(_t6[:, _t].max()) + 4.0])
            _layers.append(
                alt.Chart(pd.DataFrame({
                    "fert": _gx, "yield": _a + _b1 * _gx,
                    "season": [fm_years[_t]] * 2,
                }))
                .mark_line(size=2, clip=True)
                .encode(
                    x=_xax, y=_yax,
                    color=alt.Color("season:O", scale=alt.Scale(scheme="viridis"),
                                    legend=None),
                )
            )
    else:
        # Farm fixed effects and two-way fixed effects: one line per farm with
        # the chosen regression's common slope (for the two-way model the
        # season effects are evaluated at their average).
        _layers.append(
            alt.Chart(_long)
            .mark_circle(size=40, opacity=0.6, clip=True)
            .encode(
                x=_xax, y=_yax,
                color=alt.Color(
                    "farm:N",
                    scale=alt.Scale(domain=_names, range=_farm_colors),
                    # Right-hand legend like the season branch, so the chart
                    # width does not jump between selections. The labels drop
                    # the "Farm " prefix, keeping the legend as narrow as the
                    # season years.
                    legend=alt.Legend(
                        title="Farm", orient="right",
                        labelExpr='replace(datum.label, "Farm ", "")',
                    ),
                ),
            )
        )
        for _j in range(6):
            _a = float(_f6[_j].mean() - _b1 * _t6[_j].mean())
            _gx = np.array([float(_t6[_j].min()) - 4.0,
                            float(_t6[_j].max()) + 4.0])
            _layers.append(
                alt.Chart(pd.DataFrame({"fert": _gx, "yield": _a + _b1 * _gx,
                                        "farm": [_names[_j]] * 2}))
                .mark_line(size=2.5, clip=True)
                .encode(
                    x=_xax, y=_yax,
                    color=alt.Color("farm:N",
                                    scale=alt.Scale(domain=_names,
                                                    range=_farm_colors),
                                    legend=None),
                )
            )
    _main = alt.layer(*_layers).properties(width=430, height=340)

    _order = ["Pooled OLS", "Farm (entity) fixed effects",
              "Season fixed effects", "Two-way fixed effects"]
    _short = {"Pooled OLS": "Pooled",
              "Farm (entity) fixed effects": "Farm FE",
              "Season fixed effects": "Season FE",
              "Two-way fixed effects": "Two-way"}
    _bsc = alt.Scale(domain=[-0.4, 0.8], nice=False)
    _bars_df = pd.DataFrame({
        "est": [_short[_k] for _k in _order],
        "b1": [est_b1[_k] for _k in _order],
        "labely": [est_b1[_k] + (0.05 if est_b1[_k] >= 0 else -0.06)
                   for _k in _order],
        "chosen": [_k == _pick for _k in _order],
        "label": [f"{est_b1[_k]:+.2f}" for _k in _order],
    })
    _bx = alt.X("est:N", title=None,
                sort=[_short[_k] for _k in _order],
                axis=alt.Axis(labelAngle=-30))
    _by = alt.Y("b1:Q", scale=_bsc, title="Estimated effect of nitrogen")
    _bars = (
        alt.Chart(_bars_df)
        .mark_bar(clip=True)
        .encode(
            x=_bx, y=_by,
            color=alt.condition(
                alt.datum.chosen, alt.value("#1f4e79"), alt.value("#c3ccd6")
            ),
        )
    )
    _blabels = (
        alt.Chart(_bars_df)
        .mark_text(fontSize=10.5, color="#374151", baseline="middle")
        .encode(x=_bx, y=alt.Y("labely:Q", scale=_bsc), text="label:N")
    )
    _rule = (
        alt.Chart(pd.DataFrame({"b1": [0.30]}))
        .mark_rule(color="orange", strokeDash=[6, 4], size=2)
        .encode(y=alt.Y("b1:Q", scale=_bsc))
    )
    # Label the dashed line on the chart itself, in its color, hugging the
    # right edge where no bar reaches above the line.
    _rule_label = (
        alt.Chart(pd.DataFrame({"b1": [0.30], "label": ["True effect"]}))
        .mark_text(color="orange", fontSize=9.5, align="right", dy=-6)
        .encode(
            x=alt.value(146),
            y=alt.Y("b1:Q", scale=_bsc),
            text="label:N",
        )
    )
    _side = (_bars + _blabels + _rule + _rule_label).properties(
        width=150, height=340,
    )
    _chart = alt.hconcat(_main, _side).resolve_scale(color="independent")
    if _pick == "Pooled OLS":
        # The pooled view has no legend, so pad the figure's right edge by
        # one legend width to keep the overall chart width fixed across
        # selections. Vega-lite only allows padding on the top-level chart,
        # never inside the hconcat, and an explicit padding object zeroes
        # unspecified sides, so restore the 5px default on the others.
        _chart = _chart.properties(
            padding={"left": 5, "top": 5, "bottom": 5, "right": 75},
        )

    if _pick == "Pooled OLS":
        _msg = (
            f"One intercept for everything. Both confounders are live: soil "
            f"quality pulls the estimate down, the seed-genetics trend pushes "
            f"it up, and the net is {_b1:+.2f}, as if fertilizer did nothing. "
            f"The dashed orange line marks the true effect, +0.30."
        )
    elif _pick == "Farm (entity) fixed effects":
        _msg = (
            f"One intercept per farm absorbs soil quality, but the "
            f"seed-genetics trend remains in the error. Within every farm, "
            f"yields and nitrogen rose together, so the estimate overshoots "
            f"to {_b1:+.2f}: fertilizer takes credit for the new seed "
            f"varieties."
        )
    elif _pick == "Season fixed effects":
        _msg = (
            f"One intercept per season absorbs the seed-genetics trend (each "
            f"season's cloud slides up the chart), but soil quality is back "
            f"in the error, and comparisons across farms drag the estimate "
            f"down to {_b1:+.2f}, the same problem as Lecture 15's "
            f"cross-sections."
        )
    else:
        _msg = (
            f"Farm intercepts absorb soil quality and season intercepts "
            f"absorb the seed-genetics trend. The estimate, {_b1:+.2f}, "
            f"lands on the true effect of +0.30. Each kind of fixed effect "
            f"removes only its own kind of confounder, so the model needs "
            f"both."
        )
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:600px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_eq, _chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Standard errors in panel data

    Estimating $\beta_1$ is only half the job; we also need its standard error. Recall from Lecture 6 that the usual standard error formulas require the observations to be i.i.d. draws from the same population. In a panel, that assumption deserves suspicion, because the same farm appears in the data six times.

    Knowing a farm's nitrogen use in 2020 tells us a lot about its likely nitrogen use in 2021, since fertilizer habits persist. The same holds for the unobserved factors in the error term. A drainage problem, a pest infestation, or an irrigation upgrade that affects a farm's yield in one season tends to still be at work the next. A variable with this property is *autocorrelated*, also called *serially correlated*. Formally, $M_{it}$ is autocorrelated if $\text{corr}(M_{it}, M_{i,t+j}) \neq 0$ for some $j \neq 0$.

    Autocorrelation does not bias $\hat{\beta}_1$. The problem is the standard errors. The usual formula counts every observation as an independent piece of information, but six correlated observations on the same farm carry less information than six independent ones. The usual standard errors are therefore invalid in panels with autocorrelation, and they typically overstate precision.

    The solution is to use *clustered standard errors*, which allow the errors to be correlated in any way *within* an entity, here a farm, while assuming the errors are independent *across* entities. Statistical software makes clustering a one-option change to the regression command.

    The demonstration below shows why clustering matters. It re-simulates our 2020 to 2025 panel many times, each time drawing errors whose within-farm persistence you control with the slider, and estimates the two-way fixed effects regression on each simulated panel. The first bar is the actual spread of $\hat{\beta}_1$ across the simulated panels, the honest measure of its sampling uncertainty. The other two bars show the average standard error that the conventional formula and the clustered formula report.
    """)
    return


@app.cell(hide_code=True)
def _(fm_fert, fm_tau, fm_z, np):
    # Pre-drawn innovations for the standard-error demo: 300 simulated panels.
    # The slider only changes how these fixed innovations are combined into an
    # AR(1), so dragging it never redraws the underlying randomness. The
    # within-transformed regressor is fixed across simulations.
    ac_innov = np.random.default_rng(777).normal(0.0, 1.0, (300, 150, 6))
    _xe = fm_fert - fm_fert.mean(axis=1, keepdims=True)
    ac_xt = _xe - _xe.mean(axis=0, keepdims=True)
    ac_signal = (
        125.0 + 0.30 * fm_fert[None, :, :]
        + fm_z[None, :, None]
        + 3.5 * fm_tau[None, None, :]
    )
    return ac_innov, ac_signal, ac_xt


@app.cell(hide_code=True)
def _(mo):
    ac_rho = mo.ui.slider(
        start=0.0, stop=0.9, step=0.1, value=0.0,
        label="Within-farm persistence of the errors (ρ)",
        show_value=True,
    )
    ac_rho
    return (ac_rho,)


@app.cell(hide_code=True)
def _(ac_innov, ac_rho, ac_signal, ac_xt, alt, mo, np, pd):
    _rho = float(ac_rho.value)
    _R, _n, _T = ac_innov.shape

    # Build AR(1) errors from the fixed innovations, then estimate the two-way
    # fixed effects regression on each of the 300 simulated panels. Demeaning
    # within farm and season reproduces the indicator regression's slope; the
    # conventional variance uses the indicator regression's degrees of freedom
    # (900 observations, 156 coefficients).
    _eps = np.empty((_R, _n, _T))
    _eps[:, :, 0] = ac_innov[:, :, 0]
    for _t in range(1, _T):
        _eps[:, :, _t] = (
            _rho * _eps[:, :, _t - 1]
            + np.sqrt(1.0 - _rho**2) * ac_innov[:, :, _t]
        )
    _eps *= 8.0

    _y = ac_signal + _eps
    _yt = _y - _y.mean(axis=2, keepdims=True)
    _yt = _yt - _yt.mean(axis=1, keepdims=True)
    _sxx = float((ac_xt * ac_xt).sum())
    _b1 = (ac_xt[None] * _yt).sum(axis=(1, 2)) / _sxx
    _u = _yt - _b1[:, None, None] * ac_xt[None]

    _dof = _n * _T - (2 + (_n - 1) + (_T - 1))
    _conv = np.sqrt((_u * _u).sum(axis=(1, 2)) / _dof / _sxx)
    _clus = np.sqrt(
        _n / (_n - 1)
        * ((ac_xt[None] * _u).sum(axis=2) ** 2).sum(axis=1)
        / _sxx**2
    )

    _truth = float(_b1.std())
    _c1 = float(_conv.mean())
    _c2 = float(_clus.mean())

    _bars_df = pd.DataFrame({
        "which": ["Actual spread of estimates", "Conventional SE",
                  "Clustered SE"],
        "se": [_truth, _c1, _c2],
        "label": [f"{_truth:.3f}", f"{_c1:.3f}", f"{_c2:.3f}"],
    })
    _bx = alt.X(
        "which:N", title=None,
        sort=["Actual spread of estimates", "Conventional SE", "Clustered SE"],
        axis=alt.Axis(labelAngle=-20),
    )
    _by = alt.Y("se:Q", scale=alt.Scale(domain=[0.0, 0.055], nice=False),
                title="Sampling uncertainty of the estimate")
    _bars = (
        alt.Chart(_bars_df)
        .mark_bar(clip=True, size=52)
        .encode(
            x=_bx, y=_by,
            color=alt.Color(
                "which:N",
                scale=alt.Scale(
                    domain=["Actual spread of estimates", "Conventional SE",
                            "Clustered SE"],
                    range=["#374151", "#1f4e79", "#e69138"],
                ),
                legend=None,
            ),
        )
    )
    _labels = (
        alt.Chart(_bars_df)
        .mark_text(dy=-7, fontSize=11, color="#374151")
        .encode(x=_bx, y=_by, text="label:N")
    )
    _chart = (_bars + _labels).properties(width=340, height=300)

    if _rho == 0.0:
        _msg = (
            f"With ρ = 0 the errors are independent across seasons, the "
            f"i.i.d. assumption holds, and all three bars agree: the "
            f"conventional formula ({_c1:.3f}) and the clustered formula "
            f"({_c2:.3f}) both match the actual spread ({_truth:.3f}). Drag "
            f"ρ upward to make each farm's errors persist."
        )
    elif _c1 / _truth > 0.9:
        _msg = (
            f"With ρ = {_rho:.1f}, persistence is mild. The conventional SE "
            f"({_c1:.3f}) is starting to slip below the actual spread "
            f"({_truth:.3f}), while the clustered SE ({_c2:.3f}) stays on "
            f"target."
        )
    else:
        _msg = (
            f"With ρ = {_rho:.1f}, the conventional formula reports "
            f"{_c1:.3f} when the actual spread of the estimates is "
            f"{_truth:.3f}: it overstates precision by about "
            f"{100 * (1 - _c1 / _truth):.0f}%, so its confidence intervals "
            f"are too narrow and its t-statistics too large. The clustered "
            f"SE ({_c2:.3f}) tracks the truth, because it lets each farm's "
            f"six errors be correlated however they like."
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
    Our own farm panel was simulated with persistent errors (ρ = 0.7), so clustering is not optional there. On the two-way fixed effects regression, the conventional standard error is 0.031 while the clustered standard error is 0.038. Reporting the conventional number would claim more precision than we actually have.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Reading a panel regression table

    Applied papers report panel regressions the way Lecture 10 taught you to read them: several columns, one specification each, with rows at the bottom announcing which fixed effects are included. The table below runs the full sequence on our 900 observations from 2020 to 2025.
    """)
    return


@app.cell(hide_code=True)
def _(fm_fert, fm_yield, np):
    # The four columns of Section 5: pooled OLS, farm FE, farm + season FE,
    # and farm + season FE with standard errors clustered by farm. Each
    # regression is estimated as the indicator regression via least squares,
    # so the R-squared and degrees of freedom come from the full design
    # matrix.
    _n, _T = fm_yield.shape
    _y = fm_yield.ravel()
    _x = fm_fert.ravel()
    _fid = np.repeat(np.arange(_n), _T)
    _tid = np.tile(np.arange(_T), _n)

    def _design(_farm_fe, _season_fe):
        _cols = [np.ones(_n * _T), _x]
        if _farm_fe:
            for _i in range(1, _n):
                _cols.append((_fid == _i).astype(float))
        if _season_fe:
            for _t in range(1, _T):
                _cols.append((_tid == _t).astype(float))
        return np.column_stack(_cols)

    def _fit(_farm_fe, _season_fe, _cluster):
        _X = _design(_farm_fe, _season_fe)
        _k = _X.shape[1]
        _beta, *_rest = np.linalg.lstsq(_X, _y, rcond=None)
        _u = _y - _X @ _beta
        _ssr = float(_u @ _u)
        _tss = float(((_y - _y.mean()) ** 2).sum())
        _XtXi = np.linalg.inv(_X.T @ _X)
        if _cluster:
            # Cluster-robust variance: sum the score outer products farm by
            # farm, with the standard G/(G-1) small-sample factor.
            _meat = np.zeros((_k, _k))
            for _i in range(_n):
                _sel = _fid == _i
                _g = _X[_sel].T @ _u[_sel]
                _meat += np.outer(_g, _g)
            _V = _XtXi @ _meat @ _XtXi * (_n / (_n - 1))
        else:
            _V = _XtXi * _ssr / (_n * _T - _k)
        return {
            "b1": float(_beta[1]),
            "se1": float(np.sqrt(_V[1, 1])),
            "b0": float(_beta[0]),
            "se0": float(np.sqrt(_V[0, 0])),
            "r2": 1.0 - _ssr / _tss,
        }

    tbl_fits = [
        _fit(False, False, False),
        _fit(True, False, False),
        _fit(True, True, False),
        _fit(True, True, True),
    ]
    tbl_flags = [
        ("Farm fixed effects", ["No", "Yes", "Yes", "Yes"]),
        ("Season fixed effects", ["No", "No", "Yes", "Yes"]),
        ("Clustered SEs (by farm)", ["No", "No", "No", "Yes"]),
    ]
    return tbl_fits, tbl_flags


@app.cell(hide_code=True)
def _(mo, tbl_fits, tbl_flags):
    def _stars(_t):
        _a = abs(_t)
        return "***" if _a > 2.576 else "**" if _a > 1.96 else "*" if _a > 1.645 else ""

    _pad = "padding:3px 15px;text-align:center;"

    def _coef_cell(_b, _se):
        _inner = (
            f"{_b:+.3f}{_stars(_b / _se)}"
            f"<br><span style='color:#6b7280;'>({_se:.3f})</span>"
        )
        return f"<td style='{_pad}'>{_inner}</td>"

    _rows = []
    _rows.append(
        "<tr><td style='padding:3px 15px;text-align:left;'>Nitrogen (lbs per acre)</td>"
        + "".join(_coef_cell(_f["b1"], _f["se1"]) for _f in tbl_fits)
        + "</tr>"
    )
    _const_cells = [_coef_cell(tbl_fits[0]["b0"], tbl_fits[0]["se0"])]
    _const_cells += [f"<td style='{_pad}'></td>"] * 3
    _rows.append(
        "<tr><td style='padding:3px 15px;text-align:left;'>Constant</td>"
        + "".join(_const_cells) + "</tr>"
    )

    _top = "border-top:1px solid rgba(120,120,120,0.6);"
    for _j, (_label, _vals) in enumerate(tbl_flags):
        _b = _top if _j == 0 else ""
        _rows.append(
            f"<tr><td style='padding:3px 15px;text-align:left;{_b}'>{_label}</td>"
            + "".join(f"<td style='{_pad}{_b}'>{_v}</td>" for _v in _vals)
            + "</tr>"
        )
    _rows.append(
        "<tr><td style='padding:3px 15px;text-align:left;'>Observations</td>"
        + "".join(f"<td style='{_pad}'>900</td>" for _f in tbl_fits)
        + "</tr>"
    )
    _rows.append(
        "<tr><td style='padding:3px 15px;text-align:left;'>R²</td>"
        + "".join(f"<td style='{_pad}'>{_f['r2']:.3f}</td>" for _f in tbl_fits)
        + "</tr>"
    )

    _rule = "2px solid rgba(120,120,120,0.9)"
    _colhdr = "".join(
        f"<th style='{_pad}font-weight:600;'>({_i})</th>" for _i in range(1, 5)
    )
    _table = (
        "<div style='overflow-x:auto;text-align:center;'>"
        f"<table style='display:inline-table;width:auto;border-collapse:collapse;"
        f"margin:1rem auto;font-size:0.9rem;line-height:1.25;text-align:left;"
        f"border-top:{_rule};border-bottom:{_rule};'>"
        "<thead>"
        "<tr><td></td><td colspan='4' style='text-align:center;"
        "padding:5px 0 3px;font-weight:600;'>Dependent variable: corn yield "
        "(bushels per acre)</td></tr>"
        "<tr><td style='border-bottom:1px solid rgba(120,120,120,0.6);'></td>"
        "<td colspan='4' style='border-bottom:1px solid rgba(120,120,120,0.6);'></td></tr>"
        f"<tr><td></td>{_colhdr}</tr>"
        "</thead>"
        f"<tbody>{''.join(_rows)}</tbody>"
        "</table></div>"
    )
    _note = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:620px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        "Standard errors in parentheses. One star marks statistical significance "
        "at the 10% level, two at the 5% level, and three at the 1% level. "
        "Farm and season indicator coefficients are estimated but not reported."
        "</span>"
    )
    mo.vstack([mo.md(_table), _note])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read the table column by column, asking of each movement in the coefficient: which confounder did this column remove?

    * **Column (1), pooled OLS**, estimates $-0.04$, statistically indistinguishable from zero. Soil quality pulls the estimate down and the seed-genetics trend pushes it up, and the two roughly cancel: fertilizer looks useless.
    * **Column (2)** adds farm fixed effects. The estimate jumps to $+0.63$ as soil quality is absorbed, but it now overshoots: within every farm, the new seed varieties raised yields in the same seasons nitrogen use rose, and fertilizer takes the credit.
    * **Column (3)** adds season fixed effects on top. The estimate settles at $+0.30$, the true effect, since each season's intercept soaks up that season's seed genetics and prices. Comparing columns (2) and (3) is the Section 3 lesson in table form.
    * **Column (4)** reports the same regression as column (3); only the standard error changes, from 0.031 to 0.038, once we allow each farm's errors to be correlated across seasons. The coefficient is unchanged, the t-statistic shrinks, and the confidence interval widens honestly. The estimate remains statistically significant at the 1% level.

    Also glance at the R² row with Lecture 10's warning in mind: the fixed effects push the R² from 0.00 to above 0.95, but almost all of that fit comes from the 154 intercepts, not from nitrogen. A large R² is no evidence that a coefficient is causal.

    This four-column progression, pooled, entity effects, two-way effects, clustered standard errors, is the standard way applied economists present panel evidence. You now know how to read every row of it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** time fixed effect, two-way fixed effects regression, "
            "autocorrelated, serially correlated, clustered standard "
            "errors.\n\n"

            "**Concepts:** why an entity's fixed effect cannot absorb factors "
            "that change over time for all entities together, season "
            "indicators collapsing into a time fixed effect, the two-way "
            "model absorbing both time-invariant entity factors and common "
            "period shocks, the condition under which the two-way estimate is "
            "causal, autocorrelation of the regressor and errors within an "
            "entity, why autocorrelation invalidates the usual standard "
            "errors without biasing the estimate, clustering standard errors "
            "at the entity level, and reading a four-column panel regression "
            "table."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** We leave out the indicator for the 2025 season for the same reason we left out the indicator for Farm 150 in Lecture 15. The regression already contains the intercept $\beta_0$. If we included all six season indicators, they would add up to 1 for every observation and would therefore be an exact linear function of the intercept. The regression would exhibit perfect multicollinearity, violating the fourth OLS assumption from Lecture 9. Omitting indicators for Farm 150 and Year 2025, $\beta_0$ represents the expected corn yield for Farm 150 in 2025 when no nitrogen is applied. $\beta_0 + \delta_1$ is the expected yield for the same farm in 2020 when no nitrogen is applied. Thus, $\delta_1$ measures how much higher or lower the common level of corn yields was in 2020 than in 2025. The other $\delta$ coefficients have the same interpretation for the remaining seasons. <a href="#fnref1" title="Back to text">&#8617;</a></span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec15PanelDataI.html" target="_self">← Lecture 15</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec17BinaryDependentVariables.html" target="_self">Lecture 17 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
