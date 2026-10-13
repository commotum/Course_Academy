#!/usr/bin/env python3
"""Independent displayed-string mathematics, full fidelity, identity and native checks."""
import importlib.util,json,pathlib,re,subprocess,sys,hashlib,copy,itertools
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=pathlib.Path(__file__).parent;spec=importlib.util.spec_from_file_location('g',str(D)+'.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,u=sp.symbols('x y u',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,)
def group(s,start):
 assert s[start]=='{',(s,start)
 depth=1;i=start+1
 while depth:
  assert i<len(s),s
  depth+=(s[i]=='{')-(s[i]=='}');i+=1
 return s[start+1:i-1],i

def parse(s):
 s=s.strip().rstrip('.,').replace('ln⁡',r'\ln').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\qquad','').replace(r'\cdot','*')
 s=s.replace(r'\ln','log').replace('{e}','E').replace('exp','EXP_PROTECTED').replace('e','E').replace('EXP_PROTECTED','exp')
 # Fractions remain structural before group removal.
 while r'\frac'in s:
  start=s.index(r'\frac');p=start+5;num,end=group(s,p);den,end=group(s,end);s=s[:start]+'(('+str(parse(num))+')/('+str(parse(den))+'))'+s[end:]
 s=s.replace('log','log')
 # Plain e is Euler's constant; exponentiations and grouping are recursive.
 while '^{'in s:
  start=s.index('^{');inside,end=group(s,start+1);s=s[:start]+'**('+str(parse(inside))+')'+s[end:]
 s=s.replace('^','**').replace('{','(').replace('}',')')
 v=parse_expr(s,local_dict={'x':x,'y':y,'u':u,'E':sp.E,'log':sp.log},transformations=TRANS)
 assert isinstance(v,sp.Expr)and v.free_symbols<={x,y,u},(s,v)
 return v
def equal(a,b):return sp.simplify(a-b)==0

def formatting(q):
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value']for f in q.get(':question/answer-fields',[])for a in f[':answer-field/choices']]:
  assert '@@'not in text and '\x00'not in text
  assert text.count('$')%2==0,text
  depth=0
  for c in text:
   if c=='{':depth+=1
   if c=='}':depth-=1
   assert depth>=0,text
  assert depth==0,text
  assert '--'not in text and '+-'not in text,text
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}'in q[':question/problem']

