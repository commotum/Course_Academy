"""Explicit arithmetic-boundary and all-primitive-trig workload probes."""
import sys
sys.dont_write_bytecode=True
import runpy,json,subprocess,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;m=runpy.run_path(str(D/'validate.py'),run_name='boundary-helper');g=m['g'];records=[];raw_values=0
for case in m['CASES']:
 p={k:4 if k=='n' else 7 if k=='b' else 6 for k in case['parameters']};r=g.generate('easy',template=case['template'],parameters=p);m['readback'](r);records.append(r)
 raw_values+=m['raw_bank_readback'](g.generate('easy',template=case['template'],parameters=p,profile='observed_raw'))
for level in ('moderate','hard'):
 for trig in g.TRIG:
  for sign in (-1,1):
   p={'a':sign*4,'b':-sign*4,'n':2 if sign<0 else 4,'trig':trig}
   if level=='hard':p['d']=sign*4
   r=g.generate(level,parameters=p,field_type='blank' if sign<0 else 'radio');m['readback'](r);records.append(r)
entries=[m['engine_entry'](r,'explicit boundary '+str(i)) for i,r in enumerate(records)];(D/'boundary-engine-input.json').write_text(json.dumps(entries,indent=2)+'\n');native=m['verify_native']();subprocess.run([native,str(D/'boundary-engine-input.json'),str(D/'boundary-engine-report.json')],check=True)
assert m['baseline']()==json.loads((D/'registered-baseline.json').read_text())['files']
result={'pass':True,'records':len(records),'raw_boundary_bank_values_read_back':raw_values,'generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'parameters':[{'level':r['question'][':question/difficulty'],'template':r['generation']['template'],'parameters':r['generation']['parameters']} for r in records],'native':json.loads((D/'boundary-engine-report.json').read_text()),'registered_baseline_unchanged':True};(D/'boundary-validation.json').write_text(json.dumps(result,indent=2)+'\n');print('Boundary records',len(records),'pass')
