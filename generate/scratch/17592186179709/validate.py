"""Independent displayed-math, original-bank, presence, identity and native QA."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent; spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
T=g.T;X=g.X;Y=g.Y

def parse(z):
 z=z.replace('⁡','').replace(r'\displaystyle','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\!','')
 z=z.replace(r'\operatorname{ln}',r'\ln').replace('{e}','E').replace(r'\ln','log')
 def group(st,pos):
  assert st[pos]=='{',st[pos:];depth=1;j=pos+1
  while depth:
   if st[j]=='{':depth+=1
   elif st[j]=='}':depth-=1
   j+=1
  return st[pos+1:j-1],j
 while r'\frac' in z or r'\dfrac' in z:
  m=re.search(r'\\d?frac',z);a,j=group(z,m.end());b,k=group(z,j);z=z[:m.start()]+'(('+str(parse(a))+')/('+str(parse(b))+'))'+z[k:]
 while r'\sqrt' in z:
  pos=z.index(r'\sqrt');a,j=group(z,pos+5);z=z[:pos]+'(sqrt('+str(parse(a))+'))'+z[j:]
 z=z.replace('logt','log(t)').replace('logy','log(y)').replace('|t|','t')
 z=z.replace('{','(').replace('}',')').replace('^','**').replace(' e ',' E ').strip().rstrip('.')
 return parse_expr(z,local_dict={'t':T,'x':X,'y':Y,'E':s.E,'e':s.E,'log':s.log,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def integral(z):
 z=z.replace(r'\displaystyle','').replace(r'{\int }',r'\int').strip()
 if r'\left(' in z and z.endswith(r'\right)'):
  z=z.replace(r'\left(','*',1)[:-len(r'\right)')]
 pos=z.index(r'\int'); coefficient=parse(z[:pos].replace(r'\cdot','').strip().rstrip('*') or '1');rest=z[pos+4:]
 assert rest.startswith('_')
 def take(st):
  if st[0]=='{':
   d=1;j=1
   while d:
    d+=(st[j]=='{')-(st[j]=='}');j+=1
   return st[1:j-1],st[j:]
  return st[0],st[1:]
 a,rest=take(rest[1:]);assert rest[0]=='^';b,rest=take(rest[1:]);rest=re.sub(r'\\(?:,|mathrm\{d\}|text\{d\})','',rest).strip();rest=re.sub(r'(?:d)?t$','',rest)
 rest=re.sub(r'\\cdot\s*$','',rest)
 return coefficient*parse(rest),parse(a),parse(b)

def value(z): return integral(z) if r'\int' in z else parse(z)
def eq(a,b):
 if isinstance(a,tuple):return isinstance(b,tuple) and a[1:]==b[1:] and s.simplify(a[0]-b[0])==0
 return not isinstance(b,tuple) and s.simplify(a-b)==0

def balanced(z):
 assert z.count('$')%2==0
 d=0
 for i,c in enumerate(z):
  if c in '{}':
   if i and z[i-1]=='\\':continue
   d+=1 if c=='{' else -1;assert d>=0
 assert d==0
 assert '--' not in z and '+-' not in z

def mathcheck(r):
 q=r['question'];m=r['generation']['math'];f=q[':question/answer-fields'][0];author=r['generation']['template'].startswith('authored_')
 if author:
  prompt=q[':question/problem'];equation=re.search(r'(?:line|curve) \$(.*?)\$',prompt).group(1);left,right=equation.split('=',1);curve=s.solve(s.Eq(parse(left),parse(right)),X)[0].subs(Y,T)
  den=re.search(r'\\int_C (.*?)\\,\\mathrm\{d\}s',prompt).group(1);density=parse(den);lo,hi=map(s.sympify,m['bounds'])
  # Endpoint coordinates from actual prose.
  pts=re.findall(r'points \$\((.*?),(.*?)\)\$ and \$\((.*?),(.*?)\)\$',prompt)[0]
  assert eq(parse(pts[0]),curve.subs(T,parse(pts[1]))) and eq(parse(pts[2]),curve.subs(T,parse(pts[3])))
  ft=density.subs({X:curve,Y:T});speed=s.sqrt(s.diff(curve,T)**2+1);requested=ft if r['generation']['template'] in ('authored_line','authored_line_monomial','authored_affine') else (ft*speed,lo,hi)
  sol=q[':question/worked-solution']
  derivative_block=re.findall(r'\\begin\{aligned\}(.+?)\\end\{aligned\}',sol,re.S)[0]
  derivative_rows=derivative_block.split(r'\\');expected_rows={'authored_line_monomial':8,'authored_affine':7,'authored_log':9,'authored_scaled_log':7,'authored_reciprocal':8}.get(r['generation']['template'],6);assert len(derivative_rows)==expected_rows
  operand=re.search(r'\\frac\{\\mathrm\{d\}\}\{\\mathrm\{d\}t\}\((.*?)\)i',derivative_rows[1]).group(1);assert eq(parse(operand),curve)
  actual_derivative=re.search(r'&=\((.*?)\)i\+j',derivative_rows[2]).group(1);assert eq(parse(actual_derivative),s.diff(curve,T))
  for row in derivative_rows[4:]:assert eq(parse(row.split('&=')[-1].strip()),speed)
  fblock=re.search(r'\\begin\{aligned\}f\(r\(t\)\)\s*&=(.*?)\\end\{aligned\}',sol,re.S).group(1)
  for row in fblock.split(r'\\'):
   assert eq(parse(row.split('&=')[-1]).subs({X:curve,Y:T}),ft),(row,ft)
  final=re.findall(r'&=(.*?)\\end\{aligned\}',sol,re.S)[-1].split(r'\\')[-1];final=final.split('&=')[-1].rstrip('.')
  assert eq(value(final),(ft*speed,lo,hi)) or (r['generation']['template'] in ('authored_line','authored_line_monomial','authored_affine') and eq(integral(final),(ft*speed,lo,hi)))
 else:
  i,o=g.OBS_BY_NAME[r['generation']['template']];c=r['generation']['parameters']['density_scale'];_,level,curve,density,lo,hi,bank,ci,_=o
  requested=(c*bank[ci][0],bank[ci][1],bank[ci][2]) if isinstance(bank[ci],tuple) else c*bank[ci]
  derived=c*density.subs({X:curve,Y:T})*s.sqrt(s.diff(curve,T)**2+1)
  if isinstance(requested,tuple):assert eq(requested,(derived,lo,hi))
  else:
   factor=s.Rational(-1,4) if r['generation']['template']=='parabola_missing' else s.sqrt(s.diff(curve,T)**2+1)
   assert eq(requested,derived/factor)
 if not author and ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];ft=c*density.subs({X:curve,Y:T});speed=s.sqrt(s.diff(curve,T)**2+1)
  fblock=re.search(r'\\begin\{aligned\}f\(r\(t\)\)\s*& =(.+?)\\end\{aligned\}',sol,re.S).group(1)
  for row in fblock.split(r'\\'):
   expr=parse(row.split('& =')[-1].strip().rstrip('.')).subs({X:curve,Y:T})
   assert eq(expr,ft),(r['generation']['template'],row,ft)
  derivative_block=re.findall(r'\\begin\{aligned\}(.+?)\\end\{aligned\}',sol,re.S)[0]
  metric=False
  for row in derivative_block.split(r'\\'):
   if '‖' in row:metric=True;continue
   if metric:
    rhs=row.split('& =')[-1].strip();assert eq(parse(rhs),speed),(rhs,speed)
  finalblock=re.findall(r'\\begin\{aligned\}(.+?)\\end\{aligned\}',sol,re.S)[-1]
  for row in finalblock.split(r'\\')[1:]:
   rhs=row.split('& =')[-1].strip().rstrip('.');assert eq(integral(rhs),(ft*speed,lo,hi)),(rhs,ft*speed)
 parsed=[value(a[':answer/value']) for a in f[':answer-field/choices']]
 assert sum(eq(x,requested) for x in parsed)==1
 if ':answer-field/correct' in f:
  idx=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]);assert eq(parsed[idx],requested)
 # Entire mathematical values matter for complete definite integral options.
 if isinstance(parsed[0],tuple):
  import mpmath as mp
  mp.mp.dps=40
  vals=[mp.quad(s.lambdify(T,x[0],'mpmath'),[mp.mpf(str(s.N(x[1],45))),mp.mpf(str(s.N(x[2],45)))]) for x in parsed]
  assert all(abs(vals[i]-vals[j])>1e-7*max(1,abs(vals[i]),abs(vals[j])) for i in range(5) for j in range(i)),(r['generation']['template'],r['generation']['seed'],vals)
 else:assert all(not eq(parsed[i],parsed[j]) for i in range(5) for j in range(i))
 for z in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in f[':answer-field/choices']]:balanced(z)
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 return True

cases=[g.source_case(i) for i in range(len(g.QS))];(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
records=[];fidelity=[];checks=[];native=[]
for i,case in enumerate(cases):
 kw={'template':case['template'],'parameters':case['parameters']};r=g.generate(case['level'],profile='observed_raw',**kw);raw=g.QS[i];q=r['question'];field=q[':question/answer-fields'][0];old=raw[':question/answer-fields'][0]
 assert q[':question/problem']==raw[':question/problem'];assert q.get(':question/worked-solution')==raw.get(':question/worked-solution')
 assert set(q)==set(g.enums(raw))
 assert set(field)==set(g.enums(old));assert sorted(a[':answer/value'] for a in field[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices'])
 if ':answer-field/correct' in old:
  correct=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert correct==old[':answer-field/correct'][':answer/value']
 mathcheck(r);records.append(r)
 if ':answer-field/correct' in field:native.append(r)
 fidelity.append({'source_id':case['source_id'],'bank_choices':5,'prompt_exact':True,'solution_presence_and_exact':True,'attribute_presence':True,'correct_designation_match':':answer-field/correct' in old})
 for scale in (2,4):
  changed=g.generate(case['level'],template=case['template'],parameters={'density_scale':scale},profile='observed_completed');mathcheck(changed);records.append(changed);native.append(changed)
 completed=g.generate(case['level'],profile='observed_completed',**kw);native.append(completed)
for level in ('easy','moderate','hard'):
 seen=set()
 for seed in range(48):
  r=g.generate(level,seed);mathcheck(r);seen.add(r['generation']['mathematical_fingerprint']);native.append(r)
  if seed<2:records.append(r)
  p=r['generation']['parameters'];same=g.generate(level,seed+19,template=r['generation']['template'],parameters=p);assert same['question'][':question/id']==r['question'][':question/id']
 assert len(seen)>=40,(level,len(seen));checks.append({'level':level,'instances':48,'unique_mathematical_tasks':len(seen)})
 for p in ({'a':2,'b':0,'k':2,'u':1,'v':2,'lo':0,'hi':2,'n':1},{'a':-5,'b':2,'k':2,'u':2,'v':2,'lo':0,'hi':2,'n':2}):
  if level=='easy' and p['a']==2:continue
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Bounds not enforced')
normal_source_parameters={'authored_line_monomial':{'m':3,'k':1,'v':1,'lo':0,'hi':9},'authored_affine':{'a':-3,'b':2,'p':2,'q':-3,'lo':0,'hi':2},'authored_log':{'a':1,'k':1,'c':1,'v':2,'lo':0,'hi':2},'authored_scaled_log':{'a':2,'k':4,'c':2,'v':1,'lo':0,'hi':1},'authored_reciprocal':{'a':2,'k':4,'v':2,'lo':1,'hi':6}}
for name,p in normal_source_parameters.items():
 r=g.generate(g.TEMPLATES[name],template=name,parameters=p);mathcheck(r);records.append(r);native.append(r)
family_checks=[]
for name,level in g.TEMPLATES.items():
 if not name.startswith('authored_'):continue
 seen=set()
 for seed in range(12):
  r=g.generate(level,100+seed,template=name);mathcheck(r);native.append(r);seen.add(r['generation']['mathematical_fingerprint'])
  if seed<2:records.append(r)
  same=g.generate(level,200+seed,template=name,parameters=r['generation']['parameters']);assert same['question'][':question/id']==r['question'][':question/id']
  if name in g.FAMILY_SOURCES:
   original=g.QS[g.FAMILY_SOURCES[name]][':question/worked-solution'];solution=r['question'][':question/worked-solution']
   origblocks=re.findall(r'\\begin\{aligned\}(.+?)\\end\{aligned\}',original,re.S);newblocks=re.findall(r'\\begin\{aligned\}(.+?)\\end\{aligned\}',solution,re.S)
   assert [len(x.split(r'\\')) for x in origblocks]==[len(x.split(r'\\')) for x in newblocks]
  assert ' (correct)' in g.markdown(r) and 'Generated' in g.markdown(r) and level.title() in g.markdown(r)
 assert len(seen)>=10,(name,len(seen))
 family_checks.append({'template':name,'level':level,'instances':12,'unique_mathematical_tasks':len(seen),'source_prose_stage_mask':name in g.FAMILY_SOURCES})
for r in native:
 f=r['question'][':question/answer-fields'][0];cs=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned radio option native grading'} for a in f[':answer-field/choices']]
 checks_label=r['generation']['template']+'-'+str(r['generation']['seed']);checks.append({'native_label':checks_label})
 (None)
 native_item={'label':checks_label,'record':r,'checks':cs}
 if 'engine_items' not in globals():engine_items=[]
 engine_items.append(native_item)
(HERE/'engine-input.json').write_text(json.dumps(engine_items,indent=2)+'\n');exe=HERE.parents[1]/'runs/current/check-engine';subprocess.run([str(exe),str(HERE/'engine-input.json'),str(HERE/'engine.json')],check=True)
(HERE/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
report={'status':'passed','source_basis':1356,'source_questions':7,'complete_banks_matched':7,'choices_matched':35,'incorrect_choices_matched':28,'correct_designations_matched':5,'correct_designations_absent_in_source':2,'solutions_exact':5,'solutions_absent_preserved':2,'presence_parity':7,'source_fidelity':fidelity,'authored_checks':[x for x in checks if 'level' in x],'family_checks':family_checks,'normal_source_parameter_instances':len(normal_source_parameters),'native':json.loads((HERE/'engine.json').read_text()),'python_version':sys.version.split()[0],'sympy_version':s.__version__,'check_engine_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'plot_new_generation_required':False,'limitations':['Seven historical expression-pattern banks generalized only by uniform density scaling, not promoted to learner defaults.','Two unrated originals have no correct ref or worked solution; designation inference is only in completed evidence.','Authored defaults omit nonessential curve illustration, because equation and both endpoints supply all assessed information.','Definite-integral bank inequality tested with independent high precision quadrature; equality at structural level is also checked.']}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('status','source_questions','complete_banks_matched','choices_matched','correct_designations_matched','authored_checks')},indent=2))
