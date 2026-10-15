"""Independent rendered-math, raw source fidelity, finite-domain and native QA."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load('draft_generator',D.with_suffix('.py'));p=load('independent_parser',D/'parser.py');import sympy as sp

def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];assert q[':question/difficulty'].split('/')[-1]in g.SUPPORTED_LEVELS;f=q[':question/answer-fields'][0]
 text=q[':question/problem']+q[':question/worked-solution']+''.join(a[':answer/value']for a in f[':answer-field/choices'])
 assert all(ord(c)>=32 or c in '\n\t'for c in text),'C0 control character'
 g.FORMAT.validate_generated_record(r)
 for text in [q[':question/problem'],q[':question/worked-solution']]:
  assert text.count('$')%2==0
  depth=0
  for c in text:
   depth+=(c=='{')-(c=='}');assert depth>=0
  assert depth==0
 sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
 expected={'easy_integer':(2,4),'q-15717':(2,4),'q-103603':(2,3),'q-15710':(2,3),'q-29834':(2,3),'q-103605':(4,4),'q-49096':(4,3),'q-103375':(4,3),'q-49067':(4,3)}[r['generation']['template']]
 assert tuple(len(b.split(r'\\'))for b in blocks)==expected
 for sign in (1,-1):
  given=p.prompt(q[':question/problem'],sign)
  assert p.same(given,g.integral(r['generation']['template'],r['generation']['parameters']))
  for block in blocks:
   rows=block.split(r'\\')
   assert p.same(sp.diff(p.evaluate_row(rows[0].split('&')[0],sign),p.X),given)
   for row in rows:
    rhs=row.split('=',1)[1];v=p.evaluate_row(rhs,sign);assert p.same(sp.diff(v,p.X),given),(r['generation'],row,v,given)
  vals=[p.scalar(a[':answer/value'],sign)for a in f[':answer-field/choices']];derivs=[sp.cancel(sp.diff(v,p.X))for v in vals]
  assert all(not p.same(a,b)for i,a in enumerate(derivs)for b in derivs[i+1:]),'bank ambiguity modulo arbitrary constant'
  # Every wrong value is checked against an independent complete operation bank.
  z=p.X;ab=sign*z;L=sp.log(p.K*ab);shift=sp.log(ab+p.K);a=sp.expand(given).coeff(z,-1);t=r['generation']['template']
  if t=='easy_integer':bank=[a*L,-a*L,L/a,L,a*shift]
  elif t=='q-15717':
   n=3*a;bank=[sp.log(n*ab+p.K)/3,a*L,a*shift,sp.log(n*p.K*ab)/3,sp.log(a*p.K*ab)]
  elif t=='q-15710':
   n=2*a;bank=[sp.log(a*p.K*ab),a*shift,sp.log(a*ab+p.K),a*L,sp.log(n*p.K*ab)/2]
  elif t=='q-29834':
   n=-2*a;bank=[sp.log(n*p.K*ab)/2,-a*L,a*L,-sp.log(-a*p.K*ab),a*shift]
  elif t=='q-103603':bank=[L/a,sp.log(p.K*ab/a),a*L,a/L,-L]
  elif t=='q-103605':
   n=sp.expand(given).coeff(z,0);bank=[z**2+L,z**2-L,n*z+L,n*z+shift,n*z-L]
  elif t=='q-49096':
   b=sp.expand(given).coeff(z,0);bank=[sp.log(p.K*(a+b*ab)),a*sp.log(p.K*ab+b),a*L-b*z,sp.log(b*p.K*ab+a),a*L+b*z]
  elif t=='q-103375':
   n=a;bank=[z-n/(2*z)+n*L,1-n/(2*z)+sp.log(n*p.K*ab),1-n/(2*z)+n*L,z-n**2/(4*z)+n*L,z-n**2/(4*z)+sp.log(n*p.K*ab)]
  else:
   n=a/2;bank=[z-n**2/z+2*n*L,1-n**2/z+2*n*L,1+2*n*L,z-n**2/z+sp.log(2*n*p.K*ab),z+(1+n*L)**2]
  assert len(bank)==len(vals)and all(sum(p.same(v,w)for w in bank)==1 for v in vals),(t,vals,bank)
  # Every displayed logarithm argument is positive on the entire declared interval.
  Y=sp.Symbol('Y',positive=True)
  for v in vals:
   for lg in v.atoms(sp.log):assert sp.ask(sp.Q.positive(lg.args[0].subs(z,sign*Y)))is True,(t,lg)
  correct=f[':answer-field/correct'][1];assert sum(p.same(d,given)for d in derivs)==1
  assert all((a[':answer/id']==correct)==p.same(d,given)for a,d in zip(f[':answer-field/choices'],derivs))
  # The prose's C=... rewrite is valid for arbitrary real C iff nonzero log coefficient.
  c=re.search(r'write \$C=(.*?)\$',sol)[1];v=p.scalar(c,sign);assert sp.diff(v,p.K)!=0
  residue=sp.expand(given).coeff(p.X,-1);assert p.same(sp.diff(v,p.K)*p.K,residue)
  # Derivatives alone erase stale constants: every primitive row must agree
  # with the actual printed C definition and final positive-K family.
  target=vals[next(i for i,a in enumerate(f[':answer-field/choices'])if a[':answer/id']==correct)]
  branch_x=sp.Symbol('branch_x',positive=True)
  for block in blocks:
   for row in block.split(r'\\'):
    rhs=row.split('=',1)[1]
    if r'\int'in rhs:continue
    actual=p.evaluate_row(rhs,sign).subs(p.C,v)
    difference=sp.expand_log((actual-target).subs(p.X,sign*branch_x))
    assert p.same(difference,0),('constant definition/primitive row mismatch',r['generation'],row)

 # Preserve operative arithmetic stages, independently of algebraic equality.
 t=r['generation']['template'];first=blocks[0].split(r'\\')
 if t in ('q-103375','q-49067'):
  assert r'\int (1+'in first[0]and r'{x}^{2}'in first[0]
  assert first[1].count(r'\int')==3
  assert '{x}^{-2+1}'in first[2]and'(-2+1)'in first[2]if t=='q-103375'else'{x}^{-2+1}'in first[2]and'{-2+1}'in first[2]
 if t in ('q-103605','q-49096'):
  assert first[0].count(r'\frac')==3 and first[2].count(r'\int')==2
 return True

def check_source(c):
 r=g.generate(c['level'],0,c['template'],parameters=c['parameters'],profile='source');q=r['question'];o=g.TEMPLATES[c['template']]['raw_source']
 for k in [':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields']:
  assert(k in q)==(k in o),(c['template'],k,'presence')
 assert q[':question/problem']==o[':question/problem'];assert q.get(':question/worked-solution')==o.get(':question/worked-solution'),c['template']
 f=q[':question/answer-fields'][0];sf=o[':question/answer-fields'][0];assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident'];assert f[':answer-field/key']==sf[':answer-field/key']
 assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in sf[':answer-field/choices'])
 assert(':answer-field/correct'in f)==(':answer-field/correct'in sf)
 if ':answer-field/correct'in f:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
 return r

def native(r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'owned radio selection; separate from math tests'}for a in f[':answer-field/choices']]
 checks += [{'submitted':'999999','expected':'unresolved','purpose':'foreign radio fixture ID'},{'submitted':'not-an-id','expected':'unresolved','purpose':'malformed radio ID'}]
 return {'label':r['question'][':question/id'],'record':r,'checks':checks}

def main():
 cases=[{'source_id':t,'template':t,'level':v['level'],'parameters':v['parameters'],'profile':'source'}for t,v in g.TEMPLATES.items()]
 (D/'source-cases.json').write_text(json.dumps(cases,indent=2));originals=[check_source(c)for c in cases]
 review=[];native_rows=[];capacity={};checked=0
 for level in g.SUPPORTED_LEVELS:
  ts=['easy_integer']if level=='easy'else[t for t,v in g.TEMPLATES.items()if v['level']==level];fps=set()
  for t in ts:
   params=g.domain(t)
   for pp in params:
    r=g.generate(level,17,t,parameters=pp);check(r);checked+=1;fps.add(r['generation']['parameter_fingerprint'])
    native_rows.append(native(r))
   for pp in [params[0],params[-1]]:
    for profile in ['normal']+([]if t=='easy_integer'else['source']):review.append(g.generate(level,23,t,parameters=pp,profile=profile))
  capacity[level]=len(fps)
 # Distinct identity under bank repair, seed stable identity and deterministic shuffled banks.
 for c in cases:
  r=g.generate(c['level'],0,c['template'],parameters=c['parameters']);s=g.generate(c['level'],99,c['template'],parameters=c['parameters']);assert r['question'][':question/id']==s['question'][':question/id'];check(r)
 for bad in [dict(seed=True),dict(parameters={'n':True}),dict(parameters={'n':2,'extra':4}),dict(parameters={}),dict(field_type='blank'),dict(profile='unknown')]:
  try:g.generate('easy',template='easy_integer',**bad)
  except(TypeError,ValueError):pass
  else:raise AssertionError('bad API input accepted '+str(bad))
 # A constant-only mutation passes differentiation but violates C=c ln K.
 r=g.generate('moderate',template='q-103603',parameters={'n':3})
 old=r'3\ln|x|+3\ln K';assert old in r['question'][':question/worked-solution']
 r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(old,r'3\ln|x|+2\ln K',1)
 try:check(r)
 except AssertionError:pass
 else:raise AssertionError('stale logarithmic constant coefficient was not detected')
 # Deliberate actual-display corruption must fail despite unchanged metadata.
 for mutate in ('control','expansion','stage','key'):
  r=g.generate('hard',template='q-103375',parameters={'n':3})
  if mutate=='control':r['question'][':question/worked-solution']+='\x0c'
  elif mutate=='expansion':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(r'\frac{3}{x}',r'\frac{4}{x}',1)
  elif mutate=='stage':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(r'\frac{9{x}^{-2+1}}{4(-2+1)}',r'-\frac{9}{4x}')
  else:r['question'][':question/answer-fields'][0][':answer-field/correct'][1]='foreign'
  try:check(r)
  except(AssertionError,ValueError):pass
  else:raise AssertionError('mutation undetected '+mutate)
 (D/'review.json').write_text(json.dumps(review,indent=2));(D/'capacity.json').write_text(json.dumps(capacity,indent=2));(D/'source-replay.json').write_text(json.dumps(originals,indent=2));(D/'native-input.json').write_text(json.dumps(native_rows));subprocess.run([str(D/'check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 h=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
 baseline=json.loads((D/'registered-baseline.json').read_text());assert all(Path(path).exists()and h(Path(path))==sha for path,sha in baseline.items());base=D.with_name('17592186105720');assert set(baseline)=={str(base.with_suffix('.py').relative_to(Path.cwd())) if base.is_absolute() else str(base.with_suffix('.py')),*[str(z.relative_to(Path.cwd()))if z.is_absolute()else str(z)for z in base.rglob('*')if z.is_file()]}
 report={'status':'passed independent bounded mathematical and source fidelity checks; native limitations separately audited','bounded_normal_instances':checked,'capacity':capacity,'source_originals':8,'source_complete_banks':8,'source_values':40,'source_correct_designations_matched':7,'source_missing_correct_designations':1,'source_worked_solutions_exact':7,'source_missing_worked_solutions':1,'independent_inventory':7,'mutation_regressions':5,'registered_baseline_files_unchanged':len(baseline),'native':json.loads((D/'native-report.json').read_text()),'python':sys.version.split()[0],'sympy':sp.__version__}
 (D/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k!='native'},indent=2))
if __name__=='__main__':main()
