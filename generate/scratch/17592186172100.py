#!/usr/bin/env python3
"""Flux Green theorem: source-faithful banks with bounded positive field scaling.

Only easy and moderate are supported. Hard has no supported source evidence.
Run --difficulty easy|moderate --count N --seed N --format json|markdown.
Scale changes the field, divergence, every option and solution together. Seeds
and order do not create new identities. Catalog: 12 scales per source template.
"""
import argparse, hashlib, json, os, random, re, sys, uuid
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__':os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import checked_math_content, normalize_prose, normalize_tex
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP_ID=17592186172100
KP_UUID=SOURCE['record'][':knowledge-point/id']
TITLE=SOURCE['record'][':knowledge-point/title']
VERSION='flux-green-source-banks-1'
LEVELS=('easy','moderate')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
x,y=sp.symbols('x y')
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# Different polynomial structure, component roles, cancellation and solution
# stages remain separate templates, each retaining its own complete bank.
MODELS={
'q-127070':('x**2+1','y**2',None),
'q-127206':('y+2*x**2*y','x**2-x*y**2',None),
'q-127203':('2+x*y**2','3-x**2*y',None),
'q-127226':('x**4+y**3','(x**3+5)*y',None),
'q-127224':('x**2+y**2','x**3+y**3',None),
'q-127072':('x**2*y','5*x*y',[-1,2,0,2]),
'q-127229':('3*x*y**3','6*x*y**4',[-1,1,0,2]),
'q-127231':('y*x**2+y**3*x','-y**2*x+y**4',[-3,-1,-1,1]),
'q-127228':('x**2*y**2','12*x*y',[0,3,0,2]),
'q-127232':('6*x*y+y*x**2','-y**2',[-1,1,-1,2]),
}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def level_of(q):return q[':question/difficulty'][':db/ident'].split('/')[-1]
def group(s,start):
 assert s[start]=='{'
 depth=1
 for i in range(start+1,len(s)):
  depth+=(s[i]=='{')-(s[i]=='}')
  if depth==0:return s[start+1:i],i+1
 raise ValueError('Unclosed fraction')
def parse_poly(s):
 s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace('−','-')
 while r'\frac' in s:
  p=s.index(r'\frac');i=p+5
  a,i=group(s,i);b,j=group(s,i)
  s=s[:p]+'(('+str(parse_poly(a))+')/('+str(parse_poly(b))+'))'+s[j:]
 s=s.replace('{','(').replace('}',')').replace('^','**')
 return sp.expand(parse_expr(s,local_dict={'x':x,'y':y},transformations=standard_transformations+(implicit_multiplication_application,)))
def parse_value(s):
 if r'\int' not in s:return parse_poly(s)
 s=s.replace(r'{\int }',r'\int')
 matches=list(re.finditer(r'\\int\s*_\{([^}]+)\}\^\{([^}]+)\}',s))
 assert len(matches)==2,s
 tail=s[matches[-1].end():]
 cut=tail.index(r'\,\text{d}') if r'\,\text{d}' in tail else tail.index(r'\,\mathrm{d}')
 variables=re.findall(r'\\(?:text|mathrm)\{d\}([xy])',tail[cut:])
 assert len(variables)==2,s
 bounds=[tuple(sp.sympify(t) for t in m.groups()) for m in matches]
 # limits follow integration order, inside to outside, without evaluating.
 return sp.Integral(parse_poly(tail[:cut]),(dict(x=x,y=y)[variables[0]],*bounds[1]),(dict(x=x,y=y)[variables[1]],*bounds[0]))
def equivalent(a,b):
 if isinstance(a,sp.Integral) or isinstance(b,sp.Integral):
  return isinstance(a,sp.Integral) and isinstance(b,sp.Integral) and a.limits==b.limits and sp.expand(a.function-b.function)==0
 return sp.expand(a-b)==0
def times(v,scale):
 if isinstance(v,sp.Integral):return sp.Integral(scale*v.function,*v.limits)
 return scale*v
def tex(v):
 if isinstance(v,sp.Integral):
  inner,outer=v.limits
  return normalize_tex(r'\int_{'+str(outer[1])+'}^{'+str(outer[2])+r'}\int_{'+str(inner[1])+'}^{'+str(inner[2])+'}'+sp.latex(sp.factor(v.function))+r'\,\text{d}'+str(inner[0])+r'\,\text{d}'+str(outer[0]))
 return normalize_tex(sp.latex(sp.factor(v)))
def raw_tex(v):return normalize_tex(sp.latex(v))
def signature(rec):
 meta=rec['generation'];sid=meta['template'];s=meta['parameters']['scale'];p,q,b=MODELS[sid]
 div=sp.expand(s*(sp.diff(sp.sympify(p),x)+sp.diff(sp.sympify(q),y)))
 # The tested divergence and rectangle determine the mathematical task. Ignore
 # constant field terms, bank order, UUID, seed and nonassessed easy geometry.
 return digest([level_of(SOURCES[sid]),str(div),b])
def catalog(level):
 if level not in LEVELS:raise ValueError('Unsupported difficulty '+level+'; see capabilities.json')
 return [(sid,s) for sid,q in SOURCES.items() if level_of(q)==level for s in range(1,13)]
@checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None):
 options=catalog(level)
 if template:options=[v for v in options if v[0]==template]
 if not options:raise ValueError('Template not supported for difficulty')
 sid,scale=random.Random(seed).choice(options)
 if parameters is not None:
  assert set(parameters)=={'scale'}
  scale=parameters['scale'];assert type(scale)==int and 1<=scale<=12
 if profile not in (None,sid):raise ValueError('Each source has its own complete profile')
 source=SOURCES[sid];p0,q0,bounds=MODELS[sid]
 p,q=scale*sp.sympify(p0),scale*sp.sympify(q0)
 px,qy=sp.diff(p,x),sp.diff(q,y);div=sp.expand(px+qy)
 correct=sp.Integral(div,(y,bounds[2],bounds[3]),(x,bounds[0],bounds[1])) if bounds else div
 sf=source[':question/answer-fields'][0]
 values=[times(parse_value(a[':answer/value']),scale) for a in sf[':answer-field/choices']]
 match=[i for i,v in enumerate(values) if equivalent(v,correct)]
 assert len(match)==1
 assert sf[':answer-field/choices'][match[0]][':answer/id']==sf[':answer-field/correct'][':answer/id']
 assert all(not equivalent(a,b) for i,a in enumerate(values) for b in values[i+1:])
 fieldtex=r'\langle '+raw_tex(p)+','+raw_tex(q)+r'\rangle' if level=='easy' else '('+raw_tex(p)+r')\,i+('+raw_tex(q)+r')\,j'
 problem=re.sub(r'\$F\(x,y\)=.*?\$',lambda m:'$F(x,y)='+fieldtex+'$',source[':question/problem'],count=1,flags=re.S)
 assert problem!=source[':question/problem']
 intro=source[':question/worked-solution'].split('The region $D$')[0]
 image=re.search(r'!\[.*?\]\(.*?\)',source[':question/worked-solution'])[0]
 solution=intro+'The region $D$ and the curve $C$ for this case are shown below.\n\n'+image+'\n\n'
 solution+='We have that $P(x,y)='+raw_tex(p)+'$ and $Q(x,y)='+raw_tex(q)+'.$ So,\n\n$$\n'+r'\frac{\partial P}{\partial x}='+raw_tex(px)+r',\qquad \frac{\partial Q}{\partial y}='+raw_tex(qy)+' .\n$$\n\n'
 if bounds:
  a,b,c,d=bounds
  solution+='We can express the region $D$ as a type I region as follows:\n\n$$\n'+r'D=\{(x,y):'+str(a)+r'\le x\le '+str(b)+r',\ '+str(c)+r'\le y\le '+str(d)+r'\}'+' .\n$$\n\n'
 solution+="Therefore, applying the flux form of Green's theorem, we get\n\n$$\n"+r'\begin{aligned}\oint_C P\,\text{d}y-Q\,\text{d}x &= \iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,\text{d}A \\ &=\iint_D\left(('+raw_tex(px)+')+('+raw_tex(qy)+r')\right)\,\text{d}A \\ &='+ (tex(correct) if bounds else r'\iint_D '+tex(div)+r'\,\text{d}A')+r'.\end{aligned}'+'\n$$'
 if not bounds:solution+='\n\nHence, $f(x,y)='+tex(div)+'.$'
 problem,solution=normalize_prose(problem),normalize_prose(solution)
 bank=[normalize_tex(a[':answer/value']) if scale==1 else tex(v) for a,v in zip(sf[':answer-field/choices'],values)]
 cid=digest([VERSION,level,problem,solution,sorted(bank),bank[match[0]]])
 qid=uid(cid);fid=uid([cid,'selection'])
 answers=[{':answer/id':uid([fid,value]),':answer/type':':answer.type/math',':answer/value':value} for value in bank]
 question={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[match[0]][':answer/id']]}]}
 rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'template':sid,'profile':sid,'seed':seed,'parameters':{'scale':scale},'domain':'positive integer scale 1..12; x,y real; fixed source polygon','source_basis':SOURCE['basis'],'source_question':sid,'sympy':sp.__version__,'plot_policy':'reuse unchanged source region','recipe_policy':'each complete source bank multiplied by scale; no pooled distractors'}}
 rec['generation']['mathematical_fingerprint']=signature(rec)
 return rec
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=(*LEVELS,'hard','all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('json','markdown'),default='markdown');parser.add_argument('--template');parser.add_argument('--scale',type=int)
 args=parser.parse_args();records=[]
 for level in LEVELS if args.difficulty=='all' else (args.difficulty,):
  candidates=catalog(level)
  if args.template:candidates=[v for v in candidates if v[0]==args.template]
  if args.scale is not None:candidates=[v for v in candidates if v[1]==args.scale]
  if args.count>len(candidates):raise ValueError('Finite catalog exhausted: requested '+str(args.count)+' from '+str(len(candidates)))
  random.Random(args.seed).shuffle(candidates)
  records.extend(generate(level,args.seed,template=sid,parameters={'scale':s}) for sid,s in candidates[:args.count])
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
if __name__=='__main__':main()
