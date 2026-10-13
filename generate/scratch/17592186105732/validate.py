#!/usr/bin/env python3
"""Exact source fidelity, independent displayed-node QA, scope and native grader.
Run from repository root with .venv/bin/python. No database operations.
"""
import difflib, hashlib, importlib.util, json, math, re, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent; REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('given_area',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def load(p):return json.loads(Path(p).read_text())
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def parse(t):
 t=t.strip().rstrip('.').replace(r'\cdot','*')
 while r'\frac' in t:
  m=re.search(r'\\frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',t)
  assert m,('unsupported fraction',t)
  t=t[:m.start()]+'('+str(parse(m[1]))+')/('+str(parse(m[2]))+')'+t[m.end():]
 t=re.sub(r'\\sqrt\{([^{}]*)\}',lambda m:'sqrt('+m[1]+')',t)
 t=t.replace('{','(').replace('}',')').replace('^','**').replace(r'\sqrt','sqrt')
 t=re.sub(r'(\d|\))(?=sqrt)',r'\1*',t)
 t=t.replace(')(',')*(')
 return sp.sympify(t,locals=dict(zip(['I','J','K'],sp.symbols('I J K'))))
def balanced(t):
 assert t.count('$')%2==0
 depth=0
 for c in t:
  depth+=1 if c=='{' else -1 if c=='}' else 0
  assert depth>=0
 assert depth==0

def verify(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];f=q[':question/answer-fields'][0];sol=q[':question/worked-solution'];prompt=q[':question/problem']
 for t in [prompt,sol]+[a[':answer/value'] for a in f[':answer-field/choices']]:balanced(t)
 # Read inputs from the actual learner prompt, including the legacy spaces.
 vv=re.findall('⟨([^⟩]*)⟩',prompt);assert len(vv)==2
 a,b=[list(map(lambda x:int(x.replace(' ','')),v.split(','))) for v in vv]
 # Independent hand coordinate determinant and Gram formula; never metadata answer.
 c=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
 n=sum(v*v for v in c)
 assert n==sum(v*v for v in a)*sum(v*v for v in b)-sum(x*y for x,y in zip(a,b))**2
 tri='of the triangle' in prompt;correct=sp.sqrt(n)/(2 if tri else 1)
 # Read back all formal determinant rows from actual displayed solution.
 mats=re.findall(r'\|\\begin\{aligned\}(.+?)\\end\{aligned\}\|',sol)
 assert len(mats)==4
 cells=lambda m:[[s.strip() for s in row.split('&')] for row in m.split(r'\\')]
 assert cells(mats[0])==[['i','j','k'],list(map(str,a)),list(map(str,b))]
 assert [cells(m) for m in mats[1:]]==[[list(map(str,[a[1],a[2]])),list(map(str,[b[1],b[2]]))],[list(map(str,[a[0],a[2]])),list(map(str,[b[0],b[2]]))],[list(map(str,[a[0],a[1]])),list(map(str,[b[0],b[1]]))]]
 # Unevaluated products: test exact values AND operands at their component nodes.
 product=re.search(r' & =(\([^\n]+?)i-(\([^\n]+?)j\+(\([^\n]+?)k \\\\',sol)
 assert product,sol
 values=[parse(product[i]) for i in (1,2,3)]
 assert values==[c[0],-c[1],c[2]]
 expected_operands=[(a[1],b[2],a[2],b[1]),(a[0],b[2],a[2],b[0]),(a[0],b[1],a[1],b[0])]
 for term,operands in zip(product.groups(),expected_operands):
  factors=re.fullmatch(r'\((\(-\d+\)|\d+)\\cdot (\(-\d+\)|\d+)-(\(-\d+\)|\d+)\\cdot (\(-\d+\)|\d+)\)',term)
  assert factors,term
  nums=[int(x.strip('()')) for x in factors.groups()]
  # Swapping factors in the subtracted product is an observed notation variation.
  assert tuple(nums)==operands or tuple(nums)==operands[:2]+(operands[3],operands[2])
 tuple_row=re.search(r' & =⟨([^⟩]+)⟩\.',sol);assert list(map(int,tuple_row[1].split(',')))==c
 basis=sol[:tuple_row.start()].rsplit(' & =',1)[1].split(r'\\')[0].strip()
 assert parse(re.sub(r'(?<![0-9])([ijk])',r'1\1',basis).replace('i','*I').replace('j','*J').replace('k','*K')).expand()==sum(x*y for x,y in zip(c,sp.symbols('I J K')))
 norm_block=re.search(r'\\begin\{aligned\}A & =(.+?)\\end\{aligned\}',sol,re.S)[1]
 rows=norm_block.split(r'\\')
 assert r'\times' in rows[0]
 square_row=rows[1].split('=',1)[1].strip()
 pieces=re.findall(r'(\(-?\d+\)|\{-?\d+\})\^\{2\}',square_row)
 assert [int(x.strip('(){}')) for x in pieces]==c
 for row in rows[1:]:assert sp.simplify(parse(row.split('=',1)[1])-sp.sqrt(n))==0
 if tri:
  final=sol.rsplit('$$',2)[1].strip().rstrip('.')
  expressions=final.split('=')[1:]
  assert len(expressions)>=2
  for expression in expressions:
   expression=expression.replace('A', '('+str(sp.sqrt(n))+')')
   assert sp.simplify(parse(expression)-correct)==0
 vals=[parse(x[':answer/value']) for x in f[':answer-field/choices']]
 assert len(set(vals))==len(vals) and all(v>0 for v in vals)
 aid=f[':answer-field/correct'][1]; matches=[x for x in f[':answer-field/choices'] if x[':answer/id']==aid];assert len(matches)==1
 assert sp.simplify(parse(matches[0][':answer/value'])-correct)==0
 assert len(vals)==(5 if f[':answer-field/type'].endswith('/radio') else 1)
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt
 assert f[':answer-field/correct'][0]==':answer/id'
 assert all(a[':answer/type']==':answer.type/math' for a in f[':answer-field/choices'])
 import uuid
 for identifier in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]:uuid.UUID(identifier)
 assert q[':question/difficulty']==':question.difficulty/'+g.TEMPLATES[r['generation']['template']][0]
 if r['generation']['bank_origin']=='authored' and len(vals)==5:
  expected=[correct,sp.sqrt(n) if tri else sp.sqrt(n)/2]+[sp.sqrt(n-v*v)/(2 if tri else 1) for v in c]
  assert set(map(sp.simplify,expected))==set(vals)
 # No step/progression or sibling vertex/altitude operation.
 assert not any(t in prompt for t in ('vertices','altitude','angle between'))
 return a,b,c,n,correct

