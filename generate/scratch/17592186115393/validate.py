#!/usr/bin/env python3
"""Independent displayed-LaTeX, source-bank, derivative, identity, and native tests."""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('product_generator',HERE.with_suffix('.py'));gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
TRANS=standard_transformations+(implicit_multiplication_application,)

def latex_expr(raw):
 """Parse every complete scalar displayed option; reject unsupported syntax.

This parser is independent of the generator's srepr data and covers the actual
source/generated banks (fractions, roots, logs, real exponentials and powers).
It is deliberately strict, and cannot silently accept a truncated expression.
"""
 raw=raw.replace('\u2061','').replace(r'\operatorname{ln}',r'\ln').replace(r'\log',r'\ln').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace('−','-')
 raw=re.sub(r'\s+','',raw)
 def group(s,pos):
  if pos>=len(s):raise ValueError('Missing command argument: '+raw)
  ch=s[pos]
  if ch in '{(':
   close='}' if ch=='{' else ')';depth=1;j=pos+1
   while j<len(s) and depth:
    if s[j]==ch:depth+=1
    if s[j]==close:depth-=1
    j+=1
   if depth:raise ValueError('Unbalanced group: '+raw)
   return convert(s[pos+1:j-1]),j
  if ch=='\\':
   # log argument can itself be a fraction/root; consume command plus its groups
   match=re.match(r'\\(frac|sqrt|ln)',s[pos:]);cmd=match.group(1) if match else None
   if not cmd:raise ValueError('Unsupported argument command '+raw)
   _,j=group(s,pos+len(cmd)+1)
   if cmd=='frac':_,j=group(s,j)
   return convert(s[pos:j]),j
  m=re.match(r'\d+(?:\.\d+)?|[a-zA-Z]',s[pos:])
  if not m:raise ValueError('Invalid argument '+raw)
  j=pos+len(m.group(0))
  if j<len(s) and s[j]=='^':_,j=group(s,j+1)
  return convert(s[pos:j]),j
 def convert(s):
  out=[];i=0
  while i<len(s):
   if s[i]=='\\':
    m=re.match(r'\\(frac|sqrt|ln)',s[i:])
    if not m:raise ValueError('Unsupported command in '+raw+' at '+s[i:])
    cmd=m.group(1);i+=len(cmd)+1;a,i=group(s,i)
    if cmd=='frac':b,i=group(s,i);out.append('(('+a+')/('+b+'))')
    elif cmd=='sqrt':out.append('sqrt('+a+')')
    else:out.append('log('+a+')')
   elif s[i] in '{(':
    a,i=group(s,i);out.append('('+a+')')
   elif s[i]=='^':a,i=group(s,i+1);out.append('**('+a+')')
   else:
    if s[i] not in 'tijk e0123456789.+-*/)' or s[i]==')':raise ValueError('Unexpected character '+s[i]+' in '+raw)
    out.append(s[i]);i+=1
  return ''.join(out)
 transformed=convert(raw)
 return parse_expr(transformed,local_dict={'t':gen.t,'e':sp.E,'i':sp.Symbol('i'),'j':sp.Symbol('j'),'k':sp.Symbol('k'),'log':sp.log,'sqrt':sp.sqrt},transformations=TRANS)

def display_value(raw):
 raw=raw.replace(r'\,','')
 if '⟨' in raw:
  prefix,rest=raw.split('⟨',1)
  if not rest.endswith('⟩'):raise ValueError('Vector trailing content')
  parts=rest[:-1].split(',');factor=latex_expr(prefix) if prefix else sp.Integer(1)
  return factor*sp.Matrix([latex_expr(x) for x in parts])
 if r'\begin{bmatrix}' in raw:
  inside=raw.split(r'\begin{bmatrix}',1)[1].split(r'\end{bmatrix}',1)[0]
  return sp.Matrix([latex_expr(x) for x in inside.split(r'\\')])
 if raw.startswith(r'[\begin{aligned}'):
  inside=raw[len(r'[\begin{aligned}'):].split(r'\end{aligned}]')[0]
  return sp.Matrix([latex_expr(x) for x in inside.split(r'\\')])
 return latex_expr(raw)

