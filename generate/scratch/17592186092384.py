#!/usr/bin/env python3
"""Normal-slope source templates. Bounded coefficient-scale extension; no plots."""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 import os,sys
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
HERE=Path(__file__).with_suffix('');SOURCE=json.loads((HERE/'source.json').read_text())
KP_ID=17592186092384;KP_UUID='4a05f6c0-98ab-5197-922e-8e8dff1d4302';TITLE=SOURCE['record'][':knowledge-point/title']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'));VERSION='1.0.0';SUPPORTED_LEVELS=('easy',)
x=sp.Symbol('x',real=True)
# Every complete rated source retains its own Markdown/solution and bank profile.
SPECS={
 'q-308798':(x**2+3*x,-1), 'q-342142':(4-3*x**2,1),
 'q-342147':(x**5/4-4*x**2,2), 'q-342152':(2*x**3-x**-4,-1),
 'q-342153':(4-x**sp.Rational(-1,2),sp.Rational(1,4)),
 'q-103531':(2*x**sp.Rational(3,2)-2*x**2,1),
 'q-103532':(x**3-4*x**sp.Rational(5,2),1),
 'q-103543':(2*x**-5+7*x,1),'q-47449':(x**2+x,1),'q-71524':(x**2-5,2)}
ROWS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def expression(t):
 t=t.replace('\\\\','\\')
 t=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',t)
 return sp.sympify(t)
def task(mid,scale=1):
 f,p=SPECS[mid];f=sp.expand(scale*f);d=sp.diff(f,x);y=sp.simplify(f.subs(x,p));m=sp.simplify(d.subs(x,p));assert m!=0
 return f,p,y,d,m,sp.simplify(-1/m)
def fingerprint_expr(f,p):return digest({'curve':sp.srepr(sp.expand(sp.powdenest(f,force=True))),'abscissa':str(p)})
def bank(mid,s):
 f,p,y,d,m,a=task(mid,s)
 if mid=='q-103531':return [m,-sp.Rational(5,2)*s,-1/(-sp.Rational(5,2)*s),a,1/(-sp.Rational(5,2)*s)]
 if mid=='q-103532':return [-sp.Integer(1),1/m,-m,m,a]
 if mid=='q-103543':return [sp.Integer(1),1/m,a,m,-m]
 if mid=='q-47449':return [1/m,-sp.Integer(1),1/(2*sp.Integer(s)*p),-1/(2*sp.Integer(s)*p),a]
 if mid=='q-71524':return [a,m/(5*sp.Integer(s)),m,-2*sp.Integer(s),1/m]
 return [a]
def generate_profile(mid,scale,seed=0):
 assert mid in SPECS and scale in range(1,13)
 original=ROWS[mid];f,p,y,d,m,a=task(mid,scale);values=list(map(sp.simplify,bank(mid,scale)))
 if len(set(values))!=len(values) or values.count(a)!=1:raise ValueError('Ambiguous bank')
 fp=fingerprint_expr(f,p);qid=uid('question:'+fp+':'+mid);fid=uid(qid+':field');of=original[':question/answer-fields'][0]
 answers=[{':answer/id':uid(fid+':'+str(v)),':answer/type':':answer.type/math',':answer/value':sp.latex(v)} for v in values]
 correct=answers[values.index(a)][':answer/id']
 if scale==1:
  problem=original[':question/problem'];solution=original[':question/worked-solution']
 else:
  # Same prompt/response layout and fixed instructional sentences; explicit
  # coefficient scaling is the bounded extension, with recomputed math blocks.
  problem=original[':question/problem']
  problem=re.sub(r'\$y=.*?\$',lambda _: '$y='+sp.latex(f)+'$',problem,count=1)
  problem=re.sub(r'at the point \$.*?\$',lambda _: 'at the point $('+sp.latex(p)+','+sp.latex(y)+').$',problem,count=1)
  solution=original[':question/worked-solution']
  solution=re.sub(r'\$f\(x\)=.*?\$',lambda _: '$f(x)='+sp.latex(f)+'.$',solution,count=1)
  blocks=list(re.finditer(r'\$\$\n.*?\n\$\$',solution,re.S))
  # Preserve the observed derivative, evaluation, negative reciprocal sequence.
  rewrite=''
  if any(e<0 or e.q!=1 for e in [term.as_powers_dict().get(x,sp.Integer(0)) for term in f.as_ordered_terms()]):
   rewrite=r'\frac{\mathrm{d}}{\mathrm{d}x}\left('+sp.latex(f)+r'\right)='
  math=[r"f'(x)="+rewrite+sp.latex(d),r"m=f'("+sp.latex(p)+')='+sp.latex(d.subs(x,p,evaluate=False))+'='+sp.latex(m),r"m'=-\frac{1}{m}=-\frac{1}{\left("+sp.latex(m)+r'\right)}='+sp.latex(a)+'.']
  assert len(blocks)==3
  for match,value in reversed(list(zip(blocks,math))):solution=solution[:match.start()]+'$$\n'+value+'\n$$'+solution[match.end():]
  solution=re.sub(r'point \$.*?\$',lambda _: 'point $('+sp.latex(p)+','+sp.latex(y)+'):$',solution,count=1)
  solution=re.sub(r'\$\{f\}\^\{′\}\(.*?\)\$',lambda _: "$f'("+sp.latex(p)+')$',solution)
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 return {'question':q,'knowledge_point':{'id':KP_UUID,'title':TITLE},'generation':{'version':VERSION,'template':mid,'profile':mid if len(values)>1 else None,'parameters':{'scale':scale},'seed':seed,'parameter_fingerprint':fp,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'domain':'x>0' if mid in ('q-342153','q-103531','q-103532') else 'x!=0' if mid in ('q-342152','q-103543') else 'real x','sympy':sp.__version__}}
def batch(level,count,seed):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
 catalog=[(mid,s) for mid in SPECS for s in range(1,13)];random.Random(seed).shuffle(catalog);out=[];used=set()
 for mid,s in catalog:
  try:r=generate_profile(mid,s,seed)
  except ValueError:continue
  fp=r['generation']['parameter_fingerprint']
  if fp not in used:out.append(r);used.add(fp)
  if len(out)>=count:break
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True);p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rows=batch(a.difficulty,a.count,a.seed)
 print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in rows))
