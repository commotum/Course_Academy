"""Supplement exhaustive normal-domain run with every bounded raw replay."""
import copy,hashlib,importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
counts={}
for t in g.SOURCES:
 counts[t]=0
 for p in g.domain(t,True):
  r=g.generate(g.LEVELS[t],template=t,parameters=p,profile='observed_raw');v.validate_display(r);counts[t]+=1
 print(t,counts[t],'raw parameter sets pass',flush=True)
for params in [dict(A=1.0,k=1),dict(A=True,k=1),dict(A=1,k=1.0)]:
 try:g.generate('moderate',template='q-13461',parameters=params)
 except ValueError:pass
 else:raise AssertionError('noninteger public input')
r=g.generate('hard',template='q-350203');rr=v.rows(r['question'][':question/worked-solution']);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(rr[-2],rr[-2]+'+1',1)
try:v.validate_display(r)
except AssertionError:pass
else:raise AssertionError('endpoint mutation missed')
baseline=json.loads((H/'registered-baseline.json').read_text());actual={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path('generate/scratch/17592186068917.py'),*sorted(Path('generate/scratch/17592186068917').rglob('*'))] if p.is_file()};assert actual==baseline
v.save('supplemental-validation.json',dict(status='passed',full_raw_bounded_domain_valid=counts,strict_json_integer_types=True,endpoint_mutation_detected=True,registered_byte_path_parity=True,script_sha256=hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest()))
