#!/usr/bin/env python3
"""Fail on independent displayed mathematics, fidelity, native grading or shape errors."""
import hashlib, importlib.util, json, re, subprocess, sys, uuid
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
T=g.T
def group(s,i):
 assert s[i]=='{';depth=1;j=i+1
 while depth:
  depth+=(s[j]=='{')-(s[j]=='}');j+=1
 return s[i+1:j-1],j
def convert(s):
 s=s.replace('π',r'\pi').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 s=re.sub(re.escape('\\operatorname')+r'\{(sin|cos|tan)\}',r'\1',s)
 for token,name in ((r'\sin','sin'),(r'\cos','cos'),(r'\tan','tan')):s=s.replace(token,name)
 s=re.sub(r'(sin|cos|tan)t',r'\1(t)',s)
 for cmd in (r'\frac',r'\dfrac',r'\sqrt'):
  while cmd in s:
   start=s.index(cmd);i=start+len(cmd);a,i=group(s,i)
   if cmd.endswith('sqrt'):replacement='sqrt('+convert(a)+')'
   else:b,i=group(s,i);replacement='(('+convert(a)+')/('+convert(b)+'))'
   s=s[:start]+replacement+s[i:]
 s=s.replace(r'\pi','pi').replace('{','(').replace('}',')').replace('^','**').replace('[','(').replace(']',')')
 s=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','E',s)
 return s
