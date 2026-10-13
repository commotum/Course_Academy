#!/usr/bin/env python3
"""Commit the user-authorized, validated nine-activity import with exact receipts."""
from pathlib import Path
import json,sys,threading,subprocess,hashlib,uuid
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import loads,dumps,kw
from scripts.database.images import ImageLibrary
from scripts.storage import atomic_text,atomic_json,file_lock
out=Path(__file__).resolve().parent;m=json.loads((out/'prepared-manifest.json').read_text());a=json.loads((out/'audit.json').read_text());cfg=Config();c=EDBClient(cfg,threading.Event());commit=out/'commit';commit.mkdir(exist_ok=True)
with file_lock(cfg.database_lock):
 status=c.status();assert status['lineage']==m['lineage']
 journal=commit/'start.json'
 if journal.exists():
  saved=json.loads(journal.read_text());basis=saved['basis']
 else:
  basis=status['basis'];ids=loads((out/'pull-identities.edn').read_text())
  existing=c.query('[:find ?e ?attr ?id :in $ [[?attr ?id]] :where [?e ?attr ?id]]',[ids],commit,'candidate-identities',basis);assert not existing,'Prepared content already exists'
  args=['/tmp/f26-sequential-preview',cfg.database,str(basis),str(commit/'preview')]
  for t in m['transactions']:args += [t['source'],str(out/t['file'])]
  args += ['--repeat-immediate','--pull',str(out/'pull-pattern.edn'),str(out/'pull-identities.edn')]
  r=subprocess.run(args,env=c.environment,text=True,capture_output=True,timeout=60);atomic_text(commit/'preview-output.txt',r.stdout+r.stderr)
  if r.returncode:raise RuntimeError(r.stderr)
  subprocess.run([sys.executable,str(out/'verify.py'),str(commit/'preview')],check=True,stdout=subprocess.DEVNULL)
  atomic_json(journal,{'database':cfg.database,'lineage':status['lineage'],'basis':basis})
 images=ImageLibrary(cfg.math_root,out)
 for source,asset in a['image_map'].items():
  data=(out/'assets'/asset['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256'];assert images.store(data,source)==asset['path']
 atomic_json(commit/'images-installed.json',images.saved)
 attrs=loads((out/'db/attributes.edn').read_text());tx_attr=next(e for e,n,t,card in attrs if n==':db/txInstant')
 def material(report):return {(e,attr,dumps(v),source,added) for e,attr,v,tx,source,added in report[':edb/tx-data'] if attr!=tx_attr}
 summaries=[]
 for i,t in enumerate(m['transactions'],1):
  transaction=(out/t['file']).read_text();assert hashlib.sha256(transaction.encode()).hexdigest()==t['sha256']
  path=commit/f'stage{i}-transaction.edn';request_path=commit/f'stage{i}-request.json';receipt_path=commit/f'stage{i}-commit.edn'
  if request_path.exists():
   request=json.loads(request_path.read_text());assert request['transaction']==transaction and request['source']==t['source'] and request['basis']==basis+i-1
  else:
   atomic_text(path,transaction)
   request={'database':cfg.database,'lineage':status['lineage'],'basis':basis+i-1,'endpoint':cfg.endpoint,'request_key':'mth341-authorized-'+str(uuid.uuid4()),'source':t['source'],'file':str(path),'sha256':t['sha256'],'transaction':transaction}
   atomic_json(request_path,request)
  expected=loads((commit/f'preview/stage{i}-preview.edn').read_text())
  if receipt_path.exists():text=receipt_path.read_text()
  else:
   for attempt in range(3):
    try:
     text=c.command('transact','--file',path,'--endpoint',request['endpoint'],'--request-key',request['request_key'],'--basis',request['basis'],'--source',request['source'],'--timeout-ms',45000,timeout=55);break
    except subprocess.TimeoutExpired:
     if attempt==2:raise
     print('Recovering exact saved request for stage',i,flush=True)
   atomic_text(receipt_path,text)
  report=loads(text);assert report.get(':edb/committed') is True
  assert report[':edb/db-before-t']==request['basis'] and report[':edb/db-after-t']==request['basis']+1
  assert material(report)==material(expected),'Receipt differs from preview'
  summaries.append({'stage':i,'source':request['source'],'basis_before':report[':edb/db-before-t'],'basis_after':report[':edb/db-after-t'],'material_datoms':len(material(report)),'matches_preview':True})
  atomic_json(commit/'progress.json',{'committed_stages':summaries});print('Committed stage',i,'of 3 at basis',report[':edb/db-after-t'],flush=True)
 final=report[':edb/db-after-t'];ids=loads((out/'pull-identities.edn').read_text());pattern=(out/'pull-pattern.edn').read_text().strip()
 rows=c.query('[:find ?attr ?id (pull ?e '+pattern+') :in $ [[?attr ?id]] :where [?e ?attr ?id]]',[ids],commit,'final-entities',final)
 found={(str(attr),str(uid)):row for attr,uid,row in rows}
 atomic_text(commit/'final-pull1.edn',dumps([[identity,found[(str(identity[0]),str(identity[1]))]] for identity in ids])+'\n')
 subprocess.run([sys.executable,str(out/'verify.py'),str(commit)],check=True,stdout=subprocess.DEVNULL)
 q='[:find ?attribute ?value :in $ ?id [?attribute ...] :where [?l :learner/id ?id] [?l ?attribute ?value]]'
 args=[m['learner_id'],[kw('learner/assignments'),kw('learner/targets')]]
 before={tuple(x) for x in c.query(q,args,commit,'learner-before',basis)};after={tuple(x) for x in c.query(q,args,commit,'learner-after',final)}
 assert before<=after
 assert sum(attr==':learner/assignments' for attr,v in after-before)==9
 assert sum(attr==':learner/targets' for attr,v in after-before)==m['new_targets']
 atomic_json(commit/'result.json',{'committed':True,'basis_before':basis,'basis_after':final,'transactions':summaries,'entities_read_back':len(found),'all_content_matches_preview':True,'existing_learner_links_preserved':True,'new_assignments':9,'new_targets':m['new_targets'],'total_assignments':sum(attr==':learner/assignments' for attr,v in after),'self_reports_ungraded':True,'study_direction_preserved':True})
 v=json.loads((commit/'verification.json').read_text());v.update({'committed':True,'basis':final});atomic_json(commit/'verification.json',v)
 print('All nine activities committed and verified at basis',final,flush=True)
