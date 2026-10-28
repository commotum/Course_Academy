import json,subprocess,concurrent.futures,collections
from pathlib import Path
H=Path(__file__).resolve().parent;B=H/'native-baseline';B.mkdir(exist_ok=True);data=json.loads((H/'baseline-grading-input.json').read_text());out=[];fail=[]
def run(items,name):
 inp=B/(name+'-input.json');dest=B/(name+'-output.json');inp.write_text(json.dumps(items));p=subprocess.run([str(H.parent/'check-engine'),str(inp),str(dest)],capture_output=True,text=True)
 if p.returncode==0:return {'passed':True,'name':name,'items':len(items),'result':json.loads(dest.read_text())}
 (B/(name+'.stderr')).write_text(p.stderr)
 if len(items)==1:return {'passed':False,'name':name,'question':items[0]['label'],'error':p.stderr.strip(),'record':items[0]}
 mid=len(items)//2;return [run(items[:mid],name+'a'),run(items[mid:],name+'b')]
def collect(result):
 if isinstance(result,list):
  for r in result:collect(r)
 elif result['passed']:out.append(result)
 else:fail.append(result)
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:
 jobs=[pool.submit(run,data[i:i+100],str(i//100))for i in range(0,len(data),100)]
 for future in jobs:collect(future.result())
report={'questions':len(data),'passed_questions':sum(r['items']for r in out),'failed_questions':len(fail),'failures':fail,'passed_batches':out,'database_writes':0};(H/'baseline-native-verification.json').write_text(json.dumps(report,indent=2)+'\n');(H/'native-failures.json').write_text(json.dumps(fail,indent=2)+'\n');print('passed',report['passed_questions'],'failed',len(fail));print([(r['question'],r['error'][:180])for r in fail])
