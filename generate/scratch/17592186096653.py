#!/usr/bin/env python3
"""KP 96653: internal ratio position vectors, basis 1356. Steps 3–7 only.

All sources are moderate except one unrated record. Easy and hard are authored
ratio-arithmetic peers of the same two-vector internal-section method; no extra
path, external division, coordinate solving or coefficient matching is added.
Observed banks are explicit component recipes with underdetermined intent, used
only on request. Default radio bank is a complete authored operation bank.
The four reversed blank keys remain in observed profiles; normal outputs repair
them. Source-shaped prompts and fixed ordered worked solutions are mask-rendered
for changed ratios. Every field has owned UUIDs; identity excludes option order.
"""
from pathlib import Path
import argparse,hashlib,json,random,re,subprocess,sys,tempfile,uuid
import sympy as sp
KP_ID=17592186096653
KP_UUID='feae36e7-ae88-5f3a-957f-e65a92e399ad'
TITLE='Expressing a Vector That Satisfies a Ratio in Terms of Known Vectors'
VERSION='ratio-vector-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
R,S=sp.symbols('r s',positive=True);D=R+S
# Whole banks. Numeric constants here are fixed candidate ratio structures or
# explicit numerator operations, not inferred historical error diagnoses.
BANKS={
'q-12212':[(1,R/D),(2*R/(2*R+S),S/(2*R+S)),(S/(2*R+S),2*R/(2*R+S)),(R/D,1),(S/D,R/D)],
'q-42659':[((R+S)/(2*R+S),R/(2*R+S)),(S/D,R/D),(sp.Rational(1,2),sp.Rational(1,2)),(R/D,S/D),(R/(2*R+S),(R+S)/(2*R+S))],
'q-120285':[(R/D,S/D),(2*R/D,1-2*R/D),(sp.Rational(1,2),sp.Rational(1,2)),(S/D,R/D),(1-2*R/D,2*R/D)],
'q-120294':[(S/D,R/D),(sp.Rational(1,3),sp.Rational(2,3)),(R/D,S/D),((R-S)/R,S/R),(sp.Rational(2,3),sp.Rational(1,3))],
'q-120303':[((D+R)/D**2,1-(D+R)/D**2),(S/D,R/D),(sp.Rational(1,2),sp.Rational(1,2)),(R/D,S/D),(1-(D+R)/D**2,(D+R)/D**2)],
'q-12214':[(-S/D,R/D),(S/D,-R/D),((S-R)/D,R/D),(S/D,R/D),(S/(2*D),R/D)],
'q-12233':[((S-1)/D,-(R+1)/D),((S-1)/D,(R+1)/D),(S/D,(R+1)/D),(S/D,R/D),(S/D,-R/D)],
'q-12235':[(2*S/D,-(R-S)/D),(R/D,S/D),(S/D,R/D),(2*S/D,(R-S)/D),(S/D,-R/D)],
'q-278290':[(1,R/S),(S/R,1/R),(S/D,R/D),(1/R,1/S),(R/D,S/D)],
'q-42669':[(sp.Rational(1,3),sp.Rational(2,3)),(-R/D,S/D),(S/D,R/D),(sp.Rational(2,3),sp.Rational(1,3)),(sp.Rational(2,3),-sp.Rational(1,3))],
'q-120304':[(sp.Rational(1,2),sp.Rational(1,2)),((S+3)/D,(R-3)/D),(R/D,S/D),((S-2)/D,(R+1)/D),(S/D,R/D)],
'q-278288':[(S/R,1/R),(R/D,S/D),(1,S/R),(S/D,R/D),(1/D,1)],
'q-120289':[((R-1)/D,(S+1)/D),(S/D,R/D),(R/D,S/D),((S+1)/D,(R-1)/D),((S+2)/D,(R-2)/D)]}
REVERSED={'q-278263','q-322568','q-322576','q-322586'}
def tex(x):return sp.latex(sp.sympify(x)) .replace(r'\frac{',r'\frac{').replace('}{','}{')
def frac(x):
 x=sp.Rational(x)
 return str(x.p) if x.q==1 else '\\frac{'+str(x.p)+'}{'+str(x.q)+'}'
def v(name):return '\\overset{\\to }{'+name+'}'
def parameters_for(q):
 prompt=q[':question/problem'];ratio=re.search(r'([A-Z])([A-Z]):\s*\2([A-Z])\s*=\s*(\d+):\s*(\d+)',prompt)
 if not ratio:raise ValueError(prompt)
 A,X,B,r,s=ratio.groups()
 math=re.findall(r'\$(.*?)\$',prompt,re.S)
 if 'OP^(→)' in prompt:u,w='p','q'
 else:
  u=re.search(r'\{O'+A+r'\}=([a-z])',prompt).group(1);w=re.search(r'\{O'+B+r'\}=([a-z])',prompt).group(1)
 return dict(A=A,B=B,X=X,u=u,v=w,r=int(r),s=int(s))
