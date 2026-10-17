"""Audit source content; preserve original fields and proposed normalization separately."""
import collections,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import loads
from math_format import normalize_prose,normalize_tex,validate_prose,validate_tex,MATH

def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2,default=str)+'\n')
entities={}; fields={}; owners=collections.defaultdict(set);topics=[]
attrs=[':tutorial/content',':question/problem',':question/worked-solution',':answer/value',':answer/feedback',':multistep/context',':topic/description',':knowledge-point/description',':answer-field/prompt']
def walk(x,topic):
 if isinstance(x,list):
  for v in x:walk(v,topic)
 elif isinstance(x,dict):
  eid=x.get(':db/id')
  if eid:
   entities.setdefault(eid,{}).update(x);owners[eid].add(topic)
  for v in x.values():walk(v,topic)
for tid in json.loads((HERE/'topic-ids.json').read_text()):
 t=loads((HERE/f'{tid}.edn').read_text());topics.append(t);walk(t,tid)
for eid,e in entities.items():
 for attr in attrs:
  if not isinstance(e.get(attr),str):continue
  kind='math' if attr==':answer/value' and e.get(':answer/type',{}).get(':db/ident')==':answer.type/math' else 'prose'
  value=e[attr];flags=[]
  try:(validate_tex if kind=='math' else validate_prose)(value)
  except Exception as ex:flags.append({'kind':'validation','detail':str(ex)})
  try:
   after=(normalize_tex if kind=='math' else normalize_prose)(value)
   if after!=value:
    # Display whitespace alone is not a formatting defect.
    compact=lambda s:re.sub(r'\s+','',s)
    if compact(after)!=compact(value):flags.append({'kind':'noncanonical','detail':'Shared normalizer changes TeX structure/delimiters'})
  except Exception as ex:after=None;flags.append({'kind':'normalizer-error','detail':str(ex)})
  images=re.findall(r'!\[[^\]]*\]\(([^)]+)\)|<img\b[^>]*?src=[\"\']([^\"\']+)',value)
  imgs=[a or b for a,b in images]
  if imgs:flags.append({'kind':'images','detail':imgs})
  if re.search(r'\\(?:matrix|eqalign)\s*\{',value):flags.append({'kind':'legacy-layout','detail':'Legacy matrix/eqalign macro'})
  if re.search(r'(?<!\\left)\[\s*\\begin\{(?:aligned|matrix|array)\}',value):flags.append({'kind':'fixed-brackets','detail':'Literal brackets around a layout environment'})
  if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',value):flags.append({'kind':'control-character','detail':'Nonprinting control character'})
  if re.search(r'(?m)^ {4,}\S',value):flags.append({'kind':'indented-lines','detail':'Potential unintended Markdown code block; requires rendering'})
  fields[eid,attr]={'entity':eid,'attribute':attr,'kind':kind,'topics':sorted(owners[eid]),'value':value,'normalized':after,'flags':flags}
inv=[]
for t in topics:
 tid=t[':db/id'];es=[e for eid,e in entities.items() if tid in owners[eid]];fs=[f for f in fields.values() if tid in f['topics']]
 inv.append({'id':tid,'title':t.get(':topic/title'),'kps':[e[':db/id'] for e in es if ':knowledge-point/id' in e], 'questions':[e[':db/id'] for e in es if ':question/id' in e],'tutorials':[e[':db/id'] for e in es if ':tutorial/id' in e], 'fields':len(fs),'flags':dict(collections.Counter(flag['kind'] for f in fs for flag in f['flags']))})
save('entities.json',entities);save('fields.json',list(fields.values()));save('inventory.json',inv)
save('findings.json',[f for f in fields.values() if f['flags']])
summary={'topics':len(topics),'kps':sum(':knowledge-point/id' in e for e in entities.values()),'questions':sum(':question/id' in e for e in entities.values()),'tutorials':sum(':tutorial/id' in e for e in entities.values()),'fields':len(fields),'flags':dict(collections.Counter(flag['kind'] for f in fields.values() for flag in f['flags']))}
save('summary.json',summary);print(json.dumps(summary,indent=2))
for x in inv:print(x['id'],x['title'],len(x['kps']),len(x['questions']),x['flags'])
