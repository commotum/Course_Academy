import audit as a
S=a.S

def trig_contract(z):
 # Exact identities, not assumptions about numerical samples.
 trig=z.atoms(S.sin,S.cos,S.tan,S.cot,S.sec,S.csc);subs={}
 for v in trig:
  arg=v.args[0]
  if v.func==S.sin:
   for c in trig:
    if c.func==S.cos and S.expand(arg-2*c.args[0])==0:subs[v]=2*S.sin(c.args[0])*c
  elif v.func==S.tan:subs[v]=S.sin(arg)/S.cos(arg)
  elif v.func==S.cot:subs[v]=S.cos(arg)/S.sin(arg)
  elif v.func==S.sec:subs[v]=1/S.cos(arg)
  elif v.func==S.csc:subs[v]=1/S.sin(arg)
 return z.xreplace(subs)

def norm(pair):
 r=a.residual(pair);return trig_contract(r/r.coeff(a.D))
def zero(z):
 z=trig_contract(z)
 return S.cancel(z)==0

def check(r):
 q=r['question'];p=a.equation(q[':question/problem'].split('$$')[1]);n=norm(p);f=q[':question/answer-fields'][0];key=f[':answer-field/correct'][1];checks=[]
 for c in f[':answer-field/choices']:
  e=a.equation(c[':answer/value']);isstd=a.is_standard(e);diff=norm(e)-n;eq=zero(diff);checks.append({'choice_id':c[':answer/id'],'standard':bool(isstd),'equivalent':bool(eq),'keyed':c[':answer/id']==key})
 rows=q[':question/worked-solution'].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r' \\ ');rowresults=[zero(norm(a.equation(row))-n) for row in rows]
 return {'question_id':q[':question/id'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'choices':checks,'rows':rowresults,'passed':all((c['standard'] and c['equivalent'])==c['keyed'] for c in checks) and all(rowresults)}
if __name__=='__main__':
 rs=a.json.loads((a.E/'independent-records.json').read_text())+a.json.loads((a.E/'runner-batch.json').read_text())+a.json.loads((a.E/'counterfactual-records.json').read_text());out=[]
 for r in rs:
  try:out.append(check(r))
  except Exception as e:out.append({'id':r['question'][':question/id'],'error':repr(e),'passed':False})
 a.save('independent-math-results.json',{'command':str(a.PY)+' '+str(a.E/'fast_math.py'),'method':'Parse displayed TeX independently; normalize residual by derivative coefficient; exact rational/exponential arithmetic with explicit sin(2t)=2sin(t)cos(t) and quotient trig identities. Check all options and all worked rows.','results':out})
 print('passed',sum(v['passed'] for v in out),'/',len(out));print('failures',[v for v in out if not v['passed']][:5])
