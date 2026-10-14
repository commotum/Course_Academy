"""Parent raw replay: all prompt/solution/bank bytes and attribute presence."""
import json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
def check(g,K,D,asset_relocation=False):
 evidence=json.load(open(D/'source.json'));snapshot=R/json.load(open(R/'manifest.json')).get('source_snapshot_roots',{'1356':'.'})[str(evidence['basis'])]
 frozen=json.load(open(snapshot/f'sources/{K}.json'));assert evidence==frozen
 originals={q.get(':question/math-academy-id',str(q[':db/id'])):q for q in frozen['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q or not (D/'independent-inventory.json').exists()};counts=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0,unrated=0)
 for c in json.load(open(D/'source-cases.json')):
  o=originals.get(c.get('math_academy_id',c.get('source_ma_id',c.get('source_math_academy_id',c['source_id'])))) or next(q for q in originals.values() if str(q[':db/id'])==str(c['source_id']) or q[':question/id']==c['source_id']);q=g.generate(c.get('level',c.get('difficulty',o.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1])),template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile')))['question']
  for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (k in q)==(k in o),(c['source_id'],k)
  new=q[':question/problem'];old=o[':question/problem']
  if asset_relocation:
   a=re.findall(r'!\[.*?\]\((.*?)\)',new);b=re.findall(r'!\[.*?\]\((.*?)\)',old);assert len(a)==len(b)
   for dest,src in zip(a,b):
    native=Path('/media/jake/SSD/EDB/math')/src;assert hashlib.sha256((Path(dest) if Path(dest).is_absolute() else Path('/media/jake/SSD/EDB/math')/dest).read_bytes()).digest()==hashlib.sha256(native.read_bytes()).digest();new=new.replace(dest,src)
  assert new==old;counts['prompts']+=1;counts['unrated']+=(':question/difficulty' not in o)
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];counts['solutions']+=1
  assert len(q.get(':question/answer-fields',[]))==len(o.get(':question/answer-fields',[]))
  for f,old in zip(q.get(':question/answer-fields',[]),o.get(':question/answer-fields',[])):
   assert f[':answer-field/key']==old[':answer-field/key'];assert f[':answer-field/type']==old[':answer-field/type'][':db/ident']
   assert (':answer-field/choices' in f)==(':answer-field/choices' in old)
   assert sorted(a[':answer/value'] for a in f.get(':answer-field/choices',[]))==sorted(a[':answer/value'] for a in old.get(':answer-field/choices',[]));counts['fields']+=1;counts['values']+=len(old.get(':answer-field/choices',[]))
   for a in f.get(':answer-field/choices',[]):
    captured=next(v for v in old[':answer-field/choices'] if v[':answer/value']==a[':answer/value']);assert a[':answer/type']==captured[':answer/type'][':db/ident']
    assert (':answer/feedback' in a)==(':answer/feedback' in captured)
    if ':answer/feedback' in captured:assert a[':answer/feedback']==captured[':answer/feedback']
   assert (':answer-field/correct' in f)==(':answer-field/correct' in old)
   if ':answer-field/correct' in old:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==old[':answer-field/correct'][':answer/value'];counts['refs']+=1
   else:counts['missing_refs']+=1
 return originals,counts
