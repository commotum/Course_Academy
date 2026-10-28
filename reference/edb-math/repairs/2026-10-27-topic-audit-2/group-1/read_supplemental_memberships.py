"""Narrow read-only provenance audit of two captured default-leak choices."""
import concurrent.futures,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
DB=connection();BASIS=DB.basis();ANSWERS=[17592186298622,17592186297713];FIELDS=[17592186299291,17592186299462]
def incoming(task):
 answer,historical=task;db=connection();query='[:find ?e ?a ?tx ?source ?added :in $ ?v :where [?e ?a ?v ?tx ?source ?added]]'if historical else'[:find ?e ?a :in $ ?v :where [?e ?a ?v]]'
 return answer,historical,db.query(query,[answer],H,'supplemental-'+str(answer)+('-history'if historical else'-current'),BASIS,history=historical)
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:reads=list(pool.map(incoming,[(a,h)for a in ANSWERS for h in[False,True]]))
field_rows=DB.query('[:find (pull ?e [* {:answer-field/type [:db/ident]} {:answer-field/correct [* {:answer/type [:db/ident]}]} {:answer-field/choices [* {:answer/type [:db/ident]}]}]) :in $ [?e ...] :where [?e :answer-field/id _]]',[FIELDS],H,'supplemental-fields',BASIS)
attrs=sorted({row[1]for answer,historical,rows in reads for row in rows})
attr_rows=DB.query('[:find (pull ?a [* {:db/valueType [:db/ident]} {:db/cardinality [:db/ident]}]) :in $ [?a ...] :where [?a :db/ident _]]',[attrs],H,'supplemental-attributes',BASIS)
# Explicit response attribute flags document what indexed retained history proves.
response_schema=DB.query('[:find (pull ?a [* {:db/valueType [:db/ident]} {:db/cardinality [:db/ident]}]) :where [?a :db/ident :task-item/responses]]',[],H,'supplemental-response-schema',BASIS)
referrers=sorted({row[0]for answer,historical,rows in reads for row in rows});referrer_rows=DB.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[referrers],H,'supplemental-referrers',BASIS)
out={'basis_t':BASIS,'database':'math','answer_ids':ANSWERS,'current_fields':[r[0]for r in field_rows],'attributes':[r[0]for r in attr_rows],'response_schema':[r[0]for r in response_schema],'referrer_records':[r[0]for r in referrer_rows],'incoming':[{'answer':a,'history':hist,'rows':rows}for a,hist,rows in reads],'limits':'Retained indexed history is audited; no claim to reconstruct excised or externally purged records. No database write.'}
(H/'supplemental-membership-evidence.json').write_text(json.dumps(out,default=str,indent=2));print('basis',BASIS,'reads',[(a,h,len(rows))for a,h,rows in reads],'fields',len(field_rows),'referrers',len(referrers))
