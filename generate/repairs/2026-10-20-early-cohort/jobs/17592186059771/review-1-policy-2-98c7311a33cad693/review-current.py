"""Independent focused revision audit. Writes only beside this script.
Run with the context Python, -B. Source and arithmetic helpers reuse prior independent evidence.
"""
from independent_helpers import *
import itertools, ast, shutil
src=json.loads((J/'source/source.json').read_text());sq=src['material']['kp'][':knowledge-point/questions']
batch=json.loads((J/'samples.json').read_text());save('batch-records.json',batch)
# Fresh independent seeds, not the author's or previous review's seed range.
samples=[g.generate(d,s) for d,n in [('easy',18),('moderate',8),('hard',36)] for s in range(91027,91027+n)]
save('control-records.json',samples)
for d in ['easy','moderate','hard']:save(d+'-records.json',[r for r in samples if r['question'][':question/difficulty'].endswith('/'+d)])
# Source banks, original operations and key; compare presentation-normalized prompts separately.
replays=[];replay_results=[]
for q in sq:
 sid=q[':question/math-academy-id'];d=q[':question/difficulty'][':db/ident'].split('/')[-1]
 r=hard.replay(sid,1511) if d=='hard' else g.generate(d,1511,sid,easy.CASES[sid] if d=='easy' else None)
 replays.append(r);out=r['question']
 raw=g.normalize_prose(q[':question/problem']).replace('↔',r'\leftrightarrow')
 normalize=lambda p:re.sub(r'\s+|\\,|\\cdot|[{}.]','',p).replace('↔',r'\leftrightarrow')
 replay_results.append({'source_id':q[':question/id'],'ma_id':sid,'matrix_equal':mat(raw)==mat(out[':question/problem']),'bank_equal':sorted(str(mat(a[':answer/value'])) for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(str(mat(a[':answer/value'])) for a in out[':question/answer-fields'][0][':answer-field/choices']),'key_equal':mat(key(q)[':answer/value'])==mat(key(out)[':answer/value']),'operation_equal':ops(raw)==ops(out[':question/problem']),'field_contract_equal':len(out[':question/answer-fields'])==1 and out[':question/answer-fields'][0][':answer-field/type']==':answer-field.type/radio','prompt_normalized_equal':normalize(raw)==normalize(out[':question/problem'])})
canon=g.generate('moderate',1511,'e-4693');cq=src['material']['kp'][':knowledge-point/canonical-example']
save('canonical-replay.json',canon)
save('source-replays.json',replays)
save('source-replay-results.json',{'banks':replay_results,'canonical_problem_equal':canon['question'][':question/problem']==g.normalize_prose(cq[':question/problem']),'canonical_solution_equal':canon['question'][':question/worked-solution']==g.normalize_prose(cq[':question/worked-solution']),'canonical_no_bank':canon['question'][':question/answer-fields']==[],'correction':'q-10248 incorrect intermediate donor negation corrected; preserve donor row throughout.'})
# Controlled same-bank changes, row-role changes and irrelevant changes at fresh data.
m=[[2,-3,4],[-5,1,7],[3,8,-2]];pairs=[[1,2],[-2,1],[3,-1],[-1,-3],[2,4]]
pair_records=[];pair_results=[];case_indices={}
for case,roles in [('shared-target',[(1,0),(1,2)]),('shared-donor',[(0,2),(1,2)])]:
 group=[]
 for a,b in pairs:
  p={'matrix':m,'operations':[[*roles[0],a],[*roles[1],b]],'candidate_pairs':pairs,'name':'C'}
  group.append(g.generate('hard',2467,parameters=p))
 start=len(pair_records);pair_records+=group;case_indices[case]=start
 base=group[0];p=copy.deepcopy(base['generation']['parameters'])
 for irrelevant in ['name','order']:
  v=copy.deepcopy(p)
  if irrelevant=='name':v['name']='B'
  else:v['operations'].reverse();v['candidate_pairs']=[list(reversed(x)) for x in pairs]
  pair_records.append(g.generate('hard',2467,parameters=v))
  pair_results.append({'case':case,'kind':'irrelevant','change':irrelevant,'base_index':start,'variant_index':len(pair_records)-1,'same_result':calc(base['question'])==calc(pair_records[-1]['question']),'same_key_value':key(base['question'])[':answer/value']==key(pair_records[-1]['question'])[':answer/value'],'same_fingerprint':base['generation']['mathematical_fingerprint']==pair_records[-1]['generation']['mathematical_fingerprint']})
 banks=[sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']) for r in group]
 pair_results.append({'case':case,'kind':'relevant','change':'requested coefficient pair','indices':list(range(start,start+5)),'same_complete_bank':all(b==banks[0] for b in banks),'distinct_keys':len({key(r['question'])[':answer/value'] for r in group}),'distinct_prompts':len({r['question'][':question/problem'] for r in group}),'distinct_solutions':len({r['question'][':question/worked-solution'] for r in group})})
 # Change relevant destination: a third row is eligible, with all entries held fixed.
 p2=copy.deepcopy(p)
 if case=='shared-target':p2['operations']=[[0,1,1],[0,2,2]]
 else:p2['operations']=[[0,1,1],[2,1,2]]
 pair_records.append(g.generate('hard',2467,parameters=p2))
 pair_results.append({'case':case,'kind':'relevant','change':'row roles','base_index':start,'variant_index':len(pair_records)-1,'changed_result':calc(base['question'])!=calc(pair_records[-1]['question']),'changed_prompt':base['question'][':question/problem']!=pair_records[-1]['question'][':question/problem'],'changed_solution':base['question'][':question/worked-solution']!=pair_records[-1]['question'][':question/worked-solution']})
# Easy source-unchanged controlled decision dependencies retained as small regressions.
p={'matrix':m,'rows':[0,1]}
pair_records += [g.generate('easy',2468,'swap-complete',v) for v in [p,{**p,'rows':[0,2]},{**p,'rows':[1,0]}]]
scale={'matrix':[[6,-6,0],[1,2,3],[4,5,6]],'target':0,'factor':[1,3],'candidate_factors':[[1,3],[1,2],[2,1],[-1,2],[-1,3]]}
pair_records += [g.generate('easy',2469,'scale-arithmetic',v) for v in [scale,{**scale,'factor':[-1,2]}]]
save('counterfactual-records.json',pair_records);save('counterfactual-results.json',pair_results)
# Exercise all row-role boundaries for both changed relationships; output follows actual prompt.
roles=[]
for case in ['shared-target','shared-donor']:
 for anchor,a,b in itertools.permutations(range(3)):
  p={'matrix':m,'operations':[[anchor,a,1],[anchor,b,2]] if case=='shared-target' else [[a,anchor,1],[b,anchor,2]],'candidate_pairs':pairs,'name':'B'}
  roles.append(g.generate('hard',1421,parameters=p))
save('role-records.json',roles)
# Independent exact arithmetic parser for all visible worked stages, including expressions.
def expr(x):
 x=x.strip();x=re.sub(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',r'(\1\2/\3)',x).replace(r'\cdot','*').replace(')(',')*(')
 def run(n):
  if isinstance(n,ast.Constant) and type(n.value)==int:return F(n.value)
  if isinstance(n,ast.UnaryOp):return (-1 if isinstance(n.op,ast.USub) else 1)*run(n.operand)
  if isinstance(n,ast.BinOp):
   a,b=run(n.left),run(n.right)
   if isinstance(n.op,ast.Add):return a+b
   if isinstance(n.op,ast.Sub):return a-b
   if isinstance(n.op,ast.Mult):return a*b
   if isinstance(n.op,ast.Div):return a/b
  raise ValueError(ast.dump(n))
 return run(ast.parse(x,mode='eval').body)
def stages(q):
 actual=[]
 for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/worked-solution'],re.S):
  actual.append([[expr(v) for v in row.split('&')] for row in re.split(r'\\\\',body)])
 expected=[mat(q[':question/problem'])];current=copy.deepcopy(expected[0])
 for typ,t,s,k in ops(q[':question/problem']):
  if typ=='swap':current[t],current[s]=current[s],current[t];expected.append(copy.deepcopy(current))
  else:
   current[t]=[k*x for x in current[t]] if typ=='scale' else [a+k*b for a,b in zip(current[t],current[s])]
   expected.extend([copy.deepcopy(current),copy.deepcopy(current)])
 return {'id':q[':question/id'],'stage_count':len(actual),'all_worked_stages_correct':actual==expected}
all_records=batch+samples+replays+pair_records+roles
math_results=[{**verify(r),**stages(r['question'])} for r in all_records]
flags=['key_correct','unique_correct','five_unique','solution_final_correct','all_worked_stages_correct']
save('math-results.json',{'command':PY+' -B review-current.py','count':len(math_results),'failures':[x for x in math_results if not all(x[k] for k in flags)],'checks':math_results})
# Batch native engine outcomes including stale alternatives for controlled pairs.
gcases=[]
for i,r in enumerate(batch+replays+pair_records+roles):
 q=r['question'];expected=calc(q)
 gcases.append({'label':str(i)+': '+q[':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if mat(a[':answer/value'])==expected else 'rejected','purpose':'Independent exact visible arithmetic, all five options including any stale former key'} for a in q[':question/answer-fields'][0][':answer-field/choices']]})
save('grader-input.json',gcases)
# Measured coverage after generator resampling.
coverage={}
for d in ['easy','moderate','hard']:
 rs=[r for r in samples if r['question'][':question/difficulty'].endswith('/'+d)]
 coverage[d]={'profiles':dict(collections.Counter(r['generation']['profile'] for r in rs)),'role_assignments':dict(collections.Counter(str([(t,s) for _,t,s,k in ops(r['question'][':question/problem'])]) for r in rs)),'attempts':dict(collections.Counter(r['generation']['sampling_attempts'] for r in rs))}
save('coverage-results.json',{'fresh_seeds':{'first':91027,'easy_count':18,'moderate_count':8,'hard_count':36},'coverage':coverage,'explicit_boundaries':len(roles),'batch_profiles':dict(collections.Counter(r['generation']['profile'] for r in batch))})
# Rejection tests include newly implemented operation relationships and replay-only bank safety.
rejections=[]
for d,profile,p in [
 ('hard',None,{'matrix':m,'operations':[[0,1,0],[2,1,2]],'candidate_pairs':pairs,'name':'C'}),
 ('hard',None,{'matrix':m,'operations':[[0,0,1],[2,0,2]],'candidate_pairs':pairs,'name':'C'}),
 ('hard',None,{'matrix':m,'operations':[[0,1,1],[1,2,2]],'candidate_pairs':pairs,'name':'C'}),
 ('hard',None,{'matrix':m,'operations':[[0,1,1],[2,1,2]],'candidate_pairs':[[1,2]]*5,'name':'C'}),
 ('easy','q-10251',{'matrix':m,'rows':[0,2]}),
 ('moderate','q-10243',{'matrix':m,'target':2,'source':1,'k':-5,'name':'G'}),
 ('easy','swap-complete',{'matrix':m,'rows':[1,1]}),
 ('easy','scale-arithmetic',{**scale,'factor':[0,1]})]:
 try:g.generate(d,1421,profile,p);rejected=False;error=None
 except ValueError as ex:rejected=True;error=str(ex)
 rejections.append({'difficulty':d,'profile':profile,'parameters':p,'rejected':rejected,'error':error})
# Manifest files only relocated; actual interpreter exact version checked.
manifest=json.loads((P/'package.json').read_text());rel=E/'relocated';rel.mkdir(exist_ok=True)
for name in manifest['files']+['package.json']:shutil.copyfile(P/name,rel/name)
relocations=[]
for d in ['easy','moderate','hard']:
 args=['--difficulty',d,'--seed','91027','--count','3']
 run=lambda f:subprocess.run([PY,'-B',str(f),*args],capture_output=True,text=True,cwd=E,check=True)
 orig=run(P/'generator.py');new=run(rel/'generator.py');rs=json.loads(new.stdout);save('relocation-'+d+'-records.json',rs)
 relocations.append({'difficulty':d,'equal':json.loads(orig.stdout)==rs,'stderr':new.stderr,'command':[PY,'-B',str(rel/'generator.py'),*args]})
save('packaging-results.json',{'manifest':manifest,'actual_python':platform.python_version(),'exact_version_matches':manifest['dependencies']=={'python':platform.python_version(),'packages':{}},'deterministic':all(r==g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed']) for r in samples),'relocations':relocations,'rejections':rejections,'external_outputs':'No runtime assets required. Output JSON stdout; no stderr. All execution uses -B; copies and review files reside under evidence root.'})
# Render exact delivered batch separately, plus changed paths and counterfactuals.
save('render-batch-records.json',batch)
save('render-changed-records.json',[next(r for r in replays if r['generation']['profile']==p) for p in ['q-10251','q-10243']]+pair_records[:2]+[pair_records[5],pair_records[6],pair_records[7]]+pair_records[8:10]+[pair_records[13],pair_records[14],pair_records[15]]+pair_records[16:])
(E/'session-state.md').write_text('Source reconstruction saved before package inspection. Original strict independent regressions reproduced all retained failures on hash-matched old package, now pass current package. Actual author preflight rerun passes. Fresh samples, complete source banks, all visible math stages, role boundaries, counterfactuals, relocation and rejection checks saved. Grading, delivery and UI inspection pending.\n')
print(json.dumps({'source_banks':len(replay_results),'source_failures':[x for x in replay_results if not all(v for k,v in x.items() if k.endswith('equal'))],'math_records':len(math_results),'math_failures':[x for x in math_results if not all(x[k] for k in flags)],'coverage':coverage,'packaging':{'exact_version_matches':manifest['dependencies']=={'python':platform.python_version(),'packages':{}},'relocation':all(x['equal'] for x in relocations),'rejections':all(x['rejected'] for x in rejections)}}))
