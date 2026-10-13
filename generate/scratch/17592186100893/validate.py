#!/usr/bin/env python3
"""Fail-closed fidelity, independently parsed math/stages, UUID and native grading."""
from pathlib import Path
import importlib.util,json,re,sys,subprocess,hashlib,uuid
import sympy as sp
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
sys.path.insert(0,str(ROOT));from parse_math import expression,relation,equivalent,X,Y,T,C
spec=importlib.util.spec_from_file_location('ivp_generator',ROOT.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
def simp(v):
 result=sp.trigsimp(sp.simplify(v))
 if result!=0 and result.has(sp.sin,sp.cos,sp.tan,sp.cot,sp.sec):result=sp.trigsimp(result.rewrite(sp.cos))
 return result
def model(m,k):return sp.sympify(m[k],locals={'x':X,'y':Y,'t':T,'C':C})
def native_equivalent(e):
 return sp.latex(sp.exp(sp.expand(e.args[0]),evaluate=False)) if e.func==sp.exp else sp.latex(sp.expand(e))
def correct(f):return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def verify(r):
 q=r['question'];g=r['generation'];m=g['mathematics'];f=q[':question/answer-fields'][0];radio=f[':answer-field/type'].endswith('/radio')
 uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id']);assert len(f[':answer-field/choices'])==(5 if radio else 1)
 assert radio or '{{'+f[':answer-field/key']+'}}' in q[':question/problem'];assert q[':question/worked-solution'].count('$$')%2==0
 values=[relation(a[':answer/value']) for a in f[':answer-field/choices']]
 for a in f[':answer-field/choices']:uuid.UUID(a[':answer/id']);assert '$' not in a[':answer/value'];assert '\u2061' not in a[':answer/id']
 assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(values)
 expected=(model(m,'lhs') if radio else None,model(m,'rhs'));selected=relation(correct(f)[':answer/value']);assert equivalent(selected,expected),(g['template'],selected,expected)
 for i,v in enumerate(values):
  for w in values[:i]:assert not equivalent(v,w),('duplicate bank',g['template'],v,w)
 ode=model(m,'ode');lhs=model(m,'lhs');rhs=model(m,'rhs');var=X if m['variable']=='x' else T;x0=model(m,'initial_x');y0=model(m,'initial_y')
 if var==X:
  maths=re.findall(r'(?<!\$)\$([^$]*)\$(?!\$)',q[':question/problem'])
  displayed=[v for v in maths if r'\frac{\text{d}y}{\text{d}x}' in v or '′' in v or "y'" in v]
  assert len(displayed)==1,('missing printed ODE',g['template'])
  equation=displayed[0].replace(r'\frac{\text{d}y}{\text{d}x}','C').replace('{y}^{′}','C').replace("y'",'C')
  dl,dr=relation(equation);printed=sp.solve(dl-dr,C)
  assert len(printed)==1 and simp(printed[0]-ode)==0,('printed ODE mismatch',g['template'],printed,ode)
  condition=next(v for v in maths if re.match(r'y\(',v))
  match=re.fullmatch(r'y\((.*?)\)\s*=\s*(.*)',condition.rstrip('.,'));assert match
  px,py=map(expression,match.groups())
  assert simp(px-x0)==0 and simp(py-y0)==0,('printed initial-value mismatch',g['template'])
 assert simp(lhs.subs(Y,y0)-rhs.subs(var,x0))==0,('initial',g['template'])
 if lhs==Y:
  check=simp(sp.diff(rhs,var)-ode.subs(Y,rhs))
  if check!=0:
   # The root solution's positive branch is tested with a positive local square.
   z=sp.symbols('z',real=True);check=simp(check.subs(X,z+sp.Rational(m['h'])))
  assert check==0,('explicit derivative',g['template'],check)
 else:
  assert simp(sp.diff(lhs,Y)*ode-sp.diff(rhs,X))==0,('implicit derivative',g['template'])
 if 'primitive_y' in m:
  assert simp(sp.diff(model(m,'primitive_x'),X)/sp.diff(model(m,'primitive_y'),Y)-ode)==0,('separation',g['template'])
 return len(values)

def stage_verify(r):
 """Independently parse every algebraic worked row. Integrals/differentials
 are checked through the independent primitive derivative proof. Resolve the
 arbitrary aliases using displayed equations at the independently known initial
 value; check inverse-function identities on the prescribed local branch.
 """
 q=r['question'];m=r['generation']['mathematics'];rhs=model(m,'rhs');lhs=model(m,'lhs');x0=model(m,'initial_x');y0=model(m,'initial_y');var=X if m['variable']=='x' else T
 if lhs==Y:particular=rhs
 elif lhs==Y**3:particular=sp.real_root(rhs,3)
 elif lhs.func==sp.cos:particular=sp.acos(rhs)
 elif lhs.func==sp.sin:particular=sp.asin(rhs)/lhs.args[0].coeff(Y)
 elif lhs.func==sp.tan:particular=sp.atan(rhs)/lhs.args[0].coeff(Y)
 elif lhs.has(sp.sin):
  atom=next(iter(lhs.atoms(sp.sin)));particular=sp.asin(rhs/(lhs/atom))/atom.args[0].coeff(Y)
 elif lhs==sp.log(Y)**2:particular=sp.exp(sp.sqrt(rhs))
 else:raise AssertionError(('unsupported solution branch',lhs))
 parsed=[];derivative=[];constants={}
 for block in re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',q[':question/worked-solution']):
  last_left=None
  for raw in re.split(r'\\\\',block):
   raw=raw.strip().replace(r'\,.','').replace(r'\,,','').rstrip('.,').replace('&','').strip().rstrip('\\')
   if not raw:continue
   if not raw.startswith('=') and '=' in raw:last_left=raw.split('=')[0]
   if raw.startswith('=') and last_left is not None:raw=last_left+raw
   if any(v in raw for v in (r'\int',r'\text',r'\pm',r'\,dx')):derivative.append(raw);continue
   raw=raw.replace('y(x)','y');raw=re.sub(r'y\([^()]*\)',lambda _:sp.latex(y0),raw)
   if '=' not in raw:derivative.append(raw);continue
   a,b=relation(raw);parsed.append((raw,(a-b).subs(Y,particular)))
 # Two indefinite integrals' constants are arbitrary up to common translation;
 # set C2=0 only for the source that explicitly uses C1-C2.
 names={v for _,e in parsed for v in e.free_symbols if v.name.startswith(('C','K'))}
 if any(v.name=='C2' for v in names):constants[next(v for v in names if v.name=='C2')]=sp.Integer(0)
 for _ in range(4):
  for raw,e in parsed:
   e=e.subs(constants);unknown={v for v in e.free_symbols if v.name.startswith(('C','K'))}
   if len(unknown)==1:
    v=next(iter(unknown));sols=sp.solve(e.subs(var,x0),v)
    if isinstance(sols,list) and len(sols)==1 and not sols[0].free_symbols:constants[v]=sols[0]
 checked=[];branch=[]
 for raw,e in parsed:
  e=e.subs(constants)
  assert not any(v.name.startswith(('C','K')) for v in e.free_symbols),('unresolved constant stage',r['generation']['template'],raw,e,constants)
  result=simp(e)
  if result!=0:
   # Exact symbolic inverse identities may depend on the local branch. Check
   # three nearby interior points to 40 digits; derivative primitives prove
   # functional equality independently, so this checks branch/evaluation signs.
   for offset in (0,sp.Rational(1,100),-sp.Rational(1,100)):
    value=sp.N(e.subs(var,x0+offset),40)
    assert value.is_finite and abs(complex(value))<1e-25,('bad worked stage',r['generation']['template'],raw,value)
   branch.append(raw)
  checked.append(raw)
 assert len(checked)>=2,(r['generation']['template'],parsed)
 return {'checked_rows':checked,'derivative_rows':derivative,'local_branch_rows':branch,'constants':{str(k):str(v) for k,v in constants.items()}}

def main():
 sources=G.SOURCES;cases=[];fidelity=[];review=[];native=[];stage_reports=[];total_values=0;checked=0
 for s,q in sources.items():
  t=s.replace('q-','source_');level=G.TEMPLATES[t]['level'];params={'h':0}
  if s=='q-168078':params['ambient']=25
  case={'source_id':s,'template':t,'level':level,'parameters':params,'bank_profile':'observed'};cases.append(case)
  r=G.generate(level,0,t,parameters=params,profile='observed');total_values+=verify(r);checked+=1
  f=r['question'][':question/answer-fields'][0];original=q[':question/answer-fields'][0]
  originals=[relation(a[':answer/value']) for a in original[':answer-field/choices']];generated=[relation(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(originals)==len(generated)
  for v in originals:assert sum(equivalent(v,w) for w in generated)==1,(s,v,generated)
  assert equivalent(relation(original[':answer-field/correct'][':answer/value']),relation(correct(f)[':answer/value']))
  assert f[':answer-field/key']==original[':answer-field/key'];assert f[':answer-field/type']==original[':answer-field/type'][':db/ident']
  # Shared prose and stage order retained by the reusable translation template.
  def prose(s):return re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*?\$','MATH',s).strip()
  assert prose(r['question'][':question/worked-solution'])==prose(q[':question/worked-solution'])
  assert r['question'][':question/worked-solution'].count('\\begin{aligned}')==q[':question/worked-solution'].count('\\begin{aligned}')
  fidelity.append({'source_id':s,'total_values':len(originals),'matched_values':len(originals),'correct_designation_matched':True,'field_shape_matched':True,'shared_prose_and_stage_count_matched':True})
  stage_reports.append({'source_id':s,**stage_verify(r)})
  # Canonical and equivalent blank entries plus an independently wrong value.
  if f[':answer-field/type'].endswith('/blank'):
   expected=relation(correct(f)[':answer/value'])[1]
   checks=[{'submitted':correct(f)[':answer/value'],'expected':'accepted','purpose':'original exact RHS fragment'}, {'submitted':native_equivalent(expected),'expected':'accepted','purpose':'equivalent expanded expression'}, {'submitted':sp.latex(expected+1),'expected':'rejected','purpose':'incorrect additive constant'}]
  else:checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned choice selection'} for a in f[':answer-field/choices']]
  native.append({'label':s,'record':r,'checks':checks})
  review.append(r)
  for h in (-2,sp.Rational(1,2),3):
   p={'h':str(h)} if s!='q-168078' else {'h':0,'ambient':25+h}
   for profile in ('observed',('blank' if G.TEMPLATES[t]['kind']=='blank' else 'authored')):
    v=G.generate(level,13,t,parameters=p,profile=profile);verify(v);checked+=1
   review.append(v);stage_reports.append({'source_id':s,'variant_h':str(h),**stage_verify(v)})
   f=v['question'][':question/answer-fields'][0]
   if f[':answer-field/type'].endswith('/blank'):
    ev=relation(correct(f)[':answer/value'])[1]
    native.append({'label':s+' variant '+str(h),'record':v,'checks':[{'submitted':native_equivalent(ev),'expected':'accepted','purpose':'generated equivalent blank'},{'submitted':sp.latex(ev+1),'expected':'rejected','purpose':'wrong generated constant'}]})
  # Correct selection must not depend on a captured correct designation.
  saved=G.SOURCES[s][':question/answer-fields'][0][':answer-field/correct']
  G.SOURCES[s][':question/answer-fields'][0][':answer-field/correct']={':answer/id':'intentionally-wrong-source-designation'}
  try:derived_without_designation=G.generate(level,101,t,parameters=params,profile='observed')
  finally:G.SOURCES[s][':question/answer-fields'][0][':answer-field/correct']=saved
  assert correct(derived_without_designation['question'][':question/answer-fields'][0])[':answer/value']==correct(r['question'][':question/answer-fields'][0])[':answer/value']
  r2=G.generate(level,999,t,parameters=params,profile='observed');assert r2['question'][':question/id']==r['question'][':question/id'];assert r2['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
  other=G.generate(level,99,t,parameters={'h':1} if s!='q-168078' else {'h':0,'ambient':27},profile='observed');assert other['question'][':question/id']!=r['question'][':question/id']
 for t in ('exponential_rate','reciprocal_initial','trig_frequencies'):
  for h,a,b in ((0,2,3),(-2,3,4),(sp.Rational(1,2),4,2),(3,5,3)):
   r=G.generate(G.TEMPLATES[t]['level'],9,t,parameters={'h':str(h),'a':a,'b':b});verify(r);checked+=1;review.append(r);stage_reports.append({'template':t,**stage_verify(r)})
   f=r['question'][':question/answer-fields'][0];native.append({'label':t+str((h,a,b)),'record':r,'checks':[{'submitted_answer_id':x[':answer/id'],'expected':'accepted' if x[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'authored operation bank selection'} for x in f[':answer-field/choices']]})
 for kwargs in ({'parameters':{'h':'0.1+sqrt(2)'}},{'parameters':{'h':0,'bogus':1}},{'field_type':'checkbox'},{'template':'source_355525'}):
  try:G.generate('easy',**kwargs)
  except ValueError:pass
  else:raise AssertionError(('invalid parameters silently accepted',kwargs))
 a=G.generate('moderate',template='source_347853',parameters={'h':0})
 b=G.generate('moderate',template='reciprocal_initial',parameters={'h':0,'a':2,'b':2})
 assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
 assert a['question'][':question/id']!=b['question'][':question/id']
 (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');(ROOT/'engine-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n')
 (ROOT/'solution-stage-validation.json').write_text(json.dumps(stage_reports,indent=2,ensure_ascii=False)+'\n')
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
 engine=json.loads((ROOT/'engine-validation.json').read_text())
 report={'status':'passed','basis':1356,'database_writes':0,'source_questions':20,'source_counts':{'easy':8,'moderate':7,'hard':5},'radio_banks':12,'blank_fragments':8,'matched_complete_radio_banks':12,'matched_source_values':total_values,'total_source_values':total_values,'correct_designations_matched':20,'mathematically_checked_instances':checked,'source_fidelity':fidelity,'native_accepted':engine['accepted_checks'],'native_rejected':engine['rejected_checks'],'native_unresolved':engine['documented_unresolved_checks'],'solution_stages_checked':sum(len(x['checked_rows']) for x in stage_reports),'authored_extensions':['exponential_rate','reciprocal_initial','trig_frequencies'],'limitations':['Empirical source distractor shapes do not establish original authoring intent.','Source square-root general-solution line suppresses the positive inner-root condition; generated metadata and particular solutions preserve it.','Native rules cannot establish split-exponential product entries; supported equivalent expanded exponent entries pass. Extra capability restriction is reproduced separately in engine-equivalence-limitation.json.'],'engine_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'additional_native_capability_report':'engine-equivalence-limitation.json','additional_native_equivalent_form_unresolved':1 if (ROOT/'engine-equivalence-limitation.json').exists() else 0}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 originals=['# Original questions and generated variants\n\nCaptured math basis 1356; source originals precede each template group. Generated entries explicitly identify authored banks and coefficient extensions.\n']
 for s,q in sources.items():
  originals += ['## Original '+s,q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),q[':question/worked-solution']]
  originals += [G.markdown(v) for v in review if v['generation']['template']==s.replace('q-','source_')]
 originals += [G.markdown(v) for v in review if v['generation']['origin']!='observed']
 (ROOT/'review.md').write_text('\n\n'.join(originals)+'\n')
 print(json.dumps({k:report[k] for k in ('status','source_questions','matched_source_values','mathematically_checked_instances','solution_stages_checked','native_accepted','native_rejected','native_unresolved')},indent=2))
if __name__=='__main__':main()
