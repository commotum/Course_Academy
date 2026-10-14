#!/usr/bin/env python3
"""Read actual displayed math independently; no EDB operations or baseline imports."""
import copy,hashlib,importlib.util,json,random,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode = True
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;R=D.parents[2]
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
G=module('draft',D.with_suffix('.py'))
F=module('sourcefidelity',R/'generate/runs/current/root-source-fidelity.py')
x,y=sp.symbols('x y',real=True)

def parse(t):
 """Independent restricted TeX parser for this displayed vocabulary."""
 t=t.strip().rstrip('.').replace(r'\dfrac',r'\frac').replace(r'\pm','')
 while r'\sqrt{' in t or r'\frac{' in t:
  old=t
  t=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',t)
  t=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',t)
  if old==t:raise AssertionError('Unparsed TeX '+t)
 t=t.replace('^','**').replace('{','(').replace('}',')')
 if '\\' in t:raise AssertionError('Unrecognized command '+t)
 return parse_expr(t,local_dict={'x':x,'y':y,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))

def fields(q):return q[':question/answer-fields']
def same(a,b):
 # Independent exact real-radical test: sign is necessary, then square.
 if a==b:return True
 if a.is_negative is not None and b.is_negative is not None and a.is_negative!=b.is_negative:return False
 z=sp.expand(a**2-b**2)
 return bool(z.is_zero) if z.is_zero is not None else sp.simplify(a-b)==0
def given_from_prompt(q):
 p=q[':question/problem'];assert 'first quadrant' in p and 'unit circle' in p
 m=re.search(r'The \$(x|y)\$-coordinate of \$A\$ is \$(.*?)\$',p)
 assert m,p
 k=m[1];t='y' if k=='x' else 'x';given=parse(m[2])
 assert f'What is the ${t}' in p
 assert 0<given<1
 return k,t,given,sp.sqrt(1-given**2)

