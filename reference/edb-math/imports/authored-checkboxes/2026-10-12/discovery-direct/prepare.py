"""Capture, prepare, and noncommitting-preview reviewed checkbox conversions."""
import argparse,collections,hashlib,importlib.util,json,re,subprocess,threading
from pathlib import Path
from types import SimpleNamespace
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'Cargo.toml').exists())
AUDIT=ROOT/'generate/reports/checkbox-discovery-2026-10-12/direct-candidates.json'
spec=importlib.util.spec_from_file_location('previous_checkbox',OUT.parent/'finder-easy/prepare.py');edb=importlib.util.module_from_spec(spec);spec.loader.exec_module(edb)
edb.OUT=OUT
SOURCE=edb.SOURCE
BATCH_SIZE=195

def assert_no_submissions():
 retained=[OUT/name for name in ('commit-intent.json','commit.edn','commit-receipt.json')]
 for pattern in ('batch-*/commit-intent.json','batch-*/commit.edn','batch-*/commit-receipt.json'):
  retained.extend(OUT.glob(pattern))
 assert not any(path.exists()for path in retained), 'Retain and resolve submitted requests before rebuilding a preparation'

def capture(held_basis=None):
 assert_no_submissions()
 audit=json.loads(AUDIT.read_text());ids=sorted(q['id']for q in audit['questions']);assert len(ids)==780
 status=edb.DB.command('status');basis=int(re.search(r'\bbasis_t=(\d+)',status)[1])
 if held_basis is not None:
  assert basis>=held_basis
  basis=held_basis
 assert 'lineage='+json.loads((AUDIT.parent/'inventory.json').read_text())['lineage']in status
 questions=edb.batches('[:find (pull ?q '+edb.QUESTION+') :in $ [?q ...] :where [?q :question/id _]]',ids,'questions',basis,128)
 assert {r[0][':db/id']for r in questions}==set(ids)
 items=edb.batches('[:find ?q (pull ?item '+edb.ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]',ids,'items',basis,len(ids))
 answers=sorted({a[':db/id']for r in questions for f in r[0].get(':question/answer-fields',[])for a in f.get(':answer-field/choices',[])})
 users=edb.batches('[:find ?answer (pull ?item '+edb.ITEM+') :in $ [?answer ...] :where [?item :task-item/responses ?answer]]',answers,'response-users',basis,len(answers))
 attrs=edb.DB.attributes(OUT/'evidence',basis)
 source=edb.read('[:find (pull ?s [:db/id :db/ident :db/doc]) :in $ ?ident :where [?s :db/ident ?ident]]',[edb.kw(SOURCE)],'source',basis)
 assert len(source)==1 and source[0][0][':db/ident']==SOURCE
 # Guard against an upsert accidentally changing a prior authored entity.
 fids=[];aids=[]
 for q in audit['questions']:
  for atom in q['atomic_options']:
   token=q['ma_id']+'/authored-checkbox-v1/'+atom['label']
   fids.append(edb.stable_id('field',token))
   aids.extend(edb.stable_id('answer',token+'/'+v)for v in ('false','true'))
 assert len(set(fids))==len(fids)and len(set(aids))==len(aids)
 existing=[]
 for attr,ids_to_check in [('answer-field/id',fids),('answer/id',aids)]:
  existing.extend(edb.batches('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',ids_to_check,'identity-'+attr.split('/')[0],basis,len(ids_to_check)))
 assert not existing, 'Proposed identities already exist; review rather than upsert'
 (OUT/'snapshot.edn').write_text(edb.dumps({'basis':basis,'status':status,'questions':questions,'items':items,'response_users':users,'attributes':attrs,'source':source})+'\n')
 edb.save('capture.json',{'basis':basis,'status':status.strip(),'audit_basis':audit['basis'],'audit_sha256':hashlib.sha256(AUDIT.read_bytes()).hexdigest(),'questions':len(ids),'presentations':len(items),'response_links':len(users),'source':SOURCE,'identity_collisions':0})
 print(json.dumps({'captured':True,'basis':basis,'questions':len(ids),'presentations':len(items),'response_links':len(users)}),flush=True)

CASE=re.compile(r'(?m)^([ \t]*)(?:-\s+|(?:IV|III|II|I)[.)]\s+)([^\n]+)$')
def mathematical_text(problem):
 return re.sub(r'\s+',' ',CASE.sub(lambda m:m[1]+m[2],problem)).strip()
