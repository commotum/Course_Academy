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
 sol=q[':question/worked-solution'];env='gathered' if r'\begin{gathered}' in sol else 'aligned';rows=sol.split('\\begin{'+env+'}')[1].split('\\end{'+env+'}')[0].split(r' \\ ');rowresults=[zero(norm(a.equation(row))-n) for row in rows]
 return {'question_id':q[':question/id'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'choices':checks,'rows':rowresults,'passed':all((c['standard'] and c['equivalent'])==c['keyed'] for c in checks) and all(rowresults)}
