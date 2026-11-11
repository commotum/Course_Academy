#!/usr/bin/env python3
"""Two signed vector scale readings. All assets belong to the explicit output directory."""
from __future__ import annotations
import argparse, hashlib, json, os, random, uuid
from fractions import Fraction as F
from pathlib import Path
from math_format import normalize_prose, normalize_tex, validate_generated_record
from diagram import render
KP={'db_id':17592186096652,'id':'45b6a076-8795-5510-aabc-62a925826dd0','title':'Finding Two Scalar Factors in a Linear Combination'}
NS=uuid.UUID(KP['id']); VERSION='vector-two-scalars-3'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(NS,x))
def tex(x):
 x=F(x)
 return str(x.numerator) if x.denominator==1 else ('-' if x<0 else '')+r'\frac{'+str(abs(x.numerator))+'}{'+str(x.denominator)+'}'
def term(x,name):
 return ('-' if x<0 else '')+name if abs(x)==1 else tex(x)+name
def total(a,b):return term(a,r'\mathbf{a}')+('+' if b>0 else '')+term(b,r'\mathbf{b}')
def movement(p):
 parts=[]
 for value,pos,neg in [(p[0],'right','left'),(p[1],'up','down')]:
  if value:parts.append(f'${abs(value)}$ '+('square' if abs(value)==1 else 'squares')+' '+(pos if value>0 else neg))
 return ' and '.join(parts)
def add(p,q):return [p[i]+q[i] for i in (0,1)]
def mul(c,p):return [int(c*x) if (c*x).denominator==1 else float(c*x) for x in map(F,p)]
def transform(p,k):
 x,y=p
 if k>=4:x=-x
 for _ in range(k%4):x,y=-y,x
 return [x,y]
def sample(level,rng):
 # Decide signed scale roles before lengths, reference-slot assignments, and orientations.
 if level=='easy':a,b=map(F,[rng.randint(1,4),rng.randint(1,4)])
 else:
  profile=rng.choice(['integer','half'])
  signs=rng.choice([(-1,-1),(-1,1),(1,-1)] if level=='moderate' and profile=='integer' else [(-1,-1),(-1,1),(1,-1),(1,1)])
  a=(F(rng.randint(1,3)) if profile=='integer' else rng.choice([F(1,2),F(3,2),F(5,2)]))*signs[0]
  b=F(rng.randint(1,3))*signs[1]
  if rng.randrange(2):a,b=b,a
 first=rng.randrange(2)
 # A denominator-scaled basis makes every endpoint a visible grid intersection.
 u=[0,a.denominator*rng.choice([1,2])] if level!='hard' else [a.denominator*rng.choice([1,2]),a.denominator]
 v=[b.denominator*rng.choice([1,2]),b.denominator*rng.choice([1,2])]
 if level=='hard' and u[0]*v[1]==u[1]*v[0]:v[1]+=b.denominator
 if rng.randrange(2):u,v=v,u
 # Swapping reference shapes must keep integral endpoints for the selected fractions.
 if any(F(x)*a%1 for x in u) or any(F(x)*b%1 for x in v):
  u=[int(F(x)*a.denominator) for x in u];v=[int(F(x)*b.denominator) for x in v]
 k=rng.randrange(8);u=transform(u,k);v=transform(v,k)
 return dict(level=level,a=str(a),b=str(b),u=u,v=v,first=first,origin=[0,0])
def instance_signature(s):
 # Ignore global grid isometries, names/slot exchange and drawing order.
 u,v=s['u'],s['v'];a,b=F(s['a']),F(s['b'])
 possibilities=[]
 for k in range(8):
  x,y=transform(u,k),transform(v,k)
  possibilities += [json.dumps([x,y,str(a),str(b)]),json.dumps([y,x,str(b),str(a)])]
 return min(possibilities)
