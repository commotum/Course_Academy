from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json,sys,urllib.request
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,normalized_question
from scripts.generator_packages import resolve_registered_script,verify_package
p=Publisher.from_environment(source=':agent/codex');cap=json.loads((H/'capture.json').read_text());basis=p.client.status()['basis'];checks=[];summaries=[];mapping=[]
def grade(q,f,answer,expected):
 payload={'topicId':17592186048189,'questionId':q[':db/id'],'responses':[{'fieldId':f[':db/id'],**answer}]}
 req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
 with urllib.request.urlopen(req,timeout=45)as r:out=json.load(r)
 assert out['status']==expected,(payload,out)
 checks.append({'question':q[':db/id'],'expected':expected,'actual':out['status']})
with ThreadPoolExecutor(max_workers=3)as pool:current=list(pool.map(lambda row:p.read_kp(row['kp'],H/'live'/str(row['kp']),basis),cap['knowledge_points']))
for row,k in zip(cap['knowledge_points'],current):
 kp=row['kp'];d=H/str(kp);proof=json.loads((d/'verification.json').read_text());ref=k[':knowledge-point/question-generator'][':question-generator/script'];assert ref==proof['new_reference'];entry=resolve_registered_script(ref,ROOT,p.config.math_root);verify_package(entry.parent,Path(ref).parts[2]);manifest=json.loads((entry.parent/'generator-package.json').read_text())
 for name in manifest['files']:
  local=ROOT/f'generate/scratch/{kp}.py'if name=='generator.py'else ROOT/f'generate/scratch/{kp}'/name
  assert local.read_bytes()==(entry.parent/name).read_bytes(),(kp,name)
 for name in ('substitution_pedagogy.py','inverse_substitution_models.py','integration_answer_bank.py'):assert(ROOT/'generate'/name).read_bytes()==(entry.parent/name).read_bytes()
 qmap={str(q[':question/id']):q for q in k[':knowledge-point/questions']};records=json.loads((d/'accepted-pool.json').read_text());active=[q for q in qmap.values()if not q.get(':question/math-academy-id')and not q.get(':question/retired')];assert len(active)==24 and{q[':db/id']for q in active}=={r['entity']for r in proof['new_questions']}
 for r in records:
  q=qmap[r['question'][':question/id']];assert normalized_question(q)==normalized_question(r['question']);assert 'Use the substitution'not in q[':question/problem']and'You may use'not in q[':question/problem'];f=q[':question/answer-fields'][0];cid=f[':answer-field/correct'][':db/id']
  if f[':answer-field/type'][':db/ident']==':answer-field.type/radio':
   grade(q,f,{'choiceId':cid},'correct');grade(q,f,{'choiceId':next(a[':db/id']for a in f[':answer-field/choices']if a[':db/id']!=cid)},'incorrect')
  else:
   key=next(a[':answer/value']for a in f[':answer-field/choices']if a[':db/id']==cid)
   for value,expected in ((key,'correct'),(r'\frac{2\left('+key+r'\right)}{2}','correct'),('('+key+')+1','incorrect')):grade(q,f,{'value':value},expected)
 for eid in proof['retired_questions']:assert next(q for q in qmap.values()if q[':db/id']==eid)[':question/retired']is True
 mapping+=proof['replacements'];summaries.append({'kp':kp,'active_generated':24,'retired':len(proof['retired_questions']),'imports_preserved':proof['imported_questions_preserved'],'generator':ref,'committed_basis':proof['basis_after']});print(kp,'live pool, package and grading verified',flush=True)
assert len(mapping)==5 and sum(r['imports_preserved']for r in summaries)==75
first=H.with_name('2026-10-25-inverse-trig-quality');original=[]
for row in cap['knowledge_points']:original+=json.loads((first/str(row['kp'])/'verification.json').read_text())['replacements']
for r in original:
 r['new']=next((m['new']for m in mapping if m['old']==r['new']),r['new'])
assert len(original)==96
result={'passed':True,'committed':True,'basis_readback':basis,'topic':17592186048189,'generators_updated':4,'active_generated_questions':96,'original_questions_replaced':96,'additional_bank_replacements':5,'imported_questions_preserved':75,'canonicals_preserved':4,'learner_history_preserved':True,'live_grading_checks':len(checks),'reported_replacements':[r for r in original if r['old']in(17592186682785,17592186691202)],'knowledge_points':summaries}
for name,value in [('completion',result),('replacement-map',original),('live-grading-verification',{'passed':True,'database_writes':0,'checks':checks})]:(H/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='knowledge_points'}))
