from pathlib import Path
import json,sys,uuid,hashlib,subprocess
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
R=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads
from sync_f26_assignments import edn
from f26_assignment_content import Builder,NAV_SECTION
from import_school_assignments import tidy
BASE=R/'reference/edb-math/imports/oregon-state/2026-10-29-341-sg2';H=BASE/'deadline-2026-10-30';H.mkdir(exist_ok=True)
def save(n,v):(H/n).write_text(json.dumps(v,default=str,indent=2)+'\n')
def main():
 oldentities=json.loads((BASE/'entities.json').read_text());activity=next(e for e in oldentities if ':activity/id'in e);tutorial=next(e for e in oldentities if e.get(':tutorial/title')=='Assignment information')
 aid=activity[':activity/id']['$uuid'];tid=tutorial[':tutorial/id']['$uuid'];audit=json.loads((BASE/'source-audit.json').read_text());db=connection()
 due=datetime(2026,10,30,23,59,59,tzinfo=ZoneInfo('America/Los_Angeles')).astimezone(timezone.utc).isoformat().replace('+00:00','Z')
 path=R.parent/'study/vault/F26/341/10-30-26_SG-2.md';raw=path.read_text();intro=Builder(path.parents[3]).render_text(tidy(NAV_SECTION.sub('',raw.split('## Problem 1')[0])),path,'instructions')
 intent_path=H/'intent.json'
 if not intent_path.exists():
  basis=db.basis();ids=[[kw('activity/id'),uuid.UUID(aid)],[kw('tutorial/id'),uuid.UUID(tid)]]
  rows=db.query('[:find ?a (pull ?e [*]) :in $ [[?a ?id]] :where [?e ?a ?id]]',[ids],H,'before',basis);assert len(rows)==2
  byattr={str(a):r for a,r in rows};ar=byattr[':activity/id'];tr=byattr[':tutorial/id'];assert ar[':activity/title']=='MTH 341 — Mini Exam 2 Review'
  learner=db.query('[:find (pull ?l [:db/id [:learner/assignments :limit nil] [:learner/targets :limit nil]]) :in $ ?id :where [?l :learner/id ?id]]',[audit['learner_uuid']],H,'learner-before',basis)[0][0]
  forms=[]
  olddue=ar.get(':activity/due');oldinst={'$inst':olddue}if olddue else None
  if olddue!=due:forms.append([':db/cas',ar[':db/id'],':activity/due',oldinst,{'$inst':due}])
  if tr[':tutorial/content']!=intro:forms.append([':db/cas',tr[':db/id'],':tutorial/content',tr[':tutorial/content'],intro])
  assert forms,'Deadline already matches; no transaction needed.'
  text='[\n'+'\n'.join(edn(f)for f in forms)+'\n]\n';(H/'transaction.edn').write_text(text);sha=hashlib.sha256(text.encode()).hexdigest()
  save('before.json',{'activity':ar,'tutorial':tr,'learner':learner})
  intent={'source':audit['source'],'request_key':'f26-341-sg2-due-20261030-'+sha[:24]+'-b'+str(basis),'sha256':sha,'database':'math','basis':basis,'endpoint':'/tmp/edb-math/writer.sock','activity_uuid':aid,'tutorial_uuid':tid,'due':due,'metadata':intro};save('intent.json',intent)
 else:intent=json.loads(intent_path.read_text())
 payload=H/'transaction.edn';assert hashlib.sha256(payload.read_bytes()).hexdigest()==intent['sha256']
 receipt_path=H/'receipt.edn';receipt=loads(receipt_path.read_text())if receipt_path.exists()and receipt_path.stat().st_size else None
 if not receipt or not receipt.get(':edb/committed'):
  preview=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(payload)],env=db.env,text=True,capture_output=True,check=True);(H/'preview.log').write_text(preview.stdout)
  command=[db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--endpoint',intent['endpoint'],'--file',str(payload),'--request-key',intent['request_key'],'--timeout-ms','120000']
  with receipt_path.open('w')as out,(H/'submit.stderr').open('w')as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,check=True,timeout=160)
  receipt=loads(receipt_path.read_text())
 assert receipt[':edb/committed'];basis=receipt[':edb/db-after-t'];before=json.loads((H/'before.json').read_text());ids=[[kw('activity/id'),uuid.UUID(aid)],[kw('tutorial/id'),uuid.UUID(tid)]]
 rows=db.query('[:find ?a (pull ?e [*]) :in $ [[?a ?id]] :where [?e ?a ?id]]',[ids],H,'after',basis);byattr={str(a):r for a,r in rows};ar=byattr[':activity/id'];tr=byattr[':tutorial/id'];assert datetime.fromisoformat(ar[':activity/due'].replace('Z','+00:00'))==datetime.fromisoformat(due.replace('Z','+00:00'));assert tr[':tutorial/content']==intro
 def plain(v):return json.loads(json.dumps(v,default=str))
 ar=plain(ar);tr=plain(tr);ar.pop(':activity/due');old=before['activity'];old.pop(':activity/due',None);assert ar==old
 tr.pop(':tutorial/content');old=before['tutorial'];old.pop(':tutorial/content');assert tr==old
 learner=db.query('[:find (pull ?l [:db/id [:learner/assignments :limit nil] [:learner/targets :limit nil]]) :in $ ?id :where [?l :learner/id ?id]]',[audit['learner_uuid']],H,'learner-after',basis)[0][0];assert plain(learner)==before['learner']
 attrs=db.query('[:find ?e ?i :in $ [?i ...] :where [?e :db/ident ?i]]',[[kw('activity/due'),kw('tutorial/content'),kw('db/txInstant')]],H,'allowed-attributes',basis);allowed={str(i):e for e,i in attrs};assert all(d[1]in allowed.values()for d in receipt[':edb/tx-data'])
 report={'committed':True,'basis_t':basis,'due_date':'2026-10-30','due_utc':due,'date_only_convention':'23:59:59 America/Los_Angeles','activity_identity_preserved':True,'questions_answers_and_history_unchanged':True,'learner_targets_and_assignments_unchanged':True,'new_note':str(path)};save('verification.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
