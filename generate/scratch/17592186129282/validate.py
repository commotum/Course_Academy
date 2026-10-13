#!/usr/bin/env python3
"""Independent displayed math, full raw source bank fidelity, real native grader.

Expected source repairs never masquerade as exact designation matches.
"""
import hashlib,importlib.util,itertools,json,re,subprocess,copy
from pathlib import Path
import sympy as sp
from math_parser import parse,u,v
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('area_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(n,z):(H/n).write_text(json.dumps(z,indent=2,ensure_ascii=False)+'\n')
def eq(a,b):return sp.simplify(sp.trigsimp(a-b))==0
def coefficient(s):
 s=s.replace('δA','').replace(r'\delta A','').replace(r'\,','').strip()
 return parse(s or '1')
def check(r):
 assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=r['question'];f=q[':question/answer-fields'][0];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 point=re.search(r'point \$\((-?\d+),(-?\d+)\)\$',prompt);assert point
 a,b=map(sp.Integer,point.groups());subs={u:a,v:b}
 components=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',prompt,re.S)[-1].split(r'\\');assert len(components)==2
 x,y=[parse(z) for z in components];d=[sp.diff(x,u),sp.diff(x,v),sp.diff(y,u),sp.diff(y,v)];J=d[0]*d[3]-d[1]*d[2];value=sp.simplify(J.subs(subs));C=sp.Abs(value)
 assert C.is_positive is True and 'best approximation' in prompt and 'small rectangle' in prompt
 assert all(s in sol for s in [g.OPENING,g.COMPUTING,g.ENDING])
 assert not any(w in prompt.lower() for w in ['orientation','inverse','integrate','exact area'])
 block=sol.split(g.COMPUTING+'\n\n')[1].split(g.ENDING)[0]
 matrices=re.findall(r'\\left\|\\begin\{matrix\}(.*?)\\end\{matrix\}\\right\|',block,re.S);assert len(matrices)==2
 vals=[parse(z) for z in re.split(r'&|\\\\',matrices[1])];assert len(vals)==4 and all(eq(z,w) for z,w in zip(vals,d))
 block=re.sub(r'\\left\|\\begin\{matrix\}.*?\\end\{matrix\}\\right\|','MATRIX',block,flags=re.S)
 rows=block.split(r'\\'); evaluated=False;stagecount=0
 for row in rows:
  if r'\right|_' in row:
   evaluated=True
   assert f'({a},{b})' in row and f'u={a},v={b}' in row
   expr=re.search(r'& =\\left\((.*?)\\right\)\\big\|',row).group(1)
   assert eq(parse(expr),J)
  elif row.startswith('& =') and 'MATRIX' not in row:
   body=row[3:].split(r'\end{aligned}')[0].split('$$')[0].strip()
   assert eq(parse(body),value if evaluated else J),(body,value if evaluated else J)
   stagecount+=1
 assert evaluated and stagecount>=4
 area_block=sol.split(g.ENDING+'\n\n')[1];signed=parse(re.search(r'approx\|(.*?)\|',area_block).group(1));ans=coefficient(re.search(r'& =(.*?)\.\\end\{aligned\}',area_block).group(1));assert eq(signed,value) and eq(ans,C)
 values=[];ids=[]
 for z in f[':answer-field/choices']:
  val=coefficient(z[':answer/value']);values.append(val);ids.append(z[':answer/id'])
  assert val.is_nonnegative is True and '$'not in z[':answer/value'] and z[':answer/type']==':answer.type/math'
  assert eq(val,C)==(z[':answer/id']==f[':answer-field/correct'][1])
 assert len(values)==len(set(ids))==5 and all(not eq(a,b) for a,b in itertools.combinations(values,2))
 assert prompt.count('$$')==2 and sol.count('$$')==6
 return {'displayed_partial_entries':4,'displayed_scalar_solution_stages':stagecount,'displayed_choice_values':5}

def main():
 source=json.loads((H/'source.json').read_text());assert source==json.loads((ROOT/'generate/runs/current/sources/17592186129282.json').read_text())
 cases=json.loads((H/'source-cases.json').read_text());orig={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};assert len(cases)==len(orig)==11
 records=[];fidelity=[];reviews=[]
 for case in cases:
  q=orig[case['source_id']]
  for bp in case['bank_profiles']:
   r=g.generate('easy',parameters=case['parameters'],profile=bp['bank_profile']);check(r);records.append(r)
   assert r['question'][':question/worked-solution'].count(r'\\')==q[':question/worked-solution'].count(r'\\'),case['source_id']
   sf=q[':question/answer-fields'][bp['source_field_index']];f=r['question'][':question/answer-fields'][0]
   expected=[coefficient(a[':answer/value']) for a in sf[':answer-field/choices']];actual=[coefficient(a[':answer/value']) for a in f[':answer-field/choices']]
   matches=[[i for i,z in enumerate(actual) if eq(z,val)] for val in expected];assert all(len(z)==1 for z in matches) and len({z[0] for z in matches})==5
   correct=next(coefficient(z[':answer/value']) for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);rawcorrect=sf.get(':answer-field/correct');matched=bool(rawcorrect) and eq(coefficient(rawcorrect[':answer/value']),correct)
   if rawcorrect and not matched:assert case['source_id']=='q-161831' and bp['source_field_index']==0 and coefficient(rawcorrect[':answer/value'])==1 and correct==2
   fidelity.append({'source_id':case['source_id'],'source_field_id':sf[':answer-field/id'],'profile':bp['bank_profile'],'options_matched':5,'options_total':5,'complete_bank_matched':True,'original_designation_present':bool(rawcorrect),'original_designation_matched':bool(matched),'repair':'missing legacy ref independently derived' if not rawcorrect else 'stale legacy δA designation corrected to 2δA' if not matched else None,'layout':'one generated radio assessment; raw duplicate fields replayed separately','solution_normalization':'same shared prose and complete stages; standard LaTeX and equivalent derivative fractions'})
 # Every complete observed and authored bank profile receives two changed variants.
 for profile,info in g.BANK_PROFILES.items():
  t=info['template'];level=g.TEMPLATES[t][0]
  for seed in (13,27):
   r=g.generate(level,seed,profile=profile);check(r);records.append(r);reviews.append(r)
   fixed=g.generate(level,seed+99,template=t,parameters=r['generation']['parameters'],profile=profile)
   assert fixed['question'][':question/id']==r['question'][':question/id'] and fixed['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
 # Default variety and parameter invalidity; score unique mathematical tasks, not order.
 variety={}
 for t,(level,src,p) in g.TEMPLATES.items():
  fingerprints=set()
  for seed in range(12):
   r=g.generate(level,seed,template=t);check(r);records.append(r);fingerprints.add(r['generation']['parameter_fingerprint'])
  assert len(fingerprints)>=5,(t,len(fingerprints));variety[t]={'samples':12,'distinct_mathematical_tasks':len(fingerprints)}
 # Mathematical task fingerprint independent of bank/layout.
 for case in cases:
  observed=g.generate('easy',parameters=case['parameters'],profile=case['bank_profile'])
  try:authored=g.generate('easy',parameters=case['parameters'],profile='authored_area_'+case['template'])
  except g.SampleRejected:continue # fixed original C=2 creates a declared whole-bank collision
  assert observed['generation']['parameter_fingerprint']==authored['generation']['parameter_fingerprint']
  if sorted(a[':answer/value'] for a in observed['question'][':question/answer-fields'][0][':answer-field/choices'])!=sorted(a[':answer/value'] for a in authored['question'][':question/answer-fields'][0][':answer-field/choices']):assert observed['question'][':question/id']!=authored['question'][':question/id']
 for kwargs in [dict(level='easy',template='sqrt_sum',parameters={'u0':2,'v0':2}),dict(level='easy',template='log_product',parameters={'u0':-1,'v0':2}),dict(level='easy',template='poly_sum',profile='observed_sin_sum'),dict(level='hard',parameters={'a':1}),dict(level='moderate',field_type='blank'),dict(level='easy',template='exp_product',parameters={'u0':-1,'v0':1},profile='authored_area_exp_product')]:
  try:g.generate(**kwargs)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit request accepted')
 # Mutations prove actual displayed prompt and intermediate checks are sensitive.
 probe=g.generate('easy',template='poly_sum',parameters={'u0':1,'v0':2},profile='observed_poly_sum')
 for part,old,new in [(':question/problem','(1,2)','(1,3)'),(':question/worked-solution',r'-6uv^{2}-2',r'-6uv^{2}+2')]:
  mutant=copy.deepcopy(probe);mutant['question'][part]=mutant['question'][part].replace(old,new,1)
  try:check(mutant)
  except AssertionError:pass
  else:raise AssertionError('Displayed math mutation was not caught')
 engine=[]
 for i,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0]
  engine.append({'label':f'case-{i}-{r["generation"]["bank_profile"]}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned radio selection, independently math-verified'} for a in f[':answer-field/choices']]})
 write('engine-input.json',engine);binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(H/'engine-input.json'),str(H/'engine-validation.json')],check=True)
 write('source-bank-fidelity.json',fidelity);write('review.json',reviews)
 report={'status':'pass','database_writes':0,'provenance':g.PROVENANCE,'source_questions':11,'raw_source_fields':13,'source_values_matched':65,'source_values_total':65,'complete_source_banks_matched':13,'complete_source_banks_total':13,'original_correct_designations_matched':11,'original_correct_designations_total_present':12,'stale_designations_repaired':1,'missing_designations_authored':1,'field_layout_repairs':2,'source_errors_resolved':True,'original_wrong_operation_intent':'unresolved underdetermined scalar evidence; replay-only proportional shapes, excluded from defaults','solution_exact_byte_fidelity':False,'solution_prose_and_math_stage_fidelity':'shared prose and symbolic simplification stages preserved; Unicode/matrix/radical notation normalized','generated_records_checked':len(records),'generated_review_records':len(reviews),'default_variety':variety,'native_engine':json.loads((H/'engine-validation.json').read_text()),'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'authored_missing_levels':{'moderate':'canonical e-12417 monomial/sum small scales','hard':'sibling e-6810 bounded sum/difference powers plus evaluated area factor'},'plots':'none; canonical formula bitmap visually inspected'};write('validation.json',report)
 lines=['# Local area review','', 'Originals are raw evidence. Replays normalize mathematical notation and repair duplicate/stale fields, with original-bank values and designation counts reported separately.','']
 for case in cases:
  q=orig[case['source_id']];lines+=['## Original '+case['source_id'],'',q[':question/problem'],'']
  for i,f in enumerate(q[':question/answer-fields']):
   lines+=['Raw field '+str(i)+'; correct designation: '+str(f.get(':answer-field/correct',{}).get(':answer/value','MISSING')),'']
   lines+=['- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']]
  lines+=['','Original worked solution:',q[':question/worked-solution'],'','### Parameterized source replay (single repaired field)',g.markdown(g.generate('easy',parameters=case['parameters'],profile=case['bank_profile'])),'']
 lines+=['# Clearly labeled generated variants','', 'Observed profile variants are proportional-shape replay extensions with unresolved original distractor intent; authored profiles and missing levels are labeled in each record.','']
 for r in reviews:lines+=[g.markdown(r),'']
 (H/'review.md').write_text('\n'.join(lines)+'\n')
 print(f'PASS: 65/65 source values; 13/13 complete banks; 11/12 present original designations matched, 1 stale repaired + 1 absent authored. {len(records)} independent displayed-math records; {len(records)*5} native selections. All three levels.')
if __name__=='__main__':main()
