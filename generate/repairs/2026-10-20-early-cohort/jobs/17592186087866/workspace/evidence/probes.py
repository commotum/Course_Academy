"""Prompt-independent shortcut probes, before/after actual delivery filtering."""
import json,hashlib
from pathlib import Path
from collections import Counter,defaultdict
E=Path(__file__).resolve().parent

def probe(r):
 f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];parts=[c[':answer/value'].split('=',1) for c in cs]
 lc=Counter(p[0] for p in parts);rc=Counter(p[1] for p in parts)
 scores=[lc[l]+rc[rr] for l,rr in parts];key=f[':answer-field/correct'][1];ki=next(i for i,c in enumerate(cs) if c[':answer/id']==key)
 def picks(vals,which):
  target=which(vals);ix=[i for i,v in enumerate(vals) if v==target]
  return {'unique':len(ix)==1,'success':len(ix)==1 and ix[0]==ki}
 d=r['generation'].get('decision');result={'id':r['question'][':question/id'],'template':r['generation']['template'],'position':ki,'scores':scores,'side_frequency_max':picks(scores,max),'side_frequency_min':picks(scores,min),'shortest':picks([len(c[':answer/value']) for c in cs],min),'longest':picks([len(c[':answer/value']) for c in cs],max)}
 if d and 'q_candidates' in d:
  u=d['p_candidates'];v=d['q_candidates'];slot=d['correct_slot']
  result.update(p_rank=sorted(u).index(u[slot]),q_rank=sorted(v).index(v[slot]),signs=[d['p_sign'],d['q_sign']],coefficient_pair=[u[slot],v[slot]])
 return result

def analyze(rs):
 vals=[probe(r) for r in rs];groups=defaultdict(list)
 for v in vals:groups[v['template']].append(v)
 summaries={}
 for t,vs in groups.items():
  summaries[t]={'records':len(vs),'positions':dict(Counter(v['position'] for v in vs)),'unique_semantic_instances':len({r['generation']['mathematical_fingerprint'] for r in rs if r['generation']['template']==t}),'p_ranks':dict(Counter(v['p_rank'] for v in vs if 'p_rank' in v)),'q_ranks':dict(Counter(v['q_rank'] for v in vs if 'q_rank' in v)),'sign_pairs':dict(Counter(str(v['signs']) for v in vs if 'signs' in v))}
  for name in ('side_frequency_max','side_frequency_min','shortest','longest'):
   summaries[t][name]={'success':sum(v[name]['success'] for v in vs),'unique':sum(v[name]['unique'] for v in vs),'total':len(vs),'chance_baseline':0.2}
 return {'summaries':summaries,'cases':vals}

def main():
 out={}
 for name,path in [('before_raw',E/'before-records.json'),('before_delivered',E/'before-delivered.json'),('after_raw',E/'easy-records.json'),('after_delivered',E/'delivery/accepted.json'),('all_bands',E/'records.json')]:
  rs=json.loads(path.read_text());out[name]=analyze(rs)
  if name.startswith('after'):
   assert all(not v['side_frequency_max']['unique'] for v in out[name]['cases'])
   # Each cue must fail within every family, not just across the entire sample.
   for t,z in out[name]['summaries'].items():
    for cue in ('shortest','longest'):
     assert z[cue]['success'] < z['records'],(name,t,cue)
    assert len(z['positions'])>1,(name,t,'position')
    assert len(z['p_ranks'])>1 and len(z['q_ranks'])>1,(name,t,'coefficient rank')
 # Reproduce native within-easy uniform selection conditional on a positive
 # easy weight, using synthetic sorted IDs because publication has not run.
 rs=json.loads((E/'delivery/accepted.json').read_text());rs=sorted(rs,key=lambda r:r['question'][':question/id']);draws=[]
 for i in range(200):
  seed='author-easy-'+str(i);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);r=rs[int(u*len(rs))];draws.append(probe(r))
 selection={'draws':len(draws),'templates':dict(Counter(v['template'] for v in draws)),'side_frequency_unique':sum(v['side_frequency_max']['unique'] for v in draws),'limits':'Read-only conditional fresh-learner easy draw. Actual database entity ordering, configured band weights, and learner history unavailable; historical exclusions can only remove candidates. No claim of exercising publication or live selection.'}
 (E/'selection-results.json').write_text(json.dumps(selection,indent=2)+'\n')
 (E/'shortcut-results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({n:{t:{k:v for k,v in z.items() if k in ('records','side_frequency_max','shortest','longest')} for t,z in d['summaries'].items()} for n,d in out.items()},indent=2))
if __name__=='__main__':main()
