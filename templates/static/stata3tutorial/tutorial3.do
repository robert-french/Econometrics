* Stata Tutorial 1
* Robert French, 09/08/2026

display 2 + 2
display 10 / 4

local dataFolder "C:/Users/rober/Dropbox/LMU/Teaching/Econometrics/templates/static" 

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

* Stata Tutorial 3

regress earnings education

predict earningsHat
predict residual, residuals
summarize earningsHat residual

twoway (scatter earnings education, jitter(5)) (line earningsHat education, sort)
twoway (scatter residual education, jitter(5)), yline(0)
drop earningsHat residual

generate female = (sex == "Female")
tabulate sex female
regress earnings female
tabstat earnings, by(sex) statistics(mean n)

regress earnings age

regress earnings education, vce(robust)
regress earnings age, vce(robust)


