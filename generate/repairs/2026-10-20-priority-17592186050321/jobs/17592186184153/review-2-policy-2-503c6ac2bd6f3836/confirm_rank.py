import sys
sys.dont_write_bytecode=True
import json,pathlib,random,collections
from fractions import Fraction as F
from audit_math import tex,extract,field,answer,V,verify
R=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'workspace'))
import generator as G
def save(n,x):(R/n).write_text(json.dumps(x,indent=2)+'\n')
def load(n):return json.loads((R/n).read_text())
if '--analyze' not in sys.argv:
 allrs=G.generate(count=480,seed=94172863)
 # Keep the complete mixed generation for reproduction; the only selection is
 # the predeclared recognizable n=2 polynomial subgroup.
 save('rank-holdout-all.json',allrs)
 rs=[r for r in allrs if r['generation']['template']=='P' and r['generation']['parameters']['n']==2]
 for r in rs:verify(r)
 save('rank-holdout-records.json',rs)
 print('fresh subgroup records',len(rs))
else:
 reports=[];cases=load('grader-input-final.json');examples=[]
 for name in ['rank-holdout-records.json','rank-delivery/accepted.json']:
  rs=load(name);trials=[]
  for j,r in enumerate(rs):
   integ,v=extract(r);x=V[v];constant=integ.expand().coeff(x,0);opts=[]
   for idx,a in enumerate(field(r)[':answer-field/choices']):
    e=tex(a[':answer/value']).expand().subs(V['C'],0);lin=e.coeff(x,1)
    if lin==constant:opts.append((idx,abs((e-lin*x).as_coeff_Mul()[0])))
   chosen=max(opts,key=lambda z:z[1])[0];cs=field(r)[':answer-field/choices'];win=cs[chosen][':answer/id']==answer(r)[':answer/id']
   trials.append({'index':j,'id':r['question'][':question/id'],'chosen':chosen,'constant_matched_coefficients':list(map(lambda z:str(z[1]),opts)),'correct':win,'chance_after_constant':1/len(opts)})
   if name.startswith('rank-delivery'):
    cases.append({'label':'fresh n2 rank strategy '+str(j),'record':r,'checks':[{'submitted_answer_id':cs[chosen][':answer/id'],'expected':'accepted' if win else 'rejected','purpose':'constant matching plus maximum power-coefficient magnitude; no power-rule calculation'}]})
    if len(examples)<2 and (not examples or win!=examples[0][0]):examples.append((win,r))
  reports.append({'file':name,'correct':sum(t['correct'] for t in trials),'total':len(trials),'baseline_after_constant':sum(t['chance_after_constant'] for t in trials)/len(trials),'random_choice_baseline':0.2,'trials':trials})
 domain=[x for x in load('revised-domain-results.json')['cases'] if x['parameters']['n']==2]
 exact=sum(abs(F(x['correct_coeff']))==max(map(F,x['constant_matched_coeffs'])) for x in domain)
 save('rank-confirmation.json',{'seed':94172863,'mixed_count':480,'strategy':'For a printed quadratic term, integrate only the constant; among the matching linear terms choose largest magnitude power coefficient. Never calculate the quadratic antiderivative.','reports':reports,'exhaustive_n2':{'correct':exact,'total':len(domain),'rate':exact/len(domain),'basis':'All unordered divisor pairs and four omitted cells; equiprobable by implementation. Both signs and orders preserve magnitude.','explanation':'Only incorrect divisor 2 gives a coefficient larger than correct 1/3; incorrect divisors 4..9 give smaller coefficients. Correct row retains two or three candidates. Uniform assignments therefore yield 66/84=11/14 success.'},'assessment':'Conditional coefficient magnitude cue bypasses integrating the nonconstant summand. It is imperfect but systematically much more predictive than random selection even after correctly integrating the constant.'})
 save('grader-input-final.json',cases);save('rank-render-records.json',[r for _,r in examples])
 print([(x['file'],x['correct'],x['total'],x['baseline_after_constant']) for x in reports]);print('exhaustive',exact,len(domain))