def solution(p):
 A,B,X,u,w,r,s=[p[k] for k in ('A','B','X','u','v','r','s')];t=frac(sp.Rational(r,r+s));a=frac(sp.Rational(s,r+s))
 return f"From the diagram, we see that\n\n$$\n{v('O'+X)}={v('O'+A)}+{v(A+X)}.\n$$\n\nWe're told that ${v('O'+A)}={u},$ so we just need to work out ${v(A+X)}.$\n\nFirst, from $△O{A}{B},$ we have\n\n$$\n\\begin{{aligned}}{v(A+B)} & ={v(A+'O')}+{v('O'+B)} \\\\  & =-{v('O'+A)}+{v('O'+B)} \\\\  & =-{u}+{w} \\\\  & ={w}-{u}.\\end{{aligned}}\n$$\n\nSince ${A}{X}:{X}{B}={r}:{s},$ we have\n\n$$\n{v(A+X)}={t}{v(A+B)}={t}({w}-{u}).\n$$\n\nTherefore,\n\n$$\n\\begin{{aligned}}{v('O'+X)} & ={v('O'+A)}+{v(A+X)} \\\\  & ={u}+{t}({w}-{u}) \\\\  & ={a}{u}+{t}{w}.\\end{{aligned}}\n$$"
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'kp96653:'+x))
def render_plots(p,output_dir=None):
 folder=Path(output_dir) if output_dir else HERE/'plots';folder.mkdir(exist_ok=True);target=folder/(digest(p)[:24]+'.png')
 if target.exists() and Path(str(target)+'.json').exists():return str(target.resolve())
 with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='ratio-',dir=folder,delete=False) as f:json.dump(p,f);input_path=Path(f.name)
 tmp=target.with_name(target.stem+'-'+uuid.uuid4().hex+'.png')
 try:
  subprocess.run([sys.executable,str(HERE/'render.py'),str(input_path),str(tmp)],check=True,stdout=subprocess.DEVNULL)
  tmp.replace(target);Path(str(tmp)+'.json').replace(Path(str(target)+'.json'))
 finally:input_path.unlink(missing_ok=True)
 return str(target.resolve())
