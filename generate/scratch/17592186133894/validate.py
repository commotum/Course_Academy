#!/usr/bin/env python3
"""Fail-closed displayed-math readback, frozen-source fidelity, native grading.
Private parser is independent of generator formulas. Raw known source mistakes
are evidence failures, explicitly ineligible; normal records must pass fully.
"""
import copy, importlib.util, json, re, subprocess, sys, hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(ROOT.with_suffix('.py'),'space_generator');p=load(ROOT/'display-parser.py','independent_display')
x,y,z,t=p.x,p.y,p.z,p.t
def same(a,b):
 difference=s.sympify(a)-s.sympify(b)
 replacements={v:v.rewrite(s.exp) for v in s.preorder_traversal(difference) if v.func in (s.sinh,s.cosh)}
 difference=s.expand(difference.xreplace(replacements))
 if difference==0:return True
 variable=s.Symbol('transcendental_e');powers={v:variable**v.args[0] for v in s.preorder_traversal(difference) if v.func==s.exp and v.args[0].is_Integer};powers[s.E]=variable
 try:return s.Poly(s.fraction(s.cancel(difference.xreplace(powers)))[0],variable,domain=s.QQ).is_zero
 except (s.PolynomialError,s.CoercionFailed):return s.simplify(s.trigsimp(difference))==0
def vecsame(a,b):return len(a)==len(b) and all(same(v,w) for v,w in zip(a,b))
def blocks(text):return re.findall(r'\$\$(.*?)\$\$',text,re.S)
def clean(v):return v.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').strip().rstrip('.,')
def rows(v):return [clean(q).split('=',1)[1].strip() for q in v.split(r'\\') if '=' in q]
def group(raw,start):
 assert raw[start]=='{';depth=1;end=start+1
 while depth:
  depth+=(raw[end]=='{')-(raw[end]=='}');end+=1
 return raw[start+1:end-1],end
def limits(raw,start):
 assert raw[start]=='_';a,end=group(raw,start+1);assert raw[end]=='^';b,end=group(raw,end+1);return a,b,end
def outer_groups(raw):
 result=[];pos=0
 while pos<len(raw):
  if raw[pos]=='+':pos+=1
  assert raw.startswith(r'\left(',pos),raw[pos:]
  start=pos+len(r'\left(');depth=1;pos=start
  while depth:
   assert pos<len(raw)
   if raw.startswith(r'\left(',pos):depth+=1;pos+=len(r'\left(')
   elif raw.startswith(r'\right)',pos):depth-=1;end=pos;pos+=len(r'\right)')
   else:pos+=1
  result.append(raw[start:end])
 return result
def prompt(rec):
 text=rec['question'][':question/problem'];field=re.search(r'F\(x,\s*y,\s*z\)\s*=([^$]+)',text)[1];curve=re.search(r'r\(t\)\s*=([^$]+)',text)[1]
 F=tuple(p.vector(field));r=tuple(p.vector(curve));limit=re.search(r't\s*(?:\\in|∈)\s*\[(.*?)\]',text)[1]
 a,b=[p.scalar(q) for q in limit.split(',')];assert a<b
 f=tuple(s.simplify(v.subs(dict(zip((x,y,z),r)),simultaneous=True)) for v in F);d=tuple(s.diff(v,t) for v in r);products=tuple(s.simplify(v*w) for v,w in zip(f,d));I=s.simplify(s.trigsimp(sum(products)));anti=s.integrate(I,t);Q=s.simplify(anti.subs(t,b)-anti.subs(t,a))
 return dict(F=F,r=r,f=f,d=d,products=products,I=I,a=a,b=b,Q=Q)
def formatting(text):
 assert text.count('$')%2==0
 depth=0
 for ch in text:
  if ch=='{':depth+=1
  if ch=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert not any(q in text for q in ('+-','--','{{selection}}'))
