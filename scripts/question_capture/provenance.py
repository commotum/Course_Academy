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
    """Saved evidence needs human review; a notation repair cannot resolve it."""


def value_hash(value):
    return hashlib.sha256(dumps(value).encode()).hexdigest()


def field_value(field, attribute):
    if attribute == 'answer-field/type':
        return field[':answer-field/type'][':db/ident']
    if attribute == 'answer-field/correct':
        answer = field[':answer-field/correct']
        return [answer[':answer/type'][':db/ident'], answer[':answer/value']]
    raise ValueError(attribute)


def source_records(content, directory):
    """Recover authority from saved DOM/checkpoints, never from solver labels.

    Choice completeness must be recorded by the extractor, or demonstrated by
    the full legacy radio DOM. A successful grade confirms the submitted values
    only. An incorrect grade leaves solution-derived keys as interpretations.
    """
    from core import normalize
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
            grade = record.get('actual_result') or record.get('after', {}).get('result')
            submitted = raw.get('submitted_value')
            if grade == 'Correct' and submitted is not None and normalize(submitted, correct['type']) == normalize(correct['value'], correct['type']):
                category = 'ma_successful_grade'
            # Explicit source answers must be stored separately from solver
            # decisions. Currently the extractor does not expose such answers.
            explicit = raw.get('source_correct')
            if explicit == {'type': correct['type'], 'value': correct['value']}:
                category = 'ma_explicit_answer'
            add(mid, f['key'], 'answer-field/correct', [kw('answer.type/'+correct['type']), correct['value']], category, file)
    return result


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
        if kw(attr) in self.no_history:
            self.review(mid, key, attr, old, new, 'Installed db/noHistory would prevent retained attribute history')
            return False
        known = self.evidence(self.authored, mid, key, attr, old)
        local = [r for r in known if r['category'].startswith('local_')]
        source = [r for r in self.evidence(self.sources, mid, key, attr, new) if r['category'] in categories]
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

    def field_action(self, mid, previous, incoming, **context):
        """Version an unused field when owned components need replacement."""
        from core import compare_answers, matching_answer
        key = incoming['key']
        kind = previous[':answer-field/type'][':db/ident']
        new_kind = kw('answer-field.type/'+incoming['type'])
        c = next(c for c in incoming['choices'] if c['value'] == incoming['correct_value'])
        new_correct = [kw('answer.type/'+c['type']), c['value']]
        old_correct = field_value(previous, 'answer-field/correct')
        compared = compare_answers(old_correct[1], c['value'], c['type'], **context) if old_correct[0] == new_correct[0] else {'outcome':'different'}
        equivalent = compared['outcome'] == 'equivalent'
        changed = False
        allowed = True
        if kind != new_kind:
            changed = True
            allowed &= self.replace(mid, key, 'answer-field/type', kind, new_kind, {'ma_widget'})
        if not equivalent:
            changed = True
            allowed &= self.replace(mid, key, 'answer-field/correct', old_correct, new_correct,
                                    {'ma_explicit_answer', 'ma_successful_grade'})
            self.decisions[-1]['comparison'] = compared
        matched = {a[':db/id'] for choice in incoming['choices']
                   if (a := matching_answer(choice, previous[':answer-field/choices'], **context)) is not None}
        extras = [a for a in previous[':answer-field/choices'] if a[':db/id'] not in matched]
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
                if not local:
                    allowed = False
                    self.review(mid, key, 'answer/value', value, None, 'Complete choices omit a source or unknown value')
                else:
                    self.decisions.append(dict(question=mid, field=key, attribute='answer/value',
                        old_sha256=value_hash(value), new_sha256=value_hash(None), category=local[0]['category'],
                        authoring=local, source=complete, basis=self.basis,
                        reason='Authentic complete choice set supersedes local alternative', action='version'))
        if not changed:
            return 'merge'
        if not complete and incoming['type'] != 'blank':
            allowed = False
            self.review(mid, key, 'answer-field/choices', None, values, 'Incomplete source choice set cannot replace a field')
        if self.usage.get(mid) or mid not in self.usage:
            allowed = False
            self.review(mid, key, 'question/answer-fields', previous[':db/id'], None,
                        'Historical presentation/response exists or usage was not checked; preserve field and answer entities')
        if not allowed:
            return 'retain'
        self.decisions.append(dict(question=mid, field=key, attribute='question/answer-fields',
            old_sha256=value_hash(previous), new_sha256=value_hash(incoming), category='versioned_field',
            source=complete, basis=self.basis, reason='Detach unused field ownership; retain old field and answers', action='replace'))
        return 'version'
