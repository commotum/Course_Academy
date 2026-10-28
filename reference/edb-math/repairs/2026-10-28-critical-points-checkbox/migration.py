"""Guarded lesson-scoped conversion; exact requests and historical semantics."""
import copy,hashlib,json,sys,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable,loads,dumps,kw,digest,StaleBasis
from capture.scripts.database.commit import Committer,VerificationError
from capture.scripts.storage import atomic_json,atomic_text
from capture.scripts.database.preview import native_executable
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from core import stable_id
Q_PATTERN='''[* {:question/difficulty [:db/ident]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/ident]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/ident]}]} {:answer-field/correct [* {:answer/type [:db/ident]}]}]}
 {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:task-item/_content :limit nil] [* {:task-item/status [:db/ident]} {[:task-item/responses :limit nil] [* {:answer/type [:db/ident]}]}]}]'''
RETAIN='''[* {:answer-field/type [:db/ident]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/ident]}]} {:answer-field/correct [* {:answer/type [:db/ident]}]}]'''
ALLOWED={'answer/id','answer/type','answer/value','answer-field/id','answer-field/key','answer-field/type','answer-field/choices','answer-field/correct','question/problem','question/worked-solution','question/answer-fields','task-item/responses'}

def validate_report(report,batch,snapshot,committed=False):
 if committed:assert report.get(':edb/committed') is True
 names={r[0]:str(r[1]).lstrip(':') for r in snapshot['attributes']};types={str(r[1]).lstrip(':'):str(r[2]) for r in snapshot['attributes']};idents={str(i):e for e,i in snapshot['idents']};source=idents[batch['source']];temps=report[':edb/tempids']
 def ent(x):return temps.get(x,idents.get(x,x)) if isinstance(x,str) else x
 def expected(rows):return {(ent(e),str(a).lstrip(':'),dumps(ent(v) if types[str(a).lstrip(':')]==':db.type/ref' else v)) for e,a,v in rows}
 actual={True:set(),False:set()}
 for e,a,v,tx,s,added in report[':edb/tx-data']:
  assert s==source
  name=names[a]
  if name=='db/txInstant':assert added;continue
  assert name in ALLOWED,('Unexpected datom',e,name)
  actual[added].add((e,name,dumps(v)))
 assert actual[True]==expected(batch['assertions']) and actual[False]==expected(batch['retractions'])
 return {'source_eid':source,'assertions':len(actual[True]),'retractions':len(actual[False]),'only_reviewed_content_and_response_links_changed':True}

class MigrationCommitter(Committer):
 def preview(self,batch,snapshot):
  atomic_text(self.directory/'transaction.edn',dumps(batch['forms'])+'\n');report=loads(self.client.command('with','--file',self.directory/'transaction.edn','--source',batch['source']));atomic_text(self.directory/'preview.edn',dumps(report)+'\n')
  if report[':edb/db-before-t']!=snapshot['basis']:raise StaleBasis('Database advanced before native preview')
  assert report.get(':edb/committed') is False;validate_report(report,batch,snapshot);return report
 def verify_receipt(self,request,receipt):
  assert receipt[':edb/db-before-t']==request['basis'];return validate_report(receipt,loads(request['batch_edn']),loads(request['snapshot_edn']),True)

def portable(q):
 q=copy.deepcopy(q)
 for f in q.get(':question/answer-fields',[]):
  f[':answer-field/type']=f[':answer-field/type'].get(':db/ident') if isinstance(f[':answer-field/type'],dict) else f[':answer-field/type']
  for a in f[':answer-field/choices']:
   if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
  if isinstance(f.get(':answer-field/correct'),dict):f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 return q

