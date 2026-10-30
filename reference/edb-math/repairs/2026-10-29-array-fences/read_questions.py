import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/array-fences-2026-10-29';sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
D=H/'readback';D.mkdir(exist_ok=True);db=connection();basis=json.loads((H/'inventory.json').read_text())['basis_t'];ps=json.loads((H/'proposals.json').read_text());parents={int(k):v for k,v in json.loads((W/'parents.json').read_text()).items()};meta={int(k):v for k,v in json.loads((W/'metadata.json').read_text()).items()};ids={17592186551286};affected_kps=set();field_ids=set()
for p in ps:
 if p['attribute'].startswith('question/'):ids.add(p['entity'])
 if p['attribute'].startswith('answer-field/'):field_ids.add(p['entity'])
 if p['attribute'].startswith('answer/'):field_ids.update(e for e,a in parents.get(p['entity'],[])if a=='answer-field/choices')
for f in field_ids:ids.update(q for q,a in parents.get(f,[])if a=='question/answer-fields')
ids=sorted(ids);q='[:find (pull ?q [* {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/choices [* {:answer/type [:db/ident]}]} {:answer-field/correct [:db/id]}]}]) :in $ [?q ...] :where [?q :question/id _]]';rows=[]
for offset in range(0,len(ids),80):rows+=db.query(q,[ids[offset:offset+80]],D,'questions-'+str(offset),basis)
assert len(rows)==len(ids);qs=[r[0]for r in rows];(H/'questions.json').write_text(json.dumps(qs,default=str,indent=2)+'\n')
changes={(p['entity'],':'+p['attribute']):p['after']for p in ps}
for obj in qs:
 keys=[]
 for f in obj.get(':question/answer-fields',[]):
  old=f[':answer-field/key'];new=changes.get((f[':db/id'],':answer-field/key'),old);keys.append(new)
  if old!=new:assert '{{'+old+'}}'not in obj[':question/problem'],'Checkbox label used as blank placeholder'
 if any((f[':db/id'],':answer-field/key')in changes for f in obj.get(':question/answer-fields',[])):assert len(keys)==len(set(keys))
for eid in ids:affected_kps.update(k for k,a in parents.get(eid,[])if a in ['knowledge-point/questions','knowledge-point/canonical-example'])
generators=[]
for kp in sorted(affected_kps):
 g=meta[kp].get('knowledge-point/question-generator');ref=meta.get(g,{}).get('question-generator/script')
 if ref:generators.append({'kp':kp,'title':meta[kp].get('knowledge-point/title'),'generator':g,'reference':ref})
(H/'affected-generators.json').write_text(json.dumps(generators,indent=2)+'\n');(H/'ownership.json').write_text(json.dumps({'questions':ids,'key_fields':sorted(field_ids),'knowledge_points':sorted(affected_kps),'generators':len(generators),'checkbox_labels_unique_no_placeholders':True},indent=2)+'\n');print('Read',len(rows),'completequestions at',basis,';',len(generators),'affected generators;',len(affected_kps),'KPs',flush=True)
