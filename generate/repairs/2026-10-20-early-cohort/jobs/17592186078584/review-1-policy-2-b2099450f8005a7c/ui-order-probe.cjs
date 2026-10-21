const fs=require('fs'),path=require('path'),vm=require('vm');
const root=__dirname;
const ui='/home/jake/Developer/Course_Academy/ui/learning.js';
const source=fs.readFileSync(ui,'utf8');
const exact=source.slice(source.indexOf('function choiceOrder('),source.indexOf('function fieldControl('));
const context={};vm.createContext(context);vm.runInContext(exact+'\nthis.order=choiceOrder;',context);
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const result={implementation:ui,exact_function:exact,groups:{}};
for(const [name,records] of Object.entries({fresh:read('fresh-samples.json'),batch:read('runner-batch.json'),rendered:read('render-records.json')})){
  result.groups[name]=records.map((r,i)=>{
    const f=r.question[':question/answer-fields'][0],cid=f[':answer-field/correct'][1];
    const ids=name==='rendered'?[i+1]:[1,17,17592186080001];
    return {question_id:r.question[':question/id'],template:r.generation.template,positions:ids.map(itemId=>{
      const ch=f[':answer-field/choices'].map(a=>({id:a[':answer/id'],value:a[':answer/value']}));
      const ordered=context.order(ch,`${itemId}:${f[':answer-field/id']}`);
      return {item_id:itemId,position:ordered.findIndex(a=>a.id===cid)+1,ordered_ids:ordered.map(a=>a.id)};
    })};
  });
}
fs.writeFileSync(path.join(root,'ui-order-results.json'),JSON.stringify(result,null,2));
