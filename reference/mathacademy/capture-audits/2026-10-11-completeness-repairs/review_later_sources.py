"""Stage source-only reviews without holding the writer lock or replacing imports."""
from pathlib import Path
import argparse,subprocess,sys,json
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('offsets',type=int,nargs='+');a=p.parse_args()
for offset in a.offsets:
    print(json.dumps({'event':'source_review_start','offset':offset}),flush=True)
    with (ROOT/f'later-source-review-{offset}.log').open('w') as log:
        r=subprocess.run([sys.executable,str(ROOT/'run_later_repairs.py'),'--offset',str(offset),'--limit','1','--prepare-only'],stdout=log,stderr=subprocess.STDOUT)
    print(json.dumps({'event':'source_review_complete','offset':offset,'exit_code':r.returncode}),flush=True)
