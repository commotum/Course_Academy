"""Independent actual-displayed-math checks, raw F.check, memory-only native QA."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from functools import lru_cache
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'g');F=load(ROOT/'generate/runs/current/root-source-fidelity.py','F')
def save(n,o):(HERE/n).write_text(json.dumps(o,indent=2,default=str)+'\n')
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
@lru_cache(None)
def expr(t):
 # Separate actual displayed-token parser: recursive fraction/radical grammar,
 # not generator metadata or recipes. The captured grammar is algebraic only.
 t=t.strip().rstrip('.,').replace('{)}',')').replace(r'\,','').replace(r'\cdot','*').replace(r'\dfrac',r'\frac').replace(r'\left','').replace(r'\right','').replace('g(x)','g')
 def expr_text(text):
  # Run the same grammar recursively over an independent substring.
  out='';i=0
  def get_group(i):
   assert text[i]=='{';depth=1;j=i+1
   while depth:
    assert j<len(text)
    depth+=int(text[j]=='{')-int(text[j]=='}');j+=1
   return text[i+1:j-1],j
  while i<len(text):
   if text.startswith(r'\frac',i):
    i+=5;a,i=get_group(i);b,i=get_group(i);out+='(('+expr_text(a)+')/('+expr_text(b)+'))'
   elif text.startswith(r'\sqrt',i):
    i+=5;n='2'
    if text[i]=='[':j=text.index(']',i);n=text[i+1:j];i=j+1
    a,i=get_group(i);out+='(('+expr_text(a)+')**(1/('+n+')))'
   elif text[i]=='{':a,i=get_group(i);out+='('+expr_text(a)+')'
   elif text[i]=='^':out+='**';i+=1
   elif text[i]=='\\':raise AssertionError(('Unsupported displayed command',text[i:]))
   else:out+=text[i];i+=1
  return out
 converted=expr_text(t)
 return parse_expr(converted,local_dict={'x':g.x,'g':s.Symbol('g',positive=True)},transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)
@lru_cache(None)
def eq(a,b):
 # All radical families explicitly restrict their inner argument to positive.
 delta=s.powdenest(a,force=True)-s.powdenest(b,force=True)
 if delta==0:return True
 if delta.is_polynomial(g.x):return s.expand(delta)==0
 # x=4,5,6 satisfy every public positive-radicand domain here.
 if any(s.simplify(delta.subs(g.x,t))!=0 for t in (4,5,6)):return False
 return s.simplify(delta)==0
def displayed(rec):
 q=rec['question'];md=rec['generation'];m=md['template'];p=md['parameters'];raw=md['evidence_only']
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 assert md['dependencies']['python']==sys.version.split()[0] and md['dependencies']['sympy']==s.__version__
 inner,outer,fun,expected=g.model(m,p)
 prompt=q[':question/problem'];formula=next(t for t in re.findall(r'\$([^$]+)\$',prompt) if t.strip().startswith('f(x)'))
 df=expr(formula.split('=',1)[1].rstrip(','));assert eq(df,fun),(m,p,'printed function')
 derivative=s.diff(df,g.x);f=q[':question/answer-fields'][0]
 values=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
 if ':answer-field/correct' in f:
  answer=next(expr(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 else:
  assert raw and m in ('q-11414','q-48850');answer=next(v for v in values if eq(v,expected))
 assert eq(answer,expected),(m,p,'key')
 assert sum(eq(v,expected) for v in values)==1
 assert all(not eq(v,w) for i,v in enumerate(values) for w in values[i+1:]),(m,p,'ambiguous bank')
 # Reinsert into the actual printed answer fragment, not remembered metadata.
 if m=='q-342875':
  fragment=next(t for t in re.findall(r'\$([^$]+)\$',prompt) if '{{' not in t and t.startswith('{f}') and '=2(' in t)
  factor=expr(fragment.split('=',1)[1].removesuffix('('));assert eq(factor*answer,derivative)
 elif m=='q-342891':
  fragment=next(t for t in re.findall(r'\$([^$]+)\$',prompt) if '=\\frac' in t and not t.startswith('f(x)'))
  factor=expr(fragment.split('=',1)[1].removesuffix('('));assert eq(factor*answer,derivative)
 else:assert eq(answer,derivative)
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
  # Read both prose function definitions and every prime evaluation target.
  defs=re.findall(r'\$([^$]+)\$',sol.split('Differentiating')[0]);assert len(defs)==2
  assert defs[0].startswith('g(x)=') and eq(expr(defs[0].split('=',1)[1]),inner)
  assert defs[1].startswith('f(g(x))=')
  G=s.Symbol('g',positive=True);op=outer.subs(s.Symbol('g'),G)
  prose_outer=expr(defs[1].split('=',1)[1]);prose_outer=prose_outer.subs({v:G for v in prose_outer.free_symbols if v.name=='g'})
  # Legacy g(x) notation here means the already-defined inner value.
  if prose_outer.has(s.Function('g')):raise AssertionError('Unexpected function interpretation')
  assert eq(prose_outer,op),(m,'outer prose',prose_outer,op)
  rows=blocks[0].split(r'\\');assert len(rows)==2
  assert rows[0].startswith('{f}^{′}(g(x)) & =') and rows[1].strip().startswith('{g}^{′}(x) & =')
  for row,argument,deriv in ((rows[0],op,s.diff(op,G)),(rows[1],inner,s.diff(inner,g.x))):
   rhs=row.split(' & =',1)[1];parts=rhs.split('=');assert len(parts)>=2
   prim=parts[0].strip();assert prim.endswith('^{′}'),prim
   prim=prim[:-len('^{′}')].strip().replace('{)}',')')
   if prim.startswith('{(') and prim.endswith(')}'):prim=prim[1:-1]
   assert prim[0]=='(' and prim[-1]==')';prim=prim[1:-1]
   arg=expr(prim).subs({v:G for v in expr(prim).free_symbols if v.name=='g'});assert eq(arg,argument)
   for t in parts[1:]:
    val=expr(t).subs({v:G for v in expr(t).free_symbols if v.name=='g'});assert eq(val,deriv),(m,p,'formal derivative',t)
  rows=blocks[1].split(r'\\');assert len(rows)==3
  assert rows[0].strip()==r'{f}^{′}(x) & ={f}^{′}(g(x))\cdot {g}^{′}(x)'
  assert r'\cdot' in rows[1],'Required evaluated-factor multiplication stage absent'
  for row in rows[1:]:
   val=expr(row.split(' & =',1)[1]);val=val.subs({v:inner for v in val.free_symbols if v.name=='g'});assert eq(val,derivative),(m,p,'solution row',row,val,derivative)
  if not raw and m in g.SOURCES and ':question/worked-solution' in g.SOURCES[m]:assert sol==g.transform(g.SOURCES[m][':question/worked-solution'],m,p),'Exact normal common stage/prose fidelity'
 for text in [prompt]+([q[':question/worked-solution']] if ':question/worked-solution' in q else [])+[a[':answer/value'] for a in f[':answer-field/choices']]:
  assert text.count('$')%2==0 and text.count('{')==text.count('}')
  assert all(ord(c)>=32 or c in '\n\t' for c in text),'C0 control bytes'
 assert prompt.count('{{'+f[':answer-field/key']+'}}')==(1 if f[':answer-field/type'].endswith('/blank') else 0)
 assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(values)
 assert md['parameter_fingerprint']==g.task_fingerprint(m,p)
 # Replay catches identity, display-bank, target and feedback mutation too.
 assert rec==g.generate(md['level'],md['seed'],template=m,parameters=p,profile=md['profile'])
 return df

def checks(rec):
 f=rec['question'][':question/answer-fields'][0]
 if ':answer-field/correct' not in f:return []
 if f[':answer-field/type'].endswith('/radio'):return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual native ID grading of every complete bank option'} for a in f[':answer-field/choices']]
 a=f[':answer-field/choices'][0][':answer/value'];ex=expr(a);m=rec['generation']['template'];equiv=s.latex(s.factor(ex)) if m in ('q-342875','q-342891') else '2('+a+')/2'
 # Mathematical equivalent with unreduced product factors is actually different text.
 if equiv==a:equiv='2('+a+')/2'
 return [{'field_index':0,'submitted':v,'expected':e,'purpose':'Canonical, meaningful unreduced equivalent, incorrect fragment'} for v,e in ((a,'accepted'),(equiv,'accepted'),('0','rejected'),('('+a+')+1','rejected'))]
def failure(fn):
 try:fn()
 except (AssertionError,ValueError):return
 raise AssertionError('Negative/mutation test was accepted')

def main():
 cases=[{'source_id':m,'template':m,'level':g.LEVELS[m],'parameters':g.DEFAULTS[m],'profile':'raw-'+m,'authored_level':g.LEVELS[m] if m in ('q-11414','q-48850') else None} for m in g.SOURCES]
 save('source-cases.json',cases)
 originals,counts=F.check(g,str(g.KP_ID),HERE);assert len(originals)==9
 raw=[g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']) for c in cases]
 for r in raw:displayed(r)
 normal=[];review=[];tasks={};profile_domains={}
 for m in g.LEVELS:
  print('Checking finite family',m,flush=True)
  variants=[g.generate(g.LEVELS[m],template=m,parameters=p,seed=i) for i,p in enumerate(g.parameters_for(m))]
  for r in variants:displayed(r)
  normal+=variants;review+= [variants[0],variants[-2] if m=='authored-square' else variants[-1]]
  # Raw public profile changed boundary inputs preserve complete evidence stages.
  if m in g.SOURCES:
   for p in (g.parameters_for(m)[0],g.parameters_for(m)[-1]):
    r=g.generate(g.LEVELS[m],template=m,parameters=p,profile='raw-'+m);displayed(r);review.append(r)
 for l in g.SUPPORTED_LEVELS:
  print('Checking defaults',l,flush=True)
  tasks[l]=len({r['generation']['parameter_fingerprint'] for r in normal if r['generation']['level']==l})
  default=[g.generate(l,i) for i in range(80)]
  assert {r['generation']['template'] for r in default}=={m for m in g.LEVELS if g.LEVELS[m]==l}
  for r in default:displayed(r)
  profile_domains[l]=sorted({r['generation']['template'] for r in default})
 # Same parameters and banks remain stable under shuffling/alias spellings.
 for m in g.LEVELS:
  a=g.generate(g.LEVELS[m],0,template=m,parameters=g.DEFAULTS[m]);b=g.generate(g.LEVELS[m],91,template=m,parameters=g.DEFAULTS[m],profile='default')
  assert a['question'][':question/id']==b['question'][':question/id'] and a['generation']['content_identity']==b['generation']['content_identity']
  assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
  if m in g.SOURCES:
   rawr=g.generate(g.LEVELS[m],template=m,parameters=g.DEFAULTS[m],profile='raw-'+m)
   assert rawr['generation']['parameter_fingerprint']==a['generation']['parameter_fingerprint']
 positions=set()
 for i in range(30):
  r=g.generate('easy',i,parameters={'a':2,'b':1});f=r['question'][':question/answer-fields'][0];positions.add(next(j for j,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
 assert positions==set(range(5))
 negatives=0
 for m in g.LEVELS:
  p=g.DEFAULTS[m];wrong={k:99 for k in p};failure(lambda:g.generate(g.LEVELS[m],template=m,parameters=wrong));negatives+=1
  failure(lambda:g.generate(next(l for l in g.SUPPORTED_LEVELS if l!=g.LEVELS[m]),template=m));negatives+=1
 for args in [dict(level='easy',parameters={'a':1,'b':1}),dict(level='easy',parameters={'a':2,'b':0}),dict(level='moderate',template='q-71956',parameters={'b':0}),dict(level='hard',template='q-342891',parameters={'c':0}),dict(level='moderate',template='q-342804',field_type='radio')]:failure(lambda:g.generate(**args));negatives+=1
 # Mutations exercise actual math, prime targets, common stage and controls.
 base=g.generate('hard',template='q-342883',parameters={'b':-4})
 for name in ('prompt','outer','inner','target','stage','answer','control','domain','id'):
  r=copy.deepcopy(base);q=r['question']
  if name=='prompt':q[':question/problem']=q[':question/problem'].replace('5x-4','5x-3')
  if name=='outer':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\frac{1}{2\sqrt{g}}',r'\frac{2}{2\sqrt{g}}')
  if name=='inner':q[':question/worked-solution']=q[':question/worked-solution'].replace('^{′}=5.','^{′}=4.')
  if name=='target':q[':question/worked-solution']=q[':question/worked-solution'].replace('{f}^{′}(g(x))','{f}^{′}(x)')
  if name=='stage':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\frac{1}{2\sqrt{g}}\cdot 5',r'\frac{5}{2\sqrt{g}}')
  if name=='answer':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']=r'\frac{4}{2\sqrt{5x-4}}'
  if name=='control':q[':question/worked-solution']+='\x0c'
  if name=='domain':r['generation']['domain']['restriction']='all real x'
  if name=='id':q[':question/answer-fields'][0][':answer-field/correct'][1]=str(uuid.uuid4())
  try:failure(lambda:displayed(r))
  except StopIteration:pass
  negatives+=1
 cli=subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty','all','--count','2','--format','json'],capture_output=True,text=True,check=True);assert len(json.loads(cli.stdout))==6
 save('review.json',{'original_replays':raw,'generated_variants':review})
 parts=['# Prime-notation chain rule private draft','Raw source replay is evidence-only. Missing keys/solutions/ratings remain absent. Easy is authored; the two historical unlabeled templates receive an authored hard completion.']
 for r in raw:parts+=['## Original MA '+r['generation']['template'],g.markdown(r)]
 for r in review:parts+=['## '+('Changed-parameter raw evidence' if r['generation']['evidence_only'] else 'Generated eligible variant')+' — '+r['generation']['level']+' / '+r['generation']['template'],g.markdown(r)]
 (HERE/'review.md').write_text('\n\n'.join(parts)+'\n')
 engine=[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(raw+normal) if checks(r)]
 save('engine-input.json',engine);binary=ROOT/'generate/runs/current/check-engine'
 run=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True);(HERE/'engine.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr
 native=json.loads((HERE/'engine-report.json').read_text());assert native['documented_unresolved_checks']==0
 baseline=json.loads((HERE/'registered-baseline.json').read_text());actual=[ROOT/'generate/scratch/17592186096843.py']+sorted(p for p in (ROOT/'generate/scratch/17592186096843').rglob('*') if p.is_file());assert {str(p) for p in actual}==set(baseline)
 assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in baseline.items())
 assert json.loads((HERE/'source.json').read_text())==json.loads((ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186096843.json').read_text())
 inv=json.loads((HERE/'independent-inventory.json').read_text());assert [r['record'] for r in inv['questions']]==[q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
 report={'status':'pass','draft_only':True,'basis':2275,'source_coverage':counts,'complete_MA_originals':9,'independent_inventory_exact':3,'exhaustive_normal_records':len(normal),'meaningful_tasks_per_level':tasks,'default_family_coverage':profile_domains,'negative_and_mutation_checks':negatives,'raw_native_ungraded_missing_designation_records':2,'normal_authored_missing_designations_and_solutions':2,'native_grading':{k:native[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'registered_baseline_unchanged':True,'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'limits':['Easy is an authored conservative square-power band, not recovered source difficulty.','q-107293 coefficient20 remains unresolved historical pattern; raw replay ineligible, complete authored method bank used normally.','Two unrated originals lack correct refs and worked solutions; raw omissions are exact and receive no native grading fixture.','Function symbols f,g and independent variable x are fixed notation roles, not diversity.','Real radicals are validated only on explicitly positive-radicand differentiability domains.'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',binary]}}
 save('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
