#!/usr/bin/env python3
"""Bounded source, role-boundary, readback, native-grade and delivery checks."""
import copy,importlib.util,json,re,subprocess,sys,shutil,tempfile,os
from pathlib import Path
import sympy as sp
W=Path(__file__).resolve().parent
R=Path('/home/jake/Developer/Course_Academy')
JOB=R/'generate/repairs/2026-10-20-early-cohort/jobs/17592186087868'
E=W/'evidence';E.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('g',W/'17592186087868.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y,D=sp.symbols('x y D')
def save(name,obj): (E/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def parse(t):
 t=t.strip().rstrip('.').replace('{y}^{′}','D').replace('&','')
 t=re.sub(r'\{x\}\^\{(\d+)\}',r'x**\1',t)
 t=t.replace('{','(').replace('}',')')
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 return parse_expr(t,local_dict={'x':X,'y':Y,'D':D},transformations=standard_transformations+(implicit_multiplication_application,))
def residual(eq):
 l,r=eq.split('=');return sp.expand(parse(l)-parse(r))
def flags(record):
 fs=record['question'][':question/answer-fields'];return tuple(next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) for f in fs)
def check(record):
 q=record['question'];fs=q[':question/answer-fields'];target='inhomogeneous' if 'are inhomogeneous?' in q[':question/problem'] else 'homogeneous'
 assert len(fs)==3 and any(flags(record))
 expected=[];equations=[]
 for f in fs:
  assert f[':answer-field/type']==':answer-field.type/checkbox'
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
  e=f[':answer-field/key'].strip('$');z=residual(e)
  assert z.coeff(D)==1 and sp.diff(z,Y,2)==0 and sp.diff(z,D)==1
  forcing=sp.expand(-z.subs({Y:0,D:0}));expected.append(bool(forcing!=0)==(target=='inhomogeneous'));equations.append((e,z,forcing))
 assert tuple(expected)==flags(record)
 sections=re.split(r'- (?:First|Next|Finally), we consider the equation\n\n',q[':question/worked-solution'])[1:];assert len(sections)==3
 for section in sections:
  simple=re.findall(r'\$\$\n(.*?)\n\$\$',section,re.S)[0].rstrip('.')
  z=residual(simple);matched=[r for r in equations if sp.expand(r[1]-z)==0];assert len(matched)==1
  _,_,force=matched[0]
  aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',section,re.S)
  for block in aligned:
   rows=re.split(r'\\\\',block);assert len(rows)==3
   for row in rows:assert sp.expand(residual(row)-z)==0
   assert rows[1].replace('{y}^{′}','').count('y')==2
   assert rows[2].replace('{y}^{′}','').count('y')<=1
  if force==0:assert 'homogeneous.' in section and 'is inhomogeneous.' not in section and '*not* homogeneous.' not in section
  else:assert 'is inhomogeneous.' in section or '*not* homogeneous.' in section
  for val in re.findall(r'\$Q\(x\)=(.*?)\$',section):assert sp.expand(parse(val)-force)==0
 conclusion=q[':question/worked-solution'].split('Therefore, the correct answer is ')[-1]
 selected=re.findall(r'\$(.*?)\$',conclusion)
 assert set(selected)=={f[':answer-field/key'].strip('$') for f,b in zip(fs,expected) if b}
 assert len(selected)==sum(expected)
 for text in [q[':question/problem'],q[':question/worked-solution']]:
  assert not any(ord(c)<32 and c not in '\n\r\t' for c in text)
 return True

# Source replay, complete banks and actual independently classified source inventory.
source=json.load(open(JOB/'source/source.json'));inventory=json.load(open(JOB/'source/inventory.json'))
replays=[];fidelity=[];engine=[]
for mid,src in g.SOURCES.items():
 level=src[':question/difficulty'][':db/ident'].split('/')[-1]
 r=g.generate(level,profile='raw_'+mid);check(r);replays.append(r)
 q=r['question'];assert q[':question/problem']==g.normalize_prose(src[':question/problem'])
 assert q[':question/worked-solution']==g.normalize_prose(src[':question/worked-solution'])
 for f,sf in zip(q[':question/answer-fields'],src[':question/answer-fields']):
  assert f[':answer-field/key']==g.normalize_prose(sf[':answer-field/key'])
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in sf[':answer-field/choices']]
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
 fidelity.append({'source_id':mid,'question_id':src[':question/id'],'prompt_exact':q[':question/problem']==src[':question/problem'],'solution_exact':q[':question/worked-solution']==src[':question/worked-solution'],'normalized_complete_bank_and_key':True})
