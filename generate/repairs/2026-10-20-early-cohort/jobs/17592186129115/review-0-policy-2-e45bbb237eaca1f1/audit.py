import sys,json,pathlib,re,itertools,hashlib,platform,importlib.util,copy,subprocess,collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent; B=E.parent; W=B/'workspace'; R=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,x): (E/n).write_text(json.dumps(x,indent=2)+'\n')
def hashpkg(): return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in W.iterdir() if p.is_file()}
save('package-before.json',hashpkg());sys.path.insert(0,str(W));import generator as g
s=json.load(open(B/'source/source.json'));inv=json.load(open(B/'source/inventory.json'))
def matrix(t):
 t=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',t,re.S)[1];return [[int(v.strip()) for v in row.split('&')] for row in t.split('\\\\')]
def coords(t): return [[int(a)-1,int(b)-1] for a,b in re.findall(r'a\}?_\{([1-4])([1-4])\}',t)]
def ref(m,cs):
 out=[r[:] for r in m]
 for i,j in cs:out[i][j]=0
 prev=-1;zero=False
 for r in out:
  lead=next((i for i,v in enumerate(r) if v),None)
  if lead is None:zero=True
  elif zero or lead<=prev:return False
  else:prev=lead
 return True
def minimum(m):
 cells=[(i,j) for i in range(4) for j in range(4) if m[i][j]]
 for k in range(4):
  hits=[list(map(list,c)) for c in itertools.combinations(cells,k) if ref(m,c)]
  if hits:return hits
 return []
def correct(r):
 f=r['question'][':question/answer-fields'][0];return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
source=[]
for q in s['material']['kp'][':knowledge-point/questions']:
 m=matrix(q[':question/problem']);f=q[':question/answer-fields'][0];bank=[coords(a[':answer/value']) for a in f[':answer-field/choices']];mins=minimum(m)
 expected=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
 row={'source_id':q[':question/id'],'matrix':m,'bank':bank,'expected':expected,'independent_good':[i for i,c in enumerate(bank) if ref(m,c)],'global_minima':mins,'parameters':{'matrix':m,'bank':bank}}
 try:
  out=g.generate('moderate',9100,parameters=row['parameters']);row.update(status='accepted_changed_contract',record=out)
 except Exception as ex:row.update(status='rejected',error=str(ex))
 source.append(row)
