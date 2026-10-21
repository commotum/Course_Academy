"""Capture, validate, preview, submit and verify one authorized presentation batch.

Exact persisted intents always take precedence over fresh preparation. Rejected
bases are archived; unknown outcomes are retried only with their original key.
"""
import argparse,copy,hashlib,json,runpy,shutil,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from capture.scripts.database.edn import loads,dumps,kw
from capture.scripts.database.client import StaleBasis,EDBCommandError
QP=runpy.run_path(str(HERE/'audit.py'))['QUESTION_PULL']
SOURCE=':agent/codex';SOURCE_ID=17592186576411
ATTRS={50:':db/txInstant',1071:':question/problem',1074:':question/worked-solution',1077:':answer-field/key'}
def save(path,v):
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(jsonable(v),ensure_ascii=False,indent=2)+'\n');tmp.replace(path)
def read(path):return loads(path.read_text())if path.suffix=='.edn'else json.loads(path.read_text())
def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x)for k,x in sorted(v.items())}
 if isinstance(v,list):return sorted((canonical(x)for x in v),key=lambda x:json.dumps(x,sort_keys=True,default=str))
 return jsonable(v)
def command(args,output,env=None):
 r=subprocess.run([str(x)for x in args],env=env,capture_output=True,text=True)
 output.with_suffix('.stdout').write_text(r.stdout);output.with_suffix('.stderr').write_text(r.stderr)
 if r.returncode:raise RuntimeError(str(args[0])+': '+r.stderr[-3000:]+r.stdout[-1000:])
 return r.stdout
def verify_report(report,changes,basis,committed):
 assert report[':edb/committed'] is committed and report[':edb/db-before-t']==basis
 assert ':edb/report-error'not in report
 expected={(c['entity'],c['attribute'],c[s],added)for c in changes for s,added in [('before',False),('after',True)]}
 actual=[]
 for e,a,v,t,s,added in report[':edb/tx-data']:
  assert s==SOURCE_ID,(e,a,'wrong contributor')
  assert a in ATTRS,('unexpected attribute',a)
  if a!=50:actual.append((e,ATTRS[a],v,added))
 assert len(actual)==len(expected)and set(actual)==expected,'Unexpected transaction effect'
 return {'exact_datoms':len(actual),'contributor_verified':True}
def refresh(pub,directory,ids,basis):
 directory.mkdir(parents=True,exist_ok=True)
 groups=[['questions',QP,ids],['provenance','[:db/id :db/ident]',[SOURCE_ID,*ATTRS]]]
 (directory/'native-pulls.edn').write_text(dumps(groups)+'\n')
 command([HERE/'validation/refresh',directory,basis],directory/'refresh',pub.client.environment)
 prov=read(directory/'capture-provenance.edn')
 assert {r[':db/id']:str(r[':db/ident'])for r in prov}=={SOURCE_ID:SOURCE,**ATTRS}
 return read(directory/'capture-questions.edn')
def prepare_cases(reviewed,current):
 byid={q[':db/id']:jsonable(q)for q in current};cases=[];changes=[]
 for c in reviewed:
  qid=c['before'][':db/id'];b=byid[qid];a=copy.deepcopy(b);old=c['before'];new=c['after']
  bf={f[':db/id']:f for f in b[':question/answer-fields']};nf={f[':db/id']:f for f in new[':question/answer-fields']}
  assert set(bf)==set(nf),'Field membership changed during review'
  for attr in [':question/problem',':question/worked-solution']:
   if old.get(attr)!=new.get(attr):
    assert b.get(attr)==old.get(attr),(qid,attr,'Concurrent content edit needs review')
    a[attr]=new[attr];changes.append({'entity':qid,'attribute':attr,'before':b[attr],'after':a[attr]})
  for f in a[':question/answer-fields']:
   fid=f[':db/id'];of=next(x for x in old[':question/answer-fields']if x[':db/id']==fid)
   if of[':answer-field/key']!=nf[fid][':answer-field/key']:
    assert f[':answer-field/key']==of[':answer-field/key'],(qid,fid,'Concurrent field edit')
    changes.append({'entity':fid,'attribute':':answer-field/key','before':f[':answer-field/key'],'after':nf[fid][':answer-field/key']})
    f[':answer-field/key']=nf[fid][':answer-field/key']
  cases.append({**c,'question':qid,'before':b,'after':a})
 assert changes and len({(c['entity'],c['attribute'])for c in changes})==len(changes)
 return cases,changes
