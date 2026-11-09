import {createRiskIndex,searchRisks} from './risk-search-engine.js';
import {extractFileText,MAX_TEXT_LENGTH} from './file-text.js';
const form=document.querySelector('#document-search-form'),input=document.querySelector('#document-text');
const upload=document.querySelector('#document-file'),status=document.querySelector('#document-status');
const output=document.querySelector('#document-results'),submit=document.querySelector('#document-submit');
let indexPromise,reading=false,uploadVersion=0,lastResults=[];
const node=(tag,text,cls)=>{const el=document.createElement(tag);if(text)el.textContent=text;if(cls)el.className=cls;return el;};
function index(){return indexPromise??=(async()=>{const r=await fetch('taxonomy.json?v=20261109-v10');if(!r.ok)throw Error('분류체계를 불러오지 못했습니다. 다시 시도해 주세요.');return createRiskIndex(await r.json());})().catch(e=>{indexPromise=null;throw e;});}
function link(id,text){const a=node('a',text);a.href='#'+id;return a;}
function render(results){
 output.replaceChildren();
 if(!results.length){output.append(node('p','관련 표현이 충분히 일치하는 리스크를 찾지 못했습니다. AI의 기능, 처리하는 정보, 행동과 예상되는 피해를 더 구체적으로 입력해 주세요.'));return;}
 const summary=node('div','', 'document-summary');
 const counts=new Set(results.map(x=>x.row.L3_ID));
 summary.append(node('h3',`L3 ${counts.size}개 범주 · L4 ${results.length}개 잠재 리스크 후보`));
 summary.append(node('p','정의와 입력 내용의 표현 유사성에 따른 검색 결과입니다. 발생 가능성·심각도나 실제 리스크의 존재를 판정하지 않으며, 부정·가정·완화 조치의 맥락은 직접 확인해 주세요.','muted'));
 output.append(summary);
 const root=node('details','', 'search-root');root.open=true;root.append(node('summary',`L0 · ${results[0].row.L0_Title_ko}`));output.append(root);
 for(const domain of ['General','Agentic','Physical']){
  const domainRows=results.filter(r=>r.domain===domain);if(!domainRows.length)continue;
  const first=domainRows[0].row;
  const level1=node('details','', 'search-level');level1.open=true;level1.append(node('summary',`L1 · ${first.L1_Title_ko} · ${domainRows.length}개 후보`));root.append(level1);
  for(const l2 of new Set(domainRows.map(x=>x.row.L2_ID))){
   const l2Rows=domainRows.filter(x=>x.row.L2_ID===l2),level2=node('details','', 'search-level');level2.open=true;level2.append(node('summary',`L2 · ${l2Rows[0].row.L2_Title_ko}`));level1.append(level2);
   for(const l3 of new Set(l2Rows.map(x=>x.row.L3_ID))){
    const l3Rows=l2Rows.filter(x=>x.row.L3_ID===l3),r=l3Rows[0].row;
    const level3=node('details','', 'search-level search-category');level3.open=true;level3.append(node('summary',`L3 · ${r.L3_Title_ko} · ${l3Rows.length}개 후보`));
    level3.append(node('p',r.L3_Description_ko,'search-definition'));level3.append(link(r.L3_ID,'L3 원문 정의 보기'));level2.append(level3);
    for(const candidate of l3Rows){
     const row=candidate.row,card=node('article','', 'search-candidate');
     card.append(node('h4',`L4 · ${row.L4_Title_ko}`),node('p',row.L4_Title_en,'english'),node('p',row.L4_Description_ko));
     const english=node('details');english.append(node('summary','영문 정의'),node('p',row.L4_Description_en));card.append(english);
     card.append(node('p',`일치 표현 · ${candidate.matched.join(' · ')}`,'search-match'));
     const quote=node('blockquote',candidate.snippet);quote.setAttribute('aria-label','관련 입력 문장');card.append(node('p','관련 입력 문장','label'),quote,link(row.L4_ID,row.L4_ID+' · 원문과 댓글 보기'));
     level3.append(card);
    }
   }
  }
 }
}
async function run(){
 if(reading)return;
 const text=input.value.trim();
 if(!text){status.textContent='서비스 설명이나 검토할 내용을 입력해 주세요.';input.focus();return;}
 if(text.length>MAX_TEXT_LENGTH){status.textContent='텍스트는 10만 자 이하로 나누어 입력해 주세요.';return;}
 submit.disabled=true;status.textContent='입력 내용과 리스크 정의를 대조하고 있습니다.';
 try{
  const idx=await index();
  if(input.value.trim()!==text)return;
  lastResults=searchRisks(idx,text,{limit:Number(document.querySelector('#document-limit').value),domain:document.querySelector('#document-domain').value});
  render(lastResults);status.textContent=`검색 완료 · L4 ${lastResults.length}개 후보를 계층별로 표시했습니다.`;
 }catch(e){status.textContent=e.message;output.replaceChildren();}
 finally{submit.disabled=reading;}
}
form.addEventListener('submit',e=>{e.preventDefault();run();});
form.addEventListener('reset',()=>{uploadVersion++;reading=false;submit.disabled=false;status.textContent='';output.replaceChildren();lastResults=[];});
input.addEventListener('input',()=>{if(output.childElementCount){output.replaceChildren();status.textContent='입력이 변경되었습니다. 다시 검색해 주세요.';}});
for(const id of ['#document-domain','#document-limit'])document.querySelector(id).addEventListener('change',()=>{if(output.childElementCount)run();});
upload.addEventListener('change',async()=>{
 const file=upload.files[0];if(!file)return;
 const version=++uploadVersion;input.value='';reading=true;submit.disabled=true;output.replaceChildren();status.textContent=`${file.name}에서 텍스트를 읽고 있습니다.`;
 try{
  const text=await extractFileText(file);if(version!==uploadVersion)return;
  input.value=text;status.textContent=`${file.name} · ${text.length.toLocaleString()}자 불러오기 완료. 내용을 확인한 뒤 잠재 리스크 검색을 눌러 주세요.`;
 }catch(e){if(version===uploadVersion){status.textContent=e.message;upload.value='';}}
 finally{if(version===uploadVersion){reading=false;submit.disabled=false;}}
});
document.querySelector('#document-example').addEventListener('click',()=>{
 uploadVersion++;reading=false;submit.disabled=false;upload.value='';
 input.value='배달 로봇이 보행자를 인식하지 못해 충돌할 수 있다. 원격 운영자에게 제어권을 인계하지 못하면 비상 정지가 지연될 수 있다. 주문자의 주소와 전화번호 등 개인정보가 외부에 유출될 수 있다.';
 output.replaceChildren();status.textContent='예시를 불러왔습니다. 잠재 리스크 검색을 눌러 주세요.';input.focus();
});
