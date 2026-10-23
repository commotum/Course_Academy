"""Independent targeted revision audit. Run with repo .venv/bin/python -B supplemental.py."""
import json,re,sys,pathlib,copy,subprocess,collections,hashlib,shutil,os
R=pathlib.Path(__file__).resolve().parent;J=R.parent;P=J/'workspace';REPO=pathlib.Path('/home/jake/Developer/Course_Academy');PY=REPO/'.venv/bin/python'
# Reuse previously independent prompt parser; do not execute its sampling workload.
exec(compile((R/'audit.py').read_text().split('source=json.load')[0],str(R/'audit.py'),'exec'))
def load(n):return json.loads((R/n).read_text())
def run(args,name):
 p=subprocess.run(list(map(str,args)),capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(R/'assets')))
 save(name,{'command':p.args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p

def matrix(q):
 body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1]
 return [[int(re.sub(r'\\boxed\{(-?\d+)\}',r'\1',cell).strip()) for cell in row.split('&')] for row in body.split(r'\\')]
def canon(x):return re.sub(r'[{}\s$]','',x)
source=json.loads((J/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];replays=load('source-replays.json');sr=[]
for q,r in zip(source,replays):
 sid=q[':question/math-academy-id'];actual=r['question'];a=matrix(q);b=matrix(actual)
 fs={f[':answer-field/key']:f for f in actual[':question/answer-fields']}
 sr.append({'source':sid,'matrix_matches':a==b,'field_order_matches':[f[':answer-field/key'] for f in q[':question/answer-fields']]==list(fs),'solution_matches':canon(q.get(':question/worked-solution',''))==canon(actual[':question/worked-solution']) if ':question/worked-solution' in q else 'missing original; inferred solution checked independently','keys_match':all(canon(f[':answer-field/correct'][':answer/value'])==canon(key(fs[f[':answer-field/key']])) for f in q[':question/answer-fields'] if ':answer-field/correct' in f)})
save('source-comparison.json',sr)
# Source-derived bank shapes with every eligible answer role, independent of generator offsets.
controls=[];pairs=[]
for q in source:
 f=q[':question/answer-fields'][0]
 if not f[':answer-field/type'][':db/ident'].endswith('/radio'):continue
 sid=q[':question/math-academy-id'];cs=[coords(a[':answer/value']) for a in f[':answer-field/choices']];mi=min(i for i,j in cs);mj=min(j for i,j in cs);cells=[(i-mi+1,j-mj+1) for i,j in cs]
 template='inline_radio' if sid in ('q-13498','q-13503') else 'display_radio'
 # This arrangement must be a reachable sampler placement, not only a renderer construction.
 placements=g.bank_placements('easy',sid)
 assert any(m==4 and n==4 and set(c)==set(cells) and set(ts)==set(cells) for m,n,c,ts in placements)
 group=[]
 for i,j in cells:
  p={'matrix':[[0]*4 for _ in range(4)],'i':i,'j':j,'letter':'Z'}
  r=g.assemble('easy',817,template,p,sid,cells=cells);controls.append(r);group.append(r)
  other=copy.deepcopy(p);other['matrix']=[[1]*4 for _ in range(4)]
  irr=g.assemble('easy',817,template,other,sid,cells=cells);controls.append(irr)
  pairs.append({'kind':'irrelevant','before':len(controls)-2,'after':len(controls)-1})
 # adjacent targets in bank: matrix/letter/bank/seed constant.
 for k in range(1,len(group)):pairs.append({'kind':'relevant','before':controls.index(group[0]),'after':controls.index(group[k])})
for t in ('notation_blank','two_indices'):
 start=len(controls)
 p={'matrix':[[0]*4 for _ in range(4)],'i':1,'j':2,'letter':'Z'}
 for pp in (p,dict(p,i=3,j=4),dict(p,matrix=[[1]*4 for _ in range(4)])):
  controls.append(g.generate_easy(seed=817,template=t,parameters=pp))
 pairs += [{'kind':'relevant','before':start,'after':start+1},{'kind':'irrelevant','before':start,'after':start+2}]
save('controlled-records.json',controls)
save('controlled-pairs.json',{'parameters':'seed 817; source-derived bank; fixed zero matrix and Z label; change box or all entries','pairs':pairs})
# Small default samples plus explicit CLI profile samples exercise repaired batching nonvacuously.
fresh=[];batch_checks=[]
for seed,profile,count in [(s,None,5) for s in (77191,77192,77193)]+[(77194,k,5) for k in g.BANKS]:
 rs=g.generate_batch('easy',seed,count,profile=profile);fresh+=rs;batch_checks.append({'seed':seed,'profile':profile,'count':count,'ids':[r['question'][':question/id'] for r in rs]})
save('fresh-batches.json',fresh);save('fresh-batch-inputs.json',batch_checks)
records=load('samples.json')+load('boundaries.json')+replays+load('batch.json')+controls+fresh
results=[]
for r in records:
 f=facts(r);q=r['question'];i,j=f['position'];v=matrix(q)[i-1][j-1];sol=canon(q[':question/worked-solution']);letter=f['letter'];symbol=f'{letter}_{i}{j}'
 if len(q[':question/answer-fields'])==2:
  if f'i={i}' not in sol or f'j={j}' not in sol:f['errors'].append('wrong solution indices')
 elif symbol+'='+str(v) not in sol and str(v)+'='+symbol not in sol:f['errors'].append('wrong solution conclusion')
 results.append(f)
save('independent-math.json',{'count':len(results),'failures':[f for f in results if f['errors']],'results':results})
# Strict native tests: actual fields, every radio option, valid equivalent blanks, stale keys.
cases=[]
for r in replays+load('batch.json')+controls:
 fct=facts(r);i,j=fct['position'];letter=fct['letter'];checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  k=key(f)
  if f[':answer-field/type'].endswith('/radio'):
   checks += [{'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==k else 'rejected','purpose':'all displayed options, coordinate-checked'} for a in f[':answer-field/choices']]
  else:
   if '_' in k:good=[k,f'{letter}_{{{i}{j}}}','{{'+letter+'}}_{{'+str(i)+'}{'+str(j)+'}}',f'{letter}_{{{i}{j}}}+0'];bad=[f'{letter}_{{{i}{j%4+1}}}',f'{letter}_{{{i%4+1}{j}}}',f'k_{{{i}{j}}}',str(matrix(r['question'])[i-1][j-1]),letter]
   else:good=[k,k+'.0',str(int(k)*3)+'/3'];bad=['0',str(int(k)+1)]
   checks += [{'field_index':fi,'submitted':s,'expected':e,'purpose':'valid equivalence' if e=='accepted' else 'wrong row, column, label or entry value'} for ss,e in [(good,'accepted'),(bad,'rejected')] for s in dict.fromkeys(ss)]
 cases.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
save('native-input.json',cases)
run([REPO/'generate/runs/current/check-engine',R/'native-input.json',R/'native-report.json'],'native-execution.json')
run([REPO/'generate/runs/current/check-engine',R/'grader-symbolic-strict.json',R/'prior-strict-current-report.json'],'prior-strict-current-execution.json') if (R/'grader-symbolic-strict.json').exists() else run([REPO/'generate/runs/current/check-engine',R/'prior-grader-symbolic-strict.json',R/'prior-strict-current-report.json'],'prior-strict-current-execution.json')
# Reproduce prior bank-only failure on its preserved exact failing batch, and test new candidates.
shutil.copyfile(J/'review-0-policy-2-fd6037e892fe96a5/batch.json',R/'prior-batch.json')
for src in ['prior-batch','batch','fresh-batches','controlled-records']:
 run([PY,R/'regression_shortcut.py',R/(src+'.json'),R/(src+'-cue.json')],src+'-cue-execution.json')
# Relocated runtime and exact batch replay.
rel=R/'relocated';rel.mkdir(exist_ok=True)
for f in json.loads((P/'package.json').read_text())['files']:
 dest=rel/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/f,dest)
p=run([PY,'-B',rel/'17592186100990.py','--difficulty','easy','--seed','3782988951','--count','5','--format','json'],'relocation-execution.json')
save('relocation.json',{'matches_exact_runner_batch':json.loads(p.stdout)==load('batch.json'),'returncode':p.returncode})
# Render all exact batch, source cases, a relevant and irrelevant pair for radio and both blank types.
render=load('batch.json')+replays+[controls[k] for k in [0,1,2,50,51,52,53,54,55]]
save('render-records.json',render)
print(json.dumps({'math_count':len(results),'math_failures':len([f for f in results if f['errors']]),'native':load('native-execution.json')['returncode'],'prior_native':load('prior-strict-current-execution.json')['returncode'],'source_replays':len(sr),'controlled':len(controls),'fresh_batches':len(fresh),'relocation':load('relocation.json')}))
