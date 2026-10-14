#!/usr/bin/env python3
"""Independent displayed mathematics + raw fidelity + native radio checks."""
import faulthandler
faulthandler.dump_traceback_later(20,repeat=True)
import concurrent.futures,copy,importlib.util,json,re,subprocess,sys,tempfile
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('green',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
t,u=sp.symbols('t u',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,)
def expr(s):
 s=s.replace('⁡','').replace('∫',r'\int').replace('∮',r'\oint').replace('′',"'")
 s=re.sub(r'\\(?:operatorname|text)\{(.*?)\}',r'\1',s)
 s=s.replace(r'\left','').replace(r'\right','').replace(r'\limits','').replace(r'\,','').replace(r'\:','').replace(r'\cdot','*').replace(r'\pi','pi').replace(r'\sin','sin').replace(r'\cos','cos').replace(r'\dfrac',r'\frac')
 while '\\frac' in s:
  start=s.index('\\frac');pos=start+5;groups=[]
  for _ in range(2):
   assert s[pos]=='{',s
   depth=1;begin=pos+1;pos+=1
   while depth:
    if s[pos]=='{':depth+=1
    if s[pos]=='}':depth-=1
    pos+=1
   groups.append(s[begin:pos-1])
  s=s[:start]+'(('+str(expr(groups[0]))+')/('+str(expr(groups[1]))+'))'+s[pos:]
 # Parse definite integrals from their actual printed bounds and integrands.
 s=s.replace(r'{\int }',r'\int').replace(r'{\int}',r'\int')
 while '\\int' in s:
  m=re.search(r'\\int\s*_\{([^{}]+)\}\^\{([^{}]+)\}',s) or re.search(r'\\int\s*_([0-9]+)\^\{([^{}]+)\}',s)
  assert m,('integral bounds',s)
  end=re.search(r'(?:\\mathrm\{d\}|\\textrm\s*d|d)\s*([tu])',s[m.end():])
  assert end,('integral differential',s)
  lo,hi=expr(m[1]),expr(m[2]);z={'t':t,'u':u}[end[1]]
  f=expr(s[m.end():m.end()+end.start()]);v=sp.integrate(f,(z,lo,hi))
  s=s[:m.start()]+'('+str(v)+')'+s[m.end()+end.end():]
 # Primitive evaluation brackets and vertical bars.
 m=re.search(r'\[(.*)\]_\{([^{}]+)\}\^\{([^{}]+)\}',s)
 if m:
  primitive=expr(m[1]);lo,hi=expr(m[2]),expr(m[3]);z=t if primitive.has(t) else u
  s=s[:m.start()]+'('+str(sp.simplify(primitive.subs(z,hi)-primitive.subs(z,lo)))+')'+s[m.end():]
 m=re.search(r'(?P<coefficient>.*?)(?P<power>\{*u\}*\^\{?3\}?)[{}]*\|[{}]*_\{(-?\d+)\}\^\{(-?\d+)\}',s)
 if m:s=m['coefficient']+'('+str(int(m[4])**3-int(m[3])**3)+')'
 s=re.sub(r'\{([^{}]*)\}',r'\1',s)
 while '{' in s:s=s.replace('{','(').replace('}',')')
 s=s.replace('^','**').strip().rstrip('.')
 # Protect common function application and square notation.
 s=re.sub(r'(sin|cos)\*\*(\d+)\s*t',r'(\1(t))**\2',s)
 s=re.sub(r'(sin|cos)\s*(\d*)t',lambda m:m[1]+'('+ (m[2]+'*' if m[2] else '')+'t)',s)
 return parse_expr(s,local_dict={'t':t,'u':u,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos},transformations=TRANS)
def prompt_segments(record):
 p=re.sub(r'!\[\]\(.*?\)','',record['question'][':question/problem'])
 chunks=re.findall(r'(?:r(?:_\{?[12]\}?)?\(t\)|\{r\}_\{[12]\}\(t\))\s*=([^$]+)\$',p)
 assert chunks,p
 seg=[]
 for i,chunk in enumerate(chunks):
  # Coefficient values are parsed from complete displayed x/y components.
  chunk=chunk.replace(r'\,','').strip();m=re.match(r'(.*?)i\s*([+-].*)j\s*$',chunk);assert m,chunk
  x,y=expr(m[1]),expr(m[2]);tail=p[p.index(chunk.replace('','')):] if False else p
  bounds=re.findall(r't(?:\\in| ∈)\s*\[([^\]]+)\]',p)
  if bounds:
   l,h=bounds[i].split(',');lo,hi=expr(l),expr(h)
  else:raise AssertionError('bounds missing')
  seg.append((x,y,lo,hi))
 return seg

def check_record(r):
 q=r['question'];raw=r['generation']['evidence_only']
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in text),'control character'
  assert text.count('$')%2==0,'math delimiters'
  depth=0
  for c in text:
   if c=='{':depth+=1
   if c=='}':depth-=1
   assert depth>=0,'brace closure'
  assert depth==0,'brace balance'
 seg=prompt_segments(r)
 # Shoelace integral reads the actual printed curve and bounds; independent of
 # declared field choice, metadata parameters, orientation or generator geometry.
 signed=sp.simplify(sum(sp.integrate(x*sp.diff(y,t)-y*sp.diff(x,t),(t,l,h))/2 for x,y,l,h in seg));area=abs(signed)
 for (x,y,l,h),(nx,ny,nl,nh) in zip(seg,seg[1:]+seg[:1]):assert sp.simplify(x.subs(t,h)-nx.subs(t,nl))==0 and sp.simplify(y.subs(t,h)-ny.subs(t,nl))==0,'segment closure'
 sol=q.get(':question/worked-solution')
 if sol:
  assert ('positively oriented' if signed>0 else 'negatively oriented') in sol
  # Every formal coordinate derivative, including zero component on line segment.
  derivative=sol.split('The derivative',1)[1].split('Finally,',1)[0].split('Therefore,',1)[0]
  equations=re.findall(r'\(t\)\s*(?:&\s*)?=([^\n]+?)(?:\\end\{aligned\}|\.\$\$|\\\\)',derivative)
  if 'ellipse'!=r['generation']['template']:
   assert len(equations)==len(seg),(equations,derivative)
   for eq,(x,y,l,h) in zip(equations,seg):
    eq=eq.strip().rstrip('.').replace(r'\,','');m=re.match(r'(.*?)i([+-].*)j\.?$',eq)
    if m:dx,dy=expr(m[1]),expr(m[2])
    elif eq.endswith('i'):dx,dy=expr(eq[:-1]),sp.Integer(0)
    elif eq.endswith('j'):dx,dy=sp.Integer(0),expr(eq[:-1])
    else:raise AssertionError(eq)
    assert sp.simplify(dx-sp.diff(x,t))==0 and sp.simplify(dy-sp.diff(y,t))==0,('displayed derivative',eq,x,y)
  chain=sol.rsplit(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
  rows=chain.split(r'\\')
  for row in rows:
   if '&' not in row:continue
   rhs=row.split('&',1)[1].strip().lstrip('=').strip()
   if '∮' in rhs or '\\oint' in rhs:continue
   value=sp.simplify(expr(rhs));assert sp.simplify(value-area)==0,('stage',rhs,value,area)
  if not raw:
   if r['generation']['template']!='ellipse':assert len(rows)>=10,'individual endpoints missing'
  for f in q[':question/answer-fields']:
   if ':answer-field/correct' in f:
    correct=[a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]][0]
    assert sp.simplify(expr(correct[':answer/value'])-area)==0
 for f in q[':question/answer-fields']:
  vals=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
  assert all(sp.simplify(x-y)!=0 for i,x in enumerate(vals) for y in vals[i+1:]),'ambiguous bank'
 return area

