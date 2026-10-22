// Execute the application's actual choiceOrder function, without a browser stack.
const fs=require('fs'),vm=require('vm'),path=require('path');
const here=__dirname;
const src=fs.readFileSync('/home/jake/Developer/Course_Academy/ui/learning.js','utf8');
const start=src.indexOf('function choiceOrder('),end=src.indexOf('function fieldControl(',start);
if(start<0||end<0)throw Error('UI choice-order interface changed');
const order=vm.runInNewContext(src.slice(start,end)+';choiceOrder');
const records=JSON.parse(fs.readFileSync(path.join(here,'delivery/accepted.json')));
const fixtures=[];
for(const [dataset,records] of [['sample',JSON.parse(fs.readFileSync(path.join(here,'delivery/accepted.json')))],['controlled',JSON.parse(fs.readFileSync(path.join(here,'delivery-counterfactual/accepted.json')))]]){
for(const base of [1,17592187000000]){
 const positions=[0,0,0,0,0],groups={};
 for(let i=0;i<records.length;i++){
  const rec=records[i],field=rec.question[':question/answer-fields'][0],correct=field[':answer-field/correct'][1];
  const choices=field[':answer-field/choices'].map(a=>({id:a[':answer/id'],value:a[':answer/value']}));
  const idx=order(choices,`${base+i}:${field[':answer-field/id']}`).findIndex(a=>a.id===correct);
  if(idx<0)throw Error('lost key');positions[idx]++;
  const c=rec.generation.parameters.context;(groups[c]??=[0,0,0,0,0])[idx]++;
 }
 if(positions.some(n=>n===0))throw Error('uncovered UI key position');
 if(dataset==='controlled'&&Object.values(groups).some(ns=>Math.max(...ns)===5))throw Error('fixed UI position in controlled context');
 fixtures.push({dataset,content_id_base:base,positions,contexts:groups});
}
}
const report={passed:true,implementation:'unmodified ui/learning.js::choiceOrder',fixtures,limitation:'Content IDs are local fixtures. Publication-assigned database IDs and future learner histories are unavailable.'};
fs.writeFileSync(path.join(here,'ui-order.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
