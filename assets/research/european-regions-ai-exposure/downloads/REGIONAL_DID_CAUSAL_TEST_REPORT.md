# Regional DID significance and causal-identification diagnostics

25 November2026. Retrospective analysis, separate from prior country-industry analyses and descriptive208-region charts. Raw data and manuscript unchanged.

Primary sample is203regions,19identifying countries,2020–2025. Region and country×year fixed effects; fixed2022 employment weights. Young15–24 and older55–64 use their own baseline employment weights. The log youth/older ratio uses harmonic paired weights. Its coefficient is a paired age contrast; the separately weighted age coefficients should not be subtracted. A stacked-age DDD with region×age,region×year,country×year×age fixed effects reproduces the ratio coefficient and country-clustered standard error numerically.

Treatment is fixed2022 THAIE quintile5 versus1–4. Annual post starts2023. The three2020–2022 pre years include pandemic disruption and two months after ChatGPT launch in2022; no exact November2022 discontinuity is identified. Annual matching does not meet a three-year monthly pre/post design by itself. All earlier source observations were retained; graphs starting2022 do not determine the estimation sample.

Country-clustered CR1 t intervals and restricted country wild-bootstrap p-values are both reported. They are different inferential procedures and can disagree; primary significance interpretation uses the bootstrap. Draws9999,seed20261125. Bootstrap implementation checks compare fast reabsorbed calculations with direct recomputation. Holm adjustment covers three primary outcomes, all nine effect specifications, three joint-pretrend tests and three placebo tests as explicitly labelled families; these local families do not represent every historical exploratory analysis.

* Youth employment, ages 15–24: +2.6891%; nominal country-cluster t95% interval [0.1698, 5.2717]%; wild p=0.0746; primary-family Holm p=0.2238.
* Older employment, ages 55–64: +1.5078%; nominal country-cluster t95% interval [-0.5091, 3.5655]%; wild p=0.4150; primary-family Holm p=0.8300.
* Youth-to-older employment ratio: +1.3446%; nominal country-cluster t95% interval [-2.5245, 5.3673]%; wild p=0.4978; primary-family Holm p=0.8300.

Long-window sensitivity uses193regions,18countries,2018–2025; its cohort changes along with its time window. The group-linear-trend specification uses the same long cohort. Long youth nominal p=.0476 becomes.4284 across nine effect specifications and.2065 with a group linear trend. These results do not justify selecting a preferred specification by significance.

Joint pretrend restriction tests four leads2018–2021 relative to2022, with2023–2025 effects estimated jointly. In ALL_TESTS.csv the beta/interval fields in joint_pretrend rows describe the first event coefficient, not a single joint effect; p_wild tests all four specified leads. Full event coefficients are stored separately.

The placebo uses only2018–2021 and assigns a fake2020 break. COVID makes this a diagnostic for confounding patterns, not an alternative clean experiment. Non-rejection of pretrends or placebos is not proof of parallel trends or absence of confounding. Primary country information is concentrated, with a diagnostic effective information count of approximately4.8–4.9 despite19nominal clusters. Actual AI adoption is not observed; exposure is not random. The result does not establish a causal AI effect and does not prove no effect.

All15 tests are retained. Inputs, source SHA256, settings and numerical DDD verification are recorded in SCOPE.json and VALIDATION.json in the local analysis folder. No suppressed cells are reconstructed and no new employment imputation is introduced.
