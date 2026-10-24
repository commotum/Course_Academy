import fs from 'node:fs';
import readline from 'node:readline';
import {protectMath} from '../../../../ui/math-protection.js';
const dir=new URL('./',import.meta.url);
const allowed=new Set(['question/problem','question/worked-solution','tutorial/content','multistep/context','answer/feedback','answer-field/feedback','assigned-problem/instructions','answer/value']);
const fields=new Map(), counts={},types=new Map();
for await(const line of readline.createInterface({input:fs.createReadStream('.local/edb/emphasis-current.jsonl')})){
 const r=JSON.parse(line);
 if(r.a==='answer/type')types.set(r.e,r.v);
 if(allowed.has(r.a)&&typeof r.v==='string')fields.set(r.e+':'+r.a,r);
}
const out=[];
for(const r of fields.values()){
 if(r.a==='answer/value'&&types.get(r.e)!==17592186045499)continue;
 counts[r.a]=(counts[r.a]||0)+1;
 const mask=x=>'M'.repeat(x.length);
 let s=protectMath(r.v,mask).replace(/```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]+`/g,mask);
 const found=[];
 // Pair complete runs in order; retain correctly authored pairs in this pass
 // so their closing delimiters are never treated as opening delimiters.
 for(const re of [/(?<![\\*])\*\*(?!\*)((?:(?!\*\*)[\s\S])*?)\*\*(?!\*)/g,/(?<![\\_])__(?!_)([^_]*?)__(?!_)/g,/(?<![\\*])\*(?!\*)((?:\*\*(?!\*)[\s\S]*?\*\*(?!\*)|[^*])*?)\*(?!\*)/g,/(?<![\\_])_(?!_)([^_]*?)_(?!_)/g]){
  for(const m of s.matchAll(re)){
   if(!m[1].trim()||/\n\s*\n/.test(m[1])||!/^\s|\s$/.test(m[1]))continue;
   found.push({start:m.index,end:m.index+m[0].length,text:r.v.slice(m.index,m.index+m[0].length),context:r.v.slice(Math.max(0,m.index-70),m.index+m[0].length+70)});
  }
 }
 if(found.length)out.push({...r,found});
}
fs.writeFileSync(new URL('inventory.json',dir),JSON.stringify(out,null,2)+'\n');
fs.writeFileSync(new URL('inventory-summary.json',dir),JSON.stringify({counts,fields:fields.size,candidate_fields:out.length,candidates:out.reduce((n,r)=>n+r.found.length,0)},null,2)+'\n');
console.log(JSON.stringify({counts,candidate_fields:out.length,candidates:out.reduce((n,r)=>n+r.found.length,0)}));
console.log(out.slice(0,25).map(r=>[r.e,r.a,r.found.map(x=>x.context)]));
