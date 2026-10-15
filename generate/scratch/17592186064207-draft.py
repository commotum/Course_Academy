#!/usr/bin/env python3
"""Independent frozen basis-2275 linear-rational/constant draft. No EDB access."""
import sys
sys.dont_write_bytecode=True
import argparse,copy,hashlib,importlib.util,itertools,json,random,uuid
from pathlib import Path
import sympy as sp
PACKAGE=Path(__file__).with_suffix('')
def private(name):
 spec=importlib.util.spec_from_file_location('kp64207_'+name,PACKAGE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=private('math_format');parser=private('parser')
SOURCE=json.loads((PACKAGE/'source.json').read_text());ANCHORS=json.loads((PACKAGE/'contract.json').read_text())['anchors'];LEVELS=('easy','moderate','hard')
KP_ID=17592186064207;KP_UUID='bdbfa506-08a1-5e43-b958-2ae373df775d';TITLE=SOURCE['record'][':knowledge-point/title'];VERSION='linear-rational-C-K-b2275-draft-v1'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(v):return sp.latex(sp.sympify(v)).replace('- ','-')
def coef(v):return '' if v==1 else '-' if v==-1 else tex(v)
def denominator(p):
 n,a,b=p
 return (('' if a==1 else str(a))+'x'+('+' if b>=0 else '')+str(b)) if a>0 else str(b)+'-'+('' if a==-1 else str(-a))+'x'
def raw(sid):return next(q for q in SOURCE['record'][':knowledge-point/questions'] if q.get(':question/math-academy-id',str(q[':db/id']))==sid)
def level(sid):return raw(sid).get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1]
def strictint(v,name):
 if type(v)!=int:raise ValueError(name+' must be an integer (bool/float rejected)')
def recipe(r,p):
 n,a,b=map(sp.Integer,p);parts=r.split(':');v=sp.sympify(parts[0],locals={'n':n,'a':a,'b':b});mode=parts[1] if len(parts)>1 else 'normal';d=denominator(p)
 arg={'normal':'K|'+d+'|','divide':r'\frac{|'+d+'|}{K}','inverse':r'\frac{K}{|'+d+'|}','outside':'|'+d+'|'}[mode]
 return (tex(v*parser.K) if mode=='outside' else coef(v))+r'\operatorname{ln}('+arg+')'
def extracted_template(sid):
 """Recover ordered prose and math slots from actual frozen source, never historical generator."""
 q=raw(sid);p=ANCHORS[sid]['parameters'];n,a,b=p;d=denominator(p);j=sp.Rational(1,a);r=sp.Rational(n,a)
 prompt=q[':question/problem'].replace(d,'@@D@@').replace(r'\frac{'+str(n)+'}{',r'\frac{@@N@@}{')
 sol=q.get(':question/worked-solution','').replace(d,'@@D@@')
 sol=sol.replace(r'\frac{'+str(n)+'}{@@D@@}',r'\frac{@@N@@}{@@D@@}')
 # Whole coefficient contexts preserve signs, parentheses, and every source stage.
 for tail in [r'\operatorname{ln}',r'\int',r'(\operatorname{ln}']:
  sol=sol.replace(coef(r)+tail,'@@R@@'+tail)
 sol=sol.replace(r'\frac{\text{d}u}{\text{d}x}='+str(a),r'\frac{\text{d}u}{\text{d}x}=@@A@@')
 sol=sol.replace('='+coef(j)+r'\text{d}u','=@@J@@'+r'\text{d}u')
 sol=sol.replace(r'\cdot ('+coef(j)+')',r'\cdot (@@J@@)').replace(r'\cdot '+coef(j)+r'\,',r'\cdot @@J@@\,')
 if n!=1:sol=sol.replace(str(n)+r'\int','@@N@@'+r'\int')
 return prompt,sol
def render(sid,p):
 prompt,sol=extracted_template(sid);n,a,b=p
 for k,v in {'D':denominator(p),'N':str(n),'A':str(a),'R':coef(sp.Rational(n,a)),'J':coef(sp.Rational(1,a))}.items():prompt=prompt.replace('@@'+k+'@@',v);sol=sol.replace('@@'+k+'@@',v)
 return fmt.normalize_prose(prompt),fmt.normalize_prose(sol)