def verify_normal(rec):
 q=rec['question'];m=prompt(rec);solution=q[':question/worked-solution'];formatting(q[':question/problem']);formatting(solution)
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 bs=blocks(solution);assert len(bs)==6
 assert bs[0].strip()==r'\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.'
 actual=[p.scalar(v) for v in re.split(r',\\qquad\s*',bs[1].strip().rstrip('.')) for v in [v.split('=',1)[1]]];assert vecsame(actual,m['r'])
 rs=rows(bs[2]);assert len(rs)==3
 for index,v in enumerate(rs):
  shown=tuple(p.vector(v));shown=tuple(q.subs(dict(zip((x,y,z),m['r'])),simultaneous=True) for q in shown) if index==0 else shown
  assert vecsame(shown,m['f']),(v,m['f'])
 rs=rows(bs[3]);assert len(rs)==3
 assert rs[0]=='+'.join(r'\frac{\mathrm{d}'+q+r'}{\mathrm{d}t}\,'+b for q,b in zip('xyz','ijk'))
 args=re.findall(r'\\frac\{\\mathrm\{d\}\}\{\\mathrm\{d\}t\}\\left\((.*?)\\right\)\\,([ijk])',rs[1])
 assert [b for _,b in args]==list('ijk') and len(args)==3
 assert vecsame([p.scalar(v) for v,_ in args],m['r'])
 assert vecsame([s.diff(p.scalar(v),t) for v,_ in args],m['d'])
 assert vecsame(p.vector(rs[2]),m['d'])
 rs=rows(bs[4]);assert len(rs)==4
 # Read both actual vectors in the printed dot product, not its total only.
 first=re.match(r'\\left\((.*)\\right\)\\cdot\\left\((.*)\\right\)$',rs[0]);assert first
 assert vecsame(p.vector(first[1]),m['f']) and vecsame(p.vector(first[2]),m['d'])
 groups=re.findall(r'\\left\(\\left\((.*?)\\right\)\\cdot\\left\((.*?)\\right\)\\right\)',rs[1]);assert len(groups)==3
 for (u,v),f,d in zip(groups,m['f'],m['d']):assert same(p.scalar(u),f) and same(p.scalar(v),d)
 for raw in rs[1:]:assert same(p.scalar(raw),m['I']),(raw,m['I'])
 # Separate first distributed terms before checking collection.
 distributed=outer_groups(rs[2]);assert len(distributed)==sum(len(s.Add.make_args(s.expand(v))) for v in m['products'])
 actual=[p.scalar(v) for v in distributed];expected=[v for prod in m['products'] for v in s.Add.make_args(s.expand(prod))]
 assert all(same(a,b) for a,b in zip(actual,expected))
 rs=rows(bs[5]);assert len(rs)==6
 for index,raw in enumerate(rs[:2]):
  assert raw.startswith(r'\int_');lo,hi,end=limits(raw,len(r'\int'));assert raw.endswith(r'\,\mathrm{d}t');body=raw[end:-len(r'\,\mathrm{d}t')]
  assert same(p.scalar(lo),m['a']) and same(p.scalar(hi),m['b'])
  if index==0:assert body==r'F(r(t))\cdot r^{\prime}(t)'
  else:assert same(p.scalar(body),m['I'])
 assert rs[2].startswith(r'\left[');anti_raw,limit=rs[2][len(r'\left['):].split(r'\right]',1);lo,hi,end=limits(limit,0);assert end==len(limit)
 anti=p.scalar(anti_raw);assert same(s.diff(anti,t),m['I'])
 assert same(p.scalar(lo),m['a']) and same(p.scalar(hi),m['b'])
 # Read each unevaluated signed endpoint term and each evaluated term separately.
 terms=list(s.Add.make_args(s.expand(anti)));actual_sub=outer_groups(rs[3]);actual_eval=outer_groups(rs[4]);assert len(actual_sub)==len(actual_eval)==2*len(terms)
 expected=[value for term in terms for value in (term.subs(t,m['b']),-term.subs(t,m['a']))]
 for raw,w in zip(actual_sub,expected):assert same(p.scalar(raw),w),(raw,w)
 for raw,w in zip(actual_eval,expected):assert same(p.scalar(raw),w),(raw,w)
 assert same(p.scalar(rs[5]),m['Q'])
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 vals=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==5
 assert all(not same(a,b) for index,a in enumerate(vals) for b in vals[:index])
 correct=[idx for idx,v in enumerate(vals) if same(v,m['Q'])];assert len(correct)==1
 assert f[':answer-field/correct']==[':answer/id',f[':answer-field/choices'][correct[0]][':answer/id']]
 # Recompute all operations from the actual printed prompt, not metadata.
 P=m['products'];Q=m['Q'];a,b=m['a'],m['b'];name=rec['generation']['template']
 def integral(v):return s.simplify(s.integrate(v,(t,a,b)))
 if name in ('constant_affine','diagonal_power'):want=[Q,-Q,*[integral(sum(P)-v) for v in P]]
 elif name in ('product','mixed_polynomial','exp_cancel_xy','exp_cancel_yz'):want=[Q,*[integral(sum(P)-v) for v in P],integral(sum(m['f']))]
 elif name=='trig_cancel':
  A=s.simplify(-m['r'][0]/s.sin(t));want=[Q,-Q,2*Q,A*A*(s.sin(b)-s.sin(a))/2,-A*A*s.cos(2*b)/4]
 elif name=='radical_power':R=integral(P[0]+P[1]);Z=integral(P[2]);want=[Q,Z,R,R+Z/2,-Q]
 elif name=='helix_root':C=s.simplify(m['r'][2]/s.sqrt(t));want=[Q,0,2*Q,C*C*(s.sqrt(b)-s.sqrt(a)),C*C*(b*b-a*a)/4]
 elif name=='quotient_exp':
  C=s.diff(m['r'][2],t);k=s.simplify(s.diff(m['r'][0],t)/m['r'][0]);l=s.simplify(s.diff(m['r'][1],t)/m['r'][1]);want=[Q,C*(b-a),integral(P[0]+P[1]),integral(C*k*t*s.exp(-k*t)+P[1]+C),integral(C*k*t*s.exp(-k*t)+C*l*t*s.exp(-l*t)+C)]
 else:raise AssertionError('Unrecognized displayed family')
 assert all(sum(same(v,w) for v in vals)==1 for w in want)
 assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
 return m

