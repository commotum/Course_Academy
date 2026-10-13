"""Source-backed general-base exponential integrals; easy/moderate only."""
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('');sys.path.insert(0,str(HERE))
from scalar_parser import scalar,group,X as x
KP_ID=17592186096656;KP_UUID='19fd901f-e08d-54c5-9cda-68543a3d71a9';TITLE='Integrating a General Exponential Function With a Linear Exponent'
VERSION='general-base-linear-v1';SUPPORTED_LEVELS=('easy','moderate')
SOURCE=json.loads((HERE/'source.json').read_text());QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
CASES=json.loads((HERE/'source-cases.json').read_text())
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def tex(v):return sp.latex(sp.sympify(v),ln_notation=True)
def math(p):
 a,k,b,n=map(sp.Rational,(p['a'],p['k'],p['b'],p['n']));f=a*n**(k*x+b);F=a*n**(k*x+b)/(k*sp.log(n));L=sp.Integer(p.get('L',0));H=sp.Integer(p.get('H',0));return f,sp.simplify(F.subs(x,H)-F.subs(x,L)) if 'L' in p else F,L,H

def printed(q):
 text=q[':question/problem'].replace(r'{\int }',r'\int');tail=text.split(r'\int',1)[1].lstrip();limits=None
 if tail.startswith('_'):
  l,j=group(tail,1);assert tail[j]=='^';h,j=group(tail,j+1);tail=tail[j:];limits=(scalar(l),scalar(h))
 tail=re.split(r'\\(?:text|textrm)\{d\}x|dx',tail)[0].rstrip().removesuffix(r'\,')
 return sp.simplify(scalar(tail)),limits

def fingerprint(q):
 f,limits=printed(q);slope=sp.simplify(sp.diff(f,x)/f);constant=sp.simplify(f.subs(x,0));return digest([sp.srepr(slope),sp.srepr(constant),None if limits is None else [sp.srepr(v) for v in limits],'real'])

def bank(c,p):
 a,k,b,n=map(sp.Rational,(p['a'],p['k'],p['b'],p['n']));E=n**(k*x+b);log=sp.log(n);ans=math(p)[1];profile=c['profile']
 if profile=='legacy-positive':return [E/log,n**(k*x/2+b)/k,E/k,ans,n**(k*x/2+b)/log]
 if profile=='legacy-negative':return [n**(-k*x-b)/n,ans,-n**(-k*x-b)/log,-n**(k*x)/log,E/log]
 if profile=='negative-unit':return [ans,-E,n**x/log,E/log,-n**x/log]
 if profile=='positive':return [ans,E/k,E/log,-n**(k*x-7)/(k*log),n**x/log]
 if profile=='fraction':
  d=1/k;return [n**x/(d*log),E/(d*log),d*E/log,d*n**x/sp.log(d),E/sp.log(d)]
 if profile=='definite-radio':
  D=n**k-1;return [D/log,D/(2*n),ans,D/(2*log),(n**(k-1)-1)/(2*log)]
 return [ans]

def bounds(c,p):
 if set(p)!=set(c['parameters']):raise ValueError('Parameter shape')
 a,k,b,n=map(sp.Rational,(p['a'],p['k'],p['b'],p['n']));t=c['profile']
 if n not in range(2,7) or k==0 or abs(k)>8 or a<=0 or a>5 or abs(b)>8:raise ValueError('Bounded positive real base and scale, nonzero slope')
 if t=='legacy-positive' and (k<=1 or b==0 or a!=1):raise ValueError('Legacy positive profile')
 if t=='legacy-negative' and (k!=-1 or b>=0 or a!=1):raise ValueError('Legacy negative profile')
 if t=='negative-unit' and (k!=-1 or b!=0 or a!=1):raise ValueError('Negative unit profile')
 if t=='positive' and (k<=1 or b!=0 or a!=1):raise ValueError('Positive profile')
 if t=='fraction' and (a!=1 or b!=0 or 1/k not in range(2,7) or n==1/k):raise ValueError('Reciprocal slope profile')
 if t=='definite-radio' and (a!=1 or b!=0 or p['L']!=0 or p['H']!=1 or k not in (4,6,8)):raise ValueError('Even slope definite bank')
 if 'L' in p and (not -2<=p['L']<p['H']<=4):raise ValueError('Ordered bounded integer limits')
 if c['profile']=='blank' and sp.sign(k)!=sp.sign(sp.Rational(c['parameters']['k'])):raise ValueError('Preserve observed slope sign')

