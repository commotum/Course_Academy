"""Read-only, complete scalar presentation attestation at fixed EDB basis10067."""
import collections,concurrent.futures,copy,hashlib,json,sys,time
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];AUDIT=H.parent;OUT=H/'final-presentation-readback';OUT.mkdir(exist_ok=True);BASIS=10067
sys.path.insert(0,str(ROOT/'scripts'));from migrate_learner_history import connection,kw,loads
DB=connection();inputs={}
def read(path):
 path=Path(path);raw=path.read_bytes();inputs[str(path.relative_to(ROOT))]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)};return json.loads(raw)
model_path=AUDIT/'prepublication-check/model.json';model=read(model_path)
snaps=[read(AUDIT/g/f)for g,f in[('group-1','current.json'),('group-2','current.json'),('group-3','snapshot.json')]]
commits=read(AUDIT/'commits.json');plans=[];tutorial_cas={};commit_meta=[]
for name in commits:
 plan=read(AUDIT/name/'plan.json');verification=read(AUDIT/name/'verification.json');assert verification['committed'];tx=verification.get('basis_t',verification.get('basis',verification.get('db_after')))
 # Only tutorial presentation changes are needed; the supplied model already
 # embodies all exact committed question/field/answer changes.
 for p in plan.get('cas',[]):
  if p['attribute']in['tutorial/content','tutorial/title']:tutorial_cas[p['entity'],':'+p['attribute']]=p['after']
 commit_meta.append({'directory':name,'verification_basis':tx,'tutorial_cas':sum(p['attribute'].startswith('tutorial/')for p in plan.get('cas',[]))})
content=snaps[0]['contents']+[c for a in snaps[1]['activities']for c in a['contents']]+snaps[2]['content'];tutorials={}
for item in content:
 if ':tutorial/content'not in item and ':tutorial/id'not in item:continue
 e=item[':db/id'];item=copy.deepcopy(item)
 for(eid,a),v in tutorial_cas.items():
  if eid==e:
   if v is None:item.pop(a,None)
   else:item[a]=v
 if e in tutorials:assert tutorials[e]==item,('Conflicting tutorial snapshot',e)
 tutorials[e]=item
assert len(model)==7844 and len(tutorials)==242
ATTRS={'question':['question/problem','question/worked-solution'],
'field':['answer-field/key','answer-field/display-key','answer-field/type'],
'answer':['answer/value','answer/type','answer/feedback'],
'tutorial':['tutorial/content','tutorial/title']}
IDENTITY={'question':'question/id','field':'answer-field/id','answer':'answer/id','tutorial':'tutorial/id'}
SIZES={'question':40,'field':240,'answer':240,'tutorial':12}
objects={k:{}for k in ATTRS};conflicts=[]
def put(kind,obj):
 e=obj.get(':db/id');assert isinstance(e,int)and e>0,(kind,e)
 if e not in objects[kind]:objects[kind][e]=obj;return
 prev=objects[kind][e]
 for a in ATTRS[kind]:
  key=':'+a
  if (key in prev)!=(key in obj)or prev.get(key)!=obj.get(key):conflicts.append({'kind':kind,'entity':e,'attribute':a,'first_present':key in prev,'other_present':key in obj,'first':prev.get(key),'other':obj.get(key)})
for q in model:
 put('question',q)
 for f in q.get(':question/answer-fields',[]):
  put('field',f)
  for a in f.get(':answer-field/choices',[]):put('answer',a)
  if isinstance(f.get(':answer-field/correct'),dict)and ':answer/value'in f[':answer-field/correct']:put('answer',f[':answer-field/correct'])
for t in tutorials.values():put('tutorial',t)
assert not conflicts,conflicts[:5]
# Resolve ident-only new-answer type payloads independently at the same basis.
idents=sorted({v[':db/ident']for kind in objects for obj in objects[kind].values()for a in ATTRS[kind]if isinstance(v:=obj.get(':'+a),dict)and ':db/ident'in v})
rows=DB.query('[:find ?ident ?e :in $ [?ident ...] :where [?e :db/ident ?ident]]',[[kw(x)for x in idents]],OUT,'enum-ident-resolution',BASIS)
ENUMS={str(i):e for i,e in rows};assert set(ENUMS)==set(idents),(ENUMS,idents)
def value(v):
 if isinstance(v,dict):
  if ':db/id'in v:
   if ':db/ident'in v:assert ENUMS[str(v[':db/ident'])]==v[':db/id'],v
   return v[':db/id']
  if ':db/ident'in v:return ENUMS[str(v[':db/ident'])]
  raise ValueError(('Unexpected presentation map',v))
 return v
