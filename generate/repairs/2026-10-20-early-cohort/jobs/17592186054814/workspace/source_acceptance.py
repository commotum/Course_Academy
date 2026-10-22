"""Strict regression checks. Exit 1 until both demonstrated source defects are repaired."""
import sys,json,pathlib,traceback
sys.dont_write_bytecode=True
root=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(root))
import generator as g
source=json.load(open('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186054814/source/source.json'))['material']['kp'][':knowledge-point/questions']
failures=[]
try:
 r=g.build({'family':'radical','n':-2})
 assert 'C' in r['question'][':question/worked-solution']
 assert r['generation']['case']=='nonreal'
except Exception as e:failures.append({'test':'source sqrt(-2) must build','parameters':{'family':'radical','n':-2},'error':repr(e),'source':'5356b463-f0e3-5b2b-9ffc-35df47ad119b'})
replayed={r['generation']['source_replay']:r for r in g.replay_sources()}
for q in source:
 try:
  assert q[':question/id'] in replayed, 'supplied source absent from replay'
  r=replayed[q[':question/id']]
  assert [[a[':answer/value'] for a in f[':answer-field/choices']] for f in q[':question/answer-fields']]==[[a[':answer/value'] for a in f[':answer-field/choices']] for f in r['question'][':question/answer-fields']], 'complete bank must replay'
 except Exception as e:failures.append({'test':'all supplied source prompts and banks must replay','source':q[':question/id'],'error':repr(e)})
(root/'source-acceptance-results.json').write_text(json.dumps({'command':str(pathlib.Path(sys.executable))+' -B source_acceptance.py','failures':failures},indent=2))
print(json.dumps(failures));sys.exit(bool(failures))
