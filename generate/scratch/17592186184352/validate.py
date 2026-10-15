"""Fail-closed private validation; never opens or writes a database."""
import copy,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
g=module('definite_generator',D.with_suffix('.py'));p=module('definite_readback',D/'readback.py')
def save(name,v):(D/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def equivalent(record):
 name=record['generation']['template'];q=record['question'];sol=q[':question/worked-solution']
 if name=='exponential_ratio_blank' and record['generation']['bank_profile']=='source_blank':
  table=[z for z in sol.splitlines() if z.startswith('| $u$')][0]
  nums=[int(v) for v in __import__('re').findall(r'\$(\d+)\$',table)]
  assert len(nums)==2
  # Keep the endpoint ratio as an independently unreduced fraction. The
  # engine does not establish the general logarithm-difference identity.
  coef=p.scalar(p.rows(sol)[-2].split('=',1)[1].split('(',1)[0])
  return g.tex(coef)+g.ln(g.fr(2*nums[1],2*nums[0]))
 # Unreduced endpoint expressions and uncombined logarithmic differences.
 rows=p.rows(sol);return p.clean(rows[-2].split('=',1)[1]).strip()
def native_checks(record):
 q=record['question'];f=q[':question/answer-fields'][0];checks=[]
 correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);A=p.scalar(correct[':answer/value'])
 if f[':answer-field/type'].endswith('/radio'):
  checks += [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a==correct else 'rejected','purpose':'every owned option'} for a in f[':answer-field/choices']]
 else:
  checks += [{'submitted':correct[':answer/value'],'expected':'accepted','purpose':'canonical exact answer'},{'submitted':equivalent(record),'expected':'rejected' if record['generation']['bank_profile']=='source_presentation' else 'accepted','purpose':'documented source wording form restriction' if record['generation']['bank_profile']=='source_presentation' else 'unreduced source endpoint evaluation'}]
  for v,label in [('0','ordinary zero'),('1','ordinary one'),(g.tex(A+1),'ordinary answer plus one')]:
   checks.append({'submitted':v,'expected':'accepted' if p.equal(p.scalar(v),A) else 'rejected','purpose':label})
 return {'record':record,'label':q[':question/id']+'-'+record['generation']['bank_profile'],'checks':checks}
