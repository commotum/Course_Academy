"""Run a fresh archived controller per package, so validated code fixes load next."""
from pathlib import Path
import argparse, os, subprocess, sys, json
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--offset',type=int,required=True);p.add_argument('--limit',type=int,required=True);p.add_argument('--extra',type=int,nargs='*',default=[]);a=p.parse_args()
for i in list(range(a.offset,a.offset+a.limit))+a.extra:
    print(json.dumps({'event':'controller_start','offset':i}),flush=True)
    log=ROOT/f'later-repair-run-{i}.log'
    with log.open('w') as f:
        result=subprocess.run([sys.executable,str(ROOT/'run_later_repairs.py'),'--offset',str(i),'--limit','1'],stdout=f,stderr=subprocess.STDOUT)
    print(json.dumps({'event':'controller_complete','offset':i,'exit_code':result.returncode}),flush=True)
