* Stata Tutorial 1
* Robert French, 09/08/2026

display 2 + 2
display 10 / 4

local dataFolder "C:/Users/rfrench5/Dropbox/LMU/Teaching/Econometrics/templates/static" 

use "`dataFolder'/econ3300_educ_income_2024.dta", clear 

describe
summarize earnings education

* Stata Tutorial 2

summarize earnings, detail
histogram earnings, normal
tabulate education
tabulate sex

tabstat earnings, by(education) statistics(mean sd n)
tabstat earnings, by(sex) statistics(mean sd n)

twoway (scatter earnings age) (lfit earnings age)
twoway (scatter earnings education, jitter(5)) (lfit earnings education)

correlate earnings education age
correlate earnings education age, covariance

egen meanEarnings = mean(earnings)
egen meanEducation = mean(education)
generate product = (earnings - meanEarnings) * (education - meanEducation)
summarize product
display r(sum) / (r(N) - 1)
drop meanEarnings meanEducation product