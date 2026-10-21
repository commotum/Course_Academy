"""Restore source None answers, preserving owned banks and saved selection semantics."""
import copy,hashlib,sys,uuid
from audit import *
from capture.scripts.database.edn import kw
from capture.scripts.database.preview import _library
def stable_id(kind, source):
 return uuid.uuid5(uuid.NAMESPACE_URL, "course-academy:ma:capture:"+kind+":"+source)
SOURCE=':agent/codex'
IDENTS=dict(json.loads((ROOT/'reference/mathacademy/repairs/2026-10-18-equation-chains/idents.json').read_text()));NAMES={v:k for k,v in IDENTS.items()}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x)for k,x in v.items()}
 if isinstance(v,(tuple,list)):return sorted([canonical(x)for x in v],key=lambda x:json.dumps(x,sort_keys=True))
 return str(v)if isinstance(v,uuid.UUID)else v
def equal(a,b):return canonical(a)==canonical(b)
def ledger():
 rows=json.loads((HERE/'resolutions.json').read_text())
 # This checkbox was explicitly removed by the same historical migration policy.
 rows.append({'id':17592186234490,'ma_id':'q-96676','source_evidence':'reference/edb-math/imports/authored-checkboxes/2026-10-11/topic-3215/remove-none/plan.json','source_fields':[],'source_none_answer':None,'source_none_value':'None','key':'None of the above','none_correct':False,'prior_choice_mapping':[],'reuse_field':17592186408178})
 return sorted(rows,key=lambda r:r['id'])
def build_preview():
 library=_library(DB.config);binary=HERE/'native-preview'
 command=['rustc','--edition=2024','-O',str(HERE/'preview.rs'),'--extern','edb_core='+str(library),'-L','dependency='+str(library.parent),'-o',str(binary)]
 run=subprocess.run(command,capture_output=True,text=True);(HERE/'build.stderr').write_text(run.stderr);run.check_returncode()
 save(HERE/'build.json',{'library':str(library),'library_sha256':sha(library),'source_sha256':sha(HERE/'preview.rs'),'binary_sha256':sha(binary)})
 return binary

def field_plan(row):
 token=row['ma_id']+'/explicit-none-checkbox-v1';field='field-'+token
 return {'field_tempid':field,'field_uuid':str(stable_id('field',token)),'answer_tempids':{v:'answer-'+token+'/'+v for v in ('false','true')},'answer_uuids':{v:str(stable_id('answer',token+'/'+v))for v in ('false','true')}}

