#!/usr/bin/env python3
"""Particular solutions with resonant exponential forcing; frozen local generator.

Math database basis1356, lineage01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.
Eight easy and four moderate observed blanks. No plots. Explicit observed profiles
preserve the duplicate legacy answer and original notation. Normal removes
the redundant answer and clarifies omission of an added complementary term. Hard is an authored signed, fractional two-exponential extension
of the canonical example, using the same two unknown coefficients and four-row
product-rule derivation. No general solutions, IVPs, integrating factors or
second-order equations are assessed. Explicit inputs obey the same workload
bounds as samplers. See the adjacent extraction and independent validator.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
import sympy as sp
KP_ID=17592186229163
KP_UUID='3c7ce128-42e5-5a5a-8fa2-0e897504ff9d'
TITLE='Finding a Particular Solution When the Forcing Term is Part of the Complementary Solution'
VERSION='resonant-first-order-1.0'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={'resonant_single':'easy','resonant_sum':'moderate','signed_fractional_sum':'hard'}
# Profiles preserve notation/layout differences, not mathematical branches.
PROFILES={'normal':{},'braced':{},'plain':{'plain':True},'duplicate_legacy':{'duplicate':True},
          'punctuated':{'punctuated':True}}
OPENING='To find the general solution of an inhomogeneous first-order linear equation with constant coefficients on the left-hand side, we must find the sum of the complementary and particular solutions.'
Y='{y}_{p}'
def coeff(v):
 v=sp.Rational(v)
 if v==1:return ''
 if v==-1:return '-'
 return str(v) if v.q==1 else ('-' if v<0 else '')+r'\frac{'+str(abs(v.p))+'}{'+str(v.q)+'}'
def term(v,s):return coeff(v)+s
def join(a,b):return a+('' if b.startswith('-') else '+')+b
def exp(r,plain=False):return ('e' if plain else '{e}')+'^{'+term(r,'x')+'}'
def block(s):return '$$\n'+s+'\n$$'
def aligned(rows):return block(r'\begin{aligned}'+r' \\ '.join(l+' & ='+r for l,r in rows)+r'\end{aligned}')
def validate_parameters(level,p):
 keys={'r','a'} if level=='easy' else {'r','a','s','b'}
 if set(p)!=keys or any(type(v)!=int for v in p.values()):raise ValueError('Supply exactly integer '+str(sorted(keys)))
 r,a=p['r'],p['a']
 if not 2<=abs(r)<=6 or not 2<=a<=12:
  if level=='easy':raise ValueError('Easy: 2<=|r|<=6, 2<=a<=12')
 if level=='moderate':
  if not (-6<=r<=-2 and 2<=a<=30 and 1<=p['s']<=3 and 1<=abs(p['b'])<=12):raise ValueError('Moderate bounds')
 if level=='hard':
  s,b=p['s'],p['b'];beta=sp.Rational(b,s-r) if s!=r else sp.Integer(0)
  if not (1<=abs(r)<=6 and 1<=abs(s)<=6 and s!=r and 2<=abs(a)<=12 and 1<=abs(b)<=12 and 2<=beta.q<=7 and abs(beta.p)<=12 and (r>0 or s<0) and (a<0 or b<0)):raise ValueError('Hard requires signed forcing, extended rate signs and noninteger beta within bounded two-term workload')
def sample(level,rng):
 for _ in range(1000):
  if level=='easy':p={'r':rng.choice([-6,-5,-4,-3,-2,2,3,4,5,6]),'a':rng.randint(2,12)}
  elif level=='moderate':p={'r':-rng.randint(2,6),'a':rng.randint(2,30),'s':rng.randint(1,3),'b':rng.choice([-1,1])*rng.randint(1,12)}
  else:p={'r':rng.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]),'a':rng.choice([-1,1])*rng.randint(2,12),'s':rng.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]),'b':rng.choice([-1,1])*rng.randint(1,12)}
  try:validate_parameters(level,p);return p
  except ValueError:pass
 raise ValueError('No valid bounded instance')
def build(level,p,profile):
 r,a=p['r'],p['a'];er=exp(r);two=level!='easy';flags=PROFILES[profile]
 rhs=term(a,er);guess=r'\alpha x'+er;final=term(a,'x'+er)
 if two:
  s,b=p['s'],p['b'];es=exp(s);rhs=join(rhs,term(b,es));guess+=r'+\beta '+es;beta=sp.Rational(b,s-r);final=join(final,term(beta,es))
 prompt='Given that the differential equation \n\n'+block('{y}^{′}'+join('',term(-r,'y'))+'='+rhs+',')+'\n\nhas the complementary solution ${y}_{c}(x)=A'+er+'$, find the particular solution to the equation.\n\n$'+Y+'(x)=$\n{{field-1}}'
 if profile=='normal':prompt=prompt.replace('find the particular solution to the equation.','find the particular solution to the equation. Give a particular solution with no added complementary-solution term.')
 solution=OPENING+'\n\nWe see that the right-hand side is $'+rhs+',$ and $'+er+'$ is a term in the complementary solution'
 if two:solution+=', while $'+es+'$ is not'
 solution+=', so we assume that a particular solution takes the form \n\n'+block(Y+'='+guess+',')+'\n\nwhere $\\alpha $'+(' and $\\beta $ are constants that are' if two else ' is a constant that is')+' to be determined.\n\n'
 solution+=('Calculating the first derivative of ${y}_{p}$ gives' if two else 'We calculate the first derivative of ${y}_{p}$ using the product rule for differentiation:')+'\n\n'
 formal=r'\alpha (x'+er+')^{′}';product=r'\alpha ('+join(er,term(r,'x'+er))+')';derivative=r'\alpha ('+join('1',term(r,'x'))+')'+er
 if two:
  formal+=r'+\beta ('+es+')^{′}';product=join(product,term(s,r'\beta '+es));derivative=join(derivative,term(s,r'\beta '+es))
 period='.' if flags.get('punctuated') else ''
 solution+=aligned([(Y+'^{′}','('+guess+')^{′}'),('',formal),('',product),('',derivative+period)])+'\n\n'
 solution+='To find the '+('values' if two else 'value')+' of $\\alpha '+('$ and $\\beta ' if two else '')+',$ we substitute ${y}_{p}$ and ${y}_{p}^{′}$ into the differential equation:\n\n'
 substitute='('+derivative+')'+join('',term(-r,'('+guess+')' if two else r'\alpha x'+er))
 collected='('+join(join('1',term(r,'x')),term(-r,'x'))+r')\alpha '+er
 reduced=r'\alpha '+er
 if two:
  collected+= '+('+join(term(s,r'\beta '),term(-r,r'\beta '))+')'+es
  reduced=join(reduced,term(s-r,r'\beta '+es))
 rows=[(substitute,rhs),(collected,rhs),(reduced,rhs+period)]
 if not two:rows.append((r'\alpha ',str(a)))
 solution+=aligned(rows)+'\n\n'
 if two:
  solution+='Equating coefficients of $'+er+'$ and $'+es+'$ gives\n\n'+block(r'\alpha ='+str(a)+r'\,\text{and}\,'+term(s-r,r'\beta ')+'='+str(b)+',')+'\n\nso, we have\n\n'+block(r'\alpha ='+str(a)+r'\,\text{and}\,\beta ='+(str(beta) if beta.q==1 else coeff(beta))+'.')+'\n\n'
 solution+='Therefore, the particular solution ${y}_{p}(x)$ is\n\n'+block(Y+'(x)='+final+'.')
 values=[final]
 if flags.get('plain'):values=[final.replace('{e}','e')]
 if flags.get('duplicate'):values=[final,final.replace('{e}','e')]
 return prompt,solution,values,len(values)-1

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 name=next(t for t,l in TEMPLATES.items() if l==level)
 if template is not None and template!=name:raise ValueError('Template difficulty mismatch')
 if field_type not in (None,'blank'):raise ValueError('This KP uses blank fields')
 profile=profile or 'normal'
 if profile not in PROFILES:raise ValueError('Unknown profile')
 if level=='hard' and profile!='normal':raise ValueError('Hard has only authored normal profile')
 if (profile in ('plain','duplicate_legacy') and level!='easy') or (profile=='punctuated' and level!='moderate'):raise ValueError('Profile eligibility')
 p=dict(parameters) if parameters is not None else sample(level,random.Random(seed));validate_parameters(level,p)
 prompt,solution,values,correct=build(level,p,profile)
 # Equivalent tasks across answer spelling/profile aliases have one math fingerprint.
 math_key=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()
 content_key=hashlib.sha256(json.dumps([VERSION,level,prompt,solution,sorted(values),values[correct]],ensure_ascii=False).encode()).hexdigest()
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),content_key));fid=str(uuid.uuid5(uuid.UUID(qid),'field-1'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(i)+':'+v)),':answer/type':':answer.type/math',':answer/value':v}for i,v in enumerate(values)]
 field={':answer-field/id':fid,':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct][':answer/id']]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'parameter_fingerprint':math_key,'content_fingerprint':content_key,'authored_extension':level=='hard','source_analysis':SOURCE,'plot_rating':'none','domain':'x real','profile_origin':'authored default' if profile=='normal' else 'observed replay'}}
# EASY: one resonant forcing term; one product rule, one coefficient equation.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: resonant plus nonresonant term; two coefficient equations.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: same two terms/unknowns; signed collection and noninteger coefficient.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(rec):
 q=rec['question'];return q[':question/problem']+'\n\nAnswer: $'+q[':question/answer-fields'][0][':answer-field/choices'][-1][':answer/value']+'$\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(PROFILES));args=ap.parse_args()
 if args.count<1:ap.error('count must be positive')
 records=[generate(l,args.seed+i,args.template,profile=args.profile)for l in (['easy','moderate','hard']if args.difficulty=='all'else[args.difficulty])for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False)if args.format=='json'else'\n\n---\n\n'.join(markdown(r)for r in records))
if __name__=='__main__':main()
