#!/usr/bin/env python3
"""Read shift c and stretch k from an exponential curve; private step-7 draft.

API: generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None)
and generate_easy/moderate/hard. CLI: --difficulty easy|moderate|hard|all --seed
N --count N --format markdown|json [--template ...] [--profile ...].
All source profiles source:q-N preserve historical fields, missing attributes,
complete banks and prose. Their affine recipes reproduce values, but historical
error intent is underdetermined: evidence_only, never eligible for learning.
Normal profiles derive all five choices from the assessed shift/intercept method.
A complete bank is chosen before parameters; every collision rejects the whole
instance. No plotting/base-identification branches or database access.
"""
from __future__ import annotations
import argparse,hashlib,json,os,random,re,subprocess,sys,tempfile,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('');KP=17592186087824;VERSION='shift-stretch-v5'
SNAPSHOT=json.loads((HERE/'source.json').read_text());K=SNAPSHOT['record'];TITLE=K[':knowledge-point/title']
SOURCES={q[':question/math-academy-id']:q for q in K[':knowledge-point/questions']}
# k/c affine expressions are exact value patterns, not recovered error intent.
SPECS={
'q-18518':('easy',2,2,-2,'spaced', [('k','0'),('k','c'),('k','c+1'),('0','c'),('k','-c')]),
'q-18521':('moderate',3,3,-1,'spaced', [('k-1','c','b-1'),('k','c','b-1'),('k-1','c','b'),('k','c','b'),('k','c-1','b')]),
'q-29233':('easy',2,3,-2,'compact',[('0','-c'),('c','c'),('0','c'),('-c','-c'),('k','c')]),
'q-7239':('moderate',2,3,-1,'compact',[('k','c-1'),('k','-2*c'),('k','c'),('1','c'),('k-1','c')]),
'q-7241':('moderate',2,'1.5',4,'compact',[('k','c'),('k','c-1'),('k-1','c'),('k','c+1'),('k-1','c+1')]),
'q-7243':('moderate',3,3,2,'compact',[('k','c+1'),('k-1','c'),('k','c'),('k','c+k'),('k','2*c')]),
'q-99778':('moderate',5,3,-2,'compact',[('k-1','0'),('k','c'),('k-1','c+1'),('k+1','c-1'),('k','-c')]),
}
BANKS={
# y-intercept u=k+c: confuse u with k, reverse c, omit c, reverse subtraction.
'intercept_shift':[('k','c'),('k+c','c'),('k','-c'),('k+c','0'),('c','k')],
# Read adjacent grid level for c or intercept, or fail to subtract the shift.
'grid_reading':[('k','c'),('k-step','c+step'),('k+step','c-step'),('k+step','c'),('k+c','c')],
}
X=sp.Symbol('x');B,KK,C,STEP=sp.symbols('b k c step')
def rat(v):
 if isinstance(v,bool):raise ValueError('Boolean is not a numeric parameter')
 try:q=sp.Rational(str(v))
 except Exception as e:raise ValueError('Exact rational parameter required') from e
 return q

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'kp87824:'+v))
def num(v):
 v=rat(v)
 return str(v.p) if v.q==1 else str(float(v)) if v.q in (2,4) else sp.latex(v)
def offset(c,spaced=False):
 c=rat(c)
 if c==0:return ''
 return (' + ' if c>0 else ' - ') +num(abs(c)) if spaced else ('+' if c>0 else '-')+num(abs(c))
def eq(b,k,c,style='compact'):
 bt=str(b)+'^{x}' if style=='spaced' else '{'+str(b)+'}^{x}'
 pre='y = ' if style=='spaced' else 'y='
 coefficient='' if k==1 else num(k)
 body=bt if k==1 else coefficient+'('+bt+')'
 return pre+body+offset(c,style=='spaced')
def pair(k,c,style='compact'):
 # Historical spaced style uses asymmetric spaces after equals for negative c.
 if style=='spaced':return '$k = '+num(k)+'$ and $c ='+(' ' if c>=0 else '')+num(c)+'$'
 return '$k='+num(k)+'$ and $c='+num(c)+'$'
def bank(b,k,c,step,recipes,kind,style):
 values=[];objects=[]
 for recipe in recipes:
  env={B:b,KK:k,C:c,STEP:step}
  v=[sp.sympify(s,locals={'b':B,'k':KK,'c':C,'step':STEP}).subs(env) for s in recipe]
  a,d=v[:2];bb=v[2] if len(v)>2 else b
  values.append(pair(a,d,style) if kind=='parameters' else eq(bb,a,d,style));objects.append((bb,a,d))
 # Positive fixed bases ensure unequal triples imply distinct exponential curves,
 # except k=0 makes base incidental. Compare complete expressions for equations.
 same_base=len({bb for bb,a,d in objects})==1 and objects[0][0]>1
 expressions=[(a,d) for bb,a,d in objects] if kind=='parameters' or same_base else [a*bb**X+d for bb,a,d in objects]
 for i,obj in enumerate(expressions):
  if any((obj==other if kind=='parameters' or same_base else sp.simplify(obj-other)==0) for other in expressions[:i]):raise ValueError('Whole bank rejected: equivalent choices')
 correct=[i for i,(bb,a,d) in enumerate(objects) if a==k and d==c and (kind=='parameters' or bb==b)]
 if len(correct)!=1:raise ValueError('Whole bank rejected: missing/ambiguous answer')
 return values,objects,correct[0]
