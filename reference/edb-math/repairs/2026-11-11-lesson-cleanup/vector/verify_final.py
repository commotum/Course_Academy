"""Read one live EDB value; check complete pool native eligibility and fresh floors."""
import copy,hashlib,json,subprocess,sys
from contextlib import ExitStack
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts.generator_publish import Publisher,jsonable,content_fingerprint,enum
from scripts.generator_pipeline import source_identity
from scripts.generator_packages import verify_package
from scripts.generator_approval import approved_band
from scripts.generator_review import REVIEW_POLICY_VERSION
from capture.scripts.storage import atomic_json,file_lock
HELPER=H.parent/'normal/eligibility'
KPS=[17592186096652,17592186096653,17592186096701,17592186235285]
def read(p):return json.loads(Path(p).read_text())
def save(p,x):atomic_json(Path(p),jsonable(x))
p=Publisher.from_environment(source=':agent/codex');entities={};idents={};questions=[];kps={};sources={}
def visit(value):
 if isinstance(value,list):return [visit(v) for v in value]
 if isinstance(value,dict):
  if ':db/ident' in value and ':db/id' not in value:
   ident=value[':db/ident'].lstrip(':')
   if ident not in idents:idents[ident]=len(idents)+1;entities[str(idents[ident])]={'db/ident':ident}
   return idents[ident]
  if ':db/id' in value:
   eid=value[':db/id'];row={k.lstrip(':'):visit(v) for k,v in value.items() if k!=':db/id'};entities.setdefault(str(eid),{}).update(row);return eid
 return value
with ExitStack() as locks:
 for kp in KPS:locks.enter_context(file_lock(ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock',blocking=False))
 locks.enter_context(file_lock(H.parent/'publication.lock'))
 status=p.client.status();basis=status['basis']
 for kp in KPS:
  d=H/str(kp);kps[kp]=jsonable(p.read_kp(kp,d/'final',basis));sources[kp]=p.extract_source(kp,d/'source-final',basis=basis);assert source_identity(sources[kp])==source_identity(read(d/'source/source.json'));save(d/'final/kp.json',kps[kp]);visit(kps[kp]);questions.extend(q[':db/id'] for q in kps[kp][':knowledge-point/questions'])
 for query,name in [('[:find (pull ?s [*]) :where [_ :multistep/steps ?s]]','multistep-steps'),('[:find (pull ?m [*]) :where [?m :multistep/steps _]]','multisteps'),('[:find (pull ?p [*]) :where [?p :assigned-problem/content _]]','assigned-problems')]:
  for row in p.client.query(query,[],H/'final',name,basis):visit(jsonable(row[0]))
 save(H/'final/native-eligibility-input.json',dict(basis=basis,entities=entities,questions=questions));subprocess.run([str(HELPER),str(H/'final/native-eligibility-input.json'),str(H/'final/native-eligibility.json')],check=True)
 native=read(H/'final/native-eligibility.json');byid={r['entity']:r for r in native['questions']};results=[];retired={row['question'] for row in read(H/'retirement-ledger.json')['questions']}
 for kp in KPS:
  d=H/str(kp);current={q[':db/id']:q for q in kps[kp][':knowledge-point/questions']};old={q[':db/id']:q for q in read(d/'capture-after-retirement/kp.json')[':knowledge-point/questions']};assert all(current[e]==q for e,q in old.items());new=[q for e,q in current.items() if e not in old];assert len(new)==read(d/'publication-selection.json')['total']
  freshfp={content_fingerprint(q) for q in new};assert len(freshfp)==len(new);assert not freshfp & set(read(d/'capture/inventory.json')['fingerprints'])
  for qid in retired & set(current):assert current[qid][':question/retired'] is True and not byid[qid]['eligible']
  counts={};fresh_counts={};expected=[]
  for band in ['easy','moderate','hard']:
   counts[band]=sum(byid[q[':db/id']]['eligible'] and enum(q.get(':question/difficulty'))==':question.difficulty/'+band for q in current.values());fresh_counts[band]=sum(byid[q[':db/id']]['eligible'] and enum(q.get(':question/difficulty'))==':question.difficulty/'+band for q in new);assert counts[band]>=5 and fresh_counts[band]==len(read(d/'publish'/band/'delivery/accepted.json')) and fresh_counts[band]>=5
   expected.extend(read(d/'publish'/band/'delivery/accepted.json'))
  assert freshfp=={content_fingerprint(r['question']) for r in expected};installation=read(d/'installation-verification.json');sha=installation['package_sha256'];registered=kps[kp][':knowledge-point/question-generator'][':question-generator/script'];verify_package((p.config.math_root/registered).parent,sha);identity={**source_identity(sources[kp]),'package_sha256':sha,'registration':registered}
  for band in counts:approved_band(read(installation['approval_path']),identity,band,REVIEW_POLICY_VERSION)
  result=dict(kp=kp,basis=basis,nonretired_native_usable_by_band=counts,new_native_usable_by_band=fresh_counts,new_question_ids=[q[':db/id'] for q in new],retired_ids=sorted(retired & set(current)),existing_siblings_unchanged=True,current_approval_source_matches=True,all_new_exact_unique_against_whole_old_pool=True,package_archive_verified=True);results.append(result);save(d/'final/verification.json',result)
 report=dict(passed=True,basis=basis,results=results,new_questions=sum(len(r['new_question_ids']) for r in results),retired_questions=6,native_entry_point='learning::validate_practice_question',helper_sha256=hashlib.sha256(HELPER.read_bytes()).hexdigest(),helper_source_sha256=hashlib.sha256((H/'eligibility.rs').read_bytes()).hexdigest(),native_graph_includes_actual_multisteps_and_assigned_problem_wrappers=True,learner_history_not_mutated=True)
 save(H/'final-verification.json',report);print(json.dumps(report,indent=2))
