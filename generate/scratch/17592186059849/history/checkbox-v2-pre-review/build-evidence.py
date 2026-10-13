#!/usr/bin/env python3
import collections,importlib.util,json,re
import sympy as sp
from pathlib import Path
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Recover individual option expressions from retained legacy-bank recipes.
# Current database correct references always remain the key authority.
legacy=json.loads((P/'history/basis-1356/source.json').read_text())
checkbox={}
for sid,d in g.DEFS.items():
 if d['kind']!='checkbox':continue
 m,det,poly,roots,env=g.build(sid,g.parameters(sid));env.update(r0=roots[0],r1=roots[-1])
 expressions=[]
 for recipe in g.BANKS[sid]:
  expressions.extend(['r0','r1'] if recipe==('correct',) else list(recipe))
 candidates=[('r0',roots[0]),('r1',roots[-1])]+[(expr,sp.simplify(sp.sympify(expr,locals=env))) for expr in expressions]
 entries=[]
 for label,raw in re.findall(r'^- \*\*([IVX]+)\.\*\* \$([^$]+)\$',d['source'][':question/problem'],re.M):
  original=raw.split('=',1)[1];value=g.parse_math(original)
  expression=next(expr for expr,v in candidates if sp.simplify(v-value)==0)
  entries.append({'label':label,'expression':expression,'original_value':original})
 assert len(entries)==len(d['source'][':question/answer-fields'])
 checkbox[sid]=entries
(P/'checkbox-recipes.json').write_text(json.dumps({'source_basis':g.SOURCE['basis'],'legacy_basis':legacy['basis'],'provenance':'Individual expressions from retained complete legacy recipes; correct roots use independently solved r0/r1. Noncorrect coefficient expressions do not claim original misconception intent.','questions':checkbox},indent=2)+'\n')
cases=[{'source_id':sid,'template':d['template'],'level':d['level'],'bank_profile':sid,'parameters':g.parameters(sid),'original_difficulty':d['source'].get(':question/difficulty'),'original_correct_reference_present':all(':answer-field/correct' in f for f in d['source'][':question/answer-fields'])} for sid,d in g.DEFS.items()]
(P/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False))
levels=collections.Counter(d['level'] for d in g.DEFS.values());classification=['# Classification','',f"Snapshot: `{g.SOURCE['database']}` basis `{g.SOURCE['basis']}`, lineage `{g.SOURCE['lineage']}`. 24 practice sources: 11 easy, 10 moderate, 1 hard, 2 unrated.",'','The unrated q-9657 is assigned moderate because it expands to a quadratic with two integer roots; q-9852 is assigned hard because its determinant is identically zero. These are authored assignments, not observed ratings. The canonical e-14764 is a linear determinant equation. The sibling KPs establish cofactor expansion and singularity; the declared Quadratic Formula prerequisite supports moderate quadratics. Hard retains the observed all-parameter singularity demand rather than adding higher-degree algebra.','', 'Lesson route follows activity/first-step and step/next: Introduction → Calculating the Determinant → Singular Matrices → Identifying Singular Matrices → Solving for a Variable → this KP. Pull order is not used.','','| Template | Level | Fields | Source IDs | Plot |','|---|---|---|---|---|']
for t,sids in g.TEMPLATES.items():
 d=g.DEFS[sids[0]];classification.append('| '+t+' | '+d['level']+' | '+('two ordered blanks' if d['level']=='moderate' and d['kind']=='blank' else d['kind'])+' | '+', '.join(sids)+' | none |')