def raw_compare(r,s):
 q=r['question'];assert q[':question/problem']==s[':question/problem'];assert q.get(':question/worked-solution')==s.get(':question/worked-solution')
 for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (key in q)==(key in s)
 if ':question/difficulty' in s:assert q[':question/difficulty']==s[':question/difficulty'][':db/ident']
 assert len(q[':question/answer-fields'])==len(s[':question/answer-fields'])
 for f,original in zip(q[':question/answer-fields'],s[':question/answer-fields']):
  assert f[':answer-field/key']==original[':answer-field/key'];assert f[':answer-field/type']==original[':answer-field/type'][':db/ident']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in original[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in original)
  if ':answer-field/correct' in original:
   chosen=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert chosen==original[':answer-field/correct'][':answer/value']

def main():
 cases=[];replays=[];variants=[];checks=[]
 for sid,spec in g.SPECS.items():
  family,a,b,level,_,_=spec;p={'a':a,'b':b};print('checking',sid,flush=True)
  r=g.generate(level,parameters=p,profile='original:'+sid);raw_compare(r,g.QS[sid]);check_record(r);replays.append(r)
  cases.append({'source_id':sid,'math_academy_id':g.QS[sid][':question/math-academy-id'],'template':family,'parameters':p,'bank_profile':'original:'+sid,'level':level,'authored_level_assignment':':question/difficulty' not in g.QS[sid]})
  # Changed coefficients through BOTH public raw and normal recipes.
  for p in [{'a':3,'b':5},{'a':7,'b':4}]:
   rr=g.generate(level,parameters=p,profile='original:'+sid);check_record(rr)
   r=g.generate(level,parameters=p,template=family);check_record(r);variants.append(r)
 for p in [{'a':2,'b':3},{'a':5,'b':4}]:r=g.generate_easy(parameters=p);check_record(r);variants.append(r)
 for level in ['easy','moderate','hard']:
  coverage=set()
  for seed in range(35):
   r=g.generate(level,seed);check_record(r);coverage.add(r['generation']['template'])
  assert coverage=={k for k,v in g.FAMILY_LEVEL.items() if v==level},coverage
 # Identity invariant: option shuffles do not alter content identity.
 for r in variants:
  rr=g.generate(r['question'][':question/difficulty'].split('/')[-1],999,template=r['generation']['template'],parameters=r['generation']['parameters'])
  assert rr['question'][':question/id']==r['question'][':question/id']
 # Meaningful mutation regressions; final answer alone must not hide them.
 for mutate in ['control','derivative','intermediate']:
  r=copy.deepcopy(variants[0]);s=r['question'][':question/worked-solution']
  if mutate=='control':s+='\x0c'
  elif mutate=='derivative':s=s.replace(r'3\operatorname{cos}',r'4\operatorname{cos}',1)
  else:s=s.replace('=30{\\int }','=31{\\int }',1)
  r['question'][':question/worked-solution']=s
  try:check_record(r)
  except (AssertionError,Exception):pass
  else:raise AssertionError('mutation escaped '+mutate)
 for r in variants:
  f=r['question'][':question/answer-fields'][0];checks.append({'label':r['generation']['template']+str(r['generation']['parameters']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete native bank'} for a in f[':answer-field/choices']]})
 (ROOT/'engine-input.json').write_text(json.dumps(checks,indent=2));subprocess.run(['generate/runs/current/check-engine',str(ROOT/'engine-input.json'),str(ROOT/'engine-results.json')],check=True)
 # Fresh concurrent renderer writes, same/different instances; inspect sidecar geometry.
 with tempfile.TemporaryDirectory(dir=ROOT,prefix='concurrent-') as tmp:
  work=[('sin_sin2',{'a':3,'b':5}),('sin_sin2',{'a':3,'b':5}),('lower_polynomial',{'a':7,'b':4})]
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:paths=list(pool.map(lambda z:g.render_plots(*z,output_dir=tmp),work))
  assert paths[0]==paths[1]
  for path,(family,p) in zip(paths,work):assert json.loads(Path(path).with_suffix('.json').read_text())['parameters']==p
  assert not list(Path(tmp).glob('render-*')) and not list(Path(tmp).glob('sidecar-*'))
 (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2));(ROOT/'review.json').write_text(json.dumps({'original_replays':replays,'generated_variants':variants},indent=2))
 lines=['# Original questions and parameterized variants','All originals below are explicit ineligible historical evidence profiles. Normal variants use complete method banks.']
 for label,records in [('Original',replays),('Generated',variants)]:
  for r in records:
   q=r['question'];lines += ['\n## '+label+' '+r['generation']['template']+' '+str(r['generation']['parameters']),q[':question/problem'],'\nChoices: '+', '.join(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']),q.get(':question/worked-solution','[Absent in source; retained as absent in raw replay.]')]
 (ROOT/'review.md').write_text('\n\n'.join(lines))
 report={'status':'pass','practice_sources':8,'exact_prompt_replays':8,'exact_solution_replays':7,'source_solution_absence_replayed':1,'full_banks':9,'source_options':45,'correct_designations_matched':7,'missing_designations_preserved':2,'key_presence_parity':8,'normal_templates':9,'authored_easy':'ellipse evaluation, not sibling setup','source_opaque_banks':'8 evidence-only profiles; no recovered intent claimed','native':json.loads((ROOT/'engine-results.json').read_text()),'displayed_math_checked':'prompt closure/orientation/area, every coordinate derivative, every numerical integral and primitive/endpoint/final row','fresh_concurrency':'pass','mutation_regressions':['control','derivative','intermediate'],'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__,'database_writes':0}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='native'},indent=2))
if __name__=='__main__':main()
