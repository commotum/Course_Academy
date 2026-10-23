"""Read-only global scan of the final immutable export for formula images."""
import collections,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];RAW=ROOT/'.local/edb/math-image-import-audit-2026-10-22';sys.path.insert(0,str(ROOT/'scripts'))
from audit_math_image_imports import IMAGE,svg_kind,capture_index

def main():
 snapshot=RAW/'post-repair-facts.jsonl';assets=json.loads((ROOT/'reference/edb-math/audits/2026-10-22-math-images/assets.json').read_text());refs=collections.defaultdict(list);facts=0;strings=0
 for row in map(json.loads,snapshot.open()):
  facts+=1
  if not isinstance(row['v'],str):continue
  strings+=1
  for m in IMAGE.finditer(row['v']):refs[m[0]].append({'entity':row['e'],'attribute':row['a'],'t':row['t']})
 new=set(refs)-assets.keys();unresolved=[]
 decisions=json.loads((HERE/'post-scan-asset-decisions.json').read_text()) if (HERE/'post-scan-asset-decisions.json').exists() else {}
 for path in sorted(new):
  if path in decisions:assets[path]=decisions[path];continue
  if path.endswith('.svg'):
   kind,reason=svg_kind((Path('/media/jake/SSD/EDB/math')/path).read_text());assets[path]={'kind':kind,'reason':reason}
  else:unresolved.append(path)
 if unresolved:
  evidence=ROOT/'reference/edb-math/audits/2026-10-22-math-images/capture-evidence-files.txt';paths=[Path(p) for p in evidence.read_text().splitlines() if p];linked,stats=capture_index(paths,{Path(p).stem for p in unresolved})
  for path in unresolved:
   proofs=linked.get(Path(path).stem,[]);kind='math-raster' if any(p['kind']=='math-svg' for p in proofs) else 'source-raster' if any(p['tag']=='img' for p in proofs) else 'new-raster-review'
   assets[path]={'kind':kind,'capture_evidence':proofs}
 remaining=[{'path':p,'kind':assets[p]['kind'],'uses':uses} for p,uses in sorted(refs.items()) if assets[p]['kind'] in ('math-svg','math-raster')];unknown=[p for p in refs if assets[p]['kind'] in ('new-raster-review','invalid-svg','mixed-math-graphic')]
 report={'database':'math','basis':json.loads(snapshot.with_suffix('.manifest.json').read_text())['basis_t'],'exported_facts_scanned':facts,'textual_values_scanned':strings,'unique_referenced_image_assets':len(refs),'new_asset_paths_since_audit':len(new),'new_assets':{p:assets[p] for p in sorted(new)},'remaining_formula_image_assets':len(remaining),'remaining_formula_image_occurrences':sum(len(r['uses']) for r in remaining),'remaining':remaining,'unresolved_new_assets':unknown}
 (HERE/'global-post-repair-scan.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('new_assets','remaining')},indent=2));assert not remaining and not unknown
if __name__=='__main__':main()
