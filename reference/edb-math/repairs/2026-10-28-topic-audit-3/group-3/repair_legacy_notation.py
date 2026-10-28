import json,re
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());F={(f['entity'],f['attribute']):f for f in json.loads((H/'fields.json').read_text())};props={(r['entity'],r['attribute']):r for r in json.loads((H/'proposals.json').read_text())};dropped={r['value']for r in json.loads((H/'duplicate-field-membership-proposals.json').read_text())};exclude=set(dropped)
for q in D['questions']:
 for f in q.get(':question/answer-fields',[]):
  if f[':db/id']in dropped:exclude|={a[':db/id']for a in f[':answer-field/choices']}
  if f[':answer-field/type'][':db/id']==17592186045492:exclude|={a[':db/id']for a in f[':answer-field/choices']if a[':db/id']!=f.get(':answer-field/correct',{}).get(':db/id')}
removed=[k for k in props if k[0]in exclude]
for k in removed:del props[k]
changes=[]
for key,f in F.items():
 if key[0]in exclude:continue
 text=props.get(key,{}).get('after',f['value']);after=text
 after=re.sub(r'(\\(?:i{1,3}nt)|[∫∬∭])_\(([A-Z])\)',lambda m:m[1]+'_{'+m[2]+'}',after)
 after=re.sub(r'([A-Z]{2})\^\(→\)',lambda m:r'\overrightarrow{'+m[1]+'}',after)
 after=re.sub(r'([A-Z]{2})\^\(―\)',lambda m:r'\overline{'+m[1]+'}',after)
 if key==(17592186179958,'question/problem'):after=after.replace('AAAAA',r'\boxed{?}')
 if after==text:continue
 prior=props.get(key,{});props[key]={'entity':key[0],'attribute':key[1],'before':f['value'],'after':after,'reason':prior.get('reason','')+' Recover explicit integral region subscripts, vector/segment arrows, or a missing-expression placeholder from legacy serialization.','evidence':{**prior.get('evidence',{}),'classification':'authored notation repair supported by the complete task; not claimed as exact recovery when the original archive is unavailable','legacy_serialization_before':text,'keystroke_bank_untouched':True},'confidence':'high'};changes.append({'entity':key[0],'attribute':key[1]})
(H/'proposals.json').write_text(json.dumps(list(props.values()),indent=2));(H/'legacy-notation-evidence.json').write_text(json.dumps({'repairs':changes,'excluded_obsolete_or_learner_entities':sorted(exclude),'sourceformat_proposals_removed_for_obsolete_entities':removed},indent=2));print('notationfields',len(changes),'obsolete proposals removed',len(removed),'total content',len(props))
