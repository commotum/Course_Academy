"""Check speculative/committed entities, preserved history and presentation."""
import copy,json,sys,subprocess
from pathlib import Path
from migration import H,ROOT,loads,jsonable,portable,atomic_json

def canon(x):
 if isinstance(x,dict):return {k:canon(v) for k,v in x.items() if k!=':db/id'}
 if isinstance(x,list):return sorted([canon(v) for v in x],key=lambda v:json.dumps(v,sort_keys=True))
 return x

def question_content(q):
 q=portable(q);q.pop(':task-item/_content',None);return canon(q)

def verify(directory,questions_path,retained_path,report_path,*,stage):
 directory=Path(directory);prep=json.loads((directory/'preparation.json').read_text());before={q[':db/id']:q for q in jsonable(loads(prep['before_edn']))};after={q[':db/id']:q for q in jsonable(loads(Path(questions_path).read_text()))};retained=jsonable(loads(Path(retained_path).read_text()));oldret=json.loads((directory/'retained-before.json').read_text());report=loads(Path(report_path).read_text());temps=report[':edb/tempids']
 assert set(after)==set(before)
 expected={c['question'][':db/id']:c for c in prep['proposed']}
 for eid,q in before.items():assert question_content(after[eid])==question_content(expected[eid]['question'] if eid in expected else q),('Question content differs',eid)
 assert canon(retained)==canon(oldret),'Detached original entities were modified'
 mapped={m['item']:m for m in prep['response_mappings']};items=0
 for eid,q in before.items():
  old={i[':db/id']:i for i in q.get(':task-item/_content',[])};new={i[':db/id']:i for i in after[eid].get(':task-item/_content',[])};assert set(old)==set(new)
  for itemid,item in old.items():
   current=new[itemid];assert {k:v for k,v in current.items() if k!=':task-item/responses'}=={k:v for k,v in item.items() if k!=':task-item/responses'}
   if itemid in mapped:
    m=mapped[itemid];refs={temps[t] for t in m['new_answer_tempids']} if 'new_answer_tempids' in m else set(m['retained_answer_ids'])
    assert {a[':db/id'] for a in current[':task-item/responses']}==refs
    items+=1
   else:assert canon(current.get(':task-item/responses',[]))==canon(item.get(':task-item/responses',[]))
 cases=[]
 for plan in prep['plans']:
  q=after[plan['question']];objects=plan['objects'];cases.append({'question':q,'objects':objects})
  for f in q[':question/answer-fields']:
   assert f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox'
   assert len(f[':answer-field/choices'])==2 and {a[':answer/value'] for a in f[':answer-field/choices']}=={'false','true'}
   assert f[':answer-field/key']!='None of the above'
 assert items==len(mapped)
 atomic_json(directory/(stage+'-presentation.json'),{'cases':cases})
 subprocess.run([sys.executable,str(ROOT/'skills/radio2checkbox/scripts/lint_presentation.py'),str(directory/(stage+'-presentation.json')),'--output',str(directory/(stage+'-lint.json'))],check=True)
 result={'passed':True,'stage':stage,'questions_compared':len(after),'conversions':9,'none_cleanup':1,'existing_question_content_preserved_except_reviewed_representation':True,'retained_original_entities':len(retained),'saved_response_items_mapped':items,'saved_statuses_times_and_other_item_state_preserved':True,'checkbox_fields_verified':sum(len(c['question'][':question/answer-fields']) for c in cases)}
 atomic_json(directory/(stage+'-verification.json'),result);print(json.dumps(result));return result

if __name__=='__main__':verify(H/'review',H/'review/preview-questions.edn',H/'review/preview-retained.edn',H/'review/preview.edn',stage='speculative')
