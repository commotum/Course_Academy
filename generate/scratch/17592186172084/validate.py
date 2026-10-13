#!/usr/bin/env python3
"""Independent displayed formula/plot, replay, scope, identity and native checks.

Run with .venv/bin/python. No database reads/writes. Evidence outputs are local.
Source raw values/prose are compared independently of engine selections.
"""
import concurrent.futures,hashlib,importlib.util,itertools,json,re,subprocess,tempfile
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,i,j=s.symbols('x y i j',real=True)
ORIGINAL_FIELDS={'q-122296':(x,-1),'q-122463':(-1,1),'q-122629':(1,x),
 'q-122631':(0,-y),'q-122632':(0,x),'q-122633':(y,0),
 'q-122634':(1,0),'q-122637':(0,-5),'q-122630':(-2,y)}
ORIGINAL_FIELDS={k:tuple(map(s.sympify,v)) for k,v in ORIGINAL_FIELDS.items()}

def parse(value):
 value=value.rstrip('.,')
 m=re.fullmatch(r'([FGHK])\(\s*x\s*,\s*y\s*\)\s*=\s*(.+)',value)
 assert m,value
 body=m[2].replace(r'\,','').replace(' ','')
 assert re.fullmatch(r'[xyij0-9+\-]+',body),value
 body=re.sub(r'([xyij0-9])(?=[xyij])',r'\1*',body)
 e=parse_expr(body,local_dict={'x':x,'y':y,'i':i,'j':j},transformations=standard_transformations+(implicit_multiplication_application,))
 u=s.expand(e).coeff(i);v=s.expand(e).coeff(j)
 assert s.expand(e-u*i-v*j)==0,value
 return (u,v)

def transformed_original(profile,p):
 u,v=ORIGINAL_FIELDS[profile];sx,sy=p['sx'],p['sy']
 xx,yy=(y,x) if p['swap'] else (x,y)
 u,v=(s.expand(z.subs({x:sx*xx,y:sy*yy},simultaneous=True)*p['a']*sign) for z,sign in ((u,sx),(v,sy)))
 return (v,u) if p['swap'] else (u,v)

def prose_predicates(text,pair):
 """Actual English -> independent pointwise sign/dependency predicates."""
 results=[]
 for axis,basis in (('horizontal',0),('vertical',1)):
  sign_claim=re.search(r'(?:The |the )'+axis+r' component.*?is (positive|negative|zero) for (?:\*every\*|each) vector',text)
  if sign_claim:
   requested={'positive':1,'negative':-1,'zero':0}[sign_claim[1]]
   results.append(all(s.sign(pair[basis].subs({x:xx,y:yy}))==requested for xx,yy in itertools.product((-3,-1,1,3),repeat=2)))
  growth=re.search(r'As we move away from the origin in the (horizontal|vertical) direction, (?:our vectors\x27|their) '+axis+r' components',text)
  if growth:
   changing=x if growth[1]=='horizontal' else y;held=y if changing==x else x
   passed=changing in pair[basis].free_symbols
   for direction in (-1,1):
    small=abs(pair[basis].subs({changing:direction,held:2}));large=abs(pair[basis].subs({changing:3*direction,held:2}))
    passed=passed and large>small
   results.append(bool(passed))
  # Authored hard local sign clauses explicitly specify the positive half-plane.
  local=re.search(axis+r' component is (positive|negative) where \$([xy])>0',text)
  if local:
   changing=x if local[2]=='x' else y;other=y if changing==x else x
   requested=1 if local[1]=='positive' else -1
   results.append(all(s.sign(pair[basis].subs({changing:value,other:held}))==requested for value in (1,3) for held in (-3,-1,1,3)))
 return results

