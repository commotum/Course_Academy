import importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
records=[]
for level,family,points in [('easy','coordinate_ab',[[0,1],[6,6]]),('moderate','coordinate_cd',[[-5,-5],[3,2]]),('hard','graph_read',[[-8,8],[4,-3]]),('hard','graph_read',[[8,-8],[-3,4]])]:
 r=g.generate(level,seed=15,template=family,parameters={'points':points});records.append(r);print(r['generation']['assets'][0]['path'])
(HERE/'boundary-review.json').write_text(json.dumps(records,indent=2)+'\n')