def standard_solution(p,scaled=True):
 # Authored completion follows the source's substitution, integration, substitution back, C mapping, log-combination order.
 n,a,b=p;d=denominator(p);r=coef(sp.Rational(n,a));j=coef(sp.Rational(1,a));nr=tex(sp.Rational(n,a));I=r'\int \frac{'+str(n)+'}{'+d+r'}\,\text{d}x'
 steps=(I+' & ='+str(n)+r'\int \frac{1}{'+d+r'}\,\text{d}x \\ & ='+str(n)+r'\int \frac{1}{u}\cdot ('+j+r')\,\text{d}u') if n!=1 else (I+r' & =\int \frac{1}{u}\cdot ('+j+r')\,\text{d}u')
 return ('First, let $u='+d+'.$ Then differentiating with respect to $x$ gives\n\n$$\n'+r'\frac{\text{d}u}{\text{d}x}='+str(a)+r'\,⟹\,\text{d}x='+j+r'\text{d}u.'+'\n$$\n\nWe can now rewrite the integral in terms of $u,$ solve it, and write the final answer in terms of $x$ as follows:\n\n$$\n'+r'\begin{aligned}'+steps+r' \\ & ='+r+r'\int \frac{1}{u}\,\text{d}u \\ & ='+r+r'\operatorname{ln}|u|+C \\ & ='+r+r'\operatorname{ln}|'+d+r'|+C\end{aligned}'+'\n$$\n\nWe can further simplify the above by writing $C='+r+r'\operatorname{ln}K$ for another arbitrary positive constant $K,$ and then we can combine the two terms using the laws of logarithms, as follows:'+'\n\n$$\n'+r'\begin{aligned}'+r+r'\operatorname{ln}|'+d+'|+C & ='+r+r'\operatorname{ln}|'+d+'|'+('+' if n/a>0 else '')+r+r'\operatorname{ln}K \\ & ='+r+r'(\operatorname{ln}|'+d+r'|+\operatorname{ln}K) \\ & ='+r+r'\operatorname{ln}(K|'+d+r'|)\end{aligned}'+'\n$$\n\nSo, we finally conclude that\n\n$$\n'+I+'='+r+r'\operatorname{ln}(K|'+d+'|).\n$$')
NORMAL=['q-113532','q-113537','q-113538','q-30368','q-72445','q-72446','repair:q-113533','complete:q-49513','complete:q-49516','complete:q-49515']
def profiles(difficulty):
 return ['authored:hard-positive','authored:hard-negative'] if difficulty=='hard' else [s for s in NORMAL if (level(s.split(':')[-1]) if not s.startswith('complete:q-4951') else 'moderate')==difficulty]
def rules(sid):
 anchor=sid.split(':')[-1]
 if sid.startswith('authored:'):return ['n','1/a','-n/a','a/n','n/a']
 r=ANCHORS[anchor]['recipes'][:]
 if sid=='repair:q-113533':r[2]='-1/a:divide'
 if sid=='complete:q-49515':r=['n','1/a','-n/a','a/n','n/a']
 return r
def eligible(sid,p,difficulty):
 if not isinstance(p,(list,tuple)) or len(p)!=3 or any(type(v)!=int for v in p):return False
 n,a,b=p
 if a==0 or n<1 or b==0:return False
 if difficulty=='hard':return 7<=n<=15 and 7<=abs(a)<=15 and 1<=abs(b)<=15 and ((a>0)==sid.endswith('positive'))
 anchor=sid.split(':')[-1];n0,a0,b0=ANCHORS[anchor]['parameters']
 return (n==1 if n0==1 else 2<=n<=6) and (a==-1 if a0==-1 else 2<=abs(a)<=6 and (a>0)==(a0>0)) and 1<=abs(b)<=9

def valid_bank(sid,p):
 expr=[parser.scalar(recipe(r,p)) for r in rules(sid)];ds=[parser.derivative(v) for v in expr];n,a,b=map(sp.Integer,p);f=n/(a*parser.x+b)
 return len(expr)==5 and all(sp.cancel(v-w)!=0 for i,v in enumerate(ds) for w in ds[:i]) and sum(sp.cancel(v-f)==0 for v in ds)==1