def submit(pub,d,plan):
 tx=(d/'transaction.edn').read_text();basis=plan['basis'];digest=hashlib.sha256(tx.encode()).hexdigest()
 assert digest==plan['transaction_sha256']
 intentpath=d/'commit-intent.json'
 if intentpath.exists():intent=read(intentpath);assert intent['transaction_edn']==tx and intent['basis']==basis
 else:
  assert read(d/'preview-verification.json')['passed']
  intent={'database':plan['database'],'lineage':plan['lineage'],'basis':basis,'source':SOURCE,'request_key':'checkbox-object-labels-'+str(basis)+'-'+digest,'endpoint':pub.config.endpoint,'transaction_edn':tx,'transaction_sha256':digest,'authorized':True,'authorization':'User requested fixing all instances of the misplaced checkbox option content and authorized database repairs without waiting.'}
  save(intentpath,intent)
 assert (intent['database'],intent['lineage'])==(plan['database'],plan['lineage'])
 if not(d/'receipt.edn').exists():
  save(d/'request.json',{'state':'submitted-outcome-pending','request_key':intent['request_key']})
  for retry in range(3):
   try:
    output=pub.client.command('transact','--file',d/'transaction.edn','--endpoint',intent['endpoint'],'--source',intent['source'],'--basis',basis,'--request-key',intent['request_key'],'--timeout-ms','120000',timeout=240)
    break
   except StaleBasis as e:save(d/'request.json',{'state':'explicit-stale-basis-rejection','error':str(e),'committed':False});raise
   except EDBCommandError as e:
    save(d/'request.json',{'state':'submitted-outcome-pending','request_key':intent['request_key'],'error':str(e),'reconciliation_attempt':retry+1})
    if retry==2:raise
    time.sleep(2)
  (d/'receipt.edn').write_text(output)
 receipt=read(d/'receipt.edn');checks=verify_report(receipt,read(d/'changes.json'),basis,True)
 save(d/'request.json',{'state':'confirmed','committed':True,'basis':receipt[':edb/db-after-t'],'request_key':intent['request_key']})
 readback=d/'committed';qs=refresh(pub,readback,plan['question_ids'],receipt[':edb/db-after-t'])
 cases=read(d/'cases.json')['cases']
 assert canonical(qs)==canonical([c['after']for c in cases]),'Committed Pull differs'
 assert canonical(read(readback/'incoming.edn'))==canonical(read(d/'incoming.edn')),'Incoming references changed'
 command([sys.executable,HERE/'validation/verify.py',d/'cases.json','--before',d/'capture-questions.edn','--after',readback/'capture-questions.edn','--incoming-before',d/'incoming.edn','--incoming-after',readback/'incoming.edn','--output',readback/'validation'],readback/'verify')
 result={'passed':True,'committed':True,'basis_before':basis,'basis_after':receipt[':edb/db-after-t'],'questions':len(cases),'fields':sum(len(c['objects'])for c in cases),'changed_attributes':len(read(d/'changes.json')),'transaction_sha256':digest,**checks}
 save(d/'commit-verification.json',result);print(json.dumps(result),flush=True)
 runpy.run_path(str(HERE/'checkpoint.py'),run_name='__main__')
 return result
