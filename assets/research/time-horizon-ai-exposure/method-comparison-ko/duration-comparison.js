(()=>{ "use strict";
const curves={"gpt4_2023": {"h50_min": 4.0, "slope_per_doubling": 0.641}, "claude37_2025": {"h50_min": 60.4, "slope_per_doubling": 0.597}, "gpt5_2025": {"h50_min": 203.0, "slope_per_doubling": 0.576}, "opus46_2026": {"h50_min": 718.8, "slope_per_doubling": 0.412}};
const root=document.getElementById('method-duration-graph'); if(!root)return;
const select=root.querySelector('#mc-model');
const x=d=>82+Math.log(d)/Math.log(2880)*700, y=v=>310-v*230;
function update(){const c=curves[select.value];const p=d=>1/(1+Math.exp(c.slope_per_doubling*Math.log2(d/c.h50_min)));
root.querySelector('#mc-curve').setAttribute('d',Array.from({length:201},(_,i)=>{const d=Math.exp(Math.log(2880)*i/200);return `${i?'L':'M'}${x(d).toFixed(2)},${y(p(d)).toFixed(2)}`;}).join(' '));
const line=root.querySelector('#mc-horizon');line.setAttribute('x1',x(c.h50_min));line.setAttribute('x2',x(c.h50_min));
const label=root.querySelector('#mc-hlabel');label.setAttribute('x',x(c.h50_min));label.textContent=`h₅₀ = ${c.h50_min}분`;
for(const d of [30,1200]){root.querySelector(`#mc-dot-${d}`).setAttribute('cy',y(p(d)));root.querySelector(`#mc-value-${d}`).textContent=p(d).toFixed(3);}
root.querySelector('#duration-desc').textContent=`${select.options[select.selectedIndex].text}. Eloundou β 과업 점수는 1로 일정합니다. 설명용 THAIE는 30분 ${p(30).toFixed(3)}, 20시간 ${p(1200).toFixed(3)}입니다. 실제 과업 관측값이 아닙니다.`;
} select.addEventListener('change',update); update();
})();