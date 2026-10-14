"""Read displayed mathematics independently; original fidelity and native grading separate."""
import sys;sys.dont_write_bytecode=True
import copy,hashlib,json,re,subprocess,types,math
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
g=types.ModuleType('g');g.__file__=str(D.with_suffix('.py'));exec(compile(D.with_suffix('.py').read_text(),g.__file__,'exec'),g.__dict__)
def save(n,v):(D/n).write_text(json.dumps(v,indent=2)+'\n')
def number(text):
 text=text.replace('\\dfrac','\\frac').replace('\\left','').replace('\\right','').replace('\\cdot','*').replace('\\,','');text=re.sub(r'\\sqrt\s+([0-9])',r'\\sqrt{\1}',text)
 def group(i):
  assert text[i]=='{';depth=1;j=i+1
  while depth:depth+=(text[j]=='{')-(text[j]=='}');j+=1
  return text[i+1:j-1],j
 out='';i=0
 while i<len(text):
  if text.startswith('\\frac',i):a,j=group(i+5);b,i=group(j);out+='(('+str(number(a))+')/('+str(number(b))+'))'
  elif text.startswith('\\sqrt',i):a,i=group(i+5);out+='sqrt('+str(number(a))+')'
  else:out+=text[i];i+=1
 out=out.replace('{','(').replace('}',')');assert re.fullmatch(r'[0-9\s()+*/.\-sqrt]+',out),out
 v=sp.simplify(parse_expr(out,transformations=standard_transformations+(implicit_multiplication_application,)));assert not v.free_symbols;return v

