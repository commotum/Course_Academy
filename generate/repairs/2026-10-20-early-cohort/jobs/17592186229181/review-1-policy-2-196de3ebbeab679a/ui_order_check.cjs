const fs=require('fs'),vm=require('vm'),path=require('path');
const src=fs.readFileSync('/home/jake/Developer/Course_Academy/ui/learning.js','utf8');
const start=src.indexOf('function choiceOrder('),end=src.indexOf('function fieldControl(',start);
if(start<0||end<0)throw Error('UI choice-order interface changed');
const order=vm.runInNewContext(src.slice(start,end)+';choiceOrder');
const fixtures=[];
for(const [dataset,file] of [['sample','delivery-sample/accepted.json'],['batch','delivery-batch/accepted.json'],['controlled','delivery-counterfactual/accepted.json']]){
 const records=JSON.parse(fs.readFileSync(file));
 for(const base of [1,17592187000000]){
  const positions=[0,0,0,0,0],contexts={},rows=[];
  for(let i=0;i<records.length;i++){
   const rec=records[i],field=rec.question[':question/answer-fields'][0],correct=field[':answer-field/correct'][1];
   const choices=order(field[':answer-field/choices'].map(a=>({id:a[':answer/id'],value:a[':answer/value']})),`${base+i}:${field[':answer-field/id']}`);
   const idx=choices.findIndex(a=>a.id===correct);if(idx<0)throw Error('key missing'); positions[idx]++;
   const context=rec.generation.parameters.context;(contexts[context]??=[0,0,0,0,0])[idx]++;
   rows.push({question_id:rec.question[':question/id'],fixture_content_id:base+i,displayed_choices:choices,correct_index:idx});
  }
  fixtures.push({dataset,input_file:file,content_id_base:base,positions,contexts,rows});
 }
}
fs.writeFileSync('ui-order.json',JSON.stringify({passed:true,implementation:'unmodified ui/learning.js::choiceOrder',fixtures,limitation:'Local content IDs are explicit fixtures; publication entity IDs do not yet exist. UI permutation depends on content and field IDs, never the key. No future exact position is asserted.'},null,2));
console.log(JSON.stringify(fixtures.map(({dataset,content_id_base,positions})=>({dataset,content_id_base,positions}))));