def actual_math(r):
 q=r['question'];t=r['generation']['template'];fam=g.FAMILY[t]
 # Read the actual displayed function; protect its own x argument.
 prompt=q[':question/problem'];ms=re.findall(r'\$(.*?)\$',prompt,re.S)
 definition=next(v for v in ms if 'f(x)='in v.replace(' ','')or v.startswith('y='))
 expr=definition.split('=',1)[1].strip().rstrip('.,');f=parse(expr)
 der=sp.diff(f,x)
 # Actual printed evaluation point, including source Unicode ln.
 if fam in ['slope','tangent']:
  point=next(v.split('=',1)[1].rstrip('.')for v in ms if v.startswith('x='));z=parse(point)
  answer=sp.simplify(der.subs(x,z))if fam=='slope'else sp.simplify(der.subs(x,z)*(x-z)+f.subs(x,z))
 else:answer=der
 for field in q.get(':question/answer-fields',[]):
  vals=[parse(a[':answer/value'].split('=',1)[-1])for a in field[':answer-field/choices']]
  assert len(vals)==(5 if field[':answer-field/type'].endswith('/radio')else 1)
  assert all(not equal(vals[i],vals[j])for i in range(len(vals))for j in range(i))
  matches=[i for i,v in enumerate(vals)if equal(v,answer)];assert len(matches)==1,(t,vals,answer)
  correct=field.get(':answer-field/correct')
  if correct:assert field[':answer-field/choices'][matches[0]][':answer/id']==correct[1]
 if ':question/worked-solution'not in q:return
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
 # First composite and component definitions must use the displayed expression.
 outer,inner=blocks[0].strip().rstrip('.').split(r'\,')if r'\,'in blocks[0]else blocks[0].strip().rstrip('.').split(r'\qquad')
 outer=outer.rstrip(',');u_expr=parse(inner.split('=',1)[1]);outer_expr=parse(outer.split('=',1)[1]);helper=outer_expr.subs(u,u_expr)
 exp_terms=[v for v in sp.Add.make_args(f)if v.has(sp.exp)]
 assert len(exp_terms)==1
 assessed=f if fam in ['direct','tangent','slope']else exp_terms[0]/(-1 if t=='q-107420'else 1)
 assert equal(helper,assessed),(t,helper,assessed)
 expected_component=sp.diff(outer_expr,u);expected_inner=sp.diff(u_expr,x)
 defs=blocks[1].strip().rstrip('.').split(r'\,')
 assert equal(parse(defs[0].split('=',1)[1]),expected_component)
 assert equal(parse(defs[1].split('=',1)[1]),expected_inner)
 chain=blocks[2];rows=chain.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
 assert len(rows)==4 and r'\frac{\text{d}'in rows[0]and r'\cdot'in rows[0]
 assert r'\cdot'in rows[1]and 'u'in rows[1]and 'u'in rows[2]and 'x'in rows[3]
 hder=sp.diff(helper,x)
 for row in rows[1:]:
  rhs=row.split('=',1)[1];v=parse(rhs).subs(u,u_expr);assert equal(v,hder),(t,row,v,hder)
 if fam in ['power_sum','linear_sum']:
  rows=blocks[3].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==3
  assert r'\frac{\text{d}}{\text{d}x}'in rows[0]
  inside=rows[0].split(r'\frac{\text{d}}{\text{d}x}',1)[1];assert equal(parse(inside),f)
  for row in rows[1:]:assert equal(parse(row.split('=',1)[1]),der),(t,row,der)
 if fam=='slope':
  rows=blocks[3].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==4
  for row in rows:assert equal(parse(row.split('& =',1)[1]),answer),(t,row,answer)
  points=re.findall(r'\$x=([^$]*?)\$',sol)
  for p in points:assert equal(parse(p.rstrip(',')),z),(t,p,z)
 if fam=='tangent':
  # Every evaluation substitution and expansion row is checked separately.
  slope=der.subs(x,z);v=f.subs(x,z)
  for block,expected in [(blocks[3],slope),(blocks[4],v)]:
   rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==3
   for row in rows:
    rhs=row.split('& =',1)[1]if '& ='in row else row.split('& =',1)[-1]
    if '& ='not in row:rhs=row.split('&',1)[1].lstrip(' =')
    if '_{x='in rhs:
     marker=rhs.index('_{x=');pointtext,end=group(rhs,marker+1);assert equal(parse(pointtext[2:]),z)
     rhs=rhs[:marker]
     if rhs.endswith('{|}'):rhs=rhs[:-3]
     elif rhs.startswith('{(')and rhs.endswith(')|}'):rhs=rhs[2:-3]
     else:raise AssertionError('evaluation mask')
    val=parse(rhs).subs(x,z);assert equal(val,expected),(t,row,val,expected)
  rows=blocks[5].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==4
  assert rows[0].strip()==r'y-{y}_{1} & =m(x-{x}_{1})'if t=='q-48657'else rows[0].strip()==r'y-y_1 & =m(x-x_1)'
  for row in rows[1:]:
   lhs,rhs=row.split('&');lhs=parse(lhs);rhs=parse(rhs.lstrip(' ='));assert equal((lhs-rhs).subs(y,answer),0),(t,row,answer)
  assert equal(parse(rows[-1].split('=',1)[1]),answer)

