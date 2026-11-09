const STOP = new Set('the a an and or of to in for with that this is are be by on as from at it its can may not ai risk risks system systems model models agent agents 인공지능 시스템 리스크 위험 대한 통해 위한 경우 있는 없는 이를 또는 및 등이 등의 한다 하는 하여 되어 대한 관련 발생 가능 대한 사용 결과 서비스'.split(/\s+/));
const CONCEPTS = [
 ['개인정보','개인 정보','사생활','privacy','personal data','personal information'],
 ['유출','노출','누출','leak','disclosure','exposure'],
 ['충돌','collision','crash'],['보행자','pedestrian'],['로봇','robot'],
 ['인식','인지','recognition','perception','detect'],['센서','sensor'],
 ['권한','승인','authorization','permission','approval'],['도구','tool'],
 ['메모리','기억','memory'],['감독','oversight','supervision'],
 ['편향','차별','bias','discrimination'],['환각','허위','hallucination','misinformation'],
 ['프롬프트 인젝션','prompt injection'],['공격','attack','adversarial'],
 ['기밀','confidential','secret'],['저작권','copyright'],['제어권','인계','handover','transfer control'],
 ['안전 정지','비상 정지','emergency stop','safe state'],['자원','resource'],
];
export function normalize(text) { return String(text).normalize('NFKC').toLowerCase().replace(/[_/·–—-]+/g,' ').replace(/\s+/g,' ').trim(); }
function words(text) { return normalize(text).match(/[\p{L}\p{N}]+/gu)?.filter(w=>w.length>1&&!STOP.has(w))||[]; }
function terms(text) {
 const out = new Set(words(text));
 for (const word of [...out]) if (/^[가-힣]+$/.test(word)) {
  const stem=word.replace(/(으로부터|에서는|에게서|으로|에서|에게|까지|부터|하는|하지|하고|하여|되어|된다|한다|된다|되는|하면|했을|했던|이다|입니다|습니다|거나|이나|처럼|보다|에는|은|는|이|가|을|를|의|에|와|과|도|로)$/,'');
  if(stem.length>=2&&!STOP.has(stem))out.add(stem);
 }
 for(const group of CONCEPTS) if(group.some(t=>normalize(text).includes(t)))for(const t of group)out.add(t);
 return out;
}
function grams(text) { const set=new Set(); for(const word of words(text)) if(/^[가-힣]+$/.test(word)&&word.length>=3)for(let i=0;i<word.length-1;i++)set.add(word.slice(i,i+2));return set; }
export function createRiskIndex(taxonomy) {
 const docs=Object.entries(taxonomy.domains).flatMap(([domain,rows])=>rows.map(row=>{
  const title=[row.L4_Title_ko,row.L4_Title_en].join(' ');
  const definition=[row.L4_Description_ko,row.L4_Description_en].join(' ');
  const text=normalize(title+' '+definition);
  return {row,domain,text,title:normalize(title),terms:terms(title+' '+definition),grams:grams(title+' '+definition)};
 }));
 const freq=new Map();for(const doc of docs)for(const term of doc.terms)freq.set(term,(freq.get(term)||0)+1);
 return {docs,freq};
}
export function searchRisks(index,input,{limit=30,domain='all'}={}) {
 const normalized=normalize(input), query=terms(input), queryGrams=grams(input);
 if(!normalized||!query.size)return [];
 const sentences=String(input).split(/(?<=[.!?。！？])\s+|\n+/).map(s=>s.trim()).filter(Boolean);
 const queryTerms=[...query].filter(term=>{
  if(!/^[가-힣]+$/.test(term))return true;
  for(let i=2;i<term.length;i++)if(query.has(term.slice(0,i)))return false;
  return true;
 });
 const scores=[];
 for(const doc of index.docs){
  if(domain!=='all'&&doc.domain!==domain)continue;
  let score=0;const matched=[];
  for(const term of queryTerms){
   const exact=doc.terms.has(term);
   // A Korean stem can match an inflected word; avoid short English substring matches.
   const present=exact||(/^[가-힣]{2,}$/.test(term)&&doc.text.includes(term));
   if(!present)continue;
   const df=index.freq.get(term)||Math.ceil(index.docs.length/8);
   const idf=Math.log(1+(index.docs.length-df+.5)/(df+.5));
   score+=idf*(doc.title.includes(term)?2.4:1);
   if(normalized.includes(term))matched.push({term,weight:idf*(doc.title.includes(term)?2:1)});
  }
  // Character overlap helps Korean morphology only after at least one substantive term matches.
  if(matched.length)for(const gram of queryGrams)if(doc.grams.has(gram))score+=.12;
  const distinct=matched.filter(({term})=>!matched.some(other=>other.term!==term&&term.startsWith(other.term)));
  if(!matched.length||score<2||(distinct.length<2&&words(input).length>2))continue;
  matched.sort((a,b)=>b.weight-a.weight);
  const visibleTerms=matched.slice(0,6).map(x=>x.term);
  const snippet=sentences.map(s=>({s,n:matched.slice(0,6).reduce((n,x)=>n+(normalize(s).includes(x.term)?x.weight:0),0)})).sort((a,b)=>b.n-a.n)[0]?.s||'';
  scores.push({...doc,score,matched:visibleTerms,snippet:snippet.length>260?snippet.slice(0,260)+'…':snippet});
 }
 scores.sort((a,b)=>b.score-a.score||a.row.L4_ID.localeCompare(b.row.L4_ID));
 return scores.slice(0,Math.max(1,Math.min(60,limit)));
}