def read(s):
 return parse_expr(convert(s.strip().rstrip('.,')),local_dict={'t':T,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'pi':sp.pi,'E':sp.E},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def eq(a,b):return sp.simplify(a-b)==0
def requested(record):
 q=record['question'];prompt=q[':question/problem'];m=re.search(r'x\s*=\s*(.*?),\s*(?:\\,)?y\s*=\s*(.*?),',prompt,re.S);assert m,prompt
 x,y=map(read,m.groups());return x,y,sp.diff(x,T),sp.diff(y,T)
def displayed_domain(record):
 prompt=record['question'][':question/problem']
 m=re.search(r'x\s*=\s*(.*?),\s*(?:\\,)?y\s*=\s*(.*?),',prompt,re.S)
 tail=prompt[m.end():].split('$$')[0].split('$')[0].strip().replace(r'\,','').rstrip('.')
 if '∞' in tail or r'\infty' in tail:
  assert '-' in tail and tail.count('∞')+tail.count(r'\infty')==2
  return sp.S.Reals
 match=re.fullmatch(r'(.*?)'+re.escape(r'\le')+r'\s*t\s*('+re.escape(r'\le')+r'|<)\s*(.*)',tail)
 assert match,tail
 lo,op,hi=match.groups();return sp.Interval(read(lo),read(hi),right_open=op=='<')
def mathcheck(record):
 q=record['question'];meta=record['generation'];template=meta['template'];p=g.guards(template,meta['parameters']);x,y,dx,dy=requested(record)
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==17592186083278
 expected_fields=2 if template in ('polynomial_two','spiral_cos','spiral_sin','paired_cubics') or (template=='circle_vertical' and meta['profile']=='raw') else 1
 assert len(q[':question/answer-fields'])==expected_fields
 expected_kind=':answer-field.type/'+('blank' if template in ('polynomial_two','spiral_cos','spiral_sin','paired_cubics') else 'radio')
 assert all(f[':answer-field/type']==expected_kind for f in q[':question/answer-fields'])
 keys=[f[':answer-field/key'] for f in q[':question/answer-fields']]
 assert len(set(keys))==len(keys) or (template=='circle_vertical' and meta['profile']=='raw')
 roots=[g.e(z) for z in meta['roots']];orientation='vertical' if 'is vertical' in q[':question/problem'] else 'horizontal';assert orientation==meta['orientation']
 target=dy if orientation=='horizontal' else dx;other=dx if orientation=='horizontal' else dy
 assert all(eq(target.subs(T,z),0) and not eq(other.subs(T,z),0) for z in roots)
 domain=displayed_domain(record);assert domain==g.mathematics(template,p)[-1]
 # Independent completeness: solve the displayed derivative, restricting the displayed domain.
 if target.has(sp.sin,sp.cos):
  if template.startswith('circle'):
   expected=sp.solveset(target,T,domain=domain)
   assert expected==sp.FiniteSet(*roots),(expected,roots)
  else:
   # sin +/- cos with nonzero exp/scale; enumerate an independently derived quarter-angle grid.
   expected=[j*sp.pi/4 for j in range(9) if eq(target.subs(T,j*sp.pi/4),0) and not eq(other.subs(T,j*sp.pi/4),0)]
   assert sp.FiniteSet(*roots)==sp.FiniteSet(*expected)
   periodic=sp.expand_trig(sp.simplify(target/sp.exp(T)))
   assert sp.simplify(periodic-(sp.expand(periodic).coeff(sp.sin(T))*sp.sin(T)+sp.expand(periodic).coeff(sp.cos(T))*sp.cos(T)))==0
 else:
  expected=sp.solveset(target,T,domain=domain)
  assert expected==sp.FiniteSet(*roots),(expected,roots)
 # Read every field's actual displayed values, not UUID correctness alone.
 for f in q[':question/answer-fields']:
  uuid.UUID(f[':answer-field/id']);kind=f[':answer-field/type'];choices=f[':answer-field/choices']
  assert len({a[':answer/id'] for a in choices})==len(choices)
  parsed=[]
  for a in choices:
   uuid.UUID(a[':answer/id'])
   if kind.endswith('/blank'):obj=[read(a[':answer/value'])]
   elif a[':answer/type'].endswith('/text'):obj=[read(v) for v in re.findall(r'\$t\s*=\s*(.*?)\$',a[':answer/value'])]
   else:obj=[read(a[':answer/value'].split('=')[1])]
   assert obj
   parsed.append(sp.FiniteSet(*obj))
  assert len(set(parsed))==len(parsed)
  if ':answer-field/correct' in f:
   selected=next(i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1])
   if kind.endswith('/blank'):assert parsed[selected]==sp.FiniteSet(roots[int(f[':answer-field/key'].split('-')[-1])-1])
   else:assert parsed[selected]==sp.FiniteSet(*roots) and sum(v==sp.FiniteSet(*roots) for v in parsed)==1
  if kind.endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 solution=q.get(':question/worked-solution')
 if solution:
  bs=g.blocks(solution)
  assert len(bs)==(4 if len(roots)==2 or template=='line_cubic' else 3)
  # First formal slope block and complete derivative block are mandatory.
  assert 'm=' in bs[0] and ('frac' in bs[0])
  parts=bs[1].split(r'\,') if r'\,' in bs[1] else bs[1].split(r'\qquad')
  assert len(parts)==2
  assert eq(read(parts[0].split('=')[1]),dx)
  assert eq(read(parts[1].split('=')[1]),dy)
  rows=bs[2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\')
  # Ensure the factor/trig-solving operative chain cannot disappear while equal final values survive.
  required=6 if template.startswith('spiral') else 3 if template in ('polynomial_two','paired_cubics','line_cubic') else 1
  assert len(rows)==required,(template,rows)
  for ri,row in enumerate(rows):
   row=row.replace('&','').strip().rstrip('.')
   if '⟹' in row:
    left,final=row.split('⟹');assert eq(read(left.split('=')[0]),target);listed=[read(z) for z in final.split('=')[1].split(',')];assert sp.FiniteSet(*listed)==sp.FiniteSet(*roots)
   elif row.split('=')[0].strip()=='t':
    listed=[read(z) for z in row.split('=')[1].split(',')];assert sp.FiniteSet(*listed)==sp.FiniteSet(*roots)
   else:
    left,right=row.split('=');lhs=read(left);rhs=read(right)
    assert all(eq((lhs-rhs).subs(T,z),0) for z in roots)
    if ri==0:assert eq(lhs,target)
    if ri==1 and template in ('polynomial_two','paired_cubics','line_cubic'):assert eq(lhs,target)
  if len(bs)==4:
   rows=bs[3].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==len(roots)
   for row,z in zip(rows,roots):
    row=row.replace('&','').strip().rstrip(',');parts=row.split('=');arg=re.search(r'\((.*?)\)',parts[0]).group(1);assert eq(read(arg),z)
    values=[read(part.split(r'\ne')[0]) for part in parts[1:]]
    assert all(eq(v,other.subs(T,z)) for v in values),(template,row,values,other.subs(T,z))
    assert all(not eq(v,0) for v in values)
  else:
   note=re.search(r'Note that \$\{([xy])\}\^\{′\}\((.*?)\)=(.*?)'+re.escape(r'\ne')+r' 0\.\$',solution)
   assert note,solution
   letter,arg,val=note.groups();assert eq(read(arg),roots[0]);assert eq(read(val),(dx if letter=='x' else dy).subs(T,roots[0])) and not eq(read(val),0)
  conclusion=solution[solution.index('Therefore'):] if 'Therefore' in solution else solution[solution.index('which confirms'):]
  vals=[read(v) for v in re.findall(r'\$t\s*=\s*(.*?)\$',conclusion)]
  assert sp.FiniteSet(*vals)==sp.FiniteSet(*roots)
 for text in [q[':question/problem'],solution or '']+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
  assert text.count('$')%2==0
  depth=0
  for c in text:
   depth+=(c=='{')-(c=='}');assert depth>=0
  assert depth==0
  assert '--' not in text and '+-' not in text
 return roots

cases=json.loads((HERE/'source-cases.json').read_text());source_details=[];records=[]
counts={'prompts':0,'solutions':0,'solutions_total':0,'field_banks':0,'values':0,'distractors':0,'designations':0,'designations_total':0,'missing_correct':0}
for case in cases:
 t=case['template'];level=case['difficulty'];source=g.QUESTIONS[case['source_id']]
 raw=g.generate(level,template=t,parameters=case['parameters'],profile='raw');q=raw['question'];mathcheck(raw)
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
  assert (key in source)==(key in q)
 if ':question/difficulty' in source:assert q[':question/difficulty']==source[':question/difficulty'][':db/ident']
 assert q[':question/problem']==source[':question/problem'];counts['prompts']+=1
 if ':question/worked-solution' in source:assert q[':question/worked-solution']==source[':question/worked-solution'];counts['solutions']+=1;counts['solutions_total']+=1
 for sf,f in zip(source[':question/answer-fields'],q[':question/answer-fields']):
  assert sf[':answer-field/key']==f[':answer-field/key'] and sf[':answer-field/type'][':db/ident']==f[':answer-field/type']
  assert sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in sf[':answer-field/choices'])==sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])
  assert (':answer-field/correct' in sf)==(':answer-field/correct' in f)
  counts['field_banks']+=1;counts['values']+=len(f[':answer-field/choices'])
  if ':answer-field/correct' in sf:
   counts['designations_total']+=1
   actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert actual==sf[':answer-field/correct'][':answer/value'];counts['designations']+=1;counts['distractors']+=len(f[':answer-field/choices'])-1
  else:counts['missing_correct']+=1
 assert len(source[':question/answer-fields'])==len(q[':question/answer-fields'])
 source_details.append({'source_id':case['source_id'],'raw_exact':True,'evidence_only':True,'eligible_for_learning':False})
 # Opaque bank repairs remain evidence only; method defaults get grading checks.
 normal=g.generate(level,template=t,parameters=case['parameters']);mathcheck(normal);records.append(('original-parameter normal '+t,normal))

