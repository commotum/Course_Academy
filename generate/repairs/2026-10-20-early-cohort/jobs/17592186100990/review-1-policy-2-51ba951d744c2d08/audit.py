import json,sys,re,importlib.util,copy,pathlib,hashlib,platform,subprocess,collections
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
PKG=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else JOB/'workspace'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reviewed',PKG/'17592186100990.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,x): (ROOT/name).write_text(json.dumps(x,indent=2)+'\n')
def key(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def coords(v):
 m=re.search(r'_\{(\d)(\d)\}',v);return tuple(map(int,m.groups()))
def facts(r):
 q=r['question'];p=q[':question/problem'];body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',p,re.S)[1];rows=[r.split('&') for r in body.split(r'\\')]
 hits=[(i,j) for i,row in enumerate(rows,1) for j,v in enumerate(row,1) if '\\boxed{' in v]
 assert len(hits)==1,(q[':question/id'],hits)
 i,j=hits[0];letter=re.search(r'\$([A-Z])\$',p)
 if not letter:letter=re.search(r'\b([A-Z])=',p)
 letter=letter[1].lower(); errors=[]
 for f in q[':question/answer-fields']:
  k=key(f)
  if f[':answer-field/key']=='selection' or '_' in k:
   if coords(k)!=(i,j) or letter not in k:errors.append('incorrect symbolic key')
  elif int(k)!=({'field-1':i,'field-2':j}[f[':answer-field/key']]):errors.append('incorrect numeric key')
 sol=q[':question/worked-solution']
 if not re.search(r'intersection of the \$'+str(i)+r'\$(?:st|nd|rd|th) row and \$'+str(j)+r'\$(?:st|nd|rd|th) column',sol):errors.append('stale explanation position')
 return {'id':q[':question/id'],'shape':[len(rows),len(rows[0])],'position':[i,j],'letter':letter,'errors':errors}
source=json.load(open(JOB/'source/source.json'));qs=source['material']['kp'][':knowledge-point/questions']
# Infer signatures from ORIGINAL source banks, not generator metadata.
signatures={}
for q in qs:
 f=q[':question/answer-fields'][0]
 if f[':answer-field/type'][':db/ident'].endswith('/radio'):
  cs=[coords(a[':answer/value']) for a in f[':answer-field/choices']];mi=min(x for x,y in cs);mj=min(y for x,y in cs)
  correct=f.get(':answer-field/correct',{}).get(':answer/value')
  if correct is None:correct={'q-13498':'a_{12}','q-13503':'b_{33}'}[q[':question/math-academy-id']]
  ci,cj=coords(correct);sig=tuple(sorted((i-mi,j-mj) for i,j in cs));signatures[sig]=(ci-mi,cj-mj,q[':question/math-academy-id'])
def shortcut(records):
 out=[]
 for r in records:
  f=r['question'][':question/answer-fields'][0]
  if not str(f[':answer-field/type']).endswith('/radio'):continue
  cs=[coords(a[':answer/value']) for a in f[':answer-field/choices']];mi=min(x for x,y in cs);mj=min(y for x,y in cs);sig=tuple(sorted((i-mi,j-mj) for i,j in cs))
  role=signatures.get(sig)
  if role:
   pred=(mi+role[0],mj+role[1]);out.append({'id':r['question'][':question/id'],'recognizable_bank':role[2],'prediction':pred,'correct':pred==coords(key(f)),'choices':[a[':answer/value'] for a in f[':answer-field/choices']]})
 return out
batch=json.load(open(sys.argv[2] if len(sys.argv)>2 else JOB/'samples.json'));save('batch.json',batch)
samples=[g.generate_easy(seed=s) for s in range(114700,114740)]
boundaries=[]
for m,n in [(2,2),(2,3),(3,3),(3,4),(4,2),(4,4)]:
 for i in range(1,m+1):
  for j in range(1,n+1):boundaries.append(g.generate_easy(seed=71,template='two_indices',parameters={'matrix':[[0]*n for _ in range(m)],'i':i,'j':j,'letter':'Z'}))
save('samples.json',samples);save('boundaries.json',boundaries)
replays=[];replay_results=[]
for q in qs:
 sid=q[':question/math-academy-id']
 try:
  r=g.generate_easy(seed=73,profile='completed:'+sid);replays.append(r);f=facts(r)
  expected={(x[':answer-field/key'],x[':answer-field/type'][':db/ident']):sorted(a[':answer/value'] for a in x[':answer-field/choices']) for x in q[':question/answer-fields']}
  actual={(x[':answer-field/key'],x[':answer-field/type']):sorted(a[':answer/value'] for a in x[':answer-field/choices']) for x in r['question'][':question/answer-fields']}
  replay_results.append({'source':sid,'id':q[':question/id'],'bank_match':expected==actual,'math':f,'eligible':r['generation']['eligible_for_learning']})
 except Exception as e: replay_results.append({'source':sid,'id':q[':question/id'],'error':str(e)})
save('source-replays.json',replays);save('source-replay-results.json',replay_results)
p={'matrix':[[1,2,3,4],[5,6,7,8],[0,0,0,0]],'i':1,'j':1,'letter':'A'}
pairs=[]
for t in ['inline_radio','display_radio','two_indices','notation_blank']:
 kwargs={'template':t,'profile':'q-13489' if t.endswith('radio') else 'blank'}
 for tag,params in [('before',p),('relevant',dict(p,i=2,j=2)),('irrelevant',dict(p,matrix=[[9,8,7,6],[5,4,3,2],[1,1,1,1]]))]:
  r=g.generate_easy(seed=41,parameters=params,**kwargs);pairs.append(r)
save('counterfactual-records.json',pairs)
all_records=samples+boundaries+replays+pairs+batch
save('math-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python audit.py [package_root] [candidate-records.json]','results':[facts(r) for r in all_records]})
save('shortcut-results.json',{'method':'Normalize each visible five-choice coordinate set by its minimum row and column; match an original source signature and choose its relative correct location. Reads choices only.','source_signatures':[{'signature':s,'correct_role':v} for s,v in signatures.items()],'samples':shortcut(samples),'batch':shortcut(batch),'counts':dict(collections.Counter(r['generation']['profile'] for r in samples))})
invalid=[]
for name,changes in [('row_zero',{'i':0}),('row_outside',{'i':4}),('ragged',{'matrix':[[1],[2,3]]}),('float',{'matrix':[[1.0]*4]*3}),('lower_label',{'letter':'a'}),('too_large_entry',{'matrix':[[10]*4]*3})]:
 try:g.generate_easy(template='two_indices',parameters=dict(p,**changes));invalid.append({'case':name,'rejected':False})
 except ValueError as e:invalid.append({'case':name,'rejected':True,'message':str(e)})
manifest=json.load(open(PKG/'package.json'));save('package-hashes.json',{str(x.relative_to(PKG)):hashlib.sha256(x.read_bytes()).hexdigest() for x in PKG.rglob('*') if x.is_file()})
save('packaging-results.json',{'manifest_dependencies':manifest['dependencies'],'actual_dependencies':{'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}},'deterministic':samples==[g.generate_easy(seed=s) for s in range(114700,114740)],'batch_seed_replay':batch==g.generate_batch('easy',3782988951,5),'invalid_parameters':invalid,'external_assets':'No generated assets; matrices rendered as TeX.'})
save('render-records.json',pairs+batch+[r for r in replays if r['generation']['template']=='notation_blank'])
print(json.dumps({'samples':len(samples),'boundaries':len(boundaries),'replay':replay_results,'shortcut_samples':[len(shortcut(samples)),sum(x['correct'] for x in shortcut(samples))],'shortcut_batch':shortcut(batch)},indent=2))
