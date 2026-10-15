"""Private authoring of immutable-basis evidence and review; no live reads/writes."""
from pathlib import Path
import importlib.util,json,hashlib,sys
sys.dont_write_bytecode=True
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('kp68915',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,z):(D/n).write_text(json.dumps(z,indent=2,ensure_ascii=False)+'\n')
ma=[q for q in g.REC[':knowledge-point/questions'] if ':question/math-academy-id'in q];other=[q for q in g.REC[':knowledge-point/questions'] if ':question/math-academy-id'not in q]
save('standard-inventory.json',{'basis':2275,'all_pull_question_count':len(ma)+len(other),'ma_original_count':len(ma),'non_ma_count':len(other),'non_ma_records':other,'ma_ids':[q[':question/math-academy-id']for q in ma],'canonical_excluded':g.REC[':knowledge-point/canonical-example']})
cases=[{'source_id':sid,'template':sid,'difficulty':c[0],'parameters':c[-1],'bank_profile':'observed','incomplete_raw_reference':sid=='q-2204','missing_original':['difficulty','correct','worked-solution'] if sid=='q-2204' else []}for sid,c in g.CONFIG.items()if sid in g.QS];save('source-cases.json',cases)
review=[];md=['# KP68915 side-by-side source and served review','Basis2275; actual public generator output at source parameters and changed parameters. Seven MA sources are fidelity denominator. Four generated nonMA records are separately inventoried.']
for case in cases:
 sid=case['source_id'];q=g.QS[sid];md+=['## '+sid,'### Raw original',q[':question/problem'],q.get(':question/worked-solution','[Original solution missing]'),'\n'.join(a[':answer/value']for a in q[':question/answer-fields'][0][':answer-field/choices'])]
 for label,seed,p,profile in [('Observed source parameters',0,case['parameters'],'observed'),('Served changed parameters',321,None,'method'),('Served second changed parameters',654,None,'method')]:
  r=g.generate(case['difficulty'],seed,template=sid,parameters=p,profile=profile);review.append(r);md+=['### '+label,g.markdown(r),'Parameters `'+json.dumps(r['generation']['parameters'],sort_keys=True)+'`.']
for seed in (321,654):
 r=g.generate('hard',seed,template='authored-hard');review.append(r);md+=['## Authored hard: provisional rating',g.markdown(r),'Same shifted definite source backbone as moderate q10574. No hard-source evidence or added steps claimed.']