variation={};fingerprints={l:set() for l in ('easy','moderate','hard')}
for t,(level,sid,anchor) in g.DEFS.items():
 variation[t]=0
 for seed in range(35):
  r=g.generate(level,seed=seed,template=t);mathcheck(r);variation[t]+=1;fingerprints[level].add(r['generation']['task_fingerprint']);records.append((t+' '+str(seed),r))
  # Fixed parameter instances are identity stable after option-order changes.
  rr=g.generate(level,seed=seed+91,template=t,parameters=r['generation']['parameters']);assert rr['question'][':question/id']==r['question'][':question/id']
  assert json.loads(json.dumps(r))==r
 # Ineligible observed banks must be parameterized, and reject the whole colliding bank.
 if sid:
  for seed in range(5):mathcheck(g.generate(level,seed=seed,template=t,profile='observed'))

# Mutation tests: equally-valued but missing required source operation, incorrect displayed derivative, stale conclusion.
import copy
mutations=0
r=g.generate('easy',template='spiral_cos',parameters=g.DEFS['spiral_cos'][2])
for change in ('stage','derivative','conclusion'):
 bad=copy.deepcopy(r);s=bad['question'][':question/worked-solution']
 if change=='stage':s=s.replace(r'\operatorname{sin}⁡(t)+\operatorname{cos}⁡(t) & =0 \\ ','')
 elif change=='derivative':s=s.replace(r'{x}^{′}(t)={e}^{t}',r'{x}^{′}(t)=2{e}^{t}',1)
 else:s=s.replace('which confirms that the tangent to the curve is indeed horizontal at $t='+g.tex(3*sp.pi/4),'which confirms that the tangent to the curve is indeed horizontal at $t=0')
 bad['question'][':question/worked-solution']=s
 try:mathcheck(bad)
 except AssertionError:mutations+=1
 else:raise AssertionError('Mutation escaped: '+change)

