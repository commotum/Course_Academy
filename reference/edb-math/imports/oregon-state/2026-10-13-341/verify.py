#!/usr/bin/env python3
"""Compare all prepared content with the speculative or committed projection."""
from pathlib import Path
from datetime import datetime
from collections import Counter
from urllib.parse import urlsplit,parse_qs
import json,re,sys,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[5]/'capture'))
from scripts.database.edn import loads
out=Path(__file__).resolve().parent
preview=Path(sys.argv[1]) if len(sys.argv)>1 else out/'preview'
full=json.loads((out/'entities.json').read_text());audit=json.loads((out/'audit.json').read_text());manifest=json.loads((out/'prepared-manifest.json').read_text())
attrs={str(a):(int(e),str(t),str(c)) for e,a,t,c in loads((out/'db/attributes.edn').read_text())}
enums={str(n):int(e) for e,n in loads((out/'db/idents.edn').read_text())}
lookups={(':topic/math-academy-id',ma):int(e) for e,ma,uid in loads((out/'db/topics.edn').read_text())}
lookups.update({(':topic/id',str(uid)):int(e) for e,ma,uid in loads((out/'db/topics.edn').read_text())})
lookups.update({(':course/id',str(uid)):int(e) for e,uid in loads((out/'db/courses.edn').read_text())})
def eid(v):
 if isinstance(v,int):return v
 if isinstance(v,dict):return eid(v[':db/id'])
 if isinstance(v,list):return int(v[0])
 raise ValueError(v)
pulled={}
for identity,row in loads((preview/'final-pull1.edn').read_text()):
 key=(str(identity[0]),str(identity[1]));lookups[key]=eid(row[':db/id']);pulled[key]=row
assert len(pulled)==len(full)
ids={r[':db/id']:(a,str(v['$uuid'])) for r in full for a,v in r.items() if a.endswith('/id') and a!=':db/id'}
def image_value(v):
 def replace(m):return audit['image_map'][parse_qs(urlsplit(m[0]).query)['path'][0]]['path']
 return re.sub(r'/api/asset\?path=[^\s)"<>]+',replace,v)
def expected(v,attr):
 if isinstance(v,dict):
  if '$uuid' in v:return str(v['$uuid'])
  if '$inst' in v:return datetime.fromisoformat(v['$inst'].replace('Z','+00:00')).timestamp()
  if '$ref' in v:
   a,x=v['$ref'];return lookups[(a,str(x['$uuid']) if isinstance(x,dict) else x)]
 if isinstance(v,list):return sorted([expected(x,attr) for x in v],key=str)
 if attrs[attr][1]==':db.type/ref':return lookups[ids[v]] if v in ids else enums[v]
 if attrs[attr][1]==':db.type/string':return image_value(v)
 return v
checks=0
for r in full:
 row=pulled[ids[r[':db/id']]]
 wanted={k for k,v in r.items() if k!=':db/ensure' and v!=[]}
 assert set(row)==wanted,(r[':db/id'],set(row),wanted)
 for attr,v in r.items():
  if attr in (':db/id',':db/ensure') or v==[]:continue
  typ=attrs[attr][1];many=attrs[attr][2]==':db.cardinality/many'
  def norm(x):
   if typ==':db.type/ref':return eid(x)
   if typ==':db.type/uuid':return str(x)
   if typ==':db.type/instant':return datetime.fromisoformat(x.replace('Z','+00:00')).timestamp()
   return x
  actual=sorted([norm(x) for x in row[attr]],key=str) if many else norm(row[attr])
  assert actual==expected(v,attr),(r[':db/id'],attr,actual,expected(v,attr));checks+=1
# Regression checks for the new import cases.
assert len(audit['activities'])==9
assert sum(len(p['quizzes']) for a in audit['activities'] for p in a['problems'])==44
assert len(audit['unkeyed_self_reports'])==4
records={r[':db/id']:r for r in full}
for q in audit['unkeyed_self_reports']:
 row=records[q['question_id']]
 for field in row[':question/answer-fields']:
  assert records[field][':answer-field/type']==':answer-field.type/free'
  assert ':answer-field/correct' not in records[field]
guide=next(a for a in audit['activities'] if a['source'].endswith('_SG-1.md'))
assert guide['due'] is None and guide['problems'][0]['kind']=='study-direction'
source=loads((out/'1-assigned-material.edn').read_text())
assert not any(k in r for r in source for k in (':question/worked-solution',':question/answer-fields',':assigned-problem/topic-coverage',':answer/id',':answer-field/id'))
assert not any('{{' in r.get(':question/problem','') for r in source)
for a in audit['activities']:
 p=Path('/home/jake/Developer/study/vault')/a['source'];assert hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256']
for asset in audit['assets']:assert hashlib.sha256(Path(asset['path']).read_bytes()).hexdigest()==asset['sha256']
result={'committed':False,'entities_compared':len(full),'attribute_comparisons':checks,'all_final_attributes_match':True,'unkeyed_self_reports_ungraded':True,'study_direction_preserved':True,'exam_date_not_assignment_deadline':True,'source_layer_contains_no_authored_keys_or_solutions':True,'field_types':dict(Counter(r[':answer-field/type'] for r in full if ':answer-field/id' in r))}
(preview/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
