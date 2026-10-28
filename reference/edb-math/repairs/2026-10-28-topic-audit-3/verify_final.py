"""Read-only scoped identity, membership, canonical-key and publication verification."""
import collections,copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path[:0]=[str(R),str(R/'scripts')]
from scripts.migrate_learner_history import connection,loads,kw
from scripts.generator_packages import verify_package
D=H/(sys.argv[1]if len(sys.argv)>1 else'final-check');D.mkdir(exist_ok=True);db=connection();inventory=json.loads((H/'inventory.json').read_text());commit_names=json.loads((H/'commits.json').read_text());publication_batches=json.loads((H/'publication-batches.json').read_text())
if not(D/'basis.json').exists():(D/'basis.json').write_text(json.dumps({'basis_t':db.basis()}))
t=json.loads((D/'basis.json').read_text())['basis_t']
def query(q,inputs,name):
 p=D/(name+'.edn')
 return loads(p.read_text())if p.exists()else db.query(q,inputs,D,name,t)
def batched(q,ids,name,size=400):
 return [r for i in range(0,len(ids),size)for r in query(q,[ids[i:i+size]],name+'-'+str(i))]
snapshots=[json.loads((H/g/n).read_text())for g,n in [('group-1','current.json'),('group-2','current.json'),('group-3','snapshot.json')]]
original={q[':db/id']:q for s in snapshots for q in s['questions']};assert len(original)==len({r[2]for r in inventory['links']})
fields={f[':db/id']:f for q in original.values()for f in q.get(':question/answer-fields',[])}
answers={a[':db/id']:a for f in fields.values()for a in f.get(':answer-field/choices',[])}
enum_ids=sorted({obj[':db/id']for obj in [f[':answer-field/type']for f in fields.values()]+[a[':answer/type']for a in answers.values()]if ':db/id'in obj})
enum_names=dict(query('[:find ?e ?name :in $ [?e ...] :where [?e :db/ident ?name]]',[enum_ids],'response-enum-names'))
def enum_name(value):
 return value.get(':db/ident',enum_names.get(value.get(':db/id')))if isinstance(value,dict)else value
expected_fields={(q[':db/id'],f[':db/id'])for q in original.values()for f in q.get(':question/answer-fields',[])}
expected_banks={(f,a[':db/id'])for f,obj in fields.items()for a in obj.get(':answer-field/choices',[])}
expected_keys={f:obj[':answer-field/correct'][':db/id']for f,obj in fields.items()if ':answer-field/correct'in obj}
plans=[];created=[];reports=[]
for name in commit_names:
 d=H/name;report=json.loads((d/'verification.json').read_text());assert report['committed'];reports.append(report)
 plan=json.loads((d/'plan.json').read_text());plans.append(plan);created.extend(report.get('new_answers',[]))
 for p in plan.get('cas',[]):
  if p['attribute']=='answer-field/correct':expected_keys[p['entity']]=p['after']
 for p in plan.get('detach',[]):
  (expected_fields if p['attribute']=='question/answer-fields'else expected_banks).remove((p['entity'],p['value']))
for p in created:expected_banks.add((p['field'],p['entity']));expected_keys[p['field']]=p['entity']
scalar_expect={(p['entity'],p['attribute']):p['after']for plan in plans for p in plan.get('cas',[])}
scalar_pairs=sorted(scalar_expect);scalar_actual={};by_attribute=collections.defaultdict(list)
for e,a in scalar_pairs:by_attribute[a].append(e)
for a,entities in sorted(by_attribute.items()):
 for i in range(0,len(entities),80):
  rows=query('[:find ?e ?v :in $ ?attribute [?e ...] :where [?e ?attribute ?v]]',[kw(a),entities[i:i+80]],'reviewed-scalars-'+a.replace('/','-')+'-'+str(i))
  scalar_actual.update({(e,a):v for e,v in rows})
assert scalar_actual==scalar_expect
for kind,records,attr in [('question',original,'question/id'),('field',fields,'answer-field/id'),('answer',answers,'answer/id')]:
 rows=batched('[:find ?e ?id :in $ [?e ...] :where [?e :'+attr+' ?id]]',sorted(records),kind+'-ids')
 assert {e:str(v)for e,v in rows}=={e:str(obj[':'+attr])for e,obj in records.items()},kind
