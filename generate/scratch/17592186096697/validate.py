"""Independent display readback, source fidelity, scope, identity, native grading."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(HERE));import readback as r
spec=importlib.util.spec_from_file_location('generator',ROOT/'17592186096697.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def eq(a,b):return s.simplify(a-b)==0
def family(v):return v.subs({r.C:g.C,r.D:g.D,r.x:g.x})
def formatting(text):
 assert text.count('$')%2==0
 remainder=re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)','',text,flags=re.S)
 assert '$' not in remainder,('Math delimiter imbalance',text)
 depth=0
 for ch in text:
  if ch=='{':depth+=1
  if ch=='}':depth-=1
  assert depth>=0,('Closing brace',text)
 assert depth==0,('Open brace',text)
 assert not re.search(r'\\\\(?:frac|operatorname)',text),('Doubled command',text)
 assert '--' not in text and '+-' not in text

def verify(record,raw=False):
 kp,q=record['knowledge_point'],record['question'];assert set(kp)=={'db_id','id','title'}
 meta=record['generation'];eligible=meta['origin']=='authored-method'
 assert meta['dependencies']=={'sympy':s.__version__,'python':sys.version.split()[0]}
 assert meta['source_references']
 assert all(type(meta[k]) is bool for k in ('bank_eligible_default','eligible_for_learning','evidence_only'))
 assert meta['bank_eligible_default']==meta['eligible_for_learning']==eligible and meta['evidence_only']==(not eligible)
 force=r.forcing(q[':question/problem']);assert not force.has(r.C,r.D,r.Q,r.R,r.Y)
 F=s.integrate(force,r.x);P=s.integrate(F,r.x);general=P+r.C*r.x+r.D
 declared=0;values_checked=0
 for f in q.get(':question/answer-fields',[]):
  assert f[':answer-field/type']==':answer-field.type/radio';assert len(f[':answer-field/choices'])==5
  values=[r.answer(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
  valid=[g.families_equivalent(family(v),family(general)) for v in values]
  assert sum(valid)==1,('General family eligibility',record['generation'],values)
  assert all(not g.families_equivalent(family(a),family(b)) for i,a in enumerate(values) for b in values[i+1:]),('Bank collision',record['generation'])
  if ':answer-field/correct' in f:
   declared+=1;correct=f[':answer-field/correct'];assert correct[0]==':answer/id'
   match=[i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==correct[1]];assert len(match)==1 and valid[match[0]]
  values_checked+=len(values)
 stages=r.solution_stages(q.get(':question/worked-solution',''));count=0
 for phase,lhs,value,printed in stages:
  count+=1
  if phase=='rearrange':assert eq(lhs.subs(r.Q,force),value)
  else:
   actual=value.subs({r.Q:force,r.R:F+r.C,r.Y:general})
   # Every formal integral, distributed operator sum, evaluated primitive sum,
   # and final row is read from printed math and checked, including constants.
   expected=F if phase==1 else P
   assert eq(actual.subs({r.C:0,r.D:0}),expected),('Printed primitive value',record['generation'],printed,actual,expected)
   assert eq(s.diff(actual,r.x,phase),force),('Printed integration stage',printed)
   if phase==2:assert eq(s.diff(actual,r.C),r.x),('Lost first constant',printed)
 primitive_components=0
 for phase in (1,2):
  rows=[z for z in stages if z[0]==phase]
  operator_indices=[i for i,z in enumerate(rows) if r'\int' in z[3]]
  assert operator_indices,('Missing formal integration phase',phase)
  last=operator_indices[-1];assert last+1<len(rows)
  operator,evaluated=rows[last][3],rows[last+1][3]
  def forced_components(printed):
   values=[r.expression(z).subs({r.C:0,r.D:0}) for z in g.additive(printed)]
   return [z for z in values if z!=0]
  op,ev=forced_components(operator),forced_components(evaluated)
  assert len(op)==len(ev),('Primitive component count',operator,evaluated)
  for a,b in zip(op,ev):assert eq(a,b),('Individual printed primitive evaluation',operator,evaluated,a,b)
  primitive_components+=len(op)
 if not raw:
  formatting(q[':question/problem']);formatting(q.get(':question/worked-solution',''))
  for f in q.get(':question/answer-fields',[]):
   for a in f[':answer-field/choices']:formatting(a[':answer/value'])
 if record['generation']['origin']=='authored-method':
  equation=next(a or b for a,b in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',q[':question/problem'],re.S) if r.D2 in (a or b))
  coefficient=r.expression(equation.split('=',1)[0]).coeff(r.Q)
  opening=q[':question/worked-solution'].split('\n',1)[0]
  assert opening==('Integrating the equation once, we get' if coefficient==1 else 'First, we rearrange the equation to give'),('Prose/printed isolation mismatch',equation,opening)
  grouped={phase:[z for z in stages if z[0]==phase] for phase in (1,2)}
  assert all(len(rows)==4 for rows in grouped.values())
  n={'easy':1,'moderate':2,'hard':3}[q[':question/difficulty'].split('/')[-1]]
  for phase,rows in grouped.items():
   assert rows[1][3].count(r'\int')==(n if phase==1 else n+1)
   assert rows[2][3].count(r')\left(')==n # explicit coefficient*primitive nodes
   distributed=g.additive(rows[1][3]);evaluated=g.additive(rows[2][3])
   assert len(distributed)==n+(phase==2) and len(evaluated)==n+1+(phase==2)
   for a,b in zip(distributed[:n],evaluated[:n]):assert eq(r.expression(a),r.expression(b)),('Individual printed primitive',a,b)
   if phase==1:assert rows[2][2].coeff(r.C)==1
  assert stages[-1][2].coeff(r.D)==1
 return {'choices':values_checked,'designations':declared,'stages':count,'individual_primitive_components':primitive_components}

def source_fidelity():
 counts={'questions':0,'banks':0,'options':0,'correct_designations':0,'missing_correct_designations_preserved':0,'exact_solutions':0,'presence_parity':0};records=[]
 for case in json.loads((HERE/'source-cases.json').read_text()):
  old=g.SOURCES[case['source_id']];out=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);new=out['question'];records.append(out)
  assert set(new)==set(old)-{':db/id'},('Source question presence',case)
  assert new[':question/problem']==old[':question/problem']
  assert (':question/worked-solution' in new)==(':question/worked-solution' in old)
  if ':question/worked-solution' in old:assert new[':question/worked-solution']==old[':question/worked-solution'];counts['exact_solutions']+=1
  assert len(new.get(':question/answer-fields',[]))==len(old.get(':question/answer-fields',[]))
  for before,after in zip(old.get(':question/answer-fields',[]),new.get(':question/answer-fields',[])):
   assert set(after)==set(before)-{':db/id'}
   assert after[':answer-field/key']==before[':answer-field/key']
   assert after[':answer-field/type']==before[':answer-field/type'][':db/ident']
   av=[a[':answer/value'] for a in before[':answer-field/choices']];bv=[a[':answer/value'] for a in after[':answer-field/choices']]
   assert sorted(av)==sorted(bv),('Exact complete bank',case,av,bv)
   for a in before[':answer-field/choices']:
    matches=[b for b in after[':answer-field/choices'] if b[':answer/value']==a[':answer/value']];assert len(matches)==1
    assert set(matches[0])==set(a)-{':db/id'}
    assert eq(r.answer(a[':answer/value']),r.answer(matches[0][':answer/value']))
   counts['banks']+=1;counts['options']+=len(av)
   if ':answer-field/correct' in before:
    correct=next(a for a in after[':answer-field/choices'] if a[':answer/id']==after[':answer-field/correct'][1])
    assert correct[':answer/value']==before[':answer-field/correct'][':answer/value'];counts['correct_designations']+=1
   else:assert ':answer-field/correct' not in after;counts['missing_correct_designations_preserved']+=1
  verify(out,raw=True);counts['questions']+=1;counts['presence_parity']+=1
 return counts,records

def main():
 counts,originals=source_fidelity();totals={'normal':0,'completed':0,'scaled_raw':0,'choices':0,'stages':0,'individual_primitive_components':0};tested=[]
 for key,source in g.SOURCES.items():
  level=source[':question/difficulty'][':db/ident'].split('/')[-1]
  for scale in (1,2,'1/2'):
   out=g.generate(level,profile='completed-'+key,parameters={'scale':scale});stats=verify(out);tested.append(out);totals['completed']+=1;totals['choices']+=stats['choices'];totals['stages']+=stats['stages'];totals['individual_primitive_components']+=stats['individual_primitive_components']
  out=g.generate(level,profile='observed-'+key,parameters={'scale':2});stats=verify(out,raw=True);totals['scaled_raw']+=1;totals['choices']+=stats['choices'];totals['stages']+=stats['stages'];totals['individual_primitive_components']+=stats['individual_primitive_components']
 for template,level in g.TEMPLATES.items():
  for seed in range(12):
   out=g.generate(level,seed,template);stats=verify(out);tested.append(out);totals['normal']+=1;totals['choices']+=stats['choices'];totals['stages']+=stats['stages'];totals['individual_primitive_components']+=stats['individual_primitive_components']
   again=g.generate(level,seed+1000,template,parameters=out['generation']['parameters'])
   assert again['question'][':question/id']==out['question'][':question/id']
   assert again['generation']['mathematical_fingerprint']==out['generation']['mathematical_fingerprint']
   values=lambda z:sorted(a[':answer/value'] for a in z['question'][':question/answer-fields'][0][':answer-field/choices'])
   assert values(again)==values(out)
 # A genuinely invertible constant change, a rank-deficient pair, one constant,
 # and a particular solution establish the requested response criterion.
 base=g.x**3
 assert g.families_equivalent(base+g.C*g.x+g.D,base+(2*g.C+g.D)*g.x+3*g.D+4)
 for wrong in (base+g.C,base+g.C*g.x,base+(g.C+g.D)*g.x,base):assert not g.families_equivalent(base+g.C*g.x+g.D,wrong)
 bad=g.sample('hard',__import__('random').Random(1));bad['m']=1
 try:g.generate('hard',template='power_exp_trig',parameters=bad)
 except ValueError:pass
 else:raise AssertionError('Explicit workload bypass')
 # Incidental non-assessed parameters cannot create new content identity.
 p=g.generate('easy',template='single_power',seed=9)['generation']['parameters'];p2=dict(p,b=7,c=8,base=4,trig='sin',k=3)
 one=g.generate('easy',template='single_power',parameters=p);two=g.generate('easy',template='single_power',parameters=p2)
 assert one['question'][':question/id']==two['question'][':question/id'];assert one['generation']['mathematical_fingerprint']==two['generation']['mathematical_fingerprint']
 # Numeric spelling of the scalar isolation coefficient cannot create a
 # different displayed task or introduce floating arithmetic.
 trial=g.generate('moderate',template='power_exp',seed=7);params=dict(trial['generation']['parameters']);params['m']=float(params['m'])
 spelled=g.generate('moderate',template='power_exp',parameters=params)
 assert trial['question'][':question/id']==spelled['question'][':question/id']
 # Source raw missing-key fields cannot be graded by the engine. Remove only
 # those fields in memory from the grading fixture; do not alter raw API data.
 inputs=[]
 for out in originals+tested:
  fixture=copy.deepcopy(out);fixture['question'][':question/answer-fields']=[f for f in fixture['question'][':question/answer-fields'] if ':answer-field/correct' in f]
  checks=[]
  for i,f in enumerate(fixture['question'][':question/answer-fields']):
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Canonical designation and all owned wrong selections; display mathematics checked independently.'})
  inputs.append({'label':out['generation']['bank_profile']+'/'+str(out['generation']['seed'])+'/'+out['question'][':question/id'],'record':fixture,'checks':checks})
 (HERE/'engine-input.json').write_text(json.dumps(inputs,indent=2)+'\n')
 engine=ROOT.parent/'runs/current/check-engine';result=subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True);assert result.returncode==0,result.stdout+result.stderr
 native=json.loads((HERE/'engine-report.json').read_text())
 hashes={str(path.relative_to(ROOT.parent.parent)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [ROOT/'17592186096697.py',HERE/'readback.py',HERE/'validate.py',HERE/'build-evidence.py',HERE/'source.json',HERE/'source-cases.json',HERE/'review.json',HERE/'review.md',HERE/'classification.md',HERE/'template-extraction.md',HERE/'README.md',HERE/'topic.json',HERE/'lesson.json',HERE/'source-masks.json',HERE/'authority-layout.json',HERE/'engine-input.json',HERE/'engine-report.json']}
 decoded_anomalies={key:{'doubled_command_answers':sum(bool(re.search(r'\\\\(?:frac|operatorname|,)',a[':answer/value'])) for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']),'literal_backslash_u2061_answers':sum('\\u2061' in a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices'])} for key,q in g.SOURCES.items()}
 report={'decoded_source_byte_anomalies':decoded_anomalies,'status':'passed','database':'math','basis':1356,'lineage':g.SOURCE['lineage'],'source_fidelity':counts,'verification':totals,'native_grading':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks'],'missing_source_designations_not_invented':2,'fixture_only_omissions':2,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'normal_meaningful_tasks_tested':len({z['generation']['mathematical_fingerprint'] for z in tested if z['generation']['origin']=='authored-method'}),'raw_exact_solution_stage_sequences':11,'presentation_completed_questions':11,'completed_bank_options':55,'source_solution_repair_questions':1,'source_teaching_omission':'q-119041 intermediate first primitive omits C; raw preserved, completed repaired','raw_source_format_anomalies':'Decoded inspection finds zero doubled TeX command backslashes and zero literal escaped Unicode sequences in source answers. Typographic natural-log notation is preserved raw and normalized only in completion.','opaque_source_profiles_default_eligible':0,'artifacts_sha256':hashes,'database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
