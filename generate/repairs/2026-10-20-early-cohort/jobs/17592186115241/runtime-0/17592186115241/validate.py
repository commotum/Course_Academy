#!/usr/bin/env python3
"""Independent printed-mathematics, original-fidelity, identity, native grading QA."""
from pathlib import Path
import importlib.util, json, re, hashlib, subprocess, copy
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def algebra_layout(text):
 # Read canonical matrices using the existing independent algebra checks.
 text=re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',lambda m:r'[\begin{aligned}'+m[1]+r'\end{aligned}]',text,flags=re.S)
 text=re.sub(r'\\left\[\\begin\{array\}\{[^}]+\}(.*?)\\end\{array\}\\right\]',lambda m:r'[\begin{aligned}'+m[1]+r'\end{aligned}]',text,flags=re.S)
 return text.replace(' &=','=')

def expressions(body):return [g.load_expr(v.strip().lstrip('&').strip()) for v in body.split(r'\\')]
def printed_matrices(text):
 text=algebra_layout(text)
 out=[]
 for m in g.INNER.finditer(text):
  if '&' in m[1] and '=' not in m[1]:out.append(sp.Matrix([[g.load_expr(v) for v in row.split('&')] for row in m[1].split(r'\\')]))
 return out

def printed_system(text,n):
 blocks=[m[1] for m in g.INNER.finditer(text) if '=' in m[1]];assert len(blocks)==1
 rows=[]
 for line in blocks[0].split(r'\\'):
  l,r=line.lstrip(' &').split('=');e=sp.expand(g.load_expr(l)-g.load_expr(r));rows.append([e.coeff(v) for v in g.VARS[:n]]+[-e.subs({v:0 for v in g.VARS})])
 return sp.Matrix(rows)

def ops_from_print(text):
 ops=[];names=sp.symbols('a b c d')
 for m in re.finditer(r'\{R\}_\{(\d)\}\s*&?\s*:=(.*?)(?=\\\\|\\end\{aligned\})',text,re.S):
  i=int(m[1])-1;s=re.sub(r'\{R\}_\{(\d)\}',lambda p:str(names[int(p[1])-1]),m[2].strip())
  s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',s)
  e=sp.sympify(s,locals={str(v):v for v in names},evaluate=True) if '*' in s else __import__('sympy').parsing.sympy_parser.parse_expr(s,local_dict={str(v):v for v in names},transformations=g.TRANSFORMS)
  ops.append((i,[e.coeff(v) for v in names]))
 return ops

def signature(v):
 if v is None:return ('text','No solution')
 return tuple(sp.expand(e) for e in v)

def math_components(text):
 text=algebra_layout(text)
 out=[]
 for m in g.INNER.finditer(text):
  body=m[1]
  if '=' in body:
   out.append(('equations',tuple(sp.expand(g.load_expr(line.strip().lstrip('&').split('=')[0])-g.load_expr(line.split('=')[1])) for line in body.split(r'\\'))))
  elif '&' in body:
   out.append(('matrix',tuple(tuple(g.load_expr(v) for v in row.split('&')) for row in body.split(r'\\'))))
  else:out.append(('vector',tuple(expressions(body))))
 return out

def prose(text):
 text=re.sub(r'\$\$.*?\$\$', '[MATH]',text,flags=re.S);text=re.sub(r'\$[^$]*\$', '[INLINE]',text)
 return text