def prepare(number):
 rows=ledger()[(number-1)*200:number*200];assert rows
 base=HERE/f'batch-{number:02}'
 base.mkdir(exist_ok=True)
 assert not (base/'request.json').exists(),'Retain/reconcile existing request before preparing again'
 process=subprocess.Popen([str(HERE/'native-preview'),str(base),SOURCE],env=DB.environment,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 try:
  first=process.stdout.readline();assert first.startswith('CAPTURED_BASIS '),first;basis=int(first.split()[1]);identity=DB.status();assert identity['lineage']==json.loads((HERE/'identity.json').read_text())['lineage']
  ids=[r['id']for r in rows];sourceids=sorted({f for r in rows for f in r['source_fields']});reused=[r['reuse_field']for r in rows if r['reuse_field']]
  items=DB.query('[:find ?q ?i :in $ [?q ...] :where [?i :task-item/content ?q]]',[ids],base/'queries','items',basis)
  groups=[('questions',QUESTION,ids),('items',ITEM,sorted({i for q,i in items})),('source-fields','[* {:answer-field/correct [*]} {[:answer-field/choices :limit nil] [*]}]',sourceids),('reused-fields','[* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}]',reused)]
  before=native(base,basis,groups);save(base/'before.json',before);questions={q[':db/id']:q for q in before['questions']};sourcefields={f[':db/id']:f for f in before['source-fields']};reusedfields={f[':db/id']:f for f in before['reused-fields']}
  assert len(questions)==len(rows)
  plans=[field_plan(r)for r in rows if not r['reuse_field']]
  for kind,identities in [('answer-field', [uuid.UUID(p['field_uuid'])for p in plans]),('answer',[uuid.UUID(u)for p in plans for u in p['answer_uuids'].values()])]:
   existing=DB.query(f'[:find ?e :in $ [?id ...] :where [?e :{kind}/id ?id]]',[identities],base/'queries',kind+'-prospective-identities',basis);assert not existing
  forms=[];changes=[];mappings=[]
  for row in rows:
   q=questions[row['id']];assert q[':question/math-academy-id']==row['ma_id'];fields=q[':question/answer-fields']
   assert all(f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox'for f in fields)
   assert row['key']not in {f[':answer-field/key']for f in fields}
   assert row['none_correct']==(not any(f[':answer-field/correct'][':answer/value']=='true'for f in fields))
   if row['source_fields']:
    found=[a for fid in row['source_fields']for a in sourcefields[fid][':answer-field/choices']if a[':db/id']==row['source_none_answer']];assert len(found)==1 and found[0][':answer/value']==row['source_none_value']
   p=field_plan(row);p.update(row);p['prompt_before']=q[':question/problem'];p['prompt_after']=re.sub(r'\s*If none apply, leave all boxes unchecked\.', '',p['prompt_before'])
   if row['reuse_field']:
    f=reusedfields[row['reuse_field']];assert f[':answer-field/key']=='None'and f[':answer-field/correct'][':answer/value']=='false';assert set(a[':answer/value']for a in f[':answer-field/choices'])=={'false','true'}
    p['field_tempid']=row['reuse_field'];p['field_uuid']=str(f[':answer-field/id']);p['answer_tempids']={a[':answer/value']:a[':db/id']for a in f[':answer-field/choices']};p['answer_uuids']={a[':answer/value']:str(a[':answer/id'])for a in f[':answer-field/choices']}
    forms.append([kw('db/cas'),row['reuse_field'],kw('answer-field/key'),'None',row['key']])
   else:
    for v in ('false','true'):
     forms.append({kw('db/id'):p['answer_tempids'][v],kw('answer/id'):uuid.UUID(p['answer_uuids'][v]),kw('answer/type'):kw('answer.type/text'),kw('answer/value'):v,kw('db/ensure'):kw('answer/validate')})
    forms.append({kw('db/id'):p['field_tempid'],kw('answer-field/id'):uuid.UUID(p['field_uuid']),kw('answer-field/key'):row['key'],kw('answer-field/type'):kw('answer-field.type/checkbox'),kw('answer-field/choices'):list(p['answer_tempids'].values()),kw('answer-field/correct'):p['answer_tempids'][str(row['none_correct']).lower()],kw('db/ensure'):kw('answer-field/validate')})
   forms.extend([[kw('db/add'),row['id'],kw('question/answer-fields'),p['field_tempid']],[kw('db/ensure'),row['id'],kw('question/validate')]])
   if p['prompt_after']!=p['prompt_before']:forms.append([kw('db/cas'),row['id'],kw('question/problem'),p['prompt_before'],p['prompt_after']])
   choices={a[':db/id']:(f[':db/id'],a[':answer/value'])for f in fields for a in f[':answer-field/choices']};fids={f[':db/id']for f in fields}
   for item in before['items']:
    if item[':task-item/content'][':db/id']!=row['id']:continue
    responses=item.get(':task-item/responses',[])
    if not responses:continue
    ids0={a[':db/id']for a in responses};assert ids0<=set(choices),('unexpected saved response',row['id'],item[':db/id'])
    values={choices[aid][0]:choices[aid][1]for aid in ids0};assert set(values)==fids and len(values)==len(responses),('incomplete saved response',item[':db/id'])
    v=str(not any(x=='true'for x in values.values())).lower()
    forms.extend([[kw('db/add'),item[':db/id'],kw('task-item/responses'),p['answer_tempids'][v]],[kw('db/ensure'),item[':db/id'],kw('task-item/validate')]])
    mappings.append({'item':item[':db/id'],'question':row['id'],'old_responses':sorted(ids0),'none_value':v,'new_response_tempid':p['answer_tempids'][v],'grade_before':all(values[f[':db/id']]==f[':answer-field/correct'][':answer/value']for f in fields)})
   changes.append(p)
  tx=base/'transaction.edn';tx.write_text('[\n'+'\n'.join(dumps(f)for f in forms)+'\n]\n')
  plan={'basis':basis,'lineage':identity['lineage'],'source':SOURCE,'number':number,'questions':changes,'responses':mappings,'sha256':sha(tx)};save(base/'plan.json',plan)
  request={'database':'math','endpoint':str(DB.config.endpoint),'basis':basis,'lineage':identity['lineage'],'source':SOURCE,'sha256':sha(tx),'request_key':f'explicit-none-checkbox-v1-{number}-{basis}-{sha(tx)}'};save(base/'request.json',request)
  out,err=process.communicate('PREVIEW\n',timeout=180);(base/'preview.log').write_text(first+out);(base/'preview.stderr').write_text(err);assert process.returncode==0,err
  report=loads((base/'preview.edn').read_text());check_report(report,plan,False)
  after={n:loads((base/'speculative'/(n+'.edn')).read_text())for n,_,_ in groups};verify_state(before,after,plan,report);save(base/'speculative.json',after)
  save(base/'preview-verification.json',{'passed':True,'committed':False,'basis':basis,'questions':len(changes),'saved_responses':len(mappings),'sha256':sha(tx)})
  print(json.dumps({'preview_passed':True,'batch':number,'basis':basis,'questions':len(rows),'none_correct':sum(r['none_correct']for r in rows),'saved_responses':len(mappings)}),flush=True)
 finally:
  if process.poll()is None:process.kill();process.wait()

def resolved(ref,report):return report[':edb/tempids'][ref]if isinstance(ref,str)else ref

def check_report(report,plan,committed):
 assert report[':edb/committed']is committed and report[':edb/db-before-t']==plan['basis']
 expected=set()
 for p in plan['questions']:
  f=resolved(p['field_tempid'],report)
  if not p['reuse_field']:
   for v in ('false','true'):
    a=resolved(p['answer_tempids'][v],report);expected.update({(a,':answer/id',uuid.UUID(p['answer_uuids'][v]),True),(a,':answer/type',NAMES[':answer.type/text'],True),(a,':answer/value',v,True),(f,':answer-field/choices',a,True)})
   expected.update({(f,':answer-field/id',uuid.UUID(p['field_uuid']),True),(f,':answer-field/key',p['key'],True),(f,':answer-field/type',NAMES[':answer-field.type/checkbox'],True),(f,':answer-field/correct',resolved(p['answer_tempids'][str(p['none_correct']).lower()],report),True)})
  else:expected.update({(f,':answer-field/key','None',False),(f,':answer-field/key',p['key'],True)})
  expected.add((p['id'],':question/answer-fields',f,True))
  if p['prompt_before']!=p['prompt_after']:expected.update({(p['id'],':question/problem',p['prompt_before'],False),(p['id'],':question/problem',p['prompt_after'],True)})
 for r in plan['responses']:expected.add((r['item'],':task-item/responses',resolved(r['new_response_tempid'],report),True))
 observed=set();time=0
 for e,a,v,t,source,added in report[':edb/tx-data']:
  assert source==NAMES[SOURCE]
  if IDENTS[a]==':db/txInstant':time+=1;assert added
  else:observed.add((e,IDENTS[a],v,added))
 assert time==1 and observed==expected,('unexpected datoms',observed-expected,'missing',expected-observed)

def verify_state(before,after,plan,report):
 original={q[':db/id']:q for q in before['questions']};questions={q[':db/id']:q for q in after['questions']};assert set(original)==set(questions)
 for p in plan['questions']:
  q=questions[p['id']];old=original[p['id']];newfid=resolved(p['field_tempid'],report)
  assert equal({k:v for k,v in old.items()if k not in (':question/answer-fields',':question/problem')},{k:v for k,v in q.items()if k not in (':question/answer-fields',':question/problem')})
  assert q[':question/problem']==p['prompt_after']
  assert equal(old[':question/answer-fields'],[f for f in q[':question/answer-fields']if f[':db/id']!=newfid])
  fs=[f for f in q[':question/answer-fields']if f[':db/id']==newfid];assert len(fs)==1;f=fs[0]
  assert str(f[':answer-field/id'])==p['field_uuid']and f[':answer-field/key']==p['key']and f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox'
  bank={a[':answer/value']:a for a in f[':answer-field/choices']};assert set(bank)=={'true','false'}and len(f[':answer-field/choices'])==2
  for v,a in bank.items():assert str(a[':answer/id'])==p['answer_uuids'][v]and a[':answer/type'][':db/ident']==':answer.type/text'
  assert f[':answer-field/correct'][':db/id']==bank[str(p['none_correct']).lower()][':db/id']
  assert any(f[':answer-field/correct'][':answer/value']=='true'for f in q[':question/answer-fields'])
 assert equal(before['source-fields'],after['source-fields'])
 olditems={i[':db/id']:i for i in before['items']};newitems={i[':db/id']:i for i in after['items']};assert set(olditems)==set(newitems);maps={r['item']:r for r in plan['responses']}
 for eid,old in olditems.items():
  new=newitems[eid]
  if eid not in maps:assert equal(old,new);continue
  r=maps[eid];assert equal({k:v for k,v in old.items()if k!=':task-item/responses'},{k:v for k,v in new.items()if k!=':task-item/responses'})
  assert {a[':db/id']for a in new[':task-item/responses']}==set(r['old_responses'])|{resolved(r['new_response_tempid'],report)}
  q=questions[r['question']];selected={a[':db/id']for a in new[':task-item/responses']};assert r['grade_before']==all(f[':answer-field/correct'][':db/id']in selected for f in q[':question/answer-fields'])

def commit(number):
 base=HERE/f'batch-{number:02}';plan=json.loads((base/'plan.json').read_text());request=json.loads((base/'request.json').read_text());assert request['sha256']==sha(base/'transaction.edn')==plan['sha256'];assert json.loads((base/'preview-verification.json').read_text())['passed'];assert json.loads((base/'quality.json').read_text())['passed']
 assert DB.status()['lineage']==request['lineage']
 intent=base/'commit-intent.json'
 if intent.exists():assert json.loads(intent.read_text())==request
 else:save(intent,request)
 receipt=base/'receipt.edn'
 if receipt.exists():report=loads(receipt.read_text());assert report[':edb/committed']is True
 else:
  text=DB.command('transact','--file',base/'transaction.edn','--endpoint',request['endpoint'],'--request-key',request['request_key'],'--basis',request['basis'],'--source',SOURCE,'--timeout-ms','180000',timeout=210);receipt.write_text(text);report=loads(text)
 assert report[':edb/committed']is True
 save(base/'commit-confirmation.json',{'committed':True,'basis_before':report[':edb/db-before-t'],'basis_after':report[':edb/db-after-t'],'request_key':request['request_key'],'sha256':request['sha256']})
 check_report(report,plan,True)
 groups=loads((base/'native-pulls.edn').read_text());before=json.loads((base/'before.json').read_text());after=native(base/'committed',report[':edb/db-after-t'],groups);verify_state(before,after,plan,report);save(base/'committed.json',after)
 history=native(base/'historical',plan['basis'],groups);assert equal(history,before)
 save(base/'verification.json',{'passed':True,'committed':True,'basis_before':plan['basis'],'basis_after':report[':edb/db-after-t'],'questions':len(plan['questions']),'saved_responses_mapped':len(plan['responses']),'old_fields_answers_and_keys_unchanged':True,'source_fields_unchanged':True,'learner_state_and_grades_preserved':True,'historical_snapshot_reproduced':True,'exact_datom_scope_and_source':True})
 print((base/'verification.json').read_text(),flush=True)
if __name__=='__main__':
 if sys.argv[1]=='build':print(build_preview())
 elif sys.argv[1]=='prepare':prepare(int(sys.argv[2]))
 elif sys.argv[1]=='commit':commit(int(sys.argv[2]))
