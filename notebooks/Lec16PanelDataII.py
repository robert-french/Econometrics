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
    app_title="Lecture 16: Panel Data II: Time Effects, Two-Way Fixed Effects, and Clustered Standard Errors",
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
            mo.md("Panel Data II: Time Effects, Two-Way Fixed Effects, and Clustered Standard Errors"),
            mo.nav_menu(
                {
                    "#sec1": "1. When entity fixed effects are not enough",
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
    # Lecture 16: Panel Data II: Time Effects, Two-Way Fixed Effects, and Clustered Standard Errors
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Same-page (#fragment) links must stay plain markdown links with no inline
    # style and no styled wrapper; see the note in Lec14.
    mo.md(r"""
    ## Contents

    [1. When entity fixed effects are not enough](#sec1)<br>
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
    ## 1. When entity fixed effects are not enough

    Consider again the regression of state traffic fatalities on state beer taxes between 1982 and 1988 from Lecture 15,

    $$
    Y_{i,t} = \beta_0 + \beta_1 X_{i,t} + u_{i,t},
    $$

    where $Y_{i,t}$ is the fatality rate in state $i$ and year $t$, measured in deaths per 10,000 residents, $X_{i,t}$ is the state's beer tax in dollars per case, and $u_{i,t}$ collects the unobserved factors that influence fatalities. Lecture 15 ended with a warning: entity fixed effects absorb only the factors that are constant over time within a state. Anything that changes over the sample period stays in the error term.

    Our panel has exactly this problem, and so did the real 1980s. National traffic fatalities declined over 1982 to 1988 while states' beer taxes rose on average. The charts below show the yearly averages across our 50 states:
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # The same 50-state panel as Lecture 15 (identical seed and draw order),
    # with one addition: a nationwide downward trend in fatalities of 0.025
    # deaths per 10,000 per year, common to all states. Beer taxes drift up
    # over the sample while their cross-state spread compresses; the state
    # confounder pn_z ties drinking culture to tax levels; and the errors are
    # persistent within a state (AR(1) with coefficient 0.7), which drives the
    # standard-error discussion in Section 4. True tax effect: -0.45.
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
    pn_fat = (
        2.40 - 0.45 * pn_tax + pn_z[:, None] - 0.025 * _tau[None, :] + _eps
    )
    pn_tau = _tau
    return pn_fat, pn_states, pn_tau, pn_tax, pn_years, pn_z


@app.cell(hide_code=True)
def _(alt, mo, pd, pn_fat, pn_tax, pn_years):
    _means = pd.DataFrame({
        "year": pn_years,
        "fat": pn_fat.mean(axis=0),
        "tax": pn_tax.mean(axis=0),
    })
    _left = (
        alt.Chart(_means)
        .mark_line(color="#1f4e79", size=3, point=alt.OverlayMarkDef(color="#1f4e79"))
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y(
                "fat:Q",
                scale=alt.Scale(domain=[1.45, 2.0], nice=False),
                title="Average fatality rate (per 10,000)",
            ),
        )
        .properties(width=260, height=260)
    )
    _right = (
        alt.Chart(_means)
        .mark_line(color="#e69138", size=3, point=alt.OverlayMarkDef(color="#e69138"))
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y(
                "tax:Q",
                scale=alt.Scale(domain=[1.1, 1.6], nice=False),
                title="Average beer tax (dollars per case)",
            ),
        )
        .properties(width=260, height=260)
    )
    _chart = alt.hconcat(_left, _right)
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        "Averages across the 50 states in each year. Fatalities drift down "
        "while beer taxes drift up."
        "</span>"
    )
    mo.vstack([_chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Suppose the national decline in fatalities happened for reasons unrelated to beer taxes: federal safety regulations tightened, cars gained airbags and better brakes, and attitudes toward drunk driving shifted nationwide. These forces vary over time but hit all states together. A state fixed effect cannot absorb them, because $\alpha_i$ is one number per state, the same in 1982 as in 1988.

    The result is omitted variable bias in a new disguise. Within every state, fatalities fell while beer taxes rose, so the two move in opposite directions year by year regardless of any causal effect. A regression with only entity fixed effects conflates the nationwide safety trend with the effect of the tax. On our panel it estimates $\hat{\beta}_1 = -0.78$, far more negative than the true effect of $-0.45$ built into the simulation. The tax looks nearly twice as lifesaving as it is, because it takes credit for airbags.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Time fixed effects

    The fix mirrors Lecture 15, with the roles of state and year swapped. Decompose the error into a component that varies over time but not across states, and a remainder:

    $$
    Y_{i,t} = \beta_0 + \beta_1 X_{i,t} + \underbrace{S_t + \nu_{i,t}}_{u_{i,t}},
    $$

    where $S_t$ collects the unobserved factors that are common to all states in year $t$ (note that $S_t$ has no $i$ subscript). In our example, $S_t$ contains:

    * changes in federal vehicle safety regulations,
    * changes in vehicle safety features,
    * shifts in nationwide attitudes toward drinking and driving.

    We cannot measure $S_t$ directly, but we can give each time period its own binary variable. Let $\text{B2}_t$ equal 1 when $t$ is the second period (1983) and 0 otherwise, and likewise up to $\text{B}T_t$ for the last period:

    $$
    Y_{i,t} = \beta_0 + \beta_1 X_{i,t} + \delta_2\text{B2}_t + \delta_3\text{B3}_t + \dots + \delta_T\text{B}T_t + \nu_{i,t}.
    $$

    The period indicators are mutually exclusive, one per year, so exactly as in Lecture 15 we can collapse them into a single term:

    $$
    Y_{i,t} = \beta_0 + \beta_1 X_{i,t} + \lambda_t + \nu_{i,t},
    \qquad \text{where} \qquad
    \lambda_t = \delta_2\text{B2}_t + \delta_3\text{B3}_t + \dots + \delta_T\text{B}T_t.
    $$

    This is the *time fixed effects regression model* for panel data. Everything we learned about entity fixed effects carries over with $i$ and $t$ swapped:

    * $\lambda_2, \dots, \lambda_T$ are unknown intercepts to estimate, one per time period.
    * $\lambda_t$ controls for all factors, observed and unobserved, that are common to every state in period $t$.
    * The dummy variable trap appears again: we cannot include all $T$ period effects and the constant $\beta_0$, so we omit one period (the *base period*) and interpret each $\lambda_t$ as the mean difference in $Y$ relative to it. Alternatively, drop $\beta_0$ and keep all $T$ period effects.
    * Additional time-varying regressors $X_{1,i,t}, \dots, X_{k,i,t}$ can be added as usual.

    In our panel, the estimated $\lambda_t$ trace out the national decline: each year's intercept sits below the last, absorbing the nationwide drop in fatalities that has nothing to do with any single state's tax policy.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Two-way fixed effects

    Our panel suffers from both problems at once. Some omitted factors differ across states but are constant over time, like drinking culture: the $Z_i$ of Lecture 15. Others change over time but are common to all states, like federal safety standards: the $S_t$ of Section 2. The error term contains both,

    $$
    u_{i,t} = Z_i + S_t + \epsilon_{i,t},
    $$

    so the model needs both kinds of intercepts. Including entity fixed effects *and* time fixed effects gives the *two-way fixed effects model*:

    $$
    Y_{i,t} = \beta_0 + \beta_1 X_{i,t} + \alpha_i + \lambda_t + \epsilon_{i,t}.
    $$

    Here $\alpha_i$ absorbs the time-invariant differences across states and $\lambda_t$ absorbs the year shocks common to all states. The estimate $\hat{\beta}_1$ is causal if

    $$
    \mathbb{E}[\epsilon_{i,t} \mid X_{i,t}, \alpha_i, \lambda_t] = \mathbb{E}[\epsilon_{i,t} \mid \alpha_i, \lambda_t],
    $$

    that is, if the beer tax is unrelated to whatever unobserved factors remain after the state and year intercepts have done their work: the factors that vary both over time *and* across states, such as one state toughening its own drunk-driving enforcement in one particular year.

    The chart below puts the four estimators side by side on our panel, where the true effect is $\beta_1 = -0.45$. The left panel shows six of the fifty states; the estimates and the bars use all 350 observations.
    """)
    return


@app.cell(hide_code=True)
def _(np, pn_fat, pn_tax):
    # The four estimates of beta_1 on the full 350-observation panel. Each
    # fixed-effects regression is the dummy regression of Sections 2 and 3;
    # demeaning within state and/or year gives the identical slope and is what
    # the code computes.
    def _slope(_x, _y):
        return float((_x * _y).sum() / (_x * _x).sum())

    _x0 = pn_tax - pn_tax.mean()
    _y0 = pn_fat - pn_fat.mean()
    _xe = pn_tax - pn_tax.mean(axis=1, keepdims=True)
    _ye = pn_fat - pn_fat.mean(axis=1, keepdims=True)
    _xt = pn_tax - pn_tax.mean(axis=0, keepdims=True)
    _yt = pn_fat - pn_fat.mean(axis=0, keepdims=True)
    _xw = _xe - _xe.mean(axis=0, keepdims=True)
    _yw = _ye - _ye.mean(axis=0, keepdims=True)

    est_b1 = {
        "Pooled OLS": _slope(_x0, _y0),
        "State fixed effects": _slope(_xe, _ye),
        "Year fixed effects": _slope(_xt, _yt),
        "Two-way fixed effects": _slope(_xw, _yw),
    }
    return (est_b1,)


@app.cell(hide_code=True)
def _(mo):
    est_pick = mo.ui.radio(
        options=[
            "Pooled OLS",
            "State fixed effects",
            "Year fixed effects",
            "Two-way fixed effects",
        ],
        value="Pooled OLS",
        label="Estimator",
        inline=True,
    )
    est_pick
    return (est_pick,)


@app.cell(hide_code=True)
def _(alt, est_b1, est_pick, mo, np, pd, pn_fat, pn_states, pn_tax, pn_years):
    _pick = est_pick.value
    _b1 = est_b1[_pick]

    _six = ["CA", "FL", "IL", "NY", "TX", "WI"]
    _idx = [pn_states.index(_s) for _s in _six]
    _t6 = pn_tax[_idx]
    _f6 = pn_fat[_idx]
    _state_colors = ["#1f4e79", "#e69138", "#2a9d8f", "#7d5ba6", "#c05b5b", "#5b8bc0"]

    _xsc = alt.Scale(domain=[0.7, 1.9], nice=False)
    _ysc = alt.Scale(domain=[0.9, 2.5], nice=False)
    _xax = alt.X("tax:Q", scale=_xsc, title="Beer tax (dollars per case)")
    _yax = alt.Y("fat:Q", scale=_ysc, title="Fatality rate (per 10,000)")

    _long = pd.DataFrame({
        "tax": _t6.ravel(),
        "fat": _f6.ravel(),
        "state": np.repeat(_six, 7),
        "year": np.tile(pn_years, 6),
    })

    # Lines use the full-panel slope for the chosen estimator; each line is
    # anchored at its own group's mean point among the six displayed states.
    _layers = []
    if _pick == "Pooled OLS":
        _layers.append(
            alt.Chart(_long)
            .mark_circle(size=40, opacity=0.5, color="#6b7280", clip=True)
            .encode(x=_xax, y=_yax)
        )
        _a = float(_f6.mean() - _b1 * _t6.mean())
        _gx = np.array([float(_t6.min()) - 0.05, float(_t6.max()) + 0.05])
        _layers.append(
            alt.Chart(pd.DataFrame({"tax": _gx, "fat": _a + _b1 * _gx}))
            .mark_line(color="#111827", size=4, clip=True)
            .encode(x=_xax, y=_yax)
        )
    elif _pick == "Year fixed effects":
        _layers.append(
            alt.Chart(_long)
            .mark_circle(size=40, opacity=0.6, clip=True)
            .encode(
                x=_xax, y=_yax,
                color=alt.Color(
                    "year:O",
                    scale=alt.Scale(scheme="viridis"),
                    legend=alt.Legend(title="Year", orient="right"),
                ),
            )
        )
        for _t in range(7):
            _a = float(_f6[:, _t].mean() - _b1 * _t6[:, _t].mean())
            _gx = np.array([float(_t6[:, _t].min()) - 0.06,
                            float(_t6[:, _t].max()) + 0.06])
            _layers.append(
                alt.Chart(pd.DataFrame({
                    "tax": _gx, "fat": _a + _b1 * _gx,
                    "year": [pn_years[_t]] * 2,
                }))
                .mark_line(size=2, clip=True)
                .encode(
                    x=_xax, y=_yax,
                    color=alt.Color("year:O", scale=alt.Scale(scheme="viridis"),
                                    legend=None),
                )
            )
    else:
        # State fixed effects and two-way fixed effects: one line per state
        # with the chosen estimator's common slope (for the two-way model the
        # year effects are evaluated at their average).
        _layers.append(
            alt.Chart(_long)
            .mark_circle(size=40, opacity=0.6, clip=True)
            .encode(
                x=_xax, y=_yax,
                color=alt.Color(
                    "state:N",
                    scale=alt.Scale(domain=_six, range=_state_colors),
                    legend=alt.Legend(title=None, orient="top"),
                ),
            )
        )
        for _j in range(6):
            _a = float(_f6[_j].mean() - _b1 * _t6[_j].mean())
            _gx = np.array([float(_t6[_j].min()) - 0.06,
                            float(_t6[_j].max()) + 0.06])
            _layers.append(
                alt.Chart(pd.DataFrame({"tax": _gx, "fat": _a + _b1 * _gx,
                                        "state": [_six[_j]] * 2}))
                .mark_line(size=2.5, clip=True)
                .encode(
                    x=_xax, y=_yax,
                    color=alt.Color("state:N",
                                    scale=alt.Scale(domain=_six,
                                                    range=_state_colors),
                                    legend=None),
                )
            )
    _main = alt.layer(*_layers).properties(width=430, height=340)

    _order = ["Pooled OLS", "State fixed effects",
              "Year fixed effects", "Two-way fixed effects"]
    _short = {"Pooled OLS": "Pooled", "State fixed effects": "State FE",
              "Year fixed effects": "Year FE", "Two-way fixed effects": "Two-way"}
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
    _by = alt.Y("b1:Q", scale=alt.Scale(domain=[-0.9, 0.45], nice=False),
                title="Estimated β₁")
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
        .encode(
            x=_bx,
            y=alt.Y("labely:Q", scale=alt.Scale(domain=[-0.9, 0.45], nice=False)),
            text="label:N",
        )
    )
    _rule = (
        alt.Chart(pd.DataFrame({"b1": [-0.45]}))
        .mark_rule(color="orange", strokeDash=[6, 4], size=2)
        .encode(y=alt.Y("b1:Q", scale=alt.Scale(domain=[-0.9, 0.45], nice=False)))
    )
    _side = (_bars + _blabels + _rule).properties(width=150, height=340)
    _chart = alt.hconcat(_main, _side).resolve_scale(color="independent")

    if _pick == "Pooled OLS":
        _msg = (
            f"One intercept for everything. Both confounders are live: drinking "
            f"culture pushes the estimate up, the national trend pushes it down, "
            f"and the net is {_b1:+.2f}, the wrong sign. The dashed orange line "
            f"marks the true effect, -0.45."
        )
    elif _pick == "State fixed effects":
        _msg = (
            f"One intercept per state absorbs drinking culture, but the "
            f"national decline remains in the error. Within every state, "
            f"fatalities fell while taxes rose, so the estimate overshoots to "
            f"{_b1:+.2f}: the tax takes credit for the nationwide safety trend."
        )
    elif _pick == "Year fixed effects":
        _msg = (
            f"One intercept per year absorbs the national trend (each year's "
            f"cloud slides down the chart), but drinking culture is back in the "
            f"error, and comparisons across states drag the estimate up to "
            f"{_b1:+.2f}, the same problem as Lecture 15's cross-sections."
        )
    else:
        _msg = (
            f"State intercepts absorb drinking culture and year intercepts "
            f"absorb the national trend. The estimate, {_b1:+.2f}, finally "
            f"lands on the true effect of -0.45. Each fixed effect removes "
            f"only its own kind of confounder, so the model needs both."
        )
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:600px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Standard errors in panel data

    Estimating $\beta_1$ is only half the job; we also need its standard error. Recall from Lecture 6 that the usual standard errors require the observations to be i.i.d., drawn independently from the same population. In a panel, that assumption deserves suspicion, because the same state appears seven times.

    Knowing the beer tax in California in 1982 tells us a lot about the likely beer tax in California in 1983: tax policy persists. The same holds for the unobserved factors in the error term. A recession, a court ruling, or an enforcement push that raises California's fatalities in one year tends to still be at work the next. A variable with this property is *autocorrelated*, also called *serially correlated*. Formally, $M_{i,t}$ is autocorrelated if

    $$
    \text{corr}(M_{i,t}, M_{i,t+j}) \neq 0 \quad \text{for some } j \neq 0.
    $$

    Autocorrelated errors do not bias $\hat{\beta}_1$. The problem is the standard errors. The usual formula counts every observation as an independent piece of information, but seven autocorrelated observations on California carry less information than seven independent ones. The usual standard errors are therefore not valid, and they typically overstate precision.

    The solution is to *cluster* the standard errors at the entity level. *Clustered standard errors* allow the errors to be correlated in any way *within* an entity, here a state, while assuming the errors are independent *across* entities. Statistical software makes clustering a one-option change to the regression command.

    The demonstration below shows why clustering matters. It re-simulates our panel many times, each time drawing errors whose within-state persistence you control with the slider, and estimates the two-way fixed-effects regression on each simulated panel. The first bar is the actual spread of $\hat{\beta}_1$ across the simulated panels, the honest measure of its sampling uncertainty. The other two bars show the average standard error that the conventional formula and the clustered formula report.
    """)
    return


@app.cell(hide_code=True)
def _(np, pn_tau, pn_tax, pn_z):
    # Pre-drawn innovations for the standard-error demo: 300 simulated panels.
    # The slider only changes how these fixed innovations are combined into an
    # AR(1), so dragging it never redraws the underlying randomness. The
    # within-transformed regressor is fixed across simulations.
    ac_innov = np.random.default_rng(777).normal(0.0, 1.0, (300, 50, 7))
    _xe = pn_tax - pn_tax.mean(axis=1, keepdims=True)
    ac_xt = _xe - _xe.mean(axis=0, keepdims=True)
    ac_signal = (
        2.40 - 0.45 * pn_tax[None, :, :]
        + pn_z[None, :, None]
        - 0.025 * pn_tau[None, None, :]
    )
    return ac_innov, ac_signal, ac_xt


@app.cell(hide_code=True)
def _(mo):
    ac_rho = mo.ui.slider(
        start=0.0, stop=0.9, step=0.1, value=0.0,
        label="Within-state persistence of the errors (ρ)",
        show_value=True,
    )
    ac_rho
    return (ac_rho,)


@app.cell(hide_code=True)
def _(ac_innov, ac_rho, ac_signal, ac_xt, alt, mo, np, pd):
    _rho = float(ac_rho.value)
    _R, _n, _T = ac_innov.shape

    # Build AR(1) errors from the fixed innovations, then estimate the two-way
    # fixed-effects regression on each of the 300 simulated panels. Demeaning
    # within state and year reproduces the dummy regression's slope; the
    # conventional variance uses the dummy regression's degrees of freedom
    # (350 observations, 57 coefficients).
    _eps = np.empty((_R, _n, _T))
    _eps[:, :, 0] = ac_innov[:, :, 0]
    for _t in range(1, _T):
        _eps[:, :, _t] = (
            _rho * _eps[:, :, _t - 1]
            + np.sqrt(1.0 - _rho**2) * ac_innov[:, :, _t]
        )
    _eps *= 0.10

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
        "which": ["Actual spread of estimates", "Conventional SE", "Clustered SE"],
        "se": [_truth, _c1, _c2],
        "label": [f"{_truth:.3f}", f"{_c1:.3f}", f"{_c2:.3f}"],
    })
    _bx = alt.X(
        "which:N", title=None,
        sort=["Actual spread of estimates", "Conventional SE", "Clustered SE"],
        axis=alt.Axis(labelAngle=-20),
    )
    _by = alt.Y("se:Q", scale=alt.Scale(domain=[0.0, 0.16], nice=False),
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
            f"With ρ = 0 the errors are independent across years, the i.i.d. "
            f"assumption holds, and all three bars agree: the conventional "
            f"formula ({_c1:.3f}) and the clustered formula ({_c2:.3f}) both "
            f"match the actual spread ({_truth:.3f}). Drag ρ upward to make "
            f"each state's errors persist."
        )
    elif _c1 / _truth > 0.85:
        _msg = (
            f"With ρ = {_rho:.1f}, persistence is mild. The conventional SE "
            f"({_c1:.3f}) is starting to slip below the actual spread "
            f"({_truth:.3f}), while the clustered SE ({_c2:.3f}) stays on "
            f"target."
        )
    else:
        _msg = (
            f"With ρ = {_rho:.1f}, the conventional formula reports {_c1:.3f} "
            f"when the actual spread of the estimates is {_truth:.3f}: it overstates "
            f"precision by about {100 * (1 - _c1 / _truth):.0f}%, so its "
            f"confidence intervals are too narrow and its t-statistics too "
            f"large. The clustered SE ({_c2:.3f}) tracks the truth, because it "
            f"lets each state's seven errors be correlated however they like."
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
    Our own fatality panel was simulated with persistent errors (ρ = 0.7), so clustering is not optional there: the conventional standard error on the two-way estimate is 0.08, while the clustered standard error is 0.11. Reporting the conventional number would claim more precision than we have.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Reading a panel regression table

    Applied papers report panel regressions the way Lecture 10 taught you to read: several columns, one specification each, with rows at the bottom announcing which fixed effects are included. The table below runs the full sequence on our 350-observation panel.
    """)
    return


@app.cell(hide_code=True)
def _(np, pn_fat, pn_tax):
    # The four columns of Section 5: pooled OLS, state FE, state + year FE,
    # and state + year FE with standard errors clustered by state. Each
    # regression is estimated as the dummy regression via least squares, so
    # the R-squared and degrees of freedom come from the full design matrix.
    _n, _T = pn_fat.shape
    _y = pn_fat.ravel()
    _x = pn_tax.ravel()
    _sid = np.repeat(np.arange(_n), _T)
    _tid = np.tile(np.arange(_T), _n)

    def _design(_state_fe, _year_fe):
        _cols = [np.ones(_n * _T), _x]
        if _state_fe:
            for _i in range(1, _n):
                _cols.append((_sid == _i).astype(float))
        if _year_fe:
            for _t in range(1, _T):
                _cols.append((_tid == _t).astype(float))
        return np.column_stack(_cols)

    def _fit(_state_fe, _year_fe, _cluster):
        _X = _design(_state_fe, _year_fe)
        _k = _X.shape[1]
        _beta, *_rest = np.linalg.lstsq(_X, _y, rcond=None)
        _u = _y - _X @ _beta
        _ssr = float(_u @ _u)
        _tss = float(((_y - _y.mean()) ** 2).sum())
        _XtXi = np.linalg.inv(_X.T @ _X)
        if _cluster:
            # Cluster-robust variance: sum the score outer products state by
            # state, with the standard G/(G-1) small-sample factor.
            _meat = np.zeros((_k, _k))
            for _i in range(_n):
                _rows = _sid == _i
                _g = _X[_rows].T @ _u[_rows]
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
        ("State fixed effects", ["No", "Yes", "Yes", "Yes"]),
        ("Year fixed effects", ["No", "No", "Yes", "Yes"]),
        ("Clustered SEs (by state)", ["No", "No", "No", "Yes"]),
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
        "<tr><td style='padding:3px 15px;text-align:left;'>Beer tax (\\$ per case)</td>"
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
        + "".join(f"<td style='{_pad}'>350</td>" for _f in tbl_fits)
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
        "padding:5px 0 3px;font-weight:600;'>Dependent variable: traffic fatality "
        "rate (deaths per 10,000 residents)</td></tr>"
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
        "State and year indicator coefficients are estimated but not reported."
        "</span>"
    )
    mo.vstack([mo.md(_table), _note])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read it column by column, asking of each coefficient movement: which confounder did this column remove?

    * **Column (1), pooled OLS**, estimates $+0.10$: the wrong sign, because drinking culture and the national trend are both in the error term.
    * **Column (2)** adds state fixed effects. The estimate swings to $-0.78$ as drinking culture is absorbed, but it now overshoots: within every state, the national safety trend moves fatalities down while taxes drift up, and the tax takes the credit.
    * **Column (3)** adds year fixed effects on top. The estimate settles at $-0.43$, close to the truth of $-0.45$, since each year's intercept soaks up that year's nationwide conditions. Comparing columns (2) and (3) is the Section 3 lesson in table form.
    * **Column (4)** reports the same regression as column (3); only the standard error changes, from 0.08 to 0.11, once we allow each state's errors to be correlated over time. The coefficient is unchanged, the t-statistic shrinks, and the confidence interval widens honestly. With the clustered standard error, the estimate remains statistically significant at the 1% level.

    Also glance at the R² row with Lecture 10's warning in mind: the fixed effects push the R² from 0.02 to above 0.9, but almost all of that fit comes from 55 intercepts, not from the beer tax. A large R² is no evidence that a coefficient is causal.

    This four-column progression, pooled, entity effects, two-way effects, clustered standard errors, is the standard way applied economists present panel evidence. You now know how to read every row of it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** time fixed effects, time fixed effects regression "
            "model, base period, two-way fixed effects model, autocorrelated, "
            "serially correlated, clustered standard errors.\n\n"

            "**Concepts:** why entity fixed effects cannot absorb nationwide "
            "changes, period indicators collapsing into time fixed effects, "
            "the dummy variable trap in the time dimension, the two-way model "
            "absorbing both time-invariant state factors and common year "
            "shocks, the identification condition for the two-way model, "
            "autocorrelation of errors within an entity, why autocorrelation "
            "invalidates the usual standard errors without biasing the "
            "estimate, clustering standard errors at the entity level, and "
            "reading a four-column panel regression table."
        ),
        title="Key terms and concepts",
        kind="info",
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


if __name__ == "__main__":
    app.run()