def reviewed_problem(row):
 repairs=json.loads((OUT/'accepted-render-repairs.json').read_text())if (OUT/'accepted-render-repairs.json').exists()else {}
 repair=repairs.get(str(row['id']),{}).get('changes',{}).get('problem')
 if repair:
  assert row['problem']==repair['before']
  return repair['after']
 # These two current source repairs escape the outer set braces for rendering.
 # They were inspected explicitly; this is not a general math-normalization rule.
 problem=row['problem']
 if row['id']in (17592186278573,17592186278580):
  assert problem.count('A={(x,y)')==1 and problem.count('}.\n$$')==1
  problem=problem.replace('A={(x,y)',r'A=\{(x,y)').replace('}.\n$$',r'\}.'+'\n$$')
 return problem
def reviewed_solution(row):
 repairs=json.loads((OUT/'accepted-render-repairs.json').read_text())if (OUT/'accepted-render-repairs.json').exists()else {}
 repair=repairs.get(str(row['id']),{}).get('changes',{}).get('solution')
 if repair:
  assert row['worked_solution']==repair['before']
  return repair['after']
 return row['worked_solution']
def prompt_after(q,row):
 original=q[':question/problem'];labels=[x['label']for x in row['atomic_options']]
 assert 'Select all that apply.'not in original
 matches=list(CASE.finditer(original));assert len(matches)==len(labels),('List layout requires review',q[':db/id'])
 assert labels==list(edb.ROMAN[:len(matches)])
 iterator=iter(labels)
 changed=CASE.sub(lambda m:m[1]+'- **'+next(iterator)+'.** '+m[2],original)
 start=changed.index('- **'+labels[0]+'.** ')
 changed=changed[:start].rstrip()+'\n\nSelect all that apply.\n\n'+changed[start:]
 # Replacing just list-marker prefixes preserves multiline math after the list.
 bare=lambda p:re.sub(r'\s+',' ',CASE.sub(lambda m:m[1]+m[2],re.sub(r'(?m)^([ \t]*)- \*\*(?:IV|III|II|I)\.\*\* ',r'\1',p.replace('Select all that apply.','')))).strip()
 assert bare(changed)==bare(original)
 return labels,changed

