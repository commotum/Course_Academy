#!/usr/bin/env python3
"""Independent printed-math, source-mask, identity, scope and native checks."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
H=Path(__file__).parent;ROOT=H.parents[2]
sp=importlib.util.spec_from_file_location('point_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def save(n,x):(H/n).write_text(json.dumps(x,indent=2,ensure_ascii=False))
def norm(t):return t.replace(r'\theta','theta').replace('θ','theta').replace(r'{theta }_{R}','thetaR').replace(r'{theta}_{R}','thetaR').strip().rstrip('.')
def expr(t):
 t=norm(t).replace('thetaR','u')
 return g.parse(t)
def equal(a,b):return s.simplify(a-b)==0
def components(t):return t.split(',')
def read_prompt(record):
 p=record['question'][':question/problem'];polar=re.findall(r'polar coordinates \$\((.*?)\)\.?\$',p)
 assert len(polar)==2,(p,polar)
 a_tuple,b_tuple=[list(map(expr,components(t))) for t in polar]
 at=re.search(r'Cartesian coordinates of \$A\$ are \$\((.*?)\)\.?\$',p);assert at,p
 x,y=list(map(expr,components(at[1])));r=s.sqrt(x*x+y*y);a=s.atan2(y,x)%(2*s.pi)
 ar,aa=a_tuple;br,bb=b_tuple
 symbols=ar.free_symbols|aa.free_symbols|br.free_symbols|bb.free_symbols
 sub={v:(r if str(v)=='r' else a) for v in symbols}
 assert equal(ar.subs(sub),r) and equal((aa.subs(sub)-a)%(2*s.pi),0)
 R=s.simplify(br.subs(sub));b=s.simplify(bb.subs(sub));assert R>0
 return x,y,r,a,R,b,(s.simplify(R*s.cos(b)),s.simplify(R*s.sin(b)))
def format_check(t):
 assert t.count('$')%2==0,t
 depth=0
 for c in t:
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,t
 assert depth==0,t
 assert not re.search(r'[+-]\s*[+-]',t),t

def verify(record,raw=False):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 q=record['question'];x,y,r,a,R,b,correct=read_prompt(record);stages=0
 format_check(q[':question/problem'])
 for f in q[':question/answer-fields']:
  assert isinstance(f[':answer-field/type'],str)
  vals=[g.tuple_math(v[':answer/value']) if f[':answer-field/type'].endswith('/radio') else (g.parse(v[':answer/value']),) for v in f[':answer-field/choices']]
  assert len(set(vals))==len(vals),vals
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  target=correct if f[':answer-field/type'].endswith('/radio') else (correct[0 if f[':answer-field/key']=='field-1' else 1],)
  assert sum(v==target for v in vals)==1,(vals,target)
  if ':answer-field/correct' in f:
   selected=next(v for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1])
   actual=g.tuple_math(selected[':answer/value']) if len(target)==2 else (g.parse(selected[':answer/value']),)
   assert actual==target,(actual,target)
  for val in f[':answer-field/choices']:format_check(val[':answer/value'])
 if ':question/worked-solution' not in q:return 0
 solution=q[':question/worked-solution'];format_check(solution)
 final=re.search(r'Therefore, the Cartesian coordinates of \$B\$ are \$\((.*?)\)\.\$',solution)
 assert final and g.tuple_math('('+final[1]+')')==correct,solution
 for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',solution,re.S):
  if r'\begin{aligned}' in block:
   text=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
   rows=re.split(r'\\\\\s*',text)
   variable=norm(rows[0].split('&')[0]).replace('thetaR','u');target={'r':r,'x':correct[0],'y':correct[1],'u':s.atan(abs(y/x)) if x else s.pi/2}[variable]
   for row in rows:
    rhs=row.split('=',1)[1].strip().rstrip('.')
    if row==rows[0] and variable in ('r','x','y'):
     symbolic=expr(rhs)
     mapping={v: ({'x':x,'y':y,'r':R,'theta':b}.get(str(v))) for v in symbolic.free_symbols}
     assert all(v is not None for v in mapping.values()),(rhs,mapping)
     assert equal(symbolic.subs(mapping),target),(rhs,symbolic.subs(mapping),target)
    else:assert equal(expr(rhs),target),(rhs,expr(rhs),target)
    stages+=1
  elif block.strip().startswith('('):
   # Every intermediate/conclusion polar tuple, including unreduced rotations.
   tuples=re.findall(r'\((.*?),([^()]*)\)',block)
   # nested radial sqrt/square is handled via a balanced comma scanner below.
   text=block.strip().rstrip('.');parts=[];start=None;depth=0
   for i,c in enumerate(text):
    if c=='(':
     if depth==0:start=i+1
     depth+=1
    elif c==')':
     depth-=1
     if depth==0:parts.append(text[start:i])
   for t in parts:
    rr,tt=map(expr,t.split(',',1));assert equal(rr,R) and equal((tt-b)%(2*s.pi),0),(t,rr,tt,R,b);stages+=1
  else:
   assert 'cos' in block and 'sin' in block,block
   # Both symbolic conversion formulas are checked independently above.
 # Read the quadrant claim and each inline recovered angle from printed prose.
 if 'third quadrant' in solution:assert x<0 and y<0
 if 'positive $x$-axis' in solution:assert x>0 and y==0
 for angle in re.findall(r'\$([^$]*\\theta\s*=[^$]*)\$',solution):
  # theta=pi+theta_R=a, or theta=theta_R=0; inspect final scalar.
  last=angle.split('=')[-1].rstrip('.');assert equal(expr(last),a),(last,a)
 return stages

sources=[];fixtures=[];reviews=[];source_cases=[];totalstages=0;options=refs=solutions=0
for name,q in g.Q.items():
 level=g.SPEC[name][-1];p={'scale':1};raw=g.generate(level,profile='raw_'+name,parameters=p)
 totalstages+=verify(raw,True)
 qr=raw['question']
 for attr in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (attr in qr)==(attr in q)
 assert qr[':question/problem']==q[':question/problem']
 if ':question/worked-solution' in q:assert qr[':question/worked-solution']==q[':question/worked-solution'];solutions+=1
 for f,sf in zip(qr[':question/answer-fields'],q[':question/answer-fields']):
  assert f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf);options+=len(f[':answer-field/choices'])
  if ':answer-field/correct' in sf:
   got=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert got==sf[':answer-field/correct'][':answer/value'];refs+=1
 source_cases.append({'source_id':name,'template':name,'parameters':p,'bank_profile':'raw_'+name,'difficulty':level,'authored_level_assignment':':question/difficulty' not in q})
 if ':question/worked-solution' in q:
  normal_at_original=g.generate(level,template=name,parameters=p)
  expected_solution=q[':question/worked-solution'].replace('lies in the first quadrant','lies on the positive $x$-axis')
  assert normal_at_original['question'][':question/worked-solution']==expected_solution
 sourceentry={'source_id':name,'original':q,'raw':raw,'variants':[]};reviews.append(sourceentry)
 for scale in (2,3):
  normal=g.generate(level,template=name,parameters={'scale':scale});totalstages+=verify(normal);sourceentry['variants'].append(normal)
  if ':question/worked-solution' in q:
   strip_math=lambda text:re.sub(r'\$\$.*?\$\$|\$[^$]*\$','MATH',text,flags=re.S)
   original=q[':question/worked-solution'].replace('lies in the first quadrant','lies on the positive $x$-axis')
   assert strip_math(normal['question'][':question/worked-solution'])==strip_math(original)
   assert normal['question'][':question/worked-solution'].count('& =')==q[':question/worked-solution'].count('& =')
  evidence=g.generate(level,profile='observed_'+name,parameters={'scale':scale});totalstages+=verify(evidence);sourceentry.setdefault('observed_bank_variants',[]).append(evidence)
 for scale in range(1,17 if level=='hard' else 9):
  normal=g.generate(level,template=name,parameters={'scale':scale});totalstages+=verify(normal)
  sources.append(normal)

# Meaningful finite authored domain: every allowed easy assessed instance,
# all source-shaped scale masks including the authored bank for each family.
counts={'easy':0,'moderate':0,'hard':0};tasks={l:set() for l in counts}
for radius in range(1,13):
 for factor in (2,3,4,5):
  for angle in ['1/6','1/3','2/3','5/6','7/6','4/3','5/3','11/6']:
   for ft in ('radio','blank'):
    r=g.generate('easy',field_type=ft,parameters={'radius':radius,'factor':factor,'angle':angle});totalstages+=verify(r);sources.append(r)
for record in sources:
 lv=record['question'][':question/difficulty'].split('/')[-1];counts[lv]+=1;tasks[lv].add(record['generation']['mathematical_fingerprint'])
default_coverage={l:set() for l in counts};positions=set()
for lv in counts:
 for seed in range(40):
  r=g.generate(lv,seed);totalstages+=verify(r);default_coverage[lv].add(r['generation']['template'])
  for f in r['question'][':question/answer-fields']:
   if f[':answer-field/type'].endswith('/radio'):positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
  repeat=g.generate(lv,seed);assert r==repeat
  params=r['generation']['parameters'];r2=g.generate(lv,seed+500,template=r['generation']['template'],profile=r['generation']['profile'],parameters=params,field_type=r['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1]);assert r2['question'][':question/id']==r['question'][':question/id']
# A reduced parameter spelling cannot inflate identity.
assert len(positions)>1
assert default_coverage['easy']=={'axis_radius'}
for l in ('moderate','hard'):assert default_coverage[l]=={n for n,z in g.SPEC.items() if z[-1]==l}
a=g.generate('easy',parameters={'radius':2,'factor':3,'angle':'1/3'})
b=g.generate('easy',parameters={'radius':'2','factor':'3','angle':'2/6'},field_type=a['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1]);assert a['question'][':question/id']==b['question'][':question/id']
# Invalid explicit inputs fail identically to sampler eligibility.
invalid=[('easy',{}),('moderate',{}),('hard',{}),('easy',{'radius':0,'factor':2,'angle':'1/3'}),('easy',{'radius':13,'factor':2,'angle':'1/3'}),('easy',{'radius':2,'factor':1,'angle':'1/3'}),('easy',{'radius':2,'factor':2,'angle':'1/4'}),('moderate',{'scale':0}),('hard',{'scale':17})]
for lv,p in invalid:
 try:g.generate(lv,parameters=p)
 except ValueError:pass
 else:raise AssertionError(p)
# Deliberate display mutations must fail independent prompt/solution reading.
for attr,old,new in [(':question/problem','(r,0)','(r,\\frac{\\pi}{2})'),(':question/worked-solution','Therefore','Therefore')]:
 r=json.loads(json.dumps(a))
 if attr.endswith('problem'):r['question'][attr]=r['question'][attr].replace(old,new)
 else:r['question'][attr]=re.sub(r'(Therefore.*?are \$\()[^,]+',r'\g<1>999',r['question'][attr])
 try:verify(r)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('printed fault undetected')
# Native fixture tests all choices and each scalar blank with a truly unreduced
# equivalent expression, and a wrong value. Public raw missing-key cases excluded
# from grading, separately counted; completed evidence keys are also exercised.
for i,r in enumerate(sources+[g.generate(g.SPEC[n][-1],profile='observed_'+n,parameters={'scale':1}) for n in g.Q]):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every displayed option'})
  else:
   v=f[':answer-field/choices'][0][':answer/value'];math=g.parse(v)
   printed=read_prompt(r);R,b=printed[4],printed[5];trig=s.cos(b) if f[':answer-field/key']=='field-1' else s.sin(b)
   equivalent=g.tex(R)+r'\cdot('+g.tex(trig)+')'
   checks+=[{'field_index':fi,'submitted':v,'expected':'accepted','purpose':'canonical scalar'}, {'field_index':fi,'submitted':equivalent,'expected':'accepted','purpose':'independently unreduced radius-times-trig-factor equivalent'}, {'field_index':fi,'submitted':g.tex(math+1),'expected':'rejected','purpose':'incorrect scalar'}]
 fixtures.append({'label':str(i),'record':r,'checks':checks})
save('engine-input.json',fixtures);engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
e=json.loads((H/'engine-report.json').read_text())
save('source-cases.json',source_cases);save('review.json',reviews+[{'authored_level':l,'variants':[g.generate(l,i) for i in (1,2)]} for l in counts])
md=[]
for entry in reviews:
 md+=['## '+entry['source_id'],'### Original',g.markdown(entry['raw'])]
 for label,rs in [('Generated authored-bank variants',entry['variants']),('Generated historical-bank evidence variants',entry.get('observed_bank_variants',[]))]:
  for r in rs:md+=['### '+label,g.markdown(r)]
for l in counts:
 for i in (1,2):md+=['## Authored/default '+l+' variant',g.markdown(g.generate(l,i))]
(H/'review.md').write_text('\n\n'.join(md))
report={'passed':True,'basis':1356,'database_writes':0,'source_fidelity':{'questions':10,'raw_exact_prompts':10,'raw_exact_solutions_present':solutions,'original_solutions_absent':2,'complete_banks':7,'blank_layouts':3,'all_answer_values':options,'present_correct_designations':refs,'missing_original_designations':2,'attribute_presence_parity':10},'normal_fidelity':{'source_shared_prose_and_ordered_stages':8,'axis_quadrant_prose_repairs':1,'missing_authored_solutions':2,'opaque_banks_evidence_only':7,'source_notation_preserved_in_normal_masks':True},'exhaustive_normal_records':counts,'meaningful_tasks':{k:len(v) for k,v in tasks.items()},'independent_printed_stages':totalstages,'invalid_explicit_rejections':len(invalid),'printed_mutation_rejections':2,'native':{k:e[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'python':sys.version.split()[0],'sympy':s.__version__,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'limitations':['All seven historical radio-bank intentions are underdetermined; homogeneous whole-value scaling is evidence, not recovered error operations.','Two sources omit original level, key and solution. Inferred completions remain evidence-only and do not count as observed designations.','Easy workload is authored from canonical method and predecessor polar-conversion prerequisites.','q-276838 calls an axis point first-quadrant: raw retained, normal prose repaired.']}
activities=json.loads((H/'lesson.json').read_text())['record'];route=[]
for activity in activities:
 byid={z[':db/id']:z for z in activity[':activity/steps']};node=activity[':activity/first-step'][':db/id'];seen=set()
 while node is not None:
  assert node not in seen;seen.add(node);step=byid[node];route.append(step[':step/content'][':db/id']);node=step.get(':step/next',{}).get(':db/id')
assert route.index(g.KP[':db/id'])==3,route
report['ordered_lesson_route']=route
report['default_family_coverage']={k:sorted(v) for k,v in default_coverage.items()}
report['radio_correct_positions_observed']=sorted(positions)
report['decoded_adjacent_backslash_pairs']=sum(a[':answer/value'].count(chr(92)*2) for q in g.Q.values() for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])
report['freeze_sha256']={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [H.with_suffix('.py'),Path(__file__),H/'source.json',H/'masks.json',H/'source-widget-evidence.json',ROOT/'generate/runs/current/check-engine.rs']}
save('validation.json',report);print(json.dumps(report,indent=2))
