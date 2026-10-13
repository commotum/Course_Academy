#!/usr/bin/env python3
"""Cartesian flux formula completion, all observed levels, no EDB operations.

Twelve observed layout/bank recipes replay through the same parameterized renderer.
Numeric monomial families derive derivatives and oriented normals exactly; named
symbolic functions form a finite categorical subskill. Default monomial sampling
also transposes the two exponent roles at equal workload (authored extension).
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent/'17592186198392'
RAW=json.loads((ROOT/'source.json').read_text());DATA=json.loads((ROOT/'extraction.json').read_text())
KP_ID=17592186198392;KP_UUID=RAW['record'][':knowledge-point/id'];TITLE=RAW['record'][':knowledge-point/title'];VERSION='cartesian-flux-formula-1'
x,y,z,P,Q,R=sp.symbols('x y z P Q R',real=True)
SYMBOLS={s.name:s for s in (x,y,z,P,Q,R)}
TEMPLATES={n:d['level'] for n,d in DATA.items()}
MONOMIALS=[n for n,d in DATA.items() if d['kind']=='monomial']
BOX=r'\bbox[3pt,border:1pt solid black]{\phantom{A}}'
def digest(d):return hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest()
def tex(t):return sp.latex(sp.simplify(t)).replace('x^{','{x}^{').replace('y^{','{y}^{').replace('z^{','{z}^{').replace(' ','')
def substitute(s,slots):
 for k,v in slots.items():s=s.replace('<<'+k+'>>',v)
 if '<<' in s:raise AssertionError('Unexpanded slot')
 return s

def exact_parameters(name,params):
 d=DATA[name]
 if d['kind']=='symbolic':
  if set(params)!={'function'} or params['function'] not in ('g','h','k','f','s','w'):raise ValueError('Named differentiable graph function required')
  return dict(params)
 if set(params) not in ({'c','m','n'},{'c','m','n','a','b','h'} if name=='q-161456' else {'c','m','n'}) or any(type(params[k]) is not int for k in params):raise ValueError('Exact c,m,n and optional bilinear offsets a,b,h required')
 if name=='q-161456' and any(abs(params.get(k,0))>2 for k in ('a','b','h')):raise ValueError('Bilinear offsets must have magnitude <=2')
 c,m,n=(params[k] for k in ('c','m','n'))
 if not 1<=abs(c)<=9:raise ValueError('Nonzero coefficient of magnitude <=9 required')
 permitted={'q-161449':[(2,1),(1,2)],'q-161456':[(1,1)],'q-161453':[(2,1),(1,2)],'q-161455':[(1,3),(3,1)]}[name]
 if (m,n) not in permitted:raise ValueError('Exponent pattern is outside this peer-level family')
 return {**params,**{k:params.get(k,0) for k in ('a','b','h')}} if name=='q-161456' else dict(params)

def math_data(name,p):
 d=DATA[name];axis=d['axis'];u,v={'x':(y,z),'y':(x,z),'z':(x,y)}[axis]
 graph=sp.Function(p['function'])(u,v) if d['kind']=='symbolic' else p['c']*(u-p.get('a',0))**p['m']*(v-p.get('b',0))**p['n']+p.get('h',0)
 rr=sp.Matrix([graph if t.name==axis else t for t in (x,y,z)]);ru=rr.diff(u);rv=rr.diff(v);cross=ru.cross(rv);N=-cross if axis=='y' else cross
 full=sp.expand(sp.Matrix([P,Q,R]).dot(N))
 return {'u':u,'v':v,'graph':graph,'r':rr,'ru':ru,'rv':rv,'cross':cross,'normal':N,'full':full}

def slot_values(name,p,m):
 d=DATA[name]
 if d['kind']=='symbolic':return {}
 u,v=m['u'],m['v'];c,a,b=(p[k] for k in ('c','m','n'));f1,f2={'x':(Q,R),'y':(P,R),'z':(P,Q)}[d['axis']]
 values={'graph':m['graph'],'du':sp.diff(m['graph'],u),'dv':sp.diff(m['graph'],v),
  'negdu':-sp.diff(m['graph'],u),'negdv':-sp.diff(m['graph'],v),'baseu':(u-p.get('a',0))**(a-1)*(v-p.get('b',0))**b,'basev':(u-p.get('a',0))**a*(v-p.get('b',0))**(b-1),
  'coefu':-c*a*f1,'coefv':(c*b if name=='q-161455' else -c*b)*f2}
 original=math_data(name,d['original_parameters']);op=d['original_parameters'];ov={
  'graph':original['graph'],'du':sp.diff(original['graph'],u),'dv':sp.diff(original['graph'],v),'negdu':-sp.diff(original['graph'],u),'negdv':-sp.diff(original['graph'],v),
  'baseu':u**(op['m']-1)*v**op['n'],'basev':u**op['m']*v**(op['n']-1),'coefu':-op['c']*op['m']*f1,'coefv':(op['c']*op['n'] if name=='q-161455' else -op['c']*op['n'])*f2}
 out={k:d['aliases'][k] if sp.simplify(t-ov[k])==0 else tex(t) for k,t in values.items()}
 if name in ('q-161453','q-161455') and values['coefv'].as_coeff_Mul()[0]<0:out['coefv']='('+out['coefv']+')'
 if name=='q-161456':
  for key in ('baseu','basev'):
   if isinstance(values[key],sp.Add):out[key]='('+out[key]+')'
 return out

def rename_function(s,name,p):
 old={'x':'k','y':'h','z':'g'}[DATA[name]['axis']]
 return re.sub(r'(?<![A-Za-z])'+old+r'(?=\()|(?<=∂)'+old+r'(?![A-Za-z])',p['function'],s)

def bank_tuples(name,p):
 c,a,b=(p[k] for k in ('c','m','n'))
 if name=='q-161449':return [(-2*c*a*P,-2*c*b*Q),(-c*a*P,-c*b*Q),(-2*c*a*Q,c*b*P),(-c*a*R,c*b*Q),(c*b*P,-c*b*R)]
 if name=='q-161456':return [(-c*Q,R),(-c*Q,-c*R),(Q,R),(Q,-c*R),(-Q,-R)]
 if name=='q-161453':return [(-c*a*P,-c*b*R),(-c*b*P,c*a*R),(-c*b*P,-c*b*R),(c*a*P,-c*a*R),(-c*a*P,c*a*R)]
 if name=='q-161455':return [(-c*a*R,-c*a*P),(P,R),(P,-c*b*R),(-c*a*P,-R),(-c*a*P,c*b*R)]
 raise ValueError('Unknown numeric bank')

def bank(name,p):
 d=DATA[name]
 if d['kind']=='symbolic':return [rename_function(t,name,p) for t in d['bank']],[{'recipe':'observed_token_tuple:'+str(i)} for i in range(5)]
 tuples=bank_tuples(name,p);original=bank_tuples(name,d['original_parameters'])
 if len(set(tuples))!=5:raise ValueError('Whole bank rejected: duplicate/equivalent tuples')
 out=[]
 for val,old,spelling in zip(tuples,original,d['bank']):
  out.append(spelling if val==old else '$'+tex(val[0])+'$ and $'+tex(val[1])+'$')
 return out,[{'recipe':'observed_coefficient_operation:'+str(i),'tuple':[str(t) for t in val]} for i,val in enumerate(tuples)]

def explicit_boxes(name,s):
 # Captured text lost some widget placeholders. Replay retains it; normal output clarifies it.
 if name=='q-161189':s=s.replace('(\\frac','('+BOX+r'\frac',1).replace('+\\frac','+'+BOX+r'\frac',1)
 if name=='q-161166':s=s.replace(r'\frac{}',BOX+r'\frac{'+BOX+'}',1)
 if name=='q-161446':s=s.replace(r'P+\frac',r'P+'+BOX+r'\frac')
 if name in ('q-161453','q-161456'):s=s.replace(r'(\,','('+BOX+r'\,',1).replace(r'+\,','+'+BOX+r'\,')
 if name in ('q-161166','q-161446'):s=re.sub(r'\\frac\{(∂[A-Za-z])\}\{\}',lambda m:r'\frac{'+m[1]+'}{'+BOX+'}',s)
 if name=='q-161460':s=s.replace(r'(\,+','('+BOX+BOX+'+').replace(r'-R\,',r'-R'+BOX+r'\,')
 return s

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio layout observed')
 rng=random.Random(seed)
 if template is None and profile and profile.startswith('observed:'):template=profile.split(':',1)[1]
 # Narrow categorical formula masks remain available explicitly; defaults provide real derivative variation.
 template=template or rng.choice([n for n in MONOMIALS if TEMPLATES[n]==level])
 if template not in DATA or TEMPLATES[template]!=level:raise ValueError('Template outside difficulty')
 d=DATA[template];profile=profile or ('authored_shifted_bilinear:'+template if template=='q-161456' else 'authored:'+template)
 if profile not in (('observed:'+template,'authored:'+template,'authored_shifted_bilinear:'+template) if template=='q-161456' else ('observed:'+template,'authored:'+template)):raise ValueError('Complete bank profile belongs to its own template')
 for attempt in range(100):
  if parameters is not None:p=exact_parameters(template,parameters)
  elif d['kind']=='symbolic':p={'function':rng.choice(['g','h','k','f','s','w'])}
  else:
   permitted={'q-161449':[(2,1),(1,2)],'q-161456':[(1,1)],'q-161453':[(2,1),(1,2)],'q-161455':[(1,3),(3,1)]}[template]
   a,b=rng.choice(permitted);p={'c':rng.choice([i for i in range(-9,10) if i]),'m':a,'n':b}
   if template=='q-161456':p.update({k:rng.randint(-2,2) if profile.startswith('authored_shifted_bilinear:') else 0 for k in ('a','b','h')})
  if template=='q-161456' and not profile.startswith('authored_shifted_bilinear:') and any(p.get(k,0) for k in ('a','b','h')):raise ValueError('Nonzero offsets require the labeled authored shifted-bilinear profile')
  try:values,recipes=bank(template,p)
  except ValueError:
   if parameters is not None:raise
   continue
  break
 else:raise ValueError('No eligible whole bank')
 m=math_data(template,p);slots=slot_values(template,p,m)
 problem=substitute(d['prompt_template'],slots);solution=substitute(d['solution_template'],slots)
 if d['kind']=='symbolic':problem=rename_function(problem,template,p);solution=rename_function(solution,template,p)
 if profile.startswith('authored'):problem=explicit_boxes(template,problem)
 # Normalize graph function spelling in mathematical fingerprint; masks/profile/renaming do not invent tasks.
 canonical=str(m['graph']).replace(p.get('function','!')+'(', 'f(') if d['kind']=='symbolic' else str(sp.expand(m['graph']))
 fp=digest({'axis':d['axis'],'graph':canonical,'orientation':'positive_'+d['axis'],'assessed':'Cartesian flux formula'})
 content=digest({'version':VERSION,'problem':problem,'solution':solution,'bank':sorted(values),'parameters':fp})
 qid=uuid.uuid5(uuid.NAMESPACE_URL,f'{KP_UUID}/{content}');fid=uuid.uuid5(qid,'selection');choices=[]
 for i,value in enumerate(values):
  aid=str(uuid.uuid5(fid,value));choices.append({':answer/id':aid,':answer/type':d['answer_type'],':answer/value':value})
  if i==d['correct_index']:correct=aid
 rng.shuffle(choices)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},
 'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,'parameter_fingerprint':fp,'content_fingerprint':content,'bank_profile':profile,'bank_origin':'observed' if profile.startswith('observed:') else 'authored_parameter_extension_of_observed_operations','source_analysis':{k:RAW[k] for k in ('database','basis','lineage')},'source_question_id':d['source_id'],'authored_extension':profile.startswith('authored') or p!=exact_parameters(template,d['original_parameters']),'extension_kind':'translated_bilinear' if profile.startswith('authored_shifted_bilinear:') else 'exponent_role_or_coefficient_variation','plot_rating':'none','plot_assets':{},'domain':'D in the displayed coordinate plane; differentiable graph','orientation':'positive_'+d['axis'],'source_solution_repairs':d['repairs'],'answer_recipes':dict(zip(values,recipes)),'math':{k:[str(t) for t in value] if isinstance(value,sp.MatrixBase) else str(value) for k,value in m.items()}}}
# Easy: upward graph formula masks or two first partials of quadratic-linear monomial.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: positive-i formula masks or two first partials of a shifted bilinear graph.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: positive-j orientation reversal; same two-partial monomial formula, no flux evaluation.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def display_answer(a):return '$'+a[':answer/value']+'$' if a[':answer/type']==':answer.type/math' else a[':answer/value']
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- '+display_answer(a)+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']+'\n'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n'.join(map(markdown,records)))
if __name__=='__main__':main()
