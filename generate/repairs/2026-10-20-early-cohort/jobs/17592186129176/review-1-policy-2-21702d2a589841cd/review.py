import os,sys,json,pathlib,hashlib,importlib.util,copy,itertools,collections,subprocess,shutil,platform
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
J=E.parent; P=J/'workspace'; R=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,v): (E/n).write_text(json.dumps(v,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
snapshot={p.name:sha(p) for p in P.iterdir() if p.is_file()};save('package-before.json',snapshot)
sys.path.insert(0,str(P));import generator as g
import re
src=json.load(open(J/'source/source.json'));qs=src['material']['kp'][':knowledge-point/questions']
save('batch-records.json',json.load(open(J/'samples.json')))
def unpack(r):
 q=r['question']; text=q[':question/problem'];body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)[1]
 matrix=[[int(x.strip()) for x in row.split('&')] for row in body.split('\\\\')]
 rows=[int(n)-1 for n in re.findall(r'\$(\d)(?:\$|\\text\{)',text.split('rows')[0])]
 vals=[next(x for x in matrix[i] if x!=0) for i in rows];f=q[':question/answer-fields'][0];choices=f[':answer-field/choices']; key=next(a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]);v=int(key[':answer/value'])
 return dict(matrix=matrix,rows=rows,values=vals,total=sum(vals),key=v,bank=[int(a[':answer/value']) for a in choices],position=choices.index(key),rank=sorted(int(a[':answer/value']) for a in choices).index(v))
def oracle(r):
 a=unpack(r);s=r['question'][':question/worked-solution'];eq=re.search(r'So, the answer is \$(.*?)\.\$',s)[1];lhs,rhs=eq.split('=');import ast
 # evaluate only independent integer/addition expressions
 def ev(n):
  if isinstance(n,ast.Expression):return ev(n.body)
  if isinstance(n,ast.Constant) and type(n.value)is int:return n.value
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -ev(n.operand)
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Add):return ev(n.left)+ev(n.right)
  raise ValueError(ast.dump(n))
 expected_terms='+'.join(str(v) if i==0 or v>=0 else '('+str(v)+')' for i,v in enumerate(a['values']))
 assert a['key']==a['total']==int(rhs)==ev(ast.parse(lhs,mode='eval'))
 assert lhs==expected_terms,(lhs,expected_terms)
 assert len(set(a['bank']))==5
 assert all(-9*len(a['rows'])<=b<=9*len(a['rows']) for b in a['bank'])
 return a
# Replay uses parsed ORIGINAL prompts and banks, never the package CASES parameters.
replays=[];replay_results=[];unsupported=[]
for i,q in enumerate(qs):
 matrix=[[int(x.strip()) for x in row.split('&')] for row in re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1].split('\\\\')]
 rows=[int(n)-1 for n in re.findall(r'\$(\d)\$(?:st|nd|rd|th)',q[':question/problem'].split('rows')[0])]
 params=dict(matrix=matrix,rows=rows)
 if q[':question/math-academy-id'] not in g.CASES:
  try:g.generate(seed=803+i,profile=q[':question/math-academy-id'],parameters=params,replay=True)
  except ValueError as ex:
   unsupported.append(dict(source_id=q[':question/id'],source=q,parameters=params,seed=803+i,profile=q[':question/math-academy-id'],exception=str(ex),expected_answer=sum(next(x for x in matrix[row] if x) for row in rows)))
  continue
 r=g.generate(seed=803+i,profile=q[':question/math-academy-id'],parameters=params,replay=True);a=oracle(r)
 assert sorted(a['bank'])==sorted(int(x[':answer/value']) for x in q[':question/answer-fields'][0][':answer-field/choices'])
 assert r['question'][':question/problem']==g.normalize_prose(q[':question/problem'])
 if ':question/worked-solution' in q:assert r['question'][':question/worked-solution']==g.normalize_prose(q[':question/worked-solution'])
 replays.append(r);replay_results.append(dict(source_id=q[':question/id'],math_academy_id=q[':question/math-academy-id'],answer=a['total'],full_bank=a['bank'],prompt_equal_after_normalization=True,solution_equal_after_normalization=(':question/worked-solution' in q),missing_original_key=':answer-field/correct' not in q[':question/answer-fields'][0]))
save('unsupported-source.json',unsupported);save('source-replay-records.json',replays);save('source-replay-results.json',replay_results)
# Canonical example: no bank available; reproduce mathematical task and inspect derived solution.
q=src['material']['kp'][':knowledge-point/canonical-example'];m=[[int(x.strip()) for x in row.split('&')] for row in re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1].split('\\\\')]
canonical=g.generate(seed=442,profile='q-129206',parameters={'matrix':m,'rows':[0,2,3]});assert oracle(canonical)['total']==3
save('canonical-record.json',[canonical])
profiles=sorted(g.CASES); samples=[g.generate(seed=957301+1000*i+k,profile=p) for i,p in enumerate(profiles) for k in range(6)]
save('fresh-records.json',samples)
# Controlled pairs: preserve RNG seed, profile and bank anchor, so differences reflect evidence.
base={'matrix':[[0,2,5,-1],[0,0,-3,7],[4,0,6,-2],[0,0,0,6]],'rows':[0,1]}
params=[('base',base),('leading_value',dict(matrix=[[0,3,5,-1],*copy.deepcopy(base['matrix'][1:])],rows=[0,1])),('new_earlier_nonzero',dict(matrix=[[5,2,5,-1],*copy.deepcopy(base['matrix'][1:])],rows=[0,1])),('target_rows',dict(matrix=copy.deepcopy(base['matrix']),rows=[0,2])),('trailing_value',dict(matrix=[[0,2,9,-1],*copy.deepcopy(base['matrix'][1:])],rows=[0,1])),('unselected_row',dict(matrix=[*copy.deepcopy(base['matrix'][:2]),[-9,8,7,6],copy.deepcopy(base['matrix'][3])],rows=[0,1]))]
pairs=[g.generate(seed=551,profile='q-73143',parameters=p,anchor_rank=2) for _,p in params]
save('counterfactual-records.json',pairs)
expected=[-1,0,2,6,-1,-1];pair_results=[]
for (label,p),r,k in zip(params,pairs,expected):
 a=oracle(r);assert a['total']==k
 pair_results.append(dict(case=label,parameters=p,answer=k,render_index=len(pair_results),prompt_changed=r['question'][':question/problem']!=pairs[0]['question'][':question/problem'],solution_changed=r['question'][':question/worked-solution']!=pairs[0]['question'][':question/worked-solution'],bank=a['bank']))
