#!/usr/bin/env python3
"""Flux across fixed type I/II regions; source-bank-covariant field scaling.

Positive integer scaling changes the differentiated field and exact flux, without
changing region geometry, reasoning stages, or five-option radio contracts.
Distractor interpretations remain unresolved; complete source banks are scaled
as mathematical objects, never pooled. No easy source supports an easy band.
"""
import argparse, hashlib, importlib.util, json, random, re, uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('')
sp=importlib.util.spec_from_file_location('flux_math_parser',HERE/'math_parser.py')
p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
x,y=p.x,p.y
KP_ID=17592186172099
KP_UUID='629dd9d1-1c53-5a04-97bf-5799e71b9573'
TITLE="Calculating Flux Across Other Type I and Type II Regions"
VERSION='flux-fixed-regions-covariant-banks-v1'
LEVELS=('moderate','hard')
CAPTURE=json.loads((HERE/'reference/initial/source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['kp'][':knowledge-point/questions']}
EXCLUDED={'q-127316':'Square-root spectator terms lack continuous first partial derivatives on an open neighborhood of the boundary; conservative exclusion under the stated theorem.',
 'q-127318':'sqrt(x) is not real for negative x in the cosine region. Also square-root derivatives fail at the boundary. Source solution contains an integral with equal lower/upper limits.'}
# inner variable, lower/upper inner limits, outer variable and limits.
REGIONS={
 'q-126814':(x,-y,y,y,0,1),
 'q-126817':(y,0,x**2,x,0,1),
 'q-127309':(y,0,s.sqrt(x),x,0,2),
 'q-127316':(y,0,s.sin(x),x,0,s.pi/2),
 'q-127323':(x,-2*y,2*y,y,0,1),
 'q-127325':(x,-y/2,y/2,y,0,2),
 'q-127365':(x,-s.sqrt(y),y,y,0,1),
 'q-127302':(y,0,x**3,x,0,1),
 'q-127328':(x,-y,s.sqrt(y),y,0,1),
 'q-127370':(x,1-y,s.exp(y),y,0,1),
 'q-127318':(y,0,s.cos(x),x,-s.pi/2,s.pi/2)}
REGIONS={k:tuple(s.sympify(v) for v in vs) for k,vs in REGIONS.items()}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,default=str).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def L(v):return s.latex(s.sympify(v),mul_symbol=None).replace(r'\log',r'\ln')
def scalar(t):return p.scalar(t.replace('\\\\','\\').replace(r'\;', '').replace(r'\:', '').replace(r'\quad', '').replace(r'\operatorname{arctan}', r'\arctan').replace(r'\operatorname{atan}', r'\arctan'))
def components(problem):
 m=re.search(r'(?:⟨|\\langle)(.*?)(?:⟩|\\rangle)',problem,re.S)
 assert m,problem
 a,b=m[1].replace(r'\,','').split(',')
 return scalar(a),scalar(b)
def bank(q):return [scalar(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
def symbolic(template,scale):
 q=SOURCES[template];P,Q=components(q[':question/problem']);P=s.expand(scale*P);Q=s.expand(scale*Q)
 inner,lo,hi,outer,a,b=REGIONS[template]
 dx,dy=s.diff(P,x),s.diff(Q,y);div=s.expand(dx+dy)
 primitive=s.integrate(div,inner);integrated=s.simplify(primitive.subs(inner,hi)-primitive.subs(inner,lo))
 antiderivative=s.integrate(integrated,outer);value=s.simplify(antiderivative.subs(outer,b)-antiderivative.subs(outer,a))
 return P,Q,dx,dy,div,primitive,integrated,antiderivative,value

def signature(q):
 P,Q=components(q[':question/problem'])
 # Ignore field components annihilated by the divergence. Equivalent divergence
 # on the same region is one task, regardless of UUID, seed, bank or option order.
 region=q[':question/problem'].split('through the boundary of ',1)[1]
 div=s.expand(s.diff(P,x)+s.diff(Q,y))
 return digest([s.srepr(div),region])

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unsupported difficulty; easy has no source evidence')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio is supported')
 rng=random.Random(seed)
 eligible=sorted(k for k,q in SOURCES.items() if k not in EXCLUDED and q[':question/difficulty'][':db/ident'].endswith('/'+level))
 template=template or rng.choice(eligible)
 if template not in eligible:raise ValueError('Excluded or wrong-difficulty template')
 if profile not in (None,template):raise ValueError('Complete bank profile must match source template')
 scale=(parameters or {}).get('scale',rng.randint(2,50))
 if type(scale) is not int or scale<1:raise ValueError('scale must be a positive integer')
 if parameters and set(parameters)!={'scale'}:raise ValueError('Undeclared parameter')
 source=SOURCES[template]
 P,Q,dx,dy,div,primitive,integrated,anti,value=symbolic(template,scale)
 inner,lo,hi,outer,a,b=REGIONS[template]
 problem=re.sub(r'(?:⟨|\\langle).*?(?:⟩|\\rangle)',lambda m:r'\left\langle '+L(P)+', \\; '+L(Q)+r' \right\rangle',source[':question/problem'],flags=re.S)
 asset=re.findall(r'!\[.*?\]\((.*?)\)',source[':question/worked-solution'])[0]
 prefix=source[':question/worked-solution'].split('The region $D$')[0]
 typ='I' if inner==y else 'II'
 region=(rf'{L(a)}\leq {outer}\leq {L(b)},\quad {L(lo)}\leq {inner}\leq {L(hi)}')
 eq=rf'\oint_C \mathbf F\cdot\mathbf n\,ds'
 solution=prefix+('The region $D$ and the curve $C$ for this case are shown below.\n\n'
  f'![]({asset})\n\n'+rf'We have that $P(x,y)={L(P)}$ and $Q(x,y)={L(Q)}.$ Therefore,'+'\n\n$$\n'+
  rf'\frac{{\partial P}}{{\partial x}}={L(dx)},\qquad \frac{{\partial Q}}{{\partial y}}={L(dy)}.'+'\n$$\n\n'+
  f'We can express the region $D$ as a type {typ} region as follows:\n\n$$\n'+rf'D=\{{(x,y):{region}\}}.'+'\n$$\n\n'+
  "Therefore, applying Green's theorem in flux form, we get\n\n$$\n"+r'\begin{aligned}'+
  eq+r'&=\oint_C P\,dy-Q\,dx \\'+
  r'&=\iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,dA \\'+
  rf'&=\iint_D\left({L(div)}\right)\,dA \\'+
  rf'&=\int_{{{L(a)}}}^{{{L(b)}}}\int_{{{L(lo)}}}^{{{L(hi)}}}\left({L(div)}\right)\,d{inner}\,d{outer} \\'+
  rf'&=\int_{{{L(a)}}}^{{{L(b)}}}\left[{L(primitive)}\right]_{{{inner}={L(lo)}}}^{{{inner}={L(hi)}}}\,d{outer} \\'+
  rf'&=\int_{{{L(a)}}}^{{{L(b)}}}\left({L(integrated)}\right)\,d{outer} \\'+
  rf'&=\left[{L(anti)}\right]_{{{outer}={L(a)}}}^{{{outer}={L(b)}}} \\'+
  rf'&=\left({L(anti.subs(outer,b))}\right)-\left({L(anti.subs(outer,a))}\right) \\'+
  rf'&={L(value)}.'+r'\end{aligned}'+'\n$$')
 values=[s.simplify(scale*v) for v in bank(source)]
 assert len(values)==5 and all(s.simplify(z-w)!=0 for i,z in enumerate(values) for w in values[i+1:])
 assert sum(s.simplify(z-value)==0 for z in values)==1
 identity={'version':VERSION,'template':template,'scale':scale,'problem':problem,'bank':sorted(map(s.srepr,values))}
 qid=uid(identity);fid=uid([qid,'selection']);answers=[{':answer/id':uid([fid,s.srepr(z)]),':answer/type':':answer.type/math',':answer/value':L(z)} for z in values]
 correct=next(z[':answer/id'] for z in answers if s.simplify(scalar(z[':answer/value'])-value)==0)
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,
 ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':template,'parameters':{'scale':scale},'source_id':template,'source_basis':CAPTURE['basis'],'mathematical_fingerprint':signature(q),'dependencies':{'sympy':s.__version__},'domain':'positive integer scale; source fixed region; smooth supported vector components','asset_refs':[asset]}}

def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--template');a.add_argument('--scale',type=int);a.add_argument('--format',choices=('json','markdown'),default='json');v=a.parse_args()
 records=[generate(l,v.seed+i,template=v.template,parameters={'scale':v.scale} if v.scale else None) for l in (LEVELS if v.difficulty=='all' else [v.difficulty]) for i in range(v.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if v.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
if __name__=='__main__':main()
