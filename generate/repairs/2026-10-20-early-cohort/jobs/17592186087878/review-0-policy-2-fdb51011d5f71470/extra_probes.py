from audit import *
rs=json.load(open('independent-records.json'));out=[]
for t in g.TEMPLATES:
 subset=[r for r in rs if r['generation']['template']==t]
 for rank,label in [(0,'lowest'),(-1,'highest')]:
  hits=[]
  for r in subset:
   f=next(f for f in r['question'][':question/answer-fields'] if f[':answer-field/key']=='field-1')
   ordered=sorted(f[':answer-field/choices'],key=lambda c:float(parse(c[':answer/value']).subs(x,1)))
   hits.append(ordered[rank][':answer/id']==f[':answer-field/correct'][1])
  out.append({'template':t,'strategy':label+' numeric integrating-factor rank at x=1','correct':sum(hits),'total':len(hits),'baseline':0.25,'interpretation':'Tests rank without consulting ODE; no deterministic rank fixed in authored candidate-set sampling.'})
save('rank-shortcuts.json',out)
print(out)