def main():
 engine=ROOT/'generate/runs/current/check-engine';sha=hashlib.sha256(engine.read_bytes()).hexdigest();assert sha=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 refs=json.loads((D/'reference-manifest.json').read_text())
 for rel,h in refs.items():assert hashlib.sha256((D/rel).read_bytes()).hexdigest()==h
 sourcecases=[];review=[];native=[];counts={};fidelity={'questions':0,'bank_values':0,'distractors':0,'complete_banks':0,'existing_correct_refs':0,'inferred_correct_refs':0,'source_solutions':0,'authored_missing_solutions':0,'matched_ordered_rows':0,'raw_exact_prompts':0,'raw_exact_solutions':0}
 signatures={}
 for name,sid in g.TEMPLATES.items():
  old=g.SOURCES[sid];level=g.DIFFICULTY[name];profile='source_bank' if name.endswith('radio') else 'source_presentation'
  c={'source_id':sid,'level':level,'template':name,'parameters':g.ANCHORS[name],'bank_profile':profile};sourcecases.append(c)
  r=g.generate(level,template=name,parameters=c['parameters'],profile=profile);q=r['question'];p.check(q)
  old_prompt=next(t for t in p.blocks(old[':question/problem']) if r'\int' in t).strip().rstrip('= .')
  old_C,old_F,old_var,old_L,old_H,after=p.integral_parts(old_prompt)
  new_C,new_F,new_var,new_L,new_H,after=p.integral_parts(next(t for t in p.blocks(q[':question/problem']) if r'\int' in t).strip().rstrip('= .'))
  assert p.equal(old_C*old_F,new_C*new_F) and p.equal(old_L,new_L) and p.equal(old_H,new_H)
  of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
  assert of[':answer-field/type'][':db/ident']==nf[':answer-field/type'] and of[':answer-field/key']==nf[':answer-field/key']
  ovs=[p.scalar(a[':answer/value']) for a in of[':answer-field/choices']];nvs=[p.scalar(a[':answer/value']) for a in nf[':answer-field/choices']]
  assert len(ovs)==len(nvs) and all(sum(p.equal(a,b) for b in nvs)==1 for a in ovs)
  if ':answer-field/correct' in of:
   actual=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert p.equal(p.scalar(actual),p.scalar(of[':answer-field/correct'][':answer/value']));fidelity['existing_correct_refs']+=1
  else:fidelity['inferred_correct_refs']+=1
  if ':question/worked-solution' in old:
   original=copy.deepcopy(q);original[':question/problem']=old[':question/problem'];original[':question/worked-solution']=old[':question/worked-solution']
   p.check(original)
   signatures[name]=p.signatures(old[':question/worked-solution']);assert p.signatures(q[':question/worked-solution'])==signatures[name]
   # Each original RHS is evaluated independently, including original endpoint
   # powers, factored scalar, and logarithm reduction; source blanks have an
   # extra MathML grouping brace around one evaluation bar.
   for row in p.rows(old[':question/worked-solution']):
    rhs=row.split('=',1)[1].strip()
    assert p.equal(p.expression(rhs),p.expression(old_prompt)),rhs
   fidelity['source_solutions']+=1;fidelity['matched_ordered_rows']+=len(p.rows(q[':question/worked-solution']))
  else:signatures[name]=p.signatures(q[':question/worked-solution']);fidelity['authored_missing_solutions']+=1
  fidelity['questions']+=1;fidelity['bank_values']+=len(ovs);fidelity['distractors']+=len(ovs)-1;fidelity['complete_banks']+=1
  fidelity['raw_exact_prompts']+=int(old[':question/problem']==q[':question/problem']);fidelity['raw_exact_solutions']+=int(old.get(':question/worked-solution')==q[':question/worked-solution'])
  review.append({'role':'faithful parameterized anchor','source_id':sid,'record':r})
  if name.endswith('radio'):native.append(native_checks(r))
  else:
   canonical=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])
   native.append(native_checks(r))
 save('source-cases.json',sourcecases)
 coverage={}
 for name in g.TEMPLATES:
  profiles=['authored_method_bank','source_bank'] if name.endswith('radio') else ['source_blank']
  coverage[name]={};level=g.DIFFICULTY[name]
  for profile in profiles:
   valid=0;excluded=0;slot_values={k:set() for k in g.ANCHORS[name]};ids=set();tasks=set()
   for params in g.parameters_for(name):
    try:r=g.generate(level,template=name,parameters=params,profile=profile)
    except ValueError as exc:
     assert 'ambiguous' in str(exc);excluded+=1;continue
    stats=p.check(r['question'],signatures[name])
    for k,v in stats.items():counts[k]=counts.get(k,0)+v
    for k,v in params.items():slot_values[k].add(v)
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    same=g.generate(level,seed=987,template=name,parameters=params,profile=profile);assert same['question'][':question/id']==r['question'][':question/id']
    ids.add(r['question'][':question/id']);tasks.add(r['generation']['task_fingerprint']);native.append(native_checks(r));valid+=1
    if params!=g.ANCHORS[name] and len([v for v in review if v['role']=='changed variant' and v['record']['generation']['template']==name])<2:review.append({'role':'changed variant','source_id':g.TEMPLATES[name],'record':r})
   coverage[name][profile]={'bounded_parameter_sets':len(g.parameters_for(name)),'eligible':valid,'whole_bank_exclusions':excluded,'content_ids':len(ids),'task_fingerprints':len(tasks),'slot_values':{k:sorted(v) for k,v in slot_values.items()}}
   print(name,profile,valid,excluded,flush=True)
 defaults={n:0 for n in g.TEMPLATES}
 for level in g.LEVELS:
  for seed in range(96):defaults[g.generate(level,seed)['generation']['template']]+=1
 assert all(defaults.values())
 assert g.task_fingerprint('quadratic_scaled_base_radio',dict(b=4,k=2))==g.task_fingerprint('quadratic_scaled_base_radio',dict(b=2,k=4))
 assert g.task_fingerprint('exponential_ratio_blank',dict(a=2,c=2,h=2,l=2,r=5))==g.task_fingerprint('exponential_ratio_blank',dict(a=3,c=2,h=3,l=2,r=5))
 # Mutations catch wrong printed givens/formal operands, stale bounds,
 # bad primitives, omitted stages despite unchanged numerical answer, and C0.
 mutations=[];base=g.generate('easy',template='natural_integer_radio',parameters=dict(c=5,b=3))
 for label,key,a,b in [('prompt','problem','5xe','6xe'),('derivative','worked-solution','=2x','=3x'),('bounds','worked-solution','| $u$ | $0$','| $u$ | $1$'),('primitive','worked-solution',r'\frac{5}{2}e^{u}',r'\frac{5}{3}e^{u}'),('correlated_endpoint','worked-solution',r'(e^{\ln(3)}-e^{0})',r'((e^{\ln(3)}+1)-(e^{0}+1))'),('control','worked-solution','Therefore,','Therefore,\x0c')]:
  changed=copy.deepcopy(base['question']);kk=':question/'+key;assert a in changed[kk];changed[kk]=changed[kk].replace(a,b,1)
  try:p.check(changed,signatures['natural_integer_radio'])
  except Exception:mutations.append(label)
  else:raise AssertionError('Mutation accepted: '+label)
 changed=copy.deepcopy(base['question']);t=changed[':question/worked-solution'];part=r'\int_{0}^{\sqrt{\ln(3)}}5e^{x^{2}}\cdot x\,\mathrm{d}x';assert part in t;changed[':question/worked-solution']=t.replace(part,r'\frac{5}{2}(3-1)',1)
 try:p.check(changed,signatures['natural_integer_radio'])
 except Exception:mutations.append('missing source regrouping stage, equal scalar')
 else:raise AssertionError('Equal-value structure mutation accepted')
 save('review.json',review);save('capacity.json',coverage);save('native-input.json',native)
 subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 # Separate malformed/foreign ownership diagnostics, never ordinary wrongs.
 radio=g.generate('easy',template='natural_integer_radio',parameters=dict(c=5,b=3));blank=g.generate('hard',template='exponential_ratio_blank',parameters=g.ANCHORS['exponential_ratio_blank'])
 log_example=g.generate('hard',template='exponential_ratio_blank',parameters=dict(a=2,c=2,h=1,l=2,r=5))
 diagnostics=[{'label':'foreign owned radio ID','record':radio,'checks':[{'submitted':'999999999','expected':'unresolved','purpose':'foreign ownership'}]},{'label':'malformed blank','record':blank,'checks':[{'submitted':'\\frac{','expected':'unresolved','purpose':'malformed syntax'}]},{'label':'logarithm difference parser limitation','record':log_example,'checks':[{'submitted':p.clean(p.rows(log_example['question'][':question/worked-solution'])[-2].split('=',1)[1]),'expected':'unresolved','purpose':'mathematically equivalent log difference unsupported by native rules'}]}]
 save('diagnostic-input.json',diagnostics);subprocess.run([str(engine),str(D/'diagnostic-input.json'),str(D/'diagnostic-report.json')],check=True)
 cli=json.loads(subprocess.check_output([sys.executable,str(D.with_suffix('.py')),'--difficulty','all','--count','1','--format','json'],text=True));assert len(cli)==3 and all(isinstance(r,dict) for r in cli)
 save('cli.json',cli)
 report={'status':'passed','basis':2275,'lineage':g.SOURCE['lineage'],'source_fidelity':fidelity,'independent_display_readback':counts,'default_family_coverage':defaults,'mutations_rejected':mutations,'public_bounded_native_records':len(native),'native_engine_sha256':sha,'native':json.loads((D/'native-report.json').read_text())|{'records':'native-report.json'},'diagnostics':'diagnostic-report.json','python':sys.version.split()[0],'sympy':s.__version__,'database_writes':0,'registered':False,'limitations':['q-30977 lacked original difficulty, correct reference, and solution; moderate/solution/correctness are independently authored repairs.','Source Do not round instruction has a native equivalent-entry form restriction; faithful presentation profile retained, normal exact wording repaired.','Opaque empirical source bank transports are evidence profiles; normal radios use separately authored complete method-derived banks.','Raw exact text fidelity is not claimed; presentation normalized, mathematical operands and ordered source stages replayed.']}
 report['limitations'].append('General logarithm differences can be mathematically equivalent yet unresolved by native rules; unreduced endpoint ratios are accepted throughout the hard domain. Diagnostics retain an actual unresolved example.')
 report['status']='review_required_native_equivalence_limitation'
 report['fidelity_status']='passed'
 report['displayed_math_status']='passed'
 report['native_supported_case_status']='passed'
 report['native_overall_status']='limited: one independently valid logarithm-difference entry remains unresolved'
 report['valid_equivalent_native_unresolved']=1
 report['canonical_mathematical_tasks']=len({r['record']['generation']['task_fingerprint'] for r in native})
 report['endpoint_contributions_checked_separately']=True
 report['generator_sha256']=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
 report['validation_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 report['readback_sha256']=hashlib.sha256((D/'readback.py').read_bytes()).hexdigest()
 save('validation.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ('native','default_family_coverage','limitations')},indent=2))
if __name__=='__main__':main()