def displayed(rec):
 q=rec['question'];prompt=q[':question/problem'];m=re.search(r'\$(x|y)\$-coordinate.*?is \$(.*?)\$',prompt);assert m,prompt
 axis=m[1];k=number(m[2].rstrip(', '));missing=sp.sqrt(1-k*k);expected=sp.simplify(1/missing);target='sec' if axis=='y' else 'csc';other='cos' if axis=='y' else 'sin';given='sin' if axis=='y' else 'cos'
 assert target in prompt and 0<k<1;f=q[':question/answer-fields'][0];values=[number(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5
 assert all(sp.simplify(a-b)!=0 for i,a in enumerate(values) for b in values[i+1:])
 if ':answer-field/correct' in f:
  for a,v in zip(f[':answer-field/choices'],values):assert (sp.simplify(v-expected)==0)==(a[':answer/id']==f[':answer-field/correct'][1])
 sol=q.get(':question/worked-solution')
 if sol:
  assert 'first quadrant' in sol
  # Read all numeric formal given sentences, positive coordinate and concluding rows.
  for v in re.findall(r"(?:We're given that|Substituting).*?\$.*?=(.*?)\$",sol):assert sp.simplify(number(v)-k)==0
  m2=re.search(r'So, \$.*?=(.*?)\.\$',sol);assert m2 and sp.simplify(number(m2[1])-missing)==0
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
  formal=next(block for block in blocks if '\\pm' in block and '\\frac' not in block)
  formalrows=formal.split('\\\\');assert len(formalrows)==3
  assert 'sin' in formalrows[0] and 'cos' in formalrows[0] and '=1' in formalrows[0].replace(' ','')
  assert other in formalrows[1].split('=')[0] and given in formalrows[1].split('=')[1] and '=1-' in formalrows[1].replace(' ','')
  assert other in formalrows[2].split('=')[0] and given in formalrows[2].split('=')[1] and '\\pm' in formalrows[2] and '\\sqrt{1-' in formalrows[2].replace(' ','')
  sub=next(block for block in blocks if '\\pm' in block and '\\frac' in block)
  # Four operative stages, read actual nested expressions and squared fractions.
  rows=sub.split('\\\\');assert len(rows)==4
  assert '\\sqrt{1-' in rows[0] and '^' in rows[0]
  assert '\\sqrt{1-' in rows[1]
  fractions=re.findall(r'\\frac\{(\d+)\}\{(\d+)\}',rows[1]);assert len(fractions)==1
  r,b2=map(sp.Integer,fractions[0]);assert sp.simplify(r/b2-k*k)==0
  fractions=re.findall(r'\\frac\{(\d+)\}\{(\d+)\}',rows[2]);assert len(fractions)==1
  d,b2=map(sp.Integer,fractions[0]);assert sp.simplify(d/b2-(1-k*k))==0
  val=rows[3].split('\\pm')[1].split('\\end')[0].strip().rstrip('.');assert sp.simplify(number(val)-missing)==0
  # Every reciprocal numerical equality, including source-specific aligned row.
  reciprocal=blocks[-2] if 'rationalize' in sol else blocks[-1]
  expressions=re.split('=',reciprocal)
  assert len(expressions)>=3
  for val in expressions[1:]:
   val=val.replace('\\begin{aligned}','').replace('\\end{aligned}','').strip().rstrip('.')
   assert sp.simplify(number(val)-expected)==0
  if 'rationalize' in sol:
   rows=blocks[-1].replace('\\begin{aligned}','').replace('\\end{aligned}','').split('\\\\');assert len(rows)==(3 if rec['generation']['template']=='q-85234' else 4)
   for row in rows:
    val=row.split('=')[-1].strip();assert sp.simplify(number(val)-expected)==0
   assert '\\cdot' in rows[1] and '\\sqrt' in rows[1]
 for text in [prompt,sol or '']+[a[':answer/value'] for a in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
  depth=0
  for c in text:depth+=(c=='{')-(c=='}');assert depth>=0
  assert depth==0 and text.count('$')%2==0
 for asset in rec['generation'].get('assets',{}).values():
  x,y=map(sp.sympify,asset['point']);assert sp.simplify(x*x+y*y)==1 and x>0 and y>0;assert sp.simplify((y if axis=='y' else x)-k)==0
  assert hashlib.sha256(Path(asset['path']).read_bytes()).hexdigest()==asset['sha256']
 return {'axis':axis,'known':str(k),'missing':str(missing),'answer':str(expected)}

def native(records):
 items=[]
 for i,rec in enumerate(records):
  f=rec['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
  items.append({'label':f'radio-{i}','record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'actual original radio field owned selection'} for a in f[':answer-field/choices']]})
  if i<12:
   # Diagnostic memory-only blank fixtures test scalar semantics; never generator format.
   r=copy.deepcopy(rec);r['question'][':question/problem']+='\n\n{{selection}}';r['question'][':question/answer-fields'][0][':answer-field/type']=':answer-field.type/blank'
   val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key);k=sp.sympify(displayed(rec)['known']);equiv='1/sqrt(1-('+str(k)+')^2)'
   items.append({'label':f'scalar-diagnostic-{i}','record':r,'checks':[{'submitted':val,'expected':'accepted','purpose':'canonical exact scalar diagnostic'},{'submitted':equiv,'expected':'accepted','purpose':'unreduced Pythagorean radical reciprocal equivalent diagnostic'},{'submitted':'0','expected':'rejected','purpose':'known wrong exact scalar'}]})
 save('native-input.json',items);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 return json.loads((D/'native-report.json').read_text())

def main():
 frozen={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'generate/scratch/17592186110756.py']+sorted(x for x in (ROOT/'generate/scratch/17592186110756').rglob('*') if x.is_file())}
 assert frozen==json.loads((D/'baseline-inventory.json').read_text()),'Registered baseline changed'
 cases=[{'source_id':q[':db/id'],'math_academy_id':n,'level':'moderate' if n!='q-65066' else 'easy','template':n,'profile':'raw','parameters':{'b':g.CONFIG[n][1],'r':g.CONFIG[n][2]}} for n,q in g.SOURCES.items()];save('source-cases.json',cases)
 F=types.ModuleType('F');F.__file__=str(ROOT/'generate/runs/current/root-source-fidelity.py');exec(compile(Path(F.__file__).read_text(),F.__file__,'exec'),F.__dict__);originals,counts=F.check(g,g.K,D)
 raw=[];normal=[];review=[];banks=[]
 for c in cases:
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='raw');displayed(r);raw.append(r)
  source=g.SOURCES[c['template']];assert sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in source[':question/answer-fields'][0][':answer-field/choices'])
  # Evidence changed instance through exact same public recipe; wholebank rejection.
  success=None
  for b in range(3,10):
   for rr in ([1] if c['template'] in ('q-124750','q-124743') else range(2,b*b)):
    pp={'b':b,'r':rr}
    if pp==c['parameters']:continue
    try:v=g.generate(c['level'],template=c['template'],parameters=pp,profile='raw',plots=False);displayed(v)
    except (ValueError,AssertionError):continue
    success=g.generate(c['level'],template=c['template'],parameters=pp,profile='raw',plots=True);displayed(success);break
   if success:break
  assert success;review.append({'role':'changed observed expression-pattern evidence; ineligible','record':success})
  banks.append({'template':c['template'],'matched_values':5,'total_values':5,'correct_designation_present':':answer-field/correct' in source[':question/answer-fields'][0]})
  for level in ['easy','moderate','hard']:
   for profile in ['method-reciprocal','method-sign']:
    domain=g.domain(level,profile);assert domain
    p=domain[(len(normal)*7)%len(domain)];r=g.generate(level,17,template=c['template'],parameters=p,profile=profile,plots=(profile=='method-reciprocal'));displayed(r);normal.append(r);review.append({'role':'authored '+level+' '+profile,'record':r})
    r2=g.generate(level,81,template=c['template'],parameters=p,profile=profile,plots=(profile=='method-reciprocal'));assert r['question'][':question/id']==r2['question'][':question/id'];assert sorted(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id'] for a in r2['question'][':question/answer-fields'][0][':answer-field/choices'])
 capacity={};coverage={}
 for level in ['easy','moderate','hard']:
  domain=g.domain(level,'method-sign');capacity[level]=2*len(domain);coverage[level]={'coordinate_pairs':domain,'meaningful_tasks_both_axes':2*len(domain)}
  # Domain-level exact operation banks are checked in domain; boundaries displayed.
  for p in [domain[0],domain[-1]]:
   for name in ['q-124750','q-124743']:displayed(g.generate(level,2,template=name,parameters=p,profile='method-sign',plots=False))
  names={g.generate(level,i,plots=False)['generation']['template'] for i in range(50)};assert names==set(g.CONFIG),names
  for bad in [{'b':5,'r':9}] if level!='easy' else [{'b':5,'r':1}]:
   try:g.generate(level,parameters=bad,plots=False)
   except ValueError:pass
   else:raise AssertionError('Level guard bypass')
 report=native([r for r in raw if ':answer-field/correct' in r['question'][':question/answer-fields'][0]]+normal)
 # Fresh atomic renderer concurrency, same and different instances.
 from concurrent.futures import ThreadPoolExecutor
 fresh=[]
 for pp in g.domain('moderate','method-sign'):
  spec={'axis':'x','p':pp,'point':[str(sp.sqrt(pp['r'])/pp['b']),str(sp.sqrt(pp['b']**2-pp['r'])/pp['b'])],'role':'prompt','version':g.VERSION}
  if not (D/'plots'/(g.digest(spec)+'.png')).exists():fresh.append(pp)
  if len(fresh)==2:break
 assert len(fresh)==2
 with ThreadPoolExecutor(max_workers=3) as pool:concurrent=list(pool.map(lambda pp:g.render_plots('x',pp,'prompt'),[fresh[0],fresh[0],fresh[1]]))
 assert concurrent[0]['sha256']==concurrent[1]['sha256'] and concurrent[0]['point']!=concurrent[2]['point']
 assert not [p for p in (D/'plots').glob('tmp*')]
 save('concurrency.json',{'fresh_parameters':fresh,'same_instance_identical':True,'different_instances_distinct':True,'assets':concurrent})
 # Mutations reject a changed substitution component and a C0 control byte.
 mutations=0
 for broken in ['substitution','control','missing-stage']:
  m=copy.deepcopy(normal[-1]);sol=m['question'][':question/worked-solution']
  if broken=='substitution':sol=sol.replace('\\sqrt{1-\\frac','\\sqrt{1+\\frac',1)
  elif broken=='control':sol+='\x0c'
  else:sol=sol.replace('\\cdot','+',1)
  m['question'][':question/worked-solution']=sol
  try:displayed(m)
  except (AssertionError,ValueError):mutations+=1
  else:raise AssertionError('Mutation accepted '+broken)
 save('review.json',review);save('source-bank-replay.json',banks);save('slot-coverage.json',coverage)
 reviewtext=[]
 for r in raw:reviewtext.append('## Original raw evidence '+r['generation']['template']+'\n\n'+g.markdown(r))
 for entry in review:reviewtext.append('## '+entry['role']+' '+entry['record']['generation']['template']+'\n\n'+g.markdown(entry['record']))
 (D/'review.md').write_text('\n\n---\n\n'.join(reviewtext)+'\n')
 summary={'passed':True,'basis':2275,'source_fidelity':counts,'source_coverage':'6/6 MA originals; 30/30 values; 5/5 present correct refs; 1 preserved absent key/grade/solution','authored_completion':'q-65066 normal solution and mathematical key independently derived; raw omissions preserved','capacity':capacity,'displayed_normal_records':len(normal),'observed_changed_parameter_profiles':6,'mutation_regressions':mutations,'native':{k:report[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'baseline_byte_identical':True,'python':sys.version.split()[0],'sympy':sp.__version__,'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'repository_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'database_writes':0}
 save('validation.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
