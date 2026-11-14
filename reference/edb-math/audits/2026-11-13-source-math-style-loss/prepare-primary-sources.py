from pathlib import Path
import sys,json,re,collections
sys.path.insert(0,'scripts')
from audit_capture_math_styles_sources import canon_id,EXCLUDED_PARTS,paths,ROOT
out=Path('reference/edb-math/audits/2026-11-13-source-math-style-loss');out.mkdir(exist_ok=True,parents=True)
current=json.loads((out/'current.json').read_text());allowed={canon_id(x['ma_id'],'tutorial' if k=='tutorials' else None) for k in ['questions','tutorials'] for x in current[k]}
roots={'capture','question-capture','question-capture-workers','diagnostic-capture','review-13925710','sum-rule-13925458','factorials-13831129','multistep-13931219','assessment-13930620','progress-history-2026-10-04'}
choices={}; states=[]; counts=collections.Counter(); rows=[]
for source_path in paths([ROOT/'reference/mathacademy'/name for name in sorted(roots)]):
 p=source_path.relative_to(ROOT) if source_path.is_absolute() else source_path
 if p.parts[2] not in roots:continue
 row={'path':str(p)};rows.append(row);counts['all_files']+=1
 exclude=next((v for v in p.parts if v in EXCLUDED_PARTS),None)
 if exclude:row.update(status='excluded-derived-directory',reason=exclude);continue
 row['bytes']=p.stat().st_size
 if p.suffix=='.gz':row['status']='deferred-backup';continue
 if p.suffix=='.json' and p.with_suffix('.html').exists():row['status']='duplicate-adjacent-html';continue
 ident=canon_id(p.name)
 if ident and ident in allowed:
  role='worked-solution' if 'history-solution' in p.name else 'problem' if p.suffix=='.html' and p.name.startswith('history-q') else 'combined'
  priority=0 if p.suffix=='.html' else 1
  key=(ident,role);rank=(priority,-row['bytes'])
  if key not in choices or rank<choices[key][0]:choices[key]=(rank,row)
  row.update(status='deferred-alternate-same-identity-role',math_academy_id=ident,role=role)
 elif p.name=='state.json' and p.parts[2] in ('question-capture','question-capture-workers'):
  states.append(row);row['status']='selected-embedded-state'
 elif p.parts[2] not in ('capture','question-capture','question-capture-workers') and p.suffix in ('.html','.json'):
  states.append(row);row['status']='selected-one-off-original'
 else:row['status']='deferred-aggregate-or-unmapped-source'
for (ident,role),(rank,row) in choices.items():
 if role=='combined' and (ident,'problem') in choices and (ident,'worked-solution') in choices:
  continue
 row['status']='selected-primary-identity-role'
selected=[r for r in rows if r['status'].startswith('selected-')]
shards=[[] for _ in range(8)];sizes=[0]*8
for r in sorted(selected,key=lambda r:-r['bytes']):
 i=min(range(8),key=lambda i:sizes[i]);shards[i].append(r['path']);sizes[i]+=r['bytes']
for i,group in enumerate(shards):(out/f'primary-files-{i}.txt').write_text('\n'.join(group)+'\n')
with (out/'source-census.jsonl').open('w') as f:
 for row in rows:f.write(json.dumps(row,separators=(',',':'))+'\n')
summary={'counts':dict(collections.Counter(r['status'] for r in rows)),'bytes':dict((status,sum(r.get('bytes',0) for r in rows if r['status']==status)) for status in set(r['status'] for r in rows)),'selected_identities':len({r.get('math_academy_id') for r in selected})-1,'current_identities':len(allowed),'shard_bytes':sizes,'limitations':['Only one primary source per identity/role selected; alternative captures are censused but deferred, not assumed byte duplicates.','Aggregated/redundant pages, gzip backups, and unmapped placement-only files deferred.','Legacy state.json original embedded HTML and one-off original source trees retained.']}
(out/'source-census-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
