"""Install retirement metadata and publish the complete guarded KP repair."""
import copy,uuid
from read import *
from scripts.generator_packages import build_manifest,manifest_digest,publish_package,verify_package,materialize_package
SOURCE=':agent/codex'
BASE_IDENTS=dict(json.loads((ROOT/'reference/mathacademy/repairs/2026-10-18-equation-chains/idents.json').read_text()));NAMES={v:k for k,v in BASE_IDENTS.items()}
KP_PATTERN='[* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION+'} {[:knowledge-point/questions :limit nil] '+QUESTION+'}]'

def canonical(x):
 if isinstance(x,dict):return {str(k):canonical(v)for k,v in x.items()}
 if isinstance(x,(tuple,list)):return sorted([canonical(v)for v in x],key=lambda v:json.dumps(v,sort_keys=True))
 return str(x)if isinstance(x,uuid.UUID)else x

def same(a,b):return canonical(a)==canonical(b)

def submit(directory,request):
 tx=directory/'transaction.edn';assert sha(tx)==request['sha256'];receipt=directory/'receipt.edn'
 if receipt.exists():report=loads(receipt.read_text());assert report[':edb/committed']is True;return report
 assert DB.status()['lineage']==request['lineage']
 text=DB.command('transact','--file',tx,'--endpoint',request['endpoint'],'--request-key',request['request_key'],'--basis',request['basis'],'--source',SOURCE,'--timeout-ms','180000',timeout=210);receipt.write_text(text);report=loads(text);assert report[':edb/committed'];(directory/'commit-confirmation.json').write_text(json.dumps({'committed':True,'basis_before':report[':edb/db-before-t'],'basis_after':report[':edb/db-after-t'],'request_key':request['request_key']},indent=2)+'\n');return report

def schema():
 directory=HERE/'schema';directory.mkdir(exist_ok=True);request_path=directory/'request.json'
 if not request_path.exists():
  identity=DB.status();existing=DB.query('[:find (pull ?e [*]) :in $ ?ident :where [?e :db/ident ?ident]]',[kw('question/retired')],directory,'existing',identity['basis'])
  if existing:
   a=existing[0][0];assert a[':db/valueType']==kw('db.type/boolean')and a[':db/cardinality']==kw('db.cardinality/one');return
  text='\n'.join(l for l in (ROOT/'schema/content/4-question.edn').read_text().splitlines()if not l.lstrip().startswith(';'));definition=next(row for row in loads(text)if row.get(kw('db/ident'))==kw('question/retired'));tx=directory/'transaction.edn';tx.write_text(dumps([definition])+'\n');preview=DB.command('with','--file',tx,'--source',SOURCE);(directory/'preview.edn').write_text(preview);report=loads(preview);assert report[':edb/db-before-t']==identity['basis']and report[':edb/committed']is False
  for e,a,v,t,source,added in report[':edb/tx-data']:assert source==NAMES[SOURCE]and added
  request={**identity,'source':SOURCE,'endpoint':str(DB.config.endpoint),'sha256':sha(tx),'request_key':'question-retirement-schema-v1-'+sha(tx)};request_path.write_text(json.dumps(request,indent=2)+'\n')
 request=json.loads(request_path.read_text());report=submit(directory,request);after=DB.query('[:find (pull ?e [*]) :in $ ?ident :where [?e :db/ident ?ident]]',[kw('question/retired')],directory,'after',report[':edb/db-after-t']);assert len(after)==1;save('retirement-attribute.json',after[0][0]);print(json.dumps({'schema_committed':True,'basis':report[':edb/db-after-t']}),flush=True)

