# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(
    app_title="Stata Tutorial 1: Getting Started with Stata",
    css_file="../marimo-overrides.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


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
                '<h1 style="margin: 0.25em 0 0;"><a href="#top">Stata Tutorial 1</a></h1>'
                '</div>'
            ),
            mo.md(
                r"""
                **Getting Started with Stata**

                1. [Installing Stata](#sec1)
                1. [A first look at Stata](#sec2)
                1. [Do-files](#sec3)
                1. [Folders and file paths](#sec4)
                1. [Downloading the course dataset](#sec5)
                1. [Loading the dataset with a local](#sec6)
                1. [describe and summarize](#sec7)
                """
            ),
        ],
        width="300px",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    <a href="https://robert-french.github.io/Econometrics/" target="_self">← Course home</a>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="top"></a>
    # Stata Tutorial 1: Getting Started with Stata

    This tutorial walks you through your first Stata session, from installing the
    program to running your first commands on real data. The gray code blocks show
    Stata commands. They do not run in the browser, so open Stata and type along
    as you read. By the end you will have a working do-file that loads a dataset
    from your computer and reports descriptive statistics for it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contents

    1 [Installing Stata](#sec1)<br>
    2 [A first look at Stata](#sec2)<br>
    3 [Do-files](#sec3)<br>
    4 [Folders and file paths](#sec4)<br>
    5 [Downloading the course dataset](#sec5)<br>
    6 [Loading the dataset with a local](#sec6)<br>
    7 [describe and summarize](#sec7)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>
    ## 1 Installing Stata

    LMU provides Stata 19 SE to students for free. To install it on your own
    computer:

    1. Go to the ITS
       <a href="https://its.lmu.edu/whatwedo/computingsoftware/at-homesoftware/at-homesoftwareforstudents/" target="_blank">At-Home Software for Students</a>
       page.
    2. Click on the Stata link in the software list and follow the instructions to ''click here'' to install Stata.
    3. Log in to your LMU account and download the installer for Mac or Windows depending on your operating system
    4. Record the license information shown on the page (Serial number, Code, Authorization).
    5. Run the installer, accepting the default options, and enter the license
       information when prompted.

    If you cannot install Stata on your computer, ask for help from your peers or talk with me before class.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata1tutorial/stata1_shot1_its_page.png" alt="The ITS At-Home Software page with Stata in the software list" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>
    ## 2 A first look at Stata

    Open Stata. The window is split into several panes. The three you will use
    constantly are:

    - The **Command** window at the bottom, where you type commands.
    - The **Results** window in the middle, where Stata prints what each command
      produced.
    - The **Variables** pane on the right, which lists the variables in the
      dataset that is currently loaded (its default is empty).

    Try your first command. Click in the Command window, type the line below, and
    press Enter.

    ```stata
    display 2 + 2
    ```

    Stata echoes the command in the Results window and prints the answer, `4`.
    Every Stata command follows this pattern. You issue a command, and Stata prints
    the result.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata1tutorial/stata1_shot2_first_look.png" alt="The Stata window after running display 2 + 2" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>
    ## 3 Do-files

    Typing commands one at a time is fine for quick experiments, but real work
    happens in a *do-file*. A do-file is a plain text file of Stata commands that
    Stata runs from top to bottom. Do-files matter because your analysis should be
    *reproducible*. Six weeks from now you should be able to rerun your work with
    one click and get exactly the same results, and I should be able to run your
    do-file and see everything you did in your problem set solutio or research project.
    In this course, all of your Stata work belongs in a do-file.

    To create one, click the **New Do-file Editor** button on the toolbar (or press
    Ctrl+9 on Windows, Cmd+9 on Mac). A blank text editor will open that you can type on.
    Type the lines below to get started:

    ```stata
    * Stata Tutorial 1
    * Your name, and today's date

    display 2 + 2
    display 10 / 4
    ```

    Lines that start with `*` are comments. Stata ignores them, and you should use
    them generously to remind your future self what each part of a do-file does.
    You can also put a comment at the end of a line by typing `//`.

    Save the file as `tutorial1.do`, then run it with the **Execute (do)** button
    at the top right of the editor (Ctrl+D on Windows, Shift+Cmd+D on Mac). Stata
    runs every line in order and prints the results. If you highlight only some lines
    first, the same button runs just the highlighted lines, which is handy for
    testing one piece of a longer file. Keep this do-file open. You will add to it
    for the rest of the tutorial.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata1tutorial/stata1_shot3_dofile_editor.png" alt="The Do-file Editor with a first do-file" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>
    ## 4 Folders and file paths

    Stata reads data from files on your computer, so you need a tidy place to keep
    them. Create a folder for this course somewhere you can find it again, with a
    `data` folder inside it. For example:

    - Windows: `C:/Users/yourname/Documents/ECON3300/data`
    - Mac: `/Users/yourname/Documents/ECON3300/data`

    A *file path* like these is simply the address of a folder or file. You will
    need to paste your data folder's path into your do-file in the next section,
    and the easiest way to get it exactly right is to copy it rather than type it.

    **On Windows.** Open File Explorer and navigate into your `data` folder. Click
    the address bar at the top of the window, and the path appears as text,
    already selected. Press Ctrl+C to copy it. (You can also right-click the
    folder while holding Shift and choose "Copy as path.")

    **On a Mac.** Open Finder and navigate to your `data` folder. Right-click the
    folder, then press and hold the Option key. The menu item "Copy" changes to
    **"Copy 'data' as Pathname"**. Click it to copy the path.

    Note that Windows writes paths with backslashes, like
    `C:\Users\yourname\Documents\ECON3300\data`. Stata prefers forward slashes,
    and forward slashes work on both Windows and Mac, so after pasting a Windows
    path into your do-file, replace each `\` with `/`. Backslashes have a special
    meaning in Stata and can silently break the commands in the next section.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>
    ## 5 Downloading a Stata dataset

    Let's start working with some data. Click the link below to download a sample dataset
    recording information on education, earnings, and a few other individual characteristics.

    <a href="https://robert-french.github.io/Econometrics/stata1tutorial/econ3300_educ_income_2024.dta" download>
    <strong>Download the dataset: econ3300_educ_income_2024.dta</strong></a>

    Your browser will automatically save it to your Downloads folder. Move the file from Downloads
    into the `data` folder you created in the previous section.

    Files ending in `.dta` are Stata's own data format. Double-clicking one opens
    it in Stata. However, in this course we always load data with a
    command inside a do-file, so the do-file documents where the data came from.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec6"></a>
    ## 6 Loading the dataset with a local

    You could load the dataset by writing its full path directly into the `use`
    command. Instead, we will store the path once in a *local* and refer to the
    local everywhere else. A local is a named piece of text. You define it with
    the `local` command, and you plug its contents into another command by
    wrapping the name in a backtick `` ` `` on the left and an apostrophe `'` on
    the right. The backtick is on the same key as the tilde `~`, in the top left
    corner of most keyboards.

    Add the following lines to your do-file, replacing the path (i.e., the file location inside the quotations) with the one you
    copied from your own computer in Section 4.

    ```stata
    local dataFolder "C:/Users/yourname/Documents/ECON3300/data"

    use "`dataFolder'/econ3300_educ_income_2024.dta", clear
    ```

    The first line stores the path to your data folder in a local named `dataFolder`.

    The second line loads the dataset. Stata replaces `` `dataFolder' `` with the stored path, so the `use` command sees the full path to the file.

    The `clear` option tells Stata to remove any data currently in memory before loading the new dataset. Without it, Stata will refuse to replace unsaved data.

    Why use a local? Using a local means your data path appears only once, at the top of the do-file. If you later load the data again, save results, or move the project to another computer, you only need to update that one line. It also makes your do-file more portable; a classmate or I can run it after changing only the path at the top.

    **Run the whole do-file, not individual lines.** A local exists only while the do-file is running. If you run the `use` line by itself, `` `dataFolder' `` will be empty, and Stata will report `file /econ3300_educ_income_2024.dta not found`.  When in doubt, run the do-file from the top using the Execute (do) button.

    After the do-file runs successfully, check the Variables pane on the right. You should see the variables from the dataset listed there, confirming that the data loaded correctly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata1tutorial/stata1_shot4_use_local.png" alt="Stata after loading the dataset with a local" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec7"></a>
    ## 7 describe and summarize

    With the data loaded, two commands give you a first look at any dataset.

    **`describe`** reports the dataset's structure. It tells you how many observations (rows) and variables (columns) it contains, along with each variable's name, storage type, and label. Add it to your do-file after the `use` line and rerun the file.

    ```stata
    describe
    ```

    The output from `describe` tells you how many observations are in the dataset and how many variables it contains. In this dataset, each observation represents a person, so the number of observations tells you how many people are in the sample. The table below the header lists each variable and provides information about how Stata stores and labels it.

    Get in the habit of running `describe` immediately after loading a dataset. It helps you understand what you are working with and can quickly reveal mistakes, such as loading the wrong file.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata1tutorial/stata1_shot5_describe.png" alt="describe output for the course dataset" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`summarize`** reports descriptive statistics for the variables in your dataset. On its own, it reports statistics for every variable. You can also name specific variables to focus only on them. Add this line to your do-file and rerun the file.

    ```stata
    summarize earnings education
    ```

    Each row of the output corresponds to one variable. The `Obs` column reports the number of observations with a value for that variable. The `Mean` column reports the sample mean, `Std. dev.` reports the sample standard deviation, and `Min` and `Max` report the smallest and largest values.

    These are the estimators from Lecture 2. The `Mean` column reports the sample mean $\hat{\mu}_X$, while the `Std. dev.` column reports the sample standard deviation $\hat{\sigma}_X$. Both are calculated using the observations in this sample.

    Now look at the `Max` value for `earnings`. Survey datasets sometimes use special numeric codes for missing or top-coded values, so unusually large or otherwise suspicious values can signal that the data need to be cleaned before analysis. Spotting values like these is one reason we run `summarize` before beginning our analysis. We will deal with cleaning steps, including dropping these codes, in the next tutorial.

    Your complete do-file should now look something like this.

    ```stata
    * Stata Tutorial 1
    * Your name, and today's date
    local dataFolder "C:/Users/yourname/Documents/ECON3300/data"
    use "`dataFolder'/econ3300_educ_income_2024.dta", clear
    describe
    summarize earnings education
    ```

    Save your do-file. We will add to this do-file during our next Stata tutorial!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="https://robert-french.github.io/Econometrics/stata1tutorial/stata1_shot6_summarize.png" alt="summarize output for earnings and education" style="max-width:100%;border:1px solid #cbd2d9;border-radius:6px;">
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**Terms:** do-file, comment, file path, working folder, local, "
            "`use`, `clear`, `describe`, `summarize`.\n\n"
            "**Habits:** keep all Stata work in a do-file; store your data "
            "folder's path in a local at the top; run the whole do-file rather "
            "than single lines; run `describe` and `summarize` immediately "
            "after loading any dataset."
        ),
        title="Key terms and habits",
        kind="info",
    )
    return


if __name__ == "__main__":
    app.run()
