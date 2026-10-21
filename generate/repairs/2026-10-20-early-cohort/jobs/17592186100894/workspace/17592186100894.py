#!/usr/bin/env python3
"""Rearrange/separate IVPs: complete observed banks under x-coordinate translation.

No database access. h in {-4,...,4}; h=0 replays source. Translation changes
ODE coefficients/arguments and the initial abscissa together, preserving the
rearrangement, integration, inversion, response fragment and solution stages.
Empirical banks are whole source-expression profiles, with no inferred error
intent. q-104058 is excluded: its initial condition makes 0*y'=2.
"""
import argparse, copy, hashlib, importlib.util, json, random, re, sys, uuid
from pathlib import Path
try:
 import sympy as s
except ModuleNotFoundError:
 # The application's worker may use system Python; reuse the repo environment.
 venv=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__' and venv.is_file() and Path(sys.executable)!=venv:
  import os
  os.execv(str(venv),[str(venv),str(Path(__file__).resolve()),*sys.argv[1:]])
 raise
ROOT=Path(__file__).resolve().parent.parent.parent
HERE=Path(__file__).resolve().with_suffix('')
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import normalize_prose, normalize_tex, checked_math_content
spec=importlib.util.spec_from_file_location('ivp894_parser',HERE/'parse_math.py');pm=importlib.util.module_from_spec(spec);spec.loader.exec_module(pm)
X,Y=pm.X,pm.Y
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];ID=17592186100894
QS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
VERSION='rearrange-separate-ivp-2026-10-15-v1';SUPPORTED=('easy','moderate');SHIFTS=tuple(range(-4,5))
EXCLUDED={'q-104058':'At x=1,y=1 the supplied equation has left side 0 for every finite derivative, but right side 2; no classical solution satisfies the initial condition.'}
# Exact ODE RHS, initial abscissa, initial ordinate, and particular solution.
MODELS={
'q-20071':(s.exp(4*X-Y),0,5,s.log((s.exp(4*X)+4*s.exp(5)-1)/4)),
'q-79372':(X*Y/(X+1),1,s.E,2*s.exp(X)/(X+1)),
'q-128192':(X*Y**2,1,2,-2/(X**2-2)),
'q-104059':(Y**2*(1/X**2+1),-1,1,X/(1+X-X**2)),
'q-104064':(Y**2*(3*X**2-4*X**3),2,s.Rational(1,8),1/(X**4-X**3)),
'q-104065':(s.cot(X)+8*X,s.pi/2,s.pi**2,s.log(s.sin(X))+4*X**2),
'q-14267':(s.exp(X+Y),0,-s.log(2),-s.log(3-s.exp(X))),
'q-350957':((6*X**2-1)*s.exp(-Y),1,0,s.log(2*X**3-X)),
'q-355546':(5/X**2+8*X,1,6,-5/X+4*X**2+7),
'q-355547':(3/s.sqrt(X)+4*X,1,11,6*s.sqrt(X)+2*X**2+3),
'q-355559':(2*X*(Y**2+1)/Y,0,1,s.sqrt(2*s.exp(2*X**2)-1)),
'q-355564':(4*X*Y/(2*X-1),1,s.exp(2),(2*X-1)*s.exp(2*X)),
'q-355576':(s.exp(-2*X-Y),0,2,s.log((-s.exp(-2*X)+2*s.exp(2)+1)/2)),
'q-355577':(s.exp(-X-Y),0,-s.log(4),s.log(s.Rational(5,4)-s.exp(-X))),
'q-355582':(s.exp(-X-Y),0,0,s.log(2-s.exp(-X))),
'q-4016':(s.exp(X-2*Y),0,0,s.log(2*s.exp(X)-1)/2),
'q-79371':(3*s.exp(-X)+2*X,0,-3,X**2-3*s.exp(-X)),
'q-79373':((4*X**3-1)*s.exp(-Y),1,0,s.log(X**4-X+1)),
'q-79425':(2*X*(2+Y**3)/(3*Y**2),0,1,(3*s.exp(X**2)-2)**s.Rational(1,3)),
'q-355560':(Y**2*(4/X**2+1),2,-1,X/(4-X-X**2)),
'q-104056':(s.exp(-X)-4*X,0,7,-s.exp(-X)-2*X**2+8),
'q-104057':((3*X**2-2*X)*s.exp(-Y),1,1,s.log(X**3-X**2+s.E)),
'q-8306':(Y*(2*X+X**2),1,1,s.exp((X**3+3*X**2-4)/3))}
UNGRADABLE={
'q-350957':'Real grader leaves the wrong answer 0 unresolved for some permitted shifts; logarithmic blank domain comparison is incomplete.',
'q-355559':'Real grader cannot grade the canonical square-root-of-exponential blank (root of a symbolic quotient unsupported).',
'q-355577':'Real grader cannot reject 0 against this logarithmic blank because domain comparison is unresolved.',
'q-355582':'Same logarithmic expression/domain family as q-355577; conservatively excluded pending independent native support.'}
REPAIRS={
'q-79372':'The source says applying the natural logarithm before exponentiating; use applying the exponential function.',
'q-8306':'The source says applying the natural logarithm before exponentiating; use applying the exponential function.',
'q-128192':'Replace the unavailable cross-reference From part 6 with direct general-solution wording; retain subsequent stages.',
'q-355560':'Captured table lost its fraction layout. Restore y(x)=x/(field-1); canonical field is the denominator 4-x-x².',
'q-104056':'The initial-value substitution line has +2*0² instead of -2*0²; both are zero. Correct the sign without altering the source record.',
'q-79425':'On the declared positive branch K=exp(C1-C2)>0; the source unnecessary ± sign is removed.'}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),x))
def tex(x):return normalize_tex(s.latex(x,ln_notation=True))
def level(mid):return QS[mid][':question/difficulty'][':db/ident'].split('/')[-1]
def translate_math(text,h):
 if not h or text.strip() in ('x','x,','x.'):return text
 tokens={}
 def hold(value):
  key='ZZHOLD'+str(len(tokens))+'ZZ';tokens[key]=value;return key
 def ycall(m):
  arg=m[1]
  return hold('y(x)' if arg=='x' else 'y('+tex(pm.expression(arg)+h)+')')
 text=re.sub(r'y\(([^()]*)\)',ycall,text)
 # The differential's x denotes the independent variable, not a supplied value.
 text=re.sub(r'\\text\{d\}x',lambda m:hold(m[0]),text)
 text=re.sub(r'\\[a-zA-Z]+|x',lambda m:'('+tex(X-h)+')' if m[0]=='x' else m[0],text)
 for key,value in tokens.items():text=text.replace(key,value)
 return text

