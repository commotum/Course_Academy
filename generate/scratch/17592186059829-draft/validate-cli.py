"""Final CLI cross-level deduplication and API boundary regression."""
from pathlib import Path
import importlib.util,json,subprocess,sys,hashlib
D=Path(__file__).resolve().parent;S=D.with_suffix('.py');sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('g',S);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
args=[sys.executable,str(S),'--difficulty','all','--seed','13','--count','100','--format','json']
a=json.loads(subprocess.check_output(args,text=True));b=json.loads(subprocess.check_output(args,text=True));assert a==b and len(a)==300
fps=[r['generation']['mathematical_fingerprint'] for r in a];assert len(set(fps))==len(a)
for l in ['easy','moderate','hard']:assert sum(r['question'][':question/difficulty'].endswith('/'+l) for r in a)==100
single=json.loads(subprocess.check_output([sys.executable,str(S),'--difficulty','all','--count','1','--format','json'],text=True));assert len(single)==3
(D/'cli-validation.json').write_text(json.dumps({'generator_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'all_count1_list_length':3,'cross_level_batch_count':300,'cross_level_distinct_mathematical_fingerprints':300,'count_per_level':100,'deterministic_replay':True},indent=2)+'\n')
print('CLI all/count1 returns3; all/count100 returns300 distinct mathematical tasks across levels, deterministic.')