invalid=0
for t,(level,sid,p) in g.DEFS.items():
 bad=dict(p);bad[next(iter(bad))]=100
 try:g.generate(level,template=t,parameters=bad)
 except ValueError:invalid+=1
 else:raise AssertionError('Explicit workload bound escaped')
# Both zero derivatives are rejected rather than claimed H/V.
p=dict(g.DEFS['paired_cubics'][2]);p['u']=p['r']
try:g.generate_hard(template='paired_cubics',parameters=p)
except ValueError:invalid+=1
else:raise AssertionError('Stationary parameter accepted')

# Domain guards at allowed extreme boundaries; every accepted record is read back.
boundary_checks=0
boundaries={
 'line_quadratic':{'a':-10,'b':10,'h':5,'s':-4},
 'line_cubic':{'a':10,'b':-10,'h':4,'k':-5,'s':-5},
 'circle_horizontal':{'a':-10,'b':10,'h':10,'k':-10,'m':-3},
 'circle_vertical':{'a':10,'b':-10,'h':-10,'k':10,'m':3},
 'polynomial_two':{'r':5,'u':-8,'c':-3,'d':3},
 'power_line':{'a':-10,'b':10,'n':7,'s':-5},
 'spiral_cos':{'a':-10,'b':10,'phase':3},
 'spiral_sin':{'a':10,'b':-10,'phase':2},
 'paired_cubics':{'r':-4,'s':4,'u':-3,'v':3,'a':-2,'b':2}}
for t,p in boundaries.items():
 r=g.generate(g.DEFS[t][0],template=t,parameters=p);mathcheck(r);boundary_checks+=1;records.append(('boundary '+t,r))
# Scalar/translation aliases do not create a mathematical task; content still changes.
r=g.generate_easy(template='circle_horizontal',parameters=g.DEFS['circle_horizontal'][2]);p=dict(g.DEFS['circle_horizontal'][2]);p.update(a=-5,b=4,h=-8,k=9)
alias=g.generate_easy(template='circle_horizontal',parameters=p);assert r['generation']['task_fingerprint']==alias['generation']['task_fingerprint'];assert r['question'][':question/id']!=alias['question'][':question/id']

engine=[]
for label,r in records:
 checks=[]
 for index,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':index,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned choice grading; displayed values independently verified'})
  else:
   value=f[':answer-field/choices'][0][':answer/value'];z=read(value)
   equivalent='('+str(z*2)+')/2'
   checks.extend([{'field_index':index,'submitted':value,'expected':'accepted','purpose':'canonical fragment'},{'field_index':index,'submitted':equivalent,'expected':'accepted','purpose':'unreduced exact fraction or nested pi fraction'},{'field_index':index,'submitted':str(z+1),'expected':'rejected','purpose':'incorrect fragment'}])
 engine.append({'label':label,'record':r,'checks':checks})