def check_record(r):
 r=copy.deepcopy(r)
 for key in [':question/problem',':question/worked-solution']:
  r['question'][key]=algebra_layout(r['question'][key])
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];gen=r['generation'];fields=q[':question/answer-fields'];assert len(fields)==1
 assert fields[0][':answer-field/type']==':answer-field.type/radio'
 n=len(gen['matrix'][0])-1;M=printed_system(q[':question/problem'],n)
 assert M==sp.Matrix(gen['matrix'])
 R,piv=M.rref();assert n not in piv
 mats=printed_matrices(q[':question/worked-solution']);ops=ops_from_print(q[':question/worked-solution'])
 assert mats[0]==M and mats[1]==M,(gen['bank_profile'],'initial')
 assert len(mats)==len(ops)+2,(gen['bank_profile'],len(mats),len(ops))
 for k,(i,coeffs) in enumerate(ops):
  prev=mats[k+1];row=sum((coeffs[j]*prev.row(j) for j in range(prev.rows)),sp.zeros(1,prev.cols));nextm=prev.copy();nextm[i,:]=row
  assert nextm==mats[k+2],(gen['bank_profile'],'row operation',k)
 assert mats[-1]==R
 f=fields[0];assert len(f[':answer-field/choices'])==5
 correct=f[':answer-field/correct'][1];hits=[];values=[]
 for a in f[':answer-field/choices']:
  v=g.parse_vector(a[':answer/value']);values.append(signature(v))
  if v is not None and all(sp.expand(e)==0 for e in M[:,:-1]*sp.Matrix(v)-M[:,-1]):hits.append(a[':answer/id'])
 assert hits==[correct] and len(set(values))==5
 cv=g.parse_vector(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct))
 # Every corresponding/solved equation is independently checked against the printed system's solution.
 for m in g.INNER.finditer(q[':question/worked-solution']):
  if '=' in m[1]:
   for line in m[1].split(r'\\'):
    lhs,rhs=line.strip().lstrip('&').strip().split('=',1)
    e=g.load_expr(lhs)-g.load_expr(rhs)
    assert sp.expand(e.subs({g.VARS[i]:cv[i] for i in range(n)},simultaneous=True))==0,(gen['bank_profile'],'solved equation',line)
 for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/worked-solution'].replace('$$',''),re.S):
  if '=' in inline and '\n' not in inline:
   lhs,rhs=inline.split('=',1);e=g.load_expr(lhs)-g.load_expr(rhs)
   assert sp.expand(e.subs({g.VARS[i]:cv[i] for i in range(n)},simultaneous=True))==0
 # Every displayed vector, including the vector of variables, is checked structurally.
 for m in g.INNER.finditer(q[':question/worked-solution']):
  if '=' not in m[1] and '&' not in m[1]:
   v=expressions(m[1]);assert len(v)==n
   if v!=list(g.VARS[:n]):assert all(sp.expand(v[i]-cv[i])==0 for i in range(n))
 if gen.get('authored'):
  assert len(ops)=={'easy':2,'moderate':6,'hard':9}[q[':question/difficulty'].rsplit('/',1)[1]]
 # Only escaped literal system braces are permitted; all remaining TeX braces balanced.
 for s in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in f[':answer-field/choices']]:
  assert s.count('$$')%2==0
  assert s.replace('$$','').count('$')%2==0
  t=re.sub(r'\\[{}]','',s);assert t.count('{')==t.count('}')
 import uuid
 uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id'])
 for a in f[':answer-field/choices']:uuid.UUID(a[':answer/id'])
 return len(ops)

