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

__generated_with = "0.23.14"
app = marimo.App(
    app_title="Lecture 13: Nonlinear Regression, Interaction Terms",
    css_file="marimo-overrides.css",
)

__preliminary__ = True


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
            mo.md("# [Lecture 13](#top)"),
            mo.md("Nonlinear Regression: Interaction Terms"),
            mo.nav_menu(
                {
                    "#sec1": "1. Interacting two binary variables",
                    "#sec2": "2. Interacting a binary and a continuous variable",
                    "#sec3": "3. Interacting two continuous variables",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec12NonlinearRegressionLogarithms.html" target="_self">← Lecture 12</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec14InternalAndExternalValidity.html" target="_self">Lecture 14 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 13: Nonlinear Regression, Interaction Terms
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Same-page (#fragment) links must stay plain markdown links with no inline
    # style and no styled wrapper. marimo re-renders fragment links as React
    # navigation components, and any inline style string on the link (or on a
    # span/div around it) is passed to React as the `style` prop, which must be
    # an object, not a string -> "Minified React error #62".
    mo.md(r"""
    ## Contents

    [1. Interacting two binary variables](#sec1)<br>
    [2. Interacting a binary and a continuous variable](#sec2)<br>
    [3. Interacting two continuous variables](#sec3)
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # The same 300-worker wage-and-experience survey as Lectures 11 and 12
    # (same seed, and experience is the first draw in the same order, so the
    # experience values are the same workers), now extended with two binary
    # indicators. The wage equation is linear in levels so the straight-line
    # pictures in Section 2 match the truth. Fixed seed for reproducibility.
    _rng = np.random.default_rng(1)
    n_workers = 300
    exper = _rng.uniform(1.0, 40.0, n_workers)
    stem = (_rng.random(n_workers) < 0.35).astype(float)
    college = (_rng.random(n_workers) < 0.50).astype(float)
    wage = (
        11.0 + 0.25 * exper + 2.0 * stem + 0.15 * exper * stem
        + 4.0 * college + 3.0 * (college * stem)
        + _rng.normal(0.0, 2.5, n_workers)
    )
    return college, exper, n_workers, stem, wage


@app.cell(hide_code=True)
def _(mo):
    _intro = r"""
    <a id="sec1"></a>
    ## 1. Interacting two binary variables

    A *binary variable*, also called an *indicator variable*, takes only the values 0 and 1. Lecture 5 showed how to read a regression of $Y$ on one binary variable. The intercept $\hat{\beta}_0$ is the average of $Y$ in the group with $X = 0$, the sum $\hat{\beta}_0 + \hat{\beta}_1$ is the average in the group with $X = 1$, and the slope $\hat{\beta}_1$ is the difference between the two group averages.

    This lecture asks what a regression can say when two binary variables work together. Our running survey of 300 workers from Lectures 11 and 12 recorded two indicators we have not used yet, whether the worker holds a STEM job (science, technology, engineering, or mathematics) and whether the worker finished a college degree. Does a college degree pay off more in STEM jobs than in other jobs? To answer, the regression must let the payoff to a degree differ by job type. We do this by multiplying the two indicators together and including the product as its own regressor. The product is called an *interaction term*, and the regression becomes

    $$
    Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \beta_3 \underbrace{(X_1 \times X_2)}_{\text{interaction}} + u,
    $$

    where $X_1$ indicates a college degree and $X_2$ indicates a STEM job. The interaction term equals 1 only for workers who have both a degree and a STEM job.

    The two indicators split the workers into four groups, and the four coefficients combine to give a predicted wage for each group.

    """
    # Markdown "|" tables render as a full-width, left-aligned <table>, so the
    # table is built as raw HTML instead: display:inline-table + width:auto
    # shrinks it to its content and text-align:center on the wrapper centers it
    # (the Lec10 regression-table idiom). Raw HTML blocks skip KaTeX, so the
    # coefficient symbols use Unicode (β̂₀) rather than $\hat{\beta}_0$. The
    # table is spliced into the same mo.md as the prose so vertical spacing
    # follows the normal document flow instead of stacking vstack flex gaps;
    # the html stays on one 4-space-indented line so mo.md's dedent still
    # applies to the whole string.
    _pad = "padding:4px 18px;text-align:center;"
    _left = "padding:4px 18px;text-align:left;font-weight:600;"
    _thin = "border-bottom:1px solid rgba(120,120,120,0.6);"
    _rule = "2px solid rgba(120,120,120,0.9)"
    _table = (
        "<div style='overflow-x:auto;text-align:center;margin:0.4rem 0 1.1rem;'>"
        "<span style='display:block;text-align:center;font-size:0.9rem;"
        "font-weight:600;margin:0 0 0.35rem;'>"
        "Predicted wage for each combination of the two indicators</span>"
        "<table style='display:inline-table;width:auto;border-collapse:collapse;"
        "margin:0 auto;font-size:0.92rem;line-height:1.4;"
        f"border-top:{_rule};border-bottom:{_rule};'>"
        f"<thead><tr><th style='{_pad}{_thin}'></th>"
        f"<th style='{_pad}{_thin}font-weight:600;'>Non-STEM (<em>X</em>₂ = 0)</th>"
        f"<th style='{_pad}{_thin}font-weight:600;'>STEM (<em>X</em>₂ = 1)</th></tr></thead>"
        "<tbody>"
        f"<tr><td style='{_left}'>No degree (<em>X</em>₁ = 0)</td>"
        f"<td style='{_pad}'><em>β̂</em>₀</td>"
        f"<td style='{_pad}'><em>β̂</em>₀ + <em>β̂</em>₂</td></tr>"
        f"<tr><td style='{_left}'>College degree (<em>X</em>₁ = 1)</td>"
        f"<td style='{_pad}'><em>β̂</em>₀ + <em>β̂</em>₁</td>"
        f"<td style='{_pad}'><em>β̂</em>₀ + <em>β̂</em>₁ + <em>β̂</em>₂ + <em>β̂</em>₃</td></tr>"
        "</tbody></table></div>"
    )
    mo.md(
        _intro
        + _table
        + r"""

    The first three cells follow the single-variable logic from Lecture 5. Workers with neither trait are predicted to earn $\hat{\beta}_0$, and each indicator on its own adds its coefficient. The interaction coefficient $\hat{\beta}_3$ appears only in the bottom-right cell, where both indicators equal 1. It measures how much more (or less) the two traits pay together than the sum of what they pay separately.
    """
    )
    return


@app.cell(hide_code=True)
def _(college, mo, np, stem, wage):
    # Live saturated fit for Section 2: wage on college, STEM, and their
    # interaction. With four coefficients for four groups, the fitted values
    # reproduce the four group means exactly, which the table demonstrates.
    _X = np.column_stack([np.ones(len(wage)), college, stem, college * stem])
    _b, *_ = np.linalg.lstsq(_X, wage, rcond=None)
    _b0, _b1, _b2, _b3 = (float(_v) for _v in _b)
    _c00 = _b0
    _c10 = _b0 + _b1
    _c01 = _b0 + _b2
    _c11 = _b0 + _b1 + _b2 + _b3
    _p1 = (
        rf"Fitting this regression on the survey gives"
        "\n\n"
        rf"$$\widehat{{\text{{Wage}}}} = {_b0:.2f} + {_b1:.2f}\,\text{{College}} + {_b2:.2f}\,\text{{STEM}} + {_b3:.2f}\,(\text{{College}} \times \text{{STEM}}),$$"
        "\n\n"
        rf"and filling in the table produces the four predicted wages below. Each prediction equals the average wage of that group exactly. A regression with one coefficient per group, called a *saturated regression*, can always match every group average."
    )
    # Raw HTML table, centered via the Lec10 inline-table idiom (see the
    # symbolic table above). Inside a raw HTML block KaTeX never runs, so the
    # dollar signs are written bare rather than escaped. Spliced into one
    # mo.md with the surrounding prose so spacing follows normal document flow.
    _pad = "padding:4px 18px;text-align:center;"
    _left = "padding:4px 18px;text-align:left;font-weight:600;"
    _thin = "border-bottom:1px solid rgba(120,120,120,0.6);"
    _rule = "2px solid rgba(120,120,120,0.9)"
    _table = (
        "<div style='overflow-x:auto;text-align:center;margin:0.4rem 0 1.1rem;'>"
        "<span style='display:block;text-align:center;font-size:0.9rem;"
        "font-weight:600;margin:0 0 0.35rem;'>"
        "Predicted hourly wage by degree and job type</span>"
        "<table style='display:inline-table;width:auto;border-collapse:collapse;"
        "margin:0 auto;font-size:0.92rem;line-height:1.4;"
        f"border-top:{_rule};border-bottom:{_rule};'>"
        f"<thead><tr><th style='{_pad}{_thin}'></th>"
        f"<th style='{_pad}{_thin}font-weight:600;'>Non-STEM</th>"
        f"<th style='{_pad}{_thin}font-weight:600;'>STEM</th></tr></thead>"
        "<tbody>"
        f"<tr><td style='{_left}'>No degree</td>"
        f"<td style='{_pad}'>${_c00:.2f}</td>"
        f"<td style='{_pad}'>${_c01:.2f}</td></tr>"
        f"<tr><td style='{_left}'>College degree</td>"
        f"<td style='{_pad}'>${_c10:.2f}</td>"
        f"<td style='{_pad}'>${_c11:.2f}</td></tr>"
        "</tbody></table></div>"
    )
    _p2 = (
        rf"The interaction coefficient answers the opening question. Among workers without a degree, STEM jobs pay \${_c01 - _c00:.2f} more per hour on average (\${_c01:.2f} versus \${_c00:.2f}). Among college graduates, the STEM premium is \${_c11 - _c10:.2f} (\${_c11:.2f} versus \${_c10:.2f}). The difference between those two premiums, \${_b3:.2f}, is $\hat{{\beta}}_3$. A college degree is associated with a larger payoff in STEM jobs than elsewhere, by about \${_b3:.2f} per hour."
    )
    mo.md(_p1 + "\n\n" + _table + "\n\n" + _p2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>

    ## 2. Interacting a binary and a continuous variable

    A binary variable can also interact with a continuous one. Work experience is continuous, and an extra year of it may be worth more in a STEM job than elsewhere. Writing $D$ for the STEM indicator and $X$ for years of experience, three specifications appear in applied work. They differ in whether the two groups get their own intercept, their own slope, or both.

    ### <span style="color:#0b68cb">(a) Different intercepts, same slope</span>

    $$
    Y = \beta_0 + \beta_1 D + \beta_2 X + u
    $$

    The $D$ term shifts the whole line up or down for STEM workers. Their line sits $\beta_1$ above the non-STEM line at every level of experience, and the two lines are parallel.

    ### <span style="color:#0b68cb">(b) Different intercepts and different slopes</span>

    $$
    Y = \beta_0 + \beta_1 X + \beta_2 D + \beta_3 (X \times D) + u
    $$

    Non-STEM workers follow the line $\beta_0 + \beta_1 X$. For STEM workers the intercept becomes $\beta_0 + \beta_2$ and the slope becomes $\beta_1 + \beta_3$, so both the starting wage and the return to a year of experience can differ between the groups.

    ### <span style="color:#0b68cb">(c) Same intercept, different slopes</span>

    $$
    Y = \beta_0 + \beta_1 X + \beta_2 (X \times D) + u
    $$

    Both groups start from the same intercept $\beta_0$, and only the slopes differ. The gap between the lines is zero at $X = 0$ and grows by $\beta_2$ with each year of experience.

    Before moving on, try to sketch the three pictures. Each specification draws two straight lines, and the question is where the lines start and whether they spread apart.

    The chart below fits these specifications to our survey, and the model being fit is displayed above the chart. The first checkbox adds the $D$ term, an *intercept shift* that lets the STEM line start at a different level. The second adds the $X \times D$ term, a *slope shift* that lets the STEM line rise at a different rate. The boxes start unticked, so the fitted model pools all 300 workers onto one line. Turning on only the intercept shift gives specification (a), only the slope shift gives (c), and both give (b). The brace marks the fitted wage gap between the two lines at 40 years of experience.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    int_shift = mo.ui.checkbox(
        value=False, label="Intercept shift: include the STEM term"
    )
    slope_shift = mo.ui.checkbox(
        value=False, label="Slope shift: include the Experience × STEM term"
    )
    mo.vstack(
        [
            int_shift,
            slope_shift,
        ]
    )
    return int_shift, slope_shift


@app.cell(hide_code=True)
def _(alt, exper, int_shift, mo, n_workers, np, pd, slope_shift, stem, wage):
    _use_d = bool(int_shift.value)
    _use_xd = bool(slope_shift.value)

    # Design matrix for the active specification, fit by least squares.
    _cols = [np.ones(n_workers), exper]
    if _use_d:
        _cols.append(stem)
    if _use_xd:
        _cols.append(exper * stem)
    _X = np.column_stack(_cols)
    _b, *_ = np.linalg.lstsq(_X, wage, rcond=None)
    _b0, _bx = float(_b[0]), float(_b[1])
    _bd = float(_b[2]) if _use_d else 0.0
    _bxd = float(_b[3] if _use_d else _b[2]) if _use_xd else 0.0

    # Group lines implied by the fit: non-STEM (D=0) and STEM (D=1).
    _i0, _s0 = _b0, _bx
    _i1, _s1 = _b0 + _bd, _bx + _bxd
    _gap40 = (_i1 + 40.0 * _s1) - (_i0 + 40.0 * _s0)

    # The model being fit, shown above the chart and rebuilt on every checkbox
    # change. Coefficient numbering matches the deck's (a)/(b)/(c) frames.
    if not _use_d and not _use_xd:
        _model_lab = "Pooled model, no STEM terms"
        _model_eq = r"$$\text{Wage} = \beta_0 + \beta_1\,\text{Experience} + u$$"
    elif _use_d and not _use_xd:
        _model_lab = "Specification (a), intercept shift only"
        _model_eq = r"$$\text{Wage} = \beta_0 + \beta_1\,\text{STEM} + \beta_2\,\text{Experience} + u$$"
    elif _use_d and _use_xd:
        _model_lab = "Specification (b), intercept and slope shifts"
        _model_eq = (
            r"$$\text{Wage} = \beta_0 + \beta_1\,\text{Experience} + \beta_2\,\text{STEM}"
            r" + \beta_3\,(\text{Experience} \times \text{STEM}) + u$$"
        )
    else:
        _model_lab = "Specification (c), slope shift only"
        _model_eq = (
            r"$$\text{Wage} = \beta_0 + \beta_1\,\text{Experience}"
            r" + \beta_2\,(\text{Experience} \times \text{STEM}) + u$$"
        )
    _model = mo.md(
        "<span style='display:block;text-align:center;font-size:0.85rem;"
        "color:#6b7280;margin-top:0.4rem;'>" + _model_lab + "</span>\n\n" + _model_eq
    )

    _xsc = alt.Scale(domain=[0.0, 45.0], nice=False)
    _ysc = alt.Scale(domain=[0.0, 45.0], nice=False)
    _pts = (
        alt.Chart(pd.DataFrame({
            "exper": exper, "wage": wage,
            "group": np.where(stem == 1.0, "STEM", "Non-STEM"),
        }))
        .mark_circle(size=28, opacity=0.35, clip=True)
        .encode(
            x=alt.X("exper:Q", scale=_xsc, title="Work experience (years)"),
            y=alt.Y("wage:Q", scale=_ysc, title="Hourly wage (dollars)"),
            color=alt.Color(
                "group:N",
                scale=alt.Scale(domain=["Non-STEM", "STEM"], range=["#1f4e79", "orange"]),
                legend=alt.Legend(title=None, orient="top"),
            ),
        )
    )

    _gx = np.array([0.0, 40.0])
    _layers = [_pts]
    if _use_d or _use_xd:
        _layers.append(
            alt.Chart(pd.DataFrame({"exper": _gx, "wage": _i0 + _s0 * _gx}))
            .mark_line(color="#1f4e79", size=3, clip=True)
            .encode(x="exper:Q", y="wage:Q")
        )
        _layers.append(
            alt.Chart(pd.DataFrame({"exper": _gx, "wage": _i1 + _s1 * _gx}))
            .mark_line(color="orange", size=3, clip=True)
            .encode(x="exper:Q", y="wage:Q")
        )
    else:
        # Pooled model: one line for everyone, drawn in a neutral dark gray so
        # it does not read as either group's line.
        _layers.append(
            alt.Chart(pd.DataFrame({"exper": _gx, "wage": _i0 + _s0 * _gx}))
            .mark_line(color="#374151", size=3, clip=True)
            .encode(x="exper:Q", y="wage:Q")
        )

    def _brace_df(_a, _b_, _base, _depth):
        # Vertical curly brace spanning wages [_a, _b_] at x = _base: back edge
        # at _base, cusp reaching _depth further right at the midpoint.
        _lo, _hi = min(_a, _b_), max(_a, _b_)
        _s = np.linspace(_lo, _hi, 120)
        _half = _s[:60]
        _sharp = 300.0 / (_hi - _lo)
        _ph = (1.0 / (1.0 + np.exp(-_sharp * (_half - _half[0])))
               + 1.0 / (1.0 + np.exp(-_sharp * (_half - _half[-1]))))
        _prof = np.concatenate([_ph, _ph[::-1]])
        _prof = (_prof - _prof.min()) / (_prof.max() - _prof.min())
        _off = _base + _depth * _prof
        return pd.DataFrame({"exper": _off, "wage": _s, "o": np.arange(_s.size)})

    # The brace degenerates when its span is under about a dollar (and cannot
    # be built at all for a zero span), so it only appears when two distinct
    # lines are fit and their gap at 40 years is wide enough. The order channel
    # is essential: without it Altair sorts line vertices by x, which scrambles
    # the vertical brace into a zigzag.
    if (_use_d or _use_xd) and abs(_gap40) >= 0.8:
        _y_lo = _i0 + 40.0 * _s0
        _layers.append(
            alt.Chart(_brace_df(_y_lo, _y_lo + _gap40, 40.5, 0.9))
            .mark_line(color="#b45309", size=1.5, clip=True)
            .encode(x="exper:Q", y="wage:Q", order=alt.Order("o:Q"))
        )
        _layers.append(
            alt.Chart(pd.DataFrame({
                "exper": [41.9], "wage": [_y_lo + _gap40 / 2.0],
                "t": [f"${_gap40:.2f}"],
            }))
            .mark_text(color="#b45309", fontSize=13, align="left", baseline="middle")
            .encode(x="exper:Q", y="wage:Q", text="t:N")
        )

    _chart = alt.layer(*_layers).properties(width=560, height=340)

    if not _use_d and not _use_xd:
        _msg = (
            rf"With both boxes off, every worker shares one fitted line, "
            rf"Wage = {_b0:.2f} + {_bx:.2f}·Experience. The model makes identical "
            "predictions for STEM and non-STEM workers at every experience level."
        )
    elif _use_d and not _use_xd:
        _msg = (
            rf"Specification (a), different intercepts with a common slope. The fitted "
            rf"lines are Wage = {_i0:.2f} + {_s0:.2f}·Experience for non-STEM workers and "
            rf"Wage = {_i1:.2f} + {_s1:.2f}·Experience for STEM workers. The STEM line "
            rf"sits \${_bd:.2f} higher at every experience level, so the braced gap "
            "would be the same anywhere along the lines."
        )
    elif _use_d and _use_xd:
        _msg = (
            rf"Specification (b), different intercepts and different slopes. The fitted "
            rf"lines are Wage = {_i0:.2f} + {_s0:.2f}·Experience for non-STEM workers and "
            rf"Wage = {_i1:.2f} + {_s1:.2f}·Experience for STEM workers. At 40 years the "
            rf"gap is \${_gap40:.2f}, made of \${_bd:.2f} from the intercept shift plus "
            rf"40 × \${_bxd:.2f} = \${40.0 * _bxd:.2f} from the slope difference."
        )
    else:
        _msg = (
            rf"Specification (c), a shared intercept with different slopes. Both lines "
            rf"start at \${_b0:.2f}, and a year of experience is fitted to add "
            rf"\${_s0:.2f} outside STEM but \${_s1:.2f} in STEM. The data would prefer "
            "the STEM line to start higher too, so forcing a shared intercept pushes "
            "the fitted STEM slope above its value in specification (b) to make up "
            "the difference."
        )
    _caption = mo.md(
        "<span style='display:block;margin:0.2rem auto 1rem;max-width:560px;"
        "font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;'>"
        + _msg + "</span>"
    )
    mo.vstack([_model, _chart, _caption], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>

    ## 3. Interacting two continuous variables

    Interaction terms are not limited to indicators. Years of schooling is continuous, and an extra year of experience may be worth more to workers with more schooling. Writing $X_1$ for years of experience and $X_2$ for years of schooling, the regression is

    $$
    Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \beta_3 (X_1 \times X_2) + u.
    $$

    Experience appears in two terms, $\beta_1 X_1$ and $\beta_3 (X_1 \times X_2)$, so one more year of it changes the predicted wage by

    $$
    \frac{\Delta Y}{\Delta X_1} = \beta_1 + \beta_3 X_2.
    $$

    The return to experience is no longer a single number. It depends on the worker's schooling, and when $\beta_3 > 0$, each extra year of schooling makes a year of experience worth $\beta_3$ more.

    Suppose a study of hourly wages estimates

    $$
    \widehat{\text{Wage}} = 5.00 + 0.20\,X_1 + 0.90\,X_2 + 0.02\,(X_1 \times X_2).
    $$

    For a worker with 10 years of schooling, one more year of experience is associated with a wage that is $0.20 + 0.02 \times 10 = 0.40$ dollars higher. For a worker with 16 years of schooling, the same year of experience is worth $0.20 + 0.02 \times 16 = 0.52$ dollars. The interaction coefficient says the two investments reinforce each other; every extra year of schooling makes a year of experience worth 2 cents more per hour.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This lecture completes our nonlinear toolkit. Polynomials let a single variable's effect change with its own level, logarithms move a relationship into percent terms, and interactions let one variable's effect depend on another variable. All three are still estimated by ordinary least squares, because each model stays linear in the coefficients. Lecture 14 turns from building regression models to judging them, asking when a regression estimated on one sample gives a trustworthy answer, and for whom.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** binary variable, indicator variable, interaction "
            "term, saturated regression, intercept shift, slope shift.\n\n"
            "**Key concepts covered:** reading a binary regressor's coefficients as two "
            "group averages and their difference, how two interacted indicators produce "
            "four predicted values built from sums of coefficients, why a saturated "
            "regression matches every group average exactly, the interaction coefficient "
            "as the additional premium the two traits pay together, the three "
            "binary-by-continuous specifications (different intercepts, different "
            "slopes, or both) and how each reshapes the two fitted lines, why forcing a "
            "shared intercept distorts the fitted slopes, and the effect of one "
            "continuous variable depending on the level of another through "
            "ΔY/ΔX₁ = β₁ + β₃X₂."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec12NonlinearRegressionLogarithms.html" target="_self">← Lecture 12</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec14InternalAndExternalValidity.html" target="_self">Lecture 14 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
