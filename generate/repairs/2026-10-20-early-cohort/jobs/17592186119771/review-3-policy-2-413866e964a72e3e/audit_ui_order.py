import json,pathlib,re,subprocess,shutil
E=pathlib.Path(__file__).resolve().parent;js=pathlib.Path('/home/jake/Developer/Course_Academy/ui/learning.js').read_text();function=js[js.index('function choiceOrder('):js.index('function fieldControl(')]
script=function+'''
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
'''
(E/'ui-choice-order.cjs').write_text(script);cmd=[shutil.which('node'),str(E/'ui-choice-order.cjs'),str(E/'runner-batch.json')];p=subprocess.run(cmd,capture_output=True,text=True,check=True);orders=json.loads(p.stdout);rs=json.load(open(E/'runner-batch.json'));positions=json.load(open(E/'rendered-batch-positions.json'))
for o,position in zip(orders,positions):assert o['cases'][0]['ids']==position['choice_ids']
checks=[];summary=[];preview_hits=0;alternative_hits=0
for o,r in zip(orders,rs):
 q=r['question'];f=q[':question/answer-fields'][0];expected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);predictions=[]
 body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1]
 m=[[int(v.strip()) for v in row.split('&')] for row in body.split(r'\\')]
 diagonal=all(v==0 for i,row in enumerate(m) for j,v in enumerate(row) if i!=j)
 for case in o['cases']:
  pred=next(x for x in reversed(case['labels']) if x in ['Upper triangular matrix','Lower triangular matrix']) if not diagonal else 'Diagonal matrix'
  predictions.append(pred)
 preview_hits+=predictions[0]==expected
 alternative_hits+=sum(x==expected for x in predictions[1:])
 summary.append({'index':o['record_index'],'expected':expected,'preview_prediction':predictions[0],'alternative_hits':sum(x==expected for x in predictions[1:]),'alternative_total':128})
 if expected!='Diagonal matrix':
  for tag,case,pred in [('preview',o['cases'][0],predictions[0]),next(('alternative',case,pred) for case,pred in zip(o['cases'][1:],predictions[1:]) if pred!=expected)]:
   checks.append({'label':f'UI-{o["record_index"]}-{tag}','record':r,'checks':[{'submitted_answer_id':next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==pred),'expected':'accepted' if pred==expected else 'rejected','purpose':f'Later-orientation strategy at actual choiceOrder seed itemId={case["item_id"]}; compare task-order dependence'}]})
(E/'ui-order-cases.json').write_text(json.dumps({'command':cmd,'function_source':function,'orders':orders},indent=2)+'\n');(E/'ui-order-grader-input.json').write_text(json.dumps(checks,indent=2)+'\n')
(E/'ui-order-results.json').write_text(json.dumps({'preview_matches_actual_HTML':True,'preview_later_orientation':{'correct':preview_hits-1,'total':4},'strategy_with_diagonal_detection_preview':{'correct':preview_hits,'total':5},'alternative_task_ids':{'range':[100000,100127],'correct':alternative_hits,'total':640},'by_question':summary,'interpretation':'The fixed review fixture has a 4/4 later-orientation coincidence. The exact UI function depends on learner task-item ID as well as field and answer IDs, and yields both orders for each triangular question across possible task IDs. This is a preview-fixture predictor, not a demonstrated stable delivered-pool or generator predictor. Diagonal detection itself is part of the intended zero-region skill. Actual future item IDs unavailable.','native_cases':'ui-order-grader-input.json'},indent=2)+'\n');print(json.dumps({'preview_triangular':f'{preview_hits-1}/4','alternative_ids':f'{alternative_hits}/640','native_cases':len(checks)}))
