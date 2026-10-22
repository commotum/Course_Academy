"""Independent failing acceptance test for normal count=5 profile reachability.
Run: <job-python> reproduce_profile_omission.py
Writes evidence locally; --assert-coverage exits 1 on the demonstrated defect.
"""
import pathlib,sys,json,subprocess,collections,argparse
W=pathlib.Path(__file__).resolve().parents[1];B=W.parent;parser=argparse.ArgumentParser();parser.add_argument('--assert-coverage',action='store_true');parser.add_argument('--output-dir',default='evidence/profile-omission-after');args=parser.parse_args();E=W/args.output_dir;E.mkdir(parents=True,exist_ok=True);PY=pathlib.Path(sys.executable)
source=json.load(open(B/'source/source.json'))
eligible={q[':question/math-academy-id']:q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions'] if q[':question/difficulty'][':db/ident'].endswith('/moderate')}
results=[];records=[]
for seed in [17,43,101,281,459103,719333]:
 cmd=[str(PY),str(W/'17592186184172.py'),'--difficulty','moderate','--count','5','--seed',str(seed),'--format','json']
 p=subprocess.run(cmd,capture_output=True,text=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':''});assert p.returncode==0,p.stderr
 rows=json.loads(p.stdout);records.extend(rows);results.append({'command':cmd,'seed':seed,'count':len(rows),'profiles':[r['generation']['template'] for r in rows]})
seen={r['generation']['template'] for r in records};missing=sorted(set(eligible)-seen)
report={'requested_difficulty':'moderate','requested_count':5,'runs':results,'eligible_source_profiles':eligible,'observed':sorted(seen),'missing':missing,'acceptance_check':{'requirement':'Normal batches must allow supported source profiles to reach practice across seeds.','passed':not missing},'reported_defective_code_rule':'batch(): keys=sorted(...); for i in range(...): generate(level, seed+i, keys[i%len(keys)]). The sequence starts at i=0 for every seed and stops after 5 unique records.','minimal_counterexample':results[0],'family_wide_change':'Vary profile selection or cycle starting point with seed before truncating to count, so the configured delivery count can reach all supported bank profiles without replacing them.'}
(E/'profile-omission-records.json').write_text(json.dumps(records,indent=2)+'\n');(E/'profile-omission-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'runs':len(results),'observed':sorted(seen),'missing':missing,'coverage_acceptance_passed':not missing}))
if '--assert-coverage' in sys.argv:assert not missing, 'Normal count=5 practice cannot reach: '+', '.join(missing)