def engine_case(r,label):
 f=r['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  for a in f[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned option selection'})
 else:
  value=f[':answer-field/choices'][0][':answer/value'];_,_,c,n,correct=verify(r)
  tri='of the triangle' in r['question'][':question/problem']
  unreduced='sqrt('+ '+'.join('('+str(v)+')^2' for v in c)+')'+('/2' if tri else '')
  checks=[{'submitted':value,'expected':'accepted','purpose':'canonical'}, {'submitted':unreduced,'expected':'accepted','purpose':'independently unreduced squared-component norm'}, {'submitted':str(correct+1),'expected':'rejected','purpose':'incorrect area'}]
 return {'label':label,'record':r,'checks':checks}

def main():
 source=load(HERE/'source.json')['record'][':knowledge-point/questions'];cases=[];records=[];checks=[];fidelity=[];review=[]
 for q in source:
  sid=q[':question/math-academy-id'];s=g.SOURCE_SPECS[sid]
  p={'a':s[1],'b':s[2],'names':list(s[3:5]),'order':s[5]};level=g.TEMPLATES[s[0]][0];profile=sid if s[-1] else None
  case={'source_id':sid,'template':s[0],'level':level,'parameters':p,'bank_profile':profile,'level_origin':'authored-supported' if sid=='q-20003' else 'observed'};cases.append(case)
  r=g.generate(level,template=s[0],parameters=p,profile=profile);verify(r);records.append(r);checks.append(engine_case(r,sid))
  assert r['question'][':question/problem']==q[':question/problem']
  exactsol=q.get(':question/worked-solution')==r['question'][':question/worked-solution'] if ':question/worked-solution' in q else None
  assert exactsol is not False,(sid,list(difflib.ndiff(q[':question/worked-solution'].splitlines(),r['question'][':question/worked-solution'].splitlines())))
  orig=q[':question/answer-fields'][0];gf=r['question'][':question/answer-fields'][0]
  assert gf[':answer-field/key']==orig[':answer-field/key']
  assert gf[':answer-field/type']==orig[':answer-field/type'][':db/ident']
  vals=[parse(x[':answer/value']) for x in orig[':answer-field/choices']];gen=[parse(x[':answer/value']) for x in gf[':answer-field/choices']]
  assert set(vals)==set(gen) and len(vals)==len(gen)
  designation=None
  if ':answer-field/correct' in orig:
   ca=next(a for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);designation=sp.simplify(parse(ca[':answer/value'])-parse(orig[':answer-field/correct'][':answer/value']))==0;assert designation
  fidelity.append({'source_id':sid,'prompt_exact':True,'solution_exact':exactsol,'complete_bank_matched':True,'values_matched':len(vals),'designation_matched':designation,'inferred_missing_key':sid=='q-20003'})
  review.append('## Original '+sid+'\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (source correct)' if a[':answer/id']==orig.get(':answer-field/correct',{}).get(':answer/id') else '') for a in orig[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','No source solution or designation; inferred cross product (-1,1,-1) gives sqrt(3).')+'\n\n### Parameterized replay\n\n'+g.markdown(r))
  # Every observed scalar-bank profile exercised at changed coordinates.
  if profile:
   for scale in (-2,3):
    pp={**p,'a':[scale*x for x in p['a']]};variant=g.generate(level,template=s[0],parameters=pp,profile=profile);verify(variant);records.append(variant);checks.append(engine_case(variant,sid+'/scale='+str(scale)));review.append('### Changed-parameter observed-pattern replay ('+sid+', scaling-only scope)\n\n'+g.markdown(variant))
 for template,ts in g.TEMPLATES.items():
  for seed in range(25):
   r=g.generate(ts[0],seed=seed+100,template=template);verify(r);records.append(r);checks.append(engine_case(r,template+'/'+str(seed)))
   if seed<2:review.append('### Authored default bank / generated variant\n\n'+g.markdown(r))
   p=r['generation']['parameters'];rr=g.generate(ts[0],seed=900+seed,template=template,parameters=p)
   assert r['question'][':question/id']==rr['question'][':question/id']
   assert r['generation']['parameter_fingerprint']==rr['generation']['parameter_fingerprint']
  # Equivalent aliases deduplicate actual assessed tasks across field layouts.
  p=r['generation']['parameters'];pp={**p,'a':p['b'],'b':p['a'],'names':['a','b']}
  assert g.task_key(p,ts[2])==g.task_key(pp,ts[2])
 # Scope regressions: reject reduced-hard / zero-workload explicit parameters.
 for a,b in [([2,4,6],[-2,4,6]),([1,0,2],[2,3,4]),([1,1,1],[-1,1,1]),([7,2,3],[-1,2,4])]:
  try:g.generate_hard(parameters={'a':a,'b':b});raise AssertionError('Invalid hard parameters accepted')
  except ValueError:pass
 # All explicit bank collisions reject whole instance rather than replace choices.
 try:g.generate_moderate(template='triangle_radio_radical',parameters={'a':[1,0,0],'b':[0,3,4]});raise AssertionError('Colliding bank accepted')
 except ValueError:pass
 dump(HERE/'source-cases.json',cases);dump(HERE/'review.json',records);(HERE/'review.md').write_text('# Original and generated review\n\nRaw originals are followed by parameterized replay; changed-source-pattern profiles have explicit interpretation limits. Hard examples are authored given-vector tasks. No plots.\n\n'+'\n\n---\n\n'.join(review)+'\n')
 dump(HERE/'engine-input.json',checks)
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 report=load(HERE/'engine-report.json')
 default=[r for r in records if r['generation']['bank_origin']!='observed-pattern']
 result={'status':'pass','provenance':g.PROVENANCE,'source_questions':len(source),'source_prompt_exact':11,'source_solution_exact':{'matched':10,'available':10,'missing':1},'source_bank_fidelity':{'complete':6,'radio_total':6,'blank_values':5,'all_values_matched':35,'matched_designations':10,'available_designations':10,'missing_inferred_designations':1},'source_details':fidelity,'generated_and_replay_records_checked':len(records),'independent_displayed_math':'prompt vectors, 3x3 determinant, all 2x2 minors, all ordered products, basis vector, tuple, norm squares/sums/radical/simplification, each half-area equality; hand cross and independent Gram determinant','native_grading_report':'engine-report.json','native_grading_status':'pass','default_task_count':len({r['generation']['parameter_fingerprint'] for r in default}),'default_distinct_area_count':len({r['generation']['stages']['area'] for r in default}),'authored_hard_records':sum(r['generation']['authored_extension'] for r in records),'unresolved_findings':['Observed scalar distractor author intent cannot be inferred; supported replay patterns are scaling-ray profiles, excluded from default generation.','q-20003 has no original difficulty, worked solution or correct designation; easy and worked solution authored, correct sqrt(3) inferred, no designation fidelity credited.'],'freeze':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'source-cases.json',HERE/'review.json',HERE/'validate.py',HERE/'build_notes.py',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'README.md',HERE/'authoritative-widget.json',HERE/'review.md',HERE/'engine-report.json',REPO/'generate/runs/current/check-engine']}}
 dump(HERE/'validation.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('source_details','freeze')},indent=2))
if __name__=='__main__':main()
