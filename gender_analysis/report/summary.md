# Statistical Summary — Gender & Income Inequality

Total observations analyzed: **20**

## Descriptive statistics

### Overall

|   count |   mean |    std |   min |   25% |   50% |   75% |   max |
|--------:|-------:|-------:|------:|------:|------:|------:|------:|
|      20 | 3213.1 | 1136.2 |  1638 |  2175 |  3100 |  4175 |  5124 |

### By gender

| gender   |   count |   mean |   median |     std |
|:---------|--------:|-------:|---------:|--------:|
| Female   |      10 | 2586.2 |     2150 | 1129.61 |
| Male     |      10 | 3840   |     3850 |  758.95 |

### By race

| race   |   count |    mean |   median |    std |
|:-------|--------:|--------:|---------:|-------:|
| Black  |       5 | 2520    |     2600 | 609.92 |
| Brown  |       9 | 2715.33 |     2400 | 929.09 |
| White  |       6 | 4537.33 |     4550 | 442.95 |

## Hypothesis tests

- Welch t-test (Male vs Female): **t=2.913**, **p=0.0103**
- Mann–Whitney: **U=83.000**, **p=0.0140**

## Linear regression (log of income)

Model: `log_income ~ gender + race + school_years + age + age²`

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:             log_income   R-squared:                       0.915
Model:                            OLS   Adj. R-squared:                  0.875
Method:                 Least Squares   F-statistic:                     47.28
Date:                Wed, 22 Oct 2025   Prob (F-statistic):           4.37e-08
Time:                        18:09:54   Log-Likelihood:                 16.655
No. Observations:                  20   AIC:                            -19.31
Df Residuals:                      13   BIC:                            -12.34
Df Model:                           6                                         
Covariance Type:                  HC1                                         
===================================================================================
                      coef    std err          z      P>|z|      [0.025      0.975]
-----------------------------------------------------------------------------------
const               5.9189      0.919      6.441      0.000       4.118       7.720
is_female          -0.1313      0.079     -1.658      0.097      -0.287       0.024
race_black         -0.0050      0.131     -0.038      0.970      -0.262       0.252
race_brown         -0.0803      0.090     -0.893      0.372      -0.257       0.096
race_yellow     -6.088e-17   1.53e-16     -0.399      0.690    -3.6e-16    2.38e-16
race_indigenous -8.386e-18   1.24e-17     -0.676      0.499   -3.27e-17    1.59e-17
school_years        0.1144      0.020      5.732      0.000       0.075       0.154
age                 0.0402      0.059      0.678      0.498      -0.076       0.156
age2               -0.0004      0.001     -0.478      0.633      -0.002       0.001
==============================================================================
Omnibus:                        1.232   Durbin-Watson:                   1.206
Prob(Omnibus):                  0.540   Jarque-Bera (JB):                0.996
Skew:                          -0.317   Prob(JB):                        0.608
Kurtosis:                       2.109   Cond. No.                     3.73e+20
==============================================================================

Notes:
[1] Standard Errors are heteroscedasticity robust (HC1)
[2] The smallest eigenvalue is 2.4e-34. This might indicate that there are
strong multicollinearity problems or that the design matrix is singular.
```