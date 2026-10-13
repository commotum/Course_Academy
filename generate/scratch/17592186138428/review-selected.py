"""Scoped scientific raster QA for the exact selected graph questions."""
import json
import subprocess
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
if sys.version_info[:2]!=(3,10):
    subprocess.run(['/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10',__file__,*sys.argv[1:]],check=True);sys.exit(0)
source=(HERE/'render.py').read_text();exec(compile(source[:source.index('job=json.loads')],str(HERE/'render.py'),'exec'),globals())
from PIL import Image
folder=Path(sys.argv[1]);records=json.loads((folder/'local-generated.json').read_text())
for level in ('easy','moderate','hard'):
    peers=[r for r in records if r['question'][':question/difficulty'].endswith('/'+level)]
    fig,axes=plt.subplots(2,len(peers),figsize=(6.2*len(peers),10.8),squeeze=False)
    for col,r in enumerate(peers):
        for row,role in enumerate(('prompt','solution')):
            axes[row,col].imshow(Image.open(r['generation']['plot_assets'][role]));axes[row,col].axis('off')
            axes[row,col].set_title(level+' '+role+' '+str(col+1))
    fig.tight_layout();fig.savefig(folder/(level+'-review.png'),dpi=100);plt.close(fig)
print('Three selected prompt/solution review sheets rendered.')
