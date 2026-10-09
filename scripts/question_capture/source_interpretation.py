"""One attested source interpretation for a containing-region construction."""
import hashlib
import json
import re
from pathlib import Path
from core import ROOT

TOPIC = 2616
KP = '624215ff-efdc-5b12-8d61-9d66371672d9'
POLICY = 'zero-extension-containing-rectangle-v1'
REQUEST = 'which of the following could be the definition of the rectangular domain $R?$'
CLARIFIED_REQUEST = ('Require $D\\subseteq R$, so the rectangle contains the entire region. '
                     'Which of the following could be the definition of the rectangular domain $R?$')


def reviewed_containment(item, activity, directory):
    """Return a local, hash-bound clarification; missing evidence is ordinary solving."""
    mid = Path(directory).name
    kp = activity.get('questions', {}).get(mid, {}).get('kp_id') or activity.get('current_kp')
    problem = item.get('problem', '')
    fields = item.get('fields', [])
    if (activity.get('topic_id') != TOPIC or kp != KP or REQUEST not in problem
            or 'R\\cap D' not in problem
            or not any(s in problem for s in ('R∖D', r'R\setminus D', r'R\setminusD'))
            or len(fields) != 1 or fields[0].get('type') != 'radio'
            or not fields[0].get('choices') or '0,' not in problem
            or not any(s in problem for s in ('∬', r'\iint'))):
        return None
    correction = ROOT/'reference/mathacademy/mathematical-corrections/e-6996'
    review_path, transaction = correction/'review.json', correction/'transaction.edn'
    try:
        review_bytes, transaction_bytes = review_path.read_bytes(), transaction.read_bytes()
        proof = json.loads((correction/'verification.json').read_text())
        review = json.loads(review_bytes)
        canonical = review['original_content']
        if (proof.get('committed') is not True or proof.get('mathematical_check_passed') is not True
                or not isinstance(proof.get('basis_after'), int)
                or proof.get('review_sha256') != hashlib.sha256(review_bytes).hexdigest()
                or proof.get('transaction_sha256') != hashlib.sha256(transaction_bytes).hexdigest()
                or canonical.get('math_academy_id') != 'e-6996'
                or canonical.get('knowledge_point_id') != KP
                or 'if $R$ covers $D$ completely' not in canonical.get('worked_solution', '')
                or r'D\subseteq R' not in review['corrected_content']['problem']):
            return None
    except (OSError, ValueError, KeyError, TypeError):
        return None
    interpreted = problem.replace(REQUEST, CLARIFIED_REQUEST)
    identity = [POLICY, proof['review_sha256'], hashlib.sha256(problem.encode()).hexdigest()]
    return {'policy': POLICY, 'topic_id': TOPIC, 'knowledge_point_id': KP,
        'source_problem': problem, 'interpreted_problem': interpreted,
        'requirement': r'D\subseteq R', 'requires_study_clarification': True,
        'confidence_scope': 'Mathematical validity for the explicitly containing rectangle request; '
                            'the original equality alone can admit other choices by cancellation.',
        'canonical_review': str(review_path), 'review_sha256': proof['review_sha256'],
        'transaction_sha256': proof['transaction_sha256'], 'committed_basis': proof['basis_after'],
        'identity_sha256': hashlib.sha256(json.dumps(identity).encode()).hexdigest()}


