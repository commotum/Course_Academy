"""Demonstrated author-probe finding: unique maximum fraction count/length."""
import json,sys
sys.dont_write_bytecode=True
from repair_regression import ROOT,g
from visible_math import check_record,sep
rs=[g.generate_easy(seed,'sqrt_quotient',parameters={'a':a,'n':n}) for a,n,seed in [(1,2,31),(5,2,49),(1,4,73),(5,4,97)]]
for r in rs:
 f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];k=f[':answer-field/correct'][1];c=next(c for c in cs if c[':answer/id']==k)
 counts=[z[':answer/value'].replace(g.D,'D').count(r'\frac') for z in cs]
 assert counts.count(max(counts))>=2
 assert sum(sep(z[':answer/value']) and counts[i]==max(counts) for i,z in enumerate(cs))>=2
 assert any(z[':answer/id']!=k and len(z[':answer/value'])==len(c[':answer/value']) for z in cs)
 assert check_record(r)['passed']
(ROOT/'evidence/radical-regression.json').write_text(json.dumps({'passed':True,'tested':len(rs),'records':rs},indent=2,ensure_ascii=False))
print('radical regression:',len(rs),'passed')
# Full visible banks must remain constant when only the radical power changes.
# A prompt-blind modal-root choice can at most guess one of these two targets.
import collections,re
pairs=[];stats=[]
for a in (1,5):
 group=[g.generate_easy(17,'sqrt_quotient',parameters={'a':a,'n':n}) for n in (2,4)]
 banks=[];keys=[];hits=[]
 for r in group:
  f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];key=next(c[':answer/value'] for c in cs if c[':answer/id']==f[':answer-field/correct'][1]);keys.append(key)
  banks.append(sorted(c[':answer/value'] for c in cs));freq=collections.Counter()
  for c in cs:freq.update(re.findall(r'\\sqrt\{[1-5]\+\{y\}\^\{[24]\}\}',c[':answer/value']))
  mode=freq.most_common(1)[0][0];selected=[c[':answer/value'] for c in cs if c[':answer/value'].startswith(g.frac('1',mode)+r'\cdot '+g.D+'=')]
  hits.append(selected==[key]);assert check_record(r)['passed']
 assert banks[0]==banks[1], 'target radical leaks into visible bank'
 assert keys[0]!=keys[1] and sum(hits)<=1, 'modal-root shortcut persists'
 pairs+=group;stats.append({'a':a,'same_bank':True,'distinct_keys':keys,'modal_hits':sum(hits),'total':2})
(ROOT/'evidence/revision-2/radical-records.json').write_text(json.dumps(rs+pairs,indent=2,ensure_ascii=False))
(ROOT/'evidence/revision-2/radical-modal-regression.json').write_text(json.dumps({'passed':True,'groups':stats,'original_layout_regression_preserved':True},indent=2,ensure_ascii=False))
print('radical same-bank modal regression: 2 groups passed')
