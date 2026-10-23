import os,sys,json,re,copy,hashlib,importlib.util,pathlib,shutil
E=pathlib.Path(__file__).resolve().parent
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(E/'runtime-assets')
os.environ['MPLCONFIGDIR']=str(E/'mpl-cache');os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
spec=importlib.util.spec_from_file_location('reviewed',E/'runtime/17592186129197.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,u,v=s.symbols('x y u v',real=True)
def save(n,d): (E/n).write_text(json.dumps(d,indent=2,ensure_ascii=False,default=str)+'\n')
def parse(t):
 t=t.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace('⁡','').replace(r'\operatorname{ln}',r'\ln').strip().rstrip('.,')
 def group(text,i):
  assert text[i]=='{',(text,i)
  level=1;j=i+1
  while level:
   level+=(text[j]=='{')-(text[j]=='}');j+=1
  return text[i+1:j-1],j
 while r'\frac' in t:
  i=t.index(r'\frac');a,j=group(t,i+5);b,k=group(t,j);t=t[:i]+f'(({a})/({b}))'+t[k:]
 t=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',t)
 t=re.sub(r'\\ln\s*(\d+)',r'log(\1)',t).replace(r'\ln', 'log')
 t=t.replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(t,local_dict={'x':x,'y':y,'u':u,'v':v},transformations=standard_transformations+(implicit_multiplication_application,))
def correct(q):
 f=q[':question/answer-fields'][0];c=f.get(':answer-field/correct');cid=c.get(':answer/id') if isinstance(c,dict) else c[1] if c else None
 return next((a for a in f[':answer-field/choices'] if a[':answer/id']==cid),None)
def oracle(q):
 prompt=q[':question/problem'];maps=re.search(r'u\s*=\s*(.*?),\s*(?:\\,|\\quad|\\qquad)?\s*v\s*=\s*([^$\n]*|[^$]*)',prompt)
 # Extract the complete math chunk with both affine definitions, not generator metadata.
 chunks=re.findall(r'\$\$(.*?)\$\$|\$([^$]*)\$',prompt,re.S)
 m=next(a or b for a,b in chunks if re.search(r'u\s*=',a or b) and re.search(r'v\s*=',a or b))
 U,V=re.split(r',\s*(?:\\,|\\quad|\\qquad)?\s*v\s*=',m.split('=',1)[1]);U=parse(U);V=parse(V)
 inv=s.solve([u-U,v-V],(x,y));det=s.det(s.Matrix([U,V]).jacobian([x,y]));tail=prompt.split('bounded by',1)[1]
 equations=[]
 for t in re.findall(r'\$([^$]*)\$',tail):
  lhs,rhs=t.split('=');equations.append(s.expand((parse(lhs)-parse(rhs)).subs(inv)))
 verts=[]
 for i,a in enumerate(equations):
  for b in equations[:i]:
   for d in s.solve([a,b],(u,v),dict=True):
    if u in d and v in d and d[u].is_real and d[v].is_real: verts.append(d)
 us=sorted(set(d[u] for d in verts),key=float);lo,hi=us[0],us[-1];mid=(lo+hi)/2
 funcs=[]
 for eq in equations:
  funcs.extend(s.solve(eq,v))
 funcs=sorted(funcs,key=lambda z:float(z.subs(u,mid)));lower,upper=funcs[0],funcs[-1]
 area=s.simplify(s.integrate(upper-lower,(u,lo,hi))/abs(det))
 return {'U':str(U),'V':str(V),'det':str(det),'lo':str(lo),'hi':str(hi),'lower':str(lower),'upper':str(upper),'area':area}
def probe(r):
 q=r['question'];bank=q[':question/answer-fields'][0][':answer-field/choices'];vals=[parse(a[':answer/value']) for a in bank]
 candidates=[a for a,z in zip(bank,vals) if z>0 and any(s.simplify(z+w)==0 for w in vals)]
 key=correct(q)
 return {'id':q[':question/id'],'template':r.get('generation',{}).get('template'),'seed':r.get('generation',{}).get('seed'),'parameters':r.get('generation',{}).get('parameters'),'candidate_count':len(candidates),'selected':candidates[0][':answer/id'] if len(candidates)==1 else None,'key':key[':answer/id'] if key else None,'success':len(candidates)==1 and key is not None and candidates[0][':answer/id']==key[':answer/id'],'bank':[a[':answer/value'] for a in bank]}