save('source-replay.json',replays);save('source-fidelity.json',fidelity)
records=[];catalog_coverage={};boundaries=[]
# All eligible decision tuples; 8 coefficient/degree controls are shared per tuple.
for level in ['easy','moderate']:
 for j,roles in enumerate(g.role_catalog(level)):
  for control,(a,n,c,m) in enumerate([(1,0,1,1),(-9,3,-9,3),(2,1,4,2),(-1,2,-1,1),(-2,0,-4,2),(-2,1,4,1),(2,2,-4,3),(2,3,4,2)]):
   rhs=[];bvalues=[1,-5,3];cvalues=[c,-c,(c-(1 if c>0 else -1)) if abs(c)>1 else 2*c]
   for i,role in enumerate(roles):
    if role=='zero':rhs.append([0,0,0])
    elif role=='move_y':rhs.append([bvalues[i],0,0])
    else:rhs.append([0,cvalues[i],0 if role=='constant_forcing' else m])
   p={'a':a,'n':n,'rhs':rhs};r=g.generate(level,1000+j*8+control,parameters=p);check(r);records.append(r)
 catalog_coverage[level]=len(g.role_catalog(level))
# Finite endpoint values not all present in controls above.
for level in ['easy','moderate']:
 for a,n,b,c,m in [(9,0,5,9,0),(-1,3,-1,-1,3),(1,0,1,1,1)]:
  r=g.generate(level,parameters={'a':a,'n':n,'rhs':[[b,0,0],[0,c,m],[0,0,0]]});check(r);records.append(r);boundaries.append(r['generation']['parameters'])
# Native normal sampling small regression, both levels; deterministic replay.
for level in ['easy','moderate']:
 for seed in range(12):
  r=g.generate(level,seed);assert r==g.generate(level,seed);check(r);records.append(r)
# Explicit invalid parameters fail; no silently rewritten inputs.
rejections=[]
for label,level,p in [('empty-moderate','moderate',{'a':1,'n':1,'rhs':[[1,0,0],[-1,0,0],[0,0,0]]}),('duplicate','easy',{'a':1,'n':1,'rhs':[[1,0,0],[1,0,0],[0,1,1]]}),('out-of-range','easy',{'a':10,'n':1,'rhs':[[1,0,0],[0,1,1],[0,0,0]]})]:
 try:g.generate(level,parameters=p)
 except ValueError:rejections.append(label)
 else:raise AssertionError(label)
try:g.generate('hard')
except ValueError:rejections.append('unsupported-hard')
else:raise AssertionError('hard')
# Counterfactual: a,n and other two equations remain unchanged; one direct-zero RHS becomes forcing.
cf=[]
for level in ['easy','moderate']:
 base={'a':2,'n':2,'rhs':[[1,0,0],[0,3,1],[0,0,0]]}
 changed=copy.deepcopy(base);changed['rhs'][2]=[0,-4,0]
 pair=[g.generate(level,parameters=p) for p in [base,changed]]
 for r in pair:check(r)
 assert flags(pair[0])[2]!=flags(pair[1])[2] and flags(pair[0])[:2]==flags(pair[1])[:2]
 # Irrelevant nonzero magnitude/degree/sign and coefficient changes preserve all keys.
 irrelevant=copy.deepcopy(base);irrelevant.update(a=-9,n=3);irrelevant['rhs'][1]=[0,-9,3]
 same=g.generate(level,parameters=irrelevant);check(same);assert flags(same)==flags(pair[0])
 cf.extend(pair+[same]);records.extend(pair+[same])
save('counterfactual-records.json',cf)
# Check a stale key, displayed intermediate sign and stale conclusion are detectable.
mutations=[]
base=cf[0]
for label in ['key','intermediate','conclusion']:
 r=copy.deepcopy(base)
 if label=='key':
  f=r['question'][':question/answer-fields'][2];f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']=='false')]
 elif label=='intermediate':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('y-y & =0','y+y & =0')
 else:r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].rsplit('Therefore, the correct answer is ',1)[0]+'Therefore, the correct answer is $wrong$.'
 try:check(r)
 except (AssertionError,ValueError):mutations.append(label)
 else:raise AssertionError('Escaped mutation '+label)
# Batch all responses, including original submitted UUID on changed target.
for i,r in enumerate(replays+records):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Independently classified equation-labelled checkbox'})
 engine.append({'label':str(i),'record':r,'checks':checks})
for i in [0,3]:
 before,after=cf[i:i+2];oldflag=flags(before)[2];f=after['question'][':question/answer-fields'][2]
 engine.append({'label':'counterfactual old semantic response rejected '+str(i),'record':after,'checks':[{'field_index':2,'submitted_answer_id':next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==str(oldflag).lower()),'expected':'rejected','purpose':'Relevant evidence flips actual grade'}]})
save('engine-input.json',engine)
subprocess.run([str(R/'generate/runs/current/check-engine'),str(E/'engine-input.json'),str(E/'engine-report.json')],check=True,stdout=subprocess.DEVNULL)
save('test-records.json',records)
# Source inventory includes exactly original captures, not historical generated records.
ids={q[':question/id'] for q in g.SOURCES.values()};tested=0
for q in inventory['questions']:
 assert q[':question/id'] in ids
 src=next(s for s in g.SOURCES.values() if s[':question/id']==q[':question/id'])
 def unordered(value):
  if isinstance(value,dict):return {k:unordered(v) for k,v in value.items()}
  if isinstance(value,list):return sorted([unordered(v) for v in value],key=lambda x:json.dumps(x,sort_keys=True))
  return value
 assert unordered(q)==unordered(src)
 tested+=1
