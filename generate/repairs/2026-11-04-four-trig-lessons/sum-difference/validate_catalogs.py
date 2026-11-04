#!/usr/bin/env python3
"""Finite-domain, source replay and negative-control regression checks."""
import importlib.util,json,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from validate_repairs import KIDS,AUDIT,audit,check_solution,purpose,semantic,call

def run():
 results=[];failures=[]
 for kid in KIDS:
  folder=BASE/kid;ev=folder/'validation';capacities={}
  for band in ('easy','moderate','hard'):
   r,_=call(kid,band,1,17);capacity=r[0]['generation']['mathematical_capacity'];capacities[band]=capacity
   for count in (0,capacity+1,-1):
    proc=subprocess.run([sys.executable,str(folder/'generator.py'),'--difficulty',band,'--count',str(count),'--seed','17','--format','json'],capture_output=True,text=True)
    good=(proc.returncode==0 and json.loads(proc.stdout)==[]) if count==0 else proc.returncode!=0 and ('supports' in proc.stderr if count>0 else 'nonnegative' in proc.stderr)
    results.append({'kp':kid,'band':band,'count':count,'expected':'empty' if count==0 else 'explicit error','passed':good,'stderr':proc.stderr})
    if not good:failures.append(results[-1])
   if kid in ('17592186059665','17592186059820','17592186059821','17592186059662'):
    records,_=call(kid,band,capacity,17)
    (ev/f'{band}-complete-shift-deck.json').write_text(json.dumps(records,indent=2)+'\n')
    signatures=[semantic(r,kid) for r in records]
    assert len(signatures)==len(set(signatures))
    for i,r in enumerate(records):
     label=f'{band}-complete-shift-deck/{i}';q=r['question']
     n=audit(q,label,kid);s=check_solution(q,label,kid);p=purpose(q,kid,band)
     result={'kp':kid,'label':label,'numeric':n,'solution':s,'purpose_errors':p};results.append(result)
     if n['status']!='match' or n.get('choice_ambiguities') or s.get('suspected_bad_equalities') or s.get('unparsed_equalities') or p:failures.append(result)
  # Original runtime evidence is retained unchanged; source banks are replayed
  # with corrected normalized TeX rather than inferred from new templates.
  source_records=[]
  if kid in ('17592186059665','17592186059666'):
   proc=subprocess.run([sys.executable,str(folder/'generator.py'),'--replay-source'],capture_output=True,text=True)
   assert proc.returncode==0,proc.stderr;source_records=json.loads(proc.stdout)
  elif kid in ('17592186059820','17592186059662'):
   path=folder/('replay-data.json' if kid=='17592186059820' else 'source-cases.json')
   raw=json.loads(path.read_text());ids=list(raw) if isinstance(raw,dict) else [r['source_id'] for r in raw]
   for sid in ids:
    proc=subprocess.run([sys.executable,str(folder/'generator.py'),'--replay' if kid=='17592186059820' else '--source-case',sid],capture_output=True,text=True)
    assert proc.returncode==0,proc.stderr;source_records+=json.loads(proc.stdout)
  (ev/'replayed-source-records.json').write_text(json.dumps(source_records,indent=2)+'\n')
  for i,r in enumerate(source_records):
   q=r['question'];label=f'source-replay/{i}';n=audit(q,label,kid);s=check_solution(q,label,kid)
   result={'kp':kid,'label':label,'numeric':n,'solution':s};results.append(result)
   if n['status']!='match' or n.get('choice_ambiguities') or s.get('suspected_bad_equalities') or s.get('unparsed_equalities'):failures.append(result)
  (ev/'finite-capacities.json').write_text(json.dumps(capacities,indent=2)+'\n')
 # The same purpose checks must reject captured overscaffolding and invented tasks.
 negatives=[]
 for kid,band in [('17592186059665','easy'),('17592186059820','easy'),('17592186059821','hard'),('17592186059662','hard'),('17592186059666','hard')]:
  old=json.loads((AUDIT/'kps'/kid/'samples'/f'{band}-7.json').read_text())[0]
  violations=purpose(old['question'],kid,band)
  result={'kp':kid,'band':band,'violations':violations,'captured_question_id':old['question'][':question/id']};negatives.append(result)
  assert violations,(kid,'negative control failed')
 report={'records_checked':sum('numeric' in r for r in results),'results':results,'negative_controls':negatives,'failures':failures}
 (BASE/'catalog-validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'records_checked':report['records_checked'],'checks':len(results),'negative_controls':len(negatives),'failures':len(failures)}))
 for r in failures[:6]:print(json.dumps(r)[:1600])
 return bool(failures)
if __name__=='__main__':sys.exit(run())
