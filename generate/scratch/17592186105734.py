#!/usr/bin/env python3
"""Altitude from vertices, math basis 1356; local review records only.

API generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), plus generate_easy/moderate/hard. Source templates preserve entire
prompt/prose and ordered arithmetic masks (not literal question replay). All
source banks use explicit observational scale profiles: scalar error intent is
underdetermined. Default five-option bank instead derives complete method errors.
Whole-bank collisions/domain failures reject an instance. Authored E/M are design
claims anchored to the same canonical method, not recovered difficulty labels.
Fingerprint uses base/apex Gram geometry modulo reversing the base endpoints,
excluding translation, rigid orientation, names, seed and banks. Content identity
includes actual prompt, solution and complete sorted bank. No EDB dependencies.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, re, uuid
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parent/'17592186105734'
VERSION='altitude-v1.0'
KP={'db_id':17592186105734,'id':'9331987e-8676-5bdb-b4ce-2129b1b09a8c','title':'Calculating the Altitude of a Triangle Given Its Vertices'}
TEMPLATES=json.loads((ROOT/'templates.json').read_text())
PROFILES=json.loads((ROOT/'profiles.json').read_text())
NS=uuid.UUID(KP['id'])
def tex(x):return S.latex(S.simplify(x)).replace(' ','')
def uid(x):return str(uuid.uuid5(NS,x))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def vec(x,zeros=()):
 out=''
 for n,k in zip(x,'ijk'):
  if n==0 and k not in zeros:continue
  term=(str(abs(n)) if abs(n)!=1 else '')+k if n else '0'+k
  out+=('-' if n<0 else ('+' if out else ''))+term
 return out or '0'
def wrapped(x):
 t=vec(x);return '('+t+')' if sum(n!=0 for n in x)>1 or t.startswith('-') else t

def par(n):return '('+str(n)+')' if n<0 else str(n)
def sq(n):return ('('+str(n)+')' if n<0 else '{'+str(n)+'}')+'^{2}'
def tupletex(x):return '⟨'+','.join(map(str,x))+'⟩'
def vector_arrow(x):return r'\overset{\to }{'+x+'}'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def normrows(label,formal,x,with_raw,punct):
 n=sum(i*i for i in x); val=tex(S.sqrt(n))
 rows=[label+' & ='+formal,' & ='+r'\sqrt{'+ '+'.join(sq(i) for i in x)+'}']
 if with_raw:rows.append(' & ='+r'\sqrt{'+str(n)+'}')
 rows.append(' & ='+val+punct)
 return aligned(rows)
def mathdata(p,t):
 pts={k:S.Matrix(v) for k,v in p['vertices'].items()}
 names=t['edges']; u=pts[names[0][1]]-pts[names[0][0]];v=pts[names[1][1]]-pts[names[1][0]]
 base=pts[t['base'][1]]-pts[t['base'][0]];w=u.cross(v); l2=base.dot(base);n2=w.dot(w)
 if not l2 or not n2:raise ValueError('Nondegenerate triangle and nonzero base required')
 return [int(x) for x in u],[int(x) for x in v],[int(x) for x in w],[int(x) for x in base],S.sqrt(n2),S.sqrt(l2),S.sqrt(n2)/S.sqrt(l2)
def blocks(p,t):
 u,v,w,base,N,L,h=mathdata(p,t);e,f=t['edges'];alt=t['alt'];bn=t['base'];area=N/2
 blocks=[t['initial']]
 rows=[]
 for name,x,z in zip((e,f),(u,v),t.get('edge_zeros',[[],[]])):
  a,b=name;sub=wrapped(p['vertices'][b])+'-'+wrapped(p['vertices'][a])
  rows.extend([vector_arrow(name)+' & ='+b.lower()+'-'+a.lower(),' & ='+sub,' & ='+vec(x,z),' & ='+tupletex(x)])
 blocks.append(aligned(rows))
 def det(indices):
  return r'|\begin{aligned}'+ ' & '.join(str(u[i]) for i in indices)+r' \\ '+ ' & '.join(str(v[i]) for i in indices)+r'\end{aligned}|'
 main=r'|\begin{aligned}i & j & k \\ '+' & '.join(map(str,u))+r' \\ '+' & '.join(map(str,v))+r'\end{aligned}|'
 expansion=det((1,2))+'i-'+det((0,2))+'j+'+det((0,1))+'k'
 operands=[(u[1],v[2],u[2],v[1]),(u[0],v[2],u[2],v[0]),(u[0],v[1],u[1],v[0])]
 terms=[]
 for i,(a,b,c,d) in enumerate(operands):
  if t['swap'][i]:c,d=d,c
  dot1='' if t.get('implicit',[False]*3)[i] else r'\cdot '
  first_second=('('+str(b)+')') if not dot1 and b>=0 else par(b)
  terms.append('('+par(a)+dot1+first_second+'-'+par(c)+r'\cdot '+par(d)+')'+'ijk'[i])
 arithmetic=terms[0]+'-'+terms[1]+'+'+terms[2]
 blocks.append(aligned([vector_arrow(e)+r'\times '+vector_arrow(f)+' & ='+main,' & ='+expansion,' & ='+arithmetic,' & ='+vec(w,t.get('cross_zeros',[])),' & ='+tupletex(w)+'.']))
 blocks.append(normrows('A','|'+vector_arrow(e)+r'\times '+vector_arrow(f)+'|',w,t['cross_raw'],'.'))
 fraction=r'\frac{'+tex(N)+'}{2}'
 ar=t['area_prefix']+fraction
 if t['area_simplify']:ar+='='+tex(area)
 blocks.append(ar+'.')
 blocks.append(normrows(bn,'|'+vector_arrow(bn)+'|',base,t['base_raw'],t['base_punct']))
 half=r'\frac{1}{2}'+t.get('alt_space','')+alt+r'\cdot '
 # Reduce only the numeric factor common to both sides, retaining source's
 # distinct substituted/reduced/quotient/rationalized stages.
 cn,_=S.sqrt(sum(i*i for i in w)).as_coeff_Mul();cl,_=L.as_coeff_Mul();g=S.gcd(cn,cl)
 num=N/g;den=L/g
 rows=[]
 if t['final_mode']=='full':rows.append(r'{A}_{△} & ='+r'\frac{1}{2}'+t.get('formal_altspace','')+alt+r'\cdot '+bn)
 rows.append(tex(area)+' & ='+half+tex(L))
 if t['final_mode']=='full':
  rhs=(tex(den)+r'\,'+alt) if t.get('reversed_reduced') else alt+r'\cdot '+tex(den)
  rows.append(tex(num)+' & ='+rhs)
 else:num,den=N,L
 rows.append(alt+' & ='+r'\frac{'+tex(num)+'}{'+tex(den)+'}')
 rows.append(('' if t.get('final_empty') else alt)+' & ='+tex(h)+'.')
 blocks.append(aligned(rows))
 return blocks

def render(p,t):
 prompt=t['prompt']
 for name,style in t['coordinate_styles'].items():
  vals=p['vertices'][name];coord=','.join(t.get('coordinate_prefixes',{}).get(name,['','',''])[i]+str(n)+style[i] for i,n in enumerate(vals))
  prompt=prompt.replace('@'+name+'@',coord)
 sol=t['solution']
 for i,b in enumerate(blocks(p,t)):sol=sol.replace('@BLOCK'+str(i)+'@',b)
 return prompt,sol

def field_kind(x):
 if x is None:return None
 x=x.rsplit('/',1)[-1]
 if x not in ('radio','blank'):raise ValueError('Only radio and blank are supported')
 return x

def guard(p,t,level,observed):
 if set(p)!= {'vertices'} or set(p['vertices'])!=set(t['coordinate_styles']):raise ValueError('Exactly the named vertices are required')
 for x in p['vertices'].values():
  if len(x)!=3 or any(type(n)!=int or abs(n)>12 for n in x):raise ValueError('Bounded integer triples required')
 u,v,w,b,N,L,h=mathdata(p,t)
 if observed:
  products=sum(a!=0 and b!=0 for a,b in [(u[1],v[2]),(u[2],v[1]),(u[0],v[2]),(u[2],v[0]),(u[0],v[1]),(u[1],v[0])])
  if max(map(abs,u+v))>8 or sum(n!=0 for n in b)<2 or products<3:raise ValueError('Observed hard scope requires a non-axis base, at least three determinant products and bounded edge arithmetic')
  return
 nonzero_products=sum(a!=0 and b!=0 for a,b in [(u[1],v[2]),(u[2],v[1]),(u[0],v[2]),(u[2],v[0]),(u[0],v[1]),(u[1],v[0])])
 m=max(map(abs,u+v));b2=sum(i*i for i in b)
 if level=='easy':
  if not (u[2]==v[2]==0 and all(u[i] and v[i] for i in (0,1)) and m<=3 and abs(w[2])<=8 and math.gcd(abs(b[0]),abs(b[1]))==1 and b2>=5):raise ValueError('Easy requires a non-axis planar two-product determinant and primitive nonunit base; small coefficients')
 elif level=='moderate':
  if not (sum(n!=0 for n in b)==2 and all(v) and all(w) and m<=3 and 5<=b2<=13 and nonzero_products==4):raise ValueError('Moderate requires four nonzero determinant products, 3D geometry and two-component base')
 elif level=='hard':
  if not (3<=m<=5 and nonzero_products>=5 and all(w) and 5<=b2<=50 and math.gcd(*map(abs,b))==1):raise ValueError('Authored hard requires five/six products, nontrivial signed arithmetic and primitive base')
 else:raise ValueError('Unknown difficulty')

def options(p,t,profile):
 u,v,w,b,N,L,h=mathdata(p,t)
 if t['field']=='blank':return [S.simplify(h)],['correct']
 if profile in PROFILES:
  data=PROFILES[profile];values=[S.simplify(h*S.sympify(r)) for r in data['ratios']];recipes=['observed_scale_'+str(i) for i in range(5)]
 else:
  if profile!='method_errors':raise ValueError('Unknown profile')
  values=[h,h/2,2*h,N,N/(L**2)];recipes=['correct','triangle_area_divided_by_base','parallelogram_used_as_triangle','base_division_omitted','squared_base_used']
 values=[S.simplify(x) for x in values]
 if any(x.is_real is not True or x.is_positive is not True for x in values):raise ValueError('Whole bank rejected: nonpositive/nonreal value')
 if any(S.simplify(a-b)==0 for i,a in enumerate(values) for b in values[i+1:]):raise ValueError('Whole bank rejected: equivalent choices')
 if sum(S.simplify(x-h)==0 for x in values)!=1:raise ValueError('Whole bank rejected: correct answer absent/ambiguous')
 return values,recipes

def sample(level,rng,t):
 # Unordered peer instances: arithmetic counts are identical within E/M.
 for _ in range(20000):
  if level=='easy':u=[rng.choice([-3,-2,-1,1,2,3]),rng.choice([-3,-2,-1,1,2,3]),0];v=[rng.choice([-3,-2,-1,1,2,3]),rng.choice([-3,-2,-1,1,2,3]),0]
  elif level=='moderate':u=[rng.choice([-3,-2,-1,1,2,3]),rng.choice([-3,-2,-1,1,2,3]),0];v=[rng.choice([-3,-2,-1,1,2,3]) for _ in range(3)]
  else:u=[rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) for _ in range(3)];v=[rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) for _ in range(3)]
  # Source layouts can put the base in either edge position.
  if t['base']==t['edges'][1]:u,v=v,u
  a=t['edges'][0][0];e=t['edges'][0][1];f=t['edges'][1][1];origin=[rng.randint(-2,2) for _ in range(3)]
  p={'vertices':{a:origin,e:[x+y for x,y in zip(origin,u)],f:[x+y for x,y in zip(origin,v)]}}
  try:guard(p,t,level,False);options(p,t,'method_errors');return p
  except ValueError:continue
 raise ValueError('No eligible whole-bank instance sampled')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 rng=random.Random(seed);kind=field_kind(field_type)
 if template is None:
  template='authored_'+level+('_blank' if kind=='blank' else '_radio')
 if template not in TEMPLATES:raise ValueError('Unknown template')
 t=TEMPLATES[template]
 if t['level']!=level:raise ValueError('Template difficulty mismatch')
 if kind is not None and kind!=t['field']:raise ValueError('Field layout is fixed by template')
 profile=profile or ('none' if t['field']=='blank' else 'method_errors')
 if t['field']=='blank' and profile!='none':raise ValueError('Blanks have no distractor profile')
 observed=profile in PROFILES or t['authorship'].startswith('observed')
 if profile in PROFILES and PROFILES[profile]['template']!=template:raise ValueError('Profile belongs to a different observed template')
 p=parameters if parameters is not None else sample(level,rng,t)
 guard(p,t,level,observed);values,recipes=options(p,t,profile)
 prompt,solution=render(p,t);h=mathdata(p,t)[-1]
 bank=[tex(v) for v in values];cid=digest([VERSION,prompt,solution,sorted(bank),t['field'],t['key']])
 qid=uid('question:'+cid);fid=uid('field:'+cid+':'+t['key'])
 choices=[{':answer/id':uid('answer:'+fid+':'+value),':answer/type':':answer.type/math',':answer/value':value} for value in bank]
 correct=next(a[':answer/id'] for a,v in zip(choices,values) if S.simplify(v-h)==0);rng.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':t['key'],':answer-field/type':':answer-field.type/'+t['field'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}
 # Gram geometry invariant under arbitrary rigid motion and vertex aliases.
 pts=p['vertices'];a,b=t['base'];c=t['alt'][0];U=S.Matrix(pts[b])-S.Matrix(pts[a]);V=S.Matrix(pts[c])-S.Matrix(pts[a]);g=(int(U.dot(U)),int(V.dot(V)),int(U.dot(V)));rev=(g[0],g[1]+g[0]-2*g[2],g[0]-g[2]);geom=min(g,rev)
 return {'knowledge_point':dict(KP),'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'domain':'noncollinear integer vertices; positive exact lengths','recipes':recipes,'source_ids':t.get('source_ids',[]),'authorship':t['authorship'],'plot_rating':'none','mathematical_fingerprint':digest(geom),'content_fingerprint':cid,'provenance':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}}}

# Easy: authored planar non-axis base; two nonzero determinant products.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: authored 3D peers; four products and three nonzero cross components.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: all observed layouts plus authored five/six-product full calculation.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];lines=[q[':question/problem']]
 for f in q[':question/answer-fields']:
  lines+=['\n'+f[':answer-field/type']]+['- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']]
 lines+=['\nWorked solution\n',q[':question/worked-solution']]
 return '\n'.join(lines)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,args.template,args.field_type,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
