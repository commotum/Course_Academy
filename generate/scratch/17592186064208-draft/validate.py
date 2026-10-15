#!/usr/bin/env python3
"""Independent reads of printed operands, every operative stage, and all choices."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('draft64208',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
p=g.parser

def check(z):
 q=z['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 rr=p.Reader(re.search(r'\\int\s*(.*?)\\,?\\text\{d\}x',prompt).group(1)) if r'\text{d}x' in prompt else None
 integrands=p.integral_operands(prompt);assert len(integrands)==1;f=integrands[0]
 # Read poles from the actual uncancelled printed denominator operands.
 body=re.search(r'\\int\s*(.*?)' + (r'\\,\\text\{d\}x' if r'\text{d}x' in prompt else 'dx'),prompt.replace(r'\displaystyle','')).group(1)
 rd=p.Reader(body);rd.read();poles=sorted(set(root for d in rd.denominators for root in s.solve(d,p.x)))
 assert list(map(str,poles))==z['generation']['domain']['excluded_poles']
 rows=sol.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\');assert len(rows)==4,('operative stage erased',rows)
 lhs,rhs=rows[0].split('&',1);rhs=rhs.strip().removeprefix('=').strip()
 assert len(p.integral_operands(lhs))==1 and s.cancel(p.integral_operands(lhs)[0]-f)==0
 operands=p.integral_operands(rhs);assert len(operands)==2
 assert s.cancel(sum(operands)-f)==0,('wrong formal integral operand',rhs)
 # Each displayed primitive must differentiate to the independently read task.
 expressions=[p.scalar(row.strip().removeprefix('&').strip().removeprefix('=').strip()) for row in rows[1:]]
 for expr in expressions:assert s.cancel(p.derivative(expr)-f)==0,('wrong primitive',expr,f)
 # Derivative equality alone cannot justify stale C-to-K coefficients.
 a=s.Poly(s.denom(operands[0]),p.x).coeff_monomial(p.x)
 mapped=expressions[0].subs(p.C,s.log(p.K)/a)
 for expr in expressions[1:]:assert s.simplify(p.log_normal(expr)-p.log_normal(mapped))==0,('stale constant',mapped,expr)
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];assert len(choices)==5
 ds=[p.derivative(p.scalar(c[':answer/value'])) for c in choices]
 key=field[':answer-field/correct'][1]
 for choice,d in zip(choices,ds):assert (s.cancel(d-f)==0)==(choice[':answer/id']==key)
 assert len({c[':answer/id'] for c in choices})==5
 for i,j in itertools.combinations(range(5),2):assert s.cancel(ds[i]-ds[j])!=0
 assert z['generation']['mathematical_fingerprint']==g.digest(str(s.cancel(f)))
 return {'formal_operands':len(operands)+1,'primitive_stages':3,'choice_values':5,'real_components':len(poles)+1,'exact_C_K_equalities':2}

def run():
 report={'source_basis':2275,'registered_files':len(json.loads((HERE/'registered-baseline.json').read_text())),'source_replay':[],'cases':[],'mutations':[]}
 sourcecases=[];rawcases=[];previews=[];native=[]
 for raw in g.SOURCE[':knowledge-point/questions']:
  sid=raw[':question/math-academy-id'];case=g.source_case(sid);assert case['raw']==raw;rawcases.append(case)
  prof=sid if sid in g.PROFILES else sid+'-completed';t=g.PROFILES[prof];params=t['parameters'];z=g.generate('hard',0,prof,params);check(z)
  f=raw[':question/answer-fields'][0];generated=z['question'][':question/answer-fields'][0]
  assert len(f[':answer-field/choices'])==len(generated[':answer-field/choices'])
  for actual,expected in zip(generated[':answer-field/choices'],f[':answer-field/choices']):assert actual[':answer/value']==g.fmt.normalize_tex(expected[':answer/value']),(sid,actual,expected)
  assert z['question'][':question/problem']==g.fmt.normalize_prose(raw[':question/problem'])
  if raw.get(':question/worked-solution'):assert z['question'][':question/worked-solution']==g.fmt.normalize_prose(raw[':question/worked-solution'])
  if f.get(':answer-field/correct'):
   expected=f[':answer-field/correct'][':answer/value'];assert next(c[':answer/value'] for c in generated[':answer-field/choices'] if c[':answer/id']==generated[':answer-field/correct'][1])==g.fmt.normalize_tex(expected)
  report['source_replay'].append({'source_id':sid,'prompt':True,'worked_solution':bool(raw.get(':question/worked-solution')),'choices_matched':5,'choices_total':5,'source_correct_key':bool(f.get(':answer-field/correct')),'raw_public_replay_eligible':case['public_replay_eligible'],'completion':sid=='q-49521'})
  for variant in range(3):
   zz=z if variant==0 else g.generate('hard',200+variant,prof)
   sourcecases.append({'source_id':sid,'difficulty':'hard','template':zz['generation']['template'],'parameters':zz['generation']['parameters'],'bank_profile':prof,'variant':variant,'record':zz})
 canonical=g.source_case('e-451');assert canonical['raw']==g.SOURCE[':knowledge-point/canonical-example'];rawcases.append(canonical)
 # Every profile receives original and two meaningful changed parameter examples.
 for difficulty in g.LEVELS:
  for sid in g.profiles(difficulty):
   seen=set()
   for seed in range(100):
    z=g.generate(difficulty,500+seed,sid);fp=z['generation']['mathematical_fingerprint']
    if fp in seen:continue
    seen.add(fp);evidence=check(z);report['cases'].append({'difficulty':difficulty,'profile':sid,'parameters':z['generation']['parameters'],**evidence});previews.append(z)
    if len(seen)==3:break
   assert len(seen)==3
 # Additional bounded coverage: each level produces 60 actual distinct tasks.
 for difficulty in g.LEVELS:
  batch=g.batch(difficulty,60,1700);assert len({r['generation']['mathematical_fingerprint'] for r in batch})==60
  for z in batch:check(z)
  report.setdefault('distinct_task_counts',{})[difficulty]=60
 # Mutations keep final answer valid when possible, isolating independent readers.
 sample=g.generate('hard',99,'q-49524',[4,2,2]);original=sample['question'][':question/worked-solution']
 mutations={
 'wrong_prompt_integrand':('prompt',sample['question'][':question/problem'].replace(r'\frac{1}{2+4x}',r'\frac{2}{2+4x}',1)),
 'wrong_formal_operand':('solution',original.replace(r'=\int \frac{1}{2+4x}',r'=\int \frac{2}{2+4x}',1)),
 'stale_C_to_K_coefficient':('solution',original.replace(r'+\frac{1}{4}\operatorname{ln}⁡K',r'+\frac{1}{3}\operatorname{ln}⁡K',1)),
 'erased_primitive_stage':('solution',original.replace(original.split(r'\\')[1]+r'\\','',1)),
 'wrong_intermediate_primitive':('solution',original.replace(r'=\frac{1}{4}\operatorname{ln}⁡|2+4x|',r'=\frac{1}{3}\operatorname{ln}⁡|2+4x|',1))}
 for name,(where,value) in mutations.items():
  z=copy.deepcopy(sample);z['question'][':question/problem' if where=='prompt' else ':question/worked-solution']=value
  assert value!=(sample['question'][':question/problem'] if where=='prompt' else original),name
  try:check(z)
  except (AssertionError,ValueError,IndexError) as exc:report['mutations'].append({'name':name,'rejected':True,'reason':str(exc)[:250]})
  else:raise AssertionError('mutation survived: '+name)
 # Equivalence probes explicitly retain arbitrary constants and scaled log arguments.
 f=p.integral_operands(sample['question'][':question/problem'])[0]
 for tex in [r'\frac{1}{4}\ln(K|\frac{2+4x}{2-4x}|)+1',r'\frac{1}{4}\ln(K|\frac{6+12x}{2-4x}|)']:
  assert s.cancel(p.derivative(p.scalar(tex))-f)==0
 report['equivalence_probes']={'additive_one':'equivalent on each component','scaled_log_argument':'equivalent on each component','used_as_distractors':False}
 # Actual learner radio grading: all owned IDs; foreign and malformed IDs separately.
 for i,z in enumerate(previews):
  field=z['question'][':question/answer-fields'][0];key=field[':answer-field/correct'][1]
  checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'owned correct ID' if a[':answer/id']==key else 'owned wrong derivative option ID'} for a in field[':answer-field/choices']]
  checks += [{'field_index':0,'submitted':v,'expected':'unresolved','purpose':purpose} for v,purpose in [('foreign-answer-id','foreign ID'),('','malformed empty ID'),('99999999','foreign numeric ID')]]
  native.append({'label':str(i),'record':z,'checks':checks})
 for name,obj in [('sourcecases.json',sourcecases),('raw-replay.json',rawcases),('previews.json',previews),('validation.json',report),('native-input.json',native)]: (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
 print(json.dumps({'replay':len(report['source_replay']),'profile_cases':len(previews),'distinct_task_counts':report['distinct_task_counts'],'mutations':len(report['mutations'])}))

# Maintain standard parent integration evidence names without mixing authored cases.
def write_parent_evidence():
    src=json.loads((HERE/'source.json').read_text());old=json.loads((HERE/'sourcecases.json').read_text());rows=old['cases'] if isinstance(old,dict) else old
    original=[c for c in rows if c.get('case_role')=='original parameters or explicit repair' or c.get('variant')==0]
    for name,value in [('source-cases.json',original),('review-cases.json',rows),('independent-inventory.json',{'basis':src['basis'],'lineage':src['lineage'],'questions':[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Existing nonMA inventory, separate from recovered original templates.'} for q in src['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]})]:
        (HERE/name).write_text(json.dumps(value,indent=2)+'\n')

if __name__=='__main__':run();write_parent_evidence()
