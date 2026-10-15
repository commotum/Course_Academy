import sys
sys.dont_write_bytecode=True
import importlib.util,json,hashlib,shutil
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('gdoc',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ROOT=H.parents[2]
ref=H/'reference';ref.mkdir(exist_ok=True)
for p in [ROOT/'generate/principles.md',ROOT/'docs/math-content.md',*sorted((ROOT/'generate/docs').glob('[3-7]-*.md'))]:shutil.copyfile(p,ref/p.name)
classification='''# Classification (basis 2275)

Registered numeric generator and entire numeric tree are immutable. `registered-baseline.json` records complete original paths and SHA256 hashes, including existing caches, before imports. All imports set `sys.dont_write_bytecode=True`; private formatter and scalar parser are loaded by exact file paths. No registration, database, engine, or shared manifest changed.

Actual topic 3562 is Finding Equations of Perpendicular Lines. Lesson linked order: Introduction → Finding the Equation of a Perpendicular Line (17592186175922) → through two points (17592186175923) → this KP (17592186175924). Introduction teaches negative reciprocals, not differentiation. KP key prerequisite: Properties of Lines Given in Standard Form (topic 3725 / 17592186049201). Previous topic is Perpendicular Lines in the Coordinate Plane; successors include Thales, normal lines using differentiation, tangents, and shortest distance. None of those successor skills enters this generator. `topic.json`, `lesson.json`, and `source.json` preserve the actual evidence.

Nine MA practice sources: seven complete and two missing key/solution (q-214033 also lacks its bank). Three nonMA inventory rows are separately retained as `nonma-inventory.json` standard questions/record wrappers and never treated as MA source evidence. Canonical e-14730 supports scope, not practice counts.

Easy: one standard-form reference → slope-intercept blank family (separate expansion/zero-point templates) and one radio family finishing standard form. Moderate: reference through two points → standard-form radio; separate source arithmetic/solution stage sequences and complete-bank profiles. Hard: no observed sources; conservative authored counterparts of all moderate families at the SAME workload and integer slot domain, explicit origin on every record. No within-level progression and no extra skill to justify a hard label.

Plots: none for all nine practice sources and all authored variants. The introduction's illustration is context, not a required question plot. No assets generated.

| Source | Level | Field | Complete bank | Solution |
|---|---|---|---|---|
'''
for s,q in g.SOURCES.items():
 f=q[':question/answer-fields'][0];classification+='|'+s+'|'+g.source_level(s)+(' (inferred completion)' if s in g.INCOMPLETE else '')+'|'+f[':answer-field/type'][':db/ident'].split('/')[-1]+'|'+str(len(f.get(':answer-field/choices',[])))+' values|'+('missing, authored completion separate' if s in g.INCOMPLETE else 'raw and normalized exact replay')+'|\n'
(H/'classification.md').write_text(classification)
extraction='''# Template extraction

Fidelity and source-error handling: `raw-source-replay.json` reproduces every MA attribute exactly, including raw TeX, absent data, original bank ordering, correct markers and source difficulty. Raw records are evidence-only and never serving eligible. Seven complete cases serve normalized prose/math at original parameters with the full observed bank and exact ordered source solution; `source-replay.json` compares complete equations up to nonzero scalar multiplication. Two incomplete cases have separately authored solutions/keys, and q-214033 an authored blank answer and supported repair separating its run-together question punctuation and y= blank layout. No completion is represented as captured evidence. All source and complete authored solutions appear side-by-side in `review.md`; `sourcecases.json` includes original+two variants for each of the nine families, plus three examples for each hard family.

Backbone: extract the supplied reference slope (standard form, or the slope formula on two integer points), take its negative reciprocal, use the actual supplied target point in point-slope form, expand and isolate y, and finish standard form only where the source does. Real coordinate plane. Source slopes are finite and nonzero; A,B are both nonzero because horizontal/vertical lines require a different solution branch absent from these sources and introduction. This scope restriction is independent of grading; the complete-equation comparator itself supports both axes. Target coordinates and answer intercepts can be zero or one. No arbitrary exclusions for valid 0/1 answers.

Declared variable slots: reference standard coefficients A,B independently chosen nonzero integers [-7,7], C integers [-12,12]; target px,py independently [-9,9]. For the two-point family reference point 1 is independently in [-5,5]^2 and dx,dy independently nonzero integers [-7,7]; point 2=point 1+(dx,dy), A=dy, B=-dx, C=A*x1+B*y1. Parameters passed explicitly use integers of absolute magnitude at most 100 for A,B,C,px,py and must preserve all structural relations. All references, slopes, banks and worked equations are derived from the same slots. Reference orientations and both point coordinates vary; translation alone is insufficient novelty. Within each source-template family, all variations keep the same reasoning stages/workload. Arithmetic formatting may repeat an equal stage, preserving the source's explicit stages rather than deleting a source row as redundant.

Every bank is chosen as one complete source profile BEFORE sampling. One profile per radio source (four total, including incomplete q-23633); no pooled recipes or first-valid subsets. Define old perpendicular normal (a0,b0)=(-B0,A0), new (a,b)=(-B,A). For each complete observed option (oa,ob,oc), derive na=oa*a/a0, nb=ob*b/b0, residual=oc-oa*px0-ob*py0, nc=na*px+nb*py+residual. Clear all coefficient denominators by their positive LCM and render the entire equivalent integer standard equation na*x+nb*y=nc. This exact incidence-residual transport is an authored, conservative algebraic extension of observed coefficient patterns. Its psychological interpretation is unresolved; it is NOT claimed to identify particular learner misconceptions. Full-bank collisions/extra-correct choices reject the entire instance. Source replay retains the original notation; variants use normalized exact coefficients. Blank profiles have no distractors, and retain RHS-only y= contract.

Per-source complete mappings below give original point/reference, prompt, each full equation, exact na/a and nb/b multipliers, and constant residual. These are complete recipes, not qualitative labels. Raw worked prose and all ordered equations remain in source.json and the review, not replaced by the recipe summary.

'''
for s,q in g.SOURCES.items():
 p=g.original(s);f=q[':question/answer-fields'][0];extraction+='## '+s+'\n\n'+q[':question/problem']+'\n\nParameters: `'+json.dumps(p)+'`. Field '+f[':answer-field/key']+' / '+f[':answer-field/type'][':db/ident']+'.\n\n'
 if f[':answer-field/type'][':db/ident'].endswith('/radio'):
  extraction+='| Observed full option | na/a | nb/b | residual | Captured key |\n|---|---|---|---|---|\n'
  for a in f.get(':answer-field/choices',[]):
   oa,ob,oc=g.line(a[':answer/value']);extraction+='|`'+a[':answer/value']+'`|'+str(oa/(-p['B']))+'|'+str(ob/p['A'])+'|'+str(oc-oa*p['px']-ob*p['py'])+'|'+str(a.get(':answer/id')==f.get(':answer-field/correct',{}).get(':answer/id'))+'|\n'
 else:extraction+='Observed RHS: '+('`'+f[':answer-field/choices'][0][':answer/value']+'`' if f.get(':answer-field/choices') else 'missing (authored completion `3x-8`)')+'.\n'
 extraction+='\nOrdered source solution (missing remains missing here):\n\n'+q.get(':question/worked-solution','**Missing: authored completion is separate.**')+'\n\n'
(H/'template-extraction.md').write_text(extraction)
(H/'plot-extraction.md').write_text('# Plot extraction and generator (docs 5 and 7)\n\nNone. All supplied question/answer/solution content is algebraic text; no question plots or plot-dependent parameters. No images, SVG, Matplotlib or TikZ output is needed. Lesson introduction image is unchanged context and is not copied into practice questions.\n')
(H/'template-generator.md').write_text('''# Implementation and verification (doc 6)

`../17592186175924-draft.py` is the private entry point. `generate(level,seed,template,parameters)`, `batch(level,count,seed)` and CLI JSON/Markdown previews support easy, moderate and hard. Frozen parser/formatter reside in this tree, explicit imports only; source basis 2275. SymPy exact arithmetic and seeded randomness. Public generate is checked by the frozen official math-content decorator.

Content identity hashes the actual normalized prompt, ordered worked solution, field key/type, full unordered rendered answer bank, and correct rendered answer. Thus authored bank changes cannot collide under a prompt-only identity. Answer identities belong to each field. Mathematical task identity separately hashes reference orientation (normalized A,B with irrelevant reference intercept omitted), actual target point, perpendicular role, response shape and real domain; it excludes scaling, notation, seed and bank order. Batch deduplicates this identity. Varying only source intercept is not novelty.

`validate.py` independently reads the printed supplied coefficients/two points, target point, perpendicular role, every numerical worked equation and all full answer equations. It proves incidence and negative reciprocal direction, checks wrongs individually and mutual nonequivalence, and checks source-specific stage counts. Mutations independently alter the displayed actual point, supplied coefficient, perpendicular direction, and erase a still-correct equality stage; all are rejected. It also checks exact 0/1 intercepts, all nine raw-attribute replays, complete banks/keys, seeded deterministic contents, sourcecases, slot coverage, and immutable numeric path/hash baseline. 150 distinct instances per level plus 39 original/variant sourcecases are checked.

Native frozen check-engine SHA256 `71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea` exercises every owned answer ID separately from malformed/foreign submissions, exact/equivalent blank RHS expressions, full equations as unsupported RHS-blank response shapes, wrong intercept/direction and a rational expression with a hidden domain hole. True native limitations are retained: unsupported full-equation response shapes and invalid erased-domain rational expressions yield unresolved. Canonical and equivalent valid RHS expressions are accepted. No valid generated answer is pruned or changed to hide a limitation. Hard is authored, never claimed source-fidelity evidence. No database writes or registration.

Run: `.venv/bin/python generate/scratch/17592186175924-draft/validate.py`. CLI example: `.venv/bin/python generate/scratch/17592186175924-draft.py --difficulty hard --seed 2275 --count 3 --format markdown`.
''')
(H/'README.md').write_text('''Private review pair only; registered numeric pair untouched. See classification.md, template-extraction.md, plot-extraction.md, template-generator.md, source-replay.json, sourcecases.json, review.md, validation.json and native-grading.json. Raw MA evidence and nonMA existing inventory remain separate. Two incomplete source cases have authored completions. All E/M/H served; hard is conservative authored moderate-workload practice because no hard source exists. Full equations in RHS-only blanks are unsupported response shapes; not hidden or pruned.
''')
for p in H.glob('probe-*.json'):p.unlink()