def domain(level,p,raw=False):
 if set(p)-{'b','k','c','step'}:raise ValueError('Unknown parameter')
 if not {'b','k','c'}<=set(p):raise ValueError('Missing b/k/c')
 b,k,c=map(rat,(p['b'],p['k'],p['c']));step=rat(p.get('step','1/2' if level=='hard' else 1))
 if b.q!=1 or not 2<=b<=6 or not 1<=k<=6 or abs(c)>6 or c==0 or abs(k+c)>10:raise ValueError('Outside shared exponential-growth scope')
 if raw:
  if k.q not in (1,2,4) or c.q not in (1,2,4) or step!=1:raise ValueError('Source recipe domain: integer/quarter values, unit annotation scale')
 elif level=='easy':
  if k.q!=1 or c.q!=1 or step!=1:raise ValueError('Easy: labelled integer intercept/asymptote')
 elif level=='moderate':
  if k.q not in (1,2) or c.q!=1 or step!=1:raise ValueError('Moderate: labelled integer/half stretch and integer shift, equation response')
 else:
  if step not in (sp.Rational(1,2),sp.Rational(1,4)) or k.q==1 or c.q==1 or (k/step).q!=1 or (c/step).q!=1 or (k+c)==0:raise ValueError('Hard: noninteger stretch and shift on calibrated half/quarter grid')
 return b,k,c,step

def solution(b,k,c,kind):
 u=k+c;bt='{'+str(b)+'}^{x}';oc=offset(c)
 return ('The horizontal asymptote of the curve $y=k('+bt+')+c$ is $y=c.$ In the graph above, the horizontal asymptote is $y='+num(c)+',$ so $c='+num(c)+'.$\n\nTherefore, our function takes the form\n\n$$\ny=k('+bt+')'+oc+'.\n$$\n\nWe can solve for $k$ by finding a point on the graph and substituting for $x$ and $y.$ The labeled point on the graph is $(0,'+num(u)+'),$ so we substitute $x=0$ and $y='+num(u)+'$ into the function and solve for $k:$\n\n$$\n'+r'\begin{aligned}y & =k('+bt+')'+oc+r' \\ '+num(u)+' & =k({'+str(b)+r'}^{0})'+oc+r' \\ '+num(u)+' & =k(1)'+oc+r' \\ '+num(u)+' & =k'+oc+r' \\ '+num(k)+r' & =k\end{aligned}'+'\n$$\n\n'+('Therefore, $k='+num(k)+'$ and $c='+num(c)+'.$' if kind=='parameters' else 'Therefore, the curve is $'+eq(b,k,c)+'.$'))
