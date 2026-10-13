"""Matplotlib plots from exact instance data, using cached dependencies read-only."""
import json,os,re,sys,subprocess,tempfile,math
from pathlib import Path
HERE=Path(__file__).parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186087721-mpl'
provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates:raise RuntimeError('missing dependency '+package)
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path.resolve())
 import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
records=json.loads((HERE/'review.json').read_text())
fig,axes=plt.subplots(5,4,figsize=(20,15))
for ax,r in zip(axes.flat,records):
 ax.axis('off');q=r['question'];gen=r['generation'];ax.set_title(gen['template']+' '+q[':question/difficulty'].split('/')[-1],fontsize=10)
 formula=q[':question/problem'].split('$$')[1].strip()
 # Normalize only invisible source TeX for Matplotlib's standard math parser.
 formula=formula.replace('⁡','').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin').replace(r'\le ',r'\leq ').replace(r'\le t',r'\leq t')
 ax.text(.02,.85,'$'+formula+'$',fontsize=12)
 ax.text(.02,.55,'$x$: '+', '.join('$'+v+'$' for v in gen['derived']['xs']),fontsize=8)
 ax.text(.02,.32,'$y$: '+', '.join('$'+v+'$' for v in gen['derived']['ys']),fontsize=8)
fig.tight_layout();fig.canvas.draw();fig.savefig(HERE/'math-labels-qa.png',dpi=120);plt.close(fig)
(HERE/'render-provenance.json').write_text(json.dumps({'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance,'math_label_count':len(records)},indent=2)+'\n')
