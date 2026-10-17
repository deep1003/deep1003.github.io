"""Cached-only EXAONE appendix rendering and local publication; no model calls."""
from pathlib import Path
import json,shutil,time,hashlib,base64,zipfile,importlib.util
import numpy as np,pandas as pd,nbformat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
B=Path(__file__).resolve().parent;R=B.parent
P=Path('/Users/deep1003/Library/Mobile Documents/com~apple~CloudDocs/data3/fear_axis_pilot/output/jupyter-notebook/uncertainty_self_threat_139')
SITE=Path('/Users/deep1003/Library/Mobile Documents/com~apple~CloudDocs/data3/deep1003.github.io/assets/research/emotion-induction-design')
F=B/'figures';F.mkdir(exist_ok=True)
def m2():
 items=pd.read_csv(R/'items_139.csv');d=pd.read_csv(R/'results/trials.csv');s=json.loads((R/'results/summary.json').read_text());assert [r['term'] for r in s['primary']]==['uncertainty','threat','combined'];v=d.groupby(['item','condition']).p_unknown.mean().unstack().reindex(items.sample_id);g=items.cluster.astype('category').cat.codes.to_numpy();n=g.max()+1;w=np.random.default_rng(20261017).multinomial(n,np.ones(n)/n,size=10000)[:,g].astype(float);w/=w.sum(1,keepdims=True);colors=json.loads((P/'color-specification.json').read_text())['condition_colors']
 fig,ax=plt.subplots(1,2,figsize=(11,4.7))
 for t in range(2):
  ys=[]
  for u in range(2):
   c=f'U{u}T{t}';values=v[c].to_numpy()*100;lo,hi=np.quantile(w@values,[.025,.975]);y=values.mean();ys.append(y);label=c.replace('U','UN').replace('T','FA');ax[0].errorbar(u,y,yerr=[[y-lo],[hi-y]],fmt='o',capsize=4,color=colors[label],label=label)
  ax[0].plot([0,1],ys,color='#999999',ls='--' if t else '-',alpha=.6)
 ax[0].set(xticks=[0,1],xticklabels=['Not explicit','Explicit'],xlabel='Uncertainty wording',ylabel='P(unknown) (%)',title='A. Four-condition behavioral results');h,l=ax[0].get_legend_handles_labels();order=[0,2,1,3];ax[0].legend([h[i] for i in order],[l[i] for i in order],fontsize=8)
 for i,r in enumerate(s['primary']):
  y=100*r['estimate'];ax[1].errorbar(y,i,xerr=[[(r['estimate']-r['ci_low'])*100],[(r['ci_high']-r['estimate'])*100]],fmt='o',capsize=4,color=['#C34835','#2868A3','#8054A1'][i]);ax[1].annotate(f"Holm p = {r['p_holm']:.4f}",(y,i),xytext=(5,10),textcoords='offset points',fontsize=8)
 ax[1].axvline(0,color='#999999',ls=':');ax[1].set(yticks=range(3),yticklabels=['Uncertainty','Deletion threat','Combined (11 minus 00)'],xlabel='Effect (percentage points)',title='B. Effects including the combined contrast');ax[1].invert_yaxis();ax[1].margins(x=.35,y=.4);fig.suptitle('EXAONE3.5-7.8B Q4_K_M: exploratory replication');fig.text(.5,.01,'139 reused items; 91 clusters; 10,000 paired bootstrap draws. Pointwise 95% CIs; Holm3 for the displayed family.',ha='center',fontsize=8);fig.tight_layout(rect=[0,.04,1,.94])
 for ext in ['png','pdf','svg']:fig.savefig(F/('EXAONE_M2_behavior.'+ext),dpi=600)
 plt.close(fig)
