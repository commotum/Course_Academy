"""Independent final current-value checks for all audited lessons; read only."""
import copy,hashlib,json,subprocess,sys
from contextlib import ExitStack
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generator_publish import Publisher,jsonable,content_fingerprint,normalized_question,enum,kw
from generator_pipeline import source_identity
from generator_packages import verify_package
from generator_approval import approved_band
from generator_review import REVIEW_POLICY_VERSION
from capture.scripts.storage import atomic_json,file_lock

def read(p):return json.loads(Path(p).read_text())
def save(p,x):atomic_json(Path(p),jsonable(x))
def canon(v):
 if isinstance(v,dict):return {k:canon(x) for k,x in sorted(v.items())}
 if isinstance(v,list):return sorted([canon(x) for x in v],key=lambda x:json.dumps(x,sort_keys=True))
 return v
A=ROOT/'generate/reports/lesson-quality-audit-2026-11-11';scope=read(A/'coverage-inventory.json');kps=sorted(r['kp'] for r in scope);native_input={};idents={};qids=[];current={};sources={};fresh={kp:set() for kp in kps}
for area in ['normal','vector']:
 report=read(H/area/'final-verification.json');assert report['passed']
 for r in report['results']:fresh[r['kp']].update(r['new_question_ids'])
for r in read(H/'gaussian/publication-results.json')['results']:fresh[r['kp']].update(r['new_question_ids'])
summary=read(A/'summary.json');retired=set(summary['screened_incomplete_imports']+summary['eligible_stored_scaffolding']+summary['eligible_import_prints_answers']+[17592186735423]+[q['entity'] for q in summary['finite_radio_bank_cue']['questions']]);assert len(retired)==20

def visit(v):
 if isinstance(v,list):return [visit(x) for x in v]
 if isinstance(v,dict):
  if ':db/ident' in v and ':db/id' not in v:
   ident=v[':db/ident'].lstrip(':')
   if ident not in idents:idents[ident]=len(idents)+1;native_input[str(idents[ident])]={'db/ident':ident}
   return idents[ident]
  if ':db/id' in v:
   eid=v[':db/id'];native_input.setdefault(str(eid),{}).update({k.lstrip(':'):visit(x) for k,x in v.items() if k!=':db/id'});return eid
 return v