def prepare():
 assert_no_submissions()
 snapshot=edb.loads((OUT/'snapshot.edn').read_text());audit=json.loads(AUDIT.read_text());basis=snapshot['basis']
 assert hashlib.sha256(AUDIT.read_bytes()).hexdigest()==json.loads((OUT/'capture.json').read_text())['audit_sha256']
 qs={r[0][':db/id']:r[0]for r in snapshot['questions']};items=collections.defaultdict(dict);incoming=collections.defaultdict(dict)
 for qid,item in snapshot['items']:items[qid][item[':db/id']]=item
 for aid,item in snapshot['response_users']:incoming[aid][item[':db/id']]=item
 groups=[];all_responses=[];retained=set()
 for row in sorted(audit['questions'],key=lambda x:x['id']):
  q=qs[row['id']];qid=q[':db/id'];fs=q[':question/answer-fields'];assert len(fs)==1
  f=fs[0];assert f[':answer-field/type'][':db/ident']==':answer-field.type/radio'
  assert mathematical_text(q[':question/problem'])==mathematical_text(reviewed_problem(row)),('Mathematical content changed',qid)
  assert q[':question/worked-solution']==reviewed_solution(row)
  assert q[':question/difficulty'][':db/ident']==row['difficulty'] and not q.get(':knowledge-point/_canonical-example')
  assert {k[':db/id']for k in q[':knowledge-point/_questions']}=={k['id']for k in row['kps']}
  assert f[':db/id']==row['fields'][0][':db/id']
  assert set(f)<=set((':db/id',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct')),('Extra field metadata needs review',qid)
  bank={a[':db/id']:a for a in f[':answer-field/choices']};key=edb.subset(f[':answer-field/correct'][':answer/value'])
  assert key==set(row['correct_labels']) and f[':answer-field/correct']==bank[f[':answer-field/correct'][':db/id']]
  assert {(a[':db/id'],a[':answer/value'])for a in bank.values()}=={(a[':db/id'],a[':answer/value'])for a in row['fields'][0][':answer-field/choices']}
  labels,prompt=prompt_after(q,row)
  mappings={}
  for aid,a in bank.items():
   assert a[':answer/type'][':db/ident']==':answer.type/text' and not a.get(':answer/feedback')
   mappings[aid]=edb.subset(a[':answer/value']);assert mappings[aid]<=set(labels)
  responses=[]
  for itemid,item in sorted(items[qid].items()):
   old=[a[':db/id']for a in item.get(':task-item/responses',[])]
   if not old:continue
   assert len(old)==1 and old[0]in bank,('Saved response needs review',qid,itemid)
   assert incoming[old[0]][itemid]==item
   selected=mappings[old[0]];status=item.get(':task-item/status',{}).get(':db/ident')
   if status in (':task-item.status/correct',':task-item.status/incorrect'):
    assert (selected==key)==(status==':task-item.status/correct'),('Saved grading needs review',qid,itemid)
   responses.append({'item':itemid,'question':qid,'old_answer':old[0],'old_value':bank[old[0]][':answer/value'],'selected':[l for l in labels if l in selected],'status':status})
  forms=[];links=[];targets={}
  for label in labels:
   token=q[':question/math-academy-id']+'/authored-checkbox-v1/'+label;fid='field-'+token;aids=[]
   for value in ('false','true'):
    aid='answer-'+token+'/'+value
    forms.append({edb.kw('db/id'):aid,edb.kw('answer/id'):edb.stable_id('answer',token+'/'+value),edb.kw('answer/type'):edb.kw('answer.type/text'),edb.kw('answer/value'):value,edb.kw('db/ensure'):edb.kw('answer/validate')})
    aids.append(aid);targets[(label,value)]=aid
   forms.append({edb.kw('db/id'):fid,edb.kw('answer-field/id'):edb.stable_id('field',token),edb.kw('answer-field/key'):label,edb.kw('answer-field/type'):edb.kw('answer-field.type/checkbox'),edb.kw('answer-field/choices'):aids,edb.kw('answer-field/correct'):aids[int(label in key)],edb.kw('db/ensure'):edb.kw('answer-field/validate')})
   links.append(fid)
  forms.extend([[edb.kw('db/retract'),qid,edb.kw('question/answer-fields'),f[':db/id']],[edb.kw('db/cas'),qid,edb.kw('question/problem'),q[':question/problem'],prompt],{edb.kw('db/id'):qid,edb.kw('question/answer-fields'):links,edb.kw('db/ensure'):edb.kw('question/validate')}])
  for response in responses:
   answer_ids=[targets[(l,str(l in response['selected']).lower())]for l in labels]
   forms.extend([[edb.kw('db/retract'),response['item'],edb.kw('task-item/responses'),response['old_answer']],{edb.kw('db/id'):response['item'],edb.kw('task-item/responses'):answer_ids,edb.kw('db/ensure'):edb.kw('task-item/validate')}]);response['new_answer_tempids']=answer_ids
  old_ids={f[':db/id'],*bank};retained.update(old_ids);all_responses.extend(responses)
  change={'id':qid,'ma_id':row['ma_id'],'kps':row['kps'],'labels':labels,'correct':[l for l in labels if l in key],'old_field':f[':db/id'],'new_field_tempids':links,'problem_before':q[':question/problem'],'problem_after':prompt,'choice_mapping':[{'old_answer':aid,'old_value':a[':answer/value'],'selected':[l for l in labels if l in mappings[aid]],'new_answer_tempids':[targets[(l,str(l in mappings[aid]).lower())]for l in labels]}for aid,a in sorted(bank.items())]}
  groups.append((forms,change,responses,old_ids))
 batches=[]
 for number,start in enumerate(range(0,len(groups),BATCH_SIZE),1):
  directory=OUT/f'batch-{number:02d}';directory.mkdir(exist_ok=True);part=groups[start:start+BATCH_SIZE]
  forms=[f for forms,_,_,_ in part for f in forms];changes=[q for _,q,_,_ in part];responses=[r for _,_,rs,_ in part for r in rs]
  path=directory/'transaction.edn';path.write_text('[\n'+'\n'.join(' '+edb.dumps(f)for f in forms)+'\n]\n');digest=hashlib.sha256(path.read_bytes()).hexdigest()
  counts={'questions':len(changes),'knowledge_points':len({k['id']for q in changes for k in q['kps']}),'new_checkbox_fields':sum(len(q['labels'])for q in changes),'new_boolean_answers':2*sum(len(q['labels'])for q in changes),'saved_responses_mapped':len(responses),'presentations':sum(len(items[q['id']])for q in changes)}
  manifest={'basis':basis+number-1,'captured_basis':basis,'source':SOURCE,'transaction_sha256':digest,'counts':counts,'questions':changes,'responses':responses,'retained_original_entities':sorted(set().union(*(old for _,_,_,old in part)))}
  (directory/'plan.json').write_text(json.dumps(manifest,indent=2)+'\n')
  request={'state':'prepared_not_submitted','database':'math','endpoint':edb.DB.args.endpoint,'source':SOURCE,'sha256':digest,'request_key':f'discovery-direct-checkbox-v1-{basis}-{number}-{digest}','basis':basis+number-1,'preview_basis':basis,'transaction_file':str(path),'must_use_basis_guard':True,'previous_batch_required':number-1 if number>1 else None,'lineage':json.loads((AUDIT.parent/'inventory.json').read_text())['lineage']}
  (directory/'prepared-request.json').write_text(json.dumps(request,indent=2)+'\n');batches.append({'number':number,'directory':str(directory),**counts,'basis_guard':request['basis'],'request_key':request['request_key'],'sha256':digest})
 plan={'state':'prepared_not_submitted','basis':basis,'source':SOURCE,'counts':{'questions':len(groups),'knowledge_points':len({k['id']for _,q,_,_ in groups for k in q['kps']}),'batches':len(batches),'new_checkbox_fields':sum(b['new_checkbox_fields']for b in batches),'new_boolean_answers':sum(b['new_boolean_answers']for b in batches),'saved_responses_mapped':len(all_responses),'presentations':sum(len(v)for v in items.values())},'batches':batches,'notes':['Each transaction is atomic; the four transactions are not one atomic database commit.','Apply in order with the retained source, request key, exact EDN bytes, and chained basis guards. Confirm each receipt before the next batch.','If the basis changes unexpectedly before any submission, recapture and revalidate unsubmitted work. Never rebuild an unknown-outcome request.','Boolean fields and answers are owned per question; the original radio field and answer entities remain unchanged.','Database answer subsets, worked solutions, difficulty, KP/topic links, and learner grading/progress are preserved.','Prompts gain bold Roman labels and Select all that apply.; all mathematical text is retained.']}
 edb.save('plan.json',plan);print(json.dumps({'prepared':True,'basis':basis,**plan['counts']}),flush=True)

def held_executable():
 from capture.scripts.database.preview import _library
 library=_library(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math')))
 source=OUT/'held-preview.rs';binary=OUT/'held-preview'
 paths=[source,library,ROOT/'engine/edb/answer_fields.rs',ROOT/'engine/edb/configuration.rs',ROOT/'engine/edb/progress.rs']
 inputs={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}
 command=['rustc','--edition=2024','-O',str(source),'--extern','edb_core='+str(library),'-L','dependency='+str(library.parent),'-o',str(binary)]
 subprocess.run(command,check=True)
 assert inputs=={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}
 edb.save('held-preview-build.json',{'inputs':inputs,'command':command,'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'database_writes':0,'capability':'Captures one database value, waits for local preparation, applies four speculative with_forms calls; has no durable submission path.'})
 return binary

def preview(refresh=False):
 helper=held_executable()
 process=subprocess.Popen([str(helper),str(OUT),SOURCE],env=edb.DB.env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 try:
  line=process.stdout.readline();match=re.fullmatch(r'CAPTURED_BASIS (\d+)\n',line)
  assert match,('Could not capture native preview basis',line)
  held_basis=int(match[1])
  if refresh:capture(held_basis);prepare()
  plan=json.loads((OUT/'plan.json').read_text());snapshot=edb.loads((OUT/'snapshot.edn').read_text())
  assert held_basis==plan['basis'],'Recapture with the all action to preview one held database value'
  for batch in plan['batches']:
   directory=Path(batch['directory']);assert hashlib.sha256((directory/'transaction.edn').read_bytes()).hexdigest()==batch['sha256']
  stdout,stderr=process.communicate('PREVIEW\n',timeout=120)
  assert process.returncode==0,stderr
  (OUT/'held-preview.log').write_text(line+stdout)
  assert stdout.splitlines()==[f'PREVIEWED_BATCH {i}'for i in range(1,5)]
  reports=[];original_read=edb.read
  # Native sequential preview bases after the first are speculative. Resolve
  # the existing enum dictionary from the one captured durable basis.
  edb.read=lambda query,inputs,name,basis:original_read(query,inputs,name,held_basis)
  try:
   for batch in plan['batches']:
    directory=Path(batch['directory']);edb.OUT=directory
    (directory/'snapshot.edn').write_text(edb.dumps(snapshot)+'\n')
    edb.verify_preview(edb.loads((directory/'preview.edn').read_text()));reports.append(json.loads((directory/'preview.json').read_text()))
  finally:edb.read=original_read;edb.OUT=OUT
  observed_basis=edb.DB.basis()
  edb.save('preview.json',{'passed':True,'committed':False,'speculative':True,'basis':plan['basis'],'source':SOURCE,'counts':plan['counts'],'batches':reports,'method':'Four sequential native speculative transactions on one held immutable database value; each successor becomes the next db-before.','observed_live_basis_after_preview':observed_basis,'refresh_required_before_submission':observed_basis!=plan['basis'],'database_writes':0})
  print(json.dumps({'all_previews_passed':True,'basis':held_basis,'observed_live_basis':observed_basis,**plan['counts']}),flush=True)
 finally:
  if process.poll()is None:process.kill();process.wait()

def all():preview(refresh=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['capture','prepare','preview','all']);globals()[parser.parse_args().action]()
