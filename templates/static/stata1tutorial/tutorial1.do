* Stata Tutorial 1
* Robert French, 09/08/2026

display 2 + 2
display 10 / 4

local dataFolder "C:/Users/rfrench5/Dropbox/LMU/Teaching/Econometrics/templates/static" 

use "`dataFolder'/econ3300_educ_income_2024.dta", clear 

describe

summarize earnings education