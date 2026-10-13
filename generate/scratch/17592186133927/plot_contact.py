"""Contact sheet for actual visual inspection, using same Matplotlib runtime."""
import sys,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
if sys.version_info[:2]!=(3,10):
 subprocess.run(['/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10',str(Path(__file__))],check=True);sys.exit(0)
exec((HERE/'render.py').read_text().split('p=json.loads(')[0])
files=[p for p in sorted((HERE/'assets').glob('region*.png')) if json.loads(p.with_suffix('.json').read_text()).get('renderer_version')==2];fig,axes=plt.subplots(5,3,figsize=(15,23))
for ax,file in zip(axes.flat,files):
 p=json.loads(file.with_suffix('.json').read_text());ax.imshow(plt.imread(file));ax.axis('off');ax.set_title(p['parameters']['name']+' a='+str(p['parameters']['a'])+' clearance='+str(round(p['label_clearance_px'],1)))
fig.tight_layout();fig.savefig(HERE/'plot-review.png',dpi=105);plt.close(fig)
