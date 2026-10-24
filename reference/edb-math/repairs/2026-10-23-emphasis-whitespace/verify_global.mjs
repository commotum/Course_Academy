import fs from 'node:fs';import readline from 'node:readline';import{candidates,masked,plain}from './detect.mjs';
const allowed=new Set(['question/problem','question/worked-solution','tutorial/content','multistep/context','answer/feedback','answer-field/feedback','assigned-problem/instructions','answer/value']),fields=new Map(),types=new Map();
for await(const line of readline.createInterface({input:fs.createReadStream('.local/edb/emphasis-after.jsonl')})){const r=JSON.parse(line);if(r.a==='answer/type')types.set(r.e,r.v);if(allowed.has(r.a)&&typeof r.v==='string')fields.set(r.e+':'+r.a,r);}
const unresolved=[],counts={};let retained=0;
for(const r of fields.values()){
 if(r.a==='answer/value'&&types.get(r.e)!==17592186045499)continue;counts[r.a]=(counts[r.a]||0)+1;
 const ms=candidates(r.v);retained+=ms.filter(m=>m.status!=='repair').length;
 for(const m of ms)if(m.status==='repair')unresolved.push({entity:r.e,attribute:r.a,...m});
 const s=masked(r.v),visible=plain(s);for(const m of s.matchAll(/(?<![\\*])\*\*[ \t]+\*\*(?!\*)/g))if(visible.includes(m[0]))unresolved.push({entity:r.e,attribute:r.a,text:m[0],kind:'empty-padded-emphasis'});
}
const dir=new URL('./',import.meta.url),changes=JSON.parse(fs.readFileSync(new URL('fields.json',dir)));
for(const r of changes)if(fields.get(r.entity+':'+r.attribute)?.v!==r.after)throw Error('readback mismatch '+r.entity);
const summary={basis_t:JSON.parse(fs.readFileSync('.local/edb/emphasis-after.manifest.json')).basis_t,fields_scanned:Object.values(counts).reduce((a,b)=>a+b,0),counts,confirmed_whitespace_errors_remaining:unresolved.length,retained_valid_formatting_and_placeholders:retained,all_repaired_values_verified:true,unresolved};
fs.writeFileSync(new URL('global-verification.json',dir),JSON.stringify(summary,null,2)+'\n');console.log(summary);if(unresolved.length)process.exitCode=1;