save('counterfactual-results.json',pair_results)
# Every eligible subset and leading position; extremes/zero sums and signed values.
boundary=[]
for n in [2,3]:
 for rows in itertools.combinations(range(4),n):
  for col in range(4):
   m=[[0]*col+[(-1 if row%2 else 1)*(row+1)]+[9]*(3-col) for row in range(4)]
   boundary.append(g.generate(seed=193+col,profile='q-73143' if n==2 else 'q-129206',parameters=dict(matrix=m,rows=list(rows))))
for val in [-9,9]:
 for n in [2,3]:boundary.append(g.generate(seed=293,profile='q-73143' if n==2 else 'q-129206',parameters=dict(matrix=[[val,0,0,0]]*4,rows=list(range(n)))))
save('boundary-records.json',boundary)
allgroups={'fresh':samples,'batch':json.load(open(E/'batch-records.json')),'counterfactual':pairs,'boundary':boundary,'replay':replays,'canonical':[canonical]}
math_results={}
for name,records in allgroups.items():
 vals=[oracle(r) for r in records];math_results[name]=dict(records=len(records),passed=len(vals),sums=dict(collections.Counter('negative' if a['total']<0 else 'positive' if a['total']>0 else 'zero' for a in vals)))
save('math-results.json',math_results)
rejections=[]
for label,kwargs in [('unsupported_difficulty',dict(level='moderate')),('wrong_profile',dict(profile='nope')),('zero_row',dict(profile='q-73143',parameters=dict(matrix=[[0]*4]*4,rows=[0,1]))),('duplicate_rows',dict(profile='q-73143',parameters=dict(matrix=base['matrix'],rows=[0,0]))),('out_of_range',dict(profile='q-73143',parameters=dict(matrix=[[10]*4]*4,rows=[0,1]))),('float',dict(profile='q-73143',parameters=dict(matrix=[[1.0]*4]*4,rows=[0,1]))),('unsorted_rows',dict(profile='q-73143',parameters=dict(matrix=base['matrix'],rows=[1,0]))),('bad_anchor',dict(anchor_rank=5))]:
 try:g.generate(**kwargs)
 except (ValueError,RuntimeError) as ex:rejections.append(dict(case=label,rejected=True,message=str(ex)))
 else:rejections.append(dict(case=label,rejected=False))
assert all(x['rejected'] for x in rejections)
assert g.generate(seed=728199)==g.generate(seed=728199)
cli=subprocess.run([sys.executable,'-B',str(P/'generator.py'),'--seed','728199','--count','12'],capture_output=True,text=True,check=True);cli_records=json.loads(cli.stdout);save('cli-records.json',cli_records)
assert len({r['generation']['parameter_fingerprint'] for r in cli_records})==12
rel=E/'relocated-package';rel.mkdir(exist_ok=True)
for f in json.load(open(P/'package.json'))['files']:shutil.copyfile(P/f,rel/f)
relout=subprocess.run([sys.executable,'-B',str(rel/'generator.py'),'--seed','728199','--count','12'],cwd=E,capture_output=True,text=True,check=True)
assert cli.stdout==relout.stdout
save('packaging-results.json',dict(python=platform.python_version(),sympy=g.sp.__version__,manifest=json.load(open(P/'package.json')),rejections=rejections,deterministic=True,cli_count=12,semantic_duplicates=0,relocation_identical=True,external_outputs='none; stdout JSON only',value_sampling_attempts_max=max(r['generation']['value_sampling_attempts'] for r in samples),package_unchanged={p.name:sha(p) for p in P.iterdir() if p.is_file()}==snapshot,command=f'{sys.executable} -B {E}/review.py'))
# Native checks: every option, including all wrong distractors. Cross-pair old mathematical answer when present.
grade_records=replays+allgroups['batch']+pairs+boundary+samples[::6]+[canonical]
cases=[]
for i,r in enumerate(grade_records):
 a=oracle(r);f=r['question'][':question/answer-fields'][0]
 cases.append(dict(label=f'oracle record {i}: sum {a["total"]}',record=r,checks=[dict(submitted_answer_id=c[':answer/id'],expected='accepted' if int(c[':answer/value'])==a['total'] else 'rejected',purpose='independent first-nonzero sum; verify every radio choice') for c in f[':answer-field/choices']]))
save('grader-input.json',cases)
save('render-records.json',allgroups['batch']+pairs+[canonical,replays[0],replays[1],replays[-1]])
(E/'initial-test-state.md').write_text('Source analysis completed before package inspection. Independent source replay (14 complete banks; one captured profile q-129207 is rejected), 336 fresh records, 44 boundaries, canonical task, controlled pairs, math, rejection, determinism and relocation checks completed. Run review.py to reproduce. Native grading, actual UI, delivery and pedagogical review remain. No repair history or preflight files exist.\n')
print(json.dumps(dict(math=math_results,packaging=json.load(open(E/'packaging-results.json')),grader_records=len(cases)),indent=2))
