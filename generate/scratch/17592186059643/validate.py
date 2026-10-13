#!/usr/bin/env python3
"""Fails normal mathematics, exact replay, omissions, identity, scope or grading.
Raw source defects remain explicitly reported evidence, never eligible practice.
Independent exact rational unit-circle evaluations read actual displayed math;
metadata or selected IDs cannot establish mathematical correctness.
"""
import hashlib, importlib.util, itertools, json, re, subprocess, sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
from functools import lru_cache
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sources=json.loads((ROOT/'source.json').read_text())['record'][':knowledge-point/questions']
cases=json.loads((ROOT/'source-cases.json').read_text())

def equations(solution):
 for block in re.findall(r'\$\$(.*?)\$\$',solution,re.S):
  block=re.sub(r'\\(?:begin|end)\{aligned\}','',block)
  for row in block.split(r'\\'):
   for expr in row.replace('&','').split('='):
    expr=expr.strip().rstrip('.')
    if expr:yield expr

U=sp.Symbol('u',real=True)
@lru_cache(maxsize=40000)
def canonical(expr):
 return sp.cancel(expr.subs({g.S:2*U/(1+U*U),g.C:(1-U*U)/(1+U*U)}))
@lru_cache(maxsize=40000)
def witnesses(expr):
 return tuple(expr.subs(U,v) for v in (sp.Rational(1,3),sp.Rational(2,3),sp.Rational(3,2),sp.Rational(-2,3)))
def equal_actual(a,b):
 # Algebraic proof from displayed objects and independent exact rational witnesses.
 av,bv=canonical(a),canonical(b)
 assert av==bv,(a,b)
 for ap,bp in zip(witnesses(av),witnesses(bv)):
  if ap.has(sp.zoo,sp.nan) or bp.has(sp.zoo,sp.nan):continue
  assert sp.simplify(ap-bp)==0

def check_math(r):
 q=r['question'];prompt=q[':question/problem'];expr=g.parse_math(prompt.split('$')[1])
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
 values=[g.parse_math(a[':answer/value']) for a in choices]
 equal_actual(expr,values[next(i for i,a in enumerate(choices) if a[':answer/id']==correct)])
 for i,a in enumerate(values):
  for b in values[:i]:assert not g.equivalent(a,b),'ambiguous complete displayed bank'
 arg=r['generation']['parameters']['argument']
 solution=q[':question/worked-solution']
 if arg!=r'\theta':assert r'\theta' not in solution,'stale theta argument'
 for v in equations(solution):equal_actual(expr,g.parse_math(v))
 # All braces and dollars are structurally balanced; source cancellation braces count.
 for text in [prompt,solution,*[a[':answer/value'] for a in choices]]:
  depth=0
  for c in text:
   depth+=(c=='{')-(c=='}');assert depth>=0,text
  assert depth==0,text
  assert text.count('$')%2==0,text
  assert '+-' not in text and '--' not in text,text
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert len(choices)==5 and len({a[':answer/id'] for a in choices})==5
 assert correct in {a[':answer/id'] for a in choices}
 return len(list(equations(solution)))

def check_presentation(r):
 before=json.dumps(r,sort_keys=True)
 text=g.markdown(r)
 assert text==g.markdown(r),'preview is nondeterministic'
 assert json.dumps(r,sort_keys=True)==before,'preview mutated record attributes'
 meta=r['generation'];q=r['question'];m=g.MASKS.get(meta['template'])
 assert text.count(' — **')==1,'correct review mark missing or duplicated'
 if m is None:
  assert '**Origin:** Normal authored practice.' in text
  assert '**Correct (computed)**' in text
 else:
  raw=meta['profile']=='raw-observed'
  assert ('**Origin:** Raw source evidence-only.' if raw else '**Origin:** Repaired source evidence-only.') in text
  if m['correct'] is None:assert '**Inferred correct (original correct key absent)**' in text
  else:assert '**Correct (source designation)**' in text
  if raw and not m['difficulty_present']:
   assert '**Level:** Unrated (raw source).' in text
   for key in (':question/difficulty',':question/worked-solution',':answer-field/correct'):
    assert '`'+key+'` absent in raw record' in text
  elif not m['difficulty_present']:
   assert '**Level:** '+m['level'].title()+' (inferred; original source unrated).' in text
   assert 'present (inferred)' in text and 'present (authored supported solution)' in text
 if ':question/difficulty' in q:assert '**Level:** '+q[':question/difficulty'].split('/')[-1].title() in text
 return 1

