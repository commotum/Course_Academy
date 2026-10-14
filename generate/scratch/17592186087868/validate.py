#!/usr/bin/env python3
"""Independent displayed mathematics, exact source fidelity, and native grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SOURCE=json.loads((HERE/'source.json').read_text())
CASES=json.loads((HERE/'source-cases.json').read_text())

def formatting(text):
 assert not any(ord(c)<32 and c not in '\n\t\r' for c in text),'Control characters'
 assert text.count('$')%2==0,'Math dollars'
 depth=0
 for i,c in enumerate(text):
  if c in '{}':
   if i and text[i-1]=='\\':continue
   depth+=1 if c=='{' else -1
   assert depth>=0,'TeX groups'
 assert depth==0,'TeX groups'
 assert not re.search(r'\{\{\w+\}\}',text),'Unresolved masks'
 assert '+-' not in text and '--' not in text,'Signed operands'

def check(record):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 q=record['question'];meta=record['generation'];f=q[':question/answer-fields'][0]
 assert q[':question/difficulty']==':question.difficulty/'+g.TEMPLATES[meta['template']]['level']
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 assert meta['eligible_for_learning']==(not meta['evidence_only'])
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in f[':answer-field/choices']]:formatting(text)
 normal,forcing,correct,criterion=g.assessed_from_prompt(q[':question/problem'])
 vals=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(vals)==len(set(vals))==5
 assert all(a[':answer/type']==':answer.type/text' for a in f[':answer-field/choices'])
 assert vals.count(correct)==1
 assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==correct
 solution=q[':question/worked-solution']
 # Read each displayed equation and operand in its actual per-equation section.
 sections=re.split(r'- (?:First|Next|Finally), we consider the equation\n\n',solution)[1:]
 assert len(sections)==3
 for i,section in enumerate(sections):
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',section,re.S)
  assert blocks
  simple=blocks[0].rstrip('.')
  assert sp.expand(g.canonical_equation(simple)-normal[i])==0,'Initial equation mismatch'
  aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',section,re.S)
  if aligned:
   assert len(aligned)==1
   rows=re.split(r'\\\\',aligned[0]);rows=[s.strip().rstrip('.') for s in rows]
   assert len(rows)==(4 if meta['template']=='collect_and_normalize' else 3),'Operative row count'
   for row in rows:assert sp.expand(g.canonical_equation(row)-normal[i])==0,'Displayed intermediate operand error'
   assert rows[0].replace(' & ','')==simple,'Original aligned stage'
   # The uncollected movement row retains separate y terms; collection groups
   # their coefficient. Counting rows alone would miss a collapsed operation.
   assert rows[1].replace(g.D,'').count('y')==2,'Separate moved y terms required'
   if meta['template']=='collect_and_normalize':
    assert rows[1].count('x')>=2,'Move forcing stage'
    assert '(' in rows[2] and '\\frac' not in rows[2],'Collect stage'
    assert '\\frac' in rows[3],'Divide stage'
   else:
    assert rows[2].replace(g.D,'').count('y')==1,'Collected y coefficient'
  expected_class='homogeneous' if forcing[i]==0 else 'inhomogeneous'
  assert ('the equation is '+expected_class+'.' in section or 'this equation is '+expected_class+'.' in section or 'this equation *is* '+expected_class+'.' in section or (expected_class=='inhomogeneous' and 'this equation is *not* homogeneous.' in section)), 'Classification prose'
  for value in re.findall(r'\$Q\(x\)=(.*?)\$',section):
   assert sp.simplify(g.parse_expr(value)-forcing[i])==0,'Displayed Q operand'
 conclusion=solution.split('Therefore, the correct answer is ')[-1].strip('".\n ')
 assert conclusion.replace('I, II and III','I, II, and III')==correct,'Final conclusion'
 content=g.digest({'version':g.VERSION,'difficulty':q[':question/difficulty'].split('/')[-1],'prompt':q[':question/problem'],'solution':solution,'bank':sorted(vals)})
 assert meta['content_fingerprint']==content and q[':question/id']==g.uid('q/'+content),'Content identity'
 assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
 return True

def main():
 fidelity=[];all_records=[];distractors=0
 originals={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
 for case in CASES:
  record=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(record)
  q=record['question'];src=originals[case['source_id']];f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
  assert q[':question/problem']==src[':question/problem'],case['source_id']+' prompt'
  assert q[':question/worked-solution']==src[':question/worked-solution'],case['source_id']+' solution'
  assert set(q)-{':question/id'}==set(src)-{':db/id',':question/id'},'Question attribute presence parity'
  assert set(f)==set(sf)-{':db/id'},'Field attribute presence'
  for a in f[':answer-field/choices']:assert set(a)==set(sf[':answer-field/choices'][0])-{':db/id'}
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
  fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact':True,'complete_bank_exact':True,'correct_designation_exact':True,'attribute_presence':True});distractors+=4;all_records.append(record)
 review=[];slot_coverage={};family_coverage={l:set() for l in ('easy','moderate','hard')};fingerprints=set();identities=set();positions=set()
 for t,r in g.TEMPLATES.items():
  coverage=[]
  for seed in range(35):
   record=g.generate(r['level'],seed,template=t);check(record);all_records.append(record);coverage.append(record['generation']['parameters'])
   fingerprints.add(record['generation']['mathematical_fingerprint']);identities.add(record['question'][':question/id'])
   if seed<2:review.append(record)
   same=g.generate(r['level'],seed+1000,template=t,parameters=record['generation']['parameters'],profile=record['generation']['profile'])
   assert same['question'][':question/id']==record['question'][':question/id'],'Shuffle-independent identity'
   f=record['question'][':question/answer-fields'][0];positions.add([a[':answer/id'] for a in f[':answer-field/choices']].index(f[':answer-field/correct'][1]))
  slot_coverage[t]={'sampled_parameters':len({json.dumps(p,sort_keys=True) for p in coverage}),'coefficients':sorted({p['a'] for p in coverage}) if r['level']!='hard' else sorted({v[1] for p in coverage for v in p['equations']})}
  if r['level']!='hard':
   slot_coverage[t]['powers']=sorted({p['n'] for p in coverage})
   slot_coverage[t]['rhs_slots']=[{key:sorted({p['rhs'][i][j] for p in coverage}) for j,key in enumerate(('b','c','m'))} for i in range(3)]
  else:
   slot_coverage[t]['equation_slots']=[{key:sorted({p['equations'][i][j] for p in coverage}) for j,key in enumerate(('k','a','n','b','d','e','m'))} for i in range(3)]
 # Exercise exact range endpoints and signed forcing under public normal/raw profiles.
 for t,r in g.RECIPES.items():
  src=r['parameters']
  for magnitude in (1,9):
   for force_sign in (-1,1):
    p={'a':magnitude*(1 if src['a']>0 else -1),'n':0 if src['n']==0 else (1 if magnitude==1 else 3),'rhs':[]}
    for b,c,m in src['rhs']:
     p['rhs'].append([5*(1 if b>0 else -1),0,0] if b else ([0,force_sign*magnitude,0 if m==0 else (1 if magnitude==1 else 3)] if c else [0,0,0]))
    for prefix in ('raw_','observed_'):
     record=g.generate(r['level'],template=t,parameters=p,profile=prefix+t);check(record);all_records.append(record)
 for pos in range(3):
  for seed in (14,19):
   record=g.generate_hard(seed,profile='authored_hard_'+str(pos));check(record);all_records.append(record);review.append(record)
 for level in family_coverage:
  for seed in range(100):
   record=g.generate(level,seed);check(record);family_coverage[level].add(record['generation']['template'])
  assert family_coverage[level]=={t for t,r in g.TEMPLATES.items() if r['level']==level},'Normal sampler family coverage'
 assert len(positions)>1,'Radio shuffle'
 for profile,data in g.PROFILES.items():
  record=g.generate(g.TEMPLATES[data['template']]['level'],1,profile=profile);check(record)
 # Invalid explicit boundaries must be rejected, without resampling.
 for level,t,p,profile in [('easy','q-331601',{'a':10,'n':1,'rhs':[[0,0,0],[0,4,0],[-1,0,0]]},None),('moderate','q-331742',{'a':2,'n':0,'rhs':[[2,0,0],[0,1,1],[0,0,0]]},None),('hard','collect_and_normalize',{'equations':[[1,2,1,1,1,2,1],[2,2,1,1,1,1,1],[2,2,1,1,1,1,1]],'target':'inhomogeneous'},'authored_hard_0')]:
  try:g.generate(level,template=t,parameters=p,profile=profile)
  except ValueError:pass
  else:raise AssertionError('Explicit workload guard')
 catalog={}
 for t,r in g.RECIPES.items():
  sample_record=g.generate(r['level'],template=t,parameters=r['parameters']);catalog[sample_record['generation']['mathematical_fingerprint']]={'level':r['level'],'source_layout':t}
 for pos in range(3):
  sample_record=g.generate_hard(0,profile='authored_hard_'+str(pos));catalog[sample_record['generation']['mathematical_fingerprint']]={'level':'hard','nonzero_forcing_position':pos+1}
 assert len(catalog)==15 and fingerprints==set(catalog),'Finite semantic catalog coverage'
 mutations=[]
 anchor=g.generate_easy(template='q-331601',parameters=g.RECIPES['q-331601']['parameters'])
 for label,old,new in [('wrong displayed operand','2xy+y','2xy-y'),('missing operation','2xy+y & =0','(2x+1)y & =0'),('stale conclusion','I and III only.','II only.'),('control character','2xy+y','2xy+\x0cy')]:
  changed=copy.deepcopy(anchor);changed['question'][':question/worked-solution']=changed['question'][':question/worked-solution'].replace(old,new)
  try:check(changed)
  except (AssertionError,ValueError):mutations.append(label)
  else:raise AssertionError('Mutation escaped '+label)
 engine=[]
 for i,record in enumerate(all_records):
  f=record['question'][':question/answer-fields'][0]
  engine.append({'label':str(i),'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned categorical choice'} for a in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False,indent=2)+'\n')
 executable=ROOT/'generate/runs/current/check-engine'
 subprocess.run([str(executable),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 report=json.loads((HERE/'engine-report.json').read_text())
 validation={'passed':True,'source':g.SOURCE,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_questions':12,'source_prompt_exact':12,'source_solution_exact':12,'source_banks_exact':12,'source_choices_exact':60,'source_distractors_exact':distractors,'source_correct_designations_exact':12,'attribute_presence_exact':12,'presentation_repairs':0,'mathematical_repairs':0,'generated_checked':len(all_records)-12,'native':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'engine_sha256':hashlib.sha256(executable.read_bytes()).hexdigest(),'normal_family_coverage':{k:sorted(v) for k,v in family_coverage.items()},'slot_coverage':slot_coverage,'finite_semantic_task_count':len(catalog),'finite_semantic_task_catalog':catalog,'sampled_mathematical_fingerprints':len(fingerprints),'sampled_content_identities':len(identities),'categorical_variety_note':'Coefficient and exponent aliases do not inflate semantic task count; source templates preserve finite positional/categorical relations. Hard has three forcing-position tasks with identical normalization workload.','mutation_regressions':mutations,'failures':[],'fidelity':fidelity}
 (HERE/'validation.json').write_text(json.dumps(validation,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
 out=['# Review: homogeneous / inhomogeneous ODE recognition','All records are local drafts at math basis 1356. Raw source profiles are evidence-only. Normal generated examples preserve source operative masks. Hard is an authored scope extension.']
 for src_id,src in originals.items():
  out.extend(['## Original '+src_id,src[':question/problem'],'Bank: '+', '.join(a[':answer/value'] for a in src[':question/answer-fields'][0][':answer-field/choices']),src[':question/worked-solution']])
  for record in review:
   if record['generation']['template']==src_id:out.extend(['### Generated variant ('+record['generation']['profile']+')',g.markdown(record)])
 out.append('## Authored missing hard level')
 for record in review:
  if record['generation']['template']=='collect_and_normalize':out.append(g.markdown(record))
 (HERE/'review.md').write_text('\n\n'.join(out)+'\n')
 print(json.dumps({k:validation[k] for k in ('passed','source_questions','generated_checked','native','mutation_regressions')},indent=2))
if __name__=='__main__':main()
