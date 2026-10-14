import concurrent.futures,json,subprocess,sys, tempfile, re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
TASKS=[('hard',782),('hard',782),('moderate',784),('moderate',785)]
def run(args):
 result=subprocess.run([sys.executable,str(ROOT)+'.py','--difficulty',args[0],'--seed',str(args[1]),'--format','json'],capture_output=True,text=True,check=True)
 r=json.loads(result.stdout)[0];path=Path(re.search(r'!\[\]\((.*?)\)',r['question'][':question/problem'])[1]);side=json.loads(path.with_suffix('.json').read_text());assert side['geometry']==r['generation']['plot_geometry'];assert path.exists();return r
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:records=list(ex.map(run,TASKS))
assert records[0]['question'][':question/id']==records[1]['question'][':question/id'];assert records[2]['question'][':question/id']!=records[3]['question'][':question/id']
(ROOT/'concurrency-report.json').write_text(json.dumps({'status':'passed','separate_process_calls':4,'identical_parameter_pair':True,'different_parameter_pair':True,'atomic_geometry_sidecars':True},indent=2));print('Concurrent fresh/cached render calls passed')
