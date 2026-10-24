import fs from 'node:fs';import readline from 'node:readline';import{marked}from '../../../../ui/vendor/marked/marked.esm.js';import{protectMath}from '../../../../ui/math-protection.js';
const allowed=new Set(['question/problem','question/worked-solution','tutorial/content','multistep/context','answer/feedback','answer-field/feedback','assigned-problem/instructions','answer/value']);
const types=new Map(),fields=new Map();for await(const l of readline.createInterface({input:fs.createReadStream('.local/edb/emphasis-current.jsonl')})){const r=JSON.parse(l);if(r.a==='answer/type')types.set(r.e,r.v);if(allowed.has(r.a)&&typeof r.v==='string'&&r.v.includes('*'))fields.set(r.e+':'+r.a,r);}
const all=[];for(const r of fields.values()){
 if(r.a==='answer/value'&&types.get(r.e)!==17592186045499)continue;
 let text=protectMath(r.v,()=> 'CAMATHPLACEHOLDER').replace(/```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]+`/g,'CODEPLACEHOLDER');
 const html=marked.parse(text),visible=html.replace(/<code\b[^>]*>[\s\S]*?<\/code>/g,'CODE').replace(/<[^>]*>/g,'');
 if(visible.includes('*'))all.push({...r,masked:text,html,stars:visible.split('\n').filter(l=>l.includes('*'))});
}
fs.writeFileSync(new URL('residual.json',import.meta.url),JSON.stringify(all,null,2)+'\n');
console.log('fields with visible stars',all.length);const groups=new Map();for(const r of all)for(const s of r.stars){if(!groups.has(s))groups.set(s,[]);groups.get(s).push(r.e+':'+r.a);}
fs.writeFileSync(new URL('residual-groups.json',import.meta.url),JSON.stringify([...groups].map(([s,fields],i)=>({i,s,fields})),null,2)+'\n');
console.log('groups',groups.size);for(const [s,ids]of groups)console.log(ids.length,ids[0],s.slice(0,700));