def unresolved_study_clarifications(content, state, correction_root):
    """Flag only interpreted imported questions lacking a matching local attestation."""
    def source_identity(problem):
        return re.sub(r'!\[[^\]]*\]\([^)]*/([a-f0-9]{64}\.[a-z]+)\)',
                      lambda m: '![](@asset/'+m[1]+')', problem)
    result = []
    for q in content.get('questions', []):
        mid = q.get('math_academy_id', '')
        record = state.get('questions', {}).get(mid, {})
        meta = q.get('source_feedback_interpretation') or record.get('source_feedback_interpretation')
        expected = {POLICY: (TOPIC, KP), INTEGRAL_POLICY: (INTEGRAL_TOPIC, INTEGRAL_KP),
                    LAPLACE_POLICY: (LAPLACE_TOPIC, LAPLACE_KP)}
        if (not meta or meta.get('policy') not in expected
                or (meta.get('topic_id'), meta.get('knowledge_point_id')) != expected[meta['policy']]
                or not meta.get('requires_study_clarification')):
            continue
        matched = False
        if re.fullmatch(r'q-\d+', mid):
            directory = Path(correction_root)/mid
            try:
                review_bytes = (directory/'review.json').read_bytes()
                transaction = (directory/'transaction.edn').read_bytes()
                review = json.loads(review_bytes)
                proof = json.loads((directory/'verification.json').read_text())
                corrected = review['corrected_content']
                original = review['original_content']
                fields = lambda item: [(f['key'], f['correct_value']) for f in item['answer_fields']]
                matched = (proof.get('committed') is True and proof.get('mathematical_check_passed') is True
                    and isinstance(proof.get('basis_after'), int)
                    and proof.get('review_sha256') == hashlib.sha256(review_bytes).hexdigest()
                    and proof.get('transaction_sha256') == hashlib.sha256(transaction).hexdigest()
                    and corrected.get('math_academy_id') == mid and corrected.get('knowledge_point_id') == meta['knowledge_point_id']
                    and meta['requirement'] in corrected['problem']
                    and source_identity(original['problem']) == source_identity(meta['source_problem'])
                    and fields(corrected) == fields(q))
            except (OSError, ValueError, KeyError, TypeError):
                pass
        if not matched:
            result.append({'question_id': mid, 'reason': 'interpreted_source_requires_study_clarification',
                'requirement': meta.get('requirement'), 'canonical_review': meta.get('canonical_review'),
                'interpretation_identity_sha256': meta.get('identity_sha256')})
    return result


INTEGRAL_TOPIC = 6682
INTEGRAL_KP = 'bbefb3bb-4783-5d77-b404-1f43ee8765de'
INTEGRAL_POLICY = 'q-335252-continuous-partial-theorem-v1'


def reviewed_integral_theorem(item, activity, directory):
    """Exact source question only; the sufficient theorem is explicit in study content."""
    if Path(directory).name != 'q-335252' or activity.get('topic_id') != INTEGRAL_TOPIC:
        return None
    fields = item.get('fields', [])
    if (len(fields) != 1 or fields[0].get('key') != 'selection'
            or fields[0].get('type') != 'radio' or not fields[0].get('choices_complete', True)):
        return None
    correction = ROOT/'reference/mathacademy/mathematical-corrections/q-335252'
    try:
        review_path = correction/'review.json'
        review_bytes = review_path.read_bytes()
        transaction_bytes = (correction/'transaction.edn').read_bytes()
        proof = json.loads((correction/'verification.json').read_text())
        review = json.loads(review_bytes)
        original, corrected = review['original_content'], review['corrected_content']
        original_field, = original['answer_fields']
        corrected_field, = corrected['answer_fields']
        choices = lambda fs: sorted((c['type'], c['value']) for c in fs['choices'])
        if (proof.get('committed') is not True or proof.get('mathematical_check_passed') is not True
                or not isinstance(proof.get('basis_after'), int)
                or proof.get('review_sha256') != hashlib.sha256(review_bytes).hexdigest()
                or proof.get('transaction_sha256') != hashlib.sha256(transaction_bytes).hexdigest()
                or original.get('math_academy_id') != 'q-335252'
                or original.get('knowledge_point_id') != INTEGRAL_KP
                or corrected.get('knowledge_point_id') != INTEGRAL_KP
                or item.get('problem') != original['problem']
                or choices(fields[0]) != choices(original_field)
                or corrected_field != original_field
                or 'continuous-partial-derivative sufficient theorem' not in corrected['problem']
                or 'dominated convergence' not in corrected['worked_solution']
                or original_field.get('correct_value') != 'I and III only'):
            return None
        # A present live KP identity must agree; reviews may have none before grading.
        kp = activity.get('questions', {}).get('q-335252', {}).get('kp_id') or activity.get('current_kp')
        if kp is not None and kp != INTEGRAL_KP:
            return None
    except (OSError, ValueError, KeyError, TypeError):
        return None
    identity = [INTEGRAL_POLICY, proof['review_sha256'], hashlib.sha256(item['problem'].encode()).hexdigest()]
    return {'policy': INTEGRAL_POLICY, 'topic_id': INTEGRAL_TOPIC, 'knowledge_point_id': INTEGRAL_KP,
        'source_problem': item['problem'], 'interpreted_problem': corrected['problem'],
        'requirement': 'continuous-partial-derivative sufficient theorem',
        'requires_study_clarification': True,
        'confidence_scope': 'Applicability of the explicitly stated sufficient theorem only. '
                            'II admits differentiation by dominated convergence; failure of this theorem does not forbid interchange.',
        'canonical_review': str(review_path), 'review_sha256': proof['review_sha256'],
        'transaction_sha256': proof['transaction_sha256'], 'committed_basis': proof['basis_after'],
        'identity_sha256': hashlib.sha256(json.dumps(identity).encode()).hexdigest()}


