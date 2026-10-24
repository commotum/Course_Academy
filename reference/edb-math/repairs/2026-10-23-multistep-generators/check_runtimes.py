"""Exercise every repaired registered entrypoint against the exclusion ledger."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys

H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from generator_source_policy import reject_excluded_sources


def check(row):
    policy=json.loads(Path(row['policy_file']).read_text())
    results=[]
    for band in ('easy','moderate','hard'):
        command=[sys.executable,row['entrypoint'],'--difficulty',band,'--count','2','--seed','314159','--format','json']
        try:
            env=os.environ.copy();env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(H/'generated-assets'/str(row['kp']))
            p=subprocess.run(command,capture_output=True,text=True,timeout=45,env=env)
            item={'band':band,'returncode':p.returncode}
            if p.returncode:
                item['error']=p.stderr[-2200:]
            else:
                data=json.loads(p.stdout);records=data.get('instances',[data]) if isinstance(data,dict) else data
                reject_excluded_sources(records,policy['excluded'])
                item['records']=len(records)
                item['templates']=sorted({str(r.get('generation',{}).get('template')) for r in records})
                item['source_refs']=[r.get('generation',{}) for r in records]
            results.append(item)
        except Exception as error:results.append({'band':band,'error':repr(error),'returncode':-1})
    return {'kp':row['kp'],'title':row['title'],'entrypoint':row['entrypoint'],'results':results}


if __name__=='__main__':
    plan=json.loads((H/'installation-plan.json').read_text())
    with ThreadPoolExecutor(max_workers=6) as pool:
        results=list(pool.map(check,plan))
    (H/'runtime-validation.json').write_text(json.dumps(results,indent=2)+'\n')
    for row in results:
        print(row['kp'],[(r['band'],r.get('records',r.get('error','')[-140:])) for r in row['results']])
