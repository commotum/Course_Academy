import json,re,sys,signal
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from vector_engine import *
D=json.loads((H/'snapshot.json').read_text());ids={q for t,k,q in D['links']if t==next(t['entity']for t in D['topics']if t['ma_id']==317)};checks=[];unresolved=[];x=SYMS['x']
def atom(s):
 s=s.lstrip()
 if s.startswith('{'):
  n=1;i=1
  while n:n+=(s[i]=='{')-(s[i]=='}');i+=1
  return s[1:i-1],s[i:]
 m=re.match(r'\\[A-Za-z]+|[\dA-Za-z+-]',s);assert m,s;return m[0],s[m.end():]
def integral(s):
 s=normalize_source_tex(s).replace(r'{\int}',r'\int');s=s[s.index(r'\int')+4:].strip();bounds={}
 while s and s[0]in'_^':
  role=s[0];v,s=atom(s[1:]);bounds[role]=scalar(v);s=s.lstrip()
 s=re.sub(r'\\(?:textrm|text|mathrm)\s*\{\s*d\s*\}|\\(?:textrm|text|mathrm)\s+d', 'd',s);m=re.search(r'd\s*x\s*[.=,]?\s*$',s);assert m,s;f=scalar(s[:m.start()]);return f,bounds
signal.signal(signal.SIGALRM,lambda*a:(_ for _ in()).throw(TimeoutError('bounded IBP')))
for q in D['questions']:
 if q[':db/id']not in ids:continue
 try:
  signal.alarm(5);prompt=q[':question/problem'];f,b=integral(next(t for t in maths(prompt)if r'\int'in t));definite=bool(b);expected=sp.integrate(f,(x,b['_'],b['^']))if definite else None;fields=q.get(':question/answer-fields',[]);rows=[]
  if fields:
   assert len(fields)==1;field=fields[0];cid=field[':answer-field/correct'][':db/id']
   for a in field[':answer-field/choices']:
    try:
     value=a[':answer/value'];v=scalar(value);passed=equal(v,expected)if definite else equal(sp.diff(v,x),f);rows.append({'answer':a[':db/id'],'matches_integral':bool(passed),'value':value,'includes_constant':bool(v.has(SYMS['C']))})
    except Exception as ex:rows.append({'answer':a[':db/id'],'matches_integral':False,'interpretation':str(ex)})
   good=[r['answer']for r in rows if r['matches_integral']];ok=cid in good and(field[':answer-field/type'][':db/id']==17592186045492 or good==[cid]);proof={'canonical':cid,'matching_answers':good,'choices':rows}
   if not definite:ok=ok and any(r['answer']==cid and r['includes_constant']for r in rows)
  else:
   sol=q[':question/worked-solution'];last=maths(sol)[-1];last=re.sub(r'\\(?:begin|end)\{aligned\}','',last).replace('&','');value=last.split('=')[-1].strip().rstrip('.');v=scalar(value);ok=equal(v,expected)if definite else equal(sp.diff(v,x),f)and v.has(SYMS['C']);proof={'worked_final':value,'derivative':str(sp.diff(v,x))if not definite else None}
  checks.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'integrand':str(f),'bounds':{k:str(v)for k,v in b.items()},'expected_definite':str(expected),'passed':bool(ok),**proof})
 except Exception as ex:unresolved.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'reason':str(ex)})
 finally:signal.alarm(0)
(H/'integration-by-parts-math-validation.json').write_text(json.dumps({'checks':checks,'failures':[r for r in checks if not r['passed']],'unresolved':unresolved},indent=2));print('IBP',len(checks),'failures',sum(not r['passed']for r in checks),'unresolved',len(unresolved));print(unresolved)
