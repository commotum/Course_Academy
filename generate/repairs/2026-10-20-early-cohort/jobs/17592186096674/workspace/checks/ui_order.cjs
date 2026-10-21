// Probe exact application choice ordering and match actual rendered DOM orders.
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),ev=path.join(root,'evidence');
const ui='/home/jake/Developer/Course_Academy/ui/learning.js';
const source=fs.readFileSync(ui,'utf8');
const code=source.slice(source.indexOf('function choiceOrder('),source.indexOf('\nfunction fieldControl('));eval(code);
function measure(records){return records.filter(r=>r.question[':question/answer-fields'].length).map((r,i)=>{const f=r.question[':question/answer-fields'][0];const ordered=choiceOrder(f[':answer-field/choices'].map(c=>({id:c[':answer/id'],value:c[':answer/value']})),`${i+1}:${f[':answer-field/id']}`);return {question_id:r.question[':question/id'],profile:r.generation.source_profile,fixture_content_id:i+1,ordered_choice_ids:ordered.map(c=>c.id),correct_position:ordered.findIndex(c=>c.id===f[':answer-field/correct'][1])};});}
let reports={};for(const [stage,file] of Object.entries({before:'controlled-records.json',after:'delivery/accepted.json'}))reports[stage]=measure(JSON.parse(fs.readFileSync(path.join(ev,file))));
// Keep canonical's empty field in the original index sequence when checking DOM fixtures.
const rendered=JSON.parse(fs.readFileSync(path.join(ev,'render-records.json')));let domMatches=0;
for(let i=0;i<6;i++){
 const r=rendered[i];if(!r.question[':question/answer-fields'].length)continue;
 const f=r.question[':question/answer-fields'][0],ordered=choiceOrder(f[':answer-field/choices'].map(c=>({id:c[':answer/id'],value:c[':answer/value']})),`${i+1}:${f[':answer-field/id']}`).map(c=>c.id);
 const html=fs.readFileSync(path.join(ev,'render',`question-${String(i+1).padStart(3,'0')}.html`),'utf8');const inputs=[...html.matchAll(/<input\b[^>]*type="radio"[^>]*>/g)].map(x=>x[0]);const ids=inputs.map(s=>s.match(/value="([^"]+)"/)[1]);
 if(JSON.stringify(ordered)!==JSON.stringify(ids))throw Error(`DOM order mismatch ${i}`);domMatches++;
}
let counts={};for(const[stage,rs]of Object.entries(reports)){
 counts[stage]={};for(const r of rs){const c=counts[stage][r.profile]||={};c[r.correct_position]=(c[r.correct_position]||0)+1;}
 for(const profile of ['q-20598','q-20589'])if(Object.keys(counts[stage][profile]).length<2)throw Error(`Fixed displayed position ${stage} ${profile}`);
}
fs.writeFileSync(path.join(ev,'ui-order-results.json'),JSON.stringify({method:'Exact unmodified UI choiceOrder function; five fixtures checked against actual DOM. Fixture IDs are illustrative; production IDs not allocated.',dom_matches:domMatches,function_source:code,counts,stages:reports},null,2)+'\n');console.log(JSON.stringify({dom_matches:domMatches,restored_profile_positions:Object.fromEntries(Object.entries(counts).map(([k,v])=>[k,{'q-20598':v['q-20598'],'q-20589':v['q-20589']}]))}));
