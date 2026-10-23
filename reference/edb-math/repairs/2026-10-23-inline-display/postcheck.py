"""Global idempotency check of the formatting policy after the committed repair."""
import collections,json,re
from pathlib import Path
from prepare import ATTRS,transform
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SNAPSHOT=ROOT/'.local/edb/inline-display-repair-after.jsonl'
def main():
 counts=collections.Counter();remaining=[];retained=collections.Counter();source_exceptions=[];facts=0
 overrides=json.loads((HERE/'overrides.json').read_text()) if (HERE/'overrides.json').exists() else {}
 for row in map(json.loads,SNAPSHOT.open()):
  facts+=1
  if row['a'] not in ATTRS or not isinstance(row['v'],str):continue
  counts[row['a']]+=1
  if '$' not in row['v'] and r'\(' not in row['v']:continue
  after,edits,review=transform(row,overrides)
  if edits:remaining.append({'entity':row['e'],'attribute':row['a'],'t':row['t'],'edits':edits})
  retained.update(o['reason'] for o in review)
  if any(o['reason']=='preexisting-unbalanced-source-math' for o in review):source_exceptions.append({'entity':row['e'],'attribute':row['a'],'occurrences':[o for o in review if o['reason']=='preexisting-unbalanced-source-math']})
 report={'database':'math','basis':json.loads(SNAPSHOT.with_suffix('.manifest.json').read_text())['basis_t'],'facts_scanned':facts,'prose_fields_scanned':dict(counts),'remaining_policy_edits':sum(len(r['edits']) for r in remaining),'remaining_fields':len(remaining),'remaining':remaining,'retained_inline_reasons':dict(retained),'preexisting_source_exceptions':source_exceptions}
 (HERE/'global-post-repair-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('remaining','preexisting_source_exceptions')},indent=2));assert not remaining
if __name__=='__main__':main()
