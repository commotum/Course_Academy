#!/usr/bin/env python3
"""Independent displayed-math/readback, source-fidelity and real-engine validation."""
import importlib.util,itertools,json,re,subprocess,sys,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;script=D.with_suffix('.py');spec=importlib.util.spec_from_file_location('tangent_generator',script);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,i,j=s.symbols('x y i j',real=True);trans=standard_transformations+(implicit_multiplication_application,)
C={'source_prompts_exact':0,'source_banks_exact':0,'source_values_exact':0,'source_designations_exact':0,'source_designations_absent':0,'source_solutions_exact':0,'source_solutions_absent':0,'displayed_math_instances':0,'partial_operator_inputs':0,'tangent_expansions':0,'orthogonality_stages':0,'substitution_stages':0,'native_checks':0,'invalid_parameters_rejected':0,'finite_authored_tasks':{},'finite_observed_translation_tasks':{}}
def read(z):
 z=z.strip().rstrip('.,?').replace('&','').replace('−','-').replace('\u00a0','').replace(r'\,','').replace(r'\ ','')
 z=re.sub(r'\\(?:text|cancel)\{([^{}]*)\}',r'\1',z)
 while re.search(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',z):z=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',lambda m:'(('+m[1]+')/('+m[2]+'))',z)
 z=z.replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(z,local_dict={'x':x,'y':y,'i':i,'j':j},transformations=trans)
def points(t):return frozenset((s.simplify(read(a)),s.simplify(read(b))) for a,b in re.findall(r'\(([^(),]+),([^(),]+)\)',t))
def blocks(t):return re.findall(r'(\$\$|\$)(.*?)\1',t,re.S)
def equation(z):
 a,b=z.split('=',1);return s.expand(read(a)-read(b))
def proportional(a,b):
 a,b=s.cancel(a),s.cancel(b)
 if a==0 or b==0:return a==b
 ratio=s.cancel(a/b);num,den=s.fraction(ratio);return not num.free_symbols and num!=0

def operand(row,start):
 pos=row.index('(',start);depth=0
 for end in range(pos,len(row)):
  if row[end]=='(':depth+=1
  if row[end]==')':
   depth-=1
   if depth==0:return row[pos+1:end]
 raise AssertionError(('unbalanced operator',row))
def formatting(t):
 # Source byte evidence has no doubled slash anomaly. Every normal math group balances.
 assert t.count('$')%2==0,t
 for _,z in blocks(t):
  balance=0
  for char in z:
   if char=='{':balance+=1
   elif char=='}':balance-=1
   assert balance>=0,z
  assert balance==0,z
  assert '--' not in z and '+-' not in z,z