def prepare(p,directory):
 directory=Path(directory);directory.mkdir(parents=True,exist_ok=True);status=p.client.status();basis=status['basis'];audit=json.loads((H/'case-ledger.json').read_text());allids=json.loads((H/'capture.json').read_text())['question_ids']
 rows=[]
 for start in range(0,len(allids),20):rows+=p.client.query('[:find (pull ?q '+Q_PATTERN+') :in $ [?q ...] :where [?q :question/id _]]',[allids[start:start+20]],directory,f'before-{start}',basis)
 before={q[':db/id']:q for [q] in rows};forms=[];adds=[];retracts=[];proposed=[];plans=[];mappings=[];retained=set();newids=[];retired_fields=[]
 def add(e,a,v):forms.append([kw('db/add'),e,kw(a),v]);adds.append([e,kw(a),v])
 def retract(e,a,v):forms.append([kw('db/retract'),e,kw(a),v]);retracts.append([e,kw(a),v])
 def cas(e,a,old,new):forms.append([kw('db/cas'),e,kw(a),old,new]);adds.append([e,kw(a),new]);retracts.append([e,kw(a),old])
 def ensure(e,spec):forms.append([kw('db/ensure'),e,kw(spec)])
 for row in audit:
  if row['decision'] not in ('convert','remove_redundant_none'):continue
  eid=row['question_eid'];q=before[eid];assert q[':question/problem']==row['problem_before'];assert jsonable(q.get(':question/worked-solution'))==row['worked_solution_before']
  fs=q[':question/answer-fields'];old_fields=copy.deepcopy(fs);pq=copy.deepcopy(q);lookup={};objects=[]
  if row['decision']=='convert':
   assert len(fs)==1 and str(fs[0][':answer-field/type'][':db/ident'])==':answer-field.type/radio'
   assert jsonable(fs)==row['old_fields'];f=fs[0];oldbank={a[':db/id']:a for a in f[':answer-field/choices']};correct={o['source_label'] for o in row['objects'] if o['selected']};choice_map={c['old_answer']:set(c['selected']) for c in row['choice_mapping']}
   retained.update([f[':db/id'],*oldbank]);retired_fields.append(f[':db/id']);newfields=[]
   for obj in row['objects']:
    token=q[':question/math-academy-id']+'/authored-checkbox-v1/'+obj['source_label'];fid='field:'+token;fu=stable_id('field',token);newids.append(fu);answers=[]
    for value in ('false','true'):
     aid='answer:'+token+'/'+value;au=stable_id('answer',token+'/'+value);newids.append(au);answers.append({':answer/id':str(au),':answer/type':':answer.type/text',':answer/value':value})
     add(aid,'answer/id',au);add(aid,'answer/type',kw('answer.type/text'));add(aid,'answer/value',value);ensure(aid,'answer/validate');lookup[(obj['source_label'],value)]=aid
    add(fid,'answer-field/id',fu);add(fid,'answer-field/key',obj['content']);add(fid,'answer-field/type',kw('answer-field.type/checkbox'))
    for value in ('false','true'):add(fid,'answer-field/choices',lookup[(obj['source_label'],value)])
    add(fid,'answer-field/correct',lookup[(obj['source_label'],str(obj['selected']).lower())]);ensure(fid,'answer-field/validate');add(eid,'question/answer-fields',fid)
    correct_uuid=next(a[':answer/id'] for a in answers if a[':answer/value']==str(obj['selected']).lower());newfields.append({':answer-field/id':str(fu),':answer-field/key':obj['content'],':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_uuid]});objects.append({**obj,'field_id':str(fu)})
   retract(eid,'question/answer-fields',f[':db/id']);cas(eid,'question/problem',q[':question/problem'],row['problem_after']);pq[':question/problem']=row['problem_after'];pq[':question/answer-fields']=newfields
   if 'solution_after' in row:cas(eid,'question/worked-solution',q[':question/worked-solution'],row['solution_after']);pq[':question/worked-solution']=row['solution_after']
   for item in q.get(':task-item/_content',[]):
    old=item.get(':task-item/responses',[])
    if not old:continue
    assert len(old)==1 and old[0][':db/id'] in oldbank
    selected=choice_map[old[0][':db/id']];state=str(item[':task-item/status'][':db/ident'])
    if state in (':task-item.status/correct',':task-item.status/incorrect'):assert (selected==correct)==state.endswith('/correct')
    retract(item[':db/id'],'task-item/responses',old[0][':db/id']);new_refs=[lookup[(obj['source_label'],str(obj['source_label'] in selected).lower())] for obj in row['objects']]
    for aid in new_refs:add(item[':db/id'],'task-item/responses',aid)
    ensure(item[':db/id'],'task-item/validate');mappings.append({'item':item[':db/id'],'question':eid,'before':jsonable(item),'new_answer_tempids':new_refs,'selected':sorted(selected),'old_answer':old[0][':db/id']})
  else:
   none=next(f for f in fs if f[':answer-field/key']=='None of the above');assert jsonable(none)==row['removed_field'];retained.update([none[':db/id'],*[a[':db/id'] for a in none[':answer-field/choices']]]);retired_fields.append(none[':db/id']);retract(eid,'question/answer-fields',none[':db/id']);pq[':question/answer-fields']=[f for f in fs if f[':db/id']!=none[':db/id']];objects=row['objects']
   for item in q.get(':task-item/_content',[]):
    old=item.get(':task-item/responses',[]);none_ids={a[':db/id'] for a in none[':answer-field/choices']};none_response=[a for a in old if a[':db/id'] in none_ids]
    if not old:continue
    assert len(none_response)==1 and none_response[0][':answer/value']=='false','Contradictory or partial None response requires separate review'
    retract(item[':db/id'],'task-item/responses',none_response[0][':db/id']);ensure(item[':db/id'],'task-item/validate');mappings.append({'item':item[':db/id'],'question':eid,'before':jsonable(item),'removed_answer':none_response[0][':db/id'],'retained_answer_ids':[a[':db/id'] for a in old if a[':db/id'] not in none_ids]})
  ensure(eid,'question/validate');proposed.append({'question':portable(jsonable(pq)),'objects':objects});plans.append({'question':eid,'decision':row['decision'],'objects':objects,'choice_mapping':row.get('choice_mapping',[]),'old_fields':jsonable(old_fields)})
 assert len(proposed)==10
 collisions=p.client.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[newids],directory,'identity-collisions',basis);assert not collisions
 fieldrows=p.client.query('[:find (pull ?f [:db/id {[:question/_answer-fields :limit nil] [:db/id]}]) :in $ [?f ...] :where [?f :answer-field/id _]]',[retired_fields],directory,'field-owners',basis)
 def refs(value):return value if isinstance(value,list) else [value] if value else []
 fieldowners=[(f[':db/id'],owner[':db/id']) for [f] in fieldrows for owner in refs(f.get(':question/_answer-fields'))]
 assert {q for f,q in fieldowners}<={r['question'] for r in plans} and len(fieldowners)==len(retired_fields)
 oldanswers=[a[':db/id'] for r in plans for f in r['old_fields'] for a in f[':answer-field/choices']]
 answerrows=p.client.query('[:find (pull ?a [:db/id {[:answer-field/_choices :limit nil] [:db/id]} {[:task-item/_responses :limit nil] [:db/id {:task-item/content [:db/id]}]}]) :in $ [?a ...] :where [?a :answer/id _]]',[oldanswers],directory,'answer-owners-and-users',basis)
 owners=[(a[':db/id'],f[':db/id']) for [a] in answerrows for f in refs(a.get(':answer-field/_choices'))]
 assert all(f in {f[':db/id'] for r in plans for f in r['old_fields']} for a,f in owners) and len(owners)==len(set(oldanswers))
 users=[(a[':db/id'],item[':db/id'],item[':task-item/content'][':db/id']) for [a] in answerrows for item in refs(a.get(':task-item/_responses'))]
 expected_items={item[':db/id'] for r in plans for item in before[r['question']].get(':task-item/_content',[]) if item.get(':task-item/responses')}
 assert {item for a,item,q in users}==expected_items
 assert all(item in {i[':db/id'] for i in before[q].get(':task-item/_content',[])} for a,item,q in users)
 retrows=p.client.query('[:find (pull ?e '+RETAIN+') :in $ [?e ...] :where (or-join [?e] [?e :answer-field/id _] [?e :answer/id _])]',[sorted(retained)],directory,'retained-before',basis)
 attrs=p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],directory,'attributes',basis);idents=p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],directory,'idents',basis)
 snapshot={'basis':basis,'lineage':status['lineage'],'attributes':attrs,'idents':idents};batch={'source':':agent/codex','forms':forms,'assertions':adds,'retractions':retracts}
 atomic_json(directory/'before.json',jsonable(list(before.values())));atomic_text(directory/'before.edn',dumps(list(before.values())));atomic_json(directory/'retained-before.json',jsonable([q for [q] in retrows]));atomic_json(directory/'proposed-presentation.json',{'cases':proposed});atomic_json(directory/'render-input.json',[{'question':r['question']} for r in proposed]);atomic_text(directory/'question-pull.edn',Q_PATTERN);atomic_text(directory/'retained-pull.edn',RETAIN);atomic_text(directory/'question-ids.txt','\n'.join(map(str,allids)));atomic_text(directory/'retained-ids.txt','\n'.join(map(str,sorted(retained))))
 prepared={'basis':basis,'lineage':status['lineage'],'batch_edn':dumps(batch),'snapshot_edn':dumps(snapshot),'before_edn':dumps(list(before.values())),'plans':plans,'response_mappings':mappings,'all_question_ids':allids,'retained_ids':sorted(retained),'proposed':proposed};atomic_json(directory/'preparation.json',prepared)
 return prepared
