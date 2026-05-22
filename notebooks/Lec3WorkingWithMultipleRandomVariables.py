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

__generated_with = "0.23.6"
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

    return alt, mo, np, pd, stats


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md('<a href="https://robert-french.github.io/Econometrics/" target="_self" style="display: block; margin-bottom: 1.5em;">Course home</a>'),
            mo.md("# [Lecture 3](#top)"),
            mo.md("Working With Multiple Random Variables"),
            mo.nav_menu(
                {
                    "#sec1": "1. Joint, marginal, and conditional distributions",
                    "#sec2": "2. Covariance and correlation",
                    "#sec3": "3. Independence",
                    "#sec4": "4. Independent and identically distributed",
                    "#sec5": "5. Means and variances of sums",
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
            mo.md('<a href="https://robert-french.github.io/Econometrics/apps/Lec2RandomVariables.html" target="_self">← Lecture 2</a>'),
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

    1. [Joint, marginal, and conditional distributions](#sec1)
    2. [Covariance and correlation](#sec2)
    3. [Independence](#sec3)
    4. [Independent and identically distributed](#sec4)
    5. [Means and variances of sums](#sec5)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1. Joint, marginal, and conditional distributions

    In Lecture 2 we focused on one random variable at a time. We described its distribution, its expected value, and its spread. Most questions in econometrics, however, ask about two variables together. Does a person's earnings depend on their level of education? Does the unemployment rate depend on the inflation rate? To answer these questions we need to extend the tools from one random variable to two.

    A *joint probability distribution* describes how likely each combination of values is for two random variables. When $X$ takes possible values $x_1, x_2, \ldots, x_k$ and $Y$ takes possible values $y_1, y_2, \ldots, y_l$, the joint probability distribution lists $\mathbb{P}(X = x_i, Y = y_j)$ for every pair $(x_i, y_j)$. The table below shows one example.

    <div style="display:flex;justify-content:center;margin:1.2em 0;">
    <table style="border-collapse:collapse;text-align:center;">
    <tr><th style="padding:6px 18px;"></th><th style="padding:6px 18px;">x<sub>1</sub></th><th style="padding:6px 18px;">x<sub>2</sub></th><th style="padding:6px 18px;">x<sub>3</sub></th></tr>
    <tr><td style="padding:6px 18px;">y<sub>1</sub></td><td style="padding:6px 18px;">0.10</td><td style="padding:6px 18px;">0.15</td><td style="padding:6px 18px;">0.20</td></tr>
    <tr><td style="padding:6px 18px;">y<sub>2</sub></td><td style="padding:6px 18px;">0.20</td><td style="padding:6px 18px;">0.10</td><td style="padding:6px 18px;">0.25</td></tr>
    </table>
    </div>

    The six cells must sum to one because together they cover every possible outcome.

    A *marginal probability distribution* gives the distribution of a single variable, ignoring the other. We compute it by summing the joint probabilities over the values of the other variable. The marginal probability that $X = x_1$ is

    $$ \mathbb{P}(X = x_1) = \mathbb{P}(X = x_1, Y = y_1) + \mathbb{P}(X = x_1, Y = y_2) = 0.10 + 0.20 = 0.30. $$

    In general, $\mathbb{P}(X = x_i) = \sum_j \mathbb{P}(X = x_i, Y = y_j)$. Summing down each column gives the marginal distribution of $X$, and summing across each row gives the marginal distribution of $Y$, both shown below.

    <div style="display:flex;justify-content:center;gap:3em;margin:1.2em 0;">
    <table style="border-collapse:collapse;text-align:center;">
    <tr><th style="padding:6px 16px;border-bottom:1px solid #cbd2d9;" colspan="3">Marginal of X</th></tr>
    <tr><td style="padding:6px 16px;">x<sub>1</sub></td><td style="padding:6px 16px;">x<sub>2</sub></td><td style="padding:6px 16px;">x<sub>3</sub></td></tr>
    <tr><td style="padding:6px 16px;">0.30</td><td style="padding:6px 16px;">0.25</td><td style="padding:6px 16px;">0.45</td></tr>
    </table>
    <table style="border-collapse:collapse;text-align:center;">
    <tr><th style="padding:6px 16px;border-bottom:1px solid #cbd2d9;" colspan="2">Marginal of Y</th></tr>
    <tr><td style="padding:6px 16px;">y<sub>1</sub></td><td style="padding:6px 16px;">y<sub>2</sub></td></tr>
    <tr><td style="padding:6px 16px;">0.45</td><td style="padding:6px 16px;">0.55</td></tr>
    </table>
    </div>

    A *conditional probability distribution* gives the distribution of one variable, given the value of the other. The conditional probability that $Y = y_j$ given $X = x_i$ is

    $$ \mathbb{P}(Y = y_j \mid X = x_i) = \frac{\mathbb{P}(X = x_i, Y = y_j)}{\mathbb{P}(X = x_i)}. $$

    This formula is also known as *Bayes' rule*. It rewrites the question ''how likely is $Y = y_j$, knowing that $X = x_i$ has occurred?'' in terms of probabilities we can read off the table. For our example, the conditional probability that $Y = y_1$ given $X = x_1$ is

    $$ \mathbb{P}(Y = y_1 \mid X = x_1) = \frac{0.10}{0.30} = \frac{1}{3}. $$

    Bayes' rule turns up in many places, from medical testing to legal evidence. For this course, it is the bridge between the joint distribution and the conditional distribution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2. Covariance and correlation

    The joint distribution describes how two random variables behave together, but it does not summarize their relationship in one number. The *covariance* of $X$ and $Y$ summarizes whether they tend to move in the same direction or in opposite directions. It is defined as

    $$ \text{cov}(X, Y) \equiv \sigma_{XY} = \sum_i \sum_j (x_j - \mu_X)(y_i - \mu_Y) \cdot \mathbb{P}(X = x_j, Y = y_i). $$

    The sign of the covariance is what carries most of the meaning. A positive $\sigma_{XY}$ means that when $X$ is above its mean, $Y$ tends to be above its mean too, and the two tend to move together. A negative $\sigma_{XY}$ means one tends to be above its mean when the other is below it, so the two tend to move in opposite directions. A zero covariance means $X$ and $Y$ do not move together on average.

    The size of the covariance is harder to interpret because it depends on the units of $X$ and $Y$. The covariance between years of education and weekly earnings would be in (years $\times$ dollars), while the covariance between height and weight would be in (inches $\times$ pounds). The numbers are not comparable.

    To get a unit-free summary we divide by the standard deviations of $X$ and $Y$. The *correlation coefficient*, also written *correlation*, is

    $$ \text{corr}(X, Y) \equiv \rho_{XY} = \frac{\sigma_{XY}}{\sigma_X \sigma_Y}. $$

    The correlation always sits between $-1$ and $1$. A correlation of $+1$ means $Y$ is an exactly increasing linear function of $X$. A correlation of $-1$ means $Y$ is an exactly decreasing linear function of $X$. A correlation of $0$ means $X$ and $Y$ have no linear relationship on average.

    With data we do not observe $\sigma_{XY}$, $\sigma_X$, $\sigma_Y$ directly. We estimate them from a sample of $n$ paired observations $(X_1, Y_1), (X_2, Y_2), \ldots, (X_n, Y_n)$. The *sample covariance* is

    $$ \hat{\sigma}_{XY} = \frac{1}{n - 1} \sum_{i=1}^{n} (X_i - \hat{\mu}_X)(Y_i - \hat{\mu}_Y), $$

    and the *sample correlation* is

    $$ \widehat{\text{corr}}(X, Y) = \frac{\hat{\sigma}_{XY}}{\hat{\sigma}_X \hat{\sigma}_Y}. $$

    The \$594 weekly-earnings gap between high school graduates and bachelor's-degree holders from the BLS table in Lecture 1 is one way to summarize the relationship between education and earnings. The correlation between years of education and weekly earnings is another. The correlation uses every level of education at once, instead of just two, and reports the relationship as a single number between $-1$ and $1$.

    The plot below starts empty. Press and drag across it to spray points, building up a scatter of education-and-earnings pairs. The sample statistics under the plot update as you spray. Use the Reset button to clear the plot and start over. Try spraying along an upward line and watch the correlation climb toward $+1$; then spray a symmetric arch and watch the correlation fall back toward $0$ even though the points clearly follow a pattern.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Freehand "spray" scatter built as a self-contained HTML canvas. Dragging
    # the mouse (or a finger) sprays points; the sample variances, covariance,
    # and correlation are computed in JavaScript and shown beneath the plot.
    # This runs entirely client-side, so it works in the deployed WASM build
    # with no extra Python dependency.
    _spray_html = r"""
<!doctype html>
<html>
<head><meta charset="utf-8"><style>
  body { margin: 0; font-family: system-ui, -apple-system, sans-serif; color: #1f4e79; }
  #wrap { display: flex; flex-direction: column; align-items: center; padding: 6px; }
  canvas { border: 1px solid #cbd2d9; border-radius: 4px; cursor: crosshair; touch-action: none; }
  #controls { margin: 8px 0 4px; }
  button {
    font: inherit; color: #1f4e79; background: #eef3f8;
    border: 1px solid #1f4e79; border-radius: 4px; padding: 4px 14px; cursor: pointer;
  }
  button:hover { background: #dce7f1; }
  #stats { max-width: 560px; font-size: 0.9rem; line-height: 1.5; color: #6b7280; text-align: center; }
</style></head>
<body>
<div id="wrap">
  <canvas id="cv" width="560" height="340"></canvas>
  <div id="controls"><button id="reset">Reset</button></div>
  <div id="stats"></div>
</div>
<script>
  const cv = document.getElementById("cv");
  const ctx = cv.getContext("2d");
  const statsEl = document.getElementById("stats");
  const XMIN = 0, XMAX = 25, YMIN = 0, YMAX = 3000;
  const padL = 56, padR = 14, padT = 12, padB = 40;
  const plotW = cv.width - padL - padR;
  const plotH = cv.height - padT - padB;
  let points = [];
  let drawing = false;

  const toPxX = x => padL + (x - XMIN) / (XMAX - XMIN) * plotW;
  const toPxY = y => padT + (YMAX - y) / (YMAX - YMIN) * plotH;
  const toDataX = px => XMIN + (px - padL) / plotW * (XMAX - XMIN);
  const toDataY = py => YMAX - (py - padT) / plotH * (YMAX - YMIN);

  function drawAxes() {
    ctx.clearRect(0, 0, cv.width, cv.height);
    ctx.strokeStyle = "#eef1f4";
    ctx.fillStyle = "#6b7280";
    ctx.font = "11px system-ui, sans-serif";
    ctx.lineWidth = 1;
    // gridlines + ticks
    ctx.textAlign = "right"; ctx.textBaseline = "middle";
    for (let v = 0; v <= YMAX; v += 500) {
      const py = toPxY(v);
      ctx.strokeStyle = "#eef1f4";
      ctx.beginPath(); ctx.moveTo(padL, py); ctx.lineTo(cv.width - padR, py); ctx.stroke();
      ctx.fillText(v.toLocaleString(), padL - 6, py);
    }
    ctx.textAlign = "center"; ctx.textBaseline = "top";
    for (let v = 0; v <= XMAX; v += 5) {
      const px = toPxX(v);
      ctx.strokeStyle = "#eef1f4";
      ctx.beginPath(); ctx.moveTo(px, padT); ctx.lineTo(px, cv.height - padB); ctx.stroke();
      ctx.fillText(v, px, cv.height - padB + 6);
    }
    // axis frame
    ctx.strokeStyle = "#cbd2d9";
    ctx.strokeRect(padL, padT, plotW, plotH);
    // axis titles
    ctx.fillStyle = "#1f4e79";
    ctx.font = "12px system-ui, sans-serif";
    ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
    ctx.fillText("Years of education", padL + plotW / 2, cv.height - 6);
    ctx.save();
    ctx.translate(12, padT + plotH / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText("Weekly earnings (USD)", 0, 0);
    ctx.restore();
  }

  function drawPoints() {
    ctx.fillStyle = "rgba(31, 78, 121, 0.7)";
    for (const p of points) {
      ctx.beginPath();
      ctx.arc(toPxX(p.x), toPxY(p.y), 3, 0, 2 * Math.PI);
      ctx.fill();
    }
  }

  function redraw() { drawAxes(); drawPoints(); }

  function fmt(v, dec) {
    return v.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });
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
      sxx += (p.x - mx) ** 2;
      syy += (p.y - my) ** 2;
      sxy += (p.x - mx) * (p.y - my);
    }
    const varX = sxx / (n - 1), varY = syy / (n - 1), cov = sxy / (n - 1);
    const corr = (varX > 0 && varY > 0) ? cov / Math.sqrt(varX * varY) : 0;
    statsEl.textContent =
      "Based on n = " + n + " points:  sample var(X) = " + fmt(varX, 2) +
      ",  var(Y) = " + fmt(varY, 0) +
      ",  cov(X, Y) = " + fmt(cov, 1) +
      ",  corr(X, Y) = " + fmt(corr, 3) + ".";
  }

  function spray(px, py) {
    if (px < padL || px > cv.width - padR || py < padT || py > cv.height - padB) return;
    for (let i = 0; i < 3; i++) {
      const jx = px + (Math.random() - 0.5) * 16;
      const jy = py + (Math.random() - 0.5) * 16;
      const x = toDataX(jx), y = toDataY(jy);
      if (x >= XMIN && x <= XMAX && y >= YMIN && y <= YMAX) points.push({ x, y });
    }
    if (points.length > 2000) points = points.slice(points.length - 2000);
    redraw(); updateStats();
  }

  function pos(e) {
    const r = cv.getBoundingClientRect();
    const t = e.touches ? e.touches[0] : e;
    return [t.clientX - r.left, t.clientY - r.top];
  }

  cv.addEventListener("mousedown", e => { drawing = true; const [x, y] = pos(e); spray(x, y); });
  cv.addEventListener("mousemove", e => { if (drawing) { const [x, y] = pos(e); spray(x, y); } });
  window.addEventListener("mouseup", () => { drawing = false; });
  cv.addEventListener("mouseleave", () => { drawing = false; });
  cv.addEventListener("touchstart", e => { e.preventDefault(); drawing = true; const [x, y] = pos(e); spray(x, y); }, { passive: false });
  cv.addEventListener("touchmove", e => { e.preventDefault(); if (drawing) { const [x, y] = pos(e); spray(x, y); } }, { passive: false });
  cv.addEventListener("touchend", e => { e.preventDefault(); drawing = false; }, { passive: false });
  document.getElementById("reset").addEventListener("click", () => { points = []; redraw(); updateStats(); });

  redraw(); updateStats();
</script>
</body>
</html>
"""
    mo.iframe(_spray_html, height="470px")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3. Independence

    Two random variables are *independent* when knowing the value of one tells us nothing about the value of the other. In probability, that informal statement comes from three equivalent conditions. If $X$ and $Y$ are independent, then

    1. The conditional distribution of $Y$ does not depend on $X$, that is $\mathbb{P}(Y = y \mid X = x) = \mathbb{P}(Y = y)$ for every $x$ and $y$.
    2. The joint distribution factors into the product of the marginals, $\mathbb{P}(X = x, Y = y) = \mathbb{P}(X = x) \cdot \mathbb{P}(Y = y)$.
    3. The correlation and the covariance are both zero, $\text{corr}(X, Y) = \sigma_{XY} = 0$.

    Any one of these conditions can serve as the definition; the other two follow.

    A coin flip and an unrelated die roll are independent. Knowing that the coin landed heads tells us nothing about which face of the die is showing, so the conditional distribution of the die given the coin is the same as the unconditional distribution. The result of the first die in a pair, however, is not independent of the sum of the two dice. If we know the sum is $11$, then the first die is very likely a $5$ or a $6$, and definitely not a $1$, so the conditional distribution of the first die given the sum is different from the unconditional distribution.

    Independence is symmetric. If $X$ is independent of $Y$, then $Y$ is independent of $X$. The three conditions above are unchanged when $X$ and $Y$ are swapped.

    The third condition only goes one way. If $X$ and $Y$ are independent, then their correlation is zero. The converse, however, is not true. Two random variables can have zero correlation and still be dependent on each other, because correlation only captures the linear part of a relationship. You can see this for yourself in the scatter plot of Section 2. If you place points in a symmetric arch, the sample correlation stays near zero even though each point's height is fixed by its horizontal position, so the two coordinates are clearly dependent.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4. Independent and identically distributed

    A sequence of random variables $X_1, X_2, \ldots, X_n$ is *independently and identically distributed* (i.i.d.) when two conditions hold. First, every $X_i$ has the same distribution. Second, every pair of $X_i$ and $X_j$ with $i \ne j$ is independent. We write $X_i \stackrel{\text{i.i.d.}}{\sim} F$ for a sequence drawn i.i.d. from a distribution $F$.

    The sixty thousand households the Census Bureau surveys each month for the Bureau of Labor Statistics are treated as an i.i.d. sample from the population of U.S. households. Each household is drawn at random, so any one household's wage tells us nothing about the wages of the others (independence), and each draw comes from the same underlying population distribution of wages (identically distributed). This i.i.d. assumption is what lets us use the law of large numbers and the central limit theorem from the previous lecture on real survey data.

    Both parts of i.i.d. can fail in practice. Heights measured within the same family are not independent because tall parents tend to have tall children, so a parent's height is informative about a child's height. Heights are also not identically distributed across people of different ages, because children's heights are systematically smaller than adults'. Sampling a hundred members of one family would violate both conditions.

    The i.i.d. assumption is the starting point for the estimator properties we study in the next lecture. When it is in doubt, the methods of this course must be adjusted, and parts of the course later on (panel data, time series) deal with exactly those settings.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5. Means and variances of sums

    We often want to know the expected value and variance of a sum or weighted sum of random variables. A few short rules take care of most cases.

    The first rule is the *linearity of the expected value*, which the appendix proves. For any constants $a$ and $b$,

    $$ \mathbb{E}[a + b X] = a + b \mu_X. $$

    Linearity extends to a sum of several random variables. The expected value of a sum is the sum of the expected values, whether or not the variables are independent,

    $$ \mathbb{E}[X_1 + X_2 + \cdots + X_n] = \mathbb{E}[X_1] + \mathbb{E}[X_2] + \cdots + \mathbb{E}[X_n]. $$

    Variance has a similar but more restrictive rule. For constants $a$ and $b$,

    $$ \text{var}(a + b X) = b^2 \sigma_X^2. $$

    Covariance is symmetric and linear in each argument,

    $$ \text{cov}(X, Y) = \text{cov}(Y, X), \qquad \text{cov}(X, Y + Z) = \text{cov}(X, Y) + \text{cov}(X, Z). $$

    The variance of a sum, however, depends on whether the variables move together. When $X_1, X_2, \ldots, X_n$ are i.i.d. with variance $\sigma_X^2$, the cross covariances are zero, so the variance of the sum is simply $n$ times the variance of one,

    $$ \text{var}(X_1 + X_2 + \cdots + X_n) = n \sigma_X^2. $$

    When the variables are correlated, the cross covariances do not vanish, and the variance of the sum is larger or smaller depending on the sign of the correlations.

    The variance of the sample mean from Lecture 2 is a direct corollary. If $\hat{\mu}_X = \frac{1}{n}\sum_{i=1}^{n} X_i$ and the $X_i$ are i.i.d. with variance $\sigma_X^2$, then $\text{var}(\hat{\mu}_X) = n \sigma_X^2 / n^2 = \sigma_X^2 / n$, so $\sigma_{\hat{\mu}_X} = \sigma_X / \sqrt{n}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Key terms covered:** joint probability distribution, marginal "
            "probability distribution, conditional probability distribution, "
            "Bayes' rule, covariance, correlation, correlation coefficient, "
            "sample covariance, sample correlation, independence, "
            "independently and identically distributed (i.i.d.).\n\n"
            "**Key concepts covered:** linearity of the expected value, "
            "variance of a sum of i.i.d. random variables, zero correlation "
            "does not imply independence."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _text = mo.md(r"""
        This is bonus material. You will not be tested on the content of the appendix.

        **The covariance written with the expectation operator.**

        Section 2 defined the covariance as a double sum over the joint distribution. It can be written more compactly with the expectation operator,

        $$ \text{cov}(X, Y) \equiv \sigma_{XY} = \mathbb{E}\big[(X - \mu_X)(Y - \mu_Y)\big]. $$

        This is the same quantity. The expectation $\mathbb{E}[\cdot]$ is itself a probability-weighted sum, so expanding it reproduces the double sum from Section 2. More advanced treatments use this compact form throughout.

        **Proof of the linearity of the expected value.**

        We show that $\mathbb{E}[a + b X] = a + b \mathbb{E}[X]$ when $X$ is a discrete random variable taking values $x_1, x_2, \ldots, x_K$ with probabilities $p_1, p_2, \ldots, p_K$.

        Define $Y = a + b X$. The random variable $Y$ takes the value $a + b x_i$ with probability $p_i$. Its expected value is

        $$ \mathbb{E}[Y] = \sum_{i=1}^{K} (a + b x_i) \, p_i. $$

        Distribute the multiplication and split the sum into two parts,

        $$ \mathbb{E}[Y] = \sum_{i=1}^{K} a \, p_i + \sum_{i=1}^{K} b \, x_i \, p_i = a \sum_{i=1}^{K} p_i + b \sum_{i=1}^{K} x_i \, p_i. $$

        The first sum is $a$ times the total probability, which equals $1$ because the $p_i$ cover all outcomes. The second sum is $b$ times the expected value of $X$. So

        $$ \mathbb{E}[a + b X] = a \cdot 1 + b \cdot \mathbb{E}[X] = a + b \mathbb{E}[X]. $$

        The same argument extends to a sum of several random variables, giving linearity of the expected value in full generality.
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
