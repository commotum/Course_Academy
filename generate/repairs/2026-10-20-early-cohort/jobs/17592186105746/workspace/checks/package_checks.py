"""Exercise the declared runtime in isolation, deterministic CLI and boundaries."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from repair_checks import ROOT, E, g, independent, save


def main():
    manifest = json.loads((ROOT/'package.json').read_text())
    assert manifest['dependencies'] == {'python': sys.version.split()[0], 'packages': {'sympy': g.sp.__version__}}
    assert set(manifest['files']) == {'17592186105746.py', '17592186105746/source.json', 'math_format.py', 'requirements.txt'}
    assert 'package.json' not in manifest['files']
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE':'1', 'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(E/'assets')}
    commands = []; relocated_records = []
    with tempfile.TemporaryDirectory(prefix='ca-repair-relocated-') as dest:
        isolated = Path(dest)
        for name in manifest['files']:
            target = isolated/name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/name, target)
        for difficulty in ['easy','moderate']:
            cmd = [sys.executable,str(isolated/manifest['entrypoint']),'--difficulty',difficulty,'--count','5','--seed','7331','--format','json']
            a = subprocess.run(cmd,cwd=isolated,env=env,capture_output=True,text=True,check=True)
            b = subprocess.run(cmd,cwd=isolated,env=env,capture_output=True,text=True,check=True)
            assert a.stdout == b.stdout
            rs = json.loads(a.stdout); assert len(rs)==5
            assert rs == g.batch(difficulty,5,7331)
            for r in rs: independent(r)
            relocated_records.extend(rs)
            commands.append({'command':cmd,'passed':True,'deterministic':True,'records':len(rs)})
        invalid = []
        for args in [['--difficulty','hard'],['--count','0'],['--count','-1']]:
            result = subprocess.run([sys.executable,str(isolated/manifest['entrypoint']),*args],cwd=isolated,env=env,capture_output=True,text=True)
            assert result.returncode != 0
            invalid.append({'arguments':args,'rejected':True})
        runtime_after = sorted(str(p.relative_to(isolated)) for p in isolated.rglob('*') if p.is_file())
        assert runtime_after == sorted(manifest['files'])
    parameter_invalid = []
    for p in [{'rhs_scale':0},{'rhs_scale':5},{'intercept':33},{'intercept':'1/2'},{'residual':33},{'residual':'1/2'},{'second_rhs':1,'residual':1},{'unknown':1}]:
        try: g.generate('easy',7331,'q-42157',p)
        except ValueError: parameter_invalid.append({'parameters':p,'rejected':True})
        else: raise AssertionError(('Invalid parameter accepted',p))
    save('relocated-records.json',relocated_records)
    save('packaging-results.json',{'passed':True,'declared_runtime_only':True,'commands':commands,'no_generated_files_in_runtime':True,'cli_invalid':invalid,'parameter_invalid':parameter_invalid,'python':sys.version.split()[0],'sympy':g.sp.__version__,'no_runtime_service_or_database_access':True})
    # Native grading for the actual five delivered records plus two controlled
    # delivered cases, using independent parsed-math expectations after filtering.
    delivered = json.loads((E/'delivery-batch/accepted.json').read_text()) + json.loads((E/'delivery/accepted.json').read_text())[:2]
    grade = []
    for r in delivered:
        c = independent(r); options=r['question'][':question/answer-fields'][0][':answer-field/choices']
        grade.append({'label':'delivered '+r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==c['valid_index'] else 'rejected','purpose':'independent post-delivery bank'} for i,a in enumerate(options)]})
    save('grader-delivered-input.json',grade)
    print(json.dumps({'passed':True,'relocated_records':len(relocated_records),'invalid_inputs_rejected':len(invalid)+len(parameter_invalid),'delivered_grader_records':len(grade)}))

if __name__=='__main__':main()
