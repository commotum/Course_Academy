"""Attribute-level reconciliation of saved MA captures and documented authoring.

Evidence is local and immutable input. This module never writes to EDB. An
authoring record is usable only with its saved transaction, verification basis,
and an exact readback of that value/identity at that basis.
"""
import hashlib
import json
import re
from pathlib import Path

from edn import dumps, kw, loads


class ReconciliationReview(ValueError):
    """Saved evidence needs source review by the persistent repair session."""


def value_hash(value):
    return hashlib.sha256(dumps(value).encode()).hexdigest()


def field_value(field, attribute):
    if attribute == 'answer-field/type':
        return field[':answer-field/type'][':db/ident']
    if attribute == 'answer-field/correct':
        answer = field[':answer-field/correct']
        return [answer[':answer/type'][':db/ident'], answer[':answer/value']]
    raise ValueError(attribute)


def source_records(content, directory, *, include_reviews=True):
    """Recover authority from saved DOM/checkpoints, never from solver labels.

    Choice completeness must be recorded by the extractor, or demonstrated by
    the full legacy radio DOM. A successful grade confirms the submitted values
    only. An incorrect grade leaves solution-derived keys as interpretations.
    """
    from core import compare_answers
    from answer_policy import source_answer
    directory = Path(directory)
    state_path = directory/'state.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    metadata_path = directory/'activity-metadata.json'
    metadata = json.loads(metadata_path.read_text()) if metadata_path.exists() else []
    metadata = {r['id'].replace('question-', 'q-'): r for r in metadata}
    result = []

    def add(mid, field, attr, value, category, file):
        result.append(dict(question=mid, field=field, attribute=attr, value=value,
                           category=category, file=str(file), file_sha256=hashlib.sha256(file.read_bytes()).hexdigest()))

    for q in content['questions'] + content.get('canonical_examples', []):
        mid = q['math_academy_id']
        record = state.get('questions', {}).get(mid, {})
        before = record.get('before', {})
        after = record.get('history') or record.get('after', {})
        canonical = mid in {e['math_academy_id'] for e in content.get('canonical_examples', [])}
        file = state_path
        if canonical:
            file = directory/('example-'+mid.split('-')[1]+'.json')
            before = after = json.loads(file.read_text()) if file.exists() else {}
        if not file.exists() or before.get('errors') or after.get('errors'):
            continue
        # Do not attribute multistep's locally composed context to MA.
        for attr, capture_key, item in [('question/problem', 'problem', before),
                                        ('question/worked-solution', 'worked_solution', after)]:
            if q.get(capture_key) and q[capture_key] == item.get(capture_key):
                add(mid, None, attr, q[capture_key], 'ma_capture', file)
        rating = {'E':'easy', 'M':'moderate', 'H':'hard'}.get(metadata.get(mid, {}).get('difficulty'))
        if rating and q.get('difficulty') == rating:
            add(mid, None, 'question/difficulty', kw('question.difficulty/'+rating), 'ma_capture', metadata_path)
        fields = {f['key']: f for f in before.get('fields', [])}
        verification = record.get('verification', {})
        verified_source = source_answer(verification, {'problem':before.get('problem', ''),
            'fields':before.get('fields', []), 'worked_solution':record.get('after', {}).get('worked_solution', '')})
        for f in q.get('answer_fields', []):
            raw = fields.get(f['key'])
            if not raw or raw['type'] != f['type']:
                continue
            add(mid, f['key'], 'answer-field/type', kw('answer-field.type/'+f['type']), 'ma_widget', file)
            captured = sorted((c['type'], c['value']) for c in raw.get('choices', []))
            incoming = sorted((c['type'], c['value']) for c in f['choices'])
            legacy_count = len(re.findall(r'class="[^"\n]*\b(?:questionWidget-choiceText|choiceText)\b', before.get('html', '')))
            complete = raw.get('choices_complete') is True or (
                'choices_complete' not in raw and f['type'] == 'radio' and legacy_count == len(captured) > 0)
            if complete and f['type'] in ('radio', 'select') and captured == incoming:
                add(mid, f['key'], 'answer-field/choices', incoming, 'ma_complete_choices', file)
            correct = next((c for c in f['choices'] if c['value'] == f.get('correct_value')), None)
            if correct is None:
                continue  # Normal validation will reject incomplete input.
            category = 'model_interpretation'
            verified = next((a for a in verification.get('answers', []) if a['key'] == f['key']), None)
            if (verified_source and verified and verified['correct_value'] == correct['value']
                    and verified['value_type'] == correct['type']):
                category = 'reviewed_ma_solution'
                # Preserve original options and add only a source-solution answer.
                expected = sorted(set(captured + [(correct['type'], correct['value'])]))
                if f['type'] in ('radio', 'select') and sorted(set(incoming)) == expected:
                    add(mid, f['key'], 'answer-field/choices', incoming, 'reviewed_ma_choices', file)
            grade = record.get('actual_result') or record.get('after', {}).get('result')
            submitted = raw.get('submitted_value')
            if grade == 'Correct' and submitted is not None and compare_answers(submitted, correct['value'], correct['type'],prompt=q.get('problem',''))['outcome'] == 'equivalent':
                category = 'ma_successful_grade'
            # Explicit source answers must be stored separately from solver
            # decisions. Currently the extractor does not expose such answers.
            explicit = raw.get('source_correct')
            if explicit == {'type': correct['type'], 'value': correct['value']}:
                category = 'ma_explicit_answer'
            add(mid, f['key'], 'answer-field/correct', [kw('answer.type/'+correct['type']), correct['value']], category, file)
    if include_reviews:
        path=directory/'answer-source-reviews.json'
        if path.exists():
            for review in json.loads(path.read_text()).get('reviews',[]):
                try:
                    field,correct,bindings,files=answer_review_context(content,directory,review,result)
                    if bindings!=review.get('bindings') or files!=review.get('evidence_files'):
                        continue
                    incoming=next(f for q in content['questions']+content.get('canonical_examples',[]) if q['math_academy_id']==review['question']
                                  for f in q['answer_fields'] if f['key']==review['field'])
                    if value_hash(incoming)!=value_hash(field):continue
                    proof=Path(review['review_result'])
                    if not proof.is_file() or hashlib.sha256(proof.read_bytes()).hexdigest()!=review['review_result_sha256']:
                        continue
                    result.append(dict(question=review['question'],field=review['field'],attribute='answer-field/correct',
                        value=[kw('answer.type/'+correct['type']),correct['value']],category='reviewed_ma_solution',
                        file=str(path),file_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                        reviewer_session=review['reviewer_session'],rationale=review['rationale'],
                        bindings=bindings,evidence_files=files))
                    if field['type'] in ('radio','select'):
                        result.append(dict(question=review['question'],field=review['field'],attribute='answer-field/choices',
                            value=sorted((c['type'],c['value']) for c in field['choices']),category='reviewed_ma_choices',
                            file=str(path),file_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),rationale=review['rationale']))
                except (KeyError,ValueError,TypeError,OSError):
                    continue
    if include_reviews:
        result.extend(field_layout_review_records(content, directory, result))
    return result


