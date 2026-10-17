"""Detach invalid practice presentations; retain original records and valid work."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode=True
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from audit import TASKS,TASK_PULL
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps,loads,kw,Tagged
HERE=Path(__file__).parent.resolve()
SOURCE=':agent/gpt-6.1-sol-high'
DB=Publisher.from_environment(source=SOURCE).client
NATIVE=ROOT/'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'
BAD={17592186489498:{17592186576138:17592186514433,17592186576139:17592186235429},17592186576141:{17592186576154:17592186514464}}
ITEM_PULL='[* {[:task-item/responses :limit nil] [*]}]'
def save(path,value):path.write_text(json.dumps(value,indent=2,default=str)+'\n')
def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
 if isinstance(v,(list,tuple,set)):return sorted([canonical(x) for x in v],key=lambda x:json.dumps(x,sort_keys=True))
 return v if isinstance(v,(str,int,float,bool)) or v is None else str(v)
def prepare(out,accuracy):
 identity=DB.status();basis=identity['basis']
 def read(name,q,inputs):return DB.query(q,inputs,out/'evidence',name,basis)
 tasks=read('tasks','[:find (pull ?t '+TASK_PULL+') :in $ [?t ...] :where [?t :learner-task/id _]]',[TASKS])
 forms=[];removed=[];retained=[];summary=[]
 for [task] in tasks:
  tid=task[':db/id'];assert task[':learner-task/status'][':db/ident']==':learner-task.status/paused'
  assert task.get(':learner-task/xp-earned',0)==0 and ':learner-task/finished-at' not in task
  assert ':learner-task/active-item' not in task
  all_items={i[':db/id']:i for i in task[':learner-task/items']};bad=BAD[tid]
  assert all(all_items[i][':task-item/content'][':db/id']==q for i,q in bad.items())
  for i in bad:forms.append([kw('db/retract'),tid,kw('learner-task/items'),i])
  good={i:item for i,item in all_items.items() if i not in bad}
  for i,item in good.items():
   nxt=item.get(':task-item/next',{}).get(':db/id')
   if nxt in bad:
    cursor=nxt
    while cursor in bad:cursor=all_items[cursor].get(':task-item/next',{}).get(':db/id')
    assert cursor is None,'This repair is scoped to the observed trailing bad presentations'
    forms.append([kw('db/retract'),i,kw('task-item/next'),nxt])
  elapsed=sum(i[':task-item/elapsed-seconds'] for i in good.values())
  forms.append([kw('db/cas'),tid,kw('learner-task/elapsed-seconds'),task[':learner-task/elapsed-seconds'],elapsed])
  forms.append([kw('db/ensure'),tid,kw('learner-task/validate')])
  removed.extend(bad);retained.extend(good)
  summary.append({'task':tid,'title':task[':learner-task/activity'][':activity/title'],'removed_items':list(bad),'removed_questions':list(bad.values()),'retained_items':len(good),'elapsed_before':task[':learner-task/elapsed-seconds'],'elapsed_after':elapsed})
 if accuracy:
  corrections=loads(Path(accuracy).read_text())
  for form in corrections:
   if str(form[2])==':progress/last-direct-at':
    for index in range(3,len(form)):
     if form[index] is not None:form[index]=Tagged('inst',form[index])
  forms.extend(corrections)
 state_ids=sorted({f[1] for f in forms if str(f[0]) in [':db/cas',':db/retract'] and (str(f[2]).startswith(':progress/') or str(f[2]).startswith(':performance/'))})
 groups=[['tasks',TASK_PULL,TASKS],['items',ITEM_PULL,sorted(removed+retained)],['state','[*]',state_ids],['learner','[*]',[17592186045416]]]
 (out/'transaction.edn').write_text(dumps(forms)+'\n');(out/'native-pulls.edn').write_text(dumps(groups)+'\n')
 attrs=read('attributes','[:find ?a ?ident :where [?a :db/ident ?ident] [?a :db/valueType _]]',[])
 source=read('source','[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]',[kw(SOURCE)])
 assert len(source)==1
 sha=hashlib.sha256((out/'transaction.edn').read_bytes()).hexdigest()
 plan={**identity,'source':SOURCE,'source_eid':source[0][0],'attributes':dict(attrs),'removed_items':sorted(removed),'retained_items':sorted(retained),'tasks':summary,'accuracy_included':bool(accuracy),'sha256':sha,'request_key':f'multipart-activity-b{basis}-{sha}','endpoint':DB.config.endpoint,'transaction_file':str(out/'transaction.edn')}
 save(out/'plan.json',plan)
 print(json.dumps({'prepared':True,'basis':basis,'removed':removed,'retained':len(retained),'accuracy_included':bool(accuracy)}))

def expected_after(value,forms):
 value=copy.deepcopy(value)
 def visit(v):
  if isinstance(v,dict):
   eid=v.get(':db/id')
   for f in forms:
    if f[1]!=eid or str(f[0])==':db/ensure' or f[2] not in v:continue
    attr=f[2]
    if str(f[0])==':db/cas':
     assert canonical(v[attr])==canonical(f[3]),(eid,attr)
     if f[4] is None:v.pop(attr)
     else:v[attr]=copy.deepcopy(f[4])
    elif str(f[0])==':db/retract':
     if isinstance(v[attr],list):v[attr]=[x for x in v[attr] if x.get(':db/id')!=f[3]]
     else:v.pop(attr)
   for x in v.values():visit(x)
  elif isinstance(v,list):
   for x in v:visit(x)
 visit(value);return value

def verify_report(report,plan,committed,forms):
 assert report[':edb/committed'] is committed and report[':edb/db-before-t']==plan['basis']
 expected=set()
 for f in forms:
  op,e,a=str(f[0]),f[1],str(f[2])
  if op==':db/cas':
   if f[3] is not None:expected.add((e,a,str(f[3]),False))
   if f[4] is not None:expected.add((e,a,str(f[4]),True))
  elif op==':db/retract':expected.add((e,a,str(f[3]),False))
 actual=set()
 for e,a,v,tx,source,added in report[':edb/tx-data']:
  assert source==plan['source_eid'];attr=plan['attributes'][str(a)]
  if attr!=':db/txInstant':actual.add((e,attr,str(v),added))
 assert actual==expected,(actual-expected,expected-actual)

def preview(out):
 plan=json.loads((out/'plan.json').read_text());forms=loads((out/'transaction.edn').read_text())
 run=subprocess.run([str(NATIVE),str(out),SOURCE,str(plan['basis'])],env=DB.environment,capture_output=True,text=True,timeout=150)
 (out/'preview.stderr').write_text(run.stderr);run.check_returncode();(out/'preview.edn').write_text(run.stdout)
 verify_report(loads(run.stdout),plan,False,forms)
 for name,pattern,ids in loads((out/'native-pulls.edn').read_text()):
  before=loads((out/f'preview-{name}-before.edn').read_text());after=loads((out/f'preview-{name}-after.edn').read_text())
  assert canonical(expected_after(before,forms))==canonical(after),name
 save(out/'preview-verification.json',{'passed':True,'original_items_and_responses_retained':True,'only_planned_changes':True})
 print('Native data preview passed')

def commit(out):
 plan=json.loads((out/'plan.json').read_text());forms=loads((out/'transaction.edn').read_text())
 assert plan['accuracy_included'] and (out/'preview-verification.json').exists()
 assert (out/'application-preview.json').exists(),'Application resume/continue preview required'
 application=json.loads((out/'application-preview.json').read_text())
 assert application['passed'] and application['basis_before']==plan['basis'] and application['transaction_sha256']==plan['sha256']
 assert hashlib.sha256((out/'transaction.edn').read_bytes()).hexdigest()==plan['sha256']
 assert DB.status()['lineage']==plan['lineage']
 intent=out/'commit-intent.json'
 if intent.exists():assert json.loads(intent.read_text())==plan
 else:save(intent,plan)
 receipt=out/'receipt.edn'
 if not receipt.exists():receipt.write_text(DB.command('transact','--source',SOURCE,'--file',plan['transaction_file'],'--basis',plan['basis'],'--endpoint',plan['endpoint'],'--request-key',plan['request_key'],'--timeout-ms','120000',timeout=150))
 report=loads(receipt.read_text());verify_report(report,plan,True,forms);after_basis=report[':edb/db-after-t']
 def check(group):
  name,pattern,ids=group
  for basis,stage in [(plan['basis'],'before'),(after_basis,'after')]:
   rows=DB.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e _ _]]',[ids],out/'readback',name+'-'+stage,basis) if ids else []
   assert canonical([e for [e] in rows])==canonical(loads((out/f'preview-{name}-{stage}.edn').read_text())),name
 with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(check,loads((out/'native-pulls.edn').read_text())))
 result={'committed':True,'basis_before':plan['basis'],'basis_after':after_basis,'tasks':plan['tasks'],'removed_items':plan['removed_items'],'valid_items_retained':len(plan['retained_items']),'accuracy_replayed':True,'original_records_and_responses_retained':True,'exact_committed_and_historical_readback':True,'application_preview':'application-preview.json','request_key':plan['request_key']}
 save(out/'verification.json',result);save(HERE/'verification.json',result);print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--attempt',required=True);p.add_argument('--accuracy');p.add_argument('--preview',action='store_true');p.add_argument('--commit',action='store_true');a=p.parse_args();out=HERE/a.attempt;out.mkdir(exist_ok=True)
 if a.commit:commit(out)
 elif a.preview:preview(out)
 else:prepare(out,a.accuracy)
