#!/usr/bin/env python3
"""Definite logarithmic substitution; basis2275. Local preview only.

Each observed complete bank remains one indivisible profile. Conservative slots
are independent positive rational coefficient scale and positive x-rescaling.
Every source stage is transformed as a mathematical object, never by replacing
coincident numeric literals. Opaque distractors retain their complete observed
expression, scaled homogeneously; no misconception interpretation is claimed.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import argparse,hashlib,importlib.util,json,random,re,uuid
from pathlib import Path
import sympy as s
H=Path(__file__).with_suffix('');KP=17592186100818;VERSION='definite-logarithmic-substitution-b2275-v1'
def mod(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
fmt=mod('kp00818_format',H/'math_format.py');R=mod('kp00818_render',H/'rendered_reader.py')
SOURCE=json.loads((H/'source.json').read_text());REC=SOURCE['record'];QS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']};x,u=R.x,R.u
CONFIG={sid:q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1]for sid,q in QS.items()}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+str(v)))
def tex(z):return fmt.normalize_tex(s.latex(z,fold_short_frac=False).replace(r'\log',r'\ln'))
def original(sid):return {'coefficient_num':1,'coefficient_den':1,'x_scale':1}
REPAIRS={
 'q-49607':['Missing difficulty, worked solution and correct designation. Supported authored completion: moderate, correct answer19; raw source stays ineligible.'],
 'q-31643':['Correct derivative equality and restore x/u table order to lower then upper; integral is convergent improper at lower endpoint.'],
 'q-73655':['Extracted x-integral bounds2..4 corrected to4..16.'],
 'q-13840':['Remove extra1/x from extracted x-integral operand.'],
}
def source_solution(sid):
 sol=QS[sid].get(':question/worked-solution','')
 if sid=='q-31643':
  sol=sol.replace(r'\frac{1}{2x}\cdot 2\,⟹',r'\frac{1}{2x}\cdot 2=\frac{1}{x}\,⟹').replace('| $x$ | $e/2$ | $1/2$ |','| $x$ | $1/2$ | $e/2$ |').replace('| $u$ | $1$ | $0$ |','| $u$ | $0$ | $1$ |')
 if sid=='q-73655':sol=sol.replace(r'=2{\int }_{2}^{4}',r'=2{\int }_{4}^{16}')
 if sid=='q-13840':sol=sol.replace(r'\frac{2}{x\operatorname{ln}⁡({x}^{2})}\cdot',r'\frac{2}{\operatorname{ln}⁡({x}^{2})}\cdot')
 return fmt.normalize_prose(sol)
def source_integral(sid):
 chunks=R.blocks(fmt.normalize_prose(QS[sid][':question/problem']));raw=next(b for b in chunks if r'\int'in b);return raw.strip().rstrip('= .?(')
def complete_solution(sid):
 if sid!='q-49607':return source_solution(sid)
 return r"""Let's set $u=\ln(x).$ Then, we have

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\,⟹\,\text{d}u=\frac{1}{x}\,\text{d}x.
$$

Calculating the limits for $u$ gives the following:

| $x$ | $e^{4}$ | $e^{9}$ |
| --- | --- | --- |
| $u$ | $4$ | $9$ |

We now substitute and evaluate as follows:

