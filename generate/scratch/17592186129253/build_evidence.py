import json,hashlib,importlib.util,re,shutil
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
paths=['generate/runs/current/worker-instructions.md','generate/principles.md']+[f'generate/docs/{x}' for x in ['3-classify.md','4-template-extraction.md','5-plot-extraction.md','6-template-generator.md','7-plot-generator.md']]+['generate/runs/current/candidates.json','generate/runs/current/manifest.json','generate/runs/current/sources/17592186129253.json','generate/runs/current/topics/17592186050601.json','generate/runs/current/lessons/17592186050601.json','generate/runs/current/README.md','generate/runs/current/check-engine.rs','/home/jake/Developer/MA/DATA/Lessons/2049/Source/2049.json','/home/jake/Developer/MA/DATA/Lessons/88/88.md']
manifest={'database':'math','basis':1356,'lineage':g.SOURCE['lineage'],'read_files':[{'path':p,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in paths],'original_assets_inspected_full_resolution':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dimensions':list(Image.open(p).size)} for p in sorted((HERE/'originals').glob('*.png'))],'owning_topic':{'db_id':17592186050601,'ma_id':2049,'title':'Graphing General Polynomials'},'prerequisite':{'db_id':17592186048669,'ma_id':88,'title':'Multiplicities of the Roots of Polynomials'},'lesson_step_order':[17592186129995,17592186130184,17592186130009,17592186129998,17592186130000],'order_basis':'activity/first-step followed by step/next; not Pull collection order','unrated_widget_findings':'Original MA snapshot confirms five radio choices; no solution/key revealed. Missing correct classifications independently inferred from original red-curve behavior, not claimed as observed keys.'}
binary=Path('generate/runs/current/check-engine');manifest['native_grader']={'binary':str(binary),'sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'entry_point':'course_academy_engine::learning::grade_field','memory_only':True}
(HERE/'read-manifest.json').write_text(json.dumps(manifest,indent=2))
for kind in ['topics','lessons']:shutil.copy(f'generate/runs/current/{kind}/17592186050601.json',HERE/(kind[:-1]+'-context.json'))
raw=json.load(open('/home/jake/Developer/MA/DATA/Lessons/2049/Source/2049.json'))
def walk(x):
 if isinstance(x,dict):
  if x.get('question_id') in ['140411','140414']:yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
(HERE/'unrated-authoritative-widgets.json').write_text(json.dumps(list(walk(raw)),indent=2))
(HERE/'classification.md').write_text('''# Classification — frozen math basis 1356

KP17592186129253, “Identifying Multiplicity of a Root Given a Graph,” belongs to topic2049 “Graphing General Polynomials.” Source wrapper lineage is `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. All seven practice records are included: five labeled easy and two unrated. All have one `selection` radio field with five text options. Five have worked solutions/correct designations; two omit difficulty, solution and correct designation. Canonical e-9941 has an inline three-statement demonstration and no assessment fields.

| Observed level | Backbone | Bank | Count | Plot rating |
|---|---|---|---:|---|
| easy | One named root in local sketch; simple/non-tangent, even/tangent/bouncing, odd/tangent/crossing | Five categorical predicates |5|heavy|
| unrated | Same local graph response | Same five predicates, original spacing profiles |2|heavy|
| moderate | No observed practice | Authored two-root integer context |0 observed|heavy|
| hard | No observed practice | Authored three-root half-integer context |0 observed|heavy|

The common identification template has three conditional operative solution paths: simple, even multiple, odd multiple. Each path retains the same reference table/rules, then applies tangent and crossing/bouncing observations to exactly one root. Distinct original root values and given/shown prose are slots, not different mathematical skills. All seven complete source banks have the same five logical predicates. Original notation styles are retained as replay profiles.

The graph supports the category “even multiple” or “odd multiple,” not an exact exponent above one. Renderer representative exponents2/3 do not enter the learner's supplied information or requested answer. No polynomial equation, degree, coefficient, end behavior or other roots' classifications are requested.

Raw replay is evidence-only and preserves omissions. Completed profiles independently infer q-140411 as simple and q-140414 as even multiple, assign easy as an authored level, and supply a source-style solution. Those two inferred keys do not count toward observed key fidelity. No mathematical repair is required in the other five sources.
''')
lines=['# Template extraction','', '## 1. Describe each original','', '|Source|Observed rating|Target|Visible local cue|Original solution/key|', '|---|---|---|---|---|']
for sid,q in g.QUESTIONS.items():
 r,m,o=g.SOURCE_DATA[sid];c=g.category(m);cue=('non-tangent crossing' if c=='simple' else 'tangent, touches/reverses' if c=='even' else 'tangent crossing')+(('; above axis' if o>0 else '; below axis') if c=='even' else ('; increasing' if o>0 else '; decreasing'))
 lines.append(f'|{sid}|'+('easy' if ':question/difficulty' in q else 'unrated')+f'|{r}|{cue}|'+('present' if ':question/worked-solution' in q else 'both absent')+'|')
lines+=['','All prompts consist of a360px wide local red polynomial sketch, one labeled intercept and a horizontal arrowed x-axis, then the identical statement-selection question with “given” or “shown.” No y-scale is provided. All fields are radio, key `selection`, five text choices. The two unrated sources have complete banks but no observed correct designation.','', '## 2. Generalize the shared pattern','', 'Locate the root named by each choice, determine whether the curve is tangent to the x-axis, then if multiple determine whether it crosses (odd) or touches/reverses (even). Return one categorical statement. A simple-root solution ends after the non-tangent conclusion; a multiple-root solution has distinct tangent, parity and final conclusion paragraphs. Higher multiplicity is underdetermined.','', '## 3. Map every original component and option','', 'The table below is a complete35-choice mapping, including every incorrect option. The predicate recipes parameterize the target root; no numeric distractor fits or unrelated perturbations are used. A misconception interpretation is recorded only when structurally evident.','', '|Source|Field|Original option|Predicate recipe|Original key?|', '|---|---|---|---|---|']
for sid,q in g.QUESTIONS.items():
 f=q[':question/answer-fields'][0];correct=f.get(':answer-field/correct',{}).get(':answer/id')
 for a in f[':answer-field/choices']:
  val=a[':answer/value'];key=next(k for k,z in g.SUFFIXES.items() if val.endswith(z))
  recipe={'simple':'Multiplicity1; overlook flattening if wrong','even':'Multiple and even; confuse bouncing/crossing if wrong','odd':'Multiple and odd; confuse bouncing/crossing or simple/multiple if wrong','not':'Deny the marked intercept is a root','impossible':'Conjoin simple(m=1) and even(m even), an impossible source misconception'}[key]
  lines.append('|'+sid+'|selection|'+val+'|'+recipe+'|'+('yes' if a[':answer/id']==correct else 'no' if correct else 'missing designation')+'|')
lines+=['','## 4. Stable backbone, slots and guards','', 'Fixed: one categorical target, source five-predicate radio bank, original reference table/rules, exact conditional operative solution paths. Source bank selected whole before parameters, correct category computed first, all required other predicates derived next, then any semantic collision rejects the complete instance. No first-valid option pooling. All pairs compare their multiplicity sets; two different false statements are not equivalent merely because both are false for one graph.','', '|Slot|Meaningful domain|Dependencies|', '|---|---|---|', '|target root/position|easy integer−9..9; moderate two integers−6..6; hard three strict half-integers−13/2..13/2|axis tick, all five choices, every conclusion, plot and fingerprint|', '|local category|simple, even multiple, odd multiple|curve vanishing order, tangent/parity solution, correct choice|', '|orientation|±1|curve side signs; no change to category|', '|visible context|easy1 root; moderate2 different categories; hard3 all categories|overview plot and target-selection reading demand|', '|target index|any visible root, sorted canonical ordering|all references and local panel|', '', 'Separation≥3 for moderate/hard; level guards apply identically to sampler and explicit parameters. Moderate always has two integer roots and different categories. Hard always has three strict half-integer roots and all categories. Neither can reproduce easy, and hard cannot reproduce moderate. All within-level variants have the same number-form, context-selection and tangent/parity demand; no progression is encoded. Integer bounds include the observed signed/zero-nearby root forms and extrema−5,9. Half-integer axis reading is a conservative authored number-form extension anchored to prerequisite88’s rational roots (±2/3 and ±1/2), not a recovered source parameter.','', 'Lesson order is Introduction → this KP → true statements regarding graphs → factored-polynomial recovery → graph selection. This KP stops at its first graph-reading step. Sibling canonical e-5814 demonstrates three root types, supporting two/three-root visual context, while equation recovery, end behavior and multi-statement selection remain outside scope. Authored moderate adds locating one named root among two integer intercepts; authored hard uses three signed half-integer intercepts and matching the target to its local view. The local panel aids flatness visibility without adding a calculation.','', 'Finite meaningful task catalogs enumerate positions/configurations, category assignment, orientation and target. Positive amplitude, representative higher exponents, seed, shuffle, source/profile and notation aliases never count toward mathematical variety. Canonical sorting normalizes root-order spelling. Content identity separately includes actual prompt, full bank, fixed solution and supplied difficulty.','', 'Raw profiles are `raw-q-…`, completed profiles `completed-q-…`, default `observed-five`. Raw original omissions are maintained at changed parameters as well. Only original anchor assets are reused; changed parameters invoke normal rendering, shared solution construction and categorical banks. No literal source-payload/answer lookup branch exists.']
(HERE/'template-extraction.md').write_text('\n'.join(lines)+'\n')
(HERE/'plot-extraction.md').write_text('''# Plot extraction and specification

## 1. Original plots

All14 raster assets were opened individually at their full native resolution, including all eight prompt plots (seven practice and canonical e-9941) and six reference sketches in every worked solution. There are no graphical answer options; all35 practice options were inspected as text. Prompt root values: canonical−4 below-axis bounce; q1404113 decreasing non-tangent crossing; q140414−2 above-axis bounce; q141133−1 increasing flat crossing; q141137−5 decreasing flat crossing; q1411429 broad increasing flat crossing; q1411446 above-axis bounce; q141140−3 increasing non-tangent crossing. Exact dimensions/hashes appear in read-manifest.json. Source reference table shows both orientations for simple crossings, both above/below bounces for even multiple roots, and both orientations of flattened odd crossings.

Every prompt uses a red curve, black horizontal arrowed x-axis labeled x at the right, one labeled root and a small root tick, white/transparent background, no y-axis and no numeric y-scale. No endpoint is marked as included/excluded; these are cropped parts of graphs, not domain endpoints. Approximate shared prompt intercept raster location is x169,y88.5 for the taller seven practice sketches; individual source-raster checks independently measure the red curve there, both side signs40px away and tangent slope18px across. Canonical has its horizontal axis near the top with the below-axis bounce. Reference sketches have no numeric root label. No exact polynomial equation or higher exponent can be inferred from these unscaled images.

## 2. Shared visual pattern

A local polynomial-root sketch supplies exactly the non-tangency/tangency and crossing/bouncing cue required for qualitative multiplicity classification. Original assets can be reused only at their exact replay anchor. Changed roots/categories/configurations require a new plot. Heavy plot rating: the plotted local behavior is the problem's operative information.

## 3. Components

Fixed: red polynomial curve, true horizontal y=0 axis with right arrow/x label, readable root ticks, white background. Variable: exact root coordinates, local multiplicity class, vertical orientation and two/three-root context. Optional conditional component: target-local panel for moderate/hard. Every panel derives vertices from precisely the same polynomial; independent vertical scales are allowed because no y-value is assessed. Axis transforms, sample vertices, polynomial and PNG hash are recorded in atomic JSON sidecars. Positive vertical amplitude is unsupported and excluded from fingerprints.

## 4. Reusable renderer

Matplotlib only, Agg backend,150dpi; easy7.2×3.1 inches, moderate/hard7.2×5.1 inches. Source simple crossings use a monotonic cubic representative t(1−t²/12) restricted to |t|≤2 so no extra zero is shown. Other single roots use signed t² or t³ representatives. Multi-root curves use the exact product of distinct-root factors with representative orders1/2/3. These exponents create the assessed categories and are never assertions about hidden source exponents. Overview spans the visible roots plus2units at either side. Local view spans target±0.85, well inside the separation≥3 guard. Each panel includes its exact roots as vertices; red vertices are checked against independent evaluation and the actual PNG under the saved axes transform. Zero-line alignment is separately checked. The y-axis is drawn at x=0 only when0 lies in that panel, and roots/zero tick labels use exact signed rational TeX.

Atomic unique temporary PNG/sidecar files support simultaneous identical/different instances. Both cache files must exist; no image cache is pruned while QA may be reading. Matplotlib state is isolated per-process for concurrency verification. Generated easy/moderate/hard and signed/rational target panels were visually inspected; curves/tick labels are legible, arrow/x labels have reserved right-side space, and local panels preserve the original local category while avoiding global-scale flattening.

Fidelity does not claim raster reconstruction of an unknown equation: exact original PNGs are retained/reused at anchors. Changed-source representative plots faithfully preserve root position, orientation and qualitative crossing/bouncing/flatness. Source raster sign/slope checks are independent from generated SymPy checks and native radio grading.
''')
(HERE/'README.md').write_text('''# Root-multiplicity graph generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186129253/validate.py
.venv/bin/python generate/scratch/17592186129253.py --difficulty all --seed 2 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186129253.py --difficulty easy --profile raw-q-140411 --format json
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and easy/moderate/hard convenience functions. Parameters are `roots`, `multiplicities` (representative1/2/3), `orientation`±1, `target` index. Explicit level guards are described in template-extraction.md. No database writes, registry changes or commits.

Seven original full banks35/35 options replay, five present solutions and five present correct designations. Raw profiles preserve the two unrated sources’ missing difficulty, solution and key. Completed profiles infer those two classifications from the original plots and explicitly author their fields/level/solution. Raw records are evidence-only. Moderate and hard are authored context/coordinate-reading extensions of one categorical target; exact higher exponents and complete polynomial recovery are outside scope. Review.json/Markdown show originals, changed original profiles, and at least three variants per level. Validation.json separates source fidelity, inferred completion, independent mathematics/raster checks and real native grader outcomes. Parent independent QA remains required.
''')
(HERE/'review-notes.md').write_text('''# Worker review

Checked all14 original plots at full resolution, all35 answer options, exact original presence/prose and operative solution paths. Checked rendered easy/moderate/hard side by side. The original qualitative response cannot establish exponent3 vs5 or2 vs4; outputs consistently use categorical statements. Missing native keys remain explicit in raw evidence; completed inference is separately labeled. Source plots are not silently fit to exact polynomial equations.

The moderate/hard distinction is an authored curriculum design: two integer versus three strict half-integer named intercepts, same tangent/parity method. It introduces visual location/scale workload, not a new algebraic branch or within-level progression. Source literal bank and five-option count remain intact. Mathematical equivalence compares the actual categorical response predicates including wrong/wrong pairs. The contradictory simple-even source option is preserved as the empty multiplicity set rather than being renamed or silently deleted.

Completion requires parent QA of these design claims and the independent source/plot/native validation. No unresolved source bank mappings or unexpected native grading failures may be concealed.
''')
# Decoded-byte inspection, not JSON-print escaping.
strings=[q[k] for q in g.QUESTIONS.values() for k in [':question/problem',':question/worked-solution'] if k in q]+[a[':answer/value'] for q in g.QUESTIONS.values() for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
(HERE/'decoded-source-format.json').write_text(json.dumps({'strings_examined':len(strings),'adjacent_backslash_pairs':sum(z.count('\\\\') for z in strings),'unintended_c0':sum(sum(ord(c)<32 and c not in '\n\t' for c in z) for z in strings),'tex_repair_claimed':False},indent=2))
print('Evidence built')
