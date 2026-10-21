"""Independent audit; run with PYTHONDONTWRITEBYTECODE=1 job-python -B review.py."""
import sys
sys.dont_write_bytecode=True
import json,pathlib,hashlib,subprocess,shutil,random,re,collections,itertools,platform
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent; PKG=JOB/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(name,x): (ROOT/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def hashes(): return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}
save('package-before.json',hashes())
sys.path.insert(0,str(PKG));import generator as G
V={v:S.Symbol(v,positive=True) for v in ('x','y','t')};V['C']=S.Symbol('C')
TRANS=standard_transformations+(implicit_multiplication_application,)
def tex(src):
 text=src.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\!','').strip().rstrip('.')
 pos=0
 def group():
  nonlocal pos
  while pos<len(text) and text[pos].isspace():pos+=1
  if text[pos]=='{':pos+=1;return walk('}')
  c=text[pos];pos+=1;return c
 def walk(stop=None):
  nonlocal pos
  out=''
  while pos<len(text):
   if stop and text[pos]==stop:pos+=1;return out
   if text.startswith(r'\frac',pos) or text.startswith(r'\dfrac',pos):
    pos+=5 if text.startswith(r'\frac',pos) else 6
    a=group();b=group();out+=f'(({a})/({b}))'
   elif text.startswith(r'\sqrt',pos):
    pos+=5;d='2'
    if text[pos]=='[':end=text.index(']',pos);d=text[pos+1:end];pos=end+1
    a=group();out+=f'(({a})**(1/({d})))'
   elif text[pos]=='{':out+='('+group()+')'
   elif text[pos]=='^':pos+=1;out+='**'+('('+group()+')')
   else:out+=text[pos];pos+=1
  assert stop is None,(text,stop)
  return out
 return parse_expr(walk(),local_dict=V,transformations=TRANS)
def equal(a,b):return S.expand(S.powdenest(a-b,force=True))==0 or S.simplify(a-b)==0
def field(r):return r['question'][':question/answer-fields'][0]
def answer(r):
 f=field(r);return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def extract(r):
 p=r['question'][':question/problem']
 if "Given $y'(t)=" in p:return tex(re.search(r"Given \$y'\(t\)=(.*?)\$",p)[1]),'t'
 if 'Find the integral of $' in p:
  raw=re.search(r'of \$(.*?)\$',p)[1];return tex(raw),re.search(r'for \$([xyt])>0',p)[1]
 raw=re.search(r'\\left\((.*?)\\right\)',p)[1];v=re.search(r'\\mathrm\{d\}([xyt])',p)[1];return tex(raw),v

def verify(r):
 integrand,v=extract(r);x=V[v];f=field(r);values=[tex(a[':answer/value']) for a in f[':answer-field/choices']]
 qualifies=[equal(S.diff(a,x),integrand) for a in values]
 assert sum(qualifies)==1
 assert qualifies[next(j for j,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==answer(r)[':answer/id'])]
 assert len(set(map(str,values)))==len(values)
 sol=r['question'][':question/worked-solution'];rows=sol.split('&=')
 final=tex(rows[-1].split(r'\end')[0]);rule=tex(rows[-2].split(r'\\')[0])
 assert equal(S.diff(final,x),integrand) and equal(rule,final)
 assert equal(final,tex(answer(r)[':answer/value'])+(V['C'] if f[':answer-field/type'].endswith('/blank') else 0))
 if f[':answer-field/type'].endswith('/blank'):assert '+\\,C' in r['question'][':question/problem'] and not values[0].has(V['C'])
 else:assert len(values)==5 and all(a.has(V['C']) for a in values)
 return {'id':r['question'][':question/id'],'integrand':str(integrand),'correct':answer(r)[':answer/value'],'variable':v,'passes':True}

seeds=[20261020,9817301,458729]
raw=sum([G.generate(count=240,seed=s) for s in seeds],[])
save('samples.json',raw)
batch=json.loads((JOB/'samples.json').read_text());save('runner-batch.json',batch)
bounds=[]
for profile in ('P','R','B'):
 for n,s,k,order in itertools.product(((3,7) if profile=='R' else (2,6)),(-1,1),(-6,-1,1,6),(False,True)):
  bounds.append(G.build(G.instance(profile,n,s,k,'t' if profile=='B' else 'x',order),random.Random(109+n+k+s)))
save('boundaries.json',bounds)
base=G.instance('P',3,-1,5,'x',True,offset=-2,factors=('1/3','3'),omitted_row=0,omitted_col=2)
pairs=[];cf=[]
for label,delta,kind in [('exponent',{'n':5},'relevant'),('constant',{'k':-4},'relevant'),('sign',{'s':1},'relevant'),('term_order',{'constant_first':False},'irrelevant'),('variable',{'variable':'y'},'irrelevant')]:
 a=G.build(base,random.Random(776));b=G.build(dict(base,**delta),random.Random(776));j=len(cf);cf.extend([a,b]);pairs.append({'label':label,'kind':kind,'indices':[j,j+1],'parameters_before':base,'delta':delta})