@fmt.checked_math_content
def generate(difficulty='easy',seed=0,template=None,parameters=None,bank_profile=None):
 strictint(seed,'seed')
 if difficulty not in LEVELS:raise ValueError('unknown difficulty')
 rng=random.Random(seed);sid=bank_profile or template or rng.choice(profiles(difficulty))
 if sid not in profiles(difficulty):raise ValueError('profile/difficulty mismatch')
 if parameters is None:
  for attempt in range(1000):
   if difficulty=='hard':p=[rng.randint(7,15),rng.randint(7,15)*(1 if sid.endswith('positive') else -1),rng.choice([-1,1])*rng.randint(1,15)]
   else:
    n0,a0,b0=ANCHORS[sid.split(':')[-1]]['parameters'];p=[1 if n0==1 else rng.randint(2,6),-1 if a0==-1 else rng.randint(2,6)*(1 if a0>0 else -1),rng.choice([-1,1])*rng.randint(1,9)]
   if eligible(sid,p,difficulty) and valid_bank(sid,p):break
  else:raise ValueError('complete bank sampler exhausted')
 else:
  p=list(parameters) if isinstance(parameters,(list,tuple)) else parameters
  if not eligible(sid,p,difficulty) or not valid_bank(sid,p):raise ValueError('invalid parameter domain or complete bank collision')
 n,a,b=p
 if sid.startswith(('authored:','complete:')):
  prompt='Calculate $'+r'\int \frac{'+str(n)+'}{'+denominator(p)+r'}\,\text{d}x.$ Assume that $K$ is an arbitrary positive constant.';sol=standard_solution(p)
 else:prompt,sol=render(sid.split(':')[-1],p)
 prompt=fmt.normalize_prose(prompt);sol=fmt.normalize_prose(sol);values=[fmt.normalize_tex(recipe(r,p)) for r in rules(sid)];f=sp.cancel(n/(a*parser.x+b));ci=next(i for i,v in enumerate(values) if sp.cancel(parser.derivative(parser.scalar(v))-f)==0)
 qid=ident({'prompt':prompt,'solution':sol,'difficulty':difficulty,'bank':sorted((v,i==ci) for i,v in enumerate(values))});fid=ident([qid,'selection']);choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[ci][':answer/id']]}]}
 origin='authored_extension' if sid.startswith('authored:') else 'authored_completion' if sid.startswith('complete:') else 'source_error_repair' if sid.startswith('repair:') else 'observed_template'
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source_basis':2275,'seed':seed,'template':'scaled' if n!=1 else 'unit','bank_profile':sid,'profile':sid,'parameters':p,'origin':origin,'source_ids':[] if sid.startswith('authored:') else [sid.split(':')[-1]],'recipes':rules(sid),'mathematical_fingerprint':digest(str(f)),'constant_mapping':'C = '+tex(sp.Rational(n,a))+' ln(K); K=exp('+tex(sp.Rational(a,n))+' C)>0','domain':{'x':'real','excluded_poles':[str(-sp.Rational(b,a))],'constant':'K>0 arbitrary independently on each connected real interval'},'sympy':sp.__version__}}
def source_case(sid):
 q=SOURCE['record'][':knowledge-point/canonical-example'] if sid=='e-450' else raw(sid);issues=[]
 if not q.get(':question/answer-fields'):issues.append('missing answer fields')
 if not q.get(':question/worked-solution'):issues.append('missing worked solution')
 if not q.get(':question/difficulty'):issues.append('missing difficulty')
 if any(not f.get(':answer-field/correct') for f in q.get(':question/answer-fields',[])):issues.append('missing correct key')
 if sid=='q-113533':issues.append('equivalent correct distractor via positive K reciprocal')
 return {'source_id':sid,'raw':copy.deepcopy(q),'public_replay_eligible':not issues,'issues':issues}
def batch(difficulty,count=1,seed=0):
 strictint(count,'count');strictint(seed,'seed')
 if count<1:raise ValueError('positive count required')
 if difficulty not in LEVELS:raise ValueError('unknown difficulty')
 out=[];seen=set()
 for k in range(count*300):
  z=generate(difficulty,seed+k);fp=z['generation']['mathematical_fingerprint']
  if fp in seen:continue
  seen.add(fp);out.append(z)
  if len(out)==count:return out
 raise ValueError('finite mathematical task domain exhausted')
def markdown(z):
 q=z['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args();rows=[z for d in LEVELS if args.difficulty in (d,'all') for z in batch(d,args.count,args.seed)];print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
