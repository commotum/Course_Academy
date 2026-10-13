"""Prepare reviewed next-tier migrations and native previews; no durable submit command."""
import argparse,collections,hashlib,importlib.util,json,shutil,subprocess
from pathlib import Path
from types import SimpleNamespace
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'Cargo.toml').exists())
spec=importlib.util.spec_from_file_location('checkbox_reference',OUT.parent/'finder-easy/prepare.py')
edb=importlib.util.module_from_spec(spec);spec.loader.exec_module(edb);edb.OUT=OUT
edb.DB.args.capture_only=True
BATCH_SIZE=195

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def no_submissions():
 assert not list(OUT.glob('batch-*/commit*'))and not (OUT/'commit-intent.json').exists(),'Recover retained submitted requests; do not rebuild them'

def archive_unsubmitted(plan):
 no_submissions()
 directory=OUT/'superseded-preparations'/('basis-'+str(plan['basis']))
 if directory.exists():return
 directory.parent.mkdir(exist_ok=True)
 shutil.copytree(OUT,directory,ignore=shutil.ignore_patterns('superseded-preparations','__pycache__','held-preview','solution-preview','check-checkbox-engine'))
 (directory/'superseded.json').write_text(json.dumps({'state':'unsubmitted_superseded','basis':plan['basis'],'reason':'A new held native value has a later basis; fresh capture and guards are required.','database_writes':0},indent=2)+'\n')

def reviews():
 rows={};paths=[]
 for name in ('held-statements.json','text-cases.json','image-cases.json','held-exceptions.json'):
  path=OUT/'reviews'/name
  if not path.exists():continue
  paths.append({'path':str(path),'sha256':digest(path)})
  for row in json.loads(path.read_text())['questions']:
   if row['id']in rows:
    assert name=='held-exceptions.json','Overlapping primary review ownership'
   rows[row['id']]=row
 for name,key in (('independent-semantic-audit.json','overlays'),('semantic-qualifications.json','questions')):
  path=OUT/'reviews'/name
  assert path.exists(),('Semantic review missing',name)
  paths.append({'path':str(path),'sha256':digest(path)})
  for overlay in json.loads(path.read_text())[key]:
   before=rows[overlay['id']]
   assert set(overlay['correct_labels'])==set(before['correct_labels'])
   if name=='semantic-qualifications.json':
    rows[overlay['id']]={**before,'source_problem':overlay['current_prompt'],'proposed_prompt':overlay['proposed_prompt'],'semantic_clarification':overlay,'required_prompt_clarification':True}
   else:
    repair=overlay.get('prompt_repair')or {}
    necessary=overlay.get('necessary_prompt_clarification',False)and repair.get('before')!=repair.get('after')
    rows[overlay['id']]={**before,**overlay,'required_prompt_clarification':necessary}
 expected={q['id']for q in json.loads((OUT/'audit-input.json').read_text())}
 assert set(rows)==expected,('Incomplete case ledger',len(rows),len(expected),sorted(expected-set(rows)))
 edb.save('resolutions.json',{'basis':json.loads((OUT/'capture.json').read_text())['basis'],'database_writes':0,'review_files':paths,'questions':[rows[i]for i in sorted(rows)]})
 return rows,paths