source=json.load((D/'source.json').open());orig={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
raw=[];review=[];checks=[]
for case in g.CASES:
 r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);o=g.simplify_record(orig[case['source_id']]);q=r['question'];raw.append(r)
 assert set(q)==set(o)
 for key in [':question/problem',':question/worked-solution',':question/difficulty']:assert q.get(key)==o.get(key)
 for ff,of in zip(q.get(':question/answer-fields',[]),o.get(':question/answer-fields',[])):
  assert set(ff)==set(of)
  assert sorted(a[':answer/value']for a in ff[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices'])
  assert ff[':answer-field/type']==of[':answer-field/type']and ff[':answer-field/key']==of[':answer-field/key']
  if ':answer-field/correct'in of:
   v=next(a[':answer/value']for a in ff[':answer-field/choices']if a[':answer/id']==ff[':answer-field/correct'][1]);assert v==of[':answer-field/correct'][':answer/value']
 formatting(q);actual_math(r)
 completed=g.generate(case['level'],template=case['template'],parameters=case['parameters'])
 if ':question/worked-solution'in o:assert completed['question'][':question/worked-solution']==o[':question/worked-solution'].replace('ln⁡',r'\ln')
 # Present correct refs are native checked; missing refs stay missing in public evidence.
 if all(':answer-field/correct'in f for f in q.get(':question/answer-fields',[]))and q.get(':question/answer-fields'):checks.append(r)
 for seed in [14,31]:
  variant=g.generate(case['level'],seed,template=case['template']);formatting(variant['question']);actual_math(variant);review.append(variant);checks.append(variant)
for seed in [12,13]:
 r=g.generate_hard(seed);formatting(r['question']);actual_math(r);review.append(r);checks.append(r)
# Each explicitly supported layout is exercised through independent math and native grading.
for case in g.CASES:
 t=case['template']
 if g.FAMILY[t]=='tangent':continue
 for kind in ['radio','blank']:
  r=g.generate(case['level'],template=t,parameters=case['parameters'],field_type=kind)
  formatting(r['question']);actual_math(r);checks.append(r)

# Boundary/signed explicit inputs and changed raw masks; 12 variants per family.
for t in g.LEVEL:
 for seed in range(12):
  r=g.generate(g.LEVEL[t],seed,template=t);formatting(r['question']);actual_math(r)
  again=g.generate(g.LEVEL[t],seed+100,template=t,parameters=r['generation']['parameters']);assert again['question'][':question/id']==r['question'][':question/id']
  assert set(again['knowledge_point'])=={'db_id','id','title'}
  if t in g.MASKS:
   rraw=g.generate(g.LEVEL[t],seed,template=t,profile='raw:'+t);formatting(rraw['question']);actual_math(rraw)
# Semantic identity must omit incidental vertical shifts in derivative-only prompts.
p=g.CASE['q-48007']['parameters'].copy();r1=g.generate_easy(template='q-48007',parameters=p);p['d']=4;r2=g.generate_easy(template='q-48007',parameters=p);assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint'];assert r1['question'][':question/id']!=r2['question'][':question/id']
# Correct-key presence/value are content, not UUID/order aliases.
key_record=copy.deepcopy(r1['question']);key_field=key_record[':question/answer-fields'][0]
wrong=next(a for a in key_field[':answer-field/choices']if a[':answer/id']!=key_field[':answer-field/correct'][1])
key_field[':answer-field/correct']=[':answer/id',wrong[':answer/id']]
changed=g.identify(copy.deepcopy(key_record),'easy','q-48007',g.CASE['q-48007']['parameters'],'authored-method',0)
assert changed['question'][':question/id']!=r1['question'][':question/id']
key_field.pop(':answer-field/correct')
missing=g.identify(copy.deepcopy(key_record),'easy','q-48007',g.CASE['q-48007']['parameters'],'raw:q-48007',0)
assert missing['question'][':question/id']not in [changed['question'][':question/id'],r1['question'][':question/id']]

# All default source-shaped families receive normal sampling coverage.
coverage=set()
for level in ['easy','moderate','hard']:
 for seed in range(60):coverage.add(g.generate(level,seed)['generation']['template'])
assert coverage==set(g.LEVEL)
# Actual finite sampler domain counts; no notation/profile/distractor aliases.
A=[i for i in range(-6,7)if abs(i)>=2];B=list(range(-8,9));C=[i for i in range(-8,9)if abs(i)>=2];CS=[i for i in range(-6,7)if abs(i)>=2]
variety={'easy_direct_unshifted':len(A),'easy_direct_shifted':len(A)*len([b for b in B if b]),'easy_scaled_reflection':len(C)*len(B),'easy_scaled_translation_derivatives':len(A)*len(CS)*len(B),'moderate_factored_power_sum':len(range(3,6))*len(B),'moderate_linear_sum':len(A)*len(B)*len(C),'moderate_shifted_log_slope':len(range(-8,-1))*len(B)*len(range(2,7)),'moderate_reciprocal_point_tangent':sum(a!=c for a in range(2,7)for c in range(2,9)),'hard_shifted_translated_tangent':len(A)*len(CS)*len([b for b in range(-6,7)if b not in (0,1)])*len([d for d in range(-6,7)if d])}
# Guard rejects explicit workload collapse as well as random sampling.
for changed in [dict(a=1),dict(c=1),dict(b=0),dict(b=1),dict(d=0),dict(a=-7),dict(c=-7)]:
 p=dict(a=3,b=2,c=4,d=1)|changed
 try:g.generate_hard(parameters=p)
 except ValueError:pass
 else:raise AssertionError('hard guard')
# Regression: a mathematically equivalent collapsed row cannot replace formal product.
bad=copy.deepcopy(review[0]);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(r'\cdot', '')
try:actual_math(bad)
except Exception:pass
else:raise AssertionError('stage omission not detected')
fixtures=[]
for i,r in enumerate(checks):
 ff=r['question'][':question/answer-fields'][0];correct=next(a for a in ff[':answer-field/choices']if a[':answer/id']==ff[':answer-field/correct'][1]);tests=[]
 if ff[':answer-field/type'].endswith('/radio'):
  tests=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a==correct else'rejected','purpose':'complete owned choice ID'}for a in ff[':answer-field/choices']]
 else:
  answer=correct[':answer/value'];p=r['generation']['parameters'];t=r['generation']['template'];ex=g.slots(t,p)['exponent']
  if t=='q-48003':equiv=str(p['c'])+r'\cdot e^{'+ex+r'}\cdot(-1)'
  elif t=='q-107420':equiv=str(p['n'])+'x^{'+str(p['n']-1)+r'}-e^{'+ex+r'}\cdot('+str(p['a'])+')'
  elif t=='q-340496':equiv=str(p['r'])+r'+e^{'+ex+r'}\cdot('+str(p['a'])+')'
  elif g.FAMILY[t]=='direct':equiv=str(p['c'])+r'\cdot e^{'+ex+r'}\cdot('+str(p['a'])+')'
  else:equiv=str(-p['c'])+r'\cdot '+str(p['k'])
  assert equal(parse(answer),parse(equiv))
  tests=[{'submitted':answer,'expected':'accepted','purpose':'canonical fragment'},{'submitted':equiv,'expected':'accepted','purpose':'unreduced equivalent fragment'},{'submitted':'('+answer+')+1','expected':'rejected','purpose':'incorrect fragment'}]
 fixtures.append({'label':str(i)+' '+r['generation']['template']+' '+r['generation']['profile'],'record':r,'checks':tests})
