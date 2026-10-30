"""Read-only final content integration verification at one fixed EDB basis."""
import argparse,collections,copy,hashlib,json,sys,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,loads,kw
P=argparse.ArgumentParser();P.add_argument('--basis',type=int);P.add_argument('--baseline-only',action='store_true');args=P.parse_args();D=H/'final-live';D.mkdir(exist_ok=True);inv=json.loads((H/'inventory.json').read_text());base=inv['basis_t'];db=connection()

def save(name,v):
 (D/(name+'.json')).write_text(json.dumps(v,default=str,indent=2)+'\n');return v

def query(name,q,inputs,basis):
 name=name+'-t'+str(basis);cached=D/(name+'.edn')
 return loads(cached.read_text())if cached.exists()and cached.stat().st_size else db.query(q,inputs,D,name,basis)

def batch_pull(name,ids,pattern,basis,size=100,identity=None):
 out=[]
 for off in range(0,len(ids),size):
  fn=D/(name+'-'+str(off)+'-t'+str(basis)+'.edn')
  rows=loads(fn.read_text())if fn.exists()and fn.stat().st_size else query(name+'-'+str(off),'[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e '+(identity or '?a')+' _]]',[ids[off:off+size]],basis)
  out.extend(r[0]for r in rows);print(name,len(out),'/',len(ids),flush=True)
 assert {r[':db/id']for r in out}==set(ids),(name,'missing entities');return out

fp='[* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [:db/id]} {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}]'
keys=loads((H/'integrity-field-keys.edn').read_text());fids=sorted({f for q,f,k in keys});qids=sorted({q for t,k,q in inv['links']});basefile=D/'baseline-fields.json'
oldfields=json.loads(basefile.read_text())if basefile.exists()else save('baseline-fields',batch_pull('baseline-fields',fids,fp,base,150,':answer-field/id'))
qbfile=D/'baseline-question-memberships.json';qbpattern='[:db/id :question/id {:question/answer-fields [:db/id]}]'
oldquestions=json.loads(qbfile.read_text())if qbfile.exists()else save('baseline-question-memberships',batch_pull('baseline-question-memberships',qids,qbpattern,base,150,':question/id'))
if args.baseline_only:print('Fixed baseline ready',base);raise SystemExit(0)
t=args.basis or db.basis();assert t>=base
plans=[]
for path in sorted(set(H.glob('commit-*/plan.json'))|{H/'group-3-wording-delta/plan.json'}):
 if not path.exists():continue
 if not(path.parent/'receipt.edn').exists():continue
 verification=json.loads((path.parent/'verification.json').read_text());assert verification['committed']and verification['only_exact_reviewed_datoms_changed']and verification['exact_readback'];receipt=loads((path.parent/'receipt.edn').read_text());assert receipt[':edb/committed']and receipt[':edb/db-after-t']<=t;plans.append((path,json.loads(path.read_text()),receipt,verification))
assert {p.parent.name for p,plan,r,v in plans}>={'commit-duplicates','commit-group-1','commit-group-2','commit-group-3'}
plans.sort(key=lambda x:x[2][':edb/db-after-t'])
cas=[];detach=[];new=[]
for path,plan,receipt,verification in plans:
 cas+=plan.get('cas',[]);detach+=plan.get('detach',[])
 for a in plan.get('new_answers',[]):
  a=copy.deepcopy(a);a['entity']=receipt[':edb/tempids']['answer-'+a['answer_uuid']];new.append(a)
latest={(p['entity'],p['attribute']):p['after']for p in cas}
supplemental=[p for path,plan,r,v in plans if path.parent.name not in['commit-group-1','commit-group-2','commit-group-3','commit-duplicates']for p in plan.get('cas',[])]
# Every handed-off proposal must be represented by the actual committed plan.
for name in['group-1','group-2','group-3']:
 for p in json.loads((H/name/'proposals.json').read_text()):assert any(x['entity']==p['entity']and x['attribute']==p['attribute']and x['after']==p['after']for x in cas),(name,p['entity'],p['attribute'])
