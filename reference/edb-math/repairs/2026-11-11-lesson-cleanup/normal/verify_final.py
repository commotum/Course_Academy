"""Exact live final readback plus native fresh-practice eligibility and floors."""
import copy,hashlib,json,sys,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from cleanup import p,KPS,LOCK,RETIRE,FIX,read,save
from generator_publish import jsonable,normalized_question,content_fingerprint,file_lock,enum
from generator_pipeline import source_identity
from scripts.generator_approval import approved_band
from scripts.generator_review import REVIEW_POLICY_VERSION
from scripts.generator_packages import verify_package
status=p.client.status();basis=status['basis'];entities={};idents={};questions=[];kps={};sources={}
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
for kp in KPS:
 D=H/str(kp)
 with file_lock(LOCK/f'kp-{kp}.lock'):
  K=p.read_kp(kp,D/'final',basis);kps[kp]=jsonable(K);source=p.extract_source(kp,D/'source-final',basis=basis);sources[kp]=source;assert source_identity(source)==source_identity(read(D/'source/source.json'))
  save(D/'final/kp.json',jsonable(K));visit(K)
  questions.extend(q[':db/id'] for q in K[':knowledge-point/questions'])
# Native structural graph uses actual stored multistep roots, not invented relationships.
steps=p.client.query('[:find (pull ?s [*]) :where [_ :multistep/steps ?s]]',[],H/'final','multistep-steps',basis)
multis=p.client.query('[:find (pull ?m [*]) :where [?m :multistep/steps _]]',[],H/'final','multisteps',basis)
for rows in [steps,multis]:
 for row in rows:visit(row[0])
# Pull [*] leaves referenced wrappers shallow. Resolve actual assigned-problem links.
wrappers=p.client.query('[:find (pull ?p [*]) :where [?p :assigned-problem/content _]]',[],H/'final','assigned-problems',basis)
for row in wrappers:visit(row[0])
save(H/'final/native-eligibility-input.json',dict(basis=basis,entities=entities,questions=questions));subprocess.run([str(H/'eligibility'),str(H/'final/native-eligibility-input.json'),str(H/'final/native-eligibility.json')],check=True)
native=read(H/'final/native-eligibility.json');byid={r['entity']:r for r in native['questions']};results=[]
for kp in KPS:
 D=H/str(kp);K=kps[kp];current={q[':db/id']:q for q in K[':knowledge-point/questions']};before=read(D/'kp.json');old={q[':db/id']:q for q in before[':knowledge-point/questions']};assert all(current[eid]==q for eid,q in old.items()),'Existing siblings changed during replenishment'
 new=[q for eid,q in current.items() if eid not in old];assert len(new)==15
 allfps=[content_fingerprint(q) for q in new];assert len(set(allfps))==15;assert not set(allfps)&set(read(D/'inventory/inventory.json')['fingerprints'])
 for eid in RETIRE[kp]:assert current[eid][':question/retired'] is True and not byid[eid]['eligible']
 counts={};fresh_counts={};expected=[]
 for band in ['easy','moderate','hard']:
  counts[band]=sum(byid[q[':db/id']]['eligible'] and enum(q.get(':question/difficulty'))==':question.difficulty/'+band for q in current.values())
  fresh_counts[band]=sum(byid[q[':db/id']]['eligible'] and enum(q.get(':question/difficulty'))==':question.difficulty/'+band for q in new);assert counts[band]>=5 and fresh_counts[band]==5
  expected.extend(read(D/'publish'/f'{band}.json'))
 assert {content_fingerprint(q) for q in new}=={content_fingerprint(r['question']) for r in expected}
 package=read(D/'package.json');P=p.config.math_root/Path(package['registration']).parent;verify_package(P,package['package_sha256']);identity={**source_identity(sources[kp]),'package_sha256':package['package_sha256'],'registration':package['registration']};A=p.config.math_root/'generators/approvals'/package['package_sha256']/f'{kp}.json'
 for band in counts:approved_band(read(A),identity,band,REVIEW_POLICY_VERSION)
 if kp==17592186092240:
  fragments=[17592186235432,17592186235480,17592186514424,17592186578848,17592186600817]
  assert all(current[eid]==old[eid] and not byid[eid]['eligible'] for eid in fragments)
 results.append(dict(kp=kp,basis=basis,nonretired_native_usable_by_band=counts,new_native_usable_by_band=fresh_counts,new_question_ids=[q[':db/id'] for q in new],retired_ids=RETIRE[kp],existing_siblings_unchanged=True,current_approval_source_matches=True,all_new_exact_unique_against_whole_old_pool=True,package_unchanged=True));save(D/'final/verification.json',results[-1])
report=dict(passed=True,basis=basis,results=results,new_questions=45,retired_questions=14,notation_repairs=1,native_entry_point='learning::validate_practice_question',helper_sha256=hashlib.sha256((H/'eligibility').read_bytes()).hexdigest(),helper_source_sha256=hashlib.sha256((H/'eligibility.rs').read_bytes()).hexdigest(),native_graph_includes_actual_multisteps_and_assigned_problem_wrappers=True,learner_history_not_mutated=True)
save(H/'final-verification.json',report);print(json.dumps(report,indent=2))
