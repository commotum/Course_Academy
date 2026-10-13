#!/usr/bin/env python3
"""Independent printed-math/fidelity/identity/scope/native-grading QA."""
import importlib.util,json,re,sys,subprocess,random,collections,hashlib
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
x,u,h=s.symbols('x u h',real=True)

def group(text,i):
 assert text[i]=='{';depth=1;j=i+1
 while depth:
  if text[j]=='{':depth+=1
  if text[j]=='}':depth-=1
  j+=1
 return text[i+1:j-1],j

def convert(z):
 z=z.replace('⁡','').replace('′',"'")
 z=re.sub(r'\\operatorname\{(sin|cos)\}',r'\\\1',z)
 z=z.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 while r'\frac' in z:
  i=z.index(r'\frac');a,j=group(z,i+5);b,k=group(z,j);z=z[:i]+'(('+convert(a)+')/('+convert(b)+'))'+z[k:]
 z=z.replace(r'\sin','sin').replace(r'\cos','cos').replace(r'\exp','exp')
 # Function application without parentheses has exactly the source argument x.
 z=re.sub(r'(sin|cos)\s*x',r'\1(x)',z)
 z=z.replace('{','(').replace('}',')').replace('^','**').replace('e','E')
 # Protect function names from E substitution.
 z=z.replace('Exp','exp')
 return z

def read(z):
 z=z.strip().rstrip('.,')
 return parse_expr(convert(z),local_dict={'x':x,'u':u,'h':h,'E':s.E,'sin':s.sin,'cos':s.cos,'exp':s.exp},transformations=standard_transformations+(implicit_multiplication_application,))
def equal(a,b):return s.simplify(a-b)==0

def exp_arg(text):
 z=re.search(r'(?:\{e\}|e)\^\{',text)
 assert z,'No printed exponential'
 return group(text,z.end()-1)[0]

def check_format(text):
 assert text.count('$$')%2==0
 assert text.replace('$$','').count('$')%2==0
 # No bare positive coefficient concatenation is allowed in authored chains.
 assert '--' not in re.sub(r'\| --- \| --- \|','',text)
 depth=0
 for i,c in enumerate(text):
  if c in '{}':
   if i and text[i-1]=='\\':continue
   depth+=1 if c=='{' else -1
   assert depth>=0
 assert depth==0

