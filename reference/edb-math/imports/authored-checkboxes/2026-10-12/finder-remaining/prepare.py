"""Build and noncommit-preview the resolved batch; no submission entry point."""
import argparse
import collections
import hashlib
import importlib.util
import json
import re
import subprocess
import threading
from pathlib import Path
from types import SimpleNamespace

OUT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('easy_migration', OUT.parent / 'finder-easy/prepare.py')
edb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edb)
edb.OUT = OUT

def prompt_after(question, resolution):
    original = question[':question/problem']
    labels = resolution['labels']
    assert 'Select all that apply.' not in original
    if resolution['displayed_cases']:
        return original.rstrip() + '\n\nSelect all that apply. If none apply, leave all boxes unchecked.\n\n' + '\n'.join(
            '- **' + case['label'] + '.** ' + case['value'] for case in resolution['displayed_cases'])
    matches = list(edb.CASE_LINE.finditer(original))
    if matches:
        assert len(matches) == len(labels)
        counter = iter(labels)
        # Older fieldless imports have "I. - ..."; retain the statement once.
        def replacement(match):
            body = match[2].removeprefix('- ')
            return match[1] + '- **' + next(counter) + '.** ' + body
        changed = edb.CASE_LINE.sub(replacement, original)
        start = changed.index('- **' + labels[0] + '.** ')
        return changed[:start].rstrip() + '\n\nSelect all that apply.\n\n' + changed[start:]
    if original.startswith('!['):
        changed = original.rstrip() + '\n\nSelect all that apply.'
        if resolution['ma_id'] in ('q-36000','q-36897'):
            changed += '\n\nGraph positions: **I.** upper left; **II.** upper right; **III.** lower left; **IV.** lower right.'
        return changed
    head, sep, tail = original.partition('\n\n')
    assert sep and '?' in head
    # These original imports wrote matrix dimensions as products.
    if resolution['ma_id'] in ('q-69514','q-69515'):
        head = head.replace(r'\cdot', r'\times')
    return head + '\n\nSelect all that apply.\n\n' + tail

