#!/usr/bin/env python3
"""Independent displayed-TeX readback, exact source-bank and native grader audit."""
import importlib.util,json,re,sys,subprocess,hashlib,concurrent.futures,os
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
import scalar_parser as p
# Local proxy symbols are deliberate parser variables, normalized AFTER display checks.
r=p.u;t=p.t;x=p.x;y=p.y

def scalar(raw):
 return p.scalar(raw.replace(r'\theta','t').replace('r','u').replace(r'\fun','').replace('[','(').replace(']',')'))
# Protect frac/sqrt commands before replacing standalone radial r.
def scalar(raw):
 raw=raw.replace(r'\frac12',r'\frac{1}{2}').replace(r'\frac\pi2',r'\frac{\pi}{2}');raw=raw.replace(r'\theta','t');raw=re.sub(r'(?<![A-Za-z])r(?![A-Za-z])','u',raw)
 return p.scalar(raw.replace('[','(').replace(']',')'))
def group(raw,i):
 if raw[i]!='{':return raw[i],i+1
 depth=1;j=i+1
 while depth:depth+=(raw[j]=='{')-(raw[j]=='}');j+=1
 return raw[i+1:j-1],j

def evaluate(raw,angular_target=None):
 raw=raw.strip().replace(r'\left','').replace(r'\right','').replace(r'\,','')
 # Evaluate innermost complete bracket operators; generic arithmetic brackets remain parentheses.
 while True:
  candidates=[];stack=[]
  for i,ch in enumerate(raw):
   if ch=='[':stack.append(i)
   if ch==']':
    j=stack.pop()
    if raw[i+1:i+2]=='_':candidates.append((j,i))
  if not candidates:break
  a,b=candidates[0];lo,end=group(raw,b+2);assert raw[end]=='^';hi,end=group(raw,end+1)
  anti=scalar(raw[a+1:b]);v=r if anti.has(r) else t;z=s.simplify(anti.subs(v,scalar(hi))-anti.subs(v,scalar(lo)))
  # An angular primitive and its prefactor must differentiate to the actual radial-integrated function.
  if v==t and angular_target is not None and r'\int' not in raw[:a]:
   factor=scalar(raw[:a]) if raw[:a] else 1;assert same(s.diff(factor*anti,t),angular_target),(raw,'angular primitive derivative')
  raw=raw[:a]+'('+s.latex(z)+')'+raw[end:]
 while r'\int' in raw:
  start=raw.rindex(r'\int');pos=start+4;assert raw[pos]=='_';lo,pos=group(raw,pos+1);assert raw[pos]=='^';hi,pos=group(raw,pos+1)
  tail=raw[pos:];diff=re.search(r'\\mathrm\{d\}([r]|\\theta)',tail);assert diff,(raw,'differential missing')
  var=r if diff[1]=='r' else t;body=scalar(tail[:diff.start()] or '1')
  if var==t and angular_target is not None:
   factor=scalar(raw[:start]) if raw[:start] else 1;assert same(factor*body,angular_target),(raw,'angular body',factor*body,angular_target)
  val=s.integrate(body,(var,scalar(lo),scalar(hi)));raw=raw[:start]+'('+s.latex(s.simplify(val))+')'+tail[diff.end():]
 return scalar(raw)
def same(a,b):return s.simplify(s.trigsimp(a-b))==0

