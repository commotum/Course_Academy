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
        if (not meta or meta.get('policy') != POLICY or meta.get('topic_id') != TOPIC
                or meta.get('knowledge_point_id') != KP or not meta.get('requires_study_clarification')):
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
                    and corrected.get('math_academy_id') == mid and corrected.get('knowledge_point_id') == KP
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