def question_layout(question):
    """Bind widget roles to the original prompt and immutable component IDs."""
    return {"question_id":question[":question/id"], "problem":question[":question/problem"],
            "fields":sorted(question.get(":question/answer-fields", []), key=lambda f:str(f[":db/id"]))}


def field_layout_review_records(content, directory, sources):
    """Accept only an explicit review of an unchanged, complete blank layout.

    A key can change mathematical role even when its spelling is unchanged.
    These reviews replace the entire ownership set; no previous blank values
    are carried into a new role. Raw source captures remain untouched.
    """
    directory=Path(directory).resolve();path=directory/"field-layout-source-reviews.json"
    if not path.exists():return []
    result=[]
    for review in json.loads(path.read_text()).get("reviews", []):
        try:
            if review.get("confident") is not True or not review.get("rationale", "").strip():continue
            q=next(q for q in content["questions"] if q["math_academy_id"]==review["question"])
            fields=q["answer_fields"]
            state=json.loads((directory/"state.json").read_text())
            record=state["questions"][review["question"]];before=record["before"]
            raw=before["fields"]
            if (before.get("errors") or not fields or any(f["type"]!="blank" for f in fields)
                    or [(f["key"],f["type"]) for f in fields]!=[(f["key"],f["type"]) for f in raw]):continue
            # Count all observed blank wrappers, not merely extractor records.
            ids=re.findall(r'\bid="(freeResponseTextbox-[^"]+)"', before["html"])
            if len(ids)!=len(raw) or set(ids)!={f["dom_id"] for f in raw}:continue
            if any(q["problem"].count("{{"+f["key"]+"}}")!=1 for f in fields):continue
            bindings={"problem":value_hash(q["problem"]), "worked_solution":value_hash(q["worked_solution"]),
                      "fields":value_hash(fields), "raw_before":value_hash(before)}
            if bindings!=review.get("bindings"):continue
            if not all(any(r["question"]==review["question"] and r["attribute"]==attr
                and r["category"]=="ma_capture" and value_hash(r["value"])==bindings[key]
                for r in sources) for attr,key in (("question/problem","problem"),("question/worked-solution","worked_solution"))):continue
            if not all(any(r["question"]==review["question"] and r["field"]==f["key"]
                and r["attribute"]=="answer-field/correct" and r["category"] in
                ("ma_successful_grade","ma_explicit_answer","reviewed_ma_solution") for r in sources) for f in fields):continue
            files=review["evidence_files"]
            if not files:continue
            valid=True
            for evidence in files:
                file=(directory/evidence["path"]).resolve()
                if (not file.is_relative_to(directory) or not file.is_file()
                        or hashlib.sha256(file.read_bytes()).hexdigest()!=evidence["sha256"]):valid=False;break
            if not valid:continue
            proof=review["previous_readback"]
            if not any(f["path"]==proof for f in files):continue
            previous=next(row[0] for row in loads((directory/proof).read_text())
                          if row[0][":question/math-academy-id"]==review["question"])
            previous_hash=value_hash(question_layout(previous))
            if previous_hash!=review.get("previous_layout_sha256"):continue
            result.append(dict(question=review["question"],field=None,attribute="question/answer-fields",
                value=fields, category="reviewed_ma_field_layout", previous_layout_sha256=previous_hash,
                file=str(path),file_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                bindings=bindings,evidence_files=files,rationale=review["rationale"]))
        except (KeyError,ValueError,TypeError,OSError,StopIteration):continue
    return result