def render_plots(b,k,c,level,step,output_dir=None):
 data={'b':str(b),'k':str(k),'c':str(c),'level':level,'step':str(step),'version':VERSION}
 folder=Path(output_dir) if output_dir else HERE/'plots'/VERSION;folder.mkdir(parents=True,exist_ok=True)
 key=digest(data);png=folder/(key+'.png');side=png.with_suffix('.json');qa=png.with_suffix('.qa.json')
 if not all(x.exists() for x in (png,side,qa)):
  fd,name=tempfile.mkstemp(prefix='input-',suffix='.json',dir=folder)
  try:
   with os.fdopen(fd,'w') as f:json.dump(dict(data,output=str(png)),f)
   subprocess.run([sys.executable,str(HERE/'render.py'),name],check=True,capture_output=True)
  finally:Path(name).unlink(missing_ok=True)
 return png,json.loads(side.read_text()),json.loads(qa.read_text())
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Source supports radio only')
 rng=random.Random(seed);raw=bool(profile and profile.startswith('source:'));sid=profile[7:] if raw else None
 kind='parameters' if level=='easy' else 'equation';expected='read_parameters' if level=='easy' else 'read_equation' if level=='moderate' else 'read_grid_equation'
 if template not in (None,expected,'source' if raw else expected):raise ValueError('Incompatible template')
 if raw:
  if sid not in SPECS:raise ValueError('Unknown source')
  spec=SPECS[sid]
  if level!=spec[0]:raise ValueError('Incompatible source level')
  style=spec[4];recipes=spec[5]
  if parameters is None:parameters=dict(zip(('b','k','c'),map(str,spec[1:4])))
 else:
  style='compact';profile=profile or rng.choice(list(BANKS));
  if profile not in BANKS:raise ValueError('Unknown complete bank')
  recipes=BANKS[profile]
 for attempt in range(500):
  p=parameters
  if p is None:
   if level=='hard':
    step=rng.choice([sp.Rational(1,2),sp.Rational(1,4)]);ks=[step*i for i in range(4,25) if 1<=step*i<=6 and (step*i).q>1];cs=[step*i for i in range(-16,17) if 0<abs(step*i)<=6 and (step*i).q>1]
    p={'b':rng.randint(2,6),'k':str(rng.choice(ks)),'c':str(rng.choice(cs)),'step':str(step)}
   else:p={'b':rng.randint(2,6),'k':str(rng.choice([sp.Rational(i,2) for i in range(2,13)])) if level=='moderate' else rng.randint(1,6),'c':rng.choice([i for i in range(-6,7) if i])}
  try:
   b,k,c,step=domain(level,p,raw);values,objects,correct=bank(b,k,c,step,recipes,kind,style);break
  except ValueError:
   if parameters is not None:raise
 else:raise RuntimeError('No complete eligible bank')
 q={};asset=None;original=False
 if raw:
  oq=SOURCES[sid];ob,ok,oc=map(rat,SPECS[sid][1:4]);original=(b,k,c)==(ob,ok,oc)
  # Complete exponential component substitution retains original spacing/prose.
  old='{'+str(ob)+'}^{x}' if style=='compact' else str(ob)+'^{x}';new='{'+str(b)+'}^{x}' if style=='compact' else str(b)+'^{x}'
  problem=oq[':question/problem'].replace(old,new)
  sol=solution(b,k,c,kind) if ':question/worked-solution' in oq else None
  present_correct=':answer-field/correct' in oq[':question/answer-fields'][0]
  if ':question/difficulty' in oq:q[':question/difficulty']=':question.difficulty/'+level
 else:
  present_correct=True;q[':question/difficulty']=':question.difficulty/'+level
  problem='The graph above shows $y=k({'+str(b)+'}^{x})+c.$ '+('Find the value of $k$ and $c.$' if kind=='parameters' else 'Determine the values of $k$ and $c$ and find the equation of the curve.')
  sol=solution(b,k,c,kind)
  if level=='hard':sol=sol.replace('The labeled point on the graph is','Reading the calibrated grid, the marked point on the graph is')
 if not original:
  png,side,qa=render_plots(b,k,c,level,step);asset={'path':str(png),'sidecar':side,'readback':qa}
  problem=re.sub(r'!\[\]\([^)]*\)','![]('+str(png)+')',problem) if raw else '![]('+str(png)+')\n\n'+problem
 q[':question/problem']=problem
 if sol is not None:q[':question/worked-solution']=sol
 content=digest({'version':VERSION,'question':q,'values':sorted(values),'correct_present':present_correct})
 qid=uid(content);fid=uid(qid+':selection');answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/text' if kind=='parameters' else ':answer.type/math',':answer/value':v} for v in values]
 correctid=answers[correct][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if present_correct:field[':answer-field/correct']=[':answer/id',correctid]
 q.update({':question/id':qid,':question/answer-fields':[field]})
 return {'knowledge_point':{'db_id':KP,'id':K[':knowledge-point/id'],'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':'source' if raw else expected,'bank_profile':profile,'parameters':{'b':str(b),'k':str(k),'c':str(c),'step':str(step)},'recipes':recipes,'mathematical_fingerprint':digest({'k':str(k),'c':str(c),'response':kind,'b':None,'grid':str(step) if level=='hard' else None}),'content_fingerprint':content,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'source':{x:y for x,y in SNAPSHOT.items() if x!='record'},'source_id':sid,'evidence_only':raw,'eligible_for_learning':not raw,'inferred_correct_value':pair(k,c,style) if kind=='parameters' else eq(b,k,c,style),'authored_level':level=='hard' or raw and ':question/difficulty' not in SOURCES[sid],'plot':asset}}

# EASY (observed): read two labeled integer coordinates, subtract c from the
# intercept, select k/c. b=2..6, k=1..6, nonzero c=-6..6, |intercept|<=10.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (observed): same labeled asymptote/intercept and subtraction, then
# assemble the complete equation with its PROVIDED base; k can be a half-integer.
# No base recovery, logarithms, nonzero-x substitution or negative stretch.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): infer both coordinates from calibrated half/quarter grid,
# subtract noninteger signed values, and assemble equation. k,c both noninteger,
# marked intercept nonzero; same bounds. Every hard instance has this workload.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0];correct=f.get(':answer-field/correct',[None,None])[1]
 status='difficulty='+q.get(':question/difficulty','unrated').split('/')[-1]+'; authored_level='+str(g['authored_level']).lower()+'; inferred_correct='+str(g['evidence_only'] and ':answer-field/correct' not in f).lower()+'; evidence_only='+str(g['evidence_only']).lower()
 out='\n\n**'+('SOURCE '+g['source_id'] if g['evidence_only'] else 'GENERATED '+q[':question/difficulty'].split('/')[-1])+'**\n\n'+status+'\n\n'+q[':question/problem']+'\n\n'
 for a in f[':answer-field/choices']:out+='- '+('**Correct:** ' if a[':answer/id']==correct else '')+(a[':answer/value'] if a[':answer/type'].endswith('/text') else '$'+a[':answer/value']+'$')+'\n'
 return out+'\n'+q.get(':question/worked-solution','[Original worked solution absent; correct designation also absent.]')+'\n'
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else ''.join(markdown(r) for r in records))
