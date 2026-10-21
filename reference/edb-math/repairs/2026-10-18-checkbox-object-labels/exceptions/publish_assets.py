"""Register validated, byte-addressed SVG assets; no database transactions."""
import hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
sys.path.insert(0,str(REPO))
from capture.scripts.database.images import ImageLibrary
from scripts.generator_publish import Publisher

rows=json.loads((HERE/'panel-assets.json').read_text())
report=json.loads((HERE/'panel-render-validation.json').read_text())
assert report['status']=='pass' and report['exact_pixels']==len(rows)==191
math_root=Publisher.from_environment(source=':agent/codex').config.math_root
intent={'operation':'register_self_contained_checkbox_svg_assets','math_root':str(math_root),'assets':rows,'question_database_writes':False,'render_evidence':'panel-render-validation.json','visual_review':'All original raster diagrams and all eight rendered overview pages were visually reviewed. Every viewport contains one complete labeled graph, curve, polygon, region, or digraph, including its axes, endpoints, and arrowheads.'}
intent_path=HERE/'asset-publication-intent.json'
if intent_path.exists():assert json.loads(intent_path.read_text())==intent
else:intent_path.write_text(json.dumps(intent,indent=2)+'\n')
library=ImageLibrary(math_root,HERE/'assets');published=[]
for row in rows:
    raw=Path(row['svg']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['svg_sha256']
    previous=(math_root/row['canonical_path']).exists()
    result=library.store(raw,f'checkbox-panel:{row["question_eid"]}:{row["source_label"]}')
    assert result==row['canonical_path']
    assert (math_root/result).read_bytes()==raw
    published.append({'question_eid':row['question_eid'],'source_label':row['source_label'],'path':result,'sha256':row['svg_sha256'],'bytes':len(raw),'already_present':previous})
receipt={'status':'verified','assets':published,'question_database_writes':False}
(HERE/'asset-publication-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'verified','assets':len(published),'bytes':sum(x['bytes']for x in published),'already_present':sum(x['already_present']for x in published),'question_database_writes':False}))
