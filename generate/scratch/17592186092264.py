#!/usr/bin/env python3
"""Source-based bounded logarithmic-chain-rule generator. No database operations."""
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 for packages in (Path(__file__).resolve().parents[2]/'.venv/lib').glob('python*/site-packages'):
  sys.path.insert(0,str(packages))
 import sympy as sp
H=Path(__file__).with_suffix('');SOURCE=json.loads((H/'source.json').read_text());KP=SOURCE['record']
KP_UUID=KP[':knowledge-point/id'];TITLE=KP[':knowledge-point/title'];VERSION='log-chain-rule-v1'
GENERATOR_ID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# Template, source, parameter name, source value, bounded policy.
CONFIG={
 'scale-radio':('q-11930','a',8,[8]), 'power-radio':('q-11932','n',2,list(range(2,22))),
 'polynomial-blank':('q-341676','a',3,[3]), 'scale-blank':('q-341671','a',9,[9]),
 'slope-polynomial':('q-310144','a',5,list(range(1,21))),
 'slope-affine':('q-341679','b',7,list(range(1,21))),
 'tangent-origin':('q-150014','a',3,list(range(2,22))),
 'tangent-shift':('q-150015','t',1,list(range(1,21))),
 'tangent-scaled':('q-48654','c',4,list(range(2,22)))}
x=sp.Symbol('x',real=True)
def math_data(template,p):
 if template.startswith('scale-'): return p*x,sp.log(p*x),1/x,'x>0'
 if template=='power-radio':return x**p,sp.log(x**p),p/x,'x>0' if p%2 else 'x!=0'
 if template=='polynomial-blank':return 3-5*x**6,sp.log(3-5*x**6),-30*x**5/(3-5*x**6),'3-5x^6>0'
 if template=='slope-polynomial':return p*x**2+4,sp.log(p*x**2+4),sp.Rational(2*p,p+4),'all real x; evaluate x=1'
 if template=='slope-affine':return p-4*x,sp.log(p-4*x),-sp.Rational(4,p+4),f'x<{sp.Rational(p,4)}; evaluate x=-1'
 if template=='tangent-origin':return p*x+1,sp.log(p*x+1),p*x,f'x>{-sp.Rational(1,p)}; tangent x=0'
 if template=='tangent-shift':return p+1-x,sp.log(p+1-x),-x+p,f'x<{p+1}; tangent x={p}'
 if template=='tangent-scaled':return 2*x,p*sp.log(2*x),x-p+p*sp.log(2*p),f'x>0; tangent x={p}'
 raise ValueError(template)
def mathematical_key(template,p):
 u,f,target,domain=math_data(template,p)
 # Scale variants have the same derivative task; collapse both field layouts.
 if template.startswith('scale-'):return 'log-scale-derivative:1/x:x>0'
 return hashlib.sha256(json.dumps([template,sp.srepr(f),sp.srepr(target),domain]).encode()).hexdigest()
def simultaneous(s,mapping):
 return re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m[0]],s) if mapping else s
