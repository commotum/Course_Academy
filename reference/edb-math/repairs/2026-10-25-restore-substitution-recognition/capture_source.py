from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import sys,json
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import Publisher,loads
p=Publisher.from_environment(source=':agent/codex');cap=json.loads((H/'capture.json').read_text());status=p.client.status()
def capture(row):
 kp=row['kp'];d=H/str(kp);k=loads((d/'capture/kp.edn').read_text())[0][0]
 source=p._source_from_kp(kp,d/'fresh-source',status,cap['basis'],k)
 before=json.loads((d/'source.json').read_text());(d/'source-change.json').write_text(json.dumps({'prior_sha256':before['source_sha256'],'current_sha256':source['source_sha256'],'changed':source['source_sha256']!=before['source_sha256']},indent=2)+'\n')
 return kp
with ThreadPoolExecutor(max_workers=3)as pool:
 for kp in pool.map(capture,cap['knowledge_points']):print(kp,'current source captured',flush=True)
