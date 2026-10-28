"""Guarded mixed content repair; retained entities are never excised/deleted."""
import collections,hashlib,json,re,subprocess,sys,threading,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path[:0]=[str(R),str(R/'scripts')]
from capture.scripts.config import Config
from capture.scripts.database.preview import preview_executable
from migrate_learner_history import connection,kw,loads,dumps
D=Path(sys.argv[1]);plan=json.loads((D/'plan.json').read_text());db=connection();cas=plan.get('cas',[]);detach=plan.get('detach',[]);new=plan.get('new_answers',[]);forms=[];ensures={(e,'question/validate')for e in plan.get('questions',[])}
for p in new:
 p['tempid']='answer-'+p['answer_uuid'];forms.append({kw('db/id'):p['tempid'],kw('answer/id'):uuid.UUID(p['answer_uuid']),kw('answer/type'):kw(p['type']),kw('answer/value'):p['value']})
 forms.extend([[kw('db/add'),p['field'],kw('answer-field/choices'),p['tempid']],[kw('db/cas'),p['field'],kw('answer-field/correct'),None,p['tempid']]])
 ensures|={(p['field'],'answer-field/validate'),(p['tempid'],'answer/validate'),(p['question'],'question/validate')}
for p in cas:
 assert p['before']!=p['after'];forms.append([kw('db/cas'),p['entity'],kw(p['attribute']),p['before'],p['after']]);kind=p['attribute'].split('/')[0]
 ensures.add((p['entity'],{'answer':'answer/validate','answer-field':'answer-field/validate','question':'question/validate','tutorial':'tutorial/validate'}[kind]))
for p in detach:
 assert p['attribute']in ['question/answer-fields','answer-field/choices'];forms.append([kw('db/retract'),p['entity'],kw(p['attribute']),p['value']]);ensures.add((p['entity'],'question/validate'if p['attribute'].startswith('question/')else'answer-field/validate'))
forms +=[[kw('db/ensure'),e,kw(spec)]for e,spec in sorted(ensures,key=str)];payload=dumps(forms)+'\n';file=D/'transaction.edn'
if file.exists():assert file.read_text()==payload
else:file.write_text(payload)
sha=hashlib.sha256(payload.encode()).hexdigest();intentpath=D/'commit-intent.json';receipt=D/'receipt.edn'
def rows_at(pairs,basis,name):
 return db.query('[:find ?e ?name ?v :in $ [[?e ?name]] :where [?a :db/ident ?name] [?e ?a ?v]]',[[[e,kw(a)]for e,a in pairs]],D,name,basis)
