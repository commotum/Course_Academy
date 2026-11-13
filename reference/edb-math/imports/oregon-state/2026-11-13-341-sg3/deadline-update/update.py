from pathlib import Path
import sys,json,uuid,hashlib,subprocess,re
H=Path(__file__).resolve().parent;R=H.parents[5];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads
from sync_f26_assignments import edn
from f26_assignment_content import Builder,NAV_SECTION,PROBLEM
from import_school_assignments import tidy
P=R.parent/'study/vault/F26/341/11-13-26_SG-3.md'
def save(n,v):(H/n).write_text(json.dumps(v,default=str,indent=2)+'\n')
def prepare():
 assert not(H/'intent.json').exists()
 old=json.loads((H.parent/'entities.json').read_text());activity=next(x for x in old if ':activity/id'in x);tutorial=next(x for x in old if ':tutorial/id'in x)
 s=P.read_text();b=Builder(R.parent/'study/vault');intro=b.render_text(tidy(NAV_SECTION.sub('',s[:next(PROBLEM.finditer(s)).start()])),P,'instructions')
 expected=tutorial[':tutorial/content'].replace('Due: unknown','Due: 2026-11-13\nDue time: 11:59 p.m. PST (date-only deadline convention).\nDeadline source: user confirmation on 2026-11-13 ("due today").')
 assert intro==expected
 db=connection();basis=db.basis();ids=[[kw(':activity/id'),uuid.UUID(activity[':activity/id']['$uuid'])],[kw(':tutorial/id'),uuid.UUID(tutorial[':tutorial/id']['$uuid'])]]
 rows=db.query('[:find ?a ?id (pull ?e [*]) :in $ [[?a ?id]] :where [?e ?a ?id]]',[ids],H,'before',basis);assert len(rows)==2
 a=next(r for attr,i,r in rows if str(attr)==':activity/id');t=next(r for attr,i,r in rows if str(attr)==':tutorial/id');assert ':activity/due'not in a;assert t[':tutorial/content']==tutorial[':tutorial/content']
 due='2026-11-14T07:59:00Z';forms=[[':db/cas',a[':db/id'],':activity/due',None,{'$inst':due}],[':db/cas',t[':db/id'],':tutorial/content',t[':tutorial/content'],intro],[':db/ensure',a[':db/id'],':activity/validate'],[':db/ensure',t[':db/id'],':tutorial/validate']]
 payload='[\n'+'\n'.join(edn(f)for f in forms)+'\n]\n';(H/'transaction.edn').write_text(payload);digest=hashlib.sha256(payload.encode()).hexdigest()
 save('intent.json',{'database':'math','basis':basis,'source':':course-academy.source/editor','request_key':'f26-341-sg3-deadline-'+digest[:24],'sha256':digest,'note_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'activity_entity':a[':db/id'],'tutorial_entity':t[':db/id'],'due':due,'new_intro':intro,'old_note':'F26/341/Undated_SG-3.md','new_note':'F26/341/11-13-26_SG-3.md'})
 run=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(H/'transaction.edn')],env=db.env,capture_output=True,text=True,timeout=120);(H/'preview.log').write_text(run.stdout+run.stderr);assert run.returncode==0,(run.stdout,run.stderr)
 save('render-input.json',[{'entity':t[':db/id'],'attribute':':tutorial/content','value':intro}]);print(run.stdout.strip())
def commit():
 i=json.loads((H/'intent.json').read_text());assert hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest()==i['sha256'];assert hashlib.sha256(P.read_bytes()).hexdigest()==i['note_sha256'];assert json.loads((H/'render-verification.json').read_text())['passed'];assert 'preview_ok'in(H/'preview.log').read_text()
 db=connection();receipt_path=H/'receipt.edn';receipt=loads(receipt_path.read_text())if receipt_path.exists()and receipt_path.stat().st_size else None
 if not receipt or receipt.get(':edb/committed')is not True:
  command=[db.args.edb_bin,'transact','--database','math','--source',i['source'],'--file',str(H/'transaction.edn'),'--endpoint','/tmp/edb-math/writer.sock','--request-key',i['request_key'],'--timeout-ms','120000']
  with receipt_path.open('w')as out,(H/'submit.stderr').open('w')as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,check=True,timeout=160)
  receipt=loads(receipt_path.read_text())
 assert receipt[':edb/committed'];basis=receipt[':edb/db-after-t']
 after=db.query('[:find ?e (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[[i['activity_entity'],i['tutorial_entity']]],H,'after',basis);after=dict(after);before={r[':db/id']:r for _,_,r in loads((H/'before.edn').read_text())}
 from datetime import datetime
 assert datetime.fromisoformat(after[i['activity_entity']][':activity/due'].replace('Z','+00:00'))==datetime.fromisoformat(i['due'].replace('Z','+00:00'))
 assert after[i['tutorial_entity']][':tutorial/content']==i['new_intro']
 def norm(v):
  if isinstance(v,dict):return {k:norm(x)for k,x in v.items()}
  if isinstance(v,list):return sorted([norm(x)for x in v],key=str)
  return v
 for e,row in before.items():
  skip=':activity/due'if e==i['activity_entity']else ':tutorial/content'
  assert norm({k:v for k,v in row.items()if k!=skip})==norm({k:v for k,v in after[e].items()if k!=skip})
 attrs=db.query('[:find ?e ?i :in $ [?i ...] :where [?e :db/ident ?i]]',[[kw('activity/due'),kw('tutorial/content'),kw('db/txInstant')]],H,'attrs',basis);names={e:str(n)for e,n in attrs}
 allowed={(i['activity_entity'],':activity/due'),(i['tutorial_entity'],':tutorial/content')}
 assert all(names.get(d[1])==':db/txInstant'or(d[0],names.get(d[1]))in allowed for d in receipt[':edb/tx-data'])
 save('verification.json',{'committed':True,'basis':basis,'due':i['due'],'note':str(P),'only_deadline_and_intro_updated':True,'question_ids_responses_targets_and_history_preserved':True});print((H/'verification.json').read_text())
if __name__=='__main__':globals()[sys.argv[1]]()