def audit(r,completed=True):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];k,t,g,a=given_from_prompt(q)
 if completed:
  displayed=re.search(r'The \$(?:x|y)\$-coordinate of \$A\$ is \$(.*?)\$',q[':question/problem'])[1]
  denominator=int(re.search(r'\{(\d+)\}\.?(?:\s*)$',displayed)[1])
  assert sp.simplify(g*g).q==denominator**2,'Evaluated square lost source perfect-square denominator'
 f=fields(q)[0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 assert len(f[':answer-field/choices'])==5
 printed=[]
 for c in f[':answer-field/choices']:
  value=c[':answer/value']
  if '=' in value:
   left,value=value.split('=');assert parse(left)=={'x':x,'y':y}[t]
  printed.append(parse(value))
 assert all(v.is_real is True and v.is_finite is True for v in printed)
 assert all(not same(v,w) for i,v in enumerate(printed) for w in printed[i+1:])
 mathematical=[same(v,a) for v in printed]
 assert sum(mathematical)==1
 if completed:
  expected=[a,-a,1-g**2,sp.sqrt(1-g),sp.sqrt(1+g**2)]
  assert all(sum(same(v,e) for v in printed)==1 for e in expected),'Displayed method-bank recipe mismatch'
 if ':answer-field/correct' in f:
  correct=f[':answer-field/correct'][1]
  assert mathematical[next(i for i,c in enumerate(f[':answer-field/choices']) if c[':answer/id']==correct)]
 elif completed:raise AssertionError('Missing correct reference')
 if ':question/worked-solution' in q:
  s=q[':question/worked-solution']
  assert f'Substituting ${k}=' in s and f'solving for ${t}$' in s and f'${t}$ must be positive' in s
  intro=re.search(r'Substituting \$(x|y)=(.*?)\$',s);assert intro[1]==k and sp.simplify(parse(intro[2])-g)==0
  conclusion=re.search(r'Therefore, our final answer is \$(x|y)=(.*?)\$',s)
  assert conclusion[1]==t and sp.simplify(parse(conclusion[2])-a)==0
  body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S)[1]
  rows=body.split(r' \\ ');assert len(rows)==7
  assert rows[0]==r'{x}^{2}+{y}^{2} & =1'
  # Structure is independently read: substituted coordinate square, evaluated
  # square, subtraction, reduced rational square, root, signed simplified root.
  sub=re.search(r'\{\((.*?)\)\}\^\{2\}',rows[1]);assert sub and sp.simplify(parse(sub[1])-g)==0
  assert rows[2].count('^{2}')==1 and '1-' not in rows[2]
  assert rows[3].startswith('{'+t+'}^{2} & =1-')
  assert rows[4].startswith('{'+t+'}^{2} & =') and '1-' not in rows[4]
  assert rows[5].startswith(t+' & ='+r'\sqrt{')
  assert rows[6].startswith(t+' & ='+r'\pm ')
  assignment={x:g if k=='x' else a,y:g if k=='y' else a}
  for row in rows:
   left,right=row.split('& =');assert sp.simplify(parse(left).subs(assignment)-parse(right).subs(assignment))==0,row
 elif completed:raise AssertionError('Missing solution')
 for s in [q[':question/problem'],q.get(':question/worked-solution','')]+[c[':answer/value'] for c in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t' for c in s),'Control character'
  assert '\\'+'sin' not in s and '\\'+'cos' not in s and '\\'+'theta' not in s
 if completed:G.MF.validate_generated_record(copy.deepcopy(r))
 identity=G.digest([G.VERSION,q[':question/problem'],q.get(':question/worked-solution'),q.get(':question/difficulty'),
    r['generation']['template'],sorted(c[':answer/value'] for c in f[':answer-field/choices']),':answer-field/correct' in f])
 assert r['generation']['content_identity']==identity
 assert q[':question/id']==str(uuid.uuid5(uuid.UUID(G.KP_UUID),identity))
 assert f[':answer-field/id']==str(uuid.uuid5(uuid.UUID(q[':question/id']),'selection'))
 assert all(c[':answer/id']==str(uuid.uuid5(uuid.UUID(f[':answer-field/id']),c[':answer/value'])) for c in f[':answer-field/choices'])
 return k,t,str(sp.simplify(g*g))

def must_fail(fn):
 try:fn()
 except (ValueError,AssertionError):return
 raise AssertionError('Mutation/domain guard was not rejected')

def run():
 frozen=json.load(open(D/'baseline-hashes.json'))
 paths=[R/'generate/scratch/17592186110754.py']+[p for p in (R/'generate/scratch/17592186110754').rglob('*') if p.is_file()]
 assert set(map(lambda p:str(p.relative_to(R)),paths))==set(frozen)
 assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in frozen.items())
 base=R/'generate/scratch/17592186110754'
 directory_paths=[str(p.relative_to(R)) for p in sorted([base]+[x for x in base.rglob('*') if x.is_dir()])]
 assert directory_paths==json.load(open(D/'baseline-inventory.json'))['directory_pathset']
 originals,counts=F.check(G,G.KP_ID,D)
 raw=[G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']) for c in json.load(open(D/'source-cases.json'))]
 for r in raw:audit(r,False)
 # Every historical pattern must work at changed mathematical parameters
 # through the PUBLIC API; a literal anchor replay cannot pass this check.
 changed=[]
 for profile in G.RAW_PROFILES:
  for d in range(3,16):
   found=False
   for n in range(1,d*d):
    p=dict(n=n,d=d,known='x' if G.SOURCE_PARAMETERS[profile[4:]]['known']=='y' else 'y')
    if p==G.SOURCE_PARAMETERS[profile[4:]]:continue
    try:r=G.generate('easy',profile=profile,parameters=p);audit(r,False)
    except (ValueError,AssertionError):continue
    changed.append(r);found=True;break
   if found:break
  assert found,profile
 records=[];capacity={};slots={};profile_coverage={}
 for level in ('easy','moderate','hard'):
  params=G.pool(level);tasks=set();selected=[]
  for i,p in enumerate(params):
   r=G.generate(level,parameters=p,profile=G.METHOD_PROFILES[i%2]);audit(r)
   tasks.add(r['generation']['mathematical_fingerprint'])
   if i<20 or i>=len(params)-4:selected.append(r)
  capacity[level]={'parameter_records':len(params),'semantic_tasks_excluding_target_aliases':len(tasks),
                  'coordinate_swap_collapsed_capacity':len({tuple(sorted((str(sp.Rational(p['n'],p['d']**2)),str(1-sp.Rational(p['n'],p['d']**2))))) for p in params})}
  slots[level]=sorted({p['known'] for p in params})
  defaults=[G.generate(level,seed=i) for i in range(50)]
  profile_coverage[level]=sorted({r['generation']['profile'] for r in defaults})
  assert profile_coverage[level]==sorted(G.METHOD_PROFILES)
  assert {r['generation']['parameters']['known'] for r in defaults}=={'x','y'}
  records.extend(selected)
 # Stable content and owned answer identity under seed/ordering changes.
 for r in records+raw+changed:
  m=r['generation'];alt=G.generate(m.get('authored_level') or 'easy',seed=717,template=m['template'],profile=m['profile'],parameters=m['parameters'])
  assert alt['question'][':question/id']==r['question'][':question/id']
  assert sorted(a[':answer/id'] for a in fields(alt['question'])[0][':answer-field/choices'])==sorted(a[':answer/id'] for a in fields(r['question'])[0][':answer-field/choices'])
  assert alt['generation']['content_identity']==m['content_identity']
 for level in ('easy','moderate','hard'):
  p=G.pool(level)[0]
  a=G.generate(level,parameters=p,profile='method-value');b=G.generate(level,parameters=p,profile='method-equation')
  assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
  assert a['question'][':question/id']!=b['question'][':question/id']
 # Actual grade is an identity component, yet domains themselves are disjoint.
 domains={l:{(p['n'],p['d'],p['known']) for p in G.pool(l)} for l in ('easy','moderate','hard')}
 assert not domains['easy']&domains['moderate'] and not domains['easy']&domains['hard'] and not domains['moderate']&domains['hard']
 for l in domains:
  for p in (dict(n=0,d=5,known='x'),dict(n=25,d=5,known='x'),dict(n=4,d=16,known='x'),dict(n=4,d=5,known='z')):
   must_fail(lambda:G.generate(l,parameters=p))
  wronglevel=next(q for other in domains if other!=l for q in G.pool(other))
  must_fail(lambda:G.generate(l,parameters=wronglevel))
 assert subprocess.run([sys.executable,str(D.with_suffix('.py')),'--count','0'],capture_output=True).returncode!=0
 must_fail(lambda:G.generate('easy',profile='unknown'))
 must_fail(lambda:G.generate('easy',field_type='blank'))
 must_fail(lambda:G.generate('hard',parameters=dict(n=12,d=9,known='x')))
 mutations=[]
 r=records[0]
 for name,mutate in [
  ('conclusion',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('Therefore, our final answer is','Therefore, our final answer is $x=99$.'))),
  ('subtraction',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace(' & =1-', ' & =1+'))),
  ('control',lambda q:q.__setitem__(':question/problem',q[':question/problem']+'\x0c')),
  ('removed squared coordinate stage',lambda q:q.__setitem__(':question/worked-solution',re.sub(r'\{\((.*?)\)\}\^\{2\}',r'(\1)',q[':question/worked-solution']))),
  ('stale target',lambda q:q.__setitem__(':question/problem',q[':question/problem'].replace('What is the $y','What is the $x'))),
  ('wrong displayed choice',lambda q:q[':question/answer-fields'][0][':answer-field/choices'][0].__setitem__(':answer/value','99'))]:
  bad=copy.deepcopy(r);mutate(bad['question']);must_fail(lambda:audit(bad));mutations.append(name)
 # Use actual native engine for every displayed choice of normal examples,
 # rated raw sources and inferred completed versions of two unrated originals.
 fixtures=[]
 tested=records+[r for r in raw if ':question/difficulty' in r['question']]
 tested += [G.generate('easy',parameters=G.SOURCE_PARAMETERS[k],profile='method-equation') for k in G.UNRATED]
 for i,r in enumerate(tested):
  f=fields(r['question'])[0];key=f[':answer-field/correct'][1]
  checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==key else 'rejected','purpose':'Grade displayed owned radio choice after independent exact math check'} for c in f[':answer-field/choices']]
  fixtures.append({'label':str(i),'record':r,'checks':checks})
 json.dump(fixtures,open(D/'native-input.json','w'),indent=2)
 completed=subprocess.run([str(R/'generate/runs/current/check-engine'),str(D/'native-input.json'),str(D/'native-grading.json')],capture_output=True,text=True)
 assert completed.returncode==0,completed.stderr
 print(completed.stdout.strip())
 native=json.load(open(D/'native-grading.json'))
 report={'status':'pass','source_fidelity':counts,'source_bank_values':35,'source_inferred_missing_keys':2,
  'source_raw_profiles_evidence_only':7,'historical_changed_parameter_profiles':len(changed),'independent_inventory_count':0,
  'normal_exhaustive_records':sum(len(G.pool(l)) for l in domains),'capacity':capacity,'known_slot_coverage':slots,
  'default_profile_coverage':profile_coverage,'mutation_regressions_rejected':mutations,
  'native':{k:v for k,v in native.items() if k!='records'},
  'baseline_byte_identical':True,'baseline_pathset_identical':True,
  'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},
  'native_engine_sha256':hashlib.sha256((R/'generate/runs/current/check-engine').read_bytes()).hexdigest(),
  'limits':['Missing Moderate/Hard are authored workload calibration, not observed MA grades.',
   'Seven opaque source profiles remain evidence-only; two omit original grade/key/solution and cannot directly grade.',
   'No equivalence entry test is applicable to the observed radio response format.']}
 json.dump(report,open(D/'validation.json','w'),indent=2)
 # Originals plus one changed instance per historical profile, and two normal
 # examples per level, covering x/y and scalar/equation response shapes.
 reviews=[]
 for r in raw:reviews.append({'role':'raw original evidence','record':r})
 for r in changed:reviews.append({'role':'changed historical expression pattern; evidence only','record':r})
 for level in domains:
  p0=dict(next(p for p in G.pool(level) if p['known']=='x'))
  p1=dict(next(p for p in reversed(G.pool(level)) if p['known']=='y'))
  for j,p in enumerate((p0,p1)):reviews.append({'role':'authored '+level+' method-bank variant','record':G.generate(level,profile=G.METHOD_PROFILES[j],parameters=p)})
 json.dump(reviews,open(D/'review.json','w'),indent=2)
 (D/'review.md').write_text('# Unit-circle coordinate draft review\n\n'+ '\n\n---\n\n'.join('## '+z['role']+' — '+z['record']['generation']['profile']+'\n\n'+G.markdown(z['record']) for z in reviews))
 print(json.dumps(report,indent=2))

if __name__=='__main__':run()
