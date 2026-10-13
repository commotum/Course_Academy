#!/usr/bin/env python3
"""Independent printed-function, complete-bank, stage, fidelity and native QA."""
import importlib.util,json,re,sys,subprocess,hashlib,uuid
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as s
from math_reader import read,x,y
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
sp=importlib.util.spec_from_file_location('special_generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
A,B,C,D=s.symbols('A B C D')

def write(n,v):(ROOT/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def proof(a,b,context):
 # Strict exact expression identity, with branch assumptions applied explicitly.
 xp=s.Symbol('positive_x',positive=True)
 a,b=a.subs(x,xp),b.subs(x,xp)
 difference=s.expand(a-b)
 if difference==0:return
 difference=s.cancel(difference)
 if difference==0:return
 if s.simplify(difference)!=0:
  # Domain-valid numerical probes for transcendental simplifications only after
  # strict symbolic identity attempt; never used for source final correctness.
  raise AssertionError((context,a,b,s.simplify(a-b)))

def printed(r):
 prompt=r['question'][':question/problem']
 m=re.search(r'f\(x,y\)=(.*?)\$',prompt);h=re.search(r'\$y=(.*?),\$',prompt)
 assert m and h,prompt
 return read(m[1]),read(h[1])

def normalize_derivatives(text):
 for src,to in ((g.FX,'A'),(g.FY,'B'),(g.YD,'C'),(g.D,'D')):text=text.replace(src,to)
 return text

def rows(sol):
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,flags=re.S);parsed=[]
 for bi,block in enumerate(blocks):
  block=normalize_derivatives(block).replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
  previous=None
  for row in block.split(r'\\'):
   for segment in row.split(r'\,'):
    segment=segment.strip().rstrip('., ')
    if not segment:continue
    sides=[z.strip() for z in segment.split('=')]
    assert len(sides)>=2,segment
    if not sides[0]:sides[0]=previous
    previous=sides[0]
    parsed.append((bi,sides))
 return parsed

def formatting(text):
 assert text.count('$')%2==0
 assert text.count('$$')%2==0
 assert text.count('{')==text.count('}'),text
 assert '--' not in text and '+-' not in text
 assert r'\u2061' not in text

def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];m=r['generation'];F,H=printed(r)
 assert F.free_symbols<={x,y} and H.free_symbols<={x}
 aa=s.diff(F,x).subs(y,H);bb=s.diff(F,y).subs(y,H);cc=s.diff(H,x);dd=s.diff(F.subs(y,H),x)
 subs={A:aa,B:bb,C:cc,D:dd}
 formatting(q[':question/problem']);formatting(q[':question/worked-solution'])
 eqs=0
 for bi,ss in rows(q[':question/worked-solution']):
  # Dependency product-rule component derivative rows are checked from the
  # printed differentiated argument, rather than from generation metadata.
  if ss[0].startswith(r'\frac{\text{d}}{\text{d}x}('):
   arg=ss[0][len(r'\frac{\text{d}}{\text{d}x}('):-1];reference=s.diff(read(arg),x)
   proof(reference,read(ss[1]),(m['template'],'component derivative',ss));eqs+=1;continue
  if bi==1:local={A:s.diff(F,x),B:s.diff(F,y),C:cc,D:dd}
  else:local=subs
  vals=[read(z).subs(local) for z in ss]
  for v in vals[1:]:proof(vals[0],v,(m['template'],bi,ss));eqs+=1
 # Independently read complete banks; do not trust ID designation alone.
 f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];assert len(cs)==5
 vs=[read(a[':answer/value']) for a in cs]
 if not m['evidence_only']:
  # Derive every wrong operation independently from the printed function and
  # dependency, then compare complete rendered values one-to-one.
  expected=[dd,aa,aa-bb*cc,aa+bb,bb*cc if m['template']=='reciprocal_exp' else aa+bb*H]
  if m['template']=='radial_power':
   xp=s.Symbol('positive_x',positive=True)
   expected=[s.simplify(v.subs(x,xp)).subs(xp,x) for v in expected]
  unused=set(range(5))
  for target in expected:
   matches=[]
   for i in unused:
    if g.equal(vs[i],target):
     proof(vs[i],target,('independent wrong-operation recipe',m['template']))
     matches.append(i)
   assert len(matches)==1,(m['template'],'unmatched complete recipe',target)
   unused.remove(matches[0])
 for a in cs:formatting(a[':answer/value'])
 for i,v in enumerate(vs):
  proof(v,dd,(m['template'],'correct')) if cs[i][':answer/id']==f[':answer-field/correct'][1] else None
  for w in vs[:i]:assert not g.equal(v,w),(m['template'],'duplicate choices',v,w)
 assert len([a for a in cs if a[':answer/id']==f[':answer-field/correct'][1]])==1
 for ident in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in cs]:uuid.UUID(ident)
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 return eqs

