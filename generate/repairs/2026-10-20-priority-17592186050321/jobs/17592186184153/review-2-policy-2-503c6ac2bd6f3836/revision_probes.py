import sys
sys.dont_write_bytecode=True
import json, pathlib, random, itertools, collections
from fractions import Fraction as F
from audit_math import tex, extract, field, answer, V, verify, equal
R=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'workspace'))
import generator as G
def save(n,x): (R/n).write_text(json.dumps(x,indent=2)+'\n')
def load(n): return json.loads((R/n).read_text())
raw=load('samples.json'); delivered=load('delivery/accepted.json')
probes=[]
for stage,rs in [('raw',raw),('delivered',delivered),('runner',load('batch-delivery/accepted.json'))]:
 for t in 'PR':
  ts=[(j,r) for j,r in enumerate(rs) if r['generation']['template']==t]
  groups=[('all',ts)]
  for key in ['n','s','constant_first']:
   for val in sorted({str(r['generation']['parameters'][key]) for _,r in ts}):
    groups.append((key+'='+val,[(j,r) for j,r in ts if str(r['generation']['parameters'][key])==val]))
  for label,items in groups:
   for strategy in ['first','last','smallest_coefficient_after_constant','largest_coefficient_after_constant','old_unit_numerator_cue']:
    trials=[]
    for j,r in items:
     integ,v=extract(r);x=V[v];k=integ.expand().coeff(x,0);cs=field(r)[':answer-field/choices'];eligible=[]
     for idx,a in enumerate(cs):
      val=tex(a[':answer/value']).expand().subs(V['C'],0);linear=val.coeff(x,1)
      c=abs((val-linear*x).as_coeff_Mul()[0])
      if linear==k: eligible.append((idx,c))
     if strategy=='first':chosen=0
     elif strategy=='last':chosen=4
     elif strategy=='old_unit_numerator_cue':
      candidates=[idx for idx,c in eligible if c.p==1 and c.q<10];chosen=candidates[0] if len(candidates)==1 else -1
     else:chosen=sorted(eligible,key=lambda p:p[1],reverse=strategy.startswith('largest'))[0][0]
     trials.append({'sample_index':j,'id':r['question'][':question/id'],'chosen':chosen,'correct':chosen>=0 and cs[chosen][':answer/id']==answer(r)[':answer/id'],'eligible_count':len(eligible)})
    if trials:probes.append({'stage':stage,'template':t,'subgroup':label,'strategy':strategy,'correct':sum(x['correct'] for x in trials),'total':len(trials),'baseline':0.2,'trials':trials})
save('conditional-shortcut-results.json',probes)
# Exhaust every revised polynomial divisor pair and omitted cell. Derive domain
# independently, then check displayed coefficients, not generator bank metadata.
domain=[];representatives=[]
for n in range(2,7):
 for d1,d2 in itertools.combinations([d for d in range(2,10) if d!=n+1],2):
  for row,col in itertools.product([0,1],[1,2]):
   i=G.instance('P',n,-1,3,'x',True,offset=-2,factors=[str(F(n+1,d1)),str(F(n+1,d2))],omitted_row=row,omitted_col=col)
   r=G.build(i,random.Random(20411));x=V['x'];vals=[tex(a[':answer/value']).expand().subs(V['C'],0) for a in field(r)[':answer-field/choices']]
   coeff=[abs((a-a.coeff(x,1)*x).as_coeff_Mul()[0]) for a in vals if a.coeff(x,1)==3]
   assert len(coeff)>=2 and all(c.p==1 and 2<=c.q<=9 for c in coeff)
   assert len([a for a in vals if equal(a.diff(x),3-x**n)])==1
   domain.append({'parameters':i,'correct_coeff':str(F(-1,n+1)),'constant_matched_coeffs':list(map(str,coeff)),'old_cue_candidates':len(coeff),'passed':True})
   if d1==2 and d2==8 and row==0 and col==1:
    verify(r);representatives.append(r)
save('revised-domain-results.json',{'cases':domain,'count':len(domain),'method':'Exhaust independently specified incorrect divisor pairs 2..9 except n+1 and four omitted cells; parse served choices and differentiate exactly. Sign symmetry also covered by sampled boundaries.'})
save('revised-domain-records.json',representatives)
# Counterfactual distractor assignments preserve the response while moving its
# coefficient rank. They rule out a specification-level fixed rank.
controls=[];results=[]
for n in range(2,7):
 for label,ds in [('low',(2,3)),('high',(8,9))]:
  if n+1 in ds:continue
  i=G.instance('P',n,1,-4,'y',False,offset=2,factors=[str(F(n+1,d)) for d in ds],omitted_row=1,omitted_col=2)
  r=G.build(i,random.Random(19883));verify(r);controls.append(r)
  results.append({'n':n,'assignment':label,'index':len(controls)-1,'divisors':ds,'answer':answer(r)[':answer/value']})
for n in range(3,7):
 a,b=[r for r in controls if r['generation']['parameters']['n']==n];assert equal(tex(answer(a)[':answer/value']),tex(answer(b)[':answer/value']))
save('assignment-control-records.json',controls);save('assignment-control-results.json',results)
cases=load('grader-input-complete.json')
for j,r in enumerate(controls+representatives):
 cases.append({'label':'assignment or domain '+str(j),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==answer(r)[':answer/id'] else 'rejected','purpose':'independent derivative verification'} for a in field(r)[':answer-field/choices']]})
save('grader-input-final.json',cases)
renders=load('counterfactual-records.json')+load('reciprocal-counterfactual-records.json')+controls[:3]
for t,n in [('P',4),('P',6),('R',7)]:renders.append(next(r for r in raw if r['generation']['template']==t and r['generation']['parameters']['n']==n))
renders+=load('runner-batch.json')
save('render-records.json',renders)
print(json.dumps({'domain_cases':len(domain),'native_records':len(cases),'render_records':len(renders),'perfect_nontrivial_probes':[ {k:v for k,v in p.items() if k!='trials'} for p in probes if p['total']>=15 and p['correct']==p['total']]}))
