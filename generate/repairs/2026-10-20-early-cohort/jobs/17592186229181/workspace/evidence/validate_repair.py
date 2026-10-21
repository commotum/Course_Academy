"""Executable regression for both retained findings plus affected math/variation checks."""
from checks import *

def main():
 g=load();source=json.loads((ROOT.parent/'source/source.json').read_text());results=[];replays=[]
 # Full current replay contract, beyond the original review's presence-only test.
 for q in source['material']['kp'][':knowledge-point/questions']:
  sid=q[':db/id'];level='moderate' if 'rounded' in q[':question/problem'] else 'easy'
  rec=g.generate(level,61829,template='source_'+str(sid));rq=rec['question'];sf=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
  for field in (':question/problem',':question/worked-solution'):
   assert rq.get(field)==q.get(field) and (field in rq)==(field in q),(sid,field)
  assert rq.get(':question/difficulty')==q.get(':question/difficulty',{}).get(':db/ident')
  assert sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  assert bool(key(rq))==bool(key(q))
  if key(q):
   correct=lambda x:next(a[':answer/value'] for a in x[':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==key(x))
   assert correct(rq)==correct(q)
  results.append(dict(source_id=q[':question/id'],**visible_math(rec,True)));replays.append(rec)
 save('source-replay-records.json',replays);save('source-replay.json',{'banks':len(results),'choices':len(results)*5,'cases':results,'passed':True})
 # Exact reported seed and a small multi-context/sign regression sample.
 records=[g.generate('easy',seed) for seed in range(81031,81061)]
 extras=[g.generate(level,seed) for level in ('moderate','hard') for seed in (81031,81032)]
 assert shortcut(records[0]['question'])!=key(records[0]['question'])
 # Fixed bank, five eligible targets: changes to rate, initial mass, or concentration.
 bank={'c':['.01','.02'],'q0':[3,7],'r':[20,25]};controlled=[];role_rows=[]
 corners=((0,0,0),(0,1,1),(1,0,1),(1,1,0),(1,1,1))
 for context in g.CONTEXTS:
  rs=[]
  for role,bits in enumerate(corners):
   p={'V':500,'context':context,**{k:bank[k][bits[i]] for i,k in enumerate(('c','q0','r'))}}
   rec=g.generate('easy',99173,parameters=p,bank=bank,role=role);rs.append(rec)
  values=lambda r:[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert all(values(r)==values(rs[0]) for r in rs)
  correct_values=[next(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==key(r['question'])) for r in rs]
  assert len(set(correct_values))==5
  # A changed noun preserves the mathematical bank and designated value.
  if context==next(iter(g.CONTEXTS)):reference=correct_values
  assert correct_values==reference
  role_rows.append({'context':context,'identical_visible_bank':True,'distinct_correct_values':5,'any_bank_only_selector_max_correct':1,'total':5})
  controlled.extend(rs)
 # Each coordinate repeats and all options satisfy some valid same-scope IVP.
 # These independent visible counts catch reintroducing any single privileged coordinate.
 all_easy=records+controlled
 for rec in all_easy:
  triples=[ex(a[':answer/value']) for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]
  for coord in (lambda e,a,k:e,lambda e,a,k:e+a,lambda e,a,k:k):
   counts=collections.Counter(coord(*x) for x in triples);assert sorted(counts.values())==[2,3]
  assert shortcut(rec['question']) is None
 all_records=records+extras+controlled
 math=[visible_math(rec) for rec in all_records]
 save('samples.json',records);save('batch.json',records[:5]);save('counterfactual-records.json',controlled);save('extra-records.json',extras);save('math-results.json',{'cases':math,'passed':True})
 checks=[]
 for rec,res in zip(all_records,math):
  checks.append({'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==res['truth'] else 'rejected','purpose':'independent visible IVP oracle'} for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]})
 for rec in replays:
  if key(rec['question']):checks.append({'label':rec['generation']['template'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(rec['question']) else 'rejected','purpose':'current source bank replay'} for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]})
 save('grader-input.json',checks)
 def coverage(rs):
  position=collections.Counter();sign=collections.Counter();contexts=collections.Counter();ranks=collections.Counter()
  for rec in rs:
   q=rec['question'];opts=q[':question/answer-fields'][0][':answer-field/choices'];idx=next(i for i,o in enumerate(opts) if o[':answer/id']==key(q));position[idx]+=1
   V,q0,c,r,time=params(q);sign['increasing' if q0<V*c else 'decreasing']+=1;contexts[rec['generation']['parameters']['context']]+=1
   e,a,k=ex(opts[idx][':answer/value']);ranks[sum(int(bool(ex(o[':answer/value'])[0]<e)) for o in opts)]+=1
  semantic={(str(V*c),str(q0),str(r/V)) for rec in rs for V,q0,c,r,time in [params(rec['question'])]}
  return {'total':len(rs),'semantic_instances':len(semantic),'positions':dict(position),'signs':dict(sign),'contexts':dict(contexts),'key_equilibrium_rank':dict(ranks),'reported_shortcut_successes':sum(shortcut(r['question'])==key(r['question']) for r in rs)}
 raw=coverage(records);assert len(raw['positions'])==5 and len(coverage(controlled)['signs'])==2
 save('pedagogical-variation.json',{'raw':raw,'controlled':role_rows,'proof':'Identical ordered visible banks support all five keyed values, so any deterministic bank-only selector scores exactly 1/5 over a complete target orbit. All three coordinate values have multiplicities 2 and 3, independent of key.','passed':True})
 # Boundaries and invalid input handling remain explicit.
 for p in ({'V':300,'r':10,'c':'.01','q0':1,'context':'salt'},{'V':1000,'r':50,'c':'.06','q0':25,'context':'dye'}):visible_math(g.generate('easy',91,parameters=p))
 invalid=dict(V=500,r=0,c='.02',q0=7,context='coolant')
 try:g.generate('easy',91,parameters=invalid)
 except ValueError:pass
 else:raise AssertionError('zero flow accepted')
 save('repair-results.json',{'findings':['74aa801dd2f129f96a94','7886ce4ab282d3d4cd61'],'source_banks':10,'generated_math_cases':len(math),'controlled_contexts':len(role_rows),'passed':True})
 print(json.dumps({'source_banks':10,'math_cases':len(math),'raw_coverage':raw,'passed':True}))
if __name__=='__main__':main()