def translate_prose(text,h):
 return ''.join(part[:len(delim)]+translate_math(part[len(delim):-len(delim)],h)+delim if (delim:='$$' if part.startswith('$$') else '$' if part.startswith('$') else '') else part for part in re.split(r'(\$\$.*?\$\$|\$[^$]*\$)',text,flags=re.S))
def question_text(mid,h):
 q=QS[mid];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 if mid in ('q-79372','q-8306'):sol=sol.replace('Applying the natural logarithm to both sides','Applying the exponential function to both sides')
 if mid=='q-128192':
  prompt=re.sub(r'\s+',' ',prompt).replace(' $$ ','\n\n$$\n').replace(' $y(x)', '\n\n$y(x)')
  sol=sol.replace('From part 6, we found the general solution','Separating variables and integrating, we find the general solution')
 if mid=='q-104056':sol=sol.replace(r'+2\cdot {0}^{2}',r'-2\cdot {0}^{2}')
 if mid=='q-79425':sol=sol.replace(r'K=\pm {e}',r'K={e}')
 if mid=='q-355560':prompt=prompt.split('\n\n|')[0]+'\n\n$y(x)=\\frac{x}{\\boxed{\\text{denominator}}}$\n\nDenominator: {{field-1}}'
 return normalize_prose(translate_prose(prompt,h)),normalize_prose(translate_prose(sol,h))
