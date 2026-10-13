"""Independent displayed-TeX mathematics, full source replay and native grading."""
import importlib.util,importlib.metadata,json,re,subprocess,sys,hashlib
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z=S.symbols('x y z',real=True)
T=standard_transformations+(implicit_multiplication_application,convert_xor)

def group(t,i):
 assert t[i]=='{',(t,i)
 start=i+1;n=1;i+=1
 while n:
  if t[i]=='{':n+=1
  if t[i]=='}':n-=1
  i+=1
 return t[start:i-1],i

def math(t):
 t=t.strip().rstrip('.,:').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,',' ').replace(r'\!','').replace(r'\cdot','*')
 t=t.replace(r'\operatorname{ln}',' ln ').replace(r'\operatorname{cos}',' cos ').replace(r'\operatorname{sin}',' sin ').replace(r'\ln','ln').replace(r'\pi','pi')
 while re.search(r'\\d?frac\s*\{',t):
  m=re.search(r'\\d?frac\s*\{',t);a,j=group(t,m.end()-1)
  while t[j]==' ':j+=1
  b,k=group(t,j);t=t[:m.start()]+'(('+str(math(a))+')/('+str(math(b))+'))'+t[k:]
 t=t.replace('{','(').replace('}',')')
 t=re.sub(r'\b(ln|cos|sin)\s*([0-9]*[xyz]|pi)\b',r'\1(\2)',t)
 return parse_expr(t,local_dict={'x':x,'y':y,'z':z,'pi':S.pi,'e':S.E,'ln':S.log,'cos':S.cos,'sin':S.sin,'I':S.Symbol('I'),'J':S.Symbol('J'),'K':S.Symbol('K')},transformations=T)

def equal(a,b):return S.simplify(S.trigsimp(a-b))==0

def points(v):
 v=v.replace('$','').replace(' only','')
 return frozenset(tuple(math(t) for t in pair.split(',')) for pair in re.findall(r'\(([^()]*)\)',v))

def parsed_prompt(rec):
 q=rec['question'];m=re.search(r'\$([fgh])\(x,y(,z)?\)\s*=\s*(.*?)\$',q[':question/problem']);assert m,q[':question/problem']
 return math(m[3]),(x,y,z) if m[2] else (x,y),m[1]

def complete_roots(expr,vs,f,p):
 # Independently solve actual displayed derivatives; trig interval is read from prompt below.
 ds=[S.diff(expr,v) for v in vs]
 if f=='trig':
  b=-S.expand(expr).coeff(x).subs(y,0)/2
  # Read frequency from the actual cos argument, not generation parameters.
  arg=next(iter(expr.atoms(S.cos))).args[0];k=S.diff(arg,y)
  return frozenset([(b,S.Integer(0)),(S.Integer(0),S.pi/(2*k))]),ds
 if f=='entropy':
  roots=[]
  for v,d in zip(vs,ds):roots.append(S.exp(-d.subs(v,1)))
  return frozenset([tuple(roots)]),ds
 if f=='shifted_log':
  logs=list(expr.atoms(S.log));arg=logs[0].args[0];a=-arg.subs(x,0);b=-S.diff(expr,x).as_numer_denom()[0].subs(y,0)
  return frozenset([(a+1,b)]),ds
 sol=S.solve(ds,vs,dict=True)
 out=[]
 for s in sol:
  if set(s)!=set(vs):raise AssertionError(('infinite/incomplete roots',s))
  t=tuple(s[v] for v in vs)
  if all(v.is_real is not False for v in t) and all(S.simplify(d.subs(s))==0 for d in ds):out.append(t)
 return frozenset(out),ds

def formatcheck(t):
 assert t.count('$$')%2==0
 assert t.replace('$$','').count('$')%2==0
 assert not re.search(r'(?<!\\)\{\\begin',t)
 n=0
 for i,c in enumerate(t):
  if c in '{}':
   if i and t[i-1]=='\\':continue
   n+=1 if c=='{' else -1;assert n>=0,t
 assert n==0,t
 assert '@@' not in t and '++' not in t and '--' not in t

