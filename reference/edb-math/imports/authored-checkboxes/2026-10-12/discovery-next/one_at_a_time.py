"""Fresh capture, native preview, exact commit and verification for each batch independently."""
import hashlib,json,re,shutil,subprocess
from pathlib import Path
from types import SimpleNamespace
import prepare as migration
import commit as durable
edb=migration.edb
OUT=migration.OUT
read=lambda p:json.loads(p.read_text())
save=lambda p,d:edb.atomic_json(p,d)

def helper():
 from capture.scripts.database.preview import _library
 library=_library(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math')));source=OUT/'batch-preview.rs';binary=OUT/'batch-preview'
 paths=[source,library,migration.ROOT/'engine/edb/answer_fields.rs',migration.ROOT/'engine/edb/configuration.rs',migration.ROOT/'engine/edb/progress.rs'];hashes={str(p):migration.digest(p)for p in paths}
 command=['rustc','--edition=2024','-O',str(source),'--extern','edb_core='+str(library),'-L','dependency='+str(library.parent),'-o',str(binary)];subprocess.run(command,check=True)
 assert hashes=={str(p):migration.digest(p)for p in paths};save(OUT/'batch-preview-build.json',{'inputs':hashes,'command':command,'binary_sha256':migration.digest(binary)})
 return binary

def archive(directory):
 assert not (directory/'commit-intent.json').exists()and not (directory/'commit.edn').exists()
 if not (directory/'prepared-request.json').exists():return
 request=read(directory/'prepared-request.json');target=directory/'superseded-preparations'/request['request_key']
 if not target.exists():shutil.copytree(directory,target,ignore=shutil.ignore_patterns('superseded-preparations'))
 save(target/'superseded.json',{'state':'unsubmitted_superseded','reason':'Refresh this batch independently at a newly held native database value','basis':request['basis'],'database_writes':0})

def capture(ids,directory,basis,lineage):
 edb.OUT=directory
 status=edb.DB.command('status');assert 'lineage='+lineage in status
 questions=edb.batches('[:find (pull ?q '+edb.QUESTION+') :in $ [?q ...] :where [?q :question/id _]]',sorted(ids),'questions',basis,96)
 assert {q[':db/id']for q, in questions}==set(ids)
 items=edb.batches('[:find ?q (pull ?item '+edb.ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]',sorted(ids),'items',basis,128)
 answers=sorted({a[':db/id']for q, in questions for f in q[':question/answer-fields']for a in f[':answer-field/choices']});fields=sorted({f[':db/id']for q, in questions for f in q[':question/answer-fields']})
 users=edb.batches('[:find ?a (pull ?item '+edb.ITEM+') :in $ [?a ...] :where [?item :task-item/responses ?a]]',answers,'response-users',basis,256)
 owned_fields=edb.batches('[:find ?f (pull ?f [{[:question/_answer-fields :limit nil] [:db/id]}]) :in $ [?f ...] :where [?f :answer-field/id _]]',fields,'field-owners',basis,128)
 owned_answers=edb.batches('[:find ?a (pull ?a [{[:answer-field/_choices :limit nil] [:db/id]}]) :in $ [?a ...] :where [?a :answer/id _]]',answers,'answer-owners',basis,128)
 refs=lambda v:[v]if isinstance(v,dict)else v
 source=edb.read('[:find (pull ?s [:db/id :db/ident :db/doc]) :in $ ?ident :where [?s :db/ident ?ident]]',[edb.kw(edb.SOURCE)],'source',basis);assert len(source)==1
 snapshot={'basis':basis,'lineage':lineage,'questions':questions,'items':items,'response_users':users,'field_owners':[[f,q[':db/id']]for f,data in owned_fields for q in refs(data.get(':question/_answer-fields',[]))],'answer_owners':[[a,f[':db/id']]for a,data in owned_answers for f in refs(data.get(':answer-field/_choices',[]))],'attributes':edb.DB.attributes(directory/'evidence',basis),'source':source}
 (directory/'snapshot.edn').write_text(edb.dumps(snapshot)+'\n');save(directory/'capture.json',{'basis':basis,'lineage':lineage,'questions':len(ids),'presentations':len(items),'response_links':len(users),'source':edb.SOURCE,'snapshot_sha256':migration.digest(directory/'snapshot.edn'),'database_writes':0})
 return snapshot

def preview_group(binary,directory,prepare):
 process=subprocess.Popen([str(binary),str(directory),edb.SOURCE],env=edb.DB.env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 try:
  line=process.stdout.readline();assert line.startswith('CAPTURED_BASIS '),line;basis=int(line.split()[1])
  snapshot=prepare(basis)
  stdout,stderr=process.communicate('PREVIEW\n',timeout=180);assert process.returncode==0,stderr
  (directory/'preview.log').write_text(line+stdout);assert stdout.splitlines()==['PREVIEWED_BATCH']
  solutions=directory.name=='optional-solution-repairs'
  migration.verify_report(directory,edb.loads((directory/'preview.edn').read_text()),snapshot,solution_repairs=solutions)
  return snapshot
 finally:
  if process.poll()is None:process.kill();process.wait()

def reconcile_format(row,q,baseline,basis):
 old_problem=row.get('source_problem',row.get('problem_before',row.get('problem')));problem=q[':question/problem'];old_solution=baseline['worked_solution'];solution=q[':question/worked-solution']
 if problem==old_problem and solution==old_solution:return
 def normalized(s):
  s=re.sub(r'(?m)^(?:-\s+|(?:VIII|VII|VI|IV|V|III|II|I)\.\s+)', '',s)
  return re.sub(r'\s+','',s.replace('\\{','{').replace('\\}','}'))
 assert normalized(problem)==normalized(old_problem)and normalized(solution)==normalized(old_solution),('Substantive fresh source change requires review',row['id'])
 assert row['atomic_options'],'Only reviewed finite selectable objects can be reconciled'
 listed=dict(re.findall(r'(?m)^(VIII|VII|VI|IV|V|III|II|I)\. (.+)$',problem))
 assert set(listed)=={a['label']for a in row['atomic_options']}
 prompt=row['proposed_prompt']
 for atom in row['atomic_options']:
  before=atom['text'];after=listed[atom['label']]
  assert normalized(before)==normalized(after)and prompt.count(before)==1
  prompt=prompt.replace(before,after);atom['text']=after
 row['source_problem']=problem;row['proposed_prompt']=prompt
 proof='Fresh changes are limited to ordered list labels, whitespace and escaped literal TeX set/cases braces. Statement order, all mathematical symbols, every selectable predicate and the existing key remain unchanged. Preserve the corrected rendering and current worked solution.'
 row['fresh_source_reconciliation']={'basis':basis,'proof':proof,'preserve_current_solution':True}
 path=OUT/'fresh-source-overlays.json';data=read(path)if path.exists()else{'questions':[]}
 data['questions']=[r for r in data['questions']if r['id']!=row['id']]+[{'id':row['id'],'ma_id':row['ma_id'],'captured_basis':basis,':question/problem':{'before':old_problem,'after':problem},':question/worked-solution':{'before':old_solution,'after':solution},'problem_after':prompt,'atomic_options':row['atomic_options'],'proof':proof,'key_changes':False,'decision':'preserve_concurrent_source_correction_and_convert'}];save(path,data)
 ledger=read(OUT/'resolutions.json')
 for i,r in enumerate(ledger['questions']):
  if r['id']==row['id']:ledger['questions'][i]=row;break
 save(OUT/'resolutions.json',ledger)
 print(json.dumps({'fresh_source_format_reconciled':row['ma_id'],'key_changed':False,'basis':basis}),flush=True)

def prepare_conversions(directory,basis,scope,rows,number,lineage):
 archive(directory);snapshot=capture(scope,directory,basis,lineage)
 baseline=read(OUT/'superseded-preparations/basis-1694'/directory.name/'plan.json');base={q['id']:q for q in baseline['questions']}
 existing={q['id']:q for q in read(OUT/'fresh-source-overlays.json')['questions']}if (OUT/'fresh-source-overlays.json').exists()else{}
 for q, in snapshot['questions']:
  original=base[q[':db/id']]
  if q[':db/id']in existing:original={**original,'worked_solution':existing[q[':db/id']][':question/worked-solution']['after']}
  reconcile_format(rows[q[':db/id']],q,original,basis)
 batch_plan=migration.build(selected_ids=set(scope),snapshot=snapshot,review_rows=rows,batch_number_start=number,write_root=False)
 assert len(batch_plan['batches'])==1 and batch_plan['counts']['questions']==len(scope)
 current=read(directory/'plan.json')
 overlays={q['id']:q for q in read(OUT/'fresh-source-overlays.json')['questions']}if (OUT/'fresh-source-overlays.json').exists()else{}
 for q in current['questions']:
  expected=base[q['id']]
  if q['id']in overlays:
   overlay=overlays[q['id']]
   expected={**expected,'problem_before':overlay[':question/problem']['after'],'problem_after':overlay['problem_after'],'atomic_options':overlay['atomic_options'],'worked_solution':overlay[':question/worked-solution']['after']}
  for key in ('id','ma_id','labels','correct','atomic_options','old_field','new_field_tempids','problem_before','problem_after','choice_mapping'):
   assert q[key]==expected[key],('Approved response semantics changed',q['id'],key)
  assert q['worked_solution']==expected['worked_solution'],'Worked solution changed; inspect before preparing corrections'
 return snapshot

def prepare_solutions(directory,basis,approved,lineage):
 archive(directory);snapshot=capture({q['id']for q in approved['questions']},directory,basis,lineage);current={q[':db/id']:q for q, in snapshot['questions']};forms=[]
 for q in approved['questions']:
  assert current[q['id']][':question/worked-solution']==q['solution_before'],'Solution changed; do not replace newer content blindly'
  forms.extend([[edb.kw('db/cas'),q['id'],edb.kw('question/worked-solution'),q['solution_before'],q['solution_after']],{edb.kw('db/id'):q['id'],edb.kw('db/ensure'):edb.kw('question/validate')}])
 path=directory/'transaction.edn';path.write_text('[\n'+'\n'.join(' '+edb.dumps(f)for f in forms)+'\n]\n');sha=migration.digest(path)
 manifest={**approved,'state':'prepared_not_submitted','basis':basis,'captured_basis':basis,'transaction_sha256':sha,'requires_all_conversion_batches_first':True};save(directory/'plan.json',manifest)
 request={'state':'prepared_not_submitted','database':'math','endpoint':edb.DB.args.endpoint,'lineage':lineage,'source':edb.SOURCE,'basis':basis,'must_use_basis_guard':True,'request_key':f'discovery-next-solution-repairs-v1-{basis}-{sha}','sha256':sha,'transaction_file':str(path),'requires_all_conversion_batches_first':True};save(directory/'prepared-request.json',request)
 assert sha==approved['transaction_sha256']
 return snapshot

def run():
 plan=read(OUT/'plan.json');assert plan['counts']['questions']==1695 and plan['counts']['batches']==9 and plan['source']==edb.SOURCE
 for row in plan['review_files']:assert migration.digest(Path(row['path']))==row['sha256']
 fixture=read(OUT/'engine-fixture-verification.json');assert fixture['passed']and migration.digest(OUT/'engine-input.json')==fixture['engine_input_sha256']and migration.digest(OUT/'engine-report.json')==fixture['engine_report_sha256']
 rows={q['id']:q for q in read(OUT/'resolutions.json')['questions']};scopes={b['number']:[q['id']for q in read(Path(b['directory'])/'plan.json')['questions']]for b in plan['batches']}
 assert len(set(q for scope in scopes.values()for q in scope))==1695 and all(17592186329885 not in scope for scope in scopes.values())
 approved=read(OUT/'superseded-preparations/basis-1694/optional-solution-repairs/plan.json');assert approved['counts']['questions']==14
 binary=helper();receipts=[];execution={'state':'submission_authorized','cohort_plan_sha256':migration.digest(OUT/'plan.json'),'source':edb.SOURCE,'question_ids':sorted(q for scope in scopes.values()for q in scope),'mode':'fresh_capture_preview_commit_one_batch_at_a_time','include_solution_corrections':True}
 intent=OUT/'execution-intent.json'
 if intent.exists():assert read(intent)==execution
 else:save(intent,execution)
 for b in plan['batches']:
  number=b['number'];directory=Path(b['directory']);edb.OUT=directory
  for attempt in range(5):
   try:
    if (directory/'commit-intent.json').exists()or (directory/'commit.edn').exists():
     snapshot=edb.loads((directory/'snapshot.edn').read_text())
    else:
     snapshot=preview_group(binary,directory,lambda basis:prepare_conversions(directory,basis,scopes[number],rows,number,plan['lineage']))
    edb.DB.args.capture_only=False
    receipt=durable.submit(directory,snapshot,number=number);break
   except Exception as error:
    from database import StaleBasis
    if not isinstance(error,StaleBasis):raise
    print(json.dumps({'batch':number,'confirmed_stale_rejection':True,'refreshing_uncommitted_batch':True}),flush=True)
    if attempt==4:raise
   finally:edb.DB.args.capture_only=True
  receipts.append(receipt);durable.progress(plan,receipts)
  save(OUT/'execution-progress.json',{'mode':execution['mode'],'committed_batches':receipts,'questions_committed':sum(r['counts']['questions']for r in receipts),'next_batch':number+1 if number<9 else'solution-corrections'})
 edb.OUT=OUT;summary={'committed':True,'basis_before':receipts[0]['basis_before'],'basis_after_conversions':receipts[-1]['basis_after'],'basis_after':receipts[-1]['basis_after'],'source':edb.SOURCE,'counts':plan['counts'],'batches':receipts,'mode':execution['mode']};save(OUT/'commit-receipt.json',summary)
 directory=OUT/'optional-solution-repairs'
 for attempt in range(5):
  try:
   if (directory/'commit-intent.json').exists()or (directory/'commit.edn').exists():snapshot=edb.loads((directory/'snapshot.edn').read_text())
   else:snapshot=preview_group(binary,directory,lambda basis:prepare_solutions(directory,basis,approved,plan['lineage']))
   edb.DB.args.capture_only=False
   solution_receipt=durable.submit(directory,snapshot,number='solution-corrections',solutions=True);break
  except Exception as error:
   from database import StaleBasis
   if not isinstance(error,StaleBasis):raise
   print(json.dumps({'solution_corrections_confirmed_stale_rejection':True,'refreshing_uncommitted_batch':True}),flush=True)
   if attempt==4:raise
  finally:edb.DB.args.capture_only=True
 summary['basis_after']=solution_receipt['basis_after'];summary['solution_corrections']=solution_receipt;save(OUT/'commit-receipt.json',summary);durable.progress(plan,receipts,solution_receipt=solution_receipt)
 print(json.dumps({'all_prepared_transactions_committed':True,'basis_before':summary['basis_before'],'basis_after':summary['basis_after'],'conversion_batches':9,'questions':1695,'solution_corrections':14,'mode':execution['mode']}),flush=True)

if __name__=='__main__':run()
