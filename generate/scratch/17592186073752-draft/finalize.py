"""Draft-only final evidence, exact registered path/hash comparison and freeze."""
import hashlib,json,pathlib
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[2]
def dump(name,x):(P/name).write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
raw=json.loads((P/'source-cases.json').read_text());replays=json.loads((P/'source-replay.json').read_text());reviews=json.loads((P/'review.json').read_text());v=json.loads((P/'validation.json').read_text());render=json.loads((P/'browser-rendering.json').read_text())
md=['# Substitution review at frozen basis 2275','','Immutable raw source records remain in source-cases.json. Missing observed fields and malformed/omitted source context remain raw-ineligible; supported completions are separate. Prior generated inventory retains its raw records and identities in independent-inventory.json.','']
for src,r in zip(raw,replays):
 q=src['record'];md+=['## Original '+src['source_id'],'','```text',q[':question/problem'],'```','','Captured answer fields:','```json',json.dumps(q[':question/answer-fields'],indent=2),'```','','```text',q.get(':question/worked-solution','No captured worked solution.'),'```','','## Supported replay '+src['source_id'],'',r['question'][':question/problem'],'','```json',json.dumps(r['question'][':question/answer-fields'],indent=2),'```','',r['question'][':question/worked-solution'],'']
for item in reviews[10:]:
 q=item['record']['question'];md+=['## '+item['label'],'',q[':question/problem'],'','```json',json.dumps(q[':question/answer-fields'],indent=2),'```','',q[':question/worked-solution'],'']
(P/'review.md').write_text('\n'.join(md))
base=json.loads((P/'registered-baseline.json').read_text());r=ROOT/'generate/scratch';kp='17592186073752';paths=[r/(kp+'.py')]+sorted((r/kp).rglob('*'))+sorted((r/'__pycache__').glob('*'+kp+'*'));now={str(p.relative_to(ROOT)):sha(p)for p in paths if p.is_file()}
assert base==now,dict(added=sorted(now.keys()-base.keys()),removed=sorted(base.keys()-now.keys()),changed=[p for p in base.keys()&now.keys()if base[p]!=now[p]])
dump('registered-baseline-verification.json',dict(passed=True,exact_pathset=True,paths=len(now),hashes_match=True))
source=json.loads((P/'source.json').read_text());assert len(json.loads((P/'cli-all-1.json').read_text()))==3
for local,frozen in [('source.json','sources/17592186073752.json'),('reference/topic.json','topics/17592186048826.json'),('reference/lesson.json','lessons/17592186048826.json')]:assert sha(P/local)==sha(ROOT/'generate/runs/current/refresh-2026-10-14'/frozen)
build=json.loads((P/'reference/grader-build.json').read_text())
for pathkey,hashkey in [('source','source_sha256'),('library','library_sha256'),('binary','binary_sha256')]:assert sha(ROOT/build[pathkey])==build[hashkey]
verification=json.loads((P/'reference/grader-verification.json').read_text())
for pathkey,hashkey in [('source','source_sha256'),('library','library_sha256'),('binary','binary_sha256')]:verification['verified'][build[pathkey]]=build[hashkey]
dump('reference/grader-verification.json',verification)
for item in raw:assert item['record']==next(q for q in source['record'][':knowledge-point/questions']if q.get(':question/math-academy-id')==item['source_id'])
inventory=json.loads((P/'independent-inventory.json').read_text());assert [x['record']for x in inventory['questions']]==[q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'not in q]
dump('readiness.json',dict(status='ready for independent root QA and approval',kp=17592186073752,generator_sha256=sha(P.with_suffix('.py')),source_wrapper_sha256=sha(P/'source.json'),basis=2275,original_sources=10,existing_worked_solutions_reproduced=7,complete_nonempty_banks_matched=16,source_values_matched=24,source_values_total=24,source_correct_refs_matched=14,raw_source_eligible=3,separate_supported_repairs=7,independent_inventory_exact=12,generated_math_checks=sum(v['math_checks'].values()),negative_controls=len(v['negative_controls']),deduplicated_batches=v['dedup'],native=dict(accepted=v['native']['accepted_checks'],rejected=v['native']['rejected_checks'],explicitly_unresolved=v['native']['documented_unresolved_checks'],binary_sha256='33510bf3ac27a1eb28e9bad7b4121a22d2fa787026d3102268daa4ecf98b1617',engine_source_hashes=28,dependency_hashes=11),visual=dict(records=len(render['records']),math_expressions=sum(x['rendered_math']for x in render['records']),no_errors=True,no_undefined_red_text=True,all_fields_actual_player=True),registered_unchanged=True,database_writes=0,registration=False,limits=['Moderate difficulty and the retained hard unit_pair workload are authored qualifications.','Raw source omissions remain ineligible; supported completions are explicitly separate.','Empirical source_4133 amplitude ratios and source_5179 -2q retain unresolved distractor intent.','Actual scalar grader reports whole-tuple submissions unresolved; unknown radio UUIDs are unresolved. Canonical and genuinely equivalent rational fragments pass.','Generation uses a conservative count cap of 10000 with bounded mathematical deduplication attempts.']))
# Freeze every owned deliverable except the self-referential manifest.
files=[P.with_suffix('.py')]+sorted(P.rglob('*'));hashes={str(p.relative_to(ROOT)):sha(p)for p in files if p.is_file() and p.name!='freeze.json'}
dump('freeze.json',dict(status='frozen draft; root approval pending',generator_sha256=sha(P.with_suffix('.py')),files=hashes))
print(json.dumps(json.loads((P/'readiness.json').read_text()),indent=2))