def option(p,a,b,prefix=None,order=None):
 # Signed coefficient groups avoid +- and --. Keep course vector notation.
 terms={p['u']:sp.Rational(a),p['v']:sp.Rational(b)};body=''
 for name in order or [p['u'],p['v']]:
  c=terms[name];sign='-' if c<0 else ('+' if body else '');body+=sign+('' if abs(c)==1 else frac(abs(c)))+name
 return (prefix or v('O'+p['X']))+'='+body

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 rng=random.Random(seed);repaired=bool(profile and profile.endswith('-repaired'));source_profile='q-12212' if profile=='q-12212-legacy' else (profile.removesuffix('-repaired') if repaired else profile);observed=source_profile in QS
 if profile and not observed and profile!='authored':raise ValueError('unknown profile')
 if observed:
  if level!='moderate':raise ValueError('observed profiles are moderate replay peers')
  q=QS[source_profile];base=parameters_for(q);kind='coefficients' if len(q[':question/answer-fields'])==2 and source_profile!='q-12212' else 'radio'
 else:
  kind=template or ('coefficients' if field_type=='blank' or rng.randrange(2) else 'radio');q=None;base=dict(A='A',B='B',X='T',u='a',v='b')
 if template and template!=kind:raise ValueError('layout mismatch')
 if kind not in ('radio','coefficients'):raise ValueError('template')
 if field_type and field_type!=('blank' if kind=='coefficients' else 'radio'):raise ValueError('field type')
 if parameters is not None:
  if set(parameters)!=set(base)|{'r','s'}:raise ValueError('exact parameter keys required')
  p=dict(parameters)
 else:
  p=dict(base)
  if not observed:
   bound={'easy':4,'moderate':12,'hard':20}[level]
   pairs=[(r,s) for r in range(1,bound+1) for s in range(1,bound+1) if (level!='hard' or min(r,s)>=5 and r+s>=19 and sp.gcd(r,s)==1) and (kind!='radio' or r!=s)]
   p['r'],p['s']=rng.choice(pairs)
 if not isinstance(p['r'],int) or not isinstance(p['s'],int) or min(p['r'],p['s'])<1:raise ValueError('positive integer ratio required')
 if observed and max(p['r'],p['s'])>12:raise ValueError('observed moderate ratio bound')
 if not observed:
  bound={'easy':4,'moderate':12,'hard':20}[level]
  if max(p['r'],p['s'])>bound or level=='hard' and (min(p['r'],p['s'])<5 or p['r']+p['s']<19 or sp.gcd(p['r'],p['s'])!=1):raise ValueError('level arithmetic bound')
 for k in ('A','B','X'):
  if not re.fullmatch('[A-Z]',p[k]) or p[k]=='O':raise ValueError('point label')
 if len({p[k] for k in ('A','B','X')})<3 or not all(re.fullmatch('[a-z]',p[k]) for k in ('u','v')) or p['u']==p['v']:raise ValueError('distinct labels')
 if observed and any(p[k]!=base[k] for k in ('A','B','X','u','v')):raise ValueError('observed text masks retain labels; ratio varies')
 r,s=p['r'],p['s'];t=sp.Rational(r,r+s);a=1-t
 image=render_plots(p)
 if observed:
  prompt=q[':question/problem'];prompt=re.sub(r'!\[\]\(.*?\)','![]('+image+')',prompt)
  prompt=re.sub(r'=\s*\d+:\s*\d+',lambda m:re.sub(r'\d+',lambda n:str(r) if n.start()==len(re.match(r'=\s*',m.group()).group()) else str(s),m.group()),prompt)
  # Exact ratio spacing is retained; replacement above operates on complete ratio.
 else:
  A,B,X,u,w=[p[k] for k in ('A','B','X','u','v')]
  prompt=f'![]({image})\n\nConsider the diagram above, where ${v("O"+A)}={u},$ ${v("O"+B)}={w}$ and ${X}$ divides $\\overset{{―}}{{{A+B}}}$ in the ratio ${A+X}:{X+B}={r}:{s}.$ '
  prompt+=f'Find ${v("O"+X)}.$' if kind=='radio' else f'Express ${v("O"+X)}$ via the vectors ${u}$ and ${w}$.\n\n$\\,{v("O"+X)}=$\n{{{{field-1}}}}\n${u}+$\n{{{{field-2}}}}\n${w}$'
 sol=solution(p);banks=[];correct_indices=[]
 if kind=='coefficients':
  vals=[a,t]
  if observed and source_profile in REVERSED and not repaired:vals=[t,a]
  banks=[[frac(x)] for x in vals];correct_indices=[0,0]
 elif observed:
  pairs=[tuple(sp.sympify(z).subs({R:r,S:s}) for z in pair) for pair in BANKS[source_profile]]
  oldfields=q[':question/answer-fields'];oldfield=oldfields[0] if profile=='q-12212-legacy' else oldfields[-1]
  # Preserve source option order/component order and prefix notation. q12212
  # authoritative field has a different order from the legacy profile.
  original=oldfield[':answer-field/choices']
  if source_profile=='q-12212' and profile!='q-12212-legacy':pairs=[pairs[3],pairs[4],pairs[1],pairs[2],pairs[0]]
  for old,pair in zip(original,pairs):
   rhs=old[':answer/value'].split('=')[-1];order=re.findall(r'[a-z](?![a-z])',re.sub(r'\\frac','',rhs));order=[x for x in order if x in (p['u'],p['v'])]
   banks.append(option(p,*pair,prefix=old[':answer/value'].split('=')[0].strip(),order=order))
  banks=[banks];correct_indices=[next(i for i,pair in enumerate(pairs) if pair==(a,t))]
 else:
  pairs=[(a,t),(t,a),(1,t),(a,-t),(-a,t)]
  banks=[[option(p,*pair) for pair in pairs]];correct_indices=[0]
 if kind=='radio' and len(set(pairs))!=5:raise ValueError('whole bank collision')
 identity=digest({'version':VERSION,'prompt':prompt,'solution':sol,'banks':[sorted(b) for b in banks]})
 question_id=uid(identity);fields=[]
 for i,(bank,ci) in enumerate(zip(banks,correct_indices)):
  key='selection' if kind=='radio' else 'field-'+str(i+1);fid=uid(identity+key)
  choices=[{':answer/id':uid(fid+value),':answer/type':':answer.type/math',':answer/value':value} for value in bank]
  correct=choices[ci][':answer/id'];rng.shuffle(choices)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if kind=='radio' else 'blank'),':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':question_id,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'parameters':p,'template':kind,'bank_profile':profile or 'authored','observed':observed,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'mathematical_fingerprint':digest([str(a),str(t)]),'content_fingerprint':identity,'raw_wrong_blank_key':observed and source_profile in REVERSED and not repaired,'mathematical_repair':repaired,'plot':image}}
# Easy: authored small positive integer ratios <=4, same one internal-section path.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: observed arithmetic includes positive ratios through 12, total <=24.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: authored coprime ratio entries 5..20, total >=19; no additional operation.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 rows=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in rows))
