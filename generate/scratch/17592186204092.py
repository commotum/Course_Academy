#!/usr/bin/env python3
"""No-solution equations with variable terms on both sides; exact source layouts."""
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186204092
KP_UUID='d63847ef-6360-50b5-b585-9084140b2d67'
TITLE='Solving For an Unknown Parameter - Variables and Constants on Both Sides'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='1.0.0'
SUPPORTED_LEVELS=('easy','moderate')
DOMAIN={'a':[-9,9],'c':[-9,9],'b':[-9,9],'d':[-9,9], 'constraints':'a,c nonzero; b != d; easy positive a>=2,c>=3,b=0,d>0 and distinct complete bank; moderate b nonzero.', 'sampling_policy':'Integer magnitudes bounded at 9, preserving all observed signs and values. New coefficient ratios and constant combinations are authored sampling extensions.'}
SOURCE_BASIS=1851
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def fingerprint(p):return digest(['both-constants' if p['b'] else 'right-constant',str(sp.Rational(p['c'],p['a']))])
def term(n,s=''):
 if not s:return str(n)
 return ('-' if n==-1 else '' if n==1 else str(n))+s
def add(n,s=''):return ('+' if n>0 else '-')+term(abs(n),s) if n else ''
def bank(p):
 a,c=p['a'],p['c']
 # Observed numerical patterns; misconception interpretation is unresolved.
 return [sp.Rational(c,a),sp.Rational(a,c),sp.Rational(c-1,a),sp.Rational(c,c-1),sp.Integer(c-1)]
def parameters(level,p):
 if set(p)!={'variable','parameter','a','b','c','d'}:raise ValueError('parameter keys')
 if p['variable'] not in 'xyzuvw' or len(p['variable'])!=1 or p['parameter'] not in 'pqrkmn' or len(p['parameter'])!=1:raise ValueError('names')
 if any(type(p[k]) is not int or abs(p[k])>9 for k in 'abcd') or not p['a'] or not p['c'] or p['b']==p['d']:raise ValueError('boundaries')
 if level=='easy':
  if p['a']<2 or p['c']<3 or p['b'] or p['d']<=0 or len(set(bank(p)))!=5:raise ValueError('easy bank constraints')
 elif level=='moderate':
  if not p['b']:raise ValueError('moderate must cancel nonzero constants')
 else:raise ValueError('unsupported level')
 return dict(p)
def render(p,template):
 x,k,a,b,c,d=(p[z] for z in ('variable','parameter','a','b','c','d'))
 ak=term(a,k); ax=ak+x; cx=term(c,x); left=ax+add(b); eq=left+'='+cx+add(d)
 coef=ak+add(-c); collected=ax+add(-c,x); rhs=d-b; root=sp.Rational(c,a); val=sp.latex(root)
 prompt=f'Consider the equation in the variable ${x},$ given by\n\n$$\n{eq}\n$$\n\nwhere ${k}$ is a constant. Given that this equation has no solution, what is the value of ${k}?$'
 if b:prompt+=f'\n\n${k}=$\n{{{{field-1}}}}'
 solution='Suppose we have an equation of the form\n\n$$\nax=b\n$$\n\nwhere $a$ and $b$ are constants, and $b\\ne 0.$ If $a=0,$ then the equation has no solution.\n\n'
 solution+=f'First, we rewrite the equation in the form $a{x}=b.$ \n\n'
 action=('subtracting' if c>0 else 'adding')+' $'+term(abs(c),x)+'$'
 solution+=f'We start by {action} from both sides of the equation:\n\n$$\n'
 # Sources use "adding ... to", not "from".
 if c<0:solution=solution.rsplit(' from both',1)[0]+' to both sides of the equation:\n\n$$\n'
 lines=[left+' & ='+cx+add(d),collected+add(b)+' & ='+cx+add(d)+add(-c,x),collected+add(b)+' & ='+str(d)]
 solution+=r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}'+'\n$$\n\n'
 if b:
  solution+=f"Then, we {'subtract' if b>0 else 'add'} ${abs(b)}$ {'from' if b>0 else 'to'} both sides:\n\n$$\n"
  lines=[collected+add(b)+' & ='+str(d),collected+add(b)+add(-b)+' & ='+str(d)+add(-b),collected+' & ='+str(rhs)]
  solution+=r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}'+'\n$$\n\n'
 solution+=f'Next, we factor ${x}$ on the left-hand side. This gives\n\n$$\n({coef}){x}={rhs}.\n$$\n\n'
 form='x' if template=='both-constants-ax-layout' else x
 solution+=f'Notice that this equation is now in the form $a{form}=b:$\n\n$$\n'
 solution+='{{('+coef+')}_{⏟}}_{a}'+x+'={{'+str(rhs)+'}_{⏟}}_{b}\n$$\n\nTherefore, the equation has no solution if\n\n$$\n'+coef+'=0.\n$$\n\n'
 solution+=f'Solving this for ${k},$ we get\n\n$$\n'
 lines=[coef+' & =0',coef+add(c)+' & =0'+add(c),ak+' & ='+str(c),r'\frac{'+ak+'}{'+str(a)+'} & ='+r'\frac{'+str(c)+'}{'+str(a)+'}',k+' & ='+val+'.']
 solution+=r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}'+'\n$$'
 return prompt,solution