def representations():
 assert json.loads((B/'validation.json').read_text())['all_axes_passed']
 s=(P/'emotion_atlas.py').read_text().replace("AXIS_DATA=BASE/'representation_analysis/results/d335ad178e3c'","AXIS_DATA=BASE").replace("ITEM_DATA=BASE/'representation_analysis/item_category_alignment/output/item_alignment.csv'","ITEM_DATA=BASE/'item_alignment.csv'").replace("OUT=BASE/'representation_analysis/emotion_atlas/output'","OUT=BASE/'figures/atlas'").replace('axes_qwen_L14.npz','axes_exaone_L16.npz').replace('data.layer==14','data.layer==16').replace('pooled.layer==14','pooled.layer==16').replace('Qwen2.5-7B-Instruct, L14','EXAONE3.5-7.8B Q4_K_M, L16').replace('L14 centered','L16 centered')
 # Frozen geometry and all item-rotation values retained; only model/data paths change.
 p=B/'exaone_atlas.py';p.write_text(s);sp=importlib.util.spec_from_file_location('exaone_atlas',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.build(False)
 for ext in ['png','pdf','svg']:shutil.copy2(F/'atlas'/('Emotion_atlas_change_en.'+ext),F/('EXAONE_M3_alignment.'+ext))
 s=(P/'prompt_text_figure.py').read_text().replace("DATA=BASE/'representation_analysis/token_highlights/output'","DATA=BASE").replace("['14']","['16']").replace('layer 14','layer 16').replace("'layer':14","'layer':16").replace('Prompt text linked to internal concept alignment','EXAONE prompt text and internal alignment')
 p=B/'exaone_prompt_figure.py';p.write_text(s);sp=importlib.util.spec_from_file_location('exaone_prompt_figure',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.build('FA',False)
 for ext in ['png','pdf','svg']:shutil.copy2(F/('Prompt_text_activation_FA_en.'+ext),F/('EXAONE_M4_tokens.'+ext))
def publish():
 stamp=time.strftime('%Y%m%d_%H%M%S');bak=B/'backups'/stamp;bak.mkdir(parents=True,exist_ok=True);available=[('M2','EXAONE_M2_behavior','Behavioral results; combined effect = 11 minus 00'),('M3','EXAONE_M3_alignment','Within-item concept alignment changes, EXAONE layer16'),('M4','EXAONE_M4_tokens','Original Korean prompt and measured token-level alignment')];available=[x for x in available if (F/(x[1]+'.png')).exists()];complete=len(available)==3
 asset=SITE/'figures/exaone';asset.mkdir(parents=True,exist_ok=True);project=P/'supplements/exaone';project.mkdir(parents=True,exist_ok=True)
 for _,stem,_ in available:
  for ext in ['png','pdf','svg']:shutil.copy2(F/(stem+'.'+ext),asset/(stem+'.'+ext));shutil.copy2(F/(stem+'.'+ext),project/(stem+'.'+ext))
 for source in [R/'results/comparison.csv',R/'results/summary.json',B/'validation.json',B/'heldout_checks.csv',B/'manifest.json']:
  if source.exists():shutil.copy2(source,project/source.name)
 html=SITE/'index.html';shutil.copy2(html,bak/'website.html');soup=BeautifulSoup(html.read_text(),'html.parser');old=soup.find(id='exaone-replication')
 if old:old.decompose()
 s=json.loads((R/'results/summary.json').read_text());tr=''.join(f"<tr><td>{label}</td><td>{r['estimate']*100:+.2f}%p</td><td>{r['p_holm']:.4f}</td></tr>" for label,r in zip(['불확실성 표현','삭제 위협','복합 효과 (11−00)'],s['primary']))
 figs=''.join(f'<figure><img loading="lazy" src="figures/exaone/{stem}.png" alt="EXAONE {k}: {title}"/><figcaption>EXAONE {k}. {title}</figcaption><a href="figures/exaone/{stem}.pdf">PDF</a> · <a href="figures/exaone/{stem}.svg">SVG</a></figure>' for k,stem,title in available)
 note='동일 Q4_K_M 가중치에서 중간층16/32의 실제 활성값을 수집했습니다. 고정앵커·분리된검증문장의 paired accuracy≥.75 및 AUC≥.75를 통과했습니다. M3는139문항×3선택지순서의각조건을동일문항00과대응비교하며, M4는실제토큰바이트와한국어원문의대응을검증했습니다. 내부정렬은실제정서나토큰의인과기여가아닙니다.' if complete else 'M3·M4 실제 내부활성 수집 및 개념축 검증이 진행 중입니다. 검증 전 그림은 표시하지 않습니다.'
 section=f'<section id="exaone-replication"><h2>별첨 · 모델 ablation test · EXAONE3.5-7.8B</h2><p>동일139문항·네조건·세선택지순서. 복합효과는UN1FA1−UN0FA0이며 상호작용과 다릅니다. 91템플릿군집대응bootstrap10000회 및 세대비Holm보정. 기존103회는보존했고, 행동결과는전체출력로짓에서선택지1·2·3을직접측정했습니다.</p><table><tr><th>효과</th><th>변화</th><th>Holm p</th></tr>{tr}</table>{figs}<p>{note}</p><p>재사용선별문항의탐색결과이며 모델·정밀도·템플릿이달라 순수한모델크기효과를식별하지않습니다.</p></section>';soup.main.append(BeautifulSoup(section,'html.parser'))
 for appendix in soup.find_all('section'):
  if appendix.get('id') not in ['publication-supplement','gemma-replication','ministral-replication','exaone-replication','model-ablation-overview']:continue
  if not appendix.find('details',class_='appendix-collapse',recursive=False):
   heading=appendix.find(['h2','h3'],recursive=False);fold=soup.new_tag('details',attrs={'class':'appendix-collapse'});summary=soup.new_tag('summary');summary.append(heading.extract() if heading else '별첨 펼치기');fold.append(summary)
   for node in list(appendix.contents):fold.append(node.extract())
   appendix.append(fold)
  for fold in appendix.find_all('details'):fold.attrs.pop('open',None)
 html.write_text(str(soup))
 for path,is_main in [(R/'RUN_exaone35_direct_139.ipynb',False),(P.parent/'uncertainty_self_threat_139.ipynb',True)]:
  shutil.copy2(path,bak/path.name);nb=nbformat.read(path,4);nb.cells=[c for c in nb.cells if 'exaone_appendix' not in c.metadata.get('tags',[])];md=nbformat.v4.new_markdown_cell('## EXAONE supplementary figures\nModel-replacement ablation test against the Qwen2.5-7B main study.\nCombined effect = UN1FA1−UN0FA0. 139 reused items, 91 clusters, bootstrap10000, Holm3.\n\n'+note);md.metadata.tags=['exaone_appendix'];nb.cells.append(md)
  for name,stem,title in available:
   target=project/(stem+'.png') if is_main else F/(stem+'.png');c=nbformat.v4.new_code_cell(f"# Cached {name}: no model inference\nfrom IPython.display import display, Image\ndisplay(Image(filename={str(target)!r}))");c.metadata.tags=['exaone_appendix'];c.outputs=[nbformat.v4.new_output('display_data',data={'image/png':base64.b64encode(target.read_bytes()).decode(),'text/plain':title})];nb.cells.append(c)
  nbformat.write(nb,path)
 shutil.copy2(P.parent/'uncertainty_self_threat_139.ipynb',SITE/'downloads/uncertainty_self_threat_139.ipynb')
 # Keep the existing downloadable cached notebook bundle coherent; no inference is embedded.
 zip_path=SITE/'downloads/notebook_cached_analysis.zip';shutil.copy2(zip_path,bak/zip_path.name);nb=nbformat.read(P.parent/'uncertainty_self_threat_139.ipynb',4)
 for c in nb.cells:
  if c.cell_type=='code':c.outputs=[];c.execution_count=None
 for c in nb.cells:
  if 'exaone_appendix' in c.metadata.get('tags',[]) and c.cell_type=='code':
   for _,stem,_ in available:c.source=c.source.replace(repr(str(project/(stem+'.png'))),"str(folder / 'supplements/exaone/"+stem+".png')")
 updates={'uncertainty_self_threat_139.ipynb':nbformat.writes(nb).encode()}
 for f in project.glob('*'):updates['uncertainty_self_threat_139/supplements/exaone/'+f.name]=f.read_bytes()
 temp=zip_path.with_suffix('.tmp')
 with zipfile.ZipFile(zip_path) as z,zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED) as out:
  for i in z.infolist():
   if i.filename not in updates:out.writestr(i,z.read(i.filename))
  for k,v in updates.items():out.writestr(k,v)
 temp.replace(zip_path)
 manifest=dict(figures=[x[0] for x in available],complete=complete,website=str(html),deployment='local only; no push',original_results_preserved=True,contrast='combined=UN1FA1-UN0FA0',assets=[dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in F.glob('EXAONE_M*.*')]);(B/'publication_manifest.json').write_text(json.dumps(manifest,indent=2))
 p=SITE/'sync-manifest.json';m=json.loads(p.read_text());records={r['website']:r for r in m['records']}
 for r in records.values():
  f=SITE/r['website']
  if f.exists():r['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
 for f in asset.glob('*'):records[str(f.relative_to(SITE))]=dict(source=str(f),website=str(f.relative_to(SITE)),sha256=hashlib.sha256(f.read_bytes()).hexdigest())
 m['records']=list(records.values());m['exaone_appendix']=manifest;p.write_text(json.dumps(m,ensure_ascii=False,indent=2))
 print('Published local EXAONE appendix:',manifest['figures'],flush=True)
def finish():representations();publish()
if __name__=='__main__':m2();publish()
