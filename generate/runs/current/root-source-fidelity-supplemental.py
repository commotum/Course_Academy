"""Parent raw replay: all prompt/solution/bank bytes and attribute presence."""
import json,re,hashlib
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import importlib.util
import sympy as s
_parser_spec=importlib.util.spec_from_file_location('supplemental_root_math',Path(__file__).with_name('ode-scalar-parser.py'))
_parser=importlib.util.module_from_spec(_parser_spec);_parser_spec.loader.exec_module(_parser)
def equivalent(a,b):return s.simplify(s.expand(_parser.scalar(a.strip().rstrip('.,'))-_parser.scalar(b.strip().rstrip('.,'))))==0

R=Path(__file__).resolve().parent
def check(g,K,D,asset_relocation=False):
 evidence=json.load(open(D/'source.json'));snapshot=R/json.load(open(R/'manifest.json')).get('source_snapshot_roots',{'1356':'.'})[str(evidence['basis'])]
 frozen=json.load(open(snapshot/f'sources/{K}.json'));assert evidence==frozen
 supplemental_path=D/'source-supplemental-2548.json'
 if supplemental_path.exists():
  supplemental=json.load(open(supplemental_path));assert supplemental==json.load(open(R.parents[2]/f'generate/scratch/{K}/source.json'))
  assert supplemental['basis']==2548 and supplemental['lineage']==evidence['lineage'] and supplemental['database']==evidence['database']
  assert supplemental['record'][':db/id']==frozen['record'][':db/id']
  A={q[':question/math-academy-id']:q for q in frozen['record'][':knowledge-point/questions']};B={q[':question/math-academy-id']:q for q in supplemental['record'][':knowledge-point/questions']}
  assert all(B[k]==q for k,q in A.items())
  frozen=dict(frozen);frozen['record']=dict(frozen['record']);frozen['record'][':knowledge-point/questions']=list(A.values())+[q for k,q in B.items() if k not in A]

 originals={q.get(':question/math-academy-id',str(q[':db/id'])):q for q in frozen['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q or not (D/'independent-inventory.json').exists()};counts=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0,unrated=0)
 for c in json.load(open(D/'source-cases.json')):
  o=originals.get(c.get('math_academy_id',c.get('source_ma_id',c.get('source_math_academy_id',c['source_id'])))) or next(q for q in originals.values() if str(q[':db/id'])==str(c['source_id']) or q[':question/id']==c['source_id']);q=g.generate(c.get('level',c.get('difficulty',c.get('authored_level') or o.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1])),template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile')))['question']
  # A raw evidence API may preserve the exact Pull object, including nested
  # enums, original IDs and original correct-answer maps. Full object equality
  # is stricter than the flat generated-record comparison below.
  if q==o:
   counts['prompts']+=1;counts['solutions']+=(':question/worked-solution' in o);counts['unrated']+=(':question/difficulty' not in o)
   for field in o.get(':question/answer-fields',[]):
    counts['fields']+=1;counts['values']+=len(field.get(':answer-field/choices',[]));counts['refs']+=(':answer-field/correct' in field);counts['missing_refs']+=(':answer-field/correct' not in field)
   continue
  for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (k in q)==(k in o),(c['source_id'],k)
  if ':question/difficulty' in o:assert q[':question/difficulty']==o[':question/difficulty'][':db/ident'],(c['source_id'],'source difficulty changed')
  new=q[':question/problem'];old=o[':question/problem']
  if asset_relocation:
   a=re.findall(r'!\[.*?\]\((.*?)\)',new);b=re.findall(r'!\[.*?\]\((.*?)\)',old);assert len(a)==len(b)
   for dest,src in zip(a,b):
    native=Path('/media/jake/SSD/EDB/math')/src;assert hashlib.sha256((Path(dest) if Path(dest).is_absolute() else Path('/media/jake/SSD/EDB/math')/dest).read_bytes()).digest()==hashlib.sha256(native.read_bytes()).digest();new=new.replace(dest,src)
  assert new==(old if c['source_id']!='q-167329' else re.sub(r'(?m)^[ \t]+(?=\$)','',old));counts['prompts']+=1;counts['unrated']+=(':question/difficulty' not in o)
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];counts['solutions']+=1
  assert len(q.get(':question/answer-fields',[]))==len(o.get(':question/answer-fields',[]))
  newfields=q.get(':question/answer-fields',[]);oldfields=o.get(':question/answer-fields',[])
  # Pull field collection order does not define a blank's position. Match unique
  # keys one-to-one; legacy duplicate keys still require occurrence-order parity.
  if len({f[':answer-field/key'] for f in oldfields})==len(oldfields):
   assert len({f[':answer-field/key'] for f in newfields})==len(newfields)
   assert {f[':answer-field/key'] for f in newfields}=={f[':answer-field/key'] for f in oldfields}
   keyed={f[':answer-field/key']:f for f in newfields};newfields=[keyed[f[':answer-field/key']] for f in oldfields]
  for f,old in zip(newfields,oldfields):
   assert f[':answer-field/key']==old[':answer-field/key'];assert f[':answer-field/type']==old[':answer-field/type'][':db/ident']
   assert (':answer-field/choices' in f)==(':answer-field/choices' in old)
   remaining=list(f.get(':answer-field/choices',[]));assert len(remaining)==len(old.get(':answer-field/choices',[]))
   for captured_value in old.get(':answer-field/choices',[]):
    candidates=[i for i,a in enumerate(remaining) if equivalent(a[':answer/value'],captured_value[':answer/value'])];assert len(candidates)==1,(c['source_id'],captured_value);remaining.pop(candidates[0])
   assert not remaining;counts['fields']+=1;counts['values']+=len(old.get(':answer-field/choices',[]))
   for a in f.get(':answer-field/choices',[]):
    captured=next(v for v in old[':answer-field/choices'] if equivalent(v[':answer/value'],a[':answer/value']));assert a[':answer/type']==captured[':answer/type'][':db/ident']
    assert (':answer/feedback' in a)==(':answer/feedback' in captured)
    if ':answer/feedback' in captured:assert a[':answer/feedback']==captured[':answer/feedback']
   assert (':answer-field/correct' in f)==(':answer-field/correct' in old)
   if ':answer-field/correct' in old:assert equivalent(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]),old[':answer-field/correct'][':answer/value']);counts['refs']+=1
   else:counts['missing_refs']+=1
 return originals,counts
