#!/usr/bin/env python3
"""Exponential first-order IVPs, fixed snapshot math/basis 1356. No database writes.

Easy: one nonresonant exponential, y(0) supplied. Moderate: one resonant
exponential, product rule, y(0) supplied. Hard: authored two forcing components,
either both nonresonant or one resonant; exactly the preceding particular/general
solution methods, with one initial constant. See adjacent extraction and review.
Observed profiles preserve all original mathematical rows and shared prose.
Raw profiles replay missing answer/solution evidence through the public API.
Explicit inputs obey the same level-specific bounds as sampling; seed is not
identity. No source answer lookup, literal source-return branch, or DB client.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186229165
KP_UUID='570160ff-c937-57e7-bd78-702f7f018e64'
TITLE='Solving an Initial Value Problem'
VERSION='exponential-ivp-1.0-frozen'
ROOT=Path(__file__).with_suffix('')
x=s.Symbol('x',real=True)
TEMPLATES={'nonresonant':'easy','resonant':'moderate','two_nonresonant':'hard','mixed':'hard'}
# Presentation masks are complete mathematical components, never global number replacements.
PROFILES={
 'q-332426':dict(template='nonresonant',plain=True,missing=True),
 'q-332797':dict(template='resonant',plain=True,missing=True),
 'q-332903':dict(template='nonresonant',compact=False,dot=True),
 'q-332905':dict(template='nonresonant',compact=False,dot=True),
 'q-332906':dict(template='nonresonant',compact=True,dot=False),
 'q-332908':dict(template='nonresonant',compact=True,dot=False,answer='forcing_first'),
 'q-332909':dict(template='nonresonant',compact=True,dot=False),
 'q-333171':dict(template='nonresonant',compact=False,dot=True,coefficient_dot=True),
 'q-332936':dict(template='resonant',answer='factored'),
 'q-332937':dict(template='resonant'),
 'q-332938':dict(template='resonant',answer='unbraced'),
 'q-332940':dict(template='resonant'),
 'q-333160':dict(template='resonant'),
 'q-332942':dict(template='resonant'),
 'q-333174':dict(template='resonant',prompt_dot=True),
}
OPEN='To find the general solution of an inhomogeneous first-order linear equation with constant coefficients on the left-hand side, we must find the sum of the complementary and particular solutions.'
def tex(n):return s.latex(s.sympify(n)).replace('- ', '-')
def coef(n,body):
 n=s.sympify(n)
 if n==0:return '0'
 if not body:return tex(n)
 return ('-' if n==-1 else '' if n==1 else tex(n))+body

def exp(k,braces=True):return ('{e}' if braces else 'e')+'^{'+coef(k,'x')+'}'
def signed(n,body):return ('+' if n>=0 else '-')+coef(abs(n),body)
def summands(parts):
 out=''
 for p in parts:
  if p=='0':continue
  out+=('+' if out and not p.startswith('-') else '')+p
 return out or '0'
def block(t):return '$$\n'+t+'\n$$'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(a+' & ='+b for a,b in rows)+r'\end{aligned}'
def param_guard(level,t,p):
 expected={'h','k','f','v'}|({'k2','f2'} if level=='hard' else set())
 if set(p)!=expected:raise ValueError('Exact parameter keys required: '+str(sorted(expected)))
 if any(type(v)!=int for v in p.values()):raise ValueError('Integer parameters required')
 if not (1<=abs(p['h'])<=6 and 1<=abs(p['k'])<=6 and 1<=abs(p['f'])<=15 and abs(p['v'])<=10):raise ValueError('Coefficients outside authored workload bounds')
 if t=='nonresonant' and p['h']==p['k']:raise ValueError('Easy requires nonresonance')
 if t=='resonant' and p['h']!=p['k']:raise ValueError('Moderate requires resonance')
 if level=='hard':
  if not (1<=abs(p['k2'])<=6 and 1<=abs(p['f2'])<=12 and abs(p['f'])<=12 and abs(p['v'])<=8):raise ValueError('Hard workload bounds')
  if p['k']==p['k2']:raise ValueError('Hard requires two distinct components')
  if t=='two_nonresonant' and p['h'] in (p['k'],p['k2']):raise ValueError('Both exponents must be nonresonant')
  if t=='mixed' and sum(k==p['h'] for k in (p['k'],p['k2']))!=1:raise ValueError('Mixed requires exactly one resonant component')
def sample(level,t,r):
 resonant_position=r.randrange(2) if t=='mixed' else None
 h=r.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]);k=h if t in ('resonant','mixed') else r.choice([z for z in range(-6,7) if z and z!=h])
 p=dict(h=h,k=k,f=r.choice([z for z in range(-12,13) if z]),v=r.randint(-8,8))
 if level=='hard':p.update(k2=r.choice([z for z in range(-6,7) if z and z not in (h,k)]),f2=r.choice([z for z in range(-12,13) if z]))
 if resonant_position==1:p['k'],p['k2']=p['k2'],p['k']
 return p

def components(p):
 h=p['h'];pairs=[(p['k'],p['f'])]+([(p['k2'],p['f2'])] if 'k2' in p else [])
 cs=[s.Integer(f) if k==h else s.Rational(f,k-h) for k,f in pairs]
 A=s.Integer(p['v'])-sum(c for (k,f),c in zip(pairs,cs) if k!=h)
 particular=sum(c*(x if k==h else 1)*s.exp(k*x) for (k,f),c in zip(pairs,cs))
 return pairs,cs,A,particular,A*s.exp(h*x)+particular

def build_single(p,t,flags):
 h,k,f,v=(p[z] for z in ('h','k','f','v'));res=t=='resonant';b=exp(k);bh=exp(h);alpha=r'\alpha ';yp='{y}_{p}';yc='{y}_{c}';pairs,cs,A,part,sol=components(p);c=cs[0]
 term=coef(c,('x' if res else '')+b);final=summands([coef(A,bh),term]);general=summands(['A'+bh,term])
 forcing=coef(f,b);op=lambda body:signed(-h,body)
 equation='{y}^{′}'+op('y')+'='+forcing
 if flags.get('plain'):
  eq='y^{′}'+(' - '+coef(h,'y') if h>0 else ' + '+coef(-h,'y'))+' = '+coef(f,exp(k,False))
  prompt='Consider the following initial value problem:\n$'+eq+', y(0) = '+str(v)+'$\n\nGiven that the differential equation\n$'+eq+'$\nhas the complementary solution $y_{c} = A'+exp(h,False)+'$, solve the initial value problem.\n\n$y(x) =$\n{{field-1}}'
 else:
  prompt='Consider the following initial value problem:\n\n'+block(equation+r',\,y(0)='+str(v)+('.' if flags.get('prompt_dot') else ''))+'\n\nGiven that the differential equation \n\n'+block(equation)+'\n\nhas the complementary solution $'+yc+'=A'+bh+',$ solve the initial value problem.\n\n$y(x)=$\n{{field-1}}'
 trial=alpha+('x' if res else '')+b
 if res:
  dx=alpha+'(1'+signed(k,'x')+')'+b
  derivative=aligned([(yp+'^{′}','('+trial+')^{′}'),('',alpha+'(x'+b+')^{′}'),('',alpha+'('+b+signed(k,'x'+b)+')'),('',dx+'.')])
  substitute=[('('+dx+')'+op('('+trial+')'),forcing),('(1'+signed(k,'x')+signed(-h,'x')+')'+alpha+b,forcing),(alpha+b,forcing),(r'\alpha ',str(f)+'.')]
 else:
  dx=coef(k,alpha+b);derivative=yp+'^{′}='+dx+'.'
  if flags.get('compact'):
   substitute=[(dx+op(alpha+b),forcing),(coef(k-h,alpha+b),forcing),(r'\alpha ',tex(c)+('.' if flags.get('coefficient_dot') else ''))]
  else:
   substitute=[('('+dx+')'+op('('+trial+')'),forcing),('('+str(k)+signed(-h,'')+')'+alpha+b,forcing),(coef(k-h,alpha+b),forcing),(r'\alpha ',tex(c)+('.' if flags.get('coefficient_dot') else ''))]
 dot='.' if res or flags.get('dot') else ''
 initialpart='0' if res else tex(c)
 initlhs='A+0' if res else 'A'+('+' if c>=0 else '-')+tex(abs(c))
 pieces=[OPEN,'To find the complementary solution $'+yc+',$ we solve the corresponding homogeneous equation, given by',block(yc+'^{′}'+op(yc)+'=0.'),'Solving this equation, we find that the complementary solution is',block(yc+'=A'+bh),'where $A$ is an arbitrary constant.','We now need to find the particular solution $'+yp+'(x).$','We see that the right-hand side is $'+forcing+',$ and $'+b+'$ is '+('' if res else 'not ')+'a term in the complementary solution, so we assume a particular solution of the form',block(yp+'='+trial+','),'where $'+alpha+'$ is a constant to be determined.','We calculate the first derivative of $'+yp+'$ using the product rule for differentiation:' if res else 'Calculating the first derivative of $'+yp+'$ gives',block(derivative),'To find the value of $'+alpha+',$ we substitute $'+yp+'$ and $'+yp+"^{′}$ into the differential equation:",block(aligned(substitute)),'Therefore, the particular solution $'+yp+'(x)$ is',block(yp+'(x)='+term+'.'),'Now, since the general solution is given by',block('y(x)='+yc+'(x)+'+yp+'(x),'),'the general solution in our case is',block('y='+general+'.'),'We can find the constant $A$ using the initial conditions.','Substituting $y(0)='+str(v)+'$ into the general solution gives',block(aligned([(initlhs,str(v)),('A',tex(A)+dot)])),'Therefore, the solution to the initial value problem is',block('y='+final+'.')]
 answer=final
 if flags.get('answer')=='forcing_first':answer=summands([term,coef(A,bh)])
 if flags.get('answer')=='factored':answer='('+summands([coef(f,'x'),str(v)])+')'+exp(h,False)
 if flags.get('answer')=='unbraced':answer=answer.replace('{e}','e')
 return prompt,'\n\n'.join(pieces),answer

def build_hard(p,t):
 h=p['h'];pairs,cs,A,part,sol=components(p);alphas=[r'\alpha ',r'\beta '];bh=exp(h)
 forcing=summands([coef(f,exp(k)) for k,f in pairs]);trialparts=[a+('x' if k==h else '')+exp(k) for (k,f),a in zip(pairs,alphas)];trial='+'.join(trialparts)
 dparts=[a+'(1'+signed(k,'x')+')'+exp(k) if k==h else coef(k,a+exp(k)) for (k,f),a in zip(pairs,alphas)];deriv=summands(dparts)
 op=lambda z:signed(-h,z)
 eq='{y}^{′}'+op('y')+'='+forcing
 prompt='Consider the following initial value problem:\n\n'+block(eq+r',\,y(0)='+str(p['v']))+'\n\nGiven that the differential equation \n\n'+block(eq)+'\n\nhas the complementary solution ${y}_{c}=A'+bh+',$ solve the initial value problem.\n\n$y(x)=$\n{{field-1}}'
 terms=[coef(c,('x' if k==h else '')+exp(k)) for (k,f),c in zip(pairs,cs)];particular=summands(terms);general=summands(['A'+bh,*terms]);answer=summands([coef(A,bh),*terms])
 resonant_index=next((i for i,(k,f) in enumerate(pairs) if k==h),None)
 explanation='We examine both exponential forcing terms. '+('The '+('first' if resonant_index==0 else 'second')+' exponential is a term in the complementary solution, so its trial term is multiplied by $x$; the other exponential is not.' if t=='mixed' else 'Neither exponential is a term in the complementary solution.')+' We assume a particular solution of the form'
 pieces=[OPEN,'To find the complementary solution ${y}_{c},$ we solve the corresponding homogeneous equation, given by',block('{y}_{c}^{′}'+op('{y}_{c}')+'=0.'),'Solving this equation, we find that the complementary solution is',block('{y}_{c}=A'+bh),'where $A$ is an arbitrary constant.','We now need to find the particular solution ${y}_{p}(x).$',explanation,block('{y}_{p}='+trial+','),r'where $\alpha $ and $\beta $ are constants that are to be determined.']
 if t=='mixed':
  formal=[a+'(x'+exp(k)+')^{′}' if k==h else d for (k,f),a,d in zip(pairs,alphas,dparts)]
  product=[a+'('+exp(k)+signed(k,'x'+exp(k))+')' if k==h else d for (k,f),a,d in zip(pairs,alphas,dparts)]
  rows=[('{y}_{p}^{′}','('+trial+')^{′}'),('',summands(formal)),('',summands(product)),('',deriv+'.')]
 else:rows=[('{y}_{p}^{′}','('+trial+')^{′}'),('',deriv+'.')]
 pieces+=['We calculate the first derivative of ${y}_{p}$'+(' using the product rule for differentiation:' if t=='mixed' else ':'),block(aligned(rows)),r'To find the values of $\alpha $ and $\beta,$ we substitute ${y}_{p}$ and ${y}_{p}^{′}$ into the differential equation:']
 # Separate distribution, cancellation and coefficient stages retain mathematical structure.
 distributed=[];reduced=[]
 for (k,f),a in zip(pairs,alphas):
  if k==h:distributed.append('(1'+signed(k,'x')+signed(-h,'x')+')'+a+exp(k));reduced.append(a+exp(k))
  else:distributed.append('('+str(k)+signed(-h,'')+')'+a+exp(k));reduced.append(coef(k-h,a+exp(k)))
 pieces+=[block(aligned([('('+deriv+')'+op('('+trial+')'),forcing),('+'.join(distributed),forcing),(summands(reduced),forcing)])),'Equating coefficients of the two distinct exponentials gives',block(coef(1 if pairs[0][0]==h else pairs[0][0]-h, r'\alpha ' )+'='+str(pairs[0][1])+r',\qquad '+coef(1 if pairs[1][0]==h else pairs[1][0]-h,r'\beta ')+'='+str(pairs[1][1])+'.'),'So, we have',block(r'\alpha ='+tex(cs[0])+r',\qquad \beta ='+tex(cs[1])+'.'),'Therefore, the particular solution ${y}_{p}(x)$ is',block('{y}_{p}(x)='+particular+'.'),'Now, since the general solution is given by',block('y(x)={y}_{c}(x)+{y}_{p}(x),'),'the general solution in our case is',block('y='+general+'.'),'We can find the constant $A$ using the initial conditions.','Substituting $y(0)='+str(p['v'])+'$ into the general solution gives',block(aligned([('A'+''.join('+0' if k==h else signed(c,'') for (k,f),c in zip(pairs,cs)),str(p['v'])),('A',tex(A)+'.')])),'Therefore, the solution to the initial value problem is',block('y='+answer+'.')]
 return prompt,'\n\n'.join(pieces),answer

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'blank'):raise ValueError('Only blank fields are supported')
 raw=bool(profile and profile.startswith('raw:'));name=profile[4:] if raw else profile
 if name is not None and name not in PROFILES:raise ValueError('Unknown profile')
 flags=PROFILES.get(name,{})
 r=random.Random(seed);template=template or flags.get('template') or r.choice([t for t,l in TEMPLATES.items() if l==level])
 if template not in TEMPLATES or TEMPLATES[template]!=level or name and flags['template']!=template:raise ValueError('Template/profile difficulty mismatch')
 p=dict(parameters) if parameters is not None else sample(level,template,r);param_guard(level,template,p)
 prompt,solution,answer=build_hard(p,template) if level=='hard' else build_single(p,template,flags)
 missing=raw and flags.get('missing')
 if missing:solution=None;answer=None
 bank=[answer]
 if not missing and flags.get('answer') in ('factored','unbraced'):
  pairs,cs,A,_,_=components(p)
  expanded=summands([coef(A,exp(p['h'])),*[coef(c,('x' if k==p['h'] else '')+exp(k)) for (k,f),c in zip(pairs,cs)]])
  bank=[expanded,answer]
 pairs,_,_,_,_=components(p)
 fingerprint=hashlib.sha256(json.dumps({'method':'first-order-IVP','h':p['h'],'forcing':s.srepr(sum(s.Integer(f)*s.exp(k*x) for k,f in pairs)),'initial':p['v']},sort_keys=True).encode()).hexdigest()
 identity=hashlib.sha256(json.dumps([VERSION,prompt,solution,bank],ensure_ascii=False).encode()).hexdigest()
 qid=str(uuid.uuid5(uuid.NAMESPACE_URL,identity));fid=str(uuid.uuid5(uuid.UUID(qid),'field-1'));aids=[str(uuid.uuid5(uuid.UUID(fid),str(i)+':'+str(a))) for i,a in enumerate(bank)]
 field={':answer-field/id':fid,':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank'}
 if not missing:field.update({':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':a} for aid,a in zip(aids,bank)],':answer-field/correct':[':answer/id',aids[-1]]})
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if not (raw and flags.get('missing')):q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'origin':'observed' if name and not flags.get('missing') else 'authored','source_id':name,'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'mathematical_fingerprint':fingerprint,'content_identity':identity,'domain':'x real','source_missing_completion':bool(flags.get('missing') and not raw),'sympy':s.__version__}}
# EASY — exactly one nonresonant trial and scalar initial-constant solve.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — exactly one resonant product-rule trial and initial-constant solve.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — two same-method forcing components and one scalar initial-constant solve.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 choices=f.get(':answer-field/choices',[])
 entries='\n'.join('- '+('**Designated correct:** ' if a[':answer/id']==f[':answer-field/correct'][1] else 'Equivalent original blank alternative: ')+'$'+a[':answer/value']+'$' for a in choices) if choices else '[Answer bank and correct designation missing in raw source]'
 return q[':question/problem']+'\n\n'+entries+'\n\n'+q.get(':question/worked-solution','[missing in raw source]')
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--template',choices=TEMPLATES);a.add_argument('--profile');a.add_argument('--format',choices=['markdown','json'],default='markdown');z=a.parse_args()
 if z.count<1:a.error('Positive count required')
 records=[generate(l,z.seed+i,z.template,profile=z.profile) for l in (['easy','moderate','hard'] if z.difficulty=='all' else [z.difficulty]) for i in range(z.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if z.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
