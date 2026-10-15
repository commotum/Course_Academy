"""Exercise every finite explicit input tuple and audit all accepted printed math."""
import sys
sys.dont_write_bytecode=True
import hashlib,importlib.util,itertools,json
from pathlib import Path
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D))
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('partial_enum',D.with_suffix('.py'));audit=module('partial_audit',D/'audit-workload.py')
counts={};all_records=[];by_level={};rejections=[]
for key,f in g.FAMILIES.items():
    total=eligible=0;objects=set();reduced=set();arithmetic_rejections=bank_rejections=0;maxima={}
    for U,V,N,M,A,B in itertools.product(*f['coords'],f['ns'],f['ms'],range(1,5),range(1,5)):
        total+=1;p={'a':A,'b':B,'n':N,'m':M,'U':str(U),'V':str(V),'target':f['target']}
        try:r=g.generate(f['level'],template=key,parameters=p)
        except ValueError as exc:
            if 'Arithmetic workload:' in str(exc):arithmetic_rejections+=1
            elif 'collision' in str(exc):bank_rejections+=1
            else:raise
            rejections.append({'template':key,'parameters':p,'reason':str(exc)});continue
        metrics,obj=audit.audit(r['question'],key);eligible+=1
        objects.add(hashlib.sha256(json.dumps([obj['role_function'],obj['active_coordinate'],str(V)]).encode()).hexdigest())
        reduced.add(hashlib.sha256(json.dumps([obj['restricted_function'],obj['active_coordinate']]).encode()).hexdigest())
        all_records.append(r)
        for name,value in metrics.items():
            numeric=float(g.sym(value));maxima[name]=max(maxima.get(name,0),numeric)
    assert eligible==len(objects)
    counts[key]={'level':f['level'],'candidate_role_tasks':total,'eligible_meaningful_tasks':eligible,'conservative_restricted_function_tasks':len(reduced),'arithmetic_rejections':arithmetic_rejections,'whole_bank_collision_or_zero_rejections':bank_rejections,'all_explicit_tuples_exercised':True,'all_accepted_printed_math_audited':True,'observed_maxima':maxima,'target_aliases_counted':False,'source_bank_aliases_counted':False}
    level=by_level.setdefault(f['level'],{'eligible_role_tasks':0,'conservative_restricted_function_tasks':0});level['eligible_role_tasks']+=eligible;level['conservative_restricted_function_tasks']+=len(reduced)
    print(key,eligible,'/',total,'conservative',len(reduced),flush=True)
report={'method':'Public generate API exercised on every explicit coefficient/exponent/coordinate tuple. Independent parser recovers actual active/held factors, differentiates and evaluates them, checks all coupled bounds and every complete option rational height. Conservative counts additionally collapse identical restricted univariate functions and active points, including unused held exponents at coordinate1. Target letters, seed/order/profile aliases never count.','families':counts,'levels':by_level,'total_eligible_tasks':sum(z['eligible_meaningful_tasks'] for z in counts.values()),'conservative_restricted_function_tasks':sum(z['conservative_restricted_function_tasks'] for z in counts.values()),'all_explicit_candidate_tuples':sum(z['candidate_role_tasks'] for z in counts.values())}
(D/'finite-domain-counts.json').write_text(json.dumps(report,indent=2)+'\n');(D/'workload-accepted-records.json').write_text(json.dumps(all_records,indent=2)+'\n');(D/'workload-rejected-tuples.json').write_text(json.dumps(rejections,indent=2)+'\n')
