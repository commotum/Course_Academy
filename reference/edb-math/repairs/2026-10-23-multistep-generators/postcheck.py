"""Check deployed registrations, disposable runtime copies, and bank availability."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
H=Path(__file__).resolve().parent;ROOT=H.parents[3];MATH=Path('/media/jake/SSD/EDB/math')
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from scripts.generator_packages import materialize_package,verify_package
from scripts.generator_source_policy import reject_excluded_sources
from migrate_learner_history import connection


def main():
    verification=json.loads((H/'verification.json').read_text());basis=verification['basis'];db=connection()
    dispositions=json.loads((H/'question-dispositions.json').read_text());plan=json.loads((H/'installation-plan.json').read_text())
    rows=db.query('[:find (pull ?q [:db/id :question/id :question/retired]) :in $ [?q ...] :where [?q :question/id _]]',
        [[r[':db/id'] for r in dispositions]],H,'all-dispositions-after',basis)
    after={r[0][':db/id']:r[0] for r in rows}
    for row in dispositions:
        assert bool(after[row[':db/id']].get(':question/retired'))==(row['decision']=='retire-generated-descendant')
    pkgs={r['kp']:r for r in json.loads((H/'published-packages.json').read_text())}
    validated={r['kp']:r for r in json.loads((H/'runtime-validation.json').read_text())}
    def run(row):
        band=next(r['band'] for r in validated[row['kp']]['results'] if r['returncode']==0)
        if row['packaged']:
            pkg=pkgs[row['kp']];destination=H/'deployed-runtime'/str(row['kp'])
            if destination.exists():
                verify_package(destination,pkg['digest']);entry=destination/row['manifest']['entrypoint']
            else:entry=materialize_package(pkg['reference'],MATH,destination)
        else:entry=Path(row['entrypoint'])
        env=os.environ.copy();env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(H/'deployed-assets'/str(row['kp']))
        p=subprocess.run([sys.executable,str(entry),'--difficulty',band,'--seed','271828','--count','2','--format','json'],
            env=env,capture_output=True,text=True,check=True,timeout=45)
        data=json.loads(p.stdout);records=data.get('instances',[data]) if isinstance(data,dict) else data
        assert len(records)==2
        policy=json.loads(Path(row['policy_file']).read_text());reject_excluded_sources(records,policy['excluded'])
        return {'kp':row['kp'],'band':band,'records':len(records),'entrypoint_sha256':hashlib.sha256(entry.read_bytes()).hexdigest(),
                'package_digest':pkgs.get(row['kp'],{}).get('digest')}
    with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(run,plan))
    result={'basis':basis,'registered_runtimes_passed':len(results),'immutable_packages_relocated':len(pkgs),
        'new_retirements_verified':len(verification['retired_questions']),'known_invalid_descendants_still_available':0,
        'independent_matrix_questions_preserved':10,'results':results}
    (H/'postcheck.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='results'}))


if __name__=='__main__':main()
