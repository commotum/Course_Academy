const fs=require('fs');
function choiceOrder(choices, seed) {
  const hash = value => { let n = 2166136261; for (const c of value) n = Math.imul(n ^ c.charCodeAt(0), 16777619); return n >>> 0; };
  return [...choices].sort((a, b) => hash(`${seed}:${a.id}`) - hash(`${seed}:${b.id}`));
}

const records=JSON.parse(fs.readFileSync(process.argv[2]||'delivery-batch/accepted.json','utf8'));
const results=records.flatMap((r,i)=>{
 const f=r.question[':question/answer-fields'][0];
 if(!f[':answer-field/type'].endsWith('/radio'))return [];
 const choices=f[':answer-field/choices'].map(a=>({id:a[':answer/id']}));
 const key=f[':answer-field/correct'][1];
 const position=id=>choiceOrder(choices,`${id}:${f[':answer-field/id']}`).findIndex(a=>a.id===key);
 const draws=Array.from({length:32},(_,j)=>({runtime_content_or_item_id:j+1,position:position(j+1)}));
 return [{record:r,preview_position:position(i+1),draws}];
});
fs.writeFileSync('ui-order-probe.json',JSON.stringify({command:process.argv,implementation:'Exact choiceOrder function extracted from ui/learning.js; fieldControl uses itemId:field.id; lesson preview uses synthetic contentId=index+1. Actual task/field IDs are not captured.',results},null,2));
console.log(JSON.stringify(results.map(r=>({profile:r.record.generation.bank_profile,preview:r.preview_position,third:r.draws.filter(v=>v.position===2).length,total:r.draws.length,positions:[...new Set(r.draws.map(v=>v.position))]}))));