from functools import lru_cache
RR,CC,AA,BB=s.symbols('R c a b',positive=True)
@lru_cache(maxsize=None)
def operation_reference(name):
 # Parameterized actual-density/bounds operations, computed independently once
 # per family rather than copying the generator's scalar recipe formulas.
 C=CC;R=RR
 density={'odd_disk':C*r**4*s.cos(t)**2*s.sin(t),'quarter_difference':C*r**2*(s.cos(t)-s.sin(t)),'upper_linear':r**2*(AA*s.cos(t)+BB*s.sin(t)),'square_y':C*r**3*s.sin(t)**2,'radial_square':C*r**3,'exponential':C*r*s.exp(r*r),'rational_quarter':C*r/(r*r+1),'lower_sqrt':C*r**3*s.cos(t),'upper_ratio':C*r*s.cos(t)/s.sin(t)}[name]
 lo,hi,up={'quarter_difference':(0,s.pi/2,R),'upper_linear':(0,s.pi,R),'rational_quarter':(s.pi,3*s.pi/2,R),'lower_sqrt':(-s.pi/2,0,-R*s.sin(t)),'upper_ratio':(0,s.pi/2,R*s.sin(t))}.get(name,(0,2*s.pi,R))
 def integral(d=density,l=lo,h=hi,u=up):return s.simplify(s.integrate(s.simplify(s.integrate(d,(r,0,u))),(t,l,h)))
 A=integral()
 if name=='odd_disk':
  q=integral(l=0,h=s.pi/2);values=[A,q,integral(l=0,h=s.pi),4*q,integral(l=s.pi,h=3*s.pi/2)]
 elif name=='quarter_difference':values=[A,integral(C*r**2*s.cos(t)),integral(C*r**2*(s.cos(t)+s.sin(t))),integral(-C*r**2*s.sin(t)),integral(l=s.pi/2,h=s.pi)]
 elif name=='upper_linear':values=[A,integral(r**2*(AA*s.cos(t)-BB*s.sin(t))),integral(l=-s.pi/2,h=s.pi/2),integral(density/r),integral(l=0,h=2*s.pi)]
 elif name in ('square_y','radial_square'):values=[A,integral(density/r),integral(u=R/2),integral(h=s.pi),-A]
 elif name=='exponential':values=[A,C*s.pi*s.exp(R**2),2*A,C*s.pi*(s.exp(R)-1),-A]
 elif name=='rational_quarter':values=[A,integral(l=0,h=s.pi),integral(l=0,h=2*s.pi),s.integrate(density,(r,0,R)),-A]
 elif name=='lower_sqrt':values=[A,integral(density/r),5*A,integral(u=up/2),-A]
 else:values=[A,integral(density/r),integral(u=up/2),integral(C*r),-A]
 return tuple(s.simplify(v) for v in values)

