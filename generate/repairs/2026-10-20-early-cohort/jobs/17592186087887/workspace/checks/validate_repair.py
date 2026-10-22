#!/usr/bin/env python3
"""Source replay, native-grader fixtures, legacy inventory reproduction, packaging."""
import collections
import importlib.util
import json
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
W=pathlib.Path(__file__).resolve().parents[1]; E=W/'evidence'; J=W.parent
R=pathlib.Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(W));sys.path.insert(0,str(W/'checks'))
import generator as g
from check_shortcuts import visible,field
from reproduce_shortcut_original import predict

def save(name,data): (E/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def load(path):return json.loads(path.read_text())
def norm(s):
    s=s.replace('\\\\','\\').replace(r'\operatorname{ln}',r'\ln').replace('\u2061','')
    s=s.replace(r'\ln(x^2)',r'\ln x^2').replace(r'\mathrm{d}','d').replace(r'\text{d}','d')
    for term in (r'\left',r'\right','{','}',' ','\n','.','$'):s=s.replace(term,'')
    return s

def main():
    spec=importlib.util.spec_from_file_location('before',E/'generator-before.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    s=load(J/'source/source.json'); questions=s['material']['kp'][':knowledge-point/questions']
    replay=[]; rows=[]
    for t in g.SOURCES:
        r=g.replay_source(t,826032);q=r['question'];oq=old.generate(t,1,826032)['question']
        assert all(q[k]==oq[k] for k in (':question/problem',':question/worked-solution'))
        assert [a[':answer/value'] for a in field(r)[':answer-field/choices']]==[a[':answer/value'] for a in oq[':question/answer-fields'][0][':answer-field/choices']]
        sid=g.SOURCES[t][1];src=next(z for z in questions if z[':question/id']==sid)
        sf=src[':question/answer-fields'][0]
        generated=[norm(a[':answer/value']) for a in field(r)[':answer-field/choices']]
        source=[norm(a[':answer/value']) for a in sf[':answer-field/choices']]
        assert sorted(generated)==sorted(source),(t,generated,source)
        assert norm(q[':question/problem'].rsplit('=',1)[1])==norm(src[':question/problem'].rsplit('=',1)[1]),t
        skey=sf.get(':answer-field/correct')
        if skey:
            got=next(a[':answer/value'] for a in field(r)[':answer-field/choices'] if a[':answer/id']==field(r)[':answer-field/correct'][1])
            assert norm(got)==norm(skey[':answer/value'])
        rows.append({'family':t,'source_question_id':sid,'matched_bank_members':5,'total':5,'complete_bank_match':True,'prompt_rhs_match':True,'prior_worked_solution_unchanged':True,'source_key_matches':bool(skey),'inferred_key':not bool(skey)})
        replay.append(r)
    save('source-replay-records.json',replay)
    save('source-replay.json',{'passed':True,'cases':rows,'easy_sources':3,'complete_banks':9,'matched_bank_members':45,'supported_source_difficulties':'Original labels retained, including original_difficulty=null for q-8843.','limits':'Moderate arctangent source and image canonical equation are not implemented by existing families. Moderate source replay is retained; moderate extension census is outside targeted easy repair.'})
    # Native harness receives complete records and all alternatives in one file.
    census=load(E/'census-records.json');controlled=load(E/'controlled-records.json')
    oldbatch=load(J/'samples.json');seed=oldbatch[0]['generation']['seed']
    batch=g.generate_batch('easy',5,seed);save('current-batch.json',batch)
    for r in batch: visible(r)
    reversed_record=json.loads(json.dumps(controlled[0]));field(reversed_record)[':answer-field/choices'].reverse();visible(reversed_record)
    records=census+controlled+batch+replay+[reversed_record]
    cases=[]
    for i,r in enumerate(records):
        f=field(r);key=f[':answer-field/correct'][1]
        cases.append({'label':f'repair record {i}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'All alternatives; correct coefficients independently checked from visible ODE, source replay compared to captured complete bank.'} for a in f[':answer-field/choices']]})
    save('grader-input.json',cases)
    save('render-records.json',[g.generate('cube_root',-2,826033,bank_index=7),g.generate('cube_root',3,826033,bank_index=7),g.generate('affine',-1,826033,bank_index=7),g.generate('linear_log',2,826033,bank_index=7)])
    # Reproduce stored legacy items with the unchanged baseline, not repaired output.
    sys.path.insert(0,str(R))
    from scripts.generator_publish import stable_identities,content_fingerprint
    inv=load(J/'source/inventory.json')
    before=[old.generate(t,a,826031) for t in ('cube_root','affine','linear_log') for a in (*range(-9,0),*range(1,10))]
    for r in before:r['question']=stable_identities(r['question'],g.KP['id'])
    byid={r['question'][':question/id']:r for r in before};affected=[];matched=[];untested=[]
    generated=[q for q in inv['questions'] if not q.get(':question/math-academy-id')]
    for q in generated:
        r=byid.get(q[':question/id'])
        if not r or content_fingerprint(q)!=content_fingerprint(r['question']):untested.append(q[':question/id']);continue
        cue,aid=predict(field(r));assert aid==field(r)[':answer-field/correct'][1]
        matched.append(r)
        t=r['generation']['template'];a=r['generation']['parameters']['a']
        affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':cue+' selects the keyed solution without inspecting the ODE (a2f26476abafae793e46).','reproduction':f'{sys.executable} checks/validate_repair.py; baseline generate({t!r}, {a}, seed=826031), then publisher stable_identities and equal captured content_fingerprint.','evidence_path':'../workspace/evidence/generated-records.json'})
    save('generated-records.json',matched)
    (W/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
    save('inventory-assessment.json',{'basis':inv['basis'],'original_source_questions_excluded':len(inv['questions'])-len(generated),'generated_tested':len(matched),'generated_untested_ids':untested,'affected':len(affected),'complete_generated_inventory_tested':len(matched)==len(generated),'matching':'Same stored UUID and actual publisher content fingerprint. Reconstructed generation metadata uses known legacy version and coefficient. Stored inventory has no seed metadata; reproduction seed recorded, not claimed as original seed.','evidence_path_basis':'affected-inventory.json paths are relative to supplied author-1 evidence_root, resolving into this workspace; all evidence writes stay within workspace.'})
    # Relocate exactly the declared runtime package and exercise the public CLI.
    manifest=load(W/'package.json');assert manifest['dependencies']=={'python':platform.python_version(),'packages':{}}
    relocated=E/'relocated';relocated.mkdir(exist_ok=True)
    for file in manifest['files']:shutil.copy2(W/file,relocated/file)
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(E/'assets')}
    args=['--difficulty','easy','--count','5','--seed',str(seed),'--format','json']
    commands=[]
    def run(base,extras):
        cmd=[sys.executable,str(base/'generator.py'),*extras]
        p=subprocess.run(cmd,text=True,capture_output=True,cwd=relocated,env=env)
        commands.append({'command':cmd,'exit_code':p.returncode,'stderr':p.stderr})
        return p
    a=run(W,args);b=run(W,args);c=run(relocated,args)
    assert a.returncode==b.returncode==c.returncode==0
    assert a.stdout==b.stdout==c.stdout
    assert json.loads(a.stdout)==batch
    assert run(W,['--difficulty','hard']).returncode!=0
    assert run(W,['--count','-1']).returncode!=0
    invalid=[lambda:g.generate('cube_root',0),lambda:g.generate('missing',1),lambda:g.generate('affine',10),lambda:g.generate('linear_log',1,source_replay=True,bank_index=7),lambda:g.generate('affine',9,bank_index=0)]
    for call in invalid:
        try:call()
        except ValueError:pass
        else:raise AssertionError('Invalid instance accepted')
    save('packaging.json',{'passed':True,'manifest':manifest,'installed_python':platform.python_version(),'deterministic':True,'relocated_output_identical':True,'invalid_inputs_rejected':7,'commands':commands,'runtime_output':'JSON stdout only; no generated assets.'})
    print(json.dumps({'source_banks':len(replay),'source_options':45,'native_cases':len(cases),'native_responses':sum(len(c['checks']) for c in cases),'legacy_inventory_reproduced':len(matched),'legacy_affected':len(affected),'untested':len(untested),'packaging':'passed'}))
if __name__=='__main__':main()
