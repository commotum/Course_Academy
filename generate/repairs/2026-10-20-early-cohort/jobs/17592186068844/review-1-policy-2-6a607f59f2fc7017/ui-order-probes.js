// Executes the actual UI choiceOrder function extracted verbatim. No UI edits.
const fs=require('fs');
const source=fs.readFileSync('/home/jake/Developer/Course_Academy/ui/learning.js','utf8');
const body=source.slice(source.indexOf('function choiceOrder('),source.indexOf('function fieldControl('));
const order=new Function(body+'; return choiceOrder;')();
const input=JSON.parse(fs.readFileSync('delivery-independent/accepted.json','utf8'));
const batch=JSON.parse(fs.readFileSync('delivery-batch/accepted.json','utf8'));
function row(r,itemId){const f=r.question[':question/answer-fields'][0];const choices=f[':answer-field/choices'].map(a=>({id:a[':answer/id'],value:a[':answer/value']}));const key=f[':answer-field/correct'][1];const ordered=order(choices,`${itemId}:${f[':answer-field/id']}`);return {question_id:r.question[':question/id'],template:r.generation.template,parameters:r.generation.parameters,itemId,ordered,correct_position:ordered.findIndex(a=>a.id===key)+1};}
const tests=[];
for(const r of input) for(const itemId of [1,17,17592186600123]) tests.push(row(r,itemId));
const rendered=[];
for(const [dir,path] of [['render','render-records.json'],['render-rest','render-rest-records.json']]){const records=JSON.parse(fs.readFileSync(path,'utf8'));const report=JSON.parse(fs.readFileSync(`${dir}/rendering.json`,'utf8'));for(const c of report.cases){const r=records[c.index];const html=fs.readFileSync(`${dir}/question-${String(c.index+1).padStart(3,'0')}.html`,'utf8');const ids=[...html.matchAll(/<input(?=[^>]*type="radio")(?=[^>]*value="([^"]+)")[^>]*>/g)].map(m=>m[1]);const rr=row(r,c.index+1);if(JSON.stringify(ids)!==JSON.stringify(rr.ordered.map(z=>z.id)))throw Error('Actual DOM mismatch '+dir+' '+c.index);rendered.push({report:dir+'/rendering.json',index:c.index,...rr,dom_matches:true});}}
const grouped=[];
for(const t of [...new Set(input.map(r=>r.generation.template))])for(const itemId of [1,17,17592186600123]){const matched=tests.filter(z=>z.template===t && z.itemId===itemId && z.parameters.k===3 && z.parameters.h===(t.includes('autonomous')?0:-2));if(matched.length!==5)throw Error('matched quintuple missing');const counts={};for(const z of matched)counts[z.correct_position]=(counts[z.correct_position]||0)+1;grouped.push({template:t,itemId,total:5,position_correct_counts:counts});}
const batchRows=rendered.filter(z=>z.report==='render-rest/rendering.json'&&z.index>=8);
const counts={};for(const z of batchRows)counts[z.correct_position]=(counts[z.correct_position]||0)+1;
fs.writeFileSync('ui-order-results.json',JSON.stringify({actual_ui_function:body,rendered_dom_checks:rendered,controlled_position_probes:grouped,post_delivery_probes:tests,exact_batch_rendered_positions:counts,exact_batch_records:batchRows,limitations:['Actual production task-item IDs are unknown; configured item IDs are controlled probes.','Semantic answer-bank policies are invariant to this additional shuffle; position results are reported separately.']},null,2)+'\n');
console.log(JSON.stringify({dom_checks:rendered.length,controlled_groups:grouped.length,batch_positions:counts,max_conditional_position_hits:Math.max(...grouped.flatMap(z=>Object.values(z.position_correct_counts)))}));
