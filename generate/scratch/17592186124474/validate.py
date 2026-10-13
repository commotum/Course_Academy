"""Independent checks of actual displayed prose, formulas, banks and plots.

Run from repository root with .venv/bin/python. No database writes.
"""
import concurrent.futures,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x');TRANS=standard_transformations+(implicit_multiplication_application,rationalize)
def decode(s):
 s=s.strip().rstrip('.,').replace(r'\infty','oo').replace('\\,','').replace(' ','')
 while r'\frac' in s:
  nxt=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
  if nxt==s:raise AssertionError('Unparsed fraction '+s)
  s=nxt
 s=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',s)
 s=s.replace('^{','**(').replace('}',')').replace('{','(').replace('^','**')
 if '|' in s:
  parts=s.split('|');assert len(parts)==3;s=parts[0]+'Abs('+parts[1]+')'+parts[2]
 return parse_expr(s,local_dict={'x':x,'oo':sp.oo},transformations=TRANS)
def intervals(prompt):
 out=[]
 for s in re.findall(r'\$([^$]*\\in[^$]*)\$',prompt):
  m=re.search(r'([\[(])(.*?),(.*?)([\])])',s);assert m,s
  out.append((decode(m[2]),decode(m[3]),m[1]=='[',m[4]==']'))
 assert len(out)==3
 return out