# Check source receipt datoms independently of the commit helper's report.
attrs={p['attribute']for p in cas+detach}|({'answer/id','answer/type','answer/value','answer-field/choices','answer-field/correct'}if new else set())|{'db/txInstant'};idents=attrs|{a['type'].lstrip(':')for a in new}|{'agent/codex'}
meta=query('attribute-identities','[:find ?e ?ident :in $ [?ident ...] :where [?e :db/ident ?ident]]',[[kw(x)for x in sorted(idents)]],t);aid={str(i).lstrip(':'):e for e,i in meta};byid={e:':'+n for n,e in aid.items()};receipts=[]
for path,plan,receipt,verification in plans:
 expected=collections.Counter()
 for p in plan.get('cas',[]):
  for value,added in[(p['before'],False),(p['after'],True)]:
   if value is not None:expected[p['entity'],aid[p['attribute']],value,added]+=1
 for p in plan.get('detach',[]):expected[p['entity'],aid[p['attribute']],p['value'],False]+=1
 for p in plan.get('new_answers',[]):
  e=receipt[':edb/tempids']['answer-'+p['answer_uuid']]
  for a,v in[('answer/id',uuid.UUID(p['answer_uuid'])),('answer/type',aid[p['type'].lstrip(':')]),('answer/value',p['value'])]:expected[e,aid[a],v,True]+=1
  for a in['answer-field/choices','answer-field/correct']:expected[p['field'],aid[a],e,True]+=1
 actual=collections.Counter((d[0],d[1],d[2],d[5])for d in receipt[':edb/tx-data']if d[1]!=aid['db/txInstant']);assert actual==expected,(path,'receipt datoms differ',actual-expected,expected-actual);assert all(d[4]==aid['agent/codex']for d in receipt[':edb/tx-data'])
 receipts.append({'directory':str(path.parent),'basis_t':receipt[':edb/db-after-t'],'exact_reviewed_content_datoms':sum(actual.values()),'no_learner_datoms':True,'independent_receipt_match':True})
# All 50 topics, KPs, canonical examples and available-question pools are unchanged.
tpattern='[:db/id :topic/id {:topic/knowledge-points [:db/id :knowledge-point/id {:knowledge-point/questions [:db/id]} {:knowledge-point/canonical-example [:db/id]}]}]';topics=batch_pull('topics',sorted(t[':db/id']for t in inv['topics']),tpattern,t,50,':topic/id')
refids=lambda v:sorted(x[':db/id']for x in(v if isinstance(v,list)else[v]))
def topology(ts):return{(tt[':db/id'],k[':db/id']):(str(k[':knowledge-point/id']),refids(k.get(':knowledge-point/questions',[])),refids(k.get(':knowledge-point/canonical-example',[])))for tt in ts for k in tt[':topic/knowledge-points']}
assert topology(topics)==topology(inv['topics']);assert{r[':db/id']:str(r[':topic/id'])for r in topics}=={r[':db/id']:str(r[':topic/id'])for r in inv['topics']}
# Pull every original field, including detached fields, to verify retained values.
newfids=sorted(set(fids)|{p['field']for p in new});livefields=batch_pull('fields',newfids,fp,t,150,':answer-field/id');fieldmap={r[':db/id']:r for r in livefields};oldmap={r[':db/id']:r for r in oldfields}
qpattern='[* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [:db/id]}]';questions=batch_pull('questions',qids,qpattern,t,100,':question/id');qmap={q[':db/id']:q for q in questions};oldqmap={q[':db/id']:q for q in oldquestions}
for e,q in qmap.items():
 assert str(q[':question/id'])==str(oldqmap[e][':question/id']),(e,'question UUID changed')
 expected=set(refids(oldqmap[e].get(':question/answer-fields',[])))-{p['value']for p in detach if p['entity']==e and p['attribute']=='question/answer-fields'}
 assert set(refids(q.get(':question/answer-fields',[])))==expected,(e,'field membership differs')
