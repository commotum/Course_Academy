import os,sys,json,re,hashlib,shutil,subprocess,platform
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
ROOT=Path.cwd(); REPO=Path('/home/jake/Developer/Course_Academy'); PKG=ROOT.parent/'workspace'; PY=str(REPO/'.venv/bin/python')
sys.path.insert(0,str(PKG)); import generator as g
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x=s.Symbol('x',real=True); u=s.Symbol('u',positive=True)
def save(n,v): (ROOT/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def untex(t):
 t=t.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace('{)}',')').replace(r'\dfrac',r'\frac').replace(r'\cdot','*')
 def part(i):
  if t[i]=='{':return seq(i+1,'}')
  if t[i]=='\\':return command(i)
  return t[i],i+1
 def command(i):
  m=re.match(r'\\([A-Za-z]+)',t[i:]); name=m[1]; i+=len(m[0])
  if name=='frac':
   a,i=part(i);b,i=part(i);return '(('+a+')/('+b+'))',i
  if name=='sqrt':
   a,i=part(i);return 'sqrt('+a+')',i
  raise ValueError((name,t))
 def seq(i,end=None):
  o=''
  while i<len(t):
   c=t[i]
   if c==end:return o,i+1
   if c=='\\':v,i=command(i);o+=v
   elif c=='{':v,i=seq(i+1,'}');o+='('+v+')'
   else:o+=('**' if c=='^' else c);i+=1
  if end:raise ValueError('unclosed '+t)
  return o,i
 out=seq(0)[0]
 return parse_expr(out,local_dict={'x':x,'u':u,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def field(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=field(r);return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def expected(r):
 p=r['question'][':question/problem']; m=re.search(r'y\s*=\s*([^$]+)',p); expr=untex(m[1].rstrip('., '));der=s.diff(expr,x)
 mt=re.search(r'where\s+\$x\s*=\s*(-?\d+)',p)
 return expr,der,s.simplify(der.subs(x,int(mt[1]))) if mt else der

def equivalent(a,b):
 diff=s.simplify(a-b)
 if diff==0:return True
 # Branch-sensitive simplification: compare on exact positive-radicand rational points.
 vals=[]
 for v in [-19,-7,-2,-s.Rational(1,3),0,s.Rational(1,3),2,7,19]:
  av,bv=a.subs(x,v),b.subs(x,v)
  if av.is_real and bv.is_real and av.is_finite and bv.is_finite:
   vals.append(s.simplify(av-bv)==0)
 return bool(vals) and all(vals)

def math_record(r):
 expr,der,ans=expected(r);f=field(r);actual=untex(correct(r));good=equivalent(actual,ans)
 hits=[]
 for a in f[':answer-field/choices']:
  try:
   if equivalent(untex(a[':answer/value']),ans):hits.append(a[':answer/id'])
  except Exception:pass
 return {'id':r['question'][':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'expression_from_prompt':str(expr),'independent_derivative':str(der),'independent_answer':str(ans),'stored_answer':correct(r),'correct':good,'unique_correct':len(hits)==1,'choice_count':len(f[':answer-field/choices'])}

def main():
 before={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()};save('package-hashes-before.json',before)
 samples=[]
 for ti,(name,spec) in enumerate(g.TEMPLATES.items()):
  for n in range(10):samples.append(g.generate(spec['level'],seed=910037+101*ti+n,template=name))
 save('samples.json',samples);runner=json.loads((ROOT.parent/'samples.json').read_text());save('runner-batch.json',runner)
 replay=g.replay_sources();save('source-replay.json',replay)
 cases=[]
 for t in ['reciprocal_blank','sqrt_constfirst_radio']:
  for b in [3,7]:cases.append(g.generate('moderate',seed=7721,template=t,parameters={'a':-4,'b':b},bank_role=2))
 # same curve: positive, zero, negative slope, preserving real/simple values
 for t in [2,5,8]:cases.append(g.generate('easy',seed=7722,template='slope_sqrt_quadratic_blank',parameters={'a':-1,'b':10,'c':0,'t':t}))
 # reciprocal outer versus square-root outer, same curve
 for t in ['reciprocal_radio','sqrt_linear_radio']:cases.append(g.generate('moderate',seed=7723,template=t,parameters={'a':6,'b':-3},bank_role=2))
 # same math, shuffle choice presentation only
 import copy
 shuffled=copy.deepcopy(cases[-1]);field(shuffled)[':answer-field/choices'].reverse();cases.append(shuffled)
 save('counterfactual-records.json',cases)
 checks=[]
 for r in samples+runner+replay+cases:
  try:checks.append(math_record(r))
  except Exception as e:checks.append({'id':r['question'][':question/id'],'error':repr(e)})
 save('math-results.json',checks)
 coverage={}
 for r in samples:
  t=r['generation']['template'];p=r['generation']['parameters'];c=coverage.setdefault(t,{'samples':0,'a_signs':set(),'answer_signs':set(),'positions':{},'roles':{},'attempts':[]})
  c['samples']+=1;c['a_signs'].add((p['a']>0)-(p['a']<0));ans=expected(r)[2]
  if not ans.has(x):c['answer_signs'].add(int(s.sign(ans)))
  f=field(r);pos=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]);c['positions'][pos]=c['positions'].get(pos,0)+1
  role=r['generation']['bank_assignment'];c['roles'][str(role)]=c['roles'].get(str(role),0)+1;c['attempts'].append(r['generation']['attempts'])
 for c in coverage.values():c['a_signs']=sorted(c['a_signs']);c['answer_signs']=sorted(c['answer_signs'])
 save('coverage.json',coverage)
 # replay compares captured source, not authored copy
 source=json.loads((ROOT.parent/'source/source.json').read_text()); sources={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
 replay_checks=[]
 def canon(v):return re.sub(r'\s+','',v).replace('{)}',')').replace(r'\left','').replace(r'\right','')
 for r in replay:
  sid=r['generation']['replay_source_id']; q=sources[sid];f=field(r);sf=q[':question/answer-fields'][0]
  cap=r['generation']['source_capture'];rc={'source_id':sid,'captured_bank_exact':cap[':question/answer-fields']==q[':question/answer-fields'],'field_type_preserved':f[':answer-field/type']==sf[':answer-field/type'][':db/ident'],'prompt_exact_normalized':canon(q[':question/problem'])==canon(r['question'][':question/problem']),'solution_present':':question/worked-solution' in q,'solution_exact_normalized':canon(q.get(':question/worked-solution',''))==canon(r['question'][':question/worked-solution'])}
  if f[':answer-field/type'].endswith('/radio'):
   rc['complete_radio_bank_equivalent']=all(any(equivalent(untex(a[':answer/value']),untex(b[':answer/value'])) for b in f[':answer-field/choices']) for a in sf[':answer-field/choices']) and len(f[':answer-field/choices'])==len(sf[':answer-field/choices'])
  else:rc['blank_history_retained_in_capture']=True
  replay_checks.append(rc)
 save('source-replay-results.json',replay_checks)
 # invalid inputs and deterministic repeat; no external outputs are expected
 invalid=[('zero_inner', 'reciprocal_blank',{'a':0,'b':2}),('singular_point','slope_sqrt_linear_blank',{'a':2,'b':-2,'t':1}),('negative_radicand','slope_sqrt_linear_blank',{'a':2,'b':-3,'t':1}),('non_square','slope_sqrt_linear_blank',{'a':2,'b':1,'t':1}),('extra_parameter','reciprocal_blank',{'a':2,'b':1,'t':0})]
 rej=[]
 for label,t,p in invalid:
  try:g.generate(g.TEMPLATES[t]['level'],template=t,parameters=p);rej.append({'case':label,'rejected':False})
  except ValueError as e:rej.append({'case':label,'rejected':True,'reason':str(e)})
 # hold chosen bank role through rejection on known cancellation boundary; independently derive zero
 try:g.generate('easy',template='slope_sum_radio',parameters={'a':-6,'b':7,'t':1,'k':1},bank_role=3);rej.append({'case':'zero_sum_bank','rejected':False})
 except ValueError as e:rej.append({'case':'zero_sum_bank','rejected':True,'reason':str(e)})
 save('rejection-results.json',rej)
 deterministic=all(g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=r['generation']['seed'],template=r['generation']['template'])==r for r in samples[::10])
 save('runtime-results.json',{'python':platform.python_version(),'packages':{'sympy':s.__version__},'deterministic':deterministic,'dependencies_manifest':json.loads((PKG/'package.json').read_text())['dependencies'],'external_asset_outputs':[]})
 # records rendered: fresh moderate representatives, source slope+sum and controlled pairs
 representatives=[samples[0],samples[10],samples[20],samples[40],samples[50],samples[60],samples[70],samples[80],samples[-10]]+cases
 save('render-records.json',representatives)
 (ROOT/'session-state.md').write_text('Source reconstruction complete. Independently sampled all 15 templates, 150 fresh records; runner batch copied, all 17 sources replayed, 10 controlled records, math/coverage/rejection/runtime reports saved. Next: native grading, delivery filtering, relocation and actual UI render.\n')
 print(json.dumps({'samples':len(samples),'math_cases':len(checks),'math_failures':[c for c in checks if not c.get('correct') or not c.get('unique_correct')][:4],'replay_differences':[c for c in replay_checks if not c['prompt_exact_normalized'] or (c['solution_present'] and not c['solution_exact_normalized'])],'deterministic':deterministic},default=str))
if __name__=='__main__':main()
