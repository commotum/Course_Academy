import json, re, sys, importlib.util, pathlib, hashlib, copy, collections, subprocess
ROOT=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PKG=ROOT.parent/'workspace'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('candidate',PKG/'17592186100988.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,x): (ROOT/name).write_text(json.dumps(x,indent=2))
def load(name):return json.loads((ROOT/name).read_text())
def identify(q):
 text=q[':question/problem'];m=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',text,re.S)
 a=[[int(v.strip()) for v in row.split('&')] for row in m[1].split('\\\\')]
 ix=re.search(r'\$\{?([a-z])\}?_\{(\d)(\d)\}',text);i,j=int(ix[2]),int(ix[3]);v=a[i-1][j-1] if 1<=i<=len(a) and 1<=j<=len(a[0]) else None
 return a,i,j,'No such entry' if v is None else str(v)
def correct(q):
 f=q[':question/answer-fields'][0]; ref=f.get(':answer-field/correct');uid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1] if ref else None
 return next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==uid),None)
def norm(t):
 return re.sub(r'\s+','',t.replace('[\\begin{aligned}','\\begin{bmatrix}').replace('\\end{aligned}]','\\end{bmatrix}'))
def ty(x):return x[':db/ident'] if isinstance(x,dict) else x
manifest=load('../workspace/package.json')
save('package-before.json',{p:hashlib.sha256((PKG/p).read_bytes()).hexdigest() for p in manifest['files']+['package.json']})
src=load('../source/source.json');source_records=[];replay=[]
for q in src['material']['kp'][':knowledge-point/questions']:
 s=q[':question/math-academy-id'];r=g.generate('easy',profile='raw:'+s);source_records.append(r);rq=r['question'];f=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
 result={'source_id':q[':question/id'],'profile':'raw:'+s,'prompt_equal':norm(q[':question/problem'])==norm(rq[':question/problem']),'solution_equal':norm(q.get(':question/worked-solution',''))==norm(rq.get(':question/worked-solution','')),'bank_equal':sorted((ty(a[':answer/type']),a[':answer/value']) for a in f[':answer-field/choices'])==sorted((ty(a[':answer/type']),a[':answer/value']) for a in rf[':answer-field/choices']),'field_equal':ty(f[':answer-field/type'])==ty(rf[':answer-field/type']),'key_equal':correct(q)==correct(rq),'independent_answer':identify(q)[3]}
 replay.append(result)
canonical={'matrix':[[-1,1,2,1],[0,1,-3,-1]],'i':2,'j':3,'letter':'A'}
try: r=g.generate('easy',parameters=canonical,profile='blank'); canonical_result={'result':'accepted','record':r}
except Exception as e: canonical_result={'result':'rejected','error':str(e)}
save('source-records.json',source_records);save('source-replay.json',{'command':'python review.py','practice':replay,'canonical':{'source_id':'622baf41-fe35-55ee-bfc6-f1e6a2cb089a','parameters':canonical,**canonical_result}})
samples=[g.generate('easy',seed=s) for s in range(731100,731160)]
# Deterministic boundary coverage without duplicate distractor rejection.
boundaries=[]
for m,n in [(2,4),(3,2)]:
 for i in range(1,m+1):
  for j in range(1,n+1):
   a=[[((row*n+col)%19)-9 for col in range(n)] for row in range(m)]
   boundaries.append(g.generate('easy',seed=820001,parameters={'matrix':a,'i':i,'j':j,'letter':'Z'},profile='blank'))
save('samples.json',samples);save('boundary-records.json',boundaries);batch=load('../samples.json');save('batch.json',batch)
# Controlled target changes in both formats, irrelevant labels and non-target cells.
p={'matrix':[[1,2,3],[4,5,6]],'i':1,'j':2,'letter':'A'}
pairs=[];pair_checks=[]
for profile in ['blank','location_no_entry']:
 base=g.generate('easy',seed=981,profile=profile,parameters=p)
 for kind,change in [('relevant',{'i':2}),('irrelevant',{'letter':'Y'}),('irrelevant',{'matrix':[[1,2,8],[4,5,6]]})]:
  pp=copy.deepcopy(p);pp.update(change);after=g.generate('easy',seed=981,profile=profile,parameters=pp)
  pairs.extend([base,after]);pair_checks.append({'profile':profile,'kind':kind,'change':change,'before_index':len(pairs)-2,'after_index':len(pairs)-1,'before_answer':identify(base['question'])[3],'after_answer':identify(after['question'])[3],'prompt_changed':base['question'][':question/problem']!=after['question'][':question/problem'],'solution_changed':base['question'][':question/worked-solution']!=after['question'][':question/worked-solution']})
