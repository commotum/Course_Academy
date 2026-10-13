"""Math typesetting QA only; no sampling or generator mathematics.

The primary .venv uses Python 3.13 without Matplotlib. For this local review,
fall back to the already-cached Python 3.10/Matplotlib wheels read-only. Nothing
is installed, downloaded or written outside this evidence directory and /tmp.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186078582-mpl'
provenance={}
try:
    import matplotlib
except ImportError:
    runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
    if sys.version_info[:2]!=(3,10):
        subprocess.run([str(runtime),str(Path(__file__))],check=True)
        sys.exit(0)
    cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
    for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
        candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
        if not candidates: raise RuntimeError('Missing cached renderer dependency: '+package)
        path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[ -1]
        sys.path.insert(0,str(path));provenance[package]=str(path.resolve())
    import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
records=json.loads((HERE/'render-input.json').read_text())
for level in ('easy','moderate','hard'):
    selected=[]
    for r in records:
        if r['question'][':question/difficulty'].endswith('/'+level) and r['generation']['bank_profile'] not in [x['generation']['bank_profile'] for x in selected]: selected.append(r)
    fig,axes=plt.subplots(1,2,figsize=(18,7))
    for ax,r in zip(axes,selected):
        ax.axis('off');ax.set_title(r['generation']['bank_profile'])
        for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']): ax.text(.02,.90-i*.12,'$'+a[':answer/value']+'$',fontsize=13)
        blocks=[b.rstrip('.,') for b in re.findall(r'\$\$\n(.*?)\n\$\$',r['question'][':question/worked-solution'],re.S) if not re.search(r'[ka]',b.split('=',1)[-1])]
        ax.text(.02,.25,'Worked equations',fontsize=11)
        for i,block in enumerate(blocks): ax.text(.02,.17-i*.1,'$'+block+'$',fontsize=12)
    # Matplotlib's math parser raises on invalid equation TeX.
    fig.canvas.draw();fig.savefig(HERE/('rendered-'+level+'.png'),dpi=120,bbox_inches='tight');plt.close(fig)
(HERE/'render-provenance.json').write_text(json.dumps({'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance},indent=2)+'\n')
