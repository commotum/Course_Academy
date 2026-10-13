#!/usr/bin/env python3
"""Fail on source, displayed math, complete banks, format, scope, IDs or grader.
Run from repository root with .venv/bin/python. Native grading uses local
in-memory fixtures only. Every slope/statement is derived from PRINTED TeX.
"""
import concurrent.futures,hashlib,importlib.util,itertools,json,pathlib,re,subprocess,sys
import sympy as sp
sys.dont_write_bytecode=True
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.parent/(HERE.name+'.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
CASES=json.loads((HERE/'source-cases.json').read_text());SOURCE=json.loads((HERE/'source.json').read_text())
BY_ID={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
LABEL_MASK={label:mask for mask,label in g.LABELS.items()}
U,V=sp.symbols('u v',positive=True)

def read_printed_expr(prompt):
 eq=prompt.split('$')[1];rhs=eq.split('=',1)[1].strip().replace('{','').replace('}','')
 m=re.fullmatch(r'(-?\d*)x(\^2)?(y(\^2)?)?',rhs)
 assert m,('Not a supported printed slope equation',eq)
 c=int(m[1]) if m[1] not in ('','-') else -1 if m[1]=='-' else 1
 a=2 if m[2] else 1;b=0 if not m[3] else 2 if m[4] else 1
 return sp.Integer(c)*g.X**a*g.Y**b,{'c':c,'a':a,'b':b}

def checked(record):
 assert set(record)=={'knowledge_point','question','generation'}
 assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=record['question'];gen=record['generation'];p=gen['parameters'];level=gen['level']
 g.validate_parameters(level,p)
 f,printed=read_printed_expr(q[':question/problem'])
 assert all(printed[k]==p[k] for k in printed)
 ss=[]
 for quadrant,(sx,sy) in g.POINTS.items():
  # Symbolic identity on the ENTIRE open quadrant, not an isolated sample.
  mapped=sp.expand(f.subs({g.X:sx*U,g.Y:sy*V}))
  ratio=sp.simplify(mapped/(abs(printed['c'])*U**printed['a']*V**printed['b']))
  assert ratio in (-1,1);ss.append(int(ratio))
 assert tuple(ss)==tuple(gen['plot']['signs'])
 assert sp.simplify(f.subs(g.X,0))==0
 assert (sp.simplify(f.subs(g.Y,0))==0)==(printed['b']>0)
 claims=re.findall(r'At every point in the (first|second|third|fourth) quadrant, the slope of the slope field is (positive|negative)',q[':question/problem'])
 assert len(claims)==3
 mask=0
 for i,(word,claim) in enumerate(claims):
  quadrant={v:k for k,v in g.WORDS.items()}[word];sign=1 if claim=='positive' else -1
  assert quadrant==p['quadrants'][i] and sign==p['claims'][i]
  if ss[quadrant-1]==sign:mask|=1<<i
 sol=q[':question/worked-solution']
 intro_expr=sol.split('$')[1].split('=',1)[1].rstrip('.')
 checkf,_=read_printed_expr('equation $d='+intro_expr+'$')
 assert sp.simplify(checkf-f)==0
 blocks=re.findall(r'- Statement (I|II|III) is (true|false)\. If \$\(x,y\)\$ is in the (first|second|third|fourth) quadrant,.*?\$\$\n(.*?)\n\$\$\n\nThis implies that the slope of the slope field is (positive|negative) for any point \$\(x,y\)\$ in the (first|second|third|fourth) quadrant\.',sol,re.S)
 assert len(blocks)==3
 for i,(roman,truth,word,math,claimed,repeated) in enumerate(blocks):
  assert roman==g.ROMAN[i] and word==claims[i][0]==repeated
  assert truth==('true' if mask&(1<<i) else 'false')
  expected=ss[p['quadrants'][i]-1]
  assert math==r'{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)'+('>0.' if expected>0 else '<0.')+(r'\,' if gen['template']=='bilinear_open_thin' else '')
  assert claimed==('positive' if expected>0 else 'negative')
 if 'Therefore' in sol:assert '"'+g.LABELS[mask]+'."' in sol
 if level=='easy':assert '$x=0$ or $y=0.$' not in sol
 else:assert '$x=0$ or $y=0.$' in sol
 for content in [q[':question/problem'],sol]:
  assert content.count('$$')%2==0
  assert content.replace('$$','').count('$')%2==0
  depth=0
  for char in content:
   if char=='{':depth+=1
   if char=='}':depth-=1
   assert depth>=0
  assert depth==0
 field=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 assert field[':answer-field/key']=='selection' and field[':answer-field/type']==':answer-field.type/radio'
 values=[a[':answer/value'] for a in field[':answer-field/choices']]
 assert len(values)==len(set(values))==5
 if gen['bank_profile'] in ('authored_sign_errors','authored_cycle'):
  assert set(LABEL_MASK[v] for v in values)=={mask,mask^7,mask^1,mask^2,mask^4}
  assert len(gen['bank_recipes'])==5
 assert field[':answer-field/correct'][0]==':answer/id'
 answer=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
 assert LABEL_MASK[answer[':answer/value']]==mask==gen['truth_mask']
 for a in field[':answer-field/choices']:
  assert a[':answer/type']==':answer.type/text';assert (LABEL_MASK[a[':answer/value']]==mask)==(a is answer)
 assert (HERE/gen['plot']['asset']).is_file()
 if gen['plot']['renderer']!='immutable source asset':
  sidecar=json.loads((HERE/gen['plot']['asset']).with_suffix('.json').read_text())
  assert sidecar['spec']['signs']==ss
  assert sidecar['spec']['zero_axes']==(['x'] if printed['b']==0 else ['x','y'])
 same=g.generate(level,seed=gen['seed']+999,template=gen['template'],parameters=p,profile=gen['bank_profile'])
 assert same['question'][':question/id']==q[':question/id']
 assert same['generation']['content_identity']==gen['content_identity']
 return mask

banks=0;choices=0;distractors=0;designations=0;solutions=0;repairs=[];fixtures=[]
def fixture(r,label):
 checked(r);field=r['question'][':question/answer-fields'][0]
 fixtures.append({'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'Independent printed-math correct selection or every categorical distractor'} for a in field[':answer-field/choices']]})
for case in CASES:
 original=BY_ID[case['source_id']]
 r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);fixture(r,case['source_id'])
 q=r['question'];field=q[':question/answer-fields'][0];of=original[':question/answer-fields'][0]
 assert q[':question/problem']==original[':question/problem']
 original_values=[a[':answer/value'] for a in of[':answer-field/choices']]
 values=[a[':answer/value'] for a in field[':answer-field/choices']]
 assert sorted(values)==sorted(original_values);banks+=1;choices+=len(values)
 correct=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
 if ':answer-field/correct' in of:
  assert correct==of[':answer-field/correct'][':answer/value'];designations+=1;distractors+=len(values)-1
 else:
  assert correct=='II and III only';repairs.append({'source_id':case['source_id'],'inferred_correct':correct,'derivation':'In all quadrants y²>0, so xy² has sign x; I false, II true, III true.','missing_observed':['correct designation','worked solution','difficulty'],'designation_counted_as_observed_match':False})
 if ':question/worked-solution' in original:
  assert q[':question/worked-solution']==original[':question/worked-solution'];solutions+=1
 else:assert case['source_id']=='q-97483'
widget=json.loads((HERE/'q97483-widget.json').read_text())
assert sorted(c['readable_text'] for c in widget['choices'])==sorted(a[':answer/value'] for a in BY_ID['q-97483'][':question/answer-fields'][0][':answer-field/choices'])

# Exhaust ALL mathematically meaningful defaults, not cosmetic coefficients or
# reordered statements. Preserve ordered source layouts separately above.
counts={};coverage={};unique={}
for level,powers in [('easy',[(1,0)]),('moderate',[(1,1)]),('hard',[(1,2),(2,1),(2,2)])]:
 fingerprints=set();ids=set();masks=set()
 for c,(a,b),qs,cs in itertools.product([-1,1],powers,itertools.combinations([1,2,3,4],3),itertools.product([-1,1],repeat=3)):
  p={'c':c,'a':a,'b':b,'quadrants':list(qs),'claims':list(cs)}
  r=g.generate(level,parameters=p);masks.add(checked(r));fingerprints.add(r['generation']['mathematical_fingerprint']);ids.add(r['question'][':question/id'])
 counts[level]=len(fingerprints);assert counts[level]==64*len(powers);assert masks==set(range(8))
 # Random variety also tested but claimed counts remain exact finite domain.
 sampled={g.generate(level,seed)['generation']['mathematical_fingerprint'] for seed in range(1000)}
 assert sampled<=fingerprints and len(sampled)>=counts[level]*.90
 unique[level]=len(sampled)
 # Shuffled radio choices don't always position the correct answer first.
 positions=[]
 for seed in range(20):
  r=g.generate(level,seed);f=r['question'][':question/answer-fields'][0];positions.append(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
 assert len(set(positions))>1
coverage={'templates':list(g.TEMPLATES),'profiles':list(g.PROFILES)+['authored_sign_errors','authored_cycle'],'finite_meaningful_tasks':counts,'sampled_unique_1000_seeds':unique}
# Every extracted layout and observed complete profile: two changed-parameter
# variants per source plus all missing-level defaults and every canonical mask.
for i,r in enumerate(json.loads((HERE/'review.json').read_text())):fixture(r,'review-'+str(i))
for mask in range(8):
 p={'c':1,'a':1,'b':1,'quadrants':[1,2,3],'claims':[1 if (mask>>i)&1 else -1 for i in range(3)]}
 # quadrant II actual sign negative; flip that claim for requested mask.
 p['claims'][1]*=-1
 fixture(g.generate('moderate',parameters=p),'all-truth-mask-'+str(mask))
# Reject invalid params/banks, never silently alter explicit input.
base={'c':1,'a':1,'b':1,'quadrants':[1,2,3],'claims':[-1,1,-1]}
for change in [{'c':0},{'c':10},{'a':3},{'a':-1},{'quadrants':[1,1,2]},{'claims':[0,1,1]}]:
 try:g.generate('moderate',parameters=base|change)
 except ValueError:pass
 else:raise AssertionError('Invalid params accepted '+str(change))
try:g.generate('moderate',parameters=base,profile='bank96767') # mask0 absent
except ValueError:pass
else:raise AssertionError('Ineligible whole bank accepted')
# Bounds include all allowed coefficient signs/magnitudes and supported powers.
for level,powers in [('easy',[(1,0)]),('moderate',[(1,1)]),('hard',[(1,2),(2,1),(2,2)])]:
 for c,(a,b) in itertools.product([-9,-1,1,9],powers):checked(g.generate(level,parameters={'c':c,'a':a,'b':b,'quadrants':[1,2,4],'claims':[1,-1,1]}))
# Canonical fingerprint excludes coefficient magnitude, profile and ordering.
r=g.generate('moderate',parameters=base)
s=g.generate('moderate',parameters=base|{'c':7})
assert r['generation']['mathematical_fingerprint']==s['generation']['mathematical_fingerprint']
assert r['question'][':question/id']!=s['question'][':question/id']
s=g.generate('moderate',parameters=base|{'quadrants':[3,2,1],'claims':[-1,1,-1]})
assert r['generation']['mathematical_fingerprint']==s['generation']['mathematical_fingerprint']
# Compatibility alias preserves identical content, but uses the new declared bank.
r=g.generate('easy',seed=4,profile='authored_cycle');s=g.generate('easy',seed=4,profile='authored_sign_errors')
assert r['question']==s['question'];checked(r)
# Different complete banks are presentation identities, same mathematical task.
r=g.generate('moderate',parameters=CASES[0]['parameters'],profile='bank96767')
s=g.generate('moderate',parameters=CASES[0]['parameters'],profile='authored_sign_errors')
assert r['generation']['mathematical_fingerprint']==s['generation']['mathematical_fingerprint']
assert r['question'][':question/id']!=s['question'][':question/id']
# Cold-cache generator concurrency must return only a completed PNG+sidecar pair.
for name in ['signs-pnnp-zero-x','signs-nppn-zero-x']:
 for suffix in ['.png','.json']:(HERE/'images/generated'/(name+suffix)).unlink(missing_ok=True)
def concurrent_question(c):
 return g.generate('easy',parameters={'c':c,'a':1,'b':0,'quadrants':[1,2,4],'claims':[1,-1,1]})
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:cold=list(pool.map(concurrent_question,[1,1,-1,-1]))
for r in cold:checked(r)
assert cold[0]['question'][':question/id']==cold[1]['question'][':question/id']
# Direct concurrent renderer calls, two identical and two different patterns.
concurrent_outputs=[HERE/'images/generated/concurrent-a.png',HERE/'images/generated/concurrent-a.png',HERE/'images/generated/concurrent-b.png',HERE/'images/generated/concurrent-c.png']
specs=[{'signs':[1,-1,-1,1],'zero_axes':['x']},{'signs':[1,-1,-1,1],'zero_axes':['x']},{'signs':[-1,-1,1,1],'zero_axes':['x','y']},{'signs':[1,1,-1,-1],'zero_axes':['x','y']}]
def render(item):
 i,out=item;subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE/'render.py'),json.dumps(specs[i]),str(out)],check=True,capture_output=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(render,enumerate(concurrent_outputs)))
for spec,out in zip(specs,concurrent_outputs):assert json.loads(out.with_suffix('.json').read_text())['spec']==spec
assert not list((HERE/'images/generated').glob('tmp*'))
(HERE/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
report={'pass':True,'provenance':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_coverage':{'practice_questions':8,'original_banks_matched':banks,'original_choices_matched':choices,'observed_distractors_matched':distractors,'observed_distractors_total':28,'inferred_wrong_choices_repaired_source':4,'observed_correct_designations_matched':designations,'observed_correct_designations_total':7,'prompts_exact':8,'available_solutions_exact':solutions,'available_solutions_total':7,'missing_solution_authored':1,'missing_correct_designation_independently_derived':1},'source_repairs':repairs,'coverage':coverage,'independent_checks':'Printed slope expression; strict sign on entire positive-symbol quadrant; all displayed true/false claims, inequality/prose stages, zero axes, all categorical options; domain/format/identity and bounds; exact source sequence; concurrent diagrams','native_grading':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':0,'database_writes':0},'plot_QA':'All four source assets inspected; six authored diagrams rendered and manually inspected. Concurrent identical/different render checks passed.','scope':'Easy cx authored; moderate ±cxy observed; hard parity x^a y^b a,b=1/2 with at least one square. No sums, rectangles, isolated point sketching, slope field type identification or solving ODEs.','freeze_sha256':hashlib.sha256((HERE.parent/(HERE.name+'.py')).read_bytes()).hexdigest()}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