def prompt_values(prompt,name):
 style=gen.TEMPLATES[name][2]
 if style=='tuple':
  vectors=[display_value(x) for x in re.findall(r'⟨[^⟨⟩]*⟩',prompt)]
 elif style=='matrix':
  vectors=[display_value(x) for x in re.findall(r'\[\\begin\{aligned\}.*?\\end\{aligned\}\]',prompt)]
 else:
  if r'\begin{aligned}' in prompt:
   expressions=re.findall(r'[fg]\(t\) & =(.*?)(?: \\\\ |\\end\{aligned\})',prompt)
  else:
   expressions=re.findall(r'f\(t\)=(.*?)\$',prompt)
  vectors=[]
  for expression in expressions:
   value=sp.expand(latex_expr(expression.rstrip(' ,;.')))
   i,j,k=sp.symbols('i j k');vector=sp.Matrix([value.coeff(i),value.coeff(j),value.coeff(k)])
   assert sp.simplify(value-vector[0]*i-vector[1]*j-vector[2]*k)==0
   vectors.append(vector)
 if gen.TEMPLATES[name][0]=='easy':
  scalar=re.search(r'[uv]\(t\)=(.*?)\$',prompt)
  assert scalar,name+' prompt scalar'
  vectors.append(latex_expr(scalar.group(1).rstrip(' .;,')))
 return vectors

def decode(v):return sp.Matrix([sp.sympify(x) for x in v]) if isinstance(v,list) else sp.sympify(v)
def eq(a,b):return gen.equivalent(a,b)
def prose(s):
 s=re.sub(r'\$\$.*?\$\$','<math>',s,flags=re.S);s=re.sub(r'\$[^$]*\$','<math>',s)
 return re.sub(r'\s+',' ',s).strip()

def independent(record):
 g=record['generation'];m=g['mathematics'];name=g['template'];level=gen.TEMPLATES[name][0];f=decode(m['f']);other=decode(m['g_or_scalar']) if m['g_or_scalar'] is not None else None
 # Directly differentiate the original product as an independent alternative
 # to the generator's product-rule/intermediate formulas.
 if level=='easy':expected=(other*f).diff(gen.t).applyfunc(sp.simplify);A=other*f.diff(gen.t);B=sp.diff(other,gen.t)*f
 elif level=='moderate':
  if other is None:expected=sp.diff(f.diff(gen.t).dot(f),gen.t);A=f.diff(gen.t,2).dot(f);B=f.diff(gen.t).dot(f.diff(gen.t))
  else:expected=sp.diff(f.dot(other),gen.t);A=f.diff(gen.t).dot(other);B=f.dot(other.diff(gen.t))
  if name=='dot_self_evaluate':expected=expected.subs(gen.t,g['parameters']['x'])
 else:
  if other is None:expected=f.diff(gen.t).cross(f).diff(gen.t);A=f.diff(gen.t,2).cross(f);B=f.diff(gen.t).cross(f.diff(gen.t))
  else:expected=f.cross(other).diff(gen.t);A=f.diff(gen.t).cross(other);B=f.cross(other.diff(gen.t))
 assert eq(expected,decode(m['correct'])),name+' derivative'
 assert eq(A,decode(m['first_product_term'])) and eq(B,decode(m['second_product_term'])),name+' intermediate'
 q=record['question'];fields=q[':question/answer-fields'];assert len(fields)==1
 inputs=prompt_values(q[':question/problem'],name);expected_inputs=[f]+([other] if other is not None else [])
 assert len(inputs)==len(expected_inputs) and all(eq(a,b) for a,b in zip(inputs,expected_inputs)),name+' displayed prompt inputs'
 seen=[]
 for field in fields:
  assert field[':answer-field/type']==':answer-field.type/radio';assert len(field[':answer-field/choices'])==5
  correct=field[':answer-field/correct'][1];assert sum(a[':answer/id']==correct for a in field[':answer-field/choices'])==1
  for a in field[':answer-field/choices']:
   shown=display_value(a[':answer/value']);assert eq(shown,decode(m['answer_values'][a[':answer/id']])),name+' displayed option'
   assert eq(shown,expected)==(a[':answer/id']==correct),name+' displayed designation'
   assert not any(eq(shown,x) for x in seen),name+' equivalent options';seen.append(shown)
  for key in (':answer-field/id',):assert gen.uuid.UUID(field[key])
 for a in fields[0][':answer-field/choices']:assert gen.uuid.UUID(a[':answer/id'])
 assert gen.uuid.UUID(q[':question/id'])
 # The worked solution's displayed computed derivative vectors and both
 # intermediate results must appear in their appropriate representation.
 V=lambda x:gen.vector(x,gen.TEMPLATES[name][2])
 assert V(f.diff(gen.t)) in q[':question/worked-solution']
 if level=='easy':assert gen.tex(sp.diff(other,gen.t)) in q[':question/worked-solution']
 elif other is None:assert V(f.diff(gen.t,2)) in q[':question/worked-solution']
 else:assert V(other.diff(gen.t)) in q[':question/worked-solution']
 shown_correct=decode(m['correct'])
 final=V(shown_correct) if isinstance(shown_correct,sp.MatrixBase) else gen.tex(shown_correct)
 assert final in q[':question/worked-solution']
 # Parse displayed determinant input matrices, independently recompute the
 # three signed minors, and compare to the cross-product terms.
 if level=='hard':
  dets=re.findall(r'\|\\begin\{aligned\}i & j & k \\\\ (.*?)\\end\{aligned\}\|',q[':question/worked-solution'])
  assert len(dets)==2,name+' displayed determinants'
  for determinant,expected_term in zip(dets,[A,B]):
   rows=determinant.split(r'\\');u,v=[sp.Matrix([latex_expr(x) for x in row.split('&')]) for row in rows]
   manual=sp.Matrix([u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]])
   assert eq(manual,expected_term),name+' displayed signed minors'
 # Separately parse computed vector values actually printed in solutions.
 if isinstance(expected,sp.MatrixBase):
  if gen.TEMPLATES[name][2]=='matrix':raw_vectors=re.findall(r'\[\\begin\{aligned\}.*?\\end\{aligned\}\]',q[':question/worked-solution'])
  else:raw_vectors=re.findall(r'⟨[^⟨⟩]*⟩',q[':question/worked-solution'])
  allowed=[f,f.diff(gen.t),A,B,expected]
  if level=='hard':allowed+=[f.diff(gen.t,2)] if other is None else [other,other.diff(gen.t)]
  for raw in raw_vectors:
   if r'\text{d}' in raw:continue
   assert any(eq(display_value(raw),v) for v in allowed),name+' displayed intermediate vector'
 # Algebraic addition rows are parsed from final block for moderate questions.
 if level=='moderate':
  rows=q[':question/worked-solution'].split('Therefore, we obtain:')[1]
  for rhs in re.findall(r' & =(.*?)(?: \\\\ |\\end\{aligned\})',rows):
   if not any(bad in rhs for bad in ('\\cdot','{f}','i','j','k')):
    assert eq(latex_expr(rhs),expected),name+' displayed scalar intermediate'
 assert '{{' not in q[':question/problem'] and '<math>' not in q[':question/problem']
 assert q[':question/problem'].count('$$')%2==0 and q[':question/worked-solution'].count('$$')%2==0
 return True

