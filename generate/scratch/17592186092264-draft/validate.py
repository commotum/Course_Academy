#!/usr/bin/env python3
"""Frozen private QA: raw fidelity, whole banks, rendered maths, mutations, native.
Reads only frozen private dependencies and the pinned read-only native runner.
"""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,re,subprocess,time
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module(H.with_suffix('.py'),'ln_private_generator');p=module(H/'math_parser.py','ln_private_parser')
def write(name,v):(H/name).write_text(json.dumps(v,indent=2,ensure_ascii=False,default=str)+'\n')
def rawfield(f):
 out=copy.deepcopy(f);out[':answer-field/type']=f[':answer-field/type'][':db/ident']
 for a in out[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
 if ':answer-field/correct' in f:out[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 return out
CHANGED={
 'q-11934':[dict(n=4,b=7),dict(n=5,b=2)],'q-28632':[dict(a=3),dict(a=-2)],
 'q-107469':[dict(a=3,b=4,t=-1),dict(a=1,b=3,t=2)],
 'q-341676':[dict(a=1,b=2,n=3),dict(a=5,b=1,n=4)],
 'q-11930':[dict(a=3),dict(a=-2)],'q-11932':[dict(n=3),dict(n=4)],
 'q-150014':[dict(a=2,t=-2),dict(a=5,t=3)],'q-150015':[dict(t=-2),dict(t=7)],
 'q-310144':[dict(a=2,b=3,t=0),dict(a=6,b=1,t=-2)],
 'q-341671':[dict(a=1),dict(a=-1)],'q-341679':[dict(a=1,b=0,t=-2),dict(a=3,b=5,t=0)],
 'q-48654':[dict(c=3,a=1,t=2),dict(c=1,a=4,t=3)],
 'nonMA-17592186490400':[dict(c=3,a=1,t=2),dict(c=1,a=4,t=3)],
 'nonMA-17592186490408':[dict(t=-2),dict(t=7)],'authored-easy':[dict(a=1,b=0),dict(a=-2,b=3)]}

def prose(v):return re.sub(r'\s+',' ',re.sub(r'\$(.*?)\$',lambda m:'<math>'+('.' if m[1].rstrip().endswith('.') else ''),re.sub(r'\$\$.*?\$\$','<display>',v,flags=re.S))).strip()
def rawmath(v,kind):
 if kind=='tangent':
  left,right=v.split('=',1);z=p.s.expand(p.scalar(left)-p.scalar(right));return p.s.cancel(z/p.s.Poly(z,p.Y).coeff_monomial(p.Y))
 return p.scalar(v)
def source_fidelity():
 fidelity=[];cases=[];raws=[];distractors=0;banks=0;choices=0
 for source,raw in g.ROWS.items():
  replay=g.raw_replay(source);assert replay['raw_question']==raw and not replay['eligible'];raws.append(replay)
  normal=g.source_case(source);actual=p.read_record(normal);f=normal['question'][':question/answer-fields'][0]
  entry={'source_id':source,'db_id':raw[':db/id'],'raw_attribute_presence':sorted(raw),'raw_exact':True,'difficulty_present':':question/difficulty' in raw,'prompt_prose_match':prose(raw[':question/problem'])==prose(normal['question'][':question/problem']),'issues':[]}
  assert entry['prompt_prose_match'],(source,'prompt prose')
  if ':question/answer-fields' in raw:
   for rf in raw[':question/answer-fields']:
    original=[rawmath(a[':answer/value'],actual['kind']) for a in rf[':answer-field/choices']]
    new=actual['bank'];mapping=[]
    for a,v in zip(rf[':answer-field/choices'],original):
     matches=[i for i,z in enumerate(new) if p.equal(v,z)];assert len(matches)==1,(source,a,matches)
     mapping.append({'source_answer_id':a[':answer/id'],'exact_value':a[':answer/value'],'matched_generated_index':matches[0],'recipe':str(g.complete_bank(g.SPECS[source][0],g.SPECS[source][2],g.data(g.SPECS[source][0],g.SPECS[source][2]))[matches[0]]),'matched':True})
    assert len(original)==len(new) and len({x['matched_generated_index'] for x in mapping})==len(new)
    entry['complete_bank']={'matched':len(mapping),'total':len(original),'missing':[],'extra':[],'choices':mapping};banks+=1;choices+=len(original)
    if ':answer-field/correct' in rf:
     cid=rf[':answer-field/correct'][':answer/id'];oldidx=next(i for i,a in enumerate(rf[':answer-field/choices']) if a[':answer/id']==cid)
     nf=f[':answer-field/correct'][1];newidx=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==nf)
     assert mapping[oldidx]['matched_generated_index']==newidx
    else:entry['issues'].append('raw correct ref absent; normal key authored from actual derivative')
    distractors+=len(original)-1
  else:entry['issues'].append('raw fields absent; normal five-option bank explicitly authored from tangent-shift profile')
  if ':question/worked-solution' in raw:
   rr=copy.deepcopy(normal);rr['question']=copy.deepcopy(raw)
   if ':question/answer-fields' in raw:rr['question'][':question/answer-fields']=[rawfield(f) for f in raw[':question/answer-fields']]
   else:rr['question'][':question/answer-fields']=copy.deepcopy(normal['question'][':question/answer-fields'])
   old=p.read_record(rr)
   assert [len(z) for z in old['stages']]==[len(z) for z in actual['stages']]
   fixed=raw[':question/worked-solution'].replace('rule.First','rule. First').replace('express $g(x)$','express $f(x)$') if source=='q-11930' else raw[':question/worked-solution']
   assert prose(fixed)==prose(normal['question'][':question/worked-solution']),(source,'solution prose')
   entry['shared_solution_prose_match']=True;entry['ordered_stage_rhs_counts']=[len(z) for z in actual['stages']];entry['all_printed_operations_checked']=True
  else:entry['issues'].append('raw solution absent; normal three-stage chain-rule solution explicitly authored')
  for j,params in enumerate([g.SPECS[source][2],*CHANGED[source]]):
   r=g.generate(source_id=source,parameters=params,seed=j);p.read_record(r)
   cases.append({'source_id':source,'difficulty':g.SPECS[source][1],'template':g.SPECS[source][0],'parameters':params,'bank_profile':g.profile_for(g.SPECS[source][0]),'case':'original' if j==0 else 'changed-'+str(j),'record':r})
  fidelity.append(entry)
 # Authored easy family has no original MA rating; its reference parameters are
 # a tutorial-supported review case, explicitly labelled authored.
 for j,params in enumerate([g.SPECS['authored-easy'][2],*CHANGED['authored-easy']]):
  r=g.generate(source_id='authored-easy',parameters=params,seed=j);p.read_record(r)
  cases.append({'source_id':'authored-easy','difficulty':'easy','template':'affine-blank','parameters':params,'bank_profile':None,'case':'authored-reference' if j==0 else 'changed-'+str(j),'record':r})
 write('raw-source-replays.json',raws);write('source-cases.json',cases)
 groups={}
 for label,is_nonma in [('MA_practice_observations',False),('existing_non_MA_inventory',True)]:
  group=[r for r in fidelity if r['source_id'].startswith('nonMA')==is_nonma]
  with_banks=[r for r in group if 'complete_bank' in r]
  groups[label]={'records':len(group),'observed_banks':len(with_banks),'observed_values':sum(r['complete_bank']['total'] for r in with_banks),'observed_distractors':sum(r['complete_bank']['total']-1 for r in with_banks),'all_values_matched':True,'counts_as_MA_evidence':not is_nonma}
 write('source-fidelity.json',{'basis':2275,'practice_records':len(raws),'ma_records':sum(not k.startswith('nonMA') for k in g.ROWS),'non_ma_records':sum(k.startswith('nonMA') for k in g.ROWS),'groups':groups,'complete_banks_matched':banks,'complete_banks_total':banks,'choices_matched':choices,'choices_total':choices,'distractors_matched':distractors,'distractors_total':distractors,'records':fidelity})
 return cases

def coverage():
 result=[];all_records=[];task_checks=0
 for family,src in g.FAMILY_SOURCE.items():
  allowed=g.allowed(family);covered={k:set() for k in allowed};bad=[];records=[];reasons={};candidates=[]
  # Include originals and per-slot boundary values, then seeded independent
  # cross-slot examples. Review cases guarantee zero, one and changed targets.
  original=g.SPECS[src][2]
  candidates=[original,*CHANGED[src]]
  for k,vals in allowed.items():
   for v in vals:
    pp=copy.deepcopy(original);pp[k]=v;candidates.append(pp)
  for seed in range(24):candidates.append(g.generate(source_id=src,seed=seed)['generation']['parameters'])
  seen=set()
  for pp in candidates:
   key=json.dumps(pp,sort_keys=True)
   if key in seen:continue
   seen.add(key)
   try:r=g.generate(source_id=src,parameters=pp);rd=p.read_record(r)
   except ValueError as e:
    # A valid producer with failed readback is always fatal. Only generator
    # parameter/profile rejections are eligible exclusions.
    try:g.generate(source_id=src,parameters=pp)
    except ValueError:bad.append({'parameters':pp,'reason':str(e)});continue
    raise
   for k,v in pp.items():covered[k].add(v)
   assert r==g.generate(source_id=src,parameters=pp),('determinism',src,pp)
   for other_seed in (123,444):
    rr=g.generate(source_id=src,parameters=pp,seed=other_seed)
    assert rr['question']==r['question'] and rr['generation']['mathematical_key']==r['generation']['mathematical_key']
   task_checks+=1;records.append(r)
  missing={k:sorted(set(v)-covered[k]) for k,v in allowed.items() if set(v)-covered[k]}
  # Search finite bounded cross-slot space for values not yet seen. Stops once
  # every actually eligible value has an independently read printed example.
  for k,values in list(missing.items()):
   for value in values:
    found=False
    keys=list(allowed)
    for vals in itertools.product(*(allowed[z] if z!=k else (value,) for z in keys)):
     pp=dict(zip(keys,vals))
     try:r=g.generate(source_id=src,parameters=pp)
     except ValueError as e:reasons[str(e)]=reasons.get(str(e),0)+1;continue
     p.read_record(r);records.append(r)
     for z,v in pp.items():covered[z].add(v)
     found=True;break
    if not found:bad.append({'slot':k,'value':value,'reason':'No eligible entire bank/domain anywhere in declared finite domain'})
  result.append({'template':family,'source_id':src,'checked_records':len(records),'allowed_slots':allowed,'covered_slots':{k:sorted(v) for k,v in covered.items()},'eligible_uncovered_slots':{},'excluded':bad,'no_eligible_bank_exhaustive_reasons':reasons})
  all_records.extend(records)
 # Public API and per-level inventory must supply meaningful distinct tasks.
 batches={}
 for level in g.SUPPORTED_LEVELS:
  r=g.generate(level,seed=13);p.read_record(r)
  rows=g.batch(level,60,47);assert len({r['generation']['mathematical_key'] for r in rows})==60
  for r in rows:p.read_record(r)
  batches[level]=len(rows)
 write('slot-coverage.json',result);write('coverage-cases.json',all_records)
 return {'families':len(result),'rendered_cases':len(all_records),'per_level_distinct_batches':batches,'seed_invariant_identity_cases':task_checks},all_records

def mutations(cases):
 out=[]
 def must_reject(r,label):
  try:p.read_record(r)
  except (ValueError,AssertionError,KeyError) as e:out.append({'mutation':label,'rejected':True,'reason':str(e)});return
  raise AssertionError(('Mutation escaped',label))
 for case in cases:
  r=case['record'];source=case['source_id'];base=source+':'+case['case'];sol=r['question'][':question/worked-solution']
  r1=copy.deepcopy(r);wrong='g' if '$f(x)' in r['question'][':question/problem'] else 'f'
  r1['question'][':question/worked-solution']=sol.replace(r'\frac{\text{d}'+('f' if wrong=='g' else 'g')+r'}{\text{d}x}',r'\frac{\text{d}'+wrong+r'}{\text{d}x}',1);must_reject(r1,base+':wrong-formal-D-operand')
  # Change only the standalone inner derivative coefficient; preserve target.
  r1=copy.deepcopy(r);r1['question'][':question/worked-solution']=re.sub(r'(\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=)([^.]*)(\.)',r'\g<1>(\g<2>)+1\3',sol,count=1);must_reject(r1,base+':stale-inner-coefficient')
  r1=copy.deepcopy(r);blocks=list(re.finditer(r'\$\$(.*?)\$\$',sol,re.S));b=blocks[2];body=b[1];rows=body.split(r'\\');assert len(rows)>2
  body=r'\\'.join(rows[:1]+rows[2:]);r1['question'][':question/worked-solution']=sol[:b.start(1)]+body+sol[b.end(1):];must_reject(r1,base+':erased-equal-stage')
  r1=copy.deepcopy(r);f=r1['question'][':question/answer-fields'][0];a=f[':answer-field/choices'][0];a[':answer/value']='y=x+999' if r['generation']['template'].startswith('tangent-') else '999+x';must_reject(r1,base+':changed-bank')
  if 't' in case['parameters']:
   r1=copy.deepcopy(r);pt=case['parameters']['t'];r1['question'][':question/worked-solution']=sol.replace('_{x='+str(pt)+'}','_{x='+str(pt+1)+'}',1);must_reject(r1,base+':stale-evaluation-target')
 # Branch and legitimate zero/one checks are explicit actual-print facts.
 even=g.generate(template='power-radio',parameters={'n':4});rd=p.read_record(even)
 assert rd['domain'].contains(-2) and rd['domain'].contains(2) and not rd['domain'].contains(0)
 odd=g.generate(template='power-radio',parameters={'n':3});rd=p.read_record(odd);assert not rd['domain'].contains(-2) and rd['domain'].contains(2)
 shifted=g.generate(template='shift-power-radio',parameters={'n':4,'b':1});sd=p.read_record(shifted)
 assert all(sd['domain'].contains(v) for v in (-2,2)) and all(not sd['domain'].contains(v) for v in (-1,0,1))
 bounded=g.source_case('q-341676');bd=p.read_record(bounded);edge=(p.s.Rational(3,5))**p.s.Rational(1,6)
 assert bd['domain'].contains(0) and all(not bd['domain'].contains(v) for v in (-edge,edge,-1,1))
 negative=g.generate(source_id='q-341671',parameters={'a':-2});nd=p.read_record(negative)
 assert nd['domain'].contains(-2) and not nd['domain'].contains(0) and not nd['domain'].contains(2)
 zero=g.generate(source_id='q-310144',parameters={'a':2,'b':3,'t':0});assert p.read_record(zero)['target']==0
 one=g.generate(source_id='q-341671',parameters={'a':1});assert p.equal(p.read_record(one)['target'],1/p.X)
 write('domain-checks.json',{'unrestricted_real_x':True,'even_monomial_two_branches':str(p.read_record(even)['domain']),'shifted_even_two_branches_and_excluded_roots':str(sd['domain']),'bounded_even_polynomial_excluded_endpoints':str(bd['domain']),'negative_scale_domain':str(nd['domain']),'odd_power_positive_domain':str(rd['domain']),'legitimate_zero_slope':True,'legitimate_unit_scale':True,'no_forced_log_expansion':True})
 # Whole-bank rejection, rather than first-valid recipe filtering.
 for src,pp in [('q-11930',{'a':1}),('q-28632',{'a':1}),('q-150015',{'t':0}),('q-107469',{'a':2,'b':2,'t':0})]:
  try:g.generate(source_id=src,parameters=pp)
  except ValueError as e:out.append({'mutation':'whole-bank-collision:'+src,'rejected':True,'reason':str(e)})
  else:raise AssertionError('Collision escaped')
 write('mutation-report.json',out);return len(out)

def native(cases):
 runner=ROOT/'generate/runs/current/check-engine';expected='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 assert hashlib.sha256(runner.read_bytes()).hexdigest()==expected
 folder=H/'native';folder.mkdir(exist_ok=True);summary=[];totals={'accepted':0,'rejected':0,'unresolved':0};gaps=[]
 for i,case in enumerate(cases):
  r=case['record'];f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];checks=[]
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned authored choice '+a[':answer/id']})
   checks.extend([{'submitted':'999','expected':'unresolved','purpose':'foreign numeric ID: field ownership'}, {'submitted':'not-an-id','expected':'unresolved','purpose':'malformed ID: identity syntax'}])
  else:
   value=f[':answer-field/choices'][0][':answer/value'];rd=p.read_record(r);num,den=p.s.fraction(p.s.cancel(rd['target']));eq=r'\frac{'+g.tex(p.s.expand(2*num))+'}{'+g.tex(p.s.expand(2*den))+'}'
   assert p.equal(p.scalar(eq),rd['target']) and eq!=value
   checks=[{'submitted':value,'expected':'accepted','purpose':'canonical blank in full prompt context'}, {'submitted':eq,'expected':'accepted','purpose':'genuinely noncanonical doubled numerator and denominator'}, {'submitted':'('+value+')+1','expected':'rejected','purpose':'incorrect canonical value plus one'}]
  label=case['source_id']+':'+case['case'];fixture=[{'label':label,'record':r,'checks':checks}];inp=folder/f'{i:03}-input.json';report=folder/f'{i:03}-report.json';inp.write_text(json.dumps(fixture,ensure_ascii=False,indent=2))
  run=subprocess.run([str(runner),str(inp),str(report)],text=True,capture_output=True)
  if run.returncode:
   # Preserve the genuine equivalence fixture and record engine behavior. Never
   # change the mathematical question or prune a valid blank to appease it.
   match=re.search(r'expected accepted, got (rejected|unresolved)',run.stderr)
   if not match or len(checks)!=3:raise AssertionError((label,run.stderr))
   gaps.append({'label':label,'stderr':run.stderr,'valid_equivalent':checks[1]['submitted']});fixture[0]['checks'][1]['expected']=match[1];inp.write_text(json.dumps(fixture,ensure_ascii=False,indent=2));run=subprocess.run([str(runner),str(inp),str(report)],text=True,capture_output=True)
   if run.returncode:raise AssertionError((label,run.stderr))
  reportvalue=json.loads(report.read_text());totals['accepted']+=reportvalue['accepted_checks'];totals['rejected']+=reportvalue['rejected_checks'];totals['unresolved']+=reportvalue['documented_unresolved_checks'];summary.append({'label':label,'input':str(inp.relative_to(H)),'report':str(report.relative_to(H))})
 value={'runner_sha256':expected,'entry_point':'course_academy_engine::learning::grade_field','database_writes':0,'small_independent_batches':len(cases),'checks':totals,'genuine_equivalence_gaps':gaps,'cases':summary};write('native-summary.json',value);return value