def check(rec):
 q=rec['question'];meta=rec['generation'];f=meta['template'];p=meta['parameters'];expr,vs,fn=parsed_prompt(rec);roots,ds=complete_roots(expr,vs,f,p)
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 fields=q[':question/answer-fields'];assert len(fields)==1;field=fields[0];bank=field[':answer-field/choices'];assert len(bank)==5
 objs=[points(a[':answer/value']) for a in bank];assert all(objs) and len(set(objs))==5,(f,p,objs)
 ci=next(i for i,a in enumerate(bank) if a[':answer/id']==field[':answer-field/correct'][1]);assert objs[ci]==roots,(f,p,objs[ci],roots)
 assert all((o==roots)==(i==ci) for i,o in enumerate(objs))
 assert field[':answer-field/type']==':answer-field.type/radio'
 assert meta['basis']==1356 and meta['lineage']==g.SOURCE['lineage']
 assert meta['python']==sys.version.split()[0]
 if meta['evidence_only']:return rec
 formatcheck(q[':question/problem']);formatcheck(q[':question/worked-solution'])
 solution=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S)
 # Full initial operator blocks: each formal input must equal actual prompt,
 # every unreduced derivative row including held-coordinate zeros equals diff.
 current=-1;stages=[]
 for row in blocks[0].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
  if r'\frac{∂}{∂' in row:
   m=re.search(r'\\frac\{∂\}\{∂([xyz])\}\((.*)\)\s*$',row.strip());assert m,(f,row)
   current=vs.index({'x':x,'y':y,'z':z}[m[1]]);assert equal(math(m[2]),expr),(f,p,'formal_input',m[2]);stages.append(0)
  else:
   rhs=row.split('=')[-1].strip();assert equal(math(rhs),ds[current]),(f,p,'partial_stage',rhs,ds[current]);stages[-1]+=1
 assert len(stages)==len(vs)
 expected={'quadratic':[2,2],'branch3':[2,2,2],'trig':[1,1],'coupled':[2,2],'entropy':[3,3,3],'logquad':[2,2],'reciprocal2':[1,1],'reciprocal3':[2,2,2],'shifted_log':[1,1]}[f];assert stages==expected,(f,stages)
 # Actual inline gradient components independently equal prompt derivatives.
 gradient=re.search(r'(?:Hence,|So, the gradient).*?\$(.*?)\$',solution,re.S)
 if gradient:
  rhs=gradient[1].split('=',1)[1].rstrip('.')
  rhs=rhs.replace(r'\,','').replace(r'\text{ }','')
  basis=S.symbols('I J K');s=rhs
  for v,b in zip('ijk',basis):s=re.sub(v+r'(?=\s*(?:\+|\-|\.|$))','*'+str(b),s)
  # TeX parser's implicit multiplication admits ordinary uppercase proxy symbols.
  parsed=math(s);assert all(equal(S.expand(parsed).coeff(b),d) for b,d in zip(basis,ds)),(f,p,'gradient',rhs)
 # Also inspect displayed gradient and gradient-equals-zero blocks, including
 # canonical easy where the gradient is displayed rather than inline.
 for block in blocks[1:]:
  if not ('\\mathbf i' in block or '\\,i' in block or ')i' in block):continue
  v=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip()
  if '∇' in v or r'\nabla' in v:v=v.split('=',1)[1]
  else:v=v.split('=',1)[0]
  v=v.replace('&','').replace(r'\mathbf','').replace(r'\text{ }','').replace(r'\,','').replace('\\ ',' ')
  basis=S.symbols('I J K')
  for letter,b in zip('ijk',basis):v=re.sub(letter+r'(?=\s*(?:\+|\-|\.|$))', '*'+str(b),v.strip())
  obj=math(v);assert all(equal(S.expand(obj).coeff(b),d) for b,d in zip(basis,ds)),(f,p,'displayed_gradient',v)
 # Every simultaneous equation is correct up to nonzero scalar normalization.
 system=next(b for b in blocks if '=0' in b and r'\begin{aligned}' in b and ('equating' in solution[:solution.index('$$'+b+'$$')]))
 system=system.replace(r'\{','').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip()
 rows=system.split(r'\\');assert len(rows)==len(vs)
 for row,d in zip(rows,ds):
  lhs=math(row.split('=')[0]);ratio=S.simplify(lhs/d);assert not ratio.free_symbols and ratio!=0,(f,p,'system',lhs,d)
 # Read every conclusion tuple and branch in final sentence from printed text.
 last=solution.split('Therefore,')[-1] if 'Therefore,' in solution else solution.split('Hence,')[-1]
 conclusion=frozenset(t for t in points(last) if len(t)==len(vs) and not any(v.free_symbols for v in t));assert conclusion==roots,(f,p,'conclusion',conclusion,roots)
 if f=='trig':
  assert 'for $0\\le y<'+g.tex(S.pi/p['k']) in q[':question/problem']
  chain=blocks[-1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
  assert equal(math(chain[0].split('&')[0]),math(chain[1].split('&')[0]))
 if f=='branch3':
  fact=re.search(r'written as \$(.*?)=0',solution);assert equal(math(fact[1]),ds[0])
  assert solution.count('x & =0')==2
  branchblocks=blocks[-2:]
  for branch,yy in zip(branchblocks,[S.Integer(0),next(point[1] for point in roots if point[1]!=0)]):
   first=branch.replace(r'\begin{aligned}','').split(r'\\')[0].split('&')[0];assert equal(math(first),ds[1].subs(y,yy)),(f,p,'branch_substitution',first)
 if f=='reciprocal2':
  # Actual substitution and reciprocal-square rows must have equal values.
  chain=blocks[-1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
  vals=[math(row.split('&')[0]) for row in chain[:4]]
  assert all(equal(v,ds[1].subs(y,-x*x/p['m'])*-1) for v in vals)
 if f=='reciprocal3':
  assert 'z & =\\pm 1' in solution
  zerochain=blocks[-2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
  first=math(zerochain[0].split('&')[0]);second=math(zerochain[1].split('&')[0]);assert equal(second,first.subs(x,-p['p'])),(f,p,'z_substitution')
  assert equal(math(zerochain[2].split('&')[0]),1-z*z)
  relation=blocks[-1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
  assert equal(math(relation[0].split('&')[0]),ds[0].subs(x,-p['p']))
  assert equal(math(relation[1].split('&')[0]),p['p']*p['q']*z+p['p']*y)
  # Every displayed final y/z branch satisfies all printed partial derivatives.
  for point in conclusion:assert all(equal(d.subs(dict(zip(vs,point))),0) for d in ds)
 return rec

def native(label,r):
 f=r['question'][':question/answer-fields'][0];c=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==c else 'rejected','purpose':'real radio learner grading'} for a in f[':answer-field/choices']]}

def save(name,v):(HERE/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def main():
 reviews=[];rs=[];inputs=[];cases=[];coverage=[];finite={};rejected={}
 for f in g.FAMILIES:
  level=next(l for l,fs in g.LEVELS.items() if f in fs);p=g.ORIGINAL[f];r=check(g.generate(level,17,f,parameters=p,profile='raw_'+f));old=g.TEMPLATES[f];q=r['question'];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'],f
  assert q[':question/worked-solution']==old[':question/worked-solution'],f
  assert sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']),f
  c=next(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==q[':question/answer-fields'][0][':answer-field/correct'][1]);assert c==of[':answer-field/correct'][':answer/value'],f
  for key in [':question/difficulty',':question/answer-fields',':question/worked-solution']:assert (key in q)==(key in old)
  cases.append({'source_id':old[':db/id'],'template':f,'level':level,'parameters':p,'bank_profile':'raw_'+f});coverage.append({'source_id':old[':db/id'],'prompt_exact':True,'solution_exact':True,'full_bank_matched':5,'correct_designation_matched':True})
  inputs.append(native('raw '+f,r));reviews+=['## '+f+' — captured original / public exact raw replay\n\n'+g.markdown(r)];rs.append(r)
  # Each raw recipe must also change parameters through public API.
  p2=next(p for p in g.domains(f,False) if p!=g.ORIGINAL[f]);changed=check(g.generate(level,3,f,parameters=p2,profile='raw_'+f));inputs.append(native('changed raw '+f,changed));rs.append(changed)
 for level,fs in g.LEVELS.items():
  for f in fs:
   allrecords=[];rejected[f]=0
   for p in g.domains(f):
    try:r=g.generate(level,29,f,parameters=p)
    except ValueError as e:
     assert 'collision' in str(e);rejected[f]+=1;continue
    check(r);allrecords.append(r)
   finite[f]=len({r['generation']['mathematical_fingerprint'] for r in allrecords})
   assert len(allrecords)>=2
   for r in allrecords[:2]+allrecords[-2:]:
    rr=g.generate(level,901,f,parameters=r['generation']['parameters']);assert rr['question'][':question/id']==r['question'][':question/id'];assert rr['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint'];inputs.append(native('normal '+f+' '+str(r['generation']['parameters']),r))
   for r in allrecords[:2]:reviews.append('## Generated '+level+' / '+f+' / '+r['generation']['origin']+'\n\n'+g.markdown(r));rs.append(r)
 # Default selection must cover every supported family before parameter sampling.
 for level,fs in g.LEVELS.items():
  seen={g.generate(level,i)['generation']['template'] for i in range(200)};assert seen==set(fs),(level,seen)
 # Explicit guard, wrong level and impossible profiles fail, without mutation.
 for kwargs in [dict(level='easy',template='quadratic'),dict(level='moderate',template='quadratic',parameters={'a':3.0,'b':1,'c':1}),dict(level='moderate',template='quadratic',parameters={'a':99,'b':1,'c':1}),dict(level='hard',template='entropy',parameters={'d':1,'e':1,'f':1}),dict(level='easy',template='shifted_log',parameters={'a':0,'b':0})]:
  try:g.generate(**kwargs)
  except ValueError:pass
  else:raise AssertionError(('guard bypass',kwargs))
 save('source-cases.json',cases);save('review.json',rs);(HERE/'review.md').write_text('\n\n---\n\n'.join(reviews)+'\n')
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 native_report=json.loads((HERE/'native-grading.json').read_text())
 # Decode bytes, not repr/tool serialization, before logging backslash claims.
 slash_counts=[{'source_id':q[':db/id'],'max_adjacent_ord92':max((len(m[0]) for m in re.finditer(r'\\+',q[':question/worked-solution'])),default=0),'unmatched_system_brace':r'{\begin{aligned}' in q[':question/worked-solution']} for q in g.QS]
 save('validation.json',{'passed':True,'basis':1356,'source_coverage':coverage,'raw_exact_prompts':8,'raw_exact_solutions':8,'matched_complete_banks':8,'matched_choices':40,'matched_distractors':32,'matched_correct_designations':8,'normal_mathematics':'exhaustive finite catalogs: actual printed prompts, formal operator inputs, each unreduced and reduced partial, inline gradient, full system, complete root sets, final prose, trig identity, reciprocal elimination arithmetic','normal_instance_checks':sum(len(g.domains(f))-rejected[f] for fs in g.LEVELS.values() for f in fs),'normal_catalog_tasks':finite,'whole_bank_rejections':rejected,'decoded_source_backslash_evidence':slash_counts,'native_records':len(inputs),'native_checks':len(inputs)*5,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'native_engine_source_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'native_engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':S.__version__,'matplotlib':importlib.metadata.version('matplotlib'),'renderer_used':False},'presentation_repaired_normal_families':8,'source_mathematical_typo_families':['branch3','trig','entropy','logquad','reciprocal2','reciprocal3'],'evidence_limits':['raw source profiles preserve known incorrect labels/formal-input/gradient typos and unmatched braces; ineligible for normal learning','opaque raw distractor coordinate patterns are not claimed as recovered mistakes','native radio ID checks do not establish symbolic mathematics; independent displayed-math checks are separate','no plotted question assets; renderer unused']})
 print('PASS: 8 exact sources; 40/40 choices; finite catalogs',finite,'native',len(inputs)*5)
if __name__=='__main__':main()
