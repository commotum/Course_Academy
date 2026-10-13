"""Source-complete classification and source-bank mappings for this KP only."""
import importlib.util,json,re
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
s=json.loads((H/'source.json').read_text());analysis=[]
for q in s['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];t=g.PROFILES.get(sid);fields=q.get(':question/answer-fields',[]);bank=[]
 if t:
  c,n=t['parameters'];generated=g.bank(t,c,n)
  for f in fields:
   for a in f[':answer-field/choices']:
    matches=[i for i,z in enumerate(generated) if a[':answer/value']==z];assert len(matches)==1
    bank.append({'field_id':str(f[':answer-field/id']),'answer_id':str(a[':answer/id']),'value':a[':answer/value'],'recipe_index':matches[0],'recipe_at_source_parameters':generated[matches[0]],'exact_reproduction':True,'mathematical_expression':str(v.math(a[':answer/value'])),'correct':a[':answer/id']==f[':answer-field/correct'][':answer/id'],'profile':t['profile']})
 else:
  for f in fields:
   for a in f[':answer-field/choices']:bank.append({'field_id':str(f[':answer-field/id']),'answer_id':str(a[':answer/id']),'value':a[':answer/value'],'profile':'excluded-'+sid,'recipe':'exact observed expression; no generalized recipe or fidelity claim','correct':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')})
 analysis.append({'source_id':sid,'db_id':q[':db/id'],'difficulty':q.get(':question/difficulty',{}).get(':db/ident','unrated'),'supported':bool(t),'profile':t['profile'] if t else 'excluded-'+sid,'parameters':t['parameters'] if t else None,'field_types':[f[':answer-field/type'][':db/ident'] for f in fields],'answer_types':[a[':answer/type'][':db/ident'] for f in fields for a in f[':answer-field/choices']],'field_keys':[f[':answer-field/key'] for f in fields],'plot_rating':'none','source_record':q,'choice_components':bank})
(H/'source-analysis.json').write_text(json.dumps(analysis,indent=2)+'\n')
(H/'classification.json').write_text(json.dumps({'basis':s['basis'],'lineage':s['lineage'],'practice_sources':12,'supported_source_banks':7,'supported_levels':['easy','moderate'],'levels':{'easy':{'supported_markdown_value_templates':3,'radio_bank_profiles':2,'blank_profiles':1,'source_ids':['q-48385','q-48560','q-342420'],'field_types':['radio','blank'],'plot_rating':'none'},'moderate':{'supported_markdown_value_templates':3,'radio_bank_profiles':3,'blank_profiles':1,'source_ids':['q-72154','q-72156','q-72157','q-342424'],'field_types':['radio','blank'],'plot_rating':'none'},'hard':{'observed_templates':0,'status':'bounded-unsupported','nominal_shortage':5}},'source_assignments':analysis},indent=2)+'\n')
(H/'classification.md').write_text(f'''# Classification

Captured math basis {s['basis']}, lineage {s['lineage']}. All 12 practice questions and the canonical example were read at that basis; source.json and reference/source.edn retain them. No registered generator or supplied .generated artifact existed. The native inventory still flags an unclassified legacy source. Current distinct validated availability is rechecked before generation and under api.lock before commit.

| Difficulty | Supported layouts | Complete source bank profiles | Fields | Plots | Sources |
|---|---:|---:|---|---|---|
| Easy | 3 | 2 radio, 1 blank | single selection radio or field-1 math blank | none | q-48385, q-48560, q-342420 |
| Moderate | 3 | 3 radio, 1 blank | single selection radio or field-1 math blank | none | q-72154, q-72156, q-72157, q-342424 |
| Hard | 0 observed | 0 | none observed | none | none |

The two scaled cosine radio questions share a Markdown/value layout, but retain distinct complete distractor banks. The unit cosine, unit sine square, scaled sine square, and math-blank layouts retain their own notation and solution sequences. Source-analysis.json records every source field, choice, and profile assignment, including excluded evidence.

q-48562 is unrated and has no correct designation or worked solution; preserve it as incomplete evidence. q-143516 and q-167568 expect the coefficient fragment before cot(t), but neither prompt states the initial velocity. Their solutions supply different cosecant-square velocities; generated prompts cannot silently infer those missing givens. Both remain excluded. q-342413 and q-342427 use delimiter-wrapped text answers in a different boxed solution layout. This bounded package supports the observed math-answer layouts; it does not convert source text blanks or claim symbolic grading for them. These are separate excluded templates. The two acceleration prompts differ in captured whitespace, recorded intact. None of these originals is altered or counted by this package as validated availability.

No source question is rated hard. Hard remains a bounded unsupported capability, nominal shortage 5; absence does not prove mathematical impossibility. New verified hard evidence or an independently justified extension reopens classification. It is not called filled.
''')
(H/'template-extraction.md').write_text('''# Template extraction

The task is to differentiate c T(x)^n by first setting u=T(x), applying d(c u^n)/du=c n u^(n-1), then substituting the trig inner derivative. Source-analysis.json retains each specific prompt, solution, numerical features, variable roles, field keys, and every original answer. contract.json stores source-specific fixed instructional sentences and parameterized Markdown. review.md places originals, exact replay, and variants side by side.

The generator bank(t,c,n) is the executable component mapping below. Set m=n-1 and k=c*n. S=sin(x), C=cos(x). Each row lists the full bank in generated order, beginning with the canonical answer; original order is retained in source-analysis.json. Recipes are observed complete expressions, with learner error interpretations unresolved. No inferred error labels or feedback enter the learner presentation.

| Profile | Observed (c,n) | Full mathematical bank |
|---|---|---|
| cos-unit / q-48385 | (1,4) | -n C^m S; -n S^m; n C S^m; n C^m S; n C^m |
| sin-unit / q-48560 | (1,2) | 2SC; -SC; -2C^2; -2SC; C^2 |
| sin-scaled / q-72154 | (9,2) | kSC; -cSC; -cC^2; kSC^2; kS |
| cos-scaled-a / q-72156 | (5,8) | -k C^m S; -c S^m; c C S^m; -k C S^m; k C^m |
| cos-scaled-b / q-72157 | (4,7) | -k C^m S; -k C S^m; -k S^m; c C S^m; c C^m |
| sin-blank / q-342420 | (1,7) | n S^m C |
| cos-blank / q-342424 | (-4,5) | -k C^m S |

Every complete original bank replays with exact values, count, correct designation, prompt, and worked solution. The two cosine scaled banks remain separate profiles; no bank is pooled or mixed. Blanks have no distractors and preserve the full derivative expression response shape and field-1 placeholder.

All variables are real, and sine/cosine expressions are defined for every x. Powers are positive integers. Bounded sampling is explicitly narrower than arbitrary powers or coefficients: cosine radio n=3..9 (n=2 makes required distractors collide), sine square radio n=2, sine blank n=2..9, positive scaled radio c=2..9, negative cosine blank c=-9..-2. cos-unit c=1 and sin-unit is a singleton (1,2). Unit sine square overlaps the sine-blank task and adds no mathematical novelty. Negative cosine values are observed features, not discarded. No fractional or larger powers, alternate inner functions, or negative sine coefficient extension is claimed.

Fixed components include source sentences, field type/key, and unit trig argument. Variable components are c,n,m,k,-k and all their appearances in powers, coefficients, composite function, derivatives, multiplication, substitution, final line, and answer bank. No plots or optional learner feedback are added. An earlier draft failed to parameterize some signed final coefficients; extract.py now maps both k and -k, and independent rendered-function/solution checks reject that failure.

Distinct tasks use the exact derivative fingerprint of the displayed input function; changing profile, answer shape, identity, seed, or choice order does not create new mathematical inventory. All current practice and canonical sine/cosine tasks are excluded from generation by that fingerprint, including unrated/text-answer sources. A mathematically correct question still needs the actual learner grader: native-grading.json checks all radio choices and canonical, reordered equivalent, wrong-sign, and missing-factor blank entries over the entire bounded domain.
''')
assert not any(re.search(r'!\[|<img|images/',q[':question/problem']+q.get(':question/worked-solution','')) for q in s['record'][':knowledge-point/questions'])
(H/'plot-extraction.md').write_text('# Plot extraction and generation\n\nEvery captured source uses mathematical text only. There are no graphs, diagrams, assets, or variable plot requirements. Plot rating is none for every supported or excluded template. Stage 7 requires no rendering or asset publication.\n')
validation=json.loads((H/'validation.json').read_text())
caps={'knowledgePoint':g.KP_ID,'source_basis':s['basis'],'lineage':s['lineage'],'supported_levels':['easy','moderate'],'unsupported_levels':['hard'],'finite_distinct_task_domain':validation['finite_distinct_tasks'],'exceptions':[{'kind':'unsupported','level':'hard','nominal_shortage':5,'reason':'No verified hard source template, field, solution, or justified difficulty extension. Bounded capability; new evidence reopens classification.'},{'kind':'incomplete-source','profiles':['q-48562'],'reason':'Unrated; missing correct designation and worked solution.'},{'kind':'missing-given','profiles':['q-143516','q-167568'],'reason':'Velocity is supplied only by the solution, not the acceleration prompt; preserve fragment response layout but exclude ambiguous tasks.'},{'kind':'bounded-field-layout','profiles':['q-342413','q-342427'],'reason':'Delimiter-wrapped text blanks and boxed solution layouts are outside this math-answer package. Original values and field types preserved; no math-grading/fidelity claim.'},{'kind':'finite-profile','profile':'sin-unit','variant_limit':1,'reason':'Observed sine-square bank is fixed; its mathematical task also exists in sin-blank. No seed or shape duplicates count.'}],'unsupported_levels_filled':False}
(H/'capabilities.json').write_text(json.dumps(caps,indent=2)+'\n')
(H/'README.md').write_text('''# Trigonometric power chain rule

The generator is ../17592186064283.py. validate.py replays all seven supported source banks and checks every bounded instance with exact SymPy mathematics and the actual application grader. classification.md, source-analysis.json, contract.json, template-extraction.md, and capabilities.json record original evidence, complete recipes, limits, and exceptions. Hard remains unsupported.

replenish.py acquires the application api.lock, rechecks current basis, source stability, contributor and inventory, excludes previously shown/reserved and mathematically duplicate tasks, validates selected instances, and saves typed EDN plus native-spec preview. It holds the lock through guarded submission and exact-basis readback. Exact requests, receipts, and verification live under reference/replenishment. Only this KP generator registration and additive generated questions are allowed. Source records, canonical examples, and learner history are preserved. Repeat preparation must make no content changes.

Run with the repository .venv Python (SymPy installed). Preview and EDB calls reuse the configured integration and deployed validation predicates. No application code or scheduler changes are needed.
''')