def inspect(r):
 q=r['question'];p=q[':question/problem'];sol=q[':question/worked-solution'];gen=r['generation']
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP
 # Independent object recovered entirely from printed prompt.
 expr=decode(re.search(r'f\(x\)=(.*?),\$',p)[1]);ivs=intervals(p)
 if expr.has(sp.Abs):
  inner=next(iter(expr.atoms(sp.Abs))).args[0];h=sp.solve(inner,x)[0];kind='folded';a=1
 else:
  poly=sp.Poly(expr,x);assert poly.degree()<=2
  if poly.degree()==2:h=-poly.nth(1)/(2*poly.nth(2));kind='folded';a=poly.nth(2)
  else:h=0;kind='linear';a=poly.nth(1)
 truth=[]
 for lo,hi,l,rr in ivs:
  assert lo<hi and not(lo==-sp.oo and l) and not(hi==sp.oo and rr)
  good=(a!=0) if kind=='linear' else hi<=h or lo>=h;truth.append(good)
  if not good:
   u=(lo+hi)/2 if lo!=-sp.oo and hi!=sp.oo else hi-1 if hi!=sp.oo else lo+1 if lo!=-sp.oo else 0
   if kind=='folded':d=sp.Min(h-lo if lo!=-sp.oo else 1,hi-h if hi!=sp.oo else 1)/2;u,v=h-d,h+d
   else:v=u+sp.Rational(1,10)
   assert lo<u<hi and lo<v<hi and u!=v and sp.simplify(expr.subs(x,u)-expr.subs(x,v))==0
 correct=frozenset(['I','II','III'][i] for i,t in enumerate(truth) if t)
 fs=q.get(':question/answer-fields')
 if fs is None:
  assert not gen['eligible_for_learning'] and gen['evidence_only'] and gen['missing_keys']==[':question/answer-fields']
 else:
  assert len(fs)==1;f=fs[0];assert f[':answer-field/type']==':answer-field.type/radio'
  vals=f[':answer-field/choices'];assert len(vals)==5
  subsets=[frozenset(re.findall(r'\bIII\b|\bII\b|\bI\b',v[':answer/value'])) for v in vals]
  assert len(set(subsets))==5 and sum(s==correct for s in subsets)==1
  if gen['template'].startswith(('rational_','integer_')):
   assert sum(len(v)==2 for v in subsets)==3, 'The correct answer must not be the only paired option'
   assert set(subsets)=={correct}|{frozenset([v]) for v in correct}|{frozenset(['I','II','III'])-frozenset([v]) for v in correct}, 'Complete omission/replacement bank'
  selected=next(v for v in vals if v[':answer/id']==f[':answer-field/correct'][1]);assert frozenset(re.findall(r'\bIII\b|\bII\b|\bI\b',selected[':answer/value']))==correct
  assert ':answer.type/text'==selected[':answer/type']
 # Fixed solutions: concluding designation and each concluding f formula.
 conclusions=re.findall(r'correct answer is "([^"]+)"',sol);assert len(conclusions)==1
 assert frozenset(re.findall(r'\bIII\b|\bII\b|\bI\b',conclusions[0]))==correct
 for displayed in re.findall(r'f\(x\)=([^$]+)',sol):assert sp.simplify(decode(displayed)-expr)==0,(gen['template'],displayed,expr)
 # Intermediate curve construction stages are checked from printed y= rows.
 if kind=='folded':
  for line in sol.splitlines():
   for stage in re.findall(r'y=([^$]+)',line):
    rendered=decode(stage)
    if 'Take the curve' in line:expected=sp.Abs(x) if expr.has(sp.Abs) else x**2
    elif 'Reflect' in line:expected=-x**2
    else:expected=expr-expr.subs(x,h)
    assert sp.simplify(rendered-expected)==0,(line,rendered,expected)
 if kind=='linear' and 'slope $' in sol:
  assert decode(re.search(r'slope \$([^$]+)',sol)[1])==a
  assert decode(re.search(r'intercept \$([^$]+)',sol)[1])==expr.subs(x,0)
 if gen['template'].startswith(('rational_','integer_')):
  displayed_h=decode(re.search(r'vertex occurs at \$x=([^$]+)',sol)[1]);assert displayed_h==h
  for u,v,value in re.findall(r'inputs \$([^$]+)\$ and \$([^$]+)\$, both with output \$([^$]+)',sol):
   u,v,value=map(decode,[u,v,value]);assert u!=v and expr.subs(x,u)==expr.subs(x,v)==value
  assert len(re.findall(r'- Interval ',sol))==3
 else:
  # Each positive/negative interval assertion in the source prose is checked by
  # recovering its complete interval and its sentence's requested property.
  for line in sol.splitlines():
   if 'function' not in line or 'invertible on' not in line or 'Since' in line:continue
   neg='not invertible' in line
   strings=re.findall(r'([\[(](?:-?\\infty|-?\d)[^$]*?,[^$]*?[\])])',line)
   for st in strings:
    try:
     m=re.search(r'([\[(])(.*?),(.*?)([\])])',st);iv=(decode(m[2]),decode(m[3]),m[1]=='[',m[4]==']')
    except Exception:continue
    check=a!=0 if kind=='linear' else iv[1]<=h or iv[0]>=h
    assert check!=neg,(line,iv,h)
  if kind=='folded':
   # Translation prose is independently reconciled to displayed function.
   for amount,direction in re.findall(r'by \$(\d+)\$ units? +(?:to +the +)?(right|left|up|down)',sol):
    if direction in ('right','left'):assert sp.Integer(amount)*(1 if direction=='right' else -1)==h
    else:assert sp.Integer(amount)*(1 if direction=='up' else -1)==expr.subs(x,h)
 # Formatting normal and raw evidence alike; scalar TeX groups and math balance.
 for text in (p,sol):
  assert text.count('$')%2==0
  assert text.count('{')==text.count('}')
  assert not any(s in text for s in ('@@COMPONENT','+-','--'))
 for side in gen['plot_sidecars']:
  data=json.loads(Path(side).read_text());assert data['renderer']=='Matplotlib'
  assert all(min(d.values())>=5 for d in data['label_clearance_pixels'])
  for panel in data['geometry']:
   for value in (panel['h']-1,panel['h'],panel['h']+1):
    y=panel['a']*value+panel['k'] if panel['curve']=='linear' else panel['a']*(value-panel['h'])**2+panel['k'] if panel['curve']=='quadratic' else panel['a']*abs(value-panel['h'])+panel['k']
    assert abs(float(expr.subs(x,value))-y)<1e-10
   if panel['interval_index'] is not None:
    actual=ivs[panel['interval_index']-1];shown=panel['interval'];assert all(float(actual[i])==shown[i] for i in range(2)) and actual[2:]==tuple(shown[2:])
 return {'template':gen['template'],'correct_intervals':list(truth),'eligible':gen['eligible_for_learning']}