save('source-replay.json',source)
canon=s['material']['kp'][':knowledge-point/canonical-example'];save('canonical-check.json',{'id':canon[':question/id'],'matrix':matrix(canon[':question/problem']),'stated_replacements':[[2,1],[3,1],[3,2]],'echelon_after':ref(matrix(canon[':question/problem']),[[2,1],[3,1],[3,2]]),'answer_bank':'absent from source'})
records=[g.generate('moderate',seed) for seed in range(702311,702343)];batch=json.load(open(B/'samples.json'));save('independent-samples.json',records);save('batch-records.json',batch)
math=[]
for group,rs in [('independent',records),('batch',batch)]:
 for r in rs:
  q=r['question'];m=matrix(q[':question/problem']);bank=[coords(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']];ci=correct(r);mins=minimum(m)
  sols=re.findall(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',q[':question/worked-solution'],re.S);after=matrix(sols[-1]);want=[[0 if [i,j] in bank[ci] else v for j,v in enumerate(row)] for i,row in enumerate(m)]
  math.append({'group':group,'seed':r['generation']['seed'],'good':[i for i,c in enumerate(bank) if ref(m,c)],'key':ci,'minima':mins,'solution_matches':after==want,'passed':[i for i,c in enumerate(bank) if ref(m,c)]==[ci] and len(mins)==1 and sorted(bank[ci])==mins[0] and after==want})
save('math-results.json',math)
# Controlled dependency pair: try changing exactly one zero/nonzero cell while preserving all five choices.
cf=None
for r in records:
 p=r['generation']['parameters'];ci=correct(r)
 for i,j in itertools.product(range(4),repeat=2):
  pp=copy.deepcopy(p);pp['matrix'][i][j]=0 if pp['matrix'][i][j] else 1
  try:rr=g.generate('moderate',r['generation']['seed'],parameters=pp)
  except ValueError:continue
  if correct(rr)!=ci:cf=[r,rr];break
 if cf:break
# fallback: hold matrix numbers and four candidate sets fixed; change cell and replace one distractor only if necessary.
if cf is None:
 for r in records:
  p=r['generation']['parameters']
  for i,j in itertools.product(range(4),repeat=2):
   pp=copy.deepcopy(p);pp['matrix'][i][j]=0 if pp['matrix'][i][j] else 1;mins=minimum(pp['matrix'])
   if len(mins)!=1 or mins[0]==sorted(p['bank'][correct(r)]) or not mins[0]:continue
   valid=[b for b in pp['bank'] if all(pp['matrix'][a][b_] for a,b_ in b) and not ref(pp['matrix'],b)]
   if len(valid)<4:continue
   pp['bank']=valid[:4]+[mins[0]]
   try:rr=g.generate('moderate',r['generation']['seed'],parameters=pp)
   except ValueError:continue
   cf=[r,rr];break
  if cf:break
assert cf,'No dependency pair found'
irr=copy.deepcopy(cf[0]['generation']['parameters']);cell=next((i,j) for i in range(4) for j in range(4) if irr['matrix'][i][j]);irr['matrix'][cell[0]][cell[1]]*= -2
ir=g.generate('moderate',cf[0]['generation']['seed'],parameters=irr);save('counterfactual-records.json',cf+[ir]);save('counterfactual-results.json',{'relevant_before':cf[0]['generation']['parameters'],'relevant_after':cf[1]['generation']['parameters'],'before_answer':coords(cf[0]['question'][':question/answer-fields'][0][':answer-field/choices'][correct(cf[0])][':answer/value']),'after_answer':coords(cf[1]['question'][':question/answer-fields'][0][':answer-field/choices'][correct(cf[1])][':answer/value']),'irrelevant_cell':cell,'irrelevant_response_preserved':correct(ir)==correct(cf[0]),'render_file':'render-records.json','grading_file':'grader-results.json'})
cases=[]
for r in batch+records[:4]+cf+[ir]:
 f=r['question'][':question/answer-fields'][0];ci=correct(r)
 cases.append({'label':r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==ci else 'rejected','purpose':'independent enumeration of all offered coordinate operations'} for i,a in enumerate(f[':answer-field/choices'])]})
save('grader-input.json',cases);save('render-records.json',batch+cf+[ir])
# Stored generated records only, retaining complete captured question and generation metadata.
generated=[];inventory_summary=[]
for q in inv['questions']:
 inventory_summary.append({'id':q.get(':question/id'),'entity_id':q.get(':db/id'),'keys':list(q),'generated':any('generation' in k or 'generator' in k for k in q)})
 if any('generation' in k or 'generator' in k for k in q):generated.append(q)
save('inventory-inspection.json',{'basis':inv['basis'],'questions':inventory_summary,'generated_records':generated,'limitations':'No seed reproduction claimed until captured generation metadata is inspected. Source originals are not classified as generated.'})
save('generated-records.json',generated);save('affected-inventory.json',{'affected_questions':[]})
cat=json.load(open(W/'catalogue.json'));save('sampling-summary.json',{'catalogue_roles':len(cat),'catalogue_masks':sum(len(r['masks']) for r in cat),'target_counts':dict(collections.Counter(len(r['targets']) for r in cat)),'sample_target_counts':dict(collections.Counter(len(r['generation']['parameters']['bank'][correct(r)]) for r in records)),'batch_target_counts':dict(collections.Counter(len(r['generation']['parameters']['bank'][correct(r)]) for r in batch)),'sample_correct_positions':dict(collections.Counter(correct(r) for r in records)),'batch_correct_positions':dict(collections.Counter(correct(r) for r in batch))})
save('runtime-results.json',{'python_actual':platform.python_version(),'manifest':json.load(open(W/'package.json')),'deterministic':g.generate('moderate',702311)==records[0],'package_hashes_before':hashpkg(),'repair_history_exists':(B/'repair-history.json').exists(),'repair_preflight_exists':(B/'repair-preflight.json').exists()})
print(json.dumps({'source_statuses':dict(collections.Counter(x['status'] for x in source)),'source_key_failures':sum(x['independent_good']!=[x['expected']] for x in source),'math_cases':len(math),'math_failures':sum(not x['passed'] for x in math),'controlled_pair':cf[0]['generation']['seed'],'inventory_generated':len(generated),'summary':json.load(open(E/'sampling-summary.json'))}))
(E/'session-state.md').write_text('Independent source reconstruction saved before package read. Completed all 15 source-bank replay attempts, 32 fresh seeds plus exact 5-record batch math audit, controlled relevant/irrelevant records, captured inventory inspection. Source failures: see source-replay.json. Next: actual grader, renderer, delivery and final evidence report.\n')
