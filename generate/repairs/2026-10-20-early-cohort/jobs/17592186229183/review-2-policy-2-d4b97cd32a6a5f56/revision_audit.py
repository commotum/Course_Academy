#!/usr/bin/env python3
"""Independent revision checks. Writes only adjacent evidence artifacts."""
import sys
sys.dont_write_bytecode=True
import json,importlib.util,hashlib,re,subprocess,shutil,platform
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,ROUND_HALF_UP
from collections import Counter
import sympy as S
R=Path(__file__).resolve().parent;J=R.parent;P=J/'workspace';REPO=Path('/home/jake/Developer/Course_Academy')
def load(p):return json.loads(Path(p).read_text())
def save(n,x): (R/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module(P/'17592186229183.py','revision_candidate')
def number(tex):
 f=re.search(r'\\frac\{(-?\d+)\}\{(\d+)\}',tex)
 return Fraction(int(f[1]),int(f[2])) if f else Fraction(re.search(r'-?\d+(?:\.\d+)?',tex)[0])
def inspect(r):
 q=r['question'];terms=re.findall(r'\$([^$]+)\$',q[':question/problem']);H,v,m,c,ri,ro=map(number,terms[:6]);n=ro/(ri-ro);assert n==2
 result=c*H+(m-c*v)*(v/H)**2
 expected=(Decimal(result.numerator)/Decimal(result.denominator)).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)
 f=q[':question/answer-fields'][0];a=f[':answer-field/choices'];key=f.get(':answer-field/correct');key=key.get(':answer/id') if isinstance(key,dict) else key[1] if key else None
 i=next((i for i,x in enumerate(a) if x[':answer/id']==key),None)
 values=list(map(lambda x:number(x[':answer/value']),a));mu=sum(values)/5
 return {'question_id':q[':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'parameters_from_prompt':dict(zip(['H','v','q','c','rin','rout'],[str(x) for x in [H,v,m,c,ri,ro]])),'exact_mass':str(result),'expected':str(expected),'correct':str(values[i]) if i is not None else None,'math_pass':i is None or values[i]==Fraction(expected),'rank':sorted(values).index(values[i])+1 if i is not None else None,'position':i+1 if i is not None else None,'nearest_mean':i is not None and abs(values[i]-mu)==min(abs(x-mu) for x in values),'ranks':['%.1f'%float(x) for x in sorted(values)]}
base={'H':'210','v':'90','q':'18','c':'0.5','rin':'18','rout':'12'}
# Changed relevant quantity must change actual response; common flow scale and context do not.
pairs=[g.generate('easy',seed=41077,template='q-336506',parameters=p) for p in [base,{**base,'H':'240'},{**base,'q':'30'},{**base,'rin':'9','rout':'6'}]]
pairs.append(g.generate('easy',seed=41077,template='q-336503',parameters=base))
pa=[inspect(x) for x in pairs];assert pa[0]['expected']!=pa[1]['expected'] and pa[0]['expected']!=pa[2]['expected'];assert pa[0]['expected']==pa[3]['expected']==pa[4]['expected']
save('counterfactual-records.json',pairs);save('counterfactual-results.json',{'command':sys.argv,'order':['base','capacity 210 to 240','initial mass 18 to 30','common flow halving','context coolant to fertilizer'],'results':pa,'relationships_pass':True})
# All five eligible numerical ranks at the exact earlier counterexample.
p={'H':'20','v':'10','q':'1','c':'0.4','rin':'6','rout':'4'}
controls=[g.generate('easy',seed=seed,template='q-336506',parameters=p) for seed in [41071,41072,41073,41076,41077]]
ca=[inspect(x) for x in controls];assert {x['rank'] for x in ca}=={1,2,3,4,5};assert all(x['expected']=='7.3' for x in ca)
save('rank-controlled-records.json',controls);save('rank-control-results.json',ca)
# Confirm complete source prompts, solutions, banks, key omissions and keys.
src=load(J/'source/source.json')['material']['kp'];replays=[];replay_rows=[]
for q in src[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];r=g.generate('easy',seed=11839,profile='observed:'+sid);rq=r['question'];replays.append(r)
 row={'source_uuid':q[':question/id'],'source_id':sid,'prompt_equal':rq[':question/problem']==q[':question/problem'],'solution_equal':rq.get(':question/worked-solution')==q.get(':question/worked-solution'),'fields_equal':len(q[':question/answer-fields'])==len(rq[':question/answer-fields']),'banks_and_keys_equal':True,'difficulty_presence_equal':(':question/difficulty' in q)==(':question/difficulty' in rq)}
 for sf,rf in zip(q[':question/answer-fields'],rq[':question/answer-fields']):
  banks=sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
  sc=sf.get(':answer-field/correct',{}).get(':answer/value');rc=next((a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf.get(':answer-field/correct',[None,None])[1]),None)
  row['banks_and_keys_equal'] &= banks and sc==rc
 assert all(v for k,v in row.items() if k not in ['source_uuid','source_id']),row
 replay_rows.append(row)
save('source-replay-records.json',replays);save('source-replay-results.json',{'cases':replay_rows,'pass':True,'source_omissions':'q-336499 has no key, solution or difficulty. Canonical has no bank. Source q-336451 editorial minerals/kg slips remain in raw evidence and are corrected in normal output.','lexical_note':'Use observed profile defaults to preserve source lexical forms. Rational explicit parameters such as 4/5 instead of 0.8 are mathematically equivalent but format differently.','canonical_evidence':'canonical-parameter-records.json retains independent model replay at original parameters; no canonical bank exists.'})
# Independent display-math check: parse source-derived final Q and compare to mass-balance solution.
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
T=S.Symbol('t',nonnegative=True)
def parse(z):
 def group(z,i):
  assert z[i]=='{'; depth=1;j=i+1
  while depth:depth+=(z[j]=='{')-(z[j]=='}');j+=1
  return z[i+1:j-1],j
 def frac(z):
  out='';i=0
  while i<len(z):
   if z.startswith(r'\frac',i):
    a,j=group(z,i+5);b,k=group(z,j);out+='(('+frac(a)+')/('+frac(b)+'))';i=k
   else:out+=z[i];i+=1
  return out
 z=z.split(r'\end{aligned}')[0].strip().rstrip('.')
 z=frac(z).replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace('^','**').replace('{','(').replace('}',')').replace(r'\,','')
 return parse_expr(z,local_dict={'t':T},transformations=standard_transformations+(implicit_multiplication_application,rationalize))
normal=load(R/'sample-records.json');batch=load(R/'delivery-batch/accepted.json');display=[]
for r in [normal[i*4] for i in range(len(g.MASKS))]+pairs+batch:
 row=inspect(r);p={k:S.Rational(v) for k,v in row['parameters_from_prompt'].items()};H,v,m,c,ri,ro=[p[k] for k in ['H','v','q','c','rin','rout']];V=v+(ri-ro)*T;Q=c*V+(m-c*v)*(v/V)**2
 sol=r['question'][':question/worked-solution'];blocks=sol.split('$$');assert len(blocks)==31
 # Identified from visible "Therefore ... expression for Q(t)" block, not metadata.
 solved=parse(blocks[25].split('& =')[-1]);residual=S.simplify(solved-Q);assert residual==0
 endpoint=blocks[29];mass=number(re.search(r'[≈=]([\d.]+)\\,',endpoint)[1]);assert mass==Fraction(row['expected'])
 assert '<<' not in sol and all(f'**Step {i}**' in sol for i in range(1,5))
 display.append({'id':row['question_id'],'template':row['template'],'solved_expression':str(solved),'independent_expression_residual':str(residual),'endpoint_mass':str(mass),'pass':True})
save('displayed-math-results.json',display)
# Real native learner responses: every radio choice, controlled dependency pairs.
cases=[]
for i,r in enumerate(batch+pairs+controls+[normal[i*4] for i in range(len(g.MASKS))]):
 row=inspect(r);assert row['math_pass'];f=r['question'][':question/answer-fields'][0]
 cases.append({'label':f'independently computed mass / delivered or controlled {i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if number(a[':answer/value'])==Fraction(row['expected']) else 'rejected','purpose':'Prompt-derived exact mass; every displayed alternative tested'} for a in f[':answer-field/choices']]})
save('grader-input.json',cases);save('render-records.json',batch+pairs+controls[:1]+[normal[i*4] for i in range(len(g.MASKS))])
save('scope-results.json',{'sample_count':len(normal),'all_easy':all(r['question'][':question/difficulty']==':question.difficulty/easy' and Fraction(r['generation']['parameters']['rout'])/(Fraction(r['generation']['parameters']['rin'])-Fraction(r['generation']['parameters']['rout']))==2 for r in normal),'source_method_preserved':'Same source mass-balance, quadratic integrating factor, initial condition, overflow endpoint and one five-choice mass response. New banks replace mistake-derived offsets with nearby numerical offsets, without new learner operations.','authored_completion':'q-336499 lacks solution/key in observed evidence; normal generated completion uses independently validated source-equivalent four-step method.','limits':'Requested easy is reviewed. Retained moderate/hard authored entrypoints are not re-certified by this targeted easy review.'})
print(json.dumps({'displayed_solution_checks':len(display),'native_cases':len(cases),'controlled_ranks':[x['rank'] for x in ca],'counterfactual_masses':[x['expected'] for x in pa]}))
