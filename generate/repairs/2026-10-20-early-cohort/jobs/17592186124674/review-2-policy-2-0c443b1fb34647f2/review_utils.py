import sys,os,pathlib,json,re,hashlib,importlib.util,collections,platform,subprocess,shutil
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy');P=R/'.venv/bin/python'
def load(p):return json.loads(pathlib.Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def module(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=module(W/'17592186124674.py','current')
def q(r):return r['question']
def f(r):return q(r)[':question/answer-fields'][0]
def opts(r):return f(r)[':answer-field/choices']
def key(r):return f(r).get(':answer-field/correct',[None,None])[1]
def val(r):return next(c[':answer/value'] for c in opts(r) if c[':answer/id']==key(r))
def clean(x):return re.sub(r'\s+','',x.replace('\\\\','\\'))
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
trans=standard_transformations+(implicit_multiplication_application,)
def rhs(v):
 x=v.replace('\\\\','\\').split('=',1)[1];x=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',x)
 return sp.expand(parse_expr(x.replace('{','(').replace('}',')').replace('^','**'),local_dict={c:sp.Symbol(c) for c in 'kNMTBCPVRSFH'},transformations=trans))
def facts(r):
 prompt=q(r)[':question/problem'];s=re.search(r'\$([A-Z])\(t\)\$',prompt)[1];a=int(re.search(r'maximum.+?is \$(\d+)\$',prompt)[1]);X=sp.Symbol(s);k=sp.Symbol('k')
 eq=[rhs(c[':answer/value']) for c in opts(r)];matches=[c[':answer/id'] for c,e in zip(opts(r),eq) if sp.expand(e-k*(a-X))==0]
 linear=[i for i,x in enumerate(eq) if sp.degree(x,X)==1 and x.coeff(X)==-k and x.subs(X,0)/k>0]
 idx=next(i for i,c in enumerate(opts(r)) if c[':answer/id']==key(r));caps={i:int(eq[i].subs(X,0)/k) for i in linear};lens=[len(clean(c[':answer/value'])) for c in opts(r)]
 assert matches==[key(r)] and len(set(eq))==5,(q(r)[':question/id'],matches)
 assert str(a)+'-'+s in clean(q(r)[':question/worked-solution'])
 return {'id':q(r)[':question/id'],'capacity':a,'symbol':s,'template':r['generation']['template'],'kind':'mixed' if len(linear)==2 else 'capacities','position':idx,'rank':sorted(caps.values()).index(a),'linear_count':len(linear),'lengths':lens,'shortest_first':idx==min(range(5),key=lens.__getitem__),'unique_shortest':lens.count(min(lens))==1 and lens[idx]==min(lens),'longest_first':idx==max(range(5),key=lens.__getitem__),'minimum_capacity':caps[idx]==min(caps.values()),'maximum_capacity':caps[idx]==max(caps.values()),'middle_linear_capacity':idx==sorted(linear,key=lambda i:caps[i])[len(linear)//2]}
