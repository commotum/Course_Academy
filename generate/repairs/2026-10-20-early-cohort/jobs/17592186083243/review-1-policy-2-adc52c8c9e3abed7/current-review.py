from review import *
import subprocess
E=ROOT; B=E.parent; REPO=Path('/home/jake/Developer/Course_Academy'); ENGINE=REPO/'generate/runs/current/check-engine'
def run(cmd,log):
 p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True);save(log,{'command':list(map(str,cmd)),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p.returncode
batch=json.loads((E/'batch.json').read_text())
# Fresh independently selected cases: rational exponent, neighboring target and coefficient boundaries.
params=[dict(a=1,b=1,c=1,u=2),dict(a=2,b=3,c=-1,u=3),dict(a=5,b=2,c=4,u=4),dict(a=1,b=2,c=1,u=6)]
fresh=[g.generate('hard',66081+i,'reciprocal_exp_root_blank',parameters=p) for i,p in enumerate(params)]
easy=[g.generate('easy',80751+i) for i in range(5)]
save('fresh-hard.json',fresh);save('fresh-easy.json',easy)
save('current-math.json',[mathcheck(r) for r in batch+fresh+easy])
# Current source replay comparison against previously independently certified replay, including banks.
prior=json.loads((E/'source-replays.json').read_text());replays=[]
for old in prior:
 m=old['generation']; r=g.generate(old['question'][':question/difficulty'].split('/')[-1],m['seed'],m['template'],parameters=m['parameters'],profile=m['bank_profile'] or 'observed')
 replays.append({'id':old['question'][':question/id'],'identical':old==r})
assert all(x['identical'] for x in replays)
save('current-source-replay.json',replays)
# Retained independent grader suite plus fresh inputs; all checks strict.
cases=json.loads((E/'grader-input.json').read_text())+json.loads((E/'grader-followup-input.json').read_text())
for i,r in enumerate(fresh+batch+easy):
 f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]
 else:
  m=parse(key(r)); v=str(m).replace('**','^')
  checks=[{'submitted':x,'expected':y} for x,y in [(key(r),'accepted'),(v,'accepted'),('('+v+')+1','rejected'),('-('+v+')','rejected')]]
  if i==0:
   checks += [{'submitted':x,'expected':y} for x,y in [
    ('8/(5*sqrt(5)*exp(0.5))','accepted'),
    ('8*exp(1/2)/(5*sqrt(5)*exp(1))','accepted'),
    ('8*exp(-1/4)*exp(-1/4)/(5*sqrt(5))','accepted'),
    ('8/(5*sqrt(5)*exp(3/6))','accepted'),
    ('8/(5*sqrt(5)*exp(2/3))','rejected'),
    ('8*exp(-1/4)/(5*sqrt(5))','rejected')]]
 cases.append({'label':'fresh-'+str(i),'record':r,'checks':checks})
save('current-grader-input.json',cases)
run([ENGINE,E/'current-grader-input.json',E/'current-grader-results.json'],'current-grader-execution.json')
# Replay current CLI batch; normalize only external directory prefix.
run([sys.executable,PKG/'generator.py','--difficulty','easy','--seed','3175644378','--count','5','--format','json'],'cli-current.json')
x=json.loads((E/'cli-current.json').read_text());cli=json.loads(x['stdout'])
def norm(z):return json.dumps(z,sort_keys=True).replace(str(E/'assets'),'<assets>').replace(str(B/'outputs-1'),'<assets>')
save('current-determinism.json',{'cli_equals_actual_batch':norm(cli)==norm(batch),'same_seed_equal':fresh[0]==g.generate('hard',66081,'reciprocal_exp_root_blank',parameters=params[0])})
save('current-runtime.json',{'python':platform.python_version(),'packages':{n:importlib.metadata.version(n) for n in ['sympy','matplotlib','numpy']}})
save('current-render-records.json',batch+fresh[:2])
(E/'session-state.md').write_text('Source and unchanged evidence reused with provenance. Current source replay, fresh math and grading suite, CLI and runtime executed; see current-* reports. Delivery, renderer and final contract audit pending.\n')
print('current tests finished')