def engine_case(rec,label):
 f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return dict(label=label,record=rec,checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==correct else 'rejected',purpose='native radio selection') for a in f[':answer-field/choices']])
def source_readback(rec):
 """Parse every original mathematical stage; return only observed defects."""
 m=prompt(rec);text=rec['question'].get(':question/worked-solution');issues=[];counts={}
 if text is None:return {'issues':['source solution absent'],'counts':counts}
 bs=blocks(text);assert len(bs)==6;formatting(text)
 coordinates=bs[1].strip().rstrip('.').replace(r'\,','').split(',')
 assert vecsame([p.scalar(q.split('=',1)[1]) for q in coordinates],m['r']);counts['coordinate_components']=3
 for raw in clean(bs[2]).split('=')[1:]:
  # The row separator is layout, not a mathematical component.
  raw=raw.split(r'\\')[0].strip();v=tuple(p.vector(raw));v=tuple(q.subs(dict(zip((x,y,z),m['r'])),simultaneous=True) for q in v)
  assert vecsame(v,m['f']),(raw,m['f'])
 counts['substitution_rows']=len(clean(bs[2]).split('='))-1
 dr=rows(bs[3]);assert len(dr)==3
 first=dr[0]
 for key,value in zip('xyz',m['d']):first=first.replace(r'\frac{\text{d}'+key+r'}{\text{d}t}','('+g.tex(value)+')')
 assert vecsame(p.vector(first),m['d']);counts['formal_coordinate_derivatives']=3
 operator=dr[1];pattern=r'\frac{\text{d}}{\text{d}t}('
 while pattern in operator:
  at=operator.index(pattern);start=at+len(pattern);end=start;depth=1
  while depth:depth+=(operator[end]=='(')-(operator[end]==')');end+=1
  arg=p.scalar(operator[start:end-1]);operator=operator[:at]+'('+g.tex(s.diff(arg,t))+')'+operator[end:]
 if not vecsame(p.vector(operator),m['d']):issues.append('formal third derivative basis j instead of k')
 if not vecsame(p.vector(dr[2]),m['d']):issues.append('evaluated derivative vector uses x instead of t')
 counts['formal_argument_derivatives']=3;counts['evaluated_derivative_components']=3
 dot=rows(bs[4]);first=dot[0];a,b=first.split(r'\cdot',1);actualF=p.vector(a);actualD=p.vector(b)
 assert vecsame(actualF,m['f'])
 if not vecsame(actualD,m['d']):issues.append('dot-product derivative vector uses x instead of t')
 for raw in dot[1:]:assert same(p.scalar(raw),m['I']),(raw,m['I'])
 counts['dot_product_components']=3;counts['distributed_collected_rows']=len(dot)-1
 final=rows(bs[5]);primitive=None;endpoint=0
 for raw in final:
  if r'\int' in raw:
   raw=re.sub(r'\{\\int\s*\}',r'\\int',raw);assert raw.startswith(r'\int_');lo,hi,end=limits(raw,len(r'\int'))
   assert same(p.scalar(lo),m['a']) and same(p.scalar(hi),m['b'])
   body=re.sub(r'\\,?(?:\\text\{d\}t|dt)$','',raw[end:]).strip().removesuffix(r'\,')
   if 'F(r(t))' not in body:assert same(p.scalar(body),m['I'])
  elif '|' in raw or '[' in raw:
   before,tail=raw.rsplit('_',1);lo,hi,end=limits('_'+tail,0);assert end==len('_'+tail)
   before=before.replace('|','').replace('[','').replace(']','')
   # {|} is layout around the evaluation bar; remove resulting empty group.
   before=before.replace('{}','');primitive=p.scalar(before)
   assert same(s.diff(primitive,t),m['I']);assert same(p.scalar(lo),m['a']) and same(p.scalar(hi),m['b'])
  else:assert same(p.scalar(raw),m['Q']);endpoint+=1
 assert primitive is not None
 counts['primitive_rows']=1;counts['endpoint_and_final_rows']=endpoint
 return {'issues':issues,'counts':counts}
