"""Refresh current review plots after renderer-only layout refinements."""
from pathlib import Path
import concurrent.futures,json,subprocess,sys
H=Path(__file__).resolve().parent
records=json.loads((H/'review.json').read_text());paths=sorted({r['generation']['plot']['sidecar'] for r in records})
def render(path):subprocess.run([sys.executable,str(H/'render.py'),path],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(render,paths))
print('Refreshed',len(paths),'exact-instance diagrams.')
