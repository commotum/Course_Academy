from pathlib import Path
import sys,json,hashlib,uuid,importlib.util,subprocess
R=Path('/home/jake/Developer/Course_Academy');H=R/'reference/edb-math/imports/oregon-state/2026-11-13-256-r7';D=H/'confirmed-corrections';sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads
from sync_f26_assignments import edn
spec=importlib.util.spec_from_file_location('rec7',H/'prepare.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def save(n,v):(D/n).write_text(json.dumps(v,default=str,indent=2)+'\n')
def prepare():
 D.mkdir(exist_ok=True);assert not(D/'intent.json').exists()
 b=m.native.NativeBuilder(m.V);activity=m.Builder.assignment(b,m.REL);next(e for e in b.entities if ':activity/id'in e)[':activity/title']='MTH 256 — R-7: Quiz 3 Review';b.validate()
 old={e[':db/id']:e for e in json.loads((H/'entities.json').read_text())};new={e[':db/id']:e for e in b.entities};assert old.keys()==new.keys()
 changes=[]
 for uid,e in new.items():
  assert e.keys()==old[uid].keys()
  for a,v in e.items():
   if v!=old[uid][a]:
    assert a in [':question/problem',':question/worked-solution',':answer/value',':tutorial/content'],a
    ident=next(k for k in e if k.endswith('/id')and k!=':db/id')
    changes.append({'uid':uid,'identity_attribute':ident,'identity':e[ident]['$uuid'],'attribute':a,'old':old[uid][a],'new':v,'ensure':e[':db/ensure']})
 assert len(changes)==6 and len({c['uid']for c in changes})==4
 save('entities.json',b.entities);db=connection();basis=db.basis();identities=list({(c['identity_attribute'],c['identity'])for c in changes})
 rows=db.query('[:find ?a ?id (pull ?e [*]) :in $ [[?a ?id]] :where [?e ?a ?id]]',[[[kw(a),uuid.UUID(i)]for a,i in identities]],D,'before',basis);assert len(rows)==4
 stored={(str(a),str(i)):e for a,i,e in rows};forms=[]
 for c in changes:
  e=stored[c['identity_attribute'],c['identity']];assert e[c['attribute']]==c['old'],('Current content differs',c['attribute']);c['entity']=e[':db/id']
  forms.append([':db/cas',c['entity'],c['attribute'],c['old'],c['new']])
 for uid in {c['uid']for c in changes}:
  c=next(c for c in changes if c['uid']==uid);forms.append([':db/ensure',c['entity'],c['ensure']])
 payload='[\n'+'\n'.join(edn(f)for f in forms)+'\n]\n';(D/'transaction.edn').write_text(payload);save('changes.json',changes)
 save('intent.json',{'database':'math','source':':course-academy.source/editor','request_key':'f26-256-r7-confirmed-'+hashlib.sha256(payload.encode()).hexdigest()[:24],'sha256':hashlib.sha256(payload.encode()).hexdigest(),'prepared_basis':basis,'file':str(D/'transaction.edn'),'note_sha256':hashlib.sha256((m.V/m.REL).read_bytes()).hexdigest()})
 save('render-input.json',[{'entity':c['entity'],'attribute':c['attribute'],'value':c['new']}for c in changes])
 # Only the changed graded prompt needs a fresh grader check; its math answer is unchanged.
 qid=b.audit['activities'][0]['problems'][-1]['quizzes'][0]['question_id'];case=next(c for c in json.loads((H/'grading-input.json').read_text())if c['label']==qid);case['record']['question'][':question/problem']=new[qid][':question/problem'];save('grading-input.json',[case])
 print('Prepared six content updates on four existing entities; IDs, targets and learner responses unchanged.')
def check():
 db=connection();run=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(D/'transaction.edn')],env=db.env,capture_output=True,text=True,timeout=120);(D/'preview.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr
 run=subprocess.run([str(R/'generate/runs/current/check-engine'),str(D/'grading-input.json'),str(D/'grading-verification.json')],capture_output=True,text=True,timeout=120);assert run.returncode==0,(run.stdout,run.stderr);print(run.stdout.strip())
 print((D/'preview.log').read_text().strip())
def commit():
 intent=json.loads((D/'intent.json').read_text());p=D/'transaction.edn';assert hashlib.sha256(p.read_bytes()).hexdigest()==intent['sha256'];assert hashlib.sha256((m.V/m.REL).read_bytes()).hexdigest()==intent['note_sha256']
 assert json.loads((D/'render-verification.json').read_text())['passed'];assert json.loads((D/'grading-verification.json').read_text())['passed'];assert 'preview_ok' in(D/'preview.log').read_text()
 db=connection()
 if not(D/'receipt.edn').exists():
  receipt=db.command('transact','--file',p,'--source',intent['source'],'--request-key',intent['request_key'],'--endpoint','/tmp/edb-math/writer.sock');(D/'receipt.edn').write_text(receipt)
 receipt=loads((D/'receipt.edn').read_text());assert receipt[':edb/committed'];basis=receipt[':edb/db-after-t'];changes=json.loads((D/'changes.json').read_text())
 rows=db.query('[:find ?e (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[[c['entity']for c in changes]],D,'after',basis);after={e:r for e,r in rows}
 before_rows=loads((D/'before.edn').read_text());before={r[':db/id']:r for _,_,r in before_rows}
 for eid,row in before.items():
  expected=dict(row)
  for c in changes:
   if c['entity']==eid:expected[c['attribute']]=c['new']
  def normalize_refs(v):
   if isinstance(v,dict)and ':db/id'in v:return v[':db/id']
   if isinstance(v,list):return [normalize_refs(x)for x in v]
   return v
  assert {k:normalize_refs(v)for k,v in after[eid].items()}=={k:normalize_refs(v)for k,v in expected.items()}
 attrs=db.query('[:find ?a ?name :in $ [?name ...] :where [?a :db/ident ?name]]',[[kw(c['attribute'])for c in changes]+[kw('db/txInstant')]],D,'attributes',basis);names={e:str(n)for e,n in attrs};allowed={(c['entity'],c['attribute'])for c in changes}
 for datom in receipt[':edb/tx-data']:
  assert names.get(datom[1])==':db/txInstant'or(datom[0],names.get(datom[1]))in allowed,datom
 save('verification.json',{'committed':True,'basis_t':basis,'changed_attributes':len(changes),'changed_entities':len(after),'only_requested_content_changed':True,'learner_history_and_targets_unchanged':True,'request_key':intent['request_key']});print((D/'verification.json').read_text())
if __name__=='__main__':globals()[sys.argv[1]]()
