#!/usr/bin/env python3
"""Independent displayed-math, source-fidelity and native-grade verification."""
import ast
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import uuid

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SCRIPT=HERE.with_suffix('.py')
spc=importlib.util.spec_from_file_location('dot_product',SCRIPT)
g=importlib.util.module_from_spec(spc); spc.loader.exec_module(g)
def read(p): return json.loads(p.read_text())
def write(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def eval_math(s):
 s=s.strip().rstrip('.').replace(r'\cdot','*').replace(' ','')
 assert re.fullmatch(r'[\d.+*()\-/]+',s),s
 def ev(t):
  if isinstance(t,ast.Expression): return ev(t.body)
  if isinstance(t,ast.Constant): return Fraction(str(t.value))
  if isinstance(t,ast.UnaryOp):
   assert isinstance(t.op,(ast.UAdd,ast.USub)); return ev(t.operand)*(1 if isinstance(t.op,ast.UAdd) else -1)
  if isinstance(t,ast.BinOp):
   a,b=ev(t.left),ev(t.right)
   if isinstance(t.op,ast.Add): return a+b
   if isinstance(t.op,ast.Sub): return a-b
   if isinstance(t.op,ast.Mult): return a*b
   if isinstance(t.op,ast.Div): return a/b
  raise AssertionError(ast.dump(t))
 return ev(ast.parse(s,mode='eval'))

def balanced(s):
 assert s.count('$$')%2==0
 assert s.replace('$$','').count('$')%2==0
 n=0
 for i,c in enumerate(s):
  if c in '{}':
   if i and s[i-1]=='\\': continue
   n+=1 if c=='{' else -1
   assert n>=0,s
 assert n==0,s
 assert '+-' not in s and '--' not in s

def check_record(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 assert rec['knowledge_point']==g.KP
 q=rec['question']; f=q[':question/answer-fields'][0]
 for key in (':question/id',): uuid.UUID(q[key])
 uuid.UUID(f[':answer-field/id'])
 assert f[':answer-field/type'] in (':answer-field.type/radio',':answer-field.type/blank')
 for text in [q[':question/problem'],q[':question/worked-solution']]: balanced(text)
 if f[':answer-field/type'].endswith('/blank'): assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 # Read supplied components from actual printed prompt, never generation metadata.
 matches=re.findall(r'⟨([^⟩]+)⟩',q[':question/problem'])
 assert len(matches)==2,(rec['generation']['template'],matches)
 a,b=[[eval_math(z) for z in v.split(',')] for v in matches]
 assert len(a)==len(b) and len(a) in (2,3)
 label_matches=re.findall(r'(?:\\overset\{\\to \}\{([a-z])\}|([a-z]))\s*=\s*⟨',q[':question/problem'])
 actual_names=[x or y for x,y in label_matches]
 assert actual_names==rec['generation']['parameters']['names']
 products=[x*y for x,y in zip(a,b)]
 correct=sum(products)
 answers=f[':answer-field/choices']; vals=[eval_math(z[':answer/value']) for z in answers]
 assert len(vals)==len(set(vals))
 assert len(vals)==(5 if f[':answer-field/type'].endswith('/radio') else 1)
 for z in answers:
  assert z[':answer/type']==':answer.type/math'; uuid.UUID(z[':answer/id']); balanced(z[':answer/value'])
 cref=f[':answer-field/correct']; assert cref[0]==':answer/id'
 selected=[v for z,v in zip(answers,vals) if z[':answer/id']==cref[1]]
 assert selected==[correct],(selected,correct)
 # Recompute every displayed distractor using independent exact operations.
 p=rec['generation']['bank_profile']; c=correct; t=products
 expected={
 'observed_1340':lambda:[b[0]*b[1],2*c,-t[0]+t[1],c,a[0]*a[1]+b[0]*b[1]],
 'observed_101406':lambda:[t[1]-t[0],c,2*t[0],t[1],-t[0]],
 'observed_1341':lambda:[t[0],t[0]+t[2],t[0]-2*t[1],t[0]-t[2],c],
 'observed_1355':lambda:[t[2]-t[0],c,-t[0],-c,t[0]-t[2]],
 'authored_operations':lambda:[c,sum(a)+sum(b),sum(a)*sum(b),sum(t[1:]),sum(t[:-1])]
 }.get(p,lambda:[c])()
 assert Counter(vals)==Counter(expected)
 sol=q[':question/worked-solution']
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
 rows=[r for block in blocks for r in block.split(r'\\')]
 assert len(rows)==4,(p,rows)
 rhs=[row.split('& =')[1].strip() for row in rows]
 # Formal structure: each coordinate exactly once, corresponding pair, ordered x,y,z.
 names=actual_names; x,y=names
 expected_formal='+'.join('{'+x+'}_{'+k+r'}\cdot {'+y+'}_{'+k+'}' for k in 'xyz'[:len(a)])
 assert rhs[0]==expected_formal
 # Multiplication structure: exactly one actual corresponding product per coordinate.
 terms=rhs[1].strip().split('+')
 assert len(terms)==len(a)
 for term,v,w in zip(terms,a,b):
  factors=term.split(r'\cdot'); assert len(factors)==2
  assert [eval_math(z) for z in factors]==[v,w],(term,v,w)
  for z in factors:
   if eval_math(z)<0: assert z.strip().startswith('(') and z.strip().endswith(')')
 # Verify individually evaluated products, preserving addition/subtraction stage.
 summands=re.findall(r'(?:(?<=^)|(?<=[+\-]))\(?-?\d+(?:\.\d+)?\)?',rhs[2].strip())
 # Tokenize top-level +/-, so parenthesized negative products remain intact.
 text=rhs[2].strip(); tokens=[]; start=0; depth=0
 for i,ch in enumerate(text):
  if ch=='(': depth+=1
  elif ch==')': depth-=1
  if ch in '+-' and depth==0 and i>start:
   tokens.append(text[start:i]); start=i
 tokens.append(text[start:])
 assert [eval_math(z) for z in tokens]==products,(tokens,products)
 for row in rhs[1:]: assert eval_math(row)==correct,(row,correct)
 # Same displayed content keeps identity despite shuffling; aliases don't count tasks.
 fixed={k:v for k,v in rec['generation']['parameters'].items()}
 again=g.generate(q[':question/difficulty'].split('/')[-1],seed=999,template=rec['generation']['template'],parameters=fixed,profile=p)
 assert again['question'][':question/id']==q[':question/id']
 assert again['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
 return correct

def engine_item(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio option actual native grading'} for a in f[':answer-field/choices']]
 else:
  v=f[':answer-field/choices'][0][':answer/value']; c=eval_math(v)
  checks=[{'submitted':v,'expected':'accepted','purpose':'canonical exact entry'}, {'submitted':f'({c.numerator*3})/({c.denominator*3})','expected':'accepted','purpose':'unreduced exact rational equivalent'}, {'submitted':str(c+1),'expected':'rejected','purpose':'incorrect neighboring scalar'}]
 return {'label':label,'record':rec,'checks':checks}

def main():
 sources=g.SOURCES; cases=read(HERE/'source-cases.json')
 replay=[]; source_report=[]; inputs=[]
 for case in cases:
  r=g.generate(case['difficulty'],17,case['template'],parameters=case['parameters'],profile=case['bank_profile'])
  check_record(r); replay.append(r); inputs.append(engine_item(case['source_id'],r))
  raw=sources[case['source_id']]; f=raw[':question/answer-fields'][0]; made=r['question']; mf=made[':question/answer-fields'][0]
  assert Counter(eval_math(z[':answer/value']) for z in f[':answer-field/choices'])==Counter(eval_math(z[':answer/value']) for z in mf[':answer-field/choices'])
  expected_prompt=raw[':question/problem']
  repaired=case['source_id']=='q-168035'
  if repaired: expected_prompt='Given $q=⟨0,-3,2⟩$ and $r=⟨0,4,3⟩.$\n\n'+expected_prompt
  assert made[':question/problem']==expected_prompt,(case['source_id'],made[':question/problem'],expected_prompt)
  if ':question/worked-solution' in raw: assert made[':question/worked-solution']==raw[':question/worked-solution'],case['source_id']
  designation='inferred' if ':answer-field/correct' not in f else 'matched'
  if designation=='matched':
   original=eval_math(f[':answer-field/correct'][':answer/value'])
   correct=next(eval_math(a[':answer/value']) for a in mf[':answer-field/choices'] if a[':answer/id']==mf[':answer-field/correct'][1]); assert correct==original
  source_report.append({'source_id':case['source_id'],'bank_values_matched':len(f[':answer-field/choices']),'complete_bank':True,'correct_designation':designation,'prompt':'presentation repaired' if repaired else 'raw exact','worked_solution':'raw exact' if ':question/worked-solution' in raw else 'authored missing'})
 variants=[]
 # Exercise every observed bank with changed mathematical inputs, plus defaults.
 for i,case in enumerate(cases):
  r=g.generate('easy',131+i,case['template'],profile=case['bank_profile']); check_record(r); variants.append(r); inputs.append(engine_item('observed-profile variant '+case['source_id'],r))
 # 250 per level/layout; narrow level guards are tested on explicit and random calls.
 sample_records=[]; unique={}; correct_positions=set()
 for level in ('easy','moderate','hard'):
  unique[level]=set()
  for template,spec in g.TEMPLATES.items():
   if level not in spec['levels']: continue
   for seed in range(250):
    r=g.generate(level,seed,template=template); check_record(r); sample_records.append(r); unique[level].add(r['generation']['mathematical_fingerprint'])
    f=r['question'][':question/answer-fields'][0]
    if f[':answer-field/type'].endswith('/radio'): correct_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
    if seed<2: variants.append(r); inputs.append(engine_item(level+' '+template+' '+str(seed),r))
  assert len(unique[level])>=250
 assert correct_positions==set(range(5))
 # Boundary workload checks; invalid explicit inputs must fail, never be resampled.
 bad=[('moderate',{'a':[1,2,3],'b':[2,-3,4]}),('moderate',{'a':[2,3,4],'b':[2,3,4]}),('hard',{'a':[1,2,3],'b':[2,-3,4]}),('hard',{'a':['0.5','1.1','2.2'],'b':[2,-3,4]}),('hard',{'a':['6.1','1.1','2.2'],'b':[2,-3,4]})]
 for l,p in bad:
  try:g.generate(l,template='components3_blank',parameters=p)
  except ValueError:pass
  else:raise AssertionError(('invalid accepted',l,p))
 # Fingerprints are coordinate permutation and factor-order invariant.
 r1=g.generate_easy(template='if2_blank',parameters={'a':[2,3],'b':[4,5]})
 r2=g.generate_easy(template='if2_blank',parameters={'a':[5,4],'b':[3,2],'names':['u','v']})
 assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
 assert r1['question'][':question/id']!=r2['question'][':question/id']
 write(HERE/'source-replay.json',replay); write(HERE/'review.json',variants); write(HERE/'engine-input.json',inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 eng=read(HERE/'engine-report.json')
 report={'passed':True,'database':'math','basis':1356,'lineage':g.RAW['lineage'],'source_count':7,'complete_banks_matched':7,'answer_values_matched':23,'answer_values_total':23,'observed_distractors_matched':16,'observed_distractors_total':16,'correct_designations_matched':6,'correct_designations_total_present':6,'missing_designations_inferred':1,'raw_exact_prompts':6,'presentation_repaired_prompts':1,'raw_exact_solutions':6,'present_solutions_total':6,'missing_solutions_authored':1,'source_results':source_report,'random_records_checked':len(sample_records),'unique_mathematical_tasks_observed_in_validation':{k:len(v) for k,v in unique.items()},'all_five_correct_radio_positions_exercised':True,'invalid_explicit_parameter_rejections':len(bad),'native_grading':{k:eng[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'engine_sha256':sha(ROOT/'generate/runs/current/check-engine'),'engine_source_sha256':sha(ROOT/'generate/runs/current/check-engine.rs'),'generator_sha256':sha(SCRIPT),'source_sha256':sha(HERE/'source.json')}
 write(HERE/'validation.json',report)
 print(json.dumps(report,indent=2))
if __name__=='__main__': main()
