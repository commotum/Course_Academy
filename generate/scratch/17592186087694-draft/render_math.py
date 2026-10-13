"""Typeset the exact maximum-length displayed matrices; no new plots."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186087694-draft-mpl'
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
for record in records:
    q=record['question']; problem=q[':question/problem']
    match=re.search(r'\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\1\}',problem)
    assert match
    rows=[[v.strip() for v in row.split('&')] for row in match[2].split(r'\\')]
    nr,nc=len(rows),len(rows[0]);name='row' if nr==1 else 'column'
    fig,ax=plt.subplots(figsize=(10 if nc>1 else 8,8 if nr>1 else 3));ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
    ax.text(.02,.98,'What are the dimensions of the matrix '+('R' if nr==1 else 'C')+'?',fontsize=13,va='top')
    left,right=(.09,.92) if nc>1 else (.43,.57)
    top,bottom=(.70,.48) if nr==1 else (.90,.15)
    for i,row in enumerate(rows):
        for j,value in enumerate(row):
            x=(left+.02)+(right-left-.04)*(j/(nc-1) if nc>1 else .5)
            y=(top+bottom)/2 if nr==1 else top-.02-(top-bottom-.04)*i/(nr-1)
            ax.text(x,y,'$'+value+'$',fontsize=13 if nc>1 else 17,ha='center',va='center')
    for x,dx in [(left-.018,.014),(right+.018,-.014)]:
        ax.plot([x+dx,x,x,x+dx],[top,top,bottom,bottom],color='black',linewidth=1.4)
    ax.text(.02,.09 if nr>1 else .25,'Choices: '+',  '.join(a[':answer/value'].replace(r'\times ',' × ') for a in q[':question/answer-fields'][0][':answer-field/choices']),fontsize=11)
    fig.canvas.draw();fig.savefig(HERE/('maxlength-'+name+'.png'),dpi=120,bbox_inches='tight');plt.close(fig)
(HERE/'render-provenance.json').write_text(json.dumps({'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'dependency_paths':provenance,'input':'render-input.json','role':'Typeset exact displayed maximum-length matrices; not a mathematical plot'},indent=2)+'\n')
