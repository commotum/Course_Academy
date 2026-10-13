"""Render contact sheets for inspection; use existing cached Matplotlib runtime."""
import json,sys,subprocess,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186172084-mpl'
if sys.version_info[:2]!=(3,10):
 subprocess.run(['/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10',str(Path(__file__))],check=True);sys.exit(0)
example=json.loads(next((HERE/'plots').glob('*.json')).read_text())
for p in example['dependency_paths'].values():sys.path.insert(0,p)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=json.loads((HERE/'review.json').read_text())
if (HERE/'engine-input.json').exists():
 hard=[item['record'] for item in json.loads((HERE/'engine-input.json').read_text()) if item['record']['question'][':question/difficulty'].endswith('/hard')]
 by_task={q['generation']['mathematical_fingerprint']:q for q in hard}
 r['generated']=[q for q in r['generated'] if not q['question'][':question/difficulty'].endswith('/hard')]+list(by_task.values())
for level in ('easy','moderate','hard'):
 records=[(label,q) for label,qs in [('original',r['original_replays']),('generated',r['generated'])] for q in qs if q['question'][':question/difficulty'].endswith('/'+level)]
 cols=4;rows=(len(records)+cols-1)//cols
 fig,axes=plt.subplots(rows,cols,figsize=(12,3*rows))
 for ax in axes.flat:ax.axis('off')
 for ax,(label,q) in zip(axes.flat,records):
  path=q['generation']['plots']['prompt'];ax.imshow(plt.imread(path));ax.set_title(label+' '+q['generation']['bank_profile']+'\n'+str(q['generation']['field']),fontsize=9)
 fig.tight_layout();fig.savefig(HERE/f'inspected-{level}.png',dpi=130);plt.close(fig)
