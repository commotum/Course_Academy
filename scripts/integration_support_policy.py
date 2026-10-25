"""Ordinary integration practice retrieves mastered prerequisite facts."""
import re

def validate_prerequisite_recall(record):
    meta=record.get('generation',{})
    if meta.get('support_policy')!='mastered-prerequisite-recall':
        raise ValueError('Reviewed prerequisite-recall support policy required')
    if meta.get('provided_primitive')is not False or meta.get('provided_endpoint_values')is not False:
        raise ValueError('Blanket primitive/endpoint hints are not part of ordinary practice')
    prompt=record['question'][':question/problem']
    if re.search(r'(?im)^(?:You (?:may|can) use|Endpoint values|Recall(?: that)?)\b',prompt):
        raise ValueError('Blanket primitive/endpoint hints must be in the worked solution')

    if re.search(r'(?i)(?:use|let|take|set|given|with) (?:the substitution )?\$?u\s*=',prompt) or 'Which integral is obtained' in prompt:
        raise ValueError('Ordinary practice must retain recognition of the substitution')
    if meta.get('provided_substitution') is not False or meta.get('operation')!='evaluate':
        raise ValueError('Ordinary practice must assess the complete integral')
