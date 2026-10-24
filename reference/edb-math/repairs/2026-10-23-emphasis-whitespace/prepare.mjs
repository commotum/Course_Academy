import fs from 'node:fs';import crypto from 'node:crypto';
import {candidates,replacement,masked,plain}from './detect.mjs';
const dir=new URL('./',import.meta.url),rows=JSON.parse(fs.readFileSync(new URL('inventory.json',dir))),changes=[],reviews=[];
const extra=JSON.parse(fs.readFileSync(new URL('residual.json',dir))).find(r=>r.e===17592186163175);rows.push(extra);
const manual=new Set([17592186128834,17592186275098]);
const hash=s=>crypto.createHash('sha256').update(s).digest('hex');
for(const r of rows){
 let after=r.v,edits=[];
 for(let round=0;round<4;round++){
  let found=candidates(after);
  if(manual.has(r.e))for(const m of found)if(m.text==='** square of the volume of water**')m.status='repair-source-reviewed-nested';
  const selected=[];for(const m of found.filter(m=>m.status.startsWith('repair')).sort((a,b)=>a.start-b.start||a.end-b.end)){if(selected.every(n=>m.start>=n.end||m.end<=n.start))selected.push(m);}
  if(!selected.length)break;
  for(const m of selected.reverse()){after=after.slice(0,m.start)+replacement(m.text,m.marker)+after.slice(m.end);edits.push({...m,round});}
 }
 if(r.e===17592186163175){const beforeEmpty=after;after=after.replace('** **',' ');if(after!==beforeEmpty)edits.push({text:'** **',replacement:' ',marker:'**',status:'repair-source-reviewed-empty-emphasis'});}
 const residual=candidates(after).filter(m=>m.status==='repair');if(residual.length)throw Error('unsettled '+r.e);
 reviews.push({entity:r.e,attribute:r.a,decisions:candidates(r.v).map(m=>({...m,status:manual.has(r.e)&&m.text==='** square of the volume of water**'?'repair-source-reviewed-nested':m.status})),remaining:candidates(after)});
 if(after===r.v)continue;
 // Relocation must preserve every non-whitespace byte, including all TeX,
 // answer markers, URLs, words and Markdown delimiters, in the same order.
 if(after.replace(/\s/g,'')!==r.v.replace(r.e===17592186163175?'** **':'ZZZUNMATCHEDZZZ',' ').replace(/\s/g,''))throw Error('nonwhitespace changed '+r.e);
 changes.push({entity:r.e,attribute:r.a,before:r.v,after,before_sha256:hash(r.v),after_sha256:hash(after),edits,old_t:r.t,old_source:r.source});
}
fs.writeFileSync(new URL('fields.json',dir),JSON.stringify(changes,null,2)+'\n');
fs.writeFileSync(new URL('individual-review.json',dir),JSON.stringify(reviews,null,2)+'\n');
console.log({fields:changes.length,entities:new Set(changes.map(r=>r.entity)).size,edits:changes.reduce((n,r)=>n+r.edits.length,0),attrs:changes.reduce((c,r)=>(c[r.attribute]=(c[r.attribute]||0)+1,c),{})});
