"""Verify final owned artifacts and freeze their complete file/directory pathset."""
import sys
sys.dont_write_bytecode=True
import hashlib,importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sys.path.insert(0,str(D));import validate as validator
baseline=validator.baseline();build,hashes=validator.hashes()
for name,src in [('source.json','sources/17592186124644.json'),('topics.json','topics/17592186048707.json'),('lessons.json','lessons/17592186048707.json')]:
    assert (D/name).read_bytes()==(ROOT/'generate/runs/current/refresh-2026-10-14'/src).read_bytes()
validation=json.loads((D/'validation.json').read_text());render=json.loads((D/'render-report.json').read_text());finite=json.loads((D/'finite-domain-counts.json').read_text())
assert render['records']==38 and render['errors']==0 and render['overflow']==0 and render['radio_selection_round_trips']==190 and render['full_solution_records']==36
cli=json.loads((D/'cli-json.json').read_text());assert isinstance(cli,list) and len(cli)==6
normal=(D/'cli-markdown-normal.txt').read_text();raw=(D/'cli-markdown-source-omission.txt').read_text()
assert normal.count('Difficulty:')==6 and normal.count('**(correct)**')==6
assert 'Correct-answer designation: absent in the captured source.' in raw and '**(correct)**' not in raw
assert len(json.loads((D/'review.json').read_text()))==26
assert len(json.loads((D/'source-cases.json').read_text()))==12
assert sum(len(z['choices']) for z in json.loads((D/'bank-map.json').read_text())['source_banks'])==60
assert finite['total_eligible_tasks']==5217
(D/'numeric-baseline-final.json').write_text(json.dumps(baseline,indent=2)+'\n')
reviewed=['generated-12-tan-reciprocal','generated-14-base-exponential-tan','generated-16-sin-cos-linear','generated-18-power-log-root','generated-20-exp-log-power','generated-22-polynomial','generated-24-sec-power','generated-26-root-reciprocal','generated-28-cross-roots','generated-30-cos-log-sin','generated-32-cot-polynomial','generated-34-log-power-exp','generated-36-easy-polynomial','source-0-tan-reciprocal','source-1-base-exponential-tan']
(D/'visual-review.json').write_text(json.dumps({'viewed_family_and_omission_screenshots':reviewed,'observations':'Actual visible radio rings/selected states, complete five-option banks, full fixed solutions, readable derivative and substitution stages, signed/negative-coordinate grouping, reciprocal rewrite and separate sec/tan evaluations inspected. Theme CSS supplies real player colors. Initial logarithm-compression issue corrected and final base-exponential screenshot reinspected. No clipping or unresolved visual issue found.','automated_rendered_records':38,'full_solution_records':36,'missing_source_solutions':2,'actual_radio_selection_round_trips':190},indent=2)+'\n')
summary={'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((D/'source.json').read_bytes()).hexdigest(),'source_counts':validation['source_counts'],'math_checks':validation['math_checks'],'native':validation['native'],'render_counts':{k:render[k] for k in ('records','errors','exposed_delimiters','overflow','radio_selection_round_trips','full_solution_records')},'finite_domain_eligible_tasks':finite['total_eligible_tasks'],'numeric_baseline':baseline,'registered':False,'root_approval':'pending','limits':['Source replay is presentation-normalized mathematics and complete source prose, not byte-identical question strings.','Two original keys, ratings and worked solutions are absent and remain absent in raw public replay. Native key repair is local synthetic evidence only.','Observed wrong scalar intent is underdetermined; historical banks are anchor-only evidence profiles, with complete method-derived banks for normal variants.','Raw source2e+1 is ambiguous to native scalar parser: three known semantic failures reproduced in separate synthetic blank diagnostics. Normal e products are explicit; actual learner contract remains radio.']}
(D/'completion-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
owned=[D.with_suffix('.py'),*[p for p in D.rglob('*') if p.is_file() and p.name!='freeze-manifest.json']]
entries={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(owned)}
manifest={'scope':'Entire owned draft script and evidence directory. Excludes this self-referential manifest only. No numeric registered file/tree/cache touched.','script_sha256':summary['script_sha256'],'source_sha256':summary['source_sha256'],'files':entries,'file_count':len(entries),'directories':sorted(str(p.relative_to(ROOT)) for p in D.rglob('*') if p.is_dir()),'numeric_baseline':baseline,'verified_native_build_hashes':len(hashes)}
(D/'freeze-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for rel,expected in entries.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==expected
assert set(entries)=={str(p.relative_to(ROOT)) for p in [D.with_suffix('.py'),*[q for q in D.rglob('*') if q.is_file() and q.name!='freeze-manifest.json']]}
print(json.dumps({'script_sha256':summary['script_sha256'],'source_sha256':summary['source_sha256'],'frozen_owned_files':len(entries),'freeze_manifest_sha256':hashlib.sha256((D/'freeze-manifest.json').read_bytes()).hexdigest(),'numeric_baseline':baseline},indent=2))
