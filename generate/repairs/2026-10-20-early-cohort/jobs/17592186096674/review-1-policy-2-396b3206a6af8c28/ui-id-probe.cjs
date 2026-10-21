const fs=require('fs');
const src=fs.readFileSync('/home/jake/Developer/Course_Academy/ui/learning.js','utf8');
eval(src.slice(src.indexOf('function choiceOrder('),src.indexOf('\nfunction fieldControl(')));
const rs=JSON.parse(fs.readFileSync('delivery-batch/accepted.json'));
const rows=rs.map((r,i)=>{
  const f=r.question[':question/answer-fields'][0];
  const cases=Array.from({length:20},(_,j)=>{
    const itemId=j+1;const choices=choiceOrder(f[':answer-field/choices'].map(c=>({id:c[':answer/id']})),`${itemId}:${f[':answer-field/id']}`);
    return {item_id:itemId,correct_position:choices.findIndex(c=>c.id===f[':answer-field/correct'][1]),ordered_choice_ids:choices.map(c=>c.id)};
  });return {record_index:i,question_id:r.question[':question/id'],shape:r.generation.template,cases};
});
fs.writeFileSync('ui-id-probe.json',JSON.stringify({method:'Unmodified actual UI choiceOrder; vary only task-item ID, hold normalized record fixed. IDs are fixture probes, not allocated production IDs.',records:rows},null,2));
for(const r of rows)console.log(r.record_index,r.shape,[...new Set(r.cases.map(c=>c.correct_position))]);
// Re-render a normalized vector record at fixture ID 1 instead of ID 3.
fs.writeFileSync('render-id-counterfactual.json',JSON.stringify([rs[2]],null,2));
