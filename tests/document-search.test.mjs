import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs/promises';
import {createRiskIndex,searchRisks} from '../assets/research/heart-risk-taxonomy/risk-search-engine.js';
import {extractFileText} from '../assets/research/heart-risk-taxonomy/file-text.js';
const taxonomy=JSON.parse(await fs.readFile(new URL('../assets/research/heart-risk-taxonomy/taxonomy.json',import.meta.url)));
const idx=createRiskIndex(taxonomy);
test('uses all 592 unchanged active cards and finds bilingual risk mechanisms',()=>{
 assert.equal(idx.docs.length,592);assert.equal(searchRisks(idx,'사람 미인식에 따른 위험 감지 예측 실패')[0].row.L4_ID,'P_SYS_PERCEPTION_007');
 assert.ok(searchRisks(idx,'개인정보 유출').slice(0,5).every(x=>x.row.L3_ID==='G_INT_PRIV'));
 assert.equal(searchRisks(idx,'prompt injection')[0].row.L4_ID,'G_SYS_SECADV_044');
 assert.equal(searchRisks(idx,'zxqvbrskth').length,0);assert.equal(searchRisks(idx,'오늘 날씨가 맑다').length,0);assert.equal(searchRisks(idx,'').length,0);
 const rows=searchRisks(idx,'로봇이 사람을 인식하지 못해 충돌한다',{domain:'Physical',limit:10});assert.ok(rows.length);assert.ok(rows.every(r=>r.domain==='Physical'));assert.ok(rows.length<=10);
 for(const r of rows)for(const key of ['L0_ID','L1_ID','L2_ID','L3_ID','L4_ID'])assert.ok(r.row[key]);
});
test('file import supports Unicode plain text and rejects invalid or large inputs',async()=>{
 const f=new File(['개인정보 유출\n로봇 충돌'],'설계.txt');assert.equal(await extractFileText(f),'개인정보 유출\n로봇 충돌');
 await assert.rejects(()=>extractFileText(new File([''],'empty.txt')),/텍스트가 없습니다/);
 await assert.rejects(()=>extractFileText(new File(['x'],'image.png')),/파일을 사용/);
 await assert.rejects(()=>extractFileText({name:'big.txt',size:11*1024*1024}),/10MB/);
 await assert.rejects(()=>extractFileText(new File(['a'.repeat(100001)],'long.txt')),/10만 자/);
});