# Unknown outcomes retain the exact original request. Only a confirmed stale
# precondition may produce a newly captured basis and a new request identity.
for attempt in range(4):
 if not intentpath.exists():
  basis=db.basis();pairs={(p['entity'],p['attribute'])for p in cas+detach}|{(p['field'],a)for p in new for a in ['answer-field/choices','answer-field/correct','answer-field/id','answer-field/type']};before=rows_at(sorted(pairs),basis,'before-'+str(basis));values=collections.defaultdict(list)
  for e,a,v in before:values[e,str(a).lstrip(':')].append(v)
  for p in cas:assert values[p['entity'],p['attribute']]==([]if p['before']is None else[p['before']]),p
  for p in detach:
   actual=values[p['entity'],p['attribute']];assert p['value']in actual,p
   if 'expected_before'in p:assert set(actual)==set(p['expected_before']),p
  for p in new:
   assert not values[p['field'],'answer-field/choices']and not values[p['field'],'answer-field/correct'],p
   assert str(values[p['field'],'answer-field/id'][0])==p['field_uuid'],p
   duplicates=db.query('[:find ?a :in $ ?id :where [?a :answer/id ?id]]',[uuid.UUID(p['answer_uuid'])],D,'uuid-absence-'+str(p['field'])+'-'+str(basis),basis);assert not duplicates,p
  binary=preview_executable(Config(),threading.Event());pv=subprocess.run([str(binary),'with','--database','math','--file',str(file),'--source',':agent/codex'],env=db.env,capture_output=True,text=True);(D/'preview.edn').write_text(pv.stdout);(D/'preview.stderr').write_text(pv.stderr);pv.check_returncode();pr=loads(pv.stdout);assert pr.get(':edb/speculative')is True
  if pr[':edb/db-before-t']!=basis:continue
  intent={'sha256':sha,'request_key':'topic-audit-2-mixed-'+sha[:24]+'-'+str(basis),'basis':basis,'source':':agent/codex','database':'math','before_edn':dumps(before)};intentpath.write_text(json.dumps(intent,indent=2)+'\n')
 else:intent=json.loads(intentpath.read_text());assert intent['sha256']==sha
 if receipt.exists()and receipt.read_text().strip():break
 submitted=subprocess.run([db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',str(file),'--endpoint','/tmp/edb-math/writer.sock','--request-key',intent['request_key'],'--basis',str(intent['basis']),'--timeout-ms','120000'],env=db.env,capture_output=True,text=True,timeout=160)
 (D/'submit.stderr').write_text(submitted.stderr)
 if submitted.returncode and re.search(r'(?:code=|remote_code=)postgres/stale-basis(?:\s|$)',submitted.stderr):
  archive=D/('rejected-stale-'+str(intent['basis']));archive.mkdir(exist_ok=True);intentpath.rename(archive/'commit-intent.json');(archive/'submission.stderr').write_text(submitted.stderr);continue
 receipt.write_text(submitted.stdout);submitted.check_returncode();break
else:raise RuntimeError('Database kept advancing; no fresh dependent request submitted')
r=loads(receipt.read_text());assert r[':edb/committed']is True;t=r[':edb/db-after-t'];before=loads(intent['before_edn']);old=collections.defaultdict(set)
for e,a,v in before:old[e,str(a).lstrip(':')].add(v)
# Resolve new tempids using the durable receipt, never speculative IDs.
resolved=r.get(':edb/tempids',{});types={p['type']for p in new};attrs={p['attribute']for p in cas+detach}|({'answer/id','answer/type','answer/value','answer-field/choices','answer-field/correct'}if new else set())|{'db/txInstant'}
meta=db.query('[:find ?e ?name :in $ [?name ...] :where [?e :db/ident ?name]]',[[kw(n)for n in attrs|types]],D,'attribute-and-type-ids',t);ids={str(name).lstrip(':'):e for e,name in meta};expected=collections.Counter();want={k:set(v)for k,v in old.items()}
for p in cas:
 for v,op in [(p['before'],False),(p['after'],True)]:
  if v is not None:expected[p['entity'],ids[p['attribute']],v,op]+=1
 want[p['entity'],p['attribute']]={p['after']}if p['after']is not None else set()
for p in detach:
 expected[p['entity'],ids[p['attribute']],p['value'],False]+=1;want[p['entity'],p['attribute']].remove(p['value'])
for p in new:
 eid=resolved[p['tempid']];p['entity']=eid
 for a,v in [('answer/id',uuid.UUID(p['answer_uuid'])),('answer/type',ids[p['type'].lstrip(':')]),('answer/value',p['value'])]:expected[eid,ids[a],v,True]+=1;want[eid,a]={v}
 for a in ['answer-field/choices','answer-field/correct']:expected[p['field'],ids[a],eid,True]+=1;want[p['field'],a]={eid}
actual=collections.Counter((d[0],d[1],d[2],d[5])for d in r[':edb/tx-data']if d[1]!=ids['db/txInstant']);assert actual==expected,(actual-expected,expected-actual);assert all(d[4]==17592186576411 for d in r[':edb/tx-data'])
after=rows_at(sorted(want),t,'after');got=collections.defaultdict(set)
for e,a,v in after:got[e,str(a).lstrip(':')].add(v)
assert all(got[k]==v for k,v in want.items())
# Detaching a redundant current membership does not delete its target entity.
if detach:
 retained=db.query('[:find ?e ?a ?v :in $ [?e ...] :where [?e ?a ?v]]',[[p['value']for p in detach]],D,'detached-entities-retained',t);assert {e for e,a,v in retained}=={p['value']for p in detach}
report={'committed':True,'basis_t':t,'scalar_changes':len(cas),'membership_retractions':len(detach),'created_owned_answers':len(new),'only_exact_reviewed_datoms_changed':True,'retained_entities_and_learner_history_preserved':True,'exact_readback':True,'new_answers':new};(D/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
