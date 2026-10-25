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