def render(c,p):
 a,k,b,n=map(sp.Rational,(p['a'],p['k'],p['b'],p['n']));f,ans,L,H=math(p);u=k*x+b;power=str(n)+'^{'+tex(u)+'}';body=(tex(a)+r'\cdot ' if a!=1 else '')+power
 integral=r'\int '+body+r'\,\text{d}x'
 if 'L' in p:integral=r'\int_{'+tex(L)+'}^{'+tex(H)+'}'+body+r'\,\text{d}x'
 if c['field_type']=='blank':problem='Evaluate the following integral. Do not round the answer.\n\n$'+integral+'=$  \n{{field-1}}'
 elif c['profile'].startswith('legacy'):problem='What is $'+integral+'$?'
 elif c['profile']=='definite-radio':problem='Evaluate the integral $'+integral+'.$'
 else:problem='$'+integral+'=$'
 solution='If we let $u='+tex(u)+',$ then\n\n$$\n'+r'\frac{\text{d}u}{\text{d}x}='+tex(k)+r'\quad\Longrightarrow\quad '+tex(1/k)+r'\,\text{d}u=\text{d}x.'+'\n$$\n\n'
 factor=tex(a/k);Fu=r'\frac{'+str(n)+r'^{u}}{\ln '+str(n)+'}'
 if 'L' in p:
  lo,hi=u.subs(x,L),u.subs(x,H)
  solution+='Computing our limits of integration, we get the following:\n\n| $x$ | $'+tex(L)+'$ | $'+tex(H)+'$ |\n| --- | --- | --- |\n| $u$ | $'+tex(lo)+'$ | $'+tex(hi)+'$ |\n\n'
  U=r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'+str(n)+r'^{u}\,\text{d}u'
  rows=[integral+'&='+r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'+(tex(a)+r'\cdot ' if a!=1 else '')+str(n)+r'^{u}\cdot '+tex(1/k)+r'\,\text{d}u']
  if a/k!=1:rows+=['&='+factor+U]
  rows+=['&='+factor+r'\left['+Fu+r'\right]_{'+tex(lo)+'}^{'+tex(hi)+'}','&='+tex(a/k/sp.log(n))+r'\left('+str(n)+'^{'+tex(hi)+'}-'+str(n)+'^{'+tex(lo)+r'}\right)','&='+tex(a/k/sp.log(n))+r'\left('+tex(n**hi)+'-'+tex(n**lo)+r'\right)','&='+tex(ans)]
 else:
  U=r'\int '+str(n)+r'^{u}\,\text{d}u'
  rows=[integral+'&='+r'\int '+str(n)+r'^{u}\cdot '+tex(1/k)+r'\,\text{d}u','&='+tex(1/k)+U,'&='+tex(1/k)+Fu+'+C','&='+tex(ans)+'+C']
 solution+='Then, we can write the integral in terms of $u$ and evaluate:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
 return problem,solution

def sample(c,rng):
 p=dict(c['parameters']);t=c['profile'];p['n']=rng.randint(2,6)
 if t=='legacy-positive':p.update(k=rng.randint(2,8),b=rng.choice([-5,-3,-1,1,3,5]))
 elif t=='legacy-negative':p['b']=-rng.randint(1,8)
 elif t=='positive':p['k']=rng.randint(2,8)
 elif t=='fraction':p['k']='1/'+str(rng.randint(2,6))
 elif t=='definite-radio':p['k']=rng.choice([4,6,8])
 elif t=='blank':
  p.update(a=rng.randint(1,5),k=rng.randint(1,4)*int(sp.sign(sp.Rational(p['k']))),b=rng.randint(-4,8));p['L']=rng.randint(-2,2);p['H']=rng.randint(p['L']+1,4)
 return p

def generate(level='easy',seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Hard unsupported: no observed source family')
 rng=random.Random(seed);eligible=[c for c in CASES if c['level']==level];c=next((c for c in eligible if c['template']==template),None) if template else rng.choice(eligible)
 if c is None or profile not in (None,c['profile']):raise ValueError('Unknown template/profile')
 for attempt in range(300):
  p=parameters or sample(c,rng)
  try:
   bounds(c,p);values=bank(c,p);ans=math(p)[1]
   if any(sp.simplify(v-w)==0 for i,v in enumerate(values) for w in values[:i]):raise ValueError('Equivalent options')
   matches=[i for i,v in enumerate(values) if sp.simplify(v-ans)==0]
   if len(matches)!=1:raise ValueError('Unique correct value')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('Bounded resampling exhausted')
 problem,solution=render(c,p);fp=fingerprint({':question/problem':problem});qid=uid(VERSION+'/'+c['template']+'/'+digest(p));fid=uid(qid+'/field')
 choices=[{':answer/id':uid(fid+'/'+str(i)),':answer/type':':answer.type/math',':answer/value':tex(v)+('+C' if 'L' not in p else '')} for i,v in enumerate(values)]
 f={':answer-field/id':fid,':answer-field/key':'field-1' if c['field_type']=='blank' else 'selection',':answer-field/type':':answer-field.type/'+c['field_type'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[matches[0]][':answer/id']]}
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[f]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':c['template'],'profile':c['profile'],'parameters':p,'domain':'Real x; integer base 2..6; nonzero rational slope; ordered finite limits','source_ids':[c['source_id']],'math_fingerprint':fp,'dependencies':{'sympy':sp.__version__},'solution_policy':'Source substitution sentences and step sequence, standardized TeX; legacy missing solutions authored using canonical e-460'}}
def batch(level,count,seed=0,template=None,profile=None):
 out=[];seen=set()
 for i in range(max(200,count*100)):
  if len(out)>=count:break
  r=generate(level,seed+i,template,profile=profile);fp=r['generation']['math_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
 return out

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--template');ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args();out=batch(args.difficulty,args.count,args.seed,args.template);print(json.dumps(out,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,out)))
