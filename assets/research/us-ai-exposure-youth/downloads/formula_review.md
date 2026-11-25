# THAIE formula and aggregation review

The implemented task score agrees algebraically with equation (1) in the actual HSSC-submitted `THAIE_manuscript_review.zip/main.tex`. This checks the measurement equation, not equivalence between the Korean and American empirical designs. The US study uses its own O*NET–SOC–Census aggregation and GPT-5 capability benchmark.

The audited equations are

$$
\lambda_s=e_s p(d_s),\quad d_s=\exp(\widehat{\ell_s}),\quad
p(d)=\left[1+\exp\{-\kappa(\log_2 h_{50}-\log_2 d)\}\right]^{-1},\quad
\kappa=\frac{\ln 4}{\log_2(h_{50}/h_{80})}.
$$

For Census occupation c, matched SOC set K(c), O*NET suboccupations J(k), and task set S(j), the implemented hierarchy is

$$
\Lambda_c=\frac{1}{|K(c)|}\sum_{k\in K(c)}\frac{1}{|J(k)|}\sum_{j\in J(k)}\frac{1}{|S(j)|}\sum_{s\in S(j)}e_s p(d_s).
$$

The task score is e × p(d), where e is the clipped BGE RidgeCV prediction of exposure, d = exp(predicted natural-log minutes), and p(d) = logistic[k × (log2 h50 − log2 d)]. The slope is ln(4)/log2(h50/h80). GPT-5 inputs h50=203.012577 minutes and h80=38.312431 minutes imply k=0.5762577283029736. The completion curve returns exactly 0.5 at h50 and 0.8 at h80. No factor of 60 or natural-log/base-2 mismatch was found. The residual is e × (1−p); it is an algebraic residual and does not measure worker complementarity.

A fresh content RidgeCV fit and a fresh duration RidgeCV fit used the original task labels and embeddings. All 19,265 task identifiers align. Duration has 5,896 observed model-based source labels; predicted durations are finite and positive, ranging from 21.27 to 817.98 minutes. The content prediction is clipped into [0,1], affecting 2,131 predictions; this follows the specified estimator. The reconstructed completion factors differ from stored p by at most 2.78×10^-16. Reconstructed occupational E, THAIE, TIME, log duration, and TIME_SHARE differ from saved scores by at most 8.88×10^-16.

The audit verified 0≤THAIE≤e and e=THAIE+residual; completion declines with duration and increases with horizon at a fixed positive slope. It does not assert that curves belonging to different models, with different slopes, never cross. The simple TIME comparator is e×min(1,h50/d); TIME_SHARE is sum(e×d)/sum(d) within each O*NET suboccupation before the same outer averages. Neither comparator equals measured AI productivity.

The aggregation averages tasks within O*NET suboccupations, suboccupations within SOC, and matched SOCs within Census occupation. Explicitly reconstructed effective task weights sum to one for each retained Census occupation. These are equal hierarchical weights, not measured work-time or employment weights. They are intentionally different from pooling every task across an occupation.

One material coverage issue remains. Among 867 Census–SOC links, 69 lack a scored SOC (7.96%). Twenty-one Census occupations have no matched SOC and are excluded. Thirty-one of 547 retained Census occupations are partially covered (5.67%), including 22 with less than 80% link coverage (4.02%); minimum retained coverage is 50%. Pandas means renormalize over available linked scores. This is not arithmetic failure, but it can influence occupational scores and quintiles. A high-coverage-only sensitivity should report both the affected occupations and lost employment. Missing links must never be described as having zero exposure.

These checks validate implementation against the specified measurement construction. They do not validate transferring software benchmark completion curves to all workplace domains; source human durations are model estimates, not stopwatch observations. Fitted predictions on the rating sample are not independent out-of-sample measurement validation. Current regression uncertainty does not propagate uncertainty in e, d, horizons, or crosswalks. The fixed 2019 weights are historical, while the scores are retrospective. No manuscript was edited and no graph displayed.

The ≥80% SOC-link-coverage sensitivity preserves the original quintile labels and refits the same youth 47-month FT model. It yields −6.05% [−12.70, +1.11], p=.096, retaining 94.63% of primary-support FT employment. It excludes uncertain scores as a sensitivity rather than recalibrating the primary score after viewing results. This does not establish an effect and does not validate the missing links.
