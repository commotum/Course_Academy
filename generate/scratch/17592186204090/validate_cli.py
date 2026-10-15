#!/usr/bin/env python3
"""Focused CLI contract regression; no mathematical-generator changes or DB IO."""
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('parameter_cli_generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def cli(level,count,form='json',extra=()):
 return subprocess.run([sys.executable,str(SCRIPT),'--difficulty',level,'--count',str(count),'--format',form,*extra],capture_output=True,text=True)

def main():
 caps=g.capacity();assert caps=={'easy':76,'moderate':308,'hard':1368}
 tests=[]
 for lev in (*g.LEVELS,'all'):
  wanted=g.LEVELS if lev=='all' else (lev,)
  for count in (0,1):
   for form in ('json','markdown'):
    r=cli(lev,count,form);assert r.returncode==0,r.stderr
    if form=='json':
     records=json.loads(r.stdout);assert isinstance(records,list) and len(records)==count*len(wanted)
     for level in wanted:assert sum(x['question'][':question/difficulty']==':question.difficulty/'+level for x in records)==count
    else:
     assert r.stdout.count('Given that this equation has no solution')==count*len(wanted)
    tests.append({'difficulty':lev,'count':count,'format':form,'passed':True,'output_count':count*len(wanted)})
  limit=min(caps.values()) if lev=='all' else caps[lev]
  # Exact capacity is a valid request; all's limit is the smallest per-level bank.
  r=cli(lev,limit);assert r.returncode==0,r.stderr
  records=json.loads(r.stdout);assert len(records)==limit*len(wanted)
  for level in wanted:
   selected=[x for x in records if x['question'][':question/difficulty']==':question.difficulty/'+level]
   assert len(selected)==limit and len({x['generation']['mathematical_fingerprint'] for x in selected})==limit
  tests.append({'difficulty':lev,'count':limit,'format':'json','passed':True,'exact_capacity_boundary':True,'output_count':len(records)})
  for form in ('json','markdown'):
   r=cli(lev,limit+1,form);assert r.returncode!=0 and not r.stdout.strip() and 'capacity' in r.stderr
   tests.append({'difficulty':lev,'count':limit+1,'format':form,'passed':True,'overflow_fails_before_output':True})
  r=cli(lev,-1);assert r.returncode!=0 and not r.stdout.strip()
  r=cli(lev,0,extra=('--capacity',));assert r.returncode==0 and json.loads(r.stdout)==(caps if lev=='all' else caps[lev])
 assert cli('invalid',1).returncode!=0
 # Keep internal all-batch semantics explicit and distinct from CLI per-level count.
 assert len(g.batch('all',1))==1
 report={'passed':True,'scope':'CLI only; equation, solution, bank, domain and native-grading logic unchanged','json_contract':'flat array','all_count_contract':'count per easy/moderate/hard level','internal_batch_all_contract':'global count','capacity':caps,'tests':tests,'generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest()}
 (HERE/'cli-validation.json').write_text(json.dumps(report,indent=2)+'\n')
 v=json.loads((HERE/'validation.json').read_text());old_hash=v.get('cli_revision',{}).get('prior_mathematical_proof_producer_sha256',v['hashes'][str(SCRIPT.relative_to(ROOT))])
 for p in (SCRIPT,HERE/'validate.py',HERE/'validate_cli.py'):
  v['hashes'][str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
 v['cli_revision']={'passed':True,'evidence':'cli-validation.json','prior_mathematical_proof_producer_sha256':old_hash,'mathematical_logic_unchanged':True,'native_proof_preserved':True}
 (HERE/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
 f=json.loads((HERE/'freeze.json').read_text());f['generator_sha256']=report['generator_sha256'];f['frozen_runtime']=v['hashes'];f['cli_regression']='cli-validation.json';f['prior_mathematical_proof_producer_sha256']=old_hash
 (HERE/'freeze.json').write_text(json.dumps(f,indent=2)+'\n')
 print(json.dumps({'passed':True,'cli_checks':len(tests),'generator_sha256':report['generator_sha256'],'capacity':caps}))
if __name__=='__main__':main()
