"""Focused within-template degree-1 audit before/after shared delivery filtering."""
import collections,json,re
from pathlib import Path
import sympy as s
import generator as g
E=Path('evidence/author-2')
def stats(rs):
 groups=collections.defaultdict(list);semantic=set();out={}
 for r in rs:
  m=r['generation'];p=m['parameters'];f=r['question'][':question/answer-fields'][0]
  val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  prod=g.parse(re.search(r'\$([^$]*)\$',r['question'][':question/problem'])[1].rstrip('.'))
  semantic.add((s.srepr(s.expand(prod)),s.srepr(s.expand(g.parse(val)))))
  if m['template']!='q-310188':groups[(m['template'],p.get('trig','fixed-source-trig'))].append(r)
 for sig,items in groups.items():
  cue=collections.Counter();positions=collections.Counter();roles=set()
  for r in items:
   f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];correct=f[':answer-field/correct'][1];roles.add(str(r['generation']['missing_term']))
   if f[':answer-field/type'].endswith('/blank'):continue
   positions[next(i for i,a in enumerate(cs) if a[':answer/id']==correct)]+=1
   for name,fn in [('shortest',min),('longest',max),('fewest_minus',min),('most_minus',max)]:
    def score(a):
     z=re.sub(r'\\[A-Za-z]+|[{}\s]','',a[':answer/value'])
     return len(z) if name in ('shortest','longest') else z.count('-')
    cue[name]+=fn(cs,key=score)[':answer/id']==correct
  if positions:
   assert len(positions)>1,(sig,'fixed position')
   for name,wins in cue.items():assert wins<len(items),(sig,name,'perfect predictor')
  else:assert roles=={'0','1'}
  out[':'.join(sig)]={'records':len(items),'positions':dict(positions),'surface_strategy_successes':dict(cue),'attempts':len(items),'radio_random_baseline':0.2 if positions else None,'completion_roles':sorted(roles)}
 return {'records':len(rs),'semantic_instances':len(semantic),'within_degree_1_groups':out}
a=json.loads((E/'delivery-input.json').read_text());b=json.loads((E/'delivery/accepted.json').read_text());report={'before':stats(a),'after':stats(b)}
assert any(r['generation']['template']=='q-310188' and r['generation']['parameters']=={'b':4} for r in b)
report.update({'tested_shortcuts_passed':True,'log_failure_survives_delivery':True,'selection_limit':'Captured inventory only; existing read-only selection audit applies. Live learner history/active policy unavailable.','scope':'Degree-1 new boundary, conditioned on polynomial profile and eligible primitive trig; finite diagnostic sample, no universal absence-of-shortcuts claim.'})
(E/'variation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['tested_shortcuts_passed','log_failure_survives_delivery']}));print('before/after semantic instances',report['before']['semantic_instances'],report['after']['semantic_instances'])
