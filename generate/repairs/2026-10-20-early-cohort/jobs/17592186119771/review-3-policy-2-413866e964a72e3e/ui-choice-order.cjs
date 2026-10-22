function choiceOrder(choices, seed) {
  const hash = value => { let n = 2166136261; for (const c of value) n = Math.imul(n ^ c.charCodeAt(0), 16777619); return n >>> 0; };
  return [...choices].sort((a, b) => hash(`${seed}:${a.id}`) - hash(`${seed}:${b.id}`));
}

const fs=require('fs');const records=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let output=[];
for(let i=0;i<records.length;i++){
 const f=records[i].question[':question/answer-fields'][0];
 const bank=f[':answer-field/choices'].map(a=>({id:a[':answer/id'],value:a[':answer/value']}));
 const cases=[];
 for(const id of [i+1,...Array.from({length:128},(_,k)=>100000+k)]){
  const ordered=choiceOrder(bank,`${id}:${f[':answer-field/id']}`);
  cases.push({item_id:id,ids:ordered.map(a=>a.id),labels:ordered.map(a=>a.value)});
 }
 output.push({record_index:i,cases});
}
process.stdout.write(JSON.stringify(output));