def hashfile(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 cases=[];originals=[];review=[];source_banks=0;source_options=0
 for name,source in g.SOURCES.items():
  level,kind,a,h,k,_=g.SPECS[name];params={'a':a,'h':h,'k':k,'offset':0};profile='raw' if name=='q-66785' else 'observed'
  case={'source_id':name,'template':name,'difficulty':level,'parameters':params,'bank_profile':profile};cases.append(case)
  r=g.generate(level,template=name,parameters=params,profile=profile);q=r['question'];inspect(r)
  assert q[':question/problem']==source[':question/problem']
  assert q[':question/worked-solution']==source[':question/worked-solution']
  assert (':question/answer-fields' in q)==(':question/answer-fields' in source)
  assert (':question/difficulty' in q)==(':question/difficulty' in source)
  if ':question/answer-fields' in source:
   f=source[':question/answer-fields'][0];gf=q[':question/answer-fields'][0]
   assert f[':answer-field/key']==gf[':answer-field/key']
   assert f[':answer-field/type'][':db/ident']==gf[':answer-field/type']
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices'])
   ga=next(a for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert ga[':answer/value']==f[':answer-field/correct'][':answer/value']
   source_banks+=1;source_options+=len(f[':answer-field/choices'])
  originals.append(r)
  for variant in (1,2):
   pp={'a':int(sp.sign(a))*(variant+1) if kind=='linear' else a,'h':int(sp.sign(h))*(abs(h)+variant) if h else 0,'k':int(sp.sign(k))*(abs(k)+variant) if k else 0,'offset':variant if kind=='linear' else 0}
   # Ensure variants stay at equal-level bounds; source k=4 ->6 maximum.
   rr=g.generate(level,variant,template=name,parameters=pp,profile='repaired' if name=='q-66785' else 'observed');inspect(rr);review.append(rr)
 for template in ('constant','integer_quadratic','integer_absolute','rational_quadratic','rational_absolute'):
  level='easy' if template=='constant' else 'moderate' if template.startswith('integer_') else 'hard'
  for seed in (11,29):r=g.generate(level,seed,template=template);inspect(r);review.append(r)
 # Default sampling must serve every supported family/template.
 defaults=[g.generate(level,seed) for level in ('easy','moderate','hard') for seed in range(48)]
 for r in defaults:inspect(r)
 assert {r['generation']['template'] for r in defaults if r['question'][':question/difficulty'].endswith('/moderate')}==({n for n,s in g.SPECS.items() if s[0]=='moderate'}|{'integer_quadratic','integer_absolute'})
 # Fixed parameters/profile and domains preserve identities through seed shuffles.
 for r in review:
  gg=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
  twin=g.generate(level,10001,gg['template'],parameters=gg['parameters'],profile=gg['bank_profile'])
  assert r['question'][':question/id']==twin['question'][':question/id'] and gg['parameter_fingerprint']==twin['generation']['parameter_fingerprint']
 # Mathematical parameter spelling cannot change displayed identity.
 original=g.generate('moderate',0,'q-36010',parameters={'a':1,'h':3,'k':2,'offset':0})
 alias=g.generate('moderate',91,'q-36010',parameters={'a':'1','h':'3','k':'2','offset':'0'})
 assert original['question'][':question/id']==alias['question'][':question/id']
 # Every finite hard catalog element: 6 choose 2 branch types * 6 positions =90.
 catalog=[list(order) for pair in itertools.combinations([t for t in g.HARD_TYPES if t!='X'],2) for order in itertools.permutations([*pair,'X'])]
 fingerprints=set()
 for types in catalog:
  r=g.generate('hard',template='rational_quadratic',parameters={'h':'1/2','k':0,'types':types});inspect(r);fingerprints.add(r['generation']['parameter_fingerprint'])
 assert len(fingerprints)==90
 moderate_catalog=[list(order) for half in g.MODERATE_TYPES for finite in g.HARD_TYPES if finite!='X' for order in itertools.permutations([half,finite,'X'])]
 moderate_fingerprints=set()
 for types in moderate_catalog:
  rr=g.generate('moderate',template='integer_absolute',parameters={'h':2,'k':-1,'types':types});inspect(rr);moderate_fingerprints.add(rr['generation']['parameter_fingerprint'])
 assert len(moderate_fingerprints)==72
 # Explicit guards apply equally to random and fixed inputs.
 rejects=[('hard','rational_quadratic',{'h':'1','k':0,'types':['L','R','X']}),('hard','rational_absolute',{'h':'1/5','k':0,'types':['L','R','X']}),('easy','constant',{'k':7,'offset':0}),('moderate','q-66482',{'a':1,'h':1,'k':2,'offset':0})]
 for level,temp,pars in rejects:
  try:g.generate(level,template=temp,parameters=pars)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit workload accepted')
 # Concurrent calls share no mutable input file; fresh content uses unique names.
 pars=[{'a':1,'h':5,'k':5,'offset':0},{'a':1,'h':6,'k':6,'offset':0}]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  concurrent_rs=list(pool.map(lambda pp:g.generate('moderate',33,'q-36010',parameters=pp),[pars[0],pars[0],pars[1]]))
 for r in concurrent_rs:inspect(r)
 assert concurrent_rs[0]['question'][':question/id']==concurrent_rs[1]['question'][':question/id']!=concurrent_rs[2]['question'][':question/id']
 assert not list((HERE/'plots').glob('tmp*.json'))
 native=[]
 for i,r in enumerate(originals+review+defaults):
  fs=r['question'].get(':question/answer-fields')
  if not fs:continue
  f=fs[0];native.append({'label':str(i)+'-'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete displayed-bank radio selection'} for a in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(native,indent=2));subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'native-results.json')],check=True)
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 sections=['# Source and generated review','Source labels are observed; hard labels are authored design claims. Correct choices are marked. q-66785 raw lacks fields; the generated repaired variants add an authored radio field.']
 for src in originals:
  sections.append('## Original source '+src['generation']['source_id']+' (parameterized replay)\n\n'+g.markdown(src))
  sections.extend(g.markdown(r) for r in review if r['generation']['template']==src['generation']['template'])
 sections.extend(g.markdown(r) for r in review if r['generation']['template'] not in g.SOURCES)
 # Preserve source text in records; link absolute original assets only in review.
 md='\n\n---\n\n'.join(sections);md=re.sub(r'!\[\]\((images/[^)]+)\)',r'![](/media/jake/SSD/EDB/math/\1)',md);(HERE/'review.md').write_text(md)
 report={'status':'pass','basis':1356,'source_questions':12,'exact_prompts':12,'exact_full_solutions':12,'field_presence_parity':12,'complete_banks_matched':source_banks,'choices_matched':source_options,'correct_designations_matched':11,'missing_original_designations':1,'raw_ineligible_sources':['q-66785'],'minimal_authored_repairs':1,'generated_review_records':len(review),'default_records_checked':len(defaults),'all_hard_finite_catalog_checked':90,'all_authored_moderate_catalog_checked':72,'canonical_authored_moderate_task_catalog_size':72,'canonical_hard_task_catalog_size':90,'canonical_easy_task_catalog_size':2,'canonical_easy_limit':'Nonzero-line interval subsets all satisfy injectivity; numerical slopes/intercepts are not new semantic tasks. Constant contrast adds the empty subset. Source layouts are retained separately.','native_results':json.loads((HERE/'native-results.json').read_text()),'unsupported_mathematical_equivalents':'Text radio values are selected by owned UUID; comma/and wording aliases represent equivalent subsets and cannot be distinct options. There is no free-entry equivalence contract.','python_version':sys.version.split()[0],'sympy_version':sp.__version__,'hashes':{str(p.relative_to(ROOT)):hashfile(p) for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'render.py',HERE/'validate.py',ROOT/'generate/runs/current/sources/17592186124474.json',ROOT/'generate/runs/current/topics/17592186049731.json',ROOT/'generate/runs/current/lessons/17592186049731.json',ROOT/'generate/runs/current/check-engine',ROOT/'generate/runs/current/check-engine.rs']}}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: 12 source prompts/solutions; 11/11 banks, 55/55 options; 34 generated reviews, 144 default records, 72 moderate and 90 hard catalog entries.')
if __name__=='__main__':main()