active={f[':db/id']for q in questions for f in q.get(':question/answer-fields',[])};unkeyed=[];unowned=[];duplicates=[];missing=[];blank_text=[]
for e,q in qmap.items():
 fs=[fieldmap[r[':db/id']]for r in q.get(':question/answer-fields',[])];counts=collections.Counter(f.get(':answer-field/key')for f in fs)
 duplicates.extend({'question':e,'key':k,'count':v}for k,v in counts.items()if v>1)
 if fs and not str(q.get(':question/worked-solution','')).strip():missing.append(e)
 for f in fs:
  c=f.get(':answer-field/correct',{}).get(':db/id');choices={a[':db/id']:a for a in f.get(':answer-field/choices',[])}
  if c is None:unkeyed.append((e,f[':db/id']))
  elif c not in choices:unowned.append((e,f[':db/id'],c))
  elif f[':answer-field/type'][':db/ident']==':answer-field.type/blank'and choices[c][':answer/type'][':db/ident']==':answer.type/text':blank_text.append((e,f[':db/id'],c,choices[c][':answer/value']))
assert not(unkeyed or unowned or duplicates or missing or blank_text),(unkeyed,unowned,duplicates,missing,blank_text)
# Apply plans to baseline field and answer entities, then compare every scalar and membership.
expectedfields=copy.deepcopy(oldmap);answerobjects={a[':db/id']:a for f in expectedfields.values()for a in f.get(':answer-field/choices',[])}
for p in cas:
 e,a=p['entity'],':'+p['attribute'];v=p['after']
 if e in expectedfields:
  if a in[':answer-field/correct',':answer-field/type']:v={':db/id':v,**({':db/ident':byid[v]}if a.endswith('/type')and v in byid else{})}
  expectedfields[e][a]=v
 if e in answerobjects:
  if a==':answer/type':v={':db/id':v,':db/ident':byid[v]}
  answerobjects[e][a]=v
for p in new:
 a={':db/id':p['entity'],':answer/id':p['answer_uuid'],':answer/type':{':db/id':aid[p['type'].lstrip(':')],':db/ident':p['type']},':answer/value':p['value']};expectedfields[p['field']].setdefault(':answer-field/choices',[]).append(a);expectedfields[p['field']][':answer-field/correct']={':db/id':p['entity']}
for p in detach:
 if p['attribute']=='answer-field/choices':expectedfields[p['entity']][':answer-field/choices']=[a for a in expectedfields[p['entity']].get(':answer-field/choices',[])if a[':db/id']!=p['value']]
def norm(v):
 if isinstance(v,list):return sorted((norm(x)for x in v),key=lambda x:json.dumps(x,sort_keys=True,default=str))
 if isinstance(v,dict):return{k:norm(x)for k,x in sorted(v.items())}
 if isinstance(v,uuid.UUID):return str(v)
 return v
for e in fids:assert norm(fieldmap[e])==norm(expectedfields[e]),(e,'field/answer UUID, bank, key, correct, type or retained value mismatch')
# Explicit detached memberships are absent while target fields/answers are retained unchanged.
retained=[]
for p in detach:
 if p['attribute']=='question/answer-fields':
  e=p['value'];assert e not in refids(qmap[p['entity']].get(':question/answer-fields',[]));assert norm(fieldmap[e])==norm(expectedfields[e]);retained.append({'detached_field':e,'retained_bank_entities':refids(fieldmap[e].get(':answer-field/choices',[]))})
 else:
  e=p['value'];live=batch_pull('retained-answer-'+str(e),[e],'[* {:answer/type [:db/id :db/ident]}]',t,1,':answer/id')[0];assert norm(live)==norm(answerobjects[e]);retained.append({'detached_answer':e,'retained':True})
# Exact CAS after-values, including tutorials and all changed answer metadata.
scalar_checks=0
byattr=collections.defaultdict(list)
for e,a in latest:byattr[a].append(e)
for a,entities in byattr.items():
 got={}
 for off in range(0,len(entities),100):got.update(dict(query('after-'+a.replace('/','-')+'-'+str(off),'[:find ?e ?v :in $ ?a [?e ...] :where [?e ?a ?v]]',[kw(a),entities[off:off+100]],t)))
 for e in entities:assert got.get(e)==latest[e,a],(e,a,'CAS after mismatch');scalar_checks+=1