$$
\begin{aligned}\int_{e^{4}}^{e^{9}}\frac{3\sqrt{\ln(x)}}{2x}\,\text{d}x & =\frac{3}{2}\int_{e^{4}}^{e^{9}}\sqrt{\ln(x)}\cdot\frac{1}{x}\,\text{d}x \\ & =\frac{3}{2}\int_{4}^{9}\sqrt{u}\,\text{d}u \\ & =\frac{3}{2}\int_{4}^{9}u^{1/2}\,\text{d}u \\ & =\frac{3}{2}\cdot\frac{u^{3/2}}{3/2}|_{4}^{9} \\ & =u^{3/2}|_{4}^{9} \\ & =9^{3/2}-4^{3/2} \\ & =27-8 \\ & =19\end{aligned}
$$"""
def group(t,i):return R.group(t,i)
def scaled_side(raw,t,k):
 """Transform one displayed operative object, retaining its original operand.
 x=k*z has dx=k*dz. Equivalently evaluate source at x/k and divide
 the transformed x-integrand by k; both limits multiply by k.
 """
 clean=R.clean(R.P.fraction_measure(raw)).strip().rstrip('.,')
 if r'\int'in clean:
  start=clean.index(r'\int');pos=start+4
  while clean[pos].isspace():pos+=1
  assert clean[pos]=='_';lo,pos=group(clean,pos+1);assert clean[pos]=='^';hi,pos=group(clean,pos+1)
  m=re.search(R.P.DIFF,clean[pos:]);assert m;v=m[1];body=clean[pos:pos+m.start()].strip();body=body[:-len(r'\cdot')]if body.endswith(r'\cdot')else body
  prefix=clean[:start];coeff=R.scalar(prefix)if prefix.strip()else s.Integer(1)
  if v=='x':
   body=body.replace('x',r'\left(\frac{x}{'+str(k)+r'}\right)');coeff=coeff*t/k;lo=tex(k*R.scalar(lo));hi=tex(k*R.scalar(hi))
  else:assert v=='u';coeff*=t
  return tex(coeff)+r'\int_{'+lo+'}^{'+hi+'}'+body+r'\,\text{d}'+v
 # Evaluation bars retain original primitives and their internal unsimplified
 # arithmetic, independently scaled outside the entire primitive.
 if r'|_'in clean:
  i=clean.index(r'|_');before=clean[:i];after=clean[i:]
  before+='}'*(before.count('{')-before.count('}'))
  return tex(t)+r'\cdot\left('+before+r'\right)'+after
 return tex(t)+r'\cdot\left('+clean+r'\right)'
def rendered(sid,t,k):
 source=complete_solution(sid);prompt=fmt.normalize_prose(QS[sid][':question/problem'])
 if t==1 and k==1:return prompt,source
 raw=source_integral(sid);newI=scaled_side(raw,t,k);prompt=prompt.replace(raw,newI)
 # Reconstruct the source's prose and ordered stages, changing every reference
 # to the same inner variable and interval coherently.
 Uraw=re.search(r'\$u\s*=([^$]+)\$',source)[1].rstrip('.');U=R.scalar(Uraw);Unew=U.subs(x,x/k);du=s.diff(Unew,x);Unew_tex=Uraw.replace('x',r'\left(\frac{x}{'+str(k)+r'}\right)')
 first=source.index('$$');pre=source[:first];pre=re.sub(r'\$u\s*=[^$]+\$',lambda m:'$u='+Unew_tex+'.$',pre)
 derivative='$$\n'+r'\frac{\text{d}u}{\text{d}x}='+tex(du)+r'\,⟹\,'+tex(1/(x*du))+r'\,\text{d}u=\frac{1}{x}\,\text{d}x.'+'\n$$'
 end=source.index('$$',first+2)+2;tail=source[end:]
 table=re.search(r'\| \$x\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',tail)
 tail=tail[:table.start()]+('| $x$ | $'+tex(k*R.scalar(table[1]))+'$ | $'+tex(k*R.scalar(table[2]))+'$ |')+tail[table.end():]
 block=next(b for b in R.blocks(tail)if r'\int'in b)
 text=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','')
 stages=[scaled_side(z,t,k)for row in text.split(r'\\')for z in row.split('=')if z.strip()]
 newblock=r'\begin{aligned}'+stages[0]+''.join(r' \\ & ='+z for z in stages[1:])+r'\end{aligned}'
 tail=tail.replace(block,newblock)
 return fmt.normalize_prose(prompt),fmt.normalize_prose(pre+derivative+tail)
def generate(difficulty,seed=0,template=None,profile=None,parameters=None):
 if difficulty not in ('easy','moderate','hard')or type(seed)is not int:raise ValueError('known difficulty and builtin integer seed required')
 if profile and template and profile!=template:raise ValueError('bank profile must match its observed template')
 rng=random.Random(seed);sid=profile or template or rng.choice([z for z in CONFIG if CONFIG[z]==difficulty]);assert CONFIG[sid]==difficulty
 par=parameters or {'coefficient_num':rng.randint(1,6),'coefficient_den':rng.randint(1,6),'x_scale':rng.randint(1,6)}
 if set(par)!=set(original(sid))or any(type(v)is not int or not 1<=v<=6 for v in par.values()):raise ValueError('builtin integer coefficient slots1..6 and x_scale1..6')
 t=s.Rational(par['coefficient_num'],par['coefficient_den']);k=par['x_scale'];prompt,sol=rendered(sid,t,k)
 sf=QS[sid][':question/answer-fields'][0];kind=sf[':answer-field/type'][':db/ident'];sourceanswers=sf[':answer-field/choices'];vals=[]
 for a in sourceanswers:
  v=R.scalar(a[':answer/value']).subs(x,x/k)*t;vals.append(fmt.normalize_tex(a[':answer/value'])if t==1 and k==1 else tex(v))
 goodindex=next((i for i,a in enumerate(sourceanswers)if a[':answer/id']==sf.get(':answer-field/correct',{}).get(':answer/id')),0)
 if sid=='q-49607':goodindex=0
 content=digest({'prompt':prompt,'solution':sol,'fieldtype':kind,'values':sorted(vals),'correct':vals[goodindex],'bank_profile':sid});qid=uid(content);fid=uid(qid+sf[':answer-field/key']);answers=[{':answer/id':uid(fid+str(i)+v),':answer/type':':answer.type/math',':answer/value':v}for i,v in enumerate(vals)]
 correct=answers[goodindex][':answer/id'];field={':answer-field/id':fid,':answer-field/key':sf[':answer-field/key'],':answer-field/type':kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 if kind.endswith('/radio'):rng.shuffle(answers)
 c,F,v,lo,hi,end=R.integral(source_integral(sid));assert not end
 F=s.cancel(s.expand_log((t*c*F.subs(x,x/k)/k).subs(x,s.Symbol('positive_x',positive=True)),force=False));bounds=[s.simplify(k*lo),s.simplify(k*hi)];mathfp=digest({'integrand':s.srepr(F),'bounds':list(map(s.srepr,bounds)),'domain':'positive x; real logarithm; original continuous u-interval, convergent endpoint allowed'})
 rec={'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+difficulty,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'source_basis':SOURCE['basis'],'template':sid,'bank_profile':sid,'source_ids':[sid],'parameters':par,'eligible':True,'raw_source_eligible':sid not in REPAIRS,'evidence_only':False,'origin':'authored_completion'if sid=='q-49607'else'observed_source_pattern','source_repairs':REPAIRS.get(sid,[]),'math_fingerprint':mathfp,'domain':'positive x interval; original real logarithm branch; sqrt log>=0, denominator log nonzero in interior; q-31643 convergent improper lower endpoint','runtime':{'python':sys.version.split()[0],'sympy':s.__version__}}}
 return fmt.validate_generated_record(rec)
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def generate_batch(difficulty,seed=0,count=1,**kw):
 if type(seed)is not int or type(count)is not int or not 1<=count<=100:raise ValueError('builtin int seed/count; count1..100')
 rows=[];seen=set()
 for i in range(count*100):
  r=generate(difficulty,seed+i,**kw);fp=r['generation']['math_fingerprint']
  if fp not in seen:seen.add(fp);rows.append(r)
  if len(rows)==count:return rows
 raise ValueError('finite parameter capacity exhausted; no duplicate mathematical tasks returned')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'for f in q[':question/answer-fields']for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['all','easy','moderate','hard'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args();rows=[r for d in (['easy','moderate','hard']if a.difficulty=='all'else[a.difficulty])for r in generate_batch(d,a.seed,a.count,template=a.template,profile=a.profile)];print(json.dumps(rows,indent=2,ensure_ascii=False)if a.format=='json'else'\n\n---\n\n'.join(map(markdown,rows)))