def dump(name,v):(ROOT/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def run():
 original=json.loads((ROOT.parents[1]/'runs/current/sources/17592186133894.json').read_text());assert original==g.CAPTURE
 sourcecases=[];reviews=[];native=[];bankvalues=0;correctrefs=0;rawexact=0;sol_exact=0
 anomalies=[]
 for name,source_id in g.OBSERVED.items():
  old=g.OLDS[source_id];case={'source_id':old[':question/math-academy-id'],'source_db_id':source_id,'level':'hard','template':name,'parameters':{'lift':1},'bank_profile':'observed:'+name};sourcecases.append(case)
  rec=g.generate('hard',template=name,parameters=case['parameters'],profile=case['bank_profile']);q=rec['question'];of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'];rawexact+=1
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in old)
  assert (':answer-field/correct' in of)==(':answer-field/correct' in nf)
  if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];sol_exact+=1
  sv=[p.scalar(v[':answer/value']) for v in of[':answer-field/choices']];nv=[p.scalar(v[':answer/value']) for v in nf[':answer-field/choices']]
  assert len(sv)==len(nv)==5 and all(sum(same(v,w) for w in nv)==1 for v in sv);bankvalues+=5
  m=prompt(rec);assert sum(same(v,m['Q']) for v in nv)==1
  if ':answer-field/correct' in of:
   correctrefs+=1;correct=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert same(p.scalar(correct),p.scalar(of[':answer-field/correct'][':answer/value']));assert same(p.scalar(correct),m['Q']);native.append(engine_case(rec,'observed/'+name))
  else:
   fixture=copy.deepcopy(rec);ff=fixture['question'][':question/answer-fields'][0];aa=next(v for v in ff[':answer-field/choices'] if same(p.scalar(v[':answer/value']),m['Q']));ff[':answer-field/correct']=[':answer/id',aa[':answer/id']]
   native.append(engine_case(fixture,'INFERRED-GRADING-FIXTURE/'+name))
  text=old.get(':question/worked-solution','');errors=[]
  if re.search(r'\\frac\{\\text\{d\}\}\{\\text\{d\}t\}\([^\n]*?\)j\s*\\\\',text):errors.append('third formal derivative uses j instead of k')
  if '⁡x' in text:errors.append('secant derivative/dot-product vector uses x instead of t')
  if not text:errors+=['missing worked solution','missing correct designation','missing difficulty','non-smooth sqrt parameterization at t=0; convergent improper integral']
  audit=source_readback(rec)
  assert len(audit['issues'])==(3 if name=='trig_cancel' else 1 if name in ('product','mixed_polynomial','exp_cancel_xy','exp_cancel_yz','radical_power','helix_root') else 0),audit
  anomalies.append({'source_id':case['source_id'],'issues':errors,'independent_display_readback':audit,'bank_intent':'opaque historical scalar expressions; linear lift only; ineligible','independent_value':g.tex(m['Q'])})
  reviews.append({'label':'ORIGINAL PUBLIC EVIDENCE — INELIGIBLE','record':rec})
  lifted=g.generate('hard',template=name,parameters={'lift':2},profile=case['bank_profile']);lift_m=prompt(lifted);assert same(lift_m['Q'],2*m['Q']);reviews.append({'label':'GENERATED HISTORICAL LINEAR-LIFT VARIANT — INELIGIBLE','record':lifted})
  for idx in range(2):
   normal=g.generate('hard',seed=410+idx,template=name);verify_normal(normal);reviews.append({'label':'GENERATED METHOD-BANK VARIANT','record':normal});native.append(engine_case(normal,name+'/'+str(idx)))
 for level in ('easy','moderate'):
  for seed in (8,17):
   rec=g.generate(level,seed);verify_normal(rec);reviews.append({'label':'GENERATED AUTHORED '+level.upper(),'record':rec});native.append(engine_case(rec,level+'/'+str(seed)))
 coverage={};math_count=0
 for name,level in g.TEMPLATES.items():
  tasks=set();positions=set()
  for seed in range(24):
   rec=g.generate(level,seed=700+seed,template=name);verify_normal(rec);tasks.add(rec['generation']['mathematical_fingerprint']);math_count+=1
   pms=rec['generation']['parameters'];other=g.generate(level,seed=99,template=name,parameters=pms);assert other['question'][':question/id']==rec['question'][':question/id'];assert other['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
   ff=rec['question'][':question/answer-fields'][0];positions.add(next(i for i,v in enumerate(ff[':answer-field/choices']) if v[':answer/id']==ff[':answer-field/correct'][1]))
  assert len(positions)>1
  coverage[name]={'sampled_tasks':len(tasks),'records':24}
  print('Displayed mathematics verified: '+name,flush=True)
 # Explicit API rejects level-workload violations rather than resampling them.
 invalid_count=0
 for name,level in g.TEMPLATES.items():
  par=dict(g.generate(level,seed=711,template=name)['generation']['parameters'])
  for value in (0,6 if level=='easy' else 5 if level=='moderate' else 4):
   bad=dict(par,A=value)
   try:g.generate(level,template=name,parameters=bad)
   except ValueError:invalid_count+=1
   else:raise AssertionError('Explicit level/zero bound silently bypassed')
 # Whole-bank rejections at genuine source parameters are visible, not repaired
 # by replacing individual distractors with the first valid pooled value.
 rejected_banks=[]
 for name in ('trig_cancel','quotient_exp'):
  try:g.generate('hard',template=name,parameters=g.SOURCE_PARAMETERS[name])
  except ValueError as exc:
   assert str(exc)=='Whole-bank collision';rejected_banks.append(name)
  else:raise AssertionError('Equivalent wrong choices were allowed')
 # Native numeric-comparator probes supplement, rather than replace, radio checks.
 for item in reviews:
  rec=item['record']
  if rec['generation']['evidence_only']:continue
  copied=copy.deepcopy(rec);field=copied['question'][':question/answer-fields'][0];correct=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);field[':answer-field/type']=':answer-field.type/blank';field[':answer-field/choices']=[correct];copied['question'][':question/problem']+=' Answer: {{selection}}'
  value=p.scalar(correct[':answer/value']);unreduced='('+correct[':answer/value']+')+('+g.tex(s.Integer(3))+')-3'
  native.append({'label':'scalar-equivalence-probe/'+rec['generation']['template'],'record':copied,'checks':[{'submitted':correct[':answer/value'],'expected':'accepted','purpose':'canonical scalar'},{'submitted':unreduced,'expected':'accepted','purpose':'unreduced algebraically equivalent scalar'},{'submitted':'('+correct[':answer/value']+')+1','expected':'rejected','purpose':'incorrect scalar'}]})
 dump('source-cases.json',sourcecases);dump('review.json',reviews);dump('source-anomalies.json',anomalies);dump('engine-input.json',native)
 subprocess.run([str(ROOT.parents[1]/'runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
 report=json.loads((ROOT/'engine-validation.json').read_text());assert report['documented_unresolved_checks']==0
 summary={'status':'normal output passed; historical defects retained in ineligible evidence; frozen at step 7','source_questions':8,'raw_exact_prompts':rawexact,'raw_exact_worked_solutions':sol_exact,'worked_solution_denominator':7,'source_banks':8,'source_values':bankvalues,'source_designations_matched':correctrefs,'source_designation_denominator':7,'unrated_missing_designation':1,'inferred_native_grading_fixture':1,'source_solution_defect_count':6,'normal_readback_records':math_count+20,'explicit_bound_rejections':invalid_count,'whole_bank_collision_rejections':rejected_banks,'all_supported_templates':coverage,'source_anomalies':anomalies,'native_grading':{k:v for k,v in report.items() if k!='records'},'dependency_versions':{'python':sys.version.split()[0],'sympy':s.__version__},'database_writes':0,'plots':'none'}
 dump('validation.json',summary)
 (ROOT/'review.md').write_text('# Space-curve vector-field evaluation review\n\nBasis 1356; raw historical evidence is explicitly ineligible. Generated defaults use direct substitution, differentiation, dot product and definite integration.\n\n'+'\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in reviews)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k not in ('source_anomalies','all_supported_templates')},indent=2))
if __name__=='__main__':run()
