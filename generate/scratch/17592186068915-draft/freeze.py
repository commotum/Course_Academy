"""Freeze a verified local draft; no registration or database writes."""
from pathlib import Path
import hashlib,json
D=Path(__file__).parent;ROOT=D.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,z):(D/n).write_text(json.dumps(z,indent=2,ensure_ascii=False)+'\n')
r=json.loads((D/'validation.json').read_text());assert r['source_fidelity']['complete_banks']==7 and r['source_fidelity']['matched_choices']==27 and r['registered_pathset_and_hashes_preserved']
base=json.loads((D/'registration-baseline.json').read_text())['files'];numeric=ROOT/'generate/scratch/17592186068915';now={str(p.relative_to(ROOT)):sha(p)for p in [numeric.with_suffix('.py')]+sorted(p for p in numeric.rglob('*')if p.is_file())};assert base==now
save('snapshot-manifest.json',{'database':'math','basis':2275,'lineage':json.loads((D/'source.json').read_text())['lineage'],'captures':{n:sha(D/n)for n in ('source.json','topic.json','lesson-route.json','source-query.edn')},'registered_pathset_and_hashes_preserved':True,'original_preserved_file_count':len(base)})
review='''# Review disposition

Ready for independent root review of stages3–7. All seven MA sources replay through the parameterized public script:27/27 complete options,20/20 distractors,7/7 banks; six available source solutions match shared prose, ordered row counts and every formal operand. q2204 has no original key/solution/rating: these are explicitly authored completion, and its observed reference API is evidence-only/ineligible. Four nonMA generated full-Pull records are separately inventoried.

Independent readback validates actual rendered integrands, u and du, all solution rows, every formal integral operand, individual endpoint contributions, banks modulo arbitrary C, owned keys and every declared numerical slot. Full finite banks reject whole collisions. Actual printed fingerprints match metadata. Strict public input types, full explicit bounds, exact replay, stable IDs independent of option RNG, finite task dedup/overflow and flat CLI all/count3 JSON+Markdown pass. Capacities easy264, moderate302, hard144; hard overlaps the moderate shifted-definite domain and is provisional because no hard source evidence exists. Ordered lesson traversal and actual prerequisites keep every question within real linear sine/cosine substitution.

The unchanged SHA-pinned native grader reports244 accepted,650 rejected,4 unresolved. Three unresolved are valid ordinary wrong submission1 against4/pi,2sqrt(3)/pi,3/pi; the fourth is a separate intentionally malformed diagnostic. All scoped mathematical outputs remain eligible; no parameter exclusion hides the native gap. Two valid unsimplified equivalents are rejected under observed Do not round wording; normal wording Give an exact answer accepts genuine equivalents across every distinct bounded blank output. Native mathematical limits and source wording limits are recorded separately. Engine compatibility remains limited on those precise comparisons.

Registered numeric script and entire evidence directory path/hash set, including bytecode caches, remain unchanged. Draft only; no registration, DB writes, shared QA/queue edits, engine edits or commits. Root approval is still pending.
'''
(D/'review-disposition.md').write_text(review)
(D/'README.md').write_text((D/'README.md').read_text()+'\nNative limits: three valid ordinary wrong submissions1 against4/pi,2sqrt(3)/pi,3/pi are unresolved; one separate malformed diagnostic is unresolved. Two observed-wording equivalent rejections are documented; ordinary exact wording accepts tested equivalents. See review-disposition.md and validation.json. Ready for independent root review, with engine compatibility limits explicitly open.\n')
paths=[D.with_suffix('.py')]+sorted(p for p in D.rglob('*')if p.is_file()and p.name not in ('hash-manifest.json','ready.json'))
save('hash-manifest.json',{'algorithm':'sha256','paths':{str(p.relative_to(ROOT)):sha(p)for p in paths},'frozen_engine_sha256':r['engine_sha256'],'registered_baseline_checked':True})
save('ready.json',{'status':'ready_for_independent_root_review_with_native_limits','kp_id':17592186068915,'basis':2275,'script':str(D.with_suffix('.py').relative_to(ROOT)),'script_sha256':sha(D.with_suffix('.py')),'hash_manifest_sha256':sha(D/'hash-manifest.json'),'source_fidelity':r['source_fidelity'],'capacity':r['capacity'],'native':r['native'],'ordinary_valid_math_native_unresolved':r['ordinary_valid_math_native_unresolved'],'limitations':r['limits'],'registered_pathset_and_hashes_preserved':True,'database_writes':0,'root_approval':'pending'})
print(json.dumps(json.loads((D/'ready.json').read_text()),indent=2))
