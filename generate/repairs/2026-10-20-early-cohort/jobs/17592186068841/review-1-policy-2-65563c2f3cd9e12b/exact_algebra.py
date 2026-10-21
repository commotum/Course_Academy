from independent_math import *
results=[]
for n in ['easy-grid.json','normal-cases.json','batch.json']:
 for i,r in enumerate(json.loads((ROOT/n).read_text())):
  q=r['question'];expr=value(correct(r));f=q[':question/answer-fields'][0]
  if f[':answer-field/type'].endswith('/blank'):
   m=re.search(r'\$y=-(\d+)\(',q[':question/problem']);expr=-int(m[1])/(expr+K) if m else s.sqrt(expr+K)
  eq=rhs(q[':question/problem']);res=s.diff(expr,X)-eq.subs(Y,expr)
  xp,kp,cp=s.symbols('xp kp cp',positive=True)
  simp=s.simplify(s.powdenest(res.subs({X:xp,K:kp,C:cp}),force=False))
  results.append({'file':n,'index':i,'question_id':q[':question/id'],'zero_residual_exact_on_positive_branch':simp==0,'remaining_residual':str(simp)})
save('exact-algebra.json',{'method':'Independent printed expressions; exact SymPy differentiation and simplification on a positive nonempty branch. q-158010 additionally retains |x|<1. Normal prompts give other local branch restrictions; this is not a full real-domain census.','results':results})
print('exact',len(results),'remaining',[(r['file'],r['index'],r['remaining_residual']) for r in results if not r['zero_residual_exact_on_positive_branch']])