def sample(rng,level):
 while True:
  p={'variable':rng.choice('xyzuvw'),'parameter':rng.choice('pqrkmn'),'a':rng.choice([i for i in range(-9,10) if abs(i)>=2]),'c':rng.choice([i for i in range(-9,10) if i]),'b':rng.choice([i for i in range(-9,10) if i]),'d':rng.randint(-9,9)}
  if level=='easy':p.update(a=rng.randint(2,9),c=rng.randint(3,9),b=0,d=rng.randint(1,9))
  try:return parameters(level,p)
  except ValueError:pass

def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty: '+str(level))
 template=template or ('right-constant' if level=='easy' else 'both-constants')
 if template not in (('right-constant',) if level=='easy' else ('both-constants','both-constants-ax-layout')):raise ValueError('template')
 profile=profile or ('observed-ratio-bank' if level=='easy' else 'blank-rational')
 if profile!=('observed-ratio-bank' if level=='easy' else 'blank-rational'):raise ValueError('profile')
 p=globals()['parameters'](level,parameters if parameters is not None else sample(random.Random(seed),level))
 root=sp.solve(p['a']*sp.Symbol(p['parameter'])-p['c'],sp.Symbol(p['parameter']))[0]
 values=bank(p) if level=='easy' else [root]
 prompt,solution=render(p,template); content=digest([level,prompt,solution,sorted(map(str,values))])
 qid=uid('question:'+content);key='selection' if level=='easy' else 'field-1';fid=uid(qid+':field:'+key)
 answers=[{':answer/id':uid(fid+':answer:'+str(v)),':answer/type':':answer.type/math',':answer/value':sp.latex(v)} for v in values]
 f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if level=='easy' else 'blank'),':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[0][':answer/id']]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[f]},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'parameter_fingerprint':fingerprint(p),'content_fingerprint':content,'domain':DOMAIN,'plot_rating':'none','source_analysis':{'basis':SOURCE_BASIS,'lineage':LINEAGE,'reference':'generate/scratch/17592186204092/source-cases.json'}}}
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def batch(level,count=5,seed=0):
 if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty')
 if type(count)is not int or count<0:raise ValueError('count')
 rows=[];seen=set()
 for i in range(5000):
  if len(rows)==count:return rows
  r=generate(level,seed+i);fp=r['generation']['parameter_fingerprint']
  if fp not in seen:rows.append(r);seen.add(fp)
 raise ValueError('Finite distinct-ratio capability exhausted; no padding')
def markdown(r):return r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--output',type=Path);args=ap.parse_args()
 rows=batch(args.difficulty,args.count,args.seed);text=(json.dumps(rows,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))+'\n'
 if args.output:args.output.write_text(text)
 else:print(text,end='')
if __name__=='__main__':main()