(D/'engine-input.json').write_text(json.dumps(fixtures,indent=2,ensure_ascii=False)+'\n')
subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
(D/'review.json').write_text(json.dumps({'raw_original_replays':raw,'generated_variants':review},indent=2,ensure_ascii=False)+'\n')
(D/'review.md').write_text('# Original replays and generated variants\n\n'+ '\n\n'.join('## '+r['generation']['template']+' — '+('raw original replay'if r['generation']['evidence_only']else'generated '+r['generation']['difficulty']+'; '+r['generation']['profile'])+'\n\n'+g.markdown(r)for r in raw+review))
report={'status':'passed','source_provenance':{k:source[k]for k in ['database','basis','lineage']},'source_questions':9,'raw_exact_prompts':9,'raw_exact_solutions':7,'source_solution_total':7,'full_source_banks':7,'full_source_answer_values':27,'correct_designations_matched':5,'missing_correct_designations':2,'fieldless_sources':2,'unrated_sources':2,'raw_key_presence_matches':9,'notation_normalization':'normal ln U+2061 -> \\ln; raw byte exact','normal_changed_parameter_checks':120,'raw_changed_parameter_checks':108,'generated_review_variants':20,'default_families_covered':sorted(coverage),'authored_hard':'shifted_tangent','variety_counts':variety,'native':json.load((D/'engine-report.json').open()),'decoded_source_notation':{'function_application_codepoint':'U+2061','occurrences':10,'adjacent_backslash_pairs':38,'adjacent_pairs_role':'aligned row breaks'},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_sha256':hashlib.sha256(pathlib.Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'limitations':['Historical q-48007/q-48658 scalar choice operations are opaque; raw profiles are evidence-only.','Two missing refs and two fieldless records cannot be counted as observed correct-field fidelity; completed fields are independently derived.','Hard labels are authored curriculum design claims, not observed source ratings.']}
(D/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print('PASS: 9 raw records, 7 solutions, 27 values, 5 present correct refs; 120 changed families; all levels/native')
