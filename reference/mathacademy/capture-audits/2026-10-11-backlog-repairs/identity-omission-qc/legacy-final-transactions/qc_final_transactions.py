import json,collections,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
from scripts.database.edn import loads
from scripts.legacy_recovery import current_supported_reviews,source_record
R=Path('reference/mathacademy/capture-audits/2026-10-11-completeness-repairs/legacy-provenance');out=[]
previews=json.loads((R/'final-source-aggregate-previews.json').read_text())
for scope,p in previews.items():
 proof=Path(p['readback_directory']);old={q[':question/math-academy-id']:q for f in proof.glob('before-*.edn') if '-inputs' not in f.name and '-query' not in f.name for row in loads(f.read_text()) for q in row};qids={q[':db/id'] for q in old.values()};fields={f[':db/id']:f for q in old.values() for f in q[':question/answer-fields']};answers={a[':db/id']:a for f in fields.values() for a in f[':answer-field/choices']};tx=loads((Path(p['directory'])/'database/transaction.edn').read_text());counts=collections.Counter();retracted=[];issues=[]
 for e in tx:
  if isinstance(e,dict):
   eid=e[':db/id'];attrs=set(e)-{':db/id',':db/ensure'};counts.update(attrs)
   allowed={':question/problem',':question/worked-solution'} if eid in qids else {':answer-field/choices',':answer-field/correct'} if eid in fields else {':answer/id',':answer/type',':answer/value'} if isinstance(eid,str) else set()
   if not attrs<=allowed:issues.append(('unexpected map',eid,list(attrs)))
   if scope=='structural' and eid not in qids:issues.append(('structural altered field',eid))
  else:
   if len(e)!=4 or e[0]!=':db/retract' or e[1] not in fields or e[2]!=':answer-field/choices' or e[3] not in answers:issues.append(('bad retraction',e))
   else:
    retracted.append(e[3]);counts['retract:answer-field/choices']+=1
    if answers[e[3]].get(':task-item/_responses'):issues.append(('owned retraction',e[3]))
 if retracted:
  inp=loads((proof/'exact-retracted-choice-response-owners-inputs.edn').read_text());assert sorted(inp[0])==sorted(set(retracted));assert loads((proof/'exact-retracted-choice-response-owners.edn').read_text())==[]
 sources=[row for f in proof.glob('active-sources-*.edn') if '-inputs' not in f.name and '-query' not in f.name for row in loads(f.read_text())];assert {str(row[-1]) for row in sources}=={':org/Math-Academy'}
 out.append({'scope':scope,'basis':p['before']['basis'],'questions':len(old),'edits':len(tx),'attributes':dict(counts),'exact_retracted_eids':len(set(retracted)),'native_owners':0,'active_sources':[':org/Math-Academy'],'issues':issues})
d=json.loads((R/'duplicate-field-repair-preview.json').read_text());proof=Path(d['readback_directory']);tx=loads((Path(d['package']['directory'])/'database/transaction.edn').read_text());reviewed=current_supported_reviews(R);issues=[];summ=[]
for q in d['questions']:
 mid=q['id'];review=reviewed[mid];source=source_record(Path(review['directory']),mid) if 'directory' in review else None
 # Authoritative binding specifies exact owning state independent of review path layout.
 ev=json.loads((Path(d['package']['directory'])/'source-evidence.json').read_text());b=next(x for x in ev['bindings'] if x['id']==mid);state=json.loads(Path(b['state_file']).read_text());before=state['questions'][mid]['before'];assert hashlib.sha256(before['html'].encode()).hexdigest()==q['original_html_sha256'];raw=BeautifulSoup(before['html'],'html.parser');ids=[x['id'] for x in raw.select('.questionWidget-choiceLetterCircle')];assert ids==q['original_circle_ids'];assert len(raw.select('.questionWidget-choicesTable'))==1
 retained=q['retained_field'];incoming=next(x for x in json.loads((Path(d['package']['directory'])/'content.json').read_text())['questions'] if x['math_academy_id']==mid)['answer_fields'][0];typed=lambda a:(a[':answer/type'][':db/ident'].split('/')[-1],a[':answer/value']);normalize=lambda typ,val: ('images/'+Path(val).name[:2]+'/'+Path(val).name) if typ=='image' else val;assert {typed(a) for a in retained[':answer-field/choices']}=={(a['type'],normalize(a['type'],a['value'])) for a in incoming['choices']},mid;assert typed(retained[':answer-field/correct'])==(incoming['correct_type'],normalize(incoming['correct_type'],incoming['correct_value'])),mid
 summ.append({'id':mid,'original_own_circles':ids,'retained_field_eid':retained[':db/id'],'unlinked_field_eids':q['removed_question_link_field_eids']})
assert len(tx)==8;assert len([e for e in tx if isinstance(e,dict)])==4
assert {(e[1],e[3]) for e in tx if not isinstance(e,dict)}=={(e[1],q['removed_question_link_field_eids'][0]) for q in d['questions'] for e in tx if not isinstance(e,dict) and e[3] in q['removed_question_link_field_eids']}
assert all(e[0]==':db/retract' and e[2]==':question/answer-fields' for e in tx if not isinstance(e,dict));assert all(set(e)-{':db/id',':db/ensure'}<={':question/problem',':question/worked-solution'} for e in tx if isinstance(e,dict));assert d['all_answer_native_response_owners']==[]
out.append({'scope':'four_unowned_duplicate_field_links','basis':d['before']['basis'],'edits':8,'text_maps':4,'link_retractions':4,'old_entities_altered':False,'raw_control_and_typed_signature_checks':summ,'issues':issues})
print(json.dumps(out,indent=2));Path('/tmp/legacy-final-transactions-independent-qc.json').write_text(json.dumps(out,indent=2))
