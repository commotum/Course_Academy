"""Independent ODE/solution/bank parsing and real application grading."""
import hashlib,importlib.util,json,re,subprocess,sys
from functools import lru_cache
from pathlib import Path
sys.path.insert(0,'/tmp/ca-bernoulli-validation')
import sympy as sp
from sympy.parsing.latex import parse_latex
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('bernoulli_solve',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x',positive=True);y=sp.Symbol('y',positive=True);C=sp.Symbol('C',positive=True);D=sp.Symbol('D')
def save(p,v):p.write_text(json.dumps(v,indent=2,default=str)+'\n')
@lru_cache(None)
def parse(t):
 t=t.strip().rstrip('.,').replace(r'\pm','').replace('⁡','')
 t=re.sub(r'\\frac\{\\text\{d\}([yz])\}\{\\text\{d\}x\}|\\frac\{d([yz])\}\{dx\}', 'D',t)
 expr=parse_latex(t,strict=True)
 return expr.xreplace({a:{'x':x,'y':y,'C':C,'D':D,'e':sp.E}.get(str(a),a) for a in expr.free_symbols})
def ode(q):
 eq=re.search(r'\$\$([\s\S]*?)\$\$',q[':question/problem'])[1].strip().rstrip('.')
 lhs,rhs=eq.split('=');res=sp.expand(parse(lhs)-parse(rhs));F=sp.simplify(-res.subs(D,0)/sp.diff(res,D))
 powers={sp.simplify(y*sp.diff(term,y)/term) for term in sp.Add.make_args(sp.expand(F))};assert len(powers)==2 and 1 in powers
 n=next(p for p in powers if p!=1)
 terms=sp.Add.make_args(sp.expand(F))
 linear=sp.simplify(sum(term/y for term in terms if sp.simplify(y*sp.diff(term,y)/term)==1))
 nonlinear=sp.simplify(sum(term/y**n for term in terms if sp.simplify(y*sp.diff(term,y)/term)==n))
 assert not linear.has(y) and not nonlinear.has(y)
 return F,-linear,nonlinear,n

@lru_cache(None)
def residual(value,p,q,n):
 z=sp.powdenest(value**(1-n),force=True)
 # The square inversion of y=(C exp(u/2)-1)^2 needs the documented
 # positive square-root branch, C exp(u/2)-1>0.
 if n==sp.Rational(1,2):
  z=z.replace(sp.Abs,lambda arg:arg)
 return sp.simplify(sp.expand(sp.diff(z,x)+(1-n)*p*z-(1-n)*q))
def independent(r):
 q=r['question'];F,p,coef,n=ode(q);h=r['generation']['parameters']['shift']
 # Unit-slope translated coordinate u is positive. Substitute after parsing
 # the displayed prompt/bank; this also catches mismatched shifts.
 p=sp.simplify(p.subs(x,x-h));coef=sp.simplify(coef.subs(x,x-h));f=q[':question/answer-fields'][0]
 assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 choices=f[':answer-field/choices'];assert len(choices)==5
 values=[sp.simplify(parse(a[':answer/value'].split('=',1)[1]).subs(x,x-h)) for a in choices]
 keys=[a[':answer/id']==f[':answer-field/correct'][1] for a in choices];assert sum(keys)==1
 for a,Y,key in zip(choices,values,keys):
  res=residual(Y,p,coef,n)
  if key:assert res==0,(r['generation']['template'],a[':answer/value'],res)
  else:
   # A nonzero arbitrary-constant residual excludes equivalence as solution families.
   assert res!=0,(r['generation']['template'],'second correct family',a[':answer/value'])
   witnesses=[]
   h=r['generation']['parameters']['shift']
   for xv,cv in [(sp.Rational(1,5),3),(sp.Rational(2,5),5),(sp.Rational(1,2),7)]:
    z=res.subs({x:xv,C:cv}).evalf(20)
    if z.is_finite and abs(complex(z))>1e-9:witnesses.append([str(xv),cv,str(z)])
   assert witnesses,('no nonzero witness',a[':answer/value'])
 for i in range(5):
  for j in range(i):assert sp.simplify(values[i]-values[j])!=0,'duplicate mathematical option'
 text=q[':question/problem'];sol=q[':question/worked-solution']
 for t in (text,sol):assert t.count('$')%2==0 and t.count('{')==t.count('}')
 assert '\\te(' not in text+sol
 assert 'with respect to $x:$' in sol
 # Every concrete coefficient, solution, and key is rendered from one translation.
 template=r['generation']['template'];h=r['generation']['parameters']['shift'];source=g.SOURCES[template]
 source_solution=source[':question/worked-solution']
 if h:source_solution=source_solution.replace('(1/4x)',r'(\frac{1}{4x})').replace('(3/2x)',r'(\frac{3}{2x})')
 prefix=g.translate(source_solution,h)
 assert sol.startswith(prefix)
 if h:
  assert f'(x{h:+d})' in text and f'(x{h:+d})' in sol
  assert '{{selection}}' not in text and 'general nonzero real solution' in text
  # Reverse the algebraic translation to check all source instructional stages.
  restored=prefix.replace(f'(x{h:+d})','x');assert restored.replace(r'\cdot ','')==source_solution.replace(r'\cdot ','')
 return {'n':str(n),'linear_p':str(p),'nonlinear_q':str(coef),'correct_residual':'0'}
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete radio bank through learner grade_field'} for a in f[':answer-field/choices']]
def main():
 records=[];replay=[];coverage={};fingerprints=set()
 for t,source in g.SOURCES.items():
  level=source[':question/difficulty'][':db/ident'].split('/')[-1]
  r=g.generate(level,template=t,parameters={'shift':0});independent(r)
  q=r['question'];f=q[':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
  assert q[':question/problem']==source[':question/problem'] and q[':question/worked-solution']==source[':question/worked-solution']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
  replay.append({'source':t,'bank_values':'5/5','distractors':'4/4','correct_designation':True,'prompt_solution_exact':True});records.append(r)
  coverage[t]=[];print('Validating',t,flush=True)
  if t=='q-109029':continue
  for h in g.SHIFTS:
   r=g.generate(level,template=t,parameters={'shift':h});independent(r);records.append(r);coverage[t].append(h)
   fp=g.fingerprint(r['question']);assert fp not in fingerprints;fingerprints.add(fp)
   assert g.generate(level,seed=999,template=t,parameters={'shift':h})['question']==r['question']
 # Catch a stale key and a stale target in a concrete changed-shift case.
 import copy
 a=g.generate('hard',template='q-109172',parameters={'shift':1});b=g.generate('hard',template='q-109172',parameters={'shift':2});assert g.fingerprint(a['question'])!=g.fingerprint(b['question'])
 bad=copy.deepcopy(b);bad['question'][':question/answer-fields'][0][':answer-field/choices']=a['question'][':question/answer-fields'][0][':answer-field/choices'];bad['question'][':question/answer-fields'][0][':answer-field/correct']=a['question'][':question/answer-fields'][0][':answer-field/correct']
 try:independent(bad)
 except AssertionError:pass
 else:raise AssertionError('stale target/key not detected')
 save(HERE/'engine-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records])
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 review=[g.generate(l,template=t,parameters={'shift':h}) for l,t,h in [('moderate','q-106073',1),('moderate','q-109154',-3),('hard','q-109172',1),('hard','q-109172',2),('hard','q-109170',-2)]]
 save(HERE/'review.json',review);(HERE/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in review))
 save(HERE/'validation.json',{'status':'pass','generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_basis':g.SNAPSHOT['basis'],'source_replays':replay,'complete_banks':'10/10','source_distractors':'40/40','source_values':'50/50','mathematically_verified_variants':len(fingerprints),'slot_coverage':coverage,'deterministic_replay':True,'changed_target_stale_key_caught':True,'native':json.loads((HERE/'engine-report.json').read_text()),'dependencies':{'sympy':sp.__version__,'antlr4':'4.11.1','antlr4_path':'/tmp/ca-bernoulli-validation'},'exclusions':['q-106074 missing key/solution/difficulty; preserved','q-109029 autonomous translations do not create new tasks','easy unsupported']})
 print('Validated complete source banks and',len(fingerprints),'distinct changed ODEs.')
if __name__=='__main__':main()
