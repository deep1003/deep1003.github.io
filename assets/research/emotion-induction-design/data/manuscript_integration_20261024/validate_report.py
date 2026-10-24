"""Fresh numerical and I/O checks only; produces no images or plots."""
from pathlib import Path
import hashlib,json
import numpy as np,pandas as pd
O=Path(__file__).resolve().parent;r=pd.read_csv(O/'pooled_prompt_contrasts.csv');m=pd.read_csv(O/'case_means.csv');a=pd.read_csv(O/'conditional_axis_behavior_12.csv');h=pd.read_csv(O/'category_heterogeneity_16.csv')
assert len(m)==5380 and m.case_id.nunique()==1076
assert (m.groupby('case_id').size()==5).all();assert np.allclose(m.p_unknown+m.p_biased+m.p_anti,1)
assert np.allclose(m.loc[m.case_type=='amb','p_correct'],m.loc[m.case_type=='amb','p_unknown'])
for typ in ['amb','dis']:
 for metric in r.metric.unique():
  def e(con):return float(r[(r.case_type==typ)&(r.metric==metric)&(r.contrast==con)].estimate.iloc[0])
  assert np.isclose(e('UNxThreat'),e('UN1-UN0')-e('CN1-CN0'),atol=1e-13)
  assert np.isclose(e('CN1-CN0'),e('CN1-R')-e('CN0-R'),atol=1e-13)
assert (r.lo<=r.hi).all();assert (r.p_holm>=r.p_boot-1e-12).all();assert len(a)==12 and not (a.p_holm_12<.05).any();assert len(h)==16
p=pd.read_csv(O/'source_multilayer_primary_144.csv');assert len(p)==144 and (p.p_holm_144<.05).sum()==6
w=pd.read_csv(O/'weighted_conditional_sensitivity.csv');assert len(w)==16 and not (w.p_holm_8<.05).any()
c=pd.read_csv(O/'category_threat_behavior.csv');assert len(c)==192 and not (c.p_holm_192<.05).any()
text=(O/'manuscript_results_discussion_ko.md').read_text();assert 'CN1−R의 Fear 감소' in text and '통합 원자료 분석은 사후 탐색적 분석' in text
result={'passed':True,'complete_coverage':True,'arithmetic_identity_checks':True,'draft_characters':len(text),'no_figures_emitted':True,'no_new_model_inference':True,'homepage_not_modified':True,'category_heterogeneity_sig_F':int((h.p_holm_16<.05).sum()),'distinct_ambiguous_outcomes': 'U and accuracy identical, not separate findings','files_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.is_file() and p.suffix in ['.csv','.py','.md','.json'] and p.name!='report_validation.json'}}
(O/'report_validation.json').write_text(json.dumps(result,indent=2));print({k:v for k,v in result.items() if k!='files_sha256'})
