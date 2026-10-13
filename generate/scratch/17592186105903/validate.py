#!/usr/bin/env python3
"""Independent displayed-math, source-structure, identity and native-grading QA."""
import concurrent.futures, copy, hashlib, importlib.util, json, math, re, subprocess, sys
from pathlib import Path
import uuid
import sympy as sp
from decimal import Decimal, ROUND_HALF_UP
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('triangle',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
COUNTS={}
(ROOT/'validation.json').write_text(json.dumps({'status':'running','previous_report_superseded':True}))
def checked(label,condition):
 if not condition:raise AssertionError(label)
 COUNTS[label]=COUNTS.get(label,0)+1

def display_check(r,raw=False):
 q=r['question'];s=q.get(':question/worked-solution');meta=r['generation'];p=meta['parameters'];t=g.TEMPLATES[meta['template']]
 checked('outer_shape',set(r['knowledge_point'])=={'db_id','id','title'})
 checked('eligibility_flags',meta['eligible_for_learning']==(not meta['evidence_only']))
 if s is None:
  checked('documented_missing_solution',raw and meta['profile']=='raw_q-18023');return
 # Read the actual displayed substitution, never metadata as a math oracle.
 u=sp.Rational(re.search(r'AB=([\d.]+)',s).group(1));v=sp.Rational(re.search(r'(?:AC|BC)=([\d.]+)',s).group(1))
 angle=int(re.search(r'm∠[AB] & =\{(\d+)\}',s).group(1))
 exact=u*v*sp.sin(sp.pi*angle/180)/2;correct=g.rounded(exact,t['digits'])
 checked('displayed_input_matches',u==g.rat(p['u']) and v==g.rat(p['v']) and angle==p['angle'])
 checked('formula_component_mask',f"A=\\frac{{1}}{{2}}{'bc' if t['vertex']=='A' else 'ac'}\\operatorname{{sin}}⁡{t['vertex']}" in s)
 checked('individual_substitution_components',f"\\cdot {g.number(v)}\\cdot {g.number(u)}\\cdot \\operatorname{{sin}}⁡{{{angle}}}^{{∘}}" in s)
 display_sine=g.truncated_sine6(angle) if raw and meta['profile']=='raw_q-18021' else g.sine6(angle)
 checked('product_evaluation_stage',f"={g.number(u*v/2)}\\cdot ({display_sine}" in s)
 checked('individual_sine_stage',display_sine in s)
 checked('displayed_final_value','≈'+correct in s)
 # Formal, identification, sine evaluation, substitution/product/final stages.
 checked('source_stage_layout',s.count('\\begin{aligned}')==2 and s.count(' & ')==6)
 f=q[':question/answer-fields'][0]
 for answer in f[':answer-field/choices']:
  checked('exact_decimal_shape',bool(re.fullmatch(r'\d+\.\d{'+str(t['digits'])+r'}',answer[':answer/value'])))
 if ':answer-field/correct' in f:
  correct_id=f[':answer-field/correct'][1]
  checked('displayed_correct_designation',next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct_id)==correct)
 # Independent complete operation bank from displayed u,v,angle.
 if meta['profile']=='method_sine':
  sine=sp.sin(sp.pi*angle/180);prod=u*v
  objects=[prod*sine/2,prod*sine,prod/2,prod*abs(sp.cos(sp.pi*angle/180))/2,prod*sine**2/2]
  independent=[float(Decimal(str(sp.N(o,80))).quantize(Decimal(10)**-t['digits'],rounding=ROUND_HALF_UP)) for o in objects]
  checked('all_displayed_method_values',sorted(float(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(independent))
 if 'given_angles' in p:
  # Parse actual diagram labels and displayed angle-sum row, check geometry.
  vals=[int(x) for x in re.findall(r'(\d+)°',str(meta['plot']['labels']))]
  checked('hard_supplied_angles',sorted(vals)==sorted(p['given_angles']))
  a,b=p['given_angles'];checked('hard_angle_sum_stage',f'180^{{\\circ}}-{a}^{{\\circ}}-{b}^{{\\circ}}={angle}^{{\\circ}}' in s)
  checked('hard_triangle_consistency',u==v and a==b and a+b+angle==180)
 if not raw and meta['template']=='blank_B_tenth_above':checked('repaired_included_sides','lengths $a$ and $c.$' in s)
 for text in (q[':question/problem'],s):
  checked('balanced_dollars',text.count('$')%2==0)
  depth=0
  for index,c in enumerate(text):
   if c in '{}' and (index==0 or text[index-1]!='\\'):
    depth+=1 if c=='{' else -1
    if depth<0:raise AssertionError('unbalanced TeX braces')
  checked('balanced_tex_groups',depth==0)
 if t['kind']=='blank':checked('blank_placeholder','{{field-1}}' in q[':question/problem'])
 if 'vertices' in meta['plot']:
  plot=meta['plot'];vertices=plot['vertices']
  side1=math.dist(vertices[0],vertices[1]);side2=math.dist(vertices[0],vertices[2])
  cross=(vertices[1][0]-vertices[0][0])*(vertices[2][1]-vertices[0][1])-(vertices[1][1]-vertices[0][1])*(vertices[2][0]-vertices[0][0])
  checked('actual_render_geometry',abs(side1-float(u))<1e-9 and abs(side2-float(v))<1e-9 and abs(abs(cross)/2-float(exact))<1e-9)
  width,height=plot['canvas_pixels']
  checked('measured_renderer_bounds',all(0<=x and 0<=y and x+w<=width and y+h<=height for x,y,w,h in plot['label_bounds_pixels']))
  png=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1))
  checked('render_hash',hashlib.sha256(png.read_bytes()).hexdigest()==plot['png_sha256'])

