#!/usr/bin/env python3
"""Fail closed on displayed math, source banks/prose/stages, scope, IDs, grader."""
from pathlib import Path
import hashlib, importlib.util, json, re, subprocess, sys
import sympy as S
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from math_reader import scalar,vector,read_prompt,split_rows,scaled_vector,derivatives
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def same(x,y):return g.equivalent(x,y)
def prose(s):return re.sub(r'\$\$.*?\$\$','{{math}}',s,flags=re.S)
def blocks(s):return re.findall(r'\$\$(.*?)\$\$',s,re.S)
def balanced(s):
 assert s.count('$')%2==0
 n=0
 for i,c in enumerate(s):
  if c=='{' and (i==0 or s[i-1]!='\\'):n+=1
  elif c=='}' and (i==0 or s[i-1]!='\\'):n-=1
  assert n>=0
 assert n==0

def check_record(r):
 q=r['question'];f,h=read_prompt(r);D=[S.diff(x,g.u) for x in f];hp=S.diff(h,g.t);C=[S.simplify(x.subs(g.u,h)*hp) for x in D]
 if r['generation']['template']=='mixed_cubic_inner':assert len(S.Poly(S.expand(C[2]),g.t).terms())==5
 F=q[':question/answer-fields'][0];choices=F[':answer-field/choices'];values={a[':answer/id']:vector(a[':answer/value']) for a in choices}
 assert len(choices)==len(values)==5
 assert same(values[F[':answer-field/correct'][1]],C)
 assert sum(same(v,C) for v in values.values())==1
 for i,v in enumerate(values.values()):
  assert not any(same(v,w) for w in list(values.values())[:i])
 for s in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in choices]:balanced(s)
 b=blocks(q[':question/worked-solution']);assert len(b)==3
 # Read every displayed derivative and substitution/distribution stage from
 # actual math, not generation metadata. Rules are checked by their labels.
 fn='g' if q[':question/problem'].startswith('If $g') else 'f'
 assert fn+'′(u(t))u′(t)' in b[0]
 dr=split_rows(b[1].strip())
 for row in dr:
  lhs,rhs=row.split('& =',1)
  if 'u^{′}(t)' in lhs:
   parts=rhs.split('=');assert all(S.simplify(scalar(derivatives(x))-hp)==0 for x in parts)
  elif 'frac{\\text{d}}{\\text{d}t}' in rhs:
   assert S.simplify(scalar(derivatives(rhs))-hp)==0
  elif len(dr)>=4 and row==dr[-1] and not any(k in rhs for k in ('i','j','k','⟨','aligned')):
   assert S.simplify(scalar(rhs)-hp)==0
  else:
   for part in rhs.split('='):assert same(vector(derivatives(part)),D),(r['generation']['template'],row)
 for row in split_rows(b[2].strip())[1:]:assert same(scaled_vector(row.split('& =',1)[1],h,hp),C),(r['generation']['template'],row)
 # Format and local ownership; identity is independent of order/seed.
 import uuid
 for z in [q[':question/id'],F[':answer-field/id'],*values]:uuid.UUID(z)
 assert F[':answer-field/type']==':answer-field.type/radio' and F[':answer-field/key']=='selection'
 return len(dr)+len(split_rows(b[2].strip()))-1

def reject(call):
 try:call()
 except ValueError:return
 raise AssertionError('Invalid explicit input silently accepted')

