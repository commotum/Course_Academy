"""Parent raw replay: all prompt/solution/bank bytes and attribute presence."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
def check(g,K,D):
 frozen=json.load(open(R/f'sources/{K}.json'));assert json.load(open(D/'source.json'))==frozen
 originals={q[':question/math-academy-id']:q for q in frozen['record'][':knowledge-point/questions']};counts=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0,unrated=0)
 for c in json.load(open(D/'source-cases.json')):
  o=originals[c['source_id']];q=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile')))['question']
  for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (k in q)==(k in o),(c['source_id'],k)
  assert q[':question/problem']==o[':question/problem'];counts['prompts']+=1;counts['unrated']+=(':question/difficulty' not in o)
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];counts['solutions']+=1
  assert len(q.get(':question/answer-fields',[]))==len(o.get(':question/answer-fields',[]))
  for f,old in zip(q.get(':question/answer-fields',[]),o.get(':question/answer-fields',[])):
   assert f[':answer-field/key']==old[':answer-field/key'];assert f[':answer-field/type']==old[':answer-field/type'][':db/ident']
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices']);counts['fields']+=1;counts['values']+=len(old[':answer-field/choices'])
   assert (':answer-field/correct' in f)==(':answer-field/correct' in old)
   if ':answer-field/correct' in old:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==old[':answer-field/correct'][':answer/value'];counts['refs']+=1
   else:counts['missing_refs']+=1
 return originals,counts
