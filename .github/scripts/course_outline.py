"""
The canonical course outline and the weekly release dial.

POSTED_THROUGH is the highest lecture number students can open. It drives:
  * the homepage lecture cards (build.py): lectures past the dial keep their
    card inside the group dropdown but get the red "Coming soon" badge and a
    disabled button, like unposted problem sets;
  * every notebook's sidebar outline and prev/next nav rows
    (update_sidebars.py): lectures past the dial appear as grey
    non-clickable text.

Weekly release: bump POSTED_THROUGH, commit, push. That is the whole
release - the site build runs update_sidebars.py itself before exporting,
so the sidebars and nav rows regenerate in CI. Running
    uv run .github/scripts/update_sidebars.py
locally is optional; it just keeps the notebooks in your working copy in
sync with what the deployed site shows.

LECTURES lists (number, short sidebar title, notebook stem). A stem of None
marks a notebook that has not been written yet; it appears in every sidebar
outline as a placeholder. When the notebook is written, fill in its stem and
rerun update_sidebars.py.
"""

POSTED_THROUGH = 2

BASE_URL = "https://robert-french.github.io/Econometrics"

LECTURES = [
    (1, "Introduction", "Lec1Introduction"),
    (2, "Random Variables", "Lec2RandomVariables"),
    (3, "Multiple Random Variables", "Lec3WorkingWithMultipleRandomVariables"),
    (4, "Estimation and Hypothesis Testing", "Lec4EstimationHypothesisTestingAndConfidenceIntervals"),
    (5, "Simple Linear Regression", "Lec5SimpleLinearRegression"),
    (6, "OLS Assumptions for Causal Inference", "Lec6OLSAssumptionsForCausalInference"),
    (7, "Inference and Omitted Variable Bias", "Lec7InferenceAndOmittedVariableBias"),
    (8, "Multiple Regression", "Lec8MultipleRegression"),
    (9, "Control Variables and Inference", "Lec9ControlVariablesAndInference"),
    (10, "Reading Regression Tables", "Lec10ReadingRegressionTables"),
    (11, "Nonlinear Regression: Polynomials", "Lec11NonlinearRegressionPolynomials"),
    (12, "Nonlinear Regression: Logarithms", "Lec12NonlinearRegressionLogarithms"),
    (13, "Nonlinear Regression: Interaction Terms", "Lec13NonlinearRegressionInteractionTerms"),
    (14, "Internal and External Validity", "Lec14InternalAndExternalValidity"),
    (15, "Panel Data I", "Lec15PanelDataI"),
    (16, "Panel Data II", "Lec16PanelDataII"),
    (17, "Binary Dependent Variable Regressions", None),
    (18, "Experiments", None),
    (19, "Quasi-Experiments", None),
]
