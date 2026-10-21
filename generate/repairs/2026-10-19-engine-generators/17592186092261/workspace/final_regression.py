"""Small regression after preserving the original key among equivalent blanks."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
import generator as g
E=pathlib.Path('evidence');manifest=json.load(open('package.json'));cases=[]
for qid,spec in g.SPECS.items():
    r=g.generate(spec['level'],seed=17,template=qid,parameters=g.default_params(qid),profile='historical:'+qid)
    f=r['question'][':question/answer-fields'][0];src=g.SOURCES[qid]
    if src.get(':question/answer-fields') and ':answer-field/correct' in src[':question/answer-fields'][0]:
        expected=g.normalize_tex(g.normalized(src[':question/answer-fields'][0][':answer-field/correct'][':answer/value']))
        actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert actual==expected
    cases.append(qid)
expected=json.load(open(E/'samples.json'))
assert [g.generate('easy',seed=18+i) for i in range(5)]==expected
with tempfile.TemporaryDirectory(prefix='course-academy-final-') as temp:
    temp=pathlib.Path(temp)
    for name in manifest['files']:shutil.copyfile(name,temp/name)
    env={**os.environ,'PYTHONPATH':'','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(temp/'outputs')}
    cmd=[sys.executable,str(temp/manifest['entrypoint']),'--difficulty','easy','--seed','18','--count','5','--format','json']
    result=subprocess.run(cmd,cwd=temp,env=env,text=True,capture_output=True,check=True)
    assert json.loads(result.stdout)==expected
(E/'final-regression.json').write_text(json.dumps({'passed':True,'source_designations':cases,'normal_sample_count':5,'relocated_count':5,'generator_sha256':hashlib.sha256(pathlib.Path('generator.py').read_bytes()).hexdigest()},indent=2))
print('Final regression: all 13 source replays/designations; normal and relocated five-record batch pass.')
