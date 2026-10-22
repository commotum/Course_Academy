"""Strict acceptance test: a source-supported instance must be generatable.
Run with the job Python. Fails on the currently reviewed density restriction.
Optional first argument selects another repaired entrypoint for regression reuse.
"""
import pathlib,json,subprocess,sys
E=pathlib.Path(__file__).resolve().parent
entry=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else E.parent/'workspace/17592186119771.py'
params={'matrix':[[-2,0,0],[6,-1,0],[0,0,0]],'letter':'A','layout':'bmatrix'}
cmd=[sys.executable,str(entry),'--difficulty','easy','--count','1','--seed','739','--format','json','--parameters',json.dumps(params)]
r=subprocess.run(cmd,text=True,capture_output=True)
(E/'single-witness-acceptance.json').write_text(json.dumps({'source_id':'fe3edf12-af5b-5bb0-b5b3-efb6cd809134','command':cmd,'parameters':params,'expected':'one normal record classified Lower triangular matrix','exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr},indent=2)+'\n')
assert r.returncode==0,'Source-supported canonical matrix rejected; see single-witness-acceptance.json'
records=json.loads(r.stdout);assert len(records)==1
q=records[0]['question'];f=q[':question/answer-fields'][0]
assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])=='Lower triangular matrix'
assert records[0]['generation']['parameters']['matrix']==params['matrix']
print('Canonical single-witness acceptance passed')
