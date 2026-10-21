import sys;sys.dont_write_bytecode=True
import json,pathlib,collections,random,hashlib
from fractions import Fraction as F
from functools import lru_cache
from audit_math import tex,field,answer,V,extract,verify,S,equal
R=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'workspace'));import generator as G
load=lambda n:json.loads((R/n).read_text())
def save(n,v):(R/n).write_text(json.dumps(v,indent=2)+'\n')
@lru_cache(None)
def parsed(s):return tex(s).subs(V['C'],0).expand()
def observe(r):
 i=r['generation']['parameters'];x=V[i['variable']];p=(-S.Rational(i['n'],2) if i['profile']=='R' else S.Integer(i['n']))+1
 choices=field(r)[':answer-field/choices'];vals=[parsed(a[':answer/value']) for a in choices]
 cs=[v.coeff(x,1) for v in vals];ps=[v.coeff(x**p) for v in vals]
 ci=next(j for j,a in enumerate(choices) if a[':answer/id']==answer(r)[':answer/id'])
 count=collections.Counter(cs);eligible=[j for j,c in enumerate(cs) if count[c]>1]
 # Seeded tie draw is repeatable and independent of mathematical content.
 chosen=random.Random('review-3-'+r['question'][':question/id']).choice(eligible)
 matched=[j for j,c in enumerate(cs) if c==i['k']]
 evens=[j for j in matched if abs(ps[j]).as_numer_denom()[0]%2==0]
 parity=random.Random('parity-'+r['question'][':question/id']).choice(evens or matched)
 return {'qid':r['question'][':question/id'],'profile':i['profile'],'n':i['n'],'s':i['s'],'order':i['constant_first'],'correct_index':ci,'constant_coefficients':list(map(str,cs)),'power_coefficients':list(map(str,ps)),'row_multiplicities':[count[c] for c in cs],'eligible_indices':eligible,'chosen_index':chosen,'success':chosen==ci,'true_row_survives':ci in eligible,'conditional_parity_choice':parity,'conditional_parity_success':parity==ci,'correct_constant_candidates':matched,'lengths':[len(a[':answer/value']) for a in choices]}
stages={'raw':load('samples.json'),'delivered':load('delivery/accepted.json'),'runner':load('runner-batch.json'),'runner_delivered':load('batch-delivery/accepted.json')}
coverage={};probes=[];trials={}
for stage,rs in stages.items():
 coverage[stage]={}
 for t in 'PRB':
  group=[r for r in rs if r['generation']['template']==t];ps=[r['generation']['parameters'] for r in group]
  coverage[stage][t]={'count':len(group),**{k:dict(collections.Counter(str(p[k]) for p in ps)) for k in ['n','s','k','constant_first','variable','omitted_row','omitted_col']}}
 trials[stage]=[observe(r) for r in rs if r['generation']['template'] in 'PR']
 for subgroup,ts in [('all_radios',trials[stage])]+[(t,[o for o in trials[stage] if o['profile']==t]) for t in 'PR']:
  if not ts:continue
  probes.append({'stage':stage,'subgroup':subgroup,'strategy':'Eliminate the choice whose linear coefficient occurs only once; choose uniformly from the remaining four. No prompt inspection or integration.','correct':sum(o['success'] for o in ts),'total':len(ts),'surviving_correct':sum(o['true_row_survives'] for o in ts),'expected_rate':0.25,'baseline':0.2,'trials_file':'shortcut-trials.json'})
  for cue in ['shortest','longest','position_0','position_1','position_2','position_3','position_4']:
   chosen=lambda o: (min(range(5),key=lambda j:o['lengths'][j]) if cue=='shortest' else max(range(5),key=lambda j:o['lengths'][j]) if cue=='longest' else int(cue[-1]))
   probes.append({'stage':stage,'subgroup':subgroup,'strategy':cue,'correct':sum(chosen(o)==o['correct_index'] for o in ts),'total':len(ts),'baseline':0.2,'trials_file':'shortcut-trials.json'})
 for n in (3,7):
  ts=[o for o in trials[stage] if o['profile']=='R' and o['n']==n]
  if ts:probes.append({'stage':stage,'subgroup':f'R{n}_constant_matched','strategy':'Prefer an even displayed reciprocal numerator, breaking ties uniformly.','correct':sum(o['conditional_parity_success'] for o in ts),'total':len(ts),'baseline':0.5,'trials_file':'shortcut-trials.json'})
save('coverage.json',coverage);save('shortcut-trials.json',trials);save('shortcut-results.json',probes)
# Exhaustive graph proof covers each possible omitted cell in normal generator,
# and coefficient-side and constant-rank controls without relying on sampling.
graph=[]
for omitted_row in (1,2):
 for omitted_col in (0,1):
  cells=[(r,c) for r in range(3) for c in range(2) if (r,c)!=(omitted_row,omitted_col)]
  eligible=[cell for cell in cells if sum(a==cell[0] for a,b in cells)>1]
  graph.append({'omitted_cell':[omitted_row,omitted_col],'cells':cells,'eligible':eligible,'correct_cell':[0,0],'correct_survives':(0,0) in eligible,'eligible_count':len(eligible),'unconditional_uniform_rate':'1/5','cue_uniform_rate':'1/4'})
