#!/usr/bin/env python3
"""Independent displayed algebra, all synthetic cells, source byte parity, native grading."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('quartic',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=g.X

def read_poly(s):
 s=s.replace('−','-').replace(' ','').replace('{','').replace('}','').replace('^','**')
 s=re.sub(r'(\d)(x|\()',r'\1*\2',s);s=re.sub(r'\)\(',')*(',s)
 return sp.expand(sp.sympify(s,locals={'x':X}))

def prompt_math(record):
 text=record['question'][':question/problem']
 equation=re.search(r'([^$\n]*x[^$\n]*)P\(x\)',text).group(1)
 lhs,rhs=equation.split('=');f=read_poly(lhs);rhs=rhs.strip()
 roots=[]
 for fac in re.findall(r'\((x[^()]*)\)(?:\^\{(\d)\})?',rhs):
  expression=read_poly(fac[0]);root=sp.solve(expression,X)[0];roots.extend([root]*int(fac[1] or 1))
 assert len(roots)==2
 sign=-1 if rhs.startswith('-') else 1
 return f,roots,sign

def math_check(record):
 q=record['question'];meta=record['generation'];p=meta['parameters'];name=meta['template'];raw=meta['evidence_only']
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==g.KP_ID and record['knowledge_point']['title']==g.TITLE
 f,roots,sign=prompt_math(record)
 assert sign==g.TEMPLATES[name]['sign']
 if not raw:
  level=g.TEMPLATES[name]['level']
  if level=='easy':assert roots[0]==roots[1] and p['a']==1 and p['b']==0
  else:assert roots[0]!=roots[1]
  if level=='hard':assert sign==-1
  else:assert sign==1
 quotient,rem=sp.div(f,sign*sp.prod(X-r for r in roots));assert rem==0 and sp.degree(quotient,X)==2
 assert sp.discriminant(quotient,X)<0
 assert sorted(roots)==sorted([p['r1'],p['r2']])
 assert sp.expand(f-sign*(X-p['r1'])*(X-p['r2'])*(p['a']*X**2+p['b']*X+p['c']))==0
 if not raw:
  assert q[':question/difficulty']==':question.difficulty/'+g.TEMPLATES[name]['level']
  assert meta['eligible_for_learning'] and not meta['evidence_only']
  assert '\\underbrace{' in q[':question/worked-solution']
  for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for field in q[':question/answer-fields'] for a in field[':answer-field/choices']]:
   assert not any(ord(c)<32 and c not in '\n\t' for c in text)
 fields=q.get(':question/answer-fields',[])
 for field in fields:
  answers=field[':answer-field/choices'];values=[read_poly(a[':answer/value']) for a in answers]
  assert len(set(map(sp.srepr,values)))==len(values)
  assert sum(sp.expand(v-quotient)==0 for v in values)==1
  if ':answer-field/correct' in field:
   correct=next(a for a in answers if a[':answer/id']==field[':answer-field/correct'][1]);assert sp.expand(read_poly(correct[':answer/value'])-quotient)==0
  if field[':answer-field/type'].endswith('/blank'):assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
 if ':question/worked-solution' not in q:return
 text=q[':question/worked-solution']
 # Prose definitions and named quotient operands must match the printed problem.
 definition=re.search(r'Let \$f\(x\)=([^$]+)\$',text).group(1).rstrip('.')
 assert sp.expand(read_poly(definition)-f)==0
 for operand in re.findall(r'quotient \$\(([^$]+)\)\.\$',text):
  expected_cubic=sp.div(f,X-p['r1'])[0]
  assert sp.expand(read_poly(operand)-expected_cubic)==0
 # Read tables from actual output; independent manual multiply/add checks each cell.
 tables=re.findall(r'\|[^\n]*\n\| ---[^\n]*\n\|[^\n]*\n\|[^\n]*\n\|[^\n]*',text)
 assert len(tables)==2
 current=f
 for i,tab in enumerate(tables):
  rows=[[c.strip().strip('$') for c in row.strip().strip('|').split('|')] for row in tab.splitlines()]
  coeff=sp.Poly(current,X).all_coeffs()
  assert rows[0][1:]==['{x}^{'+str(i)+'}' for i in range(len(coeff)-1,-1,-1)]
  assert rows[3][1]=='↓'
  root=sp.Integer(rows[2][0]);assert root==p['r'+str(i+1)]
  top=list(map(sp.Integer,rows[2][1:]));product=list(map(sp.Integer,rows[3][2:]));bottom=list(map(sp.Integer,rows[4][1:]));assert top==coeff
  assert bottom[0]==top[0]
  for j in range(1,len(top)):
   assert product[j-1]==root*bottom[j-1]
   assert bottom[j]==top[j]+product[j-1]
  assert bottom[-1]==0
  independent,rem=sp.div(current,X-root);assert rem==0
  assert sp.Poly(independent,X).all_coeffs()==bottom[:-1]
  current=independent
 # Parse each displayed fraction division and verify numerator, denominator, quotient.
 fractions=re.findall(r'\\frac\{([^\n]+)\}\{(x[^{}]+)\}=([^,\n]+),',text)
 assert len(fractions)==2
 expected_num=f
 for i,(numerator,denominator,result) in enumerate(fractions):
  n,d,v=map(read_poly,(numerator,denominator,result));assert sp.expand(n-expected_num)==0
  expected_divisor=X-p['r'+str(i+1)]
  if raw and name=='q-112651' and i==1:
   assert d==X-(p['r2']-3) and sp.cancel(n/d-v)!=0 # Explicit source anomaly, not passed algebra.
   d=expected_divisor
  assert sp.expand(d-expected_divisor)==0
  assert sp.expand(n-d*v)==0
  expected_num=v
 # Every non-discriminant display block equation including aligned rows, annotations.
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)
 for block in blocks:
  if '\\frac' in block or '4ac' in block:continue
  s=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').replace(r'\,','')
  s=re.sub(r'\\underbrace\{\((.*?)\)\}_\{P\(x\)\}',r'(\1)',s)
  s=re.sub(r'\{\{\((.*?)\)\}_\{⏟\}\}_\{P\(x\)\}',r'(\1)',s)
  lhs=None
  for row in s.split('\\\\'):
   row=row.strip().rstrip('.,');left,right=row.split('=',1)
   if left.strip():lhs=f if left.strip()=='f(x)' else read_poly(left)
   assert lhs is not None
   assert sp.expand(lhs-read_poly(right))==0
 # Discriminant substitution every coefficient and calculated inequality.
 disc=re.search(r'4ac=(.*?)\^\{2\}-4\(([-\d]+)\)\(([-\d]+)\)=([-\d]+)<0',text)
 assert disc
 b=int(disc[1].strip('{}()'));a,c,D=map(int,disc.groups()[1:]);assert (a,b,c)==(p['a'],p['b'],p['c'])
 assert b*b-4*a*c==D==sp.discriminant(quotient,X)
 # Read final independent conclusion.
 final=re.search(r'Finally, \$P\(x\)=([^$]+)\$',text).group(1).rstrip('.')
 assert sp.expand(read_poly(final)-quotient)==0
 # Exact normal ordered prose/layout stages anchored to each source family.
 expected=g.solution(p,name,raw)
 if not raw:expected=g.normalize_prose(expected)
 assert text==expected

def engine_item(record,label):
 field=record['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1];p=record['generation']['parameters']
 if field[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned option grading'} for a in field[':answer-field/choices']]
 else:
  value=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==correct)
  alternate=f"{p['c']}+x*({p['a']}*x+({p['b']}))"
  checks=[{'submitted':value,'expected':'accepted','purpose':'canonical quadratic fragment'},
   {'submitted':alternate,'expected':'accepted','purpose':'genuine reordered Horner equivalent'},
   {'submitted':alternate+'+1','expected':'rejected','purpose':'wrong constant'},
   {'submitted':'-('+alternate+')','expected':'rejected','purpose':'outside sign error'}]
 return dict(label=label,record=record,checks=checks)

def main():
 immutable=REPO/'generate/runs/current/refresh-2026-10-14/sources/17592186054805.json'
 assert immutable.read_bytes()==(ROOT/'source.json').read_bytes()
 cases=[];review=[];engine=[];option_count=0;designation_count=0;source_solutions=0
 for name,p in g.ANCHORS.items():
  level=g.TEMPLATES[name]['level'];case=dict(source_id=name,template=name,parameters=p,bank_profile='observed_'+name,difficulty=level)
  cases.append(case);original=g.ORIGINALS[name];raw=g.generate(level,19,name,parameters=p,profile=case['bank_profile']);math_check(raw)
  q=raw['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in original)
  assert q[':question/problem']==original[':question/problem']
  if ':question/worked-solution' in original:assert q[':question/worked-solution']==original[':question/worked-solution'];source_solutions+=1
  if ':question/difficulty' in original:assert q[':question/difficulty']==original[':question/difficulty'][':db/ident']
  for source_field,field in zip(original.get(':question/answer-fields',[]),q.get(':question/answer-fields',[]),strict=True):
   assert field[':answer-field/key']==source_field[':answer-field/key'] and field[':answer-field/type']==source_field[':answer-field/type'][':db/ident']
   assert (':answer-field/correct' in field)==(':answer-field/correct' in source_field)
   # Stronger than algebra parity: exact answer-value bytes as unordered complete bank.
   assert sorted(a[':answer/value'] for a in field[':answer-field/choices'])==sorted(a[':answer/value'] for a in source_field[':answer-field/choices'])
   option_count+=len(field[':answer-field/choices'])
   if ':answer-field/correct' in source_field:
    expected=source_field[':answer-field/correct'][':answer/value'];actual=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert actual==expected;designation_count+=1
  review.append(raw)
  if ':question/answer-fields' in q and all(':answer-field/correct' in f for f in q[':question/answer-fields']):engine.append(engine_item(raw,name+' raw'))
  # Anchor normal (repairs/inferred fields/default banks), plus changed instances.
  normal=g.generate(level,19,name,parameters=p);math_check(normal);engine.append(engine_item(normal,name+' repaired anchor'));review.append(normal)
  for seed in range(12):
   normal=g.generate(level,seed,name);math_check(normal);engine.append(engine_item(normal,name+' variant '+str(seed)))
   if seed<2:review.append(normal)
  # Raw profile is also a parameterized recipe at non-anchor inputs.
  for seed in range(4):math_check(g.generate(level,seed,name,profile=case['bank_profile']))
 (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 # Default coverage and identity tests; aliases/order do not inflate task counts.
 defaults=[g.generate(l,s) for l in ('easy','moderate','hard') for s in range(60)]
 for record in defaults:math_check(record)
 assert set(r['generation']['template'] for r in defaults)==set(g.TEMPLATES)
 normal=g.generate('moderate',6,'q-75800');p=normal['generation']['parameters']
 replay=[g.generate('moderate',s,'q-75800',parameters=p) for s in range(10)]
 assert len({r['question'][':question/id'] for r in replay})==1
 assert len({r['generation']['parameter_fingerprint'] for r in replay})==1
 assert len({tuple(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']) for r in replay})>1
 # Stage mutation regressions: product, quotient divisor, sign extraction, prose conclusion/control.
 mutation_checks=0
 base=g.generate('hard',9,'q-328607');text=base['question'][':question/worked-solution']
 mutations=[text.replace('$↓$', '$999$',1),re.sub(r'(\\frac\{[^\n]+\}\{)x[^{}]+\}',r'\1x-99}',text,count=1),text.replace('=-(x','=(x',1),re.sub(r'(Finally, \$P\(x\)=)[^$]+',r'\g<1>x^{2}+999.',text),text+'\x0c']
 for changed in mutations:
  record=copy.deepcopy(base);record['question'][':question/worked-solution']=changed
  try:math_check(record)
  except (AssertionError,ValueError,TypeError):mutation_checks+=1
  else:raise AssertionError('Failed to reject stage mutation')
 # Invalid explicit parameter boundary calls never resample.
 for level,name,p in [('easy','q-112651',dict(r1=1,r2=2,a=1,b=0,c=1)),('moderate','q-75800',dict(r1=1,r2=2,a=1,b=4,c=1)),('hard','q-328607',dict(r1=8,r2=2,a=3,b=-1,c=5))]:
  try:g.generate(level,template=name,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit input accepted')
 # Enumerate meaningful mathematical tasks at declared workload. Swapped real factor
 # order is excluded; nonzero overall scaling is quotiented out via primitive polynomial.
 capacities={};slot_coverage={}
 for level in ('easy','moderate','hard'):
  tasks=set();roots_seen=set();coeff_seen=set();name={'easy':'q-112651','moderate':'q-270972','hard':'q-328607'}[level]
  for r1,r2 in itertools.combinations_with_replacement([i for i in range(-6,7) if i],2):
   for a,b,c in itertools.product(range(1,4),range(-4,5),range(1,10)):
    p=dict(r1=r1,r2=r2,a=a,b=b,c=c)
    try:g.validate_parameters(level,p,name)
    except ValueError:continue
    # Primitive quadratic excludes irrelevant common coefficient scale.
    divisor=sp.igcd(a,sp.igcd(b,c));task=(r1,r2,a//divisor,b//divisor,c//divisor)
    tasks.add(task);roots_seen.update((r1,r2));coeff_seen.add((a,b,c))
  capacities[level]=len(tasks);slot_coverage[level]={'roots':sorted(roots_seen),'distinct_quadratic_coefficients':len(coeff_seen)}
 (ROOT/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
 harness=REPO/'generate/runs/current/check-engine'
 subprocess.run([str(harness),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
 native=json.loads((ROOT/'engine-report.json').read_text())
 report={'status':'passed','database':'math','basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'source_questions':8,'raw_prompt_fidelity':8,'raw_full_solution_fidelity':source_solutions,'raw_complete_banks':7,'matched_source_options':option_count,'available_designations_matched':designation_count,'missing_designations_inferred_separately':2,'fieldless_sources':1,'source_math_errors_preserved_only_in_evidence':1,'source_format_repairs':['q-112651 wrong second division denominator','q-18852 p(x) vs f(x)','six historical underbrace marks','q-76184 missing answer field/placeholder'],'normal_checked':len(engine)-5+len(defaults),'raw_changed_parameter_checks':32,'mutation_regressions':mutation_checks,'meaningful_capacity_excluding_order_and_global_scalar':capacities,'slot_coverage':slot_coverage,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'script_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'native_binary_sha256':hashlib.sha256(harness.read_bytes()).hexdigest(),'parent_qa_required':True}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 out=['# Quartic factoring review','Raw evidence preserves missing labels/fields/keys and the known easy divisor typo. Normal anchor/variants use repaired solutions and authored method banks.']
 for record in review:out.append(g.markdown(record))
 (ROOT/'review.md').write_text('\n\n---\n\n'.join(out)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
