"""Read-only saved-seed sampling and real offline publication filtering."""
import argparse,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT)]
from generate.pipeline.check_delivery import audit
p=argparse.ArgumentParser();p.add_argument('kp',type=int);ns=p.parse_args();d=H/str(ns.kp);kp=json.loads((d/'inventory/kp.json').read_text());script=Path('/media/jake/SSD/EDB/math')/kp[':knowledge-point/question-generator'][':question-generator/script'];source=json.loads((d/'source/source.json').read_text());inventory=json.loads((d/'inventory/inventory.json').read_text());results=[]
seeds=[20261111,47] if ns.kp!=17592186235285 else [81]
count=4 if ns.kp!=17592186235285 else 2
for band in ['easy','moderate','hard']:
 for seed in seeds:
  out=d/'samples'/band/str(seed);out.mkdir(parents=True,exist_ok=True);assets=out/'assets';assets.mkdir(exist_ok=True)
  env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets.resolve()),'MPLCONFIGDIR':str((out/'mpl').resolve())}
  command=[sys.executable,str(script),'--difficulty',band,'--count',str(count),'--seed',str(seed),'--format','json'];run=subprocess.run(command,env=env,capture_output=True,text=True,timeout=180)
  (out/'stderr.txt').write_text(run.stderr);(out/'command.json').write_text(json.dumps(command,indent=2)+'\n')
  if run.returncode:
   results.append(dict(band=band,seed=seed,status='generation-failed',returncode=run.returncode,stderr=run.stderr[-3000:]));continue
  records=json.loads(run.stdout);(out/'records.json').write_text(json.dumps(records,indent=2)+'\n')
  result=audit(records,inventory,source,band,out/'delivery',assets,Path('/media/jake/SSD/EDB/math'));results.append(dict(band=band,seed=seed,status='sampled',records=len(records),survivors=result['accepted_count']));print(ns.kp,results[-1],flush=True)
(d/'sample-summary.json').write_text(json.dumps(results,indent=2)+'\n')
