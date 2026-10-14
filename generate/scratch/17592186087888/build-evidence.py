#!/usr/bin/env python3
"""Write evidence from immutable wrappers and generated review records."""
import hashlib,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
lesson=json.loads((ROOT/'lesson.json').read_text())
activity=lesson['record']
if isinstance(activity,list):activity=activity[0]
# Captured lesson wrapper has a collection of activities; derive each route by links.
activities=activity if isinstance(activity,list) else [activity]
if ':topic/activities' in activity:activities=activity[':topic/activities']
route=[]
for a in activities:
 if ':activity/steps' not in a:continue
 steps={s[':db/id']:s for s in a[':activity/steps']};current=a.get(':activity/first-step',{}).get(':db/id');visited=set()
 while current in steps and current not in visited:
  visited.add(current);s=steps[current];c=s.get(':step/content',{})
  route.append({'step':current,'title':c.get(':tutorial/title',c.get(':knowledge-point/title')),'content_id':c.get(':db/id')});current=s.get(':step/next',{}).get(':db/id')
rows=[]
for template,sid in g.TEMPLATES.items():
 q=g.QUESTIONS[sid];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 banks=[]
 for i,f in enumerate(q[':question/answer-fields']):
  choices=[]
  for j,(answer,e) in enumerate(zip(f[':answer-field/choices'],g.BANKS[sid][i])):
   choices.append({'index':j,'source_answer_id':answer[':answer/id'],'value':answer[':answer/value'],'exact_rhs':str(e),'parameterized_rhs':str(e.subs({g.X:g.sp.Symbol('sx',positive=True)*g.X,g.Y:g.sp.Symbol('sy',positive=True)*g.Y},simultaneous=True)),'correct':answer[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id') if ':answer-field/correct' in f else None,'mathematically_homogeneous':g.sp.simplify(g.X*g.sp.diff(e,g.X)+g.Y*g.sp.diff(e,g.Y))==0,'observed_expression_pattern':True,'distractor_intent':'Degree/scaling recognition contrast; historical author intent not inferred beyond expression pattern'})
  banks.append({'source_field':i,'field_id':f[':answer-field/id'],'field_key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'correct_present':':answer-field/correct' in f,'choices':choices})
 rows.append({'source_id':sid,'template':template,'level':level,
  'stage_1_specific_description':{'prompt':q[':question/problem'],'worked_solution':q[':question/worked-solution'],'banks':banks,'numbers':'Exact small integers, polynomial powers 1/2/3, ratio trigonometric/log/exp branches as captured.','notation':'Whole ODE mathematical radio values; q-8739 has two different derivative layouts and duplicate selection keys.'},
  'stage_2_generalization':'Select one '+('nonhomogeneous' if level=='moderate' else 'homogeneous')+' first-order ODE from five whole-equation options. Check numerator/denominator degrees then the f(tx,ty)=f(x,y) scaling definition; family-specific counterexample retained for offset quotient.',
  'stage_3_components':{'banks':banks,'solution_math_blocks':re.findall(r'\$\$([\s\S]*?)\$\$',q[':question/worked-solution']),'solution_aligned_rows':[s.split('\\\\') for s in re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',q[':question/worked-solution'])]},
  'stage_4_template':{'operative_prompt_mask':q[':question/problem'],'operative_solution_mask':q[':question/worked-solution'],'slots':['sx multiplies every RHS x factor; sy multiplies every RHS y factor, simultaneously, including implicit xy.','Offset family: x0=1,y0=2,t=2..3; all displayed numeric components are derived.'],'fixed':['five complete ODE options','one selection radio field in normal mode','both source methods and each family-specific distributed/factored/witness sequence','no solving/integration/substitution-v steps'],'constraints':{'easy':'sx,sy integers1..9, at least one is1','moderate':'sx,sy integers1..9 except offset family1..3','hard':'only cubic_quotient/quadratic_difference, sx and sy integers2..9'},'optional':'raw evidence retains missing correct key and duplicate field; malformed offset witness supports original parameters only','plots':'none'}})
extraction={'database':g.SOURCE['database'],'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'source_rows':rows,'lesson_route_by_next_links':route,'observed_templates':6,'observed_banks':7,'authored_hard_templates':2,'source_errors':[
 {'source_id':'q-8739','evidence':'two selection fields; first has five choices and no correct reference','repair':'Normal uses the already-supported second field only. Raw retains both banks and missing key.','excluded':'raw two-field record is evidence-only and unavailable to native keyed-field fixture'},
 {'source_id':'q-14322','evidence':'declares x1,y2,t3; evaluates f(2*1,2*3)=f(2,6)=5/48; simultaneous scaling would give f(3,6)=10/54=5/27','repair':'Normal derives t*x0,t*y0, actual function substitution, numerator/denominator and reduced fraction at every changed parameter.','excluded':'raw erroneous witness evidence-only'},
 {'source_id':'q-14322','evidence':'Nonhomogeneous numerator claimed sufficient to imply function nonhomogeneous without considering cancellation','repair':'Normal explains numerator degrees2/0 and homogeneous denominator degree2; nonzero constant cannot cancel, so this family is nonhomogeneous of degree zero.'}],
 'authored_scope':'Hard has no observed rating. Canonical e-2393 and introduction tutorial establish scaling recognition; preceding Homogeneous Functions and Introduction to Differential Equations are prerequisites. Route positions recognition before substitution-v and solving KPs. Hard therefore varies only the two observed easy polynomial banks with two nonunit coordinate factors, increasing coefficient bookkeeping at a fixed workload while retaining exactly the same recognition/factorization stages. No later-lesson operations or new functions.'}
(ROOT/'template-extraction.json').write_text(json.dumps(extraction,indent=2,ensure_ascii=False)+'\n')
(ROOT/'classification.md').write_text('''# Classification — KP17592186087888

Immutable math basis **2275**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Source/topic/lesson wrappers are copied byte for byte. Six practice questions all carry Math Academy IDs; there is no independent inventory. Canonical example e-2393 is context, not a practice replay count.

| Level | Observed templates | Complete banks | Fields | Source IDs | Plots |
|---|---:|---:|---|---|---|
| Easy | 3 | 4 | radio; q-8739 has two selection fields | q-8739, q-14319, q-8369 | none |
| Moderate | 3 | 3 | radio | q-8741, q-14322, q-90597 | none |
| Hard | 0 | 0 | authored radio extension | cubic_quotient and quadratic_difference masks | none |

All options are complete equations with the derivative isolated. The source's q-8739 legacy bank has no correct reference; the second field is keyed. Both raw fields are retained. Normal questions use one supported keyed field. There are 35 observed choices and 28 distractors by mathematical criterion (including four distractors in the unkeyed legacy field); stored keyed distractors number24. q-14322 has an invalid numerical scaling witness and an overbroad degree argument. Raw evidence retains these; normal output repairs both. See template-extraction.json for every source choice and source operation.

Hard is conservatively authored from the recognition tutorial, canonical scaling examples, and prerequisites. Its two nonunit coordinate factors require fixed extra coefficient bookkeeping, with the same degree and scaling steps in every question. Easy permits at most one nonunit factor. No transformation to a separable ODE or solution of an ODE is included.
''')
md=['# Template extraction — four stages','',f"Source provenance: math basis{g.SOURCE['basis']}; complete wrappers in source.json/topic.json/lesson.json.",'']
for row in rows:
 md+=['## '+row['source_id']+' — '+row['template'],'','### 1. Specific source','',row['stage_1_specific_description']['prompt'],'', 'The complete original worked solution is retained in source.json and repeated in the review. Fields and all observed bank components follow.','']
 for bank in row['stage_3_components']['banks']:
  md+=['Field '+str(bank['source_field'])+': `'+bank['field_id']+'`, key `'+bank['field_key']+'`; correct reference '+('present' if bank['correct_present'] else '**absent**')+'.','']
  for c in bank['choices']:md+=['- $'+c['value']+'$ — '+('keyed correct' if c['correct'] else 'observed option')+'; RHS recipe `'+c['parameterized_rhs']+'`.']
  md+=['']
 md+=['### 2. Shared pattern','',row['stage_2_generalization'],'','### 3. Components and operative stages','']
 for chain in row['stage_3_components']['solution_aligned_rows']:
  for i,stage in enumerate(chain):md+=['Stage '+str(i+1)+': `'+stage.strip()+'`.']
 md+=['','### 4. Reusable mask and slots','','Every RHS coordinate occurrence is a complete token slot. Simultaneous factor substitution protects derivative notation, function argument labels, and complete TeX commands; adjacent xy receives both factors. The source family’s operative chain and prose remain present under changed factors. Coefficient factor1 renders the original token, through the same recipe.', '',json.dumps(row['stage_4_template']['constraints']), '']
md+=['## Errors and authored bounds','',extraction['authored_scope'],'','Coefficients1..9 preserve one-digit number forms observed across the pool (including9); powers remain1/2/3 and recognition does not require expanding coefficient powers. Hard always carries two nonunit factors, easy at most one. The numerical counterexample family restricts factors1..3 and x0=1,y0=2,t=2..3; its largest displayed numerator is82 and denominator486, with the same square/add/multiply/fraction stages. Complete bank is selected before sampling; no individual option replacement or first-valid option pool exists. Every pair of whole ODEs, including incorrect pairs, is checked for algebraic equality. Four distractors sharing a classification are intentional; four equivalent equations would fail.','', 'Canonical mathematical-task identity uses the qualifying RHS, the response criterion and the assessed coefficient bookkeeping. Complete banks and profile/seed/notation/witness aliases are excluded; they remain in content identity. Thus the moderate linear family does not count sy changes and the moderate quadratic family does not count sx changes as new tasks.', '', 'Log-difference options require x>0,y>0 and t>0. Ratio transcendental options use real variables and their displayed denominators nonzero. Every rational option retains its displayed-denominator exclusions, including cancellable denominator factors.','']
for e in extraction['source_errors']:md+=['- '+e['source_id']+': '+e['evidence']+'. '+e['repair'],'']
(ROOT/'template-extraction.md').write_text('\n'.join(md)+'\n')
review=json.loads((ROOT/'review.json').read_text());out=['# Review: exact originals and generated variants','', 'Raw source anomalies are explicitly ineligible. Normal repairs are labeled separately. Hard examples are authored. Every source bank and both solution methods are shown.','']
for row in review:
 r=row['record'];m=r['generation'];q=r['question'];out+=['## '+row['role']+' — '+m['source_ids'][0]+' / '+m['template'],'', 'Parameters: `'+json.dumps(m['parameters'])+'`; profile `'+m['profile']+'`; eligible for learning: '+str(m['eligible_for_learning'])+'.','',q[':question/problem'],'']
 for i,f in enumerate(q[':question/answer-fields']):
  out+=['Field '+str(i)+' (selection radio), correct reference '+('present' if ':answer-field/correct' in f else '**absent**')+'.','']
  for a in f[':answer-field/choices']:out+=['- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1] else '')]
  out+=['']
 out += [q[':question/worked-solution'],'']
(ROOT/'review.md').write_text('\n'.join(out)+'\n')
(ROOT/'README.md').write_text('''# Identifying Homogeneous Differential Equations

Draft script: ../17592186087888.py. Immutable math basis2275. No database operations, registration, shared-file edits, or commits.

Verify:

```sh
.venv/bin/python generate/scratch/17592186087888/validate.py
.venv/bin/python generate/scratch/17592186087888/build-evidence.py
.venv/bin/python generate/scratch/17592186087888.py --difficulty hard --seed 11 --format markdown
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Profiles normal and raw; raw q-14322 admits original parameters only because its invalid historical numeric chain cannot be generalized honestly. Source-cases.json lists all six raw replays. Parameterization uses a single simultaneous coordinate-factor substitution recipe across every bank and every source worked solution; no literal original-return branch exists.

Easy: three observed polynomial families, at most one nonunit coordinate factor. Moderate: three observed NOT-homogeneous families with their original functional banks. Hard: two conservatively authored polynomial recognition families with two nonunit factors, never solving/integration/substitution-v. All five whole-equation choices are classified independently from the rendered TeX, with Euler and scaling checks and pairwise whole-equation equality checks. Every aligned equality is evaluated against the actual displayed keyed function; structural stage guards and mutation tests check the source operations. Native checks use the real application's memory-only learning::grade_field harness; IDs do not replace mathematical checks.

Raw q-8739 retains both duplicate-key radio fields, including the missing legacy correct reference. Normal uses the already-supported keyed field. Raw q-14322 retains the inconsistent witness and overbroad rule as ineligible evidence. Normal repairs simultaneous scaling and qualifies the cancellation argument. Calculator requirements are unknown because queried attributes are absent; no calculator policy is inferred. Parent independent QA is pending. Exact counts/hashes/runtime are in validation.json.
''')
print('Evidence written; lesson route:',route)