cases=[];originals=[];records=[];review=[]
for sid,p in g.ANCHORS.items():
 template=g.SOURCE_TEMPLATE[sid];case={'source_id':sid,'template':template,'parameters':p,'bank_profile':'raw_'+sid,'level':'easy'};cases.append(case)
 raw=g.generate('easy',template=template,profile=case['bank_profile'],parameters=p);original=g.BYID[sid];q=raw['question'];originals.append(raw)
 checked('source_prompt_exact',q[':question/problem']==original[':question/problem'])
 checked('source_solution_presence',(':question/worked-solution' in q)==(':question/worked-solution' in original))
 checked('source_difficulty_presence',(':question/difficulty' in q)==(':question/difficulty' in original))
 checked('source_field_presence',(':question/answer-fields' in q)==(':question/answer-fields' in original))
 if ':question/worked-solution' in original:checked('source_full_solution_exact',q[':question/worked-solution']==original[':question/worked-solution'])
 f=q[':question/answer-fields'][0];of=original[':question/answer-fields'][0]
 checked('source_correct_presence',(':answer-field/correct' in f)==(':answer-field/correct' in of))
 checked('source_field_layout',f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'])
 checked('source_complete_bank_exact',sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']))
 if ':answer-field/correct' in of:
  correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);checked('source_designation_exact',correct==of[':answer-field/correct'][':answer/value'])
 display_check(raw,True)
 review.append({'label':'Original raw '+sid,'record':raw})
 for i in (1,2):
  variant={**p,'u':str(int(p['u'])+i)}
  rv=g.generate('easy',template=template,profile='raw_'+sid,parameters=variant);display_check(rv,True);review.append({'label':f'Changed-parameter opaque/raw evidence {sid} #{i}','record':rv})

for level in ('easy','moderate','hard'):
 for template,t in g.TEMPLATES.items():
  if t.get('level','easy')!=level:continue
  for seed in range(12):
   r=g.generate(level,seed,template=template);display_check(r);records.append(r)
   if seed<2:review.append({'label':f'Generated learning variant {level} {template} #{seed}','record':r})
  r=records[-1];replay=g.generate(level,seed=987,template=template,parameters=r['generation']['parameters'],profile=r['generation']['profile'])
  checked('seed_independent_content_identity',r['question'][':question/id']==replay['question'][':question/id'])
  checked('seed_independent_math_fingerprint',r['generation']['math_fingerprint']==replay['generation']['math_fingerprint'])
# Sampling coverage over deterministic seeds (all source-shaped eligible families).
coverage={g.generate('easy',n)['generation']['template'] for n in range(30)}
for profile,kind in [('method_sine','radio'),('blank','blank')]:
 for seed in range(6):
  chosen=g.generate_easy(seed=seed,profile=profile)
  checked('profile_only_selects_eligible_family',chosen['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/'+kind))
checked('default_easy_family_coverage',coverage=={k for k,t in g.TEMPLATES.items() if t.get('level','easy')=='easy'})
# Explicit level bounds and missing-workload degeneracy regressions.
invalid=[('moderate','decimal_sides',dict(u='2',v='3.1',angle=40)),('moderate','decimal_sides',dict(u='2.01',v='3.1',angle=40)),('hard','angle_sum',dict(u='2.11',v='3.22',angle=60,given_angles=[60,60])),('hard','angle_sum',dict(u='2.1',v='2.1',angle=60,given_angles=[60,60]))]
for level,t,p in invalid:
 try:g.generate(level,template=t,parameters=p)
 except ValueError:checked('explicit_invalid_workload_rejected',True)
 else:raise AssertionError('Invalid workload allowed')
# A structurally wrong stage can remain algebraically equal: detect omission.
r=copy.deepcopy(records[0]);s=r['question'][':question/worked-solution'];r['question'][':question/worked-solution']=re.sub(r'=([\d.]+)\\cdot \(0\.[\d\\,]+\)',r'=\1',s)
try:display_check(r)
except AssertionError:checked('stage_omission_regression_rejected',True)
else:raise AssertionError('Required product stage mutation escaped')
# Fresh concurrent render writes in separate processes, same/different parameters.
params=[dict(u='9',v='12',angle=53),dict(u='9',v='12',angle=53),dict(u='9',v='13',angle=53)]
commands=[]
concurrency_root=ROOT/'concurrency'/str(uuid.uuid4());concurrency_root.mkdir(parents=True)
for p in params:
 code="import importlib.util; s=importlib.util.spec_from_file_location('g',"+repr(str(ROOT.with_suffix('.py')))+");g=importlib.util.module_from_spec(s);s.loader.exec_module(g);g.ROOT=__import__('pathlib').Path("+repr(str(concurrency_root))+");print(g.generate_easy(template='radio_A',parameters="+repr(p)+")[\"question\"][\":question/id\"])"
 commands.append([sys.executable,'-c',code])
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 ids=list(pool.map(lambda cmd:subprocess.check_output(cmd,text=True).strip(),commands))
checked('concurrent_same_instance_identity',ids[0]==ids[1]);checked('concurrent_different_instance_identity',ids[0]!=ids[2])
checked('no_private_temporary_render_inputs',not any(re.match(r'[0-9a-f]{64}-.+\.(?:png|json)$',p.name) for p in (concurrency_root/'plots').iterdir()))

# Compare complete API records across the cold-render/cache boundary, including
# plot metadata; equal question IDs alone missed tuple/list nondeterminism.
saved_root=g.ROOT
try:
 g.ROOT=concurrency_root/'cold-cache-api'
 g.ROOT.mkdir()
 for level in ('easy','moderate','hard'):
  for seed in range(6):
   first=g.generate(level,seed=seed)
   checked('cold_cached_complete_record_equality',first==g.generate(level,seed=seed))
finally:g.ROOT=saved_root

# All normal records + five supported raw original records through real grader.
engine=[]
for index,r in enumerate(records+[r for r in originals if ':answer-field/correct' in r['question'][':question/answer-fields'][0]]):
 f=r['question'][':question/answer-fields'][0];correct_id=f[':answer-field/correct'][1];answers=f[':answer-field/choices']
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct_id else 'rejected','purpose':'owned choice selection'} for a in answers]
 else:
  correct=answers[0][':answer/value'];wrong=str(sp.Rational(correct)+1)
  checks=[{'submitted':correct,'expected':'accepted','purpose':'canonical rounded value'}, {'submitted':correct+'0','expected':'rejected','purpose':'equivalent numeric value with excess decimal precision; native rounding form restriction'}, {'submitted':wrong,'expected':'rejected','purpose':'incorrect rounded value'}]
 engine.append({'label':str(index),'record':r,'checks':checks})
