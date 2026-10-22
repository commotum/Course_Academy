import os,sys,json,re,hashlib,importlib.util,random,shutil,subprocess,platform
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent
J=E.parent; W=J/'workspace'; R=Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(W));sp=importlib.util.spec_from_file_location('gen',W/'17592186124629.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def digest():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
save('package-hashes-before.json',digest())
def val(f):
 a=f[':answer-field/correct']; aid=a[1] if isinstance(a,list) else a[':answer/id']
 return next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==aid)
def bits(r):
 fs=r['question'][':question/answer-fields']
 return [val(f)=='true' for f in fs] if len(fs)==3 else [bool(re.search(r'\b'+x+r'\b',val(fs[0]))) for x in ['I','II','III']]
def norm(s):
 for t in [r'\operatorname',r'\textrm',r'\text',r'\mathbb']:s=s.replace(t,'')
 return re.sub(r'[{}$\s]','',s).replace('\\','').replace('**','')
def holds(s,n,rank):
 s=norm(s)
 if 'hasnobasis' in s:return False
 if 'hasabasis' in s:return True
 if 'invertible' in s or 'inverse' in s:return (rank<n) if ('notinvertible' in s or 'noinverse' in s) else rank==n
 if 'det(A)' in s:return (rank==n) if 'ne0' in s else rank<n
 if 'rank(A)' in s or 'dim(Col(A))' in s:
  if '<' in s:return rank<int(s.split('<')[-1])
  return rank==int(s.split('=')[-1])
 if 'pivotcolumns' in s:
  if 'Allcolumns' in s or 'allcolumns' in s:return rank==n
  m=re.search(r'(\d+)pivot',s);assert m,s
  return rank<int(m[1]) if ('fewerthan' in s or 'lessthan' in s) else rank==int(m[1])
 if 'Col(A)' in s:
  if 'subsetneq' in s or '⊂' in s or 'neR' in s:return rank<n
  m=re.search(r'R\^?(\d+)',s);assert m,s
  return int(m[1])==n and rank==n
 if 'nullity(A)' in s or 'dim(Null(A))' in s or 'hasdimensionzero' in s:return rank<n if ('>0' in s or 'ne0' in s) else rank==n
 if 'Null(A)' in s:
  if 'ne0' in s:return rank<n
  if 'R^' in s:return rank==0
  return rank==n
 if 'Ax=0' in s:return rank==n if ('onlythetrivial' in s or 'nonon-trivial' in s) else rank<n
 raise ValueError(s)
def visible(r):
 q=r['question'];pr=q[':question/problem'];m=re.search(r'\$([n0-9]+)\\times',pr);assert m,pr
 n=int(m[1]) if m[1]!='n' else 4
 text=pr.replace('$n$',f'${n}$').replace('{n}',str(n)).replace('=n',f'={n}').replace('<n',f'<{n}')
 premise=re.split(r',?\$?\s*then',text.split('matrix and ',1)[-1],maxsplit=1)[0] if 'matrix and ' in text else '$A$ is invertible'
 # source has comma inside math and invertible matrix phrasing
 premise=premise.replace('invertible,','invertible')
 ranks=[k for k in range(n+1) if holds(premise,n,k)]
 assert ranks,(premise,n)
 fs=q[':question/answer-fields'];ss=[f[':answer-field/key'] for f in fs] if len(fs)==3 else re.findall(r'(?:^|\n)(?:I|II|III)\. (.*)',pr)
 assert len(ss)==3,ss
 ans=[]
 for s in ss:
  s=s.replace('$n$',f'${n}$').replace('{n}',str(n)).replace('=n',f'={n}').replace('<n',f'<{n}')
  ans.append(all(holds(s,n,k) for k in ranks))
 return ans
src=json.load(open(J/'source/source.json'))['material']['kp'][':knowledge-point/questions']
replays=[];replay_report=[]
for q in src:
 sid=q[':question/math-academy-id']
 if sid not in g.CASES:continue
 r=g.generate(template=sid,parameters={'premise':'replay'},seed=911);replays.append(r)
 old=q[':question/answer-fields'];new=r['question'][':question/answer-fields']
 eq=all(a[':answer-field/key']==b[':answer-field/key'] and [c[':answer/value'] for c in a[':answer-field/choices']]==[c[':answer/value'] for c in b[':answer-field/choices']] and a[':answer-field/correct'][':answer/value']==val(b) for a,b in zip(old,new))
 assert eq; assert g.normalize_prose(q[':question/problem'])==r['question'][':question/problem']
 replay_report.append({'source_id':q[':question/id'],'template':sid,'prompt_and_complete_bank_match':eq,'choices':sum(len(f[':answer-field/choices']) for f in new),'correction':'nonzero-nullity conditional quotes' if sid=='q-141342' else 'theorem reflow only'})
save('source-replays.json',replays);save('source-replay-report.json',{'cases':replay_report,'unsupported':['q-47586 (missing answer, solution, difficulty; bank omits correct III only)'],'canonical':'no answer fields; same trivial-null-space premise and theorem reasoning exercised in decision sample'})
rng=random.Random(763019);rows=[]
for sid in sorted(g.CASES):
 for mask in g.masks(sid):
  choices=[p for p in g.domain(sid) if p['truths']==mask]
  p=rng.choice(choices);rows.append(g.generate(seed=rng.randrange(10**9),template=sid,parameters=p))
save('independent-samples.json',rows)
base={'premise':'decision','invertible':True,'hypothesis':'rank','truths':[True,False,True]}
pairs=[g.generate(seed=319,template='q-47599',parameters=p) for p in [base,{**base,'truths':[False,False,True]},{**base,'hypothesis':'nullity'},{**base,'invertible':False,'truths':[False,True,False]}]]
save('counterfactual-records.json',pairs)
batch=json.load(open(E/'runner-batch.json'));allrows=replays+rows+pairs+batch
math=[]
for i,r in enumerate(allrows):
 try:
  expected=visible(r); actual=bits(r)
  assert expected==actual,(expected,actual)
  math.append({'index':i,'id':r['question'][':question/id'],'status':'passed','independent_truths':expected})
 except Exception as e:math.append({'index':i,'id':r['question'][':question/id'],'status':'failed','error':str(e)})
save('math-results.json',math)
checks=[]
for i,r in enumerate(allrows):
 tests=[]
 for j,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   tests.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==val(f) else 'rejected','purpose':'independently evaluate proposition/subset; exercise each owned correct and distractor choice'})
 checks.append({'label':str(i),'record':r,'checks':tests})
save('native-input.json',checks)
save('render-records.json',batch+pairs)
print(json.dumps({'replays':len(replays),'samples':len(rows),'pairs':len(pairs),'math_failures':[x for x in math if x['status']=='failed'][:8],'native_checks':sum(len(c['checks']) for c in checks)}))