save('review.json',review);(D/'review.md').write_text('\n\n'.join(md)+'\n')
classification='''# Classification at math basis2275

Seven MA practice records: three observed easy (two indefinite radio, one definite blank), three moderate (two definite radio, one definite blank), one unrated incomplete indefinite radio q2204. Four nonMA generated records are full-Pull inventory, not MA fidelity evidence. Canonical e464 is contextual, excluded from practice denominator. All templates have plot rating none: no images, diagrams or graphs appear in prompt, bank or solution.

Separate source prompt and bank profiles: q10061 sine indefinite radio; q2204 sine indefinite radio with variable z and distinct bank; q10064 cosine indefinite radio with negative slope and nonzero constant shift; q350040 sine definite blank; q13647 sine definite radio; q346081 cosine definite blank with pi-scaled slope; q10574 sine definite radio with pi shift. Each indefinite has four solution rows, each definite six plus a two-row limit table. q2204 has no original key, solution or rating. The derivative selects -cos(5z)/5+C; the four-row solution and easy rating are authored completion with explicit provenance.

No observed hard level exists. authored-hard reuses the shifted definite sine radio backbone and complete q10574 bank under the identical moderate slot domain. Its hard rating is provisional and overlaps moderate workload; it introduces no extra steps, operations or progression. The actual ordered lesson begins with linear substitution, places this KP before reciprocal linear trig, and introduces nonlinear products only after both. Nonlinear arguments and reciprocal functions are excluded. Prerequisites are basic trig primitives and definite integrals by substitution, supporting all chosen slots but not a claim of MA hard calibration.
'''
(D/'classification.md').write_text(classification)
text=['# Template extraction','## 1. Specific source observations']
for case in cases:
 sid=case['source_id'];q=g.QS[sid];text+=['### '+sid,'Observed slots `'+json.dumps(case['parameters'],sort_keys=True)+'`.',q[':question/problem'],q.get(':question/worked-solution','Original solution missing; not matched.')]
 f=q[':question/answer-fields'][0]
 for a in f[':answer-field/choices']:text+=['- Field `'+f[':answer-field/key']+'`, answer `'+a[':answer/id']+'`: `$'+a[':answer/value']+'$`'+(' (observed correct)' if a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id') else '')+'.']
text+=['''## 2. Generalized backbone

Compute one real affine argument u=ax+b, its nonzero constant derivative, and solved dx; substitute into the sine/cosine integral, extract c/a, integrate, and substitute back for indefinite integrals. For definite integrals, transform both bounds, then use six ordered rows: substituted integral, factored integral, primitive evaluation bar, explicit endpoint trig expressions, individually evaluated endpoint constants, final result. Source prompts, variable roles, field type and key, and complete source banks remain fixed by template. Every served row is parameterized; raw JSON is evidence only, never a returned worked solution.

## 3. Complete component/bank recipe mapping

Let z=ax+b, c the amplitude, r=c/a. All indefinite values include arbitrary +C and compare modulo constants.

- q10061: [r cos(z), -ca cos(z), ca cos(z), -r sin(z), -r cos(z)] +C, last correct. These are sign, scale and primitive-function mistakes.
- q2204: [c cos(z), -r cos(z), r cos(z), -r cos(x), ca cos(z)] +C, second independently completed correct. Variable is z in the served question, with x above denoting its variable role. The fourth omits the argument scale; it is not a stale variable.
- q10064: [-c/b sin(z), r sin(z), -r cos(z), -r sin(z), r cos(z)] +C, second correct. The first divides by the constant shift instead of slope. This is an empirical expression recipe with inferred error intent; b stays positive, never equals -a, so complete bank members remain distinct.
- q13647: [0,V,-V,1,-1], V=c/a[cos(lo)-cos(hi)], second correct. Cases V in {0,1,-1} reject the entire five-option bank. Literal 0 and ±1 are observed bank components, not fabricated coefficient transport.
- q10574 and authored-hard: [cD/2,V,2V,V/2,caD/2], where D=cos(lo)-cos(hi), V=cD/a, second correct. Observed empirical scale patterns generalize the complete [1/2,1/3,2/3,1/6,3/2] bank at a3,c1,D1; cognitive explanations are not claimed. Any pairwise equivalence rejects the entire bank, never replacing a choice.
- q350040 and q346081 blank: one exact evaluated value, no C, no distractors. Their original keys field-1 and selection for radios persist.

All source choices map one-to-one at original parameters. q2204's missing original designation is reported as authored, never source fidelity. Raw doubled command slashes in answer captures and nested aligned environments are retained in raw evidence but normalized in served content. These are presentation repairs, no mathematical correction. No source wrong/wrong duplicate was found at original parameters; every sampled bank is checked pairwise modulo C.

## 4. Explicit finite slots and dependencies

Parameters use reduced rational strings a,b,lo,hi and strict builtin integer c (bool rejected). a is the slope except q346081, whose slope is a*pi. b is an ordinary constant for indefinite templates and b*pi for definite templates. lo,hi are transformed endpoint angles divided by pi. Actual x bounds are (lo*pi-b)/a with actual slope and shift substituted, so each table, formal operand and endpoint expression derives from one instance.

q10061/q2204: a2..10,b0,c1..4. q10064: a=-10..-4,b1..4,c1..4. Positive shift remains nonzero, negative slope remains negative. q350040/q13647: a2..6,b0,c2..9. q346081: a in 1/2,1/3,1/4,1/5; b0,c1..4. q10574/authored-hard: a2..6,b in ±1/3,±1/6;c1..4. Definite endpoint pairs are exactly ENDPOINTS in the script: three familiar pairs per source. They change endpoint arithmetic without introducing new operations. All are ordered, finite, and sine/cosine have no real poles, so the unique real component is all of R. Public explicit-parameter calls enforce exactly this full finite domain, with no wider hidden acceptance.

The family/function/variable/field/count/stage sequence is fixed because changing it changes observed banks or response contracts. Numerical amplitude, scale, shift and eligible familiar endpoint pairs vary within this defined backbone. Distinctness uses the actual integrand and x bounds; templates, prose, answer order, seed, profile and arbitrary constants do not create practice novelty. Metadata carries seed, parameters, selected complete bank, version and frozen basis. Option shuffling uses an independent RNG; content identities do not depend on seed or option order.

Exact-answer wording is preserved for profile=observed. Normal method blanks use Give an exact answer, since the unchanged native grader interprets Do not round as a restrictive format policy. This authored wording repair retains the response shape and exactness; source wording fidelity is validated separately. Unknown/incomplete source references remain source-cases and raw evidence. q2204 observed replay is explicitly evidence_only and ineligible_for_learning; its ordinary completed profile is eligible and carries authored-completion metadata. Complete source profiles and all mathematically valid scoped pi outputs remain eligible: native comparison gaps do not justify excluding valid tasks. Three wrong submissions of 1 against 4/pi, 2sqrt(3)/pi and 3/pi are unresolved by the unchanged native grader, with per-case evidence separate from malformed notation.
''']
(D/'template-extraction.md').write_text('\n\n'.join(text)+'\n')
(D/'plot-extraction.md').write_text('# Plot extraction\n\nAll source prompt/choice/solution components inspected: no images, diagrams, graphs, or plot assets. Rating none; no plotting required.\n')
for stage,f in [('3-classify.md','classification.md'),('4-template-extraction.md','template-extraction.md'),('5-plot-extraction.md','plot-extraction.md')]: (D/stage).write_text((D/f).read_text())
(D/'6-template-generator.md').write_text('# Template generator\n\nPublic ../17592186068915-draft.py implements every source family and the separately labelled authored hard calibration. Full prompt, complete banks and ordered solution rows are served from parameterized code. readback.py independently parses actual math. validate.py separately reports source fidelity, mathematical validation, full finite slot coverage, strict API contract and unchanged native grader results. Registered numeric files remain byte-preserved; no DB writes, shared QA, queue, registration or commits.\n')
(D/'7-plot-generator.md').write_text((D/'plot-extraction.md').read_text())
(D/'README.md').write_text('# KP68915 local draft\n\nRun `.venv/bin/python -B generate/scratch/17592186068915-draft/validate.py`. Preview `--difficulty all --count 1 --format json` returns a flat three-record E/M/H list. Frozen math basis2275. Registered numeric script and entire evidence path/hash set are untouched, including caches; registration-baseline.json records preservation. Source fidelity counts seven MA records, with incomplete q2204 independently completed; four nonMA full-Pull records are separate. No original hard examples exist: authored hard rating is explicitly provisional and uses the moderate shifted definite backbone.\n')
save('provenance.json',{'database':'math','basis':2275,'lineage':g.SOURCE['lineage'],'method':'immutable captured full Pull','source_path':'generate/runs/current/refresh-2026-10-14/sources/17592186068915.json','source_sha256':hashlib.sha256((D/'source.json').read_bytes()).hexdigest(),'database_writes':0,'registered_generator_untouched':True,'source_queries':'source-query.edn','inputs':[[g.KP]]})
save('scope-calibration.json',{'basis':2275,'prerequisites':g.REC[':knowledge-point/key-prerequisites'],'ordered_lesson':'lesson-route.json','observed_difficulties':{'easy':3,'moderate':3,'unrated':1,'hard':0},'authored_hard':'Same affine shifted definite sine radio backbone and numerical slot domain as q10574, provisional hard rating; no harder method or additional steps claimed.','excluded':'Nonlinear arguments; reciprocal functions; integration by parts; improper intervals; new solution stages.'})
print('Evidence built',len(review))