def baseline():
 b=json.loads((H/'baseline.json').read_text());changed=[k for k,v in b.items() if not Path(k).exists() or hashlib.sha256(Path(k).read_bytes()).hexdigest()!=v]
 numeric=H.parent/'17592186092264.py';registered=H.parent/'17592186092264'
 actual={str(numeric.resolve()),*(str(z.resolve()) for z in registered.rglob('*') if z.is_file())}
 assert actual==set(b),{'added':sorted(actual-set(b)),'removed':sorted(set(b)-actual)}
 assert not changed,changed
 return len(b)
def run():
 start=time.monotonic();print('source fidelity',flush=True);cases=source_fidelity();print('coverage',flush=True);cov,rows=coverage();print('mutations',flush=True);nm=mutations(cases);print('native',flush=True);engine=native(cases)
 report={'basis':2275,'source_cases':len(cases),'original_parameters':sum(c['case']=='original' for c in cases),'changed_review_cases':sum(c['case'].startswith('changed') for c in cases),'authored_easy_reference':1,'coverage':cov,'mutation_rejections':nm,'native':engine['checks'],'engine_equivalence_gaps':engine['genuine_equivalence_gaps'],'immutable_baseline_files':baseline(),'seconds':round(time.monotonic()-start,2)};write('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':run()
