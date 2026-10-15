"""Finding partial derivatives of two-variable functions. Draft, no EDB writes.

Twelve original MA termwise banks; explicit held/target roles. Each recipe computes
all five options and five operative solution stages from a single exact instance.
Raw omission replay is evidence-only; hard three-term sums are authored extensions.
"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, importlib.util, json, random, re, uuid
from pathlib import Path
import sympy as S
ROOT = Path(__file__).resolve().parent / '17592186124639-draft'
REPO = ROOT.parents[2]
spec = importlib.util.spec_from_file_location('kp124639_math_format', REPO/'scripts/question_capture/math_format.py')
MF = importlib.util.module_from_spec(spec); spec.loader.exec_module(MF)
VERSION='partial-two-variable-v1'
SOURCE=json.loads((ROOT/'source.json').read_text())
KP=SOURCE['record']; X,Y=S.symbols('x y', real=True)
NS=uuid.UUID('8e4c7404-773f-57ef-bfcc-bdb56d67ff31')
ORIGINALS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
SPECS={
 'cos_poly':('q-132241','easy',{'a':1,'b':1,'n':2,'m':2,'target':'y'}),
 'sin_poly':('q-35709','easy',{'a':1,'b':1,'n':2,'target':'x'}),
 'log':('q-159613','easy',{'a':1,'b':1,'n':2,'target':'y'}),
 'reciprocal':('q-159616','easy',{'a':1,'b':1,'n':2,'target':'x'}),
 'asin':('q-159619','moderate',{'a':1,'b':8,'target':'x'}),
 'exp_sum':('q-159623','moderate',{'a':2,'b':3,'m':2,'n':3,'target':'y'}),
 'tan_power':('q-159611','easy',{'a':1,'b':1,'n':3,'base':3,'target':'y'}),
 'constant_sin':('q-159614','easy',{'a':5,'b':2,'target':'x'}),
 'power_ratio':('q-159618','moderate',{'a':1,'b':6,'n':3,'m':4,'target':'x'}),
 'inverse_power':('q-159621','moderate',{'a':8,'b':3,'n':4,'m':4,'k':2,'target':'x'}),
 'cross_exp':('q-159624','moderate',{'a':1,'b':1,'target':'y'}),
 'atan':('q-159612','easy',{'a':3,'b':1,'n':2,'target':'y'}),
 'hard_log_exp':(None,'hard',{'a':2,'b':3,'c':2,'n':3,'m':2,'target':'y'}),
 'hard_trig_reciprocal':(None,'hard',{'a':3,'b':2,'c':4,'n':3,'m':2,'target':'x'}),
}

def tex(e):
 return MF.normalize_tex(S.latex(e, mul_symbol=None, inv_trig_style='full', ln_notation=True, order='lex'))
def ident(value): return str(uuid.uuid5(NS,json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'))))
def c0(text):
 if any(ord(c)<32 and c not in '\n\t' for c in text): raise ValueError('C0 control character')
def exprs(name,p):
 """Return ordered (held coefficient,target factor) components and complete bank.
 Each wrong expression is an explicit observed operation pattern, not perturbation.
 """
 u=X if p['target']=='x' else Y; v=Y if u==X else X
 a=S.Integer(p.get('a',1));b=S.Integer(p.get('b',1));c=S.Integer(p.get('c',1))
 n=p.get('n',2);m=p.get('m',2);k=p.get('k',2);B=S.Integer(p.get('base',3))
 if name=='sin_poly':
  parts=[(a*S.sin(v),u**n),(b*v,u)];C=a*n*u**(n-1)*S.sin(v)+b*v
  bank=[a*u**n*S.cos(v)+b*v,a*u**n*S.cos(v)+b*u,a*u**(n-1)*S.sin(v)+b*u,C,a*n*v**(n-1)*S.sin(v)+b*u]
 elif name=='cos_poly':
  parts=[(a*v,u**n),(b*v**m,S.cos(u))];C=a*n*v*u**(n-1)-b*v**m*S.sin(u)
  bank=[C,a*n*u**(n-1)-b*S.sin(u),a*u**n+b*m*v**(m-1)*S.sin(u),a*u**n-b*m*v**(m-1)*S.sin(u),a*n*v*u**(n-1)+b*v**m*S.sin(u)]
 elif name=='log':
  parts=[(a*v,u),(b*v**n,S.log(u))];C=a*v+b*v**n/u
  bank=[C,a*v*u+b*v**n/u,a*v+b*v**n*S.log(u),a*u+b*n*v**(n-1)*S.log(u),a*u+b*n*v**(n-1)/u]
 elif name=='reciprocal':
  parts=[(a/v,u),(-b*v,u**(-n))];C=a/v+b*n*v/u**(n+1)
  bank=[-a/v**2+b*n/u**(n+1),a*u/v+b*n*v/u**(n+1),C,-a*u/v**2-b/u**n,a/v-b*v/u**n]
 elif name=='asin':
  parts=[(a*v,S.asin(u)),(-b*v**2,S.Integer(1))];C=a*v/S.sqrt(1-u**2)
  bank=[C,C-2*b*v,a*S.asin(u)-2*b*v,a/S.sqrt(1-u**2),a*v*S.asin(u)]
 elif name=='exp_sum':
  parts=[(S.exp(a*v),S.exp(b*u)),(v**m,u**n)];E=S.exp(a*v+b*u);C=b*E+n*v**m*u**(n-1)
  bank=[E+n*v**m*u**(n-1),a*b*E+m*n*v**(m-1)*u**(n-1),b*E+m*n*v**(m-1)*u**(n-1),a*E+m*v**(m-1)*u**n,C]
 elif name=='tan_power':
  parts=[(a*v**n,S.tan(u)),(-b*B**v,B**u)];E=B**(u+v);C=a*v**n*S.sec(u)**2-b*E*S.log(B)
  bank=[a*v**n*S.sec(u)**2-b*E,a*n*v**(n-1)*S.tan(u)-b*E*S.log(B),C,a*v**n*S.csc(u)**2-b*E*S.log(B),a*n*v**(n-1)*S.tan(u)-b*E]
 elif name=='constant_sin':
  parts=[(a,v),(-b,S.sin(u))];C=-b*S.cos(u)
  bank=[a-b*S.cos(u),a-b*S.sin(u),b*S.sin(u),a*v-b*S.sin(u),C]
 elif name=='power_ratio':
  parts=[(a/v**m,u**n),(b*v,u)];C=a*n*u**(n-1)/v**m+b*v
  bank=[-a*m*u**n/v**(m+1)+b*u,a*n*m*u**(n-1)/v**m+b,a*m*u**n/v**(m+1)+b*v,C,-a*n*m*u**(n-1)/v**(m+1)+b]
 elif name=='inverse_power':
  parts=[(a*v**m,u),(b*v**k,u**(-n))];C=a*v**m-b*n*v**k/u**(n+1)
  bank=[a*m*v**(m-1)-b*n*k*v**(k-1)/u**(n+1),a*m*u*v**(m-1)+b*k*v**(k-1)/u**n,a*m*u*v**(m-1)-b*n*v**k/u**(n+1),C,a*v**m+b*k*v**(k-1)/u**n]
 elif name=='cross_exp':
  parts=[(a*v,S.exp(u)),(b*S.exp(v),u)];C=a*v*S.exp(u)+b*S.exp(v)
  bank=[C,a*S.exp(u),a*S.exp(u)+b*u*S.exp(v),a*S.exp(u)+b*S.exp(v),b*S.exp(v)]
 elif name=='atan':
  parts=[(a,S.atan(u)),(-b*v,u**n)];C=a/(1+u**2)-b*n*v*u**(n-1)
  bank=[-b*u**n,a*S.atan(u)-b*u**n,a*b*n*v*u**(n-1)/(1+u**2),a/(1+u**2)-b*u**n,C]
 elif name=='hard_log_exp':
  parts=[(a*v**m,S.log(u)),(b*v,S.exp(u)),(-c*v**2,u**(-n))]
  ds=[h*S.diff(g,u) for h,g in parts];C=sum(ds)
  bank=[C,ds[0]+ds[1]-ds[2],a*v**m*S.log(u)+ds[1]+ds[2],ds[0]+b*S.exp(u)+ds[2],S.diff(sum(h*g for h,g in parts),v)]
 elif name=='hard_trig_reciprocal':
  parts=[(a*v**m,S.sin(u)),(b*v,S.atan(u)),(-c*v**2,u**(-n))]
  ds=[h*S.diff(g,u) for h,g in parts];C=sum(ds)
  bank=[C,ds[0]+ds[1]-ds[2],a*v**m*S.sin(u)+ds[1]+ds[2],ds[0]+b/(1+u**2)+ds[2],S.diff(sum(h*g for h,g in parts),v)]
 else: raise ValueError('unknown template')
 return u,v,parts,bank,C

def signed_join(items):
 return ''.join(('+' if i and not z.startswith('-') else '')+z for i,z in enumerate(items))
def derivative(g,u):return r'\frac{∂}{∂'+str(u)+'}('+tex(g)+')'
def product(h,g):
 if h==1:return tex(g)
 if h==-1:return '-'+tex(g)
 return tex(h*g)
def row_data(name,p):
 u,v,parts,bank,C=exprs(name,p)
 # Preserve each source family’s original term order, sign, exponent splitting,
 # held-coefficient extraction and unevaluated numerical derivative products.
 terms=[product(h,g) for h,g in parts]
 if name=='exp_sum': terms[0]=tex(S.exp(p['a']*v+p['b']*u))
 if name=='tan_power': terms[1]='-'+tex(p['b']*S.Integer(p['base'])**(u+v))
 F=signed_join(terms)
 split=[];extract=[];evaluated=[]
 for i,(h,g) in enumerate(parts):
  sign='-' if h.could_extract_minus_sign() else ''
  ah=-h if sign else h
  # Source constant_sin differentiates the held variable itself, whereas
  # asin's entirely held term is factored into d/du(1).
  split.append(sign+derivative(ah*g,u))
  extract.append(sign+tex(ah)+r'\cdot '+derivative(g,u))
  dg=S.sec(u)**2 if name=='tan_power' and i==0 else S.diff(g,u)
  evaluated.append(sign+tex(ah)+r'\cdot '+('('+tex(dg)+')' if name in ('sin_poly','reciprocal','constant_sin','inverse_power') or dg.could_extract_minus_sign() else tex(dg)))
 if name=='exp_sum':
  split[0]=derivative(S.exp(p['a']*v)*S.exp(p['b']*u),u)
  # Keep explicitly separated exponential factors even though SymPy can combine.
  split[0]=r'\frac{∂}{∂'+str(u)+'}('+tex(S.exp(p['a']*v))+r'\cdot '+tex(S.exp(p['b']*u))+')'
 if name=='tan_power':
  split[1]='-'+r'\frac{∂}{∂'+str(u)+'}('+tex(p['b']*S.Integer(p['base'])**v)+r'\cdot '+tex(S.Integer(p['base'])**u)+')'
 if name=='asin':evaluated[1]='-0'
 return F,[r'\frac{∂}{∂'+str(u)+'}('+F+')',signed_join(split),signed_join(extract),signed_join(evaluated),tex(C)]

def validate_parameters(name,p):
 expected=SPECS[name][2]
 if set(p)!=set(expected): raise ValueError('parameter keys must equal '+str(sorted(expected)))
 if p['target'] not in ('x','y'):raise ValueError('target must be x or y')
 for k,v in p.items():
  if k=='target':continue
  if isinstance(v,bool) or not isinstance(v,int):raise ValueError('integer parameters required')
  bounds=(2,4) if k in ('n','m','k','base') else (1,9)
  if not bounds[0]<=v<=bounds[1]:raise ValueError('out of scope '+k)
 if name=='exp_sum' and p['a']==p['b']:raise ValueError('distinct exponential slopes required for full observed bank')
 # Reject every colliding complete bank, including wrong/wrong equivalence.
 _,_,_,bank,C=exprs(name,p)
 for i,e in enumerate(bank):
  for z in bank[:i]:
   if S.expand(e-z)==0:raise ValueError('colliding complete bank')

def sample(name,rng):
 p=dict(SPECS[name][2])
 for k in p:
  if k=='target':p[k]=rng.choice(['x','y'])
  elif k in ('n','m','k','base'):p[k]=rng.randint(2,4)
  else:p[k]=rng.randint(1,9)
 return p

def raw_layout(name,p,F,rows):
 """Parameterized source prose/masks, no original-payload return branch.
 Shared prose is preserved and mathematical spelling is normalized;
 generated solution stages remain the same five operations.
 """
 sid,level,_=SPECS[name];u=p['target']
 sub=level=='moderate' or name=='cos_poly' or level=='hard'
 op=('{f}_{'+u+'}(x,y)') if sub else (r'\frac{∂f}{∂'+u+'}')
 if name=='cos_poly':problem='Find $f_{'+u+'}(x, y)$ for $f(x, y) = '+F+'$.'
 elif sub:problem='Find $'+op+'$ for $f(x,y)='+F+'.$'
 else:problem='Find $'+op+'$ given that $f(x,y)='+F+'.$'
 intro=('The notation ${f}_{'+u+'}$ denotes the partial derivative of $f$ with respect to $'+u+'.$\n\n') if sub and name!='cos_poly' else ''
 intro+='We differentiate the given function with respect to $'+u+',$ treating all other variables as constants.\n\n'
 rule='constant multiple rule' if name=='reciprocal' else 'sum rule' if name=='exp_sum' else 'sum and constant multiple rules'
 intro+='Additionally, we use the '+rule+' for differentiation, as follows:\n\n'
 solution=intro+'$$\n'+r'\begin{aligned}'+op+' & ='+(' \\\\  & ='.join(rows))+r'\end{aligned}'+'\n$$'
 return MF.normalize_prose(problem),MF.normalize_prose(solution)

@MF.checked_math_content
def _generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only source radio layout')
 rng=random.Random(seed)
 eligible=[n for n,s in SPECS.items() if s[1]==level]
 name=template or rng.choice(eligible)
 if name not in eligible:raise ValueError('template difficulty boundary')
 if profile not in (None,'observed','raw','completed','authored'):raise ValueError('unknown profile')
 if profile=='raw' and SPECS[name][0] is None:raise ValueError('no raw original')
 if profile=='observed' and SPECS[name][0]=='q-132241':raise ValueError('unrated missing-key source requires raw or completed')
 if parameters is not None:
  p=dict(parameters);validate_parameters(name,p)
 else:
  for _ in range(200):
   p=sample(name,rng)
   try:validate_parameters(name,p);break
   except ValueError:continue
  else:raise ValueError('no eligible full bank')
 u,v,parts,bank,C=exprs(name,p);F,rows=row_data(name,p)
 problem,solution=raw_layout(name,p,F,rows)
 values=[tex(e) for e in bank]
 source_id=SPECS[name][0]
 # Raw omissions are preserved exactly; formatting decorator needs the solution
 # during validation, then raw q132241 removal is performed by public raw_replay.
 payload={'version':VERSION,'level':level,'problem':problem,'solution':solution,'values':sorted(values),'parameters':p,'template':name,'profile':'raw' if profile=='raw' else 'completed'}
 qid=ident(payload);fid=ident([qid,'selection'])
 answers=[{':answer/id':ident([fid,z]),':answer/type':':answer.type/math',':answer/value':z} for z in values]
 idx=next(i for i,e in enumerate(bank) if e==C)
 correct=answers[idx][':answer/id'];rng.shuffle(answers)
 q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 for text in [problem,solution,*values]:c0(text)
 tu,tv=S.symbols('target held', real=True)
 task=S.srepr(S.simplify(S.diff(sum(h*g for h,g in parts),u)).subs({u:tu,v:tv}, simultaneous=True))+'|components='+str(len(parts))
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':name,'seed':seed,'parameters':p,'source_id':source_id,'bank_profile':profile or ('observed' if source_id and source_id!='q-132241' else 'completed' if source_id else 'authored'),'source_basis':SOURCE['basis'],'target_variable':str(u),'held_constant_variable':str(v),'mathematical_fingerprint':hashlib.sha256(task.encode()).hexdigest(),'eligible_for_learning':profile!='raw','evidence_only':profile=='raw','domain':domain(name,p),'runtime':{'python':sys.version.split()[0],'sympy':S.__version__}}}

def domain(name,p):
 u=p['target'];v='y' if u=='x' else 'x'
 if name in ('log','hard_log_exp'):return u+'>0'
 if name=='asin':return '-1<'+u+'<1'
 if name in ('reciprocal','inverse_power','hard_trig_reciprocal'):return u+'!=0'+(' and '+v+'!=0' if name=='reciprocal' else '')
 if name=='power_ratio':return v+'!=0'
 if name=='tan_power':return 'cos('+u+')!=0'
 return 'real x,y'

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 r=_generate(level,seed,template,field_type,parameters,profile)
 if profile=='raw':
  src=ORIGINALS[SPECS[r['generation']['template']][0]]
  for key in (':question/difficulty',':question/worked-solution'):
   if key not in src:r['question'].pop(key,None)
  for f,s in zip(r['question'][':question/answer-fields'],src[':question/answer-fields']):
   if ':answer-field/correct' not in s:f.pop(':answer-field/correct',None)
 return r

def raw_replay(template,parameters=None,seed=0):
 """Raw missing attributes remain absent, independently of completed generation."""
 p=parameters or SPECS[template][2]
 r=generate(SPECS[template][1],seed,template,parameters=p,profile='raw')
 src=ORIGINALS[SPECS[template][0]]
 for key in (':question/difficulty',':question/worked-solution'):
  if key not in src:r['question'].pop(key,None)
 for f,s in zip(r['question'][':question/answer-fields'],src[':question/answer-fields']):
  if ':answer-field/correct' not in s:f.pop(':answer-field/correct',None)
 return r

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];out=['### '+q.get(':question/difficulty','unrated').split('/')[-1]+' — '+r['generation']['template'],'Bank profile: `'+r['generation']['bank_profile']+'`',q[':question/problem']]
 for f in q[':question/answer-fields']:
  out.append('Field `'+f[':answer-field/key']+'` — '+f[':answer-field/type'])
  for a in f[':answer-field/choices']:out.append('- $'+a[':answer/value']+'$'+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
 out.append(q.get(':question/worked-solution','[Source worked solution absent.]'))
 return '\n\n'.join(out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n'.join(markdown(r) for r in records))