b=G.instance('B',4,1,-3,'t',True)
for label,delta,kind in [('blank_exponent',{'n':6},'relevant'),('blank_term_order',{'constant_first':False},'irrelevant')]:
 j=len(cf);cf.extend([G.build(b),G.build(dict(b,**delta))]);pairs.append({'label':label,'kind':kind,'indices':[j,j+1],'parameters_before':b,'delta':delta})
save('counterfactual-records.json',cf)
math=[]
for group,records in [('sample',raw),('boundary',bounds),('runner',batch),('counterfactual',cf)]:
 for j,r in enumerate(records):math.append({'group':group,'index':j,**verify(r)})
save('math-results.json',{'records':math,'count':len(math),'method':'Parse actual prompt, choices, final and unsimplified power-rule row independently from text; differentiate each option, enforce unique key and equivalence of solution rows. Exact SymPy rational arithmetic.'})
for pair in pairs:
 a,b=[cf[j] for j in pair['indices']];av,bv=tex(answer(a)[':answer/value']),tex(answer(b)[':answer/value'])
 if pair['label']=='variable':av=av.subs(V['x'],V['y'])
 same=equal(av,bv);assert same==(pair['kind']=='irrelevant')
 pair.update({'before_answer':answer(a)[':answer/value'],'after_answer':answer(b)[':answer/value'],'response_relationship':'preserved under renaming' if pair['label']=='variable' else ('preserved' if same else 'changed'),'passes':True})
save('counterfactual-results.json',pairs)

# Compare against original material, never bundled source-data as authority.
source=json.loads((JOB/'source/source.json').read_text())['material']['kp'];orig={q[':question/math-academy-id']:q for q in source[':knowledge-point/questions']}
replay=G.replay_sources();save('source-replay.json',replay)
expected={'q-2159':('x',V['x']**S.Rational(1,2)-3),'q-29828':('x',V['x']**S.Rational(5,2)+V['x']**S.Rational(-5,2)),'q-113781':('x',V['x']**S.Rational(1,4)-V['x']**5),'q-71169':('x',V['x']**S.Rational(-3,2)+4),'q-71173':('y',2+V['y']**-5),'q-133291':('t',V['t']**2-2),'q-71167':('x',5-V['x']**3)}
fidelity=[];replay_real=[]
for r in replay:
 ref=r['generation']['source_refs'][0];o=orig[ref];v,f=expected[ref]
 if r.get('math_only'):
  assert r['original_problem']==o[':question/problem'] and r['original_solution']==o[':question/worked-solution']
  final=o[':question/worked-solution'].split('& =')[-1].split(r'\end')[0]
  assert equal(S.diff(tex(final),V[v]),f)
 else:
  of=o[':question/answer-fields'][0];rf=field(r)
  assert of[':answer-field/type'][':db/ident']==rf[':answer-field/type']
  assert [tex(a[':answer/value']) for a in of[':answer-field/choices']]==[tex(a[':answer/value']) for a in rf[':answer-field/choices']]
  assert equal(S.diff(tex(answer(r)[':answer/value']),V[v]),f)
  if ':answer-field/correct' in of:assert equal(tex(of[':answer-field/correct'][':answer/value']),tex(answer(r)[':answer/value']))
  prompt=r['question'][':question/problem'];assert o[':question/problem'] in prompt or re.sub(r'\s+','',o[':question/problem'])==re.sub(r'\s+','',prompt)
  if ':question/worked-solution' in o:assert re.sub(r'\s+','',o[':question/worked-solution'])==re.sub(r'\s+','',r['question'][':question/worked-solution'])
  replay_real.append(r)
 fidelity.append({'source':ref,'math_only':r.get('math_only',False),'choices':len(o.get(':question/answer-fields',[{}])[0].get(':answer-field/choices',[])),'passes':True})
# Independently exercise generalized source-bank parameter points and canonical example.
points=[G.instance('P',3,-1,5,bank='source'),G.instance('R',3,1,4,constant_first=False,bank='source'),G.instance('B',2,1,-2,'t',False),G.instance('P',2,1,1,bank='source')]
source_points=[G.build(i) for i in points];save('source-parameter-records.json',source_points)
for r in source_points:verify(r)
for r,ref in zip(source_points,('q-71167','q-71169','q-133291')):
 assert set(tex(a[':answer/value']) for a in field(r)[':answer-field/choices'])==set(tex(a[':answer/value']) for a in orig[ref][':question/answer-fields'][0][':answer-field/choices'])
