"""Read-only capture of the keyed/rated next discovery tier; no submit API."""
import argparse,collections,hashlib,importlib.util,json,re,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'Cargo.toml').exists())
AUDIT=ROOT/'generate/reports/checkbox-discovery-2026-10-12'
spec=importlib.util.spec_from_file_location('checkbox_reference',OUT.parent/'finder-easy/prepare.py')
edb=importlib.util.module_from_spec(spec);spec.loader.exec_module(edb);edb.OUT=OUT
edb.DB.args.capture_only=True

def main(basis_override=None):
 assert not list(OUT.glob('batch-*/commit*')),'Do not replace submitted preparations'
 report=json.loads((AUDIT/'report.json').read_text())
 metadata={q[':db/id']:q for q in json.loads((AUDIT/'readiness-metadata.json').read_text())}
 completed={q['id']for q in json.loads((AUDIT/'direct-candidates.json').read_text())['questions']}
 rows=[q for q in report['strong_candidates']if q['id']not in completed and metadata[q['id']].get(':question/difficulty')and q['fields']and all(f.get(':answer-field/correct')for f in q['fields'])]
 edb.save('audit-input.json',rows)
 status=edb.DB.command('status');live_basis=int(re.search(r'\bbasis_t=(\d+)',status)[1]);basis=live_basis if basis_override is None else basis_override
 assert basis<=live_basis
 assert 'lineage='+report['lineage']in status
 previous=json.loads((OUT/'capture-start.json').read_text())if (OUT/'capture-start.json').exists()else {}
 original_read=edb.read
 def cached_read(query,inputs,name,t):
  directory=OUT/'evidence';result=directory/(name+'.edn');qp=directory/(name+'-query.edn');ip=directory/(name+'-inputs.edn')
  if previous.get('basis')==t and result.exists()and qp.exists()and ip.exists()and qp.read_text().strip()==query.strip()and ip.read_text().strip()==edb.dumps(inputs):
   return edb.loads(result.read_text())
  return original_read(query,inputs,name,t)
 edb.read=cached_read
 edb.save('capture-start.json',{'basis':basis,'lineage':report['lineage'],'status':status})
 ids=sorted(q['id']for q in rows)
 questions=edb.batches('[:find (pull ?q '+edb.QUESTION+') :in $ [?q ...] :where [?q :question/id _]]',ids,'questions',basis,96)
 assert {r[0][':db/id']for r in questions}==set(ids)
 items=edb.batches('[:find ?q (pull ?item '+edb.ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]',ids,'items',basis,128)
 answers=sorted({a[':db/id']for r in questions for f in r[0].get(':question/answer-fields',[])for a in f.get(':answer-field/choices',[])})
 fields=sorted({f[':db/id']for r in questions for f in r[0].get(':question/answer-fields',[])})
 users=edb.batches('[:find ?a (pull ?item '+edb.ITEM+') :in $ [?a ...] :where [?item :task-item/responses ?a]]',answers,'response-users',basis,256)
 owned_fields=edb.batches('[:find ?f (pull ?f [{[:question/_answer-fields :limit nil] [:db/id]}]) :in $ [?f ...] :where [?f :answer-field/id _]]',fields,'field-owners',basis,128)
 def refs(value):return [value]if isinstance(value,dict)else value
 field_owners=[[f,q[':db/id']]for f,data in owned_fields for q in refs(data.get(':question/_answer-fields',[]))]
 owned_answers=edb.batches('[:find ?a (pull ?a [{[:answer-field/_choices :limit nil] [:db/id]}]) :in $ [?a ...] :where [?a :answer/id _]]',answers,'answer-owners',basis,128)
 answer_owners=[[a,f[':db/id']]for a,data in owned_answers for f in refs(data.get(':answer-field/_choices',[]))]
 attrs=edb.DB.attributes(OUT/'evidence',basis)
 source=edb.read('[:find (pull ?s [:db/id :db/ident :db/doc]) :in $ ?ident :where [?s :db/ident ?ident]]',[edb.kw(edb.SOURCE)],'source',basis)
 assert len(source)==1
 data={'basis':basis,'lineage':report['lineage'],'status':status,'source':source,'questions':questions,'items':items,'response_users':users,'field_owners':field_owners,'answer_owners':answer_owners,'attributes':attrs}
 (OUT/'snapshot.edn').write_text(edb.dumps(data)+'\n')
 edb.save('snapshot.json',json.loads(json.dumps(data,default=str)))
 current={q[':db/id']:q for q, in questions}
 counts=collections.Counter(f[':answer-field/type'][':db/ident']for q in current.values()for f in q.get(':question/answer-fields',[]))
 manifest={'state':'captured_for_review','basis':basis,'lineage':report['lineage'],'historical_basis':report['basis'],'historical_candidate_questions':len(ids),'presentations':len(items),'response_links':len(users),'source':edb.SOURCE,'current_field_types':dict(counts),'snapshot_sha256':hashlib.sha256((OUT/'snapshot.edn').read_bytes()).hexdigest(),'database_writes':0}
 edb.save('capture.json',manifest);edb.save('status.json',manifest)
 print(json.dumps(manifest),flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--basis',type=int)
 main(parser.parse_args().basis)
