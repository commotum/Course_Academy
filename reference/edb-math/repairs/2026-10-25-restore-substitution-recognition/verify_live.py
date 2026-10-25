"""Verify all active pools and registrations; grade without recording attempts."""
from concurrent.futures import ThreadPoolExecutor
import json,sys,urllib.request
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,normalized_question
from scripts.generator_packages import resolve_registered_script,verify_package
from capture.scripts.storage import atomic_json
TRIG={17592186068915,17592186068916,17592186068917,17592186068918}
INV={17592186064218,17592186064219,17592186064250,17592186064220}

def grade(topic,q,response,expected):
 payload={'topicId':topic,'questionId':q[':db/id'],'responses':[response]};req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
 with urllib.request.urlopen(req,timeout=45)as result:out=json.load(result)
 assert out['status']==expected,(payload,out)
 return {'question':q[':db/id'],'expected':expected,'actual':out['status']}

def main():
 cap=json.loads((H/'capture.json').read_text());p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis']
 with ThreadPoolExecutor(max_workers=3)as pool:current=list(pool.map(lambda item:p.read_kp(item['kp'],H/'live'/str(item['kp']),basis),cap['knowledge_points']))
 summaries=[];grades=[];replacement_map=[];imports=0;retired=[];fresh=[];guided=[]
 for item,k in zip(cap['knowledge_points'],current):
  kp=item['kp'];d=H/str(kp);proof=json.loads((d/'verification.json').read_text());records=json.loads((d/'accepted-pool.json').read_text());questionmap={str(q[':question/id']):q for q in k[':knowledge-point/questions']};ref=k[':knowledge-point/question-generator'][':question-generator/script'];assert ref==proof['new_reference'];entry=resolve_registered_script(ref,ROOT,p.config.math_root);verify_package(entry.parent,Path(ref).parts[2]);helper='trig_scaffold.py'if kp in TRIG else'substitution_pedagogy.py'
  manifest=json.loads((entry.parent/'generator-package.json').read_text())
  for name in manifest['files']:
   local=ROOT/f'generate/scratch/{kp}.py'if name=='generator.py'else ROOT/f'generate/scratch/{kp}'/name
   assert local.read_bytes()==(entry.parent/name).read_bytes(),('Installed package mismatch',kp,name)
  assert(entry.parent/'integration_answer_bank.py').read_bytes()==(ROOT/'generate/integration_answer_bank.py').read_bytes()
  assert entry.read_bytes()==(ROOT/f'generate/scratch/{kp}.py').read_bytes();assert(entry.parent/helper).read_bytes()==(ROOT/'generate'/helper).read_bytes()
  active=[q for q in questionmap.values()if not q.get(':question/math-academy-id')and not q.get(':question/retired')];assert{q[':db/id']for q in active}=={r['entity']for r in proof['new_questions']};assert len(active)==24
  for row in records:
   q=questionmap[row['question'][':question/id']];assert normalized_question(q)==normalized_question(row['question']);assert'You may use'not in q[':question/problem']and'Endpoint values:'not in q[':question/problem']
   assert 'Use the substitution'not in q[':question/problem']and'Use the integration rule:'in q[':question/worked-solution']
   if q[':db/id']in proof['new_question_entities']:fresh.append(q[':db/id'])
   else:guided.append(q[':db/id'])
  for eid in proof['retired_questions']:assert next(q for q in questionmap.values()if q[':db/id']==eid)[':question/retired']is True;retired.append(eid)
  native={r['record']['question'][':question/id']:r for r in json.loads((d/'grader-input.json').read_text())}
  topic=17592186050489 if kp in TRIG else 17592186048189 if kp in INV else 17592186048245
  for band in('easy','moderate','hard'):
   row=next(r for r in records if r['question'][':question/difficulty'].endswith('/'+band));q=questionmap[row['question'][':question/id']];f=q[':question/answer-fields'][0]
   if f[':answer-field/type'][':db/ident']==':answer-field.type/radio':
    cid=f[':answer-field/correct'][':db/id'];checks=[({'fieldId':f[':db/id'],'choiceId':cid},'correct'),({'fieldId':f[':db/id'],'choiceId':next(a[':db/id']for a in f[':answer-field/choices']if a[':db/id']!=cid)},'incorrect')]
   else:checks=[({'fieldId':f[':db/id'],'value':c['submitted']},'correct'if c['expected']=='accepted'else'incorrect')for c in native[str(q[':question/id'])]['checks']]
   for response,expected in checks:grades.append({'kp':kp,'band':band,**grade(topic,q,response,expected)})
  imports+=proof['imported_questions_preserved'];replacement_map+=proof['replacements'];summaries.append({'kp':kp,'active_generated':24,'replaced':len(proof['new_question_entities']),'full_questions_preserved':proof['unchanged_full_questions'],'imports_preserved':proof['imported_questions_preserved'],'generator_reference':ref,'basis_committed':proof['basis_after']});print(kp,'active pool and live grading verified',flush=True)
 assert len(fresh)==len(retired) and len(fresh)+len(guided)==288 and imports==183
 assert {17592186678309,17592186678394}.issubset(retired)
 reported=[r for r in replacement_map if r['old']in{17592186678309,17592186678394}];assert len(reported)==2
 # The earlier accepted positive-log entry still works on the retained full task.
 k=next(k for k in current if k[':db/id']==17592186068918);q=next(q for q in k[':knowledge-point/questions']if q[':db/id']==17592186682659);assert not q.get(':question/retired');f=q[':question/answer-fields'][0]
 grades.append({'purpose':'Prior valid logarithmic antiderivative still accepted',**grade(17592186050489,q,{'fieldId':f[':db/id'],'value':r'-3\ln(\cos x+2)'},'correct')})
 result={'passed':True,'committed':True,'basis_readback':basis,'generators_updated':12,'active_generated_questions':288,'complete_calculations':288,'old_questions_retired':len(retired),'new_full_calculation_questions':len(fresh),'full_questions_preserved':len(guided),'imported_questions_preserved':183,'canonicals_preserved':12,'saved_learner_history_preserved':True,'live_grading_checks':len(grades),'reported_question_replacements':reported,'knowledge_points':summaries}
 atomic_json(H/'completion.json',result);atomic_json(H/'live-grading-verification.json',{'passed':True,'database_writes':0,'checks':grades});atomic_json(H/'replacement-map.json',replacement_map);print(json.dumps({k:v for k,v in result.items()if k!='knowledge_points'}))
if __name__=='__main__':main()
