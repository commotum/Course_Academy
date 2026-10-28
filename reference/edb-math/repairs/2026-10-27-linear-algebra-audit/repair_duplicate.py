"""Detach a duplicate current UI field; retain all field/answer entities and history."""
import collections,hashlib,json,subprocess,sys,threading
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path[:0]=[str(R),str(R/'scripts')]
from capture.scripts.config import Config
from capture.scripts.database.preview import preview_executable
from migrate_learner_history import connection,kw,loads,dumps
D=H/'duplicate-field';D.mkdir(exist_ok=True);db=connection();q=17592186106313;old=17592186104026;keep=17592186379835
payload=dumps([[kw('db/retract'),q,kw('question/answer-fields'),old],[kw('db/ensure'),q,kw('question/validate')]])+'\n';file=D/'transaction.edn'
if file.exists():assert file.read_text()==payload
else:file.write_text(payload)
sha=hashlib.sha256(payload.encode()).hexdigest();intentpath=D/'commit-intent.json';receipt=D/'receipt.edn'
if not intentpath.exists():
 basis=db.basis()
 before=db.query('[:find (pull ?q [:db/id :question/id {:question/answer-fields [:db/id :answer-field/id :answer-field/key {:answer-field/correct [:db/id]} {:answer-field/choices [:db/id :answer/id :answer/value]}]}]) :in $ ?q :where [?q :question/id]]',[q],D,'before',basis)[0][0]
 assert {f[':db/id']for f in before[':question/answer-fields']}=={old,keep}
 refs=[]
 for target in [q,old,keep,*[a[':db/id']for f in before[':question/answer-fields']for a in f[':answer-field/choices']]]:
  refs += [[target,owner,a]for owner,a in db.query('[:find ?owner ?a :in $ ?target :where [?owner ?a ?target]]',[target],D,'incoming-'+str(target),basis)]
 attrnames={a:str(name)for a,name in db.query('[:find ?a ?name :in $ [?a ...] :where [?a :db/ident ?name]]',[sorted({a for target,owner,a in refs})],D,'incoming-attributes',basis)}
 assert all(attrnames[a]in {':knowledge-point/questions',':question/answer-fields',':answer-field/choices',':answer-field/correct'}for target,owner,a in refs),refs
 binary=preview_executable(Config(),threading.Event());p=subprocess.run([str(binary),'with','--database','math','--file',str(file),'--source',':agent/codex'],env=db.env,capture_output=True,text=True);(D/'preview.edn').write_text(p.stdout);(D/'preview.stderr').write_text(p.stderr);p.check_returncode();assert loads(p.stdout).get(':edb/speculative')is True
 intent={'sha256':sha,'request_key':'linear-algebra-duplicate-field-'+sha[:32],'source':':agent/codex','database':'math','question':q,'detached_field':old,'retained_field':keep,'no_entity_retractions':True};intentpath.write_text(json.dumps(intent,indent=2)+'\n')
else:intent=json.loads(intentpath.read_text());assert intent['sha256']==sha
if not receipt.exists()or not receipt.read_text().strip():
 p=subprocess.run([db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',str(file),'--endpoint','/tmp/edb-math/writer.sock','--request-key',intent['request_key'],'--timeout-ms','120000'],env=db.env,capture_output=True,text=True,timeout=160);receipt.write_text(p.stdout);(D/'submit.stderr').write_text(p.stderr);p.check_returncode()
r=loads(receipt.read_text());assert r[':edb/committed']is True;t=r[':edb/db-after-t'];attrs=dict((str(n),a)for a,n in db.query('[:find ?a ?n :in $ [?n ...] :where [?a :db/ident ?n]]',[[kw('question/answer-fields'),kw('db/txInstant')]],D,'attrs',t));actual=[d for d in r[':edb/tx-data']if d[1]!=attrs[':db/txInstant']];assert len(actual)==1 and actual[0][:3]==[q,attrs[':question/answer-fields'],old]and actual[0][5]is False
links=db.query('[:find ?f :in $ ?q :where [?q :question/answer-fields ?f]]',[q],D,'after',t);assert links==[[keep]]
retained=db.query('[:find (pull ?f [:db/id :answer-field/id {:answer-field/choices [:db/id :answer/id :answer/value]}]) :in $ [?f ...] :where [?f :answer-field/id]]',[[old,keep]],D,'retained-entities',t);assert len(retained)==2 and all(len(x[0][':answer-field/choices'])==5 for x in retained)
summary={'committed':True,'basis_t':t,'question':q,'detached_duplicate_field':old,'retained_field':keep,'all_field_and_answer_entities_preserved':True,'no_learner_datoms_changed':True,'exact_single_membership_retraction_verified':True};(D/'verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