def run(reviewed,name,commit):
 pub=Publisher.from_environment(source=SOURCE);parent=HERE/'batches'/name;parent.mkdir(parents=True,exist_ok=True)
 # Recover any prior attempt before making a fresh read-dependent request.
 for d in sorted(parent.glob('attempt-*')):
  if(d/'commit-verification.json').exists():return read(d/'commit-verification.json')
  if(d/'commit-intent.json').exists()and read(d/'request.json').get('state')!='explicit-stale-basis-rejection':
   try:return submit(pub,d,read(d/'plan.json'))
   except StaleBasis:continue
 ids=sorted(c['before'][':db/id']for c in reviewed)
 for attempt in range(1,11):
  status=pub.client.status();basis=status['basis'];d=parent/('attempt-'+str(basis))
  revision=1
  while d.exists():
   d=parent/('attempt-'+str(basis)+'-revision-'+str(revision));revision+=1
  current=refresh(pub,d,ids,basis);cases,changes=prepare_cases(reviewed,current)
  save(d/'cases.json',{'cases':cases});save(d/'changes.json',changes)
  forms=[[kw(':db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']]for c in changes]
  for c in cases:
   q=c['before'];forms.append([kw(':db/ensure'),q[':db/id'],kw(':question/validate')])
   for f in q[':question/answer-fields']:
    forms.append([kw(':db/ensure'),f[':db/id'],kw(':answer-field/validate')])
    for a in f[':answer-field/choices']:forms.append([kw(':db/ensure'),a[':db/id'],kw(':answer/validate')])
   for i in q.get(':task-item/_content',[]):forms.append([kw(':db/ensure'),i[':db/id'],kw(':task-item/validate')])
  tx=dumps(forms)+'\n';(d/'transaction.edn').write_text(tx)
  digest=hashlib.sha256(tx.encode()).hexdigest();plan={**status,'source':SOURCE,'source_id':SOURCE_ID,'question_ids':ids,'transaction_sha256':digest,'forms':len(forms),'bytes':len(tx.encode())};save(d/'plan.json',plan)
  command([sys.executable,HERE/'validation/verify.py',d/'cases.json','--output',d/'validation'],d/'verify')
  presentation=[{'id':c['question'],'problem':c['after'].get(':question/problem'),'solution':c['after'].get(':question/worked-solution'),'objects':c['objects']}for c in cases]
  renderhash=hashlib.sha256(json.dumps(presentation,sort_keys=True).encode()).hexdigest();cache=HERE/'render-cache'/renderhash
  # Reuse exhaustive actual-UI evidence only for byte-identical rendered cases.
  for global_render in [HERE/'mapping-render',HERE/'mapping/final-render-approved']:
   if(cache/'rendering-summary.json').exists():break
   if not(global_render/'rendering-summary.json').exists():continue
   full={c['id']:c for c in read(global_render/'render-cases.json')if c['stage']=='after'}
   local=[c for c in read(d/'validation/render-cases.json')if c['stage']=='after']
   if all(c==full.get(c['id'])for c in local):
    wanted={c['id']for c in local};summary=copy.deepcopy(read(global_render/'rendering-summary.json'));report=read(global_render/'rendering-report.json')
    selected=[m for m in report['measurements']if m['id']in wanted and m['stage']=='after']
    assert len(selected)==2*len(local)
    for key in ['afterCritical','beforeCritical','afterOverflow','beforeOverflow']:summary[key]=[r for r in summary[key]if r['id']in wanted]
    summary['rendered']=len(selected);summary['checkboxResponseChecks']=sum(len(m['responseChecks'])for m in selected)
    cache.mkdir(parents=True,exist_ok=True);save(cache/'render-cases.json',local);save(cache/'rendering-summary.json',summary)
    save(cache/'rendering-report.json',{**report,'measurements':selected,'global_evidence':str(global_render.relative_to(HERE))})
  if not(cache/'rendering-summary.json').exists():
   cache.mkdir(parents=True,exist_ok=True);shutil.copy(d/'validation/render-cases.json',cache/'render-cases.json')
   command(['node',HERE/'validation/render.cjs',cache,'--after-only'],cache/'render')
  render=read(cache/'rendering-summary.json');assert not render['errors']and not render['afterCritical'],('Rendering errors',cache,render['afterCritical'])
  save(d/'render-evidence.json',{'hash':renderhash,'directory':str(cache.relative_to(HERE)),'summary':render})
  live=pub.client.status()
  assert (status['database'],status['lineage'])==(live['database'],live['lineage'])
  if live['basis']!=basis:
   save(d/'preparation-status.json',{'state':'not-submitted-basis-advanced','current_basis':live['basis']});continue
  preview=ROOT/'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'
  output=command([preview,d,SOURCE,basis],d/'preview-run',pub.client.environment);(d/'preview.edn').write_text(output)
  checks=verify_report(loads(output),changes,basis,False)
  assert canonical(read(d/'preview-questions-before.edn'))==canonical(current)
  assert canonical(read(d/'preview-questions-after.edn'))==canonical([c['after']for c in cases])
  command([sys.executable,HERE/'validation/verify.py',d/'cases.json','--before',d/'preview-questions-before.edn','--after',d/'preview-questions-after.edn','--output',d/'preview-validation'],d/'preview-verify')
  save(d/'preview-verification.json',{'passed':True,'committed':False,'basis':basis,'transaction_sha256':digest,**checks})
  print('Prepared '+name+' at '+str(basis)+' ('+str(len(cases))+' questions)',flush=True)
  if not commit:return {'prepared':True,'directory':str(d)}
  try:return submit(pub,d,plan)
  except StaleBasis:continue
 raise RuntimeError('Repeated basis changes; all unsubmitted work preserved')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('cases',type=Path);parser.add_argument('name');parser.add_argument('--commit',action='store_true');args=parser.parse_args()
 document=read(args.cases);run(document['cases'],args.name,args.commit)