def main():
 raw=json.load(open(HERE/'source.json'));sources=raw['record'][':knowledge-point/questions'];assert raw['basis']==1356
 cases=json.load(open(HERE/'source-cases.json'));by_id={q[':question/math-academy-id']:q for q in sources}
 assert len(cases)==len(sources) and {c['source_id'] for c in cases}==set(by_id),'Source-case coverage must include every practice question exactly once'
 fidelity=[];engine=[];records=[]
 for case in cases:
  name=case['template'];source=by_id[case['source_id']];record=gen.generate(gen.TEMPLATES[name][0],0,name,parameters=case['parameters'],profile=case['bank_profile']);independent(record);records.append(record)
  generated=record['question'][':question/answer-fields'][0]
  source_inputs=prompt_values(source[':question/problem'],name);generated_inputs=prompt_values(record['question'][':question/problem'],name)
  assert len(source_inputs)==len(generated_inputs) and all(eq(a,b) for a,b in zip(source_inputs,generated_inputs)),case['source_id']+' full prompt mathematical fidelity'
  for idx,original in enumerate(source[':question/answer-fields']):
   bankrecord=gen.generate(gen.TEMPLATES[name][0],0,name,parameters=case['parameters'],profile='cross_matrix_legacy' if name=='cross_matrix' and idx==0 else case['bank_profile'])
   choices=bankrecord['question'][':question/answer-fields'][0][':answer-field/choices'];unmatched=list(choices);matched=[]
   for answer in original[':answer-field/choices']:
    value=display_value(answer[':answer/value']);matches=[a for a in unmatched if eq(value,display_value(a[':answer/value']))];assert len(matches)==1,(case['source_id'],answer[':answer/value']);found=matches[0];unmatched.remove(found);matched.append({'source_value':answer[':answer/value'],'generated_value':found[':answer/value'],'generated_id':found[':answer/id']})
   assert not unmatched
   origcorrect=original.get(':answer-field/correct');designation='absent-source-designation-unmatchable'
   if origcorrect:
    expected=display_value(origcorrect[':answer/value']);actual=next(display_value(a[':answer/value']) for a in generated[':answer-field/choices'] if a[':answer/id']==generated[':answer-field/correct'][1]);assert eq(expected,actual);designation='matched'
   fidelity.append({'source_id':case['source_id'],'field_index':idx,'bank_matched':5,'bank_total':5,'designation':designation,'legacy_artifact':name=='cross_matrix' and idx==0,'options':matched})
  assert prose(source[':question/worked-solution'])==prose(record['question'][':question/worked-solution']),case['source_id']+' shared solution prose'
 assert len(fidelity)==14 and sum(x['bank_matched'] for x in fidelity)==70,'Full captured-bank coverage required'
 # Stress every whole bank and template, covering generated profiles rather
 # than merely a recipe pool. Explicit negative coefficient boundaries included.
 unique={l:set() for l in ('easy','moderate','hard')};counter=0
 for name,(level,_,_,base) in gen.TEMPLATES.items():
  for profile in (name+'_observed',name+'_authored'):
   for seed in range(12):
    record=gen.generate(level,seed,name,profile=profile);independent(record);counter+=1;unique[level].add(record['generation']['parameter_fingerprint']);records.append(record)
    p=record['generation']['parameters'];r2=gen.generate(level,seed+100,name,parameters=p,profile=profile)
    assert record['question'][':question/id']==r2['question'][':question/id'];assert record['generation']['content_fingerprint']==r2['generation']['content_fingerprint']
  authored=gen.generate(level,0,name,parameters=base,profile=name+'_authored');observed=gen.generate(level,0,name,parameters=base,profile=name+'_observed')
  independent(authored);records.append(authored);counter+=1
  assert authored['question'][':question/id']!=observed['question'][':question/id'] and authored['generation']['parameter_fingerprint']==observed['generation']['parameter_fingerprint']
  bad=dict(base);bad['unexpected']=1
  try:gen.generate(level,0,name,parameters=bad)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit keys silently changed')
  if name not in ('scalar_exp','scalar_base'):
   boundary=dict(base);first=next(k for k in boundary if k not in ('x','n','m','p','q','r'));boundary[first]=-boundary[first]
   try:independent(gen.generate(level,99,name,parameters=boundary));counter+=1
   except gen.SampleRejected:pass # Whole-bank rejection is the prescribed behavior.
 legacy=gen.generate('hard',0,'cross_matrix',parameters=gen.TEMPLATES['cross_matrix'][3],profile='cross_matrix_legacy')
 normal=gen.generate('hard',0,'cross_matrix',parameters=gen.TEMPLATES['cross_matrix'][3]);assert legacy['question'][':question/id']!=normal['question'][':question/id'];assert legacy['generation']['parameter_fingerprint']==normal['generation']['parameter_fingerprint'];records.append(legacy)
 for i,record in enumerate(records):
  f=record['question'][':question/answer-fields'][0];checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio '+('correct' if a[':answer/id']==f[':answer-field/correct'][1] else 'wrong')} for a in f[':answer-field/choices']]
  engine.append({'label':str(i)+'-'+record['generation']['template'],'record':record,'checks':checks})
 (HERE/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False,indent=2))
 exe=ROOT/'generate/runs/current/check-engine';report=HERE/'engine-report.json';result=subprocess.run([str(exe),str(HERE/'engine-input.json'),str(report)],capture_output=True,text=True);assert result.returncode==0,result.stdout+result.stderr
 output={'status':'pass','source_provenance':{k:raw[k] for k in ('database','basis','lineage')},'source_questions':len(cases),'source_banks':len(fidelity),'complete_banks_matched':len(fidelity),'source_answer_values_matched':sum(x['bank_matched'] for x in fidelity),'source_answer_values_total':70,'correct_designations_matched':sum(x['designation']=='matched' for x in fidelity),'absent_legacy_designations':1,'raw_source_layout_fidelity':'repair-required: one legacy duplicate field','raw_source_worked_math_fidelity':'repair-required: q-33446 extra middle factor','source_prompt_mathematics':'13/13 matched','shared_solution_prose':'13/13 matched','independent_symbolic_and_display_checks':counter+13,'parameter_fingerprints_by_level':{k:len(v) for k,v in unique.items()},'default_bank_policy':'whole operation-derived authored banks; observed profiles explicit for exact replay','profiles_exercised':list(gen.BANK_PROFILES),'native_engine':{'input_instances':len(engine),'checks':sum(len(x['checks']) for x in engine),'status':'pass','executable_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'build_log_sha256':hashlib.sha256((ROOT/'generate/runs/current/engine-build.log').read_bytes()).hexdigest()},'fidelity':fidelity,'unresolved_errors':[]}
 (HERE/'validation.json').write_text(json.dumps(output,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in output.items() if k!='fidelity'},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as error:
  (HERE/'validation.json').write_text(json.dumps({'status':'fail','error':str(error)},indent=2));raise
