"""Review current packages on exact post-cleanup source and final survivor objects."""
import copy,json,sys,subprocess,tempfile,shutil,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts'),str(ROOT/'generate/reports/lesson-quality-audit-2026-11-11/normal')]
from cleanup import p,KPS,LOCK,RETIRE,FIX,read,save
from generator_publish import file_lock,prepare_records,normalized_question,enum,jsonable
from scripts.generator_packages import verify_package
from scripts.generator_refill import validate_survivors
from scripts.generator_evidence import batch_sha256,record_sha256
from generate.pipeline.check_delivery import audit
from math_tools import extract,parse,key_value,s
SEED=202611113
summary=[];reps=[];cases=[]
for kp in KPS:
 D=H/str(kp);D.mkdir(exist_ok=True)
 if (D/'source/source.json').exists():
  source=read(D/'source/source.json');K=read(D/'kp.json');inventory=read(D/'inventory/inventory.json')
 else:
  with file_lock(LOCK/f'kp-{kp}.lock'):
   status=p.client.status();basis=status['basis'];K=p.read_kp(kp,D/'inventory',basis);inventory=p.save_inventory(kp,K,status,basis,D/'inventory');source=p.extract_source(kp,D/'source',basis=basis);save(D/'kp.json',jsonable(K))
 assert all(next(q for q in K[':knowledge-point/questions'] if q[':db/id']==eid).get(':question/retired') for eid in RETIRE[kp])
 original_script=source['registered_generator'][':question-generator/script']
 if (D/'reviewed-package.json').exists():
  pkg=read(D/'reviewed-package.json');P=D/'package';script=pkg['registration'];package_hash=pkg['package_sha256'];manifest=pkg['manifest']
 else:
  script=original_script;P=p.config.math_root/Path(script).parent;package_hash=P.name;verify_package(P,package_hash);manifest=read(P/'generator-package.json');save(D/'reviewed-package.json',dict(package_sha256=package_hash,registration=script,manifest=manifest))
 with tempfile.TemporaryDirectory(prefix='normal-cleanup-',dir='/tmp') as tmp:
  T=Path(tmp)
  for name in manifest['files']:
   dst=T/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/name,dst)
  for band in ['easy','moderate','hard']:
   raw=json.loads(subprocess.check_output([sys.executable,str(T/manifest['entrypoint']),'--difficulty',band,'--count','30','--seed',str(SEED)],cwd=T,timeout=120));save(D/'samples'/f'{band}.json',raw)
   repeat=json.loads(subprocess.check_output([sys.executable,str(T/manifest['entrypoint']),'--difficulty',band,'--count','30','--seed',str(SEED)],cwd=T,timeout=120));assert raw==repeat
   out=D/'delivery'/band;delivery=audit(raw,inventory,source,band,out,T,p.config.math_root);accepted=read(out/'accepted.json');assert len(accepted)>=5
   result=validate_survivors(accepted,inventory,out/'native',root=T,manifest=manifest,band=band,python=sys.executable,repo_root=ROOT,environment=p.client.environment);assert result['status']=='passed'
   seen=set();mathrows=[]
   for record in accepted:
    q=record['question'];f,x,y,m,n,b=extract(q);checks=[];values=[]
    for i,field in enumerate(q[':question/answer-fields']):
     if kp==17592186092384:wanted=n
     elif kp==17592186092385:wanted=([s.simplify(-b/n),s.Integer(0)] if '$x$-axis' in q[':question/problem'] else [s.Integer(0),b])[int(field[':answer-field/key'].split('-')[-1])-1]
     else:wanted=({'slope':n,'intercept':b,'coefficient':m,'constant':s.simplify(x+m*y)})[field[':answer-field/key']]
     assert s.simplify(parse(key_value(field))-wanted)==0
     assert wanted.is_Rational;v=s.Rational(wanted)
     checks.extend([dict(field_index=i,submitted=f'({v.p})/({v.q})',expected='accepted',control='equivalent',purpose='Independent differentiation and perpendicular normal construction'),dict(field_index=i,submitted=str(v+1),expected='rejected',control='wrong',purpose='Offset changes the unique slope, equation coefficient, or intercept')]);values.append(str(wanted))
    cases.append(dict(label=f'{kp}-{band}',record=record,checks=checks));mathrows.append(dict(record_sha256=record_sha256(record),function=str(f),point=[str(x),str(y)],tangent=str(m),normal=str(n),intercept=str(b),expected=values))
    family=(record['generation']['template'],record['generation'].get('parameters',{}).get('axis'))
    if family not in seen:reps.append(record);seen.add(family)
   save(D/'independent'/f'{band}.json',dict(passed=True,records=mathrows))
   # Five final exact survivor objects per band; publish these after review.
   save(D/'publish'/f'{band}.json',accepted[:5]);save(D/'verification'/f'{band}.json',accepted)
   summary.append(dict(kp=kp,band=band,sampled=len(raw),surviving=len(accepted),publish_count=5,package_sha256=package_hash,source_sha256=source['source_sha256'],batch_sha256=batch_sha256(accepted),survivor_fingerprints_exclude_all_stored_including_retired=True,independent_math=True,relocated_deterministic=True))
# Include the actual repaired imported solution in both UI states.
K=read(H/'17592186092384/kp.json');q=normalized_question(next(q for q in K[':knowledge-point/questions'] if q[':db/id']==FIX))
for field in q[':question/answer-fields']:field[':answer-field/correct']=[':answer/id',field[':answer-field/correct']]
reps.append(dict(knowledge_point=dict(db_id=17592186092384,id=K[':knowledge-point/id']),question=q))
save(H/'independent-native-input.json',cases);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'independent-native-input.json'),str(H/'independent-native-report.json')],check=True)
save(H/'render-input.json',reps);save(H/'validation.json',dict(passed=True,seed=SEED,checks=summary,native_report='independent-native-report.json',representatives=len(reps),fresh_publish_count=45,database_writes=0));print(json.dumps(summary),flush=True)
