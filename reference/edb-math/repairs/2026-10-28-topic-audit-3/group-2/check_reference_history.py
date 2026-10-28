import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection,loads
D=H/'reference-history';D.mkdir(exist_ok=True);db=connection();basis=9912;C=json.loads((H/'current.json').read_text());groups=[];answers=[];fields=[];questions=[]
ns={"__file__":str(H/"propose_format.py")};exec((H/'propose_format.py').read_text().split('P=[]')[0],ns);neutral=lambda value:ns['neutral'](value.replace('θ',r'\theta'))
for q in C['questions']:
 dup=collections.defaultdict(list)
 for f in q.get(':question/answer-fields',[]):dup[f[':answer-field/key']].append(f)
 for key,fs in dup.items():
  if len(fs)<2:continue
  assert len(fs)==2;old=next(f for f in fs if not f.get(':answer-field/correct'));new=next(f for f in fs if f.get(':answer-field/correct'))
  aa={neutral(a[':answer/value']):a for a in old[':answer-field/choices']};bb={neutral(a[':answer/value']):a for a in new[':answer-field/choices']};equiv=aa.keys()==bb.keys()
  groups.append({'question':q[':db/id'],'math_academy_id':q.get(':question/math-academy-id'),'field_key':key,'old_field':old[':db/id'],'retained_field':new[':db/id'],'before_fields':[f[':db/id']for f in q[':question/answer-fields']],'after_fields':[f[':db/id']for f in q[':question/answer-fields']if f!=old],'old_answers':[a[':db/id']for a in old[':answer-field/choices']],'retained_answers':[a[':db/id']for a in new[':answer-field/choices']],'neutral_bank_equivalent':equiv,'bank_mapping':[{'before':aa[k][':db/id'],'retained':bb[k][':db/id'],'before_value':aa[k][':answer/value'],'retained_value':bb[k][':answer/value']}for k in aa if k in bb],'old_bank_unmatched':[k for k in aa if k not in bb],'new_bank_unmatched':[k for k in bb if k not in aa],'canonical':new[':answer-field/correct']})
  answers.extend(a[':db/id']for a in old[':answer-field/choices']);fields.append(old[':db/id']);questions.append(q[':db/id'])
answers.append(17592186675717)
queries={
 'current-responses':('[:find ?answer ?item :in $ [?answer ...] :where [?item :task-item/responses ?answer]]',[answers],False),
 'historical-responses':('[:find ?answer ?item ?tx ?source ?added :in $ [?answer ...] :where [?item :task-item/responses ?answer ?tx ?source ?added]]',[answers],True),
 'current-answer-ownership':('[:find ?answer ?field :in $ [?answer ...] :where [?field :answer-field/choices ?answer]]',[answers],False),
 'historical-answer-ownership':('[:find ?answer ?field ?tx ?source ?added :in $ [?answer ...] :where [?field :answer-field/choices ?answer ?tx ?source ?added]]',[answers],True),
 'current-field-ownership':('[:find ?field ?q :in $ [?field ...] :where [?q :question/answer-fields ?field]]',[fields],False),
 'historical-field-ownership':('[:find ?field ?q ?tx ?source ?added :in $ [?field ...] :where [?q :question/answer-fields ?field ?tx ?source ?added]]',[fields],True),
 'current-question-task-items':('[:find ?q ?item :in $ [?q ...] :where [?item :task-item/content ?q]]',[questions],False),
 'historical-question-task-items':('[:find ?q ?item ?tx ?source ?added :in $ [?q ...] :where [?item :task-item/content ?q ?tx ?source ?added]]',[questions],True)}
results={}
for name,(query,inputs,history)in queries.items():
 if name not in ('current-responses','historical-responses'):
  # Scalar reverse-reference probes avoid a collection join's overly broad scan.
  results[name]=[]
  variable='answer'if 'answer-ownership'in name else'field'if 'field-ownership'in name else'q'
  entities=answers if variable=='answer'else fields if variable=='field'else questions
  for entity in entities:
   scalar=query.replace('[:find ?'+variable+' ','[:find ',1).replace(':in $ [?'+variable+' ...]',':in $ ?'+variable)
   dest=D/(name+'-'+str(entity)+'.edn');rows=loads(dest.read_text())if dest.exists()else db.query(scalar,[entity],D,name+'-'+str(entity),basis,history=history)
   for row in rows:results[name].append([entity,*row])
 else:results[name]=loads((D/(name+'.edn')).read_text())if(D/(name+'.edn')).exists()else db.query(query,inputs,D,name,basis,history=history)
 print(name,len(results[name]),flush=True)
for g in groups:
 ids=set(g['old_answers']);g['current_response_refs']=[r for r in results['current-responses']if r[0]in ids];g['retained_history_response_refs']=[r for r in results['historical-responses']if r[0]in ids];g['hold_detach']=bool(g['current_response_refs']or g['retained_history_response_refs']or not g['neutral_bank_equivalent']);g['response_evidence']='reference-history/report.json'
report={'audit_basis':9837,'captured_current_basis':basis,'groups':groups,'answers':answers,'results':results,'limit':'All current refs and full retained history assertions/retractions at captured basis. No assertion about excised history. No database writes.'};(D/'report.json').write_text(json.dumps(report,indent=2,default=str)+'\n');(H/'duplicate-field-plans.json').write_text(json.dumps(groups,indent=2,default=str)+'\n');print('groups',len(groups),'held',sum(g['hold_detach']for g in groups))