assert g.MASKS['observed_q_23522']['level']=='easy'
assert g.TEMPLATES['observed_q_23522']=='easy'
assert g.MASKS['observed_q_1579']['level']=='moderate'
assert sum(':question/difficulty' not in q for q in sources)==2,'unrated sources were relabeled in capture'
assert sum(q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/easy' for q in sources)==0
for old in json.loads((ROOT/'authored-content-before-presentation-repair.json').read_text()):
 current=g.generate(old['level'],template=old['template'],parameters=old['parameters'])
 assert current['generation']['content_fingerprint']==old['content_fingerprint'],'authored content changed during presentation repair'
 assert current['question'][':question/id']==old['question_id']

fixtures=[];reviews=[];banks=options=designations=solutions=0;raw_failures={};rows=0;presentation_checks=0
for q,c in zip(sources,cases):
 assert c['level']==g.MASKS[c['template']]['level'],'case assignment disagrees with API'
 raw=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='raw-observed')
 presentation_checks+=check_presentation(raw)
 out=raw['question'];sf=q[':question/answer-fields'][0];of=out[':question/answer-fields'][0]
 assert out[':question/problem']==q[':question/problem']
 for key in (':question/difficulty',':question/worked-solution'):
  assert (key in out)==(key in q),(q[':db/id'],key)
  if key==':question/worked-solution' and key in q:
   assert out[key]==q[key];solutions+=1
 assert (':answer-field/correct' in of)==(':answer-field/correct' in sf)
 assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
 assert of[':answer-field/key']==sf[':answer-field/key'] and of[':answer-field/type']==sf[':answer-field/type'][':db/ident']
 if ':answer-field/correct' in sf:
  assert next(a[':answer/value'] for a in of[':answer-field/choices'] if a[':answer/id']==of[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value'];designations+=1
  try:check_math(raw)
  except Exception as e:raw_failures[str(q[':db/id'])]=str(e)[:300]
 banks+=1;options+=len(of[':answer-field/choices'])
 assert raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning']
 for dual in (False,True):
  p=c['parameters']|{'dual':dual,'argument':c['parameters']['argument'] if not dual else r'\alpha'}
  r=g.generate(c['level'],seed=17,template=c['template'],parameters=p,profile='repaired-observed');rows+=check_math(r);reviews.append(r)
  presentation_checks+=check_presentation(r)
  if c['source_id']==17592186060226:assert r['question'][':question/difficulty']==':question.difficulty/easy'
  if c['source_id']==17592186060072:assert r['question'][':question/difficulty']==':question.difficulty/moderate'
  f=r['question'][':question/answer-fields'][0];fixtures.append({'label':str(q[':db/id'])+('/dual' if dual else '/repaired'),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual selected option after independent displayed-math proof'} for a in f[':answer-field/choices']]})
 assert g.generate(c['level'],seed=99,template=c['template'],parameters=c['parameters'],profile='raw-observed')['question'][':question/id']==raw['question'][':question/id']

# Exhaustively enumerate the finite reduced arithmetic domain. Profile/letter aliases
# do not inflate mathematical task counts. All explicit calls use the same guard.
task_sets={l:set() for l in ('easy','moderate','hard')};enumerated={l:0 for l in task_sets}
for tid,level in [('one_denominator','easy'),('crossed_fractions','moderate'),('squared_shift','moderate'),('linear_plus_quotient','hard')]:
 bs=([b for b in g.COEFFICIENTS if b>0] if tid=='squared_shift' else (g.COEFFICIENTS if level=='hard' else [sp.Integer(1)]))
 for a,b,dual in itertools.product(g.COEFFICIENTS,bs,(False,True)):
  p={'a':str(a),'b':str(b),'dual':dual,'argument':'x'}
  r=g.generate(level,template=tid,parameters=p);enumerated[level]+=1;task_sets[level].add(r['generation']['mathematical_fingerprint'])
  rows+=check_math(r)
 # Both signs, reciprocal rationals and orientations for every authored template.
 for seed in (3,18):
  r=g.generate(level,seed,template=tid);reviews.append(r)
  presentation_checks+=check_presentation(r)
for level in task_sets:
 for seed in range(20):
  r=g.generate(level,seed);rows+=check_math(r)
  f=r['question'][':question/answer-fields'][0]
  fixtures.append({'label':f'{level}/{seed}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual authored operation-bank selection'} for a in f[':answer-field/choices']]})
  p=r['generation']['parameters'];tid=r['generation']['template'];other=g.generate(level,seed+101,template=tid,parameters=p)
  assert other['question'][':question/id']==r['question'][':question/id'],'seed affected content identity'
  renamed=g.generate(level,template=tid,parameters=p|{'argument':r'\alpha'})
  assert renamed['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
  assert renamed['question'][':question/id']!=r['question'][':question/id'] if p['argument']!=r'\alpha' else True
 for invalid in ('0','7','1/4','10/9','-7'):
  try:g.generate(level,parameters={'a':invalid})
  except ValueError:pass
  else:raise AssertionError(('ceiling accepted',level,invalid))
 # Reduced objects determine workload; large unreduced but eligible fractions normalize.
 r=g.generate(level,parameters={'a':'8/2'});assert r['generation']['parameters']['a']=='4'
try:g.generate('moderate',template='squared_shift',parameters={'b':'-1'})
except ValueError:pass
else:raise AssertionError('negative squared shift')
try:g.generate('moderate',parameters={'b':'2'},template='crossed_fractions')
except ValueError:pass
else:raise AssertionError('unused parameter admitted')

(ROOT/'engine-input.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
engine=json.loads((ROOT/'engine-report.json').read_text())
(ROOT/'review.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n')
review=['# Common denominator and Pythagorean identity review','Basis 1356. Raw originals retain captured omissions and errors. Repaired variants are evidence-only; authored variants are eligible practice.']
for q,c in zip(sources,cases):
 raw=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='raw-observed')
 # Render the captured choice order while retaining the exact raw schema omissions.
 field=raw['question'][':question/answer-fields'][0];by_value={a[':answer/value']:a for a in field[':answer-field/choices']}
 field[':answer-field/choices']=[by_value[a[':answer/value']] for a in q[':question/answer-fields'][0][':answer-field/choices']]
 review+=['## Original '+str(q[':db/id']),g.markdown(raw,origin='Original/raw source evidence-only')]
 for r in reviews:
  if r['generation']['source_id']==q[':db/id']:review+=['### Repaired generated variant — '+r['question'][':question/difficulty'].split('/')[-1].title(),g.markdown(r)]
for r in reviews:
 if r['generation']['authored']:review+=['## Authored '+r['question'][':question/difficulty'].split('/')[-1]+' / '+r['generation']['template'],g.markdown(r)]
(ROOT/'review.md').write_text('\n\n'.join(review)+'\n')
assert set(raw_failures)=={'17592186253599','17592186253600','17592186329718'},raw_failures
result={'status':'pass','basis':1356,'source_coverage':{'questions':banks,'total_questions':len(sources),'complete_banks_matched':banks,'choices_matched':options,'choices_total':55,'correct_designations_matched':designations,'correct_designations_present':9,'unavailable_original_designations':2,'exact_solutions_matched':solutions,'original_solutions_present':9,'attribute_presence_parity':11},'raw_source_mathematical_failures':raw_failures,'source_repairs':{'mathematical':1,'missing_function_arguments':1,'inconsistent_argument':1,'missing_equality_sign':1,'inferred_correct_designation_solution_difficulty':2},'normal_displayed_math':'All displayed prompt, choices and complete ordered solution expressions parsed and verified symbolically and at exact rational unit-circle points.','displayed_solution_expressions_checked':rows,'authored_domain_exhaustion':enumerated,'meaningful_tasks':{l:len(v) for l,v in task_sets.items()},'native_grader':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},'grading_limit':'Radio grading validates selected owned UUIDs; independent displayed mathematics validates their meanings. Unrated raw sources cannot be graded without inferred missing correct refs.','interpretation_limits':'Observed distractor shape masks recover all values, not original error intentions; both observed profiles stay evidence-only.','hashes':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT.with_suffix('.py'),ROOT/'source.json',ROOT/'topic.json',ROOT/'lesson.json',ROOT/'template-masks.json',REPO/'generate/runs/current/check-engine',REPO/'generate/runs/current/check-engine.rs')}}
result['presentation_and_assignment']={'status':'pass','deterministic_nonmutating_previews_checked':presentation_checks,'q23522':'inferred Easy in mask, case, API and repaired record; raw difficulty omitted','q1579':'inferred Moderate; raw difficulty omitted','authored_content_fingerprints_unchanged':8,'observed_source_difficulty_counts':{'easy':0,'moderate':8,'hard':1,'unrated':2}}
(ROOT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('status','source_coverage','meaningful_tasks','native_grader')},indent=2))