save('affected-inventory.json',{'affected_questions':[]})
save('inventory-audit.json',{'captured_questions':tested,'all_equal_authoritative_source_ignoring_collection_order':True,'independent_math_checked_fields':tested*3,'obsolete_radio_records':0,'generated_records_with_replay_metadata':0,'finding':'No demonstrated item defect in captured inventory. These are source records, not generated provenance. Generator-wide fixed-role patterns do not make a mathematically correct source item defective. No claim about uncaptured database inventory.'})
# Delivery real implementation: run separately for each supported band.
for level in ['easy','moderate']:
 subset=[r for r in records if r['question'][':question/difficulty'].endswith('/'+level)]
 save('input-'+level+'.json',subset)
 subprocess.run([sys.executable,str(R/'generate/pipeline/check_delivery.py'),'--input',str(E/('input-'+level+'.json')),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty',level,'--output',str(E/('delivery-'+level)),'--asset-root',str(E/'assets'),'--math-root','/media/jake/SSD/EDB/math'],check=True,stdout=subprocess.DEVNULL)
# Conditional shortcut/coverage measured before AND after actual filters.
def variation(rs):
 keys=[flags(r) for r in rs];role_tuples={tuple(r['generation']['roles']) for r in rs}
 buckets={}
 for r in rs:
  p=r['generation']['parameters'];key=(r['generation']['template'],r['generation']['profile'],p['n'],p['a']>0)
  buckets.setdefault(str(key),[]).append(flags(r))
 probes={}
 for key,values in buckets.items():
  counts={str(v):values.count(v) for v in set(values)}
  probes[key]={'attempts':len(values),'best_fixed_subset_success':max(counts.values()),'fixed_subset_baseline':max(counts.values())/len(values),'true_by_position':[sum(v[i] for v in values) for i in range(3)],'correct_counts':sorted({sum(v) for v in values})}
  assert len(set(values))>1
  assert all(0<sum(v[i] for v in values)<len(values) for i in range(3))
  assert len({sum(v) for v in values})>1
 return {'records':len(rs),'role_tuples':len(role_tuples),'unordered_role_multisets':len({tuple(sorted(r)) for r in role_tuples}),'true_by_position':[sum(v[i] for v in keys) for i in range(3)],'correct_counts':sorted({sum(v) for v in keys}),'within_template_probes':probes}
variation_report={}
for level in ['easy','moderate']:
 before=json.load(open(E/('input-'+level+'.json')));after=json.load(open(E/('delivery-'+level)/'accepted.json'))
 pre=variation(before);post=variation(after)
 assert {tuple(r['generation']['roles']) for r in after}==set(g.role_catalog(level))
 variation_report[level]={'before':pre,'after':post,'eligible_role_tuples':catalog_coverage[level]}
save('pedagogical-variation.json',{'decision_coverage':variation_report,'counterfactuals':{'changed_forcing_changes_one_key_and_grade':2,'irrelevant_coefficient_and_nonzero_forcing_preserves_keys':2},'mutations_caught':mutations,'rejections':rejections,'interpretation':'The reliable algebraic rule based on identically-zero forcing is intended. No fixed template/profile/coefficient-sign/degree, position or number-of-selections strategy succeeds for all cases. Semantic role multisets exclude permutations and numeric aliases.','learner_selection':'Actual shared delivery filtering used. question_selection.rs selects difficulty first, uniformly within chosen rated band with configured weights; it does not inspect equation roles. Learner seen-before state, reservations, live inventory changes and configured weights unavailable offline. Unconfigured policy chooses lowest entity ID; delivery does not assign production entity IDs.'})
# Relocation only declared runtime files, running outside workspace/repository.
manifest=json.load(open(W/'package.json'))
with tempfile.TemporaryDirectory(prefix='ode-relocated-') as td:
 t=Path(td)
 for name in manifest['files']:
  dest=t/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy(W/name,dest)
 result=subprocess.run([sys.executable,str(t/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','20','--format','json'],cwd='/tmp',env={**os.environ,'PYTHONPATH':'','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(t/'assets')},capture_output=True,text=True,check=True)
 assert json.loads(result.stdout)==json.load(open(W/'initial-records.json'))
report={'passed':True,'source_questions':len(replays),'source_fields':36,'source_choices':72,'source_exact_prompt':sum(x['prompt_exact'] for x in fidelity),'source_exact_solution':sum(x['solution_exact'] for x in fidelity),'generated_math_checked':len(records),'role_catalog':catalog_coverage,'boundary_cases':boundaries,'native_report':'engine-report.json','relocated_five_records_identical':True,'inventory_checked':tested}
save('validation.json',report);print(json.dumps(report,indent=2))