def generate(template,seed=0,p=None):
 if template not in CONFIG:raise ValueError('Unsupported template')
 mid,param,original,domain=CONFIG[template];p=original if p is None else p
 if type(p)!=int or p not in domain:raise ValueError('Outside bounded parameter domain')
 src=SOURCES[mid];u,function,target,restriction=math_data(template,p);mapping={}
 # Preserve exact source Markdown by replacing complete mathematical fragments.
 if template=='power-radio':
  mapping={r'{x}^{2}':r'{x}^{'+str(p)+'}',r'2x':str(p)+(r'x' if p==2 else r'{x}^{'+str(p-1)+'}'),r'2\cancel{x}':str(p)+r'\cancel{x}^{'+str(p-1)+'}',r'x\cdot \cancel{x}':r'x\cdot \cancel{x}^{'+str(p-1)+'}',r'\frac{2}{x}':r'\frac{'+str(p)+'}{x}',r'\frac{2}{{x}^{2}}':r'\frac{'+str(p)+'}{{x}^{'+str(p)+'}}'}
  # Original cancellation step only valid for n=2; generalize it explicitly.
 elif template=='slope-polynomial':
  mapping={r'5{x}^{2}':str(p)+r'{x}^{2}',r'5({1}^{2})':str(p)+r'({1}^{2})',r'10x':str(2*p)+'x',r'10(1)':str(2*p)+'(1)',r'\frac{10}{9}':sp.latex(target)}
 elif template=='slope-affine':mapping={'7-4':str(p)+'-4',r'\frac{4}{11}':sp.latex(-target)}
 elif template=='tangent-origin':
  mapping={'3x':str(p)+'x','3(0)':str(p)+'(0)',r'\cdot 3':r'\cdot '+str(p),r'=3.':r'='+str(p)+'.',r'=3\,':r'='+str(p)+r'\,',r'm=3.':r'm='+str(p)+'.',r'=3\cdot':r'='+str(p)+r'\cdot',r'\operatorname{ln}\u20613':r'\operatorname{ln}\u2061'+str(p)}
 elif template=='tangent-shift':
  mapping={'2-x':str(p+1)+'-x','x-2':'x-'+str(p+1),'x=1':'x='+str(p),'(1,0)':'('+str(p)+',0)','(1)-2':'('+str(p)+')-'+str(p+1),'(x-1)':'(x-'+str(p)+')',r'y & =-x+1':r'y & =-x+'+str(p)}
 elif template=='tangent-scaled':mapping={} # Render this template's parameterized sequence below.
 problem=simultaneous(src[':question/problem'],mapping);solution=simultaneous(src[':question/worked-solution'],mapping)
 # Recipes are complete observed banks, never pooled.
 if template=='scale-radio':values=[p/x,p*sp.log(p*x),1/sp.log(p*x),1/x,1/(p*x)]
 elif template=='power-radio':values=[p*x**(p-1)*sp.log(x**p),1/x,p/x**p,p/x,1/x**p]
 elif template=='tangent-origin':values=[p*x+1,p*x,x,x+p,p*x+sp.log(p)]
 elif template=='tangent-shift':values=[x+p,x-p,-x+p,-x,2*x]
 elif template=='tangent-scaled':values=[2*x-sp.Rational(p,2)-sp.log(2*p),2*x-2*p+p*sp.log(2*p),x-p,x-p+p*sp.log(2*p),x+p]
 else:values=[target]
 fieldsrc=src[':question/answer-fields'][0];ft=fieldsrc[':answer-field/type'][':db/ident'];key=fieldsrc[':answer-field/key']
 if p==original:
  rendered=[a[':answer/value'] for a in fieldsrc[':answer-field/choices']]
  correct=next(i for i,a in enumerate(fieldsrc[':answer-field/choices']) if a[':answer/id']==fieldsrc[':answer-field/correct'][':answer/id'])
 else:
  rendered=[('y=' if template.startswith('tangent-') else '')+sp.latex(v) for v in values]
  correct=next(i for i,v in enumerate(values) if sp.simplify(v-target)==0)
  if template=='power-radio':
   solution=solution.replace(r'\frac{'+str(p)+r'\cancel{x}^{'+str(p-1)+r'}}{x\cdot \cancel{x}^{'+str(p-1)+'}}',r'\frac{'+str(p)+'}{x}')
  if template=='tangent-origin':solution=solution.replace(r'\frac{3}{',r'\frac{'+str(p)+'}{')
  if template=='tangent-scaled':
   problem=f'Find the equation of the tangent to the curve $f(x)={p}ln⁡(2x)$ at the point $({p},{p}ln⁡{2*p}).$'
   solution=(f'First, we express $f(x)$ as the composite function\n\n$$f={p}ln⁡u,\\,u=2x.$$\n\nDifferentiating gives\n\n'
    f'$$\\frac{{\\text{{d}}f}}{{\\text{{d}}u}}=\\frac{{{p}}}{{u}},\\,\\frac{{\\text{{d}}u}}{{\\text{{d}}x}}=2.$$\n\nWe now apply the chain rule, and we get\n\n'
    f'$$\\begin{{aligned}}\\frac{{\\text{{d}}f}}{{\\text{{d}}x}} &=\\frac{{{p}}}{{u}}\\cdot2 \\\\ &=\\frac{{{p}}}{{2x}}\\cdot2 \\\\ &=\\frac{{{2*p}}}{{2x}} \\\\ &=\\frac{{{p}}}{{x}}.\\end{{aligned}}$$\n\n'
    f'Therefore, the slope $m$ of the tangent line at the point where $x={p}$ is\n\n$$m=\\frac{{{p}}}{{{p}}}=1.$$\n\n'
    f'Hence, the slope of the tangent line at the point $({p},{p}ln⁡{2*p})$ is $m=1.$ Now, we find the equation of the tangent at that point:\n\n'
    f'$$\\begin{{aligned}}y-y_1 &=m(x-x_1) \\\\ y-{p}ln⁡({2*p}) &=1(x-{p}) \\\\ y &={sp.latex(target)}.\\end{{aligned}}$$')
 if p!=original:
  ul=sp.latex(u);du=sp.latex(sp.diff(u,x));derivative=sp.latex(sp.simplify(sp.diff(function,x)))
  outer=p if template=='tangent-scaled' else 1
  fl=(str(outer) if outer!=1 else '')+r'\ln('+ul+')'
  if template=='power-radio':problem=f'Given that $g(x)={fl}$, find $\\frac{{\\text{{d}}g}}{{\\text{{d}}x}}.$'
  elif template.startswith('slope-'):
   point=1 if template=='slope-polynomial' else -1
   problem=f'Find the slope $m$ of the tangent to the curve $f(x)={fl}$ at the point where $x={point}.$\n\n$m=$\n{{{{field-1}}}}'
  elif template.startswith('tangent-'):
   point=0 if template=='tangent-origin' else p
   yl=sp.latex(function.subs(x,point))
   problem=f'Find the equation of the tangent to the curve $f(x)={fl}$ at the point $({point},{yl}).$'
  name='g' if template=='power-radio' else 'f'
  of=sp.latex(sp.Rational(outer,1))
  solution=(f'First, we express ${name}(x)$ as the composite function\n\n$$ {name}='+('' if outer==1 else str(outer))+r'\ln u,\,u='+ul+'.$$\n\nDifferentiating gives\n\n'
   +r'$$\frac{\text{d}'+name+r'}{\text{d}u}=\frac{'+of+r'}{u},\,\frac{\text{d}u}{\text{d}x}='+du+'.$$\n\nWe now apply the chain rule, and we get\n\n'
   +r'$$\begin{aligned}\frac{\text{d}'+name+r'}{\text{d}x} &=\frac{\text{d}'+name+r'}{\text{d}u}\cdot\frac{\text{d}u}{\text{d}x} \\ &=\frac{'+of+r'}{u}\cdot('+du+r') \\ &=\frac{'+of+r'}{'+ul+r'}\cdot('+du+r') \\ &='+derivative+r'.\end{aligned}$$')
  if template.startswith(('slope-','tangent-')):
   m=sp.simplify(sp.diff(function,x).subs(x,point));ml=sp.latex(m)
   solution+=f'\n\nTherefore, the slope $m$ of the tangent line at the point where $x={point}$ is\n\n'+r'$$m=\left.('+derivative+r')\right|_{x='+str(point)+'}='+ml+'.$$'
   if template.startswith('tangent-'):
    solution+=f'\n\nHence, the slope of the tangent line at the point $({point},{yl})$ is $m={ml}.$ Now, we find the equation of the tangent at that point:\n\n'+r'$$\begin{aligned}y-y_1 &=m(x-x_1) \\ y-('+yl+r') &=('+ml+r')(x-('+str(point)+r')) \\ y &='+sp.latex(target)+r'.\end{aligned}$$'
 # Source nested aligned environments are normalized without changing steps.
 solution=solution.replace(r'\begin{aligned}\begin{aligned}',r'\begin{aligned}').replace(r'\end{aligned}\end{aligned}',r'\end{aligned}')
 ident=str(uuid.uuid5(uuid.UUID(GENERATOR_ID),mathematical_key(template,p)+':'+template))
 fid=str(uuid.uuid5(uuid.UUID(ident),key));answers=[]
 for i,value in enumerate(rendered):answers.append({':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(i))),':answer/type':':answer.type/math',':answer/value':value})
 f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':ft,':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct][':answer/id']]}
 q={':question/id':ident,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':src[':question/difficulty'][':db/ident'],':question/answer-fields':[f]}
 return {'knowledge_point':{'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_ID,'version':VERSION,'template':template,'profile':mid,'source_question':mid,'source_basis':SOURCE['basis'],'seed':seed,'parameters':{param:p},'domain':restriction,'mathematical_key':mathematical_key(template,p),'dependencies':{'sympy':sp.__version__},'recipes':[str(v) for v in values]}}
def candidates(difficulty):
 if difficulty not in ['moderate','hard']:raise ValueError('Easy unobserved; classification exception')
 rows=[];seen=set()
 for t,c in CONFIG.items():
  if SOURCES[c[0]][':question/difficulty'][':db/ident']!=':question.difficulty/'+difficulty:continue
  for p in c[3]:
   key=mathematical_key(t,p)
   if key not in seen:rows.append((t,p));seen.add(key)
 return rows
def batch(difficulty,count,seed):
 rows=candidates(difficulty)
 if type(count)!=int or not 0<=count<=len(rows):raise ValueError('Finite policy count exceeded')
 random.Random(seed).shuffle(rows)
 return [generate(t,seed,p) for t,p in rows[:count]]
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args()
 rows=batch(a.difficulty,a.count,a.seed);print(json.dumps(rows,ensure_ascii=False) if a.format=='json' else '\n\n'.join(map(markdown,rows)))
