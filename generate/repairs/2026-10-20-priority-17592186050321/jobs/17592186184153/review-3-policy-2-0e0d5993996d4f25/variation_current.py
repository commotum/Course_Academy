import sys;sys.dont_write_bytecode=True
import json,pathlib,collections,random
from fractions import Fraction as F
from audit_math import *
R=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'workspace'));import generator as G
load=lambda p:json.loads((R/p).read_text())
def save(p,x):(R/p).write_text(json.dumps(x,indent=2)+'\n')
obs={};summary=[]
stages={'raw':load('samples.json'),'delivered':load('delivery/accepted.json'),'runner':load('runner-batch.json'),'runner_delivered':load('batch-delivery/accepted.json')}
sel=load('selection-results.json');pool={max(q[':db/id'] for q in load('../source/inventory.json')['questions'])+100+j:r for j,r in enumerate(stages['delivered'])}
for scenario in sel['scenarios']:
 stages['selected_'+scenario['scenario']]=[pool[i] for i in scenario['draws'] if i in pool]
for stage,records in stages.items():
 trials=[]
 for index,r in enumerate(records):
  if field(r)[':answer-field/type'].endswith('/blank'):continue
  it,v=extract(r);x=V[v];choices=field(r)[':answer-field/choices'];vals=[tex(a[':answer/value']).expand() for a in choices]
  cs=[a.coeff(x,1) for a in vals];ci=next(j for j,a in enumerate(choices) if a[':answer/id']==answer(r)[':answer/id'])
  repeat=collections.Counter(cs);non_single=[j for j,c in enumerate(cs) if repeat[c]>1];bounded=[j for j,c in enumerate(cs) if abs(c)<=6]
  rand=random.Random('independent-'+r['question'][':question/id'])
  lengths=[len(a[':answer/value']) for a in choices]
  choices_by_cue={'eliminate_singleton':non_single,'constant_bound_6':bounded,'shortest':[j for j,n in enumerate(lengths) if n==min(lengths)],'longest':[j for j,n in enumerate(lengths) if n==max(lengths)],**{'position_'+str(j):[j] for j in range(5)}}
  t={'index':index,'qid':r['question'][':question/id'],'profile':r['generation']['template'],'n':r['generation']['parameters']['n'],'s':r['generation']['parameters']['s'],'order':r['generation']['parameters']['constant_first'],'linear_coefficients':list(map(str,cs)),'correct_index':ci,'outside_bound':len(bounded)<5,'strategies':{}}
  for cue,eligible in choices_by_cue.items():
   chosen=rand.choice(eligible);t['strategies'][cue]={'eligible':eligible,'chosen':chosen,'success':chosen==ci,'expected_success_given_ties':float(F(int(ci in eligible),len(eligible)))}
  trials.append(t)
 obs[stage]=trials
 for group,ts in [('radios',trials)]+[(p,[o for o in trials if o['profile']==p]) for p in 'PR']+[(f'{p}_n{n}',[o for o in trials if o['profile']==p and o['n']==n]) for p,ns in [('P',range(2,7)),('R',(3,7))] for n in ns] + [('bound_visible',[o for o in trials if o['outside_bound']])]:
  if not ts:continue
  for cue in trials[0]['strategies']:
   summary.append({'stage':stage,'subgroup':group,'cue':cue,'correct':sum(o['strategies'][cue]['success'] for o in ts),'total':len(ts),'tie_averaged_rate':sum(o['strategies'][cue]['expected_success_given_ties'] for o in ts)/len(ts),'baseline':0.2})
save('shortcut-trials.json',obs);save('shortcut-results.json',summary)
# Revision: all five possible nonkey omissions are accepted and math valid.
controls=[]
base=G.instance('P',3,-1,5,'x',True,offset=-2,second_offset=2,factors=('4/3',))
for cell in [(0,1),(1,0),(1,1),(2,0),(2,1)]:
 r=G.build(dict(base,omitted_row=cell[0],omitted_col=cell[1]),random.Random(89123));verify(r);controls.append(r)
save('omission-controls.json',controls)
# Relevant/irrelevant dependency pairs on reciprocal template.
cf=[];pairs=[]
b=G.instance('R',3,1,4,'x',False,offset=-2,second_offset=1,factors=('1/2',))
for label,delta,kind in [('R_exponent',{'n':7,'factors':['5/3']},'relevant'),('R_sign',{'s':-1},'relevant'),('R_constant',{'k':5},'relevant'),('R_order',{'constant_first':True},'irrelevant')]:
 j=len(cf);a=G.build(b,random.Random(911));z=G.build(dict(b,**delta),random.Random(911));cf.extend([a,z]);verify(a);verify(z)
 same=equal(tex(answer(a)[':answer/value']),tex(answer(z)[':answer/value']));assert same==(kind=='irrelevant')
 pairs.append({'label':label,'delta':delta,'kind':kind,'indices':[j,j+1],'passes':True})
save('reciprocal-counterfactual-records.json',cf);save('reciprocal-counterfactual-results.json',pairs)
# Prompt-level antiderivative equivalence, including an additive constant absorbed by C.
blank=next(r for r in stages['raw'] if field(r)[':answer-field/type'].endswith('/blank'))
f,v=extract(blank);a=tex(answer(blank)[':answer/value']);shift=a+1
assert equal(S.diff(shift,V[v]),f)
save('constant-shift-math.json',{'record':blank,'submitted':str(shift).replace('**','^'),'derivative':str(S.diff(shift,V[v])),'integrand':str(f),'rationale':'Displayed +C is arbitrary; F(t)+1+C describes exactly the same family as F(t)+C. Prompt has no instruction forbidding a constant term in the blank.','equivalent_family':True})
cases=[]
for j,r in enumerate(cf+controls+stages['runner_delivered']):
 ff=field(r)
 if ff[':answer-field/type'].endswith('/blank'):
  aa=tex(answer(r)[':answer/value']);checks=[{'submitted':str(S.factor(aa)).replace('**','^'),'expected':'accepted','purpose':'factored equivalent'},{'submitted':str(aa+V['t']).replace('**','^'),'expected':'rejected','purpose':'wrong derivative'}]
 else:checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==answer(r)[':answer/id'] else 'rejected','purpose':'independent differentiation'} for c in ff[':answer-field/choices']]
 cases.append({'label':'current additional '+str(j),'record':r,'checks':checks})
cases.append({'label':'valid constant-shift antiderivative','record':blank,'checks':[{'submitted':str(shift).replace('**','^'),'expected':'accepted','purpose':'same general antiderivative family under displayed arbitrary +C'}]})
save('additional-grader-input.json',cases)
# Render all original pairs, new reciprocal pairs, revision omission control and complete replay radio banks.
replays=[r for r in load('source-replay.json') if not r.get('math_only')]
save('render-all.json',load('render-records.json')+cf+[controls[0],blank]+replays)
coverage={stage:{p:{'count':len([r for r in rs if r['generation']['template']==p]),**{k:dict(collections.Counter(str(r['generation']['parameters'][k]) for r in rs if r['generation']['template']==p)) for k in ['n','s','k','variable','constant_first','omitted_row','omitted_col']}} for p in 'PRB'} for stage,rs in stages.items()}
save('coverage.json',coverage)
print(json.dumps([x for x in summary if x['stage'] in ['raw','delivered'] and x['cue'] in ['eliminate_singleton','constant_bound_6'] and x['subgroup'] in ['radios','bound_visible']]))
