"""Validate each committed instance from rendered data and the native grader."""
import importlib.util,json,re,subprocess,hashlib,sys,math
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
D=Path(__file__).parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('equal_flow',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
t=sp.Symbol('t',real=True)
def parse_num(s):
 s=s.rstrip('.')
 m=re.fullmatch(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',s)
 return sp.Rational(m[1])/sp.Rational(m[2]) if m else sp.Rational(s)
def fn(s):
 s=s.replace(' ','').replace('{e}','e');s=s.split('=')[-1]
 m=re.fullmatch(r'(-?\d+(?:\.\d+)?)([+-])(\d+(?:\.\d+)?)?e\^\{(-?)([\dt.]+)/([\d.]+)\}',s)
 assert m,s
 E=sp.Rational(m[1]);A=sp.Rational(m[3] or 1)*(1 if m[2]=='+' else -1);ind=t if m[5]=='t' else sp.Rational(m[5]);k=sp.Rational(1)/sp.Rational(m[6])*(-1 if m[4] else 1)
 return E+A*sp.exp(k*ind)
def prompt_math(q):
 blocks=re.findall(r'\$([^$]+)\$',q[':question/problem'])
 start_number=r'(\\frac\{[\d.]+\}\{[\d.]+\}|[\d.]+)'
 nums=[parse_num(re.match(start_number,x)[1]) for x in blocks[:5]]
 tail=[parse_num(re.match(start_number,blocks[-1])[1])] if 'Find, rounded' in q[':question/problem'] else []
 V,q0,c,r,rout=nums
 assert r==rout and V>0 and r>0
 hard=r'\text{g/L}' in q[':question/problem'];c=c/1000 if hard else c
 return V,q0,c,r,(tail[0] if tail else None),hard

LEVELS=g.LEVELS

def check(rec):
 level=rec['question'][':question/difficulty'].split('/')[-1]
 seed=rec['generation']['seed']
 assert level in LEVELS and rec['knowledge_point']['db_id']==g.KP_ID
 assert rec['knowledge_point']['id']==g.KP_UUID
 assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
 assert rec['generation']['profile']=='method_bank'
 q=rec['question'];p=rec['generation']['parameters'];V,q0,c,r,time,hard=prompt_math(q);k=r/V;E=V*c;A=q0-E;expected=E+A*sp.exp(-k*t)
 assert hard==(level=='hard');assert level!='easy' or time is None
 f=q[':question/answer-fields'][0];answers=f[':answer-field/choices'];assert len(answers)==5
 assert set(rec['knowledge_point'])=={'db_id','id','title'};assert len({a[':answer/id'] for a in answers})==5
 correct=next(a for a in answers if a[':answer/id']==f[':answer-field/correct'][1]); models=[expected,E/2+(q0-E/2)*sp.exp(-2*k*t),2*E+(q0-2*E)*sp.exp(-k*t/2),r*c+(q0-r*c)*sp.exp(-k*t),E-A*sp.exp(-k*t)]
 observed=[fn(a[':answer/value']) if time is None else sp.Rational(re.match(r'[\d.]+',a[':answer/value'])[0]) for a in answers]
 computed=models if time is None else [sp.Rational(g.rounded(x.subs(t,time))) for x in models]
 assert all(any(sp.expand(a-b)==0 for b in computed) for a in observed)
 assert len(set(observed))==5
 assert sp.expand(fn(correct[':answer/value'])-expected)==0 if time is None else sp.Rational(re.match(r'[\d.]+',correct[':answer/value'])[0])==computed[0]
 assert sp.expand(sp.diff(expected,t)-(r*c-r*expected/V))==0 and expected.subs(t,0)==q0
 # Read actual displayed rates, equation and primitive/initial-value stages.
 sol=q[':question/worked-solution'];num=r'[\d.]+'
 rates=re.findall(r'\$('+num+r')\\,\\text\{L/min\}',sol);assert len(rates)==2 and all(parse_num(x)==r for x in rates),(level,seed,rates,r)
 conc=re.findall(r'\$('+num+r')\\,\\text\{kg/L\}',sol);assert conc and all(parse_num(x)==c for x in conc)
 assert r'\frac{Q}{'+g.num(V)+'}' in sol
 ode=re.search(r'\\frac\{dQ\}\{dt\}\+\\frac\{1\}\{('+num+r')\}Q=([^\n]+)\.',sol);assert ode and parse_num(ode[1])==V/r and parse_num(ode[2])==r*c,(level,seed,ode.group() if ode else sol)
 eqs=re.findall(r'\\alpha =('+num+r')\.(?=\n)',sol);assert eqs and all(parse_num(x)==E for x in eqs),(level,seed,eqs,E)
 part=re.search(r'\{Q\}_\{p\}\(t\)=('+num+r')\.\$',sol);assert part and parse_num(part[1])==E
 ic=re.search(r'A & =(-?'+num+r')\\end',sol);assert ic and parse_num(ic[1])==A,(level,seed,ic.group() if ic else sol,A)
 general=re.search(r'Q\(t\)=\{Q\}_\{c\}\(t\)\+\{Q\}_\{p\}\(t\)=A\{e\}\^\{-t/('+num+r')\}\+('+num+r')\.',sol);assert general and parse_num(general[1])==V/r and parse_num(general[2])==E
 final=re.findall(r'^Q\(t\)=([0-9][^\n]+)',sol,re.M);assert len(final)==1 and sp.expand(fn('Q(t)='+final[0].rstrip('.'))-expected)==0
 if time is not None:
  ev=re.search(r'^Q\(('+num+r')\)=([^≈\n]+)≈('+num+r')',sol,re.M);assert ev and parse_num(ev[1])==time and sp.expand(fn('Q(t)='+ev[2])-expected.subs(t,time))==0 and sp.Rational(ev[3])==computed[0]
  assert '$'+g.num(time)+'$ minutes after pumping begins' in sol
 assert 'supplements' not in sol if 'supplement' not in q[':question/problem'] else True
 assert sol.count('**Step ')==4 and sol.count('\\begin{aligned}')==4
 assert '**Step 4**: Integrate the equation.' in sol and 'first-order linear equation with constant coefficients' in sol
 assert 'additives enter' not in sol and 'additives exit' not in sol
 # Balanced delimiters/groups and absence of stale masks/unsupported doubled commands.
 for content in [q[':question/problem'],sol]+[a[':answer/value'] for a in answers]:
  assert content.count('$')%2==0 and content.count('{')==content.count('}') and '⟦' not in content
  assert r'\\text' not in content and not re.search(r'\+\-|\-\-',content)
 json.loads(json.dumps(rec))
 assert rec['question'][':question/id']==g.generate(level,seed+500,parameters=p)['question'][':question/id']

 replay=g.generate(level,seed,parameters=p)
 assert replay==rec
 return True

def native(rec,label=None):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label or rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native owned choice grading'} for a in f[':answer-field/choices']]}

def fingerprint(q):
 V,q0,c,r,time,hard=prompt_math(q)
 return (str(V*c),str(r/V),str(q0),str(time), 'hard' if hard else 'amount' if time is not None else 'expression')

def source_check(q):
 V,q0,c,r,time,hard=prompt_math(q)
 expected=V*c+(q0-V*c)*sp.exp(-r*t/V)
 f=q[':question/answer-fields'][0]
 assert f[':answer-field/type'][':db/ident']==':answer-field.type/radio'
 assert len(f[':answer-field/choices'])==5
 values=[fn(a[':answer/value']) if time is None else sp.Rational(re.match(r'[\d.]+',a[':answer/value'])[0]) for a in f[':answer-field/choices']]
 assert len(set(values))==5
 target=expected if time is None else sp.Rational(g.rounded(expected.subs(t,time)))
 matches=[a for a,val in zip(f[':answer-field/choices'],values) if sp.expand(val-target)==0]
 assert len(matches)==1
 correct=f.get(':answer-field/correct')
 if correct: assert correct[':answer/id']==matches[0][':answer/id']
 if q.get(':question/worked-solution'):
  finals=re.findall(r'^Q\(t\)\s*=([0-9][^\n]+)',q[':question/worked-solution'],re.M)
  assert len(finals)==1 and sp.expand(fn(finals[0].rstrip('.'))-expected)==0
 return {'source_id':q[':db/id'],'source_ma_id':q.get(':question/math-academy-id'),'parameters':{'V':str(V),'r':str(r),'c':str(c),'q0':str(q0),'T':str(time)},'correct_value':matches[0][':answer/value'],'complete_bank':[a[':answer/value'] for a in f[':answer-field/choices']],'gradable':bool(correct and q.get(':question/worked-solution') and q.get(':question/difficulty')),'family':'amount' if time is not None else 'expression','plot_rating':'none'}