def build():
    assert not (OUT / 'commit-intent.json').exists() and not (OUT / 'commit.edn').exists()
    snapshot = edb.loads((OUT / 'snapshot.edn').read_text())
    resolutions = json.loads((OUT / 'resolutions.json').read_text())
    assert resolutions['all_cases_resolved'] and not resolutions['unresolved']
    assert resolutions['basis'] == snapshot['basis']
    assert not snapshot['items'] and not snapshot['response_users'], 'New learner responses must be explicitly mapped'
    before = {q[':db/id']: q for (q,) in snapshot['questions']}
    audit = {q['id']: q for q in json.loads((OUT / 'audit-input.json').read_text())}
    forms, changes, retained = [], [], set()
    existing_field_edits = []
    for resolution in resolutions['questions']:
        qid = resolution['id']
        q = before[qid]
        assert q[':question/problem'] == audit[qid]['problem'], 'Question changed since semantic review'
        assert not q.get(':knowledge-point/_canonical-example')
        assert resolution['kp'] in {kp[':db/id'] for kp in q[':knowledge-point/_questions']}
        fields = q.get(':question/answer-fields', [])
        for field in fields:
            assert field[':answer-field/type'][':db/ident'] == ':answer-field.type/radio'
            retained.add(field[':db/id'])
            retained.update(a[':db/id'] for a in field[':answer-field/choices'])
            assert not any(a.get(':answer/feedback') for a in field[':answer-field/choices']), 'Combination feedback needs individual review'
        if resolution['action'] == 'retain_radio':
            continue
        authored_solution = None
        worked_repair = resolution.get('worked_solution_repair')
        if worked_repair:
            assert q[':question/worked-solution'] == worked_repair['before']
            forms.append([edb.kw('db/cas'),qid,edb.kw('question/worked-solution'),worked_repair['before'],worked_repair['after']])
        if not q.get(':question/worked-solution'):
            assert ':question/worked-solution' not in q
            authored_solution = resolution['reason']
            forms.append([edb.kw('db/cas'), qid, edb.kw('question/worked-solution'), None, authored_solution])
        if resolution['action'] == 'retain_radio_repair_key':
            assert len(fields) == 1 and not fields[0].get(':answer-field/correct')
            answer = next(a for a in fields[0][':answer-field/choices']
                if a[':answer/value'] == resolution['resolved_radio_value'])
            forms.append([edb.kw('db/cas'),fields[0][':db/id'],edb.kw('answer-field/correct'),None,answer[':db/id']])
            forms.append([edb.kw('db/ensure'),fields[0][':db/id'],edb.kw('answer-field/validate')])
            forms.append([edb.kw('db/ensure'),qid,edb.kw('question/validate')])
            existing_field_edits.append({'id':fields[0][':db/id'],'attribute':':answer-field/correct','new_value':answer[':db/id']})
            changes.append({'id':qid,'ma_id':resolution['ma_id'],'action':resolution['action'],
                'authored_solution':authored_solution,'radio_field':fields[0][':db/id'],'correct_answer':answer[':db/id']})
            continue
        assert resolution['action'] == 'convert_checkbox'
        links, targets = [], {}
        for label in resolution['labels']:
            token = resolution['ma_id'] + '/authored-checkbox-v1/' + label
            fid = 'field-' + token
            answers = []
            for value in ('false','true'):
                aid = 'answer-' + token + '/' + value
                forms.append({edb.kw('db/id'):aid,edb.kw('answer/id'):edb.stable_id('answer',token+'/'+value),
                    edb.kw('answer/type'):edb.kw('answer.type/text'),edb.kw('answer/value'):value,
                    edb.kw('db/ensure'):edb.kw('answer/validate')})
                answers.append(aid)
                targets[(label,value)] = aid
            forms.append({edb.kw('db/id'):fid,edb.kw('answer-field/id'):edb.stable_id('field',token),
                edb.kw('answer-field/key'):label,edb.kw('answer-field/type'):edb.kw('answer-field.type/checkbox'),
                edb.kw('answer-field/choices'):answers,
                edb.kw('answer-field/correct'):answers[int(label in resolution['correct'])],
                edb.kw('db/ensure'):edb.kw('answer-field/validate')})
            links.append(fid)
        for field in fields:
            forms.append([edb.kw('db/retract'),qid,edb.kw('question/answer-fields'),field[':db/id']])
        new_prompt = prompt_after(q,resolution)
        forms.append([edb.kw('db/cas'),qid,edb.kw('question/problem'),q[':question/problem'],new_prompt])
        forms.append({edb.kw('db/id'):qid,edb.kw('question/answer-fields'):links,edb.kw('db/ensure'):edb.kw('question/validate')})
        mappings = []
        for old in resolution['choice_mapping']:
            mappings.append({**old,'new_answer_tempids':[
                targets[(label,str(label in old['selected']).lower())] for label in resolution['labels']]})
        changes.append({'id':qid,'ma_id':resolution['ma_id'],'action':resolution['action'],
            'kp':resolution['kp'],'labels':resolution['labels'],'correct':resolution['correct'],
            'old_fields':resolution['original_field_ids'],'new_field_tempids':links,
            'problem_before':q[':question/problem'],'problem_after':new_prompt,
            'authored_solution':authored_solution,'worked_solution_repair':worked_repair,'choice_mapping':mappings})
    path = OUT / 'transaction.edn'
    path.write_text('[\n'+'\n'.join(' '+edb.dumps(f) for f in forms)+'\n]\n')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert len(changes) == 90 and sum(q['action']=='convert_checkbox' for q in changes) == 89
    counts = {**resolutions['counts'],'questions_changed':len(changes),
        'knowledge_points_changed':len({r['kp'] for r in resolutions['questions'] if r['action']!='retain_radio'}),
        'new_boolean_answers':2*resolutions['counts']['new_checkbox_fields'],
        'worked_solutions_added':sum(bool(q['authored_solution']) for q in changes),
        'saved_responses_mapped':0,'learner_presentations':0}
    edb.save('plan.json',{'basis':snapshot['basis'],'source':edb.SOURCE,'transaction_sha256':digest,
        'resolution_sha256':hashlib.sha256((OUT/'resolutions.json').read_bytes()).hexdigest(),
        'counts':counts,'questions':changes,'existing_field_edits':existing_field_edits,
        'retained_original_entities':sorted(retained),
        'unchanged_question_ids':[r['id'] for r in resolutions['questions'] if r['action']=='retain_radio'],
        'learner_state':'All 91 reviewed questions have no current presentations or saved responses at this basis. A basis guard prevents using this plan after learner-state changes.',
        'notes':['All cases resolved; q-9852 and q-130626 remain radio because their complete solution sets are all real values. q-9852 receives its missing canonical answer and solution.',
            'All original question IDs, KP/topic memberships, mathematical conditions and images remain unchanged.',
            'Five existing gradient worked solutions receive targeted variable/component, denominator and cases-format repairs; their verified solution sets remain unchanged.',
            'Adds brief authored worked solutions where absent; local evidence and independent proofs retained in resolutions.json.',
            'All duplicate radio memberships are explicitly detached together; old field and answer entities remain retained. Only the retained radio field on q-9852 receives a missing-key assertion.',
            'Numeric options use the mathematical union of old choice atoms, normalize equivalent forms, and include the complete independently verified correct set.',
            'All-false answers represent the empty set. Every numeric question receives the same leave-unchecked instruction, so it does not reveal which keys are empty.',
            'Graph panel positions are made explicit for q-36000 and q-36897. Matrix dimension notation on q-69514 and q-69515 is standardized from a product dot to a multiplication cross.']})
    edb.save('prepared-request.json',{'state':'prepared_not_submitted','database':'math','endpoint':edb.DB.args.endpoint,
        'basis':snapshot['basis'],'source':edb.SOURCE,'sha256':digest,'transaction_file':str(path),
        'request_key':'finder-remaining-checkbox-v1-'+str(snapshot['basis'])+'-'+digest,'must_use_basis_guard':True})
    print(json.dumps({'prepared':True,'basis':snapshot['basis'],**counts}),flush=True)

