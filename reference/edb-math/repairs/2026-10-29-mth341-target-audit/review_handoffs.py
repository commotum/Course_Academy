"""Check proposal payloads against the fixed source snapshots before integration."""
import collections,json
from pathlib import Path
H=Path(__file__).resolve().parent
allowed={'question/problem','question/worked-solution','tutorial/content','answer/value','answer/feedback','answer-field/key','answer-field/correct','answer/type','answer-field/type'}
def scalar(v):
 if isinstance(v,dict)and':db/id'in v:return v[':db/id']
 return v
reports=[];all_changes={}
for name in['group-1','group-2','group-3']:
 D=H/name;path=D/'proposals.json'
 if not path.exists():continue
 snapshot=json.loads((D/'current.json').read_text());values={}
 def visit(v):
  if isinstance(v,list):
   for x in v:visit(x)
  elif isinstance(v,dict):
   e=v.get(':db/id')
   for k,x in v.items():
    if e is not None:values[e,k.lstrip(':')]=scalar(x)
    if isinstance(x,(dict,list)):visit(x)
 visit(snapshot);ps=json.loads(path.read_text());seen={};errors=[]
 for p in ps:
  e,a=p['entity'],p['attribute'];before=p.get('before');pair=e,a
  if a not in allowed:errors.append({'pair':pair,'reason':'Unexpected attribute'})
  if before!=values.get(pair):errors.append({'pair':pair,'reason':'Before value does not match fixed source snapshot'})
  if p['after']==before:errors.append({'pair':pair,'reason':'No-op proposal'})
  if pair in seen:errors.append({'pair':pair,'reason':'Duplicate entity/attribute proposal'})
  if pair in all_changes and all_changes[pair]!=p['after']:errors.append({'pair':pair,'reason':'Cross-group conflict'})
  all_changes[pair]=p['after'];seen[pair]=p
 reports.append({'group':name,'proposals':len(ps),'attributes':dict(collections.Counter(p['attribute']for p in ps)),'errors':errors})
result={'passed':not any(r['errors']for r in reports),'groups':reports,'distinct_fields':len(all_changes)};(H/'handoff-preflight.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
