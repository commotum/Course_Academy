#!/usr/bin/env python3
"""Focused fidelity/closure validation for the batch-only construction repair."""
import json,re,os,shutil,subprocess,tempfile,platform
from pathlib import Path
import sympy
import validate as v

def main():
    source=json.loads((v.W.parent/'source/source.json').read_text())
    qs={q.get(':question/math-academy-id'):q for q in source['material']['kp'][':knowledge-point/questions']}
    replay=[];report=[]
    for profile,(values,_) in v.g.EASY_SOURCES.items():
        replay.append(v.g.generate('easy',profile=profile,parameters=dict(zip('abcdef',values))))
    for template in v.g.TEMPLATES:
        replay.append(v.g.generate('moderate',template=template,parameters=v.g.SOURCE_PARAMETERS[template]))
    prose=lambda t:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$','',t,flags=re.S)).strip()
    cases=[]
    for r in replay:
        profile=r['generation']['bank_profile'];q=qs[profile]
        target=v.witness(r);f=r['question'][':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
        made=[v.matrix(a[':answer/value']) for a in f[':answer-field/choices']]
        original=[v.matrix(a[':answer/value']) for a in sf[':answer-field/choices']]
        assert len(made)==len(original)==5 and set(made)==set(original)
        assert v.equations(q[':question/problem'])==v.equations(r['question'][':question/problem'])
        assert v.matrix(sf[':answer-field/correct'][':answer/value'])==target
        assert prose(q[':question/worked-solution'])==prose(r['question'][':question/worked-solution'])
        report.append({'profile':profile,'source_id':q[':question/id'],'matched_choices':5,'matched_distractors':4,'solution_prose':'matched','equations':'matched'})
        cases.append({'label':'source-replay','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if v.matrix(a[':answer/value'])==target else 'rejected','purpose':'source replay checked from visible equations'} for a in f[':answer-field/choices']]})
    v.save('repair-source-records.json',replay);v.save('repair-source-replay.json',report)
    v.save('repair-source-native-input.json',cases)
    run=subprocess.run([str(v.REPO/'generate/runs/current/check-engine'),str(v.E/'repair-source-native-input.json'),str(v.E/'repair-source-native-report.json')],capture_output=True,text=True)
    assert run.returncode==0,run.stdout+run.stderr
    # Irrelevant display order preserves the mathematical response; all choices
    # are also submitted to the real grader in reverse order.
    irrelevant=[]
    for r in json.loads((v.E/'replacement-batch.json').read_text())[:2]:
        clone=json.loads(json.dumps(r));f=clone['question'][':question/answer-fields'][0]
        f[':answer-field/choices'].reverse();assert v.witness(clone)==v.witness(r)
        irrelevant.append({'label':'irrelevant-choice-order','record':clone,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if v.matrix(a[':answer/value'])==v.witness(clone) else 'rejected','purpose':'choice order changes preserve response'} for a in f[':answer-field/choices']]})
    v.save('repair-irrelevant-native-input.json',irrelevant)
    run=subprocess.run([str(v.REPO/'generate/runs/current/check-engine'),str(v.E/'repair-irrelevant-native-input.json'),str(v.E/'repair-irrelevant-native-report.json')],capture_output=True,text=True)
    assert run.returncode==0,run.stdout+run.stderr
    manifest=json.loads((v.W/'package.json').read_text())
    assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':sympy.__version__}}
    assert (v.W/'requirements.txt').read_text().strip()=='sympy=='+sympy.__version__
    assert 'package.json' not in manifest['files']
    args=['--difficulty','easy','--count','5','--seed','2878966680','--format','json']
    original=subprocess.run([v.PY,str(v.W/manifest['entrypoint']),*args],capture_output=True,text=True);assert original.returncode==0,original.stderr
    with tempfile.TemporaryDirectory(prefix='ca-matrix-relocation-') as directory:
        root=Path(directory)
        for relative in manifest['files']:
            assert not Path(relative).is_absolute() and '..' not in Path(relative).parts
            destination=root/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(v.W/relative,destination)
        env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(root/'generated-assets')}
        run=subprocess.run([v.PY,str(root/manifest['entrypoint']),*args],capture_output=True,text=True,cwd=root,env=env)
        assert run.returncode==0,run.stderr
        assert json.loads(original.stdout)==json.loads(run.stdout)
    # Include current moderate candidates in visual review; preserve four easy banks.
    render=json.loads((v.E/'repair-render-records.json').read_text())
    replacements=json.loads((v.E/'inventory-replacement-records.json').read_text())
    for template in v.g.TEMPLATES:
        render.append(next(r for r in replacements if r['generation']['template']==template))
    render.append(json.loads((v.E/'exact-counterfactual-records.json').read_text())[1])
    v.save('repair-render-records.json',render)
    v.save('focused-validation.json',{'status':'passed','source_banks':len(report),'source_choices':5*len(report),'source_distractors':4*len(report),'source_native_checks':30,'irrelevant_order_native_checks':10,'relocation':'passed: exact batch output with manifest files only','dependencies':'exact installed versions matched','render_records':len(render),'scope':'Runtime change confined to batch construction; individual source math, recipes, accepted notation and hard-band support unchanged.'})
    print('Focused validation passed: 6 full banks / 24 distractors; 40 native checks; exact relocation and dependencies; 7 render records')

if __name__=='__main__':main()
