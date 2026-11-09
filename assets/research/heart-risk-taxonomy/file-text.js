export const MAX_FILE_SIZE=10*1024*1024;
export const MAX_TEXT_LENGTH=100000;
export async function extractFileText(file){
 if(file.size>MAX_FILE_SIZE)throw Error('파일은 10MB 이하로 업로드해 주세요.');
 const ext=file.name.split('.').pop().toLowerCase();
 let text='';
 if(['txt','text','md','markdown','csv','json'].includes(ext)){
  const buffer=await file.arrayBuffer();
  try{text=new TextDecoder('utf-8',{fatal:true}).decode(buffer);}catch{text=new TextDecoder('euc-kr').decode(buffer);}
 }else if(ext==='pdf'){
  const pdfjs=await import('./vendor/pdfjs/pdf.mjs');
  pdfjs.GlobalWorkerOptions.workerSrc=new URL('./vendor/pdfjs/pdf.worker.mjs',import.meta.url).href;
  const task=pdfjs.getDocument({data:await file.arrayBuffer(),isEvalSupported:false,useSystemFonts:true,cMapUrl:new URL('./vendor/pdfjs/cmaps/',import.meta.url).href,cMapPacked:true});
  let doc;
  try{
   doc=await task.promise;
   if(doc.numPages>100)throw Error('PDF는 100페이지 이하로 나누어 업로드해 주세요.');
   const parts=[];let length=0;
   for(let i=1;i<=doc.numPages;i++){
    const page=await doc.getPage(i),content=await page.getTextContent();
    const part=content.items.map(item=>item.str+(item.hasEOL?'\n':' ')).join('');
    parts.push(part);length+=part.length;
    if(length>MAX_TEXT_LENGTH)throw Error('추출한 텍스트가 10만 자를 넘습니다. 필요한 부분만 나누어 입력해 주세요.');
   }
   text=parts.join('\n\n');
  }finally{await task.destroy();}
 }else if(['xlsx','xls','xlsm','xlsb'].includes(ext)){
  if(!globalThis.XLSX)await new Promise((resolve,reject)=>{
   const script=document.createElement('script');script.src=new URL('./vendor/sheetjs/xlsx.full.min.js',import.meta.url).href;script.onload=resolve;script.onerror=()=>reject(Error('엑셀 읽기 도구를 불러오지 못했습니다.'));document.head.append(script);
  });
  const book=globalThis.XLSX.read(await file.arrayBuffer(),{type:'array',cellHTML:false,cellFormula:false,cellStyles:false});
  const parts=[];
  for(const name of book.SheetNames){
   const sheet=book.Sheets[name];
   if(sheet['!ref']){const range=globalThis.XLSX.utils.decode_range(sheet['!ref']);if((range.e.r+1)*(range.e.c+1)>1000000)throw Error('시트가 너무 큽니다. 필요한 행과 열만 나누어 업로드해 주세요.');}
   const csv=globalThis.XLSX.utils.sheet_to_csv(sheet,{blankrows:false});
   if(csv.trim())parts.push('[시트 '+name+']\n'+csv);
   if(parts.join('\n').length>MAX_TEXT_LENGTH)throw Error('텍스트는 10만 자 이하로 나누어 입력해 주세요.');
  }
  text=parts.join('\n\n');
 }else if(ext==='docx'){
  if(!globalThis.mammoth)await new Promise((resolve,reject)=>{
   const script=document.createElement('script');script.src=new URL('./vendor/mammoth.browser.min.js',import.meta.url).href;script.onload=resolve;script.onerror=()=>reject(Error('문서 읽기 도구를 불러오지 못했습니다. 다시 시도해 주세요.'));document.head.append(script);
  });
  text=(await globalThis.mammoth.extractRawText({arrayBuffer:await file.arrayBuffer()})).value;
 }else throw Error('Markdown, PDF, DOCX, 텍스트, CSV, 엑셀 파일을 사용해 주세요.');
 if(!text.trim())throw Error('읽을 수 있는 텍스트가 없습니다. 스캔 PDF나 이미지라면 텍스트를 추출해 붙여 넣어 주세요.');
 if(text.length>MAX_TEXT_LENGTH)throw Error('텍스트는 10만 자 이하로 나누어 입력해 주세요.');
 return text.trim();
}