def build(s,out):
 a,b=F(s['a']),F(s['b']);u,v=s['u'],s['v'];assert u[0]*v[1]-u[1]*v[0]
 target=add(mul(a,u),mul(b,v));corner=mul(a,u) if s['first']==0 else mul(b,v)
 geometry={**s,'target':target,'corner':corner,'renderer_version':5}
 name=digest(geometry)[:24];assets=[]
 for solution in (False,True):
  rel='vector-'+name+('-solution' if solution else '-prompt')+'.png'
  render(geometry,out/rel,solution);assets.append(rel)
 problem=('The vectors are drawn on a square grid: $\\overrightarrow{OA}=\\mathbf{a}$, $\\overrightarrow{OB}=\\mathbf{b}$, and $\\overrightarrow{OC}=\\mathbf{c}$.\n\n'
  f'![Vector diagram]({assets[0]})\n\n'
  r'Given that $\mathbf{c}=\lambda\mathbf{a}+\mu\mathbf{b}$, find $\lambda$ and $\mu$.'
  '\n\n$\\lambda=$ {{field-1}}\n\n$\\mu=$ {{field-2}}')
 ordered=[(a,u,'a'),(b,v,'b')]
 if s['first']:ordered.reverse()
 explanations=[]
 for i,(c,vec,n) in enumerate(ordered):
  displacement=mul(c,vec);seg='OX' if i==0 else 'XC'
  explanations.append(f'Along ${seg}$, move {movement(displacement)}. '
   f'A copy of $\\mathbf{{{n}}}$ moves {movement(vec)}. '
   f'Thus ${seg}={tex(abs(c))}|\\mathbf{{{n}}}|$ and the segment points in the '+('same' if c>0 else 'opposite')+
   f' direction to $\\mathbf{{{n}}}$. Hence $\\overrightarrow{{{seg}}}={term(c,"\\mathbf{"+n+"}")}$.')

 c1,_,n1=ordered[0];c2,_,n2=ordered[1]
 path=term(c1,'\\mathbf{'+n1+'}')+('+' if c2>0 else '')+term(c2,'\\mathbf{'+n2+'}')
 rows=[r'\mathbf{c}&=\overrightarrow{OX}+\overrightarrow{XC}', '&='+path]
 if s['first']:rows.append('&='+total(a,b))
 solution=(f'![Completed vector route]({assets[1]})\n\nConstruct the route $O\\to X\\to C$, '
  f'first parallel to $\\mathbf{{{n1}}}$ and then parallel to $\\mathbf{{{n2}}}$.\n\n'+
  '\n\n'.join(explanations)+'\n\n$$\n\\begin{aligned}\n'+r'\\'.join(rows)+'\n\\end{aligned}\n$$\n\n'+
  ('Reorder the terms to match their vector names. ' if s['first'] else '')+
  f'Since $\\mathbf{{a}}$ and $\\mathbf{{b}}$ are not parallel, their coefficients are unique. '
  f'Matching coefficients gives $\\lambda={tex(a)}$ and $\\mu={tex(b)}$.')
 fields=[{'key':'field-1','type':':answer-field.type/blank','answers':[{'type':':answer.type/math','value':tex(a),'correct':True}]},
         {'key':'field-2','type':':answer-field.type/blank','answers':[{'type':':answer.type/math','value':tex(b),'correct':True}]}]
 return record(s['level'],problem,solution,fields,{'version':VERSION,'template':'two-scales-'+s['level'],'instance':geometry,'semantic_signature':instance_signature(s),'source_ids':['q-326018','q-326022'] if s['level']=='easy' else ['q-326014','q-327074','q-326016'],'source_basis':14174})
def record(level,problem,solution,specs,metadata):
 problem=normalize_prose(problem);solution=normalize_prose(solution)
 specs=json.loads(json.dumps(specs))
 for f in specs:
  for a in f['answers']:a['value']=(normalize_tex if a['type']==':answer.type/math' else normalize_prose)(a['value'])
 identity=digest([VERSION,level,problem,solution,specs]);qid=uid(identity);fields=[]
 for f in specs:
  fid=uid(qid+'/'+f['key']);choices=[];correct=None
  for a in f['answers']:
   aid=uid(fid+'/'+a['value']);choices.append({':answer/id':aid,':answer/type':a['type'],':answer/value':a['value']})
   if a['correct']:correct=aid
  assert correct
  fields.append({':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':f['type'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]})
 r={'knowledge_point':KP,'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},'generation':metadata}
 validate_generated_record(r);return r
def replay(source_id):
 rows=json.loads(Path(__file__).with_name('source_replay.json').read_text());s=next(x for x in rows if x['id']==source_id)
 return record(s['difficulty'],s['problem'],s['solution'],s['fields'],{'version':VERSION,'template':'source-replay','source_id':s['id'],'source_db_id':s['db_id'],'source_basis':14174,'presentation_repair':s['id']=='q-275128'})
def generate_batch(level,count,seed,out):
 if count<0:raise ValueError('count must be nonnegative')
 rng=random.Random(seed);records=[];seen=set();attempts=0
 while len(records)<count:
  attempts+=1
  if attempts>max(1000,count*100):raise ValueError('Requested batch exceeds fresh supported instance capacity')
  s=sample(level,rng);signature=instance_signature(s)
  if signature in seen:continue
  seen.add(signature);r=build(s,out);r['generation']['seed']=seed;records.append(r)
 return records
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all','unclassified'],default='moderate');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');p.add_argument('--source-id');args=p.parse_args()
 if args.source_id:records=[replay(args.source_id)]
 else:
  output=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
  if not output:p.error('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required')
  out=Path(output);out.mkdir(parents=True,exist_ok=True)
  levels=['easy','moderate','hard'] if args.difficulty=='all' else ['moderate' if args.difficulty=='unclassified' else args.difficulty]
  records=[r for level in levels for r in generate_batch(level,args.count,args.seed,out)]
 print(json.dumps(records,indent=2,ensure_ascii=False))