def field_layout_retry_evidence(directory):
    """Fingerprint usable layout authority without review timestamps or paths."""
    directory=Path(directory)
    if not (directory/'field-layout-source-reviews.json').is_file():return []
    try:
        content=json.loads((directory/'content.json').read_text())
        records=source_records(content,directory)
        scopes={json.dumps({key:r[key] for key in ('question','previous_layout_sha256','bindings')},sort_keys=True)
                for r in records if r['category']=='reviewed_ma_field_layout'}
        return sorted(scopes)
    except (KeyError,ValueError,TypeError,OSError):
        return []


def answer_review_context(content,directory,review,sources):
    """Bind derived math judgment to the unchanged original question and solution."""
    import copy
    directory=Path(directory).resolve()
    if review.get('confident') is not True or not review.get('rationale','').strip():
        raise ValueError('Answer review needs a confident source-based explanation')
    question=next((q for q in content['questions']+content.get('canonical_examples',[]) if q['math_academy_id']==review['question']),None)
    if question is None:raise ValueError('Answer review names an uncaptured question')
    current=next((f for f in question.get('answer_fields',[]) if f['key']==review['field']),None)
    if current is None:raise ValueError('Answer review names an uncaptured field')
    original=review.get('original_answer_field',current)
    if original['key']!=current['key'] or original['type']!=current['type']:
        raise ValueError('Answer review cannot change a field identity or type')
    matching=lambda attr,value: any(r['question']==review['question'] and r['field']==None
        and r['attribute']==attr and value_hash(r['value'])==value_hash(value) and r['category']=='ma_capture' for r in sources)
    if (not question.get('worked_solution') or not matching('question/problem',question['problem']) or
            not matching('question/worked-solution',question['worked_solution'])):
        raise ValueError('Answer review needs the authentic problem and worked solution')
    state_path=directory/'state.json';state=json.loads(state_path.read_text()) if state_path.exists() else {}
    record=state.get('questions',{}).get(review['question'],{})
    before=record.get('before',{})
    if review['question'].startswith('e-'):
        path=directory/('example-'+review['question'].split('-')[1]+'.json')
        before=json.loads(path.read_text()) if path.exists() else {}
    raw=next((f for f in before.get('fields',[]) if f['key']==review['field']),{})
    if raw.get('type')!=original['type']:raise ValueError('Answer review needs the captured matching widget')
    choice_field=original['type'] in ('radio','select')
    if choice_field:
        pairs=lambda choices: sorted((c['type'],c['value']) for c in choices)
        complete=raw.get('choices_complete') is True or ('choices_complete' not in raw and original['type']=='radio'
            and len(re.findall(r'class="[^"\n]*\b(?:questionWidget-choiceText|choiceText)\b',before.get('html','')))==len(raw.get('choices',[]))>0)
        if not complete or pairs(raw.get('choices',[]))!=pairs(original['choices']):
            raise ValueError('Answer review needs the complete original choice set')
    field=copy.deepcopy(original)
    for correction in review.get('choice_corrections',[]):
        index=correction['option_index']
        if not choice_field or not isinstance(index,int) or not 0<=index<len(field['choices']):
            raise ValueError('Choice correction needs an original option index')
        if correction['value_type']!=field['choices'][index]['type']:
            raise ValueError('Choice correction cannot change an answer type')
        field['choices'][index]['value']=correction['value']
    correct={'type':review['value_type'],'value':review['correct_value']}
    if choice_field:
        index=review['option_index']
        if not isinstance(index,int) or not 0<=index<len(field['choices']) or field['choices'][index]!=correct:
            # Captures can carry option feedback as well as type/value.
            if not isinstance(index,int) or not 0<=index<len(field['choices']) or any(field['choices'][index].get(k)!=v for k,v in correct.items()):
                raise ValueError('Reviewed answer must identify its original observed option; '
                                 'expected '+repr(field['choices'][index] if isinstance(index,int) and 0<=index<len(field['choices']) else 'valid option index')+'; received '+repr(correct))
        grade=record.get('actual_result') or record.get('after',{}).get('result')
        submitted=raw.get('submitted_option') or raw.get('observed_selected_option')
        observed=[i for i,c in enumerate(raw['choices']) if c.get('option')==submitted] if submitted else []
        if observed and (grade=='Correct' and index!=observed[0] or grade=='Incorrect' and index==observed[0]):
            raise ValueError('Answer review contradicts the observed choice grade')
        explicit=raw.get('source_correct')
        original_choice=original['choices'][index]
        if explicit and explicit!={k:original_choice[k] for k in ('type','value')}:
            raise ValueError('Answer review contradicts the directly observed answer option')
    elif original['type']=='blank':
        if review.get('choice_corrections'):raise ValueError('Blank answer review has no original choice indices')
        explicit=raw.get('source_correct')
        if explicit:
            from core import compare_answers
            outcome=compare_answers(explicit['value'],correct['value'],correct['type'],prompt=question['problem'])['outcome']
            if explicit['type']!=correct['type'] or outcome=='different':
                raise ValueError('Answer review contradicts the directly observed answer key')
        field['choices']=[correct]
    else:raise ValueError('Answer source review supports blank, radio and select fields')
    field['correct_value']=correct['value'];field['correct_origin']='reviewed_ma_solution'
    files=[]
    for item in review.get('evidence_files',[]):
        name=item['path'] if isinstance(item,dict) else item
        path=(directory/name).resolve()
        if not path.is_relative_to(directory) or not path.is_file():raise ValueError('Answer review evidence must be a saved activity file')
        # Identity comes from the bound original widget/problem/solution, not
        # a filename. Shared activity evidence can be cited by the reviewer.
        if path==directory/'state.json':
            saved=json.loads(path.read_text());record=saved.get('questions',{}).get(review['question'],{})
            evidence={'question':review['question'],
                      'raw':{key:record.get(key) for key in ('before','after','history','actual_result')},
                      'shared_contexts':saved.get('shared_contexts',[])}
            digest=hashlib.sha256(json.dumps(evidence,sort_keys=True).encode()).hexdigest()
            files.append({'path':'state.json','sha256':digest,'scope':'question_raw_state'})
        else:
            files.append({'path':str(path.relative_to(directory)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    if not files:raise ValueError('Answer review needs original question/solution evidence')
    bindings={'problem':value_hash(question['problem']),'worked_solution':value_hash(question['worked_solution']),
              'original_field':value_hash(original),'reviewed_field':value_hash(field),
              'raw_widget':value_hash(raw)}
    return field,correct,bindings,files


def save_answer_reviews(content,directory,reviews,session_id,result_path):
    """Freeze completed reviewer judgments and update only derived content."""
    import copy
    from core import atomic_json
    directory=Path(directory)
    if (directory/'edb-import/commit-intent.json').exists():raise ValueError('Pending commit intent cannot accept new answer reviews')
    result_path=Path(result_path);sources=source_records(content,directory,include_reviews=False)
    frozen=[];updated=copy.deepcopy(content)
    for review in reviews:
        question=next(q for q in content['questions']+content.get('canonical_examples',[]) if q['math_academy_id']==review['question'])
        original=next(f for f in question['answer_fields'] if f['key']==review['field'])
        review={**review,'original_answer_field':copy.deepcopy(original)}
        field,_,bindings,files=answer_review_context(content,directory,review,sources)
        frozen.append({**review,'bindings':bindings,'evidence_files':files,'reviewer_session':session_id,
                       'review_result':str(result_path),'review_result_sha256':hashlib.sha256(result_path.read_bytes()).hexdigest()})
        q=next(q for q in updated['questions']+updated.get('canonical_examples',[]) if q['math_academy_id']==review['question'])
        q['answer_fields']=[field if f['key']==review['field'] else f for f in q['answer_fields']]
    original_hash=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
    archive=directory/('content-before-source-review-'+original_hash[:12]+'.json')
    if not archive.exists():atomic_json(archive,content)
    state_path=directory/'state.json'
    if state_path.exists():
        state=json.loads(state_path.read_text());old_state=copy.deepcopy(state)
        for question in updated['questions']:
            record=state.get('questions',{}).get(question['math_academy_id'],{})
            if 'content' in record:record['content']=question
        examples={q['math_academy_id']:q for q in updated.get('canonical_examples',[])}
        for key,example in state.get('examples',{}).items():
            if example['math_academy_id'] in examples:state['examples'][key]=examples[example['math_academy_id']]
        if state!=old_state:
            state_archive=directory/('state-before-source-review-'+original_hash[:12]+'.json')
            if not state_archive.exists():atomic_json(state_archive,old_state)
            atomic_json(state_path,state)
    path=directory/'answer-source-reviews.json';existing=json.loads(path.read_text()).get('reviews',[]) if path.exists() else []
    keys={(r['question'],r['field']) for r in frozen}
    atomic_json(path,{'reviews':[r for r in existing if (r['question'],r['field']) not in keys]+frozen})
    atomic_json(directory/'content.json',updated)
    return len(frozen)


def mathematical_correction_records(root, ids):
    """Load reviewed corrections backed by a committed, verified transaction.

    Database.reconciliation also attests every value and field identity against
    the immutable readback at the correction's basis before using these records.
    Original MA captures remain separate evidence of what the site displayed.
    """
    records = []
    for source in sorted((Path(root)/'mathematical-corrections').glob('*/review.json')):
        try:
            review = json.loads(source.read_text())
            q = review['corrected_content']
            if q['math_academy_id'] not in ids:
                continue
            tx, verification = source.parent/'transaction.edn', source.parent/'verification.json'
            proof = json.loads(verification.read_text())
            if (proof.get('committed') is not True or proof.get('mathematical_check_passed') is not True
                    or not isinstance(proof.get('basis_after'), int)
                    or proof.get('review_sha256') != hashlib.sha256(source.read_bytes()).hexdigest()
                    or proof.get('transaction_sha256') != hashlib.sha256(tx.read_bytes()).hexdigest()):
                continue
            values = [(None, 'question/problem', q['problem']),
                      (None, 'question/worked-solution', q['worked_solution'])]
            for f in q['answer_fields']:
                c = next(c for c in f['choices'] if c['value'] == f['correct_value'])
                values.append((f['key'], 'answer-field/correct', [kw('answer.type/'+c['type']), c['value']]))
            for field, attr, value in values:
                records.append(dict(question=q['math_academy_id'], field=field, attribute=attr, value=value,
                    category='mathematical_correction', file=str(source), file_sha256=proof['review_sha256'],
                    transaction=str(tx), transaction_sha256=proof['transaction_sha256'],
                    verification=str(verification), basis=proof['basis_after'], rationale=review['rationale']))
        except (KeyError, ValueError, TypeError, OSError, StopIteration):
            continue
    return records


def authoring_records(root, ids):
    """Read the two documented authoring batches; no age-based classification."""
    root = Path(root)
    records = []

    def add(q, field, attr, value, category, source, tx, verification):
        if q['math_academy_id'] not in ids or not tx.exists() or not verification.exists():
            return
        proof = json.loads(verification.read_text())
        basis = proof.get('basis_after')
        if not isinstance(basis, int) or proof.get('learner_and_engine_facts_unchanged') is not True:
            return
        # Transaction assertions bind the authorship declaration to the imported
        # value. EDB readbacks later bind it to the actual question/component.
        if dumps(value) not in tx.read_text() and attr not in ('answer-field/correct', 'answer-field/choices', 'answer/value'):
            return
        records.append(dict(question=q['math_academy_id'], field=field, attribute=attr, value=value,
            category=category, file=str(source), file_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            transaction=str(tx), transaction_sha256=hashlib.sha256(tx.read_bytes()).hexdigest(),
            verification=str(verification), basis=basis))

    factorials = root/'factorials-13831129'
    source = factorials/'authored-worked-solutions.json'
    if source.exists():
        for q in json.loads(source.read_text())['questions']:
            add(q, None, 'question/worked-solution', q['worked_solution'], 'local_authored', source,
                factorials/'worked-solutions-transaction.edn', factorials/'worked-solutions-verification.json')
    source = factorials/'completion-review.json'
    if source.exists():
        for q in json.loads(source.read_text()):
            if q.get('difficulty_provenance') == 'authored estimate, not an observed Math Academy rating':
                add(q, None, 'question/difficulty', kw('question.difficulty/'+q['difficulty']), 'local_estimate', source,
                    factorials/'completion-transaction.edn', factorials/'completion-verification.json')
    # Factorials transactions contain the field-scoped identities and exact
    # typed choices. Exclude any values explicitly observed in source content.
    source = factorials/'review.json'
    if source.exists():
        captured = json.loads((factorials/'content.json').read_text())['questions']
        observed = {q['math_academy_id']: set(q.get('source_choices', []) + [q.get('observed_answer_value')]) for q in captured}
        forms = loads((factorials/'transaction.edn').read_text())
        for q in json.loads(source.read_text()):
            if not q.get('choices_basis', '').startswith('authored distractors'):
                continue
            form = next((m for m in forms if m.get(':question/math-academy-id') == q['math_academy_id']), {})
            for f in form.get(':question/answer-fields', []):
                key = f[':answer-field/key']
                add(q, key, 'answer-field/type', f[':answer-field/type'], 'local_authored', source,
                    factorials/'transaction.edn', factorials/'verification.json')
                for a in f[':answer-field/choices']:
                    if a[':answer/value'] != q['correct_answer'] and a[':answer/value'] not in observed.get(q['math_academy_id'], set()):
                        add(q, key, 'answer/value', [a[':answer/type'], a[':answer/value']], 'local_authored', source,
                            factorials/'transaction.edn', factorials/'verification.json')
    history = root/'history-question-import-2026-10-04'
    for source, tx, verification, repaired in [
        (history/'import-ready/questions.json', history/'import-ready/database-import/transaction.edn', history/'import-ready/database-import/verification.json', False),
        (history/'format-audit/repairs.json', history/'format-audit/database-repair/transaction.edn', history/'format-audit/database-repair/verification.json', True)]:
        if not source.exists():
            continue
        for entry in json.loads(source.read_text())['questions']:
            q = entry['after'] if repaired else entry
            if q['math_academy_id'] not in ids:
                continue
            prep = q.get('preparation', {})
            if prep.get('source_problem') and prep['source_problem'] != q['problem']:
                add(q, None, 'question/problem', q['problem'], 'local_reconstruction', source, tx, verification)
            for f in q['answer_fields']:
                key = f['key']
                response = prep.get('response_repair', {})
                local = response.get('options_recovered_from_original_question') is False or (
                    not repaired and prep.get('answer_origin') == 'entered-math')
                if local:
                    add(q, key, 'answer-field/type', kw('answer-field.type/'+f['type']), 'local_reconstruction', source, tx, verification)
                correction = response.get('correct_answer_correction')
                if correction and correction.get('correct') == f['correct_value']:
                    c = next(c for c in f['choices'] if c['value'] == f['correct_value'])
                    add(q, key, 'answer-field/correct', [kw('answer.type/'+c['type']), c['value']], 'ma_explicit_answer', source, tx, verification)
                elif not prep.get('has_explicit_answer_review') and local:
                    c = next(c for c in f['choices'] if c['value'] == f['correct_value'])
                    add(q, key, 'answer-field/correct', [kw('answer.type/'+c['type']), c['value']], 'local_interpretation', source, tx, verification)
                for c in f['choices']:
                    if local and c['value'] != f['correct_value']:
                        add(q, key, 'answer/value', [kw('answer.type/'+c['type']), c['value']], 'local_authored', source, tx, verification)
    records.extend(mathematical_correction_records(root, ids))
    return records


class Reconciler:
    def __init__(self, authored=(), sources=(), basis=None, usage=None, no_history=()):
        self.authored, self.sources = list(authored), list(sources)
        self.basis, self.usage = basis, usage or {}
        self.no_history = set(no_history)
        self.decisions = []

    def evidence(self, records, mid, key, attr, value):
        return [r for r in records if r['question'] == mid and r['field'] == key and
                r['attribute'] == attr and value_hash(r['value']) == value_hash(value)]

    def review(self, mid, key, attr, old, new, reason):
        self.decisions.append(dict(question=mid, field=key, attribute=attr, old_sha256=value_hash(old),
            new_sha256=value_hash(new), category='review_required', basis=self.basis, reason=reason))

    def replace(self, mid, key, attr, old, new, categories):
        if value_hash(old) == value_hash(new):
            return False
        corrections = [r for r in self.evidence(self.authored, mid, key, attr, old)
                       if r['category'] == 'mathematical_correction']
        if corrections:
            self.decisions.append(dict(question=mid, field=key, attribute=attr,
                old_sha256=value_hash(old), new_sha256=value_hash(new), category='mathematical_correction',
                authoring=corrections, basis=self.basis, action='retain',
                reason='Retain the verified mathematical correction instead of reimporting the source error'))
            return False
        if kw(attr) in self.no_history:
            self.review(mid, key, attr, old, new, 'Installed db/noHistory would prevent retained attribute history')
            return False
        known = self.evidence(self.authored, mid, key, attr, old)
        local = [r for r in known if r['category'].startswith('local_')]
        source = [r for r in self.evidence(self.sources, mid, key, attr, new) if r['category'] in categories]
        if attr in ('question/problem','question/worked-solution','question/difficulty') and source:
            # Current observed MA content is sufficient authority for these
            # attributes. Old authorship does not veto a real source capture.
            self.decisions.append(dict(question=mid, field=key, attribute=attr,
                old_sha256=value_hash(old), new_sha256=value_hash(new), category='ma_capture',
                authoring=known, source=source, basis=self.basis,
                reason='Observed MA content supersedes the stored value', action='replace'))
            return True
        reviewed=[r for r in source if r['category']=='reviewed_ma_solution']
        if attr=='answer-field/correct' and reviewed:
            self.decisions.append(dict(question=mid,field=key,attribute=attr,
                old_sha256=value_hash(old),new_sha256=value_hash(new),category='reviewed_ma_solution',
                authoring=known,source=reviewed,basis=self.basis,
                reason='Persistent repair judgment from authentic worked solution and original choices supersedes stored key',action='replace'))
            return True
        if any(r['category'].startswith('ma_') for r in known):
            self.review(mid, key, attr, old, new, 'Contradiction between authoritative MA sources')
            return False
        if not local or not source:
            self.review(mid, key, attr, old, new, 'Unknown current provenance or missing authoritative replacement')
            return False
        self.decisions.append(dict(question=mid, field=key, attribute=attr,
            old_sha256=value_hash(old), new_sha256=value_hash(new), category=local[0]['category'],
            authoring=local, source=source, basis=self.basis, reason='MA evidence supersedes exact documented local value', action='replace'))
        return True

    @property
    def needs_review(self):
        return any(d['category'] == 'review_required' for d in self.decisions)

    def field_layout_action(self, mid, previous, incoming):
        """Authorize an exact reviewed layout, never a key-only role match."""
        fields=incoming.get('answer_fields', [])
        source=[r for r in self.evidence(self.sources,mid,None,'question/answer-fields',fields)
                if r['category']=='reviewed_ma_field_layout'
                and r.get('previous_layout_sha256')==value_hash(question_layout(previous))]
        if not source:return False
        if (mid not in self.usage or self.usage[mid] or self.no_history or
                any(r['question']==mid and r['category']=='mathematical_correction' for r in self.authored)):
            self.review(mid,None,'question/answer-fields',question_layout(previous),fields,
                        'Reviewed layout needs checked unused history and retained component relationships')
            return False
        for field in previous.get(':question/answer-fields', []):
            self.decisions.append(dict(question=mid,field=field[':answer-field/key'],
                attribute='question/answer-fields',previous_field_id=field[':db/id'],
                old_sha256=value_hash(field),new_sha256=value_hash(fields),category='reviewed_ma_field_layout',
                source=source,basis=self.basis,historical_usage=self.usage[mid],action='replace',
                reason='Reviewed source layout changes blank roles; retain original fields and answers'))
        return True

    def single_answer_widget_action(self, mid, previous, incoming, **context):
        """Version a legacy answer blank only when its source problem is identical.

        The trailing authored placeholder is presentation, not a missing part.
        Require independent source evidence for the prompt, widget, full option
        set and correct key; neither a solver label nor equal answers alone
        establishes that the two response roles are the same.
        """
        from core import compare_answers
        old_fields = previous.get(':question/answer-fields', [])
        fields = incoming.get('answer_fields', [])
        if len(old_fields) != 1 or len(fields) != 1:
            return False
        old, field = old_fields[0], fields[0]
        if (old[':answer-field/type'][':db/ident'] != ':answer-field.type/blank' or
                field['type'] != 'radio' or field['key'] != 'selection'):
            return False
        problem = previous.get(':question/problem', '')
        footer = r'\n\nAnswer: \{\{' + re.escape(old[':answer-field/key']) + r'\}\}\s*\Z'
        stem, removed = re.subn(footer, '', problem)
        if (removed != 1 or stem != incoming.get('problem') or
                '{{' in stem or '}}' in stem):
            return False
        if (mid not in self.usage or self.usage[mid] or self.no_history or
                any(r['question'] == mid and r['category'] == 'mathematical_correction'
                    for r in self.authored)):
            return False
        correct = old.get(':answer-field/correct')
        choices = [c for c in field['choices'] if c['value'] == field.get('correct_value')]
        if not correct or len(choices) != 1:
            return False
        choice = choices[0]
        value = [kw('answer.type/' + choice['type']), choice['value']]
        if (correct[':answer/type'][':db/ident'] != value[0] or
                compare_answers(correct[':answer/value'], choice['value'], choice['type'],
                                **{**context, 'prompt':stem})['outcome'] != 'equivalent'):
            return False
        requirements = [
            (None, 'question/problem', stem, {'ma_capture'}),
            (field['key'], 'answer-field/type', kw('answer-field.type/radio'), {'ma_widget'}),
            (field['key'], 'answer-field/choices',
             sorted((c['type'], c['value']) for c in field['choices']), {'ma_complete_choices'}),
            (field['key'], 'answer-field/correct', value,
             {'ma_successful_grade', 'ma_explicit_answer'}),
        ]
        source = []
        for key, attr, observed, categories in requirements:
            records = [r for r in self.evidence(self.sources, mid, key, attr, observed)
                       if r['category'] in categories]
            if not records:
                return False
            source.extend(records)
        self.decisions.append(dict(question=mid, field=old[':answer-field/key'],
            attribute='question/answer-fields', previous_field_id=old[':db/id'],
            old_sha256=value_hash(old), new_sha256=value_hash(fields),
            category='ma_single_answer_widget', source=source, basis=self.basis,
            previous_problem_sha256=value_hash(problem), source_problem_sha256=value_hash(stem),
            historical_usage=self.usage[mid], action='replace',
            reason='Identical source problem and equivalent verified single answer; retain original blank and answers'))
        return True

    def field_action(self, mid, previous, incoming, **context):
        """Version field ownership while retaining original fields and answers."""
        from core import compare_answers, matching_answer
        key = incoming['key']
        kind = previous[':answer-field/type'][':db/ident']
        new_kind = kw('answer-field.type/'+incoming['type'])
        c = next(c for c in incoming['choices'] if c['value'] == incoming['correct_value'])
        new_correct = [kw('answer.type/'+c['type']), c['value']]
        old_correct = field_value(previous, 'answer-field/correct') if previous.get(':answer-field/correct') else None
        if (kind == new_kind and previous[':answer-field/key'] == key and old_correct is not None
                and value_hash(old_correct) != value_hash(new_correct)
                and any(r['category'] == 'mathematical_correction' for r in
                        self.evidence(self.authored, mid, key, 'answer-field/correct', old_correct))):
            self.replace(mid, key, 'answer-field/correct', old_correct, new_correct, set())
            return 'retain'
        compared = compare_answers(old_correct[1], c['value'], c['type'], **context) if old_correct and old_correct[0] == new_correct[0] else {'outcome':'different'}
        equivalent = compared['outcome'] == 'equivalent'
        changed = previous[':answer-field/key'] != key
        allowed = True
        if changed and not self.evidence(self.sources,mid,key,'answer-field/type',new_kind):
            allowed = False
            self.review(mid,key,'answer-field/key',previous[':answer-field/key'],key,'Field rename needs an observed matching widget')
        if kind != new_kind:
            changed = True
            allowed &= self.replace(mid, key, 'answer-field/type', kind, new_kind, {'ma_widget'})
        if old_correct is not None and not equivalent:
            changed = True
            allowed &= self.replace(mid, key, 'answer-field/correct', old_correct, new_correct,
                                    {'ma_explicit_answer', 'ma_successful_grade','reviewed_ma_solution'})
            self.decisions[-1]['comparison'] = compared
        # Historical fields can lack both choices and a correct answer. Let
        # the normal merge path fill those gaps without inventing a conflict.
        previous_choices = previous.get(':answer-field/choices', [])
        matched = {a[':db/id'] for choice in incoming['choices']
                   if (a := matching_answer(choice, previous_choices, **context)) is not None}
        extras = [a for a in previous_choices if a[':db/id'] not in matched]
        values = sorted((a['type'], a['value']) for a in incoming['choices'])
        complete = self.evidence(self.sources, mid, key, 'answer-field/choices', values)
        if extras and incoming['type'] != 'blank' and complete:
            changed = True
            for a in extras:
                value = [a[':answer/type'][':db/ident'], a[':answer/value']]
                known = self.evidence(self.authored, mid, key, 'answer/value', value)
                local = [r for r in known if r['category'].startswith('local_')]
                if any(r['category'].startswith('ma_') for r in known):
                    local = []
                # A removed correct key needs the independent strong-answer
                # replacement decision above; it is not an invented distractor.
                if not local and value == old_correct and not equivalent:
                    local = self.evidence(self.authored, mid, key, 'answer-field/correct', value)
                # A complete observed option set is enough to replace old
                # distractors. The correct key is checked independently above.
                self.decisions.append(dict(question=mid, field=key, attribute='answer/value',
                    old_sha256=value_hash(value), new_sha256=value_hash(None), category='ma_complete_choices',
                    authoring=local, source=complete, basis=self.basis,
                    reason='Observed complete choice set supersedes old alternatives', action='version'))
        if not changed:
            return 'merge'
        if not complete and incoming['type'] != 'blank':
            allowed = False
            self.review(mid, key, 'answer-field/choices', None, values, 'Incomplete source choice set cannot replace a field')
        if mid not in self.usage:
            allowed = False
            self.review(mid, key, 'question/answer-fields', previous[':db/id'], None,
                        'Usage was not checked; preserve field and answer entities')
        if not allowed:
            return 'retain'
        self.decisions.append(dict(question=mid, field=key, attribute='question/answer-fields',
            old_sha256=value_hash(previous), new_sha256=value_hash(incoming), category='versioned_field',
            previous_field_id=previous[':db/id'],source=complete, basis=self.basis,
            historical_usage=self.usage.get(mid,[]),
            reason='Attach source field; retain original field and answers for historical references', action='replace'))
        return 'version'
