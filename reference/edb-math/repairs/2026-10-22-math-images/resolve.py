"""Match canonical SVG trees, flattening only nonsemantic SVG grouping wrappers."""
import collections,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];RAW=ROOT/'.local/edb/math-image-import-audit-2026-10-22'
FIXED={'mfrac','msup','msub','msubsup','munder','mover','munderover','mroot'}
def canonical(x):
 if isinstance(x,str):return x
 if isinstance(x,list):return [v for child in x for v in (canonical(child) if isinstance(child,list) else [canonical(child)])]
 children=[canonical(c) for c in x['c']]
 if x['k'] not in FIXED:children=canonical(children)
 out={'k':x['k'],'c':children}
 if 'rules' in x:out['rules']=x['rules']
 return out
def key(fp):return json.dumps(canonical(json.loads(fp)),separators=(',',':')) if fp else None
def resolve():
 targets=json.loads((RAW/'repair-target-fingerprints.json').read_text());candidates=json.loads((RAW/'repair-candidates.json').read_text());rendered=list(map(json.loads,(RAW/'repair-rendered-candidates.jsonl').open()));index=collections.defaultdict(list)
 for i,r in enumerate(rendered):
  if r.get('fp') and not r.get('errors') and not r.get('error'):index[key(r['fp'])].append(i)
 matches={}
 for path,fp in targets.items():
  ids=index.get(key(fp),[]) if fp else []
  if ids:
   best=min(ids,key=lambda i:len(candidates[i]['tex']));matches[path]={'tex':candidates[best]['tex'],'method':'rendered-structure-match','evidence':candidates[best]['evidence'],'matching_candidates':len(ids)}
 for file in ['direct-recoveries.json','normalized-title-recoveries.json']:
  matches.update(json.loads((HERE/file).read_text()))
 missing=[p for p in targets if p not in matches]
 (HERE/'replacements.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2)+'\n');(HERE/'unmatched-assets.json').write_text(json.dumps(missing,indent=2)+'\n')
 print('matched',len(matches),'missing',len(missing),'rendered',len(rendered));return matches,missing
if __name__=='__main__':resolve()