# Out of bounds vs valid holding the matrix fixed (profile needs to follow existence).
base=g.generate('easy',981,profile='location_no_entry',parameters=p);pp=copy.deepcopy(p);pp['i']=3
after=g.generate('easy',981,profile='overflow_locations',parameters=pp);pairs.extend([base,after]);pair_checks.append({'profile':'valid-to-overflow','kind':'relevant','change':{'i':3},'before_index':len(pairs)-2,'after_index':len(pairs)-1,'before_answer':'2','after_answer':'No such entry'})
# New fixed-layout tests for the changed existence rule.
for style in ['inline_radio','inline_no_entry_radio','display_radio','display_should_radio','display_noperiod_radio']:
 base=g.generate('easy',seed=1167,template=style,profile='location_no_entry',parameters=p)
 for kind,change,profile in [('relevant',{'i':3},'overflow_locations'),('relevant',{'j':4},'overflow_locations'),('relevant',{'i':2},'location_no_entry'),('irrelevant',{'matrix':[[1,2,8],[4,5,6]]},'location_no_entry')]:
  pp=copy.deepcopy(p);pp.update(change);after=g.generate('easy',seed=1167,template=style,profile=profile,parameters=pp)
  pairs.extend([base,after]);pair_checks.append({'profile':style,'kind':kind,'change':change,'before_index':len(pairs)-2,'after_index':len(pairs)-1,'before_answer':identify(base['question'])[3],'after_answer':identify(after['question'])[3]})
save('counterfactual-records.json',pairs);save('counterfactual-results.json',pair_checks)
math_results=[];grading=[]
for name,records in [('sample',samples),('boundary',boundaries),('batch',batch),('pair',pairs)]:
 for ix,r in enumerate(records):
  q=r['question'];a,i,j,v=identify(q);f=q[':question/answer-fields'][0];vs=[a[':answer/value'] for a in f[':answer-field/choices']];sol=q[':question/worked-solution']
  solution_ok=('no such entry' in sol.lower()) if v=='No such entry' else ('='+v+'.$') in sol
  math_results.append({'set':name,'index':ix,'expected':v,'actual':correct(q),'unique_bank':len(vs)==len(set(vs)),'solution_ok':solution_ok,'passed':v==correct(q) and len(vs)==len(set(vs)) and solution_ok})
  checks=[]
  if f[':answer-field/type'].endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==v else 'rejected','purpose':'independently parsed row/column answer'} for a in f[':answer-field/choices']]
  elif name in ('pair','batch') or ix<6:
   checks=[{'submitted':str(vv),'expected':ex,'purpose':purpose} for vv,ex,purpose in [(v,'accepted','literal'),(str(int(v)*2)+'/2','accepted','equivalent fraction'),(v+'.0','accepted','equivalent decimal'),(str(int(v)+1),'rejected','nearby wrong integer'),('-'+v if int(v)>0 else str(abs(int(v))) if int(v)<0 else '1','rejected','sign or zero confusion')]]
  if checks:grading.append({'label':f'{name}-{ix}','record':r,'checks':checks})
save('math-results.json',math_results);save('grader-input.json',grading)
# Reject invalid explicit inputs, not a silent repair.
guards=[]
for key,change in [('zero_index',{'i':0}),('negative_index',{'j':-1}),('ragged',{'matrix':[[1,2,3],[4,5]]}),('duplicate_radio',{'matrix':[[1,1,1],[1,1,1]]}),('beyond_boundary',{'i':4})]:
 pp=copy.deepcopy(p);pp.update(change)
 try: g.generate('easy',parameters=pp,profile='location_no_entry');out='accepted'
 except ValueError as e:out=str(e)
 guards.append({'case':key,'parameters':pp,'result':out})
save('guard-results.json',guards)
# Compact render includes actual batch and every controlled prompt/solution.
render=batch+list({r['question'][':question/id']:r for r in pairs}.values())
save('render-records.json',render)
inv=load('../source/inventory.json');save('inventory-analysis.json',{'basis':inv['basis'],'questions':[{'id':q[':question/id'],'entity_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'generation_fields':{k:v for k,v in q.items() if 'generat' in k or 'retir' in k},'has_key':correct(q) is not None,'answer':identify(q)[3]} for q in inv['questions']],'conclusion':'All seven captured records are original source questions; no stored generated records are present. Do not designate originals as generated. Missing keys on two originals do not establish a generated-pool defect.'})
save('affected-inventory.json',{'affected_questions':[]})
print(json.dumps({'source_replay':replay,'canonical':canonical_result['result'],'samples':len(samples),'boundaries':len(boundaries),'math_failures':[x for x in math_results if not x['passed']],'batch':[{k:r['generation'][k] for k in ('seed','template','profile','task_components')} for r in batch],'render_records':len(render)},indent=2))