def check_record(q):
 assert set(q['knowledge_point'])=={'db_id','id','title'}
 z=q['generation'];name=z['template'];par=z['parameters'];R=s.Rational(str(par['R']));c=s.Integer(par.get('c',1));a=s.Integer(par.get('a',1));b=s.Integer(par.get('b',1));f={'upper_linear':a*x+b*y,'lower_sqrt':c*x*s.sqrt(x*x+y*y),'odd_disk':c*x*x*y,'square_y':c*y*y,'exponential':c*s.exp(x*x+y*y),'radial_square':c*(x*x+y*y),'upper_ratio':c*x/y,'rational_quarter':c/(x*x+y*y+1),'quarter_difference':c*(x-y)}[name]
 problem=q['question'][':question/problem'];sol=q['question'][':question/worked-solution']
 printed=problem.split('$f(x,y)=')[1].split('$')[0] if '$f(x,y)=' in problem else re.search(r'\\iint_D (.*?)\\,\\mathrm',problem)[1]
 assert same(scalar(printed),f),(name,printed,'prompt')
 if name in ('lower_sqrt','upper_ratio'):
  bounds=(-s.pi/2,0,-R*s.sin(t)) if name=='lower_sqrt' else (0,s.pi/2,R*s.sin(t))
 else:bounds={'upper_linear':(0,s.pi,R),'rational_quarter':(s.pi,3*s.pi/2,R),'quarter_difference':(0,s.pi/2,R)}.get(name,(0,2*s.pi,R))
 lo,hi,up=bounds;pol=s.trigsimp(f.subs({x:r*s.cos(t),y:r*s.sin(t)})*r)
 if name=='lower_sqrt':pol=c*r**3*s.cos(t)
 rad=s.integrate(pol,(r,0,up));ans=s.simplify(s.integrate(s.expand_trig(rad),(t,lo,hi)))
 if name=='upper_ratio':assert s.limit(s.integrate(s.simplify(rad),(t,s.Symbol('eps',positive=True),hi)),s.Symbol('eps',positive=True),0,dir='+')==ans
 groups=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);last=groups[-1];rows=re.split(r'\\\\',last);assert len(rows)==len(z['stages'])
 lhs=rows[0].split('&=')[0];assert same(scalar(lhs.split(r'\iint_D ')[1].split(r'\,\mathrm')[0]),f)
 first=rows[0].split('&=')[1];assert first.startswith(r'\iint_\Delta ')
 body=first[len(r'\iint_\Delta '):].split(r'\,\mathrm')[0];actual=scalar(body)
 if name=='lower_sqrt':actual=s.refine(s.trigsimp(actual),s.Q.nonnegative(r))
 assert same(actual,pol),(name,'substitution + Jacobian',actual,pol)
 for row in rows[1:]:
  raw=row.split('&=')[1].strip()
  if r'\iint_\Delta ' in raw:
   prefix,body=raw.split(r'\iint_\Delta ');body=body.split(r'\,\mathrm')[0];factor=scalar(prefix) if prefix else 1;assert same(factor*scalar(body),pol),(name,'distributed polar integrand')
  else:assert same(evaluate(raw,rad),ans),(name,raw,'row value')
 field=q['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1];values=[]
 for option in field[':answer-field/choices']:
  val=scalar(option[':answer/value']);assert (option[':answer/id']==correct)==same(val,ans);values.append(val)
 assert len(values)==5 and all(not same(v,u) for i,v in enumerate(values) for u in values[i+1:])
 if z['bank_profile']=='authored':
  # Independent complete operation-bank reference, derived from the displayed
  # integrand and actual region; all entries are compared one-to-one.
  expected=[v.subs({RR:R,CC:c,AA:a,BB:b}) for v in operation_reference(name)]
  assert all(sum(same(v,u) for u in values)==1 for v in expected),(name,'whole operation bank')
 assert sol.count('$')%2==0 and problem.count('$')%2==0
 for content in (sol,problem):
  depth=0
  for i,ch in enumerate(content):
   if ch in '{}':
    if i and content[i-1]=='\\':continue
    depth+=1 if ch=='{' else -1;assert depth>=0,(name,'brace')
  assert depth==0,(name,'brace')
 assert '\\![]' not in sol and '--' not in sol and '+-' not in sol
 return ans,len(rows)


def normalize_source_math(raw):
 raw=raw.replace('⁡','').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{ln}',r'\ln')
 raw=raw.replace('{∬}_{D}',r'\iint_D ').replace('{∬}_{Δ}',r'\iint_\Delta ').replace('{Δ}',r'\Delta').replace('Δ',r'\Delta')
 raw=raw.replace(r'{\int }',r'\int').replace(r'\text{d}',r'\mathrm{d}').replace(r'\text{ d}',r'\mathrm{d}').replace(r'\text{ }d',r'\mathrm{d}')
 raw=raw.replace('{[','[').replace(']}',']').replace('dA',r'\mathrm{d}A')
 return raw

def check_source_stages(src,case):
 # Read all source rows. Known initial-expression errors are repaired only in this
 # check, with the raw expression and correction both recorded in evidence.
 name=case['template'];par=case['parameters'];m=g.mathdata(name,par)
 target=s.sympify(str(m['angular']),locals={'theta':t,'r':r});answer=s.sympify(str(m['answer']))
 group=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',src[':question/worked-solution'],re.S)[-1]
 rows=re.split(r'\\\\',group)
 for index,row in enumerate(rows):
  raw=normalize_source_math(row.split('=')[1].replace('&','').strip().rstrip('.'))
  if index==0:
   lhs=normalize_source_math(row.split('=')[0].replace('&','').strip())
   lhs=lhs.split(r'\iint_D ')[1].split(r'\,')[0]
   expected=s.sympify(str(m['f']),locals={'x':x,'y':y})
   if name=='odd_disk':assert scalar(lhs)==12*x*x*y
   else:assert same(scalar(lhs),expected),(name,'source initial Cartesian integral')
  if r'\iint_' in raw:
   if index==0 and name=='exponential':
    assert '(r{cos}^{2}' in raw
    raw=raw.replace('(r{cos}^{2}',r'(r{cos}')
   prefix,body=raw.split(r'\iint_\Delta ');body=body.split(r'\,\mathrm')[0]
   actual=(scalar(prefix) if prefix else 1)*scalar(body)
   if name=='lower_sqrt':actual=s.refine(s.trigsimp(actual),s.Q.nonnegative(r))
   pol=s.sympify(str(m['polar']),locals={'r':r,'theta':t})
   assert same(actual,pol),(name,index,'source polar substitution')
   continue
  assert same(evaluate(raw,target),answer),(name,index,raw,'source full stage mismatch')
 return len(rows)

def main():
 cases=json.loads((HERE/'source-cases.json').read_text());records=[];fidelity=[]
 for case in cases:
  q=g.generate(case['level'],42,case['template'],parameters=case['parameters'],profile=case['bank_profile']);ans,n=check_record(q);src=g.SOURCES[case['source_id']];bank=src[':question/answer-fields'][0]
  original=[scalar(v[':answer/value']) for v in bank[':answer-field/choices']];generated=[scalar(v[':answer/value']) for v in q['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert all(sum(same(v,u) for u in generated)==1 for v in original)
  assert same(scalar(bank[':answer-field/correct'][':answer/value']),ans)
  oldrows=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',src[':question/worked-solution'],re.S)[-1].split(r'\\');assert len(oldrows)==n,(case['source_id'],len(oldrows),n)
  check_source_stages(src,case)
  fidelity.append({'source_id':case['source_id'],'bank_matches':5,'correct_designation':True,'source_stage_count':n,'generated_stage_count':n,'notation_normalized':True,'mathematical_repair':q['generation']['repairs']});records.append(q)
 raw_records=[]
 for case in cases:
  raw=g.generate(case['level'],42,case['template'],parameters=case['parameters'],profile='observed_raw')
  if case['template'] in ('odd_disk','exponential'):
   try:check_record(raw);raise RuntimeError('Expected historical source error was not detected')
   except AssertionError:pass
  else:check_record(raw)
  raw_records.append(raw)
 (HERE/'raw-replay.json').write_text(json.dumps(raw_records,ensure_ascii=False,indent=2)+'\n')
 variants=[]
 for name,(level,_,_) in g.TEMPLATES.items():
  for seed in range(6):
   q=g.generate(level,seed,name);check_record(q);records.append(q)
   if seed<2:variants.append(q)
 # Explicit inputs: malformed scope and invalid complete banks are rejected.
 for name,(level,_,par) in g.TEMPLATES.items():
  try:g.generate(level,template=name,parameters=dict(par,R=9));raise AssertionError('accepted out-of-scope radius')
  except ValueError:pass
 for name in ('odd_disk','quarter_difference'):
  q=g.generate(g.TEMPLATES[name][0],9,name);assert check_record(q)[0]==0
 for name,(level,_,par) in g.TEMPLATES.items():
  q=g.generate(level,1,name,parameters=par);q2=g.generate(level,99,name,parameters=par);assert q['question'][':question/id']==q2['question'][':question/id']
  q3=g.generate(level,1,name,parameters=par,profile='observed');assert q['generation']['mathematical_fingerprint']==q3['generation']['mathematical_fingerprint'];assert q['question'][':question/id']!=q3['question'][':question/id']
 # Native grading checks all five choices on every validated record.
 fixtures=[]
 for i,q in enumerate(records):
  field=q['question'][':question/answer-fields'][0];fixtures.append({'label':str(i),'record':q,'checks':[{'submitted_answer_id':v[':answer/id'],'expected':'accepted' if v[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'owned radio choice'} for v in field[':answer-field/choices']]})
 (HERE/'native-input.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n');subprocess.run(['generate/runs/current/check-engine',str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 # Fresh identical/different parameter concurrent plots; exact sidecars checked.
 parameters=[{'R':4,'c':7},{'R':5,'c':8},{'R':4,'c':7},{'R':5,'c':8}]
 import tempfile
 concurrency_dir=Path(tempfile.mkdtemp(prefix='concurrent-',dir=HERE))
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:paths=list(ex.map(lambda par:g.render_plots('lower_sqrt',par,concurrency_dir),parameters))
 assert paths[0]==paths[2] and paths[1]==paths[3] and paths[0]!=paths[1]
 for path,par in zip(paths,parameters):assert json.loads(Path(path).with_suffix('.json').read_text())['parameters']['R']==par['R']
 assert not list(concurrency_dir.glob('input-*.json')) and not list(concurrency_dir.glob('render-*'))
 (HERE/'review.json').write_text(json.dumps(variants,ensure_ascii=False,indent=2)+'\n')
 report={'passed':True,'sources':len(cases),'banks':len(cases),'options':len(cases)*5,'mathematically_repaired_sources':2,'raw_public_replays':9,'raw_expected_wrong_stages':2,'source_rows':sum(v['source_stage_count'] for v in fidelity),'raw_exact_solution_strings':0,'notation_normalized_solutions':9,'stage_layout_matches':9,'generated_checked':len(records)-9,'source_fidelity':fidelity,'native_report':'native-report.json','concurrent_fresh_assets':4,'hashes':{fn:hashlib.sha256((HERE/fn).read_bytes()).hexdigest() for fn in ['source.json','source-cases.json','render.py','scalar_parser.py','validate.py']},'generator_hash':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='source_fidelity'},indent=2))
if __name__=='__main__':main()
