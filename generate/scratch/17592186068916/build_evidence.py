"""Private evidence authoring, no live database access."""
from pathlib import Path
import importlib.util,json,sys,hashlib,shutil
sys.dont_write_bytecode=True
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('kp68916',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
cases=[{'source_id':sid,'template':sid,'difficulty':c[0],'parameters':c[3],'bank_profile':'observed','authored_rating':sid=='q-10157','missing_original_correct':sid=='q-10157','reference_only':sid=='q-113983'} for sid,c in g.CONFIG.items()];save('source-cases.json',cases)
review=[];md=['# KP68916 source and served variant review','Basis2275. Raw source wrapper is immutable evidence; all generated records below come through the public generator. Observed profile preserves exact-answer wording; method profile uses Give an exact answer for the native grader.']
for case in cases:
 sid=case['source_id'];src=g.QS[sid];md+=['## '+sid,'### Original',src[':question/problem'],src.get(':question/worked-solution','[Missing original solution]'),'\n'.join('$'+a[':answer/value']+'$' for f in src[':question/answer-fields'] for a in f[':answer-field/choices'])]
 for label,p,profile in [('Observed source parameters',case['parameters'],'observed')]:
  r=g.generate(case['difficulty'],template=sid,parameters=p,profile=profile);review.append(r);md+=['### '+label,g.markdown(r)]
 if sid=='q-113983':
  md+=['This nonlinear source is reference-only at original parameters and is excluded from ordinary inventory; no nonlinear variants are authorized by the linear-argument curriculum.'];continue
 for seed in (321,654):
  r=g.generate(case['difficulty'],seed,template=sid);review.append(r);md+=['### Served changed-parameter variant seed'+str(seed),g.markdown(r),'Parameters: `'+json.dumps(r['generation']['parameters'],sort_keys=True)+'`.']
# Show opaque source bank patterns under changed inputs separately from method banks.
for seed in (321,654):
 r=g.generate('hard',seed,template='q-10578',profile='observed');review.append(r);md+=['## q-10578 observed-bank changed parameters seed'+str(seed),g.markdown(r)]
save('review.json',review);(HERE/'review.md').write_text('\n\n'.join(md)+'\n')
classification='''# Classification at math basis2275

Ten original MA practice questions, all analyzed; canonical e-465 supports curriculum context but is not in the fidelity denominator. Three rated easy radios, one unrated radio, two moderate (radio and blank), four hard (three blank and one radio). Missing q-10157 is authored easy on its exact sibling's linear-substitution workload. Plots: none across every family and profile; no assets or renderer required.

- Easy q-10143: linear sec*tan, five primitive choices, four solution RHS rows. q-2203 has the same mathematical backbone but a distinct prompt and five-option bank, also four rows.
- Unrated q-10157: linear csc*cot, five primitive choices, missing key, solution and difficulty. Authored easy, independently differentiated key -c/a csc(ax)+C; four shared source-style rows supplied. No original designation or solution is claimed.
- Easy q-113983: source-backed exception (c sec²x+d)sec x tan x, five polynomial-primitive choices and three rows. This nonlinear substitution in sec x is inconsistent with this linear-argument KP. The ordered lesson places derivative-proportional nonlinear products in the following tutorial/sibling68917, and original lesson478 contains no q113983. Misassignment is plausible. Preserve the five-option source and exact-parameter normalized reference replay only; it is ineligible for ordinary inventory and has no coefficient or other extensions.
- Moderate q-13663: c csc²(ax), definite integral, five numerical choices, substitution/limit table/six solution rows. q-355818 uses the same integrand and six stages but a single blank and exact-answer instruction; its different field contract is preserved.
- Hard q-346368: reciprocal linear scale, csc*cot definite integral, blank, six stages with the negative primitive grouped inside the positive reciprocal factor. q-350060: shifted sec² definite integral, blank, four stages (omits redundant substitution/scalar rows). q-350071: shifted csc*cot definite integral, blank, six stages with a signed primitive coefficient. q-10578: shifted sec*tan definite integral, five numerical choices, four stages (no separate numerical endpoint simplification row).

Choice-bank profiles are tracked per source ID, including both easy sec*tan banks. The nonlinear source is not used to justify ordinary practice or any nonlinear variation. Nine source families are ordinarily supported; the tenth is reference-only. Every hard case retains its observed reciprocal-scale or nonzero-shift workload. Every moderate instance has a nonunit scale, zero shift and familiar finite endpoints; every easy linear instance has zero shift and no limits. All intervals stay within a common component avoiding cos or sin poles.
'''
(HERE/'classification.md').write_text(classification)
extraction=['# Four-stage template extraction','## 1. Source-by-source specific observations']
for sid,c in g.CONFIG.items():
 q=g.QS[sid];f=q[':question/answer-fields'][0];extraction+=['### '+sid,'Original parameters: `'+json.dumps(c[3],sort_keys=True)+'`. Field '+c[1]+', family '+c[2]+'.',q[':question/problem']]
 for a in f[':answer-field/choices']:
  correct=f.get(':answer-field/correct',{}).get(':answer/id')==a[':answer/id']
  extraction+=['- Answer `'+a[':answer/id']+'`: `$'+a[':answer/value']+'$`; '+('observed correct' if correct else 'source option')+'.']
extraction+=['''## 2. Shared mathematical and instructional backbone

Use one substitution u=ax+bπ (with the incompatible sec(x) source analyzed only as reference evidence), derive du/dx and dx, transform definite limits where supplied, apply a reciprocal-trig primitive, evaluate or substitute back. Answer fields retain the original radio/blank contract and five/single answer counts. Source-specific omitted rows remain omitted. The full served prose and ordered rows are assembled in core(), never returned from raw JSON. The nonlinear reference profile is restricted to its original coefficients and requires explicit template=q-113983, profile=observed; its eligible_for_learning flag is false.

## 3. Complete component and bank mapping

For linear primitives write r=c/a, z=ax, F=sec(z) or csc(z). q-10143 bank is [rF, cF, -caF, -rF, caF]+C with first correct; q-10157 is [cF,rF,caF,-rF,-caF]+C with fourth independently completed correct. q-2203 is [ca sec(z), r csc(z), c sec²(z), r sec(x), r sec(z)]+C with last correct. The unscaled-argument option is a complete argument mistake and changes independently when a changes.

For q-113983 bank is [c tan³(x)/3+d tan(x), c sec²(x)/2, c sec³(x)/3+d sec(x), c sec³(x)/3, c tan³(x)/3+d sec(x)]+C, with third correct. Every primitive bank is compared modulo arbitrary integration constants by differentiating all pairs, including wrong/wrong pairs.

For q-13663 let D=cot(lo)-cot(hi). Bank [-aD/c, caD, -cD, cD/a, D] has fourth correct. These reproduce all five options, including the compound reciprocal/sign coefficient; inferred error intent is not claimed. Entire colliding banks (e.g. c=a) are rejected, never thinned or patched.

For q-10578 observed profile write L=sec(lo), H=sec(hi). Complete bank r[H-L, -H-L/2, cot(hi)-L/2, -L cot(hi)+L/2, tan(hi)+L], first correct. These are empirical endpoint-expression patterns, and their original cognitive interpretation is unresolved. The endpoint multiplier1/2 is retained explicitly, not fitted polynomially. Source-profile variants remain public for faithful replay; normal method banks use [r(H-L), -r(H-L), r(H+L), rH, r(tan(hi)-tan(lo))], all interpretable endpoint/sign/function mistakes. Review preserves this distinction; authored banks are never counted as recovered source banks.

Blank answers are the complete evaluated definite integral, with no C or distractors. The key is c/a[P(hi)-P(lo)], with P=sec,-csc,tan,-cot for sec*tan,csc*cot,sec²,csc². All dependent lower/upper x endpoints are (angle-bπ)/a. For the ordinary linear families, the two table rows, all formal integral operands, differentials, signed primitive endpoints and final value derive from the same instance.

## 4. Stable slots, constraints and dependencies

All numerical slots are exact reduced rational strings a,b, integer c. The nonlinear reference fixes a=1,b=0,c=d=1 and admits no variable slots. x and u are fixed variable roles. Source-specific trig targets remain fixed because their complete banks and primitive stages depend on them; across templates all four reciprocal primitive targets occur. c1..6 (easy1..5); easy a2..10,b0; moderate a2..6,b0; reciprocal hard a1/2,1/3,1/4,b0; shifted hard a1..4,b in ±1/6,±1/4,±1/3. Hard shifts remain nonzero and reciprocal scales remain nonintegral. Every public explicit-parameter call enforces these same bounds and the complete bank constraint.

Endpoint pairs are a finite three-pair catalog per family, listed explicitly in ENDPOINTS. This limits familiar-angle arithmetic and connected real domains, while giving coefficient, scale, shift and endpoint variation without extra operators or reasoning stages. No poles may lie in the interval: sec-based transformed intervals lie inside (-π/2,π/2), csc-based intervals inside (0,π). No negative/inverted interval or improper integral is admitted. Counts use canonical printed integrand and actual x bounds; source IDs, profiles, seed, shuffling and C are excluded.

### Source errors and presentation repairs

q-10157 lacks an original key, solution and rating: all supplied values are explicitly authored completion, not matched missing evidence. q-10143 answer captures contain doubled command slashes in actual decoded strings; raw bytes remain source.json, while served choices are normalized bare TeX. The canonical e-465 correctly factors the coefficient5 in its first row; it is contextual evidence and is not counted as practice fidelity. No other practice mathematics is repaired. Exact-answer blanks retain 'Do not round the answer.' in observed replay; normal wording 'Give an exact answer.' preserves intent and avoids the grader's format-sensitive round detection. This wording repair is separate from mathematical fidelity.
''']
(HERE/'template-extraction.md').write_text('\n\n'.join(extraction)+'\n')
(HERE/'plot-extraction.md').write_text('# Plot extraction and generator\n\nNo images, graphs, diagrams or mathematical plots occur in any prompt, choice or solution. Rating none. No plot generation needed.\n')
# Private copies of the requested workflow stages.
for prefix,target in [('3-','classification.md'),('4-','template-extraction.md'),('5-','plot-extraction.md')]:
 f=next((HERE/'reference').glob(prefix+'*.md'));(HERE/f.name).write_text((HERE/target).read_text())
(HERE/'6-template-generator.md').write_text('# Template generator\n\nPublic script ../17592186068916.py serves all source families and complete observed/method banks. Independent printed-content readback: readback.py. Validation command `.venv/bin/python generate/scratch/17592186068916/validate.py`. Source-cases and review show original parameters and real variants. Source fidelity, correctness, grader checks and authored repairs are reported separately. No EDB writes or registration.\n')
(HERE/'7-plot-generator.md').write_text((HERE/'plot-extraction.md').read_text())
(HERE/'README.md').write_text('# KP68916 local generator\n\nRun `.venv/bin/python generate/scratch/17592186068916/validate.py`; preview `.venv/bin/python generate/scratch/17592186068916.py --difficulty all --count 1 --format json`. JSON all/count1 is a flat three-record list.\n\nFrozen math basis2275; no prior registered generator or evidence directory existed. All10 MA source records are covered, including authored completion of unrated q-10157. Nine ordinary E/M/H source families and stage omissions are parameterized; the incompatible nonlinear source is an exact-parameter reference profile only; normal q10578 uses an explicitly authored method bank because the observed distractor intent is unresolved. The nonlinear easy source is excluded from ordinary inventory because lesson order and prerequisites do not establish it within the linear-argument scope. Raw captures are preserved. See classification, extraction, review, validation and hash manifest for measured results and limits. No shared files, engine, queue, registration or live DB changed.\n')
# Source read provenance request, no new live query.
(HERE/'source-query.json').write_text(json.dumps({'database':'math','basis':2275,'lineage':g.SOURCE['lineage'],'method':'read immutable captured JSON','query_template':'reference/sources-query.edn','inputs':[[g.KP]],'source_path':'generate/runs/current/refresh-2026-10-14/sources/17592186068916.json','source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest()},indent=2)+'\n')
print('Evidence written',len(review),'review records',flush=True)
