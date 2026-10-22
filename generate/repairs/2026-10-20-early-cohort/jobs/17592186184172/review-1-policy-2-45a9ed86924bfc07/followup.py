# Reuse only our own independent parser. No author test oracle.
ns={'__file__':str(__import__('pathlib').Path('audit.py').resolve())};exec(compile(open('audit.py').read().split('source=json.load')[0],'audit.py','exec'),ns)
g=ns['g'];parse=ns['parse'];save=ns['save'];native=ns['native'];E=ns['E'];B=ns['B'];W=ns['W'];run=ns['run'];PY=ns['PY']
import json,copy,pathlib,sys,subprocess,hashlib,collections
source=json.load(open(B/'source/source.json'));src={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
# Explicitly cover every source-bank outcome independently of author's allowed_truths.
covered=[];coverage=[]
for r in json.load(open('replay-records.json')):
 key=r['generation']['template'];fs=r['question'][':question/answer-fields'];p=copy.deepcopy(r['generation']['parameters']);level=r['question'][':question/difficulty'].split('/')[-1]
 for mask in range(8):
  ts=[bool(mask&(1<<i)) for i in range(3)];lab=ns['label'](ts)
  if len(fs)==1 and lab not in [a[':answer/value'] for a in fs[0][':answer-field/choices']]:continue
  if len(fs)==3 and not any(ts):continue
  p2={**p,'truths':ts};case=g.generate(level,459103,key,p2);d=parse(case);covered.append(case);coverage.append(d)
save('decision-records.json',covered);save('decision-results.json',coverage)
# Verify real batched CLI rejection/deduplication sampling, not just generate().
cli=[]
for level in ['moderate','hard']:
 command=[PY,W/'17592186184172.py','--difficulty',level,'--count','17','--seed','430917','--format','json'];x=run(command);data=json.loads(x['stdout']) if x['exit']==0 else []
 save('cli-'+level+'.json',data);cli.append({'command':x['command'],'exit':x['exit'],'requested':17,'received':len(data),'unique_ids':len({r['question'][':question/id'] for r in data}),'math':[parse(r) for r in data]})
save('cli-sampling-results.json',cli)
# Simulate a standalone declared closure in place by hiding only ancestor-repo discovery.
# Necessary because evidence_root itself is under repo_root; no files may be written outside it.
script="""import runpy,pathlib,sys
from unittest.mock import patch
orig=pathlib.Path.is_file
root=pathlib.Path(sys.argv[1]).parent
original=root/'17592186184172.py'
sys.argv=[str(original),'--difficulty','moderate','--count','5','--seed','0']
def declared_only(p):
 if str(p).endswith('/scripts/generator_policy.py'): return False
 return orig(p)
with patch.object(pathlib.Path,'is_file',declared_only):runpy.run_path(str(original),run_name='__main__')
"""
(E/'standalone_discovery.py').write_text(script)
x=run([PY,E/'standalone_discovery.py',E/'legacy/17592186184172.py']);save('legacy-failure-reproduced.json',{'result':x,'expected_failure':x['exit']!=0 and 'StopIteration' in x['stderr'],'interpretation':'Original ancestor lookup has no scripts/generator_policy.py in its declared closure. Dependency discovery outside closure is hidden because review paths must remain under repository-owned evidence_root. Current package uses declared sibling generator_policy.py and passed normal manifest-only relocation. -I is excluded from contract because it also disables sibling imports.'})
# All native checks in ONE invocation, including normalized delivered records.
allrows=json.load(open('replay-records.json'))+json.load(open('fresh-records.json'))+json.load(open('runner-batch.json'))+json.load(open('counterfactual-records.json'))+json.load(open('boundary-records.json'))+covered
for stage in ['batch','moderate','hard']:allrows+=json.load(open(f'delivery-{stage}/accepted.json'))
save('native-input.json',native(allrows));save('extended-math-results.json',{'count':len(allrows),'failures':[d for d in map(parse,allrows) if d['errors']]})
print('Controlled decision cases:',len(covered),'Native records:',len(allrows),'Legacy failure:',x['exit'],'StopIteration' in x['stderr'])