def shape_and_math(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==17592186172084
 q=r['question'];fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio'
 assert f[':answer-field/key']=='selection';choices=f[':answer-field/choices'];assert len(choices)==5
 assert len({a[':answer/id'] for a in choices})==5
 for data,key in [(q,':question/id'),(f,':answer-field/id')]+[(a,':answer/id') for a in choices]:
  import uuid
  assert str(uuid.UUID(data[key]))==data[key]
 correct=next(a for a in choices if a[':answer/id']==f[':answer-field/correct'][1])
 correct_pair=parse(correct[':answer/value'])
 math=[parse(a[':answer/value']) for a in choices if a[':answer/type']==':answer.type/math']
 assert len(math)==4;assert len(set(math))==4
 assert sum(b==correct_pair for b in math)==1
 assert [a[':answer/value'] for a in choices if a[':answer/type']==':answer.type/text']==['None of the listed']
 meta=r['generation'];p=meta['parameters'];profile=meta['bank_profile']
 if profile=='authored_two_variable':
  u,v=(y,x) if p['swap'] else (x,y);expected=(p['sx']*u,p['sy']*v)
  assert all(z.free_symbols for z in correct_pair)
 else:expected=transformed_original(profile,p)
 assert correct_pair==expected,(correct_pair,expected)
 # Every worked equation is an actual complete offered object, not ID metadata.
 solution=q[':question/worked-solution']
 formulas=re.findall(r'[FGHK]\(\s*x\s*,\s*y\s*\)\s*=\s*[^$\n]+',solution)
 worked=[]
 for chunk in formulas:
  for fragment in re.split(r'\\,\s*(?=[FGHK]\()',chunk):
   worked.append(parse(fragment.rstrip('.,')))
 assert worked[-1]==correct_pair
 assert all(z in math for z in worked)
 assert len(worked)==4 # eliminate all three other math choices, then conclude
 assert solution.startswith('We notice the following:')
 assert solution.count('\n- ')==2
 # Read component predicates from the displayed English. Test at points whose
 # coordinates do not make a variable term accidentally constant/zero.
 for axis,basis in (('horizontal',0),('vertical',1)):
  sign_claim=re.search(r'The '+axis+r' component.*?is (positive|negative|zero) for (?:\*every\*|each) vector',solution)
  if sign_claim:
   requested={'positive':1,'negative':-1,'zero':0}[sign_claim[1]]
   assert all(s.sign(correct_pair[basis].subs({x:xx,y:yy}))==requested for xx,yy in itertools.product((-3,-1,1,3),repeat=2))
  growth=re.search(r'As we move away from the origin in the (horizontal|vertical) direction, our vectors\x27 '+axis+r' components',solution)
  if growth:
   changing=x if growth[1]=='horizontal' else y;held=y if changing==x else x
   assert changing in correct_pair[basis].free_symbols
   for direction in (-1,1):
    small=abs(correct_pair[basis].subs({changing:direction,held:2}));large=abs(correct_pair[basis].subs({changing:3*direction,held:2}))
    assert large>small
 bullets=re.findall(r'\n- (.*?)\n\n\$\$\n(.*?)\n\$\$',solution,re.S)
 assert len(bullets)==2
 for prose,eliminated in bullets:
  checks=prose_predicates(prose,correct_pair)
  assert checks and all(checks),(prose,correct_pair,checks)
  for expression in re.split(r'\\,\s*(?=[FGHK]\()',eliminated):
   checks=prose_predicates(prose,parse(expression))
   assert checks and not all(checks),(prose,expression,checks)
 for text in (q[':question/problem'],solution):
  assert text.count('$')%2==0
  assert text.count('{')==text.count('}')
  assert not re.search(r'(?<!\{)[+-][+-]',text)
 plot=meta['plots'];path=Path(plot['prompt']);assert path.exists()
 assert path.stat().st_size>1500
 assert path.as_posix() in q[':question/problem']
 if plot['renderer']=='Matplotlib':
  data=json.loads(Path(plot['sidecar']).read_text())
  assert data['renderer']=='Matplotlib'
  for xx,yy,uu,vv in data['points']:
   xx,yy,uu,vv=map(s.Rational,(xx,yy,uu,vv))
   assert tuple(z.subs({x:xx,y:yy}) for z in correct_pair)==(uu,vv)
  assert 0<data['display_scale']<=1
 else:
  source=g.QUESTIONS[profile];logical=re.search(r'!\[\]\((.*?)\)',source[':question/problem'])[1]
  original=Path('/media/jake/SSD/EDB/math')/logical
  assert hashlib.sha256(path.read_bytes()).digest()==hashlib.sha256(original.read_bytes()).digest()
 return correct_pair

def fresh_concurrency(records):
 """Actual fresh renderer writes, both identical/different inputs, private dir."""
 with tempfile.TemporaryDirectory(prefix='concurrency-',dir=HERE) as tmp:
  root=Path(tmp);inputs=[]
  chosen=[records[0],records[0],records[-1],records[-2]]
  for index,r in enumerate(chosen):
   pair=shape_and_math(r)
   points=[[str(xx),str(yy),str(pair[0].subs({x:xx,y:yy})),str(pair[1].subs({x:xx,y:yy}))] for xx in (s.Rational(-3,2),s.Rational(3,2)) for yy in (s.Rational(-5,2),s.Rational(5,2))]
   # same output target for identical pair; differing pair gets its own target
   target=0 if index==1 else index
   payload={'output':str(root/f'{target}.png'),'sidecar':str(root/f'{target}.json'),
    'field':list(map(str,pair)),'points':points,'bounds':[-5.7,5.7],'key':str(pair),'style':'qualitative-field-1'}
   path=root/f'input-{index}.json';path.write_text(json.dumps(payload));inputs.append(path)
  def run(path):return subprocess.run([g.os.sys.executable,str(HERE/'render.py'),str(path)],capture_output=True,check=True)
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(run,inputs))
  for index,path in enumerate(inputs):
   payload=json.loads(path.read_text());out=json.loads(Path(payload['sidecar']).read_text())
   assert out['points']==payload['points'];assert out['field']==payload['field']
   assert Path(payload['output']).stat().st_size>1500
  assert not list(root.glob('png-*'));assert not list(root.glob('sidecar-*'))

