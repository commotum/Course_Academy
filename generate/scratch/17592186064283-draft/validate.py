"""Private independent displayed grammar, every chain factor, exact bank and native QA."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
from functools import lru_cache
D=Path(__file__).resolve().parent;R=D.parents[2]
def load(p,n):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
g=load(D.with_suffix('.py'),'g');P=load(D/'scalar_parser.py','P');x,t,u=P.x,P.t,P.u

def save(n,o):(D/n).write_text(json.dumps(o,indent=2,default=str)+'\n')
def clean(a):
 a=a.replace(r'\dfrac',r'\frac').replace('⁡','').replace(r'\qquad',',').replace(r'\,\text{and}\,',',').replace(r'\,',',').replace(r'\text{and}',',')
 a=re.sub(r'\\textrm\{d\}',r'\\text{d}',a);a=re.sub(r'\\textrm\s+d\s*([fvutx])',r'\\text{d}\1',a)
 # Strip bbox wrapper by balanced groups, preserving nested trig inputs.
 while r'\bbox' in a:
  start=a.index(r'\bbox');at=a.index('{',a.index(']',start));depth=1;end=at+1
  while depth:
   depth+=(a[end]=='{')-(a[end]=='}');end+=1
  a=a[:start]+a[at+1:end-1]+a[end:]
 return a
@lru_cache(None)
def scalar(a):return P.scalar(a.strip().rstrip('.,').replace(r'\,',''))
@lru_cache(None)
def eq(a,b):
 d=s.expand(a-b)
 if d==0:return True
 for v in (s.Rational(1,3),s.Rational(2,3)):
  z=d.subs({x:v,t:v,u:v})
  if abs(complex(z.evalf()))>1e-9:return False
 return s.simplify(s.trigsimp(d))==0

def check(rec):
 q=rec['question'];md=rec['generation'];m=md['template'];p=md['parameters'];raw=md['evidence_only'];sol=q.get(':question/worked-solution');fn='csc' if m=='authored-csc-power' else g.T[m]['function'];var=t if m in ('q-143516','q-167568') else x
 expected=p['c']*getattr(s,fn)(var)**p['n'];prompt=q[':question/problem']
 given=re.search(r'\$(?:f\(x\)|v\(t\))\s*=\s*(.*?)\$',prompt)
 if given:fun=scalar(given[1]);assert eq(fun,expected)
 else:assert raw and m in ('q-143516','q-167568');fun=expected
 derivative=s.diff(fun,var);field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];bank=[scalar(a[':answer/value'].strip('$')) for a in choices]
 answer=derivative
 if m in ('q-143516','q-167568'):
  suffix=re.search(r'\$\\cdot\s*(.*?)\$',prompt);assert suffix;answer=derivative/scalar(suffix[1])
 matches=[i for i,z in enumerate(bank) if eq(z,answer)];assert len(matches)==1,(m,p,'unique key')
 assert all(not eq(a,b) for i,a in enumerate(bank) for b in bank[i+1:])
 if ':answer-field/correct' in field:
  ref=field[':answer-field/correct'];aid=ref[':answer/id'] if isinstance(ref,dict) else ref[1];assert choices[matches[0]][':answer/id']==aid
 else:assert raw and m=='q-48562'
 assert md['domain']=={'variable':str(var),'restriction':'sin('+str(var)+') != 0' if fn=='csc' else 'all real '+str(var)}
 if sol:
  assert all(ord(c)>=32 or c=='\n' for c in sol)
  z=clean(sol);blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$|\\\[\s*(.*?)\s*\\\]',z,re.S);blocks=[a or b for a,b in blocks];assert len(blocks)>=3
  first=blocks[0].split('=',1)[1];assert eq(scalar(first),fun)
  split=re.split(r',+\s*u\s*=',blocks[1]);assert len(split)==2;label=split[0].split('=')[0].strip();outer=scalar(split[0].split('=',1)[1]);inner=scalar(split[1]);assert outer.free_symbols<={u} and inner.free_symbols<={var};assert eq(outer.subs(u,inner),fun)
  # Every formal derivative binding reads its operands, variables and RHS.
  bindings=re.findall(r'\\frac\{\\text\{d\}([fvutx])\}\{\\text\{d\}([utx])\}\s*=\s*(.*?)(?=,|$)',blocks[2]);assert len(bindings)==2,(m,blocks[2])
  target=[(label,'u',s.diff(outer,u)),('u',str(var),s.diff(inner,var))]
  for (a,b,c),(d,e,f) in zip(bindings,target):assert (a,b)==(d,e);assert eq(scalar(c),f)
  chains=re.findall(r'\\begin\{(?:aligned|align\*)\}(.*?)\\end\{(?:aligned|align\*)\}',z,re.S);assert len(chains)==1
  rows=re.split(r'\\\\(?:\[[^\]]*\])?',chains[0]);assert len(rows)>=3
  lhs=rows[0].split('&')[0].strip();assert lhs in ("f'(x)","{f}^{′}(x)",'a(t)'),(m,lhs)
  formal=r'\\frac\{\\text\{d\}([fvutx])\}\{\\text\{d\}([utx])\}'
  def subst(mm):
   a,b=mm.groups();assert (a,b) in ((label,'u'),('u',str(var)));return '('+s.latex(s.diff(outer,u) if a==label else s.diff(inner,var))+')'
  for row in rows:
   rhs=row.split('=',1)[1].strip();rhs=re.sub(formal,subst,rhs);rhs=re.sub(r'\{v\}\^\{[′\x27]\}\(t\)',lambda _:s.latex(derivative),rhs)
   
   try:value=scalar(rhs)
   except Exception:print('PARSE',m,repr(rhs));raise
   assert eq(value.subs(u,inner),derivative),(m,p,'chain stage',rhs)
  assert 'First, we' in z and 'Now, we see' in z and 'Differentiating' in z and 'We now apply the chain rule' in z
 return answer

def nativechecks(r):
 f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('radio'):return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every field-owned full-bank option'} for a in f[':answer-field/choices']]
 a=f[':answer-field/choices'][0][':answer/value'];return [{'field_index':0,'submitted':v,'expected':e,'purpose':'canonical/equivalent/zero/nonzero/+1'} for v,e in [(a,'accepted'),('2('+a+')/2','accepted'),('0','rejected'),('1','rejected'),('('+a+')+1','rejected')]]
def failure(fn):
 try:fn()
 except (AssertionError,ValueError):return
 raise AssertionError('Actual-input mutation accepted')
def main():
 raw=[];normal=[];review=[];cases=[]
 for m in g.T:
  c={'source_id':m,'level':g.LEVELS[m],'template':m,'parameters':g.T[m]['defaults'],'profile':'observed_raw'};cases.append(c);r=g.generate(c['level'],template=m,parameters=c['parameters'],profile=c['profile']);assert r['question']==g.T[m]['source'];check(r);raw.append(r)
 for m in g.LEVELS:
  print('Validate',m,flush=True)
  for i,p in enumerate(g.parameters_for(m)):
   r=g.generate(g.LEVELS[m],i,template=m,parameters=p);check(r);normal.append(r)
  review.extend([normal[-len(g.parameters_for(m))],normal[-1]])
  if m in g.T:
   for p in [g.parameters_for(m)[0],g.parameters_for(m)[-1]]:check(g.generate(g.LEVELS[m],template=m,parameters=p,profile='observed_raw'))
 negatives=0
 for m in g.LEVELS:
  failure(lambda:g.generate(g.LEVELS[m],template=m,parameters={'c':99,'n':17}));negatives+=1
 # Actual emitted operators/operands, outer, inner, signs, chain stages and key.
 base=g.generate('moderate',template='q-72157',parameters={'c':4,'n':7})
 mutators=[lambda q:q.__setitem__(':question/problem',q[':question/problem'].replace('{7}','{6}')),lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('f=4','f=5')),lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('u=\\operatorname{cos}','u=\\operatorname{sin}')),lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('=-\\operatorname{sin}','=\\operatorname{sin}')),lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('28{u}','27{u}')),lambda q:q[':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id','wrong'])]
 for fn in mutators:
  r=copy.deepcopy(base);before=copy.deepcopy(r);fn(r['question']);assert before!=r;failure(lambda:check(r));negatives+=1
 for m in g.LEVELS:
  p=g.parameters_for(m)[0];a=g.generate(g.LEVELS[m],0,template=m,parameters=p);b=g.generate(g.LEVELS[m],81,template=m,parameters=p);assert a['question'][':question/id']==b['question'][':question/id']
 cli=subprocess.run([sys.executable,str(D.with_suffix('.py')),'--difficulty','all','--count','1','--seed','5','--format','json'],capture_output=True,text=True,check=True);assert len(json.loads(cli.stdout))==3
 save('source-cases.json',cases);save('review.json',{'original_replays':raw,'generated_variants':review});(D/'review.md').write_text('\n\n'.join(['# Power of a trigonometric function — private draft']+['## '+r['generation']['template']+' / '+('Raw original' if r['generation']['evidence_only'] else 'Changed eligible variant')+'\n\n'+g.markdown(r) for r in raw+review])+'\n')
 engine=[{'label':str(i),'record':r,'checks':nativechecks(r)} for i,r in enumerate(normal)];save('engine-input.json',engine);binary=R/'generate/runs/current/check-engine';assert hashlib.sha256(binary.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea';out=subprocess.run([str(binary),str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True);(D/'engine.log').write_text(out.stdout+out.stderr);assert out.returncode==0,out.stderr
 n=json.load(open(D/'engine-report.json'));assert n['documented_unresolved_checks']==0
 baseline=json.load(open(D/'registered-baseline.json'));old=R/'generate/scratch/17592186064283';actual=[old.with_suffix('.py')]+sorted(p for p in old.rglob('*') if p.is_file());assert set(map(str,actual))==set(baseline);assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in baseline.items())
 report={'status':'pass','basis':2275,'MA_raw_originals':len(raw),'raw_complete_banks':len(raw),'independent_inventory_exact':3,'exhaustive_normal_records':len(normal),'meaningful_tasks_per_level':{l:len({r['generation']['mathematical_fingerprint'] for r in normal if r['generation']['level']==l}) for l in g.SUPPORTED_LEVELS},'actual_input_negative_controls':negatives,'all_bounded_slots_checked':True,'registered_baseline_unchanged':True,'native_grading':{k:n[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','entry_point')},'hard_authored':True,'excluded_parameters':'n>8 and |c|>9 rejected in all public eligible calls; source-raw remains exact originals within these bounds.'};save('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
