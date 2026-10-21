"""Independent visible-math checks for rational bank support, before/after delivery.
No runtime mutation, database writes or service calls. All native cases batch separately.
"""
import collections,json,sys,random
sys.dont_write_bytecode=True
from validate_repair import g,E,dump,check,summarize
from witness import system,vec,field,correct,sp,v
from fraction_shortcut import probe

def inspect(records):
 groups=collections.defaultdict(list);rational=0
 for r in records:
  check(r)
  assert not probe(r)['shortcut_correct'],(r['generation']['seed'],'sole fraction')
  M=system(r['question'][':question/problem']);_,piv=M.rref();fc=next(j for j in range(M.cols-1) if j not in piv)
  vectors=[vec(c[':answer/value']) for c in field(r)[':answer-field/choices']]
  # Read every printed coefficient independently; denominators cannot select a role.
  signatures=[tuple((int(x[j].subs(v[fc],0).q),int(sp.diff(x[j],v[fc]).q)) for j in piv) for x in vectors]
  assert len(set(signatures))==1,('numerical notation distinguishes choices',signatures)
  fractional=any(q>1 for pair in signatures[0] for q in pair);rational+=fractional
  cs=field(r)[':answer-field/choices'];ki=next(i for i,c in enumerate(cs) if c[':answer/id']==correct(r))
  groups[(r['generation']['template'],str(signatures[0]))].append((r,ki))
 out={}
 for (template,sig),group in groups.items():
  rs=[r for r,_ in group];summary=summarize(rs)[template]
  # Conditional cues must not work perfectly in a repeatedly observed template.
  for name,(attempts,hits) in summary['probes'].items():
   assert not(attempts>=4 and attempts==hits),(template,sig,name,attempts,hits)
  out[template+' / denominators '+sig]=summary
 return {'records':len(records),'rational_records':rational,'sole_fraction_successes':0,'coefficient_notation_equal_within_every_bank':True,'conditional_cues':out,'baseline':0.2}

def main():
 if len(sys.argv)>1:
  raw=json.load(open(E/'rational-records.json'));accepted=json.load(open(sys.argv[1]));a=inspect(raw);b=inspect(accepted)
  def semantic(r):
   return (str(system(r['question'][':question/problem'])),
           tuple(sorted(str(vec(c[':answer/value'])) for c in field(r)[':answer-field/choices'])),
           str(vec(next(c[':answer/value'] for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r)))))
  # The shared filter removes the deliberately repeated base of our controlled
  # pair. Compare actual visible semantic sets instead of assuming no dedup.
  assert {semantic(r) for r in raw}=={semantic(r) for r in accepted}
  assert set(a['conditional_cues'])==set(b['conditional_cues'])
  dump('rational-delivery-results.json',{'before':a,'after':b,'same_coverage':True,'same_semantic_instances':True,'duplicate_count':len(raw)-len(accepted)})
  print(json.dumps({'accepted':len(accepted),'same_coverage':True}));return
 exact=g.generate_easy(seed=71381,profile='q-32244');assert system(exact['question'][':question/problem'])==sp.Matrix([[2,2,5],[-10,-10,-25],[8,8,20]])
 records=[g.generate_easy(seed=seed,profile='q-32244') for seed in range(71381,71401)]
 for profile in sorted(g.QUESTIONS):
  if profile!='q-32244':records.extend(g.generate_easy(seed=seed,profile=profile) for seed in (71381,71382,71383,71384))
 p={'free_coefficients':['1/2',-3],'constants':['1/2',4],'mix':[1,1]}
 # Explicit rational slope, intercept, constant coordinate, equal coordinates,
 # zero intercept and alternate free column, preserving easy valid notation.
 boundary=[p,{**p,'free_coefficients':[0,'-1/2']},{**p,'free_coefficients':['1/2','1/2'],'constants':['1/2','1/2']},{**p,'constants':[0,'-1/2']},{**p,'free_coefficients':['1/2',0],'free_column':1},
           {**p,'free_coefficients':[0,-3],'constants':[0,4]},
           {**p,'free_coefficients':[0,0],'constants':[0,0]}]
 records.extend(g.generate_easy(seed=71381,parameters=pp) for pp in boundary)
 cf=[g.generate_easy(seed=71381,parameters=pp) for pp in (p,{**p,'free_coefficients':['-1/2',-3]},{**p,'mix':[-1,1]})]
 records+=cf
 keyed=lambda r:vec(next(c[':answer/value'] for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r)))
 assert keyed(cf[0])!=keyed(cf[1]);assert keyed(cf[0])==keyed(cf[2])
 assert len({r['question'][':question/problem'] for r in cf})==3
 assert len({r['question'][':question/worked-solution'] for r in cf})==3
 source_proposals=0
 for r in records:
  if r['generation']['bank_profile']=='authored_operations':continue
  rng=random.Random(r['generation']['seed']);n=system(r['question'][':question/problem']).cols-1
  expected={'scale':rng.choice([-3,-2,-1,1,2,3]),'offsets':[rng.randint(-5,5) for _ in range(n)]}
  assert r['generation']['parameters']==expected,('source sampling rejected its first valid proposal',r['generation'])
  source_proposals+=1
 report=inspect(records);report['ordinary_source_first_proposals_kept']=source_proposals
 dump('rational-records.json',records);dump('rational-results.json',report)
 dump('rational-counterfactuals.json',{'relevant_coefficient_changes_answer':True,'invertible_row_mixing_preserves_answer':True,'records':cf})
 cases=[{'label':'rational-'+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct(r) else 'rejected','purpose':'independently verified rational full-line choice'} for c in field(r)[':answer-field/choices']]} for i,r in enumerate(records)]
 # Batch native tests for previous selected response under relevant/irrelevant changes.
 import copy
 for i in (1,2):
  r=copy.deepcopy(cf[i]);old=next(c for c in field(cf[0])[':answer-field/choices'] if c[':answer/id']==correct(cf[0]))
  matching=next((c for c in field(r)[':answer-field/choices'] if vec(c[':answer/value'])==vec(old[':answer/value'])),None)
  if matching is None:
   matching=copy.deepcopy(old);field(r)[':answer-field/choices'].append(matching)
  cases.append({'label':'rational-stale-'+str(i),'record':r,'checks':[{'submitted_answer_id':matching[':answer/id'],'expected':'accepted' if i==2 else 'rejected','purpose':'old solution under relevant/irrelevant evidence change'}]})
 dump('rational-grader-input.json',cases)
 dump('rational-render-records.json',[exact,records[20],records[-8],records[-7]])
 inventory=json.load(open(E/'generated-records.json'));tested=[{'question_id':r['question'][':question/id'],'probe':probe(r)} for r in inventory]
 dump('inventory-rational-cue.json',{'tested_generated_records':tested,'demonstrated_fraction_shortcut_count':sum(x['probe']['shortcut_correct'] for x in tested),'limits':'Only ten stored generated records have reproducible historical metadata. Remainder is untested, not certified unaffected. Existing component-frequency affected-inventory.json remains applicable.'})
 print(json.dumps({'records':len(records),'rational_records':report['rational_records'],'fraction_shortcut_successes':0,'source_profiles':14,'grader_checks':sum(len(c['checks']) for c in cases)}))
if __name__=='__main__':main()
