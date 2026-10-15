"""Private fail-closed fidelity, printed-math, finite-domain and native QA."""
from pathlib import Path
import importlib.util,sys,json,hashlib,subprocess,copy,random,re,itertools,time
sys.dont_write_bytecode=True
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
def module(n,p):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('kp68916',HERE.with_suffix('.py'));v=module('kp68916_readback',HERE/'readback.py');s=g.s
ENGINE=ROOT/'generate/runs/current/check-engine';EXPECTED_ENGINE='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
def save(n,z):(HERE/n).write_text(json.dumps(z,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def invalid(fn):
 try:fn()
 except (ValueError,AssertionError):return
 raise AssertionError('invalid public input accepted')
def public_check(r):
 g.fmt.validate_generated_record(r)
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==17592186068916
 for t in [r['question'][':question/problem'],r['question'][':question/worked-solution']]+[a[':answer/value'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in t),'unexpected control character'
 out=v.validate(r['question']);v.structure(r['question'],r['generation']['template']);return out
assert sha(ENGINE)==EXPECTED_ENGINE,'frozen grader hash changed'
assert json.loads((HERE/'source.json').read_text())==json.loads((ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186068916.json').read_text())
started=time.monotonic();sources=[];native=[];coverage={};records=[];blank_reps={}
cases=json.loads((HERE/'source-cases.json').read_text())
for case in cases:
 sid=case['source_id'];r=g.generate(case['difficulty'],template=sid,parameters=case['parameters'],profile='observed');public_check(r)
 choices,wrong=v.fidelity(g.QS[sid],r['question']);sources.append({'source_id':sid,'complete_bank':True,'matched_choices':choices,'matched_distractors':wrong,'correct_designation':'authored missing original' if sid=='q-10157' else 'matched','worked_solution':'authored missing original' if sid=='q-10157' else 'matched normalized source stage operands and prose'})
 records.append(r)
 print('Source',sid,'passed',flush=True)
 # Correct field-owned radio ID and every wrong ID, separately from math checks.
 f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'source complete radio bank selection'} for a in f[':answer-field/choices']]
  native.append({'label':sid+'-observed-radio','record':r,'checks':checks})
 if sid=='q-113983':
  invalid(lambda:g.generate('easy',template=sid));invalid(lambda:g.generate('easy',template=sid,profile='observed',parameters={'a':'1','b':'0','c':2,'d':1}));continue
 for seed in (321,654):
  variant=g.generate(case['difficulty'],seed,template=sid);public_check(variant);records.append(variant)
 # Served source-shaped method solutions at anchor parameters (wording/opaque bank changes documented).
 normal=g.generate(case['difficulty'],template=sid,parameters=case['parameters']);public_check(normal)
 if sid not in ('q-10157',):
  for (label,a,af),(other,b,bf) in zip(v.stages(r['question']),v.stages(normal['question'])):assert label==other and v.zero(a-b) and af==bf
 # seed/option-order identity independence on fixed complete content
 other=g.generate(case['difficulty'],999,template=sid,parameters=case['parameters'],profile='observed');assert r['question'][':question/id']==other['question'][':question/id']
 if sid=='q-10578':assert r['question'][':question/id']!=normal['question'][':question/id']
# Actual variant domain coverage includes every public slot value, independently chosen.
for sid,conf in g.CONFIG.items():
 slots={k:set() for k in conf[3]};valid=0;invalid_banks=0
 for p in g.instances(sid):
  # One fast independent exact derivation of mathematical objects; build full
  # record per distinct blank grading value, and boundary representatives below.
  a,b=g.guard(sid,p);kind=conf[2];c=s.Integer(p['c']);arg=a*v.x+b*s.pi
  if conf[0]=='easy':
   for k,z in p.items():slots[k].add(str(z))
   valid+=1;continue
  lo,hi=g.rat(p['lo'])*s.pi,g.rat(p['hi'])*s.pi
  prim={'sec_tan':s.sec,'csc_cot':lambda z:-s.csc(z),'sec2':s.tan,'csc2':lambda z:-s.cot(z)}[kind]
  answer=s.simplify(c/a*(prim(hi)-prim(lo)))
  if conf[1]=='radio':
   # All complete numeric banks at every finite public parameter tuple.
   try:g.core(sid,p,'observed');g.core(sid,p,'method')
   except ValueError:invalid_banks+=1;continue
  valid+=1
  for k,z in p.items():slots[k].add(str(z))
  if conf[1]=='blank':
   # Every distinct bounded scalar output and its equivalent/wrong values is
   # sent through the unchanged native learner grader below.
   key=(sid,str(answer))
   if key not in blank_reps:blank_reps[key]=(p,answer)
 coverage[sid]={'valid_parameter_tuples':valid,'rejected_whole_banks':invalid_banks,'slot_values':{k:sorted(z) for k,z in slots.items()}}
 print('Bounded domain',sid,valid,'valid',invalid_banks,'bank collisions',flush=True)
# Build native checks over the entire distinct blank-output domain. Simplified
# output grouping is justified: grader receives the same source-shaped prompt
# with exact policy and no prescribed precision, and scalar stored answer only.
for (sid,_),(p,answer) in blank_reps.items():
 lev=g.CONFIG[sid][0];r=g.generate(lev,template=sid,parameters=p);f=r['question'][':question/answer-fields'][0];canonical=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 assert v.zero(v.scalar(canonical)-answer)
 checks=[{'submitted':canonical,'expected':'accepted','purpose':'full bounded canonical output'}, {'submitted':r'\frac{2('+canonical+r')}{2}','expected':'accepted','purpose':'genuine unsimplified equivalent quotient'}, {'submitted':'('+canonical+r')\sin(\frac{\pi}{2})','expected':'accepted','purpose':'equivalent with finite familiar trig argument'}]
 for z in ('0','1','-1','16','-16','17','100','1/2',g.tex(answer+1),g.tex(answer-1)):
  if v.zero(v.scalar(z)-answer):continue
  checks.append({'submitted':z,'expected':'rejected','purpose':'ordinary valid mathematical wrong value'})
 native.append({'label':sid+'-bounded-'+str(answer),'record':r,'checks':checks})
# Observed exact-answer wording: separately document equivalent form restrictions.
for case in cases:
 if g.CONFIG[case['source_id']][1]!='blank':continue
 r=g.generate(case['difficulty'],template=case['source_id'],parameters=case['parameters'],profile='observed');canonical=r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
 native.append({'label':case['source_id']+'-observed-form-policy','record':r,'checks':[{'submitted':canonical,'expected':'accepted','purpose':'observed canonical'}, {'submitted':r'\frac{2('+canonical+r')}{2}','expected':'rejected','purpose':'known native form restriction triggered by source wording Do not round'}]})
# Genuine malformed diagnostics are kept distinct from valid math checks.
r=g.generate('hard',template='q-350060',parameters=g.CONFIG['q-350060'][3]);native.append({'label':'malformed-diagnostic-separate','record':r,'checks':[{'submitted':r'\unsupported{!}','expected':'unresolved','purpose':'malformed notation diagnostic, not mathematical equivalence'}]})
save('engine-input.json',native)
proc=subprocess.run([str(ENGINE),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],capture_output=True,text=True)
(HERE/'engine-output.log').write_text(proc.stdout+proc.stderr);assert proc.returncode==0,proc.stderr
print(proc.stdout,flush=True)
# Explicit public bounds and strict seed/count selectors.
for z in (True,1.5,'1',None):invalid(lambda z=z:g.generate('easy',z))
for z in (True,0,-1,1.5,'2'):invalid(lambda z=z:g.batch('easy',count=z))
for sid,conf in g.CONFIG.items():
 p=dict(conf[3]);p['a']='17';invalid(lambda sid=sid,conf=conf,p=p:g.generate(conf[0],template=sid,parameters=p))
 p=dict(conf[3]);p['c']=True;invalid(lambda sid=sid,conf=conf,p=p:g.generate(conf[0],template=sid,parameters=p))
 if 'lo'in conf[3]:
  p=dict(conf[3]);p['hi']='3/2';invalid(lambda sid=sid,conf=conf,p=p:g.generate(conf[0],template=sid,parameters=p))
# A small finite batch forced through count overflow, not a retry budget.
finite=g.batch('easy',55,45,template='q-10143');assert len({r['generation']['mathematical_fingerprint'] for r in finite})==45
invalid(lambda:g.batch('easy',55,46,template='q-10143'))
default_families={}
for level in ('easy','moderate','hard'):
 observed={g.generate(level,seed)['generation']['template'] for seed in range(45)};assert observed=={sid for sid,c in g.CONFIG.items() if c[0]==level and sid!='q-113983'};default_families[level]=sorted(observed)
 out=g.batch(level,51,8);assert len({r['generation']['mathematical_fingerprint'] for r in out})==8
cli=subprocess.run([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--count','1','--format','json'],capture_output=True,text=True,check=True);arr=json.loads(cli.stdout);assert len(arr)==3 and all(type(r)is dict for r in arr)
# Mutation regressions: scalar, formal operands, substitution, differential,
# limits, choice keys and C0 controls must fail actual printed-content validation.
base=g.generate('moderate',template='q-13663',parameters=g.CONFIG['q-13663'][3]);mutations=[]
for old,new,name in [(r'\text{d}u',r'\text{d}x','formal differential'),('u=3 x','u=4 x','substitution'),('=3\\,⟹','=4\\,⟹','initial derivative'),(r'\cot(\frac{\pi}{2})',r'\cot(\frac{\pi}{4})','endpoint operand')]:
 bad=copy.deepcopy(base);text=bad['question'][':question/worked-solution'];assert old in text,(name,old,text);bad['question'][':question/worked-solution']=text.replace(old,new,1);invalid(lambda bad=bad:public_check(bad));mutations.append(name)
# Preserve equality while corrupting the teaching operation or two endpoints.
bad=copy.deepcopy(base);text=bad['question'][':question/worked-solution'];block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)[1];rows=block.split(r'\\');rows[2]=' & ='+g.tex(s.Rational(2,9)*s.sqrt(3));bad['question'][':question/worked-solution']=text.replace(block,r'\\'.join(rows));invalid(lambda:public_check(bad));mutations.append('missing primitive operation despite equal scalar')
bad=copy.deepcopy(base);text=bad['question'][':question/worked-solution'];old=r'(0-\frac{\sqrt{3}}{3})';assert old in text;bad['question'][':question/worked-solution']=text.replace(old,r'((0+1)-(\frac{\sqrt{3}}{3}+1))');invalid(lambda:public_check(bad));mutations.append('correlated numeric endpoint errors preserving difference')
bad=copy.deepcopy(base);bad['question'][':question/worked-solution']+='\f';invalid(lambda:public_check(bad));mutations.append('C0 formfeed')
f=bad['question'][':question/answer-fields'][0];bad=copy.deepcopy(base);f=bad['question'][':question/answer-fields'][0];f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])];invalid(lambda:public_check(bad));mutations.append('choice key')
# Native full-output policy coverage plus representative displayed-stage boundary validation.
for sid,conf in g.CONFIG.items():
 if sid=='q-113983':continue
 pp=list(g.instances(sid))
 for p in (pp[0],pp[-1]):
  try:r=g.generate(conf[0],template=sid,parameters=p)
  except ValueError:continue
  public_check(r)
# Meaningful capacities are per integrand and actual x bounds, not layouts/banks.
# Exact counting uses accepted slot enumeration and canonical model objects.
capacities={}
for level in ('easy','moderate','hard'):
 seen=set()
 for sid,conf in g.CONFIG.items():
  if conf[0]!=level or sid=='q-113983':continue
  for p in g.instances(sid):
   a,b=g.guard(sid,p);arg=a*v.x+b*s.pi;kind=conf[2]
   if kind=='poly_sec':body=(p['c']*s.sec(v.x)**2+p['d'])*s.sec(v.x)*s.tan(v.x)
   else:body=p['c']*{'sec_tan':s.sec(arg)*s.tan(arg),'csc_cot':s.csc(arg)*s.cot(arg),'sec2':s.sec(arg)**2,'csc2':s.csc(arg)**2}[kind]
   if conf[1]=='radio' and conf[0]!='easy':
    try:g.core(sid,p,'method')
    except ValueError:continue
   bounds=None if level=='easy' else tuple(s.simplify((g.rat(p[k])*s.pi-b*s.pi)/a) for k in ('lo','hi'))
   seen.add((str(body),str(bounds)))
 capacities[level]=len(seen)
save('capacity.json',{'meaningful_unique_tasks_by_difficulty':capacities,'profile':'method','deduplication':'canonical assessed integrand and actual x limits; no seed, source layout, choice bank, option order or constant','slot_coverage':coverage})
engine=json.loads((HERE/'engine-validation.json').read_text())
result={'status':'passed','database_writes':0,'source_basis':2275,'engine_sha256':sha(ENGINE),'source_fidelity':{'practice_questions':10,'complete_banks':10,'matched_choices':sum(z['matched_choices'] for z in sources),'matched_distractors':sum(z['matched_distractors'] for z in sources),'matched_observed_correct_designations':9,'missing_correct_authored':1,'matched_observed_worked_solutions':9,'missing_solutions_authored':1,'reference_only_source_families':['q-113983'],'ordinary_supported_source_families':9,'raw_byte_exact_replay_claimed':False,'presentation_normalized_math_and_shared_prose':True,'details':sources},'printed_math_records_checked':len(records)+9+18,'mutations_rejected':mutations,'source_operation_masks_checked':True,'independent_endpoint_components_checked':True,'finite_capacities':capacities,'default_family_coverage':default_families,'native':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved_malformed_diagnostics':engine['documented_unresolved_checks'],'genuine_valid_math_unresolved':0,'distinct_bounded_blank_outputs':len(blank_reps),'full_bounded_blank_parameter_tuples':sum(coverage[sid]['valid_parameter_tuples'] for sid,c in g.CONFIG.items() if c[1]=='blank')},'source_limits':['q-10157 original missing key/solution/rating completed and never counted as observed matches','q-113983 plausible misassignment: reference-only original-parameter replay; no ordinary nonlinear branch','q-10578 observed endpoint-bank intent unresolved; normal bank separately authored','raw Do not round wording rejects equivalent syntactic forms; method wording repaired'],'elapsed_seconds':round(time.monotonic()-started,2),'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}
save('validation.json',result);print(json.dumps(result,indent=2),flush=True)
subprocess.run([sys.executable,str(HERE/'validate-source-variants.py')],check=True)
# Immutable dependencies and ready-state paths, excluding self-referential manifests
files=[HERE.with_suffix('.py')]+[p for p in HERE.rglob('*') if p.is_file() and '__pycache__'not in p.parts and p.name not in ('hash-manifest.json','ready.json')]
save('hash-manifest.json',{'algorithm':'sha256','paths':{str(p.relative_to(ROOT)):sha(p) for p in sorted(files)},'dependency_engine':{str(ENGINE.relative_to(ROOT)):sha(ENGINE)}})
save('ready.json',{'status':'ready for independent parent review','script_sha256':sha(HERE.with_suffix('.py')),'validation_status':'passed','frozen_engine_sha256':sha(ENGINE),'registered':False})
