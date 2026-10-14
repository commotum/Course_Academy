import sys,json,importlib.util,re
from pathlib import Path
D=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validation',D/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g;s=g.s
k=json.loads((D/'reference/initial/kp.json').read_text())
for q in k[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];sol=q[':question/worked-solution'];prob=q[':question/problem']
 part=sol.split('suggests that we use the change of variables')[1].split('$$')[1].strip().rstrip('.')
 U,V=[v.math(t.split('=',1)[1]) for t in part.split(r'\,')]
 M=s.Matrix([[s.diff(U,g.x),s.diff(U,g.y)],[s.diff(V,g.x),s.diff(V,g.y)]]);iv=s.solve([U-g.u,V-g.v],[g.x,g.y]);pts=re.findall(r'\$\((.*?),(.*?)\)[,.]?\$',prob)
 cs=[(s.simplify(U.subs({g.x:v.math(A),g.y:v.math(B)})),s.simplify(V.subs({g.x:v.math(A),g.y:v.math(B)}))) for A,B in pts]
 F=v.math(prob.split('$$')[1].replace('{∬}_{D}','').split(r'\,dxdy')[0]);ft=s.simplify(F.subs(iv,simultaneous=True));a0=min(p[0] for p in cs);a1=max(p[0] for p in cs);b0=min(p[1] for p in cs);b1=max(p[1] for p in cs);ans=s.simplify(s.integrate(ft/abs(M.det()),(g.u,a0,a1),(g.v,b0,b1)))
 print(sid,'U,V',U,V,'bounds',a0,a1,b0,b1,'F',ft,'answer',ans,'correct',[f.get(':answer-field/correct',{}).get(':answer/value') for f in q[':question/answer-fields']])
 for f in q[':question/answer-fields']:
  vals=[v.math(a[':answer/value']) for a in f[':answer-field/choices']];assert sum(g.eq(z,ans) for z in vals)==1
  if ':answer-field/correct' in f:v.eq(v.math(f[':answer-field/correct'][':answer/value']),ans)