def inspect_report(report, committed=False):
    plan = json.loads((OUT/'plan.json').read_text())
    snapshot = edb.loads((OUT/'snapshot.edn').read_text())
    assert report[':edb/committed'] is committed
    if not committed:
        assert report[':edb/speculative'] is True
    assert report[':edb/db-before-t'] == plan['basis'], 'Database advanced; refresh snapshot and dependencies'
    assert hashlib.sha256((OUT/'transaction.edn').read_bytes()).hexdigest() == plan['transaction_sha256']
    names = dict(snapshot['attributes'])
    source_id = snapshot['source'][0][0][':db/id']
    enums = {str(ident):eid for eid,ident in edb.read(
        '[:find ?e ?ident :in $ [?ident ...] :where [?e :db/ident ?ident]]',
        [[edb.kw('answer-field.type/checkbox'),edb.kw('answer.type/text')]],'preview-enums',plan['basis'])}
    tempids = report[':edb/tempids']
    assert len(set(tempids.values())) == plan['counts']['new_checkbox_fields'] + plan['counts']['new_boolean_answers']
    forms = edb.loads((OUT/'transaction.edn').read_text())
    additions, retractions = set(), set()
    def value(v):
        if isinstance(v,edb.kw('x').__class__): return enums[str(v)]
        if isinstance(v,str) and v in tempids: return tempids[v]
        return v
    for form in forms:
        if isinstance(form,dict):
            eid = value(form[':db/id'])
            for attribute,contents in form.items():
                if attribute in (':db/id',':db/ensure'): continue
                contents = contents if isinstance(contents,list) else [contents]
                additions.update((eid,str(attribute),value(v)) for v in contents)
        elif form[0] == ':db/cas':
            _,eid,attribute,old,new = form
            additions.add((eid,str(attribute),value(new)))
            if old is not None: retractions.add((eid,str(attribute),value(old)))
        elif form[0] == ':db/retract':
            _,eid,attribute,old = form
            retractions.add((eid,str(attribute),value(old)))
        else:
            assert form[0] == ':db/ensure'
    actual_additions, actual_retractions = set(), set()
    tx_instants = 0
    for eid,attribute,contents,tx,source,added in report[':edb/tx-data']:
        assert source == source_id
        name = str(names[attribute])
        if name == ':db/txInstant':
            assert added
            tx_instants += 1
            continue
        (actual_additions if added else actual_retractions).add((eid,name,contents))
    assert tx_instants == 1
    assert actual_additions == additions, 'Unexpected/missing assertions'
    assert actual_retractions == retractions, 'Unexpected/missing retractions'
    # Exact datom equality also rules out status/progress/XP changes, deletion of
    # original entities, and unexpected mutations caused by identity upserts.
    edb.save('commit-validation.json' if committed else 'preview.json',
        {'passed':True,'committed':committed,'speculative':not committed,'basis':plan['basis'],
        'basis_after':report[':edb/db-after-t'],
        'source':edb.SOURCE,'transaction_sha256':plan['transaction_sha256'],'counts':plan['counts'],
        'datoms':len(report[':edb/tx-data']),'assertions':len(additions),'retractions':len(retractions),
        'checks':['Application-native answer-field predicates and all entity specs passed.',
            'Every expanded assertion and retraction exactly matches the reviewed logical forms.',
            'Every datom has the existing agent as source.',
            'New UUID identities resolved to exactly 337 new fields and 674 new answers; no identity upserts onto original entities.',
            'No learner state, original answer content or unrelated entity changed. Only the five explicitly reviewed existing worked solutions are corrected.',
            'Durable commit confirmed.' if committed else 'Transaction is speculative only and has not been submitted.']})
    print(json.dumps({'commit_validation_passed' if committed else 'preview_passed':True,
        'basis':plan['basis'],'datoms':len(report[':edb/tx-data']),**plan['counts']}),flush=True)

def preview():
    helper = edb.preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),
        repo_root=edb.ROOT,preview_bin=None),threading.Event())
    result = subprocess.run([str(helper),'with','--database','math','--file',str(OUT/'transaction.edn'),
        '--source',edb.SOURCE],env=edb.DB.env,check=True,capture_output=True,text=True,timeout=120)
    (OUT/'preview.edn').write_text(result.stdout)
    inspect_report(edb.loads(result.stdout))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['build','preview'])
    globals()[parser.parse_args().action]()
