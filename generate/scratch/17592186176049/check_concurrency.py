"""Fresh concurrent shared fixed-graph writes; stable question identities."""
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
code='''import importlib.util,json,sys
s=importlib.util.spec_from_file_location('g',sys.argv[1]);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
g.graph(force=True)
r=g.generate('hard',int(sys.argv[2]),template='two_identity_properties',parameters=json.loads(sys.argv[3]))
print(json.dumps({'question_id':r['question'][':question/id'],'content':r['generation']['content_identity'],'parameters':r['generation']['parameters']}))'''
a={'integer_coefficient':'1','denominator':6,'gap':'1','property':'asym','index':1}
b={'integer_coefficient':'1/2','denominator':3,'gap':'2','property':'range','index':0}
def run(arg):
 r=subprocess.run([str(HERE.parents[2]/'.venv/bin/python'),'-c',code,str(HERE.with_suffix('.py')),str(arg[0]),json.dumps(arg[1])],capture_output=True,text=True,check=True);return json.loads(r.stdout)
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,[(0,a),(20,a),(0,b),(20,b)]))
assert results[0]['question_id']==results[1]['question_id'];assert results[2]['question_id']==results[3]['question_id'];assert results[0]['question_id']!=results[2]['question_id']
meta=json.loads((HERE/'tangent.json').read_text());assert hashlib.sha256((HERE/'tangent.png').read_bytes()).hexdigest()==meta['sha256']
assert not list(HERE.glob('tmp*.png')) and not list(HERE.glob('tmp*.json'))
(HERE/'concurrency.json').write_text(json.dumps({'passed':True,'fresh_parallel_renders':4,'fixed_graph_geometry_for_all_parameters':True,'records':results,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()},indent=2)+'\n')
print('4 concurrent fresh renders and identical/different question identities passed')
