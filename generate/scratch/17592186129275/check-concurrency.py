"""Fresh same/different geometry concurrent rendering; no cache pruning."""
import importlib.util,pathlib,tempfile,shutil,concurrent.futures,json,hashlib
B=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('g',B.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
run=pathlib.Path(tempfile.mkdtemp(prefix='fresh-',dir=B));shutil.copy2(B/'render.py',run/'render.py');g.HERE=run
calls=[({'axis':'x','sign':1,'part':'lower'},g.sp.Rational(3,2)),({'axis':'x','sign':1,'part':'lower'},g.sp.Rational(3,2)),({'axis':'y','sign':1,'part':'left'},g.sp.Rational(5,2))]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda p:g.render_plots(*p),calls))
assert results[0]==results[1] and results[0]!=results[2]
checks=[]
for (c,v),paths in zip(calls,results):
 for path in paths:
  side=json.loads(pathlib.Path(path).with_suffix('.json').read_text());geometry=side['geometry'];assert geometry['a']==float(v) and geometry['axis']==c['axis'] and geometry['sign']==c['sign'] and geometry['part']==c['part'];assert pathlib.Path(path).stat().st_size>1000
  checks.append({'path':path,'sha256':hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest(),'geometry':geometry})
assert not list((run/'plots').glob('input-*.json'))
(B/'concurrency-report.json').write_text(json.dumps({'status':'pass','fresh_calls':3,'same_geometry_determinism':True,'different_geometry_isolation':True,'files':checks},indent=2)+'\n')
print('Fresh concurrent geometry: pass (3 calls, same and different parameters)')
