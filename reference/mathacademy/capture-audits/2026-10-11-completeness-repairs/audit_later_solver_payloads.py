from pathlib import Path
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'later-source-candidates.json').read_text());rows.append({'account':'multivariable','directory':str(ROOT.parents[1]/'capture/multivariable/14120884/repairs/source-candidates-v1')})
if (ROOT/'later-finite-additional-candidates.json').exists():rows.extend(json.loads((ROOT/'later-finite-additional-candidates.json').read_text()))
for name in ['literal-brace-final-apply-candidates.json', 'frozen318-14123139-candidates.json', 'frozen318-14122335-candidates.json']:
 if (ROOT/name).exists():rows.extend(json.loads((ROOT/name).read_text()))
rows=list({str(Path(row['directory']).parents[1]):row for row in rows}.values())
forbidden={'presentations','previous_submissions','submissions','responses','attempts','current_feedback','source_selected','source_correct','source_result','grade','source_grade','result','field_grades','correct_value','correct_option','correct_origin','correct_evidence','evidence','judgment','proof_feedback','screenshot','screenshot_path','feedback','status','answers','password','token','credentials','cookies','profile','checkpoint'}
seen=set();counts=Counter();bad=[];directories=[];path_bad=[]
for row in rows:
 for directory in (Path(row['directory']).parents[1]/'repairs').glob('completeness-*/solver'):
  if not list(directory.glob('*-restriction.json')):continue
  directories.append(str(directory))
  for p in directory.glob('*/attempt-*.input.json'):
   envelope=json.loads(p.read_text());h=hashlib.sha256(json.dumps(envelope,sort_keys=True).encode()).hexdigest()
   if h in seen:continue
   seen.add(h);counts[envelope.get('task')]+=1
   def walk(v,keypath=''):
    if isinstance(v,dict):
     for k,x in v.items():
      if k in forbidden:bad.append({'file':str(p),'key':keypath+'/'+k})
      walk(x,keypath+'/'+k)
    elif isinstance(v,list):
     for n,x in enumerate(v):walk(x,keypath+'/'+str(n))
    elif isinstance(v,str) and any(s in v for s in ['checkpoint.json','.aws/credentials','xp-ledger.json','retakes.json','Default/Cookies','profiles/']):path_bad.append({'file':str(p),'key':keypath})
   walk(envelope.get('payload',{}))
result={'unique_delivered_envelopes':len(seen),'tasks':dict(counts),'forbidden_payload_keys':bad,'forbidden_private_paths':path_bad,'directories':directories}
(ROOT/'later-solver-payload-audit.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='directories'})
