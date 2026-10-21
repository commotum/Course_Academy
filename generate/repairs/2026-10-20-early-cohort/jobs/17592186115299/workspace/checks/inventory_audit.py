"""Read-only audit of supplied inventory; never labels source questions generated."""
import json,sys,subprocess,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import validate_repair as c

def main():
 inv=json.loads((c.ROOT.parent/'source/inventory.json').read_text());source_ids={q[':question/id'] for q in json.loads((c.E/'source-questions.json').read_text())};generated=[q for q in inv['questions'] if q[':question/id'] not in source_ids];summary=[];fixtures=[]
 for q in generated:
  m=c.v.system(q[':question/problem']);kind=c.v.independent_class(m);checks=[];true=0
  mm=c.v.matrices(c.plain(q[':question/worked-solution']));assert mm[0]==m and mm[1]==m;c.v.operation_checks(c.plain(q[':question/worked-solution']))
  assert m.rref()[0]==mm[-1].rref()[0]
  for i,f in enumerate(q[':question/answer-fields']):
   assert f[':answer-field/type'][':db/ident'].endswith('/checkbox')
   expected='true' if c.category(f[':answer-field/key'])==kind else 'false';true+=expected=='true'
   assert f[':answer-field/correct'][':answer/value']==expected
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==expected else 'rejected','purpose':'Read-only stored generated question key audit from independently solved printed equations'})
  assert true==1
  summary.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'difficulty':q[':question/difficulty'][':db/ident'],'classification':kind,'math_and_all_keys_checked':True})
  native_q=copy.deepcopy(q)
  native_q[':question/difficulty']=native_q[':question/difficulty'][':db/ident']
  for f in native_q[':question/answer-fields']:
   f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
   for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
  fixtures.append({'label':q[':question/id'],'record':{'knowledge_point':{'db_id':c.g.KP_ID,'id':c.g.KP_UUID,'title':c.g.TITLE},'question':native_q},'checks':checks})
 assert not any(x['difficulty'].endswith('/moderate') for x in summary), 'Stored generated moderate requires exact legacy generator reproduction and shortcut audit'
 (c.ROOT/'affected-inventory.json').write_text('{"affected_questions": []}\n')
 c.dump('inventory-native-input.json',fixtures)
 subprocess.run([str(c.REPO/'generate/runs/current/check-engine'),str(c.E/'inventory-native-input.json'),str(c.E/'inventory-native-report.json')],check=True)
 c.dump('inventory-audit.json',{'passed':True,'inventory_basis':inv['basis'],'inventory_questions':len(inv['questions']),'original_source_questions':len(inv['questions'])-len(generated),'generated_questions_checked':summary,'affected_questions':[],'finding_scope':'Packaging depends on executable closure and does not corrupt a stored question. Fixed per-source moderate classifications apply to the legacy moderate generator; supplied inventory contains no generated moderate instances. All ten generated easy/hard records were independently checked for printed operations and all keys, then graded with the native engine. This is verified absence for demonstrated findings at the captured inventory, not a claim about live inventory or every possible defect.','command':'python checks/inventory_audit.py'})
 print(json.dumps({'passed':True,'generated_checked':len(generated),'affected':0}))
if __name__=='__main__':main()