if created:
 new_rows=query('[:find ?e ?id ?value ?type :in $ [?e ...] :where [?e :answer/id ?id] [?e :answer/value ?value] [?e :answer/type ?kind] [?kind :db/ident ?type]]',[[p['entity']for p in created]],'new-owned-answers')
 assert {(e,str(i),v,str(k))for e,i,v,k in new_rows}=={(p['entity'],p['answer_uuid'],p['value'],p['type'])for p in created}
assert set(map(tuple,batched('[:find ?q ?f :in $ [?q ...] :where [?q :question/answer-fields ?f]]',sorted(original),'question-fields')))==expected_fields
actual_banks=set(map(tuple,batched('[:find ?f ?a :in $ [?f ...] :where [?f :answer-field/choices ?a]]',sorted(fields),'choice-memberships')))
assert expected_banks.issubset(actual_banks),'Unexpected bank membership removed'
live_entries=actual_banks-expected_banks;live_answers={};live_by_field=collections.defaultdict(list)
if live_entries:
 # A live learner may have submitted new blank responses during this audit.
 # Require real task response refs, sole field ownership, and retained entities;
 # never mistake those user values for authored choices or remove them.
 ids=sorted({a for f,a in live_entries})
 response_refs=query('[:find ?a ?item :in $ [?a ...] :where [?item :task-item/responses ?a]]',[ids],'live-blank-response-refs')
 assert {a for a,item in response_refs}==set(ids)
 owners=query('[:find ?a ?f :in $ [?a ...] :where [?f :answer-field/choices ?a]]',[ids],'live-blank-answer-owners')
 assert {(f,a)for a,f in owners}==live_entries
 rows=query('[:find (pull ?a [* {:answer/type [:db/ident]}]) :in $ [?a ...] :where [?a :answer/id _]]',[ids],'live-blank-answer-records')
 live_answers={r[0][':db/id']:r[0]for r in rows};assert set(live_answers)==set(ids)
 for f,a in live_entries:
  assert enum_name(fields[f][':answer-field/type'])==':answer-field.type/blank'
  live_by_field[f].append(live_answers[a])
assert dict(batched('[:find ?f ?a :in $ [?f ...] :where [?f :answer-field/correct ?a]]',sorted(fields),'correct-links'))==expected_keys
inventory=json.loads((H/'inventory.json').read_text());links=query((H/'question-links-query.edn').read_text(),[[x['entity']for x in inventory['topics']]],'pool')
assert set(map(tuple,inventory['links'])).issubset(set(map(tuple,links)))
publications=[]
for name in publication_batches:publications+=json.loads((H/name/'generator-publications.json').read_text())
publication_count=len(publications);publications=list({p['kp']:p for p in publications}.values())
registered=dict(query('[:find ?kp ?path :in $ [?kp ...] :where [?kp :knowledge-point/question-generator ?g] [?g :question-generator/script ?path]]',[[p['kp']for p in publications]],'registered-generators'))
assert registered=={p['kp']:p['new_reference']for p in publications}
for p in publications:verify_package(Path('/media/jake/SSD/EDB/math')/Path(p['new_reference']).parent,p['digest'])
# Form the exact verified presentation model, including new owned blank answers.
cas={(p['entity'],':'+p['attribute']):p['after']for plan in plans for p in plan.get('cas',[])}
detaches=collections.defaultdict(set)
for plan in plans:
 for p in plan.get('detach',[]):detaches[p['entity'],':'+p['attribute']].add(p['value'])
new_by_field={p['field']:p for p in created};names={17592186045498:':answer.type/math',17592186045499:':answer.type/text'}
def transform(v):
 if isinstance(v,list):return [transform(x)for x in v]
 if not isinstance(v,dict):return v
 v=copy.deepcopy(v);e=v.get(':db/id')
 for (eid,a),value in cas.items():
  if eid!=e:continue
  v[a]=({':db/id':value}if a==':answer-field/correct'else {':db/id':value,':db/ident':names[value]}if a==':answer/type'else value)
 for (eid,a),removed in detaches.items():
  if eid==e and a in v:v[a]=[x for x in v[a]if x[':db/id']not in removed]
 if e in live_by_field:v[':answer-field/choices']=v.get(':answer-field/choices',[])+copy.deepcopy(live_by_field[e])
 if e in new_by_field:
  p=new_by_field[e];a={':db/id':p['entity'],':answer/id':p['answer_uuid'],':answer/type':{':db/ident':p['type']},':answer/value':p['value']};v[':answer-field/choices']=v.get(':answer-field/choices',[])+[a];v[':answer-field/correct']={':db/id':p['entity']}
 return {k:transform(x)for k,x in v.items()}
