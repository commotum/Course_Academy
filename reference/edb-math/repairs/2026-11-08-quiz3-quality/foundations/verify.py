import sys,json
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection,loads
H=Path(__file__).resolve().parent;db=connection();receipt=loads((H/'receipt.edn').read_text());basis=receipt[':edb/db-after-t'];changes=json.loads((H/'changes.json').read_text());ids=sorted(set(c['entity']for c in changes));r=db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[ids],H,'changed-values-after',basis);lookup={row[0][':db/id']:row[0]for row in r};checks=[]
for c in changes:
 value=lookup[c['entity']].get(c['attribute']);value=value[':db/id']if isinstance(value,dict)and ':db/id'in value else value
 checks.append({'entity':c['entity'],'attribute':c['attribute'],'passed':value==c['new']})
attrs=db.query('[:find ?id ?ident :where [?id :db/ident ?ident]]',[],H,'attribute-idents',basis);attribute_ids=dict(attrs)
protected=[d for d in receipt[':edb/tx-data']if not str(attribute_ids.get(d[1],'')).startswith((':question/',':answer-field/',':answer/',':tutorial/',':db/'))]
report={'committed':receipt[':edb/committed'],'basis':basis,'changed_attributes':len(checks),'all_changed_values_match':all(c['passed']for c in checks),'protected_or_unexpected_datoms':protected,'tempids':receipt.get(':edb/tempids'),'checks':checks};(H/'verification.json').write_text(json.dumps(report,indent=2,default=str));print(json.dumps({k:v for k,v in report.items()if k!='checks'},indent=2))
