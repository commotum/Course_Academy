"""Typesetting QA from actual printed arrays, not a parameter-generated diagram.

Use cached read-only Python3.10/Matplotlib fallback; never install dependencies.
The prompt itself remains TeX. This explicit fixed-width cell-layout inspection
checks maximum width/height legibility and does not claim browser-engine parity.
"""
import json,os,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186087693-draft-mpl'
provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__))],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates:raise RuntimeError('Missing cached renderer dependency: '+package)
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path.resolve())
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# Generation is in primary runtime with the exact version recorded by records.
payload=subprocess.run([str(HERE.parents[2]/'.venv/bin/python'),'-c',"import importlib.util,json; p='generate/scratch/17592186087693-draft.py'; s=importlib.util.spec_from_file_location('g',p);g=importlib.util.module_from_spec(s);s.loader.exec_module(g); print(json.dumps([g.generate(level,parameters={'name':'A','entries':[[str((i*3+j)%19-9) for j in range(c)] for i in range(r)]},field_type='radio') for level,r,c in [('moderate',2,12),('moderate',12,2),('hard',12,12)]]))"],capture_output=True,text=True,check=True)
records=json.loads(payload.stdout)
fig,axes=plt.subplots(1,3,figsize=(16.5,7.7),dpi=110)
for ax,rec in zip(axes,records):
 prompt=rec['question'][':question/problem']
 array=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',prompt,re.S)[1]
 rows=[[v.strip() for v in row.split('&')] for row in array.split(r'\\')];r,c=len(rows),len(rows[0])
 ax.set_xlim(0,14);ax.set_ylim(-7,14);ax.axis('off')
 ax.set_title(f"Authored {rec['generation']['level']}: {r} by {c}",fontsize=13)
 ax.text(0,13.1,'What are the dimensions of matrix A?',fontsize=11)
 for i,row in enumerate(rows):
  for j,cell in enumerate(row):ax.text(1+j,11.8-i*.8,'$'+cell+'$',fontsize=15,ha='center',va='center')
 left=.35;right=c+.65;top=12.25;bottom=11.35-(r-1)*.8
 for x,sign in ((left,1),(right,-1)):
  ax.plot([x+sign*.25,x,x,x+sign*.25],[top,top,bottom,bottom],color='black',lw=1)
 y=-.6
 for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']:
  ax.text(0,y,'$'+a[':answer/value']+'$',fontsize=13);y-=.8
 ax.text(0,-5.5,f'{r} rows, {c} columns; dimensions {r} × {c}.',fontsize=11)
fig.tight_layout();fig.canvas.draw();fig.savefig(HERE/'render-qa.png');plt.close(fig)
(HERE/'render-provenance.json').write_text(json.dumps({'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'dependency_paths':provenance,'artifact':'render-qa.png','actual_prompt_arrays_read_back':True,'cell_font_points':15,'method':'Fixed-width numerical cell typesetting inspection; not browser TeX parity','checked_shapes':[[2,12],[12,2],[12,12]]},indent=2)+'\n')
