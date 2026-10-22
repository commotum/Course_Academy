#!/usr/bin/env python3
"""Independent exact-arithmetic revision review; all writes beside this script."""
import sys
sys.dont_write_bytecode=True
import json,re,pathlib,copy,hashlib,importlib.util,subprocess,platform,collections,os,random
R=pathlib.Path(__file__).resolve().parent;J=R.parent;P=J/'workspace'
def save(n,x): (R/n).write_text(json.dumps(x,indent=2,default=str))
def load(p): return json.loads(pathlib.Path(p).read_text())
sys.path.insert(0,str(P))
spec=importlib.util.spec_from_file_location('reviewed',P/'17592186119784.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def matrices(text):
 return [[[int(c.strip()) for c in row.split('&')] for row in b.split(r'\\')] for b in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def value(f):
 ref=f[':answer-field/correct'];aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
 return next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def enum(x): return x.get(':db/ident') if isinstance(x,dict) else x
def norm(x):return re.sub(r'[{}\s$]','',x)
def derive(m,key):
 expr,kind=re.search(r'\$(.*?)\$ is (upper triangular|lower triangular|diagonal)',key).groups()
 a=norm(expr);a=a.replace(next(c for c in a if c.isalpha()),'X');t=list(map(list,zip(*m)))
 if a=='X':b=m
 elif a=='X^T':b=t
 elif a in ('X+X^T','X^T+X'):b=[[x+y for x,y in zip(r,s)] for r,s in zip(m,t)]
 elif a=='X^T-X':b=[[x-y for x,y in zip(r,s)] for r,s in zip(t,m)]
 elif a=='X-X^T':b=[[x-y for x,y in zip(r,s)] for r,s in zip(m,t)]
 else:raise AssertionError(a)
 cells=[(i,j) for i in range(len(m)) for j in range(len(m)) if (i>j if kind=='upper triangular' else i<j if kind=='lower triangular' else i!=j)]
 return all(b[i][j]==0 for i,j in cells),b,cells
def oracle(r):
 q=r['question'];m=matrices(q[':question/problem'])[0];ordinary=[derive(m,f[':answer-field/key'])[0] for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above']
 return [not any(ordinary) if f[':answer-field/key']=='None of the above' else derive(m,f[':answer-field/key'])[0] for f in q[':question/answer-fields']]
def audit(r,label):
 q=r['question'];m=matrices(q[':question/problem'])[0];exp=oracle(r);actual=[value(f) for f in q[':question/answer-fields']]
 sol=q[':question/worked-solution'];derived=[derive(m,f[':answer-field/key'])[1] for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above']
 truths=re.findall(r'\*\*(true|false)\*\*',sol)
 witnesses=[]
 for block in sol.split('\n\n- '):
  w=re.search(r'row (\d+), column (\d+) is \$(-?\d+)',block)
  if w:
   i,j,v=map(int,w.groups());b=matrices(block)[0];key=re.search(r'\$(.*?)\$ is (upper triangular|lower triangular|diagonal)',block)[0]
   witnesses.append((i-1,j-1) in derive(m,key)[2] and b[i-1][j-1]==v and v!=0)
 result={'set':label,'id':q[':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'expected':exp,'actual':actual,'keys':exp==actual,'proof_matrices':matrices(sol)==derived,'proof_truths':[v=='true' for v in truths]==exp[:len(derived)],'witnesses':all(witnesses)}
 return result
sources=load(J/'source/source.json')['material']['kp'][':knowledge-point/questions']
replays=[];source_results=[]
for q in sources:
 sid=q[':question/math-academy-id'];level=(enum(q.get(':question/difficulty')) or ':question.difficulty/hard').split('/')[-1]
 raw=g.generate(level,173,sid,profile='source-replay');rq=raw['question']
 bank=lambda fs:[(f[':answer-field/key'],enum(f[':answer-field/type']),[a[':answer/value'] for a in f[':answer-field/choices']],value(f)) for f in fs]
 checks={'prompt':rq[':question/problem']==q[':question/problem'],'solution':rq[':question/worked-solution']==q[':question/worked-solution'],'complete_bank':bank(rq[':question/answer-fields'])==bank(q[':question/answer-fields']),'difficulty':enum(rq.get(':question/difficulty'))==enum(q.get(':question/difficulty')),'independent_math':oracle(raw)==[value(f) for f in rq[':question/answer-fields']]}
 source_results.append({'source_id':q[':question/id'],'template':sid,**checks});replays.append(raw)
save('source-replay-records.json',replays);save('source-replay-results.json',source_results)
# Keep the matrix, template and seed fixed except for one answer-bearing entry.
controls=[];control_index=[];fresh=[]
for q in sources:
 sid=q[':question/math-academy-id'];level=(enum(q.get(':question/difficulty')) or ':question.difficulty/hard').split('/')[-1];n=len(matrices(q[':question/problem'])[0])
 for case in ['diagonal','upper','lower','neither']+(['symmetric','skew'] if level=='hard' else []):
  m=[[i+1 if i==j else 0 for j in range(n)] for i in range(n)]
  if case in ('upper','neither','symmetric','skew'):m[0][-1]=2
  if case in ('lower','neither','symmetric','skew'):m[-1][0]=-2 if case=='skew' else 2 if case=='symmetric' else 3
  r=g.generate(level,23861,sid,parameters={'matrix':m});controls.append(r);control_index.append({'record_index':len(controls)-1,'template':sid,'level':level,'case':case,'expected':oracle(r)})
 for seed in [92737,92801,92809]:fresh.append(g.generate(level,seed,sid))
save('controls.json',controls);save('control-index.json',control_index);save('fresh.json',fresh)
batch=load(J/'samples.json');save('batch.json',batch)
a={'matrix':[[4,0,0],[1,1,0],[0,0,3]]};b={'matrix':[[4,0,0],[0,1,0],[0,0,3]]};c=copy.deepcopy(a);c['matrix'][0][0]=-8
cf=[g.generate('moderate',101,'q-42091',parameters=p) for p in [a,b,c]]
# Hold both regions nonzero; change only the mirrored sign to alter sum cancellation.
hs=[g.generate('hard',401,'q-126474',parameters={'matrix':m}) for m in [[[1,2,0],[-2,2,0],[0,0,3]],[[1,2,0],[2,2,0],[0,0,3]]]]
save('counterfactual-records.json',cf+hs)
save('counterfactual-results.json',{'command':f'{sys.executable} -B {R}/audit_revision.py','seeded_relevant':{'before':oracle(cf[0]),'after':oracle(cf[1]),'expected_before':[False,True,True,False],'expected_after':[True,True,True,False],'passed':oracle(cf[0])==[False,True,True,False] and oracle(cf[1])==[True,True,True,False]},'irrelevant_diagonal':{'before':oracle(cf[0]),'after':oracle(cf[2]),'passed':oracle(cf[0])==oracle(cf[2])},'hard_mirrored_sign':{'before':oracle(hs[0]),'after':oracle(hs[1]),'passed':oracle(hs[0])==[False,False,True,False] and oracle(hs[1])==[False,False,False,True]}})
all_sets=[('controls',controls),('fresh',fresh),('batch',batch),('counterfactual',cf+hs)]
results=[audit(r,s) for s,rs in all_sets for r in rs];save('math-results.json',results)
grader=[]
for rs in [controls,batch,cf+hs]:
 for r in rs:
  checks=[]
  for i,(f,expected) in enumerate(zip(r['question'][':question/answer-fields'],oracle(r))):
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if (a[':answer/value']=='true')==expected else 'rejected','purpose':'Independent exact arithmetic, both true and false choice UUIDs'})
  grader.append({'label':r['generation']['template']+':'+r['question'][':question/id'],'record':r,'checks':checks})
save('grader-input.json',grader)
moderate=[r for r in controls+fresh if r['generation']['level']=='moderate'];save('moderate.json',moderate)
save('hard.json',[r for r in controls+fresh if r['generation']['level']=='hard'])
save('render-records.json',batch+cf+hs)
reject=[]
for label,p,kwargs in [('out-of-range',{'matrix':[[9,0,0],[0,0,0],[0,0,0]]},{}),('float',{'matrix':[[1.0,0,0],[0,0,0],[0,0,0]]},{}),('bool',{'matrix':[[True,0,0],[0,0,0],[0,0,0]]},{}),('nonsquare',{'matrix':[[0,0],[0,0],[0,0]]},{}),('unknown-slot',{'matrix':[[0]*3 for _ in range(3)],'target':'upper'},{}),('unknown-template',None,{'template':'missing'}),('radio',None,{'field_type':'radio'}),('unknown-profile',None,{'profile':'missing'}),('zero-boundary',{'matrix':[[0]*3 for _ in range(3)]},{}),('integer-boundary',{'matrix':[[-8,8,0],[0,8,0],[0,0,-8]]},{})]:
  try:
   r=g.generate('moderate',107,parameters=p,**({'template':'q-42091'}|kwargs));reject.append({'case':label,'rejected':False,'record':r})
  except Exception as e:reject.append({'case':label,'rejected':True,'error':str(e)})
save('rejections.json',reject)
# Copy only manifest-owned runtime files and compare public output from unrelated cwd.
manifest=load(P/'package.json');rel=R/'relocated';rel.mkdir(exist_ok=True)
for name in ['package.json']+manifest['files']:
 dst=rel/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((P/name).read_bytes())
cmd=[sys.executable,'-B',str(rel/manifest['entrypoint']),'--difficulty','moderate','--seed','92737','--count','3','--format','json']
relocated=json.loads(subprocess.check_output(cmd,cwd=R,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}));save('relocated-records.json',relocated)
runtime={'installed':{'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}},'declared':manifest['dependencies'],'exact_dependencies':manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}},'relocation_command':cmd,'relocation_equal':relocated==[g.generate('moderate',92737+i) for i in range(3)],'deterministic':all(r==g.generate(r['generation']['level'],r['generation']['seed'],r['generation']['template']) for r in fresh),'runner_replay':[r==g.generate('moderate',r['generation']['seed']) for r in batch],'external_outputs':'No assets or output files; stdout JSON. SymPy is the only third-party import. Source path is relative to entrypoint.','rejection_resampling':'Every source-bank record contains explicit None. Nonempty wrapper returns first attempt; no profile rejected or silently resampled.'}
save('packaging-results.json',runtime)
save('scope-results.json',{'source_cases':12,'authored_extensions':'All four zero-region profiles per moderate bank; same observed 3x3/4x4 sizes and expressions. Hard additionally tests cancellation/noncancellation. All 3 ordinary Boolean statements plus source-backed None.','moderate_ops':sorted(set(norm(f[':answer-field/key']) for r in moderate for f in r['question'][':question/answer-fields'])),'gaps':['Canonical example has no captured answer fields; its lesson definition and transpose difference method are covered, without inventing a bank.'],'easy':'Unchanged authored prerequisite-level family retained; prior scope evidence applies only to unchanged conceptual operations.'})
inv=load(J/'source/inventory.json');srcids={q[':question/id'] for q in sources};other=[q for q in inv['questions'] if q[':question/id'] not in srcids];save('inventory-unmatched.json',other)
save('inventory-assessment.json',{'captured_basis':inv['basis'],'count':len(inv['questions']),'original_source_count':len(srcids),'other_questions':len(other),'unprovenanced':[{'id':q[':question/id'],'entity_id':q.get(':db/id'),'generation_metadata':q.get('generation')} for q in other],'prior_independent_evidence':'Prior inventory assessment and attempts reused: source hash and inventory hash match. No stored generated instance with matching ID and generation metadata was demonstrated. Original source questions excluded.','limitation':'Empty affected list is not verified absence; one non-source stored record has no captured generation metadata.'})
save('affected-inventory.json',{'affected_questions':[]})
save('commands.json',{'audit':[sys.executable,'-B',str(R/'audit_revision.py')],'provenance':'prior-* scripts retained verbatim; audit_revision.py reuses independent parsing and exact arithmetic concepts, with current complete source replay and changed construction tests.'})
(R/'session-state.md').write_text('Retained failing examples tested on old and current code. Current independent source replay, controlled profiles, fresh seeds, counterfactuals, exact math, rejection boundaries, dependency versions and relocation saved. Next: native grader, real delivery/selection, actual UI rendering and shortcut audit.\n')
print(json.dumps({'source_failures':[x for x in source_results if not all(x[k] for k in ['prompt','solution','complete_bank','difficulty','independent_math'])],'math_count':len(results),'math_failures':[x for x in results if not all(x[k] for k in ['keys','proof_matrices','proof_truths','witnesses'])],'controls':len(controls),'fresh':len(fresh),'packaging':runtime},indent=2))
