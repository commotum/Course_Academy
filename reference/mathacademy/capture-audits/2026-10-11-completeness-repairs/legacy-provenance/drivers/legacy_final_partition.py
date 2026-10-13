import hashlib, json, re, threading, time
from pathlib import Path
from scripts.config import Config
from scripts.storage import read_json, atomic_json
from scripts.database.client import EDBClient
from scripts.database.edn import loads, kw
from scripts.database.prepare import ALLOWED
from scripts.database.images import ImageLibrary
from scripts.database.text import markdown
from scripts.legacy_recovery import current_supported_reviews, authoritative_question

root=Path('reference/mathacademy/capture-audits/2026-10-11-completeness-repairs/legacy-provenance')
comparison=read_json(root/'database-comparison.json'); basis=comparison['database']['basis']
proof=root/'final-aggregate-partition'/str(time.time_ns());proof.mkdir(parents=True)
old={}
for file in Path(comparison['readback_directory']).glob('questions-*.edn'):
    if not re.fullmatch(r'questions-\d+\.edn',file.name):continue
    old.update((row[0][':question/math-academy-id'],row[0]) for row in loads(file.read_text()))
records=current_supported_reviews(root); config=Config(); client=EDBClient(config,threading.Event())
manifests={scope:read_json(root/('database-'+scope+'-repair-candidates.json')) for scope in ('structural','control','answer')}
packages={scope:manifest['prepared'] for scope,manifest in manifests.items()}
selected={scope:sorted(q for p in held for q in p['question_ids']) for scope,held in packages.items()}
eid_questions={}; rows=[]
def typed(a):return (a[':answer/type'][':db/ident'].rsplit('/',1)[-1],a[':answer/value'])
for scope,mids in selected.items():
    for mid in mids:
        record=records[mid];q=ImageLibrary(config.math_root,Path(record['directory'])).question(authoritative_question(record['question']))
        held=old[mid]; eids={held[':db/id']};fields=[];blocked=[]
        state=read_json(Path(record['directory'])/'state.json')['questions'][mid]
        original_fields={f['key']:f for f in state['before']['fields']}
        old_fields={f[':answer-field/key']:f for f in held[':question/answer-fields']}
        if len(old_fields)!=len(held[':question/answer-fields']):blocked.append('duplicate_historical_field_keys')
        for field in held[':question/answer-fields']:
            eids.add(field[':db/id']);eids.update(c[':db/id'] for c in field[':answer-field/choices'])
            if field.get(':answer-field/correct'):eids.add(field[':answer-field/correct'][':db/id'])
        if set(old_fields)!={f['key'] for f in q['answer_fields']}:blocked.append('changed_field_keys')
        for incoming in q['answer_fields']:
            f=old_fields[incoming['key']];eids.add(f[':db/id'])
            eids.update(c[':db/id'] for c in f[':answer-field/choices']);eids.add(f[':answer-field/correct'][':db/id'])
            wanted={(c['type'],c['value']) for c in incoming['choices']};by_value={}
            for c in f[':answer-field/choices']:by_value.setdefault(typed(c),[]).append(c)
            duplicates=[{'typed':value,'entities':[c[':db/id'] for c in choices],'owners':[c.get(':task-item/_responses',[]) for c in choices]} for value,choices in by_value.items() if len(choices)>1]
            if duplicates:blocked.append('duplicate_choice_entities')
            removed=[{'eid':c[':db/id'],'uuid':str(c[':answer/id']),'typed':typed(c),'response_owners':c.get(':task-item/_responses',[])} for c in f[':answer-field/choices'] if typed(c) not in wanted]
            if any(c['response_owners'] for c in removed):blocked.append('historical_response_ownership')
            correct=typed(f[':answer-field/correct']);newcorrect=(incoming['correct_type'],incoming['correct_value'])
            raw=original_fields[incoming['key']]
            oldoptions=[str(c.get('option')) for c in raw['choices'] if (c['type'],c['value'])==correct]
            newoptions=[str(c.get('source_option',c.get('option'))) for c in incoming['choices'] if (c['type'],c['value'])==newcorrect]
            option_status='unchanged_typed_correct' if correct==newcorrect else 'same_original_source_option' if len(oldoptions)==len(newoptions)==1 and oldoptions==newoptions else 'requires_independent_key_qc'
            if scope=='control' and option_status=='requires_independent_key_qc':blocked.append('key_option_identity_unresolved')
            fields.append({'key':incoming['key'],'uuid':str(f[':answer-field/id']),'old_correct':correct,'new_correct':newcorrect,'old_source_options':oldoptions,'new_source_options':newoptions,'correct_option_identity':option_status,'removed_choices':removed,'duplicate_typed_entities':duplicates})
        for eid in eids:eid_questions.setdefault(eid,set()).add(mid)
        diffs=[]
        for part,attr in [('problem',':question/problem'),('worked_solution',':question/worked-solution')]:
            candidate=markdown(q[part]);previous=held.get(attr)
            if candidate!=previous:diffs.append({'part':part,'before':previous,'after':candidate})
        rows.append({'id':mid,'scope':scope,'directory':record['directory'],'source_hash':record['source_hash'],'question_uuid':str(held[':question/id']),'question_eid':held[':db/id'],'source_bindings':q.get('source_reconstruction',{}).get('bindings',[]),'fields':fields,'text_diffs':diffs,'block_reasons':sorted(set(blocked)),'active_fact_sources':[]})