LAPLACE_TOPIC = 6372
LAPLACE_KP = '4241972f-4023-5638-aa7a-9e4a75167c3d'
LAPLACE_POLICY = 'q-330826-reviewed-convergence-domain-v1'


def reviewed_laplace_domain(item, activity, directory):
    """Use the committed exact-question convergence correction; otherwise solve normally."""
    if Path(directory).name != 'q-330826' or activity.get('topic_id') != LAPLACE_TOPIC:
        return None
    fields = item.get('fields', [])
    if (len(fields) != 1 or fields[0].get('key') != 'selection'
            or fields[0].get('type') != 'radio' or not fields[0].get('choices_complete', True)):
        return None
    correction = ROOT/'reference/mathacademy/mathematical-corrections/q-330826'
    try:
        review_path = correction/'review.json'
        review_bytes = review_path.read_bytes()
        transaction_bytes = (correction/'transaction.edn').read_bytes()
        proof = json.loads((correction/'verification.json').read_text())
        review = json.loads(review_bytes)
        original, corrected = review['original_content'], review['corrected_content']
        original_field, = original['answer_fields']
        corrected_field, = corrected['answer_fields']
        choices = lambda field: sorted((c['type'], c['value']) for c in field['choices'])
        if (proof.get('committed') is not True or proof.get('mathematical_check_passed') is not True
                or not isinstance(proof.get('basis_after'), int)
                or proof.get('review_sha256') != hashlib.sha256(review_bytes).hexdigest()
                or proof.get('transaction_sha256') != hashlib.sha256(transaction_bytes).hexdigest()
                or original.get('math_academy_id') != 'q-330826'
                or corrected.get('math_academy_id') != 'q-330826'
                or original.get('knowledge_point_id') != LAPLACE_KP
                or corrected.get('knowledge_point_id') != LAPLACE_KP
                or item.get('problem') != original['problem']
                or not original['problem'].endswith('for $s>-3.$')
                or corrected['problem'] != original['problem'].replace('for $s>-3.$', 'for $s>0.$')
                or choices(fields[0]) != choices(original_field)
                or corrected_field != original_field
                or original_field.get('correct_value') != r'\frac{1}{s(s+3)}'
                or 'defining Laplace integral diverges' not in corrected['worked_solution']):
            return None
        kp = activity.get('questions', {}).get('q-330826', {}).get('kp_id') or activity.get('current_kp')
        if kp is not None and kp != LAPLACE_KP:
            return None
    except (OSError, ValueError, KeyError, TypeError):
        return None
    identity = [LAPLACE_POLICY, proof['review_sha256'], hashlib.sha256(item['problem'].encode()).hexdigest()]
    return {'policy': LAPLACE_POLICY, 'topic_id': LAPLACE_TOPIC, 'knowledge_point_id': LAPLACE_KP,
        'source_problem': item['problem'], 'interpreted_problem': corrected['problem'],
        'requirement': 'for $s>0.$', 'requires_study_clarification': True,
        'confidence_scope': 'Transform formula on the proven maximal real convergence domain s>0 only. '
                            'The original s>-3 and matching source-solution domain are erroneous; '
                            'the transform diverges for every real s<=0. Preserve the original grade separately.',
        'canonical_review': str(review_path), 'review_sha256': proof['review_sha256'],
        'transaction_sha256': proof['transaction_sha256'], 'committed_basis': proof['basis_after'],
        'identity_sha256': hashlib.sha256(json.dumps(identity).encode()).hexdigest()}
