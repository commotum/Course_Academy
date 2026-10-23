"""Matrix coordinates may use comma-separated subscripts. Preserve strict expectations.
Usage: python -B regression_index_notation.py [candidate-records.json]
"""
import json,pathlib,sys,subprocess,re
R=pathlib.Path(__file__).resolve().parent
records=json.load(open(sys.argv[1] if len(sys.argv)>1 else R/'source-replays.json'))
cases=[]
for r in records:
 fs=r['question'][':question/answer-fields']
 if len(fs)!=1 or not fs[0][':answer-field/type'].endswith('/blank'):continue
 f=fs[0];k=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);m=re.fullmatch(r'\{?([a-z])\}?_\{(\d)(\d)\}',k)
 if not m:continue
 b,i,j=m.groups()
 checks=[{'submitted':f'{b}_{{{i},{j}}}','expected':'accepted','purpose':'same row and column, comma-separated matrix index'}, {'submitted':f'{b}_{{{i},{int(j)%4+1}}}','expected':'rejected','purpose':'wrong column remains wrong with comma-separated notation'}]
 cases.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
assert cases,'No symbolic matrix fields tested'
(R/'comma-strict-input.json').write_text(json.dumps(cases,indent=2))
engine='/home/jake/Developer/Course_Academy/generate/runs/current/check-engine'
p=subprocess.run([engine,str(R/'comma-strict-input.json'),str(R/'comma-strict-report.json')],capture_output=True,text=True)
(R/'comma-strict-execution.json').write_text(json.dumps({'command':p.args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr},indent=2));print(p.stderr or p.stdout);sys.exit(p.returncode)