# Observed raw round wording is a known form-sensitive limitation. Probe separately before setting outcomes.
for case in cases:
 if case['template'] not in ('polynomial_two','spiral_cos','spiral_sin'):continue
 r=g.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile='raw');checks=[]
 for index,f in enumerate(r['question'][':question/answer-fields']):
  value=f[':answer-field/choices'][0][':answer/value'];z=read(value)
  checks.append({'field_index':index,'submitted':value,'expected':'accepted','purpose':'faithful exact source fragment with original rounding wording'})
 engine.append({'label':'raw blank '+case['source_id'],'record':r,'checks':checks})
(HERE/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False))
binary=HERE.parents[1]/'runs/current/check-engine'
process=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
(HERE/'engine.log').write_text(process.stdout+process.stderr)
assert process.returncode==0,process.stdout+process.stderr
engine_report=json.loads((HERE/'engine-report.json').read_text())
limitations=[]
for stem in ('raw-equivalent','unsupported'):
 probe=json.loads((HERE/(stem+'-input.json')).read_text())
 assert all(v['record']['generation']['evidence_only'] and not v['record']['generation']['eligible_for_learning'] for v in probe)
 result=subprocess.run([str(binary),str(HERE/(stem+'-input.json')),str(HERE/(stem+'-report.json'))],capture_output=True,text=True)
 assert result.returncode==0,result.stderr
 limitations.append(json.loads((HERE/(stem+'-report.json')).read_text()))
# Default sampling exposes every supported family.
seen=set()
for level in ('easy','moderate','hard'):
 for seed in range(100):seen.add(g.generate(level,seed)['generation']['template'])
assert seen==set(g.DEFS)
audit=[]
for q in g.QUESTIONS.values():
 strings=[q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
 # Double slash counts in aligned solution rows are legitimate line separators.
 audit.append({'source_id':q[':question/math-academy-id'],'prompt_adjacent_ord92':sum(a==b=='\\' for a,b in zip(strings[0],strings[0][1:])),'answer_adjacent_ord92':sum(sum(a==b=='\\' for a,b in zip(s,s[1:])) for s in strings[2:])})
report={'status':'pass','source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_questions':8,'observed_difficulties':{'easy':5,'moderate':2,'unrated':1,'hard':0},'source_fidelity':counts,'source_details':source_details,'decoded_byte_audit':audit,'generated_math_checks':sum(variation.values()),'variants_per_template':variation,'distinct_mathematical_tasks_by_level':{k:len(v) for k,v in fingerprints.items()},'default_family_coverage':sorted(seen),'mutation_regressions_rejected':mutations,'invalid_explicit_inputs_rejected':invalid,'boundary_records':boundary_checks,'native_grading':{'records':len(engine),'checks':sum(len(row['checks']) for row in engine),'accepted':engine_report['accepted_checks'],'rejected':engine_report['rejected_checks'],'status':'pass','binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest()},'native_restrictions':{'raw_round_equivalents_rejected':limitations[0]['rejected_checks'],'unsupported_acos_equivalence_unresolved':limitations[1]['documented_unresolved_checks']},'repairs':{'q-21081':'normal output uses authoritative single current five-choice radio; raw duplicate missing ref retained','q-21206':'normal inferred t=0 correct designation, authored easy and shared-method solution; raw omissions retained','blank exact instructions':'normal Give exact answers; raw Do not round wording preserved'},'limitations':['Hard workload is authored, not an observed hard difficulty label.','Raw evidence with missing refs/duplicate keys is ineligible and excluded from native complete-question grading.','Historical line/power scalar distractor intent is opaque; public observed and raw banks remain evidence-only.','Raw exact-answer round wording has a native equivalent-entry form limitation; acos notation is unsupported; no engine changes.'],'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()}
(HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps(report,indent=2))
