#!/usr/bin/env python3
"""Private readback: printed operands/orders/stages/banks; real native grade_field."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
z=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
z=importlib.util.spec_from_file_location('independent_scalar',ROOT/'scalar_parser.py');p=importlib.util.module_from_spec(z);z.loader.exec_module(p)
x=s.Symbol('x',positive=True)
DER=r'\frac{\text{d}}{\text{d}x}'
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
BLOCK=re.compile(r'\$\$\n(.*?)\n\$\$',re.S)
def parse(t):
 while '\\\\' in t:t=t.replace('\\\\','\\')
 return p.scalar(t).subs(p.x,x)
def equal(a,b):
 delta=s.expand(a-b)
 return delta==0
def formatting(text):
 assert not any(ord(c)<32 and c not in '\n\t' for c in text)
 assert text.count('$')%2==0
 # Delimiters must consume the full string in their usual nesting.
 stripped=MATH.sub('',text);assert '$' not in stripped
 for chunk in MATH.findall(text):
  depth=0
  for c in chunk:
   depth+=(c=='{')-(c=='}');assert depth>=0
  assert depth==0
 assert '--' not in text and '+-' not in text

def target_order(text):
 math=MATH.findall(text)
 # A power x^3 in the supplied operand is not a derivative request. Every
 # repeated request (including a blank's supplied LHS) must agree.
 candidates=[t for t in math if any(c in t for c in ['‴','″','′']) or re.search(r'\{[a-z]\}\^\{\([234]\)\}',t) or (r'\frac' in t and ('d^{' in t or r'\text{d}' in t))]
 assert candidates,('no derivative target',text)
 orders=[]
 for target in candidates:
  if r'\frac' in target:
   values=[int(v) for v in re.findall(r'\^\{([1-4])\}',target)]
   assert values and len(set(values))==1,('inconsistent numerator/denominator derivative order',target)
   orders.append(values[0])
  elif '(4)' in target:orders.append(4)
  elif '‴' in target or '(3)' in target:orders.append(3)
  elif '″' in target or '(2)' in target:orders.append(2)
  elif '′' in target:orders.append(1)
  else:raise AssertionError('unreadable target order')
 assert len(set(orders))==1,('inconsistent repeated target orders',orders)
 return orders[0]
def label_order(label):
 if '(4)' in label:return 4
 if '‴' in label:return 3
 if '″' in label or "''" in label:return 2
 if '′' in label or "'" in label:return 1
 if r'\frac' in label:
  if '^{3}' in label:return 3
  if '^{2}' in label:return 2
  return 1
 return 0

def readback(record):
 assert not record['generation']['evidence_only'] and record['generation']['eligible_for_learning']
 q=record['question'];problem=q[':question/problem'];solution=q[':question/worked-solution'];field=q[':question/answer-fields'][0]
 for text in [problem,solution,*[a[':answer/value'] for a in field[':answer-field/choices']]]:formatting(text)
 definition=next(m[1:-1] for m in MATH.findall(problem) if re.search(r'(?:[fgh]\(x\)|y)\s*=',m))
 lhs,rhs=definition.split('=',1);function=parse(rhs.rstrip(',.'));order=target_order(problem)
 name=lhs.strip()[0]
 # Named prompt target and every displayed derivative label must reference the
 # supplied function. Function definitions and final prose are checked too.
 for label in re.findall(r'\{([a-z])\}\^\{(?:′|″|‴|\(4\))',problem+solution):assert label==name
 if name=='y':assert 'h(x)' not in solution
 values={a[':answer/id']:parse(a[':answer/value']) for a in field[':answer-field/choices']}
 wanted=s.diff(function,x,order);assert equal(values[field[':answer-field/correct'][1]],wanted)
 pairs=list(values.values());assert not any(equal(a,b) for i,a in enumerate(pairs) for b in pairs[i+1:])
 n=0;row_count=0;formal=0
 for block in BLOCK.findall(solution):
  rows=block.split(' & =');label=rows[0].replace(r'\begin{aligned}','').strip();printed_order=label_order(label)
  if DER in block:n+=1;assert printed_order==n
  else:assert n==0 and printed_order==0
  expected=s.diff(function,x,n)
  for part in rows[1:]:
   rhs=part.split(r'\\')[0].split(r'\end{aligned}')[0].strip().rstrip('.')
   if rhs.startswith(DER):
    arg=rhs[len(DER):].strip();assert arg.startswith('(') and arg.endswith(')')
    operand=parse(arg[1:-1]);assert equal(operand,s.diff(function,x,n-1)),('formal operator input',rhs);value=s.diff(operand,x);formal+=1
   else:value=parse(rhs)
   assert equal(value,expected),('incorrect displayed stage',rhs,n,expected,value)
   row_count+=1
 assert n==order and formal>=order
 ordinals={'first':1,'second':2,'third':3,'fourth':4}
 prose=[ordinals[v.lower()] for v in re.findall(r'computing the (first|second|third|fourth) derivative',solution,re.I)]
 assert prose==list(range(1,order+1))
 domain='x>0' if function.has(s.log) or any(power.base==x and power.exp.is_Rational and power.exp.q!=1 for power in function.atoms(s.Pow)) else 'x!=0' if s.denom(s.together(function)).has(x) else 'real x'
 assert record['generation']['domain']==domain,(domain,record['generation']['domain'])
 # Source family stage profile is an independently recorded extraction artifact.
 expected_profile=PROFILES[record['generation']['template']]
 assert [len(b.split(' & ='))-1 for b in BLOCK.findall(solution)]==expected_profile
 assert field[':answer-field/type'] in [':answer-field.type/radio',':answer-field.type/blank']
 if field[':answer-field/type'].endswith('/blank'):assert '{{'+field[':answer-field/key']+'}}' in problem
 assert field[':answer-field/correct'][1] in values
 uuid.UUID(q[':question/id']);uuid.UUID(field[':answer-field/id'])
 for a in field[':answer-field/choices']:uuid.UUID(a[':answer/id']);assert '$' not in a[':answer/value']
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 return wanted,row_count

PROFILES={'polynomial_reciprocal_radio':[2,2,2,3],'cubic_reciprocal_radio':[2,2,2],'quadratic_constant_reciprocal':[2,3,3,3],'polynomial_reciprocal_blank':[2,2,2,3],'log_radical':[3,3,3],'cos_log':[2,3,2,3],'polynomial':[2,2,2],'quotient_sum':[2,3,2,3],'exponential_reciprocal':[3,2,3],'log_polynomial':[3,2,3],'sin_exponential':[2,2,2,2]}

def fails(action):
 try:action()
 except (AssertionError,ValueError,TypeError,KeyError,StopIteration):return
 raise AssertionError('negative control was accepted')

def main():
 for name,meta in json.loads((ROOT/'private-dependencies.json').read_text()).items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==meta['sha256']
 engine=REPO/'generate/runs/current/check-engine';engine_sha=hashlib.sha256(engine.read_bytes()).hexdigest();assert engine_sha=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 cases=json.loads((ROOT/'source-cases.json').read_text());assert len(cases)==11
 sources=g.SOURCES;assert {c['source_id'] for c in cases}==set(sources)
 original_rows=[];native=[];review=[];allrecords=[];counters={'raw_exact_records':0,'banks':0,'values':0,'distractors':0,'correct_designations':0,'solution_exact':0,'solution_normalized':0,'absent_solutions':0,'absent_fields':0,'absent_correct_designations':0}
 if '--resume-validated-bounds' in sys.argv:
  saved=json.loads((ROOT/'bounded-summary.json').read_text());allrecords=json.loads((ROOT/'bounded-records.json').read_text())
  counters=saved['counters'];original_rows=saved['original_rows'];review=saved['review'];sample_counts=saved['sample_counts'];tasks={k:set(range(v)) for k,v in saved['tasks'].items()};slots={k:[set(v) for v in vals] for k,vals in saved['slots'].items()};rejected_banks=saved['rejected_banks']
  for case in cases:assert g.generate(case['difficulty'],parameters={'source_id':case['source_id']},profile='raw-evidence')['question']==sources[case['source_id']]
  for r in allrecords:
   readback(r);g.F.validate_generated_record(r)
  print(f'Re-read all {len(allrecords)} previously enumerated bounded records with latest private validator and formatter.',flush=True)
 else:
  for case in cases:
   sid=case['source_id'];src=sources[sid];level=case['difficulty']
   raw=g.generate(level,parameters={'source_id':sid},profile='raw-evidence');assert raw['question']==src;assert raw['generation']['evidence_only'];counters['raw_exact_records']+=1
   r=g.generate(level,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);expected,rows=readback(r);allrecords.append(r)
   field=r['question'][':question/answer-fields'][0]
   if ':question/answer-fields' not in src:counters['absent_fields']+=1
   else:
    for sf in src[':question/answer-fields']:
     old=[parse(a[':answer/value']) for a in sf[':answer-field/choices']];new=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
     assert len(old)==len(new)
     assert all(sum(equal(a,b) for b in new)==1 for a in old);counters['banks']+=1;counters['values']+=len(old)
     if ':answer-field/correct' in sf:
      assert equal(parse(sf[':answer-field/correct'][':answer/value']),expected);counters['correct_designations']+=1;counters['distractors']+=len(old)-1
     else:counters['absent_correct_designations']+=1;counters['distractors']+=len(old)-1
   if ':question/worked-solution' not in src:counters['absent_solutions']+=1
   else:
    old=src[':question/worked-solution'];new=r['question'][':question/worked-solution'];counters['solution_exact']+=old==new
    normalized=re.sub(r'(?<![A-Za-z\\])(sin|cos|ln)(?=x)',lambda m:'\\'+m[1]+' ',old.replace('⁡',''));normalized=normalized.replace('h(x)','y') if sid=='q-28551' else normalized
    assert normalized==new,(sid,'whole worked-solution mask fidelity');counters['solution_normalized']+=1
   original_rows.append({'source_id':sid,'complete_raw_exact':True,'served_stage_rows':rows,'served_repairs':r['generation']['source_repairs']})
   review.append({'role':'served original parameters','record':r})
  # Exercise all complete profiles, all coefficient boundaries, default family
  # coverage and same-operand changed coefficient cases. No math/grader failures
  # may be filtered out. Equivalent-bank guards are tested explicitly.
  sample_counts={};observed_defaults=set();tasks={k:set() for k in g.SPECS};slots={k:[set() for _ in v[3]] for k,v in g.SPECS.items()};rejected_banks=0
  domain=[i for i in range(-6,7) if i]
  for family,(sid,level,order,parts) in g.SPECS.items():
   count=0
   # Enumerate all substantive scales, hold killed components at1; this counts
   # math tasks rather than cosmetic coefficients. Every slot still gets its
   # separate signed boundary/coverage sweep below.
   active=[i for i,t in enumerate(parts) if s.diff(t,g.x,order)!=0]
   vectors=[]
   for vals in itertools.product(domain,repeat=len(active)):
    sc=[1]*len(parts)
    for i,v in zip(active,vals):sc[i]=v
    vectors.append(sc)
   vectors.extend([[v]*len(parts) for v in domain])
   for index,sc in enumerate(vectors):
    for profile in g.PROFILES.get(family,['blank']):
     try:r=g.generate(level,index,template=family,profile=profile,parameters={'scales':sc})
     except ValueError as exc:
      assert str(exc)=='whole bank has equivalent options';rejected_banks+=1;continue
     readback(r);count+=1;tasks[family].add(r['generation']['mathematical_fingerprint'])
     for values,k in zip(slots[family],sc):values.add(k)
     allrecords.append(r)
    if index in [0,1]:review.append({'role':'generated signed coefficient variant','record':r})
   sample_counts[family]=count;print(f'Validated {family}: {count} complete instances',flush=True)
  for level in ['easy','moderate','hard']:
   for seed in range(100):
    r=g.generate(level,seed);readback(r);observed_defaults.add(r['generation']['template']);allrecords.append(r)
  assert observed_defaults==set(g.SPECS)
  for family,domainsets in slots.items():assert all(v==set(domain) for v in domainsets)
 (ROOT/'bounded-records.json').write_text(json.dumps(allrecords))
 (ROOT/'bounded-summary.json').write_text(json.dumps({'counters':counters,'original_rows':original_rows,'review':review,'sample_counts':sample_counts,'tasks':{k:len(v) for k,v in tasks.items()},'slots':{k:[sorted(x) for x in v] for k,v in slots.items()},'rejected_banks':rejected_banks}))
 # Seeds cannot manufacture identities at a fixed parameter/bank.
 for family,(sid,level,n,parts) in g.SPECS.items():
  kw={'template':family,'parameters':{'scales':[1]*len(parts)},'profile':g.PROFILES.get(family,['blank'])[0]}
  a=g.generate(level,1,**kw);b=g.generate(level,99,**kw);assert a['question'][':question/id']==b['question'][':question/id'];assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
  mutation=copy.deepcopy(a);mutation['question'][':question/problem']=mutation['question'][':question/problem'].replace('‴','″').replace('(4)','(3)').replace('d^{3}','d^{2}').replace(r'\text{d}}^{3}',r'\text{d}}^{2}');fails(lambda:readback(mutation))
  mutation=copy.deepcopy(a);sol=mutation['question'][':question/worked-solution'];position=sol.index(DER+'(')+len(DER+'(');mutation['question'][':question/worked-solution']=sol[:position]+'2*('+sol[position:sol.index(')',position)]+')'+sol[sol.index(')',position):];fails(lambda:readback(mutation))
  mutation=copy.deepcopy(a);mutation['question'][':question/worked-solution']+='\x0c';fails(lambda:readback(mutation))
  # Wrong supplied function target is independently detected.
  if re.search(r'([fgh])\(x\)=',a['question'][':question/problem']):
   mutation=copy.deepcopy(a);name=re.search(r'([fgh])\(x\)=',mutation['question'][':question/problem']).group(1);mutation['question'][':question/problem']=mutation['question'][':question/problem'].replace('{'+name+'}^{','{z}^{');fails(lambda:readback(mutation))
 for kw in [{'level':'bad'},{'level':'easy','seed':True},{'level':'easy','template':'cos_log'},{'level':'hard','field_type':'radio'},{'level':'easy','profile':'bad'},{'level':'easy','template':'polynomial','parameters':{'scales':[0,1]}},{'level':'easy','template':'polynomial','parameters':{'scales':[7,1]}},{'level':'easy','template':'polynomial','parameters':{'scales':[True,1]}},{'level':'easy','template':'polynomial','parameters':{'scales':[1,1],'n':4}},{'level':'easy','parameters':[]},{'level':'easy','profile':'raw-evidence','parameters':{'source_id':'foreign'}}]:fails(lambda kw=kw:g.generate(**kw))
 for level in ['easy','moderate','hard']:
  cap=g.capacity(level);fails(lambda level=level,cap=cap:g.generate_many(level,cap+1));assert cap>0
  batch=g.generate_many(level,2);assert len({r['generation']['mathematical_fingerprint'] for r in batch})==2
 for fmt in ['json','markdown']:
  result=subprocess.run([sys.executable,str(ROOT.with_suffix('.py')),'--difficulty','all','--count','2','--format',fmt],text=True,capture_output=True,check=True)
  if fmt=='json':assert len(json.loads(result.stdout))==6;assert [r['question'][':question/difficulty'].split('/')[-1] for r in json.loads(result.stdout)]==['easy','easy','moderate','moderate','hard','hard']
  else:assert sum(result.stdout.count(r['question'][':question/problem']) for r in [])==0;assert result.stdout.count('Finally, computing')==6
 # Native grade every successful bounded generated record and every displayed
 # choice; canonical, independently unreduced equivalent, ordinary0/1/+1.
 for i,r in enumerate(allrecords):
  field=r['question'][':question/answer-fields'][0];checks=[]
  if field[':answer-field/type'].endswith('/radio'):
   for a in field[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'owned full-bank selection'})
  else:
   correct=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
   equivalent=r'\frac{2('+correct+r')}{2}'
   checks=[{'submitted':correct,'expected':'accepted','purpose':'canonical rendered answer'},{'submitted':equivalent,'expected':'accepted','purpose':'independent unreduced whole expression'},{'submitted':'0','expected':'rejected','purpose':'ordinary wrong zero'},{'submitted':'1','expected':'rejected','purpose':'ordinary wrong one'},{'submitted':'('+correct+')+1','expected':'rejected','purpose':'ordinary wrong plus one'}]
  native.append({'label':str(i),'record':r,'checks':checks})
 (ROOT/'native-input.json').write_text(json.dumps(native));subprocess.run([str(engine),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
 # Diagnostic malformed entries are segregated from the required checks.
 diagnostic=g.generate('easy',template='polynomial',parameters={'scales':[1,1]});(ROOT/'native-diagnostics.json').write_text(json.dumps([{'label':'malformed blank','record':diagnostic,'checks':[{'submitted':'not mathematics','expected':'unresolved','purpose':'malformed diagnostic only'}]},{'label':'foreign radio identity','record':g.generate('moderate',template='polynomial_reciprocal_radio',parameters={'scales':[1,1,1]}),'checks':[{'submitted':'999999','expected':'unresolved','purpose':'foreign identity diagnostic only'}]}]));subprocess.run([str(engine),str(ROOT/'native-diagnostics.json'),str(ROOT/'native-diagnostics-report.json')],check=True)
 counters.update({'MA_originals':11,'observed_radio_banks':3,'observed_blank_values':7,'observed_designated_distractors':8,'inferred_unkeyed_distractors':4,'missing_designation_is_not_recovered':True})
 report={'status':'working','private_validation':'passed','source_basis':2275,'source_lineage':g.SOURCE['lineage'],'source_fidelity':counters,'originals':original_rows,'validated_records':len(allrecords),'profile_counts':sample_counts,'meaningful_tasks_by_family':{k:len(v) for k,v in tasks.items()},'coefficient_slot_coverage':{k:[sorted(x) for x in v] for k,v in slots.items()},'finite_level_capacity':{level:g.capacity(level) for level in ['easy','moderate','hard']},'whole_bank_equivalence_rejections':rejected_banks,'engine_sha256':engine_sha,'native':json.loads((ROOT/'native-report.json').read_text())|{'records':'see native-report.json'},'negative_controls':'target order, formal operand, target name, control character; strict public invalid inputs','independent_inventory':0,'plots':'none','limitations':['q-28550 missing original correct designation and worked solution; authored inference does not count as an observed designation','q-28551 has no original fields; served blank is authored; its initial h(x) label repaired to supplied y','observed scalar-bank error interpretations remain limited; complete algebraic patterns are reproduced','coefficient scales are bounded nonzero integers magnitude<=6; derivative orders/input powers remain fixed']}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['status','validated_records','source_fidelity','meaningful_tasks_by_family']},indent=2))
if __name__=='__main__':main()