assert all(x['correct_survives'] and x['eligible_count']==4 for x in graph)
# Legitimate same-skill bank: remove the wrong-power cell from the true constant
# row, leaving the correct cell and four wrong options. Public instance rejects.
base=G.instance('P',3,-1,5,'x',True,offset=-2,factors=('4/3',),omitted_row=1,omitted_col=1,second_offset=2)
try:
 G.instance(**dict(base,omitted_row=0,omitted_col=1));rejected=False
except ValueError as e:rejected=str(e)
save('structural-shortcut-proof.json',{'derivation':'Every normal radio is a 3x2 grid minus a cell in a wrong-constant row. Exactly one constant is singleton; the correct constant always has degree two. Eliminate singleton without inspecting integrand: exact 1/4 vs 1/5 chance, a 25% relative gain, on every P/R instance. Numerical values and option shuffling do not change this.','graphs':graph,'eligible_counterfactual':{'base':base,'change':{'omitted_row':0,'omitted_col':1},'expected':'Still five choices, exactly one antiderivative, no new operation; correct constant becomes singleton.','observed_rejection':rejected}})
# Actual relevant and irrelevant paired instances, including reciprocal dependency.
cf=[];pairs=[]
def pair(label,i,delta,kind):
 a=G.build(i,random.Random(803));b=G.build(dict(i,**delta),random.Random(803));j=len(cf);cf.extend([a,b]);verify(a);verify(b)
 av=tex(answer(a)[':answer/value']);bv=tex(answer(b)[':answer/value'])
 if label=='R_variable':av=av.subs(V['x'],V['y'])
 assert equal(av,bv)==(kind=='irrelevant')
 pairs.append({'label':label,'kind':kind,'indices':[j,j+1],'delta':delta,'before_answer':answer(a)[':answer/value'],'after_answer':answer(b)[':answer/value'],'same_under_substitution':equal(av,bv),'passes':True})
r=G.instance('R',3,1,4,'x',False,offset=-2,second_offset=1,factors=('1/2',),omitted_row=1,omitted_col=1)
pair('R_exponent',r,{'n':7,'factors':['5/3']},'relevant');pair('R_sign',r,{'s':-1},'relevant');pair('R_constant',r,{'k':5},'relevant');pair('R_order',r,{'constant_first':True},'irrelevant');pair('R_variable',r,{'variable':'y'},'irrelevant');pair('P_competitor_side',base,{'factors':['1/2']},'irrelevant')
save('additional-counterfactual-records.json',cf);save('additional-counterfactual-results.json',pairs)
# Exact unchanged-key counterfactual uses honest generated choices; this is solely
# a bank rearrangement test fixture, not a generator repair or publication.
original=G.build(base,random.Random(803));other=dict(base,omitted_row=0,omitted_col=1)
# Construct allowable alternatives independently with public record constructor.
integrand=5-V['x']**3;v='x';values=[r'5x-\frac{x^{4}}{4}+C',r'3x-\frac{x^{4}}{4}+C',r'3x-\frac{x^{4}}{3}+C',r'7x-\frac{x^{4}}{4}+C',r'7x-\frac{x^{4}}{3}+C']
control=G.record(original['question'][':question/problem'],original['question'][':question/worked-solution'],values,0,'radio','moderate',{'template':'independent-bank-counterfactual','purpose':'omit wrong coefficient from correct constant row'},random.Random(803))
verify(control);save('bank-assignment-control.json',[original,control])
# Batch native grading input: pair records, cross responses and graph control.
cases=[]
for j,record in enumerate(cf+[original,control]):
 f=field(record);cases.append({'label':'additional '+str(j),'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==answer(record)[':answer/id'] else 'rejected','purpose':'independently differentiated alternative'} for a in f[':answer-field/choices']]})
# Add equivalent cross-answers via existing blank paired records and grader harness.
save('additional-grader-input.json',cases)
save('additional-render-records.json',cf+[original,control])
(R/'session-state.md').write_text('Milestone: 475 exact text-derived math checks, seven source replays and 21 choices, CLI/runtime/relocation passed. Native initial grading and delivery completed. Structural shortcut identified: correct constant never singleton; exact 1/4 vs 1/5 cue advantage. Current grid rejects eligible omission in correct-constant row. Added independent paired bank control. Rendering/selection/final evidence pending.\n')
print(json.dumps({'stage_counts':{k:len(v) for k,v in stages.items()},'structural_probes':[x for x in probes if x['strategy'].startswith('Eliminate')],'additional_pairs':len(pairs),'legitimate_grid_rejected':rejected}))