save('source-replay-results.json',{'cases':fidelity,'complete_choices_replayed':21,'parameterized_banks':['q-71167','q-71169','q-133291'],'canonical_e371':'P n=2 s=1 k=1 independently checked','correction':'q-133291 restores missing derivative from source worked solution; two missing source keys independently derived','unsupported':'q-71173 and hard q-113781 are math-only: no captured response field; unlabelled q-2159/q-29828 replay-only. Normal generation excludes their families.','passes':True})

# Package CLI/runtime/relocation; retain all subprocess inputs, outputs and statuses.
manifest=json.loads((PKG/'package.json').read_text());runtime={'actual_python':platform.python_version(),'manifest':manifest,'commands':[]}
def run(args,cwd):
 p=subprocess.run(args,cwd=cwd,capture_output=True,text=True);runtime['commands'].append({'args':list(map(str,args)),'cwd':str(cwd),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p
args=[sys.executable,'-B','generator.py','--seed','720519','--count','8','--difficulty','moderate','--format','json']
p=run(args,PKG);p2=run(args,PKG);assert p.returncode==p2.returncode==0 and p.stdout==p2.stdout
rel=ROOT/'relocated';rel.mkdir(exist_ok=True)
for name in manifest['files']:shutil.copyfile(PKG/name,rel/name)
p3=run([sys.executable,'-I','-B',str(rel/'generator.py'),'--seed','720519','--count','8'],ROOT)
# -I forbids sibling imports; use ordinary isolated cwd invocation, the runtime contract.
p4=run([sys.executable,'-B',str(rel/'generator.py'),'--seed','720519','--count','8'],ROOT)
assert p4.returncode==0 and json.loads(p4.stdout)==json.loads(p.stdout)
for extra in [['--count','0'],['--count','-1'],['--difficulty','easy'],['--difficulty','hard']]:
 q=run([sys.executable,'-B',str(rel/'generator.py')]+extra,ROOT);assert q.returncode==(0 if extra==['--count','0'] else 2)
runtime['isolated_flag_note']='Python -I removes sibling import path and is not the declared CLI contract; ordinary relocated CLI works.'
runtime['dependencies_exact']=manifest['dependencies']=={'python':platform.python_version(),'packages':{}}
assert runtime['dependencies_exact'];runtime['package_unchanged']=hashes()==json.loads((ROOT/'package-before.json').read_text());assert runtime['package_unchanged']
save('packaging-results.json',runtime)

# Native grader input: all boundary/CF records, runner batch, replay banks, and random representatives.
cases=[]
for label,rs in [('boundary',bounds),('counterfactual',cf),('runner',batch),('source',replay_real),('random',raw[:12])]:
 for j,r in enumerate(rs):
  f=field(r);checks=[]
  if f[':answer-field/type'].endswith('/blank'):
   val=tex(answer(r)[':answer/value']);x=V['t']
   for expr,purpose in [(val,'independent expanded equivalent'),(S.factor(val),'factored equivalent'),(val+x,'wrong linear term'),(S.diff(val,x),'copied derivative')]:
    checks.append({'submitted':str(expr).replace('**','^'),'expected':'accepted' if equal(expr,val) else 'rejected','purpose':purpose})
  else:
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==answer(r)[':answer/id'] else 'rejected','purpose':'independently differentiated complete choice bank'} for a in f[':answer-field/choices']]
  cases.append({'label':f'{label} {j}','record':r,'checks':checks})
# Explicit relevant cross-answers rejected and irrelevant equivalent answers accepted for blank pairs.
for pair in pairs:
 if not pair['label'].startswith('blank'):continue
 a,b=[cf[j] for j in pair['indices']]
 cases.append({'label':'cross '+pair['label'],'record':b,'checks':[{'submitted':str(tex(answer(a)[':answer/value'])).replace('**','^'),'expected':'rejected' if pair['kind']=='relevant' else 'accepted','purpose':'counterfactual prior response'}]})
save('grader-input.json',cases)
# CF records must all be visually examined; representative source and boundary forms also rendered.
render=cf+source_points[:3]+[bounds[32],bounds[47]]+batch
save('render-records.json',render)
(ROOT/'session-state.md').write_text('Independent source account saved. Completed 835 prompt/bank/solution exact checks (see math-results.json for authoritative count), source replay and package CLI/relocation checks. Native grader, delivery, actual UI render and shortcut/selection measurements pending. Run review.py with job Python -B to reproduce.\n')
print(json.dumps({'math_records':len(math),'samples':len(raw),'boundary':len(bounds),'counterfactual':len(cf),'grader_records':len(cases),'render_records':len(render),'package_unchanged':runtime['package_unchanged']}))