classification+=['','24 matrix recipes map to '+str(len(g.TEMPLATES))+' prompt/response families. Changed coefficients alone do not count as new skills or templates. Eight questions own 40 checkbox fields; nine retain five-option radio profiles; seven blank questions own 10 fields. All source fields/answer types are retained for replay.','', 'Plots: none. Matrix TeX is mathematical notation rather than a diagram. No source or parameter-dependent graphics require steps 5/7 rendering.']
(P/'classification.md').write_text('\n'.join(classification)+'\n')
extraction=['# Template extraction','','## 1. Specific descriptions','','The following per-source entries retain the exact original prompt, fields, choices, solution and matrix coefficients. The source wrapper is copied without modification in source.json. Each constant entry c0..c8, linear coefficient v0..v8 and quadratic coefficient w0..w8 is row-major. All variables are real.','','## 2. Shared patterns','','Easy: expand the three first-row minors, collect an affine determinant and solve one linear equation. Moderate: expand to a quadratic, set the determinant to its specified value or zero, and solve by the original factorization, square-root or quadratic-formula method; two blanks retain ascending root order. Hard: expand an identically zero determinant and conclude all real parameter values, retaining either proportional rows or a zero first column. Named/unnamed and blank/radio/checkbox prompts remain distinct layouts. Finite value sets use individual Boolean fields; all-real answers remain radio.','','## 3. Components and complete bank mapping','','Coefficient formulas in the observed bank column are value-preserving inferred expressions, with unknown misconception intent. They are supported only as evidence replay and explicit profile variants. They are not default learner banks. Radio options are compared as complete root sets. Checkbox options are individual values with Boolean membership in the complete root set; both roots must appear in the pool. Their current expressions and labels are recorded in checkbox-recipes.json.','','## 4. Reusable templates and constraints','','The prompt layout masks the whole parameter-dependent matrix and target. Matrix entry i is c_i+v_i*u+w_i*u². Constant zeros, variable positions and degrees are retained. Constants sample from small signed integers; easy targets from -50..80. Moderate named/given targets are computed by evaluating a new determinant at an integer in -8..8, giving rational roots; the symmetric square template samples target 2..50 and permits radicals. Singular quadratics must retain the variable-factor structure. Proportional-row hard matrices retain row2=-2 row1; zero-column hard matrices retain column1=0. Complete banks are selected first and whole-instance equivalence/domain rejection follows. Explicit input never silently resamples.','','Default radio banks are authored operation-derived five-option profiles. Default checkbox pools take the distinct individual values from the corresponding whole operation-derived profile, include both roots and at least one nonroot, and label this an authored extension. Observed checkbox replay retains every captured value label and option count; any collision rejects the complete instance. Easy errors reverse the numerator, omit division, or report a coefficient/constant. Moderate errors reverse formula signs, lose a root or omit the quadratic constant; singular banks distinguish the zero and nonzero roots. Hard errors incorrectly demand one minor be zero, or equate variable-column entries to fixed entries. No diagnosis text is added to learner solutions.','', 'The shared worked solution retains source opening/singularity/conclusion sentences and cofactor → collect → solve sequence. Per-source product/expansion stage order and solve methods are retained; product notation is reconstructed and standardized; exact per-source row typography is a fidelity limitation. q-280403 is corrected from det(F) to the given det(A); q-280541 retains ± in the intermediate where the source incorrectly prints only +.','','Current database keys are present for all 24 questions. q-9657 now has Boolean keys for {-8,-2}; q-9852 retains the repaired Any value of k radio key. Database keys are preserved and independently checked. Both source difficulty labels remain absent, so their moderate/hard assignments are still authored. The database now supplies brief explanations on those two questions; the generator retains its independently checked full cofactor derivations, documented as a solution expansion rather than literal prose fidelity.']
review=['# Determinant unknown review','','All answers and fixed worked solutions are included for author review. Originals are immutable capture text. Generated variants are labeled with evidence replay versus authored default banks.'];variants=[]
for sid,d in g.DEFS.items():
 q=d['source'];extraction+=['', '### '+sid+' — '+d['template'], '', '**Original prompt**\n\n'+q[':question/problem'],'', 'Coefficients: `'+json.dumps(g.parameters(sid),sort_keys=True)+'`. Fields: `'+', '.join(f[':answer-field/key'] for f in q[':question/answer-fields'])+'`.', '', '| Original answer | Type | Parameterized recipe |','|---|---|---|']
 for fi,f in enumerate(q[':question/answer-fields']):
  for ai,a in enumerate(f[':answer-field/choices']):
   recipe=g.BANKS[sid][ai] if d['kind']=='radio' else ('Boolean membership for '+f[':answer-field/key'],next(item['expression'] for item in g.CHECKBOX_RECIPES[sid] if item['label']==f[':answer-field/key'])) if d['kind']=='checkbox' else ('ascending root '+f[':answer-field/key'],)
   extraction.append('| '+a[':answer/value']+' | '+a[':answer/type'][':db/ident']+' | `'+str(recipe)+'` |')
 extraction+=['','Original worked solution:\n\n'+q.get(':question/worked-solution','Not present in snapshot; generated solution is explicitly reconstructed.')]
 review+=['','## Original '+sid+' ('+(q.get(':question/difficulty',{}).get(':db/ident') or 'unrated')+')','',q[':question/problem'],'']
 for f in q[':question/answer-fields']:
  review.append('Field `'+f[':answer-field/key']+'`')
  for a in f[':answer-field/choices']:
   correct=f.get(':answer-field/correct',{}).get(':answer/id')==a[':answer/id'];review.append('- '+a[':answer/value']+(' **original correct**' if correct else ''))
 review+=['','**Original worked solution**','',q.get(':question/worked-solution','No source worked solution or correct designation is present. See independently verified repair in template-extraction.md.')]
 record=g.generate(d['level'],profile=sid,parameters=g.parameters(sid));variants.append(record);review+=['','### Parameterized original replay','',g.markdown(record)]
 for seed in (101,202):
  record=g.generate(d['level'],seed=seed,profile=sid);variants.append(record);review+=['','### Generated evidence-profile variant '+sid+' seed '+str(seed),'',g.markdown(record)]
 if d['kind'] in ('radio','checkbox'):
  record=g.generate(d['level'],seed=303,profile='authored:'+sid);variants.append(record);review+=['','### Generated authored default bank '+sid+' seed 303','',g.markdown(record)]
