#!/usr/bin/env python3
"""Rebuild extraction evidence from the frozen wrapper; does not write shared files."""
import importlib.util,json,re,itertools
from pathlib import Path
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def write(n,x): (H/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
classify=['# Classification — tangent vector KP 17592186124439',
'Frozen database math, basis 1356, lineage '+g.CAPTURE['lineage']+'. Source capture wrapper retained verbatim in source.json.',
'Actual ENUM values, rather than attribute presence: all **15 practice questions are :question.difficulty/hard**. There are no easy, moderate, unrated, fieldless or duplicate-field originals. Each has one radio field keyed selection, five mathematical choices and one designated correct choice. No practice or canonical question embeds a plot.',
'| Level | Practice sources | Templates | Field type | Bank profiles | Plot rating |\n|---|---:|---:|---|---|---|\n| Easy | 0 | 1 authored | radio/5 choices | authored complete method bank | none |\n| Moderate | 0 | 1 authored | radio/5 choices | authored complete method bank | none |\n| Hard | 15 | 15 observed derivative/operative-chain families | radio/5 choices | 15 evidence-only original whole banks; method extension per family | none |',
'## Actual lesson route and scope',
'Following activity/first-step and step/next gives: Introduction (17592186125265) → Geometric Interpretation tutorial (17592186125465) → slope KP17592186124437 (step17592186125266) → tangent-line equations KP17592186124438 (step17592186125267) → this tangent-vector KP (step17592186125268). This order was reconstructed from links, never Pull array order.',
'The tutorial identifies f_y with the slope of an x=constant slice and f_x with the slope of a y=constant slice. The preceding sibling constructs the tangent line using point-slope form. This KP’s canonical e-3070 evaluates the supplied partial derivative at P, forms two planes, crosses their normals, then scales the resulting vector to a nicer parallel vector. The key prerequisite is The Intersection of Two Planes (topic2539/db17592186050991), with partial-derivative rules on the owning topic’s incoming route.',
'The assessed response is **any nonzero tangent direction**, either sign and any nonzero scalar multiple. It is not an anchored displacement, velocity at a specified parameter, oriented vector or unit vector. Since partial derivatives are supplied, none of these generators differentiates a new function or parameterizes a space curve.',
'## Authored level claims',
'Easy supplies a constant partial derivative (signed integer magnitude2..9). Its evaluation is immediate; every instance still builds the line, obtains normals and a tangent direction. Moderate supplies a nonzero coefficient times the varying coordinate, coefficient magnitude2..9 and coordinate magnitude2..9; every instance performs exactly one substantive signed multiplication. Nonunit coordinates are enforced on explicit calls as well as sampling, so moderate cannot collapse to easy. Both coordinate-plane orientations are same-workload alternatives, with no internal progression.',
'Hard retains all fifteen actual observed families. Even the observed linear family requires subtracting the shift and multiplying, rather than the moderate single-coordinate multiplication. Other observed families retain their original sum/product/function/quotient evaluation chains. No observed hard label is reassigned. A positive outer integer coefficient1..9 supplies variety while retaining familiar evaluation anchors, perfect-square radicands and original log/trig inputs; the arithmetic remains at most54 for the largest linear slope. Coefficients are grouped around complete components. Height translation h in -9..9 affects line anchoring but not the assessed tangent direction and is excluded from mathematical-task counts.',
'Historical distractor intent is mostly opaque. Complete source banks stay evidence-only, including two redundant wrong-direction pairs. Default hard sampling first selects a family, then uses the complete five-operation method bank; normal output never samples raw opaque banks. It rejects the entire bank if any two options describe parallel directions or if another option is a valid tangent.',
'## Observed families','| Template | Source DB ID / MA ID | Slice | Point | Supplied partial | Evaluated slope | Shape |\n|---|---|---|---|---|---|---|']
extract=['# Template extraction — four stages',
'## 1. Specific source descriptions',
'All sources share the full surface/slice/point/supplied-partial/which-vector prompt, but derivative structures, operative evaluation chains, point-slope distribution/sign-normalization rows and basis-versus-tuple outputs remain separate families. Exact prompts, fields, owned answer UUIDs, enum values, omissions and full worked solutions are in source.json and source-bank-map.json. All relevant difficulty/worked-solution/answer-field/correct attributes are present.',
'## 2. Shared mathematical pattern',
'For y=b evaluate m=f_x(a,b), use z-z0=m(x-a), take slice normal(0,1,0) and a normal to the tangent-line plane. The tangent direction is parallel to(1,0,m). For x=a, use f_y and a direction parallel to(0,1,m). Either nonzero sign and every nonzero scale are valid. The explicit point still determines the line intercept and all worked-solution point references.',
'## 3. Complete source component and bank map',
'Each choice below is associated with its own field, exact raw spelling, decoded vector, correct designation and source profile. Its genuine recipe for evidence replay is vertical-translation invariance: replacing z0 with z0+h changes line intercepts but leaves every direction unchanged. The source vector coefficients are recovered constants, not inferred authoring distractor operations. This is an explicit opaque whole-bank profile, never the normal default. The public generate(...,profile="source",parameters={"h":0}) replays all originals; nonzero h executes complete affine-coordinate masks instead of a literal-source branch. Height does not inflate meaningful task counts.','## 4. Reusable masks, constraints and normal-bank extension',
'Normal hard first-partial blocks use each family’s original ordered RHS masks. A changed outer coefficient multiplies each unreduced/evaluated intermediate component as a whole; only the final slope is collected. Same-line evaluations remain same-line. The point-slope chain retains the source number of rows and its distinct operation: distribution for linear_x/factored_y/affine_x/radical_y, sign normalization plus distribution for exp_log_x, sign normalization with undistributed remaining factor for log_cube_y/radical_x, and source omission of redundant distribution rows for other families. Every source cross-product chain retains its determinant, basis-result row, and optional tuple-result row.',
'Tail masks retain shared source sentences (point-slope, next notice, normal descriptions, cross-product introduction and conclusion), fill every full point/line/normal/vector component, and use a single fixed solution independent of selected wrong choice. Source-specific normal orientations and fraction-clearing constants are retained under outer scaling. Normal presentation changes are explicit: grouped signed factors; CAS spacing/term order and basis notation; correct full P references; a visible escaped literal system brace; corrected stale plane. Raw source presentation remains unmodified in source profile.',
'The separately authored complete bank is: correct direction(1,0,m) or(0,1,m); reverse the vertical sign; swap the varying and vertical slope components; supply the slice-plane normal; supply the tangent-line-plane normal. These operations arise from the actual direction/cross-normal method, without claiming historical provenance. They contain five mathematical choices and no added learner-facing diagnosis. The bank rejects m=0,±1 and any direction collision as a whole. Original m=±1 sources remain public evidence; normal output chooses another eligible outer coefficient. This preserves source evidence without claiming an incorrect or ambiguous normal bank.',
'No source answer has adjacent backslashes: decoded ord92 checks cover75/75 values in byte-audit.json, all run-index lists empty. JSON display escaping is not a source anomaly.',
'## Source errors and repairs',
'15/15 raw prompts, complete solutions and banks are exact. All15 correct designations and60 wrong choices are mathematically valid under the requested response criterion. The two repeated **wrong** directions are not extra correct answers: source17592186338919 has ⟨-1,0,3⟩ and ⟨1,0,-3⟩; source17592186385494 has ⟨0,0,1⟩ and ⟨0,0,2⟩. Evidence records these whole banks; normal method banks have no direction duplicates.',
'Source17592186124977 says P(1,1,0) in a later prose sentence while the prompt and calculations use P(2,-3,3). Source17592186268891 calls the slice y=0 in the normal bullet while the prompt and line use y=1. Normal output repairs both from the actual instance.13/15 raw solutions open a system with an unmatched literal {; normal output uses \\{. Source17592186406798 displays x-z+-1=0; normal output groups/reduces signs without changing the plane. These are raw solution/presentation anomalies; no original correct answer is changed. Raw-exact solution fidelity is15/15; normal solutions intentionally have notation normalization and documented repairs, so no raw-exact normal-solution claim is made.']
mapdata=[]
for name,d in g.TEMPLATES.items():
 if 'source' not in d:continue
 q=d['source'];f=q[':question/answer-fields'][0];m=g.sp.simplify(d['derivative'].subs({g.X:d['point'][0],g.Y:d['point'][1]}));correct=f[':answer-field/correct'][':answer/id'];shape='tuple' if f[':answer-field/correct'][':answer/value'].startswith('⟨') else 'basis'
 classify.append('| '+name+' | '+str(q[':db/id'])+' / '+q[':question/math-academy-id']+' | '+d['plane']+' fixed | $'+g.vector(d['point'])+'$ | $'+g.tex(d['derivative'])+'$ | $'+g.tex(m)+'$ | '+shape+' |')
 blocks=re.findall(r'\$\$.*?\$\$',q[':question/worked-solution'],re.S)
 bank=[]
 extract+=['\n### '+name+' — '+str(q[':db/id'])+' / '+q[':question/math-academy-id'],q[':question/problem'],'Complete source bank:']
 for a in f[':answer-field/choices']:
  v=g.parse_vector(a[':answer/value']);item={'field_id':f[':answer-field/id'],'field_key':f[':answer-field/key'],'source_answer_id':a[':answer/id'],'value':a[':answer/value'],'decoded_vector':list(map(str,v)),'designated_correct':a[':answer/id']==correct,'recipe':'constant vector under vertical translation h','intent':'opaque historical whole-bank component; not promoted to default'};bank.append(item)
  extract.append('- $'+a[':answer/value']+'$ — '+('correct' if item['designated_correct'] else 'wrong')+'; vector '+str(item['decoded_vector'])+'; field '+f[':answer-field/id']+'; answer '+a[':answer/id'])
 extract+=['Operative evaluation block (full, raw):',blocks[0],
           'Point-slope row count '+str(blocks[1].count(r'\\')+1)+'; cross-result stages '+str(blocks[3].count('& ='))+'. Full operative solution and every shared sentence:',q[':question/worked-solution']]
 mapdata.append({'source_id':q[':db/id'],'math_academy_id':q[':question/math-academy-id'],'template':name,'level':q[':question/difficulty'][':db/ident'],'profile':'source','evidence_only':True,'eligible_for_learning':False,'parameters':{'h':0},'point':list(map(str,d['point'])),'derivative':str(d['derivative']),'slope':str(m),'prompt':q[':question/problem'],'full_worked_solution':q[':question/worked-solution'],'operative_blocks':blocks,'choices':bank})
(H/'classification.md').write_text('\n\n'.join(classify)+'\n');(H/'template-extraction.md').write_text('\n\n'.join(extract)+'\n');write('source-bank-map.json',mapdata)
# Enumerate complete permitted domains, excluding incidental coordinate/height aliases.
counts={};breakdown={}
for level in ('easy','moderate'):
 tasks=set()
 for plane,a,x,y in itertools.product(('x','y'),tuple(range(-9,-1))+tuple(range(2,10)),(-4,-3,-2,-1,1,2,3,4),(-4,-3,-2,-1,1,2,3,4)):
  p={'plane':plane,'a':a,'x':x,'y':y,'z':0}
  try:r=g.generate(level,parameters=p)
  except ValueError:continue
  tasks.add(r['generation']['mathematical_fingerprint'])
 counts[level]=len(tasks)
hard_tasks=set()
for n,d in g.TEMPLATES.items():
 if d['level']!='hard':continue
 tasks=set()
 for c in range(1,10):
  try:r=g.generate('hard',template=n,parameters={'c':c,'h':0})
  except ValueError:continue
  tasks.add(r['generation']['mathematical_fingerprint'])
 hard_tasks.update(tasks);breakdown[n]=len(tasks)
counts['hard']=len(hard_tasks)
write('diversity.json',{'meaningful_task_counts':counts,'hard_by_family':breakdown,'excluded_from_fingerprint':'height, bank/profile aliases, seed/order, fixed coordinates absent from derivative free symbols; easy all coordinates','finite_domain':'Easy32 tangent-slope/plane tasks. Moderate each distinct supplied linear expression and nonunit active substitution. Hard positive scale1..9 of each original family at familiar anchors; future wider number forms require a separate scope review.'})
(H/'plot-extraction.md').write_text('''# Plot extraction

No practice or canonical prompt, answer or solution contains plots. Classification rating none; no plot generator or renderer cache is required.

The actual lesson introduction has two explanatory rasters, inspected at original resolution using view_image: `/media/jake/SSD/EDB/math/images/86/8619c41cd0caf04ae9ee9bcae61e31739d8da583793a67c1c87e00186c3ac417.png` and `/media/jake/SSD/EDB/math/images/e9/e982ef5d6d8d4fec9c64957d46f22cea2a85bd002595642f58700cf48cce4256.png`. The first shows a blue downward paraboloid, pale x=3 plane, black intersection curve, P and orange tangent, with x/y/z axes. The second shows its yz-plane parabola, a marked P, orange descending tangent and labelled y/z axes. Their role is explaining the derivative-to-slice slope correspondence, not supplying numeric answer choices. No raster is reused in generated records and no geometry changes with sampled parameters. Therefore no Matplotlib/TikZ outputs, cached/fresh-render records or narrow-label-placement claim is applicable.
''')
print(counts,breakdown)