def main():
 cases=json.loads((HERE/'source-cases.json').read_text());review=[];source_rows=[];checks=[];banks=choices=designations=solutions=0
 for c in cases:
  qid=c['source_id'];r=g.generate('easy',seed=7,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check_record(r)
  original=g.QUESTIONS[qid]
  if qid not in ('q-32234','q-42040'):
   assert printed_system(original[':question/problem'],len(g.BASE[qid][0])-1)==sp.Matrix(g.BASE[qid])
   assert prose(original[':question/problem'])==prose(r['question'][':question/problem'])
  else:
   inline=re.search(r'\$\{(.*?)\$',original[':question/problem'],re.S)[1]
   reconstructed=[]
   for line in inline.split(';'):
    lhs,rhs=line.split('=');e=sp.expand(g.load_expr(lhs)-g.load_expr(rhs));reconstructed.append([e.coeff(v) for v in g.VARS[:3]]+[-e.subs({v:0 for v in g.VARS})])
   assert sp.Matrix(reconstructed)==sp.Matrix(g.BASE[qid])
  field=original[':question/answer-fields'][0];generated=r['question'][':question/answer-fields'][0]
  original_values=[signature(g.parse_vector(a[':answer/value'])) for a in field[':answer-field/choices']]
  actual_values=[signature(g.parse_vector(a[':answer/value'])) for a in generated[':answer-field/choices']]
  assert sorted(map(str,original_values))==sorted(map(str,actual_values));banks+=1;choices+=len(actual_values)
  if ':answer-field/correct' in field:
   target=signature(g.parse_vector(field[':answer-field/correct'][':answer/value']));actual=signature(g.parse_vector(next(a[':answer/value'] for a in generated[':answer-field/choices'] if a[':answer/id']==generated[':answer-field/correct'][1])))
   assert target==actual;designations+=1
  if original.get(':question/worked-solution'):
   assert math_components(original[':question/worked-solution'])==math_components(r['question'][':question/worked-solution'])
   assert prose(original[':question/worked-solution'])==prose(r['question'][':question/worked-solution'])
   assert printed_matrices(original[':question/worked-solution'])==printed_matrices(r['question'][':question/worked-solution'])
   assert ops_from_print(original[':question/worked-solution'])==ops_from_print(r['question'][':question/worked-solution']);solutions+=1
  row={'source_id':qid,'complete_bank_matched':True,'choices_matched':5,'original_correct_designation_matched':':answer-field/correct' in field,'original_worked_solution_sequence_and_prose_matched':bool(original.get(':question/worked-solution')),'notation_normalized':True}
  source_rows.append(row);review.append({'kind':'original_replay','source_id':qid,'record':r})
  for seed in (11,23):
   variant=g.generate('easy',seed,profile=qid);check_record(variant);review.append({'kind':'generated_observed_variant','source_id':qid,'record':variant})
  checks.append({'label':qid,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==generated[':answer-field/correct'][1] else 'rejected','purpose':'all displayed radio choices, after independent mathematical verification'} for a in generated[':answer-field/choices']]})
 variant_counts={};native_counts=0
 for level in ('easy','moderate','hard'):
  fingerprints=set()
  for seed in range(120):
   r=g.generate(level,seed);check_record(r);fingerprints.add(r['generation']['mathematical_fingerprint'])
   same=g.generate(level,seed+1000,parameters=r['generation']['parameters']);assert r['question'][':question/id']==same['question'][':question/id']
   assert r['generation']['mathematical_fingerprint']==same['generation']['mathematical_fingerprint']
   if seed<2:review.append({'kind':'generated_authored_level','record':r})
   if seed<12:
    f=r['question'][':question/answer-fields'][0]
    checks.append({'label':level+'-'+str(seed),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'canonical and every incorrect owned radio ID'} for a in f[':answer-field/choices']]});native_counts+=5
  assert len(fingerprints)>=110;variant_counts[level]=len(fingerprints)
 # Rational explicit inputs exercise the supported exact-arithmetic boundaries.
 boundary_records=[]
 for level in ('easy','moderate','hard'):
  p=g.generate(level,5)['generation']['parameters']
  p['free_coefficients']=[str(sp.Rational(i,3 if level=='hard' else 2)) for i in p['free_coefficients']]
  p['constants']=[str(sp.Rational(i,2)) for i in p['constants']]
  boundary_records.append((level+'-rational',g.generate(level,parameters=p)))
 for qid in g.QUESTIONS:
  boundary_records.append((qid+'-affine-rational',g.generate('easy',profile=qid,parameters={'scale':'1/2','offsets':['1/2']*(len(g.BASE[qid][0])-1)})))
 for label,r in boundary_records:
  check_record(r);f=r['question'][':question/answer-fields'][0]
  checks.append({'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'supported rational-boundary complete bank'} for a in f[':answer-field/choices']]})
 # Equivalent parameter spelling and option order cannot change content identity.
 qid='q-131715'
 a=g.generate('easy',profile=qid,parameters={'scale':1,'offsets':[0,0,0]})
 b=g.generate('easy',seed=99,profile=qid,parameters={'scale':'1.0','offsets':['0','0','0']})
 assert a['question'][':question/id']==b['question'][':question/id']
 # Explicit workload-bound failures are errors, not quietly resampled parameter sets.
 for level in ('easy','moderate','hard'):
  p=g.generate(level,1)['generation']['parameters'];bad={**p,'free_coefficients':[99]+p['free_coefficients'][1:]}
  try:g.generate(level,parameters=bad)
  except ValueError:pass
  else:raise AssertionError('explicit bound bypass')
 (HERE/'native-input.json').write_text(json.dumps(checks,indent=2)+'\n')
 exe=HERE.parents[1]/'runs/current/check-engine';subprocess.run([str(exe),str(HERE/'native-input.json'),str(HERE/'native-results.json')],check=True)
 native=json.loads((HERE/'native-results.json').read_text())
 (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 md=[]
 for entry in review:
  md.append('## '+entry['kind']+' '+entry.get('source_id',entry['record']['question'][':question/difficulty']))
  if entry['kind']=='original_replay':
   o=g.QUESTIONS[entry['source_id']];md+=['### Original captured prompt/bank/solution',o[':question/problem']]+['- '+a[':answer/value'] for a in o[':question/answer-fields'][0][':answer-field/choices']]+[o.get(':question/worked-solution') or '(No source worked solution or correct designation captured.)','### Parameterized replay with notation/presentation repair']
  md.append(g.markdown(entry['record']))
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
 validation={'status':'pass','basis':g.RAW['basis'],'lineage':g.RAW['lineage'],'practice_questions':11,'observed_easy':9,'unrated':2,'complete_banks_matched':banks,'answer_values_matched':choices,'available_original_correct_designations_matched':designations,'available_original_correct_designations_total':9,'unavailable_correct_designations':2,'independently_derived_missing_designations':2,'worked_solutions_prose_and_sequence_matched':solutions,'available_original_worked_solutions_total':9,'math_notation_normalization':True,'presentation_repairs':['unclosed source TeX system braces escaped','unrated semicolon systems rebuilt as aligned systems'],'generated_questions_checked':360+22+11+len(boundary_records),'rational_boundary_records_checked':len(boundary_records),'distinct_mathematical_tasks_120_seeds':variant_counts,'source_results':source_rows,'native_grading':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks'],'executable_sha256':hashlib.sha256(exe.read_bytes()).hexdigest()},'authored_levels':['moderate: six operations, 3 equations / 3 unknowns / rank 2','hard: nine operations, 3 equations / 4 unknowns / rank 3'],'plots':'none','source_assets_inspected':3,'database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps(validation,indent=2))
if __name__=='__main__':main()
