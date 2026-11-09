import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { JSDOM } from 'jsdom';
import { mountComments } from '../assets/research/heart-risk-taxonomy/comments-ui.js';
test('all 647 widgets mount and save/edit safely with failed draft retained',async()=>{
 const dom=new JSDOM(await fs.readFile(new URL('../assets/research/heart-risk-taxonomy/index.html',import.meta.url),'utf8'));
 globalThis.document=dom.window.document;globalThis.innerHeight=1000;
 let rows=[],fail=false;
 const api={authorId:async()=>'mine',list:async()=>rows,watch:()=>()=>{},save:async(r,body,id)=>{if(fail)throw Error('offline');const row={id:id||'one',body,author_id:'mine',created_at:'2026-11-09T00:00:00Z',updated_at:id?'2026-11-09T00:00:01Z':'2026-11-09T00:00:00Z'};rows=[row];return row;}};
 const sections=mountComments(api);assert.equal(sections.length,647);assert.equal(new Set(sections.map(s=>s.getAttribute('aria-label'))).size,647);
 const section=sections[0];section.querySelector('button').click();await new Promise(setImmediate);
 const input=section.querySelector('textarea'),form=section.querySelector('form');
 input.value='<img src=x onerror=alert(1)>내용';form.dispatchEvent(new dom.window.Event('submit',{cancelable:true}));await new Promise(setImmediate);
 assert.equal(section.querySelector('.comment-body').textContent,input.value||rows[0].body);assert.equal(section.querySelector('.comments-list img'),null);assert.match(section.textContent,/저장되었습니다/);
 section.querySelector('.comment-item button').click();assert.equal(input.value,rows[0].body);
 input.value='수정한 댓글';fail=true;form.dispatchEvent(new dom.window.Event('submit',{cancelable:true}));await new Promise(setImmediate);assert.equal(input.value,'수정한 댓글');assert.match(section.textContent,/저장하지 못했습니다/);
 fail=false;form.dispatchEvent(new dom.window.Event('submit',{cancelable:true}));await new Promise(setImmediate);assert.equal(section.querySelector('.comment-body').textContent,'수정한 댓글');assert.match(section.textContent,/수정됨/);dom.window.close();
});
