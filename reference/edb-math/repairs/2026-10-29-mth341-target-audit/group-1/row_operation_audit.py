import importlib.util,json,re
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('gm',H/'math_verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);checks=[];bad=[];skips=[]
fields=[(q[':db/id'],'question/worked-solution',q.get(':question/worked-solution',''),q.get(':question/math-academy-id'))for q in m.D['questions']]+[(c[':db/id'],'tutorial/content',c[':tutorial/content'],'tutorial:'+str(c[':tutorial/math-academy-id']))for c in m.D['contents']if':tutorial/content'in c]
for eid,attr,text,sid in fields:
 text=m.pm.get((eid,attr),text)
 for env in m.ENV.finditer(text):
  if env.groups()!=('begin','aligned'):continue
  span=m.environment(text,env.start());block=text[env.start():span[2]]
  if'∼'not in block and r'\sim'not in block:continue
  mats=m.mats(block)
  for x,y in zip(mats,mats[1:]):
   if x[2].shape!=y[2].shape:continue
   between=block[x[1]:y[0]];bs=between.replace('&','').replace('∼','');bs=re.sub(r'\\(?:begin|end)\{aligned\}','',bs);bs=re.sub(r'\\color\{[^{}]*\}','',bs);bs=re.sub(r'\{?R\}?_\{?(\d+)\}?',r'R\1',bs);bs=bs.replace('′',"'")
   operations=[]
   for line in re.split(r'\\\\',bs):
    swap=re.search(r'R(\d+)\s*(?:↔|\\leftrightarrow)\s*R(\d+)',line)
    assign=re.search(r'R(\d+)\s*(?::=|:\s*=|\\leftarrow)\s*([\s\S]*?)\s*$',line)
    if swap:operations.append(('swap',int(swap[1])-1,int(swap[2])-1))
    elif assign:
     expr=assign[2].strip().rstrip('}. ');expr=re.sub(r"R(\d+)\^\{?'\}?",r'R\1',expr);operations.append(('replace',int(assign[1])-1,expr))
   if not operations:skips.append({'entity':eid,'identity':sid,'between':between});continue
   A=x[2].copy()
   try:
    for kind,i,other in operations:
     if kind=='swap':A.row_swap(i,other)
     else:
      v=m.scalar(other);symbols=[S.Symbol('R'+str(j+1))for j in range(A.rows)];rhs=S.zeros(1,A.cols)
      for j,sym in enumerate(symbols):rhs+=v.coeff(sym)*A[j,:]
      assert S.simplify(v-sum(v.coeff(sym)*sym for sym in symbols))==0,(other,v)
      A[i,:]=rhs
   except Exception as ex:skips.append({'entity':eid,'identity':sid,'between':between,'error':str(ex)});continue
   entry={'entity':eid,'attribute':attr,'identity':sid,'operations':operations,'before':str(x[2]),'expected_from_operations':str(A),'shown':str(y[2]),'passed':A==y[2],'between':between};checks.append(entry)
   if not entry['passed']:bad.append(entry)
(H/'row-operation-verification.json').write_text(json.dumps({'checks':checks,'flags':bad,'parser_limitations':skips},indent=2)+'\n');print('Annotation transitions',len(checks),'flags',len(bad),'parser limitations',len(skips));print(json.dumps(bad,indent=2));print('SKIPS',json.dumps(skips,indent=2))
