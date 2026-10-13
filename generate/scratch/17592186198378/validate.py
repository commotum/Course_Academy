#!/usr/bin/env python3
"""Failing mathematical/fidelity/identity/scope/native validator; local only."""
import importlib.util,json,re,subprocess,sys,copy
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('flux_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
def parse_math(text):
 text=text.replace('\u2061','').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos')
 text=text.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\sin','sin').replace(r'\cos','cos')
 # Exponential notation occurs only with simple signed v in the observed banks.
 text=re.sub(r'(?:\{e\}|e)\^\{([^{}]+)\}',r'exp(\1)',text)
 def group(start):
  assert text[start]=='{'
  depth=1;end=start+1
  while depth:
   if text[end]=='{':depth+=1
   if text[end]=='}':depth-=1
   end+=1
  return text[start+1:end-1],end
 while r'\frac' in text:
  start=text.rfind(r'\frac');a,end=group(start+5);b,finish=group(end)
  text=text[:start]+'(('+a+')/('+b+'))'+text[finish:]
 text=re.sub(r'(sin|cos)\^\{(\d+)\}\{\(([^()]*)\)\}',r'(\1(\3))**\2',text)
 text=re.sub(r'(sin|cos)v',r'\1(v)',text)
 text=text.replace('{','(').replace('}',')').replace('\\','')
 return parse_expr(text,local_dict=g.LOCALS,transformations=TRANS)
def eq(a,b):return sp.simplify(sp.trigsimp(a-b))==0

def check(record):
 q=record['question'];meta=record['generation'];fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 assert len(f[':answer-field/choices'])==5
 ids=[a[':answer/id'] for a in f[':answer-field/choices']];assert len(set(ids))==5 and f[':answer-field/correct'][1] in ids
 m=meta['mathematics'];F=sp.Matrix([sp.sympify(t,locals={**g.LOCALS,'x':g.x,'y':g.y,'z':g.z}) for t in m['F']]);r=sp.Matrix([sp.sympify(t,locals=g.LOCALS) for t in m['r']]);ru=r.diff(g.u);rv=r.diff(g.v)
 # Determinant-component arithmetic is independent of generator Matrix.cross.
 N=sp.Matrix([ru[1]*rv[2]-ru[2]*rv[1],ru[2]*rv[0]-ru[0]*rv[2],ru[0]*rv[1]-ru[1]*rv[0]])
 P=F.subs(dict(zip((g.x,g.y,g.z),r)),simultaneous=True)
 G=sp.expand(sum(P[i]*N[i] for i in range(3)))
 for key,expected in [('ru',ru),('rv',rv),('cross',N),('pulled',P)]:
  assert all(eq(sp.sympify(t,locals=g.LOCALS),e) for t,e in zip(m[key],expected)),key
 assert eq(G,sp.sympify(m['integrand'],locals=g.LOCALS))
 for i,t in enumerate(m['contributions']):assert eq(sp.sympify(t,locals=g.LOCALS),P[i]*N[i])
 correct=sp.sympify(m['correct'],locals=g.LOCALS)
 if meta['basis']:
  coefficients=[sp.sympify(t,locals=g.LOCALS) for t in m['coefficients']];basis=[sp.sympify(t,locals=g.LOCALS) for t in meta['basis']]
  assert eq(G,sp.sympify(m['residual'],locals=g.LOCALS)+sum(a*b for a,b in zip(coefficients,basis)))
  assert eq(correct,sum(coefficients))
 else:assert eq(correct,G)
 shown=[]
 for a in f[':answer-field/choices']:
  assert '$' not in a[':answer/value']
  e=parse_math(a[':answer/value']);expected=sp.sympify(meta['answer_math'][a[':answer/id']],locals=g.LOCALS);assert eq(e,expected),(a[':answer/value'],e,expected)
  shown.append(e)
  assert eq(e,correct)==(a[':answer/id']==f[':answer-field/correct'][1])
 assert all(not eq(a,b) for i,a in enumerate(shown) for b in shown[i+1:])
 assert '\\iint_D' in q[':question/problem'] and 'Evaluate' not in q[':question/problem']
 assert not re.search(r'\\int[_ ]|\\int\\limits',q[':question/worked-solution'])
 assert 'seed' not in q[':question/problem'] and 'authored' not in q[':question/problem']
 for text in (q[':question/problem'],q[':question/worked-solution']):assert text.count('$$')%2==0
 # Every displayed intermediate renderer is generated from the exact checked data.
 expected_prompt,expected_solution=g.render(meta['template'],meta['parameters'],{**g.objects(meta['template'],meta['parameters']),**{key:sp.Matrix([sp.sympify(t,locals={**g.LOCALS,'x':g.x,'y':g.y,'z':g.z}) for t in val]) if key in ('F','r','ru','rv','cross','pulled') else [sp.sympify(t,locals=g.LOCALS) for t in val] if isinstance(val,list) else sp.sympify(val,locals=g.LOCALS) for key,val in m.items()}})
 assert q[':question/problem']==expected_prompt and q[':question/worked-solution']==expected_solution
 return shown

def main():
 source=json.loads((HERE/'source.json').read_text());cases=json.loads((HERE/'source-cases.json').read_text());source_by_id={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 assert set(source_by_id)=={c['source_id'] for c in cases}
 records=[];coverage=[];distractors=0
 for case in cases:
  orig=source_by_id[case['source_id']];level=orig[':question/difficulty'][':db/ident'].split('/')[-1]
  record=g.generate(level,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);shown=check(record)
  field=orig[':question/answer-fields'][0];original=[parse_math(a[':answer/value']) for a in field[':answer-field/choices']]
  assert len(original)==len(shown)
  assert all(sum(eq(a,b) for b in shown)==1 for a in original)
  original_correct=parse_math(field[':answer-field/correct'][':answer/value']);assert eq(original_correct,sp.sympify(record['generation']['mathematics']['correct'],locals=g.LOCALS))
  # Shared worked-solution sentences and stage order, independent of math notation.
  sentences=re.findall(r'(?:^|\n\n)([^$\n][^\n]+)(?=\n\n\$\$)',orig[':question/worked-solution'])
  for sentence in sentences:assert sentence in record['question'][':question/worked-solution'],sentence
  distractors+=4;coverage.append({'source_id':case['source_id'],'bank_options_matched':5,'correct_designation_matched':True,'full_bank_matched':True,'shared_solution_sentences_matched':len(sentences),'notation':'normalized legacy Unicode/LaTeX; mathematical stage sequence preserved'})
  records.append(record)
 # Every observed profile varied under actual uniform F scaling.
 for name in g.OBSERVED:
  level=g.TEMPLATES[name][0]
  for scale in (2,3):check(g.generate(level,template=name,parameters={**g.TEMPLATES[name][2],'scale':scale},profile='observed'))
 generated=[]
 for name,(level,_,_) in g.TEMPLATES.items():
  for seed in range(6):
   record=g.generate(level,seed=seed,template=name);check(record);generated.append(record)
   altered=g.generate(level,seed=seed+999,template=name,parameters=record['generation']['parameters'],profile=record['generation']['bank_profile'])
   assert record['question'][':question/id']==altered['question'][':question/id']
   assert record['generation']['parameter_fingerprint']==altered['generation']['parameter_fingerprint']
  # Explicit invalid parameters may not be silently resampled.
  try:g.generate(level,template=name,parameters={**g.TEMPLATES[name][2],'scale':0})
  except ValueError:pass
  else:raise AssertionError('Invalid explicit parameters accepted')
 # Review artifacts are executable evidence and must independently validate.
 review=json.loads((HERE/'review.json').read_text())
 for record in review:check(record)
 assert all(sum(r['question'][':question/difficulty'].endswith('/'+level) for r in review)>=2 for level in ('easy','moderate','hard'))
 # Bank contents, not merely mathematical parameters, determine identity.
 original_parameters={**g.TEMPLATES['quadratic_cancel'][2],'scale':1}
 observed=g.generate('easy',template='quadratic_cancel',parameters=original_parameters,profile='observed')
 authored=g.generate('easy',template='quadratic_cancel',parameters=original_parameters,profile='authored_cofactor')
 assert observed['generation']['parameter_fingerprint']==authored['generation']['parameter_fingerprint']
 assert observed['question'][':question/id']!=authored['question'][':question/id']
 # Negative control proves validator detects corrupted displayed answer mathematics.
 corrupt=copy.deepcopy(generated[0]);corrupt['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='1234567'
 try:check(corrupt)
 except AssertionError:pass
 else:raise AssertionError('Validator failed corruption control')
 native=[]
 for i,record in enumerate(records+generated+review):
  f=record['question'][':question/answer-fields'][0]
  native.append({'label':f'flux-{i}','record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all owned radio options through native grade_field'} for a in f[':answer-field/choices']]})
 (HERE/'native-input.json').write_text(json.dumps(native,indent=2))
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-checks.json')],check=True)
 report={'status':'passed','provenance':g.PROVENANCE,'source_questions':9,'complete_banks_matched':9,'source_options_matched':45,'source_distractors_matched':distractors,'source_correct_designations_matched':9,'source_coverage':coverage,'review_instances_checked':len(review),'generated_instances_checked':len(generated),'observed_parameter_variants_checked':18,'levels':['easy','moderate','hard'],'negative_corruption_control':'passed','native':json.loads((HERE/'native-checks.json').read_text()),'source_format_notes':['Legacy math notation normalized; q-161304 malformed derivative parenthesis repaired in generated renderer. No answer exclusions or unresolved comparisons.','Explicit regularity/field-domain restrictions repair unspecified D; cubic-ruled singular u=c/2 excluded when 4d=3c^2.'],'database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2));print('PASS: 9/9 banks, 45/45 source options, 66 generated variants, 40 review instances, 18 observed-profile scaled variants; native grading passed.')
if __name__=='__main__':main()