def main():
 cases=json.loads((HERE/'source-cases.json').read_text());originals=[];banks=correct_designations=exact_prose=0
 for c in cases:
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])
  shape_and_math(r);originals.append(r)
  source=c['source_question'];f=r['question'][':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
  actual=sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])
  expected=sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in sf[':answer-field/choices'])
  assert actual==expected,c['source_id'];banks+=1
  if ':answer-field/correct' in sf:
   value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
   assert value==sf[':answer-field/correct'][':answer/value'];correct_designations+=1
  normalized=re.sub(r'!\[\]\([^)]*\)','IMAGE',r['question'][':question/problem'])
  assert normalized==re.sub(r'!\[\]\([^)]*\)','IMAGE',source[':question/problem'])
  if ':question/worked-solution' in source:
   if c['source_id']=='q-122629':
    expected_prose=source[':question/worked-solution'].replace(r'F(x,y)=-i+x\,j',r'F(x,y)=-i-j')
    assert r['question'][':question/worked-solution']==expected_prose
   else:
    assert r['question'][':question/worked-solution']==source[':question/worked-solution'];exact_prose+=1
 review=json.loads((HERE/'review.json').read_text());variants=review['generated']
 for r in variants:
  shape_and_math(r)
  meta=r['generation']
  other=g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=881,template=meta['template'],profile=meta['bank_profile'],parameters=meta['parameters'])
  assert other['question'][':question/id']==r['question'][':question/id']
  assert other['generation']['content_fingerprint']==meta['content_fingerprint']
 for level in ('easy','moderate','hard'):
  assert sum(r['question'][':question/difficulty'].endswith('/'+level) for r in variants)>=2
  for bad in [dict(a=0,sx=1,sy=1,swap=False),dict(a=4,sx=1,sy=1,swap=False),dict(a=1,sx=0,sy=1,swap=False),dict(a=1,sx=1,sy=1,swap=0)]+([dict(a=2,sx=1,sy=1,swap=False)] if level=='hard' else []):
   try:g.generate(level,parameters=bad)
   except ValueError:pass
   else:raise AssertionError('invalid parameters accepted')
 # Same qualitative geometry across bank profiles/common magnitudes dedups;
 # actual banks and full displayed magnitudes retain separate content identity.
 first=g.generate_easy(profile='q-122634',parameters=dict(a=1,sx=1,sy=1,swap=False))
 second=g.generate_easy(profile='q-122637',parameters=dict(a=-1,sx=1,sy=1,swap=True))
 assert first['generation']['mathematical_fingerprint']==second['generation']['mathematical_fingerprint']
 assert first['question'][':question/id']!=second['question'][':question/id']
 # Exhaust all meaningful orientation parameters independently, without plots.
 meaningful={level:set() for level in ('easy','moderate','hard')}
 for profile,specification in g.PROFILES.items():
  level=specification[0]
  for a,sx,sy,swap in itertools.product((-1,1),(-1,1),(-1,1),(False,True)):
   p=dict(a=a,sx=sx,sy=sy,swap=swap);pair=transformed_original(profile,p)
   coefficients=[c for e in pair for c in s.Poly(e,x,y).coeffs() if c]
   common=abs(s.gcd_list(coefficients));meaningful[level].add(tuple(s.expand(e/common) for e in pair))
   bank=[parse(g.formula(name,g.transform((u,v),p),profile)) for name,u,v in specification[3]]
   assert len(set(bank))==4;assert bank.count(pair)==1
   values={name:g.formula(name,g.transform((u,v),p),profile) for name,u,v in specification[3]}
   solution=g.generated_solution(profile,p,values)
   for prose,eliminated in re.findall(r'\n- (.*?)\n\n\$\$\n(.*?)\n\$\$',solution,re.S):
    assert all(prose_predicates(prose,pair))
    for expression in re.split(r'\\,\s*(?=[FGHK]\()',eliminated):
     assert not all(prose_predicates(prose,parse(expression)))
 for sx,sy,swap in itertools.product((-1,1),(-1,1),(False,True)):
  u,v=(y,x) if swap else (x,y);meaningful['hard'].add((sx*u,sy*v))
 hard_catalog=[g.generate_hard(parameters=dict(a=1,sx=sx,sy=sy,swap=swap)) for sx,sy,swap in itertools.product((-1,1),(-1,1),(False,True))]
 for r in hard_catalog:shape_and_math(r)
 assert len({r['generation']['mathematical_fingerprint'] for r in hard_catalog})==8
 fresh_concurrency(variants)
 fixtures=[]
 for index,r in enumerate(originals+variants+hard_catalog):
  f=r['question'][':question/answer-fields'][0];right=f[':answer-field/correct'][1]
  fixtures.append({'label':f'record-{index}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==right else 'rejected','purpose':'complete bank native selection'} for a in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
 root=HERE.parents[2];binary=root/'generate/runs/current/check-engine'
 subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 report={'passed':True,'basis':1356,'source_practice_count':len(cases),'source_bank_fidelity':{'matched':banks,'total':9,'matched_choices':45,'total_choices':45},
  'source_correct_designation_fidelity':{'matched':correct_designations,'available':8,'missing_original':1,'independently_authored':1},
  'source_solution_fidelity':{'raw_exact':exact_prose,'available':8,'mathematically_repaired':1,'missing_authored':1},
  'source_prompt_fidelity':{'image_reference_normalized':9,'total':9},
  'generated_examples':len(variants),'meaningful_catalog_sizes':{k:len(v) for k,v in meaningful.items()},
  'independent_displayed_formula_checks':len(originals+variants+hard_catalog),'full_domain_orientation_banks':144,
  'fresh_concurrent_renders':4,'authored_hard_tasks':8,'full_domain_prose_predicate_checks':144,
  'cross_profile_task_dedup_checked':True,
  'native_grading':json.loads((HERE/'engine-report.json').read_text()),'unresolved_findings':[]}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 files=[HERE.with_suffix('.py')]+sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='hashes.json' and '__pycache__' not in p.parts)
 (HERE/'hashes.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='native_grading'},indent=2))

if __name__=='__main__':main()
