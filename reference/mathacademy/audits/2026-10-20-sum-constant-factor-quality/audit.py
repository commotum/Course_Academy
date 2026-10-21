import json,re,itertools
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=Path('reference/mathacademy/audits/2026-10-20-sum-constant-factor-quality');X=sp.Symbol('x',positive=True);C=sp.Symbol('C');V={'x':X,'C':C};T=standard_transformations+(implicit_multiplication_application,)
def group(text,pos):
 assert text[pos]=='{';depth=1;j=pos+1
 while depth:
  if text[j]=='{':depth+=1
  elif text[j]=='}':depth-=1
  j+=1
 return text[pos+1:j-1],j
def expr(text):
 while m:=re.search(r'\\(d?frac|sqrt)(?:\[([^]]+)\])?\{',text):
  first,pos=group(text,m.end()-1)
  if m[1]=='sqrt':replacement='(('+str(expr(first))+')**(1/'+(m[2]or'2')+'))'
  else:second,end=group(text,pos);pos=end;replacement='(('+str(expr(first))+')/('+str(expr(second))+'))'
  text=text[:m.start()]+replacement+text[pos:]
 text=text.replace(r'\left','').replace(r'\right','').replace('^','**').replace('{','(').replace('}',')')
 return parse_expr(text,local_dict=V,transformations=T)
kp=json.loads((H/'kp.json').read_text());qs=kp[':knowledge-point/questions'];rows=[]
for q in qs:
 if q.get(':question/math-academy-id'):continue
 p=q[':question/problem'];integrand=re.search(r'\\int (.*?)\\,\\mathrm\{d\}x',p)[1]
 fdef=re.search(r'Given \$f\(x\)=(.*?)\$',p)
 if fdef:integrand=integrand.replace('f(x)',r'\left('+fdef[1]+r'\right)')
 target=expr(integrand);f=q[':question/answer-fields'][0];cid=f[':answer-field/correct'][':answer/id'];parsed=[]
 for a in f[':answer-field/choices']:
  e=expr(a[':answer/value']);valid=sp.simplify(sp.diff(e,X)-target)==0;assert valid==(a[':answer/id']==cid),(q[':db/id'],a[':answer/value']);parsed.append((a,e))
 for (a,e),(b,d) in itertools.combinations(parsed,2):assert sp.simplify(sp.diff(e-d,X))!=0
 def degree(e):return max([term.as_powers_dict().get(X,0) for term in sp.expand(e).as_ordered_terms()])
 highest=max(degree(e) for a,e in parsed);winners=[a for a,e in parsed if degree(e)==highest]
 row={'question':q[':db/id'],'problem':p,'reduced_integrand':str(sp.expand(target)),'all_keys_verified_by_differentiation':True,'largest_positive_power':str(highest),'highest_power_option_unique':len(winners)==1,'highest_power_choice_correct':len(winners)==1 and winners[0][':answer/id']==cid}
 rows.append(row)
source=next(q for q in qs if q.get(':question/math-academy-id')=='q-49059');f=source[':question/answer-fields'][0];parsed=[(a,expr(a[':answer/value']))for a in f[':answer-field/choices']];winner=max(parsed,key=lambda item:degree(item[1]))[0];assert winner[':answer/id']!=f[':answer-field/correct'][':answer/id']
(H/'mathematical-audit.json').write_text(json.dumps({'passed':True,'questions':rows,'source_q49059_largest_power_shortcut_fails':True},indent=2)+'\n');print(json.dumps(rows,indent=2))