(P/'template-extraction.md').write_text('\n'.join(extraction)+'\n');(P/'review.md').write_text('\n'.join(review)+'\n');(P/'review.json').write_text(json.dumps(variants,indent=2,ensure_ascii=False))
(P/'plot-extraction.md').write_text('# Plot extraction\n\nAll 24 originals, their options and solutions contain matrix/equation TeX only. No images or diagrams occur. All template plot ratings are none; steps 5 and 7 are not applicable.\n')
(P/'README.md').write_text('''# Solving for an Unknown Given the Determinant

Local generator stops after steps 3–7. No database writes or registrations.

Verify with `.venv/bin/python generate/scratch/17592186059849/validate.py`.
Regenerate evidence with `.venv/bin/python generate/scratch/17592186059849/build-evidence.py`.
Preview with `.venv/bin/python generate/scratch/17592186059849.py --difficulty all --seed 17 --count 2 --format markdown`.

Current math basis 1522: 24 source questions (8 checkbox questions / 40 fields, 9 radios, 7 blank questions / 10 fields). Prior basis-1356 artifacts remain in history/basis-1356. All source banks are explicit profiles; source values replay through coefficient expressions. Default radio banks and checkbox pools are separately authored determinant/equation mistakes. Observed checkbox profiles reproduce the complete captured atomic pool and Boolean keys. All three levels are supported. Unrated q-9657 and q-9852 retain authored moderate/hard assignments. All current database keys are matched; the generator expands their brief database explanations into full cofactor derivations. Source prose/method is shared but intermediate worked-solution row rendering is standardized; see validation.json for that fidelity limitation. No plots are needed.

Source profiles are the source ID; authored selection profiles prefix `authored:`. `generate(level, seed, template, field_type, parameters, profile)` accepts original coefficient arrays and rejects invalid explicit parameters. `source-cases.json` contains all original calls. `review.md` includes originals, two variants per observed matrix/bank, and one authored default per radio/checkbox source. Identity depends on mathematical parameters, field layout and complete bank rather than seed/order. Native validation checks field grading, whole correct responses, flipped checkboxes, and incomplete submissions with ../source-refresh-2026-10-12/check-checkbox-engine.
''')
print('Wrote evidence:',len(cases),'sources,',len(variants),'generated reviews,',len(g.TEMPLATES),'templates')