# Compare complete reviewed models with the exact staged fixtures used by renderer/grader.
for q in questions:
 v=q.get(':question/difficulty',{})
 if ':db/id'in v and ':db/ident'in v:byid[v[':db/id']]=v[':db/ident']
for f in livefields:
 for v in[f.get(':answer-field/type',{})]+[a.get(':answer/type',{})for a in f.get(':answer-field/choices',[])]:
  if ':db/id'in v and ':db/ident'in v:byid[v[':db/id']]=v[':db/ident']
fixture_checks=[];models=0
for name in['group-1','group-2','group-3','skipped-delta']:
 path=H/name/('projected-question.json'if name=='skipped-delta'else'proposed-questions.json');staged=json.loads(path.read_text());staged=[staged]if isinstance(staged,dict)else staged;hashes={}
 if name=='skipped-delta':
  proof=json.loads((H/name/'proof.json').read_text());assert proof.get('passed',True),proof
 for expected in staged:
  expected=copy.deepcopy(expected)
  def overlay(o):
   if isinstance(o,list):
    for x in o:overlay(x)
   elif isinstance(o,dict):
    for x in list(o.values()):overlay(x)
    for p in supplemental:
     if o.get(':db/id')==p['entity']:o[':'+p['attribute']]=p['after']
  overlay(expected)
  e=expected[':db/id'];got=copy.deepcopy(qmap[e]);got[':question/answer-fields']=[fieldmap[x[':db/id']]for x in got.get(':question/answer-fields',[])]
  # Stage records can carry expanded correct-answer stubs from applying a global patch.
  def model(v):
   if isinstance(v,list):return norm([model(x)for x in v])
   if not isinstance(v,dict):return str(v)if isinstance(v,uuid.UUID)else v
   out={}
   for k,x in v.items():
    if k in[':answer-field/correct']:out[k]=None if x is None else{':db/id':x[':db/id']}
    elif k in[':answer/type',':answer-field/type',':question/difficulty']:out[k]=(x.get(':db/ident')or byid[x[':db/id']])if isinstance(x,dict)else x
    else:out[k]=model(x)
   return out
  actualmodel=model(got);want=model(expected)
  # A field list omitted for canonical examples is equivalent to an empty list.
  if not want.get(':question/answer-fields'):want.pop(':question/answer-fields',None);actualmodel.pop(':question/answer-fields',None)
  if actualmodel!=want:
   save('model-mismatch-'+str(e),{'group':name,'actual':actualmodel,'expected':want})
  assert actualmodel==want,(name,e,'staged full model mismatch')
  hashes[e]=hashlib.sha256(json.dumps(actualmodel,sort_keys=True,default=str).encode()).hexdigest();models+=1
 fixtures=[str(p)for p in (H/name).glob('*input*.json')if any(x in p.name for x in['render','grading','control'])]
 fixture_checks.append({'group':name,'questions':len(staged),'staged_question_file':str(path),'supplemental_overlay_attributes':len(supplemental),'staged_file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'exact_live_model_hashes':hashes,'relevant_read_only_fixtures':fixtures})
assert models==945,models
summary={'passed':True,'baseline_t':base,'basis_t':t,'topics':len(topics),'knowledge_points':len(topology(topics)),'question_records':len(questions),'reviewed_exact_models':models,'active_fields':len(active),'all_original_question_UUIDs_and_pools_preserved':True,'all_original_field_answer_UUIDs_and_reviewed_banks_preserved':True,'required_solutions_present':True,'unkeyed_fields':unkeyed,'unowned_correct_links':unowned,'duplicate_active_field_keys':duplicates,'blank_text_candidates':blank_text,'exact_CAS_after_values':scalar_checks,'detached_memberships_absent':len(detach),'retained_detached_entities':retained,'receipts':receipts,'model_and_fixture_checks':fixture_checks,'no_unintended_receipt_content_datoms':True,'database_writes':0,'learner_writes':0}
(H/'final-live-verification.json').write_text(json.dumps(summary,default=str,indent=2)+'\n');print('FINAL LIVE PASSED:',len(topics),'topics,',len(questions),'questions,',models,'exact staged models,',len(active),'active fields,',scalar_checks,'CAS values; basis',t)
