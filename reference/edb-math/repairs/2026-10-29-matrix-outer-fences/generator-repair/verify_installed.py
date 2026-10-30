"""Read live registrations and probe the installed immutable CLI entrypoints."""
import concurrent.futures,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path[:0]=[str(R),str(R/'scripts')]
from generator_publish import validate_question
from migrate_learner_history import connection
from scripts.generator_packages import verify_package
ps=json.loads((H/'generator-publications.json').read_text());cs={c['kp']:c for c in json.loads((H/'generator-candidates.json').read_text())};db=connection();basis=db.basis()
rows=db.query('[:find ?kp ?script :in $ [?kp ...] :where [?kp :knowledge-point/question-generator ?g] [?g :question-generator/script ?script]]',[[p['kp']for p in ps]],H,'installed-registrations',basis)
assert dict(rows)=={p['kp']:p['new_reference']for p in ps}
for p in ps:verify_package((Path('/media/jake/SSD/EDB/math')/p['new_reference']).parent,p['digest'])
def run(pair):
 p,band=pair;d=H/'installed-probes'/f"{p['kp']}-{band}";d.mkdir(parents=True,exist_ok=True);env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(d.resolve()),'TMPDIR':str(d.resolve())}
 args=[sys.executable,str(Path('/media/jake/SSD/EDB/math')/p['new_reference']),'--difficulty',band,'--count','3','--seed','29102977','--format','json']
 result=subprocess.run(args,env=env,capture_output=True,text=True,timeout=100);(d/'stdout.json').write_text(result.stdout);(d/'stderr.txt').write_text(result.stderr);result.check_returncode();rs=json.loads(result.stdout);rs=rs.get('records',[])if isinstance(rs,dict)else rs
 assert rs==json.loads((H/f"verified-{p['kp']}-{band}.json").read_text()),'Installed output changed'
 for record in rs:validate_question(record['question'])
 return{'kp':p['kp'],'band':band,'records':len(rs),'matches_reviewed_relocated_outputs':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:checks=list(pool.map(run,[(p,b)for p in ps for b in cs[p['kp']]['supported_difficulties']]))
report={'passed':True,'registration_readback_basis':basis,'registered_replacements':len(ps),'immutable_packages_verified':len(ps),'records':sum(c['records']for c in checks),'checks':checks,'database_writes':0};(H/'installed-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('Verified',len(ps),'live registrations and installed immutable packages;',report['records'],'normal CLI records match reviewed outputs')
