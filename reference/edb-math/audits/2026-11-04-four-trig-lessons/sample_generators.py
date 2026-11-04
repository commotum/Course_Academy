"""Read-only CLI probes of every registered generator and difficulty band."""
import concurrent.futures,hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3]
jobs=[(kid,band,seed) for kid in json.loads((H/'kps.json').read_text()) for band in ['easy','moderate','hard'] for seed in [7,31]]
def run(job):
    kid,band,seed=job;folder=H/'kps'/kid/'package';work=H/'kps'/kid/'samples';work.mkdir(exist_ok=True);stem=band+'-'+str(seed)
    argv=[str(ROOT/'.venv/bin/python'),str(folder/'generator.py'),'--difficulty',band,'--count','5','--seed',str(seed),'--format','json']
    try:
        p=subprocess.run(argv,cwd=folder,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,timeout=180)
        (work/(stem+'.stderr')).write_text(p.stderr)
        if p.returncode:return {'kp':kid,'band':band,'seed':seed,'ok':False,'error':p.stderr[-1600:],'exit_code':p.returncode}
        rows=json.loads(p.stdout);(work/(stem+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
        return {'kp':kid,'band':band,'seed':seed,'ok':True,'records':len(rows),'templates':sorted(set(str(r.get('generation',{}).get('template')) for r in rows))}
    except Exception as e:return {'kp':kid,'band':band,'seed':seed,'ok':False,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=[]
    for r in pool.map(run,jobs):
        results.append(r)
        if not r['ok']:print(json.dumps(r),flush=True)
(H/'generator-probes.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'calls':len(results),'failures':sum(not r['ok'] for r in results),'records':sum(r.get('records',0) for r in results)}),flush=True)
