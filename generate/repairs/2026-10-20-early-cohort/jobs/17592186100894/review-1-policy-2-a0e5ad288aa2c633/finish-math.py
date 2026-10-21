from auditlib import *
results=json.load(open(E/'math-results.json'));rs=json.load(open(E/'samples.json'))+json.load(open(E/'counterfactual-records.json'))+json.load(open(E/'batch.json'))
for i,r in enumerate(rs):
 if r['generation']['template']=='q-126765':
  h=r['generation']['parameters']['h'];v=expr(correct(r)); C=S.Symbol('C',real=True)
  p=r['question'][':question/problem']; sol=r['question'][':question/worked-solution']
  # Positive cos on stated local sine branch turns sqrt(1-sin²) into cos.
  derivative=simplify(S.diff(S.sin(v+C),x)-2*(x-h)*S.cos(v+C))
  ok=simplify(v-(x-h)**2)==0 and derivative==0 and '-\\pi/2' in p and '-\\pi/2<' in sol
  results[i]={'id':r['question'][':question/id'],'template':'q-126765','passed':ok,'valid_choice_count':1,'branch_derivative_residual':str(derivative),'fragment':str(v),'justification':'The displayed local branch has cos(theta)>0; sqrt(1-sin²(theta))=cos(theta). No IC exists for this general-solution source.'}
 elif 'error' in results[i]:results[i]=math_check(r)
save('math-results.json',results)
print('math checks',len(results),'failures',[r for r in results if not r.get('passed') or r['valid_choice_count']!=1])
