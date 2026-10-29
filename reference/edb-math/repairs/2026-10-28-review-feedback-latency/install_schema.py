import sys,json
from pathlib import Path
sys.path.insert(0,'scripts')
from generator_publish import Publisher,GeneratorCommitter,digest,kw,dumps,StaleBasis,jsonable
from capture.scripts.database.edn import loads
R=Path.cwd();E=R/'reference/edb-math/repairs/2026-10-28-review-feedback-latency/schema';E.mkdir(parents=True,exist_ok=True)
all_forms=loads((R/'schema/learner/2-2-learner-task-item.edn').read_text())
names=[':task-item/working-periods',':working-period/id',':working-period/started-at',':working-period/ended-at']
forms=[f for f in all_forms if str(f.get(':db/ident')) in names]
assert len(forms)==4
for index,form in enumerate(forms):form[kw('db/id')]=f'clock-schema-{index}'

def verify_schema(report,snapshot,forms):
 names={row[0]:str(row[1]).lstrip(':') for row in snapshot['attributes']}
 idents={str(ident):eid for eid,ident in snapshot['idents']}
 expected=set()
 for form in forms:
  entity=report[':edb/tempids'][form[':db/id']]
  expected.add((0,'db.install/attribute',dumps(entity)))
  for attr,value in form.items():
   if str(attr)==':db/id':continue
   if str(attr) in {':db/valueType',':db/cardinality',':db/unique'}:value=idents[str(value)]
   expected.add((entity,str(attr).lstrip(':'),dumps(value)))
 actual=set()
 for eid,aid,val,tx,source,added in report[':edb/tx-data']:
  assert source==idents[':application/ca-engine'] and added is True
  name=names[aid]
  if name=='db/txInstant':continue
  actual.add((eid,name,dumps(val)))
 assert actual==expected,(actual-expected,expected-actual)
 return {'exact_schema_datoms_verified':len(actual)}

class SchemaCommitter(GeneratorCommitter):
 def preview(self,batch,snapshot):
  (self.directory/'transaction.edn').write_text(dumps(batch['forms'])+'\n')
  raw=self.client.command('with','--file',self.directory/'transaction.edn','--source',batch['source'])
  (self.directory/'preview.edn').write_text(raw);report=loads(raw)
  if report[':edb/db-before-t']!=snapshot['basis']:raise StaleBasis('Schema preview basis advanced')
  assert report[':edb/committed'] is False
  verify_schema(report,snapshot,batch['forms']);return report
 def verify_receipt(self,request,receipt):
  assert receipt[':edb/committed'] is True and receipt[':edb/db-before-t']==request['basis']
  return verify_schema(receipt,loads(request['snapshot_edn']),loads(request['batch_edn'])['forms'])

p=Publisher.from_environment();c=p.client;committer=SchemaCommitter(p.config,c,E)
for attempt in range(3):
 pending=committer.pending()
 if pending is None:
  status=c.status();basis=status['basis']
  attrs=c.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],E,'attributes',basis)
  ids=c.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],E,'idents',basis)
  snap={'basis':basis,'lineage':status['lineage'],'attributes':attrs,'idents':ids}
  batch={'source':p.config.source,'forms':forms,'assertions':[],'retractions':[]}
  try:committer.preview(batch,snap)
  except StaleBasis:continue
  pending=committer.save_request(batch,snap,digest(batch))
 try:receipt=committer.submit(pending)
 except StaleBasis:
  committer.retire(pending,'rejected_stale_basis',{'reason':'Concurrent publication; refresh schema basis'});continue
 committer.verify_receipt(pending,receipt)
 rows=c.query('[:find (pull ?a [:db/ident :db/isComponent {:db/valueType [:db/ident]} {:db/cardinality [:db/ident]} {:db/unique [:db/ident]}]) :in $ [?ident ...] :where [?a :db/ident ?ident]]',[[kw(n[1:]) for n in names]],E,'readback',receipt[':edb/db-after-t'])
 assert len(rows)==4
 result={'passed':True,'basis':receipt[':edb/db-after-t'],'attributes':jsonable(rows)}
 (E/'verification.json').write_text(json.dumps(result,indent=2)+'\n');committer.retire(pending,'verified',result)
 target=Path('/media/jake/SSD/EDB/math/schema/learner/3-learner-task.edn')
 text=target.read_text();assert ' {:db/ident :task-item/next' in text
 if ':task-item/working-periods' not in text:target.write_text(text.replace(' {:db/ident :task-item/next',dumps(forms)[1:-1]+'\n\n {:db/ident :task-item/next',1))
 print(json.dumps({'passed':True,'basis':result['basis'],'installed_attributes':names}));break
else:raise RuntimeError('Schema installation repeatedly raced; saved request retained')
