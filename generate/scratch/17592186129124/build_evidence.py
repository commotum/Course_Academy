import importlib.util,json,re,hashlib
from pathlib import Path
HERE=Path(__file__).parent
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
v=json.loads((HERE/'validation.json').read_text());review=json.loads((HERE/'review.json').read_text())
variants=[]
for sid in g.RAW:
 p=g.source_parameters(sid)
 for step in (1,2):
  altered={**p,'D':str(int(p['D'])+(step if int(p['D'])>0 else -step))}
  r=g.generate(g.RAW[sid]['level'],seed=step,parameters=altered,profile='raw_'+sid);variants.append(r)
review['changed_parameter_evidence_variants']=variants
(HERE/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
with (HERE/'review.md').open('a') as f:
 f.write('\n# Changed-parameter raw bank variants\n\nThese demonstrate the extracted masks and complete bank envelopes. They are evidence-only, retain missing attributes and source errors, and are not learner defaults.\n\n')
 f.write('\n---\n'.join('### Evidence variant '+r['generation']['source_ids'][0]+'\n\n'+g.markdown(r) for r in variants))
(HERE/'classification.md').write_text('''# Classification

Database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Frozen source.json contains all nine practice records and the canonical example.

| Difficulty | Original records | Assessment layout | Shared mathematical families | Plots |
|---|---|---|---|---|
| easy | q-40908, q-10379, q-40903, q-41840 | one fieldless, three 5-choice radios | full range, signed scale and translation | none |
| moderate | q-25512, q-41964, q-65928 | one fieldless, two 5-choice radios | full range; minimum value | none |
| unrated | q-10249, q-40977 | two 5-choice radios, missing correct refs and solutions | full range; minimum value | none |
| hard | none | authored 5-choice radio | same range/minimum transformation with rational endpoint arithmetic | none |

Seven original complete banks are distinct profiles: q-10379 tests interval endpoint inclusion; q-65928 uses minimum, maximum, midline, positive and negative amplitude. q-10249 uses range/ignored-transform values with one partial-shift option. The remaining four banks include underdetermined numerical choices; their full affine component masks are public evidence profiles, without claims of recovered historical error intent. All nine raw profiles are evidence-only, even mathematically sound ones; defaults choose their eligible method bank separately.

Prompt layout variants retain original “Find”/“What” wording, y/f(x), sin/cos notation, linear/radian/degree shifts, spaces and punctuation. Seven stored solutions share three base/transformed inequality displays, multiplication/translation prose, four aligned rows and a conclusion. Two alignment styles are retained per source. Nine provenance masks are not claimed as nine different skills or mathematical templates.

The actual lesson route is reconstructed via first-step 17592186129953 and next links through 17592186129958: Introduction → amplitude → period → midline → range tutorial → this KP. Prerequisites are range of a function (754) and compound inequalities (388). Siblings assess amplitude/period/midline. No zero solving, restricted-input extrema or graph reconstruction is introduced.

The original labels overlap in workload: q-41840 is easy despite a negative coefficient. Normal authored bounds deliberately use a consistent workload distinction, without reclassifying that original: easy positive integer A, moderate negative integer A, hard negative noninteger rational A and noninteger rational D. Raw profiles preserve source labels and omit missing labels. Unrated evidence-only API calls use documented easy (q-10249) and moderate (q-40977) host levels, with no displayed difficulty attribute.
''')
lines=['# Template extraction','','## Stage 1 — specific observed records','']
for sid,src in g.ORIGINALS.items():
 p=g.source_parameters(sid);lines+=['### '+sid,'',src[':question/problem'],'',f'Parameters: {p}; trig {g.RAW[sid]["trig"]}; unit {g.RAW[sid]["unit"]}; output {g.RAW[sid]["out"]}. Difficulty attribute: '+('present' if ':question/difficulty' in src else 'absent')+'.','']
 if ':question/worked-solution' in src:lines+=['Stored solution:','',src[':question/worked-solution'],'']
 for f in src.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',{}).get(':answer/id');lines+=['Field selection / radio. Complete original bank:','']
  for a in f[':answer-field/choices']:lines+=[f'- `{a[":answer/id"]}`: `{a[":answer/value"]}`; designation '+('correct' if a[':answer/id']==correct else 'incorrect' if correct else 'original designation absent')+'.']
  lines+=['']
 if ':question/answer-fields' not in src:lines+=['Answer-fields attribute absent; no observed response shape may be claimed.','']
lines+=['''## Stage 2 — shared mathematical pattern

For unrestricted real input, a nonzero horizontal frequency/phase change preserves the full sine/cosine image [-1,1]. Multiply this compound inequality by A (reverse both inequalities if negative), add D and reorder its endpoints. The full range is [D-|A|,D+|A|], including both achieved endpoints; the minimum is D-|A|. The requested response changes only the conclusion, not the four-row method.

## Stage 3 — components and complete bank mappings

Prompt components: response demand, output symbol, signed A, nonzero B, complete phase C, trig operator and optional angle unit. Solution components: base trig image, transformed trig image, multiplying/adding prose, ordered rows for unchanged image / scaled image / translated image / ordered function image, then the correct range/minimum conclusion. TeX span masks preserve all original words and row structure at source values; the q-25512 raw scaled rows retain its source error explicitly.

For q-10379 the five complete recipes are [lo,hi] with both endpoints open, both closed, lower open, upper open, and the whole real line, in original choice order. Here lo=D-|A| and hi=D+|A|. For q-65928 the bank in original order is D, |A|, D-|A|, D+|A|, -|A|. For q-10249 it is [D-|A|,D+|A|], [-|A|,|A|], [-1,1], [D-|A|,1], [-|D|,|D|]. The last operation's misconception is not established; the absent correct ref remains absent and independently inferred correct value is recorded outside learner content.

For each choice of q-40977, q-40903, q-41840 and q-41964, numeric component e is mapped to D+q|A| with q=(e-D₀)/|A₀|. This exact affine envelope is extracted from the complete original value, including interval closures, and preserves each bank exactly. It is a numerical interpolation envelope, not a claimed source error recipe. Its uncertainty makes all such raw profiles ineligible for normal sampling. bank-mapping.json records every component coefficient q and full choice value; no unmatched choices are hidden.

Normal profiles are full banks chosen before parameters. `endpoints` follows q-10379 (correct closed interval, open both/lower/upper, real line). `extrema` follows q-65928 (minimum, maximum, midline, ±amplitude). `outer_transform` is authored: correct range, omit translation, negate translation, omit scale, and mistake B for an outer scale. Its entire five-option instance is rejected if any intervals coincide. Degree families require B=1 and therefore cannot use this profile; they use endpoints. No first-valid choice pool is used.

## Stage 4 — reusable masks and constraints

Normal masks preserve the common base/changed-image statements and exactly four ordered inequalities before the conclusion. Each named family varies sin/cos, range/minimum and horizontal form; phase/frequency affect the displayed formula but not task counts. The assessed parameters are signed A and D plus range/minimum demand. Trig aliases, horizontal changes, banks and option orders do not inflate mathematical-task identity. Content identity includes actual prompt, entire solution, difficulty, bank values and omission state, excluding seed/order and unused aliases.

Easy A is a positive integer 1..6; moderate A is a negative integer -6..-1. D is a nonzero integer -8..8. Hard A is a reduced negative noninteger rational with denominator 2,3,4, numerator magnitude ≤12 and amplitude ≤6; D is a reduced noninteger rational with denominator 2,3,4, numerator magnitude ≤16 and magnitude ≤8. Both sampler and explicit calls enforce these bounds. Nonlinear transformations and restricted x domains are excluded. Degree shifts use B=1 and familiar signed 15,30,45,60,90 degree values. Linear forms use B=1..5 and C=-3..3; radian forms use B=1..5 and familiar 0,±π,±π/2,±π/3,±π/4,±π/6 shifts. Every normal template exists at every level, with no progression inside a level.

Raw masks retain the observed integer number forms, original A sign, same bounds, and actual absent attributes. Empty explicit parameter maps are rejected rather than defaulted. Raw original profiles are available only via their documented host level and remain evidence-only.

Hard is an authored missing-level design: the tutorial's A,B,C,D are general constants, prerequisites cover additive/multiplicative compound inequalities, and sibling amplitude/period examples already use rational constants. Small rational A,D add exact fraction arithmetic to the existing reversal-and-translation method without adding a branch. This is not an observed hard classification.

## Source anomalies and repairs/exclusions

- q-10249/q-40977 lack difficulty, worked solution and correct refs. Public raw profiles omit all three. Independently derived answers are [-7,-1] and 2, stored only as author metadata; absent designations cannot count as matched.
- q-25512/q-40908 lack answer-fields. Raw profiles omit that key entirely. Normal authored defaults supply supported five-choice radios; this is not claimed as observed field fidelity.
- q-25512 prompt and first row use sin(3x), but the two central rows use sin(2x). Raw evidence retains both original wrong arguments. The supported correction is to use sin(3x) consistently; normal generation derives all four rows from the actual argument. The final interval [-1,3] is still correct because either nonzero frequency has the same unrestricted range. All nine prompt-derived answers are mathematically supported. Six of seven stored teaching sequences are consistent with their prompts; q-25512 is the one erroneous sequence. Exact stored sequence fidelity remains 7/7.
- Actual decoded adjacent ord-92 pairs are exactly three aligned row separators in each stored solution, and none in prompts. No TeX doubled-command anomaly was found or repaired.
''']
(HERE/'template-extraction.md').write_text('\n'.join(lines))
mapping=[]
for sid,src in g.ORIGINALS.items():
 r0=abs(g.sp.Rational(g.RAW[sid]['A']));d0=g.sp.Rational(g.RAW[sid]['D'])
 for f in src.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:
   nums=re.findall(r'-\s*\d+|\d+',a[':answer/value']);mapping.append(dict(source_id=sid,profile='raw_'+sid,field=f[':answer-field/key'],answer_id=a[':answer/id'],exact_value=a[':answer/value'],envelope_coefficients=[str((g.sp.Rational(n.replace(' ',''))-d0)/r0) for n in nums],recipe='explicit q-10379 closure / q-65928 extrema / q-10249 transform recipes' if sid in ('q-10379','q-65928','q-10249') else 'opaque D+q*abs(A) envelope; evidence-only',complete_value_replayed=True))
(HERE/'bank-mapping.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
(HERE/'plot-extraction.md').write_text('''# Plot extraction and generation

None of the nine practice prompts, stored choices, stored solutions or canonical example references an image. The owning topic introduction does contain a contextual sinusoid asset, but it is neither a problem figure nor an assessment component. Therefore this KP requires no source-plot extraction or generator. Original captures remain unchanged, no image references were rewritten, and Matplotlib/TikZ are not invoked. Plot rating: none. Step 7: no parameter-dependent assets required.
''')
(HERE/'README.md').write_text('''# Sinusoidal range generator

Local draft at basis 1356; stops after steps 3–7. No registration or database operations.

```sh
.venv/bin/python generate/scratch/17592186129124/validate.py
.venv/bin/python generate/scratch/17592186129124/build_evidence.py
.venv/bin/python generate/scratch/17592186129124.py --difficulty all --seed 12 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186129124.py --difficulty moderate --profile raw_q-25512 --format json
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Twelve source-shaped range/minimum × sin/cos × linear/degree/radian families; all supported at all three levels. Normal fields are five-choice radios, from complete method banks. Explicit raw source profiles preserve missing attributes and exact original strings/banks, including the q-25512 error; all raw evidence is ineligible for learning. Exact coverage: 9/9 prompts, 7/7 stored solutions, 7/7 banks (35/35 choices), 5/5 stored correct refs. Missing refs and fieldless records are not native-gradable raw fixtures; five complete original banks and all normal family/profile variations are checked with the native engine. See validation.json for independent printed-math and scope checks, and review.md/review.json for originals and variants.

Hard uses authored small rational scale/translation arithmetic. Task counts exclude horizontal/notation/bank aliases: easy 96 range + 76 minimum, moderate 96 + 76, hard 1080 + 1016. Source difficulty overlaps are preserved, while normal authored bounds distinguish easy positive integers, moderate negative integers and hard negative noninteger rationals.

Generator version 1.0.0 frozen for parent QA. Validation records actual Python/SymPy versions and native executable hash. No plots required.
''')
(HERE/'freeze.json').write_text(json.dumps(dict(version=g.VERSION,script_sha256=hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),validation_sha256=hashlib.sha256((HERE/'validation.json').read_bytes()).hexdigest(),steps_completed=[3,4,5,6,7],stage='frozen for parent QA; not registered',database='math',basis=1356,lineage=g.SOURCE['lineage']),indent=2)+'\n')
