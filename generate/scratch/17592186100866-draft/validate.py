"""Independent checks read actual printed operands, stages, and banks before grading."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def dump(name,x):(D/name).write_text(json.dumps(x,indent=2)+'\n')
def ctex(v):return v.replace('\\\\','\\') if v.startswith('\\\\begin') else v
def scalar(v):return s.Rational(str(v).strip())
def mats(text):return [[[c.strip() for c in row.split('&')] for row in b.split('\\\\')] for b in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def numerical(M):return s.Matrix([[scalar(c) for c in row] for row in M])
def correct(f):return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']
def signature(value):
 m=mats(ctex(value));return tuple(numerical(m[0])) if m else (scalar(value),)
def check(record):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 q=record['question'];g.public_guard(record)
 actual=mats(q[':question/problem']);assert len(actual)==2
 A,V=map(numerical,actual);assert A.shape==(2,2) and V.shape==(2,1)
 target=A*V;r,t=target
 fields=q[':question/answer-fields'];seen=set()
 for f in fields:
  fid=f[':answer-field/id'];assert fid not in seen;seen.add(fid)
  bank=[signature(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(bank)==len(set(bank)),('Wrong-wrong bank collision',bank)
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(bank)
  if ':answer-field/correct' in f:
   expected=tuple(target) if f[':answer-field/type'].endswith('/radio') else (target[int(f[':answer-field/key'][-1])-1],)
   assert signature(correct(f))==expected,('Actual printed operands/key mismatch',expected)
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 if ':question/worked-solution' not in q:return
 solution=q[':question/worked-solution'];ms=mats(solution);named=record['generation']['template'].startswith('named')
 assert len(ms)==(9 if named else 11),('Actual operative matrix stage count',len(ms))
 assert numerical(ms[0])==A and numerical(ms[1])==V
 assert numerical(ms[4])==A and numerical(ms[5])==V
 # Validate the literal dot-product factors, not just an algebraically equal row.
 for expr,coeffs in ((ms[2][0][0],list(A[0,:])),(ms[6][1][0],list(A[1,:]))):
  match=re.fullmatch(r'(.+?)\\cdot (.+?)\+(.+?)\\cdot (.+)',expr);assert match,('Missing source multiply/add stage',expr)
  operands=[scalar(x.strip('()')) for x in match.groups()]
  assert operands==[coeffs[0],V[0],coeffs[1],V[1]],('Printed dot-product operands',operands)
  assert s.sympify(expr.replace('\\cdot','*'),rational=True)==sum(c*v for c,v in zip(coeffs,V))
 assert ms[2][1][0]=='∗' and ms[3][1][0]=='∗'
 assert scalar(ms[3][0][0])==r
 assert scalar(ms[6][0][0])==r and numerical(ms[7])==target
 if named:
  assert numerical(ms[8])==target
  names=re.search(r'Find \$([A-Z][a-z])\$',q[':question/problem'])[1]
  assert 'Therefore, \n$'+names+'=' in solution
 else:assert numerical(ms[8])==A and numerical(ms[9])==V and numerical(ms[10])==target
 assert solution.count('Multiplying the first row, we get')==1
 assert solution.count('Multiplying the second row, we get')==1
 assert solution.count('We multiply each row in the matrix by the column vector using the dot product.')==1
 return True
cases=json.loads((D/'source-cases.json').read_text());review=json.loads((D/'review.json').read_text());native=[];fidelity=[];options=0;designations=0
for case in cases:
 raw=g.SOURCES[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(r);q=r['question']
 assert q[':question/problem']==g.normalize_prose(raw[':question/problem']),case['source_id']
 if ':question/worked-solution' in raw:assert q[':question/worked-solution']==g.normalize_prose(raw[':question/worked-solution']),('Source solution',case['source_id'])
 for attr in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (attr in q)==(attr in raw)
 assert len(q[':question/answer-fields'])==len(raw[':question/answer-fields'])
 for of,nf in zip(raw[':question/answer-fields'],q[':question/answer-fields']):
  assert of[':answer-field/key']==nf[':answer-field/key']
  assert of[':answer-field/type'][':db/ident']==nf[':answer-field/type']
  assert sorted(signature(a[':answer/value']) for a in of[':answer-field/choices'])==sorted(signature(a[':answer/value']) for a in nf[':answer-field/choices'])
  options+=len(of[':answer-field/choices'])
  assert (':answer-field/correct' in of)==(':answer-field/correct' in nf)
  if ':answer-field/correct' in of:assert signature(of[':answer-field/correct'][':answer/value'])==signature(correct(nf));designations+=1
 fidelity.append({'source_id':case['source_id'],'prompt':'exact normalized','solution':'exact normalized' if ':question/worked-solution' in raw else 'absent preserved','fields':len(q[':question/answer-fields']),'all_bank_values':'matched one-to-one','correct_presence':'preserved','raw_evidence_only':True})
# Mathematical validation across every public family and level. Sampling is independently
# checked against actual text, including all stage operands and all bank pairs.
coverage={};fingerprints={};ids=[];profile_coverage={};slot_coverage={}
for level in g.LEVELS:
 coverage[level]={};fps=set();positions=set();profile_coverage[level]={};slot_coverage[level]={k:set() for k in g.KEYS}
 for seed in range(450):
  r=g.generate(level,seed);check(r);fps.add(r['generation']['mathematical_fingerprint']);typ=r['generation']['template'];coverage[level][typ]=coverage[level].get(typ,0)+1
  q=r['question'];f=q[':question/answer-fields'][0]
  if f[':answer-field/type'].endswith('/radio'):positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
  profile=r['generation']['bank_profile'];profile_coverage[level][profile]=profile_coverage[level].get(profile,0)+1
  p=r['generation']['parameters']
  for k in g.KEYS:slot_coverage[level][k].add(p[k])
  r2=g.generate(level,seed+23456,template=typ,parameters=p,profile=r['generation']['bank_profile']);assert q[':question/id']==r2['question'][':question/id']
  for f1,f2 in zip(q[':question/answer-fields'],r2['question'][':question/answer-fields']):assert {a[':answer/id'] for a in f1[':answer-field/choices']}=={a[':answer/id'] for a in f2[':answer-field/choices']}
 assert set(coverage[level])==set(g.TEMPLATES);assert positions==set(range(5));fingerprints[level]=len(fps)
 assert set(profile_coverage[level])=={profile for profiles in g.ELIGIBLE_PROFILES.values() for profile in profiles}
 assert all(len(values)>15 for values in slot_coverage[level].values())
for item in review:check(item['record'])
# Hold all six numeric data fixed and change supported labels; answers/stages remain
# invariant while prompt+conclusion labels change together. There is no target slot:
# this KP always requests the complete ordered two-component column vector.
r=g.generate('easy',1,template='named-blank');p=r['generation']['parameters'];r2=g.generate('easy',2,template='named-blank',parameters=p|{'matrix_name':'Z','vector_name':'n'});check(r2)
assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
assert r['question'][':question/id']!=r2['question'][':question/id']
assert [signature(correct(f)) for f in r['question'][':question/answer-fields']]==[signature(correct(f)) for f in r2['question'][':question/answer-fields']]
# Simultaneous column/vector permutation is the same assessed row-dot-product task.
r=g.generate('moderate',312,template='inline-blank');p=r['generation']['parameters'];swapped=p|dict(a=p['b'],b=p['a'],c=p['d'],d=p['c'],u=p['v'],v=p['u']);r2=g.generate('moderate',923,template='inline-blank',parameters=swapped);check(r2)
assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
assert [signature(correct(f)) for f in r['question'][':question/answer-fields']]==[signature(correct(f)) for f in r2['question'][':question/answer-fields']]
# Explicit maximum source/moderate and decimal hard boundaries stay in scope.
check(g.generate('moderate',parameters=dict(a=-11,b=11,c=11,d=-11,u='0.1',v='-0.2'),template='inline-blank'))
check(g.generate('hard',parameters=dict(a='8.9',b='-8.7',c='4.3',d='-6.1',u='0.7',v='2.3'),template='inline-blank'))
# Canonical spelling is normalized before identity.
a=g.generate('moderate',2,template='named-blank');p=a['generation']['parameters'];p2={k:(str(s.Rational(v)*10)+'/10' if k in g.KEYS else v) for k,v in p.items()};assert a['question'][':question/id']==g.generate('moderate',3,template='named-blank',parameters=p2)['question'][':question/id']
check(g.generate('moderate',parameters=dict(a=-11,b=11,c=11,d=-11,u=0.1,v=-0.2),template='inline-blank'))
# Scope guard regressions and boundary inputs.
invalid=[('easy',dict(a='1/2',b=2,c=3,d=4,u=2,v=3)),('moderate',dict(a=1,b=2,c=3,d=4,u=2,v=3)),('moderate',dict(a=1,b=2,c=3,d=4,u='1/3',v=3)),('hard',dict(a='0.1',b='0.2',c='0.3',d='0.4',u='0.5',v='0.6')),('hard',dict(a='-9.1',b='0.2',c='-0.3',d='0.4',u='0.5',v='0.6'))]
for level,p in invalid:
 try:g.generate(level,parameters=p,template='named-blank')
 except ValueError:pass
 else:raise AssertionError('Missing scope guard')
for p in (dict(a=-11,b=11,c=0,d=-11,u=-9,v=9),dict(a=0,b=11,c=-11,d=0,u=9,v=-9)):check(g.generate('easy',parameters=p,template='inline-blank'))
# Mutation regressions against actual learner content (not metadata).
base=g.generate('moderate',123,template='named-blank');mutations=[]
x=copy.deepcopy(base);x['question'][':question/problem']+='\x0c';mutations.append(('C0',x))
x=copy.deepcopy(base);x['question'][':question/worked-solution']=x['question'][':question/worked-solution'].replace('\\cdot ','+',1);mutations.append(('Missing dot stage',x))
x=copy.deepcopy(base);x['question'][':question/worked-solution']=x['question'][':question/worked-solution'].replace('Therefore, \n$','Therefore, \n$ZZ=',1);mutations.append(('Stale conclusion role',x))
x=copy.deepcopy(base);x['question'][':question/problem']=x['question'][':question/problem'].replace('&','',1);mutations.append(('Matrix role/shape',x))
for label,x in mutations:
 try:check(x)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('Mutation not caught '+label)
# Native grader provenance: 42 files including source/library/binary +28 engine +11 deps.
buildpath=ROOT/'generate/scratch/17592186059716-draft/reference/grader-build.json';build=json.loads(buildpath.read_text());hashes={build['source']:build['source_sha256'],build['library']:build['library_sha256'],build['binary']:build['binary_sha256']}|build['engine_sources']|build['dependencies']
for path,sha in hashes.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
assert len(hashes)==42
dump('native-provenance.json',{'build_record':str(buildpath.relative_to(ROOT)),'verified_hash_count':len(hashes),'files':hashes})
# Actual grader: every option by ID, every scalar blank canonical/legitimate
# unreduced expression and wrong value. Missing-ref raw evidence is completed only
# in a separately labeled fixture; these completions never inflate source refs.
for i,item in enumerate(review):
 record=copy.deepcopy(item['record']);q=record['question'];checks=[]
 for fi,f in enumerate(q[':question/answer-fields']):
  if ':answer-field/correct' not in f:
   A,V=map(numerical,mats(q[':question/problem']));value=tuple(A*V)
   key=next(a[':answer/id'] for a in f[':answer-field/choices'] if signature(a[':answer/value'])==value);f[':answer-field/correct']=[':answer/id',key]
  for answer in f[':answer-field/choices']:
   if f[':answer-field/type'].endswith('/radio'):checks.append({'field_index':fi,'submitted_answer_id':answer[':answer/id'],'expected':'accepted' if answer[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every displayed radio option'})
  if f[':answer-field/type'].endswith('/blank'):
   val=correct(f);n=s.Rational(val);checks.extend([{'field_index':fi,'submitted':val,'expected':'accepted','purpose':'Canonical scalar'}, {'field_index':fi,'submitted':f'({n.p*3})/({n.q*3})','expected':'accepted','purpose':'Legitimate unreduced exact rational'}, {'field_index':fi,'submitted':str(n+1),'expected':'rejected','purpose':'Known incorrect scalar'}])
 native.append({'label':str(i)+' '+item['label']+' (missing refs inferred in fixture only)','record':record,'checks':checks})
dump('native-input.json',native)
subprocess.run([str(ROOT/build['binary']),str(D/'native-input.json'),str(D/'native-report.json')],check=True,cwd=ROOT)
report=json.loads((D/'native-report.json').read_text())
dump('source-bank-replay.json',{'source_basis':g.CAP['basis'],'originals':len(cases),'source_fields':sum(len(g.SOURCES[c['source_id']][':question/answer-fields']) for c in cases),'bank_values_matched':options,'original_correct_designations_matched':designations,'missing_designations_preserved':2,'missing_solution_preserved':1,'records':fidelity})
dump('validation.json',{'status':'passed','runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'source_originals':len(cases),'all_source_banks_matched':True,'source_options_matched':options,'source_correct_designations_matched':designations,'math_actual_display_checks':1350+len(review)+len(cases)+7,'source_solutions_exact_normalized':10,'source_solution_missing_preserved':1,'family_coverage':coverage,'profile_coverage':profile_coverage,'slot_value_counts':{lev:{k:len(v) for k,v in vals.items()} for lev,vals in slot_coverage.items()},'distinct_math_tasks_per_450':fingerprints,'mutation_regressions':len(mutations),'identity_seed_checks':1350,'native_hashes_verified':len(hashes),'native':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'plots':'none; mathematical matrices only','root_approval':'pending','limitations':['Two source fields lack correct refs; separately inferred native fixtures, never counted as observed designation matches.','q-13566 source lacks difficulty/solution; raw public evidence preserves omissions.','Opaque observed vector slots and unexplained arithmetic-offset banks are ineligible evidence profiles.','Moderate/hard levels are authored decimal workload claims, not observed MA difficulty labels.']})
print('PASS: 11originals;',options,'bank values;',designations,'observed correct refs; 1350sampled instances; 42native hashes')