def build(*,selected_ids=None,snapshot=None,review_rows=None,batch_number_start=1,write_root=True):
 if write_root:no_submissions()
 if review_rows is None:rows,review_files=reviews()
 else:rows=review_rows;review_files=json.loads((OUT/'plan.json').read_text())['review_files']
 snapshot=edb.loads((OUT/'snapshot.edn').read_text())if snapshot is None else snapshot;basis=snapshot['basis']
 qs={q[':db/id']:q for q, in snapshot['questions']};audit={q['id']:q for q in json.loads((OUT/'audit-input.json').read_text())}
 owners=collections.defaultdict(set);answer_owners=collections.defaultdict(set)
 for fid,qid in snapshot['field_owners']:owners[fid].add(qid)
 for aid,fid in snapshot['answer_owners']:answer_owners[aid].add(fid)
 items=collections.defaultdict(dict);incoming=collections.defaultdict(dict)
 for qid,item in snapshot['items']:items[qid][item[':db/id']]=item
 for aid,item in snapshot['response_users']:incoming[aid][item[':db/id']]=item
 groups=[];fids=[];aids=[];retained=set();repairs=[];decisions=collections.Counter();clarifications=[]
 for qid,row in sorted(rows.items()):
  if selected_ids is not None and qid not in selected_ids:continue
  decisions[row['decision']]+=1
  q=qs[qid]
  if row.get('required_prompt_clarification'):
   clarifications.append({'id':qid,'ma_id':row['ma_id'],'problem_before':q[':question/problem'],'problem_after':row['proposed_prompt'],'rationale':row.get('semantic_clarification',{}).get('rationale',row.get('reason'))})
  for repair in row.get('content_repairs',[]):
   repairs.append({'id':qid,'ma_id':row['ma_id'],'issue':repair,'problem':q[':question/problem'],'solution_before':q.get(':question/worked-solution'),'solution_after':row.get('proposed_worked_solution'),'included_in_checkbox_transaction':False})
  if row['decision']!='convert':continue
  original=row.get('source_problem',row.get('problem_before',row.get('problem')))
  assert original==q[':question/problem'],('Source changed; re-review',qid)
  assert q[':question/math-academy-id']==row['ma_id']
  fs=q[':question/answer-fields'];assert len(fs)==1
  f=fs[0];fid=f[':db/id'];assert f[':answer-field/type'][':db/ident']==':answer-field.type/radio'
  assert owners[fid]=={qid},('Shared field',qid,fid)
  assert not q.get(':knowledge-point/_canonical-example'),('Canonical overlap needs scope review',qid)
  assert q.get(':question/difficulty')and q.get(':question/worked-solution')
  assert set(f)<=set((':db/id',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct'))
  bank={a[':db/id']:a for a in f[':answer-field/choices']}
  assert len(bank)==len(f[':answer-field/choices'])
  assert f[':answer-field/correct']==bank[f[':answer-field/correct'][':db/id']]
  assert all(answer_owners[a]=={fid}for a in bank),('Shared answer',qid)
  assert all(a[':answer/type'][':db/ident']==':answer.type/text'and set(a)<=set((':db/id',':answer/id',':answer/type',':answer/value'))for a in bank.values())
  atoms=row['atomic_options'];labels=[a['label']for a in atoms];universe=set(labels)
  assert 2<=len(labels)<=12 and len(universe)==len(labels)and all(isinstance(l,str)and l for l in labels)
  mappings={a['answer_eid']:set(a['labels'])for a in row['choice_mapping']}
  assert set(mappings)==set(bank)and len(row['choice_mapping'])==len(bank)
  assert all(set(a['labels'])<=universe and len(a['labels'])==len(set(a['labels']))and a['value']==bank[a['answer_eid']][':answer/value']for a in row['choice_mapping'])
  key=set(row['correct_labels']);assert key==mappings[f[':answer-field/correct'][':db/id']]
  assert all(a['truth']==(a['label']in key)for a in atoms)
  # An old incorrect choice must not become identical to the canonical subset.
  assert all((aid==f[':answer-field/correct'][':db/id'])==(selected==key)for aid,selected in mappings.items()),('Duplicate correct semantics need review',qid)
  prompt=row['proposed_prompt'];assert prompt.count('Select all that apply.')==1
  forms=[];links=[];targets={};responses=[]
  for label in labels:
   token=row['ma_id']+'/authored-checkbox-v1/'+label;field='field-'+token;owned=[];field_uuid=edb.stable_id('field',token);fids.append(field_uuid)
   for value in ('false','true'):
    answer='answer-'+token+'/'+value;answer_uuid=edb.stable_id('answer',token+'/'+value);aids.append(answer_uuid)
    forms.append({edb.kw('db/id'):answer,edb.kw('answer/id'):answer_uuid,edb.kw('answer/type'):edb.kw('answer.type/text'),edb.kw('answer/value'):value,edb.kw('db/ensure'):edb.kw('answer/validate')});owned.append(answer);targets[(label,value)]=answer
   forms.append({edb.kw('db/id'):field,edb.kw('answer-field/id'):field_uuid,edb.kw('answer-field/key'):label,edb.kw('answer-field/type'):edb.kw('answer-field.type/checkbox'),edb.kw('answer-field/choices'):owned,edb.kw('answer-field/correct'):owned[int(label in key)],edb.kw('db/ensure'):edb.kw('answer-field/validate')});links.append(field)
  forms.append([edb.kw('db/retract'),qid,edb.kw('question/answer-fields'),fid])
  if prompt!=q[':question/problem']:forms.append([edb.kw('db/cas'),qid,edb.kw('question/problem'),q[':question/problem'],prompt])
  forms.append({edb.kw('db/id'):qid,edb.kw('question/answer-fields'):links,edb.kw('db/ensure'):edb.kw('question/validate')})
  for itemid,item in sorted(items[qid].items()):
   old=[a[':db/id']for a in item.get(':task-item/responses',[])]
   if not old:continue
   assert len(old)==1 and old[0]in bank,('Malformed response',qid,itemid)
   assert incoming[old[0]][itemid]==item
   selected=mappings[old[0]];status=item.get(':task-item/status',{}).get(':db/ident')
   if status in (':task-item.status/correct',':task-item.status/incorrect'):assert (selected==key)==(status==':task-item.status/correct')
   values=[targets[(l,str(l in selected).lower())]for l in labels]
   forms.extend([[edb.kw('db/retract'),itemid,edb.kw('task-item/responses'),old[0]],{edb.kw('db/id'):itemid,edb.kw('task-item/responses'):values,edb.kw('db/ensure'):edb.kw('task-item/validate')}])
   responses.append({'item':itemid,'question':qid,'old_answer':old[0],'selected':[l for l in labels if l in selected],'status':status,'new_answer_tempids':values})
  assert all(item[':db/id']in items[qid]for aid in bank for item in incoming[aid].values()),('Answer used outside scoped question',qid)
  assert {k[':db/id']for k in q[':knowledge-point/_questions']}=={k['id']for k in audit[qid]['kps']},('KP membership changed',qid)
  change={'id':qid,'ma_id':row['ma_id'],'kps':audit[qid]['kps'],'classification':row['classification'],'labels':labels,'correct':[l for l in labels if l in key],'atomic_options':atoms,'old_field':fid,'new_field_tempids':links,'problem_before':q[':question/problem'],'problem_after':prompt,'required_prompt_clarification':row.get('required_prompt_clarification',False),'worked_solution':q[':question/worked-solution'],'difficulty':q[':question/difficulty'][':db/ident'],'choice_mapping':[{'old_answer':aid,'old_value':bank[aid][':answer/value'],'selected':[l for l in labels if l in selected],'new_answer_tempids':[targets[(l,str(l in selected).lower())]for l in labels]}for aid,selected in mappings.items()]}
  old={fid,*bank};retained.update(old);groups.append((forms,change,responses,old))
 assert len(set(fids))==len(fids)and len(set(aids))==len(aids)
 collisions=[]
 for attr,ids in (('answer-field/id',fids),('answer/id',aids)):
  if ids:collisions+=edb.batches('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',ids,'identity-'+attr.split('/')[0],basis,256)
 assert not collisions,'Prospective identities exist; reconcile instead of upsert'
 edb.save('identity-check.json',{'basis':basis,'field_uuids':len(fids),'answer_uuids':len(aids),'collisions':collisions})
 batches=[]
 for number,start in enumerate(range(0,len(groups),BATCH_SIZE),batch_number_start):
  part=groups[start:start+BATCH_SIZE];directory=OUT/f'batch-{number:02d}';directory.mkdir(exist_ok=True)
  assert not (directory/'commit-intent.json').exists()and not (directory/'commit.edn').exists(),'Never rebuild an unresolved or committed batch'
  forms=[form for fs,_,_,_ in part for form in fs];changes=[q for _,q,_,_ in part];responses=[r for _,_,rs,_ in part for r in rs]
  path=directory/'transaction.edn';path.write_text('[\n'+'\n'.join(' '+edb.dumps(form)for form in forms)+'\n]\n');sha=digest(path)
  counts={'questions':len(changes),'knowledge_points':len({k['id']for q in changes for k in q['kps']}),'new_checkbox_fields':sum(len(q['labels'])for q in changes),'new_boolean_answers':2*sum(len(q['labels'])for q in changes),'saved_responses_mapped':len(responses),'presentations':sum(len(items[q['id']])for q in changes)}
  manifest={'basis':basis+number-batch_number_start,'captured_basis':basis,'source':edb.SOURCE,'transaction_sha256':sha,'counts':counts,'questions':changes,'responses':responses,'retained_original_entities':sorted(set().union(*(old for _,_,_,old in part)))}
  (directory/'plan.json').write_text(json.dumps(manifest,indent=2)+'\n')
  request={'state':'prepared_not_submitted','database':'math','endpoint':edb.DB.args.endpoint,'lineage':snapshot['lineage'],'basis':basis+number-batch_number_start,'source':edb.SOURCE,'sha256':sha,'request_key':f'discovery-next-checkbox-v1-{basis}-{number}-{sha}','transaction_file':str(path),'must_use_basis_guard':True,'previous_batch_required':number-1 if number>1 else None}
  (directory/'prepared-request.json').write_text(json.dumps(request,indent=2)+'\n');batches.append({'number':number,'directory':str(directory),'basis_guard':request['basis'],'request_key':request['request_key'],'sha256':sha,'bytes':path.stat().st_size,'forms':len(forms),**counts})
 plan={'state':'prepared_not_submitted','basis':basis,'lineage':snapshot['lineage'],'source':edb.SOURCE,'database_writes':0,'review_files':review_files,'snapshot_sha256':digest(OUT/'snapshot.edn'),'decisions':dict(decisions),'counts':{'reviewed_questions':len(rows),'questions':len(groups),'knowledge_points':len({k['id']for _,q,_,_ in groups for k in q['kps']}),'batches':len(batches),'new_checkbox_fields':len(fids),'new_boolean_answers':len(aids),'saved_responses_mapped':sum(b['saved_responses_mapped']for b in batches),'necessary_prompt_clarifications':len(clarifications)},'batches':batches,'retained_original_entities':len(retained),'solution_repairs_included':False,'prompt_clarifications':clarifications,'verification_limit':'Keys and learner semantics preserved; mathematical verification varies by reviewed class and is recorded per question. Eight necessary prompt clarifications make source intent explicit. Separate solution repairs are proposed, not silently included.'}
 if write_root:
  edb.save('proposed-content-repairs.json',{'database_writes':0,'included_in_checkbox_transactions':False,'issues':repairs});edb.save('plan.json',plan);edb.save('status.json',plan)
 print(json.dumps({'prepared':True,'basis':basis,'decisions':dict(decisions),**plan['counts']}),flush=True)
 return plan

def verify_report(directory,report,snapshot,*,committed=False,solution_repairs=False):
 manifest=json.loads((directory/'plan.json').read_text());assert report[':edb/committed']is committed
 assert report.get(':edb/speculative',False)is (not committed)
 assert report[':edb/db-before-t']==manifest['basis']and report[':edb/db-after-t']==manifest['basis']+1
 assert digest(directory/'transaction.edn')==manifest['transaction_sha256']
 ids=report[':edb/tempids'];assert len(set(ids.values()))==manifest['counts']['new_checkbox_fields']*3
 assert set(ids.values()).isdisjoint(manifest['retained_original_entities'])
 names=dict(snapshot['attributes']);source_id=snapshot['source'][0][0][':db/id']
 enums={str(ident):eid for eid,ident in edb.read('[:find ?e ?ident :in $ [?ident ...] :where [?e :db/ident ?ident]]',[[edb.kw('answer-field.type/checkbox'),edb.kw('answer.type/text')]],'preview-enums',snapshot['basis'])}
 def value(v):
  if isinstance(v,edb.kw('x').__class__):return enums[str(v)]
  if isinstance(v,str)and v in ids:return ids[v]
  return v
 additions=set();retractions=set()
 for form in edb.loads((directory/'transaction.edn').read_text()):
  if isinstance(form,dict):
   eid=value(form[':db/id'])
   for attribute,contents in form.items():
    if attribute in (':db/id',':db/ensure'):continue
    for v in contents if isinstance(contents,list)else [contents]:additions.add((eid,str(attribute),value(v)))
  elif form[0]==':db/retract':retractions.add((form[1],str(form[2]),value(form[3])))
  elif form[0]==':db/cas':
   additions.add((form[1],str(form[2]),value(form[4])));retractions.add((form[1],str(form[2]),value(form[3])))
  else:raise AssertionError(('Unexpected form',form))
 actual_additions=set();actual_retractions=set();instants=0
 for eid,attr,v,tx,source,added in report[':edb/tx-data']:
  assert source==source_id
  name=str(names[attr])
  if name==':db/txInstant':assert added;instants+=1;continue
  (actual_additions if added else actual_retractions).add((eid,name,v))
 assert instants==1 and actual_additions==additions and actual_retractions==retractions,'Datom scope differs from logical forms'
 result={'passed':True,'committed':committed,'speculative':not committed,'basis':manifest['basis'],'basis_after':report[':edb/db-after-t'],'source':edb.SOURCE,'sha256':manifest['transaction_sha256'],'datoms':len(report[':edb/tx-data']),'counts':manifest['counts'],'checks':['Application-native validators passed','Exact logical-form assertions/retractions and all source datoms checked','Only reviewed worked solutions and transaction instant changed; keys, fields, prompts, ratings, memberships and learner state unchanged'if solution_repairs else'No original fields/answers, solution, rating, memberships, grading/progress or unrelated facts changed']}
 (directory/('commit-validation.json'if committed else'preview.json')).write_text(json.dumps(result,indent=2)+'\n');return result

def helper():
 from capture.scripts.database.preview import _library
 library=_library(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math')));source=OUT/'held-preview.rs';binary=OUT/'held-preview'
 paths=[source,library,ROOT/'engine/edb/answer_fields.rs',ROOT/'engine/edb/configuration.rs',ROOT/'engine/edb/progress.rs'];hashes={str(p):digest(p)for p in paths}
 command=['rustc','--edition=2024','-O',str(source),'--extern','edb_core='+str(library),'-L','dependency='+str(library.parent),'-o',str(binary)];subprocess.run(command,check=True)
 assert hashes=={str(p):digest(p)for p in paths}
 edb.save('held-preview-build.json',{'inputs':hashes,'command':command,'binary_sha256':digest(binary),'database_writes':0});return binary

def preview():
 no_submissions();plan=json.loads((OUT/'plan.json').read_text());binary=helper()
 process=subprocess.Popen([str(binary),str(OUT),edb.SOURCE,str(len(plan['batches']))],env=edb.DB.env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 try:
  line=process.stdout.readline();assert line.startswith('CAPTURED_BASIS '),line;basis=int(line.split()[1])
  if basis!=plan['basis']:
   archive_unsubmitted(plan)
   subprocess.run([sys.executable,str(OUT/'read_capture.py'),'--basis',str(basis)],check=True);build();plan=json.loads((OUT/'plan.json').read_text())
  assert basis==plan['basis']
  stdout,stderr=process.communicate('PREVIEW\n',timeout=600);assert process.returncode==0,stderr
  (OUT/'held-preview.log').write_text(line+stdout);assert stdout.splitlines()==[f'PREVIEWED_BATCH {b["number"]}'for b in plan['batches']]
  snapshot=edb.loads((OUT/'snapshot.edn').read_text());reports=[]
  for batch in plan['batches']:
   directory=Path(batch['directory']);reports.append(verify_report(directory,edb.loads((directory/'preview.edn').read_text()),snapshot))
  result={'passed':True,'committed':False,'speculative':True,'captured_basis':basis,'predicted_final_basis':basis+len(reports),'source':edb.SOURCE,'database_writes':0,'batches':reports,'counts':plan['counts']};edb.save('preview.json',result)
  status={**plan,'state':'prepared_previewed_not_submitted','preview':str(OUT/'preview.json')};edb.save('status.json',status)
  print(json.dumps({'preview_passed':True,'basis':basis,'batches':len(reports),**plan['counts']}),flush=True)
 finally:
  if process.poll()is None:process.kill();process.wait()

if __name__=='__main__':
 import sys
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['build','preview']);globals()[parser.parse_args().action]()
