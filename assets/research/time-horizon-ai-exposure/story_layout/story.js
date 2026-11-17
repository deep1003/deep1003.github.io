'use strict';
(() => {
  // Existing deep links remain usable after moving the data browser into disclosures.
  function revealHash() {
    const id=decodeURIComponent(location.hash.slice(1));
    if(!id)return;
    const target=document.getElementById(id);
    if(!target)return;
    let ancestor=target.parentElement;
    while(ancestor){if(ancestor.tagName==='DETAILS')ancestor.open=true;ancestor=ancestor.parentElement;}
    requestAnimationFrame(()=>{target.scrollIntoView({block:'start'});window.dispatchEvent(new Event('resize'));});
  }
  document.querySelectorAll('details').forEach(detail=>{
    detail.addEventListener('toggle',()=>{if(detail.open&&detail.querySelector('#occupation-map'))window.dispatchEvent(new Event('resize'));});
  });
  window.addEventListener('hashchange',revealHash);
  revealHash();
})();