def validate_record(r):
 q=r['question'];meta=r['generation'];template=meta['template'];kind='slope' if template=='two_power_slope' else m.SPECS[template][2]
 p={k:m.exact(v) for k,v in meta['parameters'].items()}
 prompt=q[':question/problem'];sol=q.get(':question/worked-solution','');check_format(prompt);check_format(sol)
 assert meta['authored_difficulty']==(template=='two_power_slope' or (template=='q-48628' and not meta['evidence_only']))
 if kind.startswith('trig'):
  if not meta['evidence_only']:
   assert 'Here $f(h)=' in prompt
   coeff=read(re.search(r'f\(h\)=(.*?)e\^h',prompt)[1]);G=read(re.search(r'h\(x\)=(.*?)\$',prompt)[1]);F=coeff*s.exp(G)
  else:G=p['a']*s.sin(x);F=p['scale']*s.exp(G) # underdetermined raw explicitly evidence-only
 else:
  G=read(exp_arg(prompt));F=s.exp(G)
 if not meta['evidence_only'] and not kind.startswith('trig'):
  printed=s.Poly(G,x)
  assert 2<=printed.degree()<=6 and 1<=abs(printed.LC())<=4
  if template=='two_power_slope':
   assert printed.degree() in (3,4) and printed.coeff_monomial(x**2)!=0 and printed.coeff_monomial(1)!=0
   assert all(abs(c)<=4 for c in printed.all_coeffs())
 if kind.startswith('trig'):
  supplied=read(exp_arg(prompt))
  assert equal(supplied,G if kind=='trig_product' else -G),'Supplied exponential fragment mismatch'
 D=s.diff(F,x)
 expected=D
 if kind=='slope':
  t=read(re.search(r'where \$x=(.*?)\.\$',prompt)[1]);expected=D.subs(x,t)
 if kind=='trig_product':expected=s.simplify(D/s.exp(G))
 if kind=='trig_quotient':expected=s.simplify(-D*s.exp(-G))
 f=q[':question/answer-fields'][0];values=[read(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len({s.srepr(s.simplify(v)) for v in values})==len(values)
 if ':answer-field/correct' in f:
  a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(read(a[':answer/value']),expected),(template,'answer',a[':answer/value'],expected)
 else:assert meta['evidence_only'] and template=='q-48628'
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt
 if kind.startswith('trig') and not meta['evidence_only']:
  assert not any(line.startswith('    ') for line in prompt.splitlines())
  assert '| --- |' not in prompt
  relation=prompt.split('\n\n')[-1]
  if kind=='trig_product':
   assert relation.startswith(r'$\frac{dy}{dx}=$') and '\n'+r'$\cdot e^{' in relation
  else:
   assert relation.startswith(r'$\frac{dy}{dx}=-($') and '\n$)/e^{' in relation
  correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  complete=relation.replace('{{'+f[':answer-field/key']+'}}','('+correct+')').replace('$','').replace('\n','')
  actual_complete_derivative=read(complete.split('=',1)[1])
  assert equal(actual_complete_derivative,D),'Actual supplied sign/factor/fragment relation is wrong'

 designation='missing' if ':answer-field/correct' not in f else next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 identity_valid=q[':question/id']==m.content_identity(prompt,sol,[a[':answer/value'] for a in f[':answer-field/choices']],q.get(':question/difficulty'),f[':answer-field/type'].split('/')[-1],f[':answer-field/key'],designation)
 if not sol:
  assert identity_valid
  return
 inner='h' if kind.startswith('trig') else 'u'
 # Read actual composition and derivative-component blocks in their order.
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
 definition=blocks[0];components=blocks[1]
 pieces=definition.split(r'\,');ig=read(pieces[-1].split('=',1)[1]);assert equal(ig,G)
 outer=read(pieces[0].split('=',1)[1]);scale=outer/s.exp(h if inner=='h' else u)
 assert equal(scale*s.exp(G),F)
 cp=components.split(r'\,');od=read(cp[0].split('=',1)[1]);id=read(cp[1].split('=',1)[1]);assert equal(od,outer);assert equal(id,s.diff(G,x)),(template,'component',id,s.diff(G,x))
 name='f' if 'd}f}' in components else 'y'
 refs={rf'\frac{{\text{{d}}{name}}}{{\text{{d}}{inner}}}': '('+s.sstr(outer)+')',rf'\frac{{\text{{d}}{inner}}}{{\text{{d}}x}}':'('+s.sstr(s.diff(G,x))+')'}
 rows=[]
 for block_index,block in enumerate(blocks[2:]):
  rawrows=block.split(r'\\')
  for row in rawrows:
   if '& =' not in row and '&=' not in row:continue
   rhs=re.split(r'&\s*=',row)[1].split(r'\end{aligned}')[0].strip().rstrip('.')
   for ref,value in refs.items():rhs=rhs.replace(ref,value)
   rhs=rhs.replace('exp(',r'\exp(') # parser converts exp safely
   rhs=re.sub(r'\|\}_\{x=.*?\}', '}',rhs)
   rhs=re.sub(r'\|_\{x=.*?\}', '',rhs)
   rhs=rhs.replace(r'\,','')
   parsed=read(rhs).subs({u:G,h:G})
   if block_index>0:parsed=parsed.subs(x,t)
   target=D if block_index==0 else expected
   assert equal(parsed,target),(template,'row',row,parsed,target)
   rows.append(row)
 # Preserve operative source stage skeleton under changed parameters.
 if template in m.SRC and ':question/worked-solution' in m.SRC[template]:
  src=m.SRC[template].get(':question/worked-solution','')
  assert len(re.findall(r'&\s*=',sol))==len(re.findall(r'&\s*=',src))
  assert sol.count('We now apply')==src.count('We now apply')
  assert sol.count('Finally,')==src.count('Finally,')
 assert identity_valid,'Content identity ignores displayed designation'
 assert set(r['knowledge_point'])=={'db_id','id','title'}

cases=[];replay=[];totalvals=0;designations=0
for k,(level,p,kind) in m.SPECS.items():
 case={'source_id':k,'template':k,'parameters':p,'bank_profile':'observed:'+k,'authored_level_for_unrated':level if k=='q-48628' else None};cases.append(case)
 r=m.generate(level,template=k,parameters=p,profile='observed:'+k);validate_record(r);replay.append(r)
 src=m.SRC[k];q=r['question'];assert q[':question/problem']==src[':question/problem']
 for attr in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (attr in q)==(attr in src)
 assert q.get(':question/worked-solution')==src.get(':question/worked-solution'),k
 sf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
 assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
 observed=[read(a[':answer/value']) for a in sf[':answer-field/choices']];actual=[read(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(observed)==len(actual)
 assert all(sum(equal(a,b) for b in actual)==1 for a in observed),k
 totalvals+=len(actual);designations+=(':answer-field/correct' in sf)
 if ':answer-field/correct' in sf:
  actualcorrect=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(read(sf[':answer-field/correct'][':answer/value']),read(actualcorrect[':answer/value']))
(ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
records=[];counts={};coverage=collections.Counter()
for level in m.NORMAL:
 fingerprints=set()
 for seed in range(120):
  r=m.generate(level,seed);validate_record(r);records.append(r);coverage[r['generation']['template']]+=1;fingerprints.add(r['generation']['mathematical_fingerprint'])
 counts[level]=len(fingerprints);assert len(fingerprints)>=70
# Every normal family exercised explicitly with multiple changed parameters.
for level,templates in m.NORMAL.items():
 for template in templates:
  assert coverage[template]>0
  for seed in (101,202):
   r=m.generate(level,seed,template=template);validate_record(r)
   r2=m.generate(level,seed+1,template=template,parameters=r['generation']['parameters']);validate_record(r2)
   assert r['question'][':question/id']==r2['question'][':question/id'];records.append(r)
# Fragment layout aliases retain separate presentation but one assessed derivative.
trig_params=dict(a=-4,scale='1/2')
trig_product=m.generate_moderate(template='q-167329',parameters=trig_params)
trig_quotient=m.generate_moderate(template='q-167783',parameters=trig_params)
assert trig_product['generation']['mathematical_fingerprint']==trig_quotient['generation']['mathematical_fingerprint']
assert trig_product['question'][':question/id']!=trig_quotient['question'][':question/id']
# Public observed changed parameters also run through identical family masks.
observed_variants=[]
for k,(level,anchor,kind) in m.SPECS.items():
 for delta in (1,2):
  p=dict(anchor)
  if kind.startswith('trig'):p['a']-=delta;p['scale']='1/3'
  else:p['a']+=delta if p['a']>0 else -delta
  r=m.generate(level,template=k,parameters=p,profile='observed:'+k);validate_record(r);records.append(r);observed_variants.append(r)
# Scope failures must reject public explicit parameters, including primitive support.
for level,template,p in [('easy','q-107445',dict(a=1,n=2,b=0,c=0)),('hard','two_power_slope',dict(a=1,n=3,b=0,m=2,c=1,t=2)),('hard','two_power_slope',dict(a=1,n=3,b=-1,m=2,c=1,t=1))]:
 try:m.generate(level,template=template,parameters=p)
 except ValueError:pass
 else:raise AssertionError('Scope bypass')
# Actual supplied sign/factor regressions are checked mathematically before ID.
for template,old,new in [('q-167329',r'$\cdot e^{',r'$/e^{'),('q-167783',r'=-(',r'=(')]:
 bad=m.generate_moderate(44,template=template)
 assert old in bad['question'][':question/problem']
 bad['question'][':question/problem']=bad['question'][':question/problem'].replace(old,new,1)
 try:validate_record(bad)
 except AssertionError:pass
 else:raise AssertionError('Supplied relation mutation accepted')
# Polynomial coefficients are integral; the captured rational point is separate.
try:m.generate('easy',template='q-1953',parameters=dict(a='1/2',n=2,b=0,c=0))
except ValueError:pass
else:raise AssertionError('Rational arithmetic bypass')
radio=m.generate('easy',5,template='q-1953')
for missing in (False,True):
 changed=json.loads(json.dumps(radio));f=changed['question'][':question/answer-fields'][0]
 if missing:del f[':answer-field/correct']
 else:f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])]
 designation='missing' if missing else next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 q=changed['question'];newid=m.content_identity(q[':question/problem'],q[':question/worked-solution'],[a[':answer/value'] for a in f[':answer-field/choices']],q[':question/difficulty'],'radio',f[':answer-field/key'],designation)
 assert newid!=radio['question'][':question/id'],'Correct-ref mutation aliases identity'
 try:validate_record(changed)
 except AssertionError:pass
 else:raise AssertionError('Incorrect/removed correct ref accepted')
# Meaningful mutation regressions: component derivative, intermediate row, prompt.
r=m.generate('hard',10)
for old,new in [('\\cdot (','\\cdot (2+'),('u=','u=1+'),('e^{','e^{1+')]:
 changed=json.loads(json.dumps(r));q=changed['question'];key=':question/problem' if old=='e^{' else ':question/worked-solution';assert old in q[key];q[key]=q[key].replace(old,new,1)
 try:validate_record(changed)
 except (AssertionError,ValueError,SyntaxError):pass
 else:raise AssertionError('Mutation undetected')
# Enumerate bounded meaningful parameter domains without counting syntax aliases,
# complete banks, ordering, source profile names or incidental function labels.
import itertools
domain_counts={};all_tasks=set()
for level,templates in m.NORMAL.items():
 tasks=set()
 for template in templates:
  if template=='two_power_slope':
   catalog=(dict(a=a,n=n,b=b,m=2,c=c,t=t) for a,n,b,c,t in itertools.product([-3,-2,-1,1,2,3],[3,4],[-3,-2,-1,1,2,3],[-4,-3,-2,-1,1,2,3,4],[-2,2]))
  else:
   _,anchor,kind=m.SPECS[template]
   if kind.startswith('trig'):
    for a,k in itertools.product([-2,-3,-4,-5,-6],['1/2','1/3','2/3']):tasks.add(('derivative_trig',a,k))
    continue
   catalog=(dict(a=a,n=n,b=b,c=c,**({'t':t} if kind=='slope' else {})) for a,n,b,c,t in itertools.product([-4,-3,-2,-1,1,2,3,4],[2,3,4,5,6],[-5,-4,-3,-2,-1,1,2,3,4,5] if anchor['b'] else [0],[-8,-6,-4,-2,-1,1,2,4,6,8] if anchor['c'] else [0],[-2,-1,1,2] if kind=='slope' else [None]))
  for p in catalog:
   kind='slope' if template=='two_power_slope' else m.SPECS[template][2]
   n=p['n'];a=p['a'];b=p['b'];c=p['c'];power=p.get('m',1)
   if kind=='slope':
    t=p['t'];w=a*t**n+b*t**power+c;v=a*n*t**(n-1)+b*power*t**(power-1)
    if abs(w)>40 or abs(v)>100 or v==0:continue
    if m.default_field(template)=='radio' and (w==0 or v in (-1,1)):continue
   else:t=None
   tasks.add((kind,tuple(sorted([(n,a)]+([(power,b)] if b else [])+([(0,c)] if c else []))),t))
 domain_counts[level]=len(tasks);all_tasks.update(tasks)
assert all(v>=100 for v in domain_counts.values())
# Real native grader: every source with original key plus every template default.
fixtures=[]
for i,r in enumerate(replay+records[-28:]+[m.generate(l,42,template=t) for l,ts in m.NORMAL.items() for t in ts]):
 f=r['question'][':question/answer-fields'][0]
 if ':answer-field/correct' not in f:continue
 checks=[];correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete bank ID grading'} for a in f[':answer-field/choices']]
 else:
  a=f[':answer-field/choices'][0][':answer/value'];v=read(a)
  checks=[{'submitted':a,'expected':'accepted','purpose':'canonical fragment'},{'submitted':m.latex(s.expand_mul(v)),'expected':'accepted','purpose':'expanded equivalent fragment'},{'submitted':'0','expected':'rejected','purpose':'incorrect fragment'}]
 if r['generation']['evidence_only'] and f[':answer-field/type'].endswith('/blank'):
  equivalents={
   'q-340948':r'-7e^2 e',
   'q-340955':r'-\frac{3}{e}',
   'q-167329':r'\frac{1}{2}(-4\cos x)',
   'q-167783':r'-\frac{1}{2}(-4\cos x)',
   'q-312451':r'e^{4x^5}(4\cdot 5x^4)',
   'q-340949':r'12e^3 e',
  }
  # These preserve unreduced chain factors/reciprocal exponent forms; they are
  # not an identity string generated by simplifying 2*answer/2.
  if r['generation']['parameters']=={k:str(v) for k,v in m.SPECS[r['generation']['template']][1].items()}:
   checks.append({'submitted':equivalents[r['generation']['template']],'expected':'accepted','purpose':'independently unreduced chain or exponent equivalent'})
 fixtures.append({'label':str(i)+'-'+r['generation']['template'],'record':r,'checks':checks})
(ROOT/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
subprocess.run(['generate/runs/current/check-engine',str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
review=[]
for level,templates in m.NORMAL.items():
 for t in templates:
  review.extend(m.generate(level,seed,template=t) for seed in (110,210))
review.extend(observed_variants)
(ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
parts=['# Source and generated review\nAll raw observed profiles are evidence-only; generated variants below are completed method banks.']
for r in replay:
 parts+=['\n## Original '+r['generation']['template'],m.markdown(r)]
 for v in review:
  if v['generation']['template']==r['generation']['template']:parts+=['\n### '+('Evidence-only observed-bank variant' if v['generation']['evidence_only'] else 'Generated normal variant'),m.markdown(v)]
parts+=['\n## Authored hard variants']+[m.markdown(r) for r in review if r['generation']['template']=='two_power_slope']
(ROOT/'review.md').write_text('\n\n'.join(parts)+'\n')
report={'generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'normal_presentation_repairs':['q-167329: remove incidental deep indentation and show an explicit exponential product after the coefficient widget.','q-167783: replace the ambiguous two-column table with an explicit leading-minus numerator widget divided by the positive exponential.'],'status':'pass','source_practices':14,'full_source_banks':14,'source_answer_values':totalvals,'matched_correct_designations':designations,'missing_source_designations':1,'raw_exact_prompts':14,'raw_exact_worked_solutions':13,'raw_omitted_solutions':1,'source_presence_parity':14,'changed_source_cases':28,'sampled_normal_records':360,'sampled_meaningful_task_counts':counts,'enumerated_meaningful_domain_counts':domain_counts,'enumerated_cross_level_task_union':len(all_tasks),'normal_family_coverage':dict(coverage),'native':json.loads((ROOT/'engine-report.json').read_text()),'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'limitations':['Unrated q-48628 has no captured key, solution or difficulty; completed normal key/solution/level are inferred/authored.','Raw q-167329/q-167783 omit f,h definitions; evidence-only, normal presentation completes them.','Opaque historical bank operations do not establish pedagogical intent; public observed replay is evidence-only.']}
(ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='native'},indent=2))
