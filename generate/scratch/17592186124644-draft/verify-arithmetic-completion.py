"""Final exhaustive accepted-domain mathematics/native checks and targeted defaults."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import validate as v
records=json.loads((D/'workload-accepted-records.json').read_text())
for r in records:v.check(r['question']);v.audit_module.audit(r['question'],r['generation']['template'])
native=v.native([(r['generation']['template']+'-'+str(i),r) for i,r in enumerate(records)],'exhaustive-domain-native')
signs=set()
for seed in range(150):
    r=v.g.generate_easy(seed);fun,target,point=v.tm.prompt(r['question'][':question/problem']);signs.add(int(v.S.sign(point[target])))
assert signs=={-1,1}
regressions=[('power-log-root',{'a':2,'b':4,'n':4,'U':9,'V':'e**2'}),('power-log-root',{'a':3,'b':3,'n':4,'U':9,'V':'e'}),('root-reciprocal',{'a':4,'b':3,'n':3,'U':4,'V':1}),('log-power-exp',{'a':1,'b':2,'n':5,'U':1,'V':'ln(5)'})]
for key,p in regressions:v.must_fail(lambda key=key,p=p:v.g.generate(v.g.FAMILIES[key]['level'],template=key,parameters=p),'oversized arithmetic '+key)
# The signed easy review explicitly contains both signs, using already
# validated instances of both signs from the full48-seed family run.
review=json.loads((D/'review.json').read_text());easy=[i for i,z in enumerate(review) if z['level']=='easy'];assert len(easy)==2
samples=json.loads((D/'samples.json').read_text());chosen=[];seen_signs=set()
for r in samples:
    if r['generation']['template']!='easy-polynomial':continue
    sign=int(v.S.sign(v.g.sym(r['generation']['parameters']['U'])))
    if sign not in seen_signs:chosen.append(r);seen_signs.add(sign)
assert len(chosen)==2
for index,r in zip(easy,chosen):review[index]['record']=r
(D/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
report=json.loads((D/'validation.json').read_text());updated={}
for key,value in report.items():
    updated[key]=value
    if key=='default_family_coverage':updated['default_easy_active_sign_coverage']=sorted(signs)
(D/'validation.json').write_text(json.dumps(updated,indent=2,ensure_ascii=False)+'\n')
result={'unique_finite_domain_records':len(records),'independently_parsed_math_checks':v.COUNTS,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'default_easy_active_coordinate_signs':sorted(signs),'default_seeds_checked':150,'oversized_regression_cases':regressions,'all_root_regressions_rejected':True,'numeric_baseline':v.baseline()}
(D/'arithmetic-exhaustive-report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