def question_forms(record):
 q=record['question'];temp='question-'+q[':question/id'];forms=[];fields=[]
 for f in q[':question/answer-fields']:
  ft='field-'+f[':answer-field/id'];fields.append(ft);choices=[]
  for a in f[':answer-field/choices']:
   at='answer-'+a[':answer/id'];choices.append(at);forms.append({kw('db/id'):at,kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
  forms.append({kw('db/id'):ft,kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):choices,kw('answer-field/correct'):'answer-'+f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
 forms.append({kw('db/id'):temp,kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):fields,kw('db/ensure'):kw('question/validate')});forms.append([kw('db/add'),KP,kw('knowledge-point/questions'),temp]);return forms

def prepare():
 directory=HERE/'content';directory.mkdir(exist_ok=True);assert not(directory/'request.json').exists(),'Reconcile saved request before preparing again'
 for f in ('quality-verification.json','algebra-verification.json','ui-verification.json'):assert json.loads((HERE/f).read_text())['passed']
 identity=DB.status();assert identity['lineage']==json.loads((HERE/'identity.json').read_text())['lineage']
 before=native(directory/'before',identity['basis'],[('kp',KP_PATTERN,[KP])]);kp=before['kp'][0];initial=json.loads((HERE/'kp.json').read_text());assert same(kp,initial),'Current KP changed; audit additional or altered content before submitting'
 old=kp[':knowledge-point/question-generator'];replacements=json.loads((HERE/'replacements.json').read_text());ledger=json.loads((HERE/'audit-ledger.json').read_text());withdraw=[r['id']for r in ledger if r['decision']=='withdraw_and_replace'];changes=json.loads((HERE/'solution-updates.json').read_text());qids=[q[':db/id']for q in kp[':knowledge-point/questions']]
 items=DB.query('[:find ?q (pull ?i '+ITEM+') :in $ [?q ...] :where [?i :task-item/content ?q]]',[qids],directory,'items-before',identity['basis']);save('items-at-preparation.json',items)
 for kind,values in [('question',[r['question'][':question/id']for r in replacements]),('answer-field',[f[':answer-field/id']for r in replacements for f in r['question'][':question/answer-fields']]),('answer',[a[':answer/id']for r in replacements for f in r['question'][':question/answer-fields']for a in f[':answer-field/choices']])]:
  found=DB.query(f'[:find ?e :in $ [?id ...] :where [?e :{kind}/id ?id]]',[[uuid.UUID(x)for x in values]],directory,kind+'-identities',identity['basis']);assert not found
 m=json.loads((HERE/'original/generator-package.json').read_text());files=list(m['files'])+['scope-contract.json'];manifest=build_manifest(HERE/'package',m['entrypoint'],files,dependencies=m['dependencies']);digest=manifest_digest(manifest);package=publish_package(HERE/'package',m['entrypoint'],files,Path(DB.config.math_root),dependencies=m['dependencies'],expected_digest=digest);guid=uuid.uuid5(uuid.UUID(str(kp[':knowledge-point/id'])),'generator-package:'+digest)
 forms=[{kw('db/id'):'new-generator',kw('question-generator/id'):guid,kw('question-generator/script'):package.reference},[kw('db/cas'),KP,kw('knowledge-point/question-generator'),old[':db/id'],'new-generator'],[kw('db/cas'),old[':db/id'],kw('question-generator/script'),old[':question-generator/script'],old[':question-generator/script']]]
 for r in replacements:forms+=question_forms(r)
 for qid in withdraw:forms.append([kw('db/cas'),qid,kw('question/retired'),None,True])
 for c in changes:forms.extend([[kw('db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']],[kw('db/ensure'),c['entity'],kw('question/validate')]])
 forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')]);tx=directory/'transaction.edn';tx.write_text(dumps(forms)+'\n')
 plan={'basis':identity['basis'],'lineage':identity['lineage'],'old_generator':old,'generator_uuid':str(guid),'generator_reference':package.reference,'generator_digest':digest,'withdrawn':withdraw,'replacements':replacements,'solution_changes':changes,'before':before,'items_before':items};save('content/plan.json',plan)
 # Native preview plus actual proposed db_after Pull through the retained helper.
 groups=[('kp',KP_PATTERN,[KP]),('items',ITEM,sorted({i[':db/id']for q,i in items})),('old-generator','[*]',[old[':db/id']])];(directory/'native-pulls.edn').write_text(dumps(groups)+'\n');binary=ROOT/'reference/mathacademy/repairs/2026-10-20-explicit-none/native-preview';p=subprocess.run([str(binary),str(directory),SOURCE],input='PREVIEW\n',env=DB.environment,capture_output=True,text=True,timeout=180);(directory/'preview.stdout').write_text(p.stdout);(directory/'preview.stderr').write_text(p.stderr);p.check_returncode();report=loads((directory/'preview.edn').read_text());assert report[':edb/db-before-t']==identity['basis'],'Database advanced; refresh unsubmitted preparation'
 proposed={n:loads((directory/'speculative'/(n+'.edn')).read_text())for n,_,_ in groups};check_state(plan,proposed,report);check_datoms(plan,report,False);save('content/proposed.json',proposed)
 request={**identity,'source':SOURCE,'endpoint':str(DB.config.endpoint),'sha256':sha(tx),'request_key':'sum-rule-radio-marker-v1-'+str(identity['basis'])+'-'+sha(tx),'plan_sha256':sha(directory/'plan.json'),'quality_sha256':sha(HERE/'quality-verification.json')};save('content/request.json',request);print(json.dumps({'preview_passed':True,'basis':identity['basis'],'withdrawn':len(withdraw),'replacements':len(replacements),'clarified_solutions':len(changes)}),flush=True)

def check_state(plan,state,report):
 kp=state['kp'][0];expected=copy.deepcopy(plan['before']['kp'][0]);oldq={q[':db/id']:q for q in expected[':knowledge-point/questions']};newq={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert set(newq)==set(oldq)|{report[':edb/tempids']['question-'+r['question'][':question/id']]for r in plan['replacements']}
 changes={c['entity']:c for c in plan['solution_changes']}
 for eid,q in oldq.items():
  wanted=copy.deepcopy(q)
  if eid in plan['withdrawn']:wanted[':question/retired']=True
  if eid in changes:wanted[changes[eid]['attribute']]=changes[eid]['after']
  assert same(wanted,newq[eid]),('Existing question changed unexpectedly',eid)
 for r in plan['replacements']:
  source=r['question'];q=newq[report[':edb/tempids']['question-'+source[':question/id']]]
  assert str(q[':question/id'])==source[':question/id']and q[':question/problem']==source[':question/problem']and q[':question/worked-solution']==source[':question/worked-solution']and q[':question/difficulty'][':db/ident']==source[':question/difficulty']
  f=q[':question/answer-fields'][0];sf=source[':question/answer-fields'][0];assert str(f[':answer-field/id'])==sf[':answer-field/id'];assert {str(a[':answer/id']):a[':answer/value']for a in f[':answer-field/choices']}=={a[':answer/id']:a[':answer/value']for a in sf[':answer-field/choices']};assert str(f[':answer-field/correct'][':answer/id'])==sf[':answer-field/correct'][1]
 assert same(expected[':knowledge-point/canonical-example'],kp[':knowledge-point/canonical-example'])
 assert same({k:v for k,v in expected.items()if k not in (':knowledge-point/questions',':knowledge-point/question-generator')},{k:v for k,v in kp.items()if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==plan['generator_uuid']and gen[':question-generator/script']==plan['generator_reference']
 assert same([i for q,i in plan['items_before']],state['items']);assert same(state['old-generator'][0],plan['old_generator'])

def check_datoms(plan,report,committed):
 assert report[':edb/committed']is committed and report[':edb/db-before-t']==plan['basis'];retired_id=json.loads((HERE/'retirement-attribute.json').read_text())[':db/id'];idents={**BASE_IDENTS,retired_id:':question/retired'};expected=set();guards=set();ids=report[':edb/tempids'];newg=ids['new-generator'];old=plan['old_generator'];expected.update({(newg,':question-generator/id',uuid.UUID(plan['generator_uuid']),True),(newg,':question-generator/script',plan['generator_reference'],True),(KP,':knowledge-point/question-generator',old[':db/id'],False),(KP,':knowledge-point/question-generator',newg,True)});guards.add((old[':db/id'],':question-generator/script',old[':question-generator/script'],True))
 for r in plan['replacements']:
  q=r['question'];qid=ids['question-'+q[':question/id']];expected.add((KP,':knowledge-point/questions',qid,True))
  for a in ('question/id','question/problem','question/worked-solution','question/difficulty'):
   v=q[':'+a];v=uuid.UUID(v)if a.endswith('/id')else NAMES[v]if a=='question/difficulty'else v;expected.add((qid,':'+a,v,True))
  for f in q[':question/answer-fields']:
   fid=ids['field-'+f[':answer-field/id']];expected.update({(qid,':question/answer-fields',fid,True),(fid,':answer-field/id',uuid.UUID(f[':answer-field/id']),True),(fid,':answer-field/key',f[':answer-field/key'],True),(fid,':answer-field/type',NAMES[f[':answer-field/type']],True),(fid,':answer-field/correct',ids['answer-'+f[':answer-field/correct'][1]],True)})
   for a in f[':answer-field/choices']:
    aid=ids['answer-'+a[':answer/id']];expected.update({(fid,':answer-field/choices',aid,True),(aid,':answer/id',uuid.UUID(a[':answer/id']),True),(aid,':answer/type',NAMES[a[':answer/type']],True),(aid,':answer/value',a[':answer/value'],True)})
 for eid in plan['withdrawn']:expected.add((eid,':question/retired',True,True))
 for c in plan['solution_changes']:expected.update({(c['entity'],c['attribute'],c['before'],False),(c['entity'],c['attribute'],c['after'],True)})
 actual=set();times=0
 for e,a,v,t,source,added in report[':edb/tx-data']:
  assert source==NAMES[SOURCE]
  if idents[a]==':db/txInstant':assert added;times+=1
  else:actual.add((e,idents[a],v,added))
 assert times==1 and expected<=actual and actual-expected<=guards,(actual-expected-guards,expected-actual)

def commit():
 directory=HERE/'content';request=json.loads((directory/'request.json').read_text());assert sha(directory/'plan.json')==request['plan_sha256']and sha(HERE/'quality-verification.json')==request['quality_sha256'];plan=json.loads((directory/'plan.json').read_text());report=submit(directory,request);check_datoms(plan,report,True);groups=loads((directory/'native-pulls.edn').read_text());after=native(directory/'committed',report[':edb/db-after-t'],groups);check_state(plan,after,report);save('content/committed.json',after);historical=native(directory/'historical',plan['basis'],groups);assert same(historical['kp'],plan['before']['kp']);assert same(historical['items'],[i for q,i in plan['items_before']]);verify_package(Path(DB.config.math_root)/Path(plan['generator_reference']).parent,plan['generator_digest'])
 result={'passed':True,'committed':True,'basis_before':plan['basis'],'basis_after':report[':edb/db-after-t'],'fixed_questions':[c['entity']for c in plan['solution_changes']],'generator_reference':plan['generator_reference'],'existing_fields_answers_keys_solutions_unchanged':True,'math_academy_sources_unchanged':True,'blank_placeholders_preserved':True,'learner_items_unchanged':len(plan['items_before']),'historical_snapshot_reproduced':True};save('verification.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':{'schema':schema,'prepare':prepare,'commit':commit}[sys.argv[1]]()
