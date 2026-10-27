import importlib.util,json,os,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(H/'package'))
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(H/'assets')
spec=importlib.util.spec_from_file_location('triangle_generator',H/'package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
rows=[]
for i,level in enumerate(g.LEVELS):
 rows+=g.generate_batch(level,5,20261027+137*i,H/'assets')
(H/'candidate-pool.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Built',len(rows),'questions:',{level:sum(r['question'][':question/difficulty'].endswith('/'+level) for r in rows) for level in g.LEVELS})
