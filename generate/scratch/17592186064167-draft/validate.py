"""Independent displayed operand, primitive-family, full-bank and native checks. No DB."""
import sys;sys.dont_write_bytecode=True
import importlib.util,json,hashlib,re,itertools,subprocess,copy
from pathlib import Path
from functools import lru_cache
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2];SCRIPT=D.with_suffix('.py')
spec=importlib.util.spec_from_file_location('draft_monomial',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,C=sp.symbols('x C',real=True);TRANS=standard_transformations+(implicit_multiplication_application,)
DER=r'\frac{\text{d}}{\text{d}x}'
def group(s,start):
 assert s[start]=='{';depth=1;i=start+1
 while depth:
  assert i<len(s);depth+=(s[i]=='{')-(s[i]=='}');i+=1
 return s[start+1:i-1],i

@lru_cache(maxsize=None)
def expr(s):
 s=s.strip().rstrip('.').replace(r'\,','').replace('✓','').replace(r'\cdot','*').replace('{x}','x').replace(r'\dfrac',r'\frac')
 while r'\frac' in s:
  i=s.index(r'\frac');a,j=group(s,i+5);b,j=group(s,j);s=s[:i]+'(('+str(expr(a))+')/('+str(expr(b))+'))'+s[j:]
 s=re.sub(r'\^\{([^{}]+)\}',r'**(\1)',s).replace('^','**').replace('{','(').replace('}',')')
 assert '\\' not in s,s
 return parse_expr(s,local_dict={'x':x,'C':C},transformations=TRANS)
@lru_cache(maxsize=None)
def value(s):
 s=s.strip().rstrip('.')
 while DER in s:
  i=s.index(DER);j=i+len(DER);assert s[j]=='(';a=j+1;depth=1;j+=1
  while depth:depth+=(s[j]=='(')-(s[j]==')');j+=1
  v=sp.diff(expr(s[a:j-1]),x);s=s[:i]+'('+str(v)+')'+s[j:]
 return expr(s)
@lru_cache(maxsize=None)
def same(a,b):return sp.expand(a-b)==0
@lru_cache(maxsize=None)
def family(a,b):return bool(sp.diff(a,C)!=0)==bool(sp.diff(b,C)!=0) and same(sp.diff(a-b,x),0)
def exponent(prompt):
 if r'\intxdx' in prompt:return 1
 if r'\int 1' in prompt:return 0
 m=re.search(r'(?:\{x\}|x)\^(?:\{(\d+)\}|(\d+))',prompt);assert m,prompt
 return int(m[1] or m[2])
def plain(q):
 q=copy.deepcopy(q)
 for k in (':question/difficulty',):
  if isinstance(q.get(k),dict):q[k]=q[k][':db/ident']
 for f in q.get(':question/answer-fields',[]):
  if isinstance(f.get(':answer-field/type'),dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  if isinstance(f.get(':answer-field/correct'),dict):f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for a in f[':answer-field/choices']:
   if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
 return q
COUNTS={'equations':0,'options':0,'primitive_stages':0,'integral_operands':0,'derivative_rows':0}
def check(q,raw=False):
 n=exponent(q[':question/problem']);assert n in range(21);target=x**n;primitive=x**(n+1)/sp.Integer(n+1)+C
 if not raw:
  gmod=importlib.util.spec_from_file_location('format_check',D/'math_format.py');fmt=importlib.util.module_from_spec(gmod);gmod.loader.exec_module(fmt)
  fmt.validate_generated_record({'question':q})
  assert not re.search(r'\\int[a-zA-Z]',q[':question/problem'])
 # Every complete bank's values and supplied suffix are checked, independent of metadata.
 for f in q.get(':question/answer-fields',[]):
  vals=[expr(a[':answer/value']) for a in f[':answer-field/choices']];COUNTS['options']+=len(vals)
  assert len(vals)==(1 if f[':answer-field/type'].endswith('/blank') else 5)
  assert all(not family(a,b) for a,b in itertools.combinations(vals,2))
  eligible=[a for a,v in zip(f[':answer-field/choices'],vals) if family(v,primitive)]
  assert len(eligible)==1,(n,vals)
  if ':answer-field/correct' in f:assert eligible[0][':answer/id']==f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 sol=q.get(':question/worked-solution')
 if not sol:return
 # Read every integral operand and differential, including formal f/F' rows.
 integrals=re.findall(r'\\int (.*?)(?:\\,\\text\{d\}x| \\,\\textrm d x)',sol)
 assert len(integrals)==sol.count(r'\int'),('differential/operand missing',sol)
 for operand in integrals:
  if operand in ('f(x)',"{F}^{'}(x)",'{F}^{′}(x)'):pass
  else:assert same(expr(operand),target),('wrong integral operand',operand,n)
 COUNTS['integral_operands']+=len(integrals)
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==(3 if 'Remember that integration' in sol else 2)
 def rows(b):return b.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
 checkrows=rows(blocks[-1]);assert len(checkrows)==(4 if n==0 else 5)
 assert [r.count(DER) for r in checkrows]==([1,2,0,0] if n==0 else [1,2,1,0,0])
 for row in checkrows:
  assert row.count('& =')==(0 if row==checkrows[-1] else 1)
  assert same(value(row.replace('& =','')),target),('derivative row',row,n)
  COUNTS['derivative_rows']+=1
 # Derivative primitive operands must individually be the requested family.
 first=checkrows[0].replace('& =','').strip();assert first.startswith(DER+'(')
 assert family(expr(first[len(DER)+1:first.rfind(')')]),primitive)
 # Formal primitive sequence includes unsimplified successor and full +C at every stage.
 formal=blocks[-2]
 if n==0:
  stages=rows(formal);assert len(stages)==3
  assert stages[0]==r'\int 1\,\text{d}x & =\int {x}^{0}\,\text{d}x'
  targets=[s.replace(' & =','') for s in stages[1:]]
 elif 'Remember that integration' in sol:
  intro=rows(blocks[0]);prime='′' if '{F}^{′}' in sol else "'"
  assert intro==["{F}^{"+prime+"}(x) & =f(x)",r'\int {F}^{'+prime+r'}(x)\,\text{d}x & =\int f(x)\,\text{d}x',r'F(x) & =\int f(x)\,\text{d}x.']
  stages=rows(formal);assert len(stages)==4;assert stages[0]==r'F(x) & =\int f(x)\,\text{d}x'
  targets=[s.replace(' & =','') for s in stages[2:]]
 else:
  stages=formal.split('=');assert len(stages)==3;targets=stages[1:]
 for t in targets:
  assert family(expr(t),primitive) and sp.diff(expr(t),C)!=0,('primitive',t)
  COUNTS['primitive_stages']+=1
 formalnormalized=formal.replace(r'\dfrac',r'\frac').replace(' + C','+C')
 assert (r'\frac{{x}^{'+str(n)+r'+1}}{'+str(n)+r'+1}+C' in formalnormalized or r'\frac{x^{'+str(n)+r'+1}}{'+str(n)+r'+1}+C' in formalnormalized)
 assert '$n='+str(n)+'$' in sol or n==0
 assert "Let's check by differentiating:" in sol
 COUNTS['equations']+=len(checkrows)+len(targets)
def jwrite(name,obj):(D/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def main():
 sources=json.loads((D/'source-cases.json').read_text());source=json.loads((D/'source.json').read_text());canonical=source['record'][':knowledge-point/canonical-example'];findings=[];review=[]
 for case in sources+[{'source_id':'e-364','record':canonical}]:
  sid=case['source_id'];q=plain(case['record']);check(q,True);t,n=g.SOURCE_SPECS[sid];r=g.generate('easy',template=t,parameters={'n':n},profile='raw:'+sid);rq=r['question'];check(rq,True)
  for key in [':question/problem',':question/worked-solution',':question/difficulty']:
   assert q.get(key)==rq.get(key),(sid,key,q.get(key),rq.get(key))
   assert (key in q)==(key in rq)
  assert len(q.get(':question/answer-fields',[]))==len(rq.get(':question/answer-fields',[]))
  for f,rf in zip(q.get(':question/answer-fields',[]),rq.get(':question/answer-fields',[])):
   assert f[':answer-field/key']==rf[':answer-field/key'];assert f[':answer-field/type']==rf[':answer-field/type']
   av=f[':answer-field/choices'];bv=rf[':answer-field/choices'];assert sorted(a[':answer/value'] for a in av)==sorted(a[':answer/value'] for a in bv)
   assert all(sum(family(expr(a[':answer/value']),expr(b[':answer/value'])) for b in bv)==1 for a in av)
   assert (':answer-field/correct' in f)==(':answer-field/correct' in rf)
   if ':answer-field/correct' in f:
    cv=next(a[':answer/value'] for a in av if a[':answer/id']==f[':answer-field/correct'][1]);rv=next(a[':answer/value'] for a in bv if a[':answer/id']==rf[':answer-field/correct'][1]);assert family(expr(cv),expr(rv))
  findings.append({'source_id':sid,'prompt_exact':True,'present_solution_exact':':question/worked-solution' in q,'missing_attribute_parity':True,'complete_bank_choices':sum(len(f[':answer-field/choices']) for f in q.get(':question/answer-fields',[])),'captured_key':any(':answer-field/correct' in f for f in q.get(':question/answer-fields',[]))});review.append({'label':'Original raw '+sid,'record':r})
  if sid!='e-364':
   for newn in ([0] if n==0 else [5,7]):
    profile={'q-113665':'observed_113665','q-2005':'observed_2005','q-2022':'observed_2022','q-113668':'observed_113668','q-29994':'observed_29994'}.get(sid)
    nr=g.generate('easy',template=t,parameters={'n':newn},profile=profile);check(nr['question']);review.append({'label':'Normal authored completion/changed exponent','record':nr})
 # Previously generated inventory is validated independently, never added to source template counts.
 inventory=json.loads((D/'independent-inventory.json').read_text())
 for item in inventory['questions']:check(plain(item['record']))
 # Preserve every valid previous normal review instance, including question/field/answer IDs and prose.
 previous=json.loads((ROOT/'generate/scratch/17592186064167/review.json').read_text());preserved=0
 for item in previous:
  old=item['record'];p=old['generation']
  if p['evidence_only']:continue
  r=g.generate('easy',seed=p['seed'],template=p['template'],parameters=p['parameters'],profile=p['bank_profile'])
  assert r['question']==old['question'];preserved+=1
 all_records=[];variation={}
 for level in g.DOMAINS:
  seen=set();profilecounts={};ns=set()
  for n in range(21):
   templates=['constant'] if n==0 else [t for t in g.TEMPLATES if t not in ('constant','canonical_power')]
   for t in templates:
    for kind in (['blank'] if n==0 else ['blank','radio']):
     profiles=[None] if kind=='blank' else ['authored_power','observed_2005']+(['observed_2022','observed_113668','observed_29994','observed_113665'] if n>=2 else [])
     for profile in profiles:
      r=g.generate(level,seed=11,template=t,field_type=kind,parameters={'n':n},profile=profile);check(r['question']);all_records.append(r);seen.add(r['generation']['mathematical_fingerprint']);ns.add(n);profilecounts[profile or 'blank']=profilecounts.get(profile or 'blank',0)+1
      r2=g.generate(level,seed=22,template=t,field_type=kind,parameters={'n':n},profile=profile);assert r2['question'][':question/id']==r['question'][':question/id'];assert r2['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
  variation[level]={'exponents':sorted(ns),'distinct_mathematical_tasks':len(seen),'coefficient_role':'fixed unit coefficient; next topic owns constant multiple rule','profiles':profilecounts,'calibration':'observed easy' if level=='easy' else 'authored uncalibrated same-method label; no progression'}
 # Negative controls corrupt individual displayed stages while retaining the final key.
 probe=g.generate_easy(template='function',parameters={'n':4});negatives=[]
 changes=[(r'\int {x}^{4}\,\text{d}x',r'\int {x}^{3}\,\text{d}x'),(r'\frac{{x}^{4+1}}{4+1}+C',r'\frac{{x}^{4+1}}{4+2}+C'),(r'\frac{1}{5}\cdot 5\,{x}^{4}',r'\frac{1}{5}\cdot 5\,{x}^{3}'),(r'\text{d}x',r'\text{d}y'),(r'\frac{{x}^{4+1}}{4+1}+C',r'\frac{{x}^{4+1}}{4+1}'),(r'\int f(x)',r'\int F(x)')]
 for a,b in changes:
  q=copy.deepcopy(probe['question']);assert a in q[':question/worked-solution'];q[':question/worked-solution']=q[':question/worked-solution'].replace(a,b,1)
  try:check(q)
  except AssertionError:negatives.append({'from':a,'to':b,'final_key_unchanged':True,'caught':True})
  else:raise AssertionError(('missed mutation',a))
 for badseed in [True,1.0,'1',None]:
  try:g.generate_easy(seed=badseed)
  except ValueError:pass
  else:raise AssertionError('seed guard')
 for n in [-1,21,True,1.5,'4']:
  try:g.generate_easy(parameters={'n':n})
  except ValueError:pass
  else:raise AssertionError('parameter guard')
 # Native actual learner grader. Full radio choices, blank exact/equivalent/wrong and known C-family gap.
 native=[];seen=set()
 for r in all_records:
  gg=r['generation'];f=r['question'][':question/answer-fields'][0];key=(r['question'][':question/difficulty'],gg['template'],gg['bank_profile'],f[':answer-field/type'])
  if key in seen:continue
  seen.add(key);n=gg['parameters']['n'];cid=f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'independently checked complete bank option selection'} for a in f[':answer-field/choices']]
  else:
   checks=[{'submitted':f[':answer-field/choices'][0][':answer/value'],'expected':'accepted','purpose':'exact'}, {'submitted':f'x^({n}+1)/({n}+1)+C','expected':'accepted','purpose':'genuine equivalent unsimplified successor'}, {'submitted':f'x^({n}+2)/({n}+2)+C','expected':'rejected','purpose':'wrong exponent'}, {'submitted':f'x^({n}+1)/({n}+1)+2C','expected':'rejected','purpose':'qualified actual grader gap: mathematically equivalent arbitrary-C family is rejected'}]
  native.append({'label':str(key),'record':r,'checks':checks})
 jwrite('native-input.json',native)
 binary=ROOT/'generate/scratch/17592186059716-draft/check-engine';manifest=json.loads((binary.parent/'reference/grader-build.json').read_text())
 assert hashlib.sha256(binary.read_bytes()).hexdigest()==manifest['binary_sha256']
 for name,sha in manifest['engine_sources'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,('engine changed',name)
 jwrite('reference/grader-build.json',manifest)
 subprocess.run([str(binary),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 # CLI all produces 3 records; count refusal is finite, strict command integer parsing.
 for form in ['json','markdown']:
  p=subprocess.run([sys.executable,str(SCRIPT),'--difficulty','all','--count','1','--format',form],capture_output=True,text=True,check=True)
  if form=='json':assert len(json.loads(p.stdout))==3
  else:assert p.stdout.count('## Generated')==3
  (D/('cli-all.'+('json' if form=='json' else 'md'))).write_text(p.stdout)
 samples=[g.generate(level,seed=0) for level in g.DOMAINS];jwrite('samples.json',samples);jwrite('review.json',review);jwrite('source-findings.json',findings)
 (D/'review.md').write_text('\n\n---\n\n'.join(g.markdown(i['record'],i['label']) for i in review))
 before=json.loads((D/'registered-before.json').read_text());paths=[ROOT/p for p in before['pathset']];now={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};assert now==before['sha256']
 actual=[ROOT/'generate/scratch/17592186064167.py']+list((ROOT/'generate/scratch/17592186064167').rglob('*'))+list((ROOT/'generate/scratch/__pycache__').glob('17592186064167.*.pyc'));assert sorted(str(p.relative_to(ROOT)) for p in actual if p.is_file())==sorted(before['pathset'])
 report={'status':'ready for root independent QA; approval pending','source_basis':2275,'source_counts':{'MA_practice':len(sources),'canonical':1,'independent_inventory':len(inventory['questions']),'MA_complete_banks':5,'MA_choices':25,'MA_distractors':20,'captured_MA_keys':3},'source_fidelity':findings,'all_captured_worked_solutions_full_operands_checked':True,'full_finite_normal_instances':len(all_records),'parsed_math':COUNTS,'variation':variation,'negative_controls':negatives,'preserved_previous_normal_review_instances':preserved,'registered_pathset_and_sha_unchanged':True,'generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'native':json.loads((D/'native-report.json').read_text()),'limitations':['Moderate/hard are authored uncalibrated same-method labels, not calibrated workload progression.','Unit coefficient fixed by scope; only nonnegative integer exponent varies meaningfully. 21 mathematical tasks across aliases/fields/profiles/levels.','Two original radios lack keys/solutions; three original easy records and canonical lack answer fields. Raw remains evidence-only.','Arbitrary-C family equivalence is a documented native blank grading gap; retained with exact native result. No filtering or engine edits.']}
 jwrite('validation.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ['native','source_fidelity','variation']},indent=2))
if __name__=='__main__':main()