by_mid={row['id']:row for row in rows}; eids=sorted(eid_questions)
attrs=[kw(':'+a) for a in ALLOWED if a.startswith(('question/','answer-field/','answer/')) and not a.endswith('/id')]
for start in range(0,len(eids),100):
    facts=client.query('[:find ?e ?a ?source :in $ [?e ...] [?a ...] :where [?e ?a _ _ ?s] [?s :db/ident ?source]]',[eids[start:start+100],attrs],proof,'active-sources-'+str(start),basis)
    for eid,attr,source in facts:
        for mid in eid_questions[eid]:
            row=by_mid[mid];row['active_fact_sources'].append([eid,str(attr),str(source)])
            if str(source)!=':org/Math-Academy':row['block_reasons'].append('separately_attributed_correction')
removed=sorted({c['eid'] for row in rows for f in row['fields'] for c in f['removed_choices']})
owners=[]
for start in range(0,len(removed),100):
    owners.extend(client.query('[:find ?answer ?item :in $ [?answer ...] :where [?item :task-item/responses ?answer]]',[removed[start:start+100]],proof,'removed-choice-owners-'+str(start),basis))
owned={r[0] for r in owners}
for row in rows:
    if any(c['eid'] in owned for f in row['fields'] for c in f['removed_choices']):row['block_reasons'].append('historical_response_ownership')
    if not row['active_fact_sources']:row['block_reasons'].append('missing_active_source_proof')
    row['block_reasons']=sorted(set(row['block_reasons']))
result={'database':comparison['database'],'database_writes':0,'readback_directory':str(proof),'questions':rows,'eligible':{scope:[r['id'] for r in rows if r['scope']==scope and not r['block_reasons']] for scope in selected},'blocked':{scope:[r['id'] for r in rows if r['scope']==scope and r['block_reasons']] for scope in selected},'native_exact_removed_answer_owners':owners,'completed_at':time.time()}
atomic_json(proof/'partition.json',result);atomic_json(root/'final-aggregate-partition.json',result)
print(json.dumps({'eligible':{s:len(v) for s,v in result['eligible'].items()},'blocked':{s:len(v) for s,v in result['blocked'].items()},'reasons':{r['id']:r['block_reasons'] for r in rows if r['block_reasons']},'proof':str(proof)},ensure_ascii=False))