def independent(record,stages=True):
 q=record['question'];assert set(record['knowledge_point'])=={'db_id','id','title'}
 prompt=q[':question/problem'];formatting(prompt)
 b=blocks(prompt);eq=next(z for _,z in b if '=' in z);F=equation(eq)
 vs=b[-1][1].replace(r'\mathbf','').replace('{','').replace('}','').rstrip('?');v=read(vs)
 u,w=s.expand(v).coeff(i),s.expand(v).coeff(j);assert u or w
 fx,fy=s.diff(F,x),s.diff(F,y);condition=s.expand(u*fy-w*fx)
 raw=s.solve_poly_system([F,condition],x,y);assert raw is not None
 correct=frozenset((s.simplify(a),s.simplify(b)) for a,b in raw if a.is_real and b.is_real)
 assert correct and all((fx.subs({x:a,y:b}),fy.subs({x:a,y:b}))!=(0,0) for a,b in correct)
 f=q[':question/answer-fields'][0];ans=f[':answer-field/choices'];banks=[points(a[':answer/value']) for a in ans];assert all(banks) and len(set(banks))==5
 assert sum(z==correct for z in banks)==1
 if ':answer-field/correct' in f:assert [a[':answer/id'] for a,z in zip(ans,banks) if z==correct]==[f[':answer-field/correct'][1]]
 sol=q.get(':question/worked-solution')
 if sol:
  formatting(sol)
  final=sol.split('Finally',1)[1];assert points(final)==correct,('final points',final,correct)
  if stages:
   displays=[z for delim,z in blocks(sol) if delim=='$$'];derivatives=[z for z in displays if r'\frac{∂}{∂' in z];assert len(derivatives)==1
   rows=derivatives[0].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')
   deriv=next(z for z in rows if r'\frac{∂}{∂' in z)
   for variable,expected in [('y',fy),('x',fx)]:
    marker=r'\frac{∂}{∂'+variable+'}';pos=deriv.index(marker);inside=read(operand(deriv,pos));assert s.expand(s.diff(inside,y if variable=='y' else x)-expected)==0,(deriv,inside,F)
    C['partial_operator_inputs']+=1
   rhs=rows[-1].split('=',1)[1];assert s.expand(read(rhs)-(fy*i-fx*j))==0,('tangent expansion',rhs,F);C['tangent_expansions']+=1
   # Extract actual scalar orthogonality and relation from its own display.
   orth=next(z for z in displays if r'\cdot' in z and r'\begin{aligned}' in z)
   orows=orth.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')
   scalar=[row for row in orows if '=' in row and r'\cdot' not in row]
   for row in scalar:
    if r'\text' in row:continue # Only inferred two-branch evidence solution has this row.
    expression=equation(row);assert all(s.simplify(expression.subs({x:a,y:b}))==0 for a,b in correct),(row,correct)
    assert proportional(expression,condition),(row,condition);C['orthogonality_stages']+=1
   relation=scalar[-1]
   if r'\text' in relation:
    # Two original branches are present only in missing-solution completion evidence.
    assert len(correct)==3 and 'For the second relation $' in sol
    branches=re.split(r'\\text\{ or \}',relation.replace('&',''));assert len(branches)==2
    subdisplays=displays[displays.index(orth)+1:];assert len(subdisplays)==2
    for branch,display in zip(branches,subdisplays):
     rel=equation(branch);assert s.fraction(s.cancel(condition/rel))[1]==1
     repl=s.solve(rel,y);assert len(repl)==1;sub={y:repl[0]};reference=s.factor(F.subs(sub))
     reference_roots={a for a in s.solve(reference,x) if a.is_real}
     rows=display.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')
     for row in rows:
      if '=' not in row or ',' in row.split('=')[1]:continue
      expr=equation(row).subs(sub)
      assert {a for a in s.solve(expr,x) if a.is_real}==reference_roots,('two-branch inferred substitution',row,expr,reference)
      C['substitution_stages']+=1
   else:
    rel=equation(relation);lhs=read(relation.split('=')[0]);eliminate=x if lhs.free_symbols=={x} else y
    replacement=s.solve(rel,eliminate);assert len(replacement)==1
    subst={eliminate:replacement[0]};reference=s.factor(F.subs(subst));subdisplays=displays[displays.index(orth)+1:]
    assert subdisplays
    for display in subdisplays:
     rows=display.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')
     for row in rows:
      if '=' not in row or r'\pm' in row or r'\text' in row or ',' in row.split('=')[1]:continue
      expr=equation(row).subs(subst)
      assert proportional(expr,reference),('substitution row',row,expr,reference)
      C['substitution_stages']+=1
 C['displayed_math_instances']+=1
 return correct