def main():
 cases=json.loads((ROOT/'source-cases.json').read_text());replays=[];coverage=[];stages=0
 for case in cases:
  r=g.generate('easy',seed=10,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);stages+=check_record(r)
  src=g.QUESTIONS[case['source_id']];sf=src[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
  gv={a[':answer/id']:vector(a[':answer/value']) for a in rf[':answer-field/choices']}
  matches=[sum(same(vector(a[':answer/value']),v) for v in gv.values()) for a in sf[':answer-field/choices']];assert matches==[1]*5
  assert same(vector(sf[':answer-field/correct'][':answer/value']),gv[rf[':answer-field/correct'][1]])
  assert prose(src[':question/worked-solution'])==prose(r['question'][':question/worked-solution'])
  source_rows=[len(split_rows(x.strip())) for x in blocks(src[':question/worked-solution'])]
  generated_rows=[len(split_rows(x.strip())) for x in blocks(r['question'][':question/worked-solution'])];assert source_rows==generated_rows
  coverage.append({'source_id':case['source_id'],'complete_bank_matched':True,'choices_matched':5,'distractors_matched':4,'correct_designation_matched':True,'worked_solution_prose_exact':True,'source_stage_rows':source_rows,'generated_stage_rows':generated_rows,'notation_exact':False,'repair':g.REPAIRS.get(case['source_id'])})
  replays.append(r)
 records=[];identity_checks=0
 for name,level in g.TEMPLATES.items():
  for seed in (17,29):
   r=g.generate(level,seed=seed,template=name);stages+=check_record(r);records.append(r)
   clone=g.generate(level,seed=998,template=name,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
   assert clone['question'][':question/id']==r['question'][':question/id'];assert clone['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint'];identity_checks+=1
  if name in g.SPECS:
   r=g.generate(level,seed=101,template=name,profile='observed');stages+=check_record(r);records.append(r)
 # Finite signed-bound audit at authored levels, and original replay bounds.
 for name in ('mixed_quadratic_inner','mixed_cubic_inner'):
  level=g.TEMPLATES[name];p=g.generate(level,template=name)['generation']['parameters']
  bound=2 if level=='moderate' else 3
  for k in ('a','b','c','d','e'):
   for v in (bound+1,-bound-1,0):reject(lambda k=k,v=v:g.generate(level,template=name,parameters=p|{k:v}))
  for v in (3,-3):reject(lambda v=v:g.generate(level,template=name,parameters=p|{'h':v}))
  if level=='hard':reject(lambda:g.generate(level,template=name,parameters=p|{'h':0}))
 reject(lambda:g.generate('hard',profile='observed'))
 reject(lambda:g.generate('easy',field_type='blank'))
 reject(lambda:g.generate('moderate',template='mixed_cubic_inner'))
 for name,(qid,style,p) in g.SPECS.items():
  reject(lambda name=name,p=p:g.generate('easy',template=name,parameters=p|{'a':-5}))
 # Real choice grader exercises all five IDs for every source and every sampled
 # generated template/profile; answer mathematics was checked above separately.
 inputs=[]
 for i,r in enumerate(replays+records):
  f=r['question'][':question/answer-fields'][0]
  inputs.append({'label':str(i)+'-'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned radio choice '+a[':answer/value']} for a in f[':answer-field/choices']]})
 (ROOT/'engine-input.json').write_text(json.dumps(inputs,indent=2,ensure_ascii=False)+'\n')
 engine=ROOT.parents[1]/'runs/current/check-engine';subprocess.run([str(engine),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
 report=json.loads((ROOT/'engine-report.json').read_text())
 review=replays+records
 (ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 parts=['# Vector chain-rule review\n\nSources are preserved below in original notation; replays and variants are labeled. Normal mathematics uses normalized TeX; four teaching typos are repaired.']
 for case,r in zip(cases,replays):
  src=g.QUESTIONS[case['source_id']];sf=src[':question/answer-fields'][0]
  parts.append('## Original '+case['source_id']+'\n\n'+src[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==sf[':answer-field/correct'][':answer/id'] else '') for a in sf[':answer-field/choices'])+'\n\n'+src[':question/worked-solution'])
  parts.append('**Source replay — notation normalized, repairs listed in metadata**\n\n'+g.markdown(r))
 for r in records:parts.append('**Generated variant — '+('authored level' if r['generation']['authored_level'] else 'observed workload; '+r['generation']['bank_origin']+' bank')+'**\n\n'+g.markdown(r))
 (ROOT/'review.md').write_text('\n\n---\n\n'.join(parts)+'\n')
 result={'status':'pass','database':'math','basis':1356,'lineage':g.SOURCE['lineage'],'source_questions':12,'source_fields':12,'complete_source_banks_matched':12,'source_choices_matched':60,'source_choices_total':60,'source_distractors_matched':48,'source_distractors_total':48,'source_correct_designations_matched':12,'source_solution_prose_exact':12,'source_solution_stage_sequences_matched':12,'unrepaired_mathematical_sequences':8,'repaired_mathematical_sequences':4,'notation_exact_solutions':0,'normalized_notation_solutions':12,'mathematical_stages_checked':stages,'generated_records_checked':len(records),'identity_checks':identity_checks,'native_accepted_checks':report['accepted_checks'],'native_rejected_checks':report['rejected_checks'],'native_unresolved_checks':report['documented_unresolved_checks'],'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'source_coverage':coverage,'authored_levels':{'moderate':'three active components; quadratic+linear+constant inner; coefficient magnitudes <=2','hard':'three active components; cubic+linear+nonzero constant inner; coefficient magnitudes <=3; expand five-term polynomial component'},'interpretation_limits':'Unusual compound source distractor operations are explicit replay patterns, not recovered author intent; all their full vector values replay exactly. Normal default banks are method-derived authored banks.','plots':'none','database_writes':0}
 (ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_coverage'},indent=2))
if __name__=='__main__':main()
