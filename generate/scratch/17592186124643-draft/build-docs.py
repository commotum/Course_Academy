"""Build source-specific extraction and role/workload evidence."""
import sys;sys.dont_write_bytecode=True
import hashlib,importlib.util,itertools,json
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[2]
s=importlib.util.spec_from_file_location('kp124643_docs',D.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
source=json.loads((D/'source.json').read_text());qs=source['record'][':knowledge-point/questions'];specs=list(g.TEMPLATES.values())
classification='''# Classification

Immutable Math database basis 2275, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. `source.json`, `topics.json`, and `lessons.json` are exact frozen refresh-2026-10-14 wrappers. Twelve Math Academy identified practice records: six easy, five moderate, one unrated. No independently authored captured practice. Canonical e-11045 is separate evidence and is never counted as practice. The original MA lesson widget JSON is in reference/ma-lesson-1929.json.

All twelve records have one five-option radio field, with no source feedback. There are twelve mathematical/layout families and twelve complete observed bank profiles; each owns all five options. No plots occur. The unrated x sqrt(y) record lacks difficulty, correct reference, and worked solution; these omissions remain present in public observed replay. Its fourth captured option is independently the defining y quotient, and normal output receives a clearly authored easy assignment, key and solution.

| Source | Difficulty | Family | Target role | Plot |
|---|---|---|---|---|
'''
for q,sp in zip(qs,specs):classification+='| '+sp['source_id']+' | '+(sp['level'] if sp['source_difficulty_present'] else 'unrated; authored easy normal')+' | '+sp['template']+' | increment '+sp['target']+', hold '+('y' if sp['target']=='x' else 'x')+' | none |\n'
classification+='''
Hard has no observed practice. Its two authored families specialize observed monomial and sine-product quotients at an ordered point. The learner still forms a quotient limit; the limit is never evaluated using a derivative rule. The additional work is substituting the target coordinate plus h and the held coordinate into each function occurrence. This is a design claim, not recovered source difficulty.
'''
(D/'classification.md').write_text(classification)
text='''# Template extraction

## 1. Specific original descriptions

Every original is reproduced in review.md and source-replays.json. Raw records are in source.json and all sixty exact answer values, field ownership, designation presence and parameterized masks are in bank-map.json. Original display syntax, including the ASCII sqrt limit syntax and the source's f(x) versus f(x,y) prose mismatch, is retained by observed evidence profiles. Normalization uses the frozen shared math_format.py before IDs. No distractor diagnosis or feedback is fabricated.

'''
for q,sp in zip(qs,specs):
 text+='### '+sp['source_id']+' — '+sp['template']+'\n\n'+q[':question/problem']+'\n\n'
 text+='Anchor parameter slots: `'+json.dumps(sp['anchor'])+'`. Target `'+sp['target']+'`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. '
 if sp['source_solution_present']:text+='The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says '+('“The partial derivative”' if sp['level']=='easy' else '“The derivative”')+'. '
 else:text+='Difficulty, solution and correct designation are absent. The original MA widget confirms the five-choice layout but supplies no recovered key or solution. '
 text+='All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.\n\n'
 for i,mask in enumerate(sp['bank_masks']):text+='- '+str(i+1)+': `'+mask+'`'+(' (captured correct)' if i==sp['correct_index'] and sp['source_correct_present'] else ' (independently correct, captured key absent)' if i==sp['correct_index'] else '')+'\n'
text+='''
## 2. General mathematical backbone

Given a two-input function and a requested partial derivative, replace only the target input by target+h. Hold the other input fixed. Subtract the original complete function value, group that numerator, divide the complete difference by the same h, and place it under lim h→0. The answer is the entire unevaluated limit expression. Expressions that both lack a finite limit are not interchangeable answers to a request for a particular defining difference quotient: banks are compared as full increment expressions before taking the limit. No derivative rule, cancellation, rationalization or limit-evaluation stage is added.

All observed normal families retain their original three operative display stages and shared sentences. Normal output minimally changes f(x) to f(x,y) in source prose, canonicalizes visible partial/limit notation, and adds one explicit h≠0 / held-variable sentence after the chain. Raw observed replay keeps the exact normalized original sentences and absent attributes. Source q-158413 normal completion uses the same three stages and labels them authored. One concrete solution depends only on the instance and never on the learner response.

## 3. Components and bank mapping

bank-map.json accounts for every source option one-to-one, including four wrong options in each keyed bank and all five unkeyed root-product options. templates.json holds extracted masks only, not completed question records or a source-payload return branch. Every ordinary and replay record runs through fill, role substitution, parameter validation, normalization and field-owned record assembly. Anchor replay is not a special case. Source difficulty, solution and correct-key presence are separate flags; the unkeyed record cannot count toward designation matches.

The malformed-looking `x+2yy` exponential distractor is algebraically readable as x+2y², but its pedagogical operation is underdetermined. Its exact full expression pattern is public ineligible observed evidence, with c replacing every coupled2. Normal method output uses a declared complete bank that replaces only that option by shifting the held coordinate y+h in b^(x+cy). This is an authored bank extension, not a recovered error intention. All other source banks use their complete parameterized expression patterns. Wrong options never have invented learner-facing explanations.

## 4. Reusable templates, slots and constraints

Fixed: two variables; one target and one held role; one five-option radio bank; subtraction/division/limit order; increment h; exactly the original three operative display blocks (except the source's absent solution); the family-specific operators and nested expression positions. Variable: each documented numeric slot and an optional simultaneous x↔y role relabeling. Function signatures always remain ordered f(x,y); after role exchange f(x+h,y) becomes f(x,y+h). Command names and ordinary prose words are protected. Coordinate entries are never globally replaced across prose. The role swap is exercised for correctness but is not counted as another meaningful mathematical task.

'''
for name,sp in g.TEMPLATES.items():
 domain={k:[min(v),max(v)] for k,v in g.DOMAINS[name].items()}
 text+='- `'+name+'`: '+json.dumps(domain)+'. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. '
 if not domain:text+='Its source backbone has no numeric slot; it is retained as a supported finite family and is not inflated by variable-letter aliases. '
 text+='\n'
text+='''
Hard point_monomial preserves a·target²·held. Coordinates lie in {−3,−2,−1,1,2,3}; nonzero coefficient magnitude is at most5; enforce |a·target_coordinate²·held_coordinate|≤24 on explicit and sampled inputs. Every full signed function value is grouped before numerator subtraction, so negative source-point values cannot create ambiguous adjacent signs. The target-coordinate square is at most9 and absolute original complete value at most24; no high-power expansion or derivative evaluation is introduced. Hard point_sine preserves sin(xy), coordinates in {−3,−2,−1,1,2,3} with unequal entries, so their product has absolute value at most9 and both source-shaped increment errors remain distinct. Trigonometric values remain exact symbolic values, with no new trig evaluation skill. Both hard families retain formal quotient / concrete supplied-point substitution / final quotient stages. All bounds apply to public explicit calls. Equal sine coordinates reject the whole bank because target-only and other-only shifts collide; an individual option is never replaced after sampling.

Meaningful fingerprints canonicalize target/held roles and functions up to held-only additive terms (using symbolic derivatives only for internal deduplication, never learner solution steps) for symbolic tasks and the point-specialized increment expression for hard tasks. Variable-letter, seed and answer-order changes do not create another assessed task. Presentation identity includes difficulty, version, complete prompt, complete solution and full displayed bank; fields and answers own stable UUIDs. Distinct banks cannot share content identity. Runtime versions are recorded from the actual process.

No plots: plot-extraction.md records a none rating. No generation or validation step reaches EDB, a numeric registered script, shared caches, engine sources or the manifest.
'''
(D/'template-extraction.md').write_text(text)
(D/'plot-extraction.md').write_text('# Plot extraction\n\nRating: **none**. All twelve original prompts, sixty choices, eleven supplied solutions, the canonical example and generated families are symbolic prose/math only. No plot assets, parameters, or raster regeneration are needed.\n')
rows=[];counts={}
for name,sp in g.TEMPLATES.items():
 keys=list(g.DOMAINS[name]);tasks=set()
 for vals in itertools.product(*(list(g.DOMAINS[name][k]) for k in keys)):
  r=g.generate(sp['level'],template=name,parameters=dict(zip(keys,vals))|{'swap':False});tasks.add(r['generation']['mathematical_fingerprint'])
 counts[name]=len(tasks);rows.append({'template':name,'level':sp['level'],'meaningful_tasks':len(tasks),'not_counted':'seed, bank order, x/y aliases'})
for name in ['point_monomial','point_sine']:
 tasks=set();valid=0
 for X,Y,swap,a in itertools.product([-3,-2,-1,1,2,3],[-3,-2,-1,1,2,3],[False,True],[-5,-4,-3,-2,-1,1,2,3,4,5] if name=='point_monomial' else [1]):
  p={'X':X,'Y':Y,'swap':swap}|({'a':a} if name=='point_monomial' else {})
  try:r=g.generate('hard',template=name,parameters=p)
  except ValueError:continue
  tasks.add(r['generation']['mathematical_fingerprint']);valid+=1
 rows.append({'template':name,'level':'hard','meaningful_tasks':len(tasks),'eligible_parameter_tuples':valid,'not_counted':'equivalent point-specialized quotients, seed, bank order, variable aliases'})
levels={l:sum(r['meaningful_tasks'] for r in rows if r['level']==l) for l in g.LEVELS}
(D/'domains.json').write_text(json.dumps({'families':rows,'meaningful_tasks_by_level':levels,'scope':'Finite enumerated conservative same-method domains; no notation/seed/order aliases counted.'},indent=2)+'\n')
(D/'README.md').write_text('''# Partial-derivative quotient draft

Run from repository root:

```sh
.venv/bin/python -B generate/scratch/17592186124643-draft/validate.py
.venv/bin/python -B generate/scratch/17592186124643-draft/render.py
.venv/bin/python -B generate/scratch/17592186124643-draft.py --difficulty all --seed 4 --count 2 --format json
```

The CLI emits a bare JSON list or complete Markdown questions, options, correct designations, difficulty labels and worked solutions. Default profiles are supported learning records. `--profile observed` is public evidence-only raw replay preserving absent source attributes; it is not eligible learner material. Parameters and source cases replay through the ordinary generator, never a completed-payload shortcut.

Source wrappers are immutable basis2275. Twelve original MA practice records /60 source options /12 complete banks;11 captured keys and11 captured solutions, with the remaining absences preserved. Canonical example is checked separately. Authored normal completion repairs the unkeyed root product, and hard specializes two source families to an ordered point without evaluating the limit. See classification.md, template-extraction.md, bank-map.json, domains.json and review.md.

Independent validation parses actual displayed prompts, every formal and substituted expression and every bank member. All ten pairs in each five-option bank are checked, not only correct/wrong comparisons. Native provenance verifies42 hashes from the current33510bf3 grader build. Native checks select every actual option; they do not claim mathematical parser grading of arbitrary entered limits. UI rendering uses the actual radio-control and Markdown/MathJax functions, clicks a real control and reveals the entire solution. No plot generation is needed.

The pre-import immutable-baseline.json proves the numeric script/tree and sibling bytecode paths were absent; registration-context.json records the frozen dispatch's queued/no-generator state. Final verification checks the complete pathset remains absent. No DB transactions, engine changes, registrations, manifest edits or commits. Root approval remains pending.
''')
print(json.dumps({'meaningful_tasks_by_level':levels,'family_counts':rows},indent=2))
