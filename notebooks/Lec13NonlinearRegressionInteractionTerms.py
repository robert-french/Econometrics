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
    app_title="Lecture 13: Nonlinear Regression, Interaction Terms",
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
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Interacting two binary variables

    A *binary variable*, also called an *indicator variable*, takes only the values 0 and 1. Lecture 5 showed how to interpret a regression of $Y$ on a single binary variable. Recall that the intercept $\hat{\beta}_0$ is the estimated mean of $Y$ for the observations with $X=0$, while $\hat{\beta}_0+\hat{\beta}_1$ is the estimated mean for the observations with $X=1$. The slope $\hat{\beta}_1$ is therefore the difference between the two estimated means.

    This lecture considers regressions with two binary variables. Our survey of 300 workers from Lectures 11 and 12 recorded two indicator variables that we have not yet used. The first indicates whether a worker holds a job in science, technology, engineering, or mathematics (STEM). The second indicates whether the worker has completed a college degree. We can use these variables to ask whether the payoff to a college degree is larger in STEM jobs than in non-STEM jobs.

    To answer this question, the regression must allow the payoff to a college degree to differ by job type. We do this by multiplying the two indicators and including their product as an additional regressor. This product is called an *interaction term*. The regression becomes

    $$
    Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \beta_3 \underbrace{(X_1 \times X_2)}_{\text{interaction}} + u,
    $$

    where $X_1$ indicates that a worker has a college degree and $X_2$ indicates that a worker holds a STEM job. Because both variables are binary, the interaction term equals 1 only for workers who have both a college degree and a STEM job. It equals 0 for everyone else.

    The two indicators divide workers into four groups. The coefficients combine differently to give the predicted wage for each group.

    <span style="display:block;text-align:center;font-size:0.9rem;font-weight:600;margin:0.4rem 0 0;">Predicted wage for each combination of the two indicators</span>

    | | Non-STEM ($X_2 = 0$) | STEM ($X_2 = 1$) |
    |:---|:---:|:---:|
    | **No degree** ($X_1 = 0$) | $\hat{\beta}_0$ | $\hat{\beta}_0 + \hat{\beta}_2$ |
    | **College degree** ($X_1 = 1$) | $\hat{\beta}_0 + \hat{\beta}_1$ | $\hat{\beta}_0 + \hat{\beta}_1 + \hat{\beta}_2 + \hat{\beta}_3$ |

    The first three cells follow the single-variable logic from Lecture 5. Workers with neither characteristic have a predicted wage of $\hat{\beta}_0$. Among non-STEM workers, having a college degree adds $\hat{\beta}_1$ to their predicted wage. Among workers without a college degree, holding a STEM job adds $\hat{\beta}_2$ to their predicted wage.

    The interaction coefficient $\hat{\beta}_3$ appears only in the bottom-right cell, where both indicators equal 1. It captures the additional association between having both characteristics and wages, beyond the sum of their separate associations. A positive $\hat{\beta}_3$ means that the estimated payoff to a college degree is larger in STEM jobs than in non-STEM jobs. A negative $\hat{\beta}_3$ means that it is smaller.
    """)
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
        rf"Fitting the regression to the survey data gives"
        "\n\n"
        rf"$$\widehat{{\text{{Wage}}}} = {_b0:.2f} + {_b1:.2f}\,\text{{College}} + {_b2:.2f}\,\text{{STEM}} + {_b3:.2f}\,(\text{{College}} \times \text{{STEM}}),$$"
        "\n\n"
        rf"Substituting each combination of the two indicators gives the four predicted wages below. "
        rf"Each predicted wage exactly equals the average wage of the corresponding group.<sup><a id='fnref1' href='#fn1'>1</a></sup>"
    )
    # Markdown pipe table, centered course-wide by the `.prose table` rule in
    # marimo-overrides.css. Pipe tables run through the normal markdown
    # pipeline, so the dollar amounts stay \$-escaped.
    _table = (
        '<span style="display:block;text-align:center;font-size:0.9rem;'
        'font-weight:600;margin:0.4rem 0 0;">'
        "Predicted hourly wage by degree and job type</span>"
        "\n\n"
        "| | Non-STEM | STEM |\n"
        "|:---|:---:|:---:|\n"
        rf"| **No degree** | \${_c00:.2f} | \${_c01:.2f} |"
        "\n"
        rf"| **College degree** | \${_c10:.2f} | \${_c11:.2f} |"
    )

    _p2 = (
        rf"Among workers without a college degree, the estimated STEM premium is "
        rf"\${_c01 - _c00:.2f} per hour, the difference between \${_c01:.2f} and \${_c00:.2f}. "
        rf"Among college graduates, the estimated STEM premium is "
        rf"\${_c11 - _c10:.2f} per hour, the difference between \${_c11:.2f} and \${_c10:.2f}. "
        rf"The difference between these two STEM premiums is \${_b3:.2f}, which equals "
        rf"$\hat{{\beta}}_3$. A college degree is therefore associated with an additional "
        rf"\${_b3:.2f} per hour in STEM jobs relative to non-STEM jobs. "
    )
    mo.md(_p1 + "\n\n" + _table + "\n\n" + _p2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>

    ## 2. Interacting a binary and a continuous variable

    A binary variable can also interact with a continuous variable. Work experience is continuous, and the wage difference associated with an additional year of experience may be larger in STEM jobs than in non-STEM jobs. Let $D = 1$ indicate a STEM job and $D = 0$ indicate a non-STEM job, and let $X$ denote years of experience. There are three main ways we can incorporate the STEM indicator into the regression of wages on work experience.

    ### <span style="color:#0b68cb">(a) Different intercepts, same slope:</span>

    $$
    Y = \beta_0 + \beta_1 D + \beta_2 X + u
    $$

    For non-STEM workers, setting $D=0$ gives the line

    $$
    Y = \beta_0 + \beta_2 X.
    $$

    For STEM workers, setting $D=1$ gives

    $$
    Y = (\beta_0+\beta_1) + \beta_2 X.
    $$

    The STEM indicator $D$ shifts the entire STEM line up or down by $\beta_1$. The two groups have different regression intercepts but the same slope, so their fitted regression lines are parallel. At every level of experience, the predicted wage difference between STEM and non-STEM workers is $\beta_1$.

    ### <span style="color:#0b68cb">(b) Same intercept, different slopes:</span>

    $$
    Y = \beta_0 + \beta_1 X + \beta_2(X \times D) + u
    $$

    For non-STEM workers, setting $D=0$ gives

    $$
    Y = \beta_0+\beta_1X,
    $$

    while for STEM workers, setting $D=1$ gives

    $$
    Y = \beta_0+(\beta_1+\beta_2)X.
    $$

    Both groups have the same intercept $\beta_0$, but their slopes differ by $\beta_2$. The predicted wage difference is zero when $X=0$ and equals $\beta_2X$ at any other level of experience. It therefore changes by $\beta_2$ with each additional year of experience.

    This specification imposes the restriction that STEM and non-STEM workers have the same predicted wage when experience equals zero. In most applications, researchers include both the indicator and the interaction, as in specification (c) below, unless there is a substantive reason to impose this restriction. More generally, an interaction term is usually included together with the variables from which it is constructed.

    ### <span style="color:#0b68cb">(c) Different intercepts and different slopes:</span>

    $$
    Y = \beta_0 + \beta_1 X + \beta_2 D + \beta_3(X \times D) + u
    $$

    For non-STEM workers, setting $D=0$ gives

    $$
    Y = \beta_0+\beta_1X.
    $$

    For STEM workers, setting $D=1$ gives

    $$
    Y = (\beta_0+\beta_2)+(\beta_1+\beta_3)X.
    $$

    The STEM intercept differs from the non-STEM intercept by $\beta_2$, *and* the STEM slope differs from the non-STEM slope by $\beta_3$. The predicted wage difference between the two groups therefore depends on experience, $\beta_2+\beta_3X$. A positive $\beta_3$ means that the wage difference between STEM and non-STEM workers becomes larger as experience increases. A negative $\beta_3$ means that it becomes smaller.

    The chart below estimates each of these regressions using our survey data. The first checkbox adds the $D$ term, an *intercept shift* that allows the STEM and non-STEM lines to have different intercepts. The second adds the $X \times D$ term, a *slope shift* that allows their slopes to differ.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    int_shift = mo.ui.checkbox(
        value=False, label="Include the STEM indicator as a main effect in the regression"
    )
    slope_shift = mo.ui.checkbox(
        value=False, label="Interact the STEM indicator with Experience in the regression"
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

    # The model being fit, shown above the chart, and the per-line β labels
    # drawn on the plot. The labels give each line's intercept and slope as
    # the coefficient sums implied by setting STEM to 0 or 1; numbering
    # matches Section 2's (a)/(b)/(c) ordering.
    if not _use_d and not _use_xd:
        _model_eq = r"$$\text{Wage} = \beta_0 + \beta_1\,\text{Experience} + u$$"
        _lab0 = "β₀ + β₁X"
        _lab1 = None
    elif _use_d and not _use_xd:
        _model_eq = r"$$\text{Wage} = \beta_0 + \beta_1\,\text{STEM} + \beta_2\,\text{Experience} + u$$"
        _lab0 = "β₀ + β₂X"
        _lab1 = "(β₀ + β₁) + β₂X"
    elif _use_d and _use_xd:
        _model_eq = (
            r"$$\text{Wage} = \beta_0 + \beta_1\,\text{Experience} + \beta_2\,\text{STEM}"
            r" + \beta_3\,(\text{Experience} \times \text{STEM}) + u$$"
        )
        _lab0 = "β₀ + β₁X"
        _lab1 = "(β₀ + β₂) + (β₁ + β₃)X"
    else:
        _model_eq = (
            r"$$\text{Wage} = \beta_0 + \beta_1\,\text{Experience}"
            r" + \beta_2\,(\text{Experience} \times \text{STEM}) + u$$"
        )
        _lab0 = "β₀ + β₁X"
        _lab1 = "β₀ + (β₁ + β₂)X"
    _model = mo.md(_model_eq)

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
    # β labels sit at mid-chart, the non-STEM label below its line and the
    # STEM label above its line; the STEM line is fitted above the non-STEM
    # line throughout, so the offsets cannot collide. Hats: chart text cannot
    # render KaTeX, the Unicode combining circumflex draws tiny and badly
    # anchored, and a whole-string caret overlay drifts because subscript
    # digits fall back to a different font than the rest of the label. So each
    # label is hand-typeset one character at a time: every character is its
    # own centered text mark at a cursor position advanced by estimated glyph
    # widths, and each β also emits a caret mark at the SAME x, 7px up. The
    # width estimates only affect letter spacing; the hats sit exactly over
    # the betas in any font by construction.
    _lx = 30.0
    _upx = 45.0 / 560.0  # data units per pixel, x (domain / chart width)
    _upy = 45.0 / 340.0  # data units per pixel, y (domain / chart height)
    _wid = {"β": 7.2, "+": 7.6, "(": 4.3, ")": 4.3, "X": 8.7, " ": 3.6}

    def _label_rows(_x, _y, _text):
        _rows = []
        _wids = [5.2 if _c in "₀₁₂₃" else _wid.get(_c, 7.0) for _c in _text]
        _cur = -sum(_wids) / 2.0
        for _c, _w in zip(_text, _wids):
            _cx = _x + (_cur + _w / 2.0) * _upx
            if _c != " ":
                _rows.append({"exper": _cx, "wage": _y, "t": _c})
            if _c == "β":
                _rows.append({"exper": _cx, "wage": _y + 7.0 * _upy, "t": "^"})
            _cur += _w
        return pd.DataFrame(_rows)

    def _line_label(_x, _y, _text, _color):
        return [
            alt.Chart(_label_rows(_x, _y, _text))
            .mark_text(color=_color, fontSize=13, align="center", baseline="middle", clip=True)
            .encode(x="exper:Q", y="wage:Q", text="t:N")
        ]

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
        _layers.extend(_line_label(_lx, _i0 + _s0 * _lx - 2.9, _lab0, "#1f4e79"))
        _layers.extend(_line_label(_lx, _i1 + _s1 * _lx + 2.6, _lab1, "#b45309"))
    else:
        # Pooled model: one line for everyone, drawn in a neutral dark gray so
        # it does not read as either group's line.
        _layers.append(
            alt.Chart(pd.DataFrame({"exper": _gx, "wage": _i0 + _s0 * _gx}))
            .mark_line(color="#374151", size=3, clip=True)
            .encode(x="exper:Q", y="wage:Q")
        )
        _layers.extend(_line_label(_lx, _i0 + _s0 * _lx + 2.6, _lab0, "#374151"))

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
            rf"With both boxes unchecked, all workers share the same fitted line, "
            rf"Wage = {_b0:.2f} + {_bx:.2f}·Experience. The model therefore predicts "
            rf"the same wage for STEM and non-STEM workers at every level of experience."
        )

    elif _use_d and not _use_xd:
        _msg = (
            rf"Specification (a) allows different intercepts but imposes a common slope. "
            rf"The fitted line is Wage = {_i0:.2f} + {_s0:.2f}·Experience for non-STEM workers "
            rf"and Wage = {_i1:.2f} + {_s1:.2f}·Experience for STEM workers. The STEM line "
            rf"sits \${_bd:.2f} above the non-STEM line at every level of experience, so the "
            rf"predicted wage difference is constant."
        )

    elif not _use_d and _use_xd:
        _msg = (
            rf"Specification (b) imposes a common intercept but allows different slopes. "
            rf"Both fitted lines begin at \${_b0:.2f}. The fitted slope is \${_s0:.2f} per "
            rf"year of experience for non-STEM workers and \${_s1:.2f} for STEM workers. "
            rf"Because this specification forces the lines to have the same intercept even "
            rf"though specification (c) estimates a higher intercept for STEM workers, it "
            rf"compensates by fitting a steeper STEM slope than specification (c)."
        )

    else:
        _msg = (
            rf"Specification (c) allows both the intercepts and the slopes to differ. "
            rf"The fitted line is Wage = {_i0:.2f} + {_s0:.2f}·Experience for non-STEM workers "
            rf"and Wage = {_i1:.2f} + {_s1:.2f}·Experience for STEM workers. At 40 years of "
            rf"experience, the predicted STEM–non-STEM wage difference is \${_gap40:.2f}. "
            rf"It consists of the \${_bd:.2f} intercept difference plus "
            rf"40 × \${_bxd:.2f} = \${40.0 * _bxd:.2f} from the difference in slopes."
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

    Interaction terms are not limited to binary variables. Years of schooling and years of experience are both continuous, and the wage difference associated with an additional year of experience may depend on how much schooling a worker has. Let $X_1$ denote years of experience and let $X_2$ denote years of schooling. We can interact these variables in a regression,

    $$
    Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \beta_3(X_1 \times X_2) + u.
    $$

    Experience appears in two terms, $\beta_1X_1$ and $\beta_3(X_1 \times X_2)$. Holding schooling fixed, one additional year of experience therefore changes the predicted wage by $\beta_1+\beta_3X_2$.

    The wage difference associated with an additional year of experience is no longer a single number. It depends on the worker’s years of schooling. The coefficient $\beta_3$ tells us how much the relationship between wages and experience changes with each additional year of schooling. When $\beta_3>0$, the wage difference associated with an additional year of experience is larger for workers with more schooling. When $\beta_3<0$, it is smaller.

    Suppose a study of hourly wages estimates

    $$
    \widehat{\text{Wage}} = 5.00+0.20X_1+0.90X_2+0.02(X_1 \times X_2).
    $$

    For a worker with 10 years of schooling, one additional year of experience is associated with a predicted hourly wage that is $0.20+0.02(10)=0.40$ dollars higher. For a worker with 16 years of schooling, one additional year of experience is associated with a predicted hourly wage that is $0.20+0.02(16)=0.52$ dollars higher.

    The interaction coefficient of $0.02$ means that each additional year of schooling increases the experience slope by 2 cents per hour. Equivalently, each additional year of experience increases the schooling slope by 2 cents per hour. Schooling and experience are therefore associated with wages in a complementary way. The wage difference associated with either variable is larger at higher values of the other. Like in the binary case, this only describes the fitted relationship between schooling, experience, and wages; it does not by itself show that schooling or experience causes wages to rise. To make a causal statement about the relationship between wages, experience, and education, we still must assume the first least squares assumption in Lecture 9 holds.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** binary variable, indicator variable, interaction "
            "term, saturated regression, intercept shift, slope shift.\n\n"
            "**Concepts:** reading a binary regressor's coefficients as two "
            "group averages and their difference, how two interacted indicators produce "
            "four predicted wages built from sums of coefficients, the interaction "
            "coefficient as the additional wage difference associated with having both "
            "characteristics and how its sign is read, why a saturated regression "
            "reproduces every group average exactly, the three ways to include a binary "
            "indicator in a regression with a continuous variable (different intercepts, "
            "different slopes, or both) and the pair of fitted lines each produces, why "
            "an interaction term is usually included together with the variables from "
            "which it is constructed, how imposing a common intercept forces the fitted "
            "slope difference to absorb the intercept difference, how the interaction of "
            "two continuous variables makes the slope on one variable, β₁ + β₃X₂, depend "
            "on the level of the other, and that interaction coefficients describe "
            "fitted associations, not causal effects."
        ),
        kind="info",
        title="Key terms and concepts",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    <span id="fn1" style="display:block;font-size:0.9rem;">**1.** With four coefficients for four groups, this is a *saturated regression*. It is flexible enough to reproduce every group average exactly. <a href="#fnref1" title="Back to text">&#8617;</a></span>
    """)
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