def expected_fragment(mid,h):
 z=MODELS[mid][3].subs(X,X-h)
 if mid=='q-355560':return (4-X-X**2).subs(X,X-h)
 if mid=='q-355576':return ((-s.exp(-2*X)+2*s.exp(2)+1)/2).subs(X,X-h)
 return z

def math_fingerprint(mid,h):
 rhs,x0,y0,_=MODELS[mid]
 return digest([s.srepr(s.simplify(rhs.subs(X,X-h))),s.srepr(s.sympify(x0)+h),s.srepr(s.sympify(y0)),'first rearrange then separate'])
def task(q):
 # Question identity for inventory: equation + initial data + fragment contract;
 # answer order and UUIDs do not participate.
 text=normalize_prose(q[':question/problem'])
 return digest(re.sub(r'\s+',' ',text).strip())

@checked_math_content
def generate(difficulty='easy',seed=0,template=None,parameters=None,replay=False):
 if difficulty not in SUPPORTED:raise ValueError('unsupported difficulty: '+difficulty)
 rng=random.Random(seed);choices=[m for m in MODELS if level(m)==difficulty]
 mid=template or rng.choice([m for m in choices if m not in UNGRADABLE])
 if mid not in choices:raise ValueError('template/level mismatch or excluded source')
 h=0 if replay else parameters['h'] if parameters is not None else rng.choice([z for z in SHIFTS if z])
 if type(h) is not int or h not in SHIFTS or parameters is not None and set(parameters)!={'h'}:raise ValueError('declared finite h domain required')
 original=QS[mid];prompt,sol=question_text(mid,h)
 f=original[':question/answer-fields'][0];kind=f[':answer-field/type'][':db/ident'];key=f[':answer-field/key']
 values=[normalize_tex(translate_math(a[':answer/value'],h)) for a in f[':answer-field/choices']]
 profile='observed-'+mid if kind.endswith('/radio') else 'blank-'+mid
 # Seed/choice order do not enter content identity. Whole mathematical task does.
 content=math_fingerprint(mid,h);qid=uid('question:'+content);fid=uid('field:'+qid+key)
 answers=[{':answer/id':uid('answer:'+fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 cid=answers[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])][':answer/id']
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}]}
 return {'knowledge_point':{'db_id':ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':mid,'bank_profile':profile,'parameters':{'h':h},'source_ids':[mid],'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'eligible_for_learning':mid not in UNGRADABLE,'grading_exclusion':UNGRADABLE.get(mid),'math_fingerprint':content,'domain':'connected real interval through translated initial point where the original ODE and solution are defined; positive branch when specified','plot_rating':'none','recipe':'simultaneous exact substitution x -> x-h in every complete source option; IC abscissa x0 -> x0+h; no pooled distractors','python_version':sys.version.split()[0],'sympy_version':s.__version__}}

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--template');p.add_argument('--shift',type=int);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--replay',action='store_true');a=p.parse_args()
 if a.count<1:raise ValueError('positive count required')
 candidates=[(m,h) for m in MODELS if level(m)==a.difficulty and (a.template is None or a.template==m) and (a.replay or m not in UNGRADABLE) for h in ([0] if a.replay else [a.shift] if a.shift is not None else [v for v in SHIFTS if v])]
 random.Random(a.seed).shuffle(candidates)
 if a.count>len(candidates):raise ValueError('finite variant limit: '+str(len(candidates)))
 records=[generate(a.difficulty,a.seed+i,m,{'h':h},a.replay) for i,(m,h) in enumerate(candidates[:a.count])]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