p=Publisher.from_environment(source=':agent/codex')
with ExitStack() as locks:
 for kp in kps:locks.enter_context(file_lock(ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock',blocking=False))
 locks.enter_context(file_lock(H/'publication.lock'));status=p.client.status();basis=status['basis']
 for kp in kps:
  current[kp]=jsonable(p.read_kp(kp,H/'final'/str(kp)/'capture',basis));save(H/'final'/str(kp)/'kp.json',current[kp]);visit(current[kp]);qids.extend(q[':db/id'] for q in current[kp][':knowledge-point/questions']);sources[kp]=p.extract_source(kp,H/'final'/str(kp)/'source',basis=basis)
 # Real owner graph. Restrict owner payloads to references so the graph
 # cannot overwrite captured full questions or install unrelated enum records.
 def graph_record(record,attrs):
  def ref(v):
   if isinstance(v,dict) and ':db/id' in v:return {':db/id':v[':db/id']}
   if isinstance(v,list):return [ref(x) for x in v]
   return v
  return {k:ref(v) for k,v in record.items() if k==':db/id' or k in attrs}
 frontier=set(qids);contained=set(qids);depth=0
 while frontier:
  rows=[];ordered=sorted(frontier)
  for offset in range(0,len(ordered),100):
   rows+=p.client.query('[:find (pull ?p [:db/id :assigned-problem/content]) :in $ [?c ...] :where [?p :assigned-problem/content ?c]]',[ordered[offset:offset+100]],H/'final',f'wrappers-{depth}-{offset}',basis)
  parents=set()
  for row in rows:visit(graph_record(jsonable(row[0]),[':assigned-problem/content']));parents.add(row[0][':db/id'])
  frontier=parents-contained;contained|=parents;depth+=1
 steps=p.client.query('[:find (pull ?s [:db/id :step/content :multistep-step/question]) :where [_ :multistep/steps ?s]]',[],H/'final','actual-multistep-steps',basis)
 multis=p.client.query('[:find (pull ?m [:db/id :multistep/steps]) :where [?m :multistep/steps _]]',[],H/'final','actual-multisteps',basis)
 for rows in [steps,multis]:
  for row in rows:visit(graph_record(jsonable(row[0]),[':step/content',':multistep-step/question',':multistep/steps']))
 save(H/'final/native-input.json',{'basis':basis,'entities':native_input,'questions':qids});helper=H/'normal/eligibility';subprocess.run([str(helper),str(H/'final/native-input.json'),str(H/'final/native-eligibility.json')],check=True);eligible={r['entity']:r['eligible'] for r in read(H/'final/native-eligibility.json')['questions']};results=[]
 cleanup=read(H/'normal/cleanup-results/17592186092384.json');fixed=read(H/'normal/cleanup-publication/17592186092384'/str(cleanup['basis_before'])/'expected.json');fixedsolution=next(q[':question/worked-solution'] for q in fixed[':knowledge-point/questions'] if q[':db/id']==17592186317210)
 for meta in scope:
  kp=meta['kp'];before=read(ROOT/meta['snapshot']);old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in current[kp][':knowledge-point/questions']}
  assert set(now)-set(old)==fresh[kp],('Unexpected added identities',kp)
  for eid,q in old.items():
   expected=copy.deepcopy(q)
   if eid in retired:expected[':question/retired']=True
   if eid==17592186317210:expected[':question/worked-solution']=fixedsolution
   assert canon(now[eid])==canon(expected),('Unexpected old-question edit',kp,eid)
  for eid in retired&set(now):assert now[eid][':question/retired'] and not eligible[eid]
  newfp=[content_fingerprint(now[eid]) for eid in fresh[kp]];assert len(newfp)==len(set(newfp));assert not set(newfp)&{content_fingerprint(q) for q in old.values()}
  expected_new=[]
  for band in ['easy','moderate','hard']:
   if meta['lesson']=='normal':file=H/'normal'/str(kp)/'publish'/f'{band}.json'
   elif meta['lesson']=='vector':file=H/'vector'/str(kp)/'publish'/band/'delivery/accepted.json'
   else:file=H/'gaussian'/str(kp)/band/'records.json'
   expected_new.extend(read(file))
  assert {str(now[e][':question/id']):canon(normalized_question(now[e])) for e in fresh[kp]}=={str(r['question'][':question/id']):canon(normalized_question(r['question'])) for r in expected_new},('Exact new prompt/fields/keys/solution differ from reviewed batch',kp)
  counts={};newcounts={}
  for band in ['easy','moderate','hard']:
   counts[band]=sum(eligible[e] and enum(q.get(':question/difficulty'))==':question.difficulty/'+band for e,q in now.items());newcounts[band]=sum(eligible[e] and enum(now[e].get(':question/difficulty'))==':question.difficulty/'+band for e in fresh[kp]);assert counts[band]>=5 and newcounts[band]>=5,(kp,band,counts,newcounts)
  ref=current[kp][':knowledge-point/question-generator'][':question-generator/script'];sha=Path(ref).parent.name;verify_package((p.config.math_root/ref).parent,sha);approval=read(p.config.math_root/'generators/approvals'/sha/(str(kp)+'.json'));identity={**source_identity(sources[kp]),'package_sha256':sha,'registration':ref}
  for band in counts:approved_band(approval,identity,band,REVIEW_POLICY_VERSION)
  oldref=before[':knowledge-point/question-generator'][':question-generator/script'];verify_package((p.config.math_root/oldref).parent,Path(oldref).parent.name)
  results.append({'kp':kp,'registration':ref,'total_native_usable_by_band':counts,'new_native_usable_by_band':newcounts,'new_question_ids':sorted(fresh[kp]),'retired_ids':sorted(retired&set(now)),'all_new_prompts_fields_keys_solutions_match_reviewed_batches':True,'all_old_question_edits_exactly_scoped':True,'old_and_current_packages_intact':True,'all_band_approval_current_source_matches':True})
 report={'passed':True,'basis':basis,'retired_questions':len(retired),'notation_repairs':1,'new_questions':sum(len(v) for v in fresh.values()),'results':results,'native_entry_point':'learning::validate_practice_question','real_multistep_context_captured':True,'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'global_generation_setting':[line for line in (ROOT/'.local/ui.env').read_text().splitlines() if line.startswith('COURSE_ACADEMY_DISABLE_GENERATION=')],'service_configuration_edited_by_task':False,'database_writes':0};save(H/'final-verification.json',report);print(json.dumps(report,indent=2))
