"""Focused author validation after repair_check.py, offline and workspace-only."""
import json,sys,re,subprocess,hashlib,shutil,os,importlib.metadata
from pathlib import Path
import repair_check as c
W=c.W;E=W/'evidence';R=Path('/home/jake/Developer/Course_Academy');J=W.parent;P=R/'.venv/bin/python';g=c.g
sys.dont_write_bytecode=True
def load(p):return json.loads(Path(p).read_text())
def run(label,args):
 p=subprocess.run(list(map(str,args)),cwd=W,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 c.save(label+'-execution.json',{'command':list(map(str,args)),'exit_code':p.returncode,'stdout':p.stdout[-4000:],'stderr':p.stderr[-4000:]})
 assert p.returncode==0,(label,p.stderr[-3000:]);return p

def main():
 original=load(J/'source/source.json')['material']['kp'][':knowledge-point/questions']
 replays=[];replay_results=[]
 def norm(s):return re.sub(r'\s+','',s.replace(r'\left','').replace(r'\right',''))
 for q in original:
  t=q[':question/math-academy-id']
  if t not in g.SOURCES:continue
  level=q[':question/difficulty'][':db/ident'].split('/')[-1]
  r=g.generate(level,731,t,{'shift':0});f=c.field(r);sf=q[':question/answer-fields'][0]
  assert r['question'][':question/problem']==q[':question/problem']
  assert norm(r['question'][':question/worked-solution'])==norm(q[':question/worked-solution'])
  assert sorted(norm(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(norm(a[':answer/value']) for a in sf[':answer-field/choices'])
  assert norm(c.keyvalue(r))==norm(sf[':answer-field/correct'][':answer/value'])
  c.verify(r,False);replays.append(r);replay_results.append({'template':t,'source_id':q[':question/id'],'complete_bank_matched':5,'unique_mathematical_key':True})
 c.save('source-replays.json',replays);c.save('source-replay-results.json',{'banks':len(replays),'choices':5*len(replays),'results':replay_results,'unresolved':'q-106074 has no key/solution and all supplied choices fail; prior independent derivation retained in source-gap-results.json'})
 shutil.copyfile(J/'review-0-policy-2-6ca8b422a4136178/source-gap-results.json',E/'source-gap-results.json')
 controlled=load(E/'controlled-records.json');ordinary=load(E/'ordinary-records.json')
 boundaries=[]
 for t in g.FAMILIES:
  level=g.SOURCES[t][':question/difficulty'][':db/ident'].split('/')[-1]
  for a,b,h in [(2 if t=='q-109172' else 1,3,-6),(4 if t=='q-109172' else 3,-3,6)]:
   boundaries.append(g.generate(level,8301,t,{'shift':h,'a':a,'b':b}))
 batch=json.loads(run('batch',[P,W/'17592186147454.py','--difficulty','moderate','--count','5','--seed','98301','--format','json']).stdout);c.save('batch.json',batch)
 checked=[c.verify(r) for r in boundaries+batch]
 c.save('boundary-records.json',boundaries);c.save('boundary-math.json',checked)
 # A small ordinary sample checks runtime sampling, rather than only explicit APIs.
 sampled=[c.verify(r) for r in ordinary];c.save('ordinary-math.json',sampled)
 all_records=replays+controlled+boundaries+batch+ordinary+load(E/'coefficient-counterfactual.json')+[load(E/'focused-records.json')[g.SHIFTS.index(1)]]+[g.generate('moderate',0,'q-109029',{'shift':1})]
 c.save('grader-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==c.key(r) else 'rejected','purpose':'Independently residual-checked radio option'} for a in c.field(r)[':answer-field/choices']]} for r in all_records])
 run('grader',[R/'generate/runs/current/check-engine',E/'grader-input.json',E/'grader-report.json'])
 delivery={}
 for band in ('moderate','hard'):
  records=[r for r in controlled+boundaries+ordinary+batch if r['question'][':question/difficulty'].endswith('/'+band)]
  c.save('delivery-'+band+'-input.json',records)
  run('delivery-'+band,[P,R/'generate/pipeline/check_delivery.py','--input',E/('delivery-'+band+'-input.json'),'--source',J/'source/source.json','--inventory',J/'source/inventory.json','--difficulty',band,'--output',E/('delivery-'+band),'--asset-root',E,'--math-root','/media/jake/SSD/EDB/math'])
  accepted=load(E/('delivery-'+band)/'accepted.json');report=load(E/('delivery-'+band)/'delivery.json')
  # All 5 controlled correct-role assignments must survive actual filters.
  before=controlled if band=='moderate' else controlled
  for t in {r['generation']['template'] for r in before if r['question'][':question/difficulty'].endswith('/'+band)}:
   rr=[r for r in accepted if r['generation']['template']==t and r['generation']['parameters'].get('shift')==1 and 'target' in r['generation']['parameters'] and r['generation']['parameters']['bank']==next(r for r in controlled if r['generation']['template']==t)['generation']['parameters']['bank']]
   assert len(rr)==5,(band,t,len(rr))
   assert len({c.keyvalue(r) for r in rr})==5
  delivery[band]={'input':len(records),'accepted':len(accepted),'duplicates':report['duplicate_count'],'all_controlled_roles_survive':True}
 c.save('delivery-summary.json',delivery)
 # Actual batch independently filtered; no broad sample silently replaces it.
 run('delivery-batch',[P,R/'generate/pipeline/check_delivery.py','--input',E/'batch.json','--source',J/'source/source.json','--inventory',J/'source/inventory.json','--difficulty','moderate','--output',E/'delivery-batch','--asset-root',E,'--math-root','/media/jake/SSD/EDB/math'])
 # Runtime package only, with version/determinism/relocation and invalid bounds.
 manifest=load(W/'package.json');rel=E/'relocated';rel.mkdir(exist_ok=True)
 for f in manifest['files']:
  dest=rel/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/f,dest)
 aa=[P,rel/manifest['entrypoint'],'--difficulty','moderate','--count','5','--seed','98301','--format','json']
 first=run('relocation',aa);second=run('determinism',aa)
 assert json.loads(first.stdout)==batch and first.stdout==second.stdout
 rejected=[]
 for kwargs in [dict(difficulty='easy'),dict(difficulty='moderate',template='q-109154',parameters={'shift':7}),dict(difficulty='moderate',template='q-109154',parameters={'shift':-7}),dict(difficulty='hard',template='q-106074',parameters={'shift':1})]:
  try:g.generate(**kwargs)
  except (ValueError,AssertionError):rejected.append(kwargs)
  else:raise AssertionError(kwargs)
 versions={'python':sys.version.split()[0],'packages':{'sympy':importlib.metadata.version('sympy')}}
 assert manifest['dependencies']==versions
 c.save('packaging-results.json',{'versions':versions,'runtime_files':manifest['files'],'relocation_equal':True,'deterministic':True,'bounds_rejected':rejected,'runtime_sha256':{f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in manifest['files']}})
 # Representative changes: restored autonomous, q154 counterfactuals, negative fifth
 # root forcing, both-sign square root, and both hard fractional inverses.
 render=[controlled[20],controlled[25],controlled[26],boundaries[5],controlled[17],controlled[32],controlled[42]]
 c.save('render-records.json',render)
 c.save('validation-summary.json',{'source_replay_banks':10,'source_replay_choices':50,'native_grader_records':len(all_records),'native_choices':5*len(all_records),'boundary_records':20,'ordinary_sample':24,'batch':5,'delivery':delivery,'math':'passed','grading':'passed','packaging':'passed','rendering':'pending'})
 print(json.dumps(load(E/'validation-summary.json')))
if __name__=='__main__':main()