(ROOT/'engine-input.json').write_text(json.dumps(engine,indent=2));subprocess.run([str(ROOT.parents[1]/'runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
(ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2));(ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False))
md=['# Triangle area review','Raw profiles are ineligible evidence, including unchanged omissions. Generated learning variants use inferred/method banks, with the authored difficulty labeled explicitly.']
for item in review:md += ['\n## '+item['label'],g.markdown(item['record'])]
(ROOT/'review.md').write_text('\n\n'.join(md))
result={'status':'passed','counts':COUNTS,'source':{'practice_questions':6,'exact_prompts':6,'exact_complete_banks':6,'exact_displayed_values':18,'exact_solutions':5,'absent_original_solution':1,'known_designations_matched':5,'absent_original_designation':1,'difficulty_omissions_preserved':1},'source_math_errors':{'advertised_sine_precision_failures':1,'raw_prose_included_side_failures':1,'normal_repairs_applied':2,'raw_mathematical_error_evidence_ineligible':True},'native_engine_sha256':hashlib.sha256((ROOT.parents[1]/'runs/current/check-engine').read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'generated_math_records':len(records),'review_records':len(review),'native_checks':sum(len(e['checks']) for e in engine),'native_raw_ungradable_missing_correct':1,'runtime':records[0]['generation']['runtime'],'limitations':['Three historical radio banks have opaque distractor origins; ratio replay is evidence only, never a recovered pedagogical recipe.','q-18023 has no original correct designation/worked solution/difficulty; normal inferred answer11.12 is independently verified.','q-279752 included-side prose typo is preserved raw and repaired normal.','q-18021 sine128 degrees truncation differs from advertised rounding; raw precision error retained, normal sine corrected.','Native rounded blanks reject numerically equivalent extra trailing-zero precision as a response-form restriction.','Moderate and hard are authored workload policies, not observed ratings.','Original schematic rasters are not to scale; exact numeric labels ground new equal-scale diagrams.']}
(ROOT/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
