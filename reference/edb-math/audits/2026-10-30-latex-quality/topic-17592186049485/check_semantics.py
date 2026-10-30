"""Narrow numerical geometric check of every line/distance practice choice."""
import json,re,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;s=json.loads((HERE/'snapshot.json').read_text())
def num(x):
 x=x.replace('\\,','').replace(' ','')
 x=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',x)
 while re.search(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',x):x=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',x)
 x=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',x)
 x=re.sub(r'(\d)sqrt',r'\1*sqrt',x)
 assert re.fullmatch(r'[0-9+*/().sqrt-]+',x),x
 return eval(x,{'__builtins__':{},'sqrt':math.sqrt})
def vectors(t):
 return [[num(x) for x in (a.split('\\\\') if a else b.split(','))] for a,b in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}|⟨(.*?)⟩',t.replace('\\,',''))]
def points(t):return [[num(x) for x in a.split(',')] for a in re.findall(r'(?:[A-Z](?:_\{?[12]\}?)?|\{[A-Z]\}_\{[12]\})\(([^()]*)\)',t.replace('\\,',''))]
def sub(a,b):return [x-y for x,y in zip(a,b)]
def parallel(a,b):return sum((a[(i+1)%3]*b[(i+2)%3]-a[(i+2)%3]*b[(i+1)%3])**2 for i in range(3))<1e-15
def line_choice(v,p,d):return len(v)==2 and parallel(v[1],d) and parallel(sub(v[0],p),d)
results=[]
for ki,kp in enumerate(s['kps'][:3]):
 for q in kp.get(':knowledge-point/questions',[]):
  p=points(q[':question/problem'])[0];af=q[':question/answer-fields'][0]
  if ki==0:d=vectors(q[':question/problem'])[0]
  elif ki==1:d=sub(points(q[':question/problem'])[1],p)
  else:
   d=vectors(q[':question/problem'])[0];dist=num(re.search(r'(?:AP|PA|RP|PR|PQ|QP|YP|PY|XP|PX|SP|PS)=([^$]+)',q[':question/problem'])[1].rstrip('.'))
   factor=dist/math.sqrt(sum(x*x for x in d));expected=[[x+sign*factor*y for x,y in zip(p,d)] for sign in (1,-1)]
  valid=[]
  for a in af[':answer-field/choices']:
   text=a[':answer/value']
   if ki<2:ok=line_choice(vectors(text),p,d) and bool(re.search(r'\+t',text))
   else:
    got=points(text);ok=len(got)==2 and all(any(sum((x-y)**2 for x,y in zip(v,w))<1e-15 for w in expected) for v in got) and sum((got[0][i]-got[1][i])**2 for i in range(3))>1e-15
   if ok:valid.append(a[':db/id'])
  correct=af.get(':answer-field/correct',{}).get(':db/id')
  results.append({'question':q[':db/id'],'geometrically_valid_choices':valid,'correct':correct,'passed':valid==[correct]})
(HERE/'semantic-choice-checks.json').write_text(json.dumps({'method':'Independent numerical geometry (line membership/parallelism and distance endpoints), tolerance1e-15 squared; all choices checked in first3 KP pools. Segment arithmetic reviewed manually.','questions':len(results),'checks':results,'passed':all(r['passed'] for r in results)},indent=2)+'\n')
print(json.dumps({'questions':len(results),'failures':[r for r in results if not r['passed']]}))
