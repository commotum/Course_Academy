#!/usr/bin/env python3
"""Independent displayed-math verification, full bank fidelity, native grading."""
import hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
import sympy as sp
from math_parser import parse,u,v
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('evaluation',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(n,z):(HERE/n).write_text(json.dumps(z,indent=2)+'\n')
def equal(a,b):return sp.simplify(sp.trigsimp(a-b))==0

def check_record(r):
 q=r['question'];meta=r['generation'];f=q[':question/answer-fields'][0]
 assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 matrices=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'])
 x,y=map(parse,matrices[1].split(r'\\'));U,V=map(parse,matrices[3].split(r'\\'))
 ds=[sp.diff(x,u),sp.diff(x,v),sp.diff(y,u),sp.diff(y,v)];det=sp.Matrix([ds[:2],ds[2:]]).det();val=sp.simplify(det.subs({u:U,v:V}))
 assert equal(det,sp.sympify(meta['determinant'])) and equal(val,sp.sympify(meta['evaluated_value']))
 vals=[];ids=[]
 for a in f[':answer-field/choices']:
  aid=a[':answer/id'];z=parse(a[':answer/value']);ids.append(aid);vals.append(z)
  assert equal(z,sp.sympify(meta['answer_math'][aid]['expression']))
  assert equal(z,val)==(aid==f[':answer-field/correct'][1])
  assert a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value']
 assert len(ids)==len(set(ids))==5 and all(not equal(a,b) for a,b in itertools.combinations(vals,2))
 sol=q[':question/worked-solution'];deriv=sol.split('First, we find the partial derivatives:\n\n')[1].split('$$')[1]
 parts=re.split(r'&=|&\\quad |\\\\',deriv);actual=[parse(z.split(r'\end{aligned}')[0]) for z in parts[1::2]]
 assert len(actual)==4 and all(equal(a,b) for a,b in zip(actual,ds))
 symbolic=sol.split('Therefore, the corresponding Jacobian determinant is\n\n')[1].split('Finally, when')[0]
 rows=symbolic.split(r'\\');checked=0
 for row in rows:
  if row.startswith('&=') and 'matrix' not in row:
   z=parse(row[2:].split(r'\end{aligned}')[0].rstrip('.'));assert equal(z,det),row;checked+=1
 assert checked>=2
 # Read every evaluation RHS from displayed final equality, including numeric
 # substitution. This catches signed powers, missing variables and bad points.
 final=sol.rsplit('$$',2)[1];rhs=final.split('}=',1)[1].strip().rstrip('.')
 stages=rhs.split('=');assert len(stages)==2 and all(equal(parse(s),val) for s in stages)
 assert 'at the point where' in q[':question/problem'] and not any(z in q[':question/problem'].lower() for z in ['area','orientation','inverse','region'])
 assert all(s in sol for s in ['Given a transformation','the Jacobian determinant of $T,','Here, we have','First, we find the partial derivatives:','Therefore, the corresponding Jacobian determinant is','the value of our Jacobian determinant is'])
 assert sol.count('$$')%2==0 and q[':question/problem'].count('$$')%2==0
 return {'derivatives':4,'symbolic_rows':checked,'numeric_stages':len(stages)}

def main():
 src=json.loads((HERE/'source.json').read_text());qs=src['record'][':knowledge-point/questions'];cases=json.loads((HERE/'source-cases.json').read_text());assert len(cases)==len(qs)==11 and src['basis']==1356
 originals={q[':question/math-academy-id']:q for q in qs};records=[];fidelity=[]
 for c in cases:
  r=g.generate('easy',parameters=c['parameters'],profile=c['bank_profile']);check_record(r);records.append(r)
  sf=originals[c['source_id']][':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0]
  assert originals[c['source_id']][':question/worked-solution'].count(r'\\')==r['question'][':question/worked-solution'].count(r'\\'),c['source_id']
  for sentence in ['Given a transformation','the Jacobian determinant of $T,','Here, we have','First, we find the partial derivatives:','Therefore, the corresponding Jacobian determinant is','Finally, when','the value of our Jacobian determinant is']:
   assert sentence in originals[c['source_id']][':question/worked-solution'] and sentence in r['question'][':question/worked-solution']
  # Compare complete displayed source functions and point, not only bank values.
  source_vectors=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',originals[c['source_id']][':question/problem'])
  generated_vectors=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',r['question'][':question/problem'])
  for source_vector,generated_vector in [(source_vectors[1],generated_vectors[1]),(source_vectors[-1],generated_vectors[-1])]:
   assert all(equal(parse(a),parse(b)) for a,b in zip(source_vector.split(r'\\'),generated_vector.split(r'\\')))
  actual=[parse(a[':answer/value']) for a in f[':answer-field/choices']];expected=[parse(a[':answer/value']) for a in sf[':answer-field/choices']]
  matches=[[i for i,b in enumerate(actual) if equal(a,b)] for a in expected];assert all(len(i)==1 for i in matches) and len({i[0] for i in matches})==5
  corr=next(parse(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(corr,parse(sf[':answer-field/correct'][':answer/value']))
  fidelity.append({'source_id':c['source_id'],'profile':c['bank_profile'],'matched_options':5,'total_options':5,'complete_bank_match':True,'correct_designation_match':True,'field_layout_match':True,'prompt_and_solution':'shared wording and operation sequence retained, notation normalized; q-160380 trigonometric typo repaired'})
 variants=[];variety={}
 for profile,bank in g.BANK_PROFILES.items():
  t=bank['template'];level=g.TEMPLATES[t][0]
  for seed in (17,29):
   r=g.generate(level,seed,profile=profile);check_record(r);records.append(r);variants.append(r)
   fixed=g.generate(level,seed+1,parameters=r['generation']['parameters'],profile=profile)
   assert fixed['question'][':question/id']==r['question'][':question/id'] and fixed['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
 for t,(level,p) in g.TEMPLATES.items():
  fingerprints=set()
  for seed in range(20):
   r=g.generate(level,seed,template=t);check_record(r);records.append(r);fingerprints.add(r['generation']['parameter_fingerprint'])
  assert len(fingerprints)>=15,(t,len(fingerprints));variety[t]={'sampled':20,'distinct_assessed_tasks':len(fingerprints)}
 for c in cases:
  t=c['template'];a=g.generate('easy',parameters=c['parameters'],profile=c['bank_profile'])
  try:b=g.generate('easy',parameters=c['parameters'],template=t)
  except g.SampleRejected:continue # Default banks can reject source coincidences honestly.
  assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
  if sorted(x[':answer/value'] for x in a['question'][':question/answer-fields'][0][':answer-field/choices'])!=sorted(x[':answer/value'] for x in b['question'][':question/answer-fields'][0][':answer-field/choices']):assert a['question'][':question/id']!=b['question'][':question/id']
 for kw in [dict(level='easy',profile='observed_polar',template='quotient'),dict(level='hard',template='powers',parameters={'a':1,'b':1,'m':7,'n':2,'U':'1','V':'2'}),dict(level='hard',template='powers',parameters={'a':-8,'b':1,'m':3,'n':2,'U':'1','V':'2'}),dict(level='moderate',template='scaled_exp_log',parameters={'a':8,'b':3,'U':'3','V':'8'}),dict(level='moderate',template='scaled_coupled_trig',parameters={'a':4,'b':2,'c':1,'d':2,'U':'0','V':'pi/6'}),dict(level='easy',field_type='blank'),dict(level='easy',template='quotient',parameters={'a':1,'b':1,'U':'0','V':'1'})]:
  try:g.generate(**kw)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit input silently accepted')
 engine=[{'label':f'{i}-{r["generation"]["bank_profile"]}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] else 'rejected','purpose':'Owned radio choice'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]} for i,r in enumerate(records)]
 write('engine-input.json',engine);binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
 write('source-bank-fidelity.json',fidelity);write('review.json',variants)
 report={'status':'pass','provenance':g.PROVENANCE,'database_writes':0,'source_questions':11,'source_options_matched':55,'source_options_total':55,'complete_source_banks_matched':11,'original_correct_designations_matched':11,'original_correct_designations_total':11,'source_solution_exact_math':10,'source_solution_repaired_math':1,'source_correction':'q-160380 cos²+cos² -> cos²+sin²','math_records_checked':len(records),'displayed_checks':'four derivatives, every distributed/simplified determinant row, numeric substitution and final value, all five choices; parsed from learner text','variety':variety,'review_generated_records':len(variants),'native_engine':json.loads((HERE/'engine-validation.json').read_text()),'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'difficulty_origin':'moderate and hard are authored design claims, not observed levels','observed_scalar_banks':'normalized ratios are explicit replay-only patterns; author intent unresolved; not default banks','unresolved_findings':[]}
 write('validation.json',report)
 lines=['# Evaluating Jacobian review','','Original raw records below; all variants explicitly labeled. Standard matrix and trig notation normalization; one source typo repaired.','']
 for c,r in zip(cases,records):
  q=originals[c['source_id']];lines+=['## Original '+c['source_id'],'',q[':question/problem'],'','Original choices: '+', '.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),'','Original worked solution:',q[':question/worked-solution'],'','### Generated source-parameter replay','',g.markdown(r)]
 lines+=['# Clearly labeled generated variants','']
 for r in variants:lines+=[g.markdown(r)]
 (HERE/'review.md').write_text('\n'.join(lines));print(f'PASS: 55/55 values, 11/11 banks/designations; {len(records)} independent math records and {len(records)*5} native selections.')
if __name__=='__main__':
 try:main()
 except Exception as error:
  write('validation.json',{'status':'fail','error':str(error),'error_type':type(error).__name__,'database_writes':0})
  raise
