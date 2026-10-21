from pathlib import Path
from copy import deepcopy
import threading,json,math
from scripts.config import Config
from scripts.storage import read_json,atomic_json,file_lock
from scripts.database.pipeline import DatabasePipeline,jsonable
from scripts.database.commit import Committer
from scripts.database.prepare import digest
from scripts.database.evidence import authoritative_question
from scripts.activity.capture import ActivityCapture
root=Path('reference/mathacademy/repairs/2026-10-20-final-save/partials')
inventory=read_json(root/'inventory.json')
values={'q-96847':'0.0361','q-130050':'0.1404','q-130048':'0.0521','q-67410':'-2','q-67405':'-3','q-67406':'10','q-106324':'3','q-106322':r'\frac{1}{2}','q-67421':'1','q-67424':'-3','q-67441':r'-\frac{4}{3}'}
assert [round(math.exp(-lam)*lam**k/math.factorial(k),4) for lam,k in [(2,5),(5,3),(7,3)]]==[.0361,.1404,.0521]
quotes={'q-96847':'& ≈0.0361.','q-130050':'& ≈0.1404.','q-130048':'& ≈0.0521.',
'q-67410':'x & =-2','q-67405':'x & =-3','q-67406':'$x=10.$','q-106324':'x & =3','q-106322':r'$x=\frac{1}{2}.$','q-67421':'$x=1.$','q-67424':'x & =-3','q-67441':r'$x=-\frac{4}{3}.$'}
content={'kind':'catalog','questions':[],'canonical_examples':[],'partial_catalog_only':True,'source_checkpoints':[]}
unsupported=[]
a=ActivityCapture.__new__(ActivityCapture)
for row in inventory['records']:
 q=deepcopy(row['question']);mid=q['math_academy_id']
 if not row['existing']:
  if mid not in values:
   unsupported.append({'question_id':mid,'task_id':row['task_id'],'reason':'Unanswered at manual stop; no original worked solution or confirmed source key. Original prompt and controls retained in checkpoint.'});continue
  assert quotes[mid] in q['worked_solution'],mid
  fields=q.get('answer_fields',q.get('fields',[]));assert len(fields)==1
  f=fields[0];matches=[c for c in f['choices']if c['value']==values[mid]];assert len(matches)==1
  source=q.get('solution_evidence')or row['record'].get('feedback',{}).get('html_path')or q['html_path'];assert Path(source).is_file()
  f.update(correct_value=values[mid],correct_type=matches[0]['type'],evidence={'kind':'worked_solution','value':values[mid],'source_file':source,'solution_quote':quotes[mid],'matches_worked_solution':True})
  q['answer_fields']=fields;q=authoritative_question(q)
 a.activity={'kind':'lesson'};a._normalize_kp(q,example=row.get('example',False))
 content['canonical_examples'if row.get('example')else'questions'].append(q)
content['source_checkpoints']=sorted({str(Path('reference/mathacademy/capture')/r['account']/r['task_id']/'checkpoint.json')for r in inventory['records']})
atomic_json(root/'catalog-content.json',content);atomic_json(root/'retained-unanswered.json',unsupported)
atomic_json(root/'source-judgments.json',{'judgments':[{ 'question_id':k,'value':v,'MA_quote':quotes[k],'basis':'source worked solution; independently checked algebra or Poisson PMF'}for k,v in values.items()],'activity_completion_claim':False})
c=Config();pipeline=DatabasePipeline(c,threading.Event());folder=root/'database'
with file_lock(c.database_lock):
 committer=Committer(c,pipeline.client,folder);request=committer.pending()
 if request is None:
  prepared,snapshot=pipeline._prepare(content,folder,pipeline.client.basis())
  atomic_json(root/'preparation.json',jsonable(prepared))
  assert not prepared['omissions'],prepared['omissions']
  assert len(prepared['batches'])<=1
  if not prepared['batches']:
   atomic_json(root/'verification.json',{'status':'no_changes','basis':snapshot['basis'],'questions':len(content['questions']),'canonical_examples':len(content['canonical_examples']),'unanswered_retained':unsupported});print('Catalog already saved');raise SystemExit
  batch=prepared['batches'][0]
  assert batch['source']==':org/Math-Academy'
  assert all(not str(a).startswith((':activity/',':step/'))for _,a,_ in batch['assertions']+batch['retractions'])
  committer.preview(batch,snapshot);atomic_json(folder/'request-content.json',content)
  request=committer.save_request(batch,snapshot,digest(content))
 else:assert request['content_sha256']==digest(content)
 receipt=committer.submit(request);verified=pipeline._verify(committer,request,receipt,content,folder)
 assert verified.get('reimport_is_noop')is True,verified
 result={'status':'verified','basis':receipt[':edb/db-after-t'],'new_questions':len(values),'questions_retained_or_saved':len(content['questions']),'canonical_examples_preserved':len(content['canonical_examples']),'receipt':verified,'activity_or_learner_changes':False,'unanswered_retained':unsupported}
 atomic_json(root/'verification.json',result);print(json.dumps(result))
