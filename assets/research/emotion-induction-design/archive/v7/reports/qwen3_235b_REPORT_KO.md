# Qwen 235B 전체 실험 결과

기존7B와 동일한 모호108문항의 개입 결과다. 별도로 공식표본1356문항 전체의 위협·대조 조건을 측정했다. 각48조건으로5184개 고유키를 검증했다.

전체 위협 효과의95%구간은 템플릿군집3000회 bootstrap이다. 비중구간은 이미 학습된 방향과 고정fold에 조건부이며 자연적 정서매개비율을 뜻하지 않는다.

## 전체 위협 효과

- {"context_type": "amb", "rows": 108, "clusters": 108, "metric": "p_unknown", "record_mean": 0.8606215113296395, "threat_mean": 0.9416309297605049, "estimate_pp": 8.10094184308652, "ci_lo_pp": 4.176984444010065, "ci_hi_pp": 12.564940646777693, "denominator_established": true}
- {"context_type": "amb", "rows": 108, "clusters": 108, "metric": "full_unknown", "record_mean": 0.6665486054959362, "threat_mean": 0.15989008566198334, "estimate_pp": -50.665851983395285, "ci_lo_pp": -56.362323142051586, "ci_hi_pp": -44.40560027420123, "denominator_established": true}
- {"context_type": "amb", "rows": 108, "clusters": 108, "metric": "p_correct", "record_mean": 0.8606215113296395, "threat_mean": 0.9416309297605049, "estimate_pp": 8.10094184308652, "ci_lo_pp": 4.176984444010065, "ci_hi_pp": 12.564940646777693, "denominator_established": true}
- {"context_type": "amb", "rows": 108, "clusters": 108, "metric": "p_sp", "record_mean": 0.5712956542199196, "threat_mean": 0.5450096343164548, "estimate_pp": -2.628601990346488, "ci_lo_pp": -7.26085401623171, "ci_hi_pp": 2.2819136606099772, "denominator_established": false}
- {"context_type": "amb", "rows": 108, "clusters": 108, "metric": "mass", "record_mean": 0.7510410556008934, "threat_mean": 0.1656884088062187, "estimate_pp": -58.53526467946748, "ci_lo_pp": -63.042567124902526, "ci_hi_pp": -53.711001047173404, "denominator_established": true}

## 해석 제한

감정은 지정된8축 부분공간에 대한 표상이고 잔차는 그 공간 밖 성분이다. 잔차를 무감정이라고 해석하지 않는다. 상대 깊이47층이7B의14층과 기능적으로 같다는 보장은 없다. BF16 자기실행 결과이며 FP8 API 결과와 동일한 실행조건이 아니다. SDPA, 모델구조, 학습자료, 규모가 함께 달라지므로 차이를 규모 하나로 설명하지 않는다.

[{"context": "amb", "issue": "Conditional and full-vocabulary unknown changes have opposite signs; report both and choice mass."}]
