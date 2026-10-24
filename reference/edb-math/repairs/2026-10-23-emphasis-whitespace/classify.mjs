import fs from 'node:fs';
import {marked} from '../../../../ui/vendor/marked/marked.esm.js';
import {protectMath} from '../../../../ui/math-protection.js';
const dir=new URL('./',import.meta.url), rows=JSON.parse(fs.readFileSync(new URL('inventory.json',dir)));
function plain(s){return marked.parse(s).replace(/<[^>]*>/g,'').replaceAll('&amp;','&').replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&#39;',"'").replaceAll('&quot;','"');}
for(const r of rows){
 const masked=protectMath(r.v,m=>'M'.repeat(m.length));
 const visible=plain(masked);
 for(const m of r.found){
  const text=masked.slice(m.start,m.end),marker=text.match(/^[*_]+/)[0];
  m.marker=marker;
  m.literal=visible.includes(text)||visible.includes(marker+plain(text.slice(marker.length,-marker.length)).replace(/\n$/, '')+marker);
  m.status=marker.includes('_')?'retain-answer-placeholder':m.literal?'repair':'review-nested-or-already-rendered';
 }
}
fs.writeFileSync(new URL('classified.json',dir),JSON.stringify(rows,null,2)+'\n');
const c={};for(const r of rows)for(const m of r.found)c[m.status]=(c[m.status]||0)+1;console.log(c);
console.log(rows.flatMap(r=>r.found.filter(m=>m.status==='review-nested-or-already-rendered').map(m=>[r.e,m.text])).slice(0,45));