expected={};counts={};jobs=[]
for kind,obs in objects.items():
 for e,obj in obs.items():
  for a in ATTRS[kind]:expected[e,a]={'present':':'+a in obj,'value':value(obj[':'+a])if ':'+a in obj else None}
 ids=sorted(obs);counts[kind]={'entities':len(obs),'attributes':ATTRS[kind],'expected_present':sum(':'+a in o for o in obs.values()for a in ATTRS[kind]),'expected_absent':sum(':'+a not in o for o in obs.values()for a in ATTRS[kind])}
 for start in range(0,len(ids),SIZES[kind]):jobs.append((kind,start,ids[start:start+SIZES[kind]]))
input_manifest={'basis':BASIS,'inputs':inputs,'model_path':str(model_path.relative_to(ROOT)),'model_sha256':inputs[str(model_path.relative_to(ROOT))]['sha256'],'counts':counts,'expected_scalar_presence_pairs':len(expected),'commits':commit_meta,'tutorial_cas_applied':len(tutorial_cas),'database_writes':0};(OUT/'input-manifest.json').write_text(json.dumps(input_manifest,indent=2,default=str)+'\n');(OUT/'entity-inventory.json').write_text(json.dumps({k:sorted(v)for k,v in objects.items()},indent=2)+'\n');print(json.dumps({'basis':BASIS,'counts':counts,'jobs':len(jobs),'pairs':len(expected)},indent=2),flush=True)
def worker(job):
 kind,start,ids=job;attrs=' '.join(':'+a for a in ATTRS[kind]);query='[:find (pull ?e [:db/id '+attrs+']) :in $ [?e ...] :where [?e :'+IDENTITY[kind]+' _]]';name=kind+'-'+str(start);p=OUT/(name+'.edn')
 try:
  rows=loads(p.read_text())if p.exists()else DB.query(query,[ids],OUT,name,BASIS);got={r[0][':db/id']:r[0]for r in rows};mismatches=[]
  for e in ids:
   obj=got.get(e)
   if obj is None:mismatches.append({'kind':kind,'entity':e,'attribute':'entity','expected_present':True,'actual_present':False});continue
   for a in ATTRS[kind]:
    want=expected[e,a];present=':'+a in obj;actual=value(obj[':'+a])if present else None
    if want['present']!=present or want['value']!=actual:mismatches.append({'kind':kind,'entity':e,'attribute':a,'expected_present':want['present'],'actual_present':present,'expected':want['value'],'actual':actual})
  return {'name':name,'kind':kind,'entities':len(ids),'rows':len(rows),'pairs':len(ids)*len(ATTRS[kind]),'mismatches':mismatches,'actual_file_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 except Exception as ex:return {'name':name,'kind':kind,'error':repr(ex),'entities':len(ids),'pairs':len(ids)*len(ATTRS[kind])}
results=[];started=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 futures=[pool.submit(worker,j)for j in jobs]
 for f in concurrent.futures.as_completed(futures):
  r=f.result();results.append(r)
  if r.get('mismatches')or r.get('error'):print('MISMATCH/ERROR',json.dumps(r,ensure_ascii=False,default=str)[:4000],flush=True)
  if len(results)%25==0:print('completed',len(results),'/',len(jobs),'mismatches',sum(len(x.get('mismatches',[]))for x in results),'elapsed',round(time.monotonic()-started,1),flush=True)
  (OUT/'progress.json').write_text(json.dumps({'basis':BASIS,'completed_batches':len(results),'total_batches':len(jobs),'errors':[x for x in results if x.get('error')],'mismatches':[m for x in results for m in x.get('mismatches',[])]},indent=2,default=str)+'\n')
changed_inputs=[]
for name,info in inputs.items():
 path=ROOT/name
 if hashlib.sha256(path.read_bytes()).hexdigest()!=info['sha256']:changed_inputs.append(name)
errors=[x for x in results if x.get('error')];mismatches=[m for x in results for m in x.get('mismatches',[])];report={**input_manifest,'passed':not errors and not mismatches and not changed_inputs,'batch_count':len(results),'query_errors':errors,'mismatches':mismatches,'input_files_changed_during_run':changed_inputs,'checked_presence_pairs':sum(r['pairs']for r in results if not r.get('error')),'elapsed_seconds':round(time.monotonic()-started,2),'batch_evidence':sorted(results,key=lambda r:r['name']),'scope':'Every question problem/solution; every active field key, optional display-key and type; every owned choice value/type/optional feedback including noncanonical historical blank responses; all242tutorial contents and titles. Exact absent/present and empty-string distinctions retained. Enum refs compared by numeric EID after same-basis ident resolution. No normalization or acceptance of changed values. No renderer/learner write invoked.'};(OUT/'verification.json').write_text(json.dumps(report,indent=2,default=str)+'\n');print('FINAL',json.dumps({k:report[k]for k in['basis','passed','checked_presence_pairs','mismatches','query_errors','input_files_changed_during_run','elapsed_seconds']},default=str),flush=True)
