#!/usr/bin/env python3
"""Nonresonant exponential particular solutions; captured math basis 8743.

One, two, or three independent coefficients, with complete imported source
replay. All fields request the RHS of the particular solution in the forcing
exponential span. No database, assets, or sibling resonance methods.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from math import comb
from math_format import normalize_prose, normalize_tex, validate_generated_record
import sympy as sp
KP_ID=17592186229162
KP_UUID='42bcc7e2-88f7-5ef9-8c51-77c1e2c8e8af'
TITLE='Finding a Particular Solution to a First-Order Inhomogeneous ODE With Exponential Forcing'
VERSION='nonresonant-exponential-2'
SOURCE={'database':'math','basis':8743,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={'single':'easy','two_and':'moderate','two_comma':'moderate','two_doublecomma':'moderate','two_hard':'hard','three':'hard'}
CASES=[
 ('q-332644','single',{'a':3,'b':-6,'k':[4],'c':[9]}),
 ('q-332655','single',{'a':5,'b':-20,'k':[-1],'c':[15]}),
 ('q-332659','single',{'a':6,'b':-18,'k':[-2],'c':[24]}),
 ('q-332664','single',{'a':7,'b':14,'k':[-5],'c':[21]}),
 ('q-332667','two_hard',{'a':4,'b':8,'k':[2,3],'c':[5,3]}),
 ('q-332668','two_and',{'a':3,'b':9,'k':[1,4],'c':[7,4]}),
 ('q-332669','two_comma',{'a':1,'b':3,'k':[2,5],'c':[2,1]}),
 ('q-332670','two_doublecomma',{'a':2,'b':-6,'k':[1,2],'c':[3,-2]})]
SOURCE_IDS=dict(zip([c[0] for c in CASES], [
 'b0a6279e-623c-5e5d-bfce-194a9b63b40e','6e8b85e6-cf06-5623-ab71-a62bf6c263eb',
 'f2ab75a0-6cd5-582d-bf4b-82f239086002','81fa1809-9925-54c1-9732-91934088476a',
 '1545356e-4e65-553c-8118-fc733c23efcc','2ded7c26-5423-5b6f-b536-de9fa660d3cd',
 '6adfa911-36fb-57ce-b523-2914b62bca69','945e99ed-3594-5be0-95b2-a2681c44f43f']))
PROFILES={q:{'template':t,'parameters':p,'raw':True} for q,t,p in CASES}
OPENING='To find the general solution of an inhomogeneous first-order linear equation with constant coefficients on the left-hand side, we must find the sum of the complementary and particular solutions.'
def exp(k): return '{e}^{'+coef(k)+'x}'
def coef(v):
 v=sp.Rational(v)
 if v==1:return ''
 if v==-1:return '-'
 return sp.latex(v).replace("- ","-")
def term(v,f):return coef(v)+f
def summ(parts):return ''.join(('+' if i and not v.startswith('-') else '')+v for i,v in enumerate(parts))
def signed(v,f):return ('+' if v>=0 else '-')+term(abs(v),f)
def block(s):return '$$\n'+s+'\n$$'
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def validate_parameters(level,t,p,raw=False):
 if set(p)!= {'a','b','k','c'}:raise ValueError('Expected a,b,k,c only')
 if not all(type(v) is int for v in [p['a'],p['b'],*p['k'],*p['c']]):raise ValueError('Integer coefficients only')
 a,b,k,c=p['a'],p['b'],p['k'],p['c']; n=1 if t=='single' else 3 if t=='three' else 2
 if len(k)!=n or len(c)!=n or len(set(k))!=n:raise ValueError('Distinct exponential terms required')
 if a<=0 or b==0 or any(v==0 for v in [*k,*c]) or any(a*v+b==0 for v in k):raise ValueError('Nonzero, nonresonant terms required; resonance belongs to sibling KP29163')
 if not raw:
  if not 1<=a<=4 or abs(b)>16 or any(abs(v)>5 for v in k) or any(abs(v)>12 for v in c):raise ValueError('Comparable source workload bounds violated')
  if b%a:raise ValueError('Integer complementary exponent required')

def sample(level,t,rng):
 n=1 if t=='single' else 3 if t=='three' else 2
 # Choose answer-bearing denominator signs and forcing signs before magnitudes.
 r=rng.choice([-3,-2,-1,1,2,3]); available=[v for v in range(-5,6) if v and v!=-r]
 k=[];c=[]
 for i in range(n):
  sign=rng.choice([-1,1]); pool=[v for v in available if v not in k and (v+r)*sign>0]
  if not pool:pool=[v for v in available if v not in k]
  k.append(rng.choice(pool)); c.append(rng.choice([-1,1])*rng.randint(1,6))
 a=rng.randint(1,3)
 p={'a':a,'b':a*r,'k':k,'c':c}
 validate_parameters(level,t,p)
 return p

def render(p,t,raw):
 a,b,k,c=p['a'],p['b'],p['k'],p['c']; es=[exp(v) for v in k]; n=len(k)
 syms=[r'\alpha ',r'\beta ',r'\gamma '][:n]; den=[a*v+b for v in k]; ans=[sp.Rational(v,d) for v,d in zip(c,den)]
 forcing=summ([term(v,e) for v,e in zip(c,es)])
 trial=summ([s+e for s,e in zip(syms,es)]); derivative=summ([term(v,s+e) for v,s,e in zip(k,syms,es)])
 answer=summ([term(v,e) for v,e in zip(ans,es)])
 equation=term(a,r'\frac{\text{d}y}{\text{d}x}')+signed(b,'y')+'='+forcing
 prompt='Given that the differential equation \n\n'+block(equation)+'\n\nhas the complementary solution ${y}_{c}(x)=A'+exp(sp.Rational(-b,a))+'$, find the particular solution ${y}_{p}(x)$ to this equation.\n\n${y}_{p}(x)=$\n{{field-1}}'
 if n==1:
  suffix=' and $'+es[0]+'$ is not a term in the complementary solution'
  constants='where $\\alpha $ is a constant that is to be determined.'
  substitute='To find the value of $\\alpha ,$'
  distributed='('+str(a*k[0])+('+' if b>0 else '-')+str(abs(b))+')'+syms[0]+es[0]
  rows=[term(a,'('+derivative+')')+signed(b,'('+trial+')'),distributed,term(den[0],syms[0]+es[0])]
  aligned=' \\\\ '.join(v+' & ='+forcing for v in rows)+r' \\ \alpha  & ='+sp.latex(ans[0]).replace("- ","-")
 elif n==2:
  suffix=' and neither $'+es[0]+'$ nor $'+es[1]+'$ is a term in the complementary solution'
  constants='where $\\alpha $ and $\\beta $ are constants that are to be determined.'
  substitute='To find the values of $\\alpha $ and $\\beta ,$'
  distributed=summ(['('+term(a*v,s)+signed(b,s)+')'+e for v,s,e in zip(k,syms,es)])
  rows=[term(a,'('+derivative+')')+signed(b,'('+trial+')'),distributed,summ([term(d,s+e) for d,s,e in zip(den,syms,es)])]
  aligned=' \\\\ '.join(v+' & ='+forcing for v in rows)+('.' if t=='two_comma' else '')
 else:
  suffix=' and none of these exponentials occurs in the complementary solution'
  constants='where $\\alpha$, $\\beta$ and $\\gamma$ are constants to be determined.'
  substitute='To find these constants,'
  distributed=summ(['('+term(a*v,z)+signed(b,z)+')'+e for v,z,e in zip(k,syms,es)])
  rows=[term(a,'('+derivative+')')+signed(b,'('+trial+')'),distributed,summ([term(d,z+e) for d,z,e in zip(den,syms,es)])]
  aligned=r' \\ '.join(v+' & ='+forcing for v in rows)
 if not raw:
  # Display the substitution for each independent exponential on its own row.
  # Keeping the entire sum on both sides overflows the learner's solution card.
  aligned=r' \\ '.join('('+term(a,'('+term(v,z)+')')+signed(b,z)+')'+e+' &= '+term(cj,e)
                         for v,z,e,cj in zip(k,syms,es,c))
 solution=OPENING+'\n\nWe see that the right-hand side is $'+forcing+',$'+suffix+', so we assume a particular solution of the form\n\n'+block('{y}_{p}='+trial+',')+'\n\n'+constants+'\n\nCalculating the first derivative of ${y}_{p}$ gives\n\n'+block(r'\frac{\text{d}{y}_{p}}{\text{d}x}='+derivative+('.' if n==2 else ''))+'\n\n'+substitute+' we substitute ${y}_{p}$ and ${y}_{p}^{′}$ into the differential equation:\n\n'+block(r'\begin{aligned}'+aligned+r'\end{aligned}')
 if n>=2:
  sep={'two_and':r'\,\text{and}\,','two_comma':r',\,','two_doublecomma':r',\,\,','two_hard':r',\,\,','three':r',\quad '}[t]
  solved=sep.join(s+'='+sp.latex(v).replace("- ","-") for s,v in zip(syms,ans))
  coeff=sep.join(term(d,s)+'='+str(v) for d,s,v in zip(den,syms,c))
  solution+='\n\nEquating coefficients of '+', '.join('$'+e+'$' for e in es)+', respectively, gives\n\n'+block(coeff+(',' if t=='two_and' else '.'))+'\n\nSo, we have\n\n'+block(solved+'.')
 solution+='\n\nTherefore, the particular solution ${y}_{p}(x)$ is\n\n'+block('{y}_{p}(x)='+answer+'.')
 if not raw:
  solution=solution.replace('into the differential equation:', 'into the differential equation and group each exponential separately:')
  division=r' \\ '.join(z+' &= '+r'\frac{'+str(v)+'}{'+str(d)+'} = '+sp.latex(q).replace('- ','-') for z,v,d,q in zip(syms,c,den,ans))
  marker='\n\nTherefore, the particular solution'
  solution=solution.replace(marker,'\n\nSolving each coefficient equation gives\n\n'+block(r'\begin{aligned}'+division+r'\end{aligned}')+marker)
 if not raw:prompt=prompt.replace('to this equation.','to this equation. Express your answer using only the exponentials in the forcing term.')
 prompt=normalize_prose(prompt)
 if solution:solution=normalize_prose(solution)
 bankanswer=normalize_tex(answer)
 return prompt,solution,bankanswer

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard') or field_type not in (None,'blank'):raise ValueError('Unsupported level/field')
 raw=False
 if profile:
  if profile not in PROFILES:raise ValueError('Unknown observed profile')
  spec=PROFILES[profile]; raw=True
  if template and template!=spec['template']:raise ValueError('Profile/template mismatch')
  template=spec['template'];parameters=parameters or spec['parameters']
 eligible=[t for t,l in TEMPLATES.items() if l==level]
 if template and template not in eligible:raise ValueError('Template/level mismatch')
 rng=random.Random(seed);t=template or {'easy':'single','moderate':'two_and','hard':'three'}[level]
 p=json.loads(json.dumps(parameters)) if parameters is not None else sample(level,t,rng)
 validate_parameters(level,t,p,raw)
 prompt,solution,answer=render(p,t,raw)
 missing=False; q={':question/problem':prompt}
 if not missing:q[':question/difficulty']=':question.difficulty/'+level;q[':question/worked-solution']=solution
 # Equation normalized by leading a, with ordered terms sorted: common scaling
 # and term permutation do not count as new mathematical tasks.
 task=[str(sp.Rational(p['b'],p['a'])),sorted((v,str(sp.Rational(c,p['a']))) for v,c in zip(p['k'],p['c']))]
 fingerprint=sha(task); content=sha([VERSION,q,answer if not missing else None,'blank'])
 qid=uid('q:'+content);fid=uid('f:'+content);aid=uid('a:'+content+answer)
 field={':answer-field/id':fid,':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank'}
 if not missing:field.update({':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':answer}],':answer-field/correct':[':answer/id',aid]})
 q.update({':question/id':qid,':question/answer-fields':[field]})
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'parameters':p,'bank_profile':profile,'raw_evidence':raw,'parameter_fingerprint':fingerprint,'content_fingerprint':content,'source_analysis':SOURCE,'source_ids':[SOURCE_IDS[profile]] if profile else ([SOURCE_IDS[v] for v,u,w in CASES if u==t] if t!='three' else ['5e56989a-feb1-590a-8684-9442dee1b1cb','e0e14ce3-61de-571e-b34e-f56630cc2fe9']),'plot_rating':'none','authored_extension':not raw,'presentation_repairs':[] if raw else ['clarify the required trial-form fragment'],'sympy_version':sp.__version__}}
 return validate_generated_record(record)
# EASY: construct one coefficient.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: two independent nonresonant trials; a1..3, signed exponents/forcing.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored third nonresonant coefficient; source two-term replay retained.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question']; f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\nAnswer: $'+(f.get(':answer-field/choices') or [{':answer/value':'[missing in original]'}])[0][':answer/value']+'$\n\n'+q.get(':question/worked-solution','[missing in original]')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--template',choices=list(TEMPLATES));p.add_argument('--profile',choices=list(PROFILES));p.add_argument('--format',choices=['markdown','json'],default='markdown');args=p.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 if args.count<1:p.error('Positive count required')
 rs=[]
 for level in levels:
  seen=set(); structures=set(); rng=random.Random(str(args.seed)+':'+level)
  t=args.template or {'easy':'single','moderate':'two_and','hard':'three'}[level]
  n=1 if t=='single' else 3 if t=='three' else 2
  capacity=6*comb(9,n)
  for i in range(args.count):
   for attempt in range(10000):
    record=generate(level,rng.getrandbits(64),args.template,profile=args.profile)
    p=record['generation']['parameters']; structure=(p['b']//p['a'],tuple(sorted(p['k'])))
    identity=record['generation']['parameter_fingerprint']
    if args.profile or (identity not in seen and (structure not in structures or len(structures)>=capacity)):
     seen.add(identity);structures.add(structure);rs.append(record);break
   else:raise ValueError('Batch construction exhausted; request fewer distinct instances')
 print(json.dumps(rs,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
if __name__=='__main__':main()
