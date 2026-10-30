"""Read the registered immutable successor and exercise its reviewed CLI closure."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R))
from scripts.generator_packages import verify_package
sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw
D=H/'group-1';publication=json.loads((D/'generator-publications.json').read_text())[0];c=json.loads((D/'generator-candidates.json').read_text())[0]
db=connection();b=db.basis();rows=db.query('[:find ?script :in $ ?kp :where [?kp :knowledge-point/question-generator ?g] [?g :question-generator/script ?script]]',[c['kp']],H,'installed-generator-reference',b)
assert rows==[[publication['new_reference']]],rows
entry=Path('/media/jake/SSD/EDB/math')/rows[0][0];verify_package(entry.parent,c['approved_digest'])
def run(path,*args):
 r=subprocess.run([sys.executable,'-B',str(path),*args],env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,check=True);return json.loads(r.stdout)
checks=[]
for sid in ['q-140766','q-141192','q-141343','q-142357','q-141345']:
 actual=run(entry,'--replay',sid);expected=run(Path(c['directory'])/c['entrypoint'],'--replay',sid);assert actual==expected
 f=actual['question'][':question/answer-fields'][0];answers=f[':answer-field/choices'];assert len({a[':answer/id']for a in answers})==len(answers)==5
 assert f[':answer-field/correct'][1]in{a[':answer/id']for a in answers};checks.append(sid)
for band in ['easy']:
 assert run(entry,'--difficulty',band,'--count','11','--seed','291029')==run(Path(c['directory'])/c['entrypoint'],'--difficulty',band,'--count','11','--seed','291029')
unsupported=[]
for band in ['moderate','hard']:
 a=subprocess.run([sys.executable,'-B',str(entry),'--difficulty',band],capture_output=True,text=True)
 assert a.returncode!=0 and 'error:'in a.stderr;unsupported.append(band)
result={'unsupported_bands_rejected':unsupported,'passed':True,'basis_t':b,'kp':c['kp'],'registered_reference':rows[0][0],'digest':c['approved_digest'],'installed_bytes_verified':True,'explicit_replays':checks,'fresh_records_compared':11,'learner_facts_written':False}
(H/'installed-generator-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
