# Extended preperiod sensitivity

The same official files cover2017. This exploratory extension compares23prequarters2017Q1–2022Q3 with12QWI or11J2J postquarters;2022Q4 remains excluded. It is deliberately asymmetric and supplements, rather than replaces, the balanced primary comparison. Definitions, exposure, fixed effects, missingness rules and12industryclusters are unchanged.

All24main extended-window contrasts fail Holm24 correction. Youth new-hiring and nonemployment-entry estimates attenuate toward zero. The primary young-relative-to-older J2J hiring contrast also disappears. This reinforces sensitivity to the chosen preperiod, rather than establishing an AI-specific mechanism.

| product | age | outcome | estimate_pct | p_value | p_Holm24_primary |
| --- | --- | --- | --- | --- | --- |
| qwi | 22–24 | log_HirN_rate | -0.7012 | 0.8994 | 1.0000 |
| qwi | 22–24 | log_HirA_rate | -0.0607 | 0.9915 | 1.0000 |
| qwi | 22–24 | log_Sep_rate | -1.0581 | 0.8436 | 1.0000 |
| qwi | 22–24 | log_earnings | 2.4808 | 0.0466 | 1.0000 |
| qwi | 35–64 | log_HirN_rate | -5.6258 | 0.2098 | 1.0000 |
| qwi | 35–64 | log_HirA_rate | -4.3296 | 0.3321 | 1.0000 |
| qwi | 35–64 | log_Sep_rate | -2.3697 | 0.5990 | 1.0000 |
| qwi | 35–64 | log_earnings | 4.2285 | 0.1937 | 1.0000 |
| qwi | 22–24 relative to35–64 | log_HirN_rate | 5.1068 | 0.0571 | 1.0000 |
| qwi | 22–24 relative to35–64 | log_HirA_rate | 4.3358 | 0.1198 | 1.0000 |
| qwi | 22–24 relative to35–64 | log_Sep_rate | 1.0846 | 0.6233 | 1.0000 |
| qwi | 22–24 relative to35–64 | log_earnings | -1.7110 | 0.4949 | 1.0000 |
| j2j | 22–24 | log_NEHire_rate | 0.8304 | 0.8577 | 1.0000 |
| j2j | 22–24 | log_ENSep_rate | -0.4746 | 0.8845 | 1.0000 |
| j2j | 22–24 | log_J2JHire_rate | -4.3544 | 0.2439 | 1.0000 |
| j2j | 22–24 | log_earnings | 2.7091 | 0.0210 | 0.5048 |
| j2j | 35–64 | log_NEHire_rate | -4.6671 | 0.2261 | 1.0000 |
| j2j | 35–64 | log_ENSep_rate | -0.1337 | 0.9718 | 1.0000 |
| j2j | 35–64 | log_J2JHire_rate | -6.0310 | 0.0773 | 1.0000 |
| j2j | 35–64 | log_earnings | 3.6974 | 0.2364 | 1.0000 |
| j2j | 22–24 relative to35–64 | log_NEHire_rate | 5.6507 | 0.1641 | 1.0000 |
| j2j | 22–24 relative to35–64 | log_ENSep_rate | -0.1426 | 0.9613 | 1.0000 |
| j2j | 22–24 relative to35–64 | log_J2JHire_rate | 1.6232 | 0.6124 | 1.0000 |
| j2j | 22–24 relative to35–64 | log_earnings | -0.9873 | 0.7127 | 1.0000 |

## Pretrend diagnostics

The extended event study has12nonpandemic quarterly leads. With only12industryclusters their joint covariance has insufficient rank, so a full12restriction cluster Wald test is not available. The reported lower-dimensional diagnostic tests three calendar-year average leads2017,2018,2019. This examines annual pre-event divergence and does not test every within-year quarterly movement. Four seasonal reference quarters2021Q4–2022Q3 remain omitted. Failure to reject these annual restrictions cannot establish parallel trends.

| product | age | outcome | pretrend_p | pretrend_terms | pretrend_original_quarterly_terms | pretrend_quarterly_joint_singular |
| --- | --- | --- | --- | --- | --- | --- |
| j2j | 22–24 | log_ENSep_rate | 0.1833 | 3.0000 | 12.0000 | True |
| j2j | 22–24 | log_J2JHire_rate | 0.5360 | 3.0000 | 12.0000 | True |
| j2j | 22–24 | log_NEHire_rate | 0.5048 | 3.0000 | 12.0000 | True |
| j2j | 22–24 | log_earnings | 0.0605 | 3.0000 | 12.0000 | True |
| j2j | 22–24 relative to35–64 | log_ENSep_rate | 0.4808 | 3.0000 | 12.0000 | True |
| j2j | 22–24 relative to35–64 | log_J2JHire_rate | 0.1387 | 3.0000 | 12.0000 | True |
| j2j | 22–24 relative to35–64 | log_NEHire_rate | 0.0283 | 3.0000 | 12.0000 | True |
| j2j | 22–24 relative to35–64 | log_earnings | 0.9190 | 3.0000 | 12.0000 | True |
| j2j | 35–64 | log_ENSep_rate | 0.1797 | 3.0000 | 12.0000 | True |
| j2j | 35–64 | log_J2JHire_rate | 0.4486 | 3.0000 | 12.0000 | True |
| j2j | 35–64 | log_NEHire_rate | 0.8012 | 3.0000 | 12.0000 | True |
| j2j | 35–64 | log_earnings | 0.1222 | 3.0000 | 12.0000 | True |
| qwi | 22–24 | log_HirA_rate | 0.7379 | 3.0000 | 12.0000 | True |
| qwi | 22–24 | log_HirN_rate | 0.7272 | 3.0000 | 12.0000 | True |
| qwi | 22–24 | log_Sep_rate | 0.9526 | 3.0000 | 12.0000 | True |
| qwi | 22–24 | log_earnings | 0.0344 | 3.0000 | 12.0000 | True |
| qwi | 22–24 relative to35–64 | log_HirA_rate | 0.7391 | 3.0000 | 12.0000 | True |
| qwi | 22–24 relative to35–64 | log_HirN_rate | 0.7065 | 3.0000 | 12.0000 | True |
| qwi | 22–24 relative to35–64 | log_Sep_rate | 0.8764 | 3.0000 | 12.0000 | True |
| qwi | 22–24 relative to35–64 | log_earnings | 0.9253 | 3.0000 | 12.0000 | True |
| qwi | 35–64 | log_HirA_rate | 0.7746 | 3.0000 | 12.0000 | True |
| qwi | 35–64 | log_HirN_rate | 0.8641 | 3.0000 | 12.0000 | True |
| qwi | 35–64 | log_Sep_rate | 0.9080 | 3.0000 | 12.0000 | True |
| qwi | 35–64 | log_earnings | 0.0532 | 3.0000 | 12.0000 | True |

No images were displayed. Models remain exploratory with only three treated industry groups.
