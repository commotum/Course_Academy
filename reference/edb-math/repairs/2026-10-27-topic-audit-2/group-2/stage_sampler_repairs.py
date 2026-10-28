import json,shutil
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];G=json.loads((H/'generators.json').read_text())
for kp,fn,message in[(17592186192794,'sample','No distinct plausible bank for '),(17592186124639,'batch','cannot construct a varied finite batch for ')]:
 g=next(g for g in G if g['kp']==kp);old=Path(g['path']);out=H/'generators'/str(kp);out.mkdir(parents=True,exist_ok=True)
 for p in old.parent.rglob('*'):
  if p.is_file()and'__pycache__'not in p.parts:
   dest=out/p.relative_to(old.parent);dest.parent.mkdir(parents=True,exist_ok=True)
   if dest.exists():dest.chmod(0o644)
   shutil.copy2(p,dest);dest.chmod(0o644)
 s=(out/old.name).read_text();s=s.replace("VERSION = '1.0.3'","VERSION = '1.0.4-bounded-batch-retry'").replace("VERSION='partial-two-variable-package-v3'","VERSION='partial-two-variable-package-v4-bounded-batch-retry'")
 s=s.replace('def '+fn+'(', 'def '+fn+'_once(',1)
 if fn=='sample':params='level,count,seed';passed='level,count,realized_seed';error='RuntimeError'
 else:params='level,count,seed,template=None';passed='level,count,realized_seed,template';error='ValueError'
 wrapper=f'''\n# Reselect the complete deterministic batch stream when earlier incidental\n# rank choices make a later slot impossible. Every original mathematical,\n# source-domain, distinctness and pedagogy guard remains inside {fn}_once.\ndef {fn}({params}):\n    last=None\n    for attempt in range(32):\n        realized_seed=seed if attempt==0 else int(hashlib.sha256((str(seed)+':batch-retry:'+str(attempt)).encode()).hexdigest()[:16],16)\n        try:records={fn}_once({passed})\n        except {error} as error:\n            if not str(error).startswith({message!r}):raise\n            last=error;continue\n        for record in records:\n            record['generation'].update(requested_batch_seed=seed,batch_retry=attempt)\n        return records\n    raise {error}('No complete guarded batch after 32 deterministic streams: '+str(last))\n\n'''
 location=s.index('\ndef main():')if '\ndef main():'in s else s.index("\nif __name__=='__main__':")
 s=s[:location]+wrapper+s[location:];(out/old.name).write_text(s);shutil.copy2(R/'scripts/question_capture/math_format.py',out/'math_format.py')
 evidence={'basis':9122,'kp':kp,'old_reference':g['registration'][':question-generator/script'],'reproducer':{'difficulty':'moderate','count':16 if fn=='sample'else 12,'seed':271028},'change':'Bounded whole-batch deterministic stream retry on only the known schedule/rank dead-end exception. Inner mathematical/domain/distinctness/rank guards unchanged; no per-question key or distractor perturbation.','identity':'Final normalized content already contributes to UUID; version bumped where used; all notation normalization precedes existing hash.','normal_refill_limit':5}
 (out/'repair-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print(kp,out)
