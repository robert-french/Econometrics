# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "numpy",
#     "pandas",
#     "altair",
#     "scipy",
#     "anywidget",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(
    app_title="Lecture 3: Working With Multiple Random Variables",
    css_file="marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt
    from scipy import stats
    import anywidget

    return anywidget, mo


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
                <div style="font-weight: 700; font-size: 1.05em;">Course Outline</div>

                1. <a href="https://robert-french.github.io/Econometrics/apps/Lec1Introduction.html" target="_self">Introduction</a>
                2. <a href="https://robert-french.github.io/Econometrics/apps/Lec2RandomVariables.html" target="_self">Random Variables</a>
                3. **[Multiple Random Variables](#top)**
                    1. [Joint, marginal, and conditional distributions](#sec1)
                    1. [Covariance and correlation](#sec2)
                    1. [Independence](#sec3)
                    1. [Independent and identically distributed](#sec4)
                    1. [Means and variances of sums](#sec5)
                4. <a href="https://robert-french.github.io/Econometrics/apps/Lec4EstimationHypothesisTestingAndConfidenceIntervals.html" target="_self">Estimation and Hypothesis Testing</a>
                5. <a href="https://robert-french.github.io/Econometrics/apps/Lec5SimpleLinearRegression.html" target="_self">Simple Linear Regression</a>
                6. <a href="https://robert-french.github.io/Econometrics/apps/Lec6OLSAssumptionsForCausalInference.html" target="_self">OLS Assumptions for Causal Inference</a>
                7. <a href="https://robert-french.github.io/Econometrics/apps/Lec7InferenceAndOmittedVariableBias.html" target="_self">Inference and Omitted Variable Bias</a>
                8. <a href="https://robert-french.github.io/Econometrics/apps/Lec8MultipleRegression.html" target="_self">Multiple Regression</a>
                9. <a href="https://robert-french.github.io/Econometrics/apps/Lec9ControlVariablesAndInference.html" target="_self">Control Variables and Inference</a>
                10. <a href="https://robert-french.github.io/Econometrics/apps/Lec10ReadingRegressionTables.html" target="_self">Reading Regression Tables</a>
                11. <a href="https://robert-french.github.io/Econometrics/apps/Lec11NonlinearRegressionPolynomials.html" target="_self">Nonlinear Regression: Polynomials</a>
                12. <a href="https://robert-french.github.io/Econometrics/apps/Lec12NonlinearRegressionLogarithms.html" target="_self">Nonlinear Regression: Logarithms</a>
                13. <a href="https://robert-french.github.io/Econometrics/apps/Lec13NonlinearRegressionInteractionTerms.html" target="_self">Nonlinear Regression: Interaction Terms</a>
                14. <a href="https://robert-french.github.io/Econometrics/apps/Lec14InternalAndExternalValidity.html" target="_self">Internal and External Validity</a>
                15. <a href="https://robert-french.github.io/Econometrics/apps/Lec15PanelDataI.html" target="_self">Panel Data I</a>
                16. <a href="https://robert-french.github.io/Econometrics/apps/Lec16PanelDataII.html" target="_self">Panel Data II</a>
                17. <span class="soon">Binary Dependent Variable Regressions</span>
                18. <span class="soon">Experiments</span>
                19. <span class="soon">Quasi-Experiments</span>
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec2RandomVariables.html" target="_self">← Lecture 2</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/pdf/Lec3WorkingWithMultipleRandomVariables.pdf" target="_blank">Download PDF</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec4EstimationHypothesisTestingAndConfidenceIntervals.html" target="_self">Lecture 4 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Lecture 3: Working With Multiple Random Variables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contents

    3.1 [Joint, marginal, and conditional distributions](#sec1)<br>
    3.2 [Covariance and correlation](#sec2)<br>
    3.3 [Independence](#sec3)<br>
    3.4 [Independent and identically distributed](#sec4)<br>
    3.5 [Means and variances of sums](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 3.1 Joint, marginal, and conditional distributions

    In Lecture 2 we focused on one random variable at a time. We defined its distribution, its expected value, and its spread or variance. Most questions in econometrics, however, ask about two variables together. Does a person's earnings depend on their level of education? Does the unemployment rate depend on the inflation rate? To answer these questions we need to extend the tools from one random variable to two.

    A *joint probability distribution* describes how likely each combination of values is for two random variables. When $X$ takes possible values $x_1, x_2, \ldots, x_k$ and $Y$ takes possible values $y_1, y_2, \ldots, y_l$, the joint probability distribution lists the probability of each combination of these possible values, denoted $\mathbb{P}(X = x_i, Y = y_j)$, for every pair $(x_i, y_j)$. The table below shows an example of a joint probability distribution for two discrete random variables.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Rendered through mo.center (not inside mo.md) so the table keeps its
    # natural size and is centered, instead of being stretched to full width
    # by marimo's ".markdown table { display:block }" rule.
    _joint = """
    <table style="border-collapse:collapse;text-align:center;">
    <tr style="background:var(--lime-2,#f8faf3);"><th style="padding:6px 18px;border-bottom:1px solid #cbd2d9;" colspan="4">Joint Probability of X and Y</th></tr>
    <tr style="background:var(--card,#fff);"><td style="padding:6px 18px;"></td><td style="padding:6px 18px;">x<sub>1</sub></td><td style="padding:6px 18px;">x<sub>2</sub></td><td style="padding:6px 18px;">x<sub>3</sub></td></tr>
    <tr style="background:var(--lime-2,#f8faf3);"><td style="padding:6px 18px;">y<sub>1</sub></td><td style="padding:6px 18px;">0.10</td><td style="padding:6px 18px;">0.15</td><td style="padding:6px 18px;">0.20</td></tr>
    <tr style="background:var(--card,#fff);"><td style="padding:6px 18px;">y<sub>2</sub></td><td style="padding:6px 18px;">0.20</td><td style="padding:6px 18px;">0.10</td><td style="padding:6px 18px;">0.25</td></tr>
    </table>
    """
    mo.center(mo.Html(_joint))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The six cells must sum to one because together they cover the probability of every possible outcome.

    A *marginal probability distribution* gives the distribution of a single variable, ignoring the other. We compute it by summing the joint probabilities over the values of the other variable. For example, the marginal probability that $X = x_1$ is

    $$ \mathbb{P}(X = x_1) = \mathbb{P}(X = x_1, Y = y_1) + \mathbb{P}(X = x_1, Y = y_2) = 0.10 + 0.20 = 0.30. $$

    In general, $\mathbb{P}(X = x_i) = \sum_j \mathbb{P}(X = x_i, Y = y_j)$. Summing down each column gives the marginal distribution of $X$, and summing across each row gives the marginal distribution of $Y$, both shown below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Two tables laid out side by side and centered with mo.hstack. Each title
    # spans its own table via colspan, so it sits centered over the whole table.
    _marg_x = """
    <table style="border-collapse:collapse;text-align:center;">
    <tr style="background:var(--lime-2,#f8faf3);"><th style="padding:6px 16px;border-bottom:1px solid #cbd2d9;" colspan="3">Marginal of X</th></tr>
    <tr style="background:var(--card,#fff);"><td style="padding:6px 16px;">x<sub>1</sub></td><td style="padding:6px 16px;">x<sub>2</sub></td><td style="padding:6px 16px;">x<sub>3</sub></td></tr>
    <tr style="background:var(--lime-2,#f8faf3);"><td style="padding:6px 16px;">0.30</td><td style="padding:6px 16px;">0.25</td><td style="padding:6px 16px;">0.45</td></tr>
    </table>
    """
    _marg_y = """
    <table style="border-collapse:collapse;text-align:center;">
    <tr style="background:var(--lime-2,#f8faf3);"><th style="padding:6px 16px;border-bottom:1px solid #cbd2d9;" colspan="2">Marginal of Y</th></tr>
    <tr style="background:var(--card,#fff);"><td style="padding:6px 16px;">y<sub>1</sub></td><td style="padding:6px 16px;">y<sub>2</sub></td></tr>
    <tr style="background:var(--lime-2,#f8faf3);"><td style="padding:6px 16px;">0.45</td><td style="padding:6px 16px;">0.55</td></tr>
    </table>
    """
    mo.hstack(
        [mo.Html(_marg_x), mo.Html(_marg_y)],
        justify="center", align="start", gap=2.5,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A *conditional probability distribution* gives the distribution of one variable, given the value of the other. The conditional probability that $Y = y_j$ given $X = x_i$ is

    $$ \mathbb{P}(Y = y_j \mid X = x_i) = \frac{\mathbb{P}(X = x_i, Y = y_j)}{\mathbb{P}(X = x_i)}. $$

    This formula is also known as *Bayes' rule*. It restates the question ''how likely is $Y = y_j$, knowing that $X = x_i$ has occurred?'' in terms of probabilities we can read off the probability tables. For our example, the conditional probability that $Y = y_1$ given $X = x_1$ is

    $$ \mathbb{P}(Y = y_1 \mid X = x_1) = \frac{0.10}{0.30} = \frac{1}{3}. $$

    We could similarly compute $\mathbb{P}(X = x_2 \mid Y = 2_2)$, or any other such combination. Bayes' rule turns up in many places in statistics. For this course, it is the bridge between the joint distribution and the conditional distribution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 3.2 Covariance and correlation

    The joint distribution describes how two random variables behave together, but it does not summarize their relationship in one number. The *covariance* of $X$ and $Y$ summarizes whether they tend to move in the same direction or in opposite directions. It is defined as

    $$ \text{cov}(X, Y) \equiv \sigma_{XY} = \sum_i \sum_j (x_j - \mu_X)(y_i - \mu_Y) \cdot \mathbb{P}(X = x_j, Y = y_i). $$

    The sign of the covariance is what carries most of its meaning. A positive $\sigma_{XY}$ means that when $X$ is above its mean, $Y$ tends to be above its mean too, and thus the two random variables tend to move together. A negative $\sigma_{XY}$ means one tends to be above its mean when the other is below it, so the two random variables tend to move in opposite directions. A zero covariance means $X$ and $Y$ do not move together on average.

    The size of the covariance is harder to interpret because it depends on the units of $X$ and $Y$. The covariance between years of education and weekly earnings would be in units of (years $\times$ dollars), while the covariance between height and weight would be in units of (inches $\times$ pounds). These numbers are not comparable.

    To get a unit-free summary we divide the covariance by the standard deviations of $X$ and $Y$. The *correlation coefficient*, also referred to simply as the *correlation*, is

    $$ \text{corr}(X, Y) \equiv \rho_{XY} = \frac{\sigma_{XY}}{\sigma_X \sigma_Y}. $$

    The correlation always sits between $-1$ and $1$. A correlation of $+1$ means $Y$ is an exactly increasing linear function of $X$. A correlation of $-1$ means $Y$ is an exactly decreasing linear function of $X$. A correlation of $0$ means $X$ and $Y$ have no linear relationship on average.

    However, just like for the variance and expected value introduced last lecture, when working with data we do not observe $\sigma_{XY}$, $\sigma_X$, or $\sigma_Y$ directly. We instead try to estimate them from a sample of $n$ paired observations $(X_1, Y_1), (X_2, Y_2), \ldots, (X_n, Y_n)$. We compute the *sample covariance* as

    $$ \hat{\sigma}_{XY} = \frac{1}{n - 1} \sum_{i=1}^{n} (X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y), $$

    and the *sample correlation* as

    $$ \widehat{\text{corr}}(X, Y) = \frac{\hat{\sigma}_{XY}}{\hat{\sigma}_X \hat{\sigma}_Y}. $$

    Use the interactive plot below to explore how sample statistics correspond to their underlying data points. Sample statistics update under the plot as you spray it with data points.
    """)
    return


@app.cell(hide_code=True)
def _(anywidget):
    class SprayWidget(anywidget.AnyWidget):
        # A canvas drawn directly in the page (no iframe, no virtual files):
        # dragging sprays points in one colour onto axes fixed to -10..10, and
        # the sample variances, covariance, and correlation are computed and
        # shown beneath the plot. Delivered as an anywidget so the drawing runs
        # client-side in the deployed WASM build.
        _esm = r"""
    function render({ model, el }) {
      const XMIN = -15, XMAX = 15, YMIN = -10, YMAX = 10;
      const W = 660, H = 448, padL = 44, padR = 16, padT = 14, padB = 34;
      const plotW = W - padL - padR, plotH = H - padT - padB;

      const wrap = document.createElement("div");
      wrap.style.cssText = "font-family:system-ui,-apple-system,sans-serif;color:#1f4e79;display:flex;flex-direction:column;align-items:center;";
      const cv = document.createElement("canvas");
      cv.width = W; cv.height = H;
      cv.style.cssText = "cursor:crosshair;touch-action:none;max-width:100%;";
      const controls = document.createElement("div");
      controls.style.cssText = "margin:8px 0 4px;";
      const btn = document.createElement("button");
      btn.textContent = "Reset";
      btn.style.cssText = "font:inherit;color:#1f4e79;background:#eef3f8;border:1px solid #1f4e79;border-radius:4px;padding:4px 14px;cursor:pointer;";
      controls.appendChild(btn);
      const statsEl = document.createElement("div");
      statsEl.style.cssText = "max-width:620px;font-size:0.85rem;line-height:1.45;color:#6b7280;text-align:center;";
      wrap.appendChild(cv); wrap.appendChild(controls); wrap.appendChild(statsEl);
      el.appendChild(wrap);

      const ctx = cv.getContext("2d");
      let points = [];
      let drawing = false;

      const toPxX = x => padL + (x - XMIN) / (XMAX - XMIN) * plotW;
      const toPxY = y => padT + (YMAX - y) / (YMAX - YMIN) * plotH;
      const toDataX = px => XMIN + (px - padL) / plotW * (XMAX - XMIN);
      const toDataY = py => YMAX - (py - padT) / plotH * (YMAX - YMIN);

      function drawAxes() {
    ctx.clearRect(0, 0, W, H);
    ctx.lineWidth = 1;
    ctx.font = "11px system-ui, sans-serif";
    for (let v = XMIN; v <= XMAX; v += 5) {
      const px = toPxX(v);
      ctx.strokeStyle = v === 0 ? "#9aa5b1" : "#eef1f4";
      ctx.beginPath(); ctx.moveTo(px, padT); ctx.lineTo(px, padT + plotH); ctx.stroke();
    }
    for (let v = YMIN; v <= YMAX; v += 5) {
      const py = toPxY(v);
      ctx.strokeStyle = v === 0 ? "#9aa5b1" : "#eef1f4";
      ctx.beginPath(); ctx.moveTo(padL, py); ctx.lineTo(padL + plotW, py); ctx.stroke();
    }
    ctx.fillStyle = "#6b7280";
    ctx.textAlign = "center"; ctx.textBaseline = "top";
    for (let v = XMIN; v <= XMAX; v += 5) ctx.fillText(v, toPxX(v), padT + plotH + 5);
    ctx.textAlign = "right"; ctx.textBaseline = "middle";
    for (let v = YMIN; v <= YMAX; v += 5) ctx.fillText(v, padL - 5, toPxY(v));
    ctx.fillStyle = "#1f4e79";
    ctx.font = "12px system-ui, sans-serif";
    ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
    ctx.fillText("X", padL + plotW / 2, H - 4);
    ctx.save();
    ctx.translate(11, padT + plotH / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText("Y", 0, 0);
    ctx.restore();
      }

      function drawPoints() {
    ctx.fillStyle = "rgba(31, 78, 121, 0.7)";
    for (const p of points) {
      ctx.beginPath(); ctx.arc(toPxX(p.x), toPxY(p.y), 3, 0, 2 * Math.PI); ctx.fill();
    }
      }

      function redraw() { drawAxes(); drawPoints(); }

      function fmt(v, d) {
    return v.toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
      }

      function updateStats() {
    const n = points.length;
    if (n < 2) {
      statsEl.textContent = "Press and drag on the plot to spray points. Add at least two to see the sample statistics.";
      return;
    }
    let mx = 0, my = 0;
    for (const p of points) { mx += p.x; my += p.y; }
    mx /= n; my /= n;
    let sxx = 0, syy = 0, sxy = 0;
    for (const p of points) {
      sxx += (p.x - mx) ** 2; syy += (p.y - my) ** 2; sxy += (p.x - mx) * (p.y - my);
    }
    const vX = sxx / (n - 1), vY = syy / (n - 1), cov = sxy / (n - 1);
    const corr = vX > 0 && vY > 0 ? cov / Math.sqrt(vX * vY) : 0;
    statsEl.textContent =
      "From the n = " + n + " points you sprayed, the sample variance of X is " +
      fmt(vX, 2) + ", the sample variance of Y is " + fmt(vY, 2) +
      ", the sample covariance is " + fmt(cov, 2) +
      ", and the sample correlation is " + fmt(corr, 3) + ".";
      }

      function spray(px, py) {
    if (px < padL || px > padL + plotW || py < padT || py > padT + plotH) return;
    for (let i = 0; i < 3; i++) {
      const jx = px + (Math.random() - 0.5) * 16;
      const jy = py + (Math.random() - 0.5) * 16;
      const x = toDataX(jx), y = toDataY(jy);
      if (x >= XMIN && x <= XMAX && y >= YMIN && y <= YMAX) points.push({ x, y });
    }
    if (points.length > 3000) points = points.slice(points.length - 3000);
    redraw(); updateStats();
      }

      function pos(e) {
    const r = cv.getBoundingClientRect();
    return [(e.clientX - r.left) * (W / r.width), (e.clientY - r.top) * (H / r.height)];
      }

      cv.addEventListener("pointerdown", e => { drawing = true; cv.setPointerCapture(e.pointerId); const [x, y] = pos(e); spray(x, y); });
      cv.addEventListener("pointermove", e => { if (drawing) { const [x, y] = pos(e); spray(x, y); } });
      cv.addEventListener("pointerup", () => { drawing = false; });
      cv.addEventListener("pointercancel", () => { drawing = false; });
      btn.addEventListener("click", () => { points = []; redraw(); updateStats(); });

      redraw(); updateStats();
    }
    export default { render };
    """

    return (SprayWidget,)


@app.cell(hide_code=True)
def _(SprayWidget, mo):
    mo.ui.anywidget(SprayWidget())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3.3 Independence

    Two random variables are *independent* when knowing the value of one is not informative about the value of the other. In probability, independence can be expressed in two equivalent ways and has an important implication. Specifically, if $X$ and $Y$ are independent, then:

    1. The conditional distribution of $Y$ does not depend on $X$ (and vice versa). That is, $\mathbb{P}(Y = y \mid X = x) = \mathbb{P}(Y = y)$ for every $x$ and $y$.
    2. The joint distribution factors into the product of the marginals, $\mathbb{P}(X = x, Y = y) = \mathbb{P}(X = x) \cdot \mathbb{P}(Y = y)$.
    3. The correlation and covariance are both zero, $\text{corr}(X, Y) = \sigma_{XY} = 0$.

    These ideas are easiest to see with a simple example. A coin flip and an unrelated die roll are independent. Knowing that the coin landed heads tells us nothing about which face of the die is showing, so the conditional distribution of the die given the coin is the same as its unconditional distribution. Equivalently, the probability of observing any particular combination, such as heads and a $4$, is simply the probability of heads multiplied by the probability of rolling a $4$. The result of the first die in a pair of rolls, however, is not independent of the sum of the two dice. If we know the sum is $11$, then the first die is very likely a $5$ or a $6$, and definitely not a $1$. The conditional distribution of the first die therefore differs from its unconditional distribution, and the probability of a particular first-die value and sum cannot generally be obtained by multiplying their marginal probabilities.

    Either of the first two conditions can serve as the definition of independence, and each implies the third condition. Note, however, that the third condition only goes one way. If $X$ and $Y$ are independent, then their correlation is zero. The converse is not true. Two random variables can have zero correlation and still be dependent because correlation captures only the linear part of their relationship. You can see this for yourself in the interactive scatter plot in Section 3.2. If you arrange the points in a symmetric arch or trough, the sample correlation will remain near zero even though a point's horizontal position is clearly informative about its height. The two coordinates are therefore dependent despite having little or no correlation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 3.4 Independent and identically distributed

    We say the random variables $X_1, X_2, \ldots, X_n$ are *independently and identically distributed* (i.i.d.) when two conditions hold. First, every $X_i$ has the same distribution. This means each random variable is drawn from the same underlying population, so differences across observations arise from which members of that population happen to be sampled rather than from drawing from different populations. Second, the $X_i$'s are independent, so knowing the value of one observation provides no information about the values of the others. We write $X_i \stackrel{\text{i.i.d.}}{\sim} F$ when the random variables are drawn independently from the same distribution $F$.

    Suppose we randomly sample households from the population of U.S. households and record their incomes. We can treat these incomes as i.i.d. if each household is sampled independently of the others and every household is drawn from the same population. One household's income then tells us nothing about the incomes of the households that will be sampled next (independence), and every draw comes from the same underlying distribution of household income (identically distributed). This i.i.d. assumption is what allows us to apply the law of large numbers and the central limit theorem from the previous lecture to sample data.

    Both parts of i.i.d. can fail in practice. Heights measured among members of the same family may not be independent because relatives share genes and environment, so knowing one family member's height can be informative about another's. Observations may also fail to be identically distributed. For example, if our sample includes both children and adults, their heights come from systematically different distributions because height varies with age.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 3.5 Means and variances of sums

    We often want to know the expected value and variance of a sum or weighted sum of random variables. One approach would be to treat the whole sum as a new random variable and then apply the formulas from Lecture 2 to that new variable. But this can quickly become unwieldy. Instead, we can use a few simple rules that cover most cases.

    1. The *linearity of expected value* says that adding a constant shifts the expected value by that constant, and multiplying a random variable by a constant multiplies its expected value by that constant. For any numbers $a$ and $b$, which we call *constants* to distinguish them from random variables,
    $$\mathbb{E}[a + b X] = a + b\mathbb{E}[X] = a + b \mu_X. $$

    2. The expected value of a sum is the sum of the expected values. This rule holds whether or not the random variables are independent,
    $$ \mathbb{E}[X_1 + X_2 + \cdots + X_n] = \mathbb{E}[X_1] + \mathbb{E}[X_2] + \cdots + \mathbb{E}[X_n] = n\mu_X. $$

    3. The variance of a shifted and scaled random variable follows a different rule. Adding a constant does not change the variance, but multiplying by a constant multiplies the variance by the square of that constant. For any constants $a$ and $b$,
    $$ \text{var}(a + b X) = b^2 \sigma_X^2. $$

    4. Covariance is symmetric and linear in each argument. Symmetry means that the order of the two variables does not matter. Linearity means that the covariance between one variable and a sum can be split into separate covariances,
    $$ \text{cov}(X, Y) = \text{cov}(Y, X), \qquad \text{cov}(X, Y + Z) = \text{cov}(X, Y) + \text{cov}(X, Z). $$

    5. The variance of a sum depends on whether the random variables are independent or not. If $X_1, X_2, \ldots, X_n$ are i.i.d. with variance $\sigma_X^2$, then the variance of the sum is simply $n$ times the variance of one draw,
    $$ \text{var}(X_1 + X_2 + \cdots + X_n) = n \sigma_X^2. $$

    Notice that the variance of the sample mean from Lecture 2 follows directly from Rule 5. If

    $$
    \hat{\mu}_X = \frac{1}{n}\sum_{i=1}^{n} X_i
    $$

    and the $X_i$ are i.i.d. with variance $\sigma_X^2$, then

    $$
    \text{var}(\hat{\mu}_X)
    =
    \frac{1}{n^2}\text{var}\left(\sum_{i=1}^{n} X_i\right)
    =
    \frac{1}{n^2} n \sigma_X^2
    =
    \frac{\sigma_X^2}{n}.
    $$

    Therefore,

    $$
    \sigma_{\hat{\mu}_X} = \frac{\sigma_X}{\sqrt{n}}.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** joint probability distribution, marginal "
            "probability distribution, conditional probability distribution, "
            "Bayes' rule, covariance, correlation, correlation coefficient, "
            "sample covariance, sample correlation, independence, "
            "independently and identically distributed (i.i.d.), constants.\n\n"
            "**Concepts:** linearity of the expected value, "
            "variance of a sum of i.i.d. random variables, zero correlation "
            "does not imply independence."
        ),
        title="Key terms and concepts",
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _text = mo.md(r"""
        This is bonus material. You will not be tested on the content of the appendix.

        **The covariance written with the expectation operator.**

        Section 3.2 defined the covariance as a double sum over the joint distribution. It can be written more compactly with the expectation operator,

        $$ \text{cov}(X, Y) \equiv \sigma_{XY} = \mathbb{E}\big[(X - \mu_X)(Y - \mu_Y)\big]. $$

        This is the same quantity. The expectation $\mathbb{E}[\cdot]$ is itself a probability-weighted sum, defined in Section 2.3, so expanding it reproduces the double sum from Section 3.2. This formulation is more common in advanced work.

        **Proof of the linearity of the expected value.**

        Here, we show mathematically that $\mathbb{E}[a + b X] = a + b \mathbb{E}[X]$ when $X$ is a discrete random variable taking values $x_1, x_2, \ldots, x_K$ with probabilities $p_1, p_2, \ldots, p_K$.

        Define $Y = a + b X$. The random variable $Y$ takes the value $a + b x_i$ with probability $p_i$. Its expected value is

        $$ \mathbb{E}[Y] = \sum_{i=1}^{K} (a + b x_i) \, p_i. $$

        Distribute the multiplication and split the sum into two parts,

        $$ \mathbb{E}[Y] = \sum_{i=1}^{K} a \, p_i + \sum_{i=1}^{K} b \, x_i \, p_i = a \sum_{i=1}^{K} p_i + b \sum_{i=1}^{K} x_i \, p_i. $$

        The first sum is $a$ times the total probability, which equals $1$ because the $p_i$ cover all possible outcomes. The second sum is $b$ times the expected value of $X$. So

        $$ \mathbb{E}[a + b X] = a \cdot 1 + b \cdot \mathbb{E}[X] = a + b \mathbb{E}[X]. $$

        The same argument extends to a sum of several random variables, giving linearity of the expected value in full generality.

        **The variance of a sum when the variables are not i.i.d.**

        Rule 5 in Section 3.5 covers the i.i.d. case, where the variance of a sum is $n$ times the variance of one variable. In general, the variance of a sum also depends on the covariances between every pair of variables,

        $$ \text{var}\left(\sum_{i=1}^{n} X_i\right) = \sum_{i=1}^{n} \text{var}(X_i) + 2 \sum_{i < j} \text{cov}(X_i, X_j). $$

        When the variables are i.i.d., every covariance is zero and the double sum drops out, leaving $\text{var}\left(\sum_{i=1}^{n} X_i\right) = n \sigma_X^2$. When the variables are not independent, the covariances do not vanish. Positive covariances make the sum more variable, and negative covariances make it less variable, so the variance of a sum is larger or smaller depending on whether the variables tend to move together or in opposite directions.
        """)

    mo.accordion({
        "## Appendix": mo.vstack([_text]),
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec2RandomVariables.html" target="_self">← Lecture 2</a>'),
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec4EstimationHypothesisTestingAndConfidenceIntervals.html" target="_self">Lecture 4 →</a>'),
        ],
        justify="space-between", align="center",
    )
    return


if __name__ == "__main__":
    app.run()