source=g.SOURCES;cases=[];review=[];mapping=[];native=[]
for sid,q in source.items():
 case={'source_id':sid,'template':sid,'level':'hard','parameters':{'h':0,'k':0},'bank_profile':'observed_raw','original_level':'hard' if ':question/difficulty' in q else 'unrated','assignment':'observed' if ':question/difficulty' in q else 'authored hard for evidence completion; raw remains unrated'};cases.append(case)
 r=g.generate('hard',template=sid,parameters=case['parameters'],profile='observed_raw');nq=r['question'];nf=nq[':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
 assert nq[':question/problem']==q[':question/problem'];C['source_prompts_exact']+=1
 assert sorted((a[':answer/value'],a[':answer/type']) for a in nf[':answer-field/choices'])==sorted((a[':answer/value'],g.enum(a[':answer/type'])) for a in sf[':answer-field/choices']);C['source_banks_exact']+=1;C['source_values_exact']+=5
 for attr in (':question/difficulty',':question/worked-solution'):assert (attr in nq)==(attr in q),(sid,attr)
 assert (':answer-field/correct' in sf)==(':answer-field/correct' in nf)
 if ':question/worked-solution' in q:assert nq[':question/worked-solution']==q[':question/worked-solution'];C['source_solutions_exact']+=1
 else:C['source_solutions_absent']+=1
 if ':answer-field/correct' in sf:
  actual=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert actual==sf[':answer-field/correct'][':answer/value'];C['source_designations_exact']+=1
 else:C['source_designations_absent']+=1
 independent(r);review.append({'label':sid+' original raw / '+case['original_level'],'record':r})
 # Full mapping describes each complete coordinate recipe without invented error intent.
 mapping.append({'source_id':sid,'prompt_mask':q[':question/problem'],'solution_mask':q.get(':question/worked-solution'), 'fields':sf,'translation_recipe':'For every complete tuple (a,b), render (a+h,b+k); every variable component x or y in math becomes x-h or y-k; derivative operators and symbolic function argument labels stay x,y. No interpolated fit or answer lookup.','interpretation':'Historical wrong-coordinate sets opaque, evidence-only.'})
 for profile in ('observed_raw','observed_completed'):
  for h,k in ((2,-1),(-3,3)):
   changed=g.generate('hard',template=sid,parameters={'h':h,'k':k},profile=profile);independent(changed);review.append({'label':sid+' translated '+profile,'record':changed})
 completed=g.generate('hard',template=sid,parameters={'h':0,'k':0},profile='observed_completed');independent(completed);review.append({'label':sid+' completed evidence only','record':completed});native.append(completed)
 # Independent finite translation enumeration; same guard in API and sampler.
 fps=set()
 for h,k in itertools.product(range(-3,4),repeat=2):
  changed=g.generate('hard',template=sid,parameters={'h':h,'k':k},profile='observed_raw');independent(changed);fps.add(changed['generation']['mathematical_fingerprint'])
 C['finite_observed_translation_tasks'][sid]=len(fps)
for level in ('easy','moderate','hard'):
 if level=='easy':domain=({'A':A,'b':b,'r':r} for A,b,r in itertools.product(range(1,5),range(2,6),[v for v in range(-6,7) if v]))
 elif level=='moderate':domain=({'D':D,'m':m,'r':r} for D,m,r in itertools.product(range(1,4),range(2,5),range(1,5)))
 else:domain=({'a':a,'b':b} for a,b in itertools.combinations([v for v in range(-6,7) if v],2) if a+b)
 fps=set()
 for p in domain:
  r=g.generate(level,parameters=p);independent(r);fps.add(r['generation']['mathematical_fingerprint'])
 C['finite_authored_tasks'][level]=len(fps)
 for seed in (23,44):
  r=g.generate(level,seed);independent(r);review.append({'label':level+' authored generated','record':r});native.append(r)
  reordered=g.generate(level,seed+1,parameters=r['generation']['parameters']);assert reordered['question'][':question/id']==r['question'][':question/id'];assert reordered['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
for level,p in [('easy',{'A':0,'b':2,'r':1}),('easy',{'A':1,'b':1,'r':1}),('moderate',{'D':1,'m':1,'r':2}),('moderate',{'D':1,'m':2,'r':5}),('hard',{'a':-2,'b':2}),('hard',{'a':1,'b':1}),('hard',{'a':1,'b':7})]:
 try:g.generate(level,parameters=p)
 except ValueError:C['invalid_parameters_rejected']+=1
 else:raise AssertionError('invalid parameters accepted')
for sid in source:
 try:g.generate('hard',template=sid,profile='observed_raw',parameters={'h':4,'k':0})
 except ValueError:C['invalid_parameters_rejected']+=1
 else:raise AssertionError('Translation boundary accepted')
fixtures=[]
for idx,r in enumerate(native):
 f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'complete point-set radio selection'} for a in f[':answer-field/choices']]
 fixtures.append({'label':'instance-'+str(idx),'record':r,'checks':checks});C['native_checks']+=len(checks)
(D/'native-input.json').write_text(json.dumps(fixtures,indent=2));repo=D.parents[2]
engine=repo/'generate/runs/current/check-engine';proc=subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],text=True,capture_output=True);assert proc.returncode==0,proc.stdout+proc.stderr
C['native_engine_sha256']=hashlib.sha256(engine.read_bytes()).hexdigest();C['native_engine_result']='passed; actual learning::grade_field'
C['blank_equivalence']='not applicable: all source and generated fields radio, full point sets'
C['source_missing_refs_completion']='2 mathematically inferred, not counted as matched original designations'
C['raw_source_anomalies']='2 absent difficulty, solution, correct reference; no duplicate widget field; no wrong keyed values detected'
C['limits']='Historical distractor intent opaque; translation preserves full numerical banks, not recovered author code. Easy/moderate are authored labels, not observed source levels. No native free-expression grading is claimed.'
C['passed']=True;C['database_writes']=0
(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(D/'component-map.json').write_text(json.dumps(mapping,indent=2)+'\n');(D/'review.json').write_text(json.dumps(review,indent=2)+'\n');(D/'review.md').write_text('# Review: originals, evidence completions and authored variants\n\n'+ '\n\n'.join('## '+item['label']+'\n\n'+g.markdown(item['record']) for item in review)+'\n');(D/'validation.json').write_text(json.dumps(C,indent=2)+'\n');print(json.dumps(C,indent=2))