def engine(r,label):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual native selection grading; mathematical bank checked independently'} for a in f[':answer-field/choices']]}

def main():
 cases=[];review=[];native=[];fidelity=[];equalities=0
 raw_originals=[]
 for t,sid in g.FAMILIES.items():
  print('Checking source family '+t,flush=True)
  q=g.SOURCES[sid];p={'a':1};r=g.generate('easy',template=t,parameters=p,profile='observed:'+sid);raw_originals.append(r)
  eqs=check(r);equalities+=eqs
  assert r['question'][':question/problem']==q[':question/problem']
  assert r['question'][':question/worked-solution']==q[':question/worked-solution']
  assert set(r['question'])-{':question/id'}==set(q)-{':question/id',':db/id',':question/math-academy-id'}
  f=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
  expected={(a[':answer/value'],a[':answer/id']==f[':answer-field/correct'][':answer/id']) for a in f[':answer-field/choices']}
  actual={(a[':answer/value'],a[':answer/id']==rf[':answer-field/correct'][1]) for a in rf[':answer-field/choices']}
  assert expected==actual
  fidelity.append({'source_id':sid,'prompt_exact':True,'solution_exact':True,'answer_values_exact':5,'correct_designation_matched':True,'field_key_type_order_presence':True,'raw_eligible':False,'source_math_domain_error':sid=='q-95114'})
  cases.append({'source_id':sid,'template':t,'parameters':p,'bank_profile':'observed:'+sid})
  native.append(engine(r,'original/'+sid));review.append({'label':'Raw source replay '+sid,'record':r})
  # Full easy coefficient domain: check both profiles, including signed masks.
  for a in (-5,-4,-3,-2,-1,1,2,3,4,5):
   for profile in ('operations:'+t,'observed:'+sid):
    rr=g.generate('easy',template=t,parameters={'a':a},profile=profile)
    equalities+=check(rr)
    rr2=g.generate('easy',seed=90,template=t,parameters={'a':a},profile=profile)
    assert rr['question'][':question/id']==rr2['question'][':question/id']
  # Check normal source-chain fidelity independently, including original a=1.
  normal=g.generate('easy',template=t,parameters=p)
  assert normal['question'][':question/worked-solution']==q[':question/worked-solution']
  assert normal['generation']['eligible_for_learning']
  for a in (2,-3):
   rr=g.generate('easy',template=t,parameters={'a':a});review.append({'label':'Generated normal '+t+' a='+str(a),'record':rr});native.append(engine(rr,'generated/'+t+'/'+str(a)))
 # Missing-level workload domains: sign/frequency boundaries and random full
 # banks. All independent checks start from actual printed functions.
 fingerprints={}
 for level in ('moderate','hard'):
  print('Checking authored '+level,flush=True)
  fingerprints[level]=set()
  for t in [t for t,l in g.TEMPLATES.items() if l==level]:
   for p in ({'a':2,'b':-3,'c':2,'k':2},{'a':-4,'b':4,'c':-4,'k':4}):
    rr=g.generate(level,template=t,parameters=p);equalities+=check(rr);review.append({'label':'Authored missing-level '+t,'record':rr});native.append(engine(rr,'authored/'+t+'/'+str(p)))
   for seed in range(20):
    rr=g.generate(level,seed=seed,template=t);equalities+=check(rr);fingerprints[level].add(rr['generation']['mathematical_fingerprint'])
   for p in ({'a':0,'b':1,'c':1,'k':2},{'a':1,'b':1,'c':1,'k':1},{'a':-5,'b':1,'c':1,'k':2},{'a':1,'b':1,'c':1,'k':5}):
    try:g.generate(level,template=t,parameters=p)
    except ValueError:pass
    else:raise AssertionError('Invalid workload parameters accepted')
  reached={g.generate(level,seed=z)['generation']['template'] for z in range(16)}
  assert reached=={t for t,l in g.TEMPLATES.items() if l==level}
 # Product parameter aliases do not manufacture mathematical task identities.
 for lev,t in [('moderate','weighted_polynomial_sine'),('hard','exponential_product_dependency')]:
  r1=g.generate(lev,template=t,parameters={'a':2,'b':2,'c':3,'k':2});r2=g.generate(lev,template=t,parameters={'a':2,'b':3,'c':2,'k':2})
  assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
  assert r1['question'][':question/id']!=r2['question'][':question/id']
 # Normal default reaches every observed source family.
 assert {g.generate_easy(z)['generation']['template'] for z in range(40)}==set(g.FAMILIES)
 # Explicit guards cannot be bypassed, unknown/unused inputs rejected.
 for p in ({'a':0},{'a':6},{'a':-6},{'a':True},{'a':1,'unused':2}):
  try:g.generate_easy(template='sine_power',parameters=p)
  except ValueError:pass
  else:raise AssertionError('invalid easy accepted')
 # Domain counterexample to source: negative x makes its designated radial
 # answer opposite to the true derivative; keep evidence and normal repair.
 radial=raw_originals[list(g.FAMILIES).index('radial_power')];F,H=printed(radial)
 rf=radial['question'][':question/answer-fields'][0];rv=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert s.simplify(read(rv).subs(x,-1)-s.diff(F.subs(y,H),x).subs(x,-1))!=0
 write('source-cases.json',cases);write('source-fidelity.json',fidelity);write('review.json',review);write('engine-input.json',native)
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
 write('validation.json',{'passed':True,'source_basis':1356,'source_questions':9,'raw_prompt_exact':9,'raw_solution_exact':9,'raw_complete_banks_exact':9,'raw_answer_values_exact':45,'raw_correct_designations_matched':9,'normal_solution_original_chains_exact':9,'source_mathematically_valid_without_repair':8,'normal_positive_domain_repair':1,'raw_ineligible_banks':9,'displayed_stage_equalities_checked':equalities,'easy_profile_instances_checked':180,'independently_derived_normal_bank_values_checked':890,'authored_random_instances':80,'authored_boundary_instances':8,'review_records':len(review),'native_report':'engine-validation.json','native_typed_equivalents':'not applicable: all fields radio; meaningful equivalent expressions checked symbolically, actual grader selects owned UUIDs','plots':'none','runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((ROOT/'source.json').read_bytes()).hexdigest(),'grader_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'meaningful_catalog':{'easy':90,'moderate':864,'hard':864,'explanation':'signed a times distinct reduced products b*c times k; aliases removed; same dependency workload'},'sampled_unique_math_tasks':{k:len(v) for k,v in fingerprints.items()},'database_writes':0,'unresolved_limits':['Opaque original distractor intentions are not recovered; raw value-pattern profiles are evidence-only.','Source radial chain is valid only under x>0; raw replay preserves omitted domain and remains ineligible.','Missing moderate/hard definitions are authored workload designs, not observed labels.']})
 lines=['# Review: special-case multivariable chain rule','Raw source banks are evidence-only. Generated normal questions use complete operation banks. Radial normal questions state x>0.']
 for item in review:lines+=['\n## '+item['label'],g.markdown(item['record'])]
 (ROOT/'review.md').write_text('\n\n'.join(lines)+'\n')
 print('PASS: nine complete raw banks / 45 values, all source chains preserved in normal generation, independent displayed-stage math, and native radio grading.')
if __name__=='__main__':main()