model=transform(list(original.values()));missing=[];native=[];render=[]
for q in model:
 fs=q.get(':question/answer-fields',[]);assert len({f[':answer-field/key']for f in fs})==len(fs)
 for a in [':question/problem',':question/worked-solution']:
  if q.get(a):render.append({'entity':q[':db/id'],'attribute':a,'value':q[a],'fields':fs})
 checks=[];graded=[]
 for f in fs:
  bank={a[':db/id']:a for a in f.get(':answer-field/choices',[])};right=f.get(':answer-field/correct',{}).get(':db/id')
  if right is None:missing.append({'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'field':f[':db/id']});continue
  assert right in bank
  f[':answer-field/correct']=copy.deepcopy(bank[right]);kind=enum_name(f[':answer-field/type']);assert kind
  if kind==':answer-field.type/checkbox':render.append({'entity':f[':db/id'],'attribute':':answer-field/key','value':f[':answer-field/key']})
  for a in bank.values():
   if kind!=':answer-field.type/blank'or a[':db/id']==right:render.append({'entity':a[':db/id'],'attribute':':answer/value','value':a[':answer/value'],'bare_math':enum_name(a[':answer/type'])==':answer.type/math'})
  i=len(graded);f=copy.deepcopy(f);f[':answer-field/correct']=[':answer/id',bank[right][':answer/id']];f[':answer-field/type']=kind
  for a in f[':answer-field/choices']:a[':answer/type']=enum_name(a[':answer/type']);assert a[':answer/type']
  graded.append(f)
  if kind==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':bank[right][':answer/value'],'expected':'accepted','purpose':'Verified canonical blank accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect scalar rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':db/id']==right else'rejected','purpose':'Owned bank identity dispatch'}for a in bank.values())
  if f.get(':answer-field/display-key'):render.append({'entity':f[':db/id'],'attribute':':answer-field/display-key','value':f[':answer-field/display-key']})
 if checks:
  nq=copy.deepcopy(q);nq[':question/answer-fields']=graded;native.append({'label':str(q[':db/id']),'record':{'question':nq,'knowledge_point':{'title':'Verified topic audit'},'generation':{'template':'verified-database-readback'}},'checks':checks})
content=transform(snapshots[0]['contents']+[x for act in snapshots[1]['activities']for x in act['contents']]+snapshots[2]['content'])
tutorials={x[':db/id']:x for x in content if ':tutorial/content'in x}
render.extend({'entity':e,'attribute':':tutorial/content','value':v[':tutorial/content']}for e,v in tutorials.items())
(D/'model.json').write_text(json.dumps(model,indent=2,default=str)+'\n');(D/'grading-input.json').write_text(json.dumps(native,indent=2,default=str)+'\n');(D/'render-input.json').write_text(json.dumps(render,indent=2,default=str)+'\n')
report={'passed':True,'basis_t':t,'topics':len(inventory['topics']),'questions_examples':len(original),'tutorials':len(tutorials),'registered_verified_successors':len(publications),'question_field_answer_UUIDs_preserved':True,'original_pool_links_preserved':True,'exact_expected_field_and_choice_memberships':True,'retained_field_entities':len(fields),'active_fields':len(expected_fields),'created_owned_answers':len(created),'scalar_changes':sum(r['scalar_changes']for r in reports),'membership_retractions':sum(r['membership_retractions']for r in reports),'remaining_unkeyed_fields':missing}
report['immutable_package_versions_published']=publication_count
report['additional_live_learner_blank_answers']=[{'field':f,'answer':a}for f,a in sorted(live_entries)]
report['additional_pool_links_since_snapshot']=len(set(map(tuple,links))-set(map(tuple,inventory['links'])))
(H/('final-verification.json'if D.name=='final-check'else D.name+'-verification.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
